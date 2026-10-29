"""Resources defined in ``resources/misc.py``: pages, design, media and tickets."""

import json
from collections.abc import Callable
from typing import Any

import httpx2
import pytest

from cosplay2py import BadRequestError
from cosplay2py.models import PageType
from unit.conftest import ApiCall, json_response, make_client


def test_get_page() -> None:
    seen: list[httpx2.Request] = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        seen.append(request)
        return json_response(
            {
                "id": 12,
                "parent_id": 10,
                "event_id": 5,
                "type": "page",
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

    with make_client(handler) as client:
        page = client.pages.get(12)

    assert (page.id, page.parent_id, page.path) == (12, 10, "rules")
    assert page.show_in_menu is True
    assert page.content == "<p>Be nice</p>"
    assert page.model_extra == {}
    (request,) = seen
    assert request.url.path == "/api/pages/get_page"
    assert json.loads(request.content) == {"page_id": "12"}


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
