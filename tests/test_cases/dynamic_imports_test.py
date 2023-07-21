""" Test dynamic import restrictions.

PIR105 = "PIR105 Dynamic imports are currently disabled for this project."
"""
import pytest

from flake8_custom_import_rules.defaults import Settings


@pytest.mark.parametrize(
    ("test_case", "expected", "restrict_dynamic_imports"),
    [
        (
            "eval('from my_base_module.module_z import Z')",
            set(),
            True,
        ),
        (
            "eval('from my_base_module.module_z import Z')",
            set(),
            False,
        ),
        (
            "exec('import datetime')",
            set(),
            True,
        ),
        (
            "exec('import datetime')",
            set(),
            False,
        ),
        (
            "import importlib; importlib.import_module('datetime')",
            set(),
            True,
        ),
        (
            "import importlib; importlib.import_module('datetime')",
            set(),
            False,
        ),
        (
            "from importlib import import_module; importlib.import_module('datetime')",
            set(),
            True,
        ),
        (
            "from importlib import import_module; importlib.import_module('datetime')",
            set(),
            False,
        ),
        (
            "import sys; dynamic_datetime = sys.modules['datetime']",
            set(),
            True,
        ),
        (
            "import sys; dynamic_datetime = sys.modules['datetime']",
            set(),
            False,
        ),
        (
            (
                "from zipimport import zipimporter; "
                "zipimporter = zipimporter('my_module.zip'); "
                "my_module = zipimporter.load_module('my_module')"
            ),
            set(),
            True,
        ),
        (
            (
                "from zipimport import zipimporter; "
                "zipimporter = zipimporter('my_module.zip'); "
                "my_module = zipimporter.load_module('my_module')"
            ),
            set(),
            False,
        ),
    ],
)
def test_dynamic_imports(
    test_case: str,
    expected: set,
    restrict_dynamic_imports: bool,
    get_flake8_linter_results: callable,
) -> None:
    """Test wildcard imports."""
    options = {
        "checker_settings": Settings(**{"RESTRICT_DYNAMIC_IMPORTS": restrict_dynamic_imports})
    }
    actual = get_flake8_linter_results(s=test_case, options=options, delimiter=";")
    assert actual == expected


@pytest.mark.parametrize("restrict_dynamic_imports", [True, False])
def test_dynamic_import_settings_do_not_error(
    valid_custom_import_rules_imports: str,
    get_flake8_linter_results: callable,
    restrict_dynamic_imports: bool,
) -> None:
    """Test dynamic imports do not have an effect on regular import methods."""
    options = {
        "checker_settings": Settings(**{"RESTRICT_DYNAMIC_IMPORTS": restrict_dynamic_imports})
    }
    actual = get_flake8_linter_results(
        s=valid_custom_import_rules_imports, options=options, delimiter="\n"
    )
    assert actual == set()
