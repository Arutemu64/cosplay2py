from typing import Any

import httpx2

__all__ = [
    "APIConnectionError",
    "APIError",
    "APIResponseValidationError",
    "APIStatusError",
    "APITimeoutError",
    "AuthenticationError",
    "BadRequestError",
    "Cosplay2Error",
    "InternalServerError",
    "NotFoundError",
    "PermissionDeniedError",
    "RateLimitError",
]


class Cosplay2Error(Exception):
    """Base class for every error raised by cosplay2py."""


class APIError(Cosplay2Error):
    """An error that happened while talking to the Cosplay2 API."""

    message: str
    request: httpx2.Request

    def __init__(self, message: str, *, request: httpx2.Request) -> None:
        super().__init__(message)
        self.message = message
        self.request = request


class APIConnectionError(APIError):
    """The request never got a response (DNS failure, refused connection, etc.)."""

    def __init__(
        self, *, request: httpx2.Request, message: str = "Connection error."
    ) -> None:
        super().__init__(message, request=request)


class APITimeoutError(APIConnectionError):
    """The request timed out."""

    def __init__(self, *, request: httpx2.Request) -> None:
        super().__init__(request=request, message="Request timed out.")


class APIResponseValidationError(APIError):
    """The server answered successfully, but the payload did not match the expected shape."""

    response: httpx2.Response
    status_code: int

    def __init__(self, message: str, *, response: httpx2.Response) -> None:
        super().__init__(message, request=response.request)
        self.response = response
        self.status_code = response.status_code


class APIStatusError(APIError):
    """The server answered with a non-2xx status code."""

    response: httpx2.Response
    status_code: int
    body: Any

    def __init__(self, message: str, *, response: httpx2.Response, body: Any) -> None:
        super().__init__(message, request=response.request)
        self.response = response
        self.status_code = response.status_code
        self.body = body


class BadRequestError(APIStatusError):
    """HTTP 400."""


class AuthenticationError(APIStatusError):
    """HTTP 401: the API key or secret is missing, invalid or expired."""


class PermissionDeniedError(APIStatusError):
    """HTTP 403: the token has no access to this event or action."""


class NotFoundError(APIStatusError):
    """HTTP 404."""


class RateLimitError(APIStatusError):
    """HTTP 429."""


class InternalServerError(APIStatusError):
    """HTTP 5xx."""


_STATUS_ERRORS: dict[int, type[APIStatusError]] = {
    400: BadRequestError,
    401: AuthenticationError,
    403: PermissionDeniedError,
    404: NotFoundError,
    429: RateLimitError,
}


def make_status_error(response: httpx2.Response) -> APIStatusError:
    """Build the most specific ``APIStatusError`` subclass for ``response``."""
    try:
        body: Any = response.json()
    except ValueError:
        body = response.text

    message = f"HTTP {response.status_code} API request failed."

    if response.status_code >= 500:
        cls: type[APIStatusError] = InternalServerError
    else:
        cls = _STATUS_ERRORS.get(response.status_code, APIStatusError)
    return cls(message, response=response, body=body)
