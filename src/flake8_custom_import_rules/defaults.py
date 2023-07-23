"""The default settings for the flake8_custom_import_rules plugin."""
import optparse
from typing import Any

from attrs import asdict
from attrs import define
from attrs import field
from flake8.options.manager import OptionManager

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

    restricted_imports: set = field(factory=set)
    import_rules: dict = field(factory=dict)
    _dict: dict | None = None

    def __attrs_post_init__(self) -> None:
        """Post init."""
        self.restricted_imports = set(self.restricted_imports)
        self.base_packages = (
            [self.base_packages] if isinstance(self.base_packages, str) else self.base_packages
        )
        self._dict = asdict(self)

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
