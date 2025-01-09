""" Tests for node_utils.py

To run this test file only:
poetry run python -m pytest -vvvrca tests/utils/node_utils_test.py
"""

import ast
from collections import defaultdict
from functools import partial

import pytest

from flake8_custom_import_rules.utils.node_utils import check_private_module_import
from flake8_custom_import_rules.utils.node_utils import generate_identifier_path
from flake8_custom_import_rules.utils.node_utils import get_module_info_from_import_node
from flake8_custom_import_rules.utils.node_utils import get_name_info_from_import_node


@pytest.fixture(scope="function", autouse=True)
def get_import_node() -> partial:
    """Generate an AST from a file."""

    def import_node(s: str) -> ast.AST:
        """Generate an AST from a file name."""
        tree = ast.parse(s)
        return tree.body[0]

    return partial(import_node)


@pytest.mark.parametrize(
    ("test_case", "expected"),
    [
        ("module", False),
        ("module.submodule", False),
        ("module._submodule", True),
        ("_module", True),
        ("__main__", False),
    ],
)
def test_check_private_module_import(test_case: str, expected: bool) -> None:
    """Test check_private_module_imports."""
    actual = check_private_module_import(test_case)
    assert actual == expected


@pytest.mark.parametrize(
    "node,expected",
    [
        # Attribute
        (ast.parse("a.b").body[0].value, ["a", "b"]),
        # Call
        (ast.parse("func()").body[0].value, ["func"]),
        # Name
        (ast.parse("variable_name").body[0].value, ["variable_name"]),
        # Subscript
        (ast.parse("a[b]").body[0].value, ["a", "b"]),
        # Constant
        (ast.parse("42").body[0].value, ["42"]),
        # Nested Attribute and Call
        (ast.parse("a.b.c()").body[0].value, ["a", "b", "c"]),
        # Nested Subscript
        (ast.parse("a[b][c]").body[0].value, ["a", "b", "c"]),
    ],
)
def test_generate_identifier_path(node, expected):
    result = list(generate_identifier_path(node))
    assert result == expected


def test_get_module_info_from_import_node(get_import_node: callable) -> None:
    """Test get_module_info_from_import_node."""
    import_node = get_import_node("import os")
    module_info = get_module_info_from_import_node(import_node)
    assert isinstance(module_info, defaultdict)
    module_dict = module_info["os"]
    assert isinstance(module_dict, defaultdict)
    assert set(module_dict.keys()) == {
        "alias_col_offset",
        "asname",
        "col_offset",
        "import_statement",
        "lineno",
        "module",
        "node_col_offset",
        "package",
        "package_names",
        "private_identifier_import",
        "private_module_import",
    }
    assert module_dict["module"] == "os"
    assert module_dict["asname"] is None
    assert module_dict["lineno"] == 1
    assert module_dict["col_offset"] == 0
    assert module_dict["node_col_offset"] == 0
    assert module_dict["alias_col_offset"] == 7
    assert module_dict["package"] == "os"
    assert module_dict["package_names"] == ["os"]
    assert module_dict["private_identifier_import"] is False
    assert module_dict["private_module_import"] is False
    assert module_dict["import_statement"] == "import os"


def test_get_name_info_from_import_node(get_import_node: callable) -> None:
    """Test get_name_info_from_import_node."""
    import_node = get_import_node("from sys import modules")
    name_info = get_name_info_from_import_node(import_node)
    assert isinstance(name_info, defaultdict)
    name_dict = name_info["modules"]
    assert isinstance(name_dict, defaultdict)
    assert set(name_dict.keys()) == {
        "name",
        "module",
        "asname",
        "lineno",
        "col_offset",
        "node_col_offset",
        "alias_col_offset",
        "package",
        "package_names",
        "level",
        "private_identifier_import",
        "private_module_import",
        "import_statement",
    }
    assert name_dict["name"] == "modules"
    assert name_dict["module"] == "sys"
    assert name_dict["asname"] is None
    assert name_dict["lineno"] == 1
    assert name_dict["col_offset"] == 0
    assert name_dict["node_col_offset"] == 0
    assert name_dict["alias_col_offset"] == 16
    assert name_dict["package"] == "sys"
    assert name_dict["package_names"] == ["sys"]
    assert name_dict["level"] == 0
    assert name_dict["private_identifier_import"] is False
    assert name_dict["private_module_import"] is False
    assert name_dict["import_statement"] == "from sys import modules"
