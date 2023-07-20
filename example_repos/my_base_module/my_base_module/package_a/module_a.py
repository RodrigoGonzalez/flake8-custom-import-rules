""" A basic module for testing and demonstrating flake8-custom-import-rules. """
from __future__ import annotations  # Do Not Remove Needed for Examples

import sys
from datetime import datetime
from uuid import UUID
from uuid import uuid4

import pendulum
from attrs import define
from attrs import field

from my_base_module.package_b.module_b import B
from my_base_module.package_c.module_c import C
from my_base_module.package_c.package_d.module_d import D as DEE

from .module_a_relative import ARelative

if sys.version_info >= (3, 7):
    from my_base_module.package_c.package_e.module_e import OldE as VersionedE
else:
    from my_base_module.package_c.package_e.module_e import EUpdated as VersionedE


SOME_CONSTANT = "some_constant"
COMPLEX_CONSTANT = {"some_key": "some_value"}


@define(slots=True)
class A:
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

    def initialize_class_a_relative(self) -> ARelative:
        """Get the class A."""
        return ARelative(
            name=f"{self._name}: ARelative", description=f"{self._description}: ARelative"
        )

    def initialize_class_b(self) -> B:
        """Get the class B."""
        return B(name=f"{self._name}: B", description=f"{self._description}: B")

    def initialize_class_c(self) -> C:
        """Get the class C."""
        return C(name=f"{self._name}: C", description=f"{self._description}: C")

    def initialize_class_dee(self) -> DEE:
        """Get the class D."""
        return DEE(name=f"{self._name}: DEE", description=f"{self._description}: DEE")

    def initialize_class_e(self) -> VersionedE:
        """Get the class E."""
        return VersionedE(
            name=f"{self._name}: VersionedE", description=f"{self._description}: VersionedE"
        )

    def get_name_of_class_x(self, print_class_x: bool = True) -> str:
        """Get the name of class X."""
        import datetime
        from my_base_module.module_x import X, print_x

        x = X(
            name=f"{self._name}: X",
            description=f"{self._description}: X",
            created_at=datetime.datetime.now(),
        )
        if print_class_x:
            print_x(x)

        return x.name()

    @staticmethod
    def dynamic_imports_one() -> None:
        """Use dynamic imports."""
        import importlib
        importlib.import_module('datetime')
        exec('import datetime')
        eval('import datetime')

    @staticmethod
    def dynamic_imports_two() -> None:
        """Use dynamic imports."""
        from importlib import import_module
        import_module('datetime')
        __import__('datetime')
