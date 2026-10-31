# Tickets API

[API overview](../api-notes.md) · [All endpoints](index.md) · [Schemas](../api-schemas.md)

Event audience-voting tickets, votes, prizes and organizer monitoring. See [authentication](../api-notes.md#authentication) for scope limitations.

JSON request bodies use `application/json` unless an entry specifies another content type.

| Method | Endpoint |
|---|---|
| POST | [`/api/tickets/check_for_voting`](#apiticketscheck_for_voting) |
| POST | [`/api/tickets/clear_votes`](#apiticketsclear_votes) |
| POST | [`/api/tickets/create`](#apiticketscreate) |
| GET | [`/api/tickets/get_cards`](#apiticketsget_cards) |
| GET | [`/api/tickets/get_statistic`](#apiticketsget_statistic) |
| GET | [`/api/tickets/get_ticket`](#apiticketsget_ticket) |
| GET | [`/api/tickets/get_txt`](#apiticketsget_txt) |
| POST | [`/api/tickets/get_voting_data`](#apiticketsget_voting_data) |
| GET | [`/api/tickets/get_voting_statistics`](#apiticketsget_voting_statistics) |
| POST | [`/api/tickets/prize_add`](#apiticketsprize_add) |
| POST | [`/api/tickets/prize_del`](#apiticketsprize_del) |
| POST | [`/api/tickets/save_prize_field`](#apiticketssave_prize_field) |
| POST | [`/api/tickets/save_prize_handed`](#apiticketssave_prize_handed) |
| POST | [`/api/tickets/select_winner`](#apiticketsselect_winner) |

## `/api/tickets/check_for_voting`

Verify that `ticket_number` can be used to vote.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `ticket_number` | JSON | string | Voting ticket code. |

**Response:** Schema unknown.

**SDK:** `tickets.check_for_voting()`.

## `/api/tickets/clear_votes`

Clear all test votes.

**Method:** POST.

**Response:** Schema unknown.

**SDK:** `tickets.clear_votes()`.

## `/api/tickets/create`

Generate audience voting tickets.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `tickets_count` | JSON | integer | Number of voting tickets to generate. |
| `tickets_type` | JSON | [TicketKind](../api-schemas.md#ticketkind) | Test or working voting ticket kind. |
| `create_type` | JSON | [TicketCreateMode](../api-schemas.md#ticketcreatemode) | Add tickets or replace the existing set. |

**Response:** Schema unknown.

**Example:** `{"tickets_count": 42, "tickets_type": 2, "create_type": "add"}`

**SDK:** `tickets.create()`.

## `/api/tickets/get_cards`

Participant cards shown on the voting page.

**Method:** GET.

**Response:** Object with `requests`: array of object with unknown values.

**SDK:** `tickets.get_cards()`.

## `/api/tickets/get_statistic`

Active ticket count and test voting tickets.

**Method:** GET.

**Response:** [TicketStatistic](../api-schemas.md#ticketstatistic) object.

**SDK:** `tickets.get_statistic()`.

## `/api/tickets/get_ticket`

The voting ticket bound to the current user, if any.

**Method:** GET.

**Response:** object with unknown values.

**SDK:** `tickets.get_ticket()`.

## `/api/tickets/get_txt`

Download generated voting ticket codes as text.

**Method:** GET.

**Response:** Voting ticket codes as a text download; response headers are unverified.

## `/api/tickets/get_voting_data`

Topics, requests and current selections for `ticket_number`.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `ticket_number` | JSON | string | Voting ticket code. |
| `voting_type` | JSON | [VotingType](../api-schemas.md#votingtype) | Live or test voting selector. Client default: "normal". |

**Response:** object with unknown values.

**SDK:** `tickets.get_voting_data()`.

## `/api/tickets/get_voting_statistics`

Live audience voting statistics and prize winners.

**Method:** GET.

**Response:** [VotingStatistics](../api-schemas.md#votingstatistics) object.

**SDK:** `tickets.get_voting_statistics()`.

## `/api/tickets/prize_add`

Add a voter raffle prize and return the updated prizes payload.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `title` | JSON | string | Title. |
| `quantity` | JSON | integer | Number of prize units. |

**Response:** object with unknown values.

**SDK:** `tickets.add_prize()`.

## `/api/tickets/prize_del`

Delete a voter raffle prize and return the updated prizes payload.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `prize_id` | JSON | integer | Prize identifier. |

**Response:** object with unknown values.

**SDK:** `tickets.delete_prize()`.

## `/api/tickets/save_prize_field`

Set an attribute of a voter raffle prize (`title` or `quantity`).

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `prize_id` | JSON | integer | Prize identifier. |
| `field` | JSON | string | Name of the field to edit. |
| `data` | JSON | field-dependent JSON value | New field value; depends on the selected field. |

**Response:** Schema unknown.

**SDK:** `tickets.save_prize_field()`.

## `/api/tickets/save_prize_handed`

Mark whether a raffle prize has been handed to its winner.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `prize_winner_id` | JSON | integer | Prize-winner entry identifier. |
| `data` | JSON | integer | New field value; depends on the selected field. |

**Response:** Schema unknown.

**SDK:** `tickets.save_prize_handed()`.

## `/api/tickets/select_winner`

Cast or change a vote for `request_id` in `topic_id`.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `ticket_number` | JSON | string | Voting ticket code. |
| `topic_id` | JSON | integer | Topic identifier. |
| `winner_index` | JSON | integer | Winner slot index supplied by the raffle UI. |
| `request_id` | JSON | integer | Request identifier. |
| `voting_type` | JSON | [VotingType](../api-schemas.md#votingtype) | Live or test voting selector. Client default: "normal". |

**Response:** object with unknown values.

**SDK:** `tickets.select_winner()`.
