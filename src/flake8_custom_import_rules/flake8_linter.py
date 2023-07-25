""" Flake8 linter for flake8-custom-import-rules. """
import ast
import importlib.metadata
import logging
from argparse import Namespace
from collections.abc import Generator
from typing import Any

from flake8.options.manager import OptionManager

from flake8_custom_import_rules.core.error_messages import ErrorMessage
from flake8_custom_import_rules.core.rules_checker import CustomImportRulesChecker
from flake8_custom_import_rules.defaults import CUSTOM_IMPORT_RULES
from flake8_custom_import_rules.defaults import DEFAULT_CHECKER_SETTINGS
from flake8_custom_import_rules.defaults import STANDARD_PROJECT_LEVEL_RESTRICTION_KEYS
from flake8_custom_import_rules.defaults import Settings
from flake8_custom_import_rules.defaults import register_opt
from flake8_custom_import_rules.defaults import register_options

logger = logging.getLogger(f"flake8_custom_import_rules.{__name__}")


class Linter(CustomImportRulesChecker):
    """Flake8 linter for flake8-custom-import-rules.

    Attributes
    ----------
    name : str
        The name of the plugin.
    version : str
        The version of the plugin.
    _options : dict[str, list[str] | str]
        The options for the plugin.
    """

    name = "flake8-custom-import-rules"
    version = importlib.metadata.version(name)
    _options: dict[str, list[str] | str] = {}

    def __init__(
        self,
        tree: ast.AST | None = None,
        filename: str | None = None,
        lines: list | None = None,
    ) -> None:
        """Initialize flake8-custom-import-rules."""
        super().__init__(tree=tree, filename=filename, lines=lines)
        logger.info(f"filename: {filename}")
        logger.debug(f"lines: {lines}")
        logger.debug(f"tree: {tree}")

    @classmethod
    def add_options(cls, option_manager: OptionManager) -> None:
        """Add options for flake8-custom-import-rules.

        For full customization of options that can be added, see
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

        register_options(option_manager, CUSTOM_IMPORT_RULES, is_restriction=False)

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
        register_options(
            option_manager, STANDARD_PROJECT_LEVEL_RESTRICTION_KEYS, is_restriction=True
        )

    @classmethod
    def parse_options(
        cls, option_manager: OptionManager, parse_options: Namespace, *args: Any
    ) -> None:
        """Parse options for flake8-custom-import-rules."""
        logger.debug(f"Option Manager: {option_manager}")
        logger.debug(f"Options: {parse_options}")
        logger.debug(f"Args: {args}")
        print(f"\n\nOptions: {parse_options}")
        print(f"\n\nArgs: {args}")

        # Parse options for CustomImportRulesChecker
        base_packages: str | list = parse_options.base_packages
        if not isinstance(base_packages, list):
            base_packages = [
                pkg.strip() for pkg in parse_options.application_import_names.split(",")
            ]

        options: dict = {"BASE_PACKAGES": base_packages}

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
        logger.debug(f"Run Options: {self.options}")
        yield from self.check_custom_import_rules()
