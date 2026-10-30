import json

import httpx2

from unit.conftest import json_response, make_client


def test_search() -> None:
    seen: list[httpx2.Request] = []
    user = {
        "id": 7,
        "user_id": 7,
        "title": "Nick",
        "city": "Somewhere",
        "image_update_time": 1713798357,
        "friends_boost": 0,
    }

    def handler(request: httpx2.Request) -> httpx2.Response:
        seen.append(request)
        return json_response({"users": [user]})

    with make_client(handler) as client:
        (parsed,) = client.users.search("nic")

    (request,) = seen
    assert request.url.path == "/api/users/search"
    assert json.loads(request.content) == {"query": "nic"}
    assert parsed.user_id == 7
    assert parsed.friends_boost == 0
    assert parsed.model_extra == {}


import pytest


@pytest.mark.anyio
@pytest.mark.parametrize(
    ("scope", "selector"),
    [
        ("global", {}),
        ("country", {"country_code": "RU"}),
        ("area", {"area_url": "ural"}),
        ("region", {"geo_id": 179}),
        ("city", {"geo_id": 179}),
    ],
)
async def test_ratings(api, scope, selector):
    def handler(request):
        assert request.url.path == f"/api/users/ratings_{scope}"
        expected = {**selector, "category": "total"}
        if "geo_id" in expected:
            expected["geo_id"] = str(expected["geo_id"])
        assert json.loads(request.content) == expected
        return json_response({"userlist" if scope == "city" else "topusers": []})

    result = await api(
        handler, lambda c: getattr(c.users, f"ratings_{scope}")(**selector)
    )
    assert result.model_extra == {}
    assert result.userlist == [] if scope == "city" else result.topusers == []


@pytest.mark.anyio
async def test_city_rating_details(api):
    from datetime import UTC, datetime

    def handler(request):
        return json_response(
            {
                "message": "ok",
                "geo": {"id": 123, "location_lat": 55.5, "location_lng": 37.5},
                "region": {"region_id": 12, "area_url": "example"},
                "userlist": [
                    {
                        "id": 7,
                        "title": "Example",
                        "rating": 42,
                        "image_update_time": 1713798357,
                    }
                ],
            }
        )

    result = await api(handler, lambda c: c.users.ratings_city(123))
    assert result.geo.location_lat == 55.5
    assert result.region.region_id == 12
    assert result.userlist[0].rating == 42
    assert result.userlist[0].image_update_time == datetime.fromtimestamp(
        1713798357, UTC
    )
    assert result.model_extra == {}


@pytest.mark.anyio
async def test_country_rating_groups(api):
    def handler(request):
        return json_response(
            {
                "regions": None,
                "areas": [
                    {
                        "area_url": "example",
                        "sum_rating": "1234",
                        "users_count": 2,
                        "topusers": [{"id": 7, "rating": 42}],
                    }
                ],
            }
        )

    result = await api(handler, lambda c: c.users.ratings_country("RU"))
    assert result.regions is None
    assert result.areas[0].sum_rating == "1234"
    assert result.areas[0].topusers[0].rating == 42
