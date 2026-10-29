from typing import Any

from cosplay2py._types import LocalDateTime, UTCDateTime
from cosplay2py.models._base import Cosplay2Model
from cosplay2py.models.common import RequestStatus


class Topic(Cosplay2Model):
    """A nomination/category requests are submitted to (e.g. "Solo cosplay")."""

    id: int
    event_id: int
    url_code: str
    card_code: str
    title: str
    category: str | None = None
    description: str | None = None
    intro: str | None = None
    order: int
    voting_group: int
    voting_public: bool
    voting_jury: bool
    print_badges: bool
    card_enabled: bool
    default_duration: float
    public_requests: str
    time_requests_open: UTCDateTime | None = None
    time_requests_close: UTCDateTime | None = None
    time_addons_close: UTCDateTime | None = None
    time_cards_open: UTCDateTime | None = None
    time_voting_open: UTCDateTime | None = None
    time_voting_close: UTCDateTime | None = None
    card_name_rule: str | None = None
    card_announcement_rule: str | None = None
    card_diplom_rule: str | None = None
    child_topics: list[Any] | None = None
    """Only present when listing with ``with_group_text=True``."""


class TopicRequest(Cosplay2Model):
    """A request as shown in a topic's request list."""

    id: int
    number: int
    status: RequestStatus
    user_id: int
    user_title: str | None = None
    city: str | None = None
    image_update_time: UTCDateTime | None = None
    voting_number: int | None = None
    voting_title: str | None = None
    update_time: str | None = None
    """Display-formatted, without a year (e.g. ``"10 Aug 16:05"``)."""
    comment_time: UTCDateTime | None = None
    notes: str | None = None
    new_comments: int | None = None
    new_updates: int | None = None
    win: Any = None
    win_title: str | None = None
    score: Any = None


class TopicRequests(Cosplay2Model):
    topic: Topic
    requests: list[TopicRequest]


class EventRequest(Cosplay2Model):
    """A request as shown in the event-wide request list."""

    id: int
    topic_id: int
    number: int
    status: RequestStatus
    user_id: int
    user_title: str | None = None
    update_time: LocalDateTime | None = None
    comment_time: UTCDateTime | None = None
    image_update_time: UTCDateTime | None = None
    voting_number: int | None = None
    voting_title: str | None = None
    new_comments: int | None = None
    new_updates: int | None = None


class PlannerRequest(Cosplay2Model):
    id: int
    topic_id: int
    number: int
    status: RequestStatus
    user_id: int
    user_title: str | None = None
    image_update_time: UTCDateTime | None = None
    voting_number: int | None = None
    voting_title: str | None = None
    duration: float | None = None
    """Performance duration in minutes."""
    score: Any = None


class PlannerMember(Cosplay2Model):
    """A participant of a request (a request may have several members)."""

    request_id: int
    user_id: int | None = None
    title: str | None = None
    fio: str | None = None
    """Full legal name."""
    city: str | None = None


class PlannerData(Cosplay2Model):
    requests: list[PlannerRequest]
    members: list[PlannerMember]
