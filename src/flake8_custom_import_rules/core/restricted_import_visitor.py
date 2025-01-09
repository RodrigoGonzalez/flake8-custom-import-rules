""" Visitor for parsing restricted imports. """

import ast
import logging
from collections import defaultdict

from attrs import define
from attrs import field

from flake8_custom_import_rules.utils.node_utils import get_package_names
from flake8_custom_import_rules.utils.node_utils import root_package_name
from flake8_custom_import_rules.utils.restricted_import_utils import get_import_restriction_strings
from flake8_custom_import_rules.utils.restricted_import_utils import get_import_strings
from flake8_custom_import_rules.utils.restricted_import_utils import get_restricted_package_strings

logger = logging.getLogger(__name__)


@define(slots=True, kw_only=True, hash=False)
class RestrictedImportVisitor(ast.NodeVisitor):
    """
    A visitor class that inspects the Abstract Syntax Tree (AST) of Python
    code to identify restricted imports within the code.

    Attributes
    ----------
    _base_packages : list[str]
        The project base packages.
    _restricted_packages: list[str]
        List of restricted packages that are not allowed to be imported.
    _custom_restrictions: defaultdict[str, list[str]]
        Default dictionary containing import restrictions for specific packages.
    _file_packages: list[str]
        List of file packages to check. Default is an empty list.
    _restrictions: list[str]
        List of restrictions for the imports. Computed at initialization.
    _lines: list[str]
        List of lines containing the import statements.
    _tree: ast.AST
        An AST representation of the import lines.
    _package_names: list
        A list of package names extracted from the modules.
    restricted_identifiers: defaultdict[str, dict]
        Default dictionary containing restricted identifiers and related
        package information.
    """

    _base_packages: list[str] = field(factory=list)
    _restricted_packages: list[str]
    _restricted_package_list: list[str] = field(init=False)
    _custom_restrictions: defaultdict[str, list[str]]
    _import_restriction_list: list[str] = field(init=False)
    _file_packages: list[str] = field(default=list)
    _restrictions: list[str] = field(init=False)
    _lines: list[str] = field(init=False)
    _tree: ast.AST = field(init=False)
    _package_names: list = field(factory=list)

    restricted_identifiers: defaultdict[str, dict] = field(init=False)

    def __attrs_post_init__(self) -> None:
        """
        Initialize the RestrictedImportVisitor by preparing the restrictions,
        lines, AST tree, and restricted identifiers.
        """

        self._restricted_package_list = self._get_restricted_package_strings()
        self._import_restriction_list = self._get_import_restriction_strings()
        self._restrictions = sorted(
            list(set(self._restricted_package_list + self._import_restriction_list))
        )

        self._lines = get_import_strings(self._restrictions)
        self._tree = ast.parse("".join(self._lines))
        self.restricted_identifiers = defaultdict(lambda: defaultdict(str))

    def _get_restricted_package_strings(self) -> list[str]:
        """
        Retrieve the strings representing restricted packages based on
        the restricted packages and file packages.

        Returns
        -------
        list[str]
            List of restricted package strings.
        """
        return get_restricted_package_strings(self._restricted_packages, self._file_packages)

    def _get_import_restriction_strings(self) -> list[str]:
        """
        Retrieve the strings representing import restrictions based on the
        import restrictions and file packages.

        Returns
        -------
        list[str]
            List of import restriction strings.
        """

        return get_import_restriction_strings(self._custom_restrictions, self._file_packages)

    def visit_Import(self, node: ast.Import) -> None:
        """
        Visit an AST Import node to check for restricted imports and
        gather relevant information such as the module, package,
        package names, import statement, absolute path, and relative path.

        Parameters
        ----------
        node: ast.Import
            The AST Import node being visited.
        """

        for alias in node.names:
            module = alias.name
            package = root_package_name(module)
            package_names = get_package_names(module)
            restricted_package = module in self._restricted_package_list
            import_restriction = module in self._import_restriction_list

            identifier_dict = {
                "module": module,
                "package": package,
                "package_names": package_names,
                "import_statement": ast.unparse(node),
                "restricted_package": restricted_package,
                "import_restriction": import_restriction,
            }

            self.restricted_identifiers[module].update(identifier_dict)
            self._package_names.extend(package_names[:-1])

    def get_restricted_identifiers(self) -> defaultdict[str, dict]:
        """
        Get the dictionary containing information about restricted imports
        identified by visiting the AST tree.

        Returns
        -------
        defaultdict[str, dict]
            Default dictionary containing restricted identifiers and
            related information.
        """

        self.visit(self._tree)
        return self.restricted_identifiers


def get_restricted_identifiers(
    base_packages: list[str],
    restricted_packages: list[str] | str,
    custom_restrictions: defaultdict[str, list[str]] | None = None,
    file_packages: list | None = None,
) -> defaultdict[str, dict]:
    """
    Get restricted identifiers.

    Parameters
    ----------
    base_packages : list[str]
        The project base packages.
    restricted_packages : list[str]
        The list of restricted imports.
    custom_restrictions : defaultdict[str, list[str]], optional
        The list of restricted imports, by default None
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
    if custom_restrictions is None:
        custom_restrictions = defaultdict(list)

    visitor = RestrictedImportVisitor(
        base_packages=base_packages,
        restricted_packages=restricted_packages,
        custom_restrictions=custom_restrictions,
        file_packages=file_packages,
    )
    return visitor.get_restricted_identifiers()
