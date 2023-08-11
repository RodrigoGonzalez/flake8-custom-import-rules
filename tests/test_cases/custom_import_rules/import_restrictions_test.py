""" Import restriction test cases.

- CIR102
- CIR103
- CIR104
- CIR105

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
from flake8_custom_import_rules.defaults import convert_to_dict
from flake8_custom_import_rules.utils.file_utils import get_module_name_from_filename
from flake8_custom_import_rules.utils.node_utils import root_package_name

CIR102 = ErrorCode.CIR102.full_message
CIR103 = ErrorCode.CIR103.full_message
CIR104 = ErrorCode.CIR104.full_message
CIR105 = ErrorCode.CIR105.full_message


@pytest.mark.parametrize(
    ("filename", "expected_current_module", "expected_restricted_identifiers", "expected"),
    [
        (
            "example_repos/my_base_module/my_second_base_package/module_one/file_one.py",
            "my_second_base_package.module_one.file_one",
            set(),
            2,
        ),
        (
            "example_repos/my_base_module/my_second_base_package/module_one/file_two.py",
            "my_second_base_package.module_one.file_two",
            set(),
            4,
        ),
        (
            "example_repos/my_base_module/my_second_base_package/module_two/file_one.py",
            "my_second_base_package.module_two.file_one",
            set(),
            8,
        ),
        (
            "example_repos/my_base_module/my_second_base_package/module_two/file_two.py",
            "my_second_base_package.module_two.file_two",
            set(),
            8,
        ),
        (
            "example_repos/my_base_module/my_second_base_package/file.py",
            "my_second_base_package.file",
            set(),
            8,
        ),
        (
            "example_repos/my_base_module/my_second_base_package/module_three.py",
            "my_second_base_package.module_three",
            set(),
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
    custom_import_rules_fixture: str,
    package_8: list[str],
) -> None:
    """Test restricted imports."""
    lines = custom_import_rules_fixture.split("\n")
    tree = ast.parse(custom_import_rules_fixture)
    options = {
        "base_packages": ["base_package", "my_second_base_package"],
        "import_restrictions": convert_to_dict(package_8),
        "checker_settings": Settings(
            **{
                "IMPORT_RESTRICTIONS": convert_to_dict(package_8),
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

    restricted_identifiers = plugin.restricted_identifiers
    assert isinstance(restricted_identifiers, defaultdict)
    assert plugin.import_rules.restricted_identifiers == restricted_identifiers
    # assert set(restricted_identifiers.keys()) == expected_restricted_identifiers

    errors = plugin.errors
    assert isinstance(errors, list)
    # assert len(errors) == expected


@pytest.mark.parametrize(
    ("test_case", "expected"),
    [
        (
            "example_repos/my_base_module/my_second_base_package/module_one/file_one.py",
            set(),
        ),
        (
            "example_repos/my_base_module/my_second_base_package/module_one/file_two.py",
            set(),
        ),
        (
            "example_repos/my_base_module/my_second_base_package/module_two/file_one.py",
            set(),
        ),
        (
            "example_repos/my_base_module/my_second_base_package/module_two/file_two.py",
            set(),
        ),
        (
            "example_repos/my_base_module/my_second_base_package/module_three.py",
            set(),
        ),
    ],
)
def test_import_restrictions(
    test_case: str,
    expected: set,
    get_flake8_linter_results: callable,
    package_8: list[str],
) -> None:
    """Test restricted imports."""
    filename = normalize_path(test_case)
    assert os.path.exists(filename)
    lines = pycodestyle.readlines(filename)
    identifier = get_module_name_from_filename(filename)
    root_package_name(identifier)
    options = {
        "base_packages": ["base_package", "my_second_base_package"],
        "import_restrictions": convert_to_dict(package_8),
        "checker_settings": Settings(
            **{
                "IMPORT_RESTRICTIONS": convert_to_dict(package_8),
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


def test_import_restrictions_import_settings_do_not_error(
    valid_custom_import_rules_imports: str,
    get_flake8_linter_results: callable,
) -> None:
    """Test restricted imports do not have an effect on regular import methods."""
    options = {
        "checker_settings": Settings(**{"IMPORT_RESTRICTIONS": {}}),
        "import_restrictions": {},
    }
    actual = get_flake8_linter_results(
        s=valid_custom_import_rules_imports, options=options, delimiter="\n"
    )
    assert actual == set()
