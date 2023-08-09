""" Import restriction test cases.

To run this test file only:
poetry run python -m pytest -vvvrca tests/test_cases/custom_import_rules/import_restrictions_test.py
"""
import ast
import os
from collections import defaultdict

import pycodestyle
import pytest
from flake8.utils import normalize_path

from flake8_custom_import_rules.codes.error_codes import ErrorCode
from flake8_custom_import_rules.core.import_rules import CustomImportRules
from flake8_custom_import_rules.defaults import Settings
from flake8_custom_import_rules.utils.file_utils import get_module_name_from_filename
from flake8_custom_import_rules.utils.node_utils import root_package_name

CIR106 = ErrorCode.CIR106.full_message
CIR107 = ErrorCode.CIR107.full_message

RESTRICTED_PACKAGES = [
    "my_second_base_package",
    "my_second_base_package.module_one",
    "my_second_base_package.module_one.file_one",
    "my_third_base_package",
]


@pytest.mark.parametrize(
    ("filename", "expected_current_module", "expected_restricted_identifiers", "expected"),
    [
        (
            "example_repos/my_base_module/my_second_base_package/module_one/file_one.py",
            "my_second_base_package.module_one.file_one",
            {"my_third_base_package"},
            2,
        ),
        (
            "example_repos/my_base_module/my_second_base_package/module_one/file_two.py",
            "my_second_base_package.module_one.file_two",
            {"my_second_base_package.module_one.file_one", "my_third_base_package"},
            4,
        ),
        (
            "example_repos/my_base_module/my_second_base_package/module_two/file_one.py",
            "my_second_base_package.module_two.file_one",
            {
                "my_second_base_package.module_one.file_one",
                "my_second_base_package.module_one",
                "my_third_base_package",
            },
            8,
        ),
        (
            "example_repos/my_base_module/my_second_base_package/module_two/file_two.py",
            "my_second_base_package.module_two.file_two",
            {
                "my_second_base_package.module_one.file_one",
                "my_second_base_package.module_one",
                "my_third_base_package",
            },
            8,
        ),
        (
            "example_repos/my_base_module/my_second_base_package/file.py",
            "my_second_base_package.file",
            {
                "my_second_base_package.module_one.file_one",
                "my_second_base_package.module_one",
                "my_third_base_package",
            },
            8,
        ),
    ],
)
def test_complex_imports(
    filename: str,
    expected_current_module: str,
    expected_restricted_identifiers: set,
    expected: int,
    get_base_plugin: callable,
    custom_import_rules: str,
) -> None:
    """Test restricted imports."""
    lines = custom_import_rules.split("\n")
    tree = ast.parse(custom_import_rules)
    options = {
        "base_packages": ["base_package", "my_second_base_package"],
        "restricted_packages": RESTRICTED_PACKAGES,
        "checker_settings": Settings(
            **{
                "RESTRICTED_PACKAGES": RESTRICTED_PACKAGES,
                "RESTRICT_DYNAMIC_IMPORTS": False,
                "RESTRICT_LOCAL_IMPORTS": False,
                "RESTRICT_RELATIVE_IMPORTS": False,
            }
        ),
    }
    plugin = get_base_plugin(tree=tree, filename=filename, lines=lines, options=options)

    import_rules = plugin.import_rules
    assert isinstance(import_rules, CustomImportRules)
    plugin.get_run_list()
    errors = plugin.errors
    assert isinstance(errors, list)
    assert len(errors) == expected
    restricted_identifiers = plugin.restricted_identifiers
    assert isinstance(restricted_identifiers, defaultdict)
    assert set(restricted_identifiers.keys()) == expected_restricted_identifiers


@pytest.mark.parametrize(
    ("test_case", "restricted_packages", "expected"),
    [
        (
            "example_repos/my_base_module/my_second_base_package/module_three.py",
            ["my_second_base_package"],
            set(),
        ),
        (
            "example_repos/my_base_module/my_second_base_package/module_three.py",
            ["my_second_base_package.module_three"],
            set(),
        ),
        (
            "example_repos/my_base_module/my_second_base_package/module_three.py",
            ["my_second_base_package.module_one", "my_second_base_package.module_two"],
            set(),
        ),
        (
            "example_repos/my_base_module/my_second_base_package/module_three.py",
            [
                "my_second_base_package.module_one",
                "my_second_base_package.module_two",
                "my_base_module",
            ],
            set(),
        ),
        (
            "example_repos/my_base_module/my_second_base_package/module_three.py",
            ["my_second_base_package.module_one"],
            set(),
        ),
        (
            "example_repos/my_base_module/my_second_base_package/module_three.py",
            ["my_second_base_package.module_one", "my_second_base_package"],
            set(),
        ),
        (
            "example_repos/my_base_module/my_second_base_package/module_three.py",
            ["my_base_module"],
            set(),
        ),
        (
            "example_repos/my_base_module/my_second_base_package/module_three.py",
            ["my_base_module.module_x"],
            {
                (
                    "11:0: CIR107 Restricted module import. Using "
                    "'from my_base_module.module_x import X'. "
                    "Restricted package/module cannot be imported outside package/module."
                )
            },
        ),
    ],
)
def test_restricted_packages(
    test_case: str,
    restricted_packages: list[str],
    expected: set,
    get_flake8_linter_results: callable,
) -> None:
    """Test restricted imports."""
    filename = normalize_path(test_case)
    assert os.path.exists(filename)
    lines = pycodestyle.readlines(filename)
    identifier = get_module_name_from_filename(filename)
    root_package_name(identifier)
    options = {
        "base_packages": ["base_package", "my_second_base_package"],
        "restricted_packages": restricted_packages,
        "checker_settings": Settings(
            **{
                "RESTRICTED_PACKAGES": restricted_packages,
                "RESTRICT_DYNAMIC_IMPORTS": False,
                "RESTRICT_LOCAL_IMPORTS": False,
                "RESTRICT_RELATIVE_IMPORTS": False,
            }
        ),
    }
    actual = get_flake8_linter_results(
        s="".join(lines), options=options, delimiter="\n", filename=filename
    )
    assert set(actual) == expected, sorted(actual)


def test_restricted_import_settings_do_not_error(
    valid_custom_import_rules_imports: str,
    get_flake8_linter_results: callable,
) -> None:
    """Test restricted imports do not have an effect on regular import methods."""
    options = {"checker_settings": Settings(**{"RESTRICTED_PACKAGES": []})}
    actual = get_flake8_linter_results(
        s=valid_custom_import_rules_imports, options=options, delimiter="\n"
    )
    assert actual == set()
