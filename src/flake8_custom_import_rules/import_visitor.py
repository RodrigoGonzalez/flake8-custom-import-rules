from __future__ import annotations

import ast
from typing import NamedTuple

from flake8_import_order.checker import ImportVisitor
from flake8_import_order.styles import ImportType


class ParsedImport(NamedTuple):
    """Parsed import statement"""

    type: ImportType
    is_from: bool
    modules: list[str]
    names: list[str]
    lineno: int
    col_offset: int
    level: int
    root_package: str
    file_path: str | None


class PublicImportVisitor(ImportVisitor):
    """Public class to expose `_classify_type` method."""

    application_import_names: frozenset
    application_package_names: frozenset
    imports: list

    def __init__(
        self, application_import_names: list[str] | str, application_package_names: list[str] | str
    ) -> None:
        super().__init__(application_import_names, application_package_names)

    def classify_type(self, module: str) -> ImportType:
        """Classify the type of import."""
        return self._classify_type(module)


class CustomImportRulesVisitor(ast.NodeVisitor):
    """Custom import rules node visitor."""

    errors: list[tuple[int, int, str]] = list()
    current_modules: list[str] = list()
    package_names: list[list[str]] = list()
    imports: list

    def __init__(
        self,
        application_import_names: list[str],
        standard_library_only: list[str],
        filename: str,
    ) -> None:
        """Initialize the visitor."""
        self.application_import_names = frozenset(application_import_names)
        self.standard_library_only = frozenset(standard_library_only)
        self.filename = filename

        # Use the public import visitor to classify the type of import
        # TODO: make this a class attribute
        self.import_visitor = PublicImportVisitor(application_import_names, [])

    def classify_type(self, module: str) -> ImportType:
        """
        Classify the type of import.

        Parameters
        ----------
        module : str
            The module name to classify.

        Returns
        -------
        ImportType

        Notes
        -----
        This method is a wrapper around the `classify_type` method of the
        `PublicImportVisitor` class.

        This method is inspired by the implementation in the
        `flake8-import-order` package.
        See the source code on GitHub for more details:
        https://github.com/PyCQA/flake8-import-order/blob/master/flake8_import_order/__init__.py
        """
        return self.import_visitor.classify_type(module)

    def visit_Import(self, node: ast.Import) -> None:
        """Visit an Import node."""
        # Ensures a complete traversal of the AST
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Visit an Import node."""
        # Ensures a complete traversal of the AST
        self.generic_visit(node)
