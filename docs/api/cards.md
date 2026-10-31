# Cards API

[API overview](../api-notes.md) · [All endpoints](index.md) · [Schemas](../api-schemas.md)

Event participant showcase and public request list; preview variants are used in organizer screens. See [authentication](../api-notes.md#authentication) for scope limitations.

JSON request bodies use `application/json` unless an entry specifies another content type.

| Method | Endpoint |
|---|---|
| GET | [`/api/cards/get_card`](#apicardsget_card) |
| GET | [`/api/cards/get_request`](#apicardsget_request) |
| GET | [`/api/cards/get_topics_and_cards`](#apicardsget_topics_and_cards) |
| GET | [`/api/cards/get_topics_and_requests`](#apicardsget_topics_and_requests) |

## `/api/cards/get_card`

A single participant card.

**Method:** GET.

| Field | In | Type | Description |
|---|---|---|---|
| `request_id` | Query | string | Request identifier. |
| `preview` | Query | string | Optional; send "1" to enable preview, otherwise omit. |

**Response:** `CardDetails`: request, topic, sections, fields, reqsections,
reqvalues, badges and users.

**Example request URL:** `/api/cards/get_card?request_id=42`

**SDK:** `cards.get_card()`.

## `/api/cards/get_request`

A single request from the public request list.

**Method:** GET.

| Field | In | Type | Description |
|---|---|---|---|
| `request_id` | Query | string | Request identifier. |

**Response:** `PublicRequestDetails`: request, topic, sections, fields, reqsections,
reqvalues and users; no badges.

**SDK:** `cards.get_request()`.

## `/api/cards/get_topics_and_cards`

Topics and participant cards shown on the event site.

**Method:** GET.

| Field | In | Type | Description |
|---|---|---|---|
| `preview` | Query | string | Optional; send "1" to enable preview, otherwise omit. |

**Response:** `TopicsAndCards`: `topics` contains `CardTopic` rows and `requests`
contains `CardRequest` rows, including nullable `ImageValue` metadata.

**SDK:** `cards.get_topics_and_cards()`.

## `/api/cards/get_topics_and_requests`

Topics and submitted requests shown on the public request list.

**Method:** GET.

**Response:** `TopicsAndRequests`: `topics` contains `CardTopic` rows and
`requests` contains `PublicRequest` rows with status and visibility enums,
request numbers and nullable voting numbers/titles.

**SDK:** `cards.get_topics_and_requests()`.
