# Pool API

[API overview](../api-notes.md) · [All endpoints](index.md) · [Schemas](../api-schemas.md)

Browser UI change-notification context. See [authentication](../api-notes.md#authentication) for scope limitations.

JSON request bodies use `application/json` unless an entry specifies another content type.

| Method | Endpoint |
|---|---|
| POST | [`/api/pool/get`](#apipoolget) |

## `/api/pool/get`

Poll subscribed UI change channels with the last server microtime.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `last_microtime` | JSON | unknown | Starts at 0; subsequent calls use the returned microtime. |
| `pool_data` | JSON | array | Subscription channel names, including global subscriptions. |

**Response:** Object with `microtime` (next polling cursor) and `m` (array). Each message is a channel string or an object with `key` and `data`.

**Notes:** The browser polls every 10 seconds. This is a UI change-notification protocol, not a general event-data API.

