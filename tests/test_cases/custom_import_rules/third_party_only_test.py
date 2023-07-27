""" Third-party only test cases.

To run this test file only:
poetry run python -m pytest -vvvrca tests/test_cases/custom_import_rules/third_party_only_test.py
"""
import pycodestyle
import pytest
from flake8.utils import normalize_path

from flake8_custom_import_rules.defaults import Settings
from flake8_custom_import_rules.utils.file_utils import get_module_name_from_filename
from flake8_custom_import_rules.utils.node_utils import root_package_name

CIR501 = "CIR501 Non-third party package import."
CIR502 = "CIR502 Non-third party module import."
MODULE_A_ERRORS = {
    (
        f"24:4: {CIR502} Using 'from my_base_module.package_c.package_e.module_e "
        f"import OldE as VersionedE'."
    ),
    f"87:8: {CIR502} Using 'from my_base_module.module_x import print_x'.",
    f"17:0: {CIR502} Using 'from my_base_module.package_b.module_b import B'.",
    f"86:8: {CIR502} Using 'from my_base_module.module_x import X'.",
    f"19:0: {CIR502} Using 'from my_base_module.package_c.package_d.module_d import D as DEE'.",
    f"21:0: {CIR502} Using 'from .module_a_relative import ARelative'.",
    f"16:0: {CIR502} Using 'from my_base_module import module_z'.",
    f"18:0: {CIR502} Using 'from my_base_module.package_c.module_c import C'.",
    f"15:0: {CIR501} Using 'import my_base_module.module_y'.",
    (
        f"26:4: {CIR502} Using 'from my_base_module.package_c.package_e.module_e import "
        f"EUpdated as VersionedE'."
    ),
}


@pytest.mark.parametrize(
    ("test_case", "third_party_only_imports", "expected"),
    [
        (
            "example_repos/my_base_module/my_base_module/package_a/module_a.py",
            ["my_base_module"],
            MODULE_A_ERRORS,
        ),
        (
            "example_repos/my_base_module/my_base_module/package_a/module_a.py",
            ["my_base_module.package_a"],
            MODULE_A_ERRORS,
        ),
        (
            "example_repos/my_base_module/my_base_module/module_x.py",
            ["my_base_module.module_x"],
            set(),
        ),
    ],
)
def test_third_party_only_imports(
    test_case: str,
    third_party_only_imports: list[str],
    expected: set,
    get_flake8_linter_results: callable,
) -> None:
    """Test third_party_only imports."""
    filename = normalize_path(test_case)
    lines = pycodestyle.readlines(filename)
    identifier = get_module_name_from_filename(filename)
    base_packages = root_package_name(identifier)
    options = {
        "base_packages": [base_packages],
        "checker_settings": Settings(
            **{
                "THIRD_PARTY_ONLY": third_party_only_imports,
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


def test_third_party_only_import_settings_do_not_error(
    valid_custom_import_rules_imports: str,
    get_flake8_linter_results: callable,
) -> None:
    """Test third_party_only imports do not have an effect on regular import methods."""
    options = {"checker_settings": Settings(**{"THIRD_PARTY_ONLY": []})}
    actual = get_flake8_linter_results(
        s=valid_custom_import_rules_imports, options=options, delimiter="\n"
    )
    assert actual == set()
