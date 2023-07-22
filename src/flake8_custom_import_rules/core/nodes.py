"""Parsed Nodes for custom import rules."""
from enum import IntEnum

from attr import define
from attr import field


class ImportType(IntEnum):
    """Import type enum."""

    FUTURE = 0
    STDLIB = 10
    THIRD_PARTY = 20
    FIRST_PARTY = 30
    RELATIVE = 40
    DYNAMIC = 100


@define(slots=True)
class ParsedImport:
    """Parsed import statement"""

    import_type: ImportType
    module: str
    asname: str | None
    lineno: int
    col_offset: int
    node_col_offset: int
    alias_col_offset: int
    package: str
    package_names: list[str]
    private_identifier_import: bool
    private_module_import: bool
    import_node: str
    identifier: str = field(init=False)

    def __attrs_post_init__(self) -> None:
        """Post init hook."""
        # if self.level > 0:
        #     self.package = root_package_name(self.module)
        self.identifier = self.module


@define(slots=True)
class DynamicStringImport(ParsedImport):
    """Dynamic string import."""


@define(slots=True)
class ParsedFromImport:
    """Parsed import statement"""

    import_type: ImportType
    module: str
    name: str
    asname: str | None
    lineno: int
    col_offset: int
    node_col_offset: int
    alias_col_offset: int
    level: int
    package: str | None
    package_names: list[str]
    private_identifier_import: bool
    private_module_import: bool
    import_node: str
    identifier: str = field(init=False)

    def __attrs_post_init__(self) -> None:
        """Post init hook."""
        # if self.level > 0:
        #     self.package = root_package_name(self.module)
        self.identifier = f"{self.module}.{self.name}"


@define(slots=True)
class DynamicStringFromImport(ParsedFromImport):
    """Dynamic string import."""


@define(slots=True)
class ParsedLocalImport:
    """Parsed class definition"""

    lineno: int
    col_offset: int
    local_node_type: str
    import_node: str


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
    call: str | None = None


@define(slots=True)
class ParsedDynamicImport:
    """Parsed dynamic import statement"""

    lineno: int
    col_offset: int
    dynamic_import: str
    identifier: str
    confirmed: bool = False
    values: list[str] | None = None


@define(slots=True)
class ParsedIfImport:
    """Parsed if statement"""

    lineno: int
    col_offset: int
    sub_node: str


ParsedNode = (
    ParsedImport
    | ParsedFromImport
    | ParsedLocalImport
    | ParsedClassDef
    | ParsedFunctionDef
    | ParsedCall
    | ParsedDynamicImport
    | ParsedIfImport
)
