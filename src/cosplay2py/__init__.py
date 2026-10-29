"""Sync and async client for the Cosplay2.ru event API."""

from cosplay2py import models
from cosplay2py._base_client import __version__
from cosplay2py._client import AsyncCosplay2, Cosplay2
from cosplay2py._exceptions import (
    APIConnectionError,
    APIError,
    APIResponseValidationError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    Cosplay2Error,
    InternalServerError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
)

__all__ = [
    "APIConnectionError",
    "APIError",
    "APIResponseValidationError",
    "APIStatusError",
    "APITimeoutError",
    "AsyncCosplay2",
    "AuthenticationError",
    "BadRequestError",
    "Cosplay2",
    "Cosplay2Error",
    "InternalServerError",
    "NotFoundError",
    "PermissionDeniedError",
    "RateLimitError",
    "__version__",
    "models",
]
