# Geo API

[API overview](../api-notes.md) · [All endpoints](index.md) · [Schemas](../api-schemas.md)

City and region lookup used by event and portal screens. See [authentication](../api-notes.md#authentication) for scope limitations.

JSON request bodies use `application/json` unless an entry specifies another content type.

| Method | Endpoint |
|---|---|
| POST | [`/api/geo/code_city`](#apigeocode_city) |
| POST | [`/api/geo/resolve_for_map`](#apigeoresolve_for_map) |

## `/api/geo/code_city`

Geographic data for a city name.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `city` | JSON | string | City name. |

**Response:** Object with `geodata`: [CityGeodata](../api-schemas.md#citygeodata) object.

**Example:** `{"city": "example"}`

**SDK:** `geo.code_city()`.

## `/api/geo/resolve_for_map`

Resolve the unique city names from the event listing into map places keyed by city.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `cities` | JSON | array of strings | Unique, nonempty city names from the event listing. |

**Response:** Object with `places`, a mapping indexed by city name. Coordinate field types are unverified.

