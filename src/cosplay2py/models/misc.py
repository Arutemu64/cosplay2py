"""Models for the smaller resources: pages, media, e-tickets and voting tickets."""

from enum import IntEnum, StrEnum
from typing import Any

from pydantic import Field

from cosplay2py._types import UTCDateTime
from cosplay2py.models._base import Cosplay2Model
from cosplay2py.models.common import EventRole, RequestStatus
from cosplay2py.models.requests import (
    ImageValue,
    Request,
    RequestSection,
    RequestValue,
    TopicField,
    TopicSection,
)
from cosplay2py.models.topics import PublicRequests, Topic


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
    """Linked photo albums and photos returned by the event media resource."""

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
    """Active voting ticket count and test ticket data."""

    active_count: int
    test_tickets: list[Any] = Field(default_factory=list)


class VotingStatistics(Cosplay2Model):
    """Voting totals, ticket activity and prize draw statistics."""

    votes_accepted: int
    votes_by_source: list[Any] = Field(default_factory=list)
    active_tickets: int
    topics_activity: list[Any] = Field(default_factory=list)
    prizes: list[Any] = Field(default_factory=list)
    prizes_winners: list[Any] = Field(default_factory=list)
    prize_step: int | None = None
    prize_step_recommend: int | None = None
    votes_to_next_prize: int | None = None


class CardTopic(Cosplay2Model):
    """A topic in the participant showcase."""

    id: int
    url_code: str
    card_code: str
    title: str


class CardRequest(Cosplay2Model):
    """A request in the participant showcase."""

    id: int
    topic_id: int
    voting_number: int | None = None
    voting_title: str | None = None
    win: int | None = None
    user_id: int | None = None
    image: ImageValue | None = None


class TopicsAndCards(Cosplay2Model):
    """Topics and participant cards shown on the event site."""

    topics: list[CardTopic]
    requests: list[CardRequest]


class PublicRequest(Cosplay2Model):
    """A submitted request in the public request list."""

    id: int
    topic_id: int
    user_id: int
    number: int
    status: RequestStatus
    public_requests: PublicRequests
    """The topic's public request visibility setting."""
    voting_number: int | None = None
    voting_title: str | None = None


class TopicsAndRequests(Cosplay2Model):
    """Topics and submitted requests shown on the public request list."""

    topics: list[CardTopic]
    requests: list[PublicRequest]


class CardBadge(Cosplay2Model):
    """A participant badge attached to a request section."""

    request_section_id: int
    card: str
    another_requests: str | None = None
    """Display text for the participant's other requests."""


class CardUser(Cosplay2Model):
    """A user embedded in a participant card, identified by ``id``."""

    id: int
    title: str | None = None
    image_update_time: UTCDateTime | None = None


class CardDetails(Cosplay2Model):
    """A participant card with its form, values, badges and users."""

    request: Request
    topic: Topic
    sections: list[TopicSection]
    fields: list[TopicField]
    request_sections: list[RequestSection] = Field(alias="reqsections")
    values: list[RequestValue] = Field(alias="reqvalues")
    badges: list[CardBadge]
    users: list[CardUser]


class PublicRequestDetails(Cosplay2Model):
    """A public request with its form, values and users."""

    request: Request
    topic: Topic
    sections: list[TopicSection]
    fields: list[TopicField]
    request_sections: list[RequestSection] = Field(alias="reqsections")
    values: list[RequestValue] = Field(alias="reqvalues")
    users: list[CardUser]
