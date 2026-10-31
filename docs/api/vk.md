# Vk API

[API overview](../api-notes.md) · [All endpoints](index.md) · [Schemas](../api-schemas.md)

Browser VK ID authorization; separate from event API tokens. See [authentication](../api-notes.md#authentication) for scope limitations.

JSON request bodies use `application/json` unless an entry specifies another content type.

| Method | Endpoint |
|---|---|
| POST | [`/vk/api`](#vkapi) |

## `/vk/api`

Prepare VK ID browser authorization and return the provider navigation URL.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `state` | JSON or Form | string | Authorization state. |
| `return_url` | JSON or Form | string | Current page URL. |
| `rememberme` | Form | string | Login sends "1" or ""; account linking omits it. |

**Request content type:** `application/x-www-form-urlencoded` for login; `application/json` for profile linking.

**Response:** Known JSON fields: `auth_url`, `error`, `state`, `success`. Schema incomplete.

**Notes:** Login sends URL-encoded form data; the profile linking controller sends JSON. The returned state may replace the requested state before navigation to auth_url.

