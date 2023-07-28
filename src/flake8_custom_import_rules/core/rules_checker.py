"""Checker for dependency rules checker."""
import ast
import logging
from collections import defaultdict
from typing import Any
from typing import Generator

import pycodestyle
from attrs import define
from attrs import field

from flake8_custom_import_rules.core.error_messages import ErrorMessage
from flake8_custom_import_rules.core.import_rules import CustomImportRules
from flake8_custom_import_rules.core.node_visitor import CustomImportRulesVisitor
from flake8_custom_import_rules.core.nodes import ParsedNode
from flake8_custom_import_rules.core.restricted_import_visitor import get_restricted_identifiers
from flake8_custom_import_rules.defaults import DEFAULT_CHECKER_SETTINGS
from flake8_custom_import_rules.utils.parse_utils import NOQA_INLINE_REGEXP
from flake8_custom_import_rules.utils.parse_utils import parse_comma_separated_list

logger = logging.getLogger(__name__)


@define(slots=True, hash=False)
class CustomImportRulesChecker:
    """Custom import rules checker."""

    _tree: ast.AST | None = None
    _filename: str | None = None
    _lines: list[str] | None = None
    _visitor: CustomImportRulesVisitor | None = None

    _nodes: list[ParsedNode] | None = None
    _identifiers: defaultdict[str, dict] | None = None
    _identifiers_by_lineno: defaultdict[str, list] | None = None
    _restricted_identifiers: defaultdict[str, dict] | None = None

    _options: dict[str, list[str] | str | bool] = field(init=False)

    @property
    def tree(self) -> ast.AST:
        """Return the tree."""
        logger.info(f"Tree before: {self._tree}")
        if not self._tree:
            logger.info("Tree from lines")
            self._tree = ast.parse("".join(self.lines))
        logger.info(f"Tree after: {self._tree}")
        return self._tree

    @property
    def filename(self) -> str:
        """Return the filename."""
        logger.info(f"Filename: {self._filename}")
        if self._filename is None or self._filename in {"-", "/dev/stdin"}:
            return "stdin"
        logger.info(f"Filename: {self._filename}")
        return self._filename

    @property
    def lines(self) -> list[str]:
        """Return the lines."""
        # if self._lines is None and self._tree is not None:
        #     self._lines = ast.unparse(self._tree).splitlines(keepends=True)
        logger.info(f"Lines: {self._lines}")
        if self._lines is None:
            self._lines = (
                pycodestyle.stdin_get_value().splitlines(True)
                if self.filename == "stdin"
                else pycodestyle.readlines(self.filename)
            )
        logger.info(f"Lines after pycodestyle: {self._lines}")
        return self._lines

    @property
    def nodes(self) -> list[ParsedNode]:
        """Return the nodes."""
        logger.info(f"Nodes Visitor: {self._visitor}")
        logger.info(f"Nodes: {self._nodes}")
        logger.info(f"Options: {self._options}")
        if self._nodes is None:
            if self._visitor is None:
                self._visitor = self.visitor
            self._nodes = self._visitor.nodes
        # logger.info(f"Nodes after setting visitor: {self._nodes}")
        return self._nodes

    def get_visitor(self) -> CustomImportRulesVisitor:
        """Return the visitor to use for this plugin."""
        # print(f"\\nOptions: {self.options}\n\n")
        logger.info(f"Tree before lines: {self._tree}")
        logger.info(f"Lines: {self._lines}")
        logger.info(f"Tree after lines: {self._tree}")
        logger.info(f"Options: {self._options}")
        visitor = CustomImportRulesVisitor(
            base_packages=self._options.get("base_packages", []),
            filename=self._filename,
        )
        if self._tree:
            visitor.visit(self._tree)
        if self._lines:
            visitor.visit(self.tree)
        if self._filename:
            visitor.visit(self.tree)
        self._visitor = visitor
        return visitor

    @property
    def visitor(self) -> CustomImportRulesVisitor:
        """Return the visitor to use for this plugin."""
        logger.info(f"Options: {self._options}")
        # logger.info(f"Visitor: {self._visitor}")
        if self._visitor is None:
            self._visitor = self.get_visitor()
        return self._visitor

    @property
    def identifiers(self) -> defaultdict[str, dict]:
        """Return the identifiers."""
        if self._identifiers is None:
            self._identifiers = self.visitor.identifiers
        return self._identifiers

    @property
    def identifiers_by_lineno(self) -> defaultdict[str, list]:
        """Return the identifiers by lineno."""
        if self._identifiers_by_lineno is None:
            self._identifiers_by_lineno = self.visitor.identifiers_by_lineno
        return self._identifiers_by_lineno

    def get_restricted_identifiers(self) -> defaultdict[str, dict[Any, Any]] | None:
        """Return the restricted identifiers."""
        return get_restricted_identifiers(
            restricted_imports=self.options.get("restricted_imports", []),
            check_module_exists=True,
        )

    @property
    def restricted_identifiers(self) -> defaultdict[str, dict[Any, Any]] | None:
        """Return the restricted identifiers."""
        if self._restricted_identifiers is None:
            self._restricted_identifiers = self.get_restricted_identifiers()
        return self._restricted_identifiers

    @property
    def options(self) -> dict:
        """Return the options."""
        return self._options

    def update_checker_settings(self, updated_options: dict) -> None:
        """Update the checker settings."""
        test_env = self.options.get("test_env", True)
        if not test_env:
            raise ValueError("Cannot update options in a non-test environment.")
        # print(f"Updated Options: {updated_options}")
        for key, value in updated_options.items():
            self._options[key] = value

    def get_custom_import_rules(self) -> CustomImportRules:
        """Return the custom import rules class."""
        return CustomImportRules(
            nodes=self.nodes,
            checker_settings=self.options.get("checker_settings", DEFAULT_CHECKER_SETTINGS),
            identifiers=self.identifiers,
            identifiers_by_lineno=self.identifiers_by_lineno,
            restricted_identifiers=self.restricted_identifiers,
            dynamic_nodes=self.visitor.dynamic_nodes,
            filename=self.filename,
            file_identifier=self.visitor.file_identifier,
            # file_identifier=self._file_identifier,
            file_root_package_name=self.visitor.file_root_package_name,
            # file_root_package_name=self._file_root_package_name,
            file_packages=self.visitor.file_packages,
        )

    def check_custom_import_rules(self) -> Generator[Any, None, None]:
        """Run the plugin."""
        # print(f"Options under: {self._options}")
        # print(f"Visitor: {self.visitor}")
        # print(f"Nodes: {self.nodes}")
        import_rules = self.get_custom_import_rules()

        for error in import_rules.check_import_rules():
            if not self.error_is_ignored(error):
                yield self.error(error)

    @staticmethod
    def error(error: ErrorMessage) -> ErrorMessage:
        """Return the error."""
        return error

    def error_is_ignored(self, error: ErrorMessage) -> bool:
        """
        Return whether the error is ignored.

        Parameters
        ----------
        error : Any
            The error to check.

        Returns
        -------
        bool
        """
        noqa_match = NOQA_INLINE_REGEXP.search(self.lines[error.lineno - 1])

        if noqa_match is None:
            return False

        codes_str = noqa_match.group("codes")

        if codes_str is None:
            return True

        codes = parse_comma_separated_list(codes_str)
        return error.code in codes
