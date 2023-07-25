"""
Test cases for restricting __future__ imports

To run this test file only:
poetry run python -m pytest -vvvrca tests/test_cases/project_import_rules/future_import_test.py
"""

import pytest

from flake8_custom_import_rules.defaults import Settings

PIR109 = "PIR109 Future imports are disabled for this project."


@pytest.mark.parametrize(
    ("test_case", "expected", "restrict_future_imports"),
    [
        (
            "import __future__",
            {"1:0: PIR109 Future imports are disabled for this project."},
            True,
        ),
        (
            "import __future__",
            set(),
            False,
        ),
        (
            "from __future__ import annotations",
            {"1:0: PIR109 Future imports are disabled for this project."},
            True,
        ),
        (
            "from __future__ import annotations",
            set(),
            False,
        ),
    ],
)
def test_future_imports(
    test_case: str,
    expected: set,
    restrict_future_imports: bool,
    get_flake8_linter_results: callable,
) -> None:
    """Test wildcard imports."""
    options = {"checker_settings": Settings(**{"RESTRICT_FUTURE_IMPORTS": restrict_future_imports})}
    actual = get_flake8_linter_results(s=test_case, options=options, delimiter="\n")
    assert actual == expected


@pytest.mark.parametrize("restrict_future_imports", [True, False])
def test_main_import_settings_do_not_error(
    valid_custom_import_rules_imports: str,
    get_flake8_linter_results: callable,
    restrict_future_imports: bool,
) -> None:
    """Test main imports do not have an effect on regular import methods."""
    options = {"checker_settings": Settings(**{"RESTRICT_MAIN_IMPORTS": restrict_future_imports})}
    actual = get_flake8_linter_results(
        s=valid_custom_import_rules_imports, options=options, delimiter="\n"
    )
    assert actual == set()
