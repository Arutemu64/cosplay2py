from pydantic import Field

from cosplay2py._types import UTCDateTime
from cosplay2py.models._base import Cosplay2Model
from cosplay2py.models.common import UserBrief


class Friend(UserBrief):
    id: int | None = None
    """Same as ``user_id``."""


class UserSearchResult(UserBrief):
    id: int | None = None
    """Same as ``user_id``."""
    friends_boost: int | None = None
    """``0`` in every result seen so far."""


class UserProfile(UserBrief):
    """A user's profile, as shown on their profile page.

    Full name, ``birthday``, ``email`` and ``mobile`` are only sent for yourself and
    your friends.
    """

    id: int | None = None
    """Same as ``user_id``."""
    first_name: str | None = None
    second_name: str | None = None
    """Last name."""
    third_name: str | None = None
    """Patronymic."""
    sex: str | None = None
    """``"male"`` or ``"female"``."""
    birthday: str | None = None
    """``"DD.MM.YYYY"``."""
    email: str | None = None
    mobile: str | None = None
    vk: str | None = None
    """Link to the user's VK page."""
    friend_status: str | None = None
    """Your friendship with this user: ``"none"`` or ``"friend"``."""


class Friendship(Cosplay2Model):
    """A friendship of the user, as listed on their profile."""

    id: int
    """ID of the friendship itself."""
    friend_id: int
    """The friend's user ID."""
    friend_title: str | None = None
    """The friend's nickname."""
    friend_city: str | None = None
    status: int | None = None
    """``1`` for an accepted friendship."""
    invitetome: bool | None = None
    """Whether the friend sent the invitation."""


class UserDetails(Cosplay2Model):
    """A user's profile and friends, as returned by ``users.get``."""

    user: UserProfile
    friends: list[Friendship] = Field(default_factory=list)
    """Only filled in on your own profile."""


class UserEvent(Cosplay2Model):
    id: int
    title: str
    subdomain: str
    domain: str | None = None
    hostname: str | None = None
    city: str | None = None
    start_time: UTCDateTime | None = None
    end_time: UTCDateTime | None = None
    time: str | None = None
    """``"past"``, ``"current"`` or ``"future"``."""


class UserEventRole(Cosplay2Model):
    id: int
    """Event ID."""
    er: str
    """The user's role in the event, e.g. ``"ORG"``."""
    city: str | None = None


class UserEvents(Cosplay2Model):
    events: list[UserEvent]
    roles: list[UserEventRole] = Field(default_factory=list, alias="data")
