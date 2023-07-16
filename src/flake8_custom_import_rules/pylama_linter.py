""" Pylama linter for flake8-custom-import-rules. """
from collections.abc import Generator
from typing import Any

from flake8_import_order.checker import DEFAULT_IMPORT_ORDER_STYLE
from flake8_import_order.styles import lookup_entry_point
from pylama.lint import Linter as BaseLinter

from flake8_custom_import_rules import __version__
from flake8_custom_import_rules.import_rules import ErrorMessage
from flake8_custom_import_rules.rules_checker import CustomImportRulesChecker


class Linter(CustomImportRulesChecker, BaseLinter):
    name = "custom-import-rules"
    version = __version__

    def __init__(self) -> None:
        super().__init__(None, None)

    @classmethod
    def allow(cls, path: str) -> bool:
        """Check if path is allowed."""
        return path.endswith(".py")

    def error(self, error: ErrorMessage) -> dict:
        return {
            "lnum": error.lineno,
            "col": 0,
            "text": error.message,
            "type": error.code,
        }

    def run(self, path: str, **meta: Any) -> Generator[Any, None, None]:
        self._filename = path
        self.ast_tree = None
        meta.setdefault("import_order_style", DEFAULT_IMPORT_ORDER_STYLE)
        meta["import_order_style"] = lookup_entry_point(
            meta["import_order_style"],
        )
        self.options = meta

        yield from self.check_order()
