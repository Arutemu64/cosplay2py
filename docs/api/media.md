# Media API

[API overview](../api-notes.md) · [All endpoints](index.md) · [Schemas](../api-schemas.md)

Public event media and organizer album management. See [authentication](../api-notes.md#authentication) for scope limitations.

JSON request bodies use `application/json` unless an entry specifies another content type.

| Method | Endpoint |
|---|---|
| GET | [`/api/media/get_data`](#apimediaget_data) |
| POST | [`/api/media/photoalbum_add`](#apimediaphotoalbum_add) |
| POST | [`/api/media/photoalbum_delete`](#apimediaphotoalbum_delete) |
| GET | [`/api/media/recalc_photo`](#apimediarecalc_photo) |
| POST | [`/api/media/save_photoalbum_field`](#apimediasave_photoalbum_field) |

## `/api/media/get_data`

Photo albums and photos.

**Method:** GET.

**Response:** [MediaData](../api-schemas.md#mediadata) object.

**SDK:** `media.get_data()`.

## `/api/media/photoalbum_add`

Link a photo album to the event.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `user_title` | JSON | string | Album owner / credit text. |
| `url` | JSON | string | Photo album URL. |

**Response:** Success: `{"message":"ok"}`.

**Notes:** An empty JSON object returned HTTP 500; sending `user_title` and `url` succeeded.

**Example:** `{"user_title": "example", "url": "example"}`

**SDK:** `media.add_album()`.

## `/api/media/photoalbum_delete`

Remove a linked photo album from the event.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `photoalbum_id` | JSON | integer | Photo album identifier. |

**Response:** Schema unknown.

**SDK:** `media.delete_album()`.

## `/api/media/recalc_photo`

Invoke album photo recalculation through the media administration link.

**Method:** GET.

**Response:** Schema unknown.

**Notes:** Starts scanning photo albums. The UI warns that closing the browser window early interrupts scanning; it may take several minutes.

## `/api/media/save_photoalbum_field`

Set an attribute of a linked photo album (`user_title` or `url`).

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `photoalbum_id` | JSON | integer | Photo album identifier. |
| `field` | JSON | string | Name of the field to edit. |
| `data` | JSON | field-dependent JSON value | New field value; depends on the selected field. |

**Response:** Schema unknown.

**SDK:** `media.save_album_field()`.
