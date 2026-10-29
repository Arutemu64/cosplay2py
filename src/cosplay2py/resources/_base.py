from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cosplay2py._base_client import Endpoint
    from cosplay2py._client import AsyncCosplay2, Cosplay2


class SyncResource:
    def __init__(self, client: "Cosplay2") -> None:
        self._client = client

    def _request[T](self, endpoint: "Endpoint[T]") -> T:
        return self._client._request(endpoint)


class AsyncResource:
    def __init__(self, client: "AsyncCosplay2") -> None:
        self._client = client

    async def _request[T](self, endpoint: "Endpoint[T]") -> T:
        return await self._client._request(endpoint)
