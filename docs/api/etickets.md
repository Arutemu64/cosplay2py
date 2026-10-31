# Etickets API

[API overview](../api-notes.md) · [All endpoints](index.md) · [Schemas](../api-schemas.md)

Event ticket storefront, purchaser session, or organizer payment configuration, according to operation. See [authentication](../api-notes.md#authentication) for scope limitations.

JSON request bodies use `application/json` unless an entry specifies another content type.

| Method | Endpoint |
|---|---|
| POST | [`/api/etickets/create_ticket`](#apieticketscreate_ticket) |
| POST | [`/api/etickets/delete`](#apieticketsdelete) |
| GET | [`/api/etickets/dictionary-yookassa-vat`](#apieticketsdictionary-yookassa-vat) |
| POST | [`/api/etickets/eticketstypes_add`](#apieticketseticketstypes_add) |
| POST | [`/api/etickets/eticketstypes_delete`](#apieticketseticketstypes_delete) |
| POST | [`/api/etickets/eticketstypes_reorder`](#apieticketseticketstypes_reorder) |
| GET | [`/api/etickets/excel`](#apieticketsexcel) |
| GET | [`/api/etickets/get_list`](#apieticketsget_list) |
| GET | [`/api/etickets/get_paymethods`](#apieticketsget_paymethods) |
| POST | [`/api/etickets/get_ticket`](#apieticketsget_ticket) |
| POST | [`/api/etickets/get_ticket_status`](#apieticketsget_ticket_status) |
| GET / POST | [`/api/etickets/get_types`](#apieticketsget_types) |
| POST | [`/api/etickets/init-yookassa-payment`](#apieticketsinit-yookassa-payment) |
| GET | [`/api/etickets/printform`](#apieticketsprintform) |
| POST | [`/api/etickets/save_eticket_field`](#apieticketssave_eticket_field) |
| POST | [`/api/etickets/save_eticketstypes_field`](#apieticketssave_eticketstypes_field) |
| POST | [`/api/etickets/save_paymethods_field`](#apieticketssave_paymethods_field) |
| POST | [`/api/etickets/save_personal_data`](#apieticketssave_personal_data) |
| Unknown | [`/api/etickets/yandex_confirm`](#apieticketsyandex_confirm) |
| Unknown | [`/api/etickets/yookassa-postback-handler`](#apieticketsyookassa-postback-handler) |

## `/api/etickets/create_ticket`

Create an electronic ticket of `type_id` and return its id.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `etickets_type_id` | JSON | integer | Ticket tier identifier. |

**Response:** Object with `eticket_id`: integer.

**Example:** `{"etickets_type_id": 42}`

**SDK:** `etickets.create()`.

## `/api/etickets/delete`

Delete an electronic ticket.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `eticket_id` | JSON | integer | Electronic ticket order identifier. |

**Response:** Schema unknown.

**SDK:** `etickets.delete()`.

## `/api/etickets/dictionary-yookassa-vat`

Read the VAT choices used by the YooKassa setup form.

**Method:** GET. **Access:** Organizer payment configuration.

**Response:** JSON object mapping VAT labels to provider codes; the UI converts its entries into select options. Code types are unverified.

## `/api/etickets/eticketstypes_add`

Create a new electronic ticket tier.

**Method:** POST.

**Response:** Schema unknown.

**SDK:** `etickets.add_type()`.

## `/api/etickets/eticketstypes_delete`

Delete an electronic ticket tier.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `etickets_type_id` | JSON | integer | Ticket tier identifier. |

**Response:** Schema unknown.

**SDK:** `etickets.delete_type()`.

## `/api/etickets/eticketstypes_reorder`

Move an electronic ticket tier to a new position.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `etickets_type_id` | JSON | integer | Ticket tier identifier. |
| `new_index` | JSON | integer | Zero-based destination position. |

**Response:** Schema unknown.

**SDK:** `etickets.reorder_type()`.

## `/api/etickets/excel`

Download the electronic-ticket spreadsheet.

**Method:** GET.

**Response:** Electronic-ticket spreadsheet download; content type and file format are unverified.

## `/api/etickets/get_list`

All electronic tickets of the event.

**Method:** GET.

**Response:** Object with `etickets`: array of object with unknown values.

**SDK:** `etickets.get_list()`.

## `/api/etickets/get_paymethods`

Read configured payment providers.

**Method:** GET. **Access:** Organizer payment configuration.

**Response:** Known JSON fields: `etickets_paymethods`. Schema incomplete.

## `/api/etickets/get_ticket`

An electronic ticket with its tier and payment details.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `eticket_id` | JSON | string | Electronic ticket order identifier. |

**Response:** object with unknown values.

**Example:** `{"eticket_id": "42"}`

**SDK:** `etickets.get()`.

## `/api/etickets/get_ticket_status`

Payment status of an electronic ticket.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `eticket_id` | JSON | string | Electronic ticket order identifier. |

**Response:** Object with `eticket_status`: object with unknown values.

**SDK:** `etickets.get_status()`.

## `/api/etickets/get_types`

Electronic ticket tiers of the event.

**Method:** GET / POST.

| Field | In | Type | Description |
|---|---|---|---|
| `i_can_buy` | JSON | boolean | Optional. Send true to request purchasable ticket tiers. Client default: false. |

**Response:** Object with `etickets_types`: array of object with unknown values.

**Notes:** GET lists tiers; POST with `i_can_buy: true` asks for purchasable tiers.

**SDK:** `etickets.get_types()`.

## `/api/etickets/init-yookassa-payment`

Initialize a YooKassa payment from the ticket order page.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `ticket` | JSON | string | Electronic ticket order identifier. |
| `X-Idempotence-Key` | Header | string | Generated once and reused by the UI for the order attempt. |

**Response:** Object with `token` (string) used as the YooMoney widget confirmation token. Other fields and status codes are unverified.

**Notes:** Sends a JSON string body, not multipart data. Payment initialization may have external effects; retry semantics beyond the UI key reuse are unverified.

## `/api/etickets/printform`

Open the printable electronic ticket using the order id query parameter.

**Method:** GET.

| Field | In | Type | Description |
|---|---|---|---|
| `id` | Query | string | Electronic ticket order identifier. |

**Response:** Printable ticket page; response headers and populated body are unverified.

## `/api/etickets/save_eticket_field`

Set an organizer attribute of an electronic ticket and return it.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `eticket_id` | JSON | integer | Electronic ticket order identifier. |
| `field` | JSON | string | Name of the field to edit. |
| `data` | JSON | field-dependent JSON value | New field value; depends on the selected field. |

**Response:** Object with `eticket`: object with unknown values.

**SDK:** `etickets.save_field()`.

## `/api/etickets/save_eticketstypes_field`

Set an attribute of an electronic ticket tier.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `etickets_type_id` | JSON | integer | Ticket tier identifier. |
| `field` | JSON | string | Name of the field to edit. |
| `data` | JSON | field-dependent JSON value | New field value; depends on the selected field. |

**Response:** Schema unknown.

**SDK:** `etickets.save_type_field()`.

## `/api/etickets/save_paymethods_field`

Save one payment-provider setting.

**Method:** POST. **Access:** Organizer payment configuration.

| Field | In | Type | Description |
|---|---|---|---|
| `field` | JSON | string | Name of the field to edit. |
| `data` | JSON | unknown | New field value; depends on the selected field. |

**Response:** Known JSON fields: `etickets_paymethods`. Schema incomplete.

**Notes:** The UI edits yandex_enabled, yandex_account, yandex_secret, yookassa_enabled, yookassa_shop_id, yookassa_api_key, yookassa_vat_code, manual_enabled and manual_text. Enabled selectors send strings "0"/"1"; VAT values come from dictionary-yookassa-vat.

## `/api/etickets/save_personal_data`

Save buyer personal data on an electronic ticket.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `eticket_id` | JSON | string | Electronic ticket order identifier. |
| `user_data` | JSON | object | Buyer fields: fio, email, mobile and city (strings). |

**Response:** Schema unknown.

**SDK:** `etickets.save_personal_data()`.

## `/api/etickets/yandex_confirm`

Provider confirmation callback displayed in payment setup instructions.

**Method:** Unknown. **Access:** External payment provider callback.

| Field | In | Type | Description |
|---|---|---|---|
| `(body)` | Unknown | unknown | Contract not established from the linked source. |

**Response:** Schema unknown.

**Notes:** Provider callback URL displayed in setup instructions. Method, payload, signature verification and response contract were not established.

## `/api/etickets/yookassa-postback-handler`

YooKassa callback displayed in payment setup instructions.

**Method:** Unknown. **Access:** External payment provider callback.

| Field | In | Type | Description |
|---|---|---|---|
| `(body)` | Unknown | unknown | Contract not established from the linked source. |

**Response:** Schema unknown.

**Notes:** Provider callback URL displayed in setup instructions. Method, payload, signature verification and response contract were not established.

