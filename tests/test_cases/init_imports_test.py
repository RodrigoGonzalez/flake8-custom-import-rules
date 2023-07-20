""" Test cases for restricting init imports: 207 and 208. """
import pytest

from flake8_custom_import_rules.defaults import Settings


@pytest.mark.parametrize(
    ("test_case", "expected", "checker_settings"),
    [
        (
            "import __init__; from .module_a import A",
            {"1:0: PIR207 Importing `__init__` is not permitted."},
            {"RESTRICT_INIT_IMPORTS": True},
        ),
        (
            "import __init__; from .module_a import A",
            set(),
            {"RESTRICT_INIT_IMPORTS": False},
        ),
        (
            "from . import __init__; from .module_a import A",
            {"1:0: PIR208 Importing from `__init__.py` files is not permitted."},
            {"RESTRICT_INIT_IMPORTS": True},
        ),
        (
            "from . import __init__; from .module_a import A",
            set(),
            {"RESTRICT_INIT_IMPORTS": False},
        ),
        (
            "from __init__ import module; from .module_a import A",
            {"1:0: PIR208 Importing from `__init__.py` files is not permitted."},
            {"RESTRICT_INIT_IMPORTS": True},
        ),
        (
            "from __init__ import module; from .module_a import A",
            set(),
            {"RESTRICT_INIT_IMPORTS": False},
        ),
    ],
)
def test_init_import_codes(
    test_case: str, expected: set, checker_settings: dict, get_flake8_linter_results: callable
) -> None:
    """Test init imports."""
    options = {"checker_settings": Settings(**checker_settings)}
    assert get_flake8_linter_results(s=test_case, options=options) == expected
