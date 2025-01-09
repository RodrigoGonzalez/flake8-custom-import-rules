""" Tests for file_utils.py

To run this test file only:
poetry run python -m pytest -vvvrca tests/utils/file_utils_test.py
"""

import os
import sys

import pytest

from flake8_custom_import_rules.utils.file_utils import convert_module_to_file_paths
from flake8_custom_import_rules.utils.file_utils import convert_name
from flake8_custom_import_rules.utils.file_utils import find_prefix
from flake8_custom_import_rules.utils.file_utils import get_file_path_from_module_name
from flake8_custom_import_rules.utils.file_utils import get_module_name_from_filename
from flake8_custom_import_rules.utils.file_utils import get_relative_path_from_absolute_path

# We get the current directory of this file.
current_dir = os.path.dirname(os.path.abspath(__file__))

# We navigate to the root of the project.
root_dir = os.path.join(current_dir, "..", "..")


@pytest.mark.parametrize(
    "filename, parent, normalized_path, is_file, prefix, converted_name",
    [
        ("test.py", os.curdir, "normalized_test.py", True, "prefix_", "prefix_test"),
        ("not_exist.py", os.curdir, "normalized_not_exist.py", False, "", ""),
    ],
)
def test_get_module_name_from_filename(
    mocker, filename, parent, normalized_path, is_file, prefix, converted_name
):
    """Test get_module_name_from_filename."""
    # Mocking normalize_path function
    mocker.patch(
        "flake8_custom_import_rules.utils.file_utils.normalize_path", return_value=normalized_path
    )

    # Mocking os.path.isfile function
    mocker.patch("os.path.isfile", return_value=is_file)

    # Mocking find_prefix function
    mocker.patch("flake8_custom_import_rules.utils.file_utils.find_prefix", return_value=prefix)

    # Mocking convert_name function
    mocker.patch(
        "flake8_custom_import_rules.utils.file_utils.convert_name", return_value=converted_name
    )

    if is_file:
        assert get_module_name_from_filename(filename, parent) == converted_name
    else:
        with pytest.raises(FileNotFoundError):
            get_module_name_from_filename(filename, parent)


@pytest.mark.parametrize(
    "filename, sys_path, platform, expected_prefix, expected_export_string",
    [
        ("/path/to/file.py", ["/path/to", "/another/path"], "linux", "/path/to", None),
        (
            "/no/match/file.py",
            ["/path/to", "/another/path"],
            "win32",
            None,
            "set PYTHONPATH=%PYTHONPATH%;",
        ),
        (
            "/no/match/file.py",
            ["/path/to", "/another/path"],
            "linux",
            None,
            "export PYTHONPATH=$PYTHONPATH:",
        ),
    ],
)
def test_find_prefix(mocker, filename, sys_path, platform, expected_prefix, expected_export_string):
    """Test find_prefix."""
    mocker.patch.object(os.path, "abspath", return_value=filename)
    mocker.patch.object(sys, "platform", platform)
    mocker.patch.object(sys, "path", sys_path)

    if expected_prefix:
        assert find_prefix(filename) == expected_prefix
    else:
        with pytest.raises(ValueError) as e:
            find_prefix(filename)
        assert "Could not find prefix" in str(e.value)
        assert expected_export_string in str(e.value)


@pytest.mark.parametrize(
    "filename, prefix, expected_name",
    [
        ("/path/to/module.py", "/path/to", "module"),
        ("/path/to/__init__.py", "/path/to", "__init__"),
        ("/path/without/extension", "/path", "without.extension"),
        ("/path/with/special_chars.py", "/path", "with.special_chars"),
        ("", None, ""),  # Empty filename
    ],
)
def test_convert_name(mocker, filename, prefix, expected_name):
    """Test convert_name."""
    mocker.patch.object(os.path, "abspath", return_value=filename)

    assert convert_name(filename, prefix) == expected_name


@pytest.mark.parametrize(
    "module_name, expected_file_paths",
    [
        ("module", ["module.py", "module/__init__.py"]),
        ("nested.module", ["nested/module.py", "nested/module/__init__.py"]),
        ("", [".py", "/__init__.py"]),  # Empty module name
        ("special_chars.module", ["special_chars/module.py", "special_chars/module/__init__.py"]),
    ],
)
def test_convert_module_to_file_paths(module_name, expected_file_paths):
    """Test convert_module_to_file_paths."""
    assert convert_module_to_file_paths(module_name) == expected_file_paths


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
