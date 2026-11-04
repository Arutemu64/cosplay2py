"""Offline MCP protocol tests; skipped when the optional extra is absent."""

import json
from collections.abc import AsyncGenerator, Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from typing import Any

import httpx2
import pytest

pytest.importorskip("fastmcp")

from fastmcp import Client

from cosplay2py import mcp
from unit.conftest import TOPIC, Handler, json_response, make_async_client

pytestmark = pytest.mark.anyio

type McpProtocol = Callable[..., AbstractAsyncContextManager[Any]]


@pytest.fixture
def anyio_backend() -> str:
    # FastMCP's client uses asyncio internally; the library still tests both backends.
    return "asyncio"


@pytest.fixture
def mcp_protocol(monkeypatch: pytest.MonkeyPatch) -> McpProtocol:
    @asynccontextmanager
    async def open_protocol(
        handler: Handler, *, max_retries: int = 2
    ) -> AsyncGenerator[Any]:
        client = make_async_client(handler, max_retries=max_retries)
        monkeypatch.setattr(mcp, "AsyncCosplay2", lambda: client)
        try:
            async with Client(mcp.create_server()) as protocol:
                yield protocol
        finally:
            await client._http.aclose()

    return open_protocol


async def test_discovery_and_lifecycle(monkeypatch: pytest.MonkeyPatch) -> None:
    client = make_async_client(lambda r: json_response({}))
    monkeypatch.setattr(mcp, "AsyncCosplay2", lambda: client)
    client._owns_http = True
    assert not client._http.is_closed
    server = mcp.create_server()
    assert server.name == "cosplay2_mcp"
    async with Client(server) as protocol:
        tools = await protocol.list_tools()
        assert {t.name for t in tools} == {
            "cosplay2_get_event_settings",
            "cosplay2_get_event_state",
            "cosplay2_list_topic_deadlines",
            "cosplay2_list_topic_statistics",
            "cosplay2_list_topics",
            "cosplay2_get_topic_form",
            "cosplay2_list_topic_requests",
            "cosplay2_list_all_requests",
            "cosplay2_search_requests",
            "cosplay2_get_request",
            "cosplay2_list_request_comments",
            "cosplay2_list_pages",
            "cosplay2_get_page",
            "cosplay2_get_schedule",
            "cosplay2_get_winners",
        }
        for tool in tools:
            assert tool.annotations.title
            assert tool.annotations.read_only_hint is True
            assert tool.annotations.destructive_hint is False
            assert tool.annotations.idempotent_hint is True
            assert tool.annotations.open_world_hint is True
            assert tool.output_schema
            properties = tool.input_schema.get("properties", {})
            assert "ctx" not in properties
            for prop_schema in properties.values():
                assert prop_schema.get("description")
            assert "api_secret" not in json.dumps(tool.input_schema)
    assert client._http.is_closed


async def test_pagination(mcp_protocol: McpProtocol) -> None:
    seen: list[httpx2.Request] = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        seen.append(request)
        return json_response([TOPIC, {**TOPIC, "id": 2}])

    async with mcp_protocol(handler) as protocol:
        first = await protocol.call_tool("cosplay2_list_topics", {"limit": 1})
        assert first.structured_content["total"] == 2
        assert first.structured_content["next_offset"] == 1
        assert first.structured_content["items"][0]["id"] == 1
        last = await protocol.call_tool(
            "cosplay2_list_topics", {"offset": 1, "limit": 1}
        )
        assert last.structured_content["next_offset"] is None
        assert last.structured_content["items"][0]["id"] == 2
        empty = await protocol.call_tool("cosplay2_list_topics", {"offset": 10})
        assert empty.structured_content["items"] == []
    assert all(r.url.path == "/api/topics/get_list" for r in seen)


@pytest.mark.parametrize(
    ("name", "arguments"),
    [
        ("cosplay2_list_topics", {"limit": 101}),
        ("cosplay2_list_topics", {"offset": -1}),
        ("cosplay2_search_requests", {"query": ""}),
        ("cosplay2_get_request", {"request_id": 0}),
        ("cosplay2_list_all_requests", {"status": "invalid"}),
        ("cosplay2_list_all_requests", {"topic_id": 0}),
        ("cosplay2_get_page", {"page_id": 0}),
    ],
)
async def test_validation(
    mcp_protocol: McpProtocol, name: str, arguments: dict[str, Any]
) -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        pytest.fail("Invalid input must not reach the API")

    async with mcp_protocol(handler) as protocol:
        result = await protocol.call_tool(name, arguments, raise_on_error=False)
        assert result.is_error


@pytest.mark.parametrize(
    ("status_code", "expected"),
    [
        (401, "Authentication failed (HTTP 401)"),
        (403, "Permission denied (HTTP 403)"),
        (404, "Resource not found or invalid identifier (HTTP 404)"),
        (429, "Rate limit exceeded (HTTP 429)"),
        (500, "Cosplay2 API request failed"),
    ],
)
async def test_error_redaction(
    mcp_protocol: McpProtocol, status_code: int, expected: str
) -> None:
    async with mcp_protocol(
        lambda r: json_response({"secret": "private"}, status_code), max_retries=0
    ) as protocol:
        result = await protocol.call_tool(
            "cosplay2_get_event_state", raise_on_error=False
        )
        assert result.is_error
        text = str(result.content)
        assert expected in text
        assert "private" not in text


@pytest.mark.parametrize(
    ("exc", "expected"),
    [
        (httpx2.ReadTimeout("timeout"), "Cosplay2 API request timed out"),
        (httpx2.ConnectError("refused"), "Could not connect to the Cosplay2 API"),
    ],
)
async def test_transport_and_validation_errors(
    mcp_protocol: McpProtocol, exc: Exception, expected: str
) -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        raise exc

    async with mcp_protocol(handler, max_retries=0) as protocol:
        result = await protocol.call_tool(
            "cosplay2_get_event_state", raise_on_error=False
        )
        assert result.is_error
        assert expected in str(result.content)


async def test_response_validation_error_redaction(
    mcp_protocol: McpProtocol,
) -> None:
    async with mcp_protocol(
        lambda r: json_response({"state": {"secret": "private"}}), max_retries=0
    ) as protocol:
        result = await protocol.call_tool(
            "cosplay2_get_event_state", raise_on_error=False
        )
        assert result.is_error
        text = str(result.content)
        assert "unexpected payload shape" in text
        assert "private" not in text


@pytest.mark.anyio
@pytest.mark.parametrize(
    ("name", "arguments", "path", "body", "payload"),
    [
        (
            "cosplay2_list_topic_deadlines",
            {},
            "/api/events/get_topics_state",
            None,
            {"state": []},
        ),
        (
            "cosplay2_list_topic_statistics",
            {},
            "/api/events/get_topics_statistic",
            None,
            {"stats": []},
        ),
        ("cosplay2_get_schedule", {}, "/api/events/get_plan", None, {"plan": "[]"}),
        (
            "cosplay2_get_winners",
            {},
            "/api/events/winners",
            None,
            {"topics": [], "winners": []},
        ),
        (
            "cosplay2_search_requests",
            {"query": "synthetic"},
            "/api/requests/search",
            {"search_text": "synthetic"},
            {
                "requests": [
                    {
                        "id": 5,
                        "topic_id": 1,
                        "number": 3,
                        "status": "new",
                        "voting_number": None,
                        "voting_title": None,
                        "user_title": "Example participant",
                        "city": "Example city",
                        "card_code": "example",
                    }
                ]
            },
        ),
        (
            "cosplay2_get_topic_form",
            {"url_code": "solo"},
            "/api/topics/get_with_fields",
            {"topic_url_code": "solo"},
            {
                "topic": TOPIC,
                "topic_sections": [],
                "topic_fields": [],
                "requests_count": 0,
            },
        ),
        (
            "cosplay2_list_topic_requests",
            {"topic": 1},
            "/api/topics/get_requests",
            {"topic_id": 1},
            {"topic": TOPIC, "requests": []},
        ),
        (
            "cosplay2_list_topic_requests",
            {"topic": "solo"},
            "/api/topics/get_requests",
            {"topic_url_code": "solo"},
            {"topic": TOPIC, "requests": []},
        ),
        (
            "cosplay2_get_request",
            {"request_id": 5},
            "/api/requests/get",
            {"request_id": "5"},
            {
                "request": {
                    "id": 5,
                    "event_id": 10,
                    "topic_id": 1,
                    "user_id": 7,
                    "number": 3,
                    "status": "new",
                },
                "author": {"user_id": 7},
                "topic": TOPIC,
                "sections": [],
                "fields": [],
                "reqsections": [],
                "reqvalues": [],
            },
        ),
        (
            "cosplay2_get_event_settings",
            {},
            "/api/events/get_settings",
            None,
            {
                "event": {
                    "id": 10,
                    "event_type_id": 1,
                    "title": "Synthetic Fest",
                    "subdomain": "fest",
                    "user_id": 7,
                    "timezone": "Europe/Moscow",
                    "status": "public",
                    "design": '{"custom_css": "body {}"}',
                    "plan": '[{"type": "day", "nodes": []}]',
                }
            },
        ),
        (
            "cosplay2_get_event_state",
            {},
            "/api/events/get_event_state",
            None,
            {
                "state": {
                    "topics_count": 1,
                    "requests_pending": 0,
                    "requests_waiting": 0,
                    "requests_materials": 0,
                    "requests_review": 0,
                    "requests_approved": 0,
                    "requests_disapproved": 0,
                    "tickets_voting": 0,
                }
            },
        ),
        (
            "cosplay2_list_all_requests",
            {},
            "/api/topics/get_all_requests",
            {},
            [],
        ),
        (
            "cosplay2_list_request_comments",
            {"request_id": 5},
            "/api/requests/get_comments",
            {"request_id": "5"},
            {"comments": []},
        ),
        (
            "cosplay2_list_pages",
            {},
            "/api/pages/get_list",
            None,
            [],
        ),
        (
            "cosplay2_get_page",
            {"page_id": 2},
            "/api/pages/get_page",
            {"page_id": "2"},
            {
                "id": 2,
                "path": "rules",
                "type": "page",
                "title": "Rules",
                "show_in_menu": 1,
                "right": 0,
                "content": "<p>Synthetic rules</p>",
            },
        ),
    ],
)
async def test_tool_routing(
    mcp_protocol: McpProtocol,
    name: str,
    arguments: dict[str, Any],
    path: str,
    body: dict[str, Any] | None,
    payload: Any,
) -> None:
    seen: list[httpx2.Request] = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        seen.append(request)
        assert request.url.path == path
        assert request.method == ("POST" if body is not None else "GET")
        if body is not None and body:
            assert json.loads(request.content) == body
        assert request.headers["X-API-Key"] == "key"
        assert request.headers["X-API-Secret"] == "secret"
        return json_response(payload)

    async with mcp_protocol(handler) as protocol:
        result = await protocol.call_tool(name, arguments)
        assert not result.is_error
        assert result.structured_content is not None
        if name == "cosplay2_get_event_settings":
            assert result.structured_content["plan"] is None
            assert result.structured_content["design"] is None
    assert len(seen) == 1


async def test_request_filtering(mcp_protocol: McpProtocol) -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        if request.url.path == "/api/topics/get_requests":
            return json_response(
                {
                    "topic": TOPIC,
                    "requests": [
                        {
                            "id": 1,
                            "number": 1,
                            "status": "approved",
                            "user_id": 7,
                        },
                        {
                            "id": 2,
                            "number": 2,
                            "status": "review",
                            "user_id": 8,
                        },
                    ],
                }
            )
        assert request.url.path == "/api/topics/get_all_requests"
        return json_response(
            [
                {
                    "id": 1,
                    "topic_id": 1,
                    "number": 1,
                    "status": "approved",
                    "user_id": 7,
                },
                {
                    "id": 2,
                    "topic_id": 1,
                    "number": 2,
                    "status": "review",
                    "user_id": 8,
                },
                {
                    "id": 3,
                    "topic_id": 2,
                    "number": 1,
                    "status": "approved",
                    "user_id": 9,
                },
            ]
        )

    async with mcp_protocol(handler) as protocol:
        topic_filtered = await protocol.call_tool(
            "cosplay2_list_topic_requests", {"topic": 1, "status": "review"}
        )
        assert [r["id"] for r in topic_filtered.structured_content["items"]] == [2]
        assert topic_filtered.structured_content["total"] == 1

        all_filtered = await protocol.call_tool(
            "cosplay2_list_all_requests", {"status": "approved", "topic_id": 1}
        )
        assert [r["id"] for r in all_filtered.structured_content["items"]] == [1]
        assert all_filtered.structured_content["total"] == 1
