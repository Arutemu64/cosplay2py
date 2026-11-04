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
    PublicRequestDetails,
    PublicRequests,
    RequestStatus,
    TicketCreateMode,
    TicketKind,
    TopicsAndRequests,
    VotingType,
)
from unit.conftest import TOPIC, ApiCall, json_response

pytestmark = pytest.mark.anyio


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


async def test_get_page_rejects_unknown_page_type(api: ApiCall) -> None:
    payload = {
        "id": 12,
        "type": "unknown_page_type",
        "path": "rules",
        "show_in_menu": 1,
        "title": "Festival rules",
        "right": 0,
    }
    with pytest.raises(APIResponseValidationError):
        await api(lambda request: json_response(payload), lambda c: c.pages.get(12))


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


async def test_delete_non_empty_folder(api: ApiCall) -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        return httpx2.Response(400, text="Сначала удалите вложенные страницы.")

    with pytest.raises(BadRequestError):
        await api(handler, lambda c: c.pages.delete(10))


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


async def test_design_get(api: ApiCall) -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        assert request.method == "GET"
        assert request.url.path == "/api/event_design/get"
        return json_response(
            {"design": {"custom_css": "body {}", "content_opacity": 0.9}}
        )

    design = await api(handler, lambda c: c.design.get())
    assert design.custom_css == "body {}"
    assert design.content_opacity == 0.9
    assert design.model_extra == {}


async def test_design_get_images(api: ApiCall) -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        assert request.method == "GET"
        assert request.url.path == "/api/event_design/get_eventimages"
        return json_response({"eventimages": {"1": "header.png"}})

    assert await api(handler, lambda c: c.design.get_images()) == {1: "header.png"}


async def test_media_get_data(api: ApiCall) -> None:
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

    data = await api(
        lambda request: json_response(payload), lambda c: c.media.get_data()
    )

    (album,) = data.albums
    assert album.id == 678
    assert album.time_add == datetime(2026, 10, 29, 16, 58, 11, tzinfo=UTC)
    assert album.model_extra == {}
    (photo,) = data.photos
    assert photo.likes == 15
    assert photo.model_extra == {}


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


async def test_etickets_get_list(api: ApiCall) -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        assert request.method == "GET"
        assert request.url.path == "/api/etickets/get_list"
        return json_response({"etickets": [{"id": 10}]})

    assert await api(handler, lambda c: c.etickets.get_list()) == [{"id": 10}]


@pytest.mark.parametrize("i_can_buy", [False, True])
async def test_etickets_get_types(api: ApiCall, i_can_buy: bool) -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        assert request.url.path == "/api/etickets/get_types"
        if i_can_buy:
            assert request.method == "POST"
            assert json.loads(request.content) == {"i_can_buy": True}
        else:
            assert request.method == "GET"
        return json_response({"etickets_types": [{"id": 1}]})

    assert await api(handler, lambda c: c.etickets.get_types(i_can_buy=i_can_buy)) == [
        {"id": 1}
    ]


async def test_etickets_create(api: ApiCall) -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        assert request.url.path == "/api/etickets/create_ticket"
        assert json.loads(request.content) == {"etickets_type_id": 3}
        return json_response({"message": "ok", "eticket_id": "10"})

    assert await api(handler, lambda c: c.etickets.create(3)) == 10


async def test_etickets_get(api: ApiCall) -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        assert request.url.path == "/api/etickets/get_ticket"
        assert json.loads(request.content) == {"eticket_id": "10"}
        return json_response({"eticket": {"id": 10}})

    assert await api(handler, lambda c: c.etickets.get(10)) == {"eticket": {"id": 10}}


async def test_etickets_get_status(api: ApiCall) -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        assert request.url.path == "/api/etickets/get_ticket_status"
        assert json.loads(request.content) == {"eticket_id": "10"}
        return json_response({"eticket_status": {"paid": 1}})

    assert await api(handler, lambda c: c.etickets.get_status(10)) == {"paid": 1}


async def test_etickets_save_field(api: ApiCall) -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        assert request.url.path == "/api/etickets/save_eticket_field"
        assert json.loads(request.content) == {
            "eticket_id": 10,
            "field": "paid",
            "data": 1,
        }
        return json_response({"message": "ok", "eticket": {"id": 10, "paid": 1}})

    assert await api(handler, lambda c: c.etickets.save_field(10, "paid", 1)) == {
        "id": 10,
        "paid": 1,
    }


async def test_tickets_statistics(api: ApiCall) -> None:
    def stat_handler(request: httpx2.Request) -> httpx2.Response:
        assert request.method == "GET"
        assert request.url.path == "/api/tickets/get_statistic"
        return json_response({"active_count": 10, "test_tickets": []})

    stat = await api(stat_handler, lambda c: c.tickets.get_statistic())
    assert stat.active_count == 10

    def voting_stat_handler(request: httpx2.Request) -> httpx2.Response:
        assert request.method == "GET"
        assert request.url.path == "/api/tickets/get_voting_statistics"
        return json_response({"votes_accepted": 5, "active_tickets": 3})

    voting_stat = await api(
        voting_stat_handler, lambda c: c.tickets.get_voting_statistics()
    )
    assert voting_stat.votes_accepted == 5
    assert voting_stat.active_tickets == 3


async def test_tickets_clear_votes(api: ApiCall) -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        assert request.method == "POST"
        assert request.url.path == "/api/tickets/clear_votes"
        return json_response({"message": "ok"})

    assert await api(handler, lambda c: c.tickets.clear_votes()) is None


@pytest.mark.parametrize(
    ("call", "path", "body"),
    [
        (
            lambda c: c.tickets.add_prize("Mug", 5),
            "prize_add",
            {"title": "Mug", "quantity": 5},
        ),
        (
            lambda c: c.tickets.delete_prize(1),
            "prize_del",
            {"prize_id": 1},
        ),
    ],
)
async def test_tickets_prizes(
    api: ApiCall, call: Callable[[Any], Any], path: str, body: dict[str, object]
) -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        assert request.url.path == f"/api/tickets/{path}"
        assert json.loads(request.content) == body
        return json_response({"prizes": [], "prize_step_recommend": 10})

    assert await api(handler, call) == {"prizes": [], "prize_step_recommend": 10}


async def test_tickets_get_ticket_and_cards(api: ApiCall) -> None:
    def ticket_handler(request: httpx2.Request) -> httpx2.Response:
        assert request.method == "GET"
        assert request.url.path == "/api/tickets/get_ticket"
        return json_response({"ticket_number": "123456"})

    assert await api(ticket_handler, lambda c: c.tickets.get_ticket()) == {
        "ticket_number": "123456"
    }

    def cards_handler(request: httpx2.Request) -> httpx2.Response:
        assert request.method == "GET"
        assert request.url.path == "/api/tickets/get_cards"
        return json_response({"requests": [{"id": 42}]})

    assert await api(cards_handler, lambda c: c.tickets.get_cards()) == [{"id": 42}]


async def test_tickets_voting_flow(api: ApiCall) -> None:
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
async def test_create_tickets_rejects_invalid_ticket_type(
    api: ApiCall, bad_type: Any, exc: type[Exception]
) -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        raise AssertionError("no request expected")

    with pytest.raises(exc):
        await api(handler, lambda c: c.tickets.create(10, ticket_type=bad_type))


async def test_cards_get_topics_and_cards_preview(api: ApiCall) -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        assert request.method == "GET"
        assert request.url.path == "/api/cards/get_topics_and_cards"
        assert dict(request.url.params) == {"preview": "1"}
        return json_response({"topics": [], "requests": []})

    result = await api(
        handler,
        lambda c: c.cards.get_topics_and_cards(preview=True),
    )
    assert result.topics == []
    assert result.requests == []


@pytest.mark.parametrize("preview", [False, True])
async def test_cards_get_card(api: ApiCall, preview: bool) -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        assert request.method == "GET"
        assert request.url.path == "/api/cards/get_card"
        expected_params = {"request_id": "42", **({"preview": "1"} if preview else {})}
        assert dict(request.url.params) == expected_params
        return json_response(
            {
                "message": "ok",
                "request": {
                    "id": 42,
                    "event_id": 10,
                    "topic_id": 1,
                    "user_id": 7,
                    "number": 2,
                    "status": "approved",
                },
                "topic": TOPIC,
                "sections": [
                    {
                        "id": 100,
                        "topic_id": 1,
                        "title": "Participant",
                        "order": 0,
                        "max_repeat": 1,
                        "visible_to_all": 1,
                        "registration_blanks": 1,
                        "image_section": "0",
                        "user_section": "1",
                    }
                ],
                "fields": [],
                "reqsections": [],
                "reqvalues": [],
                "badges": [
                    {"request_section_id": 3, "card": "s2", "another_requests": "d4"},
                    {"request_section_id": 4, "card": "s2", "another_requests": None},
                ],
                "users": [
                    {"id": 7, "title": "Example", "image_update_time": 1700000000}
                ],
            }
        )

    card = await api(handler, lambda c: c.cards.get_card(42, preview=preview))
    assert card.request.id == 42
    assert card.sections[0].image_section is False
    assert card.sections[0].user_section is True
    assert card.badges[0].another_requests == "d4"
    assert card.badges[1].another_requests is None
    assert card.users[0].image_update_time == datetime.fromtimestamp(1700000000, UTC)
    assert card.request_sections == card.values == []
    assert card.model_extra == {}


async def test_cards_get_topics_and_requests(api: ApiCall) -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        assert request.method == "GET"
        assert request.url.path == "/api/cards/get_topics_and_requests"
        assert dict(request.url.params) == {}
        return json_response(
            {
                "message": "ok",
                "topics": [
                    {"id": 1, "url_code": "solo", "card_code": "s", "title": "Solo"}
                ],
                "requests": [
                    {
                        "id": 42,
                        "topic_id": 1,
                        "user_id": 7,
                        "number": 2,
                        "status": "approved",
                        "public_requests": "WITHSTATUS",
                        "voting_number": 3,
                        "voting_title": "Example",
                    },
                    {
                        "id": 43,
                        "topic_id": 1,
                        "user_id": 8,
                        "number": 3,
                        "status": "new",
                        "public_requests": "WITHOUTSTATUS",
                        "voting_number": None,
                        "voting_title": None,
                    },
                ],
            }
        )

    listing = await api(handler, lambda c: c.cards.get_topics_and_requests())
    assert isinstance(listing, TopicsAndRequests)
    assert listing.topics[0].url_code == "solo"
    assert listing.requests[0].status is RequestStatus.APPROVED
    assert listing.requests[0].public_requests is PublicRequests.WITH_STATUS
    assert listing.requests[0].voting_number == 3
    assert listing.requests[1].voting_number is None
    assert listing.requests[1].voting_title is None
    assert listing.model_extra == listing.requests[0].model_extra == {}

    empty = await api(
        lambda request: json_response({"topics": [], "requests": []}),
        lambda c: c.cards.get_topics_and_requests(),
    )
    assert empty.topics == empty.requests == []


async def test_cards_get_request(api: ApiCall) -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        assert request.method == "GET"
        assert request.url.path == "/api/cards/get_request"
        assert dict(request.url.params) == {"request_id": "42"}
        return json_response(
            {
                "message": "ok",
                "request": {
                    "id": 42,
                    "event_id": 10,
                    "topic_id": 1,
                    "user_id": 7,
                    "number": 2,
                    "status": "approved",
                    "creation_time": "2026-01-01 12:00:00",
                    "edit_enabled": False,
                    "friendedit_enabled": True,
                    "ER": 5,
                },
                "topic": TOPIC,
                "sections": [],
                "fields": [],
                "reqsections": [
                    {"id": 3, "request_id": 42, "topic_section_id": 100, "order": 0}
                ],
                "reqvalues": [
                    {
                        "id": 4,
                        "request_id": 42,
                        "request_section_id": 3,
                        "topic_field_id": 200,
                        "value": "Example",
                        "update_time": "2026-01-01 12:00:00",
                        "user_id": 7,
                    }
                ],
                "users": [
                    {"id": 7, "title": "Example", "image_update_time": 1700000000}
                ],
            }
        )

    detail = await api(handler, lambda c: c.cards.get_request(42))
    assert isinstance(detail, PublicRequestDetails)
    assert detail.request.er is EventRole.ORG
    assert detail.request.edit_enabled is False
    assert detail.request_sections[0].topic_section_id == 100
    assert detail.values[0].value == "Example"
    assert detail.values[0].update_time == datetime(2026, 1, 1, 12, tzinfo=UTC)
    assert detail.users[0].image_update_time == datetime.fromtimestamp(1700000000, UTC)
    assert detail.model_extra == detail.request.model_extra == {}


async def test_card_listing_types(api: ApiCall) -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        assert dict(request.url.params) == {}
        return json_response(
            {
                "topics": [
                    {"id": 1, "url_code": "solo", "card_code": "s", "title": "Solo"}
                ],
                "requests": [
                    {
                        "id": 42,
                        "topic_id": 1,
                        "voting_number": 2,
                        "voting_title": "Example",
                        "win": None,
                        "user_id": 7,
                        "image": {
                            "filename": 1700000000,
                            "original": {"width": 800, "height": 600},
                        },
                    },
                    {"id": 43, "topic_id": 1, "image": None},
                ],
            }
        )

    result = await api(handler, lambda c: c.cards.get_topics_and_cards())
    assert result.topics[0].card_code == "s"
    image = result.requests[0].image
    assert image is not None
    assert image.original is not None
    assert image.original.width == 800
    assert result.requests[1].image is None
    assert result.requests[0].model_extra == {}
