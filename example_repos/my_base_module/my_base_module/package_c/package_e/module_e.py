""" A basic module. """
from datetime import datetime
from uuid import UUID
from uuid import uuid4

import pendulum
from attrs import define
from attrs import field


@define(slots=True)
class OldE:
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


@define(slots=True)
class EUpdated:
    """A basic class"""

    _id: UUID | None = field(factory=uuid4)
    _name: str | None = field(default="name")
    _description: str | None = field(default="description")
    _created_at: datetime | None = field(factory=pendulum.now)

    def __attrs_post_init__(self):
        """Post init hook."""
        self._updated_at = pendulum.now()

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

    def updated_at(self):
        """Get the updated_at."""
        return self._updated_at
