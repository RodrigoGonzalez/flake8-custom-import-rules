""" Tests for parse_utils.py """
import pytest

from flake8_custom_import_rules.utils.parse_utils import parse_module_string


@pytest.mark.parametrize(
    ("module_string", "substring_match", "prefix", "suffix", "expected"),
    [
        ("foo", None, None, None, ["foo"]),
        ("foo.and.bar", None, "fo", "biz", ["foo"]),
        ("foo.and.bar", "and", "fo", "biz", ["foo", "and"]),
        ("foo.and.bar", None, None, "bar", ["bar"]),
        ("foo.and.bar", None, None, None, ["foo", "and", "bar"]),
        ("foo.and.bar.and.baz", ["bar", "baz"], None, None, ["bar", "baz"]),
        ("foo.and.bar.and.baz", "and", None, None, ["and", "and"]),
    ],
)
def test_parse_module_string(module_string, substring_match, prefix, suffix, expected) -> None:
    """Test parse_module_string."""
    assert (
        parse_module_string(
            value=module_string, substring_match=substring_match, prefix=prefix, suffix=suffix
        )
        == expected
    )
