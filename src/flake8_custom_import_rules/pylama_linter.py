""" Pylama linter for flake8-custom-import-rules. """
import sys
from collections.abc import Generator
from typing import Any

from pylama.lint import Linter as BaseLinter

from flake8_custom_import_rules.core.error_messages import ErrorMessage
from flake8_custom_import_rules.core.rules_checker import CustomImportRulesChecker

if sys.version_info < (3, 8):
    import importlib_metadata
else:
    import importlib.metadata as importlib_metadata


class Linter(CustomImportRulesChecker, BaseLinter):
    name = "flake8-custom-import-rules"
    version = importlib_metadata.version(name)
    ast_tree = None
    _filename = None

    def __init__(self) -> None:
        super().__init__(None, None)

    @classmethod
    def allow(cls, path: str) -> bool:
        """Check if path is allowed."""
        return path.endswith(".py")

    def error(self, error: ErrorMessage) -> dict:
        """Convert an error message to a dictionary."""
        return {
            "lnum": error.lineno,
            "col": error.col_offset,
            "text": error.message,
            "type": error.code,
        }

    def run(self, path: str, **meta: dict) -> Generator[Any, None, None]:
        self._filename = path
        # meta.setdefault("import_order_style", DEFAULT_IMPORT_ORDER_STYLE)
        # meta["import_order_style"] = lookup_entry_point(
        #     meta["import_order_style"],
        # )
        self._options = meta

        yield from self.check_order()
