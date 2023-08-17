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
from flake8_custom_import_rules.defaults import STDIN_IDENTIFIERS
from flake8_custom_import_rules.utils.parse_utils import NOQA_INLINE_REGEXP
from flake8_custom_import_rules.utils.parse_utils import parse_comma_separated_list

logger = logging.getLogger(__name__)


@define(slots=True, hash=False)
class CustomImportRulesChecker:
    """Custom import rules checker.

    Custom import rules checker for analyzing and validating import statements
    within Python code. It utilizes Abstract Syntax Trees (AST) to parse the code
    and apply specified import rules.

    Attributes
    ----------
    _tree : ast.AST
        Abstract syntax tree representation of the code.
    _filename : str
        The name of the file being checked.
    _lines : list[str]
        List of code lines.
    _visitor : CustomImportRulesVisitor
        Visitor object for traversing and analyzing the AST.
    _nodes : list[ParsedNode] | None
        List of parsed nodes in the AST.
    _identifiers : defaultdict[str, dict] | None
        Identifiers found in the code.
    _identifiers_by_lineno : defaultdict[str, list] | None
        Identifiers indexed by line number.
    _restricted_identifiers : defaultdict[str, dict] | None
        Identifiers that are restricted according to the rules.
    _import_rules : CustomImportRules
        Custom import rules to be applied.
    _options : dict[str, list[str] | str | bool]
        Options for configuring the checker behavior.
    """

    _tree: ast.AST = field(default=None)
    _filename: str = field(default=None)
    _lines: list[str] = field(default=None)
    _visitor: CustomImportRulesVisitor = field(default=None)

    _nodes: list[ParsedNode] | None = None
    _identifiers: defaultdict[str, dict] | None = None
    _identifiers_by_lineno: defaultdict[str, list] | None = None
    _restricted_identifiers: defaultdict[str, dict] | None = None
    _import_rules: CustomImportRules = field(init=False)

    _options: dict[str, list[str] | str | bool] = field(init=False)

    def __attrs_post_init__(self) -> None:
        """
        Initialize the CustomImportRulesChecker by parsing the code and
        setting up the necessary attributes.
        """
        if not self._lines and self._filename is not None:
            if self._filename in STDIN_IDENTIFIERS:
                self._filename = "stdin"
                self._lines = pycodestyle.stdin_get_value().splitlines(True)
            else:
                self._lines = (
                    pycodestyle.readlines(self._filename) if self._filename is not None else []
                )
        if not self._tree:
            self._tree = ast.parse("".join(self._lines))

        if not self._lines:
            self._lines = ast.unparse(self._tree).splitlines(keepends=True)

    @property
    def tree(self) -> ast.AST:
        """Return the tree: Get the abstract syntax tree of the code."""
        logger.debug(f"Tree: {self._tree}")
        return self._tree

    @property
    def filename(self) -> str:
        """Return the filename: Get the name of the file being checked."""
        if self._filename in STDIN_IDENTIFIERS:
            self._filename = "stdin"
        logger.debug(f"Filename: {self._filename}")
        assert self._filename is not None
        return self._filename

    @property
    def lines(self) -> list[str]:
        """Return the lines: Get the lines of code from the file."""
        logger.debug(f"Lines: {self._lines}")
        return self._lines

    @property
    def nodes(self) -> list[ParsedNode]:
        """Return the nodes: Get the parsed nodes from the visitor."""
        # logger.info(f"Nodes: {self._nodes}")
        logger.debug(f"Options: {self._options}")
        if self._nodes is None:
            self._nodes = self.visitor.nodes
        # logger.info(f"Nodes after setting visitor: {self._nodes}")
        return self._nodes

    @property
    def visitor(self) -> CustomImportRulesVisitor:
        """Return the visitor to use for this plugin."""
        # logger.info(f"Options: {self._options}")
        # logger.info(f"Visitor: {self._visitor}")
        if self._visitor is None:
            self._visitor = CustomImportRulesVisitor(
                base_packages=self.options.get("base_packages", []),
                filename=self.filename,
            )
            self._visitor.visit(self.tree)
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

    @property
    def restricted_identifiers(self) -> defaultdict[str, dict[Any, Any]] | None:
        """Return the restricted identifiers."""
        logger.debug(f"file_packages: {self.visitor.file_packages}")
        if self._restricted_identifiers is None:
            self._restricted_identifiers = get_restricted_identifiers(
                base_packages=self.options.get("base_packages", []),
                restricted_packages=self.options.get("restricted_packages", []),
                custom_restrictions=self.options.get("custom_restrictions", defaultdict(list)),
                file_packages=self.visitor.file_packages,
            )
        logger.debug(f"Restricted Identifiers: {self._restricted_identifiers}")
        logger.debug(f"Restricted Identifiers Keys: {self._restricted_identifiers.keys()}")
        return self._restricted_identifiers

    @property
    def options(self) -> dict:
        """Return the options."""
        return self._options

    def update_checker_settings(self, updated_options: dict) -> None:
        """
        Update the checker settings. Helper method for testing.

        Parameters
        ----------
        updated_options : dict
            The updated options to use.
        """
        test_env = self.options.get("test_env", True)
        if not test_env:
            raise ValueError("Cannot update options in a non-test environment.")
        logger.debug(f"Updated Options: {updated_options}")
        for key, value in updated_options.items():
            self._options[key] = value

    @property
    def import_rules(self) -> CustomImportRules:
        """Return the import rules."""
        visitor = self.visitor

        self._import_rules = CustomImportRules(
            nodes=self.nodes,
            dynamic_nodes=visitor.dynamic_nodes,
            identifiers=self.identifiers,
            identifiers_by_lineno=self.identifiers_by_lineno,
            restricted_identifiers=self.restricted_identifiers,
            checker_settings=self.options.get("checker_settings", DEFAULT_CHECKER_SETTINGS),
            filename=self.filename,
            file_identifier=visitor.file_identifier,
            file_root_package_name=visitor.file_root_package_name,
            file_packages=visitor.file_packages,
        )
        logger.debug(f"Restricted Identifiers: {self.restricted_identifiers}")
        return self._import_rules

    def check_custom_import_rules(self) -> Generator[ErrorMessage, None, None]:
        """Run the plugin:
        Check the code against the custom import rules and yield any
        violations.

        Yields
        ------
        ErrorMessage
        """
        import_rules = self.import_rules

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
