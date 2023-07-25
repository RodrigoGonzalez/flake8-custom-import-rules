""" Standard library only test cases.

"""
from textwrap import dedent

import pytest

from flake8_custom_import_rules.defaults import Settings

LOCAL_IMPORT_CODE = dedent(
    """
    import os
    import pandas as pd
    from my_base_module.module_z import Z
    """
)


@pytest.mark.parametrize(
    ("test_case", "expected"),
    [
        (
            LOCAL_IMPORT_CODE,
            set(),
        ),
        (
            LOCAL_IMPORT_CODE,
            set(),
        ),
    ],
)
def test_std_lib_only_imports(
    test_case: str,
    expected: set,
    get_flake8_linter_results: callable,
) -> None:
    """Test std_lib_only imports."""
    options = {"checker_settings": Settings(**{"STD_LIB_ONLY": [""]})}
    actual = get_flake8_linter_results(s=test_case, options=options, delimiter="\n")
    assert actual == expected


@pytest.mark.parametrize("std_lib_only_imports", [True, False])
def test_std_lib_only_import_settings_do_not_error(
    valid_custom_import_rules_imports: str,
    get_flake8_linter_results: callable,
    std_lib_only_imports: bool,
) -> None:
    """Test std_lib_only imports do not have an effect on regular import methods."""
    options = {"checker_settings": Settings(**{"STD_LIB_ONLY": std_lib_only_imports})}
    actual = get_flake8_linter_results(
        s=valid_custom_import_rules_imports, options=options, delimiter="\n"
    )
    assert actual == set()
