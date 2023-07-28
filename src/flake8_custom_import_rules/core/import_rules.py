""" Custom Import Rules for Flake8 & Python Projects. """
from __future__ import annotations

import logging
from collections import defaultdict
from typing import Callable
from typing import Generator

from attrs import define
from attrs import field

from flake8_custom_import_rules.codes.error_codes import ErrorCode
from flake8_custom_import_rules.core.error_messages import ErrorMessage
from flake8_custom_import_rules.core.error_messages import first_party_only_error
from flake8_custom_import_rules.core.error_messages import isolated_imports_error
from flake8_custom_import_rules.core.error_messages import restricted_imports_error
from flake8_custom_import_rules.core.error_messages import standard_error_message
from flake8_custom_import_rules.core.error_messages import std_lib_only_error
from flake8_custom_import_rules.core.error_messages import third_party_only_error
from flake8_custom_import_rules.core.nodes import DynamicStringFromImport
from flake8_custom_import_rules.core.nodes import DynamicStringStraightImport
from flake8_custom_import_rules.core.nodes import ImportType
from flake8_custom_import_rules.core.nodes import ParsedDynamicImport
from flake8_custom_import_rules.core.nodes import ParsedFromImport
from flake8_custom_import_rules.core.nodes import ParsedIfImport
from flake8_custom_import_rules.core.nodes import ParsedLocalImport
from flake8_custom_import_rules.core.nodes import ParsedNode
from flake8_custom_import_rules.core.nodes import ParsedStraightImport
from flake8_custom_import_rules.defaults import STDIN_IDENTIFIERS
from flake8_custom_import_rules.defaults import Settings
from flake8_custom_import_rules.utils.parse_utils import check_string
from flake8_custom_import_rules.utils.parse_utils import does_file_match_custom_rule
from flake8_custom_import_rules.utils.parse_utils import does_import_match_restricted_imports

logger = logging.getLogger(__name__)


def filename_not_in_stdin_identifiers(
    filename: str,
) -> bool:
    """Check if filename is not in STDIN_IDENTIFIERS."""
    return filename not in STDIN_IDENTIFIERS


def get_file_matches_custom_rule(option_key: str) -> Callable[[CustomImportRules], bool]:
    """Get rule."""
    option_key = option_key.upper()

    def match_custom_rule(instance: CustomImportRules) -> bool:
        """Match custom rule."""
        custom_rule = getattr(instance.checker_settings, option_key, None)
        if custom_rule is None:
            logger.error(f"Option key '{option_key}' not found in checker settings")
            return False

        return does_file_match_custom_rule(instance.file_identifier, custom_rule)

    return match_custom_rule


def get_isolated_package_rule(option_key: str) -> Callable[[CustomImportRules], bool]:
    """Get isolated package rule."""
    option_key = option_key.upper()

    def isolated_package(instance: CustomImportRules) -> bool:
        """Match custom rule."""
        custom_rule = getattr(instance.checker_settings, option_key, None)
        if custom_rule is None:
            logger.error(f"Option key '{option_key}' not found in checker settings")
            return False

        return instance.isolated_module and instance.file_identifier not in custom_rule

    return isolated_package


@define(slots=True)
class CustomImportRules:
    """Custom Import Rules for Flake8 & Python Projects"""

    nodes: list[ParsedNode] = field(factory=list)
    dynamic_nodes: defaultdict[str, list] = defaultdict(list)
    identifiers: defaultdict[str, dict] = defaultdict(lambda: defaultdict(str))
    identifiers_by_lineno: defaultdict[str, list] = defaultdict(list)
    checker_settings: Settings = field(factory=Settings)
    codes_to_check: list[ErrorCode] = ErrorCode.get_all_error_codes()

    filename: str = field(default=None)
    file_identifier: str = field(default=None)
    file_root_package_name: str = field(default=None)
    file_packages: list = field(default=None)
    check_custom_import_rules: bool = field(default=filename_not_in_stdin_identifiers(filename))

    project_only: bool = field(default=False)
    base_package_only: bool = field(default=False)
    first_party_only: bool = field(default=False)
    isolated_module: bool = field(default=False)
    isolated_package: bool = field(default=False)
    std_lib_only: bool = field(default=False)
    third_party_only: bool = field(default=False)

    import_restrictions: dict = field(factory=dict)
    restricted_packages: list[str] = field(factory=list)
    file_in_restricted_packages: bool = field(default=False)
    restricted_identifiers: dict = field(factory=dict)

    check_top_level_only: bool = field(default=False)

    def __attrs_post_init__(self) -> None:
        """Post init."""
        logging.debug(f"file_identifier: {self.file_identifier}")
        self.nodes = sorted(self.nodes, key=lambda element: element.lineno)

        # for these restrictions we want to match a file identifier
        # because the import rules correspond to an ImportType
        self.project_only = get_file_matches_custom_rule("PROJECT_ONLY")(self)
        self.base_package_only = get_file_matches_custom_rule("BASE_PACKAGE_ONLY")(self)
        self.first_party_only = get_file_matches_custom_rule("FIRST_PARTY_ONLY")(self)
        self.isolated_module = get_file_matches_custom_rule("ISOLATED_MODULES")(self)
        self.isolated_package = get_isolated_package_rule("ISOLATED_MODULES")(self)
        self.std_lib_only = get_file_matches_custom_rule("STD_LIB_ONLY")(self)
        self.third_party_only = get_file_matches_custom_rule("THIRD_PARTY_ONLY")(self)

        self.restricted_packages = self.checker_settings.RESTRICTED_PACKAGES
        self.file_in_restricted_packages = get_file_matches_custom_rule("RESTRICTED_PACKAGES")(self)

        print(f"Restricted packages: {self.restricted_packages}")
        logger.info(f"File packages: {self.file_packages}")
        logger.info(f"Restricted packages: {self.restricted_packages}")
        logger.info(f"Restricted identifiers: {self.restricted_identifiers}")
        logger.info(f"Restricted identifiers keys: {list(self.restricted_identifiers.keys())}")

    def check_import_rules(self) -> Generator[ErrorMessage, None, None]:
        """Check imports"""
        for node in self.nodes:
            yield from self._check_import_rules(node)

    def _check_import_rules(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check import rules"""
        yield from self._check_project_level_restrictions(node)

        # Custom Import Rules can only be checked when
        # filename is provided
        if self.check_custom_import_rules:
            yield from self._check_custom_import_rules(node)

    def _check_custom_import_rules(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check custom import rules"""
        yield from self._check_project_imports(node)
        yield from self._check_if_isolated_module(node)
        yield from self._check_std_lib_only_imports(node)
        yield from self._check_third_party_only_imports(node)
        yield from self._check_restricted_imports(node)

    def _check_restricted_imports(
        self,
        node: ParsedNode,
    ) -> Generator[ErrorMessage, None, None]:
        """Check restricted imports"""
        if self.restricted_packages:
            if isinstance(node, ParsedStraightImport):
                yield from self._check_for_cir106(node)

            elif isinstance(node, ParsedFromImport):
                yield from self._check_for_cir107(node)

    def _check_project_imports(
        self,
        node: ParsedNode,
    ) -> Generator[ErrorMessage, None, None]:
        """Check project imports"""
        if self.project_only:
            if isinstance(node, ParsedStraightImport):
                yield from self._check_for_cir201(node)

            elif isinstance(node, ParsedFromImport):
                yield from self._check_for_cir202(node)

        if self.base_package_only:
            if isinstance(node, ParsedStraightImport):
                yield from self._check_for_cir203(node)

            elif isinstance(node, ParsedFromImport):
                yield from self._check_for_cir204(node)

        if self.first_party_only:
            if isinstance(node, ParsedStraightImport):
                yield from self._check_for_cir205(node)

            if isinstance(node, ParsedFromImport):
                yield from self._check_for_cir206(node)

    def _check_if_isolated_module(
        self,
        node: ParsedNode,
    ) -> Generator[ErrorMessage, None, None]:
        """Check isolated module"""
        if self.isolated_module:
            if self.isolated_package:
                if isinstance(node, ParsedStraightImport):
                    yield from self._check_for_cir301(node)

                elif isinstance(node, ParsedFromImport):
                    yield from self._check_for_cir302(node)

            elif isinstance(node, ParsedStraightImport):
                yield from self._check_for_cir303(node)

            elif isinstance(node, ParsedFromImport):
                yield from self._check_for_cir304(node)

    def _check_std_lib_only_imports(
        self,
        node: ParsedNode,
    ) -> Generator[ErrorMessage, None, None]:
        """Check standard library only imports"""
        if self.std_lib_only:
            if isinstance(node, ParsedStraightImport):
                yield from self._check_for_cir401(node)

            elif isinstance(node, ParsedFromImport):
                yield from self._check_for_cir402(node)

    def _check_third_party_only_imports(
        self,
        node: ParsedNode,
    ) -> Generator[ErrorMessage, None, None]:
        """Check third party only imports"""
        if self.third_party_only:
            if isinstance(node, ParsedStraightImport):
                yield from self._check_for_cir501(node)

            elif isinstance(node, ParsedFromImport):
                yield from self._check_for_cir502(node)

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
            #     [ParsedStraightImport, ParsedFromImport],
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
                [ParsedStraightImport, ParsedFromImport],
                self._check_for_pir106,
            ),
            (
                self.checker_settings.RESTRICT_WILDCARD_IMPORTS,
                [ParsedStraightImport, ParsedFromImport],
                self._check_for_pir107,
            ),
            (
                self.checker_settings.RESTRICT_ALIASED_IMPORTS,
                [ParsedStraightImport, ParsedFromImport],
                self._check_for_pir108,
            ),
            (
                self.checker_settings.RESTRICT_FUTURE_IMPORTS,
                [ParsedStraightImport, ParsedFromImport],
                self._check_for_pir109,
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
            if isinstance(node, ParsedStraightImport):
                yield from self._check_for_pir207(node)
            elif isinstance(node, ParsedFromImport):
                yield from self._check_for_pir208(node)

        if self.checker_settings.RESTRICT_MAIN_IMPORTS:
            if isinstance(node, ParsedStraightImport):
                yield from self._check_for_pir209(node)
            elif isinstance(node, ParsedFromImport):
                yield from self._check_for_pir210(node)

        if self.checker_settings.RESTRICT_TEST_IMPORTS:
            yield from self._check_test_import_restrictions(node)

    def _check_test_import_restrictions(
        self, node: ParsedNode
    ) -> Generator[ErrorMessage, None, None]:
        """Check test import restrictions"""
        if isinstance(node, ParsedStraightImport):
            yield from self._check_for_pir201(node)
            yield from self._check_for_pir203(node)
            yield from self._check_for_pir205(node)

        elif isinstance(node, ParsedFromImport):
            yield from self._check_for_pir202(node)
            yield from self._check_for_pir204(node)
            yield from self._check_for_pir206(node)

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

    def _check_if_restricted_package(self, node: ParsedNode) -> bool:
        """Check if restricted package."""
        logging.info(
            f"Node import_statement: `{node.import_statement}`, "
            f"import_type: {node.import_type}, "
            f"module: `{node.module}`,"
        )
        # if node.import_type != ImportType.FIRST_PARTY:
        #     return False
        if node.module in self.restricted_packages:
            return True
        return bool(does_import_match_restricted_imports(node.identifier, self.restricted_packages))

    def _check_if_file_in_restricted_packages(self, node: ParsedNode) -> bool:
        """Check if file in restricted packages."""
        return does_file_match_custom_rule(self.file_identifier, self.restricted_packages)

    def _check_for_cir106(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for CIR106."""
        condition = self._check_if_restricted_package(node)
        if ErrorCode.CIR106.code in self.codes_to_check and condition:
            yield restricted_imports_error(node, ErrorCode.CIR106)

    def _check_for_cir107(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for CIR107."""
        condition = self._check_if_restricted_package(node)
        if ErrorCode.CIR107.code in self.codes_to_check and condition:
            yield restricted_imports_error(node, ErrorCode.CIR107)

    @staticmethod
    def _check_if_project_imports(node: ParsedNode) -> bool:
        """Check for project imports"""
        return node.import_type not in {
            ImportType.FUTURE,
            ImportType.STDLIB,
            ImportType.FIRST_PARTY,
        }

    def _check_if_project_base_package_imports(self, node: ParsedNode) -> bool:
        """Check for project base imports"""
        # logging.debug(f"node.import_type: {node.import_type.name}")
        if node.import_type == ImportType.FIRST_PARTY:
            # logging.debug(
            #     f"node.package: {node.package}, "
            #     f"file_root_package_name: {self.file_root_package_name}"
            # )
            return node.package != self.file_root_package_name
        return self._check_if_project_imports(node)

    def _check_if_non_first_party_imports(self, node: ParsedNode) -> bool:
        """Check for project base imports"""
        # logging.debug(f"node.import_type: {node.import_type.name}")
        if node.import_type == ImportType.FIRST_PARTY:
            # logging.debug(
            #     f"node.package: {node.package}, "
            #     f"file_root_package_name: {self.file_root_package_name}"
            # )
            return node.package == self.file_root_package_name
        return self._check_if_project_imports(node)

    def _check_for_cir201(self, node: ParsedStraightImport) -> Generator[ErrorMessage, None, None]:
        """Check for CIR201."""
        condition = self._check_if_project_imports(node)
        if ErrorCode.CIR201.code in self.codes_to_check and condition:
            yield first_party_only_error(node, ErrorCode.CIR201)

    def _check_for_cir202(self, node: ParsedFromImport) -> Generator[ErrorMessage, None, None]:
        """Check for CIR202."""
        condition = self._check_if_project_imports(node)
        if ErrorCode.CIR202.code in self.codes_to_check and condition:
            yield first_party_only_error(node, ErrorCode.CIR202)

    def _check_for_cir203(self, node: ParsedStraightImport) -> Generator[ErrorMessage, None, None]:
        """Check for CIR203."""
        condition = self._check_if_project_base_package_imports(node)
        if ErrorCode.CIR203.code in self.codes_to_check and condition:
            yield first_party_only_error(node, ErrorCode.CIR203)

    def _check_for_cir204(self, node: ParsedFromImport) -> Generator[ErrorMessage, None, None]:
        """Check for CIR204."""
        condition = self._check_if_project_base_package_imports(node)
        if ErrorCode.CIR204.code in self.codes_to_check and condition:
            yield first_party_only_error(node, ErrorCode.CIR204)

    def _check_for_cir205(self, node: ParsedStraightImport) -> Generator[ErrorMessage, None, None]:
        """Check for CIR205."""
        condition = self._check_if_non_first_party_imports(node)
        if ErrorCode.CIR205.code in self.codes_to_check and condition:
            yield first_party_only_error(node, ErrorCode.CIR205)

    def _check_for_cir206(self, node: ParsedFromImport) -> Generator[ErrorMessage, None, None]:
        """Check for CIR206."""
        condition = self._check_if_non_first_party_imports(node)
        if ErrorCode.CIR206.code in self.codes_to_check and condition:
            yield first_party_only_error(node, ErrorCode.CIR206)

    def _check_for_cir301(self, node: ParsedStraightImport) -> Generator[ErrorMessage, None, None]:
        """Check for CIR301, check if isolated module."""
        condition = node.import_type == ImportType.FIRST_PARTY
        if ErrorCode.CIR301.code in self.codes_to_check and condition:
            yield isolated_imports_error(node, ErrorCode.CIR301, self.file_identifier)

    def _check_for_cir302(self, node: ParsedFromImport) -> Generator[ErrorMessage, None, None]:
        """Check for CIR302, check if isolated module."""
        condition = node.import_type == ImportType.FIRST_PARTY
        if ErrorCode.CIR302.code in self.codes_to_check and condition:
            yield isolated_imports_error(node, ErrorCode.CIR302, self.file_identifier)

    def _check_for_cir303(self, node: ParsedStraightImport) -> Generator[ErrorMessage, None, None]:
        """Check for CIR303, check if isolated module."""
        condition = node.import_type == ImportType.FIRST_PARTY
        if ErrorCode.CIR303.code in self.codes_to_check and condition:
            yield isolated_imports_error(node, ErrorCode.CIR303, self.file_identifier)

    def _check_for_cir304(self, node: ParsedFromImport) -> Generator[ErrorMessage, None, None]:
        """Check for CIR304, check if isolated module."""
        condition = node.import_type == ImportType.FIRST_PARTY
        if ErrorCode.CIR304.code in self.codes_to_check and condition:
            yield isolated_imports_error(node, ErrorCode.CIR304, self.file_identifier)

    def _check_for_cir401(self, node: ParsedStraightImport) -> Generator[ErrorMessage, None, None]:
        """Check for CIR401."""
        condition = node.import_type not in {ImportType.FUTURE, ImportType.STDLIB}
        if ErrorCode.CIR401.code in self.codes_to_check and condition:
            yield std_lib_only_error(node, ErrorCode.CIR401)

    def _check_for_cir402(self, node: ParsedFromImport) -> Generator[ErrorMessage, None, None]:
        """Check for CIR402."""
        condition = node.import_type not in {ImportType.FUTURE, ImportType.STDLIB}
        if ErrorCode.CIR402.code in self.codes_to_check and condition:
            yield std_lib_only_error(node, ErrorCode.CIR402)

    def _check_for_cir501(self, node: ParsedStraightImport) -> Generator[ErrorMessage, None, None]:
        """Check for CIR501."""
        condition = node.import_type not in {
            ImportType.FUTURE,
            ImportType.STDLIB,
            ImportType.THIRD_PARTY,
        }
        if ErrorCode.CIR501.code in self.codes_to_check and condition:
            yield third_party_only_error(node, ErrorCode.CIR501)

    def _check_for_cir502(self, node: ParsedFromImport) -> Generator[ErrorMessage, None, None]:
        """Check for CIR502."""
        condition = node.import_type not in {
            ImportType.FUTURE,
            ImportType.STDLIB,
            ImportType.THIRD_PARTY,
        }
        if ErrorCode.CIR502.code in self.codes_to_check and condition:
            yield third_party_only_error(node, ErrorCode.CIR502)

    def _check_for_pir101(self, node: ParsedNode) -> Generator[ErrorMessage, None, None]:
        """Check for PIR101, only top level imports are permitted."""
        if ErrorCode.PIR101.code in self.codes_to_check:
            yield standard_error_message(node, ErrorCode.PIR101)

    def _check_for_pir102(self, node: ParsedFromImport) -> Generator[ErrorMessage, None, None]:
        """Check for PIR102, relative import restrictions."""
        condition = node.level > 0
        if ErrorCode.PIR102.code in self.codes_to_check and condition:
            yield standard_error_message(node, ErrorCode.PIR102)

    def _check_for_pir103(self, node: ParsedLocalImport) -> Generator[ErrorMessage, None, None]:
        """Check for PIR103, local import restrictions."""
        condition = isinstance(node, ParsedLocalImport)
        if ErrorCode.PIR103.code in self.codes_to_check and condition:
            yield standard_error_message(node, ErrorCode.PIR103)

    def _check_for_pir104(self, node: ParsedIfImport) -> Generator[ErrorMessage, None, None]:
        """Check for PIR104, conditional import restrictions."""
        if ErrorCode.PIR104.code in self.codes_to_check:
            yield standard_error_message(node, ErrorCode.PIR104)

    def _get_dynamic_import_nodes(self, node: ParsedDynamicImport) -> list[ParsedNode]:
        """Get dynamic nodes."""
        return [
            dynamic_node
            for dynamic_node in self.dynamic_nodes[str(node.lineno)]
            if isinstance(dynamic_node, (DynamicStringStraightImport, DynamicStringFromImport))
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
        self, node: ParsedStraightImport | ParsedFromImport
    ) -> Generator[ErrorMessage, None, None]:
        """Check for PIR106, private import restrictions."""
        condition = node.private_identifier_import or node.private_module_import
        if ErrorCode.PIR106.code in self.codes_to_check and condition:
            yield standard_error_message(node, ErrorCode.PIR106)

    def _check_for_pir107(
        self, node: ParsedStraightImport | ParsedFromImport
    ) -> Generator[ErrorMessage, None, None]:
        """Check for PIR107, wildcard or star import restrictions (i.e., from * imports)."""
        condition = check_string(node.identifier, substring_match="*")
        if ErrorCode.PIR107.code in self.codes_to_check and condition:
            yield standard_error_message(node, ErrorCode.PIR107)

    def _check_for_pir108(
        self, node: ParsedStraightImport | ParsedFromImport
    ) -> Generator[ErrorMessage, None, None]:
        """Check for PIR108, aliased import restrictions."""
        condition = hasattr(node, "asname") and node.asname is not None
        if ErrorCode.PIR108.code in self.codes_to_check and condition:
            yield standard_error_message(node, ErrorCode.PIR108)

    def _check_for_pir109(
        self, node: ParsedStraightImport | ParsedFromImport
    ) -> Generator[ErrorMessage, None, None]:
        """Check for PIR109, __future__ import restrictions."""
        condition = node.import_type == ImportType.FUTURE
        if ErrorCode.PIR109.code in self.codes_to_check and condition:
            yield standard_error_message(node, ErrorCode.PIR109)

    def _check_for_pir201(self, node: ParsedStraightImport) -> Generator[ErrorMessage, None, None]:
        """Check for PIR201, import test_*/*_test modules is restricted."""
        condition = check_string(node.identifier, prefix="test_", suffix="_test")
        if ErrorCode.PIR201.code in self.codes_to_check and condition:
            yield standard_error_message(node, ErrorCode.PIR201)

    def _check_for_pir202(self, node: ParsedFromImport) -> Generator[ErrorMessage, None, None]:
        """Check for PIR202, import from test_*/*_test modules is restricted."""
        condition = check_string(node.identifier, prefix="test_", suffix="_test")
        if ErrorCode.PIR202.code in self.codes_to_check and condition:
            yield standard_error_message(node, ErrorCode.PIR202)

    def _check_for_pir203(self, node: ParsedStraightImport) -> Generator[ErrorMessage, None, None]:
        """Check for PIR203, import conftest is restricted."""
        condition = check_string(node.identifier, substring_match="conftest")
        if ErrorCode.PIR203.code in self.codes_to_check and condition:
            yield standard_error_message(node, ErrorCode.PIR203)

    def _check_for_pir204(self, node: ParsedFromImport) -> Generator[ErrorMessage, None, None]:
        """Check for PIR204, import from conftest is restricted."""
        condition = check_string(node.identifier, substring_match="conftest")
        if ErrorCode.PIR204.code in self.codes_to_check and condition:
            yield standard_error_message(node, ErrorCode.PIR204)

    def _check_for_pir205(self, node: ParsedStraightImport) -> Generator[ErrorMessage, None, None]:
        """Check for PIR205 import tests directory is restricted."""
        condition = check_string(node.identifier, substring_match="tests")
        if ErrorCode.PIR205.code in self.codes_to_check and condition:
            yield standard_error_message(node, ErrorCode.PIR205)

    def _check_for_pir206(self, node: ParsedFromImport) -> Generator[ErrorMessage, None, None]:
        """Check for PIR206, import from tests directory is restricted."""
        condition = check_string(node.identifier, substring_match="tests")
        if ErrorCode.PIR206.code in self.codes_to_check and condition:
            yield standard_error_message(node, ErrorCode.PIR206)

    def _check_for_pir207(self, node: ParsedStraightImport) -> Generator[ErrorMessage, None, None]:
        """Check for PIR207, import __init__."""
        condition = check_string(node.identifier, substring_match="__init__")
        if ErrorCode.PIR207.code in self.codes_to_check and condition:
            yield standard_error_message(node, ErrorCode.PIR207)

    def _check_for_pir208(self, node: ParsedFromImport) -> Generator[ErrorMessage, None, None]:
        """Check for PIR208, from __init__ imports."""
        condition = check_string(node.identifier, substring_match="__init__")
        if ErrorCode.PIR208.code in self.codes_to_check and condition:
            yield standard_error_message(node, ErrorCode.PIR208)

    def _check_for_pir209(self, node: ParsedStraightImport) -> Generator[ErrorMessage, None, None]:
        """Check for PIR209 import __main__."""
        condition = check_string(node.identifier, substring_match="__main__")
        if ErrorCode.PIR209.code in self.codes_to_check and condition:
            yield standard_error_message(node, ErrorCode.PIR209)

    def _check_for_pir210(self, node: ParsedFromImport) -> Generator[ErrorMessage, None, None]:
        """Check for PIR210 for from __main__ imports."""
        condition = check_string(node.identifier, substring_match="__main__")
        if ErrorCode.PIR210.code in self.codes_to_check and condition:
            yield standard_error_message(node, ErrorCode.PIR210)
