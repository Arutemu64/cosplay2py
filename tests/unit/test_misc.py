"""Resources defined in ``resources/misc.py``: pages, design, media and tickets."""

import json
from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any

import httpx2
import pytest

from cosplay2py import APIResponseValidationError, BadRequestError
from cosplay2py.models import (
    EventRole,
    PageType,
    TicketCreateMode,
    TicketKind,
    VotingType,
)
from unit.conftest import ApiCall, json_response, make_client


@pytest.mark.anyio
@pytest.mark.parametrize("page_type", list(PageType))
async def test_get_page(api: ApiCall, page_type: PageType) -> None:
    seen: list[httpx2.Request] = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        seen.append(request)
        return json_response(
            {
                "id": 12,
                "parent_id": 10,
                "event_id": 5,
                "type": str(page_type),
                "path": "rules",
                "show_in_menu": 1,
                "menu_title": "Rules",
                "title": "Festival rules",
                "order": 1,
                "source": None,
                "content": "<p>Be nice</p>",
                "right": 0,
            }
        )

    page = await api(handler, lambda c: c.pages.get(12))

    assert (page.id, page.parent_id, page.path) == (12, 10, "rules")
    assert page.show_in_menu is True
    assert page.right is EventRole.GUEST
    assert page.content == "<p>Be nice</p>"
    assert page.model_extra == {}
    assert page.type is page_type
    assert json.loads(page.model_dump_json())["type"] == page_type
    (request,) = seen
    assert request.url.path == "/api/pages/get_page"
    assert json.loads(request.content) == {"page_id": "12"}


def test_get_page_rejects_unknown_page_type() -> None:
    payload = {
        "id": 12,
        "type": "unknown_page_type",
        "path": "rules",
        "show_in_menu": 1,
        "title": "Festival rules",
        "right": 0,
    }
    with (
        make_client(lambda request: json_response(payload)) as client,
        pytest.raises(APIResponseValidationError),
    ):
        client.pages.get(12)


@pytest.mark.anyio
async def test_create_page(api: ApiCall) -> None:
    seen: list[httpx2.Request] = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        seen.append(request)
        return json_response({"message": "ok", "page_id": "13"})

    assert await api(handler, lambda c: c.pages.create(PageType.FOLDER)) == 13
    assert (
        await api(handler, lambda c: c.pages.create(PageType.LINK, parent_id=13)) == 13
    )

    assert [json.loads(r.content) for r in seen] == [
        {"parent_id": None, "type": "folder"},
        {"parent_id": 13, "type": "link"},
    ]
    assert {r.url.path for r in seen} == {"/api/pages/add_page"}


@pytest.mark.anyio
@pytest.mark.parametrize(
    ("call", "path", "body"),
    [
        (
            lambda c: c.pages.save_field(12, "menu_title", "Rules"),
            "save_page_field",
            {"id": 12, "field": "menu_title", "data": "Rules"},
        ),
        (
            lambda c: c.pages.save_fields(
                12, {"source": "<p>Hi</p>", "content": "<p>Hi</p>"}
            ),
            "save_page_fields",
            {
                "id": 12,
                "page_data": {"source": "<p>Hi</p>", "content": "<p>Hi</p>"},
            },
        ),
        (lambda c: c.pages.delete(12), "delete_page", {"id": 12}),
    ],
)
async def test_page_writes(
    api: ApiCall, call: Callable[[Any], Any], path: str, body: dict[str, object]
) -> None:
    seen: list[httpx2.Request] = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        seen.append(request)
        return json_response({"message": "ok"})

    assert await api(handler, call) is None

    (request,) = seen
    assert request.method == "POST"
    assert request.url.path == f"/api/pages/{path}"
    assert json.loads(request.content) == body


def test_delete_non_empty_folder() -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        return httpx2.Response(400, text="Сначала удалите вложенные страницы.")

    with make_client(handler) as client, pytest.raises(BadRequestError):
        client.pages.delete(10)


@pytest.mark.anyio
@pytest.mark.parametrize(
    ("call", "path", "body"),
    [
        (
            lambda c: c.design.save({"custom_css": "body {}"}),
            "event_design/save_design",
            {"custom_css": "body {}"},
        ),
        (
            lambda c: c.pages.reorder(12, 2),
            "pages/page_reorder",
            {
                "page_id": 12,
                "new_index": 2,
                "source_page_id": None,
                "target_page_id": None,
            },
        ),
        (
            lambda c: c.pages.reorder(12, 1, source_page_id=3, target_page_id=4),
            "pages/page_reorder",
            {"page_id": 12, "new_index": 1, "source_page_id": 3, "target_page_id": 4},
        ),
        (
            lambda c: c.media.add_album("Photographer", "https://vk.com/album1_2"),
            "media/photoalbum_add",
            {"user_title": "Photographer", "url": "https://vk.com/album1_2"},
        ),
        (
            lambda c: c.media.save_album_field(5, "user_title", "New Name"),
            "media/save_photoalbum_field",
            {"photoalbum_id": 5, "field": "user_title", "data": "New Name"},
        ),
        (
            lambda c: c.media.delete_album(5),
            "media/photoalbum_delete",
            {"photoalbum_id": 5},
        ),
        (
            lambda c: c.etickets.add_type(),
            "etickets/eticketstypes_add",
            {},
        ),
        (
            lambda c: c.etickets.delete_type(3),
            "etickets/eticketstypes_delete",
            {"etickets_type_id": 3},
        ),
        (
            lambda c: c.etickets.reorder_type(3, 1),
            "etickets/eticketstypes_reorder",
            {"etickets_type_id": 3, "new_index": 1},
        ),
        (
            lambda c: c.etickets.save_type_field(3, "price", 1500),
            "etickets/save_eticketstypes_field",
            {"etickets_type_id": 3, "field": "price", "data": 1500},
        ),
        (
            lambda c: c.etickets.delete(10),
            "etickets/delete",
            {"eticket_id": 10},
        ),
        (
            lambda c: c.etickets.save_personal_data(10, {"fio": "Ivan"}),
            "etickets/save_personal_data",
            {"eticket_id": "10", "user_data": {"fio": "Ivan"}},
        ),
        (
            lambda c: c.tickets.create(
                50, ticket_type=TicketKind.TEST, mode=TicketCreateMode.REPLACE
            ),
            "tickets/create",
            {"tickets_count": 50, "tickets_type": 1, "create_type": "replace"},
        ),
        (
            lambda c: c.tickets.save_prize_field(2, "title", "Plush"),
            "tickets/save_prize_field",
            {"prize_id": 2, "field": "title", "data": "Plush"},
        ),
        (
            lambda c: c.tickets.save_prize_handed(4, True),
            "tickets/save_prize_handed",
            {"prize_winner_id": 4, "data": 1},
        ),
        (
            lambda c: c.tickets.check_for_voting("123456"),
            "tickets/check_for_voting",
            {"ticket_number": "123456"},
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
@pytest.mark.parametrize("upload", [True, False])
async def test_design_images(api: ApiCall, upload: bool) -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        assert request.method == "POST"
        if upload:
            assert request.url.path == "/api/event_design/upload_image"
            assert "multipart/form-data" in request.headers["content-type"]
            assert b'name="eventimage"' in request.content
            assert b'filename="sample.png"' in request.content
            assert b"fake-image" in request.content
        else:
            assert request.url.path == "/api/event_design/delete_eventimage"
            assert json.loads(request.content) == {"eventimage": "sample.png"}
        return json_response({"message": "ok", "eventimages": {"2": "other.png"}})

    if upload:
        result = await api(
            handler, lambda c: c.design.upload_image(b"fake-image", "sample.png")
        )
    else:
        result = await api(handler, lambda c: c.design.delete_image("sample.png"))
    assert result == {2: "other.png"}


def test_media_get_data() -> None:
    payload = {
        "albums": [
            {
                "id": 678,
                "event_id": 1583,
                "user_title": "Photographer",
                "user_id": None,
                "url": "https://vk.com/album1_2",
                "time_add": "2026-10-29 16:58:11",
                "count": 42,
                "likes": 100,
                "recalc_time": None,
                "recalc_message": None,
            }
        ],
        "photos": [
            {
                "id": 1,
                "photoalbum_id": 678,
                "user_title": "Photographer",
                "likes": 15,
                "src": "https://example.com/thumb.jpg",
                "photo_url": "https://vk.com/photo1_2",
            }
        ],
    }

    with make_client(lambda request: json_response(payload)) as client:
        data = client.media.get_data()

    (album,) = data.albums
    assert album.id == 678
    assert album.time_add == datetime(2026, 10, 29, 16, 58, 11, tzinfo=UTC)
    assert album.model_extra == {}
    (photo,) = data.photos
    assert photo.likes == 15
    assert photo.model_extra == {}


@pytest.mark.anyio
@pytest.mark.parametrize(
    ("call", "path"),
    [
        (lambda c: c.design.delete_panel_logo(), "delete_panel_logo"),
        (lambda c: c.design.delete_header_logo(), "delete_header_logo"),
        (lambda c: c.design.delete_site_background(), "delete_site_background"),
    ],
)
async def test_design_delete_logos(
    api: ApiCall, call: Callable[[Any], Any], path: str
) -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        assert request.method == "GET"
        assert request.url.path == f"/api/event_design/{path}"
        return json_response({"message": "ok"})

    assert await api(handler, call) is None


@pytest.mark.anyio
async def test_etickets_endpoints(api: ApiCall) -> None:
    def types_handler(request: httpx2.Request) -> httpx2.Response:
        assert request.method == "POST"
        assert request.url.path == "/api/etickets/get_types"
        assert json.loads(request.content) == {"i_can_buy": True}
        return json_response({"etickets_types": [{"id": 1}]})

    assert await api(types_handler, lambda c: c.etickets.get_types(i_can_buy=True)) == [
        {"id": 1}
    ]

    def create_handler(request: httpx2.Request) -> httpx2.Response:
        assert request.url.path == "/api/etickets/create_ticket"
        assert json.loads(request.content) == {"etickets_type_id": 3}
        return json_response({"message": "ok", "eticket_id": "10"})

    assert await api(create_handler, lambda c: c.etickets.create(3)) == 10

    def get_handler(request: httpx2.Request) -> httpx2.Response:
        assert request.url.path == "/api/etickets/get_ticket"
        assert json.loads(request.content) == {"eticket_id": "10"}
        return json_response({"eticket": {"id": 10}})

    assert await api(get_handler, lambda c: c.etickets.get(10)) == {
        "eticket": {"id": 10}
    }

    def status_handler(request: httpx2.Request) -> httpx2.Response:
        assert request.url.path == "/api/etickets/get_ticket_status"
        assert json.loads(request.content) == {"eticket_id": "10"}
        return json_response({"eticket_status": {"paid": 1}})

    assert await api(status_handler, lambda c: c.etickets.get_status(10)) == {"paid": 1}

    def save_handler(request: httpx2.Request) -> httpx2.Response:
        assert request.url.path == "/api/etickets/save_eticket_field"
        assert json.loads(request.content) == {
            "eticket_id": 10,
            "field": "paid",
            "data": 1,
        }
        return json_response({"message": "ok", "eticket": {"id": 10, "paid": 1}})

    assert await api(save_handler, lambda c: c.etickets.save_field(10, "paid", 1)) == {
        "id": 10,
        "paid": 1,
    }


@pytest.mark.anyio
async def test_tickets_endpoints(api: ApiCall) -> None:
    def clear_handler(request: httpx2.Request) -> httpx2.Response:
        assert request.method == "POST"
        assert request.url.path == "/api/tickets/clear_votes"
        return json_response({"message": "ok"})

    assert await api(clear_handler, lambda c: c.tickets.clear_votes()) is None

    def add_prize_handler(request: httpx2.Request) -> httpx2.Response:
        assert request.url.path == "/api/tickets/prize_add"
        assert json.loads(request.content) == {"title": "Mug", "quantity": 5}
        return json_response({"prizes": [{"id": 1}], "prize_step_recommend": 10})

    assert await api(add_prize_handler, lambda c: c.tickets.add_prize("Mug", 5)) == {
        "prizes": [{"id": 1}],
        "prize_step_recommend": 10,
    }

    def del_prize_handler(request: httpx2.Request) -> httpx2.Response:
        assert request.url.path == "/api/tickets/prize_del"
        assert json.loads(request.content) == {"prize_id": 1}
        return json_response({"prizes": [], "prize_step_recommend": 0})

    assert await api(del_prize_handler, lambda c: c.tickets.delete_prize(1)) == {
        "prizes": [],
        "prize_step_recommend": 0,
    }

    def ticket_handler(request: httpx2.Request) -> httpx2.Response:
        assert request.method == "GET"
        assert request.url.path == "/api/tickets/get_ticket"
        return json_response({"ticket_number": "123456"})

    assert await api(ticket_handler, lambda c: c.tickets.get_ticket()) == {
        "ticket_number": "123456"
    }

    def voting_data_handler(request: httpx2.Request) -> httpx2.Response:
        assert request.url.path == "/api/tickets/get_voting_data"
        assert json.loads(request.content) == {
            "ticket_number": "123456",
            "voting_type": "test",
        }
        return json_response({"topics": [], "requests": []})

    assert await api(
        voting_data_handler,
        lambda c: c.tickets.get_voting_data("123456", voting_type=VotingType.TEST),
    ) == {"topics": [], "requests": []}

    def cards_handler(request: httpx2.Request) -> httpx2.Response:
        assert request.method == "GET"
        assert request.url.path == "/api/tickets/get_cards"
        return json_response({"requests": [{"id": 42}]})

    assert await api(cards_handler, lambda c: c.tickets.get_cards()) == [{"id": 42}]

    def select_handler(request: httpx2.Request) -> httpx2.Response:
        assert request.url.path == "/api/tickets/select_winner"
        assert json.loads(request.content) == {
            "ticket_number": "123456",
            "topic_id": 7,
            "winner_index": 0,
            "request_id": 42,
            "voting_type": "normal",
        }
        return json_response({"message": "ok", "prize": None})

    assert await api(
        select_handler,
        lambda c: c.tickets.select_winner("123456", 7, 0, 42),
    ) == {"prize": None}


@pytest.mark.parametrize(
    ("bad_type", "exc"), [(True, TypeError), (0, ValueError), (3, ValueError)]
)
def test_create_tickets_rejects_invalid_ticket_type(
    bad_type: Any, exc: type[Exception]
) -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        raise AssertionError("no request expected")

    with make_client(handler) as client, pytest.raises(exc):
        client.tickets.create(10, ticket_type=bad_type)


@pytest.mark.anyio
async def test_cards_endpoints(api: ApiCall) -> None:
    def topics_cards_handler(request: httpx2.Request) -> httpx2.Response:
        assert request.method == "GET"
        assert request.url.path == "/api/cards/get_topics_and_cards"
        assert dict(request.url.params) == {"preview": "1"}
        return json_response({"topics": [], "requests": []})

    assert await api(
        topics_cards_handler,
        lambda c: c.cards.get_topics_and_cards(preview=True),
    ) == {"topics": [], "requests": []}

    def card_handler(request: httpx2.Request) -> httpx2.Response:
        assert request.method == "GET"
        assert request.url.path == "/api/cards/get_card"
        assert dict(request.url.params) == {"request_id": "42", "preview": "1"}
        return json_response({"request": {"id": 42}})

    assert await api(card_handler, lambda c: c.cards.get_card(42, preview=True)) == {
        "request": {"id": 42}
    }

    def topics_reqs_handler(request: httpx2.Request) -> httpx2.Response:
        assert request.method == "GET"
        assert request.url.path == "/api/cards/get_topics_and_requests"
        assert dict(request.url.params) == {}
        return json_response({"topics": [], "requests": []})

    assert await api(
        topics_reqs_handler, lambda c: c.cards.get_topics_and_requests()
    ) == {"topics": [], "requests": []}

    def req_handler(request: httpx2.Request) -> httpx2.Response:
        assert request.method == "GET"
        assert request.url.path == "/api/cards/get_request"
        assert dict(request.url.params) == {"request_id": "42"}
        return json_response({"request": {"id": 42}})

    assert await api(req_handler, lambda c: c.cards.get_request(42)) == {
        "request": {"id": 42}
    }
