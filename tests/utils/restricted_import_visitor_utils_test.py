""" Tests for parse_utils.py

To run this test file only:
poetry run python -m pytest -vvvrca tests/utils/restricted_import_visitor_utils_test.py
"""
from collections import defaultdict

import pytest

from flake8_custom_import_rules.utils.restricted_import_utils import find_keys_with_string
from flake8_custom_import_rules.utils.restricted_import_utils import get_import_restriction_strings
from flake8_custom_import_rules.utils.restricted_import_utils import get_import_strings
from flake8_custom_import_rules.utils.restricted_import_utils import get_restricted_package_strings
from flake8_custom_import_rules.utils.restricted_import_utils import subdict_from_keys


@pytest.mark.parametrize(
    ("restricted_packages", "file_packages", "expected"),
    [
        (["numpy", "pandas"], ["scipy"], ["numpy", "pandas"]),
        (["numpy", "pandas"], ["numpy"], ["pandas"]),
        ([], ["numpy"], []),
    ],
)
def test_get_restricted_package_strings(restricted_packages, file_packages, expected) -> None:
    """Test get_restricted_package_strings."""
    assert get_restricted_package_strings(restricted_packages, file_packages) == expected


@pytest.mark.parametrize(
    ("custom_restrictions", "file_packages", "expected"),
    [
        (defaultdict(list, {"numpy": ["pandas"]}), ["numpy"], ["pandas"]),
        (defaultdict(list, {"numpy": ["pandas"]}), ["scipy"], []),
        (defaultdict(list), ["numpy"], []),
    ],
)
def test_get_import_restriction_strings(custom_restrictions, file_packages, expected) -> None:
    """Test get_import_restriction_strings."""
    assert get_import_restriction_strings(custom_restrictions, file_packages) == expected


@pytest.mark.parametrize(
    ("restrictions", "expected"),
    [
        (["numpy", "pandas"], ["import numpy\n", "import pandas\n"]),
        ([], []),
    ],
)
def test_get_import_strings(restrictions, expected) -> None:
    """Test get_import_strings."""
    assert get_import_strings(restrictions) == expected


@pytest.mark.parametrize(
    ("custom_restrictions", "keys", "expected"),
    [
        (
            defaultdict(list, {"numpy": ["pandas"], "scipy": ["matplotlib"]}),
            ["numpy"],
            {"numpy": ["pandas"]},
        ),
        (defaultdict(list, {"numpy": ["pandas"], "scipy": ["matplotlib"]}), ["tensorflow"], {}),
    ],
)
def test_subdict_from_keys(custom_restrictions, keys, expected) -> None:
    """Test subdict_from_keys."""
    assert subdict_from_keys(custom_restrictions, keys) == expected


@pytest.mark.parametrize(
    ("custom_restrictions", "target_string", "expected"),
    [
        (
            defaultdict(list, {"numpy": ["pandas"], "scipy": ["pandas"]}),
            "pandas",
            ["numpy", "scipy"],
        ),
        (defaultdict(list, {"numpy": ["pandas"], "scipy": ["matplotlib"]}), "tensorflow", []),
    ],
)
def test_find_keys_with_string(custom_restrictions, target_string, expected) -> None:
    """Test find_keys_with_string."""
    assert find_keys_with_string(custom_restrictions, target_string) == expected
