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
