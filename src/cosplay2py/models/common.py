from enum import IntEnum, StrEnum

from cosplay2py._types import UTCDateTime
from cosplay2py.models._base import Cosplay2Model


class EventRole(IntEnum):
    """Numeric role / permission level in an event (``globals.ER`` on the site)."""

    GUEST = 0
    USER = 1
    REQ_MEMBER = 2
    REQ_AUTHOR = 3
    CURATOR = 4
    ORG = 5
    MAINORG = 6
    GOD = 100


class EventTime(StrEnum):
    """Whether an event is currently running, upcoming, or over."""

    ACTIVE = "active"
    FUTURE = "future"
    PAST = "past"


class RequestStatus(StrEnum):
    """Lifecycle status of a request (an application to take part in a topic)."""

    NEW = "new"
    """Seen on a request right after ``requests.create``."""
    PENDING = "pending"
    WAITING = "waiting"
    MATERIALS = "materials"
    REVIEW = "review"
    APPROVED = "approved"
    DISAPPROVED = "disapproved"


class UserBrief(Cosplay2Model):
    """A short public user profile, as embedded in many responses."""

    user_id: int
    title: str | None = None
    """The user's nickname."""
    city: str | None = None
    image_update_time: UTCDateTime | None = None
    """When the avatar was last changed; useful as a cache buster."""
