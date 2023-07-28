"""
Restricted import visitor tests.

To run this test file only:
poetry run python -m pytest -vvvrca tests/core/restricted_import_visitor_test.py
"""
from collections import defaultdict

import pytest

from flake8_custom_import_rules.core.restricted_import_visitor import get_restricted_identifiers

PACKAGE_6 = [
    "my_second_base_package",
    "my_second_base_package.module_one",
    "my_second_base_package.module_one.file_one",
    "my_third_base_package",
    "my_second_base_package.module_one",
    "my_second_base_package.module_two",
    "my_base_module",
]


@pytest.mark.parametrize(
    ("restricted_imports", "check_module_exists", "expected"),
    [(PACKAGE_6, True, {}), (PACKAGE_6, False, {}), ([], True, {})],
)
def test_get_restricted_identifiers(
    restricted_imports: list[str] | str,
    check_module_exists: bool,
    expected: dict,
) -> None:
    """Test get_restricted_identifiers."""
    restricted_identifiers = get_restricted_identifiers(
        restricted_imports=restricted_imports, check_module_exists=check_module_exists
    )
    assert isinstance(restricted_identifiers, defaultdict)
