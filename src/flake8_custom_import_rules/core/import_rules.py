""" Custom Import Rules for Flake8 & Python Projects. """
import logging
from collections import defaultdict
from typing import Any
from typing import Generator

from attrs import define
from attrs import field

from flake8_custom_import_rules.codes.error_codes import ErrorCode
from flake8_custom_import_rules.core.error_messages import ErrorMessage
from flake8_custom_import_rules.core.error_messages import standard_error_message
from flake8_custom_import_rules.core.error_messages import std_lib_only_error
from flake8_custom_import_rules.core.nodes import DynamicStringFromImport
from flake8_custom_import_rules.core.nodes import DynamicStringImport
from flake8_custom_import_rules.core.nodes import ImportType
from flake8_custom_import_rules.core.nodes import ParsedDynamicImport
from flake8_custom_import_rules.core.nodes import ParsedFromImport
from flake8_custom_import_rules.core.nodes import ParsedIfImport
from flake8_custom_import_rules.core.nodes import ParsedImport
from flake8_custom_import_rules.core.nodes import ParsedLocalImport
from flake8_custom_import_rules.core.nodes import ParsedNode
from flake8_custom_import_rules.defaults import Settings
from flake8_custom_import_rules.utils.parse_utils import check_string
from flake8_custom_import_rules.utils.parse_utils import does_file_match_custom_rule
from flake8_custom_import_rules.utils.parse_utils import parse_custom_rule

logger = logging.getLogger(f"flake8_custom_import_rules.{__name__}")


@define(slots=True)
class CustomImportRules:
    """Custom Import Rules for Flake8 & Python Projects"""

    nodes: list[ParsedNode] = field(factory=list)
    dynamic_nodes: defaultdict[str, list] = defaultdict(list)
    options: dict = field(factory=dict)
    identifiers: defaultdict[str, dict] = defaultdict(lambda: defaultdict(str))
    identifiers_by_lineno: defaultdict[str, list] = defaultdict(list)
    checker_settings: Settings = field(factory=Settings)
    errors: list[ErrorMessage] = field(factory=list)
    codes_to_check: list[ErrorCode] = ErrorCode.get_all_error_codes()

    filename: str = field(default=None)
    file_identifier: str = field(default=None)
    check_custom_import_rules: bool = field(default=False)
    std_lib_only: bool = field(default=False)

    import_restrictions: dict = field(factory=dict)
    isolated_modules: list[str] = field(factory=list)
    foundation_modules: list[str] = field(factory=list)

    check_top_level_only: bool = field(default=False)

    def __attrs_post_init__(self) -> None:
        """Post init."""
        self.nodes = sorted(
            self.nodes,
            key=lambda element: element.lineno,
        )
        self.check_custom_import_rules = (
            self.filename not in self.checker_settings.stdin_identifiers
        )
        options = self.options

        self.import_restrictions = parse_custom_rule(
            options.get("import_restrictions", []),
        )
        self.isolated_modules = options.get(
            "isolated_modules",
            [],
        )
        self.std_lib_only = does_file_match_custom_rule(
            self.file_identifier,
            self.checker_settings.STD_LIB_ONLY,
        )
        logging.debug(f"STD LIB ONLY: {self.std_lib_only}")

    def check_import_rules(self) -> Generator[ErrorMessage, None, None]:
        """Check imports"""
        for node in self.nodes:
            yield from self._check_import_rules(node)

    def _check_import_rules(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check import rules"""
        # file_identifier = os.path.split(self.filename)[-1].split(".")[0]
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
        #         code_offset, file_identifier, import_string, module_name, node
        #     )
        #
        #     # Check isolated imports
        #     self._check_isolated_imports(
        #         code_offset, file_identifier, import_string, module_name, node
        #     )
        #
        #     # Check standard library only imports
        #     self._check_std_lib_only_imports(
        #         code_offset, file_identifier, import_string, module_name, node
        #     )
        # _ = node
        # for node in self.nodes:
        #     if self.check_top_level_only and node.level != 0:
        #         break
        yield from self._check_custom_import_rules(node)
        yield from self._check_project_level_restrictions(node)

    def _check_custom_import_rules(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        yield from self._check_std_lib_only_imports(node)

    def _check_std_lib_only_imports(
        self,
        node: ParsedNode,
    ) -> Generator[ErrorMessage, None, None]:
        """Check standard library only imports"""
        if self.std_lib_only:
            if isinstance(node, ParsedImport):
                yield from self._check_for_cir401(node)

            elif isinstance(node, ParsedFromImport):
                yield from self._check_for_cir402(node)

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
        restrictions = [
            # (
            #     self.checker_settings.TOP_LEVEL_ONLY_IMPORTS,
            #     [ParsedImport, ParsedFromImport],
            #     self._check_for_pir101,
            # ),
            (
                self.checker_settings.RESTRICT_RELATIVE_IMPORTS,
                [ParsedFromImport],
                self._check_for_pir102,
            ),
            (
                self.checker_settings.RESTRICT_LOCAL_IMPORTS,
                [ParsedLocalImport],
                self._check_for_pir103,
            ),
            (
                self.checker_settings.RESTRICT_CONDITIONAL_IMPORTS,
                [ParsedIfImport],
                self._check_for_pir104,
            ),
            (
                self.checker_settings.RESTRICT_DYNAMIC_IMPORTS,
                [ParsedDynamicImport],
                self._check_for_pir105,
            ),
            (
                self.checker_settings.RESTRICT_PRIVATE_IMPORTS,
                [ParsedImport, ParsedFromImport],
                self._check_for_pir106,
            ),
            (
                self.checker_settings.RESTRICT_WILDCARD_IMPORTS,
                [ParsedImport, ParsedFromImport],
                self._check_for_pir107,
            ),
            (
                self.checker_settings.RESTRICT_ALIASED_IMPORTS,
                [ParsedImport, ParsedFromImport],
                self._check_for_pir108,
            ),
        ]

        for is_restriction_active, node_types, check_func in restrictions:
            if is_restriction_active and isinstance(node, tuple(node_types)):
                yield from check_func(node)

    def _check_special_cases_import_restrictions(
        self, node: ParsedNode
    ) -> Generator[ErrorMessage, None, None]:
        """Check special cases import restrictions"""

        if self.checker_settings.RESTRICT_INIT_IMPORTS:
            if isinstance(node, ParsedImport):
                yield from self._check_for_pir207(node)
            elif isinstance(node, ParsedFromImport):
                yield from self._check_for_pir208(node)

        if self.checker_settings.RESTRICT_MAIN_IMPORTS:
            if isinstance(node, ParsedImport):
                yield from self._check_for_pir209(node)
            elif isinstance(node, ParsedFromImport):
                yield from self._check_for_pir210(node)

        if self.checker_settings.RESTRICT_TEST_IMPORTS:
            yield from self._check_test_import_restrictions(node)

    def _check_test_import_restrictions(
        self, node: ParsedNode
    ) -> Generator[ErrorMessage, None, None]:
        """Check test import restrictions"""
        if isinstance(node, ParsedImport):
            yield from self._check_for_pir201(node)
            yield from self._check_for_pir203(node)
            yield from self._check_for_pir205(node)

        elif isinstance(node, ParsedFromImport):
            yield from self._check_for_pir202(node)
            yield from self._check_for_pir204(node)
            yield from self._check_for_pir206(node)

    def _check_restricted_imports(
        self,
        code_offset: int,
        file_identifier: str,
        import_string: str,
        module_name: str,
        node: ParsedNode,
    ) -> Generator[tuple[int, int, str, type], Any, Any] | None:
        """Check restricted imports"""
        if (
            file_identifier in self.import_restrictions
            and module_name in self.import_restrictions[file_identifier]
        ):
            yield self.error(
                f"CIM{101 + code_offset}",
                node.lineno,
                node.col_offset,
                (
                    f"Using '{import_string}' in module '{file_identifier}' "
                    f"is not allowed to import '{module_name}'."
                ),
            )

    def _check_isolated_imports(
        self,
        code_offset: int,
        file_identifier: str,
        import_string: str,
        module_name: str,
        node: ParsedNode,
    ) -> Generator[tuple[int, int, str, type], Any, Any] | None:
        """Check isolated imports"""
        if file_identifier in self.isolated_modules and any(
            module_name.startswith(prefix) for prefix in self.isolated_modules
        ):
            yield self.error(
                f"CIM{201 + code_offset}",
                node.lineno,
                node.col_offset,
                (
                    f"Using '{import_string}' in module '{file_identifier}' "
                    f"cannot import from other modules within the base module."
                ),
            )

    def error(
        self, code: str, lineno: int, col_offset: int, message: str
    ) -> tuple[int, int, str, type]:
        """Report errors."""
        return lineno, col_offset, f"{code} {message}", type(self)
        # self.error(*error)

    def _check_for_cir101(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for CIR101."""
        if ErrorCode.CIR101.code in self.codes_to_check:
            yield standard_error_message(node, ErrorCode.CIR101)

    def _check_for_cir102(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for CIR102."""
        if ErrorCode.CIR102.code in self.codes_to_check:
            yield standard_error_message(node, ErrorCode.CIR102)

    def _check_for_cir103(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for CIR103."""
        if ErrorCode.CIR103.code in self.codes_to_check:
            yield standard_error_message(node, ErrorCode.CIR103)

    def _check_for_cir104(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for CIR104."""
        if ErrorCode.CIR104.code in self.codes_to_check:
            yield standard_error_message(node, ErrorCode.CIR104)

    def _check_for_cir105(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for CIR105."""
        if ErrorCode.CIR105.code in self.codes_to_check:
            yield standard_error_message(node, ErrorCode.CIR105)

    def _check_for_cir106(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for CIR106."""
        if ErrorCode.CIR106.code in self.codes_to_check:
            yield standard_error_message(node, ErrorCode.CIR106)

    def _check_for_cir107(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for CIR107."""
        if ErrorCode.CIR107.code in self.codes_to_check:
            yield standard_error_message(node, ErrorCode.CIR107)

    def _check_for_cir201(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for CIR201."""
        if ErrorCode.CIR201.code in self.codes_to_check:
            yield standard_error_message(node, ErrorCode.CIR201)

    def _check_for_cir202(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for CIR202."""
        if ErrorCode.CIR202.code in self.codes_to_check:
            yield standard_error_message(node, ErrorCode.CIR202)

    def _check_for_cir203(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for CIR203."""
        if ErrorCode.CIR203.code in self.codes_to_check:
            yield standard_error_message(node, ErrorCode.CIR203)

    def _check_for_cir204(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for CIR204."""
        if ErrorCode.CIR204.code in self.codes_to_check:
            yield standard_error_message(node, ErrorCode.CIR204)

    def _check_for_cir301(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for CIR301."""
        if ErrorCode.CIR301.code in self.codes_to_check:
            yield standard_error_message(node, ErrorCode.CIR301)

    def _check_for_cir302(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for CIR302."""
        if ErrorCode.CIR302.code in self.codes_to_check:
            yield standard_error_message(node, ErrorCode.CIR302)

    def _check_for_cir303(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for CIR303."""
        if ErrorCode.CIR303.code in self.codes_to_check:
            yield standard_error_message(node, ErrorCode.CIR303)

    def _check_for_cir304(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for CIR304."""
        if ErrorCode.CIR304.code in self.codes_to_check:
            yield standard_error_message(node, ErrorCode.CIR304)

    def _check_for_cir401(self, node: ParsedImport) -> Generator[ErrorMessage, None, None]:
        """Check for CIR401."""
        condition = node.import_type not in {ImportType.FUTURE, ImportType.STDLIB}
        if ErrorCode.CIR401.code in self.codes_to_check and condition:
            yield std_lib_only_error(node, ErrorCode.CIR401)

    def _check_for_cir402(self, node: ParsedFromImport) -> Generator[ErrorMessage, None, None]:
        """Check for CIR402."""
        condition = node.import_type not in {ImportType.FUTURE, ImportType.STDLIB}
        if ErrorCode.CIR402.code in self.codes_to_check and condition:
            yield std_lib_only_error(node, ErrorCode.CIR402)

    def _check_for_cir501(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for CIR501."""
        if ErrorCode.CIR501.code in self.codes_to_check:
            yield standard_error_message(node, ErrorCode.CIR501)

    def _check_for_cir502(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for CIR502."""
        if ErrorCode.CIR502.code in self.codes_to_check:
            yield standard_error_message(node, ErrorCode.CIR502)

    def _check_for_pir101(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for PIR101, only top level imports are permitted."""
        if ErrorCode.PIR101.code in self.codes_to_check:
            yield standard_error_message(node, ErrorCode.PIR101)

    def _check_for_pir102(self, node: ParsedFromImport) -> Generator[ErrorMessage, None, None]:
        """Check for PIR102, relative import restrictions."""
        condition = node.level > 0
        if ErrorCode.PIR102.code in self.codes_to_check and condition:
            yield standard_error_message(node, ErrorCode.PIR102)

    def _check_for_pir103(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for PIR103, local import restrictions."""
        condition = isinstance(node, ParsedLocalImport)
        if ErrorCode.PIR103.code in self.codes_to_check and condition:
            yield standard_error_message(node, ErrorCode.PIR103)

    def _check_for_pir104(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for PIR104, conditional import restrictions."""
        if ErrorCode.PIR104.code in self.codes_to_check:
            yield standard_error_message(node, ErrorCode.PIR104)

    def _get_dynamic_import_nodes(self, node: ParsedDynamicImport) -> list[ParsedNode]:
        """Get dynamic nodes."""
        return [
            dynamic_node
            for dynamic_node in self.dynamic_nodes[str(node.lineno)]
            if isinstance(dynamic_node, (DynamicStringImport, DynamicStringFromImport))
        ]

    def _dynamic_import_check(self, node: ParsedDynamicImport) -> bool:
        """Check if a node is a dynamic import."""
        if not node.confirmed and check_string(node.identifier, substring_match="modules"):
            node.confirmed = self.identifiers["modules"]["package"] == "sys"
        if not node.confirmed and check_string(
            node.identifier, substring_match=["get_loader", "iter_modules"]
        ):
            node.confirmed = self.identifiers["get_loader"]["package"] == "pkgutil"

        if not node.confirmed and check_string(node.identifier, substring_match=["eval", "exec"]):
            dynamic_nodes = self._get_dynamic_import_nodes(node)
            node.confirmed = bool(dynamic_nodes)

        return bool(node.confirmed)

    def _check_for_pir105(self, node: ParsedDynamicImport) -> Generator[ErrorMessage, None, None]:
        """Check for PIR105, dynamic import restrictions."""
        condition = self._dynamic_import_check(node)
        if ErrorCode.PIR105.code in self.codes_to_check and condition:
            yield standard_error_message(node, ErrorCode.PIR105)
        # if ErrorCode.PIR301.code in self.codes_to_check and not condition:
        #     yield standard_error_message(node, ErrorCode.PIR301)

    def _check_for_pir106(
        self, node: ParsedImport | ParsedFromImport
    ) -> Generator[ErrorMessage, None, None]:
        """Check for PIR106, private import restrictions."""
        condition = node.private_identifier_import or node.private_module_import
        if ErrorCode.PIR106.code in self.codes_to_check and condition:
            yield standard_error_message(node, ErrorCode.PIR106)

    def _check_for_pir107(
        self, node: ParsedImport | ParsedFromImport
    ) -> Generator[ErrorMessage, None, None]:
        """Check for PIR107, wildcard or star import restrictions (i.e., from * imports)."""
        condition = check_string(node.identifier, substring_match="*")
        if ErrorCode.PIR107.code in self.codes_to_check and condition:
            yield standard_error_message(node, ErrorCode.PIR107)

    def _check_for_pir108(
        self, node: ParsedImport | ParsedFromImport
    ) -> Generator[ErrorMessage, None, None]:
        """Check for PIR108, aliased import restrictions."""
        condition = hasattr(node, "asname") and node.asname is not None
        if ErrorCode.PIR108.code in self.codes_to_check and condition:
            yield standard_error_message(node, ErrorCode.PIR108)

    def _check_for_pir201(self, node: ParsedImport) -> Generator[ErrorMessage, None, None]:
        """Check for PIR201, import test_*/*_test modules is restricted."""
        condition = check_string(node.identifier, prefix="test_", suffix="_test")
        if ErrorCode.PIR201.code in self.codes_to_check and condition:
            yield standard_error_message(node, ErrorCode.PIR201)

    def _check_for_pir202(self, node: ParsedFromImport) -> Generator[ErrorMessage, None, None]:
        """Check for PIR202, import from test_*/*_test modules is restricted."""
        condition = check_string(node.identifier, prefix="test_", suffix="_test")
        if ErrorCode.PIR202.code in self.codes_to_check and condition:
            yield standard_error_message(node, ErrorCode.PIR202)

    def _check_for_pir203(self, node: ParsedImport) -> Generator[ErrorMessage, None, None]:
        """Check for PIR203, import conftest is restricted."""
        condition = check_string(node.identifier, substring_match="conftest")
        if ErrorCode.PIR203.code in self.codes_to_check and condition:
            yield standard_error_message(node, ErrorCode.PIR203)

    def _check_for_pir204(self, node: ParsedFromImport) -> Generator[ErrorMessage, None, None]:
        """Check for PIR204, import from conftest is restricted."""
        condition = check_string(node.identifier, substring_match="conftest")
        if ErrorCode.PIR204.code in self.codes_to_check and condition:
            yield standard_error_message(node, ErrorCode.PIR204)

    def _check_for_pir205(self, node: ParsedImport) -> Generator[ErrorMessage, None, None]:
        """Check for PIR205 import tests directory is restricted."""
        condition = check_string(node.identifier, substring_match="tests")
        if ErrorCode.PIR205.code in self.codes_to_check and condition:
            yield standard_error_message(node, ErrorCode.PIR205)

    def _check_for_pir206(self, node: ParsedFromImport) -> Generator[ErrorMessage, None, None]:
        """Check for PIR206, import from tests directory is restricted."""
        condition = check_string(node.identifier, substring_match="tests")
        if ErrorCode.PIR206.code in self.codes_to_check and condition:
            yield standard_error_message(node, ErrorCode.PIR206)

    def _check_for_pir207(self, node: ParsedImport) -> Generator[ErrorMessage, None, None]:
        """Check for PIR207, import __init__."""
        condition = check_string(node.identifier, substring_match="__init__")
        if ErrorCode.PIR207.code in self.codes_to_check and condition:
            yield standard_error_message(node, ErrorCode.PIR207)

    def _check_for_pir208(self, node: ParsedFromImport) -> Generator[ErrorMessage, None, None]:
        """Check for PIR208, from __init__ imports."""
        condition = check_string(node.identifier, substring_match="__init__")
        if ErrorCode.PIR208.code in self.codes_to_check and condition:
            yield standard_error_message(node, ErrorCode.PIR208)

    def _check_for_pir209(self, node: ParsedImport) -> Generator[ErrorMessage, None, None]:
        """Check for PIR209 import __main__."""
        condition = check_string(node.identifier, substring_match="__main__")
        if ErrorCode.PIR209.code in self.codes_to_check and condition:
            yield standard_error_message(node, ErrorCode.PIR209)

    def _check_for_pir210(self, node: ParsedFromImport) -> Generator[ErrorMessage, None, None]:
        """Check for PIR210 for from __main__ imports."""
        condition = check_string(node.identifier, substring_match="__main__")
        if ErrorCode.PIR210.code in self.codes_to_check and condition:
            yield standard_error_message(node, ErrorCode.PIR210)
