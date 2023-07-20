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


def parse_comma_separated_list(value: str) -> set[str]:
    """Parse a comma-separated list of values."""
    items = re.split(r"\s*,\s*", value)
    return {item for item in items if item}


def parse_custom_rule(rules: list[str]) -> dict[str, list[str]]:
    """Parse custom rules."""
    return {src.strip(): dest.split(",") for rule in rules for src, dest in (rule.split(":"),)}
