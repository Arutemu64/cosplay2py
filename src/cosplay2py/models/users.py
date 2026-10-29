from enum import StrEnum
from typing import Annotated, Literal

from pydantic import Field

from cosplay2py._types import EmptyAsNone, UTCDateTime
from cosplay2py.models._base import Cosplay2Model
from cosplay2py.models.common import EventTime, RequestStatus, UserBrief


class Sex(StrEnum):
    """User's sex as stored in their profile."""

    MALE = "male"
    FEMALE = "female"


class FriendStatus(StrEnum):
    """Friendship status between the current user and another user."""

    NONE = "none"
    FRIEND = "friend"
    HE_WANTS_TO_FRIEND = "he_wants_to_friend"
    I_WANT_TO_FRIEND = "i_want_to_friend"


class UserEventRoleType(StrEnum):
    """A user's role in an event, as listed in ``UserEvents.roles``."""

    MAINORG = "MAINORG"
    ORG = "ORG"
    CURATOR = "CURATOR"
    REQ_AUTHOR = "REQ_AUTHOR"
    REQ_MEMBER = "REQ_MEMBER"


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
    sex: Annotated[Sex | None, EmptyAsNone] = None
    birthday: str | None = None
    """``"DD.MM.YYYY"``."""
    email: str | None = None
    mobile: str | None = None
    vk: str | None = None
    """Link to the user's VK page."""
    friend_status: FriendStatus | None = None


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
    time: EventTime | None = None


class UserEventRole(Cosplay2Model):
    id: int
    """Event ID."""
    er: UserEventRoleType
    """The user's role in the event, e.g. ``"ORG"``."""
    city: str | None = None
    t_title: str | None = None
    """Topic title (for ``CURATOR``, ``REQ_AUTHOR`` and ``REQ_MEMBER``)."""
    r_id: int | None = None
    """Request ID (for ``REQ_AUTHOR`` and ``REQ_MEMBER``)."""
    number: int | None = None
    """Request number within its topic."""
    status: RequestStatus | None = None
    card_enabled: bool | None = None
    card_code: str | None = None
    voting_number: int | None = None
    voting_title: str | None = None
    win: Literal[1, 2, 3] | None = None
    win_title: str | None = None


class UserEvents(Cosplay2Model):
    events: list[UserEvent]
    roles: list[UserEventRole] = Field(default_factory=list, alias="data")
