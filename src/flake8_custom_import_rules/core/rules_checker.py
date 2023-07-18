"""Checker for dependency rules checker."""
import ast
from typing import Any
from typing import Generator

import pycodestyle

from flake8_custom_import_rules.core.node_visitor import CustomImportRulesVisitor
from flake8_custom_import_rules.core.node_visitor import ParsedNode
from flake8_custom_import_rules.utils.parse_utils import NOQA_INLINE_REGEXP
from flake8_custom_import_rules.utils.parse_utils import parse_comma_separated_list


class CustomImportRulesChecker:
    """Custom import rules checker."""

    options: dict[str, list[str] | str] = {}

    def __init__(self, tree: ast.AST | None = None, filename: str | None = None):
        """Initialize the checker."""
        self._tree = tree
        self._filename = filename
        self._lines: list[str] | None = None
        self._nodes: list[ParsedNode] | None = None

    @property
    def filename(self) -> str:
        """Return the filename."""
        if self._filename is None or self._filename in {"-", "/dev/stdin"}:
            return "stdin"
        return self._filename

    @property
    def tree(self) -> ast.AST:
        """Return the tree."""
        if not self._tree:
            self._tree = ast.parse("".join(self.lines))
        return self._tree

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
            visitor = self.get_visitor()
            self._nodes = visitor.nodes
        return self._nodes

    @staticmethod
    def error(error: Any) -> Any:
        """Return the error."""
        return error

    def get_visitor(self) -> CustomImportRulesVisitor:
        """Return the visitor to use for this plugin."""

        visitor = CustomImportRulesVisitor(
            self.options.get("base_packages", []),
            [],
            filename=self.filename,
        )
        visitor.visit(self.tree)
        return visitor

    def error_is_ignored(self, error: Any) -> bool:
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
    def __init__(self, tree: ast.AST | None = None, filename: str | None = None):
        """Initialize the checker."""
        super().__init__(tree, filename)

    def run(self) -> Generator[Any, None, None]:
        """Run the plugin."""
        self.options["base_packages"] = ["my_base_module"]
        for node in self.nodes:
            yield node.lineno, node.col_offset, node, type(self)

    def get_run_list(self) -> list:
        """Return the run list."""
        return list(self.run())
