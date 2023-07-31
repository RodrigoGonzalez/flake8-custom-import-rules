""" Visitor for parsing restricted imports. """
import ast
import logging
import os
from collections import defaultdict

from attrs import define
from attrs import field

from flake8_custom_import_rules.utils.file_utils import get_file_path_from_module_name
from flake8_custom_import_rules.utils.file_utils import get_relative_path_from_absolute_path
from flake8_custom_import_rules.utils.node_utils import get_package_names
from flake8_custom_import_rules.utils.node_utils import root_package_name

logger = logging.getLogger(__name__)


def get_restricted_package_strings(
    restricted_packages: list[str],
    file_packages: list[str],
) -> list[str]:
    """
    Get restricted package strings.

    Parameters
    ----------
    restricted_packages: list[str]
        The restricted packages.
    file_packages: list[str]
        The file packages to check. (The module and parent packages.)

    Returns
    -------
    list[str]
        The restricted package strings.
    """
    return [
        restricted_import
        for restricted_import in restricted_packages
        if restricted_import not in file_packages
    ]


def get_import_restriction_strings(
    import_restrictions: defaultdict[str, list[str]],
    file_packages: list[str],
) -> list[str]:
    """
    Get import restriction strings.

    Parameters
    ----------
    import_restrictions: defaultdict[str, list[str]]
        The import restrictions.
    file_packages: list[str]
        The file packages to check. (The module and parent packages.)

    Returns
    -------
    list[str]
        The import restriction strings.
    """
    import_restriction_keys = list(import_restrictions.keys())
    parsed_import_restriction_keys: list = [
        import_restriction_key
        for import_restriction_key in import_restriction_keys
        if import_restriction_key in file_packages
    ]
    import_restrictions_from_keys = {
        restrictions
        for key in parsed_import_restriction_keys
        for restrictions in import_restrictions[key]
    }
    parsed_import_restrictions = list(import_restrictions_from_keys)

    return get_restricted_package_strings(parsed_import_restrictions, file_packages)


def get_import_strings(
    restrictions: list[str],
) -> list[str]:
    """
    Get import strings.

    Parameters
    ----------
    restrictions: list[str]
        The restrictions to get the import strings for.

    Returns
    -------
    list[str]
        The import strings.
    """
    return [f"import {restriction}\n" for restriction in sorted(restrictions)]


def subdict_from_keys(
    import_restrictions: defaultdict[str, list[str]],
    keys: list[str],
) -> dict[str, list[str]]:
    """
    Function to create a subset of a dictionary given a list of keys.

    Parameters
    ----------
    import_restrictions: defaultdict[str, list[str]]
        The original dictionary.
    keys: list[str]
        The keys for the sub-dictionary.

    Returns
    -------
    dict
        A sub-dictionary with the given keys.
    """
    return {k: import_restrictions[k] for k in keys if k in import_restrictions}


def find_keys_with_string(
    import_restrictions: defaultdict[str, list[str]], target_string: str
) -> list[str]:
    """
    Function to find keys with the target string in their lists.

    Parameters
    ----------
    import_restrictions : defaultdict
        The defaultdict(list) to search.
    target_string : str
        The string to search for.

    Returns
    -------
    list
        A list of keys where the string is found in their lists.
    """
    return [k for k, v in import_restrictions.items() if target_string in v]


@define(slots=True, kw_only=True, hash=False)
class RestrictedImportVisitor(ast.NodeVisitor):
    """Visitor for dynamic strings."""

    _restricted_packages: list[str]
    _import_restrictions: defaultdict[str, list[str]]
    _check_module_exists: bool = field(default=True)  # Not Implemented
    _file_packages: list[str] = field(default=list)
    _restrictions: list[str] = field(init=False)
    _lines: list[str] = field(init=False)
    _tree: ast.AST = field(init=False)
    _package_names: list = field(factory=list)

    restricted_identifiers: defaultdict[str, dict] = field(init=False)

    def __attrs_post_init__(self) -> None:
        """Initialize RestrictedImportVisitor."""
        self._restrictions = self._get_restricted_package_strings()
        self._restrictions.extend(self._get_import_restriction_strings())
        self._restrictions = sorted(list(set(self._restrictions)))

        self._lines = get_import_strings(self._restrictions)
        self._tree = ast.parse("".join(self._lines))
        self.restricted_identifiers = defaultdict(lambda: defaultdict(str))

        # Not Implemented
        # TODO: Implement checking if modules exist
        self._check_module_exists = False

    def _get_restricted_package_strings(self) -> list[str]:
        """Get restricted package strings."""
        return get_restricted_package_strings(self._restricted_packages, self._file_packages)

    def _get_import_restriction_strings(self) -> list[str]:
        """Get restricted package strings."""
        return get_import_restriction_strings(self._import_restrictions, self._file_packages)

    def visit_Import(self, node: ast.Import) -> None:
        """Visit a String Import node."""

        for alias in node.names:
            module = alias.name
            package = root_package_name(module)
            package_names = get_package_names(module)

            if self._check_module_exists:
                absolute_path = get_file_path_from_module_name(module)
                relative_path = (
                    get_relative_path_from_absolute_path(absolute_path, os.getcwd())
                    if absolute_path
                    else None
                )

                logging.debug(f"Module: {module}")
                logging.debug(f"Absolute path: {absolute_path}")
                logging.debug(f"Current working directory: {os.getcwd()}")

                identifier_dict = {
                    "module": module,
                    "package": package,
                    "package_names": package_names,
                    "import_statement": ast.unparse(node),
                    "absolute_path": absolute_path,
                    "relative_path": relative_path,
                }

            else:
                identifier_dict = {
                    "module": module,
                    "package": package,
                    "package_names": package_names,
                    "import_statement": ast.unparse(node),
                }

            self.restricted_identifiers[module].update(identifier_dict)
            self._package_names.extend(package_names[:-1])

    # def _process_package_names(self) -> None:
    #     """Process package names."""
    #     for package_name in set(self._package_names):
    #         self._package_names.append(package_name)

    def get_restricted_identifiers(self) -> defaultdict[str, dict]:
        """Get the list of restricted imports."""
        self.visit(self._tree)
        return self.restricted_identifiers


def get_restricted_identifiers(
    restricted_packages: list[str] | str,
    import_restrictions: defaultdict[str, list[str]] | None = None,
    check_module_exists: bool = True,  # Not Implemented
    file_packages: list | None = None,
) -> defaultdict[str, dict]:
    """
    Get restricted identifiers.

    Parameters
    ----------
    restricted_packages : list[str]
        The list of restricted imports.
    import_restrictions : defaultdict[str, list[str]], optional
        The list of restricted imports, by default None
    check_module_exists : bool, optional
        Whether to check if the module exists, by default True
    file_packages : list[str], optional
        The list of parent packages of the file, by default None

    Returns
    -------
    defaultdict[str, dict]
        The restricted import node.
    """
    if not file_packages:
        file_packages = []
    if isinstance(restricted_packages, str):
        restricted_packages = [restricted_packages]
    if import_restrictions is None:
        import_restrictions = defaultdict(list)

    visitor = RestrictedImportVisitor(
        restricted_packages=restricted_packages,
        import_restrictions=import_restrictions,
        check_module_exists=check_module_exists,  # Not Implemented
        file_packages=file_packages,
    )
    return visitor.get_restricted_identifiers()
