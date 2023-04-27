from __future__ import annotations

from typing import Any
from typing import Generator
from typing import NamedTuple

from flake8_import_order import ImportType
from stdlib_list import stdlib_list

from flake8_custom_import_rules.node_visitor import ParsedNode
from flake8_custom_import_rules.parse_utils import parse_custom_rule


class ErrorMessage(NamedTuple):
    lineno: int
    col_offset: int
    message: str
    type: str


class CustomImportRules:
    """Custom Import Rules for Flake8 & Python Projects"""

    def __init__(self, nodes: list[ParsedNode], options: dict[str, list[str] | str]) -> None:
        self.nodes = sorted(
            nodes,
            key=lambda element: element.lineno,
        )
        self.options = options

        # Store the Python version for checking the standard library
        self.use_python_version = options.get("use_python_version", 3)

        self.restricted_imports = parse_custom_rule(
            options.get("restricted_imports", []),
        )
        self.isolated_modules = options.get(
            "isolated_modules",
            [],
        )
        self.standard_library_only = options.get(
            "standard_library_only",
            [],
        )
        self.check_top_level_only = options.get(
            "check_top_level_only",
            False,
        )
        self.prohibit_relative_imports = options.get(
            "prohibit_relative_imports",
            False,
        )
        self.prohibit_conditional_imports = options.get(
            "prohibit_conditional_imports",
            False,
        )
        self.prohibit_local_imports = options.get(
            "prohibit_local_imports",
            False,
        )
        self.prohibit_functional_imports = options.get(
            "prohibit_functional_imports",
            False,
        )
        self.prohibit_dynamic_imports = options.get(
            "prohibit_dynamic_imports",
            False,
        )
        self.prohibit_aliased_imports = options.get(
            "prohibit_aliased_imports",
            False,
        )
        self.prohibit_imports_from_init = options.get(
            "prohibit_imports_from_init",
            False,
        )
        self.prohibit_imports_from_tests = options.get(
            "prohibit_imports_from_tests",
            False,
        )
        self.prohibit_imports_from_conftest = options.get(
            "prohibit_imports_from_conftest",
            False,
        )

    # def check_import_rules(self) -> Generator[tuple[int, int, str], Any, None]:
    #     """Check imports"""
    # for node in self.nodes:
    #     if self.check_top_level_only and node.level != 0:
    #         break
    #     yield self._check_import_rules(node)

    # def _check_import_rules(self, node):
    # current_module = os.path.split(self.filename)[-1].split('.')[0]
    # is_from_import = isinstance(node, ast.ImportFrom)
    # code_offset = 1 if is_from_import else 0
    #
    # # Adjust the message based on the import type
    # import_type = 'from ... import' if is_from_import else 'import'
    #
    # for alias in node.names:
    #     module_name = alias.name.split('.')[0]
    #
    #     if is_from_import and isinstance(node, ast.ImportFrom):
    #         module_name = node.module.split('.')[0]
    #
    #     # Check restricted imports
    #     self._check_restricted_imports(
    #         code_offset, current_module, import_type, module_name, node
    #     )
    #
    #     # Check isolated imports
    #     self._check_isolated_imports(
    #         code_offset, current_module, import_type, module_name, node
    #     )
    #
    #     # Check standard library only imports
    #     self._check_std_lib_only_imports(
    #         code_offset, current_module, import_type, module_name, node
    #     )
    # _ = node
    # yield 1, 1, "CIM100", "Custom Import Rules"

    def _check_restricted_imports(
        self,
        code_offset: int,
        current_module: str,
        import_type: ImportType,
        module_name: str,
        node: ParsedNode,
    ) -> Generator[tuple[int, int, str, type], Any, Any] | None:
        """Check restricted imports"""
        if (
            current_module in self.restricted_imports
            and module_name in self.restricted_imports[current_module]
        ):
            yield self.error(
                f"CIM{101 + code_offset}",
                node.lineno,
                node.col_offset,
                (
                    f"Using '{import_type}' in module '{current_module}' "
                    f"is not allowed to import '{module_name}'."
                ),
            )

    def _check_isolated_imports(
        self,
        code_offset: int,
        current_module: str,
        import_type: ImportType,
        module_name: str,
        node: ParsedNode,
    ) -> Generator[tuple[int, int, str, type], Any, Any] | None:
        """Check isolated imports"""
        if current_module in self.isolated_modules and any(
            module_name.startswith(prefix) for prefix in self.isolated_modules
        ):
            yield self.error(
                f"CIM{201 + code_offset}",
                node.lineno,
                node.col_offset,
                (
                    f"Using '{import_type}' in module '{current_module}' "
                    f"cannot import from other modules within the base module."
                ),
            )

    def _check_std_lib_only_imports(
        self,
        code_offset: int,
        current_module: str,
        import_type: ImportType,
        module_name: str,
        node: ParsedNode,
    ) -> Generator[tuple[int, int, str, type], Any, Any] | None:
        """Check standard library only imports"""
        if current_module in self.standard_library_only and not self._is_standard_library_import(
            module_name
        ):
            yield self.error(
                f"CIM{301 + code_offset}",
                node.lineno,
                node.col_offset,
                (
                    f"Using '{import_type}' in module '{current_module}' "
                    f"can only import from the Python standard library, "
                    f"'{module_name}' is not allowed."
                ),
            )

    def error(
        self, code: str, lineno: int, col_offset: int, message: str
    ) -> tuple[int, int, str, type]:
        """Report errors."""
        return (lineno, col_offset, f"{code} {message}", type(self))
        # self.error(*error)

    def _is_standard_library_import(self, module_name: str) -> bool:
        """Check module is standard library module using specific Python version."""
        standard_lib_modules = stdlib_list(self.use_python_version)
        return module_name in standard_lib_modules
