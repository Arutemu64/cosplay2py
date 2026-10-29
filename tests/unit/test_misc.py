"""Resources defined in ``resources/misc.py``: pages, design, media and tickets."""

import json
from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any

import httpx2
import pytest

from cosplay2py import APIResponseValidationError, BadRequestError
from cosplay2py.models import EventRole, PageType
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


def test_etickets_get_paymethods() -> None:
    payload = {
        "etickets_paymethods": {
            "yookassa_allowed": True,
            "yookassa_enabled": "1",
            "yookassa_shop_id": "12345",
            "yookassa_api_key": "secret",
            "yookassa_vat_code": 1,
            "yandex_enabled": "0",
            "yandex_account": None,
            "yandex_secret": None,
            "manual_enabled": 1,
            "manual_text": "Send to card",
        }
    }

    with make_client(lambda request: json_response(payload)) as client:
        pm = client.etickets.get_paymethods()

    assert pm.yookassa_allowed is True
    assert pm.yookassa_enabled is True
    assert pm.yandex_enabled is False
    assert pm.manual_enabled is True
    assert pm.yookassa_vat_code == 1
    assert pm.model_extra == {}
