from typing import Any

from cosplay2py._base_client import Endpoint
from cosplay2py.models import RatingCategory, UserSearchResult
from cosplay2py.models.users import (
    AreaRatings,
    CityRatings,
    CountryRatings,
    GlobalRatings,
    RegionRatings,
)
from cosplay2py.resources._base import AsyncResource, SyncResource


def _search(query: str) -> Endpoint[list[UserSearchResult]]:
    return Endpoint(
        "POST",
        "/api/users/search",
        list[UserSearchResult],
        key="users",
        json={"query": query},
        idempotent=True,
    )


class Users(SyncResource):
    def search(self, query: str) -> list[UserSearchResult]:
        """Users whose nickname contains ``query``, as in the site's user picker.

        A two-letter query came back empty where three letters found matches.
        """
        return self._request(_search(query))

    def ratings_global(
        self, category: RatingCategory = RatingCategory.TOTAL
    ) -> GlobalRatings:
        """Participant ratings for the global scope."""
        return self._request(
            Endpoint(
                "POST",
                "/api/users/ratings_global",
                GlobalRatings,
                json={"category": RatingCategory(category)},
                idempotent=True,
            )
        )

    def ratings_country(
        self, country_code: str, category: RatingCategory = RatingCategory.TOTAL
    ) -> CountryRatings:
        """Participant ratings for the country scope."""
        return self._request(
            Endpoint(
                "POST",
                "/api/users/ratings_country",
                CountryRatings,
                json={
                    "category": RatingCategory(category),
                    "country_code": country_code,
                },
                idempotent=True,
            )
        )

    def ratings_area(
        self, area_url: str, category: RatingCategory = RatingCategory.TOTAL
    ) -> AreaRatings:
        """Participant ratings for the area scope."""
        return self._request(
            Endpoint(
                "POST",
                "/api/users/ratings_area",
                AreaRatings,
                json={"category": RatingCategory(category), "area_url": area_url},
                idempotent=True,
            )
        )

    def ratings_region(
        self, geo_id: int, category: RatingCategory = RatingCategory.TOTAL
    ) -> RegionRatings:
        """Participant ratings for the region scope."""
        return self._request(
            Endpoint(
                "POST",
                "/api/users/ratings_region",
                RegionRatings,
                json={"category": RatingCategory(category), "geo_id": str(geo_id)},
                idempotent=True,
            )
        )

    def ratings_city(
        self, geo_id: int, category: RatingCategory = RatingCategory.TOTAL
    ) -> CityRatings:
        """Participant ratings for the city scope."""
        return self._request(
            Endpoint(
                "POST",
                "/api/users/ratings_city",
                CityRatings,
                json={"category": RatingCategory(category), "geo_id": str(geo_id)},
                idempotent=True,
            )
        )

    def get_region_geo_id(self, region: str, country_code: str) -> Any:
        """Geographic identifier for a region."""
        return self._request(
            Endpoint(
                "POST",
                "/api/users/get_region_geo_id",
                Any,
                json={"region": region, "country_code": country_code},
                idempotent=True,
            )
        )


class AsyncUsers(AsyncResource):
    async def search(self, query: str) -> list[UserSearchResult]:
        """Users whose nickname contains ``query``, as in the site's user picker.

        A two-letter query came back empty where three letters found matches.
        """
        return await self._request(_search(query))

    async def ratings_global(
        self, category: RatingCategory = RatingCategory.TOTAL
    ) -> GlobalRatings:
        """Participant ratings for the global scope."""
        return await self._request(
            Endpoint(
                "POST",
                "/api/users/ratings_global",
                GlobalRatings,
                json={"category": RatingCategory(category)},
                idempotent=True,
            )
        )

    async def ratings_country(
        self, country_code: str, category: RatingCategory = RatingCategory.TOTAL
    ) -> CountryRatings:
        """Participant ratings for the country scope."""
        return await self._request(
            Endpoint(
                "POST",
                "/api/users/ratings_country",
                CountryRatings,
                json={
                    "category": RatingCategory(category),
                    "country_code": country_code,
                },
                idempotent=True,
            )
        )

    async def ratings_area(
        self, area_url: str, category: RatingCategory = RatingCategory.TOTAL
    ) -> AreaRatings:
        """Participant ratings for the area scope."""
        return await self._request(
            Endpoint(
                "POST",
                "/api/users/ratings_area",
                AreaRatings,
                json={"category": RatingCategory(category), "area_url": area_url},
                idempotent=True,
            )
        )

    async def ratings_region(
        self, geo_id: int, category: RatingCategory = RatingCategory.TOTAL
    ) -> RegionRatings:
        """Participant ratings for the region scope."""
        return await self._request(
            Endpoint(
                "POST",
                "/api/users/ratings_region",
                RegionRatings,
                json={"category": RatingCategory(category), "geo_id": str(geo_id)},
                idempotent=True,
            )
        )

    async def ratings_city(
        self, geo_id: int, category: RatingCategory = RatingCategory.TOTAL
    ) -> CityRatings:
        """Participant ratings for the city scope."""
        return await self._request(
            Endpoint(
                "POST",
                "/api/users/ratings_city",
                CityRatings,
                json={"category": RatingCategory(category), "geo_id": str(geo_id)},
                idempotent=True,
            )
        )

    async def get_region_geo_id(self, region: str, country_code: str) -> Any:
        """Geographic identifier for a region."""
        return await self._request(
            Endpoint(
                "POST",
                "/api/users/get_region_geo_id",
                Any,
                json={"region": region, "country_code": country_code},
                idempotent=True,
            )
        )
