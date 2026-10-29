from collections.abc import Awaitable, Callable
from typing import Any

import httpx2
import pytest

from cosplay2py import AsyncCosplay2, Cosplay2
from cosplay2py._base_client import BaseClient

Handler = Callable[[httpx2.Request], httpx2.Response]
type ApiCall = Callable[[Handler, Callable[[Any], Any]], Awaitable[Any]]

# Captured before ``_no_retry_sleep`` patches it, for tests of the backoff itself.
REAL_RETRY_DELAY = BaseClient._retry_delay


@pytest.fixture(params=["asyncio", "trio"])
def anyio_backend(request: pytest.FixtureRequest) -> str:
    return request.param


@pytest.fixture(autouse=True)
def _no_env_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in ("COSPLAY2_API_KEY", "COSPLAY2_API_SECRET", "COSPLAY2_BASE_URL"):
        monkeypatch.delenv(name, raising=False)


@pytest.fixture(autouse=True)
def _no_retry_sleep(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "cosplay2py._base_client.BaseClient._retry_delay", lambda *a: 0.0
    )


@pytest.fixture(params=["sync", "async"])
def api(request: pytest.FixtureRequest) -> ApiCall:
    """Runs ``call(client)`` on a sync or an async client, awaiting it if needed.

    Tests using it need ``@pytest.mark.anyio`` and run once per client.
    """

    async def run(handler: Handler, call: Callable[[Any], Any]) -> Any:
        if request.param == "sync":
            with make_client(handler) as client:
                return call(client)
        async with make_async_client(handler) as client:
            return await call(client)

    return run


def make_client(handler: Handler, max_retries: int = 2) -> Cosplay2:
    http = httpx2.Client(transport=httpx2.MockTransport(handler))
    return Cosplay2(
        subdomain="fest",
        api_key="key",
        api_secret="secret",
        http_client=http,
        max_retries=max_retries,
    )


def make_async_client(handler: Handler, max_retries: int = 2) -> AsyncCosplay2:
    http = httpx2.AsyncClient(transport=httpx2.MockTransport(handler))
    return AsyncCosplay2(
        subdomain="fest",
        api_key="key",
        api_secret="secret",
        http_client=http,
        max_retries=max_retries,
    )


def json_response(data: Any, status_code: int = 200) -> httpx2.Response:
    # The real API serves JSON with a text/html content type.
    return httpx2.Response(
        status_code, json=data, headers={"content-type": "text/html; charset=UTF-8"}
    )


TOPIC = {
    "id": 1,
    "event_id": 10,
    "url_code": "solo",
    "category": "defile",
    "voting_group": 0,
    "card_code": "s",
    "order": 1,
    "title": "Solo",
    "description": "",
    "voting_public": 0,
    "voting_jury": 1,
    "print_badges": 0,
    "card_enabled": 1,
    "default_duration": 1,
    "time_requests_open": "2026-04-01 09:00:00",
    "time_requests_close": "2026-08-07 20:59:00",
    "time_addons_close": "2026-08-09 20:59:00",
    "time_cards_open": None,
    "time_voting_open": None,
    "time_voting_close": None,
    "card_name_rule": "{a|b}",
    "card_announcement_rule": None,
    "card_diplom_rule": None,
    "intro": None,
    "public_requests": "NO",
}
