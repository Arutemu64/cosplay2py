"""Core client behaviour: configuration, transport, errors and retries."""

import inspect
import json
from collections.abc import Callable, Iterator
from typing import Any

import httpx2
import pytest

from cosplay2py import (
    APIConnectionError,
    APIResponseValidationError,
    APIStatusError,
    APITimeoutError,
    AsyncCosplay2,
    AuthenticationError,
    BadRequestError,
    Cosplay2,
    Cosplay2Error,
    InternalServerError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
)
from cosplay2py.models import BlankId
from unit.conftest import (
    REAL_RETRY_DELAY,
    json_response,
    make_async_client,
    make_client,
)

SYNC_RESOURCES = inspect.get_annotations(Cosplay2)
ASYNC_RESOURCES = inspect.get_annotations(AsyncCosplay2)


def _public_methods(cls: type) -> dict[str, Callable[..., Any]]:
    return {
        name: func
        for name, func in vars(cls).items()
        if not name.startswith("_") and callable(func)
    }


class TestConfiguration:
    def test_requires_event(self) -> None:
        with pytest.raises(Cosplay2Error, match="subdomain"):
            Cosplay2(api_key="k", api_secret="s")

    def test_requires_credentials(self) -> None:
        with pytest.raises(Cosplay2Error, match="api_secret"):
            Cosplay2(subdomain="fest", api_key="k")

    def test_rejects_both_subdomain_and_base_url(self) -> None:
        with pytest.raises(Cosplay2Error):
            Cosplay2(
                subdomain="a",
                base_url="https://b.cosplay2.ru",
                api_key="k",
                api_secret="s",
            )

    def test_reads_environment(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("COSPLAY2_API_KEY", "k")
        monkeypatch.setenv("COSPLAY2_API_SECRET", "s")
        monkeypatch.setenv("COSPLAY2_BASE_URL", "https://fest.example.org")
        with Cosplay2() as client:
            assert str(client.base_url) == "https://fest.example.org"

    def test_repr_hides_secret(self) -> None:
        with Cosplay2(subdomain="fest", api_key="key", api_secret="secret") as client:
            assert "secret" not in repr(client)
            assert "fest.cosplay2.ru" in repr(client)

    def test_does_not_close_foreign_http_client(self) -> None:
        http = httpx2.Client()
        Cosplay2(subdomain="f", api_key="k", api_secret="s", http_client=http).close()
        assert not http.is_closed
        http.close()

    @pytest.mark.anyio
    async def test_async_does_not_close_foreign_http_client(self) -> None:
        http = httpx2.AsyncClient()
        client = AsyncCosplay2(
            subdomain="f", api_key="k", api_secret="s", http_client=http
        )
        await client.aclose()
        assert not http.is_closed
        await http.aclose()


class TestAsyncParity:
    def test_same_resources(self) -> None:
        assert SYNC_RESOURCES.keys() == ASYNC_RESOURCES.keys()

    @pytest.mark.parametrize("resource", SYNC_RESOURCES)
    def test_async_resource_mirrors_sync(self, resource: str) -> None:
        sync_methods = _public_methods(SYNC_RESOURCES[resource])
        async_methods = _public_methods(ASYNC_RESOURCES[resource])

        assert sync_methods.keys() == async_methods.keys()
        for name, func in sync_methods.items():
            twin = async_methods[name]
            assert inspect.iscoroutinefunction(twin), name
            assert inspect.signature(twin) == inspect.signature(func), name
            assert inspect.getdoc(twin) == inspect.getdoc(func), name


class TestRequests:
    def test_sends_auth_headers_and_json_body(self) -> None:
        seen: list[httpx2.Request] = []

        def handler(request: httpx2.Request) -> httpx2.Response:
            seen.append(request)
            return json_response(
                {"html": "<b>x</b>", "blank_title": "T", "file_title": "f"}
            )

        with make_client(handler) as client:
            blank = client.events.get_blank(BlankId.JURY)

        assert blank.html == "<b>x</b>"
        (request,) = seen
        assert request.method == "POST"
        assert str(request.url) == "https://fest.cosplay2.ru/api/events/get_blank_by_id"
        assert request.headers["X-API-Key"] == "key"
        assert request.headers["X-API-Secret"] == "secret"
        # The API requires this header on every POST request.
        assert request.headers["Content-Type"] == "application/json"
        assert json.loads(request.content) == {
            "blank_id": "jury",
            "req_approved": True,
            "picture_height": 80,
        }

    def test_drops_ok_message_envelope(self) -> None:
        def handler(request: httpx2.Request) -> httpx2.Response:
            return json_response(
                {"active_count": 1, "test_tickets": [], "message": "ok"}
            )

        with make_client(handler) as client:
            stats = client.tickets.get_statistic()

        assert stats.model_extra == {}

    def test_keeps_unknown_fields(self) -> None:
        def handler(request: httpx2.Request) -> httpx2.Response:
            return json_response(
                {"active_count": 1, "test_tickets": [], "new_field": 42}
            )

        with make_client(handler) as client:
            stats = client.tickets.get_statistic()

        assert stats.model_extra == {"new_field": 42}


class TestErrors:
    @pytest.mark.parametrize(
        ("status", "error"),
        [
            (400, BadRequestError),
            (401, AuthenticationError),
            (403, PermissionDeniedError),
            (404, NotFoundError),
            (422, APIStatusError),
            (500, InternalServerError),
            (502, InternalServerError),
        ],
    )
    def test_status_errors(self, status: int, error: type[APIStatusError]) -> None:
        def handler(request: httpx2.Request) -> httpx2.Response:
            return json_response({"message": "Nope"}, status_code=status)

        with (
            make_client(handler, max_retries=0) as client,
            pytest.raises(error) as info,
        ):
            client.events.get_state()

        assert type(info.value) is error
        assert info.value.status_code == status
        assert info.value.body == {"message": "Nope"}
        assert "Nope" not in str(info.value)
        assert "secret" not in str(info.value)
        assert "secret" not in repr(info.value)

    def test_plain_text_error_body(self) -> None:
        def handler(request: httpx2.Request) -> httpx2.Response:
            return httpx2.Response(400, text="Сначала удалите вложенные страницы.")

        with make_client(handler) as client, pytest.raises(BadRequestError) as info:
            client.events.get_state()

        assert str(info.value) == "HTTP 400 API request failed."

    def test_redirect_is_an_error(self) -> None:
        def handler(request: httpx2.Request) -> httpx2.Response:
            return httpx2.Response(302, headers={"location": "/login"})

        with make_client(handler) as client, pytest.raises(Cosplay2Error):
            client.events.get_state()

    def test_invalid_json(self) -> None:
        def handler(request: httpx2.Request) -> httpx2.Response:
            return httpx2.Response(200, text="<html>")

        with make_client(handler) as client, pytest.raises(APIResponseValidationError):
            client.events.get_state()

    def test_unexpected_shape(self) -> None:
        def handler(request: httpx2.Request) -> httpx2.Response:
            return json_response({"state": {"topics_count": "many"}})

        with make_client(handler) as client, pytest.raises(APIResponseValidationError):
            client.events.get_state()

    @pytest.mark.anyio
    async def test_async_timeout(self) -> None:
        def handler(request: httpx2.Request) -> httpx2.Response:
            raise httpx2.ReadTimeout("slow", request=request)

        async with make_async_client(handler, max_retries=0) as client:
            with pytest.raises(APITimeoutError):
                await client.events.get_state()

    @pytest.mark.anyio
    async def test_async_connection_error(self) -> None:
        def handler(request: httpx2.Request) -> httpx2.Response:
            raise httpx2.ConnectError("boom", request=request)

        async with make_async_client(handler, max_retries=0) as client:
            with pytest.raises(APIConnectionError):
                await client.events.get_state()


class TestRetries:
    def test_retries_rate_limit_then_succeeds(self) -> None:
        calls = 0

        def handler(request: httpx2.Request) -> httpx2.Response:
            nonlocal calls
            calls += 1
            if calls < 3:
                return json_response({}, status_code=429)
            return json_response([])

        with make_client(handler, max_retries=2) as client:
            assert client.pages.get_list() == []
        assert calls == 3

    def test_gives_up_after_max_retries(self) -> None:
        calls = 0

        def handler(request: httpx2.Request) -> httpx2.Response:
            nonlocal calls
            calls += 1
            return json_response({}, status_code=429)

        with (
            make_client(handler, max_retries=1) as client,
            pytest.raises(RateLimitError),
        ):
            client.pages.get_list()
        assert calls == 2

    def test_connection_error(self) -> None:
        def handler(request: httpx2.Request) -> httpx2.Response:
            raise httpx2.ConnectError("boom", request=request)

        with (
            make_client(handler, max_retries=1) as client,
            pytest.raises(APIConnectionError),
        ):
            client.pages.get_list()

    def test_write_not_retried_on_server_error(self) -> None:
        calls = 0

        def handler(request: httpx2.Request) -> httpx2.Response:
            nonlocal calls
            calls += 1
            return json_response({}, status_code=503)

        with make_client(handler) as client, pytest.raises(InternalServerError):
            client.requests.add_comment(1, "hi")
        assert calls == 1

    def test_write_not_retried_on_timeout(self) -> None:
        calls = 0

        def handler(request: httpx2.Request) -> httpx2.Response:
            nonlocal calls
            calls += 1
            raise httpx2.ReadTimeout("slow", request=request)

        with make_client(handler) as client, pytest.raises(APITimeoutError):
            client.requests.add_comment(1, "hi")
        assert calls == 1

    def test_write_retried_only_on_connect_error(self) -> None:
        calls = 0

        def handler(request: httpx2.Request) -> httpx2.Response:
            nonlocal calls
            calls += 1
            if calls == 1:
                raise httpx2.ConnectError("boom", request=request)
            return json_response({"message": "ok"})

        with make_client(handler) as client:
            client.requests.add_comment(1, "hi")
        assert calls == 2

    @pytest.mark.anyio
    async def test_async_retries_then_errors(self) -> None:
        calls = 0

        def handler(request: httpx2.Request) -> httpx2.Response:
            nonlocal calls
            calls += 1
            return json_response({"message": "down"}, status_code=503)

        async with make_async_client(handler, max_retries=2) as client:
            with pytest.raises(InternalServerError):
                await client.events.get_state()
        assert calls == 3


class TestRetryDelay:
    @pytest.fixture
    def client(self) -> Iterator[Cosplay2]:
        with make_client(lambda request: json_response({})) as client:
            yield client

    @pytest.mark.parametrize(("header", "delay"), [("3", 3.0), ("999", 999.0)])
    def test_honours_retry_after(
        self, client: Cosplay2, header: str, delay: float
    ) -> None:
        response = httpx2.Response(429, headers={"Retry-After": header})
        assert REAL_RETRY_DELAY(client, 0, response) == delay

    @pytest.mark.parametrize(("attempt", "base"), [(0, 0.5), (2, 2.0), (10, 30.0)])
    def test_exponential_backoff_with_jitter(
        self, client: Cosplay2, attempt: int, base: float
    ) -> None:
        # Malformed dates fall back to backoff.
        causes = [
            httpx2.Response(503),
            httpx2.Response(503, headers={"Retry-After": "Wed, 21 Oct 2026"}),
            httpx2.ConnectError("boom"),
        ]
        for cause in causes:
            delay = REAL_RETRY_DELAY(client, attempt, cause)
            assert base * 0.75 <= delay <= base


@pytest.mark.anyio
@pytest.mark.parametrize("status", [429, 503])
async def test_writes_never_retry_responses(api, status):
    calls = []

    def handler(request):
        calls.append(request)
        return json_response({}, status_code=status)

    with pytest.raises(APIStatusError):
        await api(handler, lambda c: c.requests.add_comment(1, "hello"))
    assert len(calls) == 1


@pytest.mark.anyio
@pytest.mark.parametrize("error", [httpx2.ReadTimeout, httpx2.WriteTimeout])
async def test_write_timeouts_both_clients(api, error):
    calls = []

    def handler(request):
        calls.append(request)
        raise error("private-input", request=request)

    with pytest.raises(APITimeoutError):
        await api(handler, lambda c: c.requests.add_comment(1, "hello"))
    assert len(calls) == 1


@pytest.mark.anyio
@pytest.mark.parametrize("asynchronous", [False, True])
async def test_foreign_client_redirects_disabled(asynchronous):
    calls = []

    def handler(request):
        calls.append(request)
        return httpx2.Response(302, headers={"location": "https://other.example/"})

    if asynchronous:
        async with httpx2.AsyncClient(
            transport=httpx2.MockTransport(handler), follow_redirects=True
        ) as http:
            client = AsyncCosplay2(
                subdomain="fest", api_key="key", api_secret="secret", http_client=http
            )
            with pytest.raises(APIStatusError):
                await client.events.get_state()
    else:
        with httpx2.Client(
            transport=httpx2.MockTransport(handler), follow_redirects=True
        ) as http:
            client = Cosplay2(
                subdomain="fest", api_key="key", api_secret="secret", http_client=http
            )
            with pytest.raises(APIStatusError):
                client.events.get_state()
    assert len(calls) == 1


@pytest.mark.parametrize("value", [-1, True, 1.5, "2"])
def test_invalid_retry_count(value):
    with pytest.raises(Cosplay2Error, match="nonnegative integer"):
        Cosplay2(
            subdomain="fest", api_key="key", api_secret="secret", max_retries=value
        )


@pytest.mark.parametrize(
    "url",
    [
        "ftp://example.org",
        "https://u:private-input@example.org",
        "https://example.org?token=private-input",
        "https://example.org#private-input",
        "https://example.org:invalid",
    ],
)
def test_invalid_url_does_not_echo_input(url):
    with pytest.raises(Cosplay2Error) as info:
        Cosplay2(base_url=url, api_key="key", api_secret="secret")
    assert "private-input" not in str(info.value)


@pytest.mark.anyio
@pytest.mark.parametrize(
    ("payload", "status"),
    [
        ({"message": "private-input"}, 400),
        ({"state": {"topics_count": "private-input"}}, 200),
    ],
)
async def test_safe_diagnostics(api, payload, status):
    import traceback

    with pytest.raises(Cosplay2Error) as info:
        await api(
            lambda r: json_response(payload, status), lambda c: c.events.get_state()
        )
    assert "private-input" not in "".join(traceback.format_exception(info.value))
    assert isinstance(info.value, APIStatusError | APIResponseValidationError)
    assert info.value.response.json() == payload


@pytest.mark.anyio
async def test_retry_after_over_budget(api):
    calls = []

    def handler(request):
        calls.append(request)
        return httpx2.Response(429, headers={"Retry-After": "120"})

    with pytest.raises(RateLimitError):
        await api(handler, lambda c: c.events.get_state())
    assert len(calls) == 1


@pytest.mark.parametrize("seconds", [-10, 10, 120])
def test_retry_after_date(seconds):
    from datetime import UTC, datetime, timedelta
    from email.utils import format_datetime

    response = httpx2.Response(
        429,
        headers={
            "Retry-After": format_datetime(
                datetime.now(UTC) + timedelta(seconds=seconds)
            )
        },
    )
    with make_client(lambda r: response) as client:
        delay = REAL_RETRY_DELAY(client, 0, response)
    assert max(0, seconds - 1) <= delay <= max(0, seconds)


@pytest.mark.anyio
async def test_async_cancellation_during_backoff(monkeypatch):
    import anyio

    calls = []

    def handler(request):
        calls.append(request)
        return httpx2.Response(503)

    monkeypatch.setattr(
        "cosplay2py._base_client.BaseClient._retry_delay", lambda *a: 60
    )
    async with make_async_client(handler) as client:
        with anyio.move_on_after(0.01) as scope:
            await client.events.get_state()
        assert scope.cancel_called
    assert len(calls) == 1


@pytest.mark.anyio
async def test_upload_replay_after_connect_failure(api):
    bodies = []

    def handler(request):
        bodies.append(request.content)
        if len(bodies) == 1:
            raise httpx2.ConnectError("failed", request=request)
        return json_response({}, 400)

    with pytest.raises(BadRequestError):
        await api(
            handler,
            lambda c: c.requests.upload_image(1, 2, 3, b"image-content", "image.png"),
        )
    assert len(bodies) == 2
    assert bodies[0] == bodies[1]
    assert b"image-content" in bodies[1]


def test_retry_log_omits_exception_text(caplog):
    import logging

    with (
        make_client(lambda r: json_response({})) as client,
        caplog.at_level(logging.INFO, logger="cosplay2py"),
    ):
        REAL_RETRY_DELAY(client, 0, httpx2.ConnectError("private-input"))
    assert "private-input" not in caplog.text
    assert "ConnectError" in caplog.text


def test_foreign_client_headers_and_timeout():
    def handler(request):
        assert request.headers["X-Custom"] == "custom"
        assert request.headers["X-API-Key"] == "key"
        assert request.extensions["timeout"]["read"] == 7
        return json_response([])

    with (
        httpx2.Client(
            transport=httpx2.MockTransport(handler),
            timeout=7,
            headers={"X-Custom": "custom", "X-API-Key": "wrong"},
        ) as http,
        Cosplay2(
            subdomain="fest",
            api_key="key",
            api_secret="secret",
            timeout=1,
            http_client=http,
        ) as client,
    ):
        client.pages.get_list()
