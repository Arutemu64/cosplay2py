import json
from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any

import httpx2
import pytest

from cosplay2py.models import (
    CardField,
    FieldTemplate,
    PublicRequests,
    RequestStatus,
    SectionTemplate,
    TopicCategory,
    TopicGroup,
    TopicGroupLink,
    TopicTemplate,
)
from unit.conftest import TOPIC, ApiCall, json_response, make_client


def test_get_list_unwraps_and_parses() -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        assert request.method == "GET"
        return json_response([TOPIC])

    with make_client(handler) as client:
        (topic,) = client.topics.get_list()

    assert topic.url_code == "solo"
    assert topic.category is TopicCategory.DEFILE
    assert topic.public_requests is PublicRequests.NO
    assert topic.card_enabled is True
    assert topic.voting_public is False
    assert topic.time_requests_open == datetime(2026, 4, 1, 9, tzinfo=UTC)
    assert topic.time_voting_open is None


@pytest.mark.parametrize(
    ("kwargs", "body"),
    [
        ({"event_id": 81}, {"event_id": 81}),
        (
            {"with_group_text": True, "event_id": 81},
            {"with_group_text": True, "event_id": 81},
        ),
    ],
)
def test_get_list_posts_filters(
    kwargs: dict[str, Any], body: dict[str, object]
) -> None:
    seen: list[httpx2.Request] = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        seen.append(request)
        return json_response([TOPIC])

    with make_client(handler) as client:
        (topic,) = client.topics.get_list(**kwargs)

    assert topic.id == TOPIC["id"]
    (request,) = seen
    assert request.method == "POST"
    assert json.loads(request.content) == body


@pytest.mark.parametrize(
    ("topic", "body"),
    [(7, {"topic_id": 7}), ("solo", {"topic_url_code": "solo"})],
)
def test_get_requests_by_id_or_url_code(
    topic: int | str, body: dict[str, object]
) -> None:
    seen: list[httpx2.Request] = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        seen.append(request)
        return json_response({"message": "ok", "topic": TOPIC, "requests": []})

    with make_client(handler) as client:
        listing = client.topics.get_requests(topic)

    assert listing.topic.id == TOPIC["id"]
    (request,) = seen
    assert request.url.path == "/api/topics/get_requests"
    assert json.loads(request.content) == body


def test_get_all_requests() -> None:
    item = {
        "id": 1,
        "topic_id": 7,
        "number": 52,
        "status": "approved",
        "update_time": "28.05.25 16:38",
        "comment_time": "2025-05-28 14:06:38",
        "user_id": 3,
        "user_title": "Someone",
        "image_update_time": 1527353038,
        "voting_number": None,
        "voting_title": "Title",
        "new_comments": -1,
        "new_updates": None,
    }

    def handler(request: httpx2.Request) -> httpx2.Response:
        assert request.method == "POST"
        assert request.url.path == "/api/topics/get_all_requests"
        return json_response([item])

    with make_client(handler) as client:
        (parsed,) = client.topics.get_all_requests()

    assert parsed.status is RequestStatus.APPROVED
    assert parsed.update_time == datetime(2025, 5, 28, 16, 38)  # noqa: DTZ001
    assert parsed.comment_time == datetime(2025, 5, 28, 14, 6, 38, tzinfo=UTC)
    assert parsed.image_update_time == datetime(2018, 5, 26, 16, 43, 58, tzinfo=UTC)
    assert parsed.model_extra == {}


def test_get_form() -> None:
    seen: list[httpx2.Request] = []
    section = {
        "id": 3,
        "topic_id": 1,
        "title": "Performance",
        "kogo_title": "",
        "order": 1,
        "max_repeat": 1,
        "visible_to_all": 1,
        "registration_blanks": 1,
        "internal_name": "common",
    }
    custom_section = {**section, "id": 4, "internal_name": ""}
    field = {
        "id": 5,
        "section_id": 3,
        "title": "Team",
        "type": "text",
        "order": 1,
        "hint": "",
        "data": None,
        "visible_to_all": 1,
        "internal_name": "team",
    }
    custom_field = {**field, "id": 6, "internal_name": ""}

    def handler(request: httpx2.Request) -> httpx2.Response:
        seen.append(request)
        return json_response(
            {
                "topic": TOPIC,
                "topic_sections": [section, custom_section],
                "topic_fields": [field, custom_field],
                "requests_count": 0,
            }
        )

    with make_client(handler) as client:
        form = client.topics.get_form("solo")

    assert form.topic.id == TOPIC["id"]
    assert [s.internal_name for s in form.sections] == [SectionTemplate.COMMON, None]
    assert [f.internal_name for f in form.fields] == [FieldTemplate.TEAM, None]
    assert form.requests_count == 0
    (request,) = seen
    assert request.url.path == "/api/topics/get_with_fields"
    assert json.loads(request.content) == {"topic_url_code": "solo"}


@pytest.mark.anyio
@pytest.mark.parametrize(
    ("call", "path", "body"),
    [
        (lambda c: c.topics.create(), "add", {"voting_group": 0}),
        (lambda c: c.topics.delete(7), "topic_delete", {"topic_id": 7}),
        (
            lambda c: c.topics.reorder(7, 30),
            "topic_reorder",
            {"topic_id": 7, "new_index": 30},
        ),
        (
            lambda c: c.topics.fill_from_template(7, TopicTemplate.ART),
            "fill_from_template",
            {"topic_id": 7, "internal_name": "art"},
        ),
        (
            lambda c: c.topics.fill_from_topic(7, 1030),
            "fill_from_topic",
            {"topic_id": 7, "src_topic_id": 1030},
        ),
        (
            lambda c: c.topics.add_section(7, SectionTemplate.COMMON),
            "section_add",
            {"topic_id": 7, "internal_name": "common"},
        ),
        (
            lambda c: c.topics.save_section(7, 3, "max_repeat", 2),
            "save_section_field",
            {"topic_id": 7, "section_id": 3, "field": "max_repeat", "data": 2},
        ),
        (
            lambda c: c.topics.delete_section(7, 3),
            "section_delete",
            {"topic_id": 7, "section_id": 3},
        ),
        (
            lambda c: c.topics.add_field(7, 3, FieldTemplate.FIRST_NAME),
            "field_add",
            {"topic_id": 7, "section_id": 3, "internal_name": "first_name"},
        ),
    ],
)
async def test_writes(
    api: ApiCall, call: Callable[[Any], Any], path: str, body: dict[str, object]
) -> None:
    seen: list[httpx2.Request] = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        seen.append(request)
        return json_response({"message": "ok"})

    assert await api(handler, call) is None

    (request,) = seen
    assert request.method == "POST"
    assert request.url.path == f"/api/topics/{path}"
    assert json.loads(request.content) == body


@pytest.mark.anyio
@pytest.mark.parametrize(
    ("call", "path", "body"),
    [
        (
            lambda c: c.topics.delete_field(7, 3, 5),
            "topics/field_delete",
            {"topic_id": 7, "section_id": 3, "field_id": 5},
        ),
        (
            lambda c: c.topics.save_field(7, 3, 5, "title", "Name"),
            "topics/save_field_field",
            {
                "topic_id": 7,
                "section_id": 3,
                "field_id": 5,
                "field": "title",
                "data": "Name",
            },
        ),
        (
            lambda c: c.topics.save_topic(7, "card_name_rule", "Name"),
            "topics/save_topic_field",
            {"topic_id": 7, "field": "card_name_rule", "data": "Name"},
        ),
        (
            lambda c: c.topics.reorder_section(7, 3, 2),
            "topics/section_reorder",
            {"topic_id": 7, "section_id": 3, "new_index": 2},
        ),
        (
            lambda c: c.topics.reorder_field(
                7, 5, 1, source_section_id=3, target_section_id=4
            ),
            "topics/field_reorder",
            {
                "topic_id": 7,
                "source_section_id": 3,
                "target_section_id": 4,
                "field_id": 5,
                "new_index": 1,
            },
        ),
        (
            lambda c: c.topics.reorder_requests(7),
            "topics/reorder_requests",
            {"topic_id": 7},
        ),
    ],
)
async def test_new_writes(
    api: ApiCall, call: Callable[[Any], Any], path: str, body: dict[str, object]
) -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        assert request.method == "POST"
        assert request.url.path == f"/api/{path}"
        assert json.loads(request.content) == body
        return json_response({"message": "ok"})

    assert await api(handler, call) is None


@pytest.mark.anyio
async def test_generate_card_titles(api: ApiCall) -> None:
    req = {
        "id": 10,
        "number": 1,
        "status": "approved",
        "user_id": 7,
        "voting_title": "Card 1",
    }

    def handler(request: httpx2.Request) -> httpx2.Response:
        assert request.method == "POST"
        assert request.url.path == "/api/topics/generate_cards_title"
        assert json.loads(request.content) == {"topic_id": 7, "field_num": 2}
        return json_response({"message": "ok", "requests": [req]})

    (parsed,) = await api(
        handler,
        lambda c: c.topics.generate_card_titles(7, CardField.ANNOUNCEMENT_TITLE),
    )
    assert parsed.id == 10
    assert parsed.voting_title == "Card 1"


@pytest.mark.parametrize(
    ("bad_field", "exc"), [(True, TypeError), (0, ValueError), (4, ValueError)]
)
def test_generate_card_titles_rejects_invalid_field(
    bad_field: Any, exc: type[Exception]
) -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        raise AssertionError("no request expected")

    with make_client(handler) as client, pytest.raises(exc):
        client.topics.generate_card_titles(7, bad_field)


@pytest.mark.anyio
async def test_group_topics(api: ApiCall) -> None:
    def get_handler(request: httpx2.Request) -> httpx2.Response:
        assert request.method == "POST"
        assert request.url.path == "/api/topics/get_with_groups"
        assert json.loads(request.content) == {"topic_url_code": "grp"}
        return json_response(
            {
                "topic": TOPIC,
                "topics": [TOPIC],
                "child_topics": [{"group_topic_id": 7, "child_topic_id": 2}],
            }
        )

    group = await api(get_handler, lambda c: c.topics.get_with_groups("grp"))
    assert isinstance(group, TopicGroup)
    assert group.topic.id == TOPIC["id"]
    assert group.topics[0].id == TOPIC["id"]
    assert group.child_topics == [TopicGroupLink(group_topic_id=7, child_topic_id=2)]
    assert group.model_extra == {}

    for action, method in [
        ("add", lambda c: c.topics.add_child_topic("grp", 2)),
        ("del", lambda c: c.topics.delete_child_topic("grp", 2)),
    ]:

        def child_handler(
            request: httpx2.Request, expected: str = action
        ) -> httpx2.Response:
            assert request.method == "POST"
            assert request.url.path == f"/api/topics/{expected}_child_topic"
            assert json.loads(request.content) == {
                "topic_url_code": "grp",
                "child_topic_id": 2,
            }
            return json_response(
                {
                    "message": "ok",
                    "child_topics": [{"group_topic_id": 7, "child_topic_id": 2}],
                }
            )

        assert await api(child_handler, method) == [
            TopicGroupLink(group_topic_id=7, child_topic_id=2)
        ]


@pytest.mark.anyio
async def test_empty_group_links(api: ApiCall) -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        if request.url.path == "/api/topics/get_with_groups":
            return json_response(
                {"topic": TOPIC, "topics": [TOPIC], "child_topics": []}
            )
        return json_response({"child_topics": []})

    group = await api(handler, lambda c: c.topics.get_with_groups("grp"))
    assert group.child_topics == []
    assert await api(handler, lambda c: c.topics.delete_child_topic("grp", 2)) == []


@pytest.mark.anyio
@pytest.mark.parametrize("group_text", [None, "Solo, Group"])
async def test_get_list_group_display_data(
    api: ApiCall, group_text: str | None
) -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        assert request.method == "POST"
        assert json.loads(request.content) == {"with_group_text": True}
        return json_response([{**TOPIC, "child_topics": group_text}])

    (topic,) = await api(handler, lambda c: c.topics.get_list(with_group_text=True))
    assert topic.child_topics == group_text
