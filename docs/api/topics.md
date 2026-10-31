# Topics API

[API overview](../api-notes.md) · [All endpoints](index.md) · [Schemas](../api-schemas.md)

Event topics; organizer context for form editing and request administration. See [authentication](../api-notes.md#authentication) for scope limitations.

JSON request bodies use `application/json` unless an entry specifies another content type.

| Method | Endpoint |
|---|---|
| POST | [`/api/topics/add`](#apitopicsadd) |
| POST | [`/api/topics/add_child_topic`](#apitopicsadd_child_topic) |
| POST | [`/api/topics/del_child_topic`](#apitopicsdel_child_topic) |
| GET | [`/api/topics/download_files/{topic_url_code}`](#apitopicsdownload_filestopic_url_code) |
| POST | [`/api/topics/field_add`](#apitopicsfield_add) |
| POST | [`/api/topics/field_delete`](#apitopicsfield_delete) |
| POST | [`/api/topics/field_move`](#apitopicsfield_move) |
| POST | [`/api/topics/field_reorder`](#apitopicsfield_reorder) |
| POST | [`/api/topics/fill_from_template`](#apitopicsfill_from_template) |
| POST | [`/api/topics/fill_from_topic`](#apitopicsfill_from_topic) |
| POST | [`/api/topics/generate_cards_title`](#apitopicsgenerate_cards_title) |
| POST | [`/api/topics/get_all_requests`](#apitopicsget_all_requests) |
| GET / POST | [`/api/topics/get_list`](#apitopicsget_list) |
| GET | [`/api/topics/get_req_for_planner`](#apitopicsget_req_for_planner) |
| POST | [`/api/topics/get_requests`](#apitopicsget_requests) |
| POST | [`/api/topics/get_with_fields`](#apitopicsget_with_fields) |
| POST | [`/api/topics/get_with_groups`](#apitopicsget_with_groups) |
| POST | [`/api/topics/reorder_requests`](#apitopicsreorder_requests) |
| POST | [`/api/topics/save_field_field`](#apitopicssave_field_field) |
| POST | [`/api/topics/save_section_field`](#apitopicssave_section_field) |
| POST | [`/api/topics/save_topic_field`](#apitopicssave_topic_field) |
| POST | [`/api/topics/section_add`](#apitopicssection_add) |
| POST | [`/api/topics/section_delete`](#apitopicssection_delete) |
| POST | [`/api/topics/section_move`](#apitopicssection_move) |
| POST | [`/api/topics/section_reorder`](#apitopicssection_reorder) |
| POST | [`/api/topics/topic_delete`](#apitopicstopic_delete) |
| POST | [`/api/topics/topic_move`](#apitopicstopic_move) |
| POST | [`/api/topics/topic_reorder`](#apitopicstopic_reorder) |

## `/api/topics/add`

Create an empty topic at the end of the list.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `voting_group` | JSON | integer | Voting group identifier. Client default: 0. |

**Response:** Schema unknown.

**Notes:** No new id is returned. Fetch the new topic with `get_with_fields` and `topic_url_code: "new"`.

**SDK:** `topics.create()`.

## `/api/topics/add_child_topic`

Add `child_topic_id` to the group topic `url_code`.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `topic_url_code` | JSON | string | Topic URL code. |
| `child_topic_id` | JSON | integer | Topic to link or unlink in this group. |

**Response:** Object with `child_topics`: array of [TopicGroupLink](../api-schemas.md#topicgrouplink) objects.

**Response example:** `{"message": "ok", "child_topics": []}`

**SDK:** `topics.add_child_topic()`.

## `/api/topics/del_child_topic`

Remove `child_topic_id` from the group topic `url_code`.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `topic_url_code` | JSON | string | Topic URL code. |
| `child_topic_id` | JSON | integer | Topic to link or unlink in this group. |

**Response:** Object with `child_topics`: array of [TopicGroupLink](../api-schemas.md#topicgrouplink) objects.

**SDK:** `topics.delete_child_topic()`.

## `/api/topics/download_files/{topic_url_code}`

Download submitted files for the topic identified in the URL path.

**Method:** GET.

| Field | In | Type | Description |
|---|---|---|---|
| `topic_url_code` | Path | string | Topic URL code. |

**Response:** File download; archive format, content type and error representation are unverified.

## `/api/topics/field_add`

Add a built-in field to a section of a topic's form.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `topic_id` | JSON | integer | Topic identifier. |
| `section_id` | JSON | integer | Topic form section identifier. |
| `internal_name` | JSON | [FieldTemplate](../api-schemas.md#fieldtemplate) | Built-in template identifier. |

**Response:** Schema unknown.

**SDK:** `topics.add_field()`.

## `/api/topics/field_delete`

Delete a form field.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `topic_id` | JSON | integer | Topic identifier. |
| `section_id` | JSON | integer | Topic form section identifier. |
| `field_id` | JSON | integer | Form field identifier. |

**Response:** Schema unknown.

**SDK:** `topics.delete_field()`.

## `/api/topics/field_move`

Move a form field using the frontend movement action.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `topic_id` | JSON | identifier | Topic identifier. |
| `section_id` | JSON | identifier | Topic form section identifier. |
| `field_id` | JSON | identifier | Form field identifier. |
| `direction` | JSON | unknown | Movement selector; allowed values were not established. |

**Response:** Schema unknown.

## `/api/topics/field_reorder`

Move a form field to a new position or section.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `topic_id` | JSON | integer | Topic identifier. |
| `source_section_id` | JSON | integer | Source form section. |
| `target_section_id` | JSON | integer | Destination form section. |
| `field_id` | JSON | integer | Form field identifier. |
| `new_index` | JSON | integer | Zero-based destination position. |

**Response:** Schema unknown.

**SDK:** `topics.reorder_field()`.

## `/api/topics/fill_from_template`

Replace a topic's form with a built-in template.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `topic_id` | JSON | integer | Topic identifier. |
| `internal_name` | JSON | [TopicTemplate](../api-schemas.md#topictemplate) | Built-in template identifier. |

**Response:** Schema unknown.

**SDK:** `topics.fill_from_template()`.

## `/api/topics/fill_from_topic`

Replace a topic's form (and card rules) with a copy of another topic's.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `topic_id` | JSON | integer | Topic identifier. |
| `src_topic_id` | JSON | integer | Topic whose form and card rules are copied. |

**Response:** Schema unknown.

**SDK:** `topics.fill_from_topic()`.

## `/api/topics/generate_cards_title`

Rebuild card titles, announcements or diploma titles for all requests in a topic and return the updated topic requests.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `topic_id` | JSON | integer | Topic identifier. |
| `field_num` | JSON | [CardField](../api-schemas.md#cardfield) | Generated card field selector. Client default: 1. |

**Response:** Object with `requests`: array of [TopicRequest](../api-schemas.md#topicrequest) object.

**SDK:** `topics.generate_card_titles()`.

## `/api/topics/get_all_requests`

Every request of the event, across all topics.

**Method:** POST.

**Response:** array of [EventRequest](../api-schemas.md#eventrequest) object.

**SDK:** `topics.get_all_requests()`.

## `/api/topics/get_list`

All topics of the event.

**Method:** GET / POST.

| Field | In | Type | Description |
|---|---|---|---|
| `with_group_text` | JSON | boolean | Optional. Include topic grouping data. Client default: false. |
| `event_id` | JSON | integer | Optional. Event identifier. |

**Response:** array of [Topic](../api-schemas.md#topic) object.

**Notes:** GET returns the plain list; POST adds selectors or grouping options.

**SDK:** `topics.get_list()`.

## `/api/topics/get_req_for_planner`

Every request of the event with durations and members, for scheduling.

**Method:** GET.

**Response:** [PlannerData](../api-schemas.md#plannerdata) object.

**SDK:** `topics.get_requests_for_planner()`.

## `/api/topics/get_requests`

A topic and its requests.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `topic_id` | JSON | integer | Optional. Topic identifier. |
| `topic_url_code` | JSON | string | Optional. Topic URL code. |

**Response:** [TopicRequests](../api-schemas.md#topicrequests) object.

**Notes:** The caller sends either numeric `topic_id` or string `topic_url_code`, not both.

**Example:** `{"topic_id": 42}`

**SDK:** `topics.get_requests()`.

## `/api/topics/get_with_fields`

A topic with the sections and fields of its form.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `topic_url_code` | JSON | string | Topic URL code. |

**Response:** [TopicForm](../api-schemas.md#topicform) object.

**Example:** `{"topic_url_code": "example"}`

**SDK:** `topics.get_form()`.

## `/api/topics/get_with_groups`

A group topic with all event topics and its linked child topics.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `topic_url_code` | JSON | string | Topic URL code. |

**Response:** [TopicGroup](../api-schemas.md#topicgroup) object.

**SDK:** `topics.get_with_groups()`.

## `/api/topics/reorder_requests`

Renumber requests in a topic according to the planner schedule.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `topic_id` | JSON | integer | Topic identifier. |

**Response:** Schema unknown.

**SDK:** `topics.reorder_requests()`.

## `/api/topics/save_field_field`

Set a form field attribute.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `topic_id` | JSON | integer | Topic identifier. |
| `section_id` | JSON | integer | Topic form section identifier. |
| `field_id` | JSON | integer | Form field identifier. |
| `field` | JSON | string | Name of the field to edit. |
| `data` | JSON | field-dependent JSON value | New field value; depends on the selected field. |

**Response:** Schema unknown.

**SDK:** `topics.save_field()`.

## `/api/topics/save_section_field`

Set an attribute of a form section.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `topic_id` | JSON | integer | Topic identifier. |
| `section_id` | JSON | integer | Topic form section identifier. |
| `field` | JSON | string | Name of the field to edit. |
| `data` | JSON | field-dependent JSON value | New field value; depends on the selected field. |

**Response:** Schema unknown.

**SDK:** `topics.save_section()`.

## `/api/topics/save_topic_field`

Set a topic attribute.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `topic_id` | JSON | integer | Topic identifier. |
| `field` | JSON | string | Name of the field to edit. |
| `data` | JSON | field-dependent JSON value | New field value; depends on the selected field. |

**Response:** Schema unknown.

**SDK:** `topics.save_topic()`.

## `/api/topics/section_add`

Add a built-in section to a topic's form.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `topic_id` | JSON | integer | Topic identifier. |
| `internal_name` | JSON | [SectionTemplate](../api-schemas.md#sectiontemplate) | Built-in template identifier. |

**Response:** Schema unknown.

**SDK:** `topics.add_section()`.

## `/api/topics/section_delete`

Remove a section, with its fields, from a topic's form.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `topic_id` | JSON | integer | Topic identifier. |
| `section_id` | JSON | integer | Topic form section identifier. |

**Response:** Schema unknown.

**SDK:** `topics.delete_section()`.

## `/api/topics/section_move`

Move a form section using the frontend movement action.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `topic_id` | JSON | identifier | Topic identifier. |
| `section_id` | JSON | identifier | Topic form section identifier. |
| `direction` | JSON | unknown | Movement selector; allowed values were not established. |

**Response:** Schema unknown.

## `/api/topics/section_reorder`

Move a form section to a new position.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `topic_id` | JSON | integer | Topic identifier. |
| `section_id` | JSON | integer | Topic form section identifier. |
| `new_index` | JSON | integer | Zero-based destination position. |

**Response:** Schema unknown.

**SDK:** `topics.reorder_section()`.

## `/api/topics/topic_delete`

Delete a topic.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `topic_id` | JSON | integer | Topic identifier. |

**Response:** Schema unknown.

**SDK:** `topics.delete()`.

## `/api/topics/topic_move`

Move a topic using the frontend’s legacy movement action.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `topic_id` | JSON | identifier | Topic identifier. |
| `direction` | JSON | unknown | Movement selector; allowed values were not established. |

**Response:** Schema unknown.

## `/api/topics/topic_reorder`

Move a topic to another position in the list.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `topic_id` | JSON | integer | Topic identifier. |
| `new_index` | JSON | integer | Zero-based destination position. |

**Response:** Schema unknown.

**SDK:** `topics.reorder()`.
