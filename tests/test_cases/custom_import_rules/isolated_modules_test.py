""" First-party only test cases.

To run this test file only:
poetry run python -m pytest -vvvrca tests/test_cases/custom_import_rules/isolated_modules_test.py
"""
import pycodestyle
import pytest
from flake8.utils import normalize_path

from flake8_custom_import_rules.defaults import Settings
from flake8_custom_import_rules.utils.file_utils import get_module_name_from_filename
from flake8_custom_import_rules.utils.node_utils import root_package_name

CIR301 = "CIR301 Isolated package, imports from project disabled."
CIR302 = "CIR302 Isolated package, from imports from project disabled."
CIR303 = "CIR303 Isolated module, imports from project disabled."
CIR304 = "CIR304 Isolated module, from imports from project disabled."
CUSTOM_MSG = (
    ". Isolated module 'my_second_base_package.module_three' cannot import from project packages."
)

MODULE_THREE_PACKAGE_ERRORS = {
    f"12:0: {CIR302} Using 'from my_base_module.module_x import X'{CUSTOM_MSG}",
    f"13:0: {CIR302} Using 'from my_second_base_package.module_two import ModuleTwo'{CUSTOM_MSG}",
    f"11:0: {CIR301} Using 'import my_second_base_package.module_one'{CUSTOM_MSG}",
    f"10:0: {CIR301} Using 'import my_base_module.module_y'{CUSTOM_MSG}",
}

MODULE_THREE_MODULE_ERRORS = {
    f"10:0: {CIR303} Using 'import my_base_module.module_y'{CUSTOM_MSG}",
    f"12:0: {CIR304} Using 'from my_base_module.module_x import X'{CUSTOM_MSG}",
    f"11:0: {CIR303} Using 'import my_second_base_package.module_one'{CUSTOM_MSG}",
    f"13:0: {CIR304} Using 'from my_second_base_package.module_two import ModuleTwo'{CUSTOM_MSG}",
}


@pytest.mark.parametrize(
    ("test_case", "isolated_modules_imports", "expected"),
    [
        (
            "example_repos/my_base_module/my_second_base_package/module_three.py",
            ["my_second_base_package"],
            MODULE_THREE_PACKAGE_ERRORS,
        ),
        (
            "example_repos/my_base_module/my_second_base_package/module_three.py",
            ["my_second_base_package.module_three"],
            MODULE_THREE_MODULE_ERRORS,
        ),
    ],
)
def test_isolated_modules_imports(
    test_case: str,
    isolated_modules_imports: list[str],
    expected: set,
    get_flake8_linter_results: callable,
) -> None:
    """Test isolated_modules imports."""
    filename = normalize_path(test_case)
    lines = pycodestyle.readlines(filename)
    identifier = get_module_name_from_filename(filename)
    root_package_name(identifier)
    options = {
        "base_packages": ["my_second_base_package", "my_base_module"],
        "checker_settings": Settings(
            **{
                "ISOLATED_MODULES": isolated_modules_imports,
                "RESTRICT_DYNAMIC_IMPORTS": False,
                "RESTRICT_LOCAL_IMPORTS": False,
                "RESTRICT_RELATIVE_IMPORTS": False,
            }
        ),
    }
    actual = get_flake8_linter_results(
        s="".join(lines), options=options, delimiter="\n", filename=filename
    )
    assert actual == expected, sorted(actual)


def test_isolated_modules_import_settings_do_not_error(
    valid_custom_import_rules_imports: str,
    get_flake8_linter_results: callable,
) -> None:
    """Test isolated_modules imports do not have an effect on regular import methods."""
    options = {"checker_settings": Settings(**{"ISOLATED_MODULES": []})}
    actual = get_flake8_linter_results(
        s=valid_custom_import_rules_imports, options=options, delimiter="\n"
    )
    assert actual == set()
