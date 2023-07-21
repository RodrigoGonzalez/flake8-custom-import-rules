""" Test cases for restricting __main__ imports

PIR209 = "PIR209 Importing `__main__` is not permitted."
PIR210 = "PIR210 Importing from `__main__.py` files is not permitted."
"""
from textwrap import dedent

import pytest

from flake8_custom_import_rules.defaults import Settings

MAIN_IMPORT_CODE = dedent(
    """
    import __main__
    import main_module
    import module

    from module import main_function
    from . import __main__
    from __main__ import module
    """
)


@pytest.mark.parametrize(
    ("test_case", "expected", "restrict_main_imports"),
    [
        (
            MAIN_IMPORT_CODE,
            {
                "2:0: PIR209 Importing `__main__` is not permitted.",
                "7:0: PIR210 Importing from `__main__.py` files is not permitted.",
                "8:0: PIR210 Importing from `__main__.py` files is not permitted.",
            },
            True,
        ),
        (
            MAIN_IMPORT_CODE,
            set(),
            False,
        ),
    ],
)
def test_main_imports(
    test_case: str,
    expected: set,
    restrict_main_imports: bool,
    get_flake8_linter_results: callable,
) -> None:
    """Test wildcard imports."""
    options = {
        "checker_settings": Settings(
            **{"RESTRICT_MAIN_IMPORTS": restrict_main_imports, "RESTRICT_RELATIVE_IMPORTS": False}
        )
    }
    actual = get_flake8_linter_results(s=test_case, options=options, splitter="\n")
    assert actual == expected


@pytest.mark.parametrize("restrict_main_imports", [True, False])
def test_main_import_settings_do_not_error(
    valid_custom_import_rules_imports: str,
    get_flake8_linter_results: callable,
    restrict_main_imports: bool,
) -> None:
    """Test main imports do not have an effect on regular import methods."""
    options = {"checker_settings": Settings(**{"RESTRICT_MAIN_IMPORTS": restrict_main_imports})}
    actual = get_flake8_linter_results(
        s=valid_custom_import_rules_imports, options=options, splitter="\n"
    )
    assert actual == set()
