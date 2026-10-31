import json
from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any

import httpx2
import pytest

from cosplay2py.models import (
    BlankId,
    Deadline,
    EventWinner,
    EventWinners,
    PlanNodeType,
    RequestStatus,
    Topic,
)
from unit.conftest import ApiCall, json_response, make_client


def test_parses_reg_topics() -> None:
    seen: list[httpx2.Request] = []
    participant = {
        "user_id": 7,
        "display_name": "Neko",
        "fio": "-",
        "city": "Moscow",
        "phone": "+70000000000",
        "requests": [{"request_id": 100, "number": 3}],
    }

    def handler(request: httpx2.Request) -> httpx2.Response:
        seen.append(request)
        return json_response(
            {
                "title": "T",
                "data": [
                    {
                        "topic_id": 1,
                        "topic_name": "A",
                        "participants": [participant],
                    },
                    {"topic_id": 2, "topic_name": "B", "participants": None},
                ],
            }
        )

    with make_client(handler) as client:
        report = client.events.get_reg_topics(req_approved=False)

    first, empty = report.data
    assert first.participants[0].requests[0].number == 3
    assert empty.participants == []
    assert json.loads(seen[0].content)["blank_id"] == "reg_topics"
    assert json.loads(seen[0].content)["req_approved"] is False


def test_blank_status_filters_sent_only_when_set() -> None:
    seen: list[httpx2.Request] = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        seen.append(request)
        return json_response({"title": "T", "data": []})

    with make_client(handler) as client:
        client.events.get_reg_topics(req_disapproved=True)
        client.events.get_reg_topics(req_disapproved=True, req_other=True)

    assert [json.loads(r.content) for r in seen] == [
        {
            "blank_id": "reg_topics",
            "req_approved": True,
            "req_disapproved": True,
            "picture_height": 80,
        },
        {
            "blank_id": "reg_topics",
            "req_approved": True,
            "req_disapproved": True,
            "req_other": True,
            "picture_height": 80,
        },
    ]


def test_parses_reg_alphabet_numeric_strings() -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        return json_response(
            {
                "title": "T",
                "data": [
                    {
                        "user_id": "23295",
                        "display_name": "Neko",
                        "fio": "-",
                        "requests": [{"request_id": 100, "number": 3}],
                        "city": "Moscow",
                        "phone": "+70000000000",
                        "onscene_count": "0",
                        "offscene_count": "1",
                    }
                ],
            }
        )

    with make_client(handler) as client:
        (row,) = client.events.get_reg_alphabet().data

    assert row.user_id == 23295
    assert (row.onscene_count, row.offscene_count) == (0, 1)


@pytest.mark.parametrize("blank_id", [BlankId.REG_TOPICS, BlankId.REG_ALPHABET])
def test_get_blank_rejects_data_reports(blank_id: BlankId) -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        raise AssertionError("no request expected")

    with (
        make_client(handler) as client,
        pytest.raises(ValueError, match="get_reg_"),
    ):
        client.events.get_blank(blank_id)


def test_set_deadline() -> None:
    seen: list[httpx2.Request] = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        seen.append(request)
        return json_response({"message": "ok"})

    with make_client(handler) as client:
        client.events.set_deadline(
            7,
            Deadline.ADDONS_CLOSE,
            datetime(2025, 8, 13, 23, 58),  # noqa: DTZ001
        )
        client.events.set_deadline(
            [7, 8],
            Deadline.VOTING_OPEN,
            datetime(2025, 8, 1, 9, 5, 30),  # noqa: DTZ001
        )

    single, bulk = seen
    assert single.url.path == bulk.url.path == "/api/events/set_gate"
    assert json.loads(single.content) == {
        "topic_id": 7,
        "datetype": "time_addons_close",
        "data": "13.08.25 23:58",
    }
    assert json.loads(bulk.content) == {
        "dates": [
            {
                "topic_id": 7,
                "datetype": "time_voting_open",
                "data": "01.08.25 09:05",
            },
            {
                "topic_id": 8,
                "datetype": "time_voting_open",
                "data": "01.08.25 09:05",
            },
        ]
    }


def test_set_deadline_rejects_aware_datetime() -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        raise AssertionError("no request expected")

    with (
        make_client(handler) as client,
        pytest.raises(ValueError, match="naive"),
    ):
        client.events.set_deadline(
            7, Deadline.ADDONS_CLOSE, datetime(2025, 8, 13, tzinfo=UTC)
        )


def test_parses_nested_json_strings() -> None:
    plan = [{"type": "day", "title": "Day 1", "date_start": 1787367600000, "nodes": []}]

    def handler(request: httpx2.Request) -> httpx2.Response:
        return json_response({"message": "ok", "plan": json.dumps(plan)})

    with make_client(handler) as client:
        (day,) = client.events.get_plan()

    assert day.type is PlanNodeType.DAY
    assert day.date_start == datetime(2026, 8, 22, 3, tzinfo=UTC)


def test_save_plan_round_trips() -> None:
    plan = [
        {
            "uid": "d1",
            "type": "day",
            "title": "День 1",
            "date_start": 1787367600000,
            "sum_count": 1,
            "nodes": [
                {
                    "uid": "r1",
                    "type": "request",
                    "request_id": 5,
                    "status": "approved",
                    "request_length": 1.5,
                    "time_start": 1787385600000,
                    "time_end": 1787385690000,
                    "distance": -600000,
                    "members": [
                        {
                            "request_id": 5,
                            "title": "Nick",
                            "uid": "m1",
                            "distance": -600000,
                            "intersections": [
                                {
                                    "uid": "i1",
                                    "request_id": 6,
                                    "title": "Other",
                                    "status": "approved",
                                    "topic_id": 2,
                                    "card_code": "D",
                                    "distance": -600000,
                                }
                            ],
                            "$$hashKey": "object:12",
                        }
                    ],
                }
            ],
        }
    ]
    seen: list[httpx2.Request] = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        seen.append(request)
        if request.url.path == "/api/events/get_plan":
            return json_response({"message": "ok", "plan": json.dumps(plan)})
        return json_response({"message": "ok"})

    with make_client(handler) as client:
        parsed_plan = client.events.get_plan()
        (intersection,) = parsed_plan[0].nodes[0].members[0].intersections
        assert intersection.request_id == 6
        assert intersection.status is RequestStatus.APPROVED
        assert intersection.model_extra == {}
        client.events.save_plan(parsed_plan)

    saved = seen[-1]
    assert saved.method == "POST"
    assert saved.url.path == "/api/events/save_plan"
    body = json.loads(saved.content)
    assert list(body) == ["plan"]
    assert "День" in body["plan"]
    dumped = json.loads(body["plan"])
    assert "$$hashKey" not in dumped[0]["nodes"][0]["members"][0]
    del plan[0]["nodes"][0]["members"][0]["$$hashKey"]
    assert dumped == plan


def test_search() -> None:
    seen: list[httpx2.Request] = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        seen.append(request)
        return json_response({"events": [{"id": 29, "title": "Some Fest"}]})

    with make_client(handler) as client:
        (event,) = client.events.search("fest")

    assert (event.id, event.title) == (29, "Some Fest")
    (request,) = seen
    assert request.url.path == "/api/events/search"
    assert json.loads(request.content) == {"query": "fest"}


@pytest.mark.anyio
async def test_observed_event_state(api):
    import json
    from pathlib import Path

    payload = json.loads(
        (Path(__file__).parents[1] / "fixtures" / "event_state.json").read_text("utf-8")
    )
    result = await api(
        lambda request: json_response(payload), lambda c: c.events.get_state()
    )
    assert result.topics_count == 1
    assert result.requests_total == 6


@pytest.mark.anyio
async def test_get_winners(api: ApiCall) -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        assert request.method == "GET"
        assert request.url.path == "/api/events/winners"
        return json_response(
            {
                "topics": [
                    {
                        "id": 1,
                        "event_id": 2,
                        "url_code": "solo",
                        "voting_group": 0,
                        "voting_public": 0,
                        "voting_jury": 1,
                        "print_badges": 1,
                        "card_enabled": 1,
                        "default_duration": 2.5,
                        "public_requests": "NO",
                        "card_code": "S",
                        "title": "Solo",
                        "order": 0,
                    }
                ],
                "winners": [
                    {
                        "id": 10,
                        "topic_id": 1,
                        "number": 3,
                        "voting_number": 103,
                        "voting_title": "Example entry",
                        "win": 1,
                        "win_title": None,
                    }
                ],
            }
        )

    result = await api(handler, lambda c: c.events.get_winners())
    assert isinstance(result, EventWinners)
    assert isinstance(result.topics[0], Topic)
    assert result.topics[0].title == "Solo"
    assert isinstance(result.winners[0], EventWinner)
    assert result.winners[0].id == 10
    assert result.winners[0].topic_id == result.topics[0].id
    assert result.winners[0].voting_number == 103
    assert result.winners[0].win == 1
    assert result.winners[0].win_title is None


@pytest.mark.anyio
@pytest.mark.parametrize(
    ("call", "path", "body"),
    [
        (
            lambda c: c.events.save_setting("short_title", "FF"),
            "save_setting",
            {"event_field": "short_title", "data": "FF"},
        ),
        (lambda c: c.events.add_org(42), "add_org", {"user_id": 42}),
        (lambda c: c.events.delete_org(42), "delete_org", {"user_id": 42}),
        (lambda c: c.events.change_main_org(42), "change_mainorg", {"user_id": 42}),
        (
            lambda c: c.events.add_curator(42, 7),
            "add_curator",
            {"user_id": 42, "topic_id": 7},
        ),
        (
            lambda c: c.events.delete_curator(42, 7),
            "delete_curator",
            {"user_id": 42, "topic_id": 7},
        ),
    ],
)
async def test_event_writes(
    api: ApiCall, call: Callable[[Any], Any], path: str, body: dict[str, object]
) -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        assert request.method == "POST"
        assert request.url.path == f"/api/events/{path}"
        assert json.loads(request.content) == body
        return json_response({"message": "ok"})

    assert await api(handler, call) is None
