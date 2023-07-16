""" A basic module. """
from abc import ABC
from abc import abstractmethod
from datetime import datetime
from uuid import UUID
from uuid import uuid4

import pendulum
from attrs import define
from attrs import field


class _Base(ABC):
    """Base class"""

    @abstractmethod
    def id(self):
        """Get the id."""

    @abstractmethod
    def name(self):
        """Get the name."""

    @abstractmethod
    def description(self):
        """Get the description."""

    @abstractmethod
    def created_at(self):
        """Get the created_at."""

    @abstractmethod
    def print_hello(self):
        pass


@define(slots=True)
class B(_Base):
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

    def print_hello(self):
        print("Hello world")
