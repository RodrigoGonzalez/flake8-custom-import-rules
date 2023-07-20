"""Custom import rules node visitor."""
import ast
import logging
from enum import IntEnum
from pathlib import Path

from attrs import define
from attrs import field
from flake8_import_order.stdlib_list import STDLIB_NAMES

from flake8_custom_import_rules.utils.node_utils import get_module_info_from_import_node
from flake8_custom_import_rules.utils.node_utils import get_name_info_from_import_node
from flake8_custom_import_rules.utils.node_utils import get_package_names
from flake8_custom_import_rules.utils.node_utils import root_package_name

logger = logging.getLogger(f"flake8_custom_import_rules.{__name__}")


DYNAMIC_IMPORTS = {
    "__import__",
    "importlib",
    "importlib.import_module",
    "import_module",
    "eval",
    "exec",
}


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
    call_type: str
    values: list[str]
    module: str | None = None


@define(slots=True)
class ParsedIfImport:
    """Parsed if statement"""

    lineno: int
    col_offset: int


@define(slots=True)
class ParsedComment:
    """Parsed noqa comment"""

    lineno: int
    col_offset: int
    codes: list[str]


ParsedNode = (
    ParsedImport
    | ParsedFromImport
    | ParsedClassDef
    | ParsedFunctionDef
    | ParsedCall
    | ParsedIfImport
)


@define(slots=True)
class CustomImportRulesVisitor(ast.NodeVisitor):
    """Custom import rules node visitor."""

    package_names: list[str] = field(factory=list)
    filename: str | None = None
    nodes: list = field(factory=list)
    current_package: list[str] = field(factory=list)
    file_path: Path | None = None
    resolve_local_imports: bool | None = field(default=False)

    def __attrs_post_init__(self) -> None:
        filename = self.filename
        self.file_path = Path(filename) if filename else None
        logger.info(f"Visitor filename: {self.filename}")
        self.resolve_local_imports = filename not in {"stdin", "-", "/dev/stdin", "", None}
        logger.info(f"Resolve local imports: {self.resolve_local_imports}")

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
        parent = self.file_path.parents[node_level - 1] if self.file_path else None
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

    @staticmethod
    def _get_args_for_calls(args: list) -> list[str]:
        """Get the function args."""
        return [arg.value for arg in args if hasattr(arg, "value")]

    def visit_Call(self, node: ast.Call) -> None:
        """Visit a Call node."""
        if isinstance(node.func, ast.Name):
            if self._func_name(node.func) in DYNAMIC_IMPORTS:
                self.nodes.append(
                    ParsedCall(
                        func=self._func_name(node.func),
                        lineno=node.lineno,
                        col_offset=node.col_offset,
                        call_type="ast.Name",
                        values=self._get_args_for_calls(node.args),
                    )
                )
        elif isinstance(node.func, ast.Attribute):
            if self._func_attribute(node.func) in DYNAMIC_IMPORTS:
                self.nodes.append(
                    ParsedCall(
                        func=self._func_attribute(node.func),
                        module=node.func.value.id if hasattr(node.func.value, "id") else None,
                        lineno=node.lineno,
                        col_offset=node.col_offset,
                        call_type="ast.Attribute",
                        values=self._get_args_for_calls(node.args),
                    )
                )
        self.generic_visit(node)

    def visit_If(self, node: ast.If) -> None:
        """Visit an If node."""
        other_nodes = node.body + node.orelse
        if conditional_imports := (
            (sub_node.lineno, sub_node.col_offset)
            for sub_node in other_nodes
            if isinstance(sub_node, (ast.Import, ast.ImportFrom))
        ):
            for lineno, col_offset in conditional_imports:
                self.nodes.append(
                    ParsedIfImport(
                        lineno=lineno,
                        col_offset=col_offset,
                    )
                )
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
            elif package in self.current_package:
                return ImportType.FIRST_PARTY
            elif package in STDLIB_NAMES:
                return ImportType.STDLIB

        # Not future, stdlib or an application import.
        # Must be 3rd party.
        return ImportType.THIRD_PARTY
