""" Parse utils. """
import re

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
    r"# noqa(?:: (?P<codes>([A-Z][0-9]+(?:[,\s]+)?)+))?",
    re.IGNORECASE,
)

BLANK_LINE_RE = re.compile(r"\s*\n")
IMPORT_RE = re.compile(r"\bimport\b")
# string = "lot sof wel;kjhtrjklwehc  import dskjsdfk import akjsdjk"
# match = IMPORT_RE.search(string)


def parse_comma_separated_list(value: str) -> set[str]:
    """Parse a comma-separated list of values."""
    items = re.split(r"\s*,\s*", value)
    return {item for item in items if item}


def parse_module_string(
    value: str,
    substring_match: list | str | None = None,
    prefix: str | None = None,
    suffix: str | None = None,
    delimiter: str = ".",
) -> list:
    """Parse a module."""
    substrings = value.split(delimiter)
    if isinstance(substring_match, str):
        substring_match = [substring_match]
    if substring_match or prefix or suffix:
        matches: list[str] = []
        matches.extend(
            substring
            for substring in substrings
            if (substring_match and substring in substring_match)
            or (prefix and substring.startswith(prefix))
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
    """Check string for matches."""
    if substring_match or prefix or suffix:
        if isinstance(strings_to_check, list):
            strings_to_check = f"{delimiter}".join(strings_to_check)
        matches = parse_module_string(strings_to_check, substring_match, prefix, suffix, delimiter)
        return bool(matches)
    else:
        return False


def parse_custom_rule(rules: list[str]) -> dict[str, list[str]]:
    """Parse custom rules."""
    return {src.strip(): dest.split(",") for rule in rules for src, dest in (rule.split(":"),)}
