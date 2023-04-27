"""Checker for dependency rules checker."""
from __future__ import annotations

import ast

import pycodestyle
from flake8_import_order.checker import ImportOrderChecker

from flake8_custom_import_rules.node_visitor import CustomImportRulesVisitor
from flake8_custom_import_rules.node_visitor import ParsedNode


class CustomImportRulesChecker(ImportOrderChecker):
    """Custom import rules checker."""

    visitor_class = CustomImportRulesVisitor
    options: dict[str, list[str] | str] = {}

    def __init__(self, filename: str | None = None, tree: ast.AST | None = None):
        """Initialize the checker."""
        self._filename = filename
        self._tree = tree
        self._lines: list[str] | None = None
        self._nodes: list[ParsedNode] | None = None
        super().__init__(self.filename, self.tree)

    @property
    def filename(self) -> str:
        """Return the filename."""
        if self._filename is None or self._filename in ["-", "/dev/stdin"]:
            self._filename = "stdin"
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
        if not self._lines:
            if self.filename == "stdin":
                lines = pycodestyle.stdin_get_value().splitlines(True)
            else:
                lines = pycodestyle.readlines(self.filename)
            self._lines = lines
        self._lines = self._lines or []
        return self._lines

    @property
    def nodes(self) -> list[ParsedNode]:
        """Return the nodes."""
        if not self._nodes:
            visitor = self.get_visitor()
            visitor.visit(self.tree)
            self._nodes = visitor.nodes

        self._nodes = self._nodes or []
        return self._nodes

    def get_visitor(self) -> CustomImportRulesVisitor:
        """Return the visitor to use for this plugin."""

        return self.visitor_class(
            self.options.get("base_packages", []),
            [],
        )
