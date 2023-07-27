"""Custom import rules node visitor."""
import ast
import logging
import sys
from collections import defaultdict
from pathlib import Path

from attrs import define
from attrs import field
from stdlib_list import stdlib_list

from flake8_custom_import_rules.core.nodes import DynamicStringFromImport
from flake8_custom_import_rules.core.nodes import DynamicStringParseSyntaxFailure
from flake8_custom_import_rules.core.nodes import DynamicStringStraightImport
from flake8_custom_import_rules.core.nodes import ImportType
from flake8_custom_import_rules.core.nodes import ParsedClassDef
from flake8_custom_import_rules.core.nodes import ParsedDynamicImport
from flake8_custom_import_rules.core.nodes import ParsedFromImport
from flake8_custom_import_rules.core.nodes import ParsedFunctionDef
from flake8_custom_import_rules.core.nodes import ParsedIfImport
from flake8_custom_import_rules.core.nodes import ParsedLocalImport
from flake8_custom_import_rules.core.nodes import ParsedNode
from flake8_custom_import_rules.core.nodes import ParsedStraightImport
from flake8_custom_import_rules.defaults import POTENTIAL_DYNAMIC_IMPORTS
from flake8_custom_import_rules.defaults import STDIN_IDENTIFIERS
from flake8_custom_import_rules.utils.file_utils import get_module_name_from_filename
from flake8_custom_import_rules.utils.node_utils import generate_identifier_path
from flake8_custom_import_rules.utils.node_utils import get_module_info_from_import_node
from flake8_custom_import_rules.utils.node_utils import get_name_info_from_import_node
from flake8_custom_import_rules.utils.node_utils import root_package_name
from flake8_custom_import_rules.utils.parse_utils import check_string

logger = logging.getLogger(f"flake8_custom_import_rules.{__name__}")


@define(slots=True)
class CustomImportRulesVisitor(ast.NodeVisitor):
    """Custom import rules node visitor.

    Attributes
    ----------
    base_packages : list[str]
        Base packages
    filename : str | None
        The current file name
    nodes : list
        The resulting nodes from the visitor
    dynamic_nodes : defaultdict[str, list]
        The resulting nodes from the visitor that parses dynamic strings
    file_path : Path | None
        File path equal to Path(filename) if filename is not empty or None,
        otherwise None
    resolve_local_imports : bool | None
        Resolve local imports
    identifiers : defaultdict[str, dict]
        An identifier is the name of a variable, function, class, module, or
        other object. When you import something, you're essentially creating a
        new identifier in your current namespace that refers to the object
        you're importing.
    identifiers_by_lineno : defaultdict[str, list]
        Identifiers by line number
    stdlib_names : set | frozenset
        Standard library names for the current Python version
    file_identifier : str | None
        The file identifier (i.e., the module name)
    file_root_package_name : str | None
        The file root package name
    """

    base_packages: list[str] = field(factory=list)
    filename: str | None = None
    nodes: list = field(factory=list)
    dynamic_nodes: defaultdict[str, list] = defaultdict(list)
    file_path: Path | None = None
    resolve_local_imports: bool | None = field(default=False)
    identifiers: defaultdict[str, dict] = defaultdict(lambda: defaultdict(str))
    identifiers_by_lineno: defaultdict[str, list] = defaultdict(list)
    stdlib_names: set | frozenset = field(init=False)
    file_identifier: str | None = field(init=False)
    file_root_package_name: str | None = field(init=False)

    def __attrs_post_init__(self) -> None:
        """Initialize the attributes after object creation.

        If the current Python version is less than (3, 10), it assigns the set
        of standard library names for the current Python version to
        self.stdlib_names using stdlib_list. Otherwise, it assigns
        sys.stdlib_module_names to self.stdlib_names.
        """
        self.resolve_local_imports = self.filename not in STDIN_IDENTIFIERS
        logger.debug(f"Resolve local imports: {self.resolve_local_imports}")
        self.file_path = (
            Path(self.filename) if (self.resolve_local_imports and self.filename) else None
        )
        logger.info(f"Visitor filename: {self.filename}")
        self.file_identifier = (
            get_module_name_from_filename(self.filename) if self.resolve_local_imports else None
        )
        self.file_root_package_name = (
            root_package_name(self.file_identifier) if self.resolve_local_imports else None
        )

        if sys.version_info < (3, 10):
            # stdlib_list only supports up to Python 3.9
            self.stdlib_names = set(
                stdlib_list(f"{sys.version_info.major}.{sys.version_info.minor}")
            )
        else:
            self.stdlib_names = sys.stdlib_module_names

    def get_all_nodes(self) -> list[ParsedNode]:
        """Get all nodes."""
        return self.nodes + list(self.dynamic_nodes.values())

    def _resolve_local_import(self, module: str, node_level: int) -> Path | None:
        """Resolve a local import."""
        # parent = self.file_path.parents[node_level - 1] if self.file_path else None
        # return parent / f"{module}.py" if parent else None
        raise NotImplementedError("This method is not implemented yet.")

    def resolve_relative_import(self, relative_import: str) -> str:
        """Resolve a relative import to its absolute form."""
        # Remove leading dots from the relative import

        # relative_import = relative_import.lstrip('.')
        # return f"{self}.{relative_import}"
        raise NotImplementedError("This method is not implemented yet.")

    @staticmethod
    def _get_straight_import_node(module_info: dict) -> ParsedStraightImport:
        """
        Get a parsed import node.

        Parameters
        ----------
        module_info : dict
            A dictionary containing information about the module.

        Returns
        -------
        ParsedStraightImport
        """
        return ParsedStraightImport(
            import_type=module_info["import_type"],
            module=module_info["module"],
            asname=module_info["asname"],
            lineno=module_info["lineno"],
            col_offset=module_info["col_offset"],
            node_col_offset=module_info["node_col_offset"],
            alias_col_offset=module_info["alias_col_offset"],
            package=module_info["package"],
            package_names=module_info["package_names"],
            private_identifier_import=module_info["private_identifier_import"],
            private_module_import=module_info["private_module_import"],
            import_statement=module_info["import_statement"],
        )

    def visit_Import(self, node: ast.Import) -> None:
        """Visit an Import node."""
        parsed_imports_dict = get_module_info_from_import_node(node)

        # pprint.pprint("\nParsed import dict:")
        # pprint.pprint(parsed_imports_dict)

        for alias in node.names:
            module_info = parsed_imports_dict[alias.name]
            module_info["import_type"] = self._classify_type(module_info["package_names"])
            parsed_import = self._get_straight_import_node(module_info)

            self.nodes.append(parsed_import)
            self.identifiers_by_lineno[str(node.lineno)].append(module_info)
            self.identifiers[parsed_import.identifier].update(module_info)
            self.identifiers[alias.name].update(module_info)

        # Ensures a complete traversal of the AST
        self.generic_visit(node)

    def _get_from_import_type(self, node_level: int, package_names: list[str]) -> ImportType:
        """Get the import type for a module. This will be used to determine
        whether the custom import rules is violated.

        Parameters
        ----------
        node_level : int
            The level of the node.
        package_names : list[str]
            The package names.

        Returns
        -------
        ImportType
        """
        return ImportType.RELATIVE if node_level > 0 else self._classify_type(package_names)

    @staticmethod
    def _get_from_import_node(name_info: dict) -> ParsedFromImport:
        """
        Get a parsed from import node.

        Parameters
        ----------
        name_info : dict
            A dictionary containing information about the from input.

        Returns
        -------
        ParsedFromImport
        """
        return ParsedFromImport(
            import_type=name_info["import_type"],
            module=name_info["module"],
            name=name_info["name"],
            asname=name_info["asname"],
            lineno=name_info["lineno"],
            col_offset=name_info["col_offset"],
            node_col_offset=name_info["node_col_offset"],
            alias_col_offset=name_info["alias_col_offset"],
            level=name_info["level"],
            package=name_info["package"],
            package_names=name_info["package_names"],
            private_identifier_import=name_info["private_identifier_import"],
            private_module_import=name_info["private_module_import"],
            import_statement=name_info["import_statement"],
        )

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Visit an Import From node."""
        parsed_from_imports_dict = get_name_info_from_import_node(node)

        # pprint.pprint("\nParsed from import dict:")
        # pprint.pprint(parsed_from_imports_dict)

        for alias in node.names:
            name_info = parsed_from_imports_dict[alias.name]
            name_info["import_type"] = self._get_from_import_type(
                name_info["level"], name_info["package_names"]
            )
            parsed_from_import = self._get_from_import_node(name_info)

            self.nodes.append(parsed_from_import)
            self.identifiers_by_lineno[str(node.lineno)].append(name_info)
            self.identifiers[parsed_from_import.identifier].update(name_info)
            self.identifiers[alias.name].update(name_info)

        # Ensures a complete traversal of the AST
        self.generic_visit(node)

    def _check_local_import(
        self, node: ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef
    ) -> None:
        """Check if a local import is resolved."""
        for stmt in node.body:
            if isinstance(stmt, (ast.Import, ast.ImportFrom)):
                assert isinstance(stmt, ast.AST)  # for linters
                self.nodes.append(
                    ParsedLocalImport(
                        lineno=stmt.lineno,
                        col_offset=stmt.col_offset,
                        local_node_type=str(type(node)),
                        import_statement=ast.unparse(stmt),
                    )
                )

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Visit a ClassDef node."""
        self.nodes.append(
            ParsedClassDef(
                name=node.name,
                lineno=node.lineno,
                col_offset=node.col_offset,
            )
        )
        self._check_local_import(node)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visit a FunctionDef node."""
        self.nodes.append(
            ParsedFunctionDef(
                name=node.name,
                lineno=node.lineno,
                col_offset=node.col_offset,
            )
        )
        self._check_local_import(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """Visit a AsyncFunctionDef node."""
        self.nodes.append(
            ParsedFunctionDef(
                name=node.name,
                lineno=node.lineno,
                col_offset=node.col_offset,
            )
        )
        self._check_local_import(node)
        self.generic_visit(node)

    def _get_dynamic_string_visitor(self, lineno: int, col_offset: int) -> "DynamicStringVisitor":
        """Get the dynamic string visitor."""
        return DynamicStringVisitor(
            base_packages=self.base_packages,
            filename=self.filename,
            lineno=lineno,
            col_offset=col_offset,
        )

    def _try_parse_value_string(self, value: str, lineno: int, col_offset: int) -> str:
        """Attempt to parse the value strings and handle exceptions."""
        try:
            node = ast.parse(value)

        except (SyntaxError, TypeError, ValueError):
            logger.warning(f"Parsing error in string {value} at line {lineno}, column {col_offset}")
            dynamic_node_failure = DynamicStringParseSyntaxFailure(
                lineno=lineno, col_offset=col_offset, value=value
            )
            self.dynamic_nodes[str(lineno)].append(dynamic_node_failure)
            return value

        dynamic_string_visitor = self._get_dynamic_string_visitor(lineno, col_offset)
        dynamic_string_visitor.visit(node)

        for dynamic_node in dynamic_string_visitor.nodes:
            self.dynamic_nodes[str(lineno)].append(dynamic_node)

        return value

    @staticmethod
    def _has_value(arg: ast.Constant) -> bool:
        """Check if the argument has a value attribute."""
        return hasattr(arg, "value")

    def _get_args_for_calls(self, args: list, lineno: int, col_offset: int) -> list[str]:
        """Get the function args."""
        return [
            self._try_parse_value_string(arg.value, lineno, col_offset)
            for arg in args
            if self._has_value(arg)
        ]

    @staticmethod
    def _check_for_dynamic_imports(strings_to_check: list[str]) -> bool:
        """Check for dynamic imports."""
        return check_string(
            strings_to_check=strings_to_check,
            substring_match=list(POTENTIAL_DYNAMIC_IMPORTS),
        )

    @staticmethod
    def _check_dynamic_code_execution_functions(strings_to_check: list[str]) -> bool:
        """Check for dynamic code execution functions.

        Dynamic Code Execution Functions: These functions can execute Python
        code dynamically, which means the code they execute is not known until
        runtime. This can be useful for running code that is generated or
        modified on the fly, but it also presents potential security risks if
        the executed code comes from an untrusted source.

        "eval" and "exec" are not confirmed to contain dynamic imports, but we
        will parse their arguments to see if they do.

        Please note that using eval and exec should generally be avoided when
        possible, due to the security risks involved and the potential for
        introducing bugs. Python's rich language features and libraries
        usually provide safer and more efficient ways to accomplish what you
        might otherwise use eval or exec for. For example, to dynamically
        access object attributes or call functions by name, you can use getattr
        and callable instead.
        """
        return check_string(
            strings_to_check=strings_to_check,
            substring_match=["eval", "exec"],
        )

    @staticmethod
    def _check_if_contains_package(strings_to_check: list[str]) -> bool:
        """Check if the string does not contain package information.

        "modules" is a common object name, so we need to check
        that it was imported from the "sys" package.
        However, this should be done after running the node visitor.
        """
        if check_string(strings_to_check, substring_match="modules"):
            # if "modules" is in the string, check if it was imported from "sys"
            # if "sys" is not in the string, the following will return True
            return not check_string(strings_to_check, substring_match="sys")

        if check_string(strings_to_check, substring_match=["get_loader", "iter_modules"]):
            return not check_string(strings_to_check, substring_match="pkgutil")

        return False

    def _check_if_confirmed_dynamic_import(self, strings_to_check: list[str]) -> bool:
        """Check if the dynamic import is confirmed.
        # a bare "modules" is not a confirmed dynamic import
        """
        if self._check_if_contains_package(strings_to_check):
            return False
        return not self._check_dynamic_code_execution_functions(strings_to_check)

    def _get_parsed_dynamic_import(
        self, strings_to_check: list[str], node: ast.Call | ast.Assign
    ) -> ParsedDynamicImport:
        values = None

        if isinstance(node, ast.Call):
            values = self._get_args_for_calls(node.args, node.lineno, node.col_offset)

        return ParsedDynamicImport(
            lineno=node.lineno,
            col_offset=node.col_offset,
            dynamic_import=ast.unparse(node),
            identifier=".".join(strings_to_check),
            confirmed=self._check_if_confirmed_dynamic_import(strings_to_check),
            values=values,
        )

    def visit_Call(self, node: ast.Call) -> None:
        """Visit a Call node."""
        identifier_path = list(generate_identifier_path(node.func))

        if self._check_for_dynamic_imports(identifier_path):
            parsed_dynamic_import = self._get_parsed_dynamic_import(identifier_path, node)
            self.nodes.append(parsed_dynamic_import)

        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> None:
        """Visit an Assign node."""
        identifier_path = list(generate_identifier_path(node.value))

        if self._check_for_dynamic_imports(identifier_path):
            parsed_dynamic_import = self._get_parsed_dynamic_import(identifier_path, node)
            self.nodes.append(parsed_dynamic_import)

        self.generic_visit(node)

    def visit_If(self, node: ast.If) -> None:
        """Visit an If node."""
        all_branch_nodes = node.body + node.orelse
        conditional_imports = (
            (sub_node.lineno, sub_node.col_offset, sub_node)
            for sub_node in all_branch_nodes
            if isinstance(sub_node, (ast.Import, ast.ImportFrom))
        )

        for lineno, col_offset, sub_node in conditional_imports:
            assert isinstance(sub_node, ast.AST)
            self.nodes.append(
                ParsedIfImport(
                    lineno=lineno,
                    col_offset=col_offset,
                    sub_node=ast.unparse(sub_node),
                )
            )

        self.generic_visit(node)

    def _classify_type(self, package_names: list[str]) -> ImportType:
        """
        Classify the import type.

        Start by walking through package names from most-specific to
        least-specific, taking the first match found.

        Parameters
        ----------
        package_names : list[str]
            Package names

        Returns
        -------
        ImportType
        """
        for package in reversed(package_names):
            if package == "__future__":
                return ImportType.FUTURE
            elif package in self.base_packages:
                return ImportType.FIRST_PARTY
            elif package in self.stdlib_names:
                return ImportType.STDLIB

        return ImportType.THIRD_PARTY


@define(slots=True)
class DynamicStringVisitor(ast.NodeVisitor):
    """Dynamic string visitor for parsing dynamic imports.

    Future support will be added for parsing dynamic strings for custom
    import rules, so that users can specify custom rules for dynamic imports.
    """

    base_packages: list[str] = field(factory=list)
    filename: str | None = None
    nodes: list = field(factory=list)

    # we want the line number and column offset to match the node that
    # contains the dynamic string
    lineno: int | None = 0
    col_offset: int | None = 0

    def visit_Import(self, node: ast.Import) -> None:
        """Visit an Dynamic String Import node."""
        parsed_imports_dict = get_module_info_from_import_node(node)

        for alias in node.names:
            module_info = parsed_imports_dict[alias.name]
            module_info["import_type"] = ImportType.DYNAMIC

            dynamic_string_import = DynamicStringStraightImport(
                import_type=module_info["import_type"],
                module=module_info["module"],
                asname=module_info["asname"],
                lineno=self.lineno,
                col_offset=self.col_offset,
                node_col_offset=module_info["node_col_offset"],
                alias_col_offset=module_info["alias_col_offset"],
                package=module_info["package"],
                package_names=module_info["package_names"],
                private_identifier_import=module_info["private_identifier_import"],
                private_module_import=module_info["private_module_import"],
                import_statement=module_info["import_statement"],
            )
            self.nodes.append(dynamic_string_import)

        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Visit a Dynamic String Import From node."""
        parsed_from_imports_dict = get_name_info_from_import_node(node)

        for alias in node.names:
            name_info = parsed_from_imports_dict[alias.name]
            name_info["import_type"] = ImportType.DYNAMIC

            dynamic_string_from_import = DynamicStringFromImport(
                import_type=name_info["import_type"],
                module=name_info["module"],
                name=name_info["name"],
                asname=name_info["asname"],
                lineno=self.lineno,
                col_offset=name_info["col_offset"],
                node_col_offset=name_info["node_col_offset"],
                alias_col_offset=name_info["alias_col_offset"],
                level=name_info["level"],
                package=name_info["package"],
                package_names=name_info["package_names"],
                private_identifier_import=name_info["private_identifier_import"],
                private_module_import=name_info["private_module_import"],
                import_statement=name_info["import_statement"],
            )
            self.nodes.append(dynamic_string_from_import)

        self.generic_visit(node)
