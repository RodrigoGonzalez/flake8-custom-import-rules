"""Flake8 plugin to check for custom import rules."""
from __future__ import annotations

import ast
import importlib
import pkgutil
from typing import Any
from typing import Generator

from flake8_import_order.checker import DEFAULT_IMPORT_ORDER_STYLE
from flake8_import_order.checker import ImportOrderChecker
from flake8_import_order.checker import ImportVisitor
from flake8_import_order.styles import lookup_entry_point


def get_package_names(name: str) -> list[str]:
    """Return a list of package names for a module name."""
    tree = ast.parse(name)
    parts = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute):
            parts.append(node.attr)
        if isinstance(node, ast.Name):
            parts.append(node.id)

    if not parts:
        return []

    last_package_name = parts.pop()
    package_names = [last_package_name]

    for part in reversed(parts):
        last_package_name = f"{last_package_name}.{part}"
        package_names.append(last_package_name)

    return package_names


def root_package_name(name: str) -> str | None:
    """Return the root package name from a dotted name."""
    tree = ast.parse(name)
    return next(
        (node.id for node in ast.walk(tree) if isinstance(node, ast.Name)),
        None,
    )


def get_submodules(module_name: str) -> list:
    """Return a list of submodules for a module name."""
    module = importlib.import_module(module_name)
    module_path = module.__path__[0]
    submodules = []

    for _, submodule_name, is_pkg in pkgutil.iter_modules([module_path]):
        if is_pkg:
            qualified_name = f"{module_name}.{submodule_name}"
            submodules.append(qualified_name)
            submodules.extend(get_submodules(qualified_name))
        else:
            submodules.append(f"{module_name}.{submodule_name}")

    return submodules


def get_base_module_path(base_module_name: str) -> str:
    """Return the path of a base module."""
    try:
        base_module = importlib.import_module(base_module_name)
        if hasattr(base_module, "__path__"):
            base_module_path = base_module.__path__[0]
            return base_module_path
        else:
            raise ValueError(f"{base_module_name} is not a package")
    except ImportError:
        raise ValueError(f"Failed to import the base module: {base_module_name}")


def _parse_custom_rule(rules: list[str] | None) -> dict:
    """Parse custom rules"""
    parsed_rules: dict = {}
    if rules is None:
        return parsed_rules
    for rule in rules:
        src, dest = rule.split(":")
        parsed_rules[src] = dest.split(",")
    return parsed_rules


class CustomImportRulesVisitor(ImportVisitor):
    """Custom import rules node visitor."""

    errors: list[tuple[int, int, str]] = []
    current_modules: list[str] = []
    package_names: list[list[str]] = []

    def __init__(
        self, application_import_names: list[str] | str, application_package_names: list[str] | str
    ) -> None:
        super().__init__(application_import_names, application_package_names)

    def visit_Import(self, node: ast.Import) -> None:
        """Visit an Import node."""
        super().visit_Import(node)

        # if node.col_offset == 0:
        #     modules = [alias.name for alias in node.names]
        #     current_modules = [root_package_name(module) for module in modules]
        #     self.current_modules.extend(current_modules)
        #     package_names = [get_package_names(module) for module in modules]
        #     self.package_names.extend(package_names)

        # Ensures a complete traversal of the AST
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Visit an ImportFrom node."""
        super().visit_ImportFrom(node)

        # if node.col_offset == 0:
        #     module = node.module or ''
        #     current_module = root_package_name(module)
        #     self.current_modules.append(current_module)
        #     package_names = get_package_names(current_module)
        #     self.package_names.extend([package_names])
        # Ensures a complete traversal of the AST
        self.generic_visit(node)


class CustomImportRulesCheckerPlugin(ImportOrderChecker):
    """Plugin for checking custom import rules."""

    visitor_class = CustomImportRulesVisitor

    def __init__(self, filename: str | None, tree: ast.AST | None) -> None:
        super().__init__(filename, tree)
        # if filename in ("stdin", "-", None):
        #     filename = "stdin"
        #     lines = pycodestyle.stdin_get_value().splitlines(True)
        # else:
        #     lines = pycodestyle.readlines(filename)
        self._filename = filename
        self._tree = tree
        # self._lines = lines

    @property
    def filename(self) -> str:
        """Return the filename."""
        if not self._filename:
            raise RuntimeError("Filename is not set")
        return self._filename

    @property
    def tree(self) -> ast.AST:
        """Return the tree."""
        if not self._tree:
            raise RuntimeError("Tree is not set")
        return self._tree

    # @property
    # def lines(self) -> list[str]:
    #     """Return the lines."""
    #     return self._lines

    def get_visitor(self) -> CustomImportRulesVisitor:
        """Return the visitor to use for this plugin."""
        try:
            style_entry_point = self.options["import_order_style"]
        except KeyError:
            style_entry_point = lookup_entry_point(DEFAULT_IMPORT_ORDER_STYLE)
        style_cls = style_entry_point.load()
        return (
            self.visitor_class(
                self.options.get("application_import_names", []),
                self.options.get("application_package_names", []),
            )
            if style_cls.accepts_application_package_names
            else self.visitor_class(
                self.options.get("application_import_names", []),
                [],
            )
        )

    def run(self) -> Generator[tuple[int, int, str, type[Any]], None, None]:
        """Run the plugin."""
        if not self.tree or not self.lines:
            self.load_file()

        visitor = self.get_visitor()
        visitor.visit(self.tree)

        for line, col, msg in visitor.errors:
            yield line, col, msg, type(self)
