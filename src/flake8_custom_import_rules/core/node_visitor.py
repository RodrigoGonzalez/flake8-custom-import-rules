"""Custom import rules node visitor."""
import ast
import logging
from collections import defaultdict
from pathlib import Path

from attrs import define
from attrs import field
from flake8_import_order.stdlib_list import STDLIB_NAMES

from flake8_custom_import_rules.core.nodes import ImportType
from flake8_custom_import_rules.core.nodes import ParsedCall
from flake8_custom_import_rules.core.nodes import ParsedClassDef
from flake8_custom_import_rules.core.nodes import ParsedDynamicImport
from flake8_custom_import_rules.core.nodes import ParsedFromImport
from flake8_custom_import_rules.core.nodes import ParsedFunctionDef
from flake8_custom_import_rules.core.nodes import ParsedIfImport
from flake8_custom_import_rules.core.nodes import ParsedImport
from flake8_custom_import_rules.core.nodes import ParsedLocalImport
from flake8_custom_import_rules.utils.node_utils import generate_identifier_path
from flake8_custom_import_rules.utils.node_utils import get_module_info_from_import_node
from flake8_custom_import_rules.utils.node_utils import get_name_info_from_import_node
from flake8_custom_import_rules.utils.parse_utils import check_string

logger = logging.getLogger(f"flake8_custom_import_rules.{__name__}")


POTENTIAL_DYNAMIC_IMPORTS = {
    "__import__",
    "importlib",
    "importlib.import_module",
    "import_module",
    "pkgutil",
    "pkgutil.get_loader",
    "pkgutil.iter_modules",
    "sys.modules",
    "modules",
    "zipimport",
    "zipimport.zipimporter",
    "zipimporter",
    "zipimporter.load_module",
    "eval",
    "exec",
}


@define(slots=True)
class CustomImportRulesVisitor(ast.NodeVisitor):
    """Custom import rules node visitor."""

    package_names: list[str] = field(factory=list)
    filename: str | None = None
    nodes: list = field(factory=list)
    current_package: list[str] = field(factory=list)
    file_path: Path | None = None
    resolve_local_imports: bool | None = field(default=False)
    names: dict = field(factory=dict, init=False)
    assigns: dict = field(factory=dict, init=False)
    attributes: dict = field(factory=dict, init=False)
    identifiers: defaultdict[str, dict] = defaultdict(lambda: defaultdict(str))
    identifiers_by_lineno: defaultdict[str, list] = defaultdict(list)

    def __attrs_post_init__(self) -> None:
        filename = self.filename
        self.file_path = Path(filename) if filename else None
        logger.info(f"Visitor filename: {self.filename}")
        self.resolve_local_imports = filename not in {"stdin", "-", "/dev/stdin", "", None}
        logger.info(f"Resolve local imports: {self.resolve_local_imports}")

    def _resolve_local_import(self, module: str, node_level: int) -> Path | None:
        """Resolve a local import."""
        parent = self.file_path.parents[node_level - 1] if self.file_path else None
        return parent / f"{module}.py" if parent else None

    @staticmethod
    def _get_import_node(module_info: dict) -> ParsedImport:
        """Get a parsed import node."""
        return ParsedImport(
            import_type=module_info["import_type"],
            module=module_info["module"],
            asname=module_info["asname"],
            lineno=module_info["lineno"],
            col_offset=module_info["col_offset"],
            node_col_offset=module_info["node_col_offset"],
            alias_col_offset=module_info["alias_col_offset"],
            package=module_info["package"],
            package_names=module_info["package_names"],
            private_identifier_import=module_info["private_identifier_import"],
            private_module_import=module_info["private_module_import"],
            import_node=module_info["import_node"],
        )

    def visit_Import(self, node: ast.Import) -> None:
        """Visit an Import node."""
        parsed_imports_dict = get_module_info_from_import_node(node)

        # pprint.pprint("\nParsed import dict:")
        # pprint.pprint(parsed_imports_dict)

        for alias in node.names:
            module_info = parsed_imports_dict[alias.name]
            module_info["import_type"] = self._classify_type(module_info["package_names"])
            parsed_import = self._get_import_node(module_info)

            self.nodes.append(parsed_import)
            self.identifiers_by_lineno[str(node.lineno)].append(module_info)
            self.identifiers[parsed_import.identifier].update(module_info)
            self.identifiers[alias.name].update(module_info)

        # Ensures a complete traversal of the AST
        self.generic_visit(node)

    def _get_import_type(self, node_level: int, package_names: list[str]) -> ImportType:
        """Get the import type for a module."""
        return ImportType.RELATIVE if node_level > 0 else self._classify_type(package_names)

    @staticmethod
    def _get_from_import_node(name_info: dict) -> ParsedFromImport:
        """Get a parsed from import node."""
        return ParsedFromImport(
            import_type=name_info["import_type"],
            module=name_info["module"],
            name=name_info["name"],
            asname=name_info["asname"],
            lineno=name_info["lineno"],
            col_offset=name_info["col_offset"],
            node_col_offset=name_info["node_col_offset"],
            alias_col_offset=name_info["alias_col_offset"],
            level=name_info["level"],
            package=name_info["package"],
            package_names=name_info["package_names"],
            private_identifier_import=name_info["private_identifier_import"],
            private_module_import=name_info["private_module_import"],
            import_node=name_info["import_node"],
        )

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Visit an Import node."""
        parsed_from_imports_dict = get_name_info_from_import_node(node)

        # pprint.pprint("\nParsed from import dict:")
        # pprint.pprint(parsed_from_imports_dict)

        for alias in node.names:
            name_info = parsed_from_imports_dict[alias.name]
            name_info["import_type"] = self._get_import_type(
                name_info["level"], name_info["package_names"]
            )
            parsed_from_import = self._get_from_import_node(name_info)

            self.nodes.append(parsed_from_import)
            self.identifiers_by_lineno[str(node.lineno)].append(name_info)
            self.identifiers[parsed_from_import.identifier].update(name_info)
            self.identifiers[alias.name].update(name_info)

        # Ensures a complete traversal of the AST
        self.generic_visit(node)

    def _check_local_import(
        self, node: ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef
    ) -> None:
        """Check if a local import is resolved."""
        for stmt in node.body:
            if isinstance(stmt, (ast.Import, ast.ImportFrom)):
                self.nodes.append(
                    ParsedLocalImport(
                        lineno=stmt.lineno,
                        col_offset=stmt.col_offset,
                        local_node_type=str(type(node)),
                        import_node=ast.unparse(stmt),
                    )
                )

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Visit a ClassDef node."""
        self.nodes.append(
            ParsedClassDef(
                name=node.name,
                lineno=node.lineno,
                col_offset=node.col_offset,
            )
        )
        self._check_local_import(node)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visit a FunctionDef node."""
        self.nodes.append(
            ParsedFunctionDef(
                name=node.name,
                lineno=node.lineno,
                col_offset=node.col_offset,
            )
        )
        self._check_local_import(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """Visit a AsyncFunctionDef node."""
        self.nodes.append(
            ParsedFunctionDef(
                name=node.name,
                lineno=node.lineno,
                col_offset=node.col_offset,
            )
        )
        self._check_local_import(node)
        self.generic_visit(node)

    @staticmethod
    def _func_name(func: ast.Name) -> str:
        """Get the function name."""
        return func.id

    @staticmethod
    def _func_attribute(func: ast.Attribute) -> str:
        """Get the function name."""
        return func.attr

    @staticmethod
    def _get_args_for_calls(args: list) -> list[str]:
        """Get the function args."""
        return [arg.value for arg in args if hasattr(arg, "value")]

    def visit_Call(self, node: ast.Call) -> None:
        """Visit a Call node."""
        if isinstance(node.func, ast.Name):
            # print(f"visit_Call: {node.func}")
            if self._func_name(node.func) in POTENTIAL_DYNAMIC_IMPORTS:
                self.nodes.append(
                    ParsedCall(
                        func=self._func_name(node.func),
                        lineno=node.lineno,
                        col_offset=node.col_offset,
                        call_type="ast.Name",
                        values=self._get_args_for_calls(node.args),
                        call=ast.unparse(node),
                    )
                )
        elif isinstance(node.func, ast.Attribute):
            # print(f"visit_Call: {node.func}")
            if self._func_attribute(node.func) in POTENTIAL_DYNAMIC_IMPORTS:
                self.nodes.append(
                    ParsedCall(
                        func=self._func_attribute(node.func),
                        module=node.func.value.id if hasattr(node.func.value, "id") else None,
                        lineno=node.lineno,
                        col_offset=node.col_offset,
                        call_type="ast.Attribute",
                        values=self._get_args_for_calls(node.args),
                        call=ast.unparse(node),
                    )
                )
        self.generic_visit(node)

    def visit_If(self, node: ast.If) -> None:
        """Visit an If node."""
        other_nodes = node.body + node.orelse
        if conditional_imports := (
            (sub_node.lineno, sub_node.col_offset, sub_node)
            for sub_node in other_nodes
            if isinstance(sub_node, (ast.Import, ast.ImportFrom))
        ):
            for lineno, col_offset, sub_node in conditional_imports:
                self.nodes.append(
                    ParsedIfImport(
                        lineno=lineno,
                        col_offset=col_offset,
                        sub_node=ast.unparse(sub_node),
                    )
                )
        self.generic_visit(node)

    @staticmethod
    def _check_for_dynamic_imports(strings_to_check: list[str]) -> bool:
        """Check for dynamic imports."""
        return check_string(
            strings_to_check=strings_to_check,
            substring_match=list(POTENTIAL_DYNAMIC_IMPORTS),
        )

    def visit_Assign(self, node: ast.Assign) -> None:
        """Visit an Assign node."""
        identifier_path = list(generate_identifier_path(node.value))

        if self._check_for_dynamic_imports(identifier_path):
            if check_string(identifier_path, substring_match="modules"):
                # "modules" is a common object name, so we need to check
                # that it was imported from the "sys" package.
                self.nodes.append(
                    ParsedDynamicImport(
                        lineno=node.lineno,
                        col_offset=node.col_offset,
                        dynamic_import=ast.unparse(node),
                        identifier=".".join(identifier_path),
                    )
                )
            else:
                self.nodes.append(
                    ParsedDynamicImport(
                        lineno=node.lineno,
                        col_offset=node.col_offset,
                        dynamic_import=ast.unparse(node),
                        identifier=".".join(identifier_path),
                        confirmed=True,
                    )
                )

        self.generic_visit(node)

    def _classify_type(self, package_names: list[str]) -> ImportType:
        """
        Classify the import type.

        Parameters
        ----------
        module : str
            Module name

        Returns
        -------
        ImportType
        """

        # Walk through package names from most-specific to least-specific,
        # taking the first match found.
        for package in reversed(package_names):
            if package == "__future__":
                return ImportType.FUTURE
            elif package in self.current_package:
                return ImportType.FIRST_PARTY
            elif package in STDLIB_NAMES:
                return ImportType.STDLIB

        # Not future, stdlib or an application import.
        # Must be 3rd party.
        return ImportType.THIRD_PARTY
