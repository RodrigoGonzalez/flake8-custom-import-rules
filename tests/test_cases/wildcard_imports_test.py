""" Test star imports restriction. """ ""
import pytest

from flake8_custom_import_rules.defaults import Settings


@pytest.mark.parametrize(
    ("test_case", "expected", "restrict_star_imports"),
    [
        (
            "from my_base_module.module_z import *",
            {"1:0: PIR107 Wildcard imports are not permitted in the project."},
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
    assert get_flake8_linter_results(s=test_case, options=options) == expected
