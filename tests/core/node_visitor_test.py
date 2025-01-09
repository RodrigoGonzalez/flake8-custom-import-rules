"""
Node visitor tests.

To run this test file only:
poetry run python -m pytest -vvvrca tests/core/node_visitor_test.py
"""

import ast

import pytest

from flake8_custom_import_rules.core.node_visitor import CustomImportRulesVisitor
from flake8_custom_import_rules.core.nodes import ImportType
from flake8_custom_import_rules.core.nodes import ParsedClassDef
from flake8_custom_import_rules.core.nodes import ParsedFromImport
from flake8_custom_import_rules.core.nodes import ParsedFunctionDef
from flake8_custom_import_rules.core.nodes import ParsedStraightImport


@pytest.fixture(scope="function")
def import_visitor():
    """Return an instance of the import visitor."""
    return CustomImportRulesVisitor([], None)


@pytest.fixture()
def parsed_import():
    """
    Return a function that creates an instance of a parsed import or a parsed
    from import using default values when unspecified.
    """

    def _create_parsed_import(
        import_type=ImportType.STDLIB,
        module="os",
        name=None,
        asname=None,
        lineno=1,
        col_offset=0,
        level=0,
        package="os",
        package_names=None,
        alias_col_offset=7,
        import_statement="",
    ):
        if name:
            return ParsedFromImport(
                import_type=import_type,
                module=module,
                name=name,
                asname=asname,
                lineno=lineno,
                col_offset=col_offset,
                level=level,
                package=package,
                package_names=package_names,
                node_col_offset=col_offset,
                alias_col_offset=alias_col_offset,
                private_identifier_import=False,
                private_module_import=False,
                import_statement=import_statement,
            )
        return ParsedStraightImport(
            import_type=import_type,
            module=module,
            asname=asname,
            lineno=lineno,
            col_offset=col_offset,
            package=package,
            package_names=package_names,
            node_col_offset=col_offset,
            alias_col_offset=alias_col_offset,
            private_identifier_import=False,
            private_module_import=False,
            import_statement=import_statement,
        )

    return _create_parsed_import


def test_visit_import_simple(parsed_import, import_visitor):
    """Test that the visit_Import method correctly parses an import statement."""
    source = "import os"
    tree = ast.parse(source)
    visitor = import_visitor
    visitor.visit(tree)
    assert len(visitor.nodes) == 1
    assert visitor.nodes[0] == parsed_import(
        name=None, package_names=["os"], import_statement="import os"
    )


@pytest.mark.usefixtures("parsed_import")
def test_visit_import_alias(parsed_import, import_visitor):
    """Test that the `visit_Import` method correctly parses an`import` that includes an alias."""
    source = "import os as my_os"
    tree = ast.parse(source)
    visitor = import_visitor
    visitor.visit(tree)
    assert len(visitor.nodes) == 1
    assert visitor.nodes[0] == parsed_import(
        asname="my_os", package_names=["os"], import_statement="import os as my_os"
    )


def test_visit_import_from_simple(import_visitor):
    """
    Test that the`visit_ImportFrom` method correctly parses a
    `from ... import ...` statement`.
    """
    source = "from os import path"
    tree = ast.parse(source)
    visitor = import_visitor
    visitor.visit(tree)
    assert len(visitor.nodes) == 1
    assert visitor.nodes[0] == ParsedFromImport(
        import_type=ImportType.STDLIB,
        module="os",
        name="path",
        asname=None,
        lineno=1,
        col_offset=0,
        level=0,
        package="os",
        package_names=["os"],
        node_col_offset=0,
        alias_col_offset=15,
        private_identifier_import=False,
        private_module_import=False,
        import_statement="from os import path",
    )


def test_visit_import_from_alias(parsed_import, import_visitor):
    """
    Test that the `visit_ImportFrom` method correctly parses a `from ... import ...`
    statement with an alias
    """
    source = "from os import path as my_path"
    tree = ast.parse(source)
    visitor = import_visitor
    visitor.visit(tree)
    assert len(visitor.nodes) == 1
    assert visitor.nodes[0] == parsed_import(
        name="path",
        asname="my_path",
        level=0,
        package_names=["os"],
        alias_col_offset=15,
        import_statement="from os import path as my_path",
    )


def test_visit_import_from_relative(parsed_import, import_visitor):
    """
    Test that the `visit_ImportFrom` method correctly parses a `from ... import ...`
    statement with a relative import.
    """
    source = "from . import sibling_module"
    tree = ast.parse(source)
    visitor = import_visitor
    visitor.visit(tree)
    assert len(visitor.nodes) == 1
    assert visitor.nodes[0] == ParsedFromImport(
        import_type=ImportType.RELATIVE,
        module="",
        name="sibling_module",
        asname=None,
        lineno=1,
        col_offset=0,
        level=1,
        package=None,
        package_names=[],
        node_col_offset=0,
        alias_col_offset=14,
        private_identifier_import=False,
        private_module_import=False,
        import_statement="from . import sibling_module",
    )


def test_visit_class_def(import_visitor):
    """Test that the `visit_ClassDef` method correctly parses a class definition."""
    source = "class MyClass:\n    pass"
    tree = ast.parse(source)
    visitor = import_visitor
    visitor.visit(tree)

    assert len(visitor.nodes) == 1


def test_visit_class_def_base_class(import_visitor):
    """Test that the`visit_ClassDef`method correctly parses a class definition with a base class."""
    source = "class MyClass(BaseClass):\n    pass"
    tree = ast.parse(source)
    visitor = import_visitor
    visitor.visit(tree)
    assert len(visitor.nodes) == 1
    assert visitor.nodes[0] == ParsedClassDef(
        name="MyClass",
        lineno=1,
        col_offset=0,
    )


def test_visit_function_def(import_visitor):
    """Test that the`visit_FunctionDef` method correctly parses a function definition."""
    source = "def my_function():\n    pass"
    tree = ast.parse(source)
    visitor = import_visitor
    visitor.visit(tree)
    assert len(visitor.nodes) == 1
    assert visitor.nodes[0] == ParsedFunctionDef(
        name="my_function",
        lineno=1,
        col_offset=0,
    )


def test_visit_import_multiple(import_visitor):
    """
    Test that the`visit_Import` method correctly parses multiple
    `import` statements.
    """
    source = "import os, sys"
    tree = ast.parse(source)
    visitor = import_visitor
    visitor.visit(tree)
    assert len(visitor.nodes) == 2
    assert visitor.nodes[0] == ParsedStraightImport(
        import_type=ImportType.STDLIB,
        module="os",
        asname=None,
        lineno=1,
        col_offset=0,
        package="os",
        package_names=["os"],
        node_col_offset=0,
        alias_col_offset=7,
        private_identifier_import=False,
        private_module_import=False,
        import_statement="import os, sys",
    )
    assert visitor.nodes[1] == ParsedStraightImport(
        import_type=ImportType.STDLIB,
        module="sys",
        asname=None,
        lineno=1,
        col_offset=0,
        package="sys",
        package_names=["sys"],
        node_col_offset=0,
        alias_col_offset=11,
        private_identifier_import=False,
        private_module_import=False,
        import_statement="import os, sys",
    )


def test_visit_import_from_multiple(import_visitor):
    """
    Test that the`visit_ImportFrom`method correctly parses a `from ... import ...`
    statement with multiple names"""
    source = "from os import path, environ"
    tree = ast.parse(source)
    visitor = import_visitor
    visitor.visit(tree)
    assert len(visitor.nodes) == 2
    assert visitor.nodes[0] == ParsedFromImport(
        import_type=ImportType.STDLIB,
        module="os",
        name="path",
        asname=None,
        lineno=1,
        col_offset=0,
        level=0,
        package="os",
        package_names=["os"],
        node_col_offset=0,
        alias_col_offset=15,
        private_identifier_import=False,
        private_module_import=False,
        import_statement="from os import path, environ",
    )
    assert visitor.nodes[1] == ParsedFromImport(
        import_type=ImportType.STDLIB,
        module="os",
        name="environ",
        asname=None,
        lineno=1,
        col_offset=0,
        level=0,
        package="os",
        package_names=["os"],
        node_col_offset=0,
        alias_col_offset=21,
        private_identifier_import=False,
        private_module_import=False,
        import_statement="from os import path, environ",
    )


@pytest.mark.usefixtures("parsed_import")
def test_complex_code(parsed_import, import_visitor):
    """Test that the`CustomImportRulesVisitor` correctly handles a complex source
    code file with multiple imports, class definitions, and function definitions.
    """
    source = (
        "\n"
        "import os\n"
        "from sys import argv\n"
        "import requests as req\n"
        "\n"
        "class MyClass:\n"
        "    def method(self):\n"
        "        pass\n"
        "\n"
        "def my_function():\n"
        "    pass\n"
        ""
    )
    tree = ast.parse(source)
    visitor = import_visitor
    visitor.visit(tree)
    assert len(visitor.nodes) == 6  # Check the first import statement
    assert visitor.nodes[0] == parsed_import(
        import_type=ImportType.STDLIB,
        module="os",
        lineno=2,
        package_names=["os"],
        import_statement="import os",
    )

    # Check the second import statement
    assert visitor.nodes[1] == parsed_import(
        module="sys",
        name="argv",
        lineno=3,
        package="sys",
        package_names=["sys"],
        alias_col_offset=16,
        import_statement="from sys import argv",
    )
    # Check the third import statement
    assert visitor.nodes[2] == parsed_import(
        import_type=ImportType.THIRD_PARTY,
        module="requests",
        asname="req",
        lineno=4,
        package="requests",
        package_names=["requests"],
        import_statement="import requests as req",
    )
    # Check the class definition
    assert visitor.nodes[3] == ParsedClassDef(
        name="MyClass",
        lineno=6,
        col_offset=0,
    )
    # Check the function definition
    assert visitor.nodes[4] == ParsedFunctionDef(
        name="method",
        lineno=7,
        col_offset=4,
    )

    # Check the function definition
    assert visitor.nodes[5] == ParsedFunctionDef(
        name="my_function",
        lineno=10,
        col_offset=0,
    )


def test_empty_code(import_visitor):
    """Test that the`CustomImportRulesVisitor`correctly handles an empty source code file"""
    source = ""
    tree = ast.parse(source)
    visitor = import_visitor
    visitor.visit(tree)
    assert len(visitor.nodes) == 0


@pytest.mark.usefixtures("parsed_import")
def test_aliased_from_import(parsed_import, import_visitor):
    """
    Test that the`CustomImportRulesVisitor`correctly handles a source code
    file with an aliased `from  import` statement.
    """
    source = """from datetime import datetime as dt"""
    tree = ast.parse(source)
    visitor = import_visitor
    visitor.visit(tree)
    assert len(visitor.nodes) == 1
    assert visitor.nodes[0] == parsed_import(
        module="datetime",
        name="datetime",
        asname="dt",
        package="datetime",
        package_names=["datetime"],
        alias_col_offset=21,
        import_statement="from datetime import datetime as dt",
    )


@pytest.mark.usefixtures("parsed_import")
def test_multiple_imports_same_line(parsed_import, import_visitor):
    """
    Test that the`CustomImportRulesVisitor`correctly handles a source code
    file with multiple import statements on the same line.
    """
    source = """import os, sys"""
    tree = ast.parse(source)
    visitor = import_visitor
    visitor.visit(tree)
    assert len(visitor.nodes) == 2
    assert visitor.nodes[0] == parsed_import(
        module="os",
        package_names=["os"],
        import_statement="import os, sys",
    )
    assert visitor.nodes[1] == parsed_import(
        module="sys",
        package="sys",
        package_names=["sys"],
        alias_col_offset=11,
        import_statement="import os, sys",
    )


def test_mixture_of_nodes(import_visitor):
    """
    Test that the `CustomImportRulesVisitor` correctly handles a source code file
    with relative imports
    """
    source = (
        "\n"
        "import os\n"
        "from sys import argv\n"
        "\n"
        "class MyClass:\n"
        "    pass\n"
        "\n"
        "def my_function():\n"
        "    pass\n"
        "\n"
        "import requests as req\n"
    )
    tree = ast.parse(source)
    visitor = import_visitor
    visitor.visit(tree)
    assert len(visitor.nodes) == 5


@pytest.mark.usefixtures("parsed_import")
def test_relative_imports(parsed_import, import_visitor):
    """
    Test that the`CustomImportRulesVisitor`correctly handles a source code
    file with relative imports.
    """
    source = "\n" "from . import foo\n" "from .. import bar\n" "from ... import baz\n" ""
    tree = ast.parse(source)
    visitor = import_visitor
    visitor.visit(tree)
    assert len(visitor.nodes) == 3
    assert visitor.nodes[0] == parsed_import(
        import_type=ImportType.RELATIVE,
        module="",
        name="foo",
        asname=None,
        lineno=2,
        col_offset=0,
        level=1,
        package=None,
        package_names=[],
        alias_col_offset=14,
        import_statement="from . import foo",
    )
    assert visitor.nodes[1] == parsed_import(
        import_type=ImportType.RELATIVE,
        module="",
        name="bar",
        lineno=3,
        level=2,
        package=None,
        package_names=[],
        alias_col_offset=15,
        import_statement="from .. import bar",
    )
    assert visitor.nodes[2] == parsed_import(
        import_type=ImportType.RELATIVE,
        module="",
        name="baz",
        level=3,
        lineno=4,
        package=None,
        package_names=[],
        alias_col_offset=16,
        import_statement="from ... import baz",
    )


@pytest.mark.usefixtures("parsed_import")
def test_multiple_from_imports_same_line(parsed_import, import_visitor):
    """
    Test that the `CustomImportRulesVisitor` correctly handles a source code
    file with multiple `from  import` statements on the same line.
    """
    source = """from sys import argv, exit"""
    tree = ast.parse(source)
    visitor = import_visitor
    visitor.visit(tree)
    assert len(visitor.nodes) == 2
    assert visitor.nodes[0] == parsed_import(
        module="sys",
        name="argv",
        package="sys",
        package_names=["sys"],
        alias_col_offset=16,
        import_statement="from sys import argv, exit",
    )
    assert visitor.nodes[1] == parsed_import(
        module="sys",
        name="exit",
        package="sys",
        package_names=["sys"],
        alias_col_offset=22,
        import_statement="from sys import argv, exit",
    )


def test_multiple_classes_and_functions(import_visitor):
    """
    Test that the`CustomImportRulesVisitor`correctly handles a source code
    file with multiple classes and functions.
    """
    source = (
        "\n"
        "class Foo:\n"
        "    pass\n"
        "\n"
        "class Bar:\n"
        "    pass\n"
        "\n"
        "def func1():\n"
        "   pass\n"
        "\n"
        "def func2():\n"
        "    pass\n"
    )
    tree = ast.parse(source)
    visitor = import_visitor
    visitor.visit(tree)
    assert len(visitor.nodes) == 4


def test_nested_classes_and_functions(import_visitor):
    """
    Test that the `CustomImportRulesVisitor` correctly handles a source code
    file with nested classes and functions
    """
    source = (
        "\n"
        "class OuterClass:\n"
        "   class InnerClass:\n"
        "       pass\n"
        "\n"
        "   def inner_func():\n"
        "       pass\n"
        "\n"
        "def outer_func():\n"
        "   def nested_func():\n"
        "       pass\n"
    )

    tree = ast.parse(source)
    visitor = import_visitor
    visitor.visit(tree)
    assert len(visitor.nodes) == 5


def test_comments(import_visitor):
    """
    Test that the `CustomImportRulesVisitor` correctly handles a source code
    file with comments.
    """
    source = """
    # This is a comment import os
    # Another comment
    """
    tree = ast.parse(source)
    visitor = import_visitor
    visitor.visit(tree)
    assert len(visitor.nodes) == 0
