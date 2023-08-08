""" A basic module. """
from datetime import datetime
from uuid import UUID
from uuid import uuid4


from attrs import (
    define,
    field,
)

from my_second_base_package.module_one.file_two import ModuleTwo
from my_second_base_package.module_two.file_two import ModuleTwoFileTwo

@define(slots=True)
class ModuleTwoFileOne:
    """A basic class"""

    _id: UUID | None = field(factory=uuid4)
    _name: str | None = field(default="name")
    _description: str | None = field(default="description")
    _created_at: datetime | None = field(factory=datetime.now)

    def id(self):
        """Get the id."""
        return self._id

    def name(self):
        """Get the name."""
        return self._name

    def description(self):
        """Get the description."""
        return self._description

    def created_at(self):
        """Get the created_at."""
        return self._created_at

    def initialize_class_two(self) -> ModuleTwo:
        """Initialize class two."""
        return ModuleTwo(
            name=f"{self._name}: ModuleTwo",
            description=f"{self._description}: ModuleTwo",
        )

    def initialize_class_two_file_two(self) -> ModuleTwoFileTwo:
        """Initialize class two file two."""
        return ModuleTwoFileTwo(
            name=f"{self._name}: ModuleTwoFileTwo",
            description=f"{self._description}: ModuleTwoFileTwo",
        )
