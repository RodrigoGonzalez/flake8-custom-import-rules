""" Test wildcard/star imports restriction.

PIR107 = "PIR107 Wildcard Imports are disabled for this project."

To run this test file only:
poetry run python -m pytest -vvvrca tests/test_cases/project_import_rules/wildcard_imports_test.py
"""

import pytest

from flake8_custom_import_rules.defaults import Settings


@pytest.mark.parametrize(
    ("test_case", "expected", "restrict_star_imports"),
    [
        (
            "from my_base_module.module_z import *",
            {"1:0: PIR107 Wildcard Imports are disabled for this project."},
            True,
        ),
        (
            "from my_base_module.module_z import *",
            set(),
            False,
        ),
    ],
)
def test_star_imports(
    test_case: str, expected: set, restrict_star_imports: bool, get_flake8_linter_results: callable
) -> None:
    """Test wildcard imports."""
    options = {"checker_settings": Settings(**{"RESTRICT_WILDCARD_IMPORTS": restrict_star_imports})}
    actual = get_flake8_linter_results(s=test_case, options=options)
    assert actual == expected


@pytest.mark.parametrize("restrict_wildcard_imports", [True, False])
def test_wildcard_import_settings_do_not_error(
    valid_custom_import_rules_imports: str,
    get_flake8_linter_results: callable,
    restrict_wildcard_imports: bool,
) -> None:
    """Test wildcard imports do not have an effect on regular import methods."""
    options = {
        "checker_settings": Settings(**{"RESTRICT_WILDCARD_IMPORTS": restrict_wildcard_imports})
    }
    actual = get_flake8_linter_results(
        s=valid_custom_import_rules_imports, options=options, delimiter="\n"
    )
    assert actual == set()
