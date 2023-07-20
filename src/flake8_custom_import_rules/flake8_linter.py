""" Flake8 linter for flake8-custom-import-rules. """
import ast
import logging
import optparse
import sys
from argparse import Namespace
from collections.abc import Generator
from typing import Any

from flake8.options.manager import OptionManager

from flake8_custom_import_rules.core.import_rules import ErrorMessage
from flake8_custom_import_rules.core.rules_checker import CustomImportRulesChecker
from flake8_custom_import_rules.defaults import DEFAULT_CHECKER_SETTINGS
from flake8_custom_import_rules.defaults import Settings

if sys.version_info < (3, 8):
    import importlib_metadata
else:
    import importlib.metadata as importlib_metadata

logger = logging.getLogger(f"flake8_custom_import_rules.{__name__}")


class Linter(CustomImportRulesChecker):
    name = "flake8-custom-import-rules"
    version = importlib_metadata.version(name)
    _options: dict[str, list[str] | str] = {}

    def __init__(
        self, tree: ast.AST | None = None, filename: str | None = None, lines: list | None = None
    ) -> None:
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
        # cls.add_custom_rules_options(option_manager)

        register_opt(
            option_manager,
            "--base-packages",
            default="my_base_module",  # TODO: change back to "" when ready
            action="store",
            type=str,
            help=(
                "Import names to consider as first party modules (i.e., the name of "
                "your package or library)."
            ),
            parse_from_config=True,
            comma_separated_list=True,
            normalize_paths=False,
        )

        register_opt(
            option_manager,
            "--top-level-only",
            default=DEFAULT_CHECKER_SETTINGS.TOP_LEVEL_ONLY,
            action="store",
            type=bool,
            help="Only top level imports are permitted in the project.",
            parse_from_config=True,
            comma_separated_list=False,
            normalize_paths=False,
        )

        register_opt(
            option_manager,
            "--restrict-relative-imports",
            default=DEFAULT_CHECKER_SETTINGS.RESTRICT_RELATIVE_IMPORTS,
            action="store",
            type=bool,
            help="Relative imports are currently disabled for this project.",
            parse_from_config=True,
            comma_separated_list=False,
            normalize_paths=False,
        )

        register_opt(
            option_manager,
            "--restrict-local-imports",
            default=DEFAULT_CHECKER_SETTINGS.RESTRICT_LOCAL_IMPORTS,
            action="store",
            type=bool,
            help="Local imports are currently disabled for this project.",
            parse_from_config=True,
            comma_separated_list=False,
            normalize_paths=False,
        )

        register_opt(
            option_manager,
            "--restrict-conditional-imports",
            default=DEFAULT_CHECKER_SETTINGS.RESTRICT_CONDITIONAL_IMPORTS,
            action="store",
            type=bool,
            help="Conditional imports are currently disabled for this project.",
            parse_from_config=True,
            comma_separated_list=False,
            normalize_paths=False,
        )

        register_opt(
            option_manager,
            "--restrict-dynamic-imports",
            default=DEFAULT_CHECKER_SETTINGS.RESTRICT_DYNAMIC_IMPORTS,
            action="store",
            type=bool,
            help="Dynamic imports are currently disabled for this project.",
            parse_from_config=True,
            comma_separated_list=False,
            normalize_paths=False,
        )

        register_opt(
            option_manager,
            "--restrict-private-imports",
            default=DEFAULT_CHECKER_SETTINGS.RESTRICT_PRIVATE_IMPORTS,
            action="store",
            type=bool,
            help="Private imports are currently disabled for this project.",
            parse_from_config=True,
            comma_separated_list=False,
            normalize_paths=False,
        )

        register_opt(
            option_manager,
            "--restrict-wildcard-imports",
            default=DEFAULT_CHECKER_SETTINGS.RESTRICT_WILDCARD_IMPORTS,
            action="store",
            type=bool,
            help="Wildcard/star imports are currently disabled for this project.",
            parse_from_config=True,
            comma_separated_list=False,
            normalize_paths=False,
        )

        register_opt(
            option_manager,
            "--restrict-aliased-imports",
            default=DEFAULT_CHECKER_SETTINGS.RESTRICT_ALIASED_IMPORTS,
            action="store",
            type=bool,
            help="Dynamic imports are currently disabled for this project.",
            parse_from_config=True,
            comma_separated_list=False,
            normalize_paths=False,
        )

        register_opt(
            option_manager,
            "--restrict-init-imports",
            default=DEFAULT_CHECKER_SETTINGS.RESTRICT_INIT_IMPORTS,
            action="store",
            type=bool,
            help="Init imports are currently disabled for this project.",
            parse_from_config=True,
            comma_separated_list=False,
            normalize_paths=False,
        )

        register_opt(
            option_manager,
            "--restrict-test-imports",
            default=DEFAULT_CHECKER_SETTINGS.RESTRICT_TEST_IMPORTS,
            action="store",
            type=bool,
            help="Test imports are currently disabled for this project.",
            parse_from_config=True,
            comma_separated_list=False,
            normalize_paths=False,
        )

        register_opt(
            option_manager,
            "--restrict-conftest-imports",
            default=DEFAULT_CHECKER_SETTINGS.RESTRICT_CONFTEST_IMPORTS,
            action="store",
            type=bool,
            help="Conftest imports are currently disabled for this project.",
            parse_from_config=True,
            comma_separated_list=False,
            normalize_paths=False,
        )

    @classmethod
    def parse_options(
        cls, option_manager: OptionManager, parse_options: Namespace, *args: Any
    ) -> None:
        """Parse options for flake8-custom-import-rules."""
        logger.debug(f"Option Manager: {option_manager}")
        logger.debug(f"Options: {parse_options}")
        logger.debug(f"Args: {args}")
        # print(f"\nOption Manager: {option_manager}")
        # print(f"\nOptions: {parse_options}")
        # print(f"\nArgs: {args}")
        # Parse options for CustomImportRulesChecker
        # cls.parse_custom_rules_options(options)

        base_packages: str | list = parse_options.base_packages
        if not isinstance(base_packages, list):
            base_packages = [
                pkg.strip() for pkg in parse_options.application_import_names.split(",")
            ]

        options: dict = {"base_package": base_packages}
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
        # print(f"Parsed Options: {parsed_options}")
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
        # print(f"Slots: {self.__slots__}")
        yield from self.check_custom_import_rules()

    # def setup_test_run(self, options: dict) -> None:
    #     """Run flake8-custom-import-rules."""
    #     self._options = options
    #     # yield from self.check_custom_import_rules()


def register_opt(self: OptionManager, *args: Any, **kwargs: Any) -> None:
    """Register options for flake8-custom-import-rules."""
    try:
        # Flake8 3.x registration
        self.add_option(*args, **kwargs)
    except (optparse.OptionError, TypeError):
        # Flake8 2.x registration
        parse_from_config = kwargs.pop("parse_from_config", False)
        kwargs.pop("comma_separated_list", False)
        kwargs.pop("normalize_paths", False)
        self.add_option(*args, **kwargs)
        if parse_from_config:
            self.config_options.append(args[-1].lstrip("-"))
