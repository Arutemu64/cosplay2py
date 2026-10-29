from decimal import Decimal
from enum import StrEnum
from typing import Annotated, Any

from pydantic import BeforeValidator, Field

from cosplay2py._types import JsonEncoded, LocalDateTime, UTCDateTime
from cosplay2py.models._base import Cosplay2Model
from cosplay2py.models.common import RequestStatus, UserBrief
from cosplay2py.models.topics import PlannerMember


class EventDesign(Cosplay2Model):
    panel_background_color: str | None = None
    panel_text_color: str | None = None
    panel_small_text_color: str | None = None
    panel_buttons_color: str | None = None
    panel_buttons_active_color: str | None = None
    back_background_color: str | None = None
    userpanel_background_color: str | None = None
    userpanel_text_color: str | None = None
    header_height: str | None = None
    header_background_color: str | None = None
    content_background_color: str | None = None
    content_text_color: str | None = None
    content_link_color: str | None = None
    content_opacity: float | None = None
    custom_css: str | None = None
    wid: str | None = None
    """The site's per-tab pool id, stored along with the design when it was saved;
    meaningless."""


class PlanMember(PlannerMember):
    uid: str | None = None
    distance: int | None = None
    intersections: list[Any] = Field(default_factory=list)
    """Other plan entries this member overlaps with."""
    hash_key: str | None = Field(default=None, alias="$$hashKey")
    """AngularJS bookkeeping saved along with the plan; meaningless."""


class PlanNode(Cosplay2Model):
    """A node of the schedule tree: day -> place -> event (performance block)."""

    type: str
    """``"day"``, ``"place"``, ``"topic"``, ``"request"``, ``"event"`` or ``"break"``."""
    title: str | None = None
    uid: str | None = None
    nodes: list["PlanNode"] = Field(default_factory=list)
    date_start: UTCDateTime | None = None
    time_start: UTCDateTime | None = None
    time_end: UTCDateTime | None = None
    request_length: float | None = None
    """Duration in minutes."""
    sum_count: int | None = None
    sum_length: float | None = None
    approved_count: int | None = None
    approved_length: float | None = None
    other_count: int | None = None
    other_length: float | None = None
    # Topic and request nodes:
    topic_id: int | None = None
    distance: int | None = None
    # Topic nodes:
    collapsed: bool | None = None
    total_requests_count: int | None = None
    # Request nodes:
    request_id: int | None = None
    card_code: str | None = None
    status: RequestStatus | None = None
    request_length_text: str | None = None
    """``request_length`` formatted for display, e.g. ``"10 мин."``."""
    members: list[PlanMember] = Field(default_factory=list)


Plan = Annotated[list[PlanNode], JsonEncoded]


class Event(Cosplay2Model):
    """Event (festival) settings."""

    id: int
    event_type_id: int
    title: str
    short_title: str | None = None
    description: str | None = None
    subdomain: str
    domain: str | None = None
    """Custom domain, if the event is served from one."""
    user_id: int
    """The main organizer."""
    city: str | None = None
    geo_id: int | None = None
    region: str | None = None
    country: str | None = None
    start_time: LocalDateTime | None = None
    end_time: LocalDateTime | None = None
    timezone: str
    status: str
    event_status: str | None = None
    """``"past"``, ``"future"``, ..."""
    design: Annotated[EventDesign | None, JsonEncoded] = None
    plan: Annotated[list[PlanNode] | None, JsonEncoded] = None
    ad: int | None = None
    sms_price: Decimal | None = None
    prize_step: int | None = None
    files_url: str | None = None


class EventState(Cosplay2Model):
    """Request counters for the whole event."""

    topics_count: int
    requests_pending: int
    requests_waiting: int
    requests_materials: int
    requests_review: int
    requests_approved: int
    requests_disapproved: int
    tickets_voting: int
    sms_cost: Decimal | None = None

    @property
    def requests_total(self) -> int:
        return (
            self.requests_pending
            + self.requests_waiting
            + self.requests_materials
            + self.requests_review
            + self.requests_approved
            + self.requests_disapproved
        )


class TopicState(Cosplay2Model):
    """Topic deadlines, formatted in the event's timezone."""

    id: int
    title: str
    voting_group: int
    voting_public: bool
    voting_jury: bool
    card_enabled: bool
    time_requests_open: LocalDateTime | None = None
    time_requests_close: LocalDateTime | None = None
    time_addons_close: LocalDateTime | None = None
    time_cards_open: LocalDateTime | None = None
    time_voting_open: LocalDateTime | None = None
    time_voting_close: LocalDateTime | None = None


class Deadline(StrEnum):
    """The topic dates ("гейты") that ``events.set_deadline()`` can change."""

    REQUESTS_OPEN = "time_requests_open"
    REQUESTS_CLOSE = "time_requests_close"
    ADDONS_CLOSE = "time_addons_close"
    CARDS_OPEN = "time_cards_open"
    VOTING_OPEN = "time_voting_open"
    VOTING_CLOSE = "time_voting_close"


class TopicStatistic(Cosplay2Model):
    """Request counters for one topic."""

    id: int
    title: str
    card_code: str
    url_code: str
    count_pending: int
    count_waiting: int
    count_materials: int
    count_review: int
    count_approved: int
    count_disapproved: int


class ButtonState(Cosplay2Model):
    state: int


class ButtonsState(Cosplay2Model):
    """Availability of the main event sections (registration, cards, voting, ...)."""

    new_request: ButtonState
    cards: ButtonState
    voting: ButtonState
    etickets: ButtonState
    media: ButtonState
    requestlist: ButtonState


class Curator(UserBrief):
    topic_id: int
    card_code: str
    topic_title: str


class EventStaff(Cosplay2Model):
    orgs: list[UserBrief]
    curators: list[Curator]
    mainorg: UserBrief


class EventBrief(Cosplay2Model):
    """An event as found by ``events.search``."""

    id: int
    title: str


class DomainCheck(Cosplay2Model):
    valid: bool
    expected_ip: str | None = None
    expected_ips: list[str] = Field(default_factory=list)
    domain_ips: list[str] = Field(default_factory=list)


class BlankId(StrEnum):
    """Printable reports ("бланки") available to organizers."""

    WINNERS = "winners"
    REG_TOPICS = "reg_topics"
    REG_ALPHABET = "reg_alphabet"
    GEO = "geo"
    TECH_HELPERS = "tech_helpers"
    FOR_PROGRAMM = "for_programm"
    ANNOUNCEMENT = "announcement"
    JURY = "jury"
    BADGES = "badges"
    FOR_SIGNING_PRIZES = "for_signing_prizes"


class Blank(Cosplay2Model):
    """A rendered printable report."""

    html: str
    blank_title: str
    file_title: str


class RegistrationRequest(Cosplay2Model):
    request_id: int
    number: int
    """The request's number within its topic."""


class RegistrationParticipant(Cosplay2Model):
    """A row of a registration table: one person and their requests."""

    user_id: int
    display_name: str
    fio: str
    """Full name, as entered by the participant (``"-"`` when left out)."""
    city: str | None = None
    phone: str | None = None
    requests: list[RegistrationRequest] = Field(default_factory=list)


class AlphabetParticipant(RegistrationParticipant):
    onscene_count: int
    offscene_count: int


class TopicParticipants(Cosplay2Model):
    topic_id: int
    topic_name: str
    # null when nobody has registered in the topic.
    participants: Annotated[
        list[RegistrationParticipant], BeforeValidator(lambda v: v or [])
    ] = Field(default_factory=list)


class TopicsRegistration(Cosplay2Model):
    """The ``reg_topics`` report: participants grouped by topic."""

    title: str
    data: list[TopicParticipants]


class AlphabetRegistration(Cosplay2Model):
    """The ``reg_alphabet`` report: every participant once, in alphabetical order."""

    title: str
    data: list[AlphabetParticipant]
