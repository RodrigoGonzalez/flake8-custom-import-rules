""" Test cases for restricting init imports

PIR207 = "PIR207 Importing `__init__` is not permitted."
PIR208 = "PIR208 Importing from `__init__.py` files is not permitted."
"""
import pytest

from flake8_custom_import_rules.defaults import Settings


@pytest.mark.parametrize(
    ("test_case", "expected", "restrict_init_imports"),
    [
        (
            "import __init__; from .module_a import A",
            {"1:0: PIR207 Importing `__init__` is not permitted."},
            True,
        ),
        (
            "import __init__; from .module_a import A",
            set(),
            False,
        ),
        (
            "from . import __init__; from .module_a import A",
            {"1:0: PIR208 Importing from `__init__.py` files is not permitted."},
            True,
        ),
        (
            "from . import __init__; from .module_a import A",
            set(),
            False,
        ),
        (
            "from __init__ import module; from .module_a import A",
            {"1:0: PIR208 Importing from `__init__.py` files is not permitted."},
            True,
        ),
        (
            "from __init__ import module; from .module_a import A",
            set(),
            False,
        ),
    ],
)
def test_init_import_codes(
    test_case: str, expected: set, restrict_init_imports: bool, get_flake8_linter_results: callable
) -> None:
    """Test init imports."""
    options = {
        "checker_settings": Settings(
            **{"RESTRICT_INIT_IMPORTS": restrict_init_imports, "RESTRICT_RELATIVE_IMPORTS": False}
        )
    }
    actual = get_flake8_linter_results(s=test_case, options=options)
    assert actual == expected


@pytest.mark.parametrize("restrict_init_imports", [True, False])
def test_init_import_settings_do_not_error(
    valid_custom_import_rules_imports: str,
    get_flake8_linter_results: callable,
    restrict_init_imports: bool,
) -> None:
    """Test init imports do not have an effect on regular import methods."""
    options = {"checker_settings": Settings(**{"RESTRICT_INIT_IMPORTS": restrict_init_imports})}
    actual = get_flake8_linter_results(
        s=valid_custom_import_rules_imports, options=options, splitter="\n"
    )
    assert actual == set()
