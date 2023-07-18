"""Custom import rules node visitor."""
import ast
from enum import IntEnum
from pathlib import Path

from attrs import define
from flake8_import_order.stdlib_list import STDLIB_NAMES

from flake8_custom_import_rules.utils.node_utils import get_module_info_from_import_node
from flake8_custom_import_rules.utils.node_utils import get_name_info_from_import_node
from flake8_custom_import_rules.utils.node_utils import get_package_names
from flake8_custom_import_rules.utils.node_utils import root_package_name


class ImportType(IntEnum):
    """Import type enum."""

    FUTURE = 0
    STDLIB = 10
    THIRD_PARTY = 20
    FIRST_PARTY = 30
    LOCAL = 40


@define(slots=True)
class ParsedImport:
    """Parsed import statement"""

    import_type: ImportType
    module: str
    asname: str | None
    lineno: int
    col_offset: int
    package: str
    package_names: list[str]


@define(slots=True)
class ParsedFromImport:
    """Parsed import statement"""

    import_type: ImportType
    module: str
    name: str
    asname: str | None
    lineno: int
    col_offset: int
    level: int
    package: str | None
    package_names: list[str]


@define(slots=True)
class ParsedClassDef:
    """Parsed class definition"""

    name: str
    lineno: int
    col_offset: int


@define(slots=True)
class ParsedFunctionDef:
    """Parsed function definition"""

    name: str
    lineno: int
    col_offset: int


@define(slots=True)
class ParsedCall:
    """Parsed call statement"""

    func: str
    lineno: int
    col_offset: int


@define(slots=True)
class ParsedComment:
    """Parsed noqa comment"""

    lineno: int
    col_offset: int
    codes: list[str]


ParsedNode = ParsedImport | ParsedFromImport | ParsedClassDef | ParsedFunctionDef | ParsedCall


class CustomImportRulesVisitor(ast.NodeVisitor):
    """Custom import rules node visitor."""

    errors: list[tuple[int, int, str]] = list()
    current_modules: list[str] = list()
    package_names: list[list[str]] = list()
    imports: list = list()
    nodes: list = list()
    filename: Path | None = None

    def __init__(
        self,
        application_import_names: list[str],
        standard_library_only: list[str],
        filename: str | None = None,
    ) -> None:
        """Initialize the visitor."""
        self.nodes: list = []
        self.current_modules: list = application_import_names
        self.standard_library_only = standard_library_only
        self.filename = Path(filename) if filename else None
        print(f"Visitor filename: {self.filename}")
        self.resolve_local_imports = filename not in {"stdin", "-", "/dev/stdin", None}
        print(f"Resolve local imports: {self.resolve_local_imports}")

    def visit_Import(self, node: ast.Import) -> None:
        """Visit an Import node."""
        parsed_imports_dict = get_module_info_from_import_node(node)
        modules = parsed_imports_dict["node_modules_lineno"][str(node.lineno)]

        for module in modules:
            module_info = parsed_imports_dict[module]
            import_type = self._classify_type(module)
            module_info["import_type"] = import_type
            self.nodes.append(
                ParsedImport(
                    import_type=import_type,
                    module=module,
                    asname=module_info["asname"],
                    lineno=node.lineno,
                    col_offset=node.col_offset,
                    package=root_package_name(module),
                    package_names=get_package_names(module),
                )
            )

        # Ensures a complete traversal of the AST
        self.generic_visit(node)

    def _resolve_local_import(self, module: str, node_level: int) -> Path | None:
        """Resolve a local import."""
        parent = self.filename.parents[node_level - 1] if self.filename else None
        return parent / f"{module}.py" if parent else None

    def _get_import_type(self, module: str, node_level: int) -> ImportType:
        """Get the import type for a module."""
        return ImportType.LOCAL if node_level > 0 else self._classify_type(module)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Visit an Import node."""
        module = node.module or ""
        import_type = self._get_import_type(module, node.level)
        parsed_from_imports_dict = get_name_info_from_import_node(node)
        names = parsed_from_imports_dict["node_names_lineno"][str(node.lineno)]

        for name in names:
            name_info = parsed_from_imports_dict[name]
            name_info["import_type"] = import_type
            self.nodes.append(
                ParsedFromImport(
                    import_type=import_type,
                    module=module,
                    name=name,
                    asname=name_info["asname"],
                    lineno=node.lineno,
                    col_offset=node.col_offset,
                    level=node.level,
                    package=root_package_name(module),
                    package_names=get_package_names(module),
                )
            )

        # Ensures a complete traversal of the AST
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Visit a ClassDef node."""
        self.nodes.append(
            ParsedClassDef(
                name=node.name,
                lineno=node.lineno,
                col_offset=node.col_offset,
            )
        )
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
        self.generic_visit(node)

    @staticmethod
    def _func_name(func: ast.Name) -> str:
        """Get the function name."""
        return func.id

    @staticmethod
    def _func_attribute(func: ast.Attribute) -> str:
        """Get the function name."""
        return func.attr

    def visit_Call(self, node: ast.Call) -> None:
        """Visit a Call node."""
        if isinstance(node.func, ast.Name):
            self.nodes.append(
                ParsedCall(
                    func=self._func_name(node.func),
                    lineno=node.lineno,
                    col_offset=node.col_offset,
                )
            )
        elif isinstance(node.func, ast.Attribute):
            self.nodes.append(
                ParsedCall(
                    func=self._func_attribute(node.func),
                    lineno=node.lineno,
                    col_offset=node.col_offset,
                )
            )
        # else:
        #     self.nodes.append(
        #         ParsedCall(
        #             func=self._func_name(node),
        #             lineno=node.lineno,
        #             col_offset=node.col_offset,
        #         )
        #     )
        self.generic_visit(node)

    def _classify_type(self, module: str) -> ImportType:
        """
        Classify the import type.

        Parameters
        ----------
        module : str
            Module name

        Returns
        -------
        ImportType
        """
        package_names = get_package_names(module)

        # Walk through package names from most-specific to least-specific,
        # taking the first match found.
        for package in reversed(package_names):
            if package == "__future__":
                return ImportType.FUTURE
            elif package in self.current_modules:
                return ImportType.FIRST_PARTY
            elif package in STDLIB_NAMES:
                return ImportType.STDLIB

        # Not future, stdlib or an application import.
        # Must be 3rd party.
        return ImportType.THIRD_PARTY
