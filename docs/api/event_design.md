# Event Design API

[API overview](../api-notes.md) · [All endpoints](index.md) · [Schemas](../api-schemas.md)

Event design; organizer context for editing. See [authentication](../api-notes.md#authentication) for scope limitations.

JSON request bodies use `application/json` unless an entry specifies another content type.

| Method | Endpoint |
|---|---|
| POST | [`/api/event_design/delete_eventimage`](#apievent_designdelete_eventimage) |
| GET | [`/api/event_design/delete_header_logo`](#apievent_designdelete_header_logo) |
| GET | [`/api/event_design/delete_panel_logo`](#apievent_designdelete_panel_logo) |
| GET | [`/api/event_design/delete_site_background`](#apievent_designdelete_site_background) |
| GET | [`/api/event_design/get`](#apievent_designget) |
| GET | [`/api/event_design/get_eventimages`](#apievent_designget_eventimages) |
| POST | [`/api/event_design/save_design`](#apievent_designsave_design) |
| POST | [`/api/event_design/upload_image`](#apievent_designupload_image) |

## `/api/event_design/delete_eventimage`

Delete a design image by file name and return the image mapping.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `eventimage` | JSON | string | Stored image filename. |

**Response:** Object with `eventimages`: object with string values.

**SDK:** `design.delete_image()`.

## `/api/event_design/delete_header_logo`

Delete the site header logo.

**Method:** GET.

**Response:** Schema unknown.

**Notes:** Deletes the selected design asset despite using GET.

**SDK:** `design.delete_header_logo()`.

## `/api/event_design/delete_panel_logo`

Delete the top navigation bar logo.

**Method:** GET.

**Response:** Schema unknown.

**Notes:** Deletes the selected design asset despite using GET.

**SDK:** `design.delete_panel_logo()`.

## `/api/event_design/delete_site_background`

Delete the site background image.

**Method:** GET.

**Response:** Schema unknown.

**Notes:** Deletes the selected design asset despite using GET.

**SDK:** `design.delete_site_background()`.

## `/api/event_design/get`

Colors and custom CSS of the event site.

**Method:** GET.

**Response:** Object with `design`: [EventDesign](../api-schemas.md#eventdesign) object.

**SDK:** `design.get()`.

## `/api/event_design/get_eventimages`

Uploaded design images: image ID -> file name.

**Method:** GET.

**Response:** Object with `eventimages`: object with string values.

**SDK:** `design.get_images()`.

## `/api/event_design/save_design`

Update the supplied design settings.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `(partial design fields)` | JSON | object | Top-level fields from the EventDesign schema; send only changed fields. |

**Response:** Schema unknown.

**Notes:** Partial design objects are accepted; palette, header and CSS were observed saved separately.

**SDK:** `design.save()`.

## `/api/event_design/upload_image`

Upload a design image and return the updated image mapping.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `eventimage` | Multipart | file | Stored image filename. |

**Request content type:** `multipart/form-data`.

**Response:** Object with `eventimages`: object with string values.

**SDK:** `design.upload_image()`.
