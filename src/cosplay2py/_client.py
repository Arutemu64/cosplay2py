import time
from itertools import count
from types import TracebackType
from typing import Self

import anyio
import httpx2

from cosplay2py._base_client import (
    DEFAULT_MAX_RETRIES,
    DEFAULT_TIMEOUT,
    BaseClient,
    Endpoint,
)
from cosplay2py._exceptions import APIConnectionError, APITimeoutError
from cosplay2py.resources import (
    AsyncCards,
    AsyncDesign,
    AsyncETickets,
    AsyncEvents,
    AsyncGeo,
    AsyncMedia,
    AsyncPages,
    AsyncRequests,
    AsyncTickets,
    AsyncTopics,
    AsyncUsers,
    Cards,
    Design,
    ETickets,
    Events,
    Geo,
    Media,
    Pages,
    Requests,
    Tickets,
    Topics,
    Users,
)


class Cosplay2(BaseClient[httpx2.Client]):
    """Synchronous client for the API of one Cosplay2 event.

    API tokens are issued per event (Orgs -> Settings -> API tokens), so a client is
    bound to a single event site::

        with Cosplay2(subdomain="ff26summer", api_key="...", api_secret="...") as c2:
            for topic in c2.topics.get_list():
                print(topic.title)

    Credentials and the event fall back to the ``COSPLAY2_API_KEY``,
    ``COSPLAY2_API_SECRET`` and ``COSPLAY2_BASE_URL`` environment variables.

    :param subdomain: Event subdomain on cosplay2.ru, e.g. ``"ff26summer"``.
    :param base_url: Full event URL instead of ``subdomain``; use it for events
        served from a custom domain.
    :param max_retries: Retries for connection errors, timeouts and 429/502/503/504.
    :param http_client: Bring your own ``httpx2.Client`` (proxies, transports, ...).
        It is not closed by ``close()``; its ``base_url`` is ignored. Its timeout and default headers apply;
        wrapper headers take precedence. Redirects are always disabled.
    """

    events: Events
    topics: Topics
    requests: Requests
    geo: Geo
    users: Users
    design: Design
    pages: Pages
    media: Media
    cards: Cards
    etickets: ETickets
    tickets: Tickets

    def __init__(
        self,
        *,
        api_key: str | None = None,
        api_secret: str | None = None,
        subdomain: str | None = None,
        base_url: str | None = None,
        timeout: float | httpx2.Timeout = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        headers: dict[str, str] | None = None,
        http_client: httpx2.Client | None = None,
    ) -> None:
        super().__init__(
            api_key=api_key,
            api_secret=api_secret,
            base_url=base_url,
            subdomain=subdomain,
            max_retries=max_retries,
            headers=headers,
        )
        self._owns_http = http_client is None
        self._http = http_client or httpx2.Client(timeout=timeout)

        self.events = Events(self)
        self.topics = Topics(self)
        self.requests = Requests(self)
        self.geo = Geo(self)
        self.users = Users(self)
        self.design = Design(self)
        self.pages = Pages(self)
        self.media = Media(self)
        self.cards = Cards(self)
        self.etickets = ETickets(self)
        self.tickets = Tickets(self)

    def close(self) -> None:
        """Close the underlying HTTP client, unless it was passed in by the caller."""
        if self._owns_http:
            self._http.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.close()

    def _request[T](self, endpoint: Endpoint[T]) -> T:
        request = self._build_request(endpoint)
        for attempt in count():
            try:
                response = self._http.send(request, follow_redirects=False)
            except httpx2.TransportError as exc:
                if self._should_retry(endpoint, exc, attempt):
                    time.sleep(self._retry_delay(attempt, exc))
                    continue
                if isinstance(exc, httpx2.TimeoutException):
                    raise APITimeoutError(request=request) from None
                raise APIConnectionError(request=request) from None

            if self._should_retry(endpoint, response, attempt):
                response.close()
                time.sleep(self._retry_delay(attempt, response))
                continue
            return self._process_response(endpoint, response)
        raise AssertionError("unreachable")


class AsyncCosplay2(BaseClient[httpx2.AsyncClient]):
    """Asynchronous client for the API of one Cosplay2 event.

    Same interface as ``Cosplay2``, with awaitable methods::

        async with AsyncCosplay2(subdomain="ff26summer") as c2:
            topics = await c2.topics.get_list()

    Works with asyncio and trio.
    """

    events: AsyncEvents
    topics: AsyncTopics
    requests: AsyncRequests
    geo: AsyncGeo
    users: AsyncUsers
    design: AsyncDesign
    pages: AsyncPages
    media: AsyncMedia
    cards: AsyncCards
    etickets: AsyncETickets
    tickets: AsyncTickets

    def __init__(
        self,
        *,
        api_key: str | None = None,
        api_secret: str | None = None,
        subdomain: str | None = None,
        base_url: str | None = None,
        timeout: float | httpx2.Timeout = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        headers: dict[str, str] | None = None,
        http_client: httpx2.AsyncClient | None = None,
    ) -> None:
        super().__init__(
            api_key=api_key,
            api_secret=api_secret,
            base_url=base_url,
            subdomain=subdomain,
            max_retries=max_retries,
            headers=headers,
        )
        self._owns_http = http_client is None
        self._http = http_client or httpx2.AsyncClient(timeout=timeout)

        self.events = AsyncEvents(self)
        self.topics = AsyncTopics(self)
        self.requests = AsyncRequests(self)
        self.geo = AsyncGeo(self)
        self.users = AsyncUsers(self)
        self.design = AsyncDesign(self)
        self.pages = AsyncPages(self)
        self.media = AsyncMedia(self)
        self.cards = AsyncCards(self)
        self.etickets = AsyncETickets(self)
        self.tickets = AsyncTickets(self)

    async def aclose(self) -> None:
        """Close the underlying HTTP client, unless it was passed in by the caller."""
        if self._owns_http:
            await self._http.aclose()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        await self.aclose()

    async def _request[T](self, endpoint: Endpoint[T]) -> T:
        request = self._build_request(endpoint)
        for attempt in count():
            try:
                response = await self._http.send(request, follow_redirects=False)
            except httpx2.TransportError as exc:
                if self._should_retry(endpoint, exc, attempt):
                    await anyio.sleep(self._retry_delay(attempt, exc))
                    continue
                if isinstance(exc, httpx2.TimeoutException):
                    raise APITimeoutError(request=request) from None
                raise APIConnectionError(request=request) from None

            if self._should_retry(endpoint, response, attempt):
                await response.aclose()
                await anyio.sleep(self._retry_delay(attempt, response))
                continue
            return self._process_response(endpoint, response)
        raise AssertionError("unreachable")
