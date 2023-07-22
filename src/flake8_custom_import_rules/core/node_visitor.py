"""Custom import rules node visitor."""
import ast
import logging
from collections import defaultdict
from pathlib import Path

from attrs import define
from attrs import field
from flake8_import_order.stdlib_list import STDLIB_NAMES

from flake8_custom_import_rules.core.nodes import DynamicStringFromImport
from flake8_custom_import_rules.core.nodes import DynamicStringImport
from flake8_custom_import_rules.core.nodes import ImportType
from flake8_custom_import_rules.core.nodes import ParsedCall
from flake8_custom_import_rules.core.nodes import ParsedClassDef
from flake8_custom_import_rules.core.nodes import ParsedDynamicImport
from flake8_custom_import_rules.core.nodes import ParsedFromImport
from flake8_custom_import_rules.core.nodes import ParsedFunctionDef
from flake8_custom_import_rules.core.nodes import ParsedIfImport
from flake8_custom_import_rules.core.nodes import ParsedImport
from flake8_custom_import_rules.core.nodes import ParsedLocalImport
from flake8_custom_import_rules.utils.node_utils import generate_identifier_path
from flake8_custom_import_rules.utils.node_utils import get_module_info_from_import_node
from flake8_custom_import_rules.utils.node_utils import get_name_info_from_import_node
from flake8_custom_import_rules.utils.parse_utils import check_string

logger = logging.getLogger(f"flake8_custom_import_rules.{__name__}")


POTENTIAL_DYNAMIC_IMPORTS = {
    "__import__",
    "importlib",
    "importlib.import_module",
    "import_module",
    "pkgutil",
    "pkgutil.get_loader",
    "pkgutil.iter_modules",
    "sys.modules",
    "modules",
    "zipimport",
    "zipimport.zipimporter",
    "zipimporter",
    "zipimporter.load_module",
    "eval",
    "exec",
}


@define(slots=True)
class CustomImportRulesVisitor(ast.NodeVisitor):
    """Custom import rules node visitor."""

    package_names: list[str] = field(factory=list)
    filename: str | None = None
    nodes: list = field(factory=list)
    dynamic_nodes: defaultdict[str, list] = defaultdict(list)
    current_package: list[str] = field(factory=list)
    file_path: Path | None = None
    resolve_local_imports: bool | None = field(default=False)
    identifiers: defaultdict[str, dict] = defaultdict(lambda: defaultdict(str))
    identifiers_by_lineno: defaultdict[str, list] = defaultdict(list)

    def __attrs_post_init__(self) -> None:
        filename = self.filename
        self.file_path = Path(filename) if filename else None
        logger.info(f"Visitor filename: {self.filename}")
        self.resolve_local_imports = filename not in {"stdin", "-", "/dev/stdin", "", None}
        logger.info(f"Resolve local imports: {self.resolve_local_imports}")

    def _resolve_local_import(self, module: str, node_level: int) -> Path | None:
        """Resolve a local import."""
        parent = self.file_path.parents[node_level - 1] if self.file_path else None
        return parent / f"{module}.py" if parent else None

    @staticmethod
    def _get_import_node(module_info: dict) -> ParsedImport:
        """Get a parsed import node."""
        return ParsedImport(
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
            import_node=module_info["import_node"],
        )

    def visit_Import(self, node: ast.Import) -> None:
        """Visit an Import node."""
        parsed_imports_dict = get_module_info_from_import_node(node)

        # pprint.pprint("\nParsed import dict:")
        # pprint.pprint(parsed_imports_dict)

        for alias in node.names:
            module_info = parsed_imports_dict[alias.name]
            module_info["import_type"] = self._classify_type(module_info["package_names"])
            parsed_import = self._get_import_node(module_info)

            self.nodes.append(parsed_import)
            self.identifiers_by_lineno[str(node.lineno)].append(module_info)
            self.identifiers[parsed_import.identifier].update(module_info)
            self.identifiers[alias.name].update(module_info)

        # Ensures a complete traversal of the AST
        self.generic_visit(node)

    def _get_import_type(self, node_level: int, package_names: list[str]) -> ImportType:
        """Get the import type for a module."""
        return ImportType.RELATIVE if node_level > 0 else self._classify_type(package_names)

    @staticmethod
    def _get_from_import_node(name_info: dict) -> ParsedFromImport:
        """Get a parsed from import node."""
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
            import_node=name_info["import_node"],
        )

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Visit an Import From node."""
        parsed_from_imports_dict = get_name_info_from_import_node(node)

        # pprint.pprint("\nParsed from import dict:")
        # pprint.pprint(parsed_from_imports_dict)

        for alias in node.names:
            name_info = parsed_from_imports_dict[alias.name]
            name_info["import_type"] = self._get_import_type(
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
                self.nodes.append(
                    ParsedLocalImport(
                        lineno=stmt.lineno,
                        col_offset=stmt.col_offset,
                        local_node_type=str(type(node)),
                        import_node=ast.unparse(stmt),
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

    @staticmethod
    def _func_name(func: ast.Name) -> str:
        """Get the function name."""
        return func.id

    @staticmethod
    def _func_attribute(func: ast.Attribute) -> str:
        """Get the function name."""
        return func.attr

    def _get_dynamic_string_visitor(self, lineno: int, col_offset: int) -> "DynamicStringVisitor":
        """Get the dynamic string visitor."""
        print(f"get_dynamic_string_visitor: {lineno}")
        return DynamicStringVisitor(
            package_names=self.package_names,
            filename=self.filename,
            lineno=lineno,
            col_offset=col_offset,
        )

    def _parse_value_string(self, value: str, lineno: int, col_offset: int) -> str:
        """Parse the value strings."""
        print(f"parse_value_string: {value}")
        node = ast.parse(value)
        print(f"node: {node}")
        dynamic_string_visitor = self._get_dynamic_string_visitor(lineno, col_offset)
        dynamic_string_visitor.visit(node)

        for dynamic_node in dynamic_string_visitor.nodes:
            self.dynamic_nodes[str(lineno)].append(dynamic_node)
            self.nodes.append(dynamic_node)

        return value

    def _get_args_for_calls(self, args: list, lineno: int, col_offset: int) -> list[str]:
        """Get the function args."""
        print(f"get_args_for_calls: {args} lineno: {lineno}")
        return [
            self._parse_value_string(arg.value, lineno, col_offset)
            for arg in args
            if hasattr(arg, "value")
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
    def _check_if_bare_modules(strings_to_check: list[str]) -> bool:
        """Check if the string is a bare module.

        "modules" is a common object name, so we need to check
        that it was imported from the "sys" package.
        However, this should be done after running the node visitor.
        """
        if check_string(strings_to_check, substring_match="modules"):
            # if "modules" is in the string, check if it was imported from "sys"
            # if "sys" is not in the string, the following will return True
            return not check_string(strings_to_check, substring_match="sys")
        return False

    def _check_if_confirmed_dynamic_import(self, strings_to_check: list[str]) -> bool:
        # a bare "modules" is not a confirmed dynamic import
        if self._check_if_bare_modules(strings_to_check):
            return False
        return not self._check_dynamic_code_execution_functions(strings_to_check)

    def visit_Call(self, node: ast.Call) -> None:
        """Visit a Call node."""
        identifier_path = list(generate_identifier_path(node.func))
        print(f"{node.lineno} visit_Call: {identifier_path}")
        if self._check_for_dynamic_imports(identifier_path):
            parsed_dynamic_import = ParsedDynamicImport(
                lineno=node.lineno,
                col_offset=node.col_offset,
                dynamic_import=ast.unparse(node),
                identifier=".".join(identifier_path),
                confirmed=self._check_if_confirmed_dynamic_import(identifier_path),
                values=self._get_args_for_calls(node.args, node.lineno, node.col_offset),
            )
            self.nodes.append(parsed_dynamic_import)

        if isinstance(node.func, ast.Name):
            # print(f"visit_Call: {node.func}")
            if self._func_name(node.func) in POTENTIAL_DYNAMIC_IMPORTS:
                self.nodes.append(
                    ParsedCall(
                        func=self._func_name(node.func),
                        lineno=node.lineno,
                        col_offset=node.col_offset,
                        call_type="ast.Name",
                        values=self._get_args_for_calls(node.args, node.lineno, node.col_offset),
                        call=ast.unparse(node),
                    )
                )
        elif isinstance(node.func, ast.Attribute):
            # print(f"visit_Call: {node.func}")
            if self._func_attribute(node.func) in POTENTIAL_DYNAMIC_IMPORTS:
                self.nodes.append(
                    ParsedCall(
                        func=self._func_attribute(node.func),
                        module=node.func.value.id if hasattr(node.func.value, "id") else None,
                        lineno=node.lineno,
                        col_offset=node.col_offset,
                        call_type="ast.Attribute",
                        values=self._get_args_for_calls(node.args, node.lineno, node.col_offset),
                        call=ast.unparse(node),
                    )
                )
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> None:
        """Visit an Assign node."""
        identifier_path = list(generate_identifier_path(node.value))

        if self._check_for_dynamic_imports(identifier_path):
            self.nodes.append(
                ParsedDynamicImport(
                    lineno=node.lineno,
                    col_offset=node.col_offset,
                    dynamic_import=ast.unparse(node),
                    identifier=".".join(identifier_path),
                    confirmed=self._check_if_confirmed_dynamic_import(identifier_path),
                )
            )

        self.generic_visit(node)

    def visit_If(self, node: ast.If) -> None:
        """Visit an If node."""
        other_nodes = node.body + node.orelse
        if conditional_imports := (
            (sub_node.lineno, sub_node.col_offset, sub_node)
            for sub_node in other_nodes
            if isinstance(sub_node, (ast.Import, ast.ImportFrom))
        ):
            for lineno, col_offset, sub_node in conditional_imports:
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

        Parameters
        ----------
        package_names : list[str]
            Package names

        Returns
        -------
        ImportType
        """

        # Walk through package names from most-specific to least-specific,
        # taking the first match found.
        for package in reversed(package_names):
            if package == "__future__":
                return ImportType.FUTURE
            elif package in self.current_package:
                return ImportType.FIRST_PARTY
            elif package in STDLIB_NAMES:
                return ImportType.STDLIB

        # Not future, stdlib or an application import.
        # Must be 3rd party.
        return ImportType.THIRD_PARTY


@define(slots=True)
class DynamicStringVisitor(ast.NodeVisitor):
    """Dynamic string visitor for parse dynamic imports."""

    package_names: list[str] = field(factory=list)
    filename: str | None = None
    nodes: list = field(factory=list)

    # we want the line number to match the node that contains the dynamic string
    lineno: int | None = 0
    col_offset: int | None = 0

    def visit_Import(self, node: ast.Import) -> None:
        """Visit an Dynamic String Import node."""
        parsed_imports_dict = get_module_info_from_import_node(node)

        for alias in node.names:
            module_info = parsed_imports_dict[alias.name]
            module_info["import_type"] = ImportType.DYNAMIC

            dynamic_string_import = DynamicStringImport(
                import_type=module_info["import_type"],
                module=module_info["module"],
                asname=module_info["asname"],
                lineno=self.lineno,
                col_offset=module_info["col_offset"],
                node_col_offset=module_info["node_col_offset"],
                alias_col_offset=module_info["alias_col_offset"],
                package=module_info["package"],
                package_names=module_info["package_names"],
                private_identifier_import=module_info["private_identifier_import"],
                private_module_import=module_info["private_module_import"],
                import_node=module_info["import_node"],
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
                import_node=name_info["import_node"],
            )
            self.nodes.append(dynamic_string_from_import)

        self.generic_visit(node)
