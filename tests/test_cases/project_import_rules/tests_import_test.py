""" Import from test modules, files, and packages.

PIR201 = "PIR201 Importing test_*/*_test modules is restricted."
PIR202 = "PIR202 Importing from test_*.py/*_test.py modules is restricted."
PIR203 = "PIR203 Importing 'conftest' is restricted."
PIR204 = "PIR204 Importing from `conftest.py` modules is restricted."
PIR205 = "PIR205 Importing tests directory or tests subdirectories is restricted."
PIR206 = "PIR206 Importing from tests directory or its subdirectories is restricted."

To run this test file only:
poetry run python -m pytest -vvvrca tests/test_cases/project_import_rules/tests_import_test.py
"""

from textwrap import dedent

import pytest

from flake8_custom_import_rules.defaults import Settings

TEST_IMPORT_CODE = dedent(
    """
    import test_module
    import module
    import conftest
    import tests

    from test_module import function
    from test_module import test_function, second_function
    from module import test_function
    from module.test_module import another_function
    from tests.test_module import and_another_function
    from conftest import a_fixture
    from conftest import test_function
    """
)


@pytest.mark.parametrize(
    ("test_case", "expected", "restrict_test_imports"),
    [
        (
            TEST_IMPORT_CODE,
            {
                "2:0: PIR201 Importing test_*/*_test modules is restricted.",
                "4:0: PIR203 Importing 'conftest' is restricted.",
                "5:0: PIR205 Importing tests directory or tests subdirectories is restricted.",
                "7:0: PIR202 Importing from test_*.py/*_test.py modules is restricted.",
                "8:0: PIR202 Importing from test_*.py/*_test.py modules is restricted.",
                "9:0: PIR202 Importing from test_*.py/*_test.py modules is restricted.",
                "10:0: PIR202 Importing from test_*.py/*_test.py modules is restricted.",
                "11:0: PIR202 Importing from test_*.py/*_test.py modules is restricted.",
                "11:0: PIR206 Importing from tests directory or its subdirectories is restricted.",
                "12:0: PIR204 Importing from `conftest.py` modules is restricted.",
                "13:0: PIR202 Importing from test_*.py/*_test.py modules is restricted.",
                "13:0: PIR204 Importing from `conftest.py` modules is restricted.",
            },
            True,
        ),
        (
            "from conftest import function_test; from module_test import conftest",
            {
                "1:0: PIR202 Importing from test_*.py/*_test.py modules is restricted.",
                "1:0: PIR204 Importing from `conftest.py` modules is restricted.",
                "1:36: PIR202 Importing from test_*.py/*_test.py modules is restricted.",
                "1:36: PIR204 Importing from `conftest.py` modules is restricted.",
            },
            True,
        ),
        (
            TEST_IMPORT_CODE,
            set(),
            False,
        ),
    ],
)
def test_test_imports(
    test_case: str,
    expected: set,
    restrict_test_imports: bool,
    get_flake8_linter_results: callable,
) -> None:
    """Test wildcard imports."""
    options = {"checker_settings": Settings(**{"RESTRICT_TEST_IMPORTS": restrict_test_imports})}
    actual = get_flake8_linter_results(s=test_case, options=options, delimiter="\n")
    assert actual == expected


@pytest.mark.parametrize("restrict_test_imports", [True, False])
def test_test_import_settings_do_not_error(
    valid_custom_import_rules_imports: str,
    get_flake8_linter_results: callable,
    restrict_test_imports: bool,
) -> None:
    """Test that test import restrictions do not have an effect on regular import methods."""
    options = {"checker_settings": Settings(**{"RESTRICT_TEST_IMPORTS": restrict_test_imports})}
    actual = get_flake8_linter_results(
        s=valid_custom_import_rules_imports, options=options, delimiter="\n"
    )
    assert actual == set()
