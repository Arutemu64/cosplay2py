# Api Keys API

[API overview](../api-notes.md) · [All endpoints](index.md) · [Schemas](../api-schemas.md)

Organizer token screen and platform administration. Query-routed organizer calls and path-routed admin calls have distinct contexts. See [authentication](../api-notes.md#authentication) for scope limitations.

JSON request bodies use `application/json` unless an entry specifies another content type.

| Method | Endpoint |
|---|---|
| POST | [`/?get=api/api_keys/deactivate`](#getapiapi_keysdeactivate) |
| POST | [`/?get=api/api_keys/generate_org`](#getapiapi_keysgenerate_org) |
| GET | [`/?get=api/api_keys/get_user_tokens`](#getapiapi_keysget_user_tokens) |
| POST | [`/api/api_keys/deactivate`](#apiapi_keysdeactivate) |
| POST | [`/api/api_keys/generate`](#apiapi_keysgenerate) |
| GET | [`/api/api_keys/list`](#apiapi_keyslist) |

## `/?get=api/api_keys/deactivate`

Deactivate the selected API key.

**Method:** POST. **Access:** Organizer token screen.

| Field | In | Type | Description |
|---|---|---|---|
| `api_key` | JSON | string | Key to deactivate; treat as a credential. |

**Response:** Schema unknown.

## `/?get=api/api_keys/generate_org`

Generate an organizer API token from script metadata.

**Method:** POST. **Access:** Organizer token screen.

| Field | In | Type | Description |
|---|---|---|---|
| `script_name` | JSON | string | Script or integration name. |
| `description` | JSON | string | Description supplied by the user. |

**Response:** JSON object whose `api_key`, `api_secret` and `expires_at` fields are displayed by the token template. Field formats and complete schema are unverified.

## `/?get=api/api_keys/get_user_tokens`

List the current user’s tokens for the organizer token screen.

**Method:** GET. **Access:** Organizer token screen.

**Response:** Known JSON fields: `tokens`. Schema incomplete.

## `/api/api_keys/deactivate`

Deactivate the selected API key.

**Method:** POST. **Access:** Platform administration browser UI.

| Field | In | Type | Description |
|---|---|---|---|
| `api_key` | JSON | string | Key to deactivate; treat as a credential. |

**Response:** Known JSON fields: `success`. Schema incomplete.

## `/api/api_keys/generate`

Generate an API credential with the selected user/event scope and lifetime.

**Method:** POST. **Access:** Platform administration browser UI.

| Field | In | Type | Description |
|---|---|---|---|
| `key_type` | JSON | string | Options: "user", "external". UI default: "user". |
| `script_name` | JSON | string | Script or integration name. |
| `description` | JSON | string | Description supplied by the user. |
| `lifetime_days` | JSON | integer | Parsed as integer; UI fallback: 30. |
| `user_id` | JSON | integer | Sent for user keys. |
| `event_id` | JSON | integer | Optional for user keys. |
| `allowed_endpoints` | JSON | array of strings | Sent for external keys; UI splits comma-separated text and trims each entry. |

**Response:** JSON object used by the template as `api_key`, `api_secret`, `expires_at` and `key_type`. Field formats and complete schema are unverified.

## `/api/api_keys/list`

List credentials in the platform administration screen.

**Method:** GET. **Access:** Platform administration browser UI.

**Response:** Schema unknown.

