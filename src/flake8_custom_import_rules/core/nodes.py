"""Parsed Node Classes to store library and module info to check custom import rules."""

from enum import Enum

from attrs import define
from attrs import field


class ImportType(Enum):
    """Import type enum."""

    FUTURE = "FUTURE"
    STDLIB = "STDLIB"
    THIRD_PARTY = "THIRD_PARTY"
    FIRST_PARTY = "FIRST_PARTY"
    RELATIVE = "RELATIVE"
    DYNAMIC = "DYNAMIC"


@define(slots=True)
class ParsedStraightImport:
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
    import_statement: str
    identifier: str = field(init=False)

    def __attrs_post_init__(self) -> None:
        """Post init hook."""
        self.identifier = self.module


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
    import_statement: str
    identifier: str = field(init=False)

    def __attrs_post_init__(self) -> None:
        """Post init hook."""
        self.identifier = f"{self.module}.{self.name}"


@define(slots=True)
class ParsedLocalImport:
    """Parsed class definition"""

    lineno: int
    col_offset: int
    local_node_type: str
    import_statement: str


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


@define(slots=True)
class DynamicStringFromImport(ParsedFromImport):
    """Dynamic string import."""


@define(slots=True)
class DynamicStringStraightImport(ParsedStraightImport):
    """Dynamic string import."""


@define(slots=True)
class DynamicStringParseSyntaxFailure:
    """Dynamic string import syntax failure."""

    lineno: int
    col_offset: int
    value: str


@define(slots=True)
class HelperParsedImport:
    """Helper parsed import statement for tests."""

    lineno: int = 0
    col_offset: int = 0
    import_statement: str = ""
    identifier: str = ""


ParsedNode = (
    ParsedStraightImport
    | ParsedFromImport
    | ParsedLocalImport
    | ParsedClassDef
    | ParsedFunctionDef
    | ParsedCall
    | HelperParsedImport
    | ParsedDynamicImport
    | ParsedIfImport
    | DynamicStringStraightImport
    | DynamicStringFromImport
)
