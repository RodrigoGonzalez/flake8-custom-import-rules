"""
Test top-level only import restrictions.

PIR101 = "PIR101 Only top level imports are permitted in the project."

To run this test file only:
poetry run python -m pytest -vvvrca tests/test_cases/project_import_rules/top_level_only_test.py
"""
from textwrap import dedent

import pytest

from flake8_custom_import_rules.defaults import Settings

TOP_LEVEL_ONLY_IMPORT_CODE = dedent(
    """
    import _private_module
    import module

    from _private_module import function
    from _private_module import _private_function, second_function
    from module import _private_function
    from module._private_module import function
    """
)


@pytest.mark.parametrize(
    ("test_case", "expected", "top_level_only_imports"),
    [
        (
            TOP_LEVEL_ONLY_IMPORT_CODE,
            {
                "2:0: PIR106 Private Imports are disabled for this project.",
                "5:0: PIR106 Private Imports are disabled for this project.",
                "6:0: PIR106 Private Imports are disabled for this project.",
                "7:0: PIR106 Private Imports are disabled for this project.",
                "8:0: PIR106 Private Imports are disabled for this project.",
            },
            True,
        ),
        (
            TOP_LEVEL_ONLY_IMPORT_CODE,
            set(),
            False,
        ),
    ],
)
def test_private_imports(
    test_case: str,
    expected: set,
    top_level_only_imports: bool,
    get_flake8_linter_results: callable,
) -> None:
    """Test wildcard imports."""
    options = {"checker_settings": Settings(**{"RESTRICT_PRIVATE_IMPORTS": top_level_only_imports})}
    actual = get_flake8_linter_results(s=test_case, options=options, delimiter="\n")
    assert actual == expected


@pytest.mark.parametrize("top_level_only_imports", [True, False])
def test_private_import_settings_do_not_error(
    valid_custom_import_rules_imports: str,
    get_flake8_linter_results: callable,
    top_level_only_imports: bool,
) -> None:
    """Test private imports do not have an effect on regular import methods."""
    options = {"checker_settings": Settings(**{"RESTRICT_PRIVATE_IMPORTS": top_level_only_imports})}
    actual = get_flake8_linter_results(
        s=valid_custom_import_rules_imports, options=options, delimiter="\n"
    )
    assert actual == set()
