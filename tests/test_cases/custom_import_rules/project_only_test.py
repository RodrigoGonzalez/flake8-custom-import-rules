""" Project only test cases.

- CIR201
- CIR202

To run this test file only:
poetry run python -m pytest -vvvrca tests/test_cases/custom_import_rules/project_only_test.py
"""

import pycodestyle
import pytest
from flake8.utils import normalize_path

from flake8_custom_import_rules.codes.error_codes import ErrorCode
from flake8_custom_import_rules.defaults import Settings
from flake8_custom_import_rules.utils.file_utils import get_module_name_from_filename
from flake8_custom_import_rules.utils.node_utils import root_package_name

CIR201 = ErrorCode.CIR201.full_message
CIR202 = ErrorCode.CIR202.full_message

MODULE_THREE_ERRORS = {
    f"6:0: {CIR202} Using 'from attrs import define'.",
    f"7:0: {CIR202} Using 'from attrs import field'.",
}


@pytest.mark.parametrize(
    ("test_case", "project_only_imports", "expected"),
    [
        (
            "example_repos/my_base_module/my_second_base_package/module_three.py",
            ["my_second_base_package"],
            MODULE_THREE_ERRORS,
        ),
        (
            "example_repos/my_base_module/my_second_base_package/module_three.py",
            ["my_second_base_package.module_three"],
            MODULE_THREE_ERRORS,
        ),
    ],
)
def test_project_only_imports(
    test_case: str,
    project_only_imports: list[str],
    expected: set,
    get_flake8_linter_results: callable,
) -> None:
    """Test project_only imports."""
    filename = normalize_path(test_case)
    lines = pycodestyle.readlines(filename)
    identifier = get_module_name_from_filename(filename)
    root_package_name(identifier)
    options = {
        "base_packages": ["my_second_base_package", "my_base_module"],
        "checker_settings": Settings(
            **{
                "PROJECT_ONLY": project_only_imports,
                "RESTRICT_DYNAMIC_IMPORTS": False,
                "RESTRICT_LOCAL_SCOPE_IMPORTS": False,
                "RESTRICT_RELATIVE_IMPORTS": False,
            }
        ),
    }
    actual = get_flake8_linter_results(
        s="".join(lines), options=options, delimiter="\n", filename=filename
    )
    assert actual == expected, sorted(actual)


def test_project_only_import_settings_do_not_error(
    valid_custom_import_rules_imports: str,
    get_flake8_linter_results: callable,
) -> None:
    """Test project_only imports do not have an effect on regular import methods."""
    options = {"checker_settings": Settings(**{"PROJECT_ONLY": []})}
    actual = get_flake8_linter_results(
        s=valid_custom_import_rules_imports, options=options, delimiter="\n"
    )
    assert actual == set()
