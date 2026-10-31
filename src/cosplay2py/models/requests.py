import json
from enum import IntEnum, StrEnum
from typing import Annotated, Literal

from pydantic import Field

from cosplay2py._types import EmptyAsNone, LocalDateTime, UTCDateTime
from cosplay2py.models._base import Cosplay2Model
from cosplay2py.models.common import EventRole, RequestStatus, UserBrief
from cosplay2py.models.topics import FieldTemplate, SectionTemplate, Topic


class Request(Cosplay2Model):
    """A request (application) to take part in a topic."""

    id: int
    event_id: int
    topic_id: int
    user_id: int
    number: int
    status: RequestStatus
    creation_time: UTCDateTime | None = None
    update_time: UTCDateTime | None = None
    comment_time: UTCDateTime | None = None
    voting_number: int | None = None
    voting_title: str | None = None
    announcement_title: str | None = None
    diplom_title: str | None = None
    program_title: str | None = None
    win: Literal[1, 2, 3] | None = None
    win_title: str | None = None
    notes: str | None = None
    score: int | None = None
    edit_enabled: bool | None = None
    friendedit_enabled: bool | None = None
    er: EventRole | None = Field(default=None, alias="ER")
    """The current user's role relative to this request."""


class TopicSection(Cosplay2Model):
    """A section of a topic's form (e.g. "Performance", "Participant")."""

    id: int
    topic_id: int
    title: str
    kogo_title: str | None = None
    order: int
    max_repeat: int
    """How many times the section may repeat (e.g. several participants)."""
    visible_to_all: bool
    registration_blanks: bool
    image_section: bool | None = None
    user_section: bool | None = None
    internal_name: Annotated[SectionTemplate | None, EmptyAsNone] = None


class TopicFieldType(StrEnum):
    """Kind of a field in a topic's form."""

    TEXT = "text"
    TEXTAREA = "textarea"
    NUM = "num"
    SELECT = "select"
    CHECKBOX = "checkbox"
    FILE = "file"
    IMAGE = "image"
    LINK = "link"
    PHONE = "phone"
    DURATION = "duration"
    USER = "user"


class TopicField(Cosplay2Model):
    """A field of a topic's form."""

    id: int
    section_id: int
    title: str
    type: TopicFieldType
    order: int
    hint: str | None = None
    data: str | None = None
    """Field configuration; for ``select`` fields, a JSON array of options."""
    visible_to_all: bool
    internal_name: Annotated[FieldTemplate | None, EmptyAsNone] = None
    topic_title: str | None = None
    """Title of the field's section; only sent by ``requests.change_topic``."""

    @property
    def options(self) -> list[str]:
        """Choices of a ``select`` field (empty for other field types)."""
        if not self.data:
            return []
        try:
            parsed = json.loads(self.data)
        except ValueError:
            return []
        return [str(o) for o in parsed] if isinstance(parsed, list) else []


class TopicForm(Cosplay2Model):
    """A topic with its form: the sections and fields a request fills in."""

    topic: Topic
    sections: list[TopicSection] = Field(alias="topic_sections")
    fields: list[TopicField] = Field(alias="topic_fields")
    requests_count: int


class RequestSection(Cosplay2Model):
    """An instance of a ``TopicSection`` filled in a specific request."""

    id: int
    request_id: int
    topic_section_id: int
    order: int


class RequestValue(Cosplay2Model):
    """A value of a ``TopicField`` within a ``RequestSection``."""

    id: int
    request_id: int
    request_section_id: int
    topic_field_id: int
    """The form definition's ``TopicField.id``, shared across requests."""
    value: str | None = None
    """Stored text; image and file fields contain JSON-encoded metadata."""
    update_time: UTCDateTime | None = None
    user_id: int | None = None
    changed: int | None = None


class ImageSize(Cosplay2Model):
    """Dimensions of an uploaded image or one of its resized versions."""

    width: int
    height: int


class ImageValue(Cosplay2Model):
    """An image uploaded to an ``image`` field.

    ``RequestValue.value`` of such a field holds this object as a JSON string.
    """

    filename: int
    """Name of the stored file; it matched the upload time in Unix seconds."""
    original: ImageSize | None = None
    large: ImageSize | None = None
    medium: ImageSize | None = None


class FileValue(Cosplay2Model):
    """A file uploaded to a ``file`` field.

    ``RequestValue.value`` of such a field holds this object as a JSON string.
    """

    filename: str
    filesize: int
    """Size of the stored file in bytes."""
    fileext: str
    """File extension returned by the server; not a closed domain."""


class UploadedFile(Cosplay2Model):
    """A file just stored in a request's form field."""

    id: int
    """``RequestValue.id`` of the stored value."""
    value: FileValue


class UploadedImage(Cosplay2Model):
    """An image just stored in a request's form field."""

    id: int
    """``RequestValue.id`` of the stored value."""
    value: ImageValue


class ValueChange(UserBrief):
    """A saved version of a request's form value and the user who saved it."""

    update_time: UTCDateTime
    value: str | None = None
    """The value as stored, e.g. an ``ImageValue`` JSON string for images."""


class NewRequestSection(Cosplay2Model):
    """A section just added to a request, with the values the site prefilled."""

    id: int
    """``RequestSection.id`` of the new section."""
    values: list[RequestValue] = Field(default_factory=list)
    """Values filled in from the user's profile (e.g. nickname, contacts)."""


class TopicChange(Cosplay2Model):
    """The outcome of moving a request to another topic."""

    message: Literal["ok", "target_not_found"] = "ok"
    """``ok`` once moved; ``target_not_found`` when some sections or fields have no
    counterpart in the target topic and nothing was changed."""
    error_sections: list[TopicSection] = Field(default_factory=list)
    """Sections that would be lost by the move."""
    error_fields: list[TopicField] = Field(default_factory=list)
    """Fields that would be lost by the move."""

    @property
    def moved(self) -> bool:
        """Whether the request now belongs to the target topic."""
        return self.message == "ok"


class RequestScore(Cosplay2Model):
    """An organizer's rating of a request."""

    user_id: int
    user_title: str | None = None
    score: int


class RequestDetails(Cosplay2Model):
    """A request with its topic, form schema and filled-in values."""

    request: Request
    author: UserBrief
    topic: Topic
    sections: list[TopicSection]
    fields: list[TopicField]
    request_sections: list[RequestSection] = Field(alias="reqsections")
    values: list[RequestValue] = Field(alias="reqvalues")
    scores: list[RequestScore] = Field(default_factory=list)
    edit_enabled: bool | None = Field(default=None, alias="editEnabled")
    friendedit_enabled: bool | None = Field(default=None, alias="friendeditEnabled")

    def values_by_field(self) -> dict[str, list[str | None]]:
        """Group values by field ``internal_name`` (falling back to the field title).

        Lists are used because sections may repeat (e.g. one per participant).
        """
        fields = {f.id: f.internal_name or f.title for f in self.fields}
        result: dict[str, list[str | None]] = {}
        for value in self.values:
            name = fields.get(value.topic_field_id, str(value.topic_field_id))
            result.setdefault(name, []).append(value.value)
        return result


class Comment(Cosplay2Model):
    """A comment in a request's discussion, with notification flags."""

    id: int
    user_id: int
    user_title: str | None = None
    content: str
    creation_time: UTCDateTime
    creation_time_local: LocalDateTime | None = Field(
        default=None, alias="creationtime"
    )
    """``creation_time`` as shown on the site, in the event's local time."""
    sms: bool | None = None
    """Whether the comment was also sent by SMS."""
    email: bool | None = None
    """Whether the comment was also sent by email."""
    changed: int | None = None


class RequestUser(UserBrief):
    """A participant profile included in ``requests.get_user``."""

    id: int
    age: int | None = None


class OtherRequest(Cosplay2Model):
    """Another request by the participant in the same event."""

    request_id: int
    status: RequestStatus
    card: str | None = None


class StatusChange(Cosplay2Model):
    """The numbers a request holds after its status was changed."""

    request_number: int | None = None
    voting_number: int | None = None


class FeedbackMark(IntEnum):
    """Rating on organizer feedback about a participant."""

    NEGATIVE = -1
    NEUTRAL = 0
    POSITIVE = 1


class Feedback(Cosplay2Model):
    """Organizer feedback about a participant."""

    id: int | None = None
    create_time: UTCDateTime | None = None
    org_id: int | None = None
    user_id: int | None = None
    event_id: int | None = None
    mark: FeedbackMark | None = None
    info: str | None = None
    event_title: str | None = None
    event_subdomain: str | None = None
    org_title: str | None = None
    org_city: str | None = None
    org_image_update_time: UTCDateTime | None = None


class RequestUserInfo(Cosplay2Model):
    """A request participant plus their other requests in this event."""

    user: RequestUser
    another_requests: list[OtherRequest] = Field(default_factory=list)
    feedbacks: list[Feedback] = Field(default_factory=list)


class RequestSearchResult(Cosplay2Model):
    """A request found by text search in an event."""

    id: int
    topic_id: int
    number: int
    status: RequestStatus
    voting_number: int
    voting_title: str
    user_title: str
    city: str
    card_code: str
