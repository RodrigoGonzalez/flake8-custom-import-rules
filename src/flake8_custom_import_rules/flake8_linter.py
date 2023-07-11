""" Flake8 linter for flake8-custom-import-rules. """
import ast
import optparse
from collections.abc import Generator
from typing import Any

from flake8_import_order.styles import list_entry_points

from flake8_custom_import_rules import __version__
from flake8_custom_import_rules.rules_checker import CustomImportRulesChecker


class Linter(CustomImportRulesChecker):
    name = "custom-import-rules"
    version = __version__

    def __init__(
        self, tree: ast.AST | None = None, filename: str | None = None, lines: list | None = None
    ) -> None:
        super().__init__(filename, tree)
        self._lines = lines

    @classmethod
    def add_options(cls, parser: Any) -> None:
        """Add options for flake8-custom-import-rules."""
        # Add options for CustomImportRulesChecker
        # cls.add_custom_rules_options(parser)

        # Add options for ImportOrderChecker
        # ...

    @staticmethod
    def list_available_styles() -> list[str]:
        """List available styles."""
        entry_points = list_entry_points()
        return sorted(entry_point.name for entry_point in entry_points)

    @classmethod
    def parse_options(cls, options: dict) -> None:
        """Parse options for flake8-custom-import-rules."""

        # Parse options for CustomImportRulesChecker
        # cls.parse_custom_rules_options(options)

        # Parse options for ImportOrderChecker
        # ...

    def run(self) -> Generator[Any, None, None]:
        # Run CustomImportRulesChecker
        # yield from self.check_custom_import_rules()

        # Run ImportOrderChecker
        # ...
        raise NotImplementedError()


def register_opt(parser: Any, *args: Any, **kwargs: Any) -> None:
    """Register options for flake8-custom-import-rules."""
    try:
        # Flake8 3.x registration
        parser.add_option(*args, **kwargs)
    except (optparse.OptionError, TypeError):
        # Flake8 2.x registration
        parse_from_config = kwargs.pop("parse_from_config", False)
        kwargs.pop("comma_separated_list", False)
        kwargs.pop("normalize_paths", False)
        parser.add_option(*args, **kwargs)
        if parse_from_config:
            parser.config_options.append(args[-1].lstrip("-"))
