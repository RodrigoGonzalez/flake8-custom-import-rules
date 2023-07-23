"""The default settings for the flake8_custom_import_rules plugin."""
import optparse
import os
from typing import Any

from attrs import asdict
from attrs import define
from attrs import field
from flake8.options.manager import OptionManager

# import argparse
# argparse.ArgumentParser.add_argument


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
    # "BASE_PACKAGES",
    "RESTRICTED_IMPORTS",
    "RESTRICTED_PACKAGES",
    "ISOLATED_PACKAGES",
    "STD_LIB_ONLY",
    "THIRD_PARTY_ONLY",
    "FIRST_PARTY_ONLY",
    "PROJECT_ONLY",
]

POTENTIAL_DYNAMIC_IMPORTS = {
    "__import__",
    "importlib",
    "importlib.import_module",
    "import_module",
    # "pkgutil",
    "pkgutil.get_loader",
    "get_loader",
    "pkgutil.iter_modules",
    "iter_modules",
    "sys.modules",
    "modules",
    "zipimport",
    "zipimport.zipimporter",
    "zipimporter",
    "zipimporter.load_module",
    "eval",
    "exec",
}


def convert_to_list(value: str | list[str] | None) -> list:
    """Convert a string to a list and strip leading and trailing whitespace."""
    if isinstance(value, str):
        return [item.strip() for item in value.split(",")]
    return [] if value is None else value


@define(slots=True)
class Settings:
    """The default settings for the flake8_custom_import_rules plugin."""

    BASE_PACKAGES: str | list[str] | None = None
    RESTRICTED_IMPORTS: str | list[str] | None = None
    RESTRICTED_PACKAGES: str | list[str] | None = None
    ISOLATED_PACKAGES: str | list[str] | None = None
    STD_LIB_ONLY: str | list[str] | None = None
    THIRD_PARTY_ONLY: str | list[str] | None = None
    FIRST_PARTY_ONLY: str | list[str] | None = None
    PROJECT_ONLY: str | list[str] | None = None

    # Set Defaults for Project Import Restrictions
    TOP_LEVEL_ONLY_IMPORTS: bool = True
    RESTRICT_RELATIVE_IMPORTS: bool = True
    RESTRICT_LOCAL_IMPORTS: bool = True
    RESTRICT_CONDITIONAL_IMPORTS: bool = False
    RESTRICT_DYNAMIC_IMPORTS: bool = True
    RESTRICT_PRIVATE_IMPORTS: bool = True
    RESTRICT_WILDCARD_IMPORTS: bool = True
    RESTRICT_ALIASED_IMPORTS: bool = False

    RESTRICT_INIT_IMPORTS: bool = True
    RESTRICT_MAIN_IMPORTS: bool = True
    RESTRICT_TEST_IMPORTS: bool = True
    RESTRICT_CONFTEST_IMPORTS: bool = True

    import_rules: dict = field(factory=dict)
    _dict: dict | None = None

    def __attrs_post_init__(self) -> None:
        """Post init."""
        self._dict = asdict(self)
        self.BASE_PACKAGES = convert_to_list(self.BASE_PACKAGES)
        self.RESTRICTED_IMPORTS = convert_to_list(self.RESTRICTED_IMPORTS)
        self.RESTRICTED_PACKAGES = convert_to_list(self.RESTRICTED_PACKAGES)
        self.ISOLATED_PACKAGES = convert_to_list(self.ISOLATED_PACKAGES)
        self.STD_LIB_ONLY = convert_to_list(self.STD_LIB_ONLY)
        self.THIRD_PARTY_ONLY = convert_to_list(self.THIRD_PARTY_ONLY)
        self.FIRST_PARTY_ONLY = convert_to_list(self.FIRST_PARTY_ONLY)
        self.PROJECT_ONLY = convert_to_list(self.PROJECT_ONLY)

    @property
    def dict(self) -> dict:
        """Return the settings as a dictionary."""
        if not self._dict:
            self._dict = asdict(self)
        return self._dict

    def get_option_keys(self) -> list:
        """Return the options as a dictionary."""
        return [key for key in self.dict.keys() if key.isupper()]

    def get_settings_value(self, key: str) -> Any:
        """Return the settings as a dictionary."""
        if not hasattr(self, key):
            raise KeyError(f"Settings '{key}' does not exist.")
        return self.dict[key]


DEFAULT_CHECKER_SETTINGS = Settings()


def register_custom_import_rules(
    option_manager: OptionManager, custom_import_rule: list | str, **kwargs: Any
) -> None:
    """Register custom import rules.

    If using short options, set both the following options:
        short_option_name: str | _ARG = _ARG.NO
        long_option_name: str | _ARG = _ARG.NO

    If using long options, just pass a single string into register_opt.
    """
    if isinstance(custom_import_rule, list):
        for rule in custom_import_rule:
            register_custom_import_rules(option_manager, rule, **kwargs)
        return

    assert isinstance(custom_import_rule, str), (
        f"Project restrictions must be a str. "
        f"Got {type(custom_import_rule).__name__} for {custom_import_rule}."
    )

    setting_key = f"{custom_import_rule.replace('_', '-').lower()}"

    help_string = f"{setting_key}. (default: '')"

    register_opt(
        option_manager,
        f"--{custom_import_rule.replace('_', '-').lower()}",
        default="",
        action="store",
        type=str,
        help=help_string,
        parse_from_config=True,
        comma_separated_list=True,
        normalize_paths=False,
    )


def register_options(
    option_manager: OptionManager,
    item: list | str,
    is_restriction: bool = True,
    option_default_value: str | bool = "",
    help_string: str | None = None,
    **kwargs: Any,
) -> None:
    """Register rules or restrictions.

    If using short options, set both the following options:
        short_option_name: str | _ARG = _ARG.NO
        long_option_name: str | _ARG = _ARG.NO

    If using long options, just pass a single string into register_opt.
    """
    if isinstance(item, list):
        for single_item in item:
            register_options(
                option_manager, single_item, is_restriction, option_default_value, **kwargs
            )
        return

    assert isinstance(item, str), f"Item must be a str. Got {type(item).__name__} for {item}."

    if is_restriction:
        setting_key = f"RESTRICT_{item.upper()}_IMPORTS"
        option_default_value = DEFAULT_CHECKER_SETTINGS.get_settings_value(setting_key)
        if not help_string:
            help_string = (
                f"Disables {item.title()} Imports for this project. "
                f"(default: {option_default_value})"
            )
    else:
        setting_key = f"{item.replace('_', '-').lower()}"
        help_string = f"{setting_key}. (default: {option_default_value})"

    if not isinstance(option_default_value, (str, bool)):
        raise TypeError(
            f"Default value for {setting_key} must be a {str if is_restriction else bool} "
            f"if registering as a {'restriction' if is_restriction else 'rule'}."
        )

    register_opt(
        option_manager,
        f"--{setting_key.lower()}",
        default=option_default_value,
        action="store",
        type=type(option_default_value),
        help=help_string,
        parse_from_config=True,
        comma_separated_list=not is_restriction,
        normalize_paths=False,
    )


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


def normalize_path(path: str, parent: str = os.curdir) -> str:
    """Normalize a single-path.

    :returns:
        The normalized path.
    """
    # NOTE(sigmavirus24): Using os.path.sep and os.path.altsep allow for
    # Windows compatibility with both Windows-style paths (c:\foo\bar) and
    # Unix style paths (/foo/bar).
    separator = os.path.sep
    # NOTE(sigmavirus24): os.path.altsep may be None
    alternate_separator = os.path.altsep or ""
    if path == "." or separator in path or (alternate_separator and alternate_separator in path):
        path = os.path.abspath(os.path.join(parent, path))
    return path.rstrip(separator + alternate_separator)
