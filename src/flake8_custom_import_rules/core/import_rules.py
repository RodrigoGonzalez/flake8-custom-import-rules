""" Custom Import Rules for Flake8 & Python Projects. """
from typing import Any
from typing import Generator

from attrs import define
from attrs import field
from stdlib_list import stdlib_list

from flake8_custom_import_rules.codes.error_codes import ErrorCode
from flake8_custom_import_rules.core.node_visitor import ParsedFromImport
from flake8_custom_import_rules.core.node_visitor import ParsedImport
from flake8_custom_import_rules.core.node_visitor import ParsedNode
from flake8_custom_import_rules.defaults import Settings
from flake8_custom_import_rules.utils.parse_utils import parse_custom_rule


@define(slots=True)
class ErrorMessage:
    """Error message"""

    lineno: int
    col_offset: int
    code: str
    message: str
    custom_explanation: str | None = None

    def __attrs_post_init__(self) -> None:
        """Post init."""
        self.custom_explanation = self.custom_explanation or ""
        self.message = f"{self.message} {self.custom_explanation}".strip()


def generate_from_node(node: ParsedNode, error_code: ErrorCode) -> ErrorMessage:
    """Generate error message from node."""
    return ErrorMessage(
        lineno=node.lineno,
        col_offset=node.col_offset,
        code=error_code.code,
        message=error_code.message,
    )


@define(slots=True)
class CustomImportRules:
    """Custom Import Rules for Flake8 & Python Projects"""

    nodes: list[ParsedNode] = field(factory=list)
    options: dict = field(factory=dict)
    checker_settings: Settings = field(factory=Settings)
    errors: list[ErrorMessage] = field(factory=list)
    codes_to_check: list[ErrorCode] = ErrorCode.get_all_error_codes()

    use_python_version: float | int | str | None = field(default=3.9)

    filename: str = field(default=None)
    restricted_imports: dict = field(factory=dict)
    isolated_modules: list[str] = field(factory=list)
    foundation_modules: list[str] = field(factory=list)
    standard_library_only: list[str] = field(factory=list)
    check_top_level_only: bool = field(default=False)

    def __attrs_post_init__(self) -> None:
        self.nodes = sorted(
            self.nodes,
            key=lambda element: element.lineno,
        )
        options = self.options

        # Store the Python version for checking the standard library
        self.use_python_version = str(options.get("use_python_version", 3.9))

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

    def check_import_rules(self) -> Generator[ErrorMessage, None, None]:
        """Check imports"""
        for node in self.nodes:
            if self.check_top_level_only and node.level != 0:
                break
            yield from self._check_import_rules(node)

    # TODO: Make sure to remove the type ignore when I figure out how to fix it
    def _check_import_rules(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check import rules"""
        # current_module = os.path.split(self.filename)[-1].split(".")[0]
        # is_from_import = isinstance(node, ast.ImportFrom)
        # code_offset = 1 if is_from_import else 0
        #
        # # Adjust the message based on the import type
        # import_string = "from ... import" if is_from_import else "import"
        #
        # for alias in node.names:
        #     module_name = alias.name.split(".")[0]
        #
        #     if is_from_import and isinstance(node, ast.ImportFrom):
        #         # TODO: Remove this ignore when I figure out how to fix it
        #         module_name = node.module.split(".")[0]  # type: ignore
        #
        #     # Check restricted imports
        #     self._check_restricted_imports(
        #         code_offset, current_module, import_string, module_name, node
        #     )
        #
        #     # Check isolated imports
        #     self._check_isolated_imports(
        #         code_offset, current_module, import_string, module_name, node
        #     )
        #
        #     # Check standard library only imports
        #     self._check_std_lib_only_imports(
        #         code_offset, current_module, import_string, module_name, node
        #     )
        # _ = node
        # for node in self.nodes:
        #     if self.check_top_level_only and node.level != 0:
        #         break
        yield from self._check_project_level_restrictions(node)

    def _check_project_level_restrictions(
        self, node: ParsedNode
    ) -> Generator[ErrorMessage, None, None]:
        """Check project level restrictions"""
        yield from self._check_standard_import_restrictions(node)
        yield from self._check_special_cases_import_restrictions(node)

    def _check_standard_import_restrictions(
        self, node: ParsedNode
    ) -> Generator[ErrorMessage, None, None]:
        """Check standard import restrictions"""
        # if self.checker_settings.TOP_LEVEL_ONLY and (
        #     isinstance(node, (ParsedImport, ParsedFromImport))
        # ):
        #     yield from self._check_for_pir101(node)

        if self.checker_settings.RESTRICT_RELATIVE_IMPORTS and (isinstance(node, ParsedFromImport)):
            yield from self._check_for_pir102(node)

        # if self.checker_settings.RESTRICT_LOCAL_IMPORTS and (
        #     isinstance(node, (ParsedImport, ParsedFromImport))
        # ):
        #     yield from self._check_for_pir103(node)
        #
        # if self.checker_settings.RESTRICT_CONDITIONAL_IMPORTS and (
        #     isinstance(node, ParsedIfImport)
        # ):
        #     yield from self._check_for_pir104(node)
        #
        # if self.checker_settings.RESTRICT_DYNAMIC_IMPORTS and (
        #     isinstance(node, (ParsedImport, ParsedFromImport))
        # ):
        #     yield from self._check_for_pir105(node)
        #
        # if self.checker_settings.RESTRICT_PRIVATE_IMPORTS and (
        #     isinstance(node, (ParsedImport, ParsedFromImport))
        # ):
        #     yield from self._check_for_pir106(node)

        if self.checker_settings.RESTRICT_WILDCARD_IMPORTS and (
            isinstance(node, (ParsedImport, ParsedFromImport))
        ):
            yield from self._check_for_pir107(node)

    def _check_special_cases_import_restrictions(
        self, node: ParsedNode
    ) -> Generator[ErrorMessage, None, None]:
        """Check special cases import restrictions"""
        if self.checker_settings.RESTRICT_INIT_IMPORTS:
            if isinstance(node, ParsedImport):
                yield from self._check_for_pir207(node)
            elif isinstance(node, ParsedFromImport):
                yield from self._check_for_pir208(node)

    def _check_restricted_imports(
        self,
        code_offset: int,
        current_module: str,
        import_string: str,
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
                    f"Using '{import_string}' in module '{current_module}' "
                    f"is not allowed to import '{module_name}'."
                ),
            )

    def _check_isolated_imports(
        self,
        code_offset: int,
        current_module: str,
        import_string: str,
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
                    f"Using '{import_string}' in module '{current_module}' "
                    f"cannot import from other modules within the base module."
                ),
            )

    def _check_std_lib_only_imports(
        self,
        code_offset: int,
        current_module: str,
        import_string: str,
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
                    f"Using '{import_string}' in module '{current_module}' "
                    f"can only import from the Python standard library, "
                    f"'{module_name}' is not allowed."
                ),
            )

    def error(
        self, code: str, lineno: int, col_offset: int, message: str
    ) -> tuple[int, int, str, type]:
        """Report errors."""
        return lineno, col_offset, f"{code} {message}", type(self)
        # self.error(*error)

    def _is_standard_library_import(self, module_name: str) -> bool:
        """Check module is standard library module using specific Python version."""
        standard_lib_modules = stdlib_list(self.use_python_version)
        return module_name in standard_lib_modules

    def _check_for_cir101(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for CIR101."""
        if ErrorCode.CIR101.code in self.codes_to_check:
            yield generate_from_node(node, ErrorCode.CIR101)

    def _check_for_cir102(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for CIR102."""
        if ErrorCode.CIR102.code in self.codes_to_check:
            yield generate_from_node(node, ErrorCode.CIR102)

    def _check_for_cir103(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for CIR103."""
        if ErrorCode.CIR103.code in self.codes_to_check:
            yield generate_from_node(node, ErrorCode.CIR103)

    def _check_for_cir104(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for CIR104."""
        if ErrorCode.CIR104.code in self.codes_to_check:
            yield generate_from_node(node, ErrorCode.CIR104)

    def _check_for_cir105(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for CIR105."""
        if ErrorCode.CIR105.code in self.codes_to_check:
            yield generate_from_node(node, ErrorCode.CIR105)

    def _check_for_cir106(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for CIR106."""
        if ErrorCode.CIR106.code in self.codes_to_check:
            yield generate_from_node(node, ErrorCode.CIR106)

    def _check_for_cir107(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for CIR107."""
        if ErrorCode.CIR107.code in self.codes_to_check:
            yield generate_from_node(node, ErrorCode.CIR107)

    def _check_for_cir201(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for CIR201."""
        if ErrorCode.CIR201.code in self.codes_to_check:
            yield generate_from_node(node, ErrorCode.CIR201)

    def _check_for_cir202(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for CIR202."""
        if ErrorCode.CIR202.code in self.codes_to_check:
            yield generate_from_node(node, ErrorCode.CIR202)

    def _check_for_cir203(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for CIR203."""
        if ErrorCode.CIR203.code in self.codes_to_check:
            yield generate_from_node(node, ErrorCode.CIR203)

    def _check_for_cir204(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for CIR204."""
        if ErrorCode.CIR204.code in self.codes_to_check:
            yield generate_from_node(node, ErrorCode.CIR204)

    def _check_for_cir301(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for CIR301."""
        if ErrorCode.CIR301.code in self.codes_to_check:
            yield generate_from_node(node, ErrorCode.CIR301)

    def _check_for_cir302(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for CIR302."""
        if ErrorCode.CIR302.code in self.codes_to_check:
            yield generate_from_node(node, ErrorCode.CIR302)

    def _check_for_cir303(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for CIR303."""
        if ErrorCode.CIR303.code in self.codes_to_check:
            yield generate_from_node(node, ErrorCode.CIR303)

    def _check_for_cir304(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for CIR304."""
        if ErrorCode.CIR304.code in self.codes_to_check:
            yield generate_from_node(node, ErrorCode.CIR304)

    def _check_for_cir401(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for CIR401."""
        if ErrorCode.CIR401.code in self.codes_to_check:
            yield generate_from_node(node, ErrorCode.CIR401)

    def _check_for_cir402(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for CIR402."""
        if ErrorCode.CIR402.code in self.codes_to_check:
            yield generate_from_node(node, ErrorCode.CIR402)

    def _check_for_cir403(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for CIR403."""
        if ErrorCode.CIR403.code in self.codes_to_check:
            yield generate_from_node(node, ErrorCode.CIR403)

    def _check_for_cir404(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for CIR404."""
        if ErrorCode.CIR404.code in self.codes_to_check:
            yield generate_from_node(node, ErrorCode.CIR404)

    def _check_for_cir501(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for CIR501."""
        if ErrorCode.CIR501.code in self.codes_to_check:
            yield generate_from_node(node, ErrorCode.CIR501)

    def _check_for_cir502(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for CIR502."""
        if ErrorCode.CIR502.code in self.codes_to_check:
            yield generate_from_node(node, ErrorCode.CIR502)

    def _check_for_pir101(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for PIR101, only top level imports are permitted."""
        if ErrorCode.PIR101.code in self.codes_to_check:
            yield generate_from_node(node, ErrorCode.PIR101)

    def _check_for_pir102(self, node: ParsedFromImport) -> Generator[ErrorMessage, None, None]:
        """Check for PIR102, relative import restrictions."""
        condition = node.level > 0
        if ErrorCode.PIR102.code in self.codes_to_check and condition:
            yield generate_from_node(node, ErrorCode.PIR102)

    def _check_for_pir103(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for PIR103, local import restrictions."""
        if ErrorCode.PIR103.code in self.codes_to_check:
            yield generate_from_node(node, ErrorCode.PIR103)

    def _check_for_pir104(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for PIR104, conditional import restrictions."""
        if ErrorCode.PIR104.code in self.codes_to_check:
            yield generate_from_node(node, ErrorCode.PIR104)

    def _check_for_pir105(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for PIR105, dynamic import restrictions."""
        if ErrorCode.PIR105.code in self.codes_to_check:
            yield generate_from_node(node, ErrorCode.PIR105)

    def _check_for_pir106(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for PIR106, functional import restrictions."""
        if ErrorCode.PIR106.code in self.codes_to_check:
            yield generate_from_node(node, ErrorCode.PIR106)

    def _check_for_pir107(
        self, node: ParsedFromImport | ParsedImport
    ) -> Generator[ErrorMessage, None, None]:
        """Check for PIR107, wildcard or star import restrictions (i.e., from * imports)."""
        condition = "*" in node.module or "*" in node.name if hasattr(node, "name") else False
        if ErrorCode.PIR107.code in self.codes_to_check and condition:
            yield generate_from_node(node, ErrorCode.PIR107)

    def _check_for_pir108(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for PIR108, aliased import restrictions."""
        if ErrorCode.PIR108.code in self.codes_to_check:
            yield generate_from_node(node, ErrorCode.PIR108)

    def _check_for_pir201(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for PIR201."""
        if ErrorCode.PIR201.code in self.codes_to_check:
            yield generate_from_node(node, ErrorCode.PIR201)

    def _check_for_pir202(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for PIR202."""
        if ErrorCode.PIR202.code in self.codes_to_check:
            yield generate_from_node(node, ErrorCode.PIR202)

    def _check_for_pir203(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for PIR203."""
        if ErrorCode.PIR203.code in self.codes_to_check:
            yield generate_from_node(node, ErrorCode.PIR203)

    def _check_for_pir204(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for PIR204."""
        if ErrorCode.PIR204.code in self.codes_to_check:
            yield generate_from_node(node, ErrorCode.PIR204)

    def _check_for_pir205(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for PIR205."""
        if ErrorCode.PIR205.code in self.codes_to_check:
            yield generate_from_node(node, ErrorCode.PIR205)

    def _check_for_pir206(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for PIR206."""
        if ErrorCode.PIR206.code in self.codes_to_check:
            yield generate_from_node(node, ErrorCode.PIR206)

    def _check_for_pir207(self, node: ParsedImport) -> Generator[ErrorMessage, None, None]:
        """Check for PIR207, import __init__."""
        condition = "__init__" in node.module
        if ErrorCode.PIR207.code in self.codes_to_check and condition:
            yield generate_from_node(node, ErrorCode.PIR207)

    def _check_for_pir208(self, node: ParsedFromImport) -> Generator[ErrorMessage, None, None]:
        """Check for PIR208, from __init__ imports."""
        condition = "__init__" in node.module or "__init__" in node.name
        if ErrorCode.PIR208.code in self.codes_to_check and condition:
            yield generate_from_node(node, ErrorCode.PIR208)
