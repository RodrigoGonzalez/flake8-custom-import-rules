""" Tests for file_utils.py

To run this test file only:
poetry run python -m pytest -vvvrca tests/utils/file_utils_test.py
"""
import os

import pytest

from flake8_custom_import_rules.utils.file_utils import get_file_path_from_module_name
from flake8_custom_import_rules.utils.file_utils import get_relative_path_from_absolute_path

# We get the current directory of this file.
current_dir = os.path.dirname(os.path.abspath(__file__))

# We navigate to the root of the project.
root_dir = os.path.join(current_dir, "..", "..")


@pytest.mark.parametrize(
    ("module_name", "expected_abs_path", "expected_rel_path"),
    [
        (
            "my_second_base_package.module_one",
            os.path.join(
                root_dir,
                "example_repos",
                "my_base_module",
                "my_second_base_package",
                "module_one",
                "__init__.py",
            ),
            "example_repos/my_base_module/my_second_base_package/module_one/__init__.py",
        ),
        (
            "my_second_base_package.module_two",
            os.path.join(
                root_dir,
                "example_repos",
                "my_base_module",
                "my_second_base_package",
                "module_two",
                "__init__.py",
            ),
            "example_repos/my_base_module/my_second_base_package/module_two/__init__.py",
        ),
        (
            "my_second_base_package.module_three",
            os.path.join(
                root_dir,
                "example_repos",
                "my_base_module",
                "my_second_base_package",
                "module_three.py",
            ),
            "example_repos/my_base_module/my_second_base_package/module_three.py",
        ),
        (
            "my_second_base_package.module_one.file_one",
            os.path.join(
                root_dir,
                "example_repos",
                "my_base_module",
                "my_second_base_package",
                "module_one",
                "file_one.py",
            ),
            "example_repos/my_base_module/my_second_base_package/module_one/file_one.py",
        ),
        (
            "my_second_base_package.module_one.file_two",
            os.path.join(
                root_dir,
                "example_repos",
                "my_base_module",
                "my_second_base_package",
                "module_one",
                "file_two.py",
            ),
            "example_repos/my_base_module/my_second_base_package/module_one/file_two.py",
        ),
        (
            "my_second_base_package.module_two.file_two",
            os.path.join(
                root_dir,
                "example_repos",
                "my_base_module",
                "my_second_base_package",
                "module_two",
                "file_two.py",
            ),
            "example_repos/my_base_module/my_second_base_package/module_two/file_two.py",
        ),
        (
            "my_second_base_package.file",
            os.path.join(
                root_dir,
                "example_repos",
                "my_base_module",
                "my_second_base_package",
                "file.py",
            ),
            "example_repos/my_base_module/my_second_base_package/file.py",
        ),
    ],
)
def test_get_file_path_from_module_name(
    module_name: str,
    expected_abs_path: str,
    expected_rel_path: str,
) -> None:
    """Test get_file_path_from_module_name."""
    actual = get_file_path_from_module_name(module_name)
    assert actual == os.path.normpath(expected_abs_path)
    assert get_relative_path_from_absolute_path(actual) == expected_rel_path


def test_get_file_path_from_module_name__none() -> None:
    """Test get_file_path_from_module_name when module does not exist."""
    actual = get_file_path_from_module_name("none")
    assert actual is None
