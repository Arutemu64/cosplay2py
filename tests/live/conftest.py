"""Read-only smoke tests against a real event.

They check that the token is accepted and that real payloads still validate. Fields
the models don't know about yet are reported as warnings: that is how API drift shows
up before it turns into a validation error.

Run with::

    COSPLAY2_API_KEY=... COSPLAY2_API_SECRET=... \
    COSPLAY2_BASE_URL=https://<event>.cosplay2.ru uv run pytest -m live -rw
"""

import os
import warnings
from collections.abc import Iterator
from typing import Any

import pytest
from pydantic import BaseModel

from cosplay2py import AsyncCosplay2, Cosplay2

_REQUIRED_ENV = ("COSPLAY2_API_KEY", "COSPLAY2_API_SECRET", "COSPLAY2_BASE_URL")


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    missing = [name for name in _REQUIRED_ENV if not os.environ.get(name)]
    if not missing:
        return
    skip = pytest.mark.skip(reason=f"live tests need {', '.join(missing)}")
    for item in items:
        if item.get_closest_marker("live"):
            item.add_marker(skip)


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session")
def client() -> Iterator[Cosplay2]:
    # One retry only: a flaky live run should fail loudly, not hammer the site.
    with Cosplay2(max_retries=1) as c2:
        yield c2


@pytest.fixture
async def async_client() -> Any:
    async with AsyncCosplay2(max_retries=1) as c2:
        yield c2


class UnknownFieldsWarning(UserWarning):
    """The API returned fields that the models don't declare."""


def _unknown_fields(value: Any, found: set[str]) -> set[str]:
    if isinstance(value, BaseModel):
        found.update(f"{type(value).__name__}.{k}" for k in value.model_extra or {})
        for name in type(value).model_fields:
            _unknown_fields(getattr(value, name), found)
    elif isinstance(value, list | tuple):
        for item in value:
            _unknown_fields(item, found)
    elif isinstance(value, dict):
        for item in value.values():
            _unknown_fields(item, found)
    return found


def report_drift(value: Any) -> Any:
    """Warn about undeclared fields in ``value``; returns ``value`` unchanged."""
    if unknown := _unknown_fields(value, set()):
        warnings.warn(
            f"Undeclared fields: {', '.join(sorted(unknown))}",
            UnknownFieldsWarning,
            stacklevel=2,
        )
    return value
