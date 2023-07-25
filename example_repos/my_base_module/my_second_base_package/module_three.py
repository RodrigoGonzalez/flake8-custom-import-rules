""" A basic module. """
from datetime import datetime
from uuid import UUID
from uuid import uuid4

import pendulum
from attrs import define
from attrs import field

import my_base_module.module_y
import my_second_base_package.module_one
from my_base_module.module_x import X
from my_second_base_package.module_two import ModuleTwo


@define(slots=True)
class ModuleThree:
    """A basic class"""

    _id: UUID | None = field(factory=uuid4)
    _name: str | None = field(default="name")
    _description: str | None = field(default="description")
    _created_at: datetime | None = field(factory=pendulum.now)

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


    def initialize_class_x(self) -> X:
        """Initialize class x."""
        return X(
            name=f"{self._name}: X",
            description=f"{self._description}: X",
        )

    def initialize_class_y(self) -> my_base_module.module_y.Y:
        """Initialize class y."""
        return my_base_module.module_y.Y(
            name=f"{self._name}: Y",
            description=f"{self._description}: Y",
        )

    def initialize_class_one(self) -> my_second_base_package.module_one.ModuleOne:
        """Initialize class one."""
        return my_second_base_package.module_one.ModuleOne(
            name=f"{self._name}: ModuleOne",
            description=f"{self._description}: ModuleOne",
        )

    def initialize_class_two(self) -> ModuleTwo:
        """Initialize class two."""
        return ModuleTwo(
            name=f"{self._name}: ModuleTwo",
            description=f"{self._description}: ModuleTwo",
        )
