"""Functions for processing nodes."""
import ast
from collections import defaultdict


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
    package_dict: defaultdict[str, list] = defaultdict(list)
    node_modules_lineno: defaultdict[str, list] = defaultdict(list)

    for alias in node.names:
        module = alias.name

        package = root_package_name(module)
        if package:
            package_dict[package].append(module)
        package_names = get_package_names(module)
        node_modules_lineno[str(node.lineno)].append(module)

        module_info[module].update(
            {
                "module": module,
                "asname": alias.asname,
                "lineno": node.lineno,
                "col_offset": node.col_offset,
                "package": package,
                "package_names": package_names,
            }
        )

    module_info["node_modules_lineno"] = node_modules_lineno
    module_info["package_dict"] = package_dict
    return module_info


def get_name_info_from_import_node(node: ast.ImportFrom) -> dict:
    """Get the names of the import."""
    name_info: defaultdict[str, dict] = defaultdict(lambda: defaultdict(str))
    node_names_lineno: defaultdict[str, list] = defaultdict(list)

    module = node.module or ""
    package = root_package_name(module)
    package_names = get_package_names(module)

    for alias in node.names:
        name = alias.name
        node_names_lineno[str(node.lineno)].append(name)

        name_info[name].update(
            {
                "name": name,
                "module": module,
                "asname": alias.asname,
                "lineno": node.lineno,
                "col_offset": node.col_offset,
                "package": package,
                "package_names": package_names,
                "level": node.level,
            }
        )

    name_info["node_names_lineno"] = node_names_lineno

    return name_info
