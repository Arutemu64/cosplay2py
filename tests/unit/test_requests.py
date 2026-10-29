import json
from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any

import httpx2
import pytest

from cosplay2py import APIResponseValidationError
from cosplay2py.models import (
    EventRole,
    FeedbackMark,
    RequestStatus,
    TopicFieldType,
)
from unit.conftest import TOPIC, ApiCall, json_response, make_client

pytestmark = pytest.mark.anyio


@pytest.mark.parametrize("status", ["approved", "new"])
@pytest.mark.parametrize("field_type", list(TopicFieldType))
async def test_get(api: ApiCall, status: str, field_type: TopicFieldType) -> None:
    payload = {
        "message": "ok",
        "editEnabled": True,
        "friendeditEnabled": False,
        "request": {
            "id": 5,
            "event_id": 10,
            "topic_id": 1,
            "user_id": 7,
            "number": 3,
            "status": status,
            "creation_time": "2026-07-06 16:40:23",
            "win": 1,
            "score": 6,
            "ER": 5,
        },
        "author": {
            "user_id": 7,
            "title": "Nick",
            "city": "City",
            "image_update_time": "2025-12-23 19:51:11",
        },
        "topic": TOPIC,
        "sections": [
            {
                "id": 100,
                "topic_id": 1,
                "title": "Main",
                "kogo_title": "",
                "order": 1,
                "max_repeat": 1,
                "visible_to_all": 1,
                "registration_blanks": 1,
                "internal_name": "common",
            }
        ],
        "fields": [
            {
                "id": 200,
                "section_id": 100,
                "title": "Character",
                "type": str(field_type),
                "order": 1,
                "hint": "",
                "data": '["A","B"]',
                "visible_to_all": 1,
                "internal_name": "character",
            }
        ],
        "reqsections": [
            {"id": 300, "request_id": 5, "topic_section_id": 100, "order": 0}
        ],
        "reqvalues": [
            {
                "id": 400,
                "request_id": 5,
                "request_section_id": 300,
                "topic_field_id": 200,
                "value": "A",
                "user_id": 7,
                "changed": -1,
                "update_time": "2026-07-06 16:40:25",
            }
        ],
        "scores": [{"user_id": 2, "user_title": "Jury", "score": 6}],
    }

    def handler(request: httpx2.Request) -> httpx2.Response:
        assert json.loads(request.content) == {"request_id": "5"}
        return json_response(payload)

    details = await api(handler, lambda c: c.requests.get(5))

    assert details.request.status is RequestStatus(status)
    assert details.request.er is EventRole.ORG
    assert details.request.win == 1
    assert details.request.score == 6
    assert details.edit_enabled is True
    assert details.scores[0].user_id == 2
    assert details.scores[0].score == 6
    assert details.scores[0].model_extra == {}
    assert details.fields[0].options == ["A", "B"]
    assert details.fields[0].type is field_type
    assert json.loads(details.fields[0].model_dump_json())["type"] == field_type
    assert details.values_by_field() == {"character": ["A"]}


def test_get_rejects_unknown_field_type() -> None:
    payload = {
        "message": "ok",
        "request": {
            "id": 5,
            "event_id": 10,
            "topic_id": 1,
            "user_id": 7,
            "number": 3,
            "status": "approved",
        },
        "author": {"user_id": 7},
        "topic": TOPIC,
        "sections": [],
        "fields": [
            {
                "id": 200,
                "section_id": 100,
                "title": "Character",
                "type": "unknown_field_type",
                "order": 1,
                "visible_to_all": 1,
            }
        ],
        "reqsections": [],
        "reqvalues": [],
    }

    with (
        make_client(lambda request: json_response(payload)) as client,
        pytest.raises(APIResponseValidationError),
    ):
        client.requests.get(5)


@pytest.mark.parametrize(
    ("call", "path", "body"),
    [
        (
            lambda c: c.requests.add_comment(42, "Looks good", sms=True),
            "add_comment",
            {"request_id": "42", "comment": "Looks good", "email": True, "sms": True},
        ),
        (
            lambda c: c.requests.delete_comment(42, 9),
            "del_comment",
            {"request_id": "42", "comment_id": 9},
        ),
        (
            lambda c: c.requests.save_data(42, "win", 3),
            "save_data",
            {"request_id": 42, "field": "win", "data": 3},
        ),
        (
            lambda c: c.requests.delete_image(42, 3, 5, 9),
            "delete_image",
            {
                "request_id": 42,
                "request_section_id": "3",
                "topic_field_id": 5,
                "value_id": "9",
            },
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
    assert request.url.path == f"/api/requests/{path}"
    assert json.loads(request.content) == body


@pytest.mark.parametrize("card", ["title", "announcement", "diplom"])
async def test_generate_card(api: ApiCall, card: str) -> None:
    seen: list[httpx2.Request] = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        seen.append(request)
        return json_response({"message": "ok", "text": "Косплей Тест по ф. Тест"})

    text = await api(
        handler, lambda c: getattr(c.requests, f"generate_card_{card}")(42)
    )

    assert text == "Косплей Тест по ф. Тест"
    (request,) = seen
    assert request.url.path == f"/api/requests/generate_card_{card}"
    assert json.loads(request.content) == {"request_id": 42}


async def test_set_status(api: ApiCall) -> None:
    seen: list[httpx2.Request] = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        seen.append(request)
        return json_response(
            {"message": "ok", "request_number": 12, "voting_number": 34}
        )

    change = await api(
        handler, lambda c: c.requests.set_status(42, RequestStatus.WAITING)
    )

    assert change.request_number == 12
    assert change.voting_number == 34
    (request,) = seen
    assert request.url.path == "/api/requests/set_status"
    assert json.loads(request.content) == {"request_id": 42, "status": "waiting"}


@pytest.mark.parametrize(("value_id", "extra"), [(7, {"value_id": 7}), (None, {})])
async def test_save_field(
    api: ApiCall, value_id: int | None, extra: dict[str, object]
) -> None:
    seen: list[httpx2.Request] = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        seen.append(request)
        return json_response({"message": "ok", "id": "7"})

    stored = await api(
        handler,
        lambda c: c.requests.save_field(42, 3, 5, "Привет", value_id=value_id),
    )

    assert stored == 7
    (request,) = seen
    assert request.url.path == "/api/requests/save_field"
    assert json.loads(request.content) == {
        "request_id": 42,
        "request_section_id": 3,
        "topic_field_id": 5,
        "data": "Привет",
        **extra,
    }


@pytest.mark.parametrize(("value", "sent"), [(8, 8), (None, None)])
def test_save_field_user_or_empty(value: int | None, sent: object) -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        assert json.loads(request.content)["data"] == sent
        return json_response({"message": "ok", "id": "7"})

    with make_client(handler) as client:
        assert client.requests.save_field(42, 3, 5, value, value_id=7) == 7


def test_get_value_history() -> None:
    seen: list[httpx2.Request] = []
    change = {
        "update_time": "2026-10-28 18:27:30",
        "user_id": 7,
        "title": "Nick",
        "city": "Somewhere",
        "image_update_time": "2023-01-19 12:52:12",
        "value": '{"filename":1793212048}',
    }

    def handler(request: httpx2.Request) -> httpx2.Response:
        seen.append(request)
        return json_response({"message": "ok", "value_history": [change]})

    with make_client(handler) as client:
        (parsed,) = client.requests.get_value_history(42, 9)

    (request,) = seen
    assert request.url.path == "/api/requests/get_value_history"
    assert json.loads(request.content) == {"request_id": 42, "value_id": "9"}
    assert parsed.update_time == datetime(2026, 10, 28, 18, 27, 30, tzinfo=UTC)
    assert parsed.value == '{"filename":1793212048}'
    assert parsed.model_extra == {}


@pytest.mark.parametrize(("value_id", "sent"), [(None, b"0"), (9, b"9")])
async def test_upload_image(api: ApiCall, value_id: int | None, sent: bytes) -> None:
    seen: list[httpx2.Request] = []
    size = {"width": 4, "height": 3}
    value = {"filename": 1793212048, "original": size, "large": size}

    def handler(request: httpx2.Request) -> httpx2.Response:
        request.read()
        seen.append(request)
        return json_response({"message": "ok", "id": "9", "value": value})

    uploaded = await api(
        handler,
        lambda c: c.requests.upload_image(
            42, 3, 5, b"\xff\xd8", "cat.jpg", value_id=value_id
        ),
    )

    (request,) = seen
    assert request.url.path == "/api/requests/upload_image"
    assert request.headers["content-type"].startswith("multipart/form-data")
    body = request.content
    for name, field in [
        ("request_id", b"42"),
        ("request_section_id", b"3"),
        ("topic_field_id", b"5"),
        ("value_id", sent),
    ]:
        assert f'name="{name}"\r\n\r\n'.encode() + field + b"\r\n" in body
    assert b'name="uploaded_image"; filename="cat.jpg"' in body
    # The part's content type is guessed from the extension (platform-dependent).
    assert b"Content-Type: image/" in body
    assert b"\r\n\r\n\xff\xd8\r\n--" in body
    assert uploaded.id == 9
    assert uploaded.value.filename == 1793212048
    assert uploaded.value.large == uploaded.value.original
    assert uploaded.value.medium is None


async def test_create(api: ApiCall) -> None:
    seen: list[httpx2.Request] = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        seen.append(request)
        return json_response({"requestId": "42"})

    assert await api(handler, lambda c: c.requests.create(7)) == 42

    (request,) = seen
    assert request.url.path == "/api/requests/create"
    assert json.loads(request.content) == {"topic_id": 7}


async def test_create_section(api: ApiCall) -> None:
    seen: list[httpx2.Request] = []
    value = {
        "id": 9,
        "request_id": 42,
        "request_section_id": 3,
        "topic_field_id": 5,
        "value": "Тестер",
        "update_time": "2025-06-01 12:00:00",
        "user_id": 1,
    }

    def handler(request: httpx2.Request) -> httpx2.Response:
        seen.append(request)
        return json_response({"message": "ok", "id": "3", "values": [value]})

    section = await api(handler, lambda c: c.requests.create_section(42, 11))

    assert section.id == 3
    assert [v.value for v in section.values] == ["Тестер"]
    (request,) = seen
    assert request.url.path == "/api/requests/create_reqsection"
    assert json.loads(request.content) == {
        "request_id": 42,
        "topic_section_id": 11,
        "ord": 0,
    }


def test_change_topic_conflict() -> None:
    seen: list[httpx2.Request] = []
    section = {
        "id": 11,
        "topic_id": 7,
        "title": "Номер",
        "kogo_title": "",
        "order": 1,
        "max_repeat": 1,
        "visible_to_all": 1,
        "registration_blanks": 1,
        "internal_name": "common_video",
    }
    field = {
        "id": 5,
        "section_id": 11,
        "title": "Видео",
        "type": "link",
        "order": 1,
        "hint": "",
        "data": None,
        "visible_to_all": 0,
        "internal_name": "video_link",
        "topic_title": "Номер",
    }

    def handler(request: httpx2.Request) -> httpx2.Response:
        seen.append(request)
        return json_response(
            {
                "message": "target_not_found",
                "error_sections": [section],
                "error_fields": [field],
            }
        )

    with make_client(handler) as client:
        change = client.requests.change_topic(42, 8)

    assert not change.moved
    assert [s.id for s in change.error_sections] == [11]
    assert [f.topic_title for f in change.error_fields] == ["Номер"]
    (request,) = seen
    assert request.url.path == "/api/requests/change_topic"
    assert json.loads(request.content) == {"request_id": 42, "target_topic_id": 8}


async def test_change_topic_force(api: ApiCall) -> None:
    seen: list[httpx2.Request] = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        seen.append(request)
        return json_response({"message": "ok"})

    change = await api(handler, lambda c: c.requests.change_topic(42, 8, force=True))

    assert change.moved
    assert change.error_sections == []
    (request,) = seen
    assert json.loads(request.content) == {
        "request_id": 42,
        "target_topic_id": 8,
        "forceflag": "force",
    }


def test_get_comments() -> None:
    comment = {
        "id": 1,
        "user_id": 2,
        "content": "Hello",
        "user_title": "Org",
        "creation_time": "2026-10-28 16:47:50",
        "sms": 0,
        "email": 1,
        "changed": 0,
        "creationtime": "28.10.26 19:47",
    }

    def handler(request: httpx2.Request) -> httpx2.Response:
        return json_response({"message": "ok", "comments": [comment]})

    with make_client(handler) as client:
        (parsed,) = client.requests.get_comments(42)

    assert parsed.creation_time == datetime(2026, 10, 28, 16, 47, 50, tzinfo=UTC)
    # Naive by design: the site shows local time without an offset.
    assert parsed.creation_time_local == datetime(2026, 10, 28, 19, 47)  # noqa: DTZ001
    assert parsed.email is True
    assert parsed.sms is False
    assert parsed.model_extra == {}


@pytest.mark.anyio
@pytest.mark.parametrize(
    ("call", "path", "body"),
    [
        (
            lambda c: c.requests.add_org_comment(42, "Hello"),
            "requests/add_orgcomment",
            {"request_id": "42", "comment": "Hello"},
        ),
        (
            lambda c: c.requests.delete_org_comment(42, 3),
            "requests/del_orgcomment",
            {"request_id": "42", "comment_id": 3},
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
@pytest.mark.parametrize("action", ["get", "add", "del"])
async def test_feedbacks(api: ApiCall, action: str) -> None:
    payload = {
        "id": 5,
        "create_time": "2025-06-01 12:00:00",
        "org_id": 2,
        "user_id": 3,
        "event_id": 7,
        "mark": -1,
        "info": "Example",
        "event_title": "Festival",
        "event_subdomain": "example",
        "org_title": "Organizer",
        "org_city": "City",
        "org_image_update_time": 0,
    }

    def handler(request: httpx2.Request) -> httpx2.Response:
        assert request.url.path == f"/api/requests/feedbacks_{action}"
        expected: dict[str, object] = {"request_id": 42, "user_id": 3}
        if action == "add":
            expected.update(mark="-1", info="Example")
        elif action == "del":
            expected["feedback_id"] = 5
        assert json.loads(request.content) == expected
        return json_response({"message": "ok", "feedbacks": [payload]})

    calls = {
        "get": lambda c: c.requests.get_feedbacks(42, 3),
        "add": lambda c: c.requests.add_feedback(
            42, 3, FeedbackMark.NEGATIVE, "Example"
        ),
        "del": lambda c: c.requests.delete_feedback(42, 3, 5),
    }
    (feedback,) = await api(handler, calls[action])
    assert feedback.mark is FeedbackMark.NEGATIVE
    assert feedback.create_time == datetime(2025, 6, 1, 12, tzinfo=UTC)
    assert feedback.org_image_update_time == datetime(1970, 1, 1, tzinfo=UTC)
    assert feedback.model_extra == {}


@pytest.mark.parametrize(
    ("bad_mark", "exc"), [(True, TypeError), (2, ValueError), (-2, ValueError)]
)
def test_add_feedback_rejects_invalid_mark(bad_mark: Any, exc: type[Exception]) -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        raise AssertionError("no request expected")

    with make_client(handler) as client, pytest.raises(exc):
        client.requests.add_feedback(42, 3, bad_mark, "Example")
