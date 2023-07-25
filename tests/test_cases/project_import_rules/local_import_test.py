""" Test local import restrictions.

PIR103 = "PIR103 Local imports are disabled for this project."

To run this test file only:
poetry run python -m pytest -vvvrca tests/test_cases/project_import_rules/local_import_test.py
"""
from textwrap import dedent

import pytest

from flake8_custom_import_rules.defaults import Settings

LOCAL_IMPORT_CODE = dedent(
    """
    import os

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
                "5:4: PIR103 Local imports are disabled for this project.",
                "8:4: PIR103 Local imports are disabled for this project.",
                "11:4: PIR103 Local imports are disabled for this project.",
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
    """Test local imports."""
    options = {"checker_settings": Settings(**{"RESTRICT_LOCAL_IMPORTS": restrict_local_imports})}
    actual = get_flake8_linter_results(s=test_case, options=options, delimiter="\n")
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
        s=valid_custom_import_rules_imports, options=options, delimiter="\n"
    )
    assert actual == set()
