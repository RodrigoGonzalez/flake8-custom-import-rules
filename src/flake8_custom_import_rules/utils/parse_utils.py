""" Parse utils. """
import os
import re
import sys

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

BLANK_LINE_RE = re.compile(r"\s*\n")
COMMA_SEPARATED_LIST_RE = re.compile(r"[,\s]")


def parse_comma_separated_list(value: list | str) -> set[str]:
    """Parse a comma-separated list of values."""
    # items = re.split(r"\s*,\s*", value)
    # return {item.strip() for item in items if item}
    if isinstance(value, list):
        return {item.strip() for item in value if item}
    value = COMMA_SEPARATED_LIST_RE.split(value)
    item_gen = (item.strip() for item in value)
    return {item for item in item_gen if item}


def parse_module_string(
    value: str,
    substring_match: list | str | None = None,
    prefix: str | None = None,
    suffix: str | None = None,
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
    prefix: str | None = None,
    suffix: str | None = None,
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


def parse_custom_rule(rules: list[str]) -> dict[str, list[str]]:
    """Parse custom rules."""
    return {src.strip(): dest.split(",") for rule in rules for src, dest in (rule.split(":"),)}


def get_module_name_from_file(base_module: str, filename: str) -> str | None:
    """
    Get the module name for a given file path based on a base module.

    Parameters
    ----------
    base_module : str
        The base module to use as a reference.
    filename : str
        The file path to get the module name for.

    Returns
    -------
    str | None
    """

    # Check if the base module is in the file path
    if base_module not in filename:
        raise ValueError(f"The base module {base_module} is not in the file path {filename}")

    # Get the part of the file path that is relative to the base module
    relative_path = filename.partition(base_module)[2].strip("/")

    # Remove the .py extension and replace / with . to get the module name
    return os.path.splitext(relative_path)[0].replace("/", ".")


def find_prefix(filename: str) -> str:
    """
    Find the appropriate module prefix string for the filename.

    Parameters
    ----------
    filename : str
        The filename to find the prefix for.

    Returns
    -------
    str
    """
    filename = os.path.abspath(filename)

    # Find the deepest path
    matches = (path for path in sys.path if filename.startswith(path))

    return max(matches, key=len)


def convert_name(filename: str, prefix: str | None = None) -> str:
    """
    Convert filename to a module name by removing prefix and .py extension,
    and replacing / with .

    Parameters
    ----------
    filename : str
        The filename to convert.
    prefix : str | None
        The prefix to remove from the filename.

    Returns
    -------
    str
    """
    filename = os.path.abspath(filename)

    if prefix and filename.startswith(prefix):
        filename = filename[len(prefix) :]

    if filename.endswith(".py"):
        filename = filename[:-3]

    return filename.lstrip("/").replace("/", ".")


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
