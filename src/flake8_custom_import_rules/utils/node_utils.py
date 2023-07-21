"""Functions for processing nodes."""
import ast
from collections import defaultdict

from flake8_custom_import_rules.utils.parse_utils import parse_module_string


def get_package_names(module_name: str) -> list[str] | None:
    """
    Return a list of package names for a module name.

    Parameters
    ----------
    module_name : str

    Returns
    -------
    list[str] | None
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

    for part in reversed(parts):
        last_package_name = f"{package_names[-1]}.{part}"
        package_names.append(last_package_name)

    return package_names


def root_package_name(module_name: str) -> str | None:
    """
    Return the root package name of a module name.

    Parameters
    ----------
    module_name : str
        The module name.

    Returns
    -------
    str | None
        The root package name.
    """
    tree = ast.parse(module_name)
    return next(
        (node.id for node in ast.walk(tree) if isinstance(node, ast.Name)),
        None,
    )


def check_private_module_import(module: str) -> bool:
    """Check if an Import node is a private module import."""
    return bool(_ := parse_module_string(module, prefix="_"))


def get_module_info_from_import_node(node: ast.Import) -> dict:
    """
    Get the names of the import from the node.

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
                "alias_col_offset": alias.col_offset,
                "package": package,
                "package_names": package_names,
                "private_identifier_import": False,
                "private_module_import": check_private_module_import(module),
            }
        )

    return module_info


def get_name_info_from_import_node(node: ast.ImportFrom) -> dict:
    """Get the names of the import."""
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
                "alias_col_offset": alias.col_offset,
                "package": package,
                "package_names": package_names,
                "level": node.level,
                "private_identifier_import": alias.name.startswith("_"),
                "private_module_import": check_private_module_import(module),
            }
        )

    return name_info
