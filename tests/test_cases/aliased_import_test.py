""" Test aliased import restrictions.

PIR108 = "PIR108 Aliased imports are currently disabled for this project."
"""
import pytest

from flake8_custom_import_rules.defaults import Settings


@pytest.mark.parametrize(
    ("test_case", "expected", "restrict_aliased_imports"),
    [
        (
            "from module_z import Z as Zee",
            {"1:0: PIR108 Aliased imports are currently disabled for this project."},
            True,
        ),
        (
            "from module_z import Z as Zee",
            set(),
            False,
        ),
        (
            "import numpy as np",
            {"1:0: PIR108 Aliased imports are currently disabled for this project."},
            True,
        ),
        (
            "import numpy as np",
            set(),
            False,
        ),
        (
            "import pandas as pd",
            {"1:0: PIR108 Aliased imports are currently disabled for this project."},
            True,
        ),
        (
            "import pandas as pd",
            set(),
            False,
        ),
    ],
)
def test_aliased_imports(
    test_case: str,
    expected: set,
    restrict_aliased_imports: bool,
    get_flake8_linter_results: callable,
) -> None:
    """Test aliased imports."""
    options = {
        "checker_settings": Settings(**{"RESTRICT_ALIASED_IMPORTS": restrict_aliased_imports})
    }
    actual = get_flake8_linter_results(s=test_case, options=options)
    assert actual == expected


@pytest.mark.parametrize("restrict_aliased_imports", [True, False])
def test_aliased_import_settings_do_not_error(
    valid_custom_import_rules_imports: str,
    get_flake8_linter_results: callable,
    restrict_aliased_imports: bool,
) -> None:
    """Test aliased imports do not have an effect on regular import methods."""
    options = {
        "checker_settings": Settings(**{"RESTRICT_ALIASED_IMPORTS": restrict_aliased_imports})
    }
    actual = get_flake8_linter_results(
        s=valid_custom_import_rules_imports, options=options, splitter="\n"
    )
    assert actual == set()
