from enum import StrEnum

from cosplay2py._types import UTCDateTime
from cosplay2py.models._base import Cosplay2Model
from cosplay2py.models.common import UserBrief


class RatingCategory(StrEnum):
    """Participant rating category (``globals.ratingCategories`` on the site)."""

    TOTAL = "total"
    SCENE = "scene"
    DEFILE = "defile"
    KARAOKE = "karaoke"
    DANCE = "dance"
    ART = "art"
    PHOTO = "photo"
    VIDEO = "video"
    AMV = "amv"
    GAME = "game"
    VNEKONKURS = "vnekonkurs"
    SMI = "smi"
    FAIR = "fair"
    VOLUNTEERS = "volunteers"
    ORGS = "orgs"


class UserSearchResult(UserBrief):
    """A user found by nickname in the site's user picker."""

    id: int | None = None
    """Same as ``user_id``."""
    friends_boost: int | None = None
    """``0`` in every result seen so far."""


class RatingUser(Cosplay2Model):
    """A participant and their rating in a leaderboard."""

    id: int | None = None
    title: str | None = None
    city: str | None = None
    image_update_time: UTCDateTime | None = None
    rating: int | None = None
    rating_code: str | None = None


class RatingGroup(Cosplay2Model):
    """Rating totals and leading participants for a geographic group."""

    geo_id: int | None = None
    country: str | None = None
    country_code: str | None = None
    area_short: str | None = None
    area_url: str | None = None
    region: str | None = None
    city: str | None = None
    sum_rating: str | None = None
    users_count: int | None = None
    topusers: list[RatingUser] | None = None


class RatingGeo(Cosplay2Model):
    """Geographic details accompanying a regional or city leaderboard."""

    id: int | None = None
    country: str | None = None
    country_code: str | None = None
    region: str | None = None
    city: str | None = None
    bounds: str | None = None
    viewport: str | None = None
    location_lat: float | None = None
    location_lng: float | None = None


class RatingRegion(Cosplay2Model):
    """A leaderboard region and the area it belongs to."""

    region_id: int | None = None
    region: str | None = None
    area: str | None = None
    area_short: str | None = None
    area_url: str | None = None


class GlobalRatings(Cosplay2Model):
    """Global participant leaders and ratings grouped by country."""

    topusers: list[RatingUser] | None = None
    countries: list[RatingGroup] | None = None


class CountryRatings(Cosplay2Model):
    """Country participant leaders and ratings grouped by area and region."""

    topusers: list[RatingUser] | None = None
    areas: list[RatingGroup] | None = None
    regions: list[RatingGroup] | None = None


class AreaRatings(Cosplay2Model):
    """Area participant leaders and ratings grouped by region."""

    topusers: list[RatingUser] | None = None
    regions: list[RatingGroup] | None = None


class RegionRatings(Cosplay2Model):
    """Region geography, participant leaders and ratings grouped by city."""

    geo: RatingGeo | None = None
    region: RatingRegion | None = None
    topusers: list[RatingUser] | None = None
    cities: list[RatingGroup] | None = None


class CityRatings(Cosplay2Model):
    """City geography and its participant leaderboard."""

    geo: RatingGeo | None = None
    region: RatingRegion | None = None
    userlist: list[RatingUser] | None = None


class CityGeodata(Cosplay2Model):
    """City location data returned by ``geo.code_city``."""

    country_code: str | None = None
    country: str | None = None
    region: str | None = None
    city: str | None = None
    bounds: str | None = None
    viewport: str | None = None
    location_lng: str | None = None
    location_lat: str | None = None
