"""The default settings for the flake8_custom_import_rules plugin."""
from attrs import asdict
from attrs import define
from attrs import field


@define(slots=True)
class Settings:
    """The default settings for the flake8_custom_import_rules plugin."""

    base_package: str | list[str] | None = field(default=None)

    TOP_LEVEL_ONLY: bool = field(default=True)
    RESTRICT_RELATIVE_IMPORTS: bool = field(default=True)
    RESTRICT_LOCAL_IMPORTS: bool = field(default=True)
    RESTRICT_CONDITIONAL_IMPORTS: bool = field(default=True)
    RESTRICT_DYNAMIC_IMPORTS: bool = field(default=True)
    RESTRICT_PRIVATE_IMPORTS: bool = field(default=False)
    RESTRICT_WILDCARD_IMPORTS: bool = field(default=True)
    RESTRICT_ALIASED_IMPORTS: bool = field(default=False)

    RESTRICT_INIT_IMPORTS: bool = field(default=True)
    RESTRICT_TEST_IMPORTS: bool = field(default=True)
    RESTRICT_CONFTEST_IMPORTS: bool = field(default=True)

    restricted_imports: set = field(factory=set)
    import_rules: dict = field(factory=dict)

    def __attrs_post_init__(self) -> None:
        self.restricted_imports = set(self.restricted_imports)
        self.base_package = (
            [self.base_package] if isinstance(self.base_package, str) else self.base_package
        )

    def to_dict(self) -> dict:
        """Return the settings as a dictionary."""
        return asdict(self)

    def get_option_keys(self) -> list:
        """Return the options as a dictionary."""
        settings = self.to_dict()
        return [key for key in settings.keys() if key.isupper()]


DEFAULT_CHECKER_SETTINGS = Settings()
