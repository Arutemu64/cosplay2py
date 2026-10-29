"""Transport-agnostic plumbing shared by the sync and async clients."""

import logging
import os
import random
import re
from dataclasses import dataclass, field
from datetime import UTC, datetime
from email.utils import parsedate_to_datetime
from functools import cache
from importlib.metadata import PackageNotFoundError, version
from typing import Any, Literal

import httpx2
from pydantic import TypeAdapter, ValidationError

from cosplay2py._exceptions import (
    APIResponseValidationError,
    Cosplay2Error,
    make_status_error,
)

log = logging.getLogger("cosplay2py")

try:
    __version__ = version("cosplay2py")
except PackageNotFoundError:  # pragma: no cover - running from a source checkout
    __version__ = "0.0.0"

DEFAULT_TIMEOUT = httpx2.Timeout(30.0, connect=10.0)
DEFAULT_MAX_RETRIES = 2
RETRYABLE_STATUSES = frozenset({429, 502, 503, 504})
_MAX_RETRY_DELAY = 30.0


@dataclass(frozen=True, slots=True)
class Endpoint[T]:
    """Everything needed to perform one API call and parse its result.

    Resources build these; the clients execute them. Keeping the description of an
    endpoint free of any I/O is what lets one definition serve both sync and async.
    """

    method: Literal["GET", "POST"]
    path: str
    response_type: Any
    """The type the (possibly unwrapped) JSON payload is validated against."""
    key: str | None = None
    """Top-level key to unwrap, e.g. ``"state"`` for ``{"state": {...}}``."""
    json: dict[str, Any] | None = None
    params: dict[str, Any] | None = None
    """Query string parameters; a few endpoints take their arguments there."""
    data: dict[str, Any] | None = None
    files: dict[str, Any] | None = None
    """Multipart form fields and files, for uploads."""
    idempotent: bool = field(kw_only=True)
    """Whether repeating the call is harmless. Writes are only retried when the server
    cannot have acted on the request (a failed connection)."""


@cache
def _adapter(tp: Any) -> TypeAdapter[Any]:
    return TypeAdapter(tp)


def _resolve_base_url(base_url: str | None, subdomain: str | None) -> httpx2.URL:
    if base_url and subdomain:
        raise Cosplay2Error("Pass either `base_url` or `subdomain`, not both.")
    if subdomain and not re.fullmatch(
        r"[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?", subdomain
    ):
        raise Cosplay2Error("Invalid event subdomain.")
    if subdomain:
        base_url = f"https://{subdomain}.cosplay2.ru"
    base_url = base_url or os.environ.get("COSPLAY2_BASE_URL")
    if not base_url:
        raise Cosplay2Error(
            "No event to talk to: pass `subdomain=` (e.g. 'ff26summer'), `base_url=` "
            "(e.g. 'https://ff26summer.cosplay2.ru') or set COSPLAY2_BASE_URL."
        )
    try:
        url = httpx2.URL(base_url)
    except (httpx2.InvalidURL, ValueError):
        raise Cosplay2Error(
            "Invalid base_url: expected an HTTP(S) event URL."
        ) from None
    if url.scheme not in {"http", "https"} or not url.host:
        raise Cosplay2Error("Invalid base_url: expected an HTTP(S) event URL.")
    if url.userinfo or url.query or url.fragment:
        raise Cosplay2Error("base_url must not contain credentials, query or fragment.")
    return url


def _resolve_credential(value: str | None, env: str, name: str) -> str:
    value = value or os.environ.get(env)
    if not value:
        raise Cosplay2Error(f"Missing {name}: pass `{name}=` or set {env}.")
    return value


class BaseClient[HttpClientT: (httpx2.Client, httpx2.AsyncClient)]:
    base_url: httpx2.URL
    max_retries: int
    _http: HttpClientT
    _owns_http: bool

    def __init__(
        self,
        *,
        api_key: str | None,
        api_secret: str | None,
        base_url: str | None,
        subdomain: str | None,
        max_retries: int,
        headers: dict[str, str] | None,
    ) -> None:
        if type(max_retries) is not int or max_retries < 0:
            raise Cosplay2Error("max_retries must be a nonnegative integer.")
        self.base_url = _resolve_base_url(base_url, subdomain)
        self.max_retries = max_retries
        self._headers = {
            "Accept": "application/json",
            "User-Agent": f"cosplay2py/{__version__}",
            **(headers or {}),
            "X-API-Key": _resolve_credential(api_key, "COSPLAY2_API_KEY", "api_key"),
            "X-API-Secret": _resolve_credential(
                api_secret, "COSPLAY2_API_SECRET", "api_secret"
            ),
        }

    def __repr__(self) -> str:
        # Never include the credentials: reprs end up in logs and tracebacks.
        return f"{type(self).__name__}(base_url={str(self.base_url.copy_with(path='/'))!r})"

    def _build_request(self, endpoint: Endpoint[Any]) -> httpx2.Request:
        return self._http.build_request(
            endpoint.method,
            self.base_url.join(endpoint.path),
            params=endpoint.params,
            json=endpoint.json,
            data=endpoint.data,
            files=endpoint.files,
            headers=self._headers,
        )

    def _process_response[T](
        self, endpoint: Endpoint[T], response: httpx2.Response
    ) -> T:
        log.debug("%s %s -> %s", endpoint.method, endpoint.path, response.status_code)
        # Redirects are treated as errors too: an unauthenticated request may get
        # bounced to an HTML page instead of a JSON error.
        if not response.is_success:
            raise make_status_error(response)

        try:
            data = response.json()
        except ValueError:
            raise APIResponseValidationError(
                "Response body is not valid JSON.", response=response
            ) from None

        if endpoint.key is not None:
            if not isinstance(data, dict) or endpoint.key not in data:
                raise APIResponseValidationError(
                    f"Expected a JSON object with a {endpoint.key!r} key.",
                    response=response,
                )
            data = data[endpoint.key]
        elif isinstance(data, dict) and data.get("message") == "ok":
            # A success marker many endpoints put next to the payload, not part of it.
            data = {k: v for k, v in data.items() if k != "message"}

        try:
            return _adapter(endpoint.response_type).validate_python(data)
        except ValidationError:
            raise APIResponseValidationError(
                f"Unexpected response shape for {endpoint.path}.",
                response=response,
            ) from None

    def _should_retry(
        self, endpoint: Endpoint[Any], cause: httpx2.Response | Exception, attempt: int
    ) -> bool:
        if attempt >= self.max_retries:
            return False
        if isinstance(cause, httpx2.Response):
            if not endpoint.idempotent:
                return False
            delay = _retry_after(cause)
            return cause.status_code in RETRYABLE_STATUSES and (
                delay is None or delay <= _MAX_RETRY_DELAY
            )
        return endpoint.idempotent or isinstance(cause, httpx2.ConnectError)

    def _retry_delay(self, attempt: int, cause: httpx2.Response | Exception) -> float:
        delay = _retry_after(cause) if isinstance(cause, httpx2.Response) else None
        if delay is None:
            delay = min(0.5 * 2 ** min(attempt, 6), _MAX_RETRY_DELAY) * random.uniform(
                0.75, 1.0
            )
        log.info(
            "Retrying %s in %.2fs (%s)",
            type(self).__name__,
            delay,
            type(cause).__name__,
        )
        return delay


def _retry_after(response: httpx2.Response) -> float | None:
    value = response.headers.get("Retry-After", "").strip()
    if re.fullmatch(r"[0-9]+", value):
        return float(value)
    try:
        date = parsedate_to_datetime(value)
        if date.tzinfo is None:
            return None
        return max(0.0, (date - datetime.now(UTC)).total_seconds())
    except (ValueError, TypeError, OverflowError):
        return None
