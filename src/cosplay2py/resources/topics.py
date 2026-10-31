from typing import Any

from cosplay2py._base_client import Endpoint
from cosplay2py.models import (
    CardField,
    EventRequest,
    FieldTemplate,
    PlannerData,
    SectionTemplate,
    Topic,
    TopicForm,
    TopicGroup,
    TopicGroupLink,
    TopicRequest,
    TopicRequests,
    TopicTemplate,
)
from cosplay2py.resources._base import AsyncResource, SyncResource

_GET_ALL_REQUESTS = Endpoint[list[EventRequest]](
    "POST", "/api/topics/get_all_requests", list[EventRequest], idempotent=True
)
_GET_FOR_PLANNER = Endpoint[PlannerData](
    "GET", "/api/topics/get_req_for_planner", PlannerData, idempotent=True
)


def _get_list(with_group_text: bool, event_id: int | None) -> Endpoint[list[Topic]]:
    body: dict[str, Any] = {}
    if with_group_text:
        body["with_group_text"] = True
    if event_id is not None:
        body["event_id"] = event_id
    if body:
        return Endpoint(
            "POST", "/api/topics/get_list", list[Topic], json=body, idempotent=True
        )
    return Endpoint("GET", "/api/topics/get_list", list[Topic], idempotent=True)


def _get_requests(topic: int | str) -> Endpoint[TopicRequests]:
    body = {"topic_id": topic} if isinstance(topic, int) else {"topic_url_code": topic}
    return Endpoint(
        "POST", "/api/topics/get_requests", TopicRequests, json=body, idempotent=True
    )


def _get_form(url_code: str) -> Endpoint[TopicForm]:
    return Endpoint(
        "POST",
        "/api/topics/get_with_fields",
        TopicForm,
        json={"topic_url_code": url_code},
        idempotent=True,
    )


def _get_with_groups(url_code: str) -> Endpoint[TopicGroup]:
    return Endpoint(
        "POST",
        "/api/topics/get_with_groups",
        TopicGroup,
        json={"topic_url_code": url_code},
        idempotent=True,
    )


def _child_topic(
    action: str, url_code: str, child_topic_id: int
) -> Endpoint[list[TopicGroupLink]]:
    return Endpoint(
        "POST",
        f"/api/topics/{action}_child_topic",
        list[TopicGroupLink],
        key="child_topics",
        json={"topic_url_code": url_code, "child_topic_id": child_topic_id},
        idempotent=False,
    )


def _generate_card_titles(
    topic_id: int, field_num: CardField
) -> Endpoint[list[TopicRequest]]:
    if isinstance(field_num, bool):
        raise TypeError(f"{field_num!r} is not a valid CardField")
    field_num = CardField(field_num)
    return Endpoint(
        "POST",
        "/api/topics/generate_cards_title",
        list[TopicRequest],
        key="requests",
        json={"topic_id": topic_id, "field_num": int(field_num)},
        idempotent=False,
    )


def _write(path: str, body: dict[str, Any]) -> Endpoint[Any]:
    """An organizer action that only answers ``{"message": "ok"}``."""
    return Endpoint("POST", f"/api/topics/{path}", Any, json=body, idempotent=False)


class Topics(SyncResource):
    """Topics (nominations) of the event."""

    def get_list(
        self, *, with_group_text: bool = False, event_id: int | None = None
    ) -> list[Topic]:
        """All topics of the event.

        :param with_group_text: Also return grouping info (``Topic.child_topics``).
        :param event_id: List the topics of another event instead, e.g. to pick a
            source for ``fill_from_topic``.
        """
        return self._request(_get_list(with_group_text, event_id))

    def get_requests(self, topic: int | str) -> TopicRequests:
        """A topic and its requests.

        :param topic: ``Topic.id`` or ``Topic.url_code`` (e.g. ``"solo_vostok"``).
        """
        return self._request(_get_requests(topic))

    def get_all_requests(self) -> list[EventRequest]:
        """Every request of the event, across all topics."""
        return self._request(_GET_ALL_REQUESTS)

    def get_requests_for_planner(self) -> PlannerData:
        """Every request of the event with durations and members, for scheduling."""
        return self._request(_GET_FOR_PLANNER)

    def get_form(self, url_code: str) -> TopicForm:
        """A topic with the sections and fields of its form.

        :param url_code: ``Topic.url_code``.
        """
        return self._request(_get_form(url_code))

    def create(self, *, voting_group: int = 0) -> None:
        """Create an empty topic at the end of the list.

        The response carries no id: the new topic has the url code ``"new"``, so
        fetch it with ``get_form("new")``.

        :param voting_group: ``Topic.voting_group`` of the new topic.
        """
        self._request(_write("add", {"voting_group": voting_group}))

    def delete(self, topic_id: int) -> None:
        """Delete a topic."""
        self._request(_write("topic_delete", {"topic_id": topic_id}))

    def reorder(self, topic_id: int, new_index: int) -> None:
        """Move a topic to another position in the list.

        :param new_index: zero-based position among the event's topics.
        """
        self._request(
            _write("topic_reorder", {"topic_id": topic_id, "new_index": new_index})
        )

    def fill_from_template(self, topic_id: int, template: TopicTemplate) -> None:
        """Replace a topic's form with a built-in template.

        :param template: template name, e.g. ``TopicTemplate.ART``.
        """
        template = TopicTemplate(template)
        self._request(
            _write(
                "fill_from_template", {"topic_id": topic_id, "internal_name": template}
            )
        )

    def fill_from_topic(self, topic_id: int, src_topic_id: int) -> None:
        """Replace a topic's form (and card rules) with a copy of another topic's.

        :param src_topic_id: ``Topic.id`` to copy from, possibly of another event
            (see ``get_list(event_id=)``).
        """
        self._request(
            _write(
                "fill_from_topic", {"topic_id": topic_id, "src_topic_id": src_topic_id}
            )
        )

    def add_section(self, topic_id: int, template: SectionTemplate) -> None:
        """Add a built-in section to a topic's form.

        :param template: section template name, e.g. ``SectionTemplate.COMMON``.
        """
        template = SectionTemplate(template)
        self._request(
            _write("section_add", {"topic_id": topic_id, "internal_name": template})
        )

    def save_section(
        self, topic_id: int, section_id: int, field: str, value: Any
    ) -> None:
        """Set an attribute of a form section.

        :param section_id: ``TopicSection.id``.
        :param field: the ``TopicSection`` attribute to set, e.g. ``title``,
            ``kogo_title``, ``max_repeat`` or ``internal_name``.
        """
        self._request(
            _write(
                "save_section_field",
                {
                    "topic_id": topic_id,
                    "section_id": section_id,
                    "field": field,
                    "data": value,
                },
            )
        )

    def delete_section(self, topic_id: int, section_id: int) -> None:
        """Remove a section, with its fields, from a topic's form."""
        self._request(
            _write("section_delete", {"topic_id": topic_id, "section_id": section_id})
        )

    def add_field(
        self, topic_id: int, section_id: int, template: FieldTemplate
    ) -> None:
        """Add a built-in field to a section of a topic's form.

        :param section_id: ``TopicSection.id``.
        :param template: field template name, e.g. ``FieldTemplate.FIRST_NAME``.
        """
        template = FieldTemplate(template)
        self._request(
            _write(
                "field_add",
                {
                    "topic_id": topic_id,
                    "section_id": section_id,
                    "internal_name": template,
                },
            )
        )

    def delete_field(self, topic_id: int, section_id: int, field_id: int) -> None:
        """Delete a form field."""
        self._request(
            _write(
                "field_delete",
                {"topic_id": topic_id, "section_id": section_id, "field_id": field_id},
            )
        )

    def save_field(
        self, topic_id: int, section_id: int, field_id: int, field: str, value: Any
    ) -> None:
        """Set a form field attribute."""
        self._request(
            _write(
                "save_field_field",
                {
                    "topic_id": topic_id,
                    "section_id": section_id,
                    "field_id": field_id,
                    "field": field,
                    "data": value,
                },
            )
        )

    def save_topic(self, topic_id: int, field: str, value: Any) -> None:
        """Set a topic attribute."""
        self._request(
            _write(
                "save_topic_field",
                {"topic_id": topic_id, "field": field, "data": value},
            )
        )

    def reorder_section(self, topic_id: int, section_id: int, new_index: int) -> None:
        """Move a form section to a new position."""
        self._request(
            _write(
                "section_reorder",
                {
                    "topic_id": topic_id,
                    "section_id": section_id,
                    "new_index": new_index,
                },
            )
        )

    def reorder_field(
        self,
        topic_id: int,
        field_id: int,
        new_index: int,
        *,
        source_section_id: int,
        target_section_id: int,
    ) -> None:
        """Move a form field to a new position or section."""
        self._request(
            _write(
                "field_reorder",
                {
                    "topic_id": topic_id,
                    "source_section_id": source_section_id,
                    "target_section_id": target_section_id,
                    "field_id": field_id,
                    "new_index": new_index,
                },
            )
        )

    def generate_card_titles(
        self, topic_id: int, field_num: CardField = CardField.VOTING_TITLE
    ) -> list[TopicRequest]:
        """Rebuild card titles, announcements or diploma titles for all requests in a
        topic and return the updated topic requests.
        """
        return self._request(_generate_card_titles(topic_id, field_num))

    def reorder_requests(self, topic_id: int) -> None:
        """Renumber requests in a topic according to the planner schedule."""
        self._request(_write("reorder_requests", {"topic_id": topic_id}))

    def get_with_groups(self, url_code: str) -> TopicGroup:
        """A group topic with all event topics and its linked child topics."""
        return self._request(_get_with_groups(url_code))

    def add_child_topic(
        self, url_code: str, child_topic_id: int
    ) -> list[TopicGroupLink]:
        """Add ``child_topic_id`` to the group topic ``url_code``."""
        return self._request(_child_topic("add", url_code, child_topic_id))

    def delete_child_topic(
        self, url_code: str, child_topic_id: int
    ) -> list[TopicGroupLink]:
        """Remove ``child_topic_id`` from the group topic ``url_code``."""
        return self._request(_child_topic("del", url_code, child_topic_id))


class AsyncTopics(AsyncResource):
    """Topics (nominations) of the event."""

    async def get_list(
        self, *, with_group_text: bool = False, event_id: int | None = None
    ) -> list[Topic]:
        """All topics of the event.

        :param with_group_text: Also return grouping info (``Topic.child_topics``).
        :param event_id: List the topics of another event instead, e.g. to pick a
            source for ``fill_from_topic``.
        """
        return await self._request(_get_list(with_group_text, event_id))

    async def get_requests(self, topic: int | str) -> TopicRequests:
        """A topic and its requests.

        :param topic: ``Topic.id`` or ``Topic.url_code`` (e.g. ``"solo_vostok"``).
        """
        return await self._request(_get_requests(topic))

    async def get_all_requests(self) -> list[EventRequest]:
        """Every request of the event, across all topics."""
        return await self._request(_GET_ALL_REQUESTS)

    async def get_requests_for_planner(self) -> PlannerData:
        """Every request of the event with durations and members, for scheduling."""
        return await self._request(_GET_FOR_PLANNER)

    async def get_form(self, url_code: str) -> TopicForm:
        """A topic with the sections and fields of its form.

        :param url_code: ``Topic.url_code``.
        """
        return await self._request(_get_form(url_code))

    async def create(self, *, voting_group: int = 0) -> None:
        """Create an empty topic at the end of the list.

        The response carries no id: the new topic has the url code ``"new"``, so
        fetch it with ``get_form("new")``.

        :param voting_group: ``Topic.voting_group`` of the new topic.
        """
        await self._request(_write("add", {"voting_group": voting_group}))

    async def delete(self, topic_id: int) -> None:
        """Delete a topic."""
        await self._request(_write("topic_delete", {"topic_id": topic_id}))

    async def reorder(self, topic_id: int, new_index: int) -> None:
        """Move a topic to another position in the list.

        :param new_index: zero-based position among the event's topics.
        """
        await self._request(
            _write("topic_reorder", {"topic_id": topic_id, "new_index": new_index})
        )

    async def fill_from_template(self, topic_id: int, template: TopicTemplate) -> None:
        """Replace a topic's form with a built-in template.

        :param template: template name, e.g. ``TopicTemplate.ART``.
        """
        template = TopicTemplate(template)
        await self._request(
            _write(
                "fill_from_template", {"topic_id": topic_id, "internal_name": template}
            )
        )

    async def fill_from_topic(self, topic_id: int, src_topic_id: int) -> None:
        """Replace a topic's form (and card rules) with a copy of another topic's.

        :param src_topic_id: ``Topic.id`` to copy from, possibly of another event
            (see ``get_list(event_id=)``).
        """
        await self._request(
            _write(
                "fill_from_topic", {"topic_id": topic_id, "src_topic_id": src_topic_id}
            )
        )

    async def add_section(self, topic_id: int, template: SectionTemplate) -> None:
        """Add a built-in section to a topic's form.

        :param template: section template name, e.g. ``SectionTemplate.COMMON``.
        """
        template = SectionTemplate(template)
        await self._request(
            _write("section_add", {"topic_id": topic_id, "internal_name": template})
        )

    async def save_section(
        self, topic_id: int, section_id: int, field: str, value: Any
    ) -> None:
        """Set an attribute of a form section.

        :param section_id: ``TopicSection.id``.
        :param field: the ``TopicSection`` attribute to set, e.g. ``title``,
            ``kogo_title``, ``max_repeat`` or ``internal_name``.
        """
        await self._request(
            _write(
                "save_section_field",
                {
                    "topic_id": topic_id,
                    "section_id": section_id,
                    "field": field,
                    "data": value,
                },
            )
        )

    async def delete_section(self, topic_id: int, section_id: int) -> None:
        """Remove a section, with its fields, from a topic's form."""
        await self._request(
            _write("section_delete", {"topic_id": topic_id, "section_id": section_id})
        )

    async def add_field(
        self, topic_id: int, section_id: int, template: FieldTemplate
    ) -> None:
        """Add a built-in field to a section of a topic's form.

        :param section_id: ``TopicSection.id``.
        :param template: field template name, e.g. ``FieldTemplate.FIRST_NAME``.
        """
        template = FieldTemplate(template)
        await self._request(
            _write(
                "field_add",
                {
                    "topic_id": topic_id,
                    "section_id": section_id,
                    "internal_name": template,
                },
            )
        )

    async def delete_field(self, topic_id: int, section_id: int, field_id: int) -> None:
        """Delete a form field."""
        await self._request(
            _write(
                "field_delete",
                {"topic_id": topic_id, "section_id": section_id, "field_id": field_id},
            )
        )

    async def save_field(
        self, topic_id: int, section_id: int, field_id: int, field: str, value: Any
    ) -> None:
        """Set a form field attribute."""
        await self._request(
            _write(
                "save_field_field",
                {
                    "topic_id": topic_id,
                    "section_id": section_id,
                    "field_id": field_id,
                    "field": field,
                    "data": value,
                },
            )
        )

    async def save_topic(self, topic_id: int, field: str, value: Any) -> None:
        """Set a topic attribute."""
        await self._request(
            _write(
                "save_topic_field",
                {"topic_id": topic_id, "field": field, "data": value},
            )
        )

    async def reorder_section(
        self, topic_id: int, section_id: int, new_index: int
    ) -> None:
        """Move a form section to a new position."""
        await self._request(
            _write(
                "section_reorder",
                {
                    "topic_id": topic_id,
                    "section_id": section_id,
                    "new_index": new_index,
                },
            )
        )

    async def reorder_field(
        self,
        topic_id: int,
        field_id: int,
        new_index: int,
        *,
        source_section_id: int,
        target_section_id: int,
    ) -> None:
        """Move a form field to a new position or section."""
        await self._request(
            _write(
                "field_reorder",
                {
                    "topic_id": topic_id,
                    "source_section_id": source_section_id,
                    "target_section_id": target_section_id,
                    "field_id": field_id,
                    "new_index": new_index,
                },
            )
        )

    async def generate_card_titles(
        self, topic_id: int, field_num: CardField = CardField.VOTING_TITLE
    ) -> list[TopicRequest]:
        """Rebuild card titles, announcements or diploma titles for all requests in a
        topic and return the updated topic requests.
        """
        return await self._request(_generate_card_titles(topic_id, field_num))

    async def reorder_requests(self, topic_id: int) -> None:
        """Renumber requests in a topic according to the planner schedule."""
        await self._request(_write("reorder_requests", {"topic_id": topic_id}))

    async def get_with_groups(self, url_code: str) -> TopicGroup:
        """A group topic with all event topics and its linked child topics."""
        return await self._request(_get_with_groups(url_code))

    async def add_child_topic(
        self, url_code: str, child_topic_id: int
    ) -> list[TopicGroupLink]:
        """Add ``child_topic_id`` to the group topic ``url_code``."""
        return await self._request(_child_topic("add", url_code, child_topic_id))

    async def delete_child_topic(
        self, url_code: str, child_topic_id: int
    ) -> list[TopicGroupLink]:
        """Remove ``child_topic_id`` from the group topic ``url_code``."""
        return await self._request(_child_topic("del", url_code, child_topic_id))
