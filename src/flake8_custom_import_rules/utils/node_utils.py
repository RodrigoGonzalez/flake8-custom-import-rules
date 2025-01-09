"""Functions for processing nodes."""

import ast
from collections import defaultdict
from typing import Generator

from flake8_custom_import_rules.utils.parse_utils import parse_module_string


def get_package_names(module_name: str) -> list[str] | None:
    """
    Get the package names for a given module.

    Parameters
    ----------
    module_name : str
        The name of the module.

    Returns
    -------
    list[str] | None
        A list of package names for the module. Returns None
        if no package names are found.
    """
    tree = ast.parse(module_name)

    parts = [
        node.attr if isinstance(node, ast.Attribute) else node.id
        for node in ast.walk(tree)
        if isinstance(node, (ast.Attribute, ast.Name))
    ]

    if not parts:
        return []

    package_names = [parts.pop()]
    package_names.extend(f"{package_names[-1]}.{part}" for part in reversed(parts))
    return package_names


def root_package_name(module_name: str) -> str | None:
    """
    Retrieve the root package name from a given module name.

    This function parses the module name using the `ast` module and searches
    for the first occurrence of a `Name` node in the parsed AST. The `Name`
    node represents a possible root package name.

    Parameters
    ----------
    module_name : str
        The name of the module.

    Returns
    -------
    str | None
        The root package name if found, or `None` if no root package name is
        found.
    """

    tree = ast.parse(module_name)
    return next(
        (node.id for node in ast.walk(tree) if isinstance(node, ast.Name)),
        None,
    )


def generate_identifier_path(node: ast.AST | ast.expr) -> Generator[str, None, None]:
    """
    Generates a path for a given node in the Abstract Syntax Tree (AST).

    This function recursively traverses the AST to generate a path representing
    the location of the given node. The path consists of the attribute names,
    function names, variable names, and constant values encountered while
    traversing the AST.

    Parameters
    ----------
    node : ast.AST
        The node in the AST for which the path needs to be generated.

    Yields
    ------
    str
        The components of the path as strings.
    """
    if isinstance(node, ast.Attribute):
        yield from generate_identifier_path(node.value)
        yield node.attr
    elif isinstance(node, ast.Call):
        yield from generate_identifier_path(node.func)
    elif isinstance(node, ast.Name):
        yield node.id
    elif isinstance(node, ast.Subscript):
        yield from generate_identifier_path(node.value)
        yield from generate_identifier_path(node.slice)
    elif isinstance(node, ast.Constant):
        yield str(node.value)


def check_private_module_import(module: str) -> bool:
    """Check if an Import node is a private module import."""
    return bool(_ := parse_module_string(module, prefix="_"))


def get_module_info_from_import_node(node: ast.Import) -> dict:
    """
    Get import node information.

    Parameters
    ----------
    node : ast.Import
        The node to get the names from.

    Returns
    -------
    dict
        The names of the import.
    """
    module_info: defaultdict[str, dict] = defaultdict(lambda: defaultdict(str))

    for alias in node.names:
        module = alias.name
        package = root_package_name(module)
        package_names = get_package_names(module)

        module_info[module].update(
            {
                "module": module,
                "asname": alias.asname,
                "lineno": node.lineno,
                "col_offset": node.col_offset,
                "node_col_offset": node.col_offset,
                "alias_col_offset": alias.col_offset,
                "package": package,
                "package_names": package_names,
                "private_identifier_import": False,
                "private_module_import": check_private_module_import(module),
                "import_statement": ast.unparse(node),
            }
        )

    return module_info


def get_name_info_from_import_node(node: ast.ImportFrom) -> dict:
    """
    Get from import node information.

    Parameters
    ----------
    node : ast.ImportFrom
        The node to get the names from.

    Returns
    -------
    dict
        The names of the import.
    """
    name_info: defaultdict[str, dict] = defaultdict(lambda: defaultdict(str))

    module = node.module or ""
    package = root_package_name(module)
    package_names = get_package_names(module)

    for alias in node.names:
        name = alias.name
        name_info[name].update(
            {
                "name": name,
                "module": module,
                "asname": alias.asname,
                "lineno": node.lineno,
                "col_offset": node.col_offset,
                "node_col_offset": node.col_offset,
                "alias_col_offset": alias.col_offset,
                "package": package,
                "package_names": package_names,
                "level": node.level,
                "private_identifier_import": check_private_module_import(alias.name),
                "private_module_import": check_private_module_import(module),
                "import_statement": ast.unparse(node),
            }
        )

    return name_info
