""" Parse utils. """

import logging
import re

logger = logging.getLogger(__name__)


NOQA_INLINE_REGEXP = re.compile(
    # We're looking for items that look like this:
    # ``# noqa``
    # ``# noqa: E123``
    # ``# noqa: E123,W451,F921``
    # ``# NoQA: E123,W451,F921``
    # ``# NOQA: E123,W451,F921``
    # We do not care about the ``: `` that follows ``noqa``
    # We do not care about the casing of ``noqa``
    # We want a comma-separated list of errors
    # r'# noqa(?:: (?P<codes>([A-Z][0-9]+(?:[,\s]+)?)+))?',
    r"# noqa *:?(?P<codes>[A-Za-z0-9, ]+)?",
    re.IGNORECASE,
)

COMMA_SEPARATED_LIST_RE = re.compile(r"[,\s]")


def parse_comma_separated_list(value: list | str) -> set[str]:
    """
    Parse a comma-separated list of values.

    Parameters
    ----------
    value : list | str
        The value to parse.

    Returns
    -------
    set[str]
    """
    if isinstance(value, list):
        return {item.strip() for item in value if item}
    value = COMMA_SEPARATED_LIST_RE.split(value)
    item_gen = (item.strip() for item in value)
    return {item for item in item_gen if item}


def parse_module_string(
    value: str,
    substring_match: list | str | None = None,
    prefix: tuple | str | None = None,
    suffix: tuple | str | None = None,
    delimiter: str = ".",
) -> list:
    """Parse a module and return substrings that match certain criteria.

    Parameters
    ----------
    value : str
        The string to parse.
    substring_match : list | str | None
        A list of substrings or a single substring to match against. If a
        substring in the value matches, it will be returned in the result.
    prefix : str | None
        A prefix to match against. If a substring in the value has this prefix,
        it will be returned in the result.
    suffix : str | None
        A suffix to match against. If a substring in the value has this suffix,
        it will be returned in the result.
    delimiter : str
        The delimiter to use when splitting the value.

    Returns
    -------
    list
        A list of substrings from the value that match the provided criteria.
    """
    substrings = [item.strip() for item in value.split(delimiter) if item]
    if isinstance(substring_match, str):
        substring_match = [substring_match]

    if substring_match or prefix or suffix:
        checking_private_identifiers = prefix == "_"
        matches: list[str] = []
        matches.extend(
            substring
            for substring in substrings
            if (substring_match and substring in substring_match)
            or (
                prefix
                and substring.startswith(prefix)
                and not (
                    checking_private_identifiers
                    and substring.startswith("__")  # exclude dunder methods
                    and substring.endswith("__")
                )
            )
            or (suffix and substring.endswith(suffix))
        )
        return matches
    else:
        return substrings


def check_string(
    strings_to_check: list | str,
    substring_match: list | str | None = None,
    prefix: tuple | str | None = None,
    suffix: tuple | str | None = None,
    delimiter: str = ".",
) -> bool:
    """Check a string or list of strings for matches against certain criteria.

    Parameters
    ----------
    strings_to_check : list | str
        The string(s) to check.
    substring_match : list | str | None
        A list of substrings or a single substring to match against. If a
        substring in the string(s) to check matches, the function will return
        True.
    prefix : str | None
        A prefix to match against. If a string in the string(s) to check has
        this prefix, the function will return True.
    suffix : str | None
        A suffix to match against. If a string in the string(s) to check has
        this suffix, the function will return True.
    delimiter : str
        The delimiter to use when splitting the string(s) to check.

    Returns
    -------
    bool
        True if any matches are found, False otherwise.
    """
    if substring_match or prefix or suffix:
        if isinstance(strings_to_check, list):
            # delimiter = "."
            strings_to_check = f"{delimiter}".join(strings_to_check)
        matches = parse_module_string(strings_to_check, substring_match, prefix, suffix, delimiter)
        return bool(matches)
    else:
        return False


def does_file_match_custom_rule(
    file_packages: list[str] | str, custom_rules: list[str] | str | None
) -> bool:
    """
    Check if a file identifier is in a custom rule.

    Parameters
    ----------
    file_packages : list[str] | str
        The file package identifiers to check.
    custom_rules : list[str] | str | None
        A list of custom rules or a single custom rule to check against.

    Returns
    -------
    bool
    """
    if custom_rules is None:
        return False
    custom_rules = [custom_rules] if isinstance(custom_rules, str) else custom_rules
    return check_string(file_packages, substring_match=custom_rules, delimiter=" ")


def does_import_match_custom_import_restriction(
    node_identifier: str, standalone_imports: list[str] | str | None
) -> bool:
    """
    Check if an import identifier is in a standalone import.

    Parameters
    ----------
    node_identifier : str
        The import identifier to check.
    standalone_imports : list[str] | str | None
        A list of standalone imports or a single standalone import to check against.

    Returns
    -------
    bool
    """
    if standalone_imports is None:
        return False
    restricted_imports = (
        [standalone_imports] if isinstance(standalone_imports, str) else standalone_imports
    )
    return check_string(node_identifier, prefix=tuple(restricted_imports), delimiter=" ")


def retrieve_custom_rule_matches(identifier: str, custom_rules: list[str] | str) -> list[str]:
    """Retrieve custom rule matches."""
    if isinstance(custom_rules, str):
        custom_rules = [custom_rules]
    matches: list[str] = [
        custom_rule_match
        for custom_rule_match in custom_rules
        if check_string(identifier, prefix=custom_rule_match, delimiter=" ")
    ]
    return matches  # max(matches, key=len)
