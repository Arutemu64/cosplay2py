# Admin API

[API overview](../api-notes.md) · [All endpoints](index.md) · [Schemas](../api-schemas.md)

Platform administration browser context; UI gate: role >= 100. See [authentication](../api-notes.md#authentication) for scope limitations.

JSON request bodies use `application/json` unless an entry specifies another content type.

| Method | Endpoint |
|---|---|
| POST | [`/api/admin/calc_size`](#apiadmincalc_size) |
| POST | [`/api/admin/del_files`](#apiadmindel_files) |
| POST | [`/api/admin/events_list`](#apiadminevents_list) |
| GET | [`/api/admin/get_freespace`](#apiadminget_freespace) |
| GET | [`/api/admin/new_events_list`](#apiadminnew_events_list) |

## `/api/admin/calc_size`

Recalculate event disk usage, or aggregate usage when the event selector is null.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `event_id` | JSON | identifier or null | Selected event; null requests aggregate usage. |

**Response:** Known JSON fields: `disk_free_space`, `disk_total_space`, `event_size`. Schema incomplete.

## `/api/admin/del_files`

Delete the selected event files and refresh disk-usage figures.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `event_id` | JSON | identifier | Event identifier. |

**Response:** Known JSON fields: `disk_free_space`, `disk_total_space`, `event_size`. Schema incomplete.

## `/api/admin/events_list`

List events for platform administration, optionally limited to hosted events.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `only_on_hosting` | JSON | boolean | Limit results to hosted events. |

**Response:** Known JSON fields: `events`. Schema incomplete.

## `/api/admin/get_freespace`

Read total and available hosting disk space.

**Method:** GET.

**Response:** Known JSON fields: `disk_free_space`, `disk_total_space`. Schema incomplete.

## `/api/admin/new_events_list`

List new event submissions for moderation.

**Method:** GET.

**Response:** Known JSON fields: `new_events`. Schema incomplete.

