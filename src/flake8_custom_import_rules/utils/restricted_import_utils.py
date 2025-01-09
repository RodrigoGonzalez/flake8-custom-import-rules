""" Utils to use by RestrictedImportVisitor class."""

from collections import defaultdict


def get_restricted_package_strings(
    restricted_packages: list[str],
    file_packages: list[str],
) -> list[str]:
    """
    Retrieve the strings representing restricted packages based on
    the restricted packages and file packages.

    Parameters
    ----------
    restricted_packages: list[str]
        The restricted packages.
    file_packages: list[str]
        The file packages to check. (The module and parent packages.)

    Returns
    -------
    list[str]
        The restricted package strings.
    """
    return [
        restricted_import
        for restricted_import in restricted_packages
        if restricted_import not in file_packages
    ]


def get_import_restriction_strings(
    custom_restrictions: defaultdict[str, list[str]],
    file_packages: list[str],
) -> list[str]:
    """
    Retrieve the strings representing import restrictions based on the
    import restrictions and file packages.

    Parameters
    ----------
    custom_restrictions: defaultdict[str, list[str]]
        The import restrictions.
    file_packages: list[str]
        The file packages to check. (The module and parent packages.)

    Returns
    -------
    list[str]
        The import restriction strings.
    """
    import_restriction_keys = list(custom_restrictions.keys())
    parsed_import_restriction_keys: list = [
        import_restriction_key
        for import_restriction_key in import_restriction_keys
        if import_restriction_key in file_packages
    ]
    custom_restrictions_from_keys = {
        restrictions
        for key in parsed_import_restriction_keys
        for restrictions in custom_restrictions[key]
    }
    parsed_custom_restrictions = list(custom_restrictions_from_keys)

    return get_restricted_package_strings(parsed_custom_restrictions, file_packages)


def get_import_strings(
    restrictions: list[str],
) -> list[str]:
    """
    Get import strings.

    Parameters
    ----------
    restrictions: list[str]
        The restrictions to get the import strings for.

    Returns
    -------
    list[str]
        The import strings.
    """
    return [f"import {restriction}\n" for restriction in sorted(restrictions)]


def subdict_from_keys(
    custom_restrictions: defaultdict[str, list[str]],
    keys: list[str],
) -> dict[str, list[str]]:
    """
    Function to create a subset of a dictionary given a list of keys.

    Parameters
    ----------
    custom_restrictions: defaultdict[str, list[str]]
        The original dictionary.
    keys: list[str]
        The keys for the sub-dictionary.

    Returns
    -------
    dict
        A sub-dictionary with the given keys.
    """
    return {k: custom_restrictions[k] for k in keys if k in custom_restrictions}


def find_keys_with_string(
    custom_restrictions: defaultdict[str, list[str]], target_string: str
) -> list[str]:
    """
    Function to find keys with the target string in their lists.

    Parameters
    ----------
    custom_restrictions : defaultdict
        The defaultdict(list) to search.
    target_string : str
        The string to search for.

    Returns
    -------
    list
        A list of keys where the string is found in their lists.
    """
    return [k for k, v in custom_restrictions.items() if target_string in v]


def check_if_project_package(base_packages: list[str], import_packages: list[str]) -> bool:
    """
    Check if the project restriction is satisfied.

    Parameters
    ----------
    base_packages: list[str]
        The base packages.
    import_packages: list[str]
        The file packages.

    Returns
    -------
    bool
        True if the project restriction is satisfied, False otherwise.
    """
    return any(package in base_packages for package in reversed(import_packages))
