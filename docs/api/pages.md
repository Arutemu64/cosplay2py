# Pages API

[API overview](../api-notes.md) · [All endpoints](index.md) · [Schemas](../api-schemas.md)

Event pages; organizer context for editing. See [authentication](../api-notes.md#authentication) for scope limitations.

JSON request bodies use `application/json` unless an entry specifies another content type.

| Method | Endpoint |
|---|---|
| POST | [`/api/pages/add_page`](#apipagesadd_page) |
| POST | [`/api/pages/delete_page`](#apipagesdelete_page) |
| GET | [`/api/pages/get_list`](#apipagesget_list) |
| POST | [`/api/pages/get_page`](#apipagesget_page) |
| POST | [`/api/pages/page_reorder`](#apipagespage_reorder) |
| POST | [`/api/pages/save_page_field`](#apipagessave_page_field) |
| POST | [`/api/pages/save_page_fields`](#apipagessave_page_fields) |

## `/api/pages/add_page`

Add an empty page, folder or link and return its id.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `parent_id` | JSON | integer or null | Parent folder; null selects the top level. |
| `type` | JSON | [PageType](../api-schemas.md#pagetype) | Page or folder type. |

**Response:** Object with `page_id`: integer.

**Example:** `{"parent_id": null, "type": "page"}`

**SDK:** `pages.create()`.

## `/api/pages/delete_page`

Remove a page, folder or link.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `id` | JSON | integer | Resource identifier. |

**Response:** Schema unknown.

**SDK:** `pages.delete()`.

## `/api/pages/get_list`

Text pages of the event site.

**Method:** GET.

**Response:** array of [Page](../api-schemas.md#page) object.

**SDK:** `pages.get_list()`.

## `/api/pages/get_page`

A page with its content.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `page_id` | JSON | string | Page identifier. |

**Response:** [PageDetails](../api-schemas.md#pagedetails) object.

**SDK:** `pages.get()`.

## `/api/pages/page_reorder`

Move a page to a new position.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `page_id` | JSON | integer | Page identifier. |
| `source_page_id` | JSON | integer or null | Source folder id; null means top level. |
| `target_page_id` | JSON | integer or null | Destination folder id; null means top level. |
| `new_index` | JSON | integer | Zero-based destination position. |

**Response:** Schema unknown.

**Notes:** Only top-level moves with both parent ids null were observed in captures; moves between folders are frontend evidence only.

**SDK:** `pages.reorder()`.

## `/api/pages/save_page_field`

Set an attribute of a page.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `id` | JSON | integer | Resource identifier. |
| `field` | JSON | string | Name of the field to edit. |
| `data` | JSON | field-dependent JSON value | New field value; depends on the selected field. |

**Response:** Schema unknown.

**Example:** `{"id": 42, "field": "title", "data": "Example"}`

**SDK:** `pages.save_field()`.

## `/api/pages/save_page_fields`

Set several attributes of a page at once.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `id` | JSON | integer | Resource identifier. |
| `page_data` | JSON | object | Partial page fields to save. |

**Response:** Schema unknown.

**SDK:** `pages.save_fields()`.
