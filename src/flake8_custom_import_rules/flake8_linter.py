""" Flake8 linter for flake8-custom-import-rules. """
import ast
import logging
import sys
from argparse import Namespace
from collections.abc import Generator
from typing import Any

from flake8.options.manager import OptionManager

from flake8_custom_import_rules.core.import_rules import ErrorMessage
from flake8_custom_import_rules.core.rules_checker import CustomImportRulesChecker
from flake8_custom_import_rules.defaults import DEFAULT_CHECKER_SETTINGS
from flake8_custom_import_rules.defaults import Settings
from flake8_custom_import_rules.defaults import register_custom_import_rules
from flake8_custom_import_rules.defaults import register_opt
from flake8_custom_import_rules.defaults import register_project_restrictions

if sys.version_info < (3, 8):
    import importlib_metadata
else:
    import importlib.metadata as importlib_metadata

logger = logging.getLogger(f"flake8_custom_import_rules.{__name__}")


STANDARD_PROJECT_LEVEL_RESTRICTION_KEYS = [
    "relative",
    "local",
    "conditional",
    "dynamic",
    "private",
    "wildcard",
    "aliased",
    "init",
    "main",
    "test",
    "conftest",
]

CUSTOM_IMPORT_RULES = [
    # "base_packages",
    "restricted_imports",
    "restricted_packages",
    "isolated_packages",
    "standard_library_only",
    "third_party_only",
    "first_party_only",
    "project_only",
]


class Linter(CustomImportRulesChecker):
    name = "flake8-custom-import-rules"
    version = importlib_metadata.version(name)
    _options: dict[str, list[str] | str] = {}

    def __init__(
        self, tree: ast.AST | None = None, filename: str | None = None, lines: list | None = None
    ) -> None:
        """Initialize flake8-custom-import-rules."""
        # print(f"\n\nTree: {tree}\n\n")
        # from flake8_custom_import_rules.defaults import normalize_path
        # print(f"\n\nFile Name: {normalize_path(filename)}\n\n")
        # print(f"\n\nLines: {lines}\n\n")
        super().__init__(tree=tree, filename=filename, lines=lines)
        logger.info(f"filename: {filename}")
        logger.debug(f"lines: {lines}")
        logger.debug(f"tree: {tree}")

    @classmethod
    def add_options(cls, option_manager: OptionManager) -> None:
        """Add options for flake8-custom-import-rules.

        For full customization of options added, see
        https://github.com/PyCQA/flake8/blob/main/src/flake8/options/manager.py
        """
        # Add options for CustomImportRulesChecker

        register_opt(
            option_manager,
            "--base-packages",
            default="",
            action="store",
            type=str,
            help=(
                "Import names to consider as first party modules (i.e., the name of "
                "your package or library). If not set, some functionality will be "
                "disabled. (default: '')"
            ),
            parse_from_config=True,
            comma_separated_list=True,
            normalize_paths=False,
        )

        register_custom_import_rules(option_manager, CUSTOM_IMPORT_RULES)

        register_opt(
            option_manager,
            "--top-level-only-imports",
            default=DEFAULT_CHECKER_SETTINGS.TOP_LEVEL_ONLY_IMPORTS,
            action="store",
            type=bool,
            help=(
                f"Only top level imports are permitted in the project. "
                f"(default: {DEFAULT_CHECKER_SETTINGS.TOP_LEVEL_ONLY_IMPORTS})"
            ),
            parse_from_config=True,
            comma_separated_list=False,
            normalize_paths=False,
        )

        # Additional project restrictions
        register_project_restrictions(option_manager, STANDARD_PROJECT_LEVEL_RESTRICTION_KEYS)

    @classmethod
    def parse_options(
        cls, option_manager: OptionManager, parse_options: Namespace, *args: Any
    ) -> None:
        """Parse options for flake8-custom-import-rules."""
        logger.debug(f"Option Manager: {option_manager}")
        logger.debug(f"Options: {parse_options}")
        logger.debug(f"Args: {args}")
        from pprint import pprint

        pprint("\nOptions:")
        pprint(parse_options)
        pprint(f"\nArgs: {args}")

        # Parse options for CustomImportRulesChecker
        base_packages: str | list = parse_options.base_packages
        if not isinstance(base_packages, list):
            base_packages = [
                pkg.strip() for pkg in parse_options.application_import_names.split(",")
            ]

        options: dict = {"base_packages": base_packages}

        # Update options with the options set in the config or on the command line
        for option_key in DEFAULT_CHECKER_SETTINGS.get_option_keys():
            option_value = getattr(parse_options, option_key.lower())
            if option_value is not None:
                options[option_key] = option_value

        parsed_options: dict = {
            "base_packages": base_packages,
            "checker_settings": Settings(**options),
            "test_env": False,
        }

        logger.debug(f"Parsed Options: {parsed_options}")
        # print(f"\n\nParsed Options: {parsed_options}")
        cls._options = parsed_options

    def error(self, error: ErrorMessage) -> tuple:
        """Return the error."""
        return (
            error.lineno,
            error.col_offset,
            f"{error.code} {error.message}",
            Linter,
        )

    def run(self) -> Generator[tuple[int, int, str, type[Any]], None, None]:
        """Run flake8-custom-import-rules."""
        # Run CustomImportRulesChecker
        yield from self.check_custom_import_rules()
