""" Functions for working with files and paths. """
import logging
import os
import sys

from flake8.utils import normalize_path

logger = logging.getLogger(__name__)


def check_module_in_package(base_module: str, filename: str) -> str | None:
    """
    Get the module name for a given file path based on a base module.

    Parameters
    ----------
    base_module : str
        The base module to use as a reference.
    filename : str
        The file path to get the module name for.

    Returns
    -------
    str | None
    """

    # Check if the base module is in the file path
    if base_module not in filename:
        raise ValueError(f"The base module {base_module} is not in the file path {filename}")

    # Get the part of the file path that is relative to the base module
    relative_path = filename.partition(base_module)[2].strip("/")

    # Remove the .py extension and replace / with . to get the module name
    return os.path.splitext(relative_path)[0].replace("/", ".")


def get_module_name_from_filename(filename: str, parent: str = os.curdir) -> str | None:
    """
    Get the module name for a given file path based on a base module.

    Parameters
    ----------
    filename : str
        The file path to get the module name for.
    parent : str, optional
        The parent path, by default os.curdir

    Returns
    -------
    str | None
    """

    # Normalize the file path
    filename = normalize_path(filename, parent=parent)

    # Check if the file exists
    if not os.path.isfile(filename):
        raise FileNotFoundError(filename)

    module_prefix = find_prefix(filename)

    return convert_name(filename, prefix=module_prefix)


def find_prefix(filename: str) -> str:
    """
    Find the appropriate module prefix string for the filename.

    Parameters
    ----------
    filename : str
        The filename to find the prefix for.

    Returns
    -------
    str
    """
    filename = os.path.abspath(filename)

    # Find the deepest path
    matches = (path for path in sys.path if filename.startswith(path))

    return max(matches, key=len)


def convert_name(filename: str, prefix: str | None = None) -> str:
    """
    Convert filename to a module name by removing prefix and .py extension,
    and replacing / with .

    Parameters
    ----------
    filename : str
        The filename to convert.
    prefix : str | None
        The prefix to remove from the filename.

    Returns
    -------
    str
    """
    filename = os.path.abspath(filename)

    if prefix and filename.startswith(prefix):
        filename = filename[len(prefix) :]

    if filename.endswith(".py"):
        filename = filename[:-3]

    return filename.lstrip("/").replace("/", ".")


def convert_module_to_file_paths(module_name: str) -> list[str]:
    """
    Convert module name to a relative file path by replacing . with /
    and adding .py and /__init__.py extensions.

    Parameters
    ----------
    module_name : str
        The module name to convert.

    Returns
    -------
    str
    """
    return [module_name.replace(".", "/") + ext for ext in [".py", "/__init__.py"]]


def get_file_path_from_module_name(module_name: str) -> str | None:
    """
    Get the file path for a given module name. If the module is a package,
    return the path to its __init__.py file.

    Parameters
    ----------
    module_name : str
        The module name to get the file path for.

    Returns
    -------
    str | None
    """
    # Construct possible full file paths
    possible_paths = [
        os.path.join(path, file_path)
        for path in sys.path
        for file_path in convert_module_to_file_paths(module_name)
    ]

    if not (existing_paths := list(filter(os.path.isfile, possible_paths))):
        # raise FileNotFoundError(module_name)
        return None
    logger.debug(f"existing_paths: {existing_paths}")
    assert isinstance(existing_paths, list)
    # return max(existing_paths, key=len) if existing_paths else None
    return existing_paths[0]


def get_relative_path_from_absolute_path(
    absolute_path: list | str, cwd: str | None = os.getcwd()
) -> str | None:
    """
    Get the relative path for a given absolute path.

    Parameters
    ----------
    absolute_path : str
        The absolute path to get the relative path for.
    cwd : str, optional
        The current working directory, by default os.getcwd()

    Returns
    -------
    str
    """
    logger.debug(f"absolute_path type: {type(absolute_path)}")
    if not absolute_path:
        return None
    if isinstance(absolute_path, list):
        return absolute_path[0]
    if not isinstance(absolute_path, str):
        raise TypeError(f"Absolute path expected, got {type(absolute_path)}: {absolute_path}")
    return os.path.relpath(absolute_path, start=cwd)
