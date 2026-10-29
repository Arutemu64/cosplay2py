import json
from collections.abc import Iterable
from datetime import datetime
from typing import Any

from cosplay2py._base_client import Endpoint
from cosplay2py.models import (
    AlphabetRegistration,
    Blank,
    BlankId,
    ButtonsState,
    Deadline,
    DomainCheck,
    Event,
    EventBrief,
    EventStaff,
    EventState,
    Plan,
    PlanNode,
    TopicsRegistration,
    TopicState,
    TopicStatistic,
)
from cosplay2py.resources._base import AsyncResource, SyncResource

_GET_SETTINGS = Endpoint[Event](
    "GET", "/api/events/get_settings", Event, key="event", idempotent=True
)
_GET_STATE = Endpoint[EventState](
    "GET", "/api/events/get_event_state", EventState, key="state", idempotent=True
)
_GET_TOPICS_STATE = Endpoint[list[TopicState]](
    "GET",
    "/api/events/get_topics_state",
    list[TopicState],
    key="state",
    idempotent=True,
)
_GET_TOPICS_STATISTIC = Endpoint[list[TopicStatistic]](
    "GET",
    "/api/events/get_topics_statistic",
    list[TopicStatistic],
    key="stats",
    idempotent=True,
)
_GET_BUTTONS_STATE = Endpoint[ButtonsState](
    "GET", "/api/events/get_buttons_state_1", ButtonsState, idempotent=True
)
_GET_STAFF = Endpoint[EventStaff](
    "GET", "/api/events/get_orgs_curators", EventStaff, idempotent=True
)
_GET_PLAN = Endpoint[list[PlanNode]](
    "GET", "/api/events/get_plan", Plan, key="plan", idempotent=True
)


# These two reports come back as data rather than rendered HTML.
_DATA_BLANKS: dict[BlankId, str] = {
    BlankId.REG_TOPICS: "get_reg_topics",
    BlankId.REG_ALPHABET: "get_reg_alphabet",
}


def _blank_endpoint[T](
    blank_id: BlankId,
    response_type: type[T],
    req_approved: bool,
    req_disapproved: bool = False,
    req_other: bool = False,
    picture_height: int = 80,
) -> Endpoint[T]:
    body: dict[str, Any] = {"blank_id": str(blank_id), "req_approved": req_approved}
    # The site only sends these two when their checkbox is ticked.
    if req_disapproved:
        body["req_disapproved"] = True
    if req_other:
        body["req_other"] = True
    body["picture_height"] = picture_height
    return Endpoint(
        "POST", "/api/events/get_blank_by_id", response_type, json=body, idempotent=True
    )


def _get_blank(
    blank_id: BlankId,
    req_approved: bool,
    req_disapproved: bool,
    req_other: bool,
    picture_height: int,
) -> Endpoint[Blank]:
    blank_id = BlankId(blank_id)
    if method := _DATA_BLANKS.get(blank_id):
        raise ValueError(
            f"{blank_id!s} is not an HTML report; use events.{method}() instead."
        )
    return _blank_endpoint(
        blank_id, Blank, req_approved, req_disapproved, req_other, picture_height
    )


def _check_external_domain(domain: str) -> Endpoint[DomainCheck]:
    return Endpoint(
        "POST",
        "/api/events/check_external_domain",
        DomainCheck,
        json={"domain": domain},
        idempotent=True,
    )


def _search(query: str) -> Endpoint[list[EventBrief]]:
    return Endpoint(
        "POST",
        "/api/events/search",
        list[EventBrief],
        key="events",
        json={"query": query},
        idempotent=True,
    )


def _set_deadline(
    topic_id: int | Iterable[int], deadline: Deadline, time: datetime
) -> Endpoint[Any]:
    deadline = Deadline(deadline)
    if time.tzinfo is not None:
        raise ValueError("Pass a naive datetime in the event's timezone.")
    data = time.strftime("%d.%m.%y %H:%M")
    if isinstance(topic_id, int):
        body = {"topic_id": topic_id, "datetype": str(deadline), "data": data}
    else:
        body = {
            "dates": [
                {"topic_id": tid, "datetype": str(deadline), "data": data}
                for tid in topic_id
            ]
        }
    return Endpoint("POST", "/api/events/set_gate", Any, json=body, idempotent=False)


def _epoch_ms(value: Any) -> int:
    if isinstance(value, datetime):
        return round(value.timestamp() * 1000)
    raise TypeError(f"Cannot serialize {type(value).__name__} in a plan.")


def _save_plan(plan: Iterable[PlanNode]) -> Endpoint[Any]:
    # The site stores the tree as a JSON string with Unix-millisecond timestamps.
    # Leaving out unset fields sends back what get_plan() returned, extras included.
    nodes = [node.model_dump(by_alias=True, exclude_unset=True) for node in plan]
    data = json.dumps(
        nodes, ensure_ascii=False, separators=(",", ":"), default=_epoch_ms
    )
    return Endpoint(
        "POST", "/api/events/save_plan", Any, json={"plan": data}, idempotent=False
    )


class Events(SyncResource):
    """The event the client is bound to."""

    def get_settings(self) -> Event:
        """Event settings: title, dates, timezone, design, ..."""
        return self._request(_GET_SETTINGS)

    def get_state(self) -> EventState:
        """Request counters for the whole event."""
        return self._request(_GET_STATE)

    def get_topics_state(self) -> list[TopicState]:
        """Deadlines of every topic, in the event's local time."""
        return self._request(_GET_TOPICS_STATE)

    def get_topics_statistic(self) -> list[TopicStatistic]:
        """Request counters per topic."""
        return self._request(_GET_TOPICS_STATISTIC)

    def get_buttons_state(self) -> ButtonsState:
        return self._request(_GET_BUTTONS_STATE)

    def get_staff(self) -> EventStaff:
        """Organizers, topic curators and the main organizer."""
        return self._request(_GET_STAFF)

    def get_plan(self) -> list[PlanNode]:
        """The schedule tree built in the planner (days -> places -> blocks)."""
        return self._request(_GET_PLAN)

    def save_plan(self, plan: Iterable[PlanNode]) -> None:
        """Replace the whole schedule tree, e.g. with an edited :meth:`get_plan`.

        The site saves the full tree on every change in the planner; there is no way
        to update a single node.
        """
        self._request(_save_plan(plan))

    def get_blank(
        self,
        blank_id: BlankId,
        *,
        req_approved: bool = True,
        req_disapproved: bool = False,
        req_other: bool = False,
        picture_height: int = 80,
    ) -> Blank:
        """Render a printable report as HTML.

        ``reg_topics`` and ``reg_alphabet`` are returned as data instead: fetch them
        with :meth:`get_reg_topics` and :meth:`get_reg_alphabet`.

        :param req_approved: Include approved requests.
        :param req_disapproved: Include rejected requests.
        :param req_other: Include requests in any other status.
        :param picture_height: Height of embedded pictures, in pixels.
        """
        return self._request(
            _get_blank(
                blank_id, req_approved, req_disapproved, req_other, picture_height
            )
        )

    def get_reg_topics(
        self,
        *,
        req_approved: bool = True,
        req_disapproved: bool = False,
        req_other: bool = False,
    ) -> TopicsRegistration:
        """The registration table: participants grouped by topic.

        :param req_approved: Include approved requests.
        :param req_disapproved: Include rejected requests.
        :param req_other: Include requests in any other status.
        """
        return self._request(
            _blank_endpoint(
                BlankId.REG_TOPICS,
                TopicsRegistration,
                req_approved,
                req_disapproved,
                req_other,
            )
        )

    def get_reg_alphabet(
        self,
        *,
        req_approved: bool = True,
        req_disapproved: bool = False,
        req_other: bool = False,
    ) -> AlphabetRegistration:
        """The registration table: every participant once, sorted by name.

        :param req_approved: Include approved requests.
        :param req_disapproved: Include rejected requests.
        :param req_other: Include requests in any other status.
        """
        return self._request(
            _blank_endpoint(
                BlankId.REG_ALPHABET,
                AlphabetRegistration,
                req_approved,
                req_disapproved,
                req_other,
            )
        )

    def check_external_domain(self, domain: str) -> DomainCheck:
        """Check whether ``domain`` resolves to Cosplay2 and can be attached to the event."""
        return self._request(_check_external_domain(domain))

    def search(self, query: str) -> list[EventBrief]:
        """All Cosplay2 events whose title matches ``query``."""
        return self._request(_search(query))

    def set_deadline(
        self, topic_id: int | Iterable[int], deadline: Deadline, time: datetime
    ) -> None:
        """Set a deadline of one topic, or the same deadline of several topics.

        :param deadline: which date to set, e.g. ``Deadline.ADDONS_CLOSE``.
        :param time: a naive datetime in the event's timezone (see ``Event.timezone``),
            as shown by :meth:`get_topics_state`; seconds are dropped.
        """
        self._request(_set_deadline(topic_id, deadline, time))


class AsyncEvents(AsyncResource):
    """The event the client is bound to."""

    async def get_settings(self) -> Event:
        """Event settings: title, dates, timezone, design, ..."""
        return await self._request(_GET_SETTINGS)

    async def get_state(self) -> EventState:
        """Request counters for the whole event."""
        return await self._request(_GET_STATE)

    async def get_topics_state(self) -> list[TopicState]:
        """Deadlines of every topic, in the event's local time."""
        return await self._request(_GET_TOPICS_STATE)

    async def get_topics_statistic(self) -> list[TopicStatistic]:
        """Request counters per topic."""
        return await self._request(_GET_TOPICS_STATISTIC)

    async def get_buttons_state(self) -> ButtonsState:
        return await self._request(_GET_BUTTONS_STATE)

    async def get_staff(self) -> EventStaff:
        """Organizers, topic curators and the main organizer."""
        return await self._request(_GET_STAFF)

    async def get_plan(self) -> list[PlanNode]:
        """The schedule tree built in the planner (days -> places -> blocks)."""
        return await self._request(_GET_PLAN)

    async def save_plan(self, plan: Iterable[PlanNode]) -> None:
        """Replace the whole schedule tree, e.g. with an edited :meth:`get_plan`.

        The site saves the full tree on every change in the planner; there is no way
        to update a single node.
        """
        await self._request(_save_plan(plan))

    async def get_blank(
        self,
        blank_id: BlankId,
        *,
        req_approved: bool = True,
        req_disapproved: bool = False,
        req_other: bool = False,
        picture_height: int = 80,
    ) -> Blank:
        """Render a printable report as HTML.

        ``reg_topics`` and ``reg_alphabet`` are returned as data instead: fetch them
        with :meth:`get_reg_topics` and :meth:`get_reg_alphabet`.

        :param req_approved: Include approved requests.
        :param req_disapproved: Include rejected requests.
        :param req_other: Include requests in any other status.
        :param picture_height: Height of embedded pictures, in pixels.
        """
        return await self._request(
            _get_blank(
                blank_id, req_approved, req_disapproved, req_other, picture_height
            )
        )

    async def get_reg_topics(
        self,
        *,
        req_approved: bool = True,
        req_disapproved: bool = False,
        req_other: bool = False,
    ) -> TopicsRegistration:
        """The registration table: participants grouped by topic.

        :param req_approved: Include approved requests.
        :param req_disapproved: Include rejected requests.
        :param req_other: Include requests in any other status.
        """
        return await self._request(
            _blank_endpoint(
                BlankId.REG_TOPICS,
                TopicsRegistration,
                req_approved,
                req_disapproved,
                req_other,
            )
        )

    async def get_reg_alphabet(
        self,
        *,
        req_approved: bool = True,
        req_disapproved: bool = False,
        req_other: bool = False,
    ) -> AlphabetRegistration:
        """The registration table: every participant once, sorted by name.

        :param req_approved: Include approved requests.
        :param req_disapproved: Include rejected requests.
        :param req_other: Include requests in any other status.
        """
        return await self._request(
            _blank_endpoint(
                BlankId.REG_ALPHABET,
                AlphabetRegistration,
                req_approved,
                req_disapproved,
                req_other,
            )
        )

    async def check_external_domain(self, domain: str) -> DomainCheck:
        """Check whether ``domain`` resolves to Cosplay2 and can be attached to the event."""
        return await self._request(_check_external_domain(domain))

    async def search(self, query: str) -> list[EventBrief]:
        """All Cosplay2 events whose title matches ``query``."""
        return await self._request(_search(query))

    async def set_deadline(
        self, topic_id: int | Iterable[int], deadline: Deadline, time: datetime
    ) -> None:
        """Set a deadline of one topic, or the same deadline of several topics.

        :param deadline: which date to set, e.g. ``Deadline.ADDONS_CLOSE``.
        :param time: a naive datetime in the event's timezone (see ``Event.timezone``),
            as shown by :meth:`get_topics_state`; seconds are dropped.
        """
        await self._request(_set_deadline(topic_id, deadline, time))
