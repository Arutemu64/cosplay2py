import json
from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any

import httpx2
import pytest

from cosplay2py.models import (
    EventTime,
    FriendStatus,
    RequestStatus,
    Sex,
    UserEventRoleType,
)
from unit.conftest import ApiCall, json_response, make_client


def test_get() -> None:
    seen: list[httpx2.Request] = []
    user = {
        "id": 7,
        "user_id": 7,
        "title": "Nick",
        "city": "Somewhere",
        "vk": "https://vk.ru/nick",
        "sex": "female",
        "first_name": "Anna",
        "second_name": "Example",
        "third_name": "Testovna",
        "email": "nick@example.com",
        "mobile": "+70000000000",
        "birthday": "01.02.2000",
        "image_update_time": 1674132732,
        "friend_status": "none",
    }
    friend = {
        "id": 3,
        "friend_id": 8,
        "friend_title": "Pal",
        "friend_city": "Elsewhere",
        "status": 1,
        "invitetome": "0",
    }

    def handler(request: httpx2.Request) -> httpx2.Response:
        seen.append(request)
        return json_response({"message": "ok", "user": user, "friends": [friend]})

    with make_client(handler) as client:
        details = client.users.get(7)

    (request,) = seen
    assert request.method == "POST"
    assert request.url.path == "/api/users/get"
    assert request.url.params["user_id"] == "7"
    assert request.content == b""
    assert details.user.second_name == "Example"
    assert details.user.sex is Sex.FEMALE
    assert details.user.friend_status is FriendStatus.NONE
    assert details.user.image_update_time == datetime(
        2023, 1, 19, 12, 52, 12, tzinfo=UTC
    )
    assert details.user.model_extra == {}
    (parsed,) = details.friends
    assert parsed.friend_id == 8
    assert parsed.invitetome is False
    assert parsed.model_extra == {}


@pytest.mark.anyio
@pytest.mark.parametrize(
    ("call", "path", "body"),
    [
        (
            lambda c: c.users.save_field(7, "birthday", "01.02.2000"),
            "save",
            {"userId": 7, "field": "birthday", "data": "01.02.2000"},
        ),
        (lambda c: c.users.add_friend(8), "friend_add", {"friend_id": 8}),
        (
            lambda c: c.users.cancel_friend_invite(8),
            "friend_invite_cancel",
            {"friend_id": 8},
        ),
        (lambda c: c.users.remove_friend(8), "friend_remove", {"friend_id": 8}),
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
    assert request.url.path == f"/api/users/{path}"
    assert json.loads(request.content) == body


@pytest.mark.anyio
@pytest.mark.parametrize(("only_new", "flag"), [(True, 1), (False, 0)])
async def test_get_feeds(api: ApiCall, only_new: bool, flag: int) -> None:
    seen: list[httpx2.Request] = []
    feed = {"id": 1, "type": "comment", "request_id": 42, "text": "New comment"}

    def handler(request: httpx2.Request) -> httpx2.Response:
        seen.append(request)
        return json_response({"message": "ok", "feeds": [feed]})

    feeds = await api(
        handler, lambda c: c.users.get_feeds(7, limit=10, only_new=only_new)
    )

    assert feeds == [feed]
    (request,) = seen
    assert request.method == "POST"
    assert request.url.path == "/api/users/get_feeds"
    assert json.loads(request.content) == {
        "user_id": 7,
        "limit": 10,
        "onlynew": flag,
    }


def test_get_friends() -> None:
    friend = {"id": 7, "user_id": 7, "title": "Friend", "city": "Somewhere"}

    def handler(request: httpx2.Request) -> httpx2.Response:
        return json_response({"users": [friend]})

    with make_client(handler) as client:
        (parsed,) = client.users.get_friends()

    assert parsed.user_id == 7
    assert parsed.title == "Friend"
    assert parsed.model_extra == {}


def test_search() -> None:
    seen: list[httpx2.Request] = []
    user = {
        "id": 7,
        "user_id": 7,
        "title": "Nick",
        "city": "Somewhere",
        "image_update_time": 1713798357,
        "friends_boost": 0,
    }

    def handler(request: httpx2.Request) -> httpx2.Response:
        seen.append(request)
        return json_response({"users": [user]})

    with make_client(handler) as client:
        (parsed,) = client.users.search("nic")

    (request,) = seen
    assert request.url.path == "/api/users/search"
    assert json.loads(request.content) == {"query": "nic"}
    assert parsed.user_id == 7
    assert parsed.friends_boost == 0
    assert parsed.model_extra == {}


def test_get_events_parses_curator_and_participant_roles() -> None:
    payload = {
        "events": [
            {
                "id": 2545,
                "title": "Fest",
                "subdomain": "fest",
                "start_time": 1804896000000,
                "end_time": 1804896000000,
                "time": "future",
            }
        ],
        "data": [
            {
                "id": 2545,
                "er": "CURATOR",
                "t_title": "Solo defile",
            },
            {
                "id": 2545,
                "er": "REQ_AUTHOR",
                "r_id": 101,
                "number": 4,
                "status": "approved",
                "t_title": "Solo defile",
                "card_enabled": 1,
                "card_code": "D",
                "voting_number": 12,
                "voting_title": "Cosplay",
                "win": 1,
                "win_title": "1st place",
            },
        ],
    }

    with make_client(lambda request: json_response(payload)) as client:
        result = client.users.get_events(7)

    assert result.events[0].time is EventTime.FUTURE
    curator, author = result.roles
    assert curator.er is UserEventRoleType.CURATOR
    assert curator.t_title == "Solo defile"
    assert curator.model_extra == {}
    assert author.er is UserEventRoleType.REQ_AUTHOR
    assert author.r_id == 101
    assert author.status is RequestStatus.APPROVED
    assert author.card_enabled is True
    assert author.win == 1
    assert author.model_extra == {}
