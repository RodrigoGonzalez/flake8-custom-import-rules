""" Utility functions for the flake8-custom-import-rules plugin options. """


def check_conflicts(settings_dict: dict) -> list | None:
    """
    Check for conflicts in the provided settings.

    Parameters
    ----------
    settings_dict : dict
        An instance of the Settings class with the configurations.

    Returns
    -------
    list | None
        A list of messages indicating any conflicts or stating that
        there are no conflicts.
    """

    conflicts = []

    # Extract lists from settings
    restricted_packages = settings_dict.get("RESTRICTED_PACKAGES", [])
    standalone_modules = settings_dict.get("STANDALONE_MODULES", [])
    std_lib_only = settings_dict.get("STD_LIB_ONLY", [])
    third_party_only = settings_dict.get("THIRD_PARTY_ONLY", [])
    first_party_only = settings_dict.get("FIRST_PARTY_ONLY", [])
    project_only = settings_dict.get("PROJECT_ONLY", [])
    base_package_only = settings_dict.get("BASE_PACKAGE_ONLY", [])

    # Extract dict from settings
    custom_restrictions = settings_dict.get("CUSTOM_RESTRICTIONS", {})

    # Check for intersections among list options
    if conflict := set(third_party_only).intersection(first_party_only):
        conflicts.append(
            f"Conflict: {conflict}. A package cannot be set to both "
            f"--third-party-only and --first-party-only."
        )
    if conflict := set(std_lib_only).intersection(third_party_only):
        conflicts.append(
            f"Conflict: {conflict}. A package cannot be set to both "
            f"--std-lib-only and --third-party-only."
        )

    # Check for intersections between standalone_modules and other list options
    conflicts.extend(
        f"Conflict: {set(standalone_modules).intersection(packages)}. "
        f"Modules set to --standalone-modules cannot be included in {option}."
        for option, packages in [
            ("--custom-restrictions", list(custom_restrictions.keys())),
            ("--restricted-packages", restricted_packages),
            ("--std-lib-only", std_lib_only),
            ("--third-party-only", third_party_only),
            ("--first-party-only", first_party_only),
            ("--project-only", project_only),
            ("--base-package-only", base_package_only),
        ]
        if set(standalone_modules).intersection(packages)
    )

    # If no conflicts are detected
    return conflicts or None


def get_bool_value(value: int | str | bool) -> bool:
    """
    Interprets and coerces a given value to a boolean type.

    This function is designed to handle a variety of input types (int, str,
    bool) and interpret them as boolean values. For example, it treats the
    string "yes" as True and "no" as False. It raises a ValueError for
    unexpected inputs.

    Parameters
    ----------
    value : int | str | bool
        The value to be interpreted as a boolean. This can be an integer
        (0 or 1), a string ("true", "false", "yes", "no", etc.), or a boolean
        value.

    Returns
    -------
    bool
        The boolean interpretation of the input value.

    Raises
    ------
    ValueError
        If the input value cannot be interpreted as a boolean.
    """
    if isinstance(value, bool):
        return value

    lowered = str(value).lower()
    if lowered in {"false", "0", "no", "n", ""}:
        return False
    elif lowered in {"true", "1", "yes", "y"}:
        return True
    else:
        raise ValueError(f'Cannot interpret value "{value}" as boolean')
