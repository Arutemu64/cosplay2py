"""Read-only calls against the real API. Nothing here may create or modify data."""

from collections.abc import Callable
from typing import Any

import pytest

from cosplay2py import APIStatusError, AsyncCosplay2, Cosplay2
from cosplay2py.models import BlankId
from live.conftest import report_drift

pytestmark = pytest.mark.live

# Endpoints that need no dynamic IDs.
NO_ARG_CALLS: dict[str, Callable[[Cosplay2], Any]] = {
    "events.get_settings": lambda c: c.events.get_settings(),
    "events.get_state": lambda c: c.events.get_state(),
    "events.get_topics_state": lambda c: c.events.get_topics_state(),
    "events.get_topics_statistic": lambda c: c.events.get_topics_statistic(),
    "events.get_staff": lambda c: c.events.get_staff(),
    "events.get_winners": lambda c: c.events.get_winners(),
    "events.get_plan": lambda c: c.events.get_plan(),
    "events.get_blank": lambda c: c.events.get_blank(BlankId.JURY),
    "events.get_reg_topics": lambda c: c.events.get_reg_topics(),
    "events.get_reg_alphabet": lambda c: c.events.get_reg_alphabet(),
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
    "users.search": lambda c: c.users.search("cos"),
    "users.ratings_global": lambda c: c.users.ratings_global(),
    "geo.code_city": lambda c: c.geo.code_city("Moscow"),
    "design.get": lambda c: c.design.get(),
    "design.get_images": lambda c: c.design.get_images(),
    "pages.get_list": lambda c: c.pages.get_list(),
    "media.get_data": lambda c: c.media.get_data(),
    "etickets.get_list": lambda c: c.etickets.get_list(),
    "etickets.get_types": lambda c: c.etickets.get_types(),
    "tickets.get_statistic": lambda c: c.tickets.get_statistic(),
    "tickets.get_voting_statistics": lambda c: c.tickets.get_voting_statistics(),
    "cards.get_topics_and_cards": lambda c: c.cards.get_topics_and_cards(),
    "cards.get_topics_and_requests": lambda c: c.cards.get_topics_and_requests(),
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
    if details.values:
        report_drift(client.requests.get_value_history(first.id, details.values[0].id))


def test_page(client: Cosplay2) -> None:
    page = next((p for p in client.pages.get_list() if p.type == "page"), None)
    if page is None:
        pytest.skip("event has no pages")
    details = report_drift(client.pages.get(page.id))
    assert details.id == page.id


def test_ratings_chain(client: Cosplay2) -> None:
    """Walk country -> area -> region -> city using returned selectors."""
    global_ratings = report_drift(client.users.ratings_global())
    country_code = next(
        (c.country_code for c in global_ratings.countries or [] if c.country_code),
        None,
    )
    if country_code is None:
        pytest.skip("global ratings have no country selectors")
    country = report_drift(client.users.ratings_country(country_code))
    regions = country.regions or []
    area_url = next((a.area_url for a in country.areas or [] if a.area_url), None)
    if area_url is not None:
        area = report_drift(client.users.ratings_area(area_url))
        regions = area.regions or []
    region_id = next((r.geo_id for r in regions if r.geo_id is not None), None)
    if region_id is None:
        pytest.skip("country/area ratings have no region selectors")
    region = report_drift(client.users.ratings_region(region_id))
    if region.geo is not None:
        assert region.geo.id == region_id
    city_id = next(
        (c.geo_id for c in region.cities or [] if c.geo_id is not None), None
    )
    if city_id is None:
        pytest.skip("region ratings have no city selectors")
    city = report_drift(client.users.ratings_city(city_id))
    if city.geo is not None:
        assert city.geo.id == city_id


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
