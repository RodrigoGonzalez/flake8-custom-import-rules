"""Checker for dependency rules checker."""
import ast
from collections import defaultdict
from typing import Any
from typing import Generator

import pycodestyle
from attrs import define
from attrs import field

from flake8_custom_import_rules.core.error_messages import ErrorMessage
from flake8_custom_import_rules.core.import_rules import CustomImportRules
from flake8_custom_import_rules.core.node_visitor import CustomImportRulesVisitor
from flake8_custom_import_rules.core.nodes import ParsedFromImport
from flake8_custom_import_rules.core.nodes import ParsedImport
from flake8_custom_import_rules.core.nodes import ParsedNode
from flake8_custom_import_rules.defaults import DEFAULT_CHECKER_SETTINGS
from flake8_custom_import_rules.utils.parse_utils import NOQA_INLINE_REGEXP
from flake8_custom_import_rules.utils.parse_utils import parse_comma_separated_list


@define(slots=True, hash=False)
class CustomImportRulesChecker:
    """Custom import rules checker."""

    _tree: ast.AST | None = None
    _filename: str | None = None
    _lines: list[str] | None = None
    _nodes: list[ParsedNode] | None = None
    _visitor: CustomImportRulesVisitor | None = None
    _identifiers: defaultdict[str, dict] | None = None
    _identifiers_by_lineno: defaultdict[str, list] | None = None
    _options: dict[str, list[str] | str] = field(init=False)

    @property
    def tree(self) -> ast.AST:
        """Return the tree."""
        if not self._tree:
            self._tree = ast.parse("".join(self.lines))
        return self._tree

    @property
    def filename(self) -> str:
        """Return the filename."""
        if self._filename is None or self._filename in {"-", "/dev/stdin"}:
            return "stdin"
        return self._filename

    @property
    def lines(self) -> list[str]:
        """Return the lines."""
        if self._lines is None:
            self._lines = (
                pycodestyle.stdin_get_value().splitlines(True)
                if self.filename == "stdin"
                else pycodestyle.readlines(self.filename)
            )
        return self._lines

    @property
    def nodes(self) -> list[ParsedNode]:
        """Return the nodes."""
        if self._nodes is None:
            if self._visitor is None:
                visitor = self.visitor
                self._nodes = visitor.nodes
            else:
                self._nodes = self.visitor.nodes
        return self._nodes

    @property
    def visitor(self) -> CustomImportRulesVisitor:
        """Return the visitor to use for this plugin."""
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

    def get_visitor(self) -> CustomImportRulesVisitor:
        """Return the visitor to use for this plugin."""
        # print(f"\\nOptions: {self.options}\n\n")
        visitor = CustomImportRulesVisitor(
            base_packages=self.options.get("base_packages", []),
            filename=self.filename,
        )
        visitor.visit(self.tree)
        return visitor

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
            dynamic_nodes=self.visitor.dynamic_nodes,
            filename=self.filename,
            file_identifier=self.visitor.file_identifier,
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


class BaseCustomImportRulePlugin(CustomImportRulesChecker):
    _run_list: list

    def __init__(
        self, tree: ast.AST | None = None, filename: str | None = None, lines: list | None = None
    ) -> None:
        """Initialize the checker."""
        super().__init__(tree=tree, filename=filename, lines=lines)
        self._options = {}

    def run(self) -> Generator[Any, None, None]:
        """Run the plugin."""
        self._options["base_packages"] = ["my_base_module"]
        for node in self.nodes:
            yield node.lineno, node.col_offset, node, type(self)

    def get_run_list(self, sort: bool = True) -> list:
        """Return the run list."""
        self._run_list = list(self.run())
        if sort:
            self._run_list.sort(key=lambda x: x[0])
        return self._run_list

    def get_import_nodes(self) -> list[ParsedNode]:
        """Return the import nodes."""
        return [
            node for node in self._run_list if isinstance(node[2], (ParsedImport, ParsedFromImport))
        ]
