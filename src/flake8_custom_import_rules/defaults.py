"""The default settings for the flake8_custom_import_rules plugin."""

import optparse
from collections import defaultdict
from typing import Any

from attrs import asdict
from attrs import define
from attrs import field
from flake8.options.manager import OptionManager

POTENTIAL_DYNAMIC_IMPORTS = {
    "__import__",
    "importlib.import_module",
    "import_module",
    "importlib.util.find_spec",
    "find_spec",
    "importlib.util.spec_from_loader",
    "spec_from_loader",
    "importlib.util.module_from_spec",
    "module_from_spec",
    "importlib.util.exec_module",
    "exec_module",
    # "importlib.abc.Loader.create_module",
    # "importlib.abc.Loader.exec_module",
    # "importlib.abc.InspectLoader.get_code",
    # "importlib.abc.InspectLoader.get_source",
    # "importlib.machinery.SourceFileLoader.get_code",
    # "importlib.machinery.SourceFileLoader.get_source",
    # "importlib.machinery.ExtensionFileLoader.get_code",
    # "importlib.machinery.ExtensionFileLoader.get_source",
    # "importlib.machinery.SourcelessFileLoader.get_code",
    # "importlib.machinery.SourcelessFileLoader.get_source",
    # "importlib.machinery.SourceLoader.get_code",
    # "importlib.machinery.SourceLoader.get_source",
    "imp.find_module",
    "find_module",
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
    "load_module",
    "eval",
    "exec",
}

STDIN_IDENTIFIERS = {"stdin", "-", "/dev/stdin", "", None}

STANDARD_PROJECT_LEVEL_RESTRICTION_KEYS = [
    "RESTRICT_RELATIVE_IMPORTS",
    "RESTRICT_LOCAL_SCOPE_IMPORTS",
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
    "BASE_PACKAGES",
    "CUSTOM_RESTRICTIONS",
    "RESTRICTED_PACKAGES",
    "STD_LIB_ONLY",
    "PROJECT_ONLY",
    "BASE_PACKAGE_ONLY",
    "FIRST_PARTY_ONLY",
    "THIRD_PARTY_ONLY",
    "STANDALONE_MODULES",
]


def convert_to_list(value: str | list[str] | None) -> list:
    """
    Convert a string to a list and strip leading and trailing whitespace.

    Parameters
    ----------
    value : str | list[str] | None
        The value to convert to a list.

    Returns
    -------
    list[str]
        The converted list.
    """
    if value is None:
        return []
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item != ""]
    return convert_to_list(",".join(value)) if isinstance(value, list) else []


def convert_to_dict(value: str | list[str] | None, delimiter: str | None = ":") -> defaultdict:
    """
    Convert a string to a dict and strip leading and trailing whitespace.

    Parameters
    ----------
    value : str | list[str] | None
        The value to convert to a dict.
    delimiter : str, default=":"
        The delimiter to use to split the string.

    Returns
    -------
    defaultdict[str, list]
        The converted dict.
    """
    if value is None:
        return defaultdict(list)
    elif isinstance(value, str):
        value = [value]

    # Using defaultdict so that we can handle empty dicts
    module_dict: defaultdict[str, list] = defaultdict(list)
    for modules in value:
        if not modules.strip():
            continue
        if modules in {"", ":", ";"}:
            continue
        module, *submodules = modules.split(delimiter)
        module_dict[module.strip()].extend(convert_to_list(submodules))
    return module_dict


@define(slots=True)
class Settings:
    """
    This class defines the default settings for the flake8_custom_import_rules
    plugin.

    The settings include various import rules and restrictions that can be
    customized by the user. These settings are used to control the behavior of
    the plugin, allowing it to enforce specific import rules and restrictions
    in a Python project.
    """

    # Set Necessary Options for Project Import Restrictions
    BASE_PACKAGES: list = field(factory=list, converter=convert_to_list)

    # Set Defaults for Project Import Restrictions
    TOP_LEVEL_ONLY_IMPORTS: bool = True
    RESTRICT_RELATIVE_IMPORTS: bool = True
    RESTRICT_LOCAL_SCOPE_IMPORTS: bool = True
    RESTRICT_CONDITIONAL_IMPORTS: bool = False
    RESTRICT_DYNAMIC_IMPORTS: bool = True
    RESTRICT_PRIVATE_IMPORTS: bool = True
    RESTRICT_WILDCARD_IMPORTS: bool = True
    RESTRICT_ALIASED_IMPORTS: bool = False
    RESTRICT_FUTURE_IMPORTS: bool = False

    # Set Defaults for Project Import Restriction Special Cases
    RESTRICT_INIT_IMPORTS: bool = True
    RESTRICT_MAIN_IMPORTS: bool = True
    RESTRICT_TEST_IMPORTS: bool = True
    RESTRICT_CONFTEST_IMPORTS: bool = True

    # Set Defaults for Custom Import Rules
    CUSTOM_RESTRICTIONS: defaultdict[str, list] = field(factory=dict, converter=convert_to_dict)
    RESTRICTED_PACKAGES: list = field(factory=list, converter=convert_to_list)
    STANDALONE_MODULES: list = field(factory=list, converter=convert_to_list)
    STD_LIB_ONLY: list = field(factory=list, converter=convert_to_list)
    THIRD_PARTY_ONLY: list = field(factory=list, converter=convert_to_list)
    FIRST_PARTY_ONLY: list = field(factory=list, converter=convert_to_list)
    PROJECT_ONLY: list = field(factory=list, converter=convert_to_list)
    BASE_PACKAGE_ONLY: list = field(factory=list, converter=convert_to_list)

    @property
    def dict(self) -> dict:
        """
        Return the settings as a dictionary.

        This method converts the settings of the flake8_custom_import_rules
        plugin into a dictionary format. The dictionary includes all the
        default and custom import rules defined in the settings.

        Returns
        -------
        dict
            A dictionary representation of the settings.
        """
        return asdict(self)

    def get_option_keys(self) -> list:
        """
        Return a list of option keys from the settings dictionary.

        This method retrieves all the keys from the settings dictionary that
        are in uppercase. These keys represent the options for the
        flake8_custom_import_rules plugin.

        Returns
        -------
        list
            A list of option keys from the settings dictionary.
        """
        return [key for key in self.dict.keys() if key.isupper()]

    def get_settings_value(self, key: str) -> Any:
        """
        Get the value of a setting given its key.

        Parameters
        ----------
        key : str
            The key of the setting.

        Raises
        ------
        KeyError: If the setting does not exist.

        Returns
        -------
        Any
            The value of the setting.
        """
        if not hasattr(self, key):
            raise KeyError(f"Settings '{key}' does not exist.")
        return self.dict[key]


DEFAULT_CHECKER_SETTINGS = Settings()


HELP_STRINGS = {
    "base-packages": (
        "This option defines the primary packages that constitute your "
        "project, categorized as first-party. It serves as a foundational "
        "configuration, clearly delineating main project components from "
        "external dependencies. For example, include 'my_library' as a base "
        "package if developing a library with that name. Without this "
        "configuration, some functionality will be limited or disabled. "
        "This option is required for the plugin to work as intended. "
        "Specify base-packages using a comma-separated list."
    ),
    "custom-restrictions": (
        "This option enables granular control over importing specific "
        "packages or modules within your project. "
        "Useful in managing complex dependencies and preventing accidental "
        "interactions between specific packages."
        "Specify a package or module, followed by a colon, then list the "
        "custom restrictions for that package or module separate by "
        "additional colons. (i.e., other modules or packages in your "
        "project, even third-party or standard library modules). "
    ),
    "restricted-packages": (
        "This flag restricts the import of specified packages or modules into "
        "all other packages within your project. It enforces clear separation "
        "between high-level and low-level packages, such as preventing the "
        "`app` package from being imported by `common`, `utils`, `core`, etc. "
        "Specify restricted-packages using a comma-separated list."
    ),
    "std-lib-only": (
        "This flag ensures that only standard library modules can be imported "
        "within the specified package or module. Useful in scenarios where "
        "the target is intended to rely solely on the standard library, "
        "without any third-party or project dependencies. "
        "Specify std-lib-only using a comma-separated list."
    ),
    "project-only": (
        "This flag enforces that only project packages can be imported in the "
        "specified modules and packages. Useful to minimize third-party "
        "dependencies when most functionality is implemented within the "
        "project. Packages that can be imported (i.e. project packages) are"
        "defined by the base-packages flag. "
        "Specify project-only using a comma-separated list."
    ),
    "base-package-only": (
        "This flag enforces that only the root package of the package or "
        "module can be imported into the specified packages or modules. "
        "Useful in a project where a clear hierarchy and dependency flow is "
        "required, and all functionality must be accessed through the root "
        "package. Only useful if you have more than one package defined by "
        "the base-packages flag, in this case, if you would like to prevent "
        "imports from the base-package of your project from being imported, "
        "the `custom-restrictions`, `std-lib-only`, and `third-party-only` "
        "flags may be more appropriate. "
        "Specify base-package-only using a comma-separated list."
    ),
    "first-party-only": (
        "This flag enforces that only first-party modules can be imported, "
        "including all imports in base packages except for its own root "
        "package. Useful in security-sensitive environments or to minimize "
        "external dependencies, giving more control over the codebase. For, "
        "example, you only want a specific module to import from the other "
        "packages in your project, but not from any third-party packages. "
        "Specify first-party-only using a comma-separated list."
    ),
    "third-party-only": (
        "This flag enforces that only third-party modules can be imported, "
        "excluding standard modules. For example, in a plugin system, this "
        "ensures that only external libraries are imported, maintaining a "
        "separation of concerns and strict adherence to the design "
        "principles. "
        "Specify third-party-only using a comma-separated list."
    ),
    "standalone-modules": (
        "This flag defines packages that cannot import from any other "
        "packages within your project, except for modules and packages within "
        "the root package of the standalone module. This ensures certain "
        "packages remain standalone, promoting modular design and aiding in "
        "maintainability and scalability. "
        "Specify standalone-modules using a comma-separated list."
    ),
    # "top-level-only-imports": If set to True, only top-level imports are
    # permitted in the project. (default: True)
    # "restrict-relative-imports": If set to True, relative imports for the
    # project are disabled. (default: True)
    # restrict-local-scope-imports RESTRICT_LOCAL_SCOPE_IMPORTS: If set to True, local
    # imports for the project are disabled. (default: True)
    # restrict-conditional-imports RESTRICT_CONDITIONAL_IMPORTS: If set to
    # True, conditional imports for the project are disabled. (default: False)
    # restrict-dynamic-imports RESTRICT_DYNAMIC_IMPORTS: If set to True,
    # dynamic imports for the project are disabled. (default: True)
    # restrict-private-imports RESTRICT_PRIVATE_IMPORTS: If set to True,
    # private imports for the project are disabled. (default: True)
    # restrict-wildcard-imports RESTRICT_WILDCARD_IMPORTS: If set to True,
    # wildcard imports for the project are disabled. (default: True)
    # restrict-aliased-imports RESTRICT_ALIASED_IMPORTS: If set to True,
    # aliased imports for the project are disabled. (default: False)
    # restrict-future-imports RESTRICT_FUTURE_IMPORTS: If set to True,
    # future imports for the project are disabled. (default: False)
    # restrict-init-imports RESTRICT_INIT_IMPORTS: If set to True, importing
    # __init__ files is restricted for the project. (default: True)
    # restrict-main-imports RESTRICT_MAIN_IMPORTS: If set to True, importing
    # __main__ files is restricted for the project. (default: True)
    # restrict-test-imports RESTRICT_TEST_IMPORTS: If set to True, importing
    # test modules (test_*/ *_test.py) is restricted for the project. (default: True)
    # restrict-conftest-imports RESTRICT_CONFTEST_IMPORTS: If set to True,
    # importing from conftest.py files is restricted for the project. (default: True)
}

ERROR_CODES = {
    "base-packages": "",
    "custom-restrictions": "CIR102 to CIR105",
    "restricted-packages": "CIR106 and CIR107",
    "std-lib-only": "CIR401 and CIR402",
    "project-only": "CIR201 and CIR202",
    "base-package-only": "CIR203 and CIR204",
    "first-party-only": "CIR205 and CIR206",
    "third-party-only": "CIR501 and CIR502",
    "standalone-modules": "CIR301 to CIR304",
    "top-level-only-imports": "PIR101",
    "restrict-relative-imports": "PIR102",
    "restrict-local-scope-imports": "PIR103",
    "restrict-conditional-imports": "PIR104",
    "restrict-dynamic-imports": "PIR105",
    "restrict-private-imports": "PIR106",
    "restrict-wildcard-imports": "PIR107",
    "restrict-aliased-imports": "PIR108",
    "restrict-future-imports": "PIR109",
    "restrict-init-imports": "PIR207 and PIR208",
    "restrict-main-imports": "PIR209 and PIR210",
    "restrict-test-imports": "PIR201, PIR202, PIR205, and PIR206",
    "restrict-conftest-imports": "PIR203 and PIR204",
}


def register_options(
    option_manager: OptionManager,
    item: list | str,
    is_restriction: bool = True,
    option_default_value: str | bool | None = "",
    help_string: str | None = None,
    **kwargs: Any,
) -> None:
    """
    Register rules or restrictions for the flake8_custom_import_rules plugin.

    This function is used to register either rules or restrictions for the
    flake8_custom_import_rules plugin. Rules are custom import rules that the
    user can define, while restrictions are predefined rules that the user can
    enable or disable.

    If using short options, set both the following options:
        short_option_name: str | _ARG = _ARG.NO
        long_option_name: str | _ARG = _ARG.NO

    If using long options, just pass a single string into register_opt.

    Parameters
    ----------
    option_manager : OptionManager
        The option manager instance that is used to register the options.
    item : list | str
        The item or list of items to register. Each item is a string that
        represents the name of the rule or restriction.
    is_restriction : bool, optional
        A flag that indicates whether the item is a restriction. If True, the
        option is either True or False, by default True (i.e., we are
        registering a restriction).
        If False, the item is considered a rule.
    option_default_value : str | bool, optional
        The default value for the option. For restrictions, this is typically
        a boolean value. For rules, this can be any string value, by
        default "".
    help_string : str | None, optional
        The help string for the option. This string is displayed when the user
        requests help on this option, by default None.
    kwargs : Any
        Additional keyword arguments to pass to register_opt. These are passed
        directly to the underlying option registration function.
    """
    if isinstance(item, list):
        for single_item in item:
            register_options(
                option_manager, single_item, is_restriction, option_default_value, **kwargs
            )
        return

    assert isinstance(item, str), f"Item must be a str. Got {type(item).__name__} for {item}."

    setting_key = f"{item.replace('_', '-').lower()}"

    if setting_key == "base-packages":
        error_codes = ""
    else:
        error_codes = f"If violated, leads to error codes {ERROR_CODES[setting_key]}."

    if is_restriction:
        option_default_value = DEFAULT_CHECKER_SETTINGS.get_settings_value(item.upper())
        import_type = item.split("_")[1]
        if not help_string:
            help_string = (
                f"This option allows you to disable {import_type.lower()} "
                f"imports for project. {error_codes} "
                f"(default: {option_default_value})"
            )

    # defaults for is_restriction is False
    if option_default_value == "":
        help_string = f"{HELP_STRINGS[setting_key]} {error_codes}"

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
        type=str,
        help=help_string,
        parse_from_config=True,
        comma_separated_list=not is_restriction,
        normalize_paths=False,
    )


def register_opt(self: OptionManager, *args: Any, **kwargs: Any) -> None:
    """
    Register options for the flake8-custom-import-rules plugin.

    This function is responsible for registering the options that are used by
    the flake8-custom-import-rules plugin. These options include both rules
    and restrictions that can be defined by the user. The function takes in an
    OptionManager instance, a list or string representing the item(s) to
    register, and several optional parameters that further define the behavior
    of the registered item(s).
    """
    try:
        # flake8 3.x registration
        self.add_option(*args, **kwargs)
    except (optparse.OptionError, TypeError):
        # flake8 2.x registration
        parse_from_config = kwargs.pop("parse_from_config", False)
        kwargs.pop("comma_separated_list", False)
        kwargs.pop("normalize_paths", False)
        self.add_option(*args, **kwargs)
        if parse_from_config:
            self.config_options.append(args[-1].lstrip("-"))
