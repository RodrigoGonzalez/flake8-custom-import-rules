""" Tests for parse_utils.py

To run this test file only:
poetry run python -m pytest -vvvrca tests/utils/parse_utils_test.py
"""

import pytest

from flake8_custom_import_rules.utils.node_utils import get_package_names
from flake8_custom_import_rules.utils.parse_utils import check_string
from flake8_custom_import_rules.utils.parse_utils import does_file_match_custom_rule
from flake8_custom_import_rules.utils.parse_utils import does_import_match_custom_import_restriction
from flake8_custom_import_rules.utils.parse_utils import parse_module_string
from flake8_custom_import_rules.utils.parse_utils import retrieve_custom_rule_matches


@pytest.mark.parametrize(
    ("module_string", "substring_match", "prefix", "suffix", "delimiter", "expected"),
    [
        ("foo", None, None, None, ".", ["foo"]),
        ("foo.and.bar", None, "fo", "biz", ".", ["foo"]),
        ("foo.and.bar", "and", "fo", "biz", ".", ["foo", "and"]),
        ("foo.and.bar", None, None, "bar", ".", ["bar"]),
        ("foo.and.bar", None, None, None, ".", ["foo", "and", "bar"]),
        ("foo.and.bar.and.baz", ["bar", "baz"], None, None, ".", ["bar", "baz"]),
        ("foo.and.bar.and.baz", "and", None, None, ".", ["and", "and"]),
        ("foo,and,bar,and,baz", "and", None, None, ",", ["and", "and"]),
    ],
)
def test_parse_module_string(
    module_string, substring_match, prefix, suffix, delimiter, expected
) -> None:
    """Test parse_module_string."""
    assert (
        parse_module_string(
            value=module_string,
            substring_match=substring_match,
            prefix=prefix,
            suffix=suffix,
            delimiter=delimiter,
        )
        == expected
    )


@pytest.mark.parametrize(
    ("strings_to_check", "substring_match", "prefix", "suffix", "delimiter", "expected"),
    [
        ("foo", None, None, None, ".", False),
        ("foo.and.bar", None, "fo", "biz", ".", True),
        ("foo.and.bar", "and", "fo", "biz", ".", True),
        ("foo.and.bar", None, None, "bar", ".", True),
        ("foo.and.bar", None, None, None, ".", False),
        ("foo.and.bar.and.baz", ["bar", "baz"], None, None, ".", True),
        ("foo.and.bar.and.baz", "and", None, None, ".", True),
        ("foo,and,bar,and,baz", "and", None, None, ",", True),
        ("eval", ["eval", "exec"], None, None, ".", True),
        (["eval"], ["eval", "exec"], None, None, ".", True),
        ("exec", ["eval", "exec"], None, None, ".", True),
        (["exec"], ["eval", "exec"], None, None, ".", True),
        ("os", ["eval", "exec"], None, None, ".", False),
        (["os"], ["eval", "exec"], None, None, ".", False),
        ("__init__", "__init__", None, None, ".", True),
        (["__init__"], "__init__", None, None, ".", True),
        ("__main__", "__main__", None, None, ".", True),
        (["__main__"], "__main__", None, None, ".", True),
        ("__future__", "__future__", None, None, ".", True),
        (["__future__"], "__future__", None, None, ".", True),
    ],
)
def test_check_string(
    strings_to_check,
    substring_match,
    prefix,
    suffix,
    delimiter,
    expected: bool,
) -> None:
    """Test check_string."""
    assert (
        check_string(
            strings_to_check=strings_to_check,
            substring_match=substring_match,
            prefix=prefix,
            suffix=suffix,
            delimiter=delimiter,
        )
        == expected
    )


PACKAGE_1 = ["my_base_package.package_a", "my_base_package.package_b"]
PACKAGE_2 = ["my_base_package.package_c"]
PACKAGE_3 = ["my_base_package"]
PACKAGE_4 = ["my_second_package"]
PACKAGE_5 = ["my_base_package.package_a.mod_a"]


@pytest.mark.parametrize(
    ("file_packages", "custom_rules", "expected"),
    [
        ("my_base_package.package_c", PACKAGE_1, False),
        ("my_base_package.package_a", PACKAGE_1, True),
        ("my_base_package.package_a.mod_a", PACKAGE_1, True),
        ("my_base_package.package_c", PACKAGE_2, True),
        ("my_base_package.package_a", PACKAGE_2, False),
        ("my_base_package.package_a.mod_a", PACKAGE_2, False),
        ("my_base_package.package_c", PACKAGE_3, True),
        ("my_base_package.package_a", PACKAGE_3, True),
        ("my_base_package.package_a.mod_a", PACKAGE_3, True),
        ("my_base_package.package_c", PACKAGE_4, False),
        ("my_base_package.package_a", PACKAGE_4, False),
        ("my_base_package.package_a.mod_a", PACKAGE_4, False),
        ("my_base_package.package_c", PACKAGE_5, False),
        ("my_base_package.package_a", PACKAGE_5, False),
        ("my_base_package.package_a.mod_a", PACKAGE_5, True),
    ],
)
def test_does_file_match_custom_rule(
    file_packages: str, custom_rules: list[str], expected: bool
) -> None:
    """Test does_file_match_custom_rule."""
    assert (
        does_file_match_custom_rule(
            file_packages=get_package_names(file_packages), custom_rules=custom_rules
        )
        == expected
    )


PACKAGE_6 = [
    "my_second_base_package",
    "my_second_base_package.module_one",
    "my_second_base_package.module_one.file_one",
    "my_third_base_package",
]


@pytest.mark.parametrize(
    ("node_identifier", "standalone_imports", "expected"),
    [
        ("my_second_base_package.module_one.file_one", PACKAGE_6, True),
        ("my_second_base_package.module_one.file_two", PACKAGE_6, True),
        ("my_second_base_package.module_one.file_three", PACKAGE_6, True),
        ("my_second_base_package.module_two.file_one", PACKAGE_6, True),
        ("my_second_base_package.module_two.file_two", PACKAGE_6, True),
        ("my_second_base_package.module_two.file_three", PACKAGE_6, True),
        ("my_second_base_package.file", PACKAGE_6, True),
        ("base_package.file", PACKAGE_6, False),
        ("my_third_base_package.file", PACKAGE_6, True),
    ],
)
def test_does_import_match_custom_import_restriction(
    node_identifier: str, standalone_imports: list[str], expected: bool
) -> None:
    """Test does_import_match_custom_import_restriction."""
    assert (
        does_import_match_custom_import_restriction(
            node_identifier=node_identifier, standalone_imports=standalone_imports
        )
        == expected
    )


@pytest.mark.parametrize(
    ("identifier", "custom_rules", "expected"),
    [
        (
            "my_second_base_package.module_one.file_one",
            PACKAGE_6,
            [
                "my_second_base_package",
                "my_second_base_package.module_one",
                "my_second_base_package.module_one.file_one",
            ],
        ),
        (
            "my_second_base_package.module_one.file_two",
            PACKAGE_6,
            [
                "my_second_base_package",
                "my_second_base_package.module_one",
            ],
        ),
        (
            "my_second_base_package.module_two.file_one",
            PACKAGE_6,
            [
                "my_second_base_package",
            ],
        ),
        (
            "my_second_base_package.module_two.file_two",
            PACKAGE_6,
            [
                "my_second_base_package",
            ],
        ),
        (
            "my_second_base_package.file",
            PACKAGE_6,
            [
                "my_second_base_package",
            ],
        ),
        (
            "base_package.file",
            PACKAGE_6,
            [],
        ),
    ],
)
def test_retrieve_custom_rule_matches(
    identifier: str, custom_rules: list[str], expected: str
) -> None:
    """Test retrieve_custom_rule_matches."""
    assert (
        retrieve_custom_rule_matches(identifier=identifier, custom_rules=custom_rules) == expected
    )
