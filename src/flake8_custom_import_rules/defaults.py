"""The default settings for the flake8_custom_import_rules plugin."""
from attrs import asdict
from attrs import define
from attrs import field


@define(slots=True)
class Settings:
    """The default settings for the flake8_custom_import_rules plugin."""

    BASE_PACKAGE: str | list[str] | None = field(default=None)

    TOP_LEVEL_ONLY: bool = field(default=True)
    RESTRICT_RELATIVE_IMPORTS: bool = field(default=True)
    RESTRICT_LOCAL_IMPORTS: bool = field(default=True)
    RESTRICT_CONDITIONAL_IMPORTS: bool = field(default=True)
    RESTRICT_DYNAMIC_IMPORTS: bool = field(default=True)
    RESTRICT_FUNCTIONAL_IMPORTS: bool = field(default=False)
    RESTRICT_WILDCARD_IMPORTS: bool = field(default=True)
    RESTRICT_ALIASED_IMPORTS: bool = field(default=False)

    RESTRICT_IMPORTS_FROM_INIT: bool = field(default=True)
    RESTRICT_IMPORTS_FROM_TESTS: bool = field(default=True)
    RESTRICT_IMPORTS_FROM_CONFTEST: bool = field(default=True)

    RESTRICTED_IMPORTS: set = field(factory=set)
    IMPORT_RULES: dict = field(factory=dict)

    def __attrs_post_init__(self) -> None:
        self.RESTRICTED_IMPORTS = set(self.RESTRICTED_IMPORTS)
        self.BASE_PACKAGE = (
            [self.BASE_PACKAGE] if isinstance(self.BASE_PACKAGE, str) else self.BASE_PACKAGE
        )

    def to_dict(self) -> dict:
        """Return the settings as a dictionary."""
        return asdict(self)


DEFAULT_SETTINGS = Settings()
