""" Test cases for restricting __main__ imports

PIR209 = "PIR209 Importing `__main__` is restricted."
PIR210 = "PIR210 Importing from `__main__.py` files is restricted."

To run this test file only:
poetry run python -m pytest -vvvrca tests/test_cases/project_import_rules/main_imports_test.py
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
                "2:0: PIR209 Importing `__main__` is restricted.",
                "7:0: PIR210 Importing from `__main__.py` files is restricted.",
                "8:0: PIR210 Importing from `__main__.py` files is restricted.",
            },
            True,
        ),
        (
            MAIN_IMPORT_CODE,
            set(),
            False,
        ),
        # check noqa works
        (
            "import __main__",
            {"1:0: PIR209 Importing `__main__` is restricted."},
            True,
        ),
        (
            "import __main__  # noqa",
            set(),
            True,
        ),
        (
            "import __main__  # NOQA",
            set(),
            True,
        ),
        (
            "import __main__  # noqa: PIR210",
            {"1:0: PIR209 Importing `__main__` is restricted."},
            True,
        ),
        (
            "import __main__  # noqa: PIR209",
            set(),
            True,
        ),
        (
            "import __main__  # noqa: PIR209, PIR210",
            set(),
            True,
        ),
        (
            "import __main__  # noqa: PIR209,PIR210",
            set(),
            True,
        ),
        (
            "import __main__  # NOQA: PIR209",
            set(),
            True,
        ),
        (
            "import __main__  # NOQA:PIR209",
            set(),
            True,
        ),
        (
            "import __main__  # NOQA: PIR209, PIR210",
            set(),
            True,
        ),
        (
            "import __main__  # NOQA: PIR209,PIR210",
            set(),
            True,
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
    actual = get_flake8_linter_results(s=test_case, options=options, delimiter="\n")
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
        s=valid_custom_import_rules_imports, options=options, delimiter="\n"
    )
    assert actual == set()
