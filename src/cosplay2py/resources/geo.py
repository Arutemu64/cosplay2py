from cosplay2py._base_client import Endpoint
from cosplay2py.models.users import CityGeodata
from cosplay2py.resources._base import AsyncResource, SyncResource


class Geo(SyncResource):
    def code_city(self, city: str) -> CityGeodata:
        """Geographic data for a city name."""
        return self._request(
            Endpoint(
                "POST",
                "/api/geo/code_city",
                CityGeodata,
                key="geodata",
                json={"city": city},
                idempotent=True,
            )
        )


class AsyncGeo(AsyncResource):
    async def code_city(self, city: str) -> CityGeodata:
        """Geographic data for a city name."""
        return await self._request(
            Endpoint(
                "POST",
                "/api/geo/code_city",
                CityGeodata,
                key="geodata",
                json={"city": city},
                idempotent=True,
            )
        )
