"""The default settings for the flake8_custom_import_rules plugin."""
import optparse
from typing import Any

from attrs import asdict
from attrs import define
from attrs import field
from flake8.options.manager import OptionManager

# import argparse
# argparse.ArgumentParser.add_argument


POTENTIAL_DYNAMIC_IMPORTS = {
    "__import__",
    # "importlib",
    "importlib.import_module",
    "import_module",
    "importlib.util",
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

STDIN_IDENTIFIERS = {"stdin", "-", "/dev/stdin", "", None}

STANDARD_PROJECT_LEVEL_RESTRICTION_KEYS = [
    "RESTRICT_RELATIVE_IMPORTS",
    "RESTRICT_LOCAL_IMPORTS",
    "RESTRICT_CONDITIONAL_IMPORTS",
    "RESTRICT_DYNAMIC_IMPORTS",
    "RESTRICT_PRIVATE_IMPORTS",
    "RESTRICT_WILDCARD_IMPORTS",
    "RESTRICT_ALIASED_IMPORTS",
    "RESTRICT_FUTURE_IMPORTS",
    "RESTRICT_INIT_IMPORTS",
    "RESTRICT_MAIN_IMPORTS",
    "RESTRICT_TEST_IMPORTS",
    "RESTRICT_CONFTEST_IMPORTS",
]

CUSTOM_IMPORT_RULES = [
    # "BASE_PACKAGES",
    "IMPORT_RESTRICTIONS",
    "RESTRICTED_PACKAGES",
    "ISOLATED_MODULES",
    "STD_LIB_ONLY",
    "THIRD_PARTY_ONLY",
    "FIRST_PARTY_ONLY",
    "PROJECT_ONLY",
    "BASE_PACKAGE_ONLY",
]


def convert_to_list(value: str | list[str] | None) -> list:
    """Convert a string to a list and strip leading and trailing whitespace."""
    if isinstance(value, str):
        return [item.strip() for item in value.split(",")]
    return [] if value is None else value


@define(slots=True)
class Settings:
    """The default settings for the flake8_custom_import_rules plugin."""

    # Set Defaults for Project Import Restrictions
    TOP_LEVEL_ONLY_IMPORTS: bool = True
    RESTRICT_RELATIVE_IMPORTS: bool = True
    RESTRICT_LOCAL_IMPORTS: bool = True
    RESTRICT_CONDITIONAL_IMPORTS: bool = False
    RESTRICT_DYNAMIC_IMPORTS: bool = True
    RESTRICT_PRIVATE_IMPORTS: bool = True
    RESTRICT_WILDCARD_IMPORTS: bool = True
    RESTRICT_ALIASED_IMPORTS: bool = False
    RESTRICT_FUTURE_IMPORTS: bool = False

    RESTRICT_INIT_IMPORTS: bool = True
    RESTRICT_MAIN_IMPORTS: bool = True
    RESTRICT_TEST_IMPORTS: bool = True
    RESTRICT_CONFTEST_IMPORTS: bool = True

    # Set Defaults for Custom Import Rules

    BASE_PACKAGES: list = field(factory=list, converter=convert_to_list)
    IMPORT_RESTRICTIONS: list = field(factory=list, converter=convert_to_list)
    RESTRICTED_PACKAGES: list = field(factory=list, converter=convert_to_list)
    ISOLATED_MODULES: list = field(factory=list, converter=convert_to_list)
    STD_LIB_ONLY: list = field(factory=list, converter=convert_to_list)
    THIRD_PARTY_ONLY: list = field(factory=list, converter=convert_to_list)
    FIRST_PARTY_ONLY: list = field(factory=list, converter=convert_to_list)
    PROJECT_ONLY: list = field(factory=list, converter=convert_to_list)
    BASE_PACKAGE_ONLY: list = field(factory=list, converter=convert_to_list)

    _import_rules: dict = field(factory=dict)

    # def __attrs_post_init__(self) -> None:
    #     """Post init."""

    @property
    def import_rules(self) -> dict:
        """Return the settings as a dictionary."""
        if not self._import_rules:
            self._import_rules = asdict(self)
        return self._import_rules

    @property
    def dict(self) -> dict:
        """Return the settings as a dictionary."""
        return asdict(self)

    def get_option_keys(self) -> list:
        """Return the options as a dictionary."""
        return [key for key in self.dict.keys() if key.isupper()]

    def get_settings_value(self, key: str) -> Any:
        """Return the settings as a dictionary."""
        if not hasattr(self, key):
            raise KeyError(f"Settings '{key}' does not exist.")
        return self.dict[key]


DEFAULT_CHECKER_SETTINGS = Settings()


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

    Parameters
    ----------
    option_manager : OptionManager
        The option manager.
    item : list | str
        The item or list of items to register.
    is_restriction : bool, optional
        Whether the item is a restriction, meaning the option is either True
        or False, by default True (i.e., we are registering a restriction).
    option_default_value : str | bool, optional
        The default value for the option, by default "".
    help_string : str | None, optional
        The help string for the option, by default None.
    kwargs : Any
        Additional keyword arguments to pass to register_opt.
    """
    if isinstance(item, list):
        for single_item in item:
            register_options(
                option_manager, single_item, is_restriction, option_default_value, **kwargs
            )
        return

    assert isinstance(item, str), f"Item must be a str. Got {type(item).__name__} for {item}."

    if is_restriction:
        setting_key = item.upper()
        option_default_value = DEFAULT_CHECKER_SETTINGS.get_settings_value(setting_key)
        if not help_string:
            help_string = (
                f"Disables {item.title()} Imports for this project. "
                f"(default: {option_default_value})"
            )
    else:
        setting_key = f"{item.replace('_', '-').lower()}"
        help_string = f"{setting_key}. (default: {option_default_value})"

    if not isinstance(option_default_value, bool if is_restriction else str):
        raise TypeError(
            f"Default value for {setting_key} must be a {bool if is_restriction else str} "
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
