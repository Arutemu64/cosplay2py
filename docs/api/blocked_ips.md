# Blocked Ips API

[API overview](../api-notes.md) · [All endpoints](index.md) · [Schemas](../api-schemas.md)

Platform administration browser context; UI gate: role >= 100. See [authentication](../api-notes.md#authentication) for scope limitations.

JSON request bodies use `application/json` unless an entry specifies another content type.

| Method | Endpoint |
|---|---|
| POST | [`/api/blocked_ips/list_detailed`](#apiblocked_ipslist_detailed) |
| POST | [`/api/blocked_ips/returnto_list`](#apiblocked_ipsreturnto_list) |
| POST | [`/api/blocked_ips/returnto_settings`](#apiblocked_ipsreturnto_settings) |
| POST | [`/api/blocked_ips/returnto_unblock`](#apiblocked_ipsreturnto_unblock) |
| POST | [`/api/blocked_ips/settings`](#apiblocked_ipssettings) |
| POST | [`/api/blocked_ips/unblock`](#apiblocked_ipsunblock) |

## `/api/blocked_ips/list_detailed`

List CSRF-related IP blocks for administration.

**Method:** POST.

**Input:** Empty JSON object: `{}`.

**Response:** Known JSON fields: `blocked_ips`. Schema incomplete.

## `/api/blocked_ips/returnto_list`

List return-URL-related IP blocks for administration.

**Method:** POST.

**Input:** Empty JSON object: `{}`.

**Response:** Known JSON fields: `blocked_ips`. Schema incomplete.

## `/api/blocked_ips/returnto_settings`

Read return-URL blocking settings.

**Method:** POST.

**Input:** Empty JSON object: `{}`.

**Response:** Schema unknown.

## `/api/blocked_ips/returnto_unblock`

Remove an IP block in the return-URL blocking system.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `ip` | JSON | string | IP address to unblock. |

**Response:** Known JSON fields: `success`. Schema incomplete.

## `/api/blocked_ips/settings`

Read CSRF blocking settings.

**Method:** POST.

**Input:** Empty JSON object: `{}`.

**Response:** Schema unknown.

## `/api/blocked_ips/unblock`

Remove an IP block in the CSRF blocking system.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `ip` | JSON | string | IP address to unblock. |

**Response:** Known JSON fields: `success`. Schema incomplete.

