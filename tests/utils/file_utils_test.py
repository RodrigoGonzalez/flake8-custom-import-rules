""" Tests for file_utils.py

To run this test file only:
poetry run python -m pytest -vvvrca tests/utils/file_utils_test.py
"""
import pytest

from flake8_custom_import_rules.utils.file_utils import get_file_path_from_module_name
from flake8_custom_import_rules.utils.file_utils import get_relative_path_from_absolute_path


@pytest.mark.parametrize(
    ("module_name", "expected"),
    [
        (
            "my_second_base_package.module_one",
            "example_repos/my_base_module/my_second_base_package/module_one/__init__.py",
        ),
        (
            "my_second_base_package.module_two",
            "example_repos/my_base_module/my_second_base_package/module_two/__init__.py",
        ),
        (
            "my_second_base_package.module_three",
            "example_repos/my_base_module/my_second_base_package/module_three.py",
        ),
        # (
        #     "os",
        #     (
        #             '/opt/homebrew/Cellar/python@3.10/3.10.12_1/Frameworks/Python.'
        #             'framework/Versions/3.10/lib/python3.10/os.py'
        #     ),
        # )
        (
            "my_second_base_package.module_one.file_one",
            "example_repos/my_base_module/my_second_base_package/module_one/file_one.py",
        ),
        (
            "my_second_base_package.module_one.file_two",
            "example_repos/my_base_module/my_second_base_package/module_one/file_two.py",
        ),
        (
            "my_second_base_package.module_two.file_two",
            "example_repos/my_base_module/my_second_base_package/module_two/file_two.py",
        ),
        (
            "my_second_base_package.file",
            "example_repos/my_base_module/my_second_base_package/file.py",
        ),
        (
            "base_package.file",
            None,
        ),
    ],
)
def test_get_file_path_from_module_name(module_name: str, expected: str) -> None:
    """Test get_file_path_from_module_name."""
    actual = get_file_path_from_module_name(module_name)
    if actual:
        actual = actual.split("flake8-custom-import-rules/")[1]
    assert get_relative_path_from_absolute_path(actual) == expected
