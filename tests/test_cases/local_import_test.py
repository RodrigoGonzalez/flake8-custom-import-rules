""" Test local import restrictions.

PIR103 = "PIR103 Local imports are currently disabled for this project."
"""
from textwrap import dedent

import pytest

from flake8_custom_import_rules.defaults import Settings

LOCAL_IMPORT_CODE = dedent(
    """
    def func():
        import os

    async def async_func():
        from math import sqrt

    class MyClass:
        import sys
    """
)


@pytest.mark.parametrize(
    ("test_case", "expected", "restrict_local_imports"),
    [
        (
            LOCAL_IMPORT_CODE,
            {
                "3:4: PIR103 Local imports are currently disabled for this project.",
                "6:4: PIR103 Local imports are currently disabled for this project.",
                "9:4: PIR103 Local imports are currently disabled for this project.",
            },
            True,
        ),
        (
            LOCAL_IMPORT_CODE,
            set(),
            False,
        ),
    ],
)
def test_local_imports(
    test_case: str, expected: set, restrict_local_imports: bool, get_flake8_linter_results: callable
) -> None:
    """Test wildcard imports."""
    options = {"checker_settings": Settings(**{"RESTRICT_LOCAL_IMPORTS": restrict_local_imports})}
    actual = get_flake8_linter_results(s=test_case, options=options, splitter="\n")
    assert actual == expected


@pytest.mark.parametrize("restrict_local_imports", [True, False])
def test_local_import_settings_do_not_error(
    valid_custom_import_rules_imports: str,
    get_flake8_linter_results: callable,
    restrict_local_imports: bool,
) -> None:
    """Test local imports do not have an effect on regular import methods."""
    options = {"checker_settings": Settings(**{"RESTRICT_LOCAL_IMPORTS": restrict_local_imports})}
    actual = get_flake8_linter_results(
        s=valid_custom_import_rules_imports, options=options, splitter="\n"
    )
    assert actual == set()
