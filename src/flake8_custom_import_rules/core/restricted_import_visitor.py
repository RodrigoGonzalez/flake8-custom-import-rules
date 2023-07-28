""" Visitor for parsing restricted imports. """
import ast
import logging
import os
from collections import defaultdict

from attr import define
from attr import field

from flake8_custom_import_rules.utils.file_utils import get_file_path_from_module_name
from flake8_custom_import_rules.utils.file_utils import get_relative_path_from_absolute_path
from flake8_custom_import_rules.utils.node_utils import get_package_names
from flake8_custom_import_rules.utils.node_utils import root_package_name

logger = logging.getLogger(__name__)


@define(slots=True, kw_only=True, hash=False)
class RestrictedImportVisitor(ast.NodeVisitor):
    """Visitor for dynamic strings."""

    _restricted_packages: list[str]
    _check_module_exists: bool = field(default=True)
    _file_packages: list[str] = field(default=list)
    _lines: list[str] = field(init=False)
    _tree: ast.AST = field(init=False)
    _package_names: list = field(factory=list)

    restricted_identifiers: defaultdict[str, dict] = field(init=False)

    def __attrs_post_init__(self) -> None:
        """Initialize."""
        self._lines = [
            f"import {restricted_import}\n"
            for restricted_import in self._restricted_packages
            if restricted_import not in self._file_packages
        ]
        self._tree = ast.parse("".join(self._lines))
        self.restricted_identifiers = defaultdict(lambda: defaultdict(str))

    def visit_Import(self, node: ast.Import) -> None:
        """Visit an Dynamic String Import node."""

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

                logging.info(f"Module: {module}")
                logging.info(f"Absolute path: {absolute_path}")
                logging.info(f"Current working directory: {os.getcwd()}")

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
    check_module_exists: bool = True,
    file_packages: list | None = None,
) -> defaultdict[str, dict]:
    """
    Get restricted identifiers.

    Parameters
    ----------
    restricted_packages : list[str]
        The list of restricted imports.
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

    visitor = RestrictedImportVisitor(
        restricted_packages=restricted_packages,
        check_module_exists=check_module_exists,
        file_packages=file_packages,
    )
    return visitor.get_restricted_identifiers()
