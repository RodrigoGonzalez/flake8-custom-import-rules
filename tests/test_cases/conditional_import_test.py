""" Test conditional import restrictions.

PIR104 = "PIR104 Conditional imports are currently disabled for this project."
"""
from textwrap import dedent

import pytest

from flake8_custom_import_rules.defaults import Settings

CONDITIONAL_TEST_CODE = dedent(
    """
    import sys

    if sys.version_info < (3, 8):
        import importlib_metadata
    else:
        import importlib.metadata as importlib_metadata
    """
)


@pytest.mark.parametrize(
    ("test_case", "expected", "restrict_conditional_imports"),
    [
        (
            CONDITIONAL_TEST_CODE,
            {
                "5:4: PIR104 Conditional imports are currently disabled for this project.",
                "7:4: PIR104 Conditional imports are currently disabled for this project.",
            },
            True,
        ),
        (
            CONDITIONAL_TEST_CODE,
            set(),
            False,
        ),
    ],
)
def test_conditional_imports(
    test_case: str,
    expected: set,
    restrict_conditional_imports: bool,
    get_flake8_linter_results: callable,
) -> None:
    """Test conditional imports."""
    options = {
        "checker_settings": Settings(
            **{"RESTRICT_CONDITIONAL_IMPORTS": restrict_conditional_imports}
        )
    }
    actual = get_flake8_linter_results(s=test_case, options=options, splitter="\n")
    assert actual == expected


@pytest.mark.parametrize("restrict_conditional_imports", [True, False])
def test_conditional_import_settings_do_not_error(
    valid_custom_import_rules_imports: str,
    get_flake8_linter_results: callable,
    restrict_conditional_imports: bool,
) -> None:
    """Test conditional imports do not have an effect on regular import methods."""
    options = {
        "checker_settings": Settings(
            **{"RESTRICT_CONDITIONAL_IMPORTS": restrict_conditional_imports}
        )
    }
    actual = get_flake8_linter_results(
        s=valid_custom_import_rules_imports, options=options, splitter="\n"
    )
    assert actual == set()
