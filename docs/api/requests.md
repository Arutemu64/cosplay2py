# Requests API

[API overview](../api-notes.md) · [All endpoints](index.md) · [Schemas](../api-schemas.md)

Event requests; author, participant, curator or organizer visibility depends on the operation. See [authentication](../api-notes.md#authentication) for scope limitations.

JSON request bodies use `application/json` unless an entry specifies another content type.

| Method | Endpoint |
|---|---|
| POST | [`/api/requests/add_comment`](#apirequestsadd_comment) |
| POST | [`/api/requests/add_orgcomment`](#apirequestsadd_orgcomment) |
| POST | [`/api/requests/change_topic`](#apirequestschange_topic) |
| POST | [`/api/requests/create`](#apirequestscreate) |
| POST | [`/api/requests/create_reqsection`](#apirequestscreate_reqsection) |
| POST | [`/api/requests/del_comment`](#apirequestsdel_comment) |
| POST | [`/api/requests/del_orgcomment`](#apirequestsdel_orgcomment) |
| POST | [`/api/requests/delete_file`](#apirequestsdelete_file) |
| POST | [`/api/requests/delete_image`](#apirequestsdelete_image) |
| POST | [`/api/requests/delete_reqsection`](#apirequestsdelete_reqsection) |
| POST | [`/api/requests/feedbacks_add`](#apirequestsfeedbacks_add) |
| POST | [`/api/requests/feedbacks_del`](#apirequestsfeedbacks_del) |
| POST | [`/api/requests/feedbacks_get`](#apirequestsfeedbacks_get) |
| POST | [`/api/requests/generate_card_announcement`](#apirequestsgenerate_card_announcement) |
| POST | [`/api/requests/generate_card_diplom`](#apirequestsgenerate_card_diplom) |
| POST | [`/api/requests/generate_card_title`](#apirequestsgenerate_card_title) |
| POST | [`/api/requests/generate_voting_num`](#apirequestsgenerate_voting_num) |
| POST | [`/api/requests/get`](#apirequestsget) |
| POST | [`/api/requests/get_comments`](#apirequestsget_comments) |
| POST | [`/api/requests/get_orgcomments`](#apirequestsget_orgcomments) |
| POST | [`/api/requests/get_user`](#apirequestsget_user) |
| POST | [`/api/requests/get_value_history`](#apirequestsget_value_history) |
| POST | [`/api/requests/save_data`](#apirequestssave_data) |
| POST | [`/api/requests/save_field`](#apirequestssave_field) |
| POST | [`/api/requests/search`](#apirequestssearch) |
| POST | [`/api/requests/set_status`](#apirequestsset_status) |
| POST | [`/api/requests/upload_file`](#apirequestsupload_file) |
| POST | [`/api/requests/upload_image`](#apirequestsupload_image) |

## `/api/requests/add_comment`

Post a comment visible to the request's author.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `request_id` | JSON | string | Request identifier. |
| `comment` | JSON | string | Comment text. |
| `email` | JSON | boolean | Notify the author by email. Client default: true. |
| `sms` | JSON | boolean | Notify the author by SMS. Client default: false. |

**Response:** Observed response includes `message: "ok"` and `sms_result: null`; the non-null SMS result shape is unknown.

**SDK:** `requests.add_comment()`.

## `/api/requests/add_orgcomment`

Post an internal organizer comment.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `request_id` | JSON | string | Request identifier. |
| `comment` | JSON | string | Comment text. |

**Response:** Schema unknown.

**SDK:** `requests.add_org_comment()`.

## `/api/requests/change_topic`

Move a request to another topic of the event.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `request_id` | JSON | integer | Request identifier. |
| `target_topic_id` | JSON | integer | Destination topic identifier. |
| `forceflag` | JSON | string | Optional. Use "force" to discard incompatible fields during a topic move. |

**Response:** [TopicChange](../api-schemas.md#topicchange) object.

**Notes:** A compatible destination must contain all existing sections and fields. `forceflag: "force"` allows the move while dropping incompatible data.

**SDK:** `requests.change_topic()`.

## `/api/requests/create`

Create an empty request in a topic and return its id.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `topic_id` | JSON | integer | Topic identifier. |

**Response:** Object with `requestId`: integer.

**Notes:** Follow creation with one `create_reqsection` call per form section; see [request creation](workflows.md#create-a-request).

**Example:** `{"topic_id": 42}`

**Response example:** `{"message": "ok", "requestId": 5001}`

**SDK:** `requests.create()`.

## `/api/requests/create_reqsection`

Add a section of the request's topic to a request.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `request_id` | JSON | integer | Request identifier. |
| `topic_section_id` | JSON | integer | Topic form section identifier. |
| `ord` | JSON | integer | Order of this request section instance. |

**Response:** [NewRequestSection](../api-schemas.md#newrequestsection) object.

**Example:** `{"request_id": 42, "topic_section_id": 42, "ord": 0}`

**SDK:** `requests.create_section()`.

## `/api/requests/del_comment`

Delete a comment of a request (`Comment.id`).

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `request_id` | JSON | string | Request identifier. |
| `comment_id` | JSON | integer | Comment identifier. |

**Response:** Schema unknown.

**SDK:** `requests.delete_comment()`.

## `/api/requests/del_orgcomment`

Delete an internal organizer comment.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `request_id` | JSON | string | Request identifier. |
| `comment_id` | JSON | integer | Comment identifier. |

**Response:** Schema unknown.

**SDK:** `requests.delete_org_comment()`.

## `/api/requests/delete_file`

Remove the file stored as `value_id` from a `file` field.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `request_id` | JSON | integer | Request identifier. |
| `request_section_id` | JSON | string | Request section instance identifier. |
| `topic_field_id` | JSON | integer | Topic form field identifier. |
| `value_id` | JSON | string | Stored value identifier; uploads use 0 for an empty field. |

**Response:** Schema unknown.

**SDK:** `requests.delete_file()`.

## `/api/requests/delete_image`

Remove the image stored as `value_id` from an `image` field.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `request_id` | JSON | integer | Request identifier. |
| `request_section_id` | JSON | string | Request section instance identifier. |
| `topic_field_id` | JSON | integer | Topic form field identifier. |
| `value_id` | JSON | string | Stored value identifier; uploads use 0 for an empty field. |

**Response:** Schema unknown.

**SDK:** `requests.delete_image()`.

## `/api/requests/delete_reqsection`

Remove a repeated section (`RequestSection.id`) from a request.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `request_id` | JSON | integer | Request identifier. |
| `request_section_id` | JSON | integer | Request section instance identifier. |

**Response:** Schema unknown.

**SDK:** `requests.delete_section()`.

## `/api/requests/feedbacks_add`

Add feedback and return the updated feedback list.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `request_id` | JSON | integer | Request identifier. |
| `user_id` | JSON | integer | User identifier. |
| `mark` | JSON | string | Feedback mark as a string: "-1", "0" or "1". |
| `info` | JSON | string | Feedback text. |

**Response:** Object with `feedbacks`: array of [Feedback](../api-schemas.md#feedback) object.

**Example:** `{"request_id": 42, "user_id": 42, "mark": "-1", "info": "example"}`

**SDK:** `requests.add_feedback()`.

## `/api/requests/feedbacks_del`

Delete feedback and return the updated feedback list.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `request_id` | JSON | integer | Request identifier. |
| `user_id` | JSON | integer | User identifier. |
| `feedback_id` | JSON | integer | Feedback entry to delete. |

**Response:** Object with `feedbacks`: array of [Feedback](../api-schemas.md#feedback) object.

**SDK:** `requests.delete_feedback()`.

## `/api/requests/feedbacks_get`

Organizer feedback about a request participant.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `request_id` | JSON | integer | Request identifier. |
| `user_id` | JSON | integer | User identifier. |

**Response:** Object with `feedbacks`: array of [Feedback](../api-schemas.md#feedback) object.

**SDK:** `requests.get_feedbacks()`.

## `/api/requests/generate_card_announcement`

The request's announcement text, from `card_announcement_rule`.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `request_id` | JSON | integer | Request identifier. |

**Response:** Object with `text`: string.

**SDK:** `requests.generate_card_announcement()`.

## `/api/requests/generate_card_diplom`

The request's diploma text, built from the topic's `card_diplom_rule`.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `request_id` | JSON | integer | Request identifier. |

**Response:** Object with `text`: string.

**SDK:** `requests.generate_card_diplom()`.

## `/api/requests/generate_card_title`

The request's card title, built from the topic's `card_name_rule`.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `request_id` | JSON | integer | Request identifier. |

**Response:** Object with `text`: string.

**SDK:** `requests.generate_card_title()`.

## `/api/requests/generate_voting_num`

Assign and return the next voting number for a request.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `request_id` | JSON | integer | Request identifier. |

**Response:** Object with `voting_number`: integer.

**SDK:** `requests.generate_voting_number()`.

## `/api/requests/get`

A request with its topic, form schema and filled-in values.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `request_id` | JSON | string | Request identifier. |

**Response:** [RequestDetails](../api-schemas.md#requestdetails) object.

**SDK:** `requests.get()`.

## `/api/requests/get_comments`

Comments visible to the request's author.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `request_id` | JSON | string | Request identifier. |

**Response:** Object with `comments`: array of [Comment](../api-schemas.md#comment) object.

**Example:** `{"request_id": "42"}`

**Response example:** `{"message": "ok", "comments": []}`

**SDK:** `requests.get_comments()`.

## `/api/requests/get_orgcomments`

Internal comments visible to organizers only.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `request_id` | JSON | string | Request identifier. |

**Response:** Object with `comments`: array of [Comment](../api-schemas.md#comment) object.

**SDK:** `requests.get_org_comments()`.

## `/api/requests/get_user`

A participant of the request and their other requests in this event.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `user_id` | JSON | string | User identifier. |
| `request_id` | JSON | integer | Request identifier. |

**Response:** [RequestUserInfo](../api-schemas.md#requestuserinfo) object.

**Example:** `{"user_id": "42", "request_id": 42}`

**SDK:** `requests.get_user()`.

## `/api/requests/get_value_history`

Saved versions of a form value (`RequestValue.id`) and who saved them.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `request_id` | JSON | integer | Request identifier. |
| `value_id` | JSON | string | Stored value identifier; uploads use 0 for an empty field. |

**Response:** Object with `value_history`: array of [ValueChange](../api-schemas.md#valuechange) object.

**Notes:** Here avatar `image_update_time` uses a UTC timestamp string, unlike numeric avatar times on some other endpoints.

**SDK:** `requests.get_value_history()`.

## `/api/requests/save_data`

Set an organizer field of a request.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `request_id` | JSON | integer | Request identifier. |
| `field` | JSON | string | Name of the field to edit. |
| `data` | JSON | field-dependent JSON value | New field value; depends on the selected field. |

**Response:** Schema unknown.

**SDK:** `requests.save_data()`.

## `/api/requests/save_field`

Set a form field of a request and return the id of the stored value.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `request_id` | JSON | integer | Request identifier. |
| `request_section_id` | JSON | integer | Request section instance identifier. |
| `topic_field_id` | JSON | integer | Topic form field identifier. |
| `data` | JSON | string, integer or null | New field value; depends on the selected field. |
| `value_id` | JSON | integer | Optional. Stored value identifier; uploads use 0 for an empty field. |

**Response:** Object with `id`: integer.

**Notes:** Strings are used for most field values, a numeric user id for a user picker, and null to clear. File links are JSON-encoded strings. Images and uploaded files use separate endpoints.

**Example:** `{"request_id": 42, "request_section_id": 42, "topic_field_id": 42, "data": "example"}`

**Response example:** `{"message": "ok", "id": 9}`

**SDK:** `requests.save_field()`.

## `/api/requests/search`

Search requests in the event by text.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `search_text` | JSON | string | Search text. |

**Response:** Object with `requests`: array of [RequestSearchResult](../api-schemas.md#requestsearchresult) objects.

**SDK:** `requests.search()`.

## `/api/requests/set_status`

Move a request to `status` and return its request and voting numbers.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `request_id` | JSON | integer | Request identifier. |
| `status` | JSON | [RequestStatus](../api-schemas.md#requeststatus) | New request status. |

**Response:** [StatusChange](../api-schemas.md#statuschange) object.

**SDK:** `requests.set_status()`.

## `/api/requests/upload_file`

Upload a file into a `file` field of a request.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `request_id` | Multipart | text form field | Request identifier. |
| `request_section_id` | Multipart | text form field | Request section instance identifier. |
| `topic_field_id` | Multipart | text form field | Topic form field identifier. |
| `value_id` | Multipart | text form field | Stored value identifier; uploads use 0 for an empty field. |
| `uploaded_file` | Multipart | file | File contents. |

**Request content type:** `multipart/form-data`.

**Response:** [UploadedFile](../api-schemas.md#uploadedfile) object.

**Notes:** Use multipart/form-data. The returned `id` replaces the empty value id; `value` becomes the stored form value. See [uploads](workflows.md#upload-a-request-image-or-file).

**SDK:** `requests.upload_file()`.

## `/api/requests/upload_image`

Upload an image into an `image` field of a request.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `request_id` | Multipart | text form field | Request identifier. |
| `request_section_id` | Multipart | text form field | Request section instance identifier. |
| `topic_field_id` | Multipart | text form field | Topic form field identifier. |
| `value_id` | Multipart | text form field | Stored value identifier; uploads use 0 for an empty field. |
| `uploaded_image` | Multipart | file | Image contents. |

**Request content type:** `multipart/form-data`.

**Response:** [UploadedImage](../api-schemas.md#uploadedimage) object.

**Notes:** Use multipart/form-data. The returned `id` replaces the empty value id; `value` becomes the stored form value. See [uploads](workflows.md#upload-a-request-image-or-file).

**SDK:** `requests.upload_image()`.
