""" A basic module. """
from datetime import datetime
from uuid import UUID
from uuid import uuid4

import pendulum
from attrs import define
from attrs import field


@define(slots=True)
class ARelative:
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
