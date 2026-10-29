"""Models for the smaller resources: pages, media, e-tickets and voting tickets."""

from enum import StrEnum
from typing import Any

from pydantic import Field

from cosplay2py.models._base import Cosplay2Model


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
    type: str
    title: str
    menu_title: str | None = None
    show_in_menu: bool
    right: int
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


class MediaData(Cosplay2Model):
    albums: list[Any] = Field(default_factory=list)
    photos: list[Any] = Field(default_factory=list)


class PayMethods(Cosplay2Model):
    yookassa_allowed: bool


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
