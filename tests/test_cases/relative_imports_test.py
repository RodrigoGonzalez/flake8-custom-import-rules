""" Test relative import restrictions.

PIR102 = "PIR102 Relative imports are currently disabled for this project."
"""
import pytest

from flake8_custom_import_rules.defaults import Settings


@pytest.mark.parametrize(
    ("test_case", "expected", "restrict_relative_imports"),
    [
        (
            "from .module_z import Z",
            {"1:0: PIR102 Relative imports are currently disabled for this project."},
            True,
        ),
        (
            "from .module_z import Z",
            set(),
            False,
        ),
        (
            "from . import module_z",
            {"1:0: PIR102 Relative imports are currently disabled for this project."},
            True,
        ),
        (
            "from . import module_z",
            set(),
            False,
        ),
        (
            "from ..module_z import Z",
            {"1:0: PIR102 Relative imports are currently disabled for this project."},
            True,
        ),
        (
            "from ..module_z import Z",
            set(),
            False,
        ),
    ],
)
def test_relative_imports(
    test_case: str,
    expected: set,
    restrict_relative_imports: bool,
    get_flake8_linter_results: callable,
) -> None:
    """Test wildcard imports."""
    options = {
        "checker_settings": Settings(**{"RESTRICT_RELATIVE_IMPORTS": restrict_relative_imports})
    }
    actual = get_flake8_linter_results(s=test_case, options=options)
    assert actual == expected
