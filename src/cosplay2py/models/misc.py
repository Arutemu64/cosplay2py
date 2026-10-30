"""Models for the smaller resources: pages, media, e-tickets and voting tickets."""

from enum import IntEnum, StrEnum
from typing import Any

from pydantic import Field

from cosplay2py._types import UTCDateTime
from cosplay2py.models._base import Cosplay2Model
from cosplay2py.models.common import EventRole


class PageType(StrEnum):
    """Kind of an entry in the event site's page tree."""

    PAGE = "page"
    FOLDER = "folder"
    """A menu group holding other pages."""
    LINK = "link"
    """A menu item pointing at the URL in ``path``."""


class Page(Cosplay2Model):
    """A text page of the event site."""

    id: int
    parent_id: int | None = None
    """The folder the page sits in, or ``None`` at the top level."""
    path: str
    """URL slug of the page; the target URL for a ``link``."""
    type: PageType
    title: str
    menu_title: str | None = None
    show_in_menu: bool
    right: EventRole
    """Minimum role required to view the page."""


class PageDetails(Page):
    """A page with its content, as returned by ``pages.get``."""

    event_id: int | None = None
    order: int | None = None
    """Position among the pages of the same folder."""
    source: str | None = None
    """HTML as written in the page editor."""
    content: str | None = None
    """HTML shown on the site."""


class MediaAlbum(Cosplay2Model):
    """A photo album linked to the event."""

    id: int
    event_id: int | None = None
    user_id: int | None = None
    user_title: str | None = None
    """Photographer's name."""
    url: str | None = None
    time_add: UTCDateTime | None = None
    count: int | None = None
    likes: int | None = None
    recalc_time: UTCDateTime | None = None
    recalc_message: str | None = None


class MediaPhoto(Cosplay2Model):
    """A photo from a linked album."""

    id: int | None = None
    photoalbum_id: int | None = None
    user_title: str | None = None
    likes: int | None = None
    src: str | None = None
    photo_url: str | None = None


class MediaData(Cosplay2Model):
    albums: list[MediaAlbum] = Field(default_factory=list)
    photos: list[MediaPhoto] = Field(default_factory=list)


class TicketKind(IntEnum):
    """Kind of voting tickets created by ``tickets.create``."""

    TEST = 1
    WORK = 2


class TicketCreateMode(StrEnum):
    """Whether ``tickets.create`` adds to existing tickets or replaces them."""

    ADD = "add"
    REPLACE = "replace"


class VotingType(StrEnum):
    """Whether a voting call is for live audience voting or test voting."""

    NORMAL = "normal"
    TEST = "test"


class TicketStatistic(Cosplay2Model):
    active_count: int
    test_tickets: list[Any] = Field(default_factory=list)


class VotingStatistics(Cosplay2Model):
    votes_accepted: int
    votes_by_source: list[Any] = Field(default_factory=list)
    active_tickets: int
    topics_activity: list[Any] = Field(default_factory=list)
    prizes: list[Any] = Field(default_factory=list)
    prizes_winners: list[Any] = Field(default_factory=list)
    prize_step: int | None = None
    prize_step_recommend: int | None = None
    votes_to_next_prize: int | None = None
