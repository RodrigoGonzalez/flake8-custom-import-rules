""" Flake8 linter for flake8-custom-import-rules. """
import ast
import optparse
import sys
from collections.abc import Generator
from typing import Any

from flake8_custom_import_rules.core.rules_checker import CustomImportRulesChecker

if sys.version_info < (3, 8):
    import importlib_metadata
else:
    import importlib.metadata as importlib_metadata


class Linter(CustomImportRulesChecker):
    name = "flake8-custom-import-rules"
    version = importlib_metadata.version(name)

    def __init__(
        self, tree: ast.AST | None = None, filename: str | None = None, lines: list | None = None
    ) -> None:
        super().__init__(tree, filename)
        self._lines = lines
        # print(f"filename: {filename}")
        # print(f"lines: {lines}")
        # print(f"tree: {tree}")

    @classmethod
    def add_options(cls, parser: Any) -> None:
        """Add options for flake8-custom-import-rules."""
        # Add options for CustomImportRulesChecker
        # cls.add_custom_rules_options(parser)

        register_opt(
            parser,
            "--base-package",
            default="my_base_module",  # TODO: change back to "" when ready
            action="store",
            type=str,
            help="Import names to consider as application-specific",
            parse_from_config=True,
            comma_separated_list=True,
        )

    @classmethod
    def parse_options(cls, options: dict) -> None:
        """Parse options for flake8-custom-import-rules."""

        # Parse options for CustomImportRulesChecker
        # cls.parse_custom_rules_options(options)

        # Parse options for ImportOrderChecker
        # ...

    def run(self) -> Generator[tuple[int, int, str, type[Any]], None, None]:
        """Run flake8-custom-import-rules."""
        # Run CustomImportRulesChecker
        # yield from self.check_custom_import_rules()

        # Run ImportOrderChecker
        # ...
        yield 1, 0, "CIR101 Custom Import Rule", type(self)


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
