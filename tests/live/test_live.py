"""Read-only calls against the real API. Nothing here may create or modify data."""

from collections.abc import Callable
from typing import Any

import pytest

from cosplay2py import APIStatusError, AsyncCosplay2, Cosplay2
from cosplay2py.models import BlankId
from live.conftest import report_drift

pytestmark = pytest.mark.live

# Endpoints that need no arguments. Feeds are left out on purpose: `onlynew` may
# mark notifications as read for the token's owner.
NO_ARG_CALLS: dict[str, Callable[[Cosplay2], Any]] = {
    "events.get_settings": lambda c: c.events.get_settings(),
    "events.get_state": lambda c: c.events.get_state(),
    "events.get_topics_state": lambda c: c.events.get_topics_state(),
    "events.get_topics_statistic": lambda c: c.events.get_topics_statistic(),
    "events.get_buttons_state": lambda c: c.events.get_buttons_state(),
    "events.get_staff": lambda c: c.events.get_staff(),
    "events.get_plan": lambda c: c.events.get_plan(),
    "events.get_blank": lambda c: c.events.get_blank(BlankId.JURY),
    "events.get_reg_topics": lambda c: c.events.get_reg_topics(),
    "events.get_reg_alphabet": lambda c: c.events.get_reg_alphabet(),
    "events.check_external_domain": lambda c: c.events.check_external_domain(""),
    "events.search": lambda c: c.events.search("fan"),
    "topics.get_list": lambda c: c.topics.get_list(),
    "topics.get_list(with_group_text)": lambda c: c.topics.get_list(
        with_group_text=True
    ),
    "topics.get_list(event_id)": lambda c: c.topics.get_list(
        event_id=c.events.get_settings().id
    ),
    "topics.get_all_requests": lambda c: c.topics.get_all_requests(),
    "topics.get_requests_for_planner": lambda c: c.topics.get_requests_for_planner(),
    "users.get_friends": lambda c: c.users.get_friends(),
    "users.search": lambda c: c.users.search("cos"),
    "design.get": lambda c: c.design.get(),
    "design.get_images": lambda c: c.design.get_images(),
    "pages.get_list": lambda c: c.pages.get_list(),
    "media.get_data": lambda c: c.media.get_data(),
    "etickets.get_list": lambda c: c.etickets.get_list(),
    "etickets.get_types": lambda c: c.etickets.get_types(),
    "etickets.get_paymethods": lambda c: c.etickets.get_paymethods(),
    "etickets.get_vat_dictionary": lambda c: c.etickets.get_vat_dictionary(),
    "tickets.get_statistic": lambda c: c.tickets.get_statistic(),
    "tickets.get_voting_statistics": lambda c: c.tickets.get_voting_statistics(),
}


@pytest.mark.parametrize("call", NO_ARG_CALLS.values(), ids=NO_ARG_CALLS.keys())
def test_endpoint(client: Cosplay2, call: Callable[[Cosplay2], Any]) -> None:
    report_drift(call(client))


def test_settings_match_configured_event(client: Cosplay2) -> None:
    event = client.events.get_settings()
    host = client.base_url.host
    assert host == event.domain or host.startswith(f"{event.subdomain}.")


def test_request_chain(client: Cosplay2) -> None:
    """Walk topic -> its requests -> one request, using real IDs."""
    topic = next(
        (
            t
            for t in client.topics.get_list()
            if client.topics.get_requests(t.url_code).requests
        ),
        None,
    )
    if topic is None:
        pytest.skip("event has no requests")

    listing = report_drift(client.topics.get_requests(topic.url_code))
    form = report_drift(client.topics.get_form(topic.url_code))
    assert form.topic.id == topic.id
    assert client.topics.get_requests(topic.id) == listing
    first = listing.requests[0]

    details = report_drift(client.requests.get(first.id))
    assert details.request.id == first.id
    assert details.topic.id == topic.id

    report_drift(client.requests.get_comments(first.id))
    report_drift(client.requests.get_org_comments(first.id))
    report_drift(client.requests.get_user(first.id, details.request.user_id))
    report_drift(client.requests.get_feedbacks(first.id, details.request.user_id))
    report_drift(client.users.get_events(details.request.user_id))
    report_drift(client.users.get(details.request.user_id))
    if details.values:
        report_drift(client.requests.get_value_history(first.id, details.values[0].id))


def test_page(client: Cosplay2) -> None:
    page = next((p for p in client.pages.get_list() if p.type == "page"), None)
    if page is None:
        pytest.skip("event has no pages")
    details = report_drift(client.pages.get(page.id))
    assert details.id == page.id


def test_wrong_secret_is_rejected(client: Cosplay2) -> None:
    """Documents how the server reacts to bad credentials.

    If this fails, look at the actual status/body and adjust the error mapping.
    """
    with (
        Cosplay2(base_url=str(client.base_url), api_secret="definitely-wrong") as bad,
        pytest.raises(APIStatusError) as info,
    ):
        bad.events.get_state()
    assert info.value.status_code in {401, 403}, info.value.body


@pytest.mark.anyio
async def test_async_client(async_client: AsyncCosplay2) -> None:
    state = await async_client.events.get_state()
    assert state.topics_count >= 0
