from __future__ import annotations

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
