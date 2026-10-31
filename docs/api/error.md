# Error API

[API overview](../api-notes.md) · [All endpoints](index.md) · [Schemas](../api-schemas.md)

Ticket-page frontend diagnostics. See [authentication](../api-notes.md#authentication) for scope limitations.

JSON request bodies use `application/json` unless an entry specifies another content type.

| Method | Endpoint |
|---|---|
| POST | [`/api/error/handle`](#apierrorhandle) |

## `/api/error/handle`

Submit frontend ticket error diagnostics; the caller sets module, entity and trace headers.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `X-Error-Module` | Header | string | UI sends "eticket". |
| `X-Entity-Id` | Header | identifier | Electronic ticket order identifier. |
| `X-Trace-Id` | Header | string | Generated UUID shown to the user. |

**Response:** Response schema unknown; the success callback does not inspect the body.

**Notes:** The controller passes `body` in its AngularJS HTTP config instead of `data`; the actual transmitted diagnostics payload is unverified.

