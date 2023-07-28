""" Project only test cases.

To run this test file only:
poetry run python -m pytest -vvvrca tests/test_cases/custom_import_rules/restricted_package_test.py
"""
import ast
import logging
import os
from textwrap import dedent

import pytest
from flake8.utils import normalize_path

from flake8_custom_import_rules.defaults import Settings

logger = logging.Logger(__name__)

CIR106 = "CIR106 Restricted package import."
CIR107 = "CIR107 Restricted module import."
MODULE_A_ERRORS = set()


COMPLEX_IMPORTS = dedent(
    """
    import my_second_base_package.module_one.file_one
    import my_second_base_package.module_one.file_two
    import my_second_base_package.module_one
    import my_second_base_package.module_two.file_one
    import my_second_base_package.module_two.file_two
    import my_second_base_package.module_two
    import my_second_base_package.file
    import my_second_base_package
    import base_package
    import my_third_base_package

    from my_second_base_package.module_one.file_one import A
    from my_second_base_package.module_one.file_two import B
    from my_second_base_package.module_one import file_one
    from my_second_base_package.module_one import file_two
    from my_second_base_package.module_one import C
    from my_second_base_package.module_two import file_one
    from my_second_base_package.module_two import file_two
    from my_second_base_package.module_two import D
    from my_second_base_package.file import C
    from my_second_base_package import module_one
    from my_second_base_package import module_two
    from my_second_base_package import file
    from my_second_base_package import E
    from base_package import F
    from my_third_base_package import G
    """
)

RESTRICTED_PACKAGES = [
    "my_second_base_package",
    "my_second_base_package.module_one",
    "my_second_base_package.module_one.file_one",
    "my_third_base_package",
]


@pytest.mark.parametrize(
    ("test_case", "expected_current_module", "expected"),
    [
        (
            "example_repos/my_base_module/my_second_base_package/module_one/file_one.py",
            "my_second_base_package.module_one.file_one",
            list,
        ),
        # (
        #     "example_repos/my_base_module/my_second_base_package/module_one/file_two.py",
        #     "my_second_base_package.module_one.file_two",
        #     list,
        # ),
        # (
        #     "example_repos/my_base_module/my_second_base_package/module_two/file_one.py",
        #     "my_second_base_package.module_two.file_one",
        #     list,
        # ),
        # (
        #     "example_repos/my_base_module/my_second_base_package/module_two/file_two.py",
        #     "my_second_base_package.module_two.file_two",
        #     list,
        # ),
        # (
        #     "example_repos/my_base_module/my_second_base_package/file.py",
        #     "my_second_base_package.file",
        #     list
        # ),
    ],
)
def test_complex_imports(
    test_case: str,
    expected_current_module: str,
    expected: type,
    get_base_plugin: callable,
    capsys: pytest.CaptureFixture,
) -> None:
    """Test restricted imports."""
    # filename = normalize_path(test_case)
    lines = COMPLEX_IMPORTS.split("\n")
    tree = ast.parse(COMPLEX_IMPORTS)
    # identifier = get_module_name_from_filename(filename)
    # root_package_name(identifier)
    options = {
        "base_packages": ["base_package", "my_second_base_package"],
        "checker_settings": Settings(
            **{
                "RESTRICTED_PACKAGES": RESTRICTED_PACKAGES,
                "RESTRICT_DYNAMIC_IMPORTS": False,
                "RESTRICT_LOCAL_IMPORTS": False,
                "RESTRICT_RELATIVE_IMPORTS": False,
            }
        ),
    }
    logger.info("Call get_base_plugin.")
    plugin = get_base_plugin(tree=tree, filename=test_case, lines=lines, options=options)
    logger.info("Call get_run_list.")
    # capsys
    plugin.get_run_list()
    logger.info("Call get_import_nodes.")
    parsed_imports = [parsed_import for _, _, parsed_import, _ in plugin.get_import_nodes()]
    # for parsed_import in parsed_imports:
    #     print(
    #         f"Is '{parsed_import.import_statement}' allowed in '{current_module}'? "
    #         f"{is_import_restricted(parsed_import, current_module, restricted_imports)}"
    #     )
    assert isinstance(parsed_imports, expected)


@pytest.mark.parametrize(
    ("test_case", "restricted_packages", "expected"),
    [
        # (
        #     "example_repos/my_base_module/my_second_base_package/module_three.py",
        #     ["my_second_base_package"],
        #     set(),
        # ),
        (
            "example_repos/my_base_module/my_second_base_package/module_three.py",
            ["my_second_base_package.module_three"],
            set(),
        ),
        # (
        #     "example_repos/my_base_module/my_second_base_package/module_three.py",
        #     ["my_second_base_package.module_one", "my_second_base_package.module_two"],
        #     set(),
        # ),
        # (
        #     "example_repos/my_base_module/my_second_base_package/module_three.py",
        #     [
        #         "my_second_base_package.module_one",
        #         "my_second_base_package.module_two",
        #         "my_base_module",
        #     ],
        #     set(),
        # ),
        # (
        #     "example_repos/my_base_module/my_second_base_package/module_three.py",
        #     ["my_second_base_package.module_one"],
        #     set(),
        # ),
        # (
        #     "example_repos/my_base_module/my_second_base_package/module_three.py",
        #     ["my_second_base_package.module_one", "my_second_base_package"],
        #     set(),
        # ),
        # (
        #     "example_repos/my_base_module/my_second_base_package/module_three.py",
        #     ["my_base_module"],
        #     set(),
        # ),
        # (
        #     "example_repos/my_base_module/my_second_base_package/module_three.py",
        #     ["my_base_module.module_x"],
        #     set(),
        # ),
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
    # lines = pycodestyle.readlines(filename)
    # identifier = get_module_name_from_filename(filename)
    # root_package_name(identifier)
    # options = {
    #     "base_packages": ["my_second_base_package"],
    #     "checker_settings": Settings(
    #         **{
    #             "RESTRICTED_PACKAGES": restricted_packages,
    #             "RESTRICT_DYNAMIC_IMPORTS": False,
    #             "RESTRICT_LOCAL_IMPORTS": False,
    #             "RESTRICT_RELATIVE_IMPORTS": False,
    #         }
    #     ),
    # }
    # actual = get_flake8_linter_results(
    #     s="".join(lines), options=options, delimiter="\n", filename=filename
    # )
    # assert actual == expected, sorted(actual)


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
