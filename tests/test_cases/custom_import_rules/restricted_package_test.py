""" Project only test cases.

To run this test file only:
poetry run python -m pytest -vvvrca tests/test_cases/custom_import_rules/restricted_package_test.py
"""
# import pycodestyle
# import pytest
# from flake8.utils import normalize_path
#
# from flake8_custom_import_rules.defaults import Settings
# from flake8_custom_import_rules.utils.node_utils import root_package_name
# from flake8_custom_import_rules.utils.parse_utils import get_module_name_from_filename
#
# CIR106 = "CIR106 Restricted package import."
# CIR107 = "CIR107 Restricted module import."
# MODULE_A_ERRORS = {}
#
#
# @pytest.mark.parametrize(
#     ("test_case", "restricted_imports", "expected"),
#     [
#         (
#             "example_repos/my_base_module/my_base_module/package_a/module_a.py",
#             ["my_base_module"],
#             MODULE_A_ERRORS,
#         ),
#         (
#             "example_repos/my_base_module/my_base_module/package_a/module_a.py",
#             ["my_base_module.package_a"],
#             MODULE_A_ERRORS,
#         ),
#     ],
# )
# def test_restricted_imports(
#     test_case: str,
#     restricted_imports: list[str],
#     expected: set,
#     get_flake8_linter_results: callable,
# ) -> None:
#     """Test restricted imports."""
#     filename = normalize_path(test_case)
#     lines = pycodestyle.readlines(filename)
#     identifier = get_module_name_from_filename(filename)
#     base_packages = root_package_name(identifier)
#     options = {
#         "base_packages": [base_packages],
#         "checker_settings": Settings(
#             **{
#                 "RESTRICTED_PACKAGES": restricted_imports,
#                 "RESTRICT_DYNAMIC_IMPORTS": False,
#                 "RESTRICT_LOCAL_IMPORTS": False,
#                 "RESTRICT_RELATIVE_IMPORTS": False,
#             }
#         ),
#     }
#     actual = get_flake8_linter_results(
#         s="".join(lines), options=options, delimiter="\n", filename=filename
#     )
#     assert actual == expected, sorted(actual)
#
#
# def test_restricted_import_settings_do_not_error(
#     valid_custom_import_rules_imports: str,
#     get_flake8_linter_results: callable,
# ) -> None:
#     """Test restricted imports do not have an effect on regular import methods."""
#     options = {"checker_settings": Settings(**{"RESTRICTED_PACKAGES": []})}
#     actual = get_flake8_linter_results(
#         s=valid_custom_import_rules_imports, options=options, delimiter="\n"
#     )
#     assert actual == set()
