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


@define(slots=True)
class Settings:
    """The default settings for the flake8_custom_import_rules plugin."""

    base_packages: str | list[str] | None = None
    restricted_imports: str | list[str] | None = None
    restricted_packages: str | list[str] | None = None
    isolated_packages: str | list[str] | None = None
    standard_library_only: str | list[str] | None = None
    third_party_only: str | list[str] | None = None
    first_party_only: str | list[str] | None = None
    project_only: str | list[str] | None = None

    TOP_LEVEL_ONLY_IMPORTS: bool = True
    RESTRICT_RELATIVE_IMPORTS: bool = True
    RESTRICT_LOCAL_IMPORTS: bool = True
    RESTRICT_CONDITIONAL_IMPORTS: bool = True
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
        self.base_packages = (
            [self.base_packages] if isinstance(self.base_packages, str) else self.base_packages
        )
        self.restricted_imports = (
            [self.restricted_imports]
            if isinstance(self.restricted_imports, str)
            else self.restricted_imports
        )

        self.restricted_packages = (
            [self.restricted_packages]
            if isinstance(self.restricted_packages, str)
            else self.restricted_packages
        )

        self.isolated_packages = (
            [self.isolated_packages]
            if isinstance(self.isolated_packages, str)
            else self.isolated_packages
        )

        self.standard_library_only = (
            [self.standard_library_only]
            if isinstance(self.standard_library_only, str)
            else self.standard_library_only
        )

        self.third_party_only = (
            [self.third_party_only]
            if isinstance(self.third_party_only, str)
            else self.third_party_only
        )

        self.first_party_only = (
            [self.first_party_only]
            if isinstance(self.first_party_only, str)
            else self.first_party_only
        )

        self.project_only = (
            [self.project_only] if isinstance(self.project_only, str) else self.project_only
        )

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


def register_project_restrictions(
    option_manager: OptionManager, project_restriction: list | str, **kwargs: Any
) -> None:
    """Register project restrictions.

    If using short options, set both the following options:
        short_option_name: str | _ARG = _ARG.NO
        long_option_name: str | _ARG = _ARG.NO

    If using long options, just pass a single string into register_opt.
    """
    if isinstance(project_restriction, list):
        for restriction in project_restriction:
            register_project_restrictions(option_manager, restriction, **kwargs)
        return

    assert isinstance(project_restriction, str), (
        f"Project restrictions must be a str. "
        f"Got {type(project_restriction).__name__} for {project_restriction}."
    )

    setting_key = f"RESTRICT_{project_restriction.upper()}_IMPORTS"
    default_value = DEFAULT_CHECKER_SETTINGS.get_settings_value(setting_key)

    if not isinstance(default_value, bool):
        raise TypeError(
            f"Project restrictions must be a bool. Default value for "
            f"{setting_key} must be a bool if registering as a project restriction."
        )

    help_string = (
        f"Disables {project_restriction.title()} Imports for this project. "
        f"(default: {default_value})"
    )

    register_opt(
        option_manager,
        f"--restrict-{project_restriction.lower()}-imports",
        default=default_value,
        action="store",
        type=bool,
        help=help_string,
        parse_from_config=True,
        comma_separated_list=False,
        normalize_paths=False,
    )


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
        f"--{custom_import_rule.replace('-', '_').lower()}",
        default="",
        action="store",
        type=str,
        help=help_string,
        parse_from_config=True,
        comma_separated_list=True,
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
