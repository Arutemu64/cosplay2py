"""Reusable annotated types that normalize Cosplay2's inconsistent wire formats."""

import json
from datetime import UTC, datetime
from typing import Annotated, Any

from pydantic import AfterValidator, BeforeValidator


def _as_utc(value: datetime) -> datetime:
    return value.replace(tzinfo=UTC) if value.tzinfo is None else value


def _parse_local(value: Any) -> Any:
    if isinstance(value, str):
        return datetime.strptime(value, "%d.%m.%y %H:%M")  # noqa: DTZ007 - naive by design
    return value


def _parse_json(value: Any) -> Any:
    if isinstance(value, str):
        return json.loads(value) if value.strip() else None
    return value


UTCDateTime = Annotated[datetime, AfterValidator(_as_utc)]
"""A timezone-aware UTC datetime.

The API sends these as ``"YYYY-MM-DD HH:MM:SS"`` strings (in UTC), Unix seconds
or Unix milliseconds depending on the endpoint.
"""

LocalDateTime = Annotated[datetime, BeforeValidator(_parse_local)]
"""A naive datetime, exactly as displayed by the site.

Some endpoints return pre-formatted ``"DD.MM.YY HH:MM"`` strings meant for display;
these are usually in the event's timezone (see ``Event.timezone``).
"""

JsonEncoded = BeforeValidator(_parse_json)
"""Marker for fields that the API returns as a JSON document packed into a string."""
