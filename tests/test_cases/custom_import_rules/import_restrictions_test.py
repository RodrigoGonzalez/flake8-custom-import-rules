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

BASE_EXPECTED_RESTRICTED_IDENTIFIERS = {
    "my_base_module",
    "my_base_module.file",
    "my_base_module.module_one",
    "my_base_module.module_one.file_one",
    "my_base_module.module_one.file_two",
    "my_base_module.module_two",
    "my_base_module.module_two.file_one",
    "my_base_module.module_two.file_two",
    "my_third_base_package",
    "my_third_base_package.G",
    "my_third_base_package.file",
    "my_third_base_package.module_one",
    "my_third_base_package.module_one.file_one",
    "my_third_base_package.module_one.file_two",
    "my_third_base_package.module_two",
    "my_third_base_package.module_two.file_one",
    "my_third_base_package.module_two.file_two",
    "uuid",
    "uuid.UUID",
    "uuid.uuid4",
}


@pytest.mark.parametrize(
    (
        "filename",
        "expected_current_module",
        "expected_restricted_identifiers",
        "expected",
        "expected_errors",
    ),
    [
        (
            "example_repos/my_base_module/my_second_base_package/module_one/file_one.py",
            "my_second_base_package.module_one.file_one",
            BASE_EXPECTED_RESTRICTED_IDENTIFIERS.union(
                {
                    "my_second_base_package.file",
                    "my_second_base_package.module_one.file_two",
                    "my_second_base_package.module_two",
                    "my_second_base_package.module_two.file_one",
                    "my_second_base_package.module_two.file_two",
                    "my_second_base_package.file.C",
                    "my_second_base_package.module_one.file_two.B",
                    "my_second_base_package.module_two.D",
                }
            ),
            12,
            {
                f"10:0: {CIR102}",
                f"11:0: {CIR102}",
                f"14:0: {CIR104}",
                f"26:0: {CIR103}",
                f"28:0: {CIR103}",
                f"29:0: {CIR103}",
                f"33:0: {CIR103}",
                f"34:0: {CIR103}",
                f"3:0: {CIR104}",
                f"6:0: {CIR102}",
                f"8:0: {CIR102}",
                f"9:0: {CIR102}",
            },
        ),
        (
            "example_repos/my_base_module/my_second_base_package/module_one/file_two.py",
            "my_second_base_package.module_one.file_two",
            BASE_EXPECTED_RESTRICTED_IDENTIFIERS.union(
                {
                    "my_second_base_package.file",
                    "my_second_base_package.module_one.file_one",
                    "my_second_base_package.module_two",
                    "my_second_base_package.module_two.file_one",
                    "my_second_base_package.module_two.file_two",
                    "my_second_base_package.file.C",
                    "my_second_base_package.module_one.file_one.A",
                    "my_second_base_package.module_two.D",
                }
            ),
            12,
            {
                f"10:0: {CIR102}",
                f"11:0: {CIR102}",
                f"14:0: {CIR104}",
                f"25:0: {CIR103}",
                f"28:0: {CIR103}",
                f"29:0: {CIR103}",
                f"33:0: {CIR103}",
                f"34:0: {CIR103}",
                f"3:0: {CIR104}",
                f"5:0: {CIR102}",
                f"8:0: {CIR102}",
                f"9:0: {CIR102}",
            },
        ),
        (
            "example_repos/my_base_module/my_second_base_package/module_two/file_one.py",
            "my_second_base_package.module_two.file_one",
            BASE_EXPECTED_RESTRICTED_IDENTIFIERS.union(
                {
                    "my_second_base_package.file",
                    "my_second_base_package.module_one",
                    "my_second_base_package.module_one.file_one",
                    "my_second_base_package.module_one.file_two",
                    "my_second_base_package.module_two.file_two",
                    "my_second_base_package.file.C",
                    "my_second_base_package.module_one.C",
                    "my_second_base_package.module_one.file_one.A",
                    "my_second_base_package.module_one.file_two.B",
                }
            ),
            12,
            {
                f"11:0: {CIR102}",
                f"14:0: {CIR104}",
                f"25:0: {CIR103}",
                f"26:0: {CIR103}",
                f"29:0: {CIR103}",
                f"32:0: {CIR103}",
                f"34:0: {CIR103}",
                f"3:0: {CIR104}",
                f"5:0: {CIR102}",
                f"6:0: {CIR102}",
                f"7:0: {CIR102}",
                f"9:0: {CIR102}",
            },
        ),
        (
            "example_repos/my_base_module/my_second_base_package/module_two/file_two.py",
            "my_second_base_package.module_two.file_two",
            BASE_EXPECTED_RESTRICTED_IDENTIFIERS.union(
                {
                    "my_second_base_package.file",
                    "my_second_base_package.module_one",
                    "my_second_base_package.module_one.file_one",
                    "my_second_base_package.module_one.file_two",
                    "my_second_base_package.module_two.file_one",
                    "my_second_base_package.file.C",
                    "my_second_base_package.module_one.C",
                    "my_second_base_package.module_one.file_one.A",
                    "my_second_base_package.module_one.file_two.B",
                }
            ),
            12,
            {
                f"11:0: {CIR102}",
                f"14:0: {CIR104}",
                f"25:0: {CIR103}",
                f"26:0: {CIR103}",
                f"28:0: {CIR103}",
                f"32:0: {CIR103}",
                f"34:0: {CIR103}",
                f"3:0: {CIR104}",
                f"5:0: {CIR102}",
                f"6:0: {CIR102}",
                f"7:0: {CIR102}",
                f"8:0: {CIR102}",
            },
        ),
        (
            "example_repos/my_base_module/my_second_base_package/file.py",
            "my_second_base_package.file",
            BASE_EXPECTED_RESTRICTED_IDENTIFIERS.union(
                {
                    "my_second_base_package.module_one",
                    "my_second_base_package.module_one.C",
                    "my_second_base_package.module_one.file_one",
                    "my_second_base_package.module_one.file_one.A",
                    "my_second_base_package.module_one.file_two",
                    "my_second_base_package.module_one.file_two.B",
                    "my_second_base_package.module_two",
                    "my_second_base_package.module_two.D",
                    "my_second_base_package.module_two.file_one",
                    "my_second_base_package.module_two.file_two",
                }
            ),
            14,
            {
                f"10:0: {CIR102}",
                f"14:0: {CIR104}",
                f"25:0: {CIR103}",
                f"26:0: {CIR103}",
                f"28:0: {CIR103}",
                f"29:0: {CIR103}",
                f"32:0: {CIR103}",
                f"33:0: {CIR103}",
                f"3:0: {CIR104}",
                f"5:0: {CIR102}",
                f"6:0: {CIR102}",
                f"7:0: {CIR102}",
                f"8:0: {CIR102}",
                f"9:0: {CIR102}",
            },
        ),
        (
            "example_repos/my_base_module/my_second_base_package/module_three.py",
            "my_second_base_package.module_three",
            BASE_EXPECTED_RESTRICTED_IDENTIFIERS,
            2,
            {
                f"14:0: {CIR104}",
                f"3:0: {CIR104}",
            },
        ),
    ],
)
def test_complex_imports(
    filename: str,
    expected_current_module: str,
    expected_restricted_identifiers: set,
    expected: int,
    expected_errors: set[str],
    get_base_plugin: callable,
    custom_import_rules_fixture: str,
    package_10: list[str],
) -> None:
    """Test restricted imports."""
    lines = custom_import_rules_fixture.split("\n")
    tree = ast.parse(custom_import_rules_fixture)
    options = {
        "base_packages": ["my_second_base_package"],
        "import_restrictions": convert_to_dict(package_10),
        "checker_settings": Settings(
            **{
                "IMPORT_RESTRICTIONS": convert_to_dict(package_10),
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
    # for key in restricted_identifiers.keys():
    #     assert restricted_identifiers[key]["project_package"] == key.startswith(
    #         "my_second_base_package"
    #     )

    assert set(restricted_identifiers.keys()) == expected_restricted_identifiers

    errors = plugin.errors
    assert isinstance(errors, list)
    assert len(errors) == expected
    assert plugin.errors_set == expected_errors


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
            {f"2:0: {CIR104}"},
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
    package_10: list[str],
) -> None:
    """Test restricted imports."""
    filename = normalize_path(test_case)
    assert os.path.exists(filename)
    lines = pycodestyle.readlines(filename)
    identifier = get_module_name_from_filename(filename)
    root_package_name(identifier)
    options = {
        "base_packages": ["base_package", "my_second_base_package"],
        "import_restrictions": convert_to_dict(package_10),
        "checker_settings": Settings(
            **{
                "IMPORT_RESTRICTIONS": convert_to_dict(package_10),
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
