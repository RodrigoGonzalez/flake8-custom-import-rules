import ast
from typing import NamedTuple

from flake8_import_order.checker import ImportVisitor
from flake8_import_order.styles import ImportType

from flake8_custom_import_rules.node_utils import get_module_info_from_import_node
from flake8_custom_import_rules.node_utils import get_name_info_from_import_node
from flake8_custom_import_rules.node_utils import get_package_names
from flake8_custom_import_rules.node_utils import root_package_name


class ParsedImport(NamedTuple):
    """Parsed import statement"""

    import_type: ImportType
    module: str
    asname: str | None
    lineno: int
    col_offset: int
    package: str
    package_names: list[str]


class ParsedFromImport(NamedTuple):
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


class ParsedClassDef(NamedTuple):
    """Parsed class definition"""

    name: str
    lineno: int
    col_offset: int


class ParsedFunctionDef(NamedTuple):
    """Parsed function definition"""

    name: str
    lineno: int
    col_offset: int


class ParsedComment(NamedTuple):
    """Parsed noqa comment"""

    lineno: int
    col_offset: int
    codes: list[str]


ParsedNode = ParsedImport | ParsedFromImport | ParsedClassDef | ParsedFunctionDef


class PublicImportVisitor(ImportVisitor):
    """Public class to expose `_classify_type` method."""

    application_import_names: frozenset
    application_package_names: frozenset
    imports: list

    def __init__(
        self, application_import_names: list[str] | str, application_package_names: list[str] | str
    ) -> None:
        super().__init__(application_import_names, application_package_names)

    def classify_type(self, module: str) -> ImportType:
        """Classify the type of import."""
        return self._classify_type(module)


class CustomImportRulesVisitor(ast.NodeVisitor):
    """Custom import rules node visitor."""

    errors: list[tuple[int, int, str]] = list()
    current_modules: list[str] = list()
    package_names: list[list[str]] = list()
    imports: list = list()
    nodes: list = list()

    def __init__(
        self,
        application_import_names: list[str],
        standard_library_only: list[str],
    ) -> None:
        """Initialize the visitor."""
        self.import_visitor = PublicImportVisitor(application_import_names, standard_library_only)
        self.nodes = []

    def visit_Import(self, node: ast.Import) -> None:
        """Visit an Import node."""
        parsed_imports_dict = get_module_info_from_import_node(node)
        modules = parsed_imports_dict["node_modules_lineno"][str(node.lineno)]
        for module in modules:
            import_type = self.import_visitor.classify_type(module)
            parsed_imports_dict[module]["import_type"] = import_type
            self.nodes.append(
                ParsedImport(
                    import_type=import_type,
                    module=module,
                    asname=parsed_imports_dict[module]["asname"],
                    lineno=node.lineno,
                    col_offset=node.col_offset,
                    package=root_package_name(module),
                    package_names=get_package_names(module),
                )
            )
        # Ensures a complete traversal of the AST
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Visit an Import node."""
        module = node.module or ""

        if node.level > 0:
            import_type = ImportType.APPLICATION_RELATIVE
        else:
            import_type = self.import_visitor.classify_type(module)
        parsed_from_imports_dict = get_name_info_from_import_node(node)
        names = parsed_from_imports_dict["node_names_lineno"][str(node.lineno)]
        for name in names:
            parsed_from_imports_dict[name]["import_type"] = import_type
            self.nodes.append(
                ParsedFromImport(
                    import_type=import_type,
                    module=module,
                    name=name,
                    asname=parsed_from_imports_dict[name]["asname"],
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
