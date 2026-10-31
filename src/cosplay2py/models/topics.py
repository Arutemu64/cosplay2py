from enum import IntEnum, StrEnum
from typing import Annotated, Literal

from cosplay2py._types import EmptyAsNone, LocalDateTime, UTCDateTime
from cosplay2py.models._base import Cosplay2Model
from cosplay2py.models.common import RequestStatus


class CardField(IntEnum):
    """Which generated card field to rebuild with ``topics.generate_card_titles``."""

    VOTING_TITLE = 1
    ANNOUNCEMENT_TITLE = 2
    DIPLOM_TITLE = 3


class TopicCategory(StrEnum):
    """Category of a topic (``globals.topicCategories`` on the site)."""

    SCENE = "scene"
    DEFILE = "defile"
    KARAOKE = "karaoke"
    DANCE = "dance"
    ART = "art"
    PHOTO = "photo"
    VIDEO = "video"
    AMV = "amv"
    GAME = "game"
    VNEKONKURS = "vnekonkurs"
    OTHER = "other"
    NORATING = "norating"


class PublicRequests(StrEnum):
    """Whether a topic's request list is publicly visible."""

    NO = "NO"
    WITHOUT_STATUS = "WITHOUTSTATUS"
    WITH_STATUS = "WITHSTATUS"


class TopicTemplate(StrEnum):
    """Predefined topic form templates used by ``topics.fill_from_template``."""

    STAGE = "stage"
    DEFILE_SOLO = "defile_solo"
    DEFILE_GROUP = "defile_group"
    KARAOKE = "karaoke"
    DANCE = "dance"
    ART = "art"
    PHOTOCOSPLAY = "photocosplay"
    VIDEO = "video"
    AMV = "amv"
    VNEKONKURS = "vnekonkurs"
    SMI = "smi"
    VOLUNTEERS = "volunteers"
    FAIR = "fair"


class SectionTemplate(StrEnum):
    """Predefined section templates (``TopicSection.internal_name``)."""

    COMMON = "common"
    COMMON_SIMPLE = "common_simple"
    COMMON_VIDEO = "common_video"
    IMAGE_MAIN = "image_main"
    AUTHOR = "author"
    AUTHOR_COSPLAY = "author_cosplay"
    AUTHOR_IMAGE = "author_image"
    MEMBERS = "members"
    MEMBERS_COSPLAY = "members_cosplay"
    MEMBERS_ROLE = "members_role"
    HELPERS = "helpers"
    LINKS = "links"
    IMAGE_GALLERY = "image_gallery"
    FILES = "files"


class FieldTemplate(StrEnum):
    """Predefined field templates (``TopicField.internal_name``)."""

    FIO = "fio"
    SECOND_NAME = "second_name"
    FIRST_NAME = "first_name"
    THIRD_NAME = "third_name"
    NAME = "name"
    CITY = "city"
    DURATION = "duration"
    TITLE = "title"
    TEAM = "team"
    ABOUT = "about"
    WISHES = "wishes"
    ABOUT_TEXT = "about_text"
    ABOUT_FAIR = "about_fair"
    IMAGE = "image"
    IMAGE_MAIN = "image_main"
    IMAGE_SELF = "image_self"
    CHARACTER = "character"
    FANDOM = "fandom"
    ROLE = "role"
    USER = "user"
    PHONE = "phone"
    VK = "vk"
    LINK = "link"
    VIDEO_LINK = "video_link"
    UPLOADED_FILE = "uploaded_file"


class Topic(Cosplay2Model):
    """A nomination/category requests are submitted to (e.g. "Solo cosplay")."""

    id: int
    event_id: int
    url_code: str
    card_code: str
    title: str
    category: Annotated[TopicCategory | None, EmptyAsNone] = None
    description: str | None = None
    intro: str | None = None
    order: int
    voting_group: int
    voting_public: bool
    voting_jury: bool
    print_badges: bool
    card_enabled: bool
    default_duration: float
    public_requests: PublicRequests
    time_requests_open: UTCDateTime | None = None
    time_requests_close: UTCDateTime | None = None
    time_addons_close: UTCDateTime | None = None
    time_cards_open: UTCDateTime | None = None
    time_voting_open: UTCDateTime | None = None
    time_voting_close: UTCDateTime | None = None
    card_name_rule: str | None = None
    card_announcement_rule: str | None = None
    card_diplom_rule: str | None = None
    child_topics: str | None = None
    """Grouping display text returned with ``with_group_text=True``."""


class TopicGroupLink(Cosplay2Model):
    """A link between a group topic and one of its child topics."""

    group_topic_id: int
    child_topic_id: int


class TopicGroup(Cosplay2Model):
    """A group topic, all event topics, and its child links."""

    topic: Topic
    topics: list[Topic]
    child_topics: list[TopicGroupLink]


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
    win: Literal[1, 2, 3] | None = None
    win_title: str | None = None
    score: int | None = None


class TopicRequests(Cosplay2Model):
    """A topic and the requests in its request list."""

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
    """A request available to the schedule planner, with its duration."""

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
    score: int | None = None


class PlannerMember(Cosplay2Model):
    """A participant of a request (a request may have several members)."""

    request_id: int
    user_id: int | None = None
    title: str | None = None
    fio: str | None = None
    """Full legal name."""
    city: str | None = None


class PlannerData(Cosplay2Model):
    """Requests and their participants available to the schedule planner."""

    requests: list[PlannerRequest]
    members: list[PlannerMember]
