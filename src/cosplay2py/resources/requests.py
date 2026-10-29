from typing import Any

from cosplay2py._base_client import Endpoint
from cosplay2py.models import (
    Comment,
    Feedback,
    NewRequestSection,
    RequestDetails,
    RequestStatus,
    RequestUserInfo,
    StatusChange,
    TopicChange,
    UploadedImage,
    ValueChange,
)
from cosplay2py.resources._base import AsyncResource, SyncResource


def _get(request_id: int) -> Endpoint[RequestDetails]:
    return Endpoint(
        "POST",
        "/api/requests/get",
        RequestDetails,
        json={"request_id": str(request_id)},
        idempotent=True,
    )


def _get_comments(request_id: int) -> Endpoint[list[Comment]]:
    return Endpoint(
        "POST",
        "/api/requests/get_comments",
        list[Comment],
        key="comments",
        json={"request_id": str(request_id)},
        idempotent=True,
    )


def _get_org_comments(request_id: int) -> Endpoint[list[Comment]]:
    return Endpoint(
        "POST",
        "/api/requests/get_orgcomments",
        list[Comment],
        key="comments",
        json={"request_id": str(request_id)},
        idempotent=True,
    )


def _add_comment(
    request_id: int, comment: str, *, email: bool, sms: bool
) -> Endpoint[Any]:
    return Endpoint(
        "POST",
        "/api/requests/add_comment",
        Any,
        json={
            "request_id": str(request_id),
            "comment": comment,
            "email": email,
            "sms": sms,
        },
        idempotent=False,
    )


def _delete_comment(request_id: int, comment_id: int) -> Endpoint[Any]:
    return Endpoint(
        "POST",
        "/api/requests/del_comment",
        Any,
        json={"request_id": str(request_id), "comment_id": comment_id},
        idempotent=False,
    )


def _save_field(
    request_id: int,
    request_section_id: int,
    topic_field_id: int,
    value: str | int | None,
    value_id: int | None,
) -> Endpoint[int]:
    body: dict[str, Any] = {
        "request_id": request_id,
        "request_section_id": request_section_id,
        "topic_field_id": topic_field_id,
    }
    if value_id is not None:
        body["value_id"] = value_id
    body["data"] = value
    return Endpoint(
        "POST", "/api/requests/save_field", int, key="id", json=body, idempotent=False
    )


def _get_value_history(request_id: int, value_id: int) -> Endpoint[list[ValueChange]]:
    return Endpoint(
        "POST",
        "/api/requests/get_value_history",
        list[ValueChange],
        key="value_history",
        json={"request_id": request_id, "value_id": str(value_id)},
        idempotent=True,
    )


def _upload_image(
    request_id: int,
    request_section_id: int,
    topic_field_id: int,
    image: bytes,
    filename: str,
    value_id: int | None,
) -> Endpoint[UploadedImage]:
    return Endpoint(
        "POST",
        "/api/requests/upload_image",
        UploadedImage,
        data={
            "request_id": str(request_id),
            "request_section_id": str(request_section_id),
            "topic_field_id": str(topic_field_id),
            "value_id": str(value_id or 0),
        },
        files={"uploaded_image": (filename, image)},
        idempotent=False,
    )


def _delete_image(
    request_id: int, request_section_id: int, topic_field_id: int, value_id: int
) -> Endpoint[Any]:
    return Endpoint(
        "POST",
        "/api/requests/delete_image",
        Any,
        json={
            "request_id": request_id,
            "request_section_id": str(request_section_id),
            "topic_field_id": topic_field_id,
            "value_id": str(value_id),
        },
        idempotent=False,
    )


def _get_user(request_id: int, user_id: int) -> Endpoint[RequestUserInfo]:
    return Endpoint(
        "POST",
        "/api/requests/get_user",
        RequestUserInfo,
        json={"user_id": str(user_id), "request_id": request_id},
        idempotent=True,
    )


def _set_status(request_id: int, status: RequestStatus) -> Endpoint[StatusChange]:
    return Endpoint(
        "POST",
        "/api/requests/set_status",
        StatusChange,
        json={"request_id": request_id, "status": status},
        idempotent=False,
    )


def _save_data(request_id: int, field: str, value: Any) -> Endpoint[Any]:
    return Endpoint(
        "POST",
        "/api/requests/save_data",
        Any,
        json={"request_id": request_id, "field": field, "data": value},
        idempotent=False,
    )


def _create(topic_id: int) -> Endpoint[int]:
    return Endpoint(
        "POST",
        "/api/requests/create",
        int,
        key="requestId",
        json={"topic_id": topic_id},
        idempotent=False,
    )


def _create_section(
    request_id: int, topic_section_id: int, order: int
) -> Endpoint[NewRequestSection]:
    return Endpoint(
        "POST",
        "/api/requests/create_reqsection",
        NewRequestSection,
        json={
            "request_id": request_id,
            "topic_section_id": topic_section_id,
            "ord": order,
        },
        idempotent=False,
    )


def _change_topic(
    request_id: int, target_topic_id: int, *, force: bool
) -> Endpoint[TopicChange]:
    body: dict[str, Any] = {
        "request_id": request_id,
        "target_topic_id": target_topic_id,
    }
    if force:
        body["forceflag"] = "force"
    return Endpoint(
        "POST", "/api/requests/change_topic", TopicChange, json=body, idempotent=False
    )


def _generate_card(request_id: int, card: str) -> Endpoint[str]:
    return Endpoint(
        "POST",
        f"/api/requests/generate_card_{card}",
        str,
        key="text",
        json={"request_id": request_id},
        idempotent=True,
    )


def _org_comment(path: str, request_id: int, fields: dict[str, Any]) -> Endpoint[Any]:
    return Endpoint(
        "POST",
        f"/api/requests/{path}",
        Any,
        json={"request_id": str(request_id), **fields},
        idempotent=False,
    )


def _feedbacks(
    action: str, request_id: int, user_id: int, fields: dict[str, Any] | None = None
) -> Endpoint[list[Feedback]]:
    return Endpoint(
        "POST",
        f"/api/requests/feedbacks_{action}",
        list[Feedback],
        key="feedbacks",
        json={"request_id": request_id, "user_id": user_id, **(fields or {})},
        idempotent=action == "get",
    )


class Requests(SyncResource):
    """Requests (applications to take part in a topic)."""

    def get(self, request_id: int) -> RequestDetails:
        """A request with its topic, form schema and filled-in values."""
        return self._request(_get(request_id))

    def get_comments(self, request_id: int) -> list[Comment]:
        """Comments visible to the request's author."""
        return self._request(_get_comments(request_id))

    def get_org_comments(self, request_id: int) -> list[Comment]:
        """Internal comments visible to organizers only."""
        return self._request(_get_org_comments(request_id))

    def add_comment(
        self, request_id: int, comment: str, *, email: bool = True, sms: bool = False
    ) -> None:
        """Post a comment visible to the request's author.

        :param email: also notify the author by email.
        :param sms: also notify the author by SMS.
        """
        self._request(_add_comment(request_id, comment, email=email, sms=sms))

    def delete_comment(self, request_id: int, comment_id: int) -> None:
        """Delete a comment of a request (``Comment.id``)."""
        self._request(_delete_comment(request_id, comment_id))

    def save_field(
        self,
        request_id: int,
        request_section_id: int,
        topic_field_id: int,
        value: str | int | None,
        *,
        value_id: int | None = None,
    ) -> int:
        """Set a form field of a request and return the id of the stored value.

        The ids come from ``RequestDetails``: ``RequestSection.id`` and
        ``TopicField.id``.

        :param value: the new value, as the site stores it: a string, the user's id
            for a ``user`` field (see ``users.search``), or ``None`` to clear it.
            Use ``upload_image`` for ``image`` fields.
        :param value_id: ``RequestValue.id`` of the value being replaced, if the
            field already has one.
        """
        return self._request(
            _save_field(request_id, request_section_id, topic_field_id, value, value_id)
        )

    def get_value_history(self, request_id: int, value_id: int) -> list[ValueChange]:
        """Saved versions of a form value (``RequestValue.id``) and who saved them."""
        return self._request(_get_value_history(request_id, value_id))

    def upload_image(
        self,
        request_id: int,
        request_section_id: int,
        topic_field_id: int,
        image: bytes,
        filename: str,
        *,
        value_id: int | None = None,
    ) -> UploadedImage:
        """Upload an image into an ``image`` field of a request.

        :param image: the file's contents.
        :param filename: the file's name; its extension sets the content type.
        :param value_id: ``RequestValue.id`` of the field's current value, if any;
            the site sends ``0`` for an empty field.
        """
        return self._request(
            _upload_image(
                request_id,
                request_section_id,
                topic_field_id,
                image,
                filename,
                value_id,
            )
        )

    def delete_image(
        self,
        request_id: int,
        request_section_id: int,
        topic_field_id: int,
        value_id: int,
    ) -> None:
        """Remove the image stored as ``value_id`` from an ``image`` field."""
        self._request(
            _delete_image(request_id, request_section_id, topic_field_id, value_id)
        )

    def get_user(self, request_id: int, user_id: int) -> RequestUserInfo:
        """A participant of the request and their other requests in this event."""
        return self._request(_get_user(request_id, user_id))

    def set_status(self, request_id: int, status: RequestStatus) -> StatusChange:
        """Move a request to ``status`` and return its request and voting numbers."""
        return self._request(_set_status(request_id, status))

    def save_data(self, request_id: int, field: str, value: Any) -> None:
        """Set an organizer field of a request.

        :param field: the ``Request`` attribute to set, e.g. ``voting_number``,
            ``win``, ``notes``, ``announcement_title`` or ``diplom_title``.
        :param value: the new value; ``win`` only accepts ``1``, ``2`` or ``3``.
        """
        self._request(_save_data(request_id, field, value))

    def create(self, topic_id: int) -> int:
        """Create an empty request in a topic and return its id.

        The site then adds one section per ``TopicSection`` with ``create_section``.
        """
        return self._request(_create(topic_id))

    def create_section(
        self, request_id: int, topic_section_id: int, *, order: int = 0
    ) -> NewRequestSection:
        """Add a section of the request's topic to a request.

        :param topic_section_id: ``TopicSection.id`` of the section to add.
        :param order: sort position among repeats of the section; the site sends
            ``0``.
        """
        return self._request(_create_section(request_id, topic_section_id, order))

    def change_topic(
        self, request_id: int, target_topic_id: int, *, force: bool = False
    ) -> TopicChange:
        """Move a request to another topic of the event.

        Without ``force`` nothing changes if the target topic lacks some of the
        request's sections or fields; they are listed in the result instead.

        :param force: move anyway, dropping the sections and fields that don't fit.
        """
        return self._request(_change_topic(request_id, target_topic_id, force=force))

    def generate_card_title(self, request_id: int) -> str:
        """The request's card title, built from the topic's ``card_name_rule``."""
        return self._request(_generate_card(request_id, "title"))

    def generate_card_announcement(self, request_id: int) -> str:
        """The request's announcement text, from ``card_announcement_rule``."""
        return self._request(_generate_card(request_id, "announcement"))

    def generate_card_diplom(self, request_id: int) -> str:
        """The request's diploma text, built from the topic's ``card_diplom_rule``.

        Nothing is stored; save it with ``save_data(id, "diplom_title", text)``.
        """
        return self._request(_generate_card(request_id, "diplom"))

    def add_org_comment(self, request_id: int, comment: str) -> None:
        """Post an internal organizer comment."""
        self._request(_org_comment("add_orgcomment", request_id, {"comment": comment}))

    def delete_org_comment(self, request_id: int, comment_id: int) -> None:
        """Delete an internal organizer comment."""
        self._request(
            _org_comment("del_orgcomment", request_id, {"comment_id": comment_id})
        )

    def get_feedbacks(self, request_id: int, user_id: int) -> list[Feedback]:
        """Organizer feedback about a request participant."""
        return self._request(_feedbacks("get", request_id, user_id))

    def add_feedback(
        self, request_id: int, user_id: int, mark: int, info: str
    ) -> list[Feedback]:
        """Add feedback and return the updated feedback list.

        :param mark: negative (-1), neutral (0), or positive (1).
        """
        return self._request(
            _feedbacks("add", request_id, user_id, {"mark": str(mark), "info": info})
        )

    def delete_feedback(
        self, request_id: int, user_id: int, feedback_id: int
    ) -> list[Feedback]:
        """Delete feedback and return the updated feedback list."""
        return self._request(
            _feedbacks("del", request_id, user_id, {"feedback_id": feedback_id})
        )


class AsyncRequests(AsyncResource):
    """Requests (applications to take part in a topic)."""

    async def get(self, request_id: int) -> RequestDetails:
        """A request with its topic, form schema and filled-in values."""
        return await self._request(_get(request_id))

    async def get_comments(self, request_id: int) -> list[Comment]:
        """Comments visible to the request's author."""
        return await self._request(_get_comments(request_id))

    async def get_org_comments(self, request_id: int) -> list[Comment]:
        """Internal comments visible to organizers only."""
        return await self._request(_get_org_comments(request_id))

    async def add_comment(
        self, request_id: int, comment: str, *, email: bool = True, sms: bool = False
    ) -> None:
        """Post a comment visible to the request's author.

        :param email: also notify the author by email.
        :param sms: also notify the author by SMS.
        """
        await self._request(_add_comment(request_id, comment, email=email, sms=sms))

    async def delete_comment(self, request_id: int, comment_id: int) -> None:
        """Delete a comment of a request (``Comment.id``)."""
        await self._request(_delete_comment(request_id, comment_id))

    async def save_field(
        self,
        request_id: int,
        request_section_id: int,
        topic_field_id: int,
        value: str | int | None,
        *,
        value_id: int | None = None,
    ) -> int:
        """Set a form field of a request and return the id of the stored value.

        The ids come from ``RequestDetails``: ``RequestSection.id`` and
        ``TopicField.id``.

        :param value: the new value, as the site stores it: a string, the user's id
            for a ``user`` field (see ``users.search``), or ``None`` to clear it.
            Use ``upload_image`` for ``image`` fields.
        :param value_id: ``RequestValue.id`` of the value being replaced, if the
            field already has one.
        """
        return await self._request(
            _save_field(request_id, request_section_id, topic_field_id, value, value_id)
        )

    async def get_value_history(
        self, request_id: int, value_id: int
    ) -> list[ValueChange]:
        """Saved versions of a form value (``RequestValue.id``) and who saved them."""
        return await self._request(_get_value_history(request_id, value_id))

    async def upload_image(
        self,
        request_id: int,
        request_section_id: int,
        topic_field_id: int,
        image: bytes,
        filename: str,
        *,
        value_id: int | None = None,
    ) -> UploadedImage:
        """Upload an image into an ``image`` field of a request.

        :param image: the file's contents.
        :param filename: the file's name; its extension sets the content type.
        :param value_id: ``RequestValue.id`` of the field's current value, if any;
            the site sends ``0`` for an empty field.
        """
        return await self._request(
            _upload_image(
                request_id,
                request_section_id,
                topic_field_id,
                image,
                filename,
                value_id,
            )
        )

    async def delete_image(
        self,
        request_id: int,
        request_section_id: int,
        topic_field_id: int,
        value_id: int,
    ) -> None:
        """Remove the image stored as ``value_id`` from an ``image`` field."""
        await self._request(
            _delete_image(request_id, request_section_id, topic_field_id, value_id)
        )

    async def get_user(self, request_id: int, user_id: int) -> RequestUserInfo:
        """A participant of the request and their other requests in this event."""
        return await self._request(_get_user(request_id, user_id))

    async def set_status(self, request_id: int, status: RequestStatus) -> StatusChange:
        """Move a request to ``status`` and return its request and voting numbers."""
        return await self._request(_set_status(request_id, status))

    async def save_data(self, request_id: int, field: str, value: Any) -> None:
        """Set an organizer field of a request.

        :param field: the ``Request`` attribute to set, e.g. ``voting_number``,
            ``win``, ``notes``, ``announcement_title`` or ``diplom_title``.
        :param value: the new value; ``win`` only accepts ``1``, ``2`` or ``3``.
        """
        await self._request(_save_data(request_id, field, value))

    async def create(self, topic_id: int) -> int:
        """Create an empty request in a topic and return its id.

        The site then adds one section per ``TopicSection`` with ``create_section``.
        """
        return await self._request(_create(topic_id))

    async def create_section(
        self, request_id: int, topic_section_id: int, *, order: int = 0
    ) -> NewRequestSection:
        """Add a section of the request's topic to a request.

        :param topic_section_id: ``TopicSection.id`` of the section to add.
        :param order: sort position among repeats of the section; the site sends
            ``0``.
        """
        return await self._request(_create_section(request_id, topic_section_id, order))

    async def change_topic(
        self, request_id: int, target_topic_id: int, *, force: bool = False
    ) -> TopicChange:
        """Move a request to another topic of the event.

        Without ``force`` nothing changes if the target topic lacks some of the
        request's sections or fields; they are listed in the result instead.

        :param force: move anyway, dropping the sections and fields that don't fit.
        """
        return await self._request(
            _change_topic(request_id, target_topic_id, force=force)
        )

    async def generate_card_title(self, request_id: int) -> str:
        """The request's card title, built from the topic's ``card_name_rule``."""
        return await self._request(_generate_card(request_id, "title"))

    async def generate_card_announcement(self, request_id: int) -> str:
        """The request's announcement text, from ``card_announcement_rule``."""
        return await self._request(_generate_card(request_id, "announcement"))

    async def generate_card_diplom(self, request_id: int) -> str:
        """The request's diploma text, built from the topic's ``card_diplom_rule``.

        Nothing is stored; save it with ``save_data(id, "diplom_title", text)``.
        """
        return await self._request(_generate_card(request_id, "diplom"))

    async def add_org_comment(self, request_id: int, comment: str) -> None:
        """Post an internal organizer comment."""
        await self._request(
            _org_comment("add_orgcomment", request_id, {"comment": comment})
        )

    async def delete_org_comment(self, request_id: int, comment_id: int) -> None:
        """Delete an internal organizer comment."""
        await self._request(
            _org_comment("del_orgcomment", request_id, {"comment_id": comment_id})
        )

    async def get_feedbacks(self, request_id: int, user_id: int) -> list[Feedback]:
        """Organizer feedback about a request participant."""
        return await self._request(_feedbacks("get", request_id, user_id))

    async def add_feedback(
        self, request_id: int, user_id: int, mark: int, info: str
    ) -> list[Feedback]:
        """Add feedback and return the updated feedback list.

        :param mark: negative (-1), neutral (0), or positive (1).
        """
        return await self._request(
            _feedbacks("add", request_id, user_id, {"mark": str(mark), "info": info})
        )

    async def delete_feedback(
        self, request_id: int, user_id: int, feedback_id: int
    ) -> list[Feedback]:
        """Delete feedback and return the updated feedback list."""
        return await self._request(
            _feedbacks("del", request_id, user_id, {"feedback_id": feedback_id})
        )
