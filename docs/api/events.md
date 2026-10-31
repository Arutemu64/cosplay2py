# Events API

[API overview](../api-notes.md) · [All endpoints](index.md) · [Schemas](../api-schemas.md)

Event context for settings and organizer operations; portal context for listings and creation. See [authentication](../api-notes.md#authentication) for scope limitations.

JSON request bodies use `application/json` unless an entry specifies another content type.

| Method | Endpoint |
|---|---|
| POST | [`/api/events/add_curator`](#apieventsadd_curator) |
| POST | [`/api/events/add_org`](#apieventsadd_org) |
| POST | [`/api/events/change_mainorg`](#apieventschange_mainorg) |
| POST | [`/api/events/check_external_domain`](#apieventscheck_external_domain) |
| POST | [`/api/events/create_festival`](#apieventscreate_festival) |
| POST | [`/api/events/create_festival_logo`](#apieventscreate_festival_logo) |
| POST | [`/api/events/delete_curator`](#apieventsdelete_curator) |
| POST | [`/api/events/delete_org`](#apieventsdelete_org) |
| GET | [`/api/events/export_plan`](#apieventsexport_plan) |
| POST | [`/api/events/filter_list`](#apieventsfilter_list) |
| GET | [`/api/events/get/{id}`](#apieventsgetid) |
| POST | [`/api/events/get_blank_by_id`](#apieventsget_blank_by_id) |
| GET | [`/api/events/get_blank_xls`](#apieventsget_blank_xls) |
| GET | [`/api/events/get_buttons_state_1`](#apieventsget_buttons_state_1) |
| GET | [`/api/events/get_event_state`](#apieventsget_event_state) |
| GET | [`/api/events/get_html_menu`](#apieventsget_html_menu) |
| GET | [`/api/events/get_newrequest_state`](#apieventsget_newrequest_state) |
| GET | [`/api/events/get_orgs_curators`](#apieventsget_orgs_curators) |
| GET | [`/api/events/get_plan`](#apieventsget_plan) |
| GET | [`/api/events/get_settings`](#apieventsget_settings) |
| GET | [`/api/events/get_topics_state`](#apieventsget_topics_state) |
| GET | [`/api/events/get_topics_statistic`](#apieventsget_topics_statistic) |
| GET | [`/api/events/get_types`](#apieventsget_types) |
| POST | [`/api/events/save_newevents_field`](#apieventssave_newevents_field) |
| POST | [`/api/events/save_newevents_status`](#apieventssave_newevents_status) |
| POST | [`/api/events/save_plan`](#apieventssave_plan) |
| POST | [`/api/events/save_setting`](#apieventssave_setting) |
| POST | [`/api/events/search`](#apieventssearch) |
| POST | [`/api/events/set_gate`](#apieventsset_gate) |
| GET | [`/api/events/winners`](#apieventswinners) |

## `/api/events/add_curator`

Assign `user_id` as a curator of `topic_id`.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `user_id` | JSON | integer | User identifier. |
| `topic_id` | JSON | integer | Topic identifier. |

**Response:** Schema unknown.

**SDK:** `events.add_curator()`.

## `/api/events/add_org`

Add an organizer to the event.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `user_id` | JSON | integer | User identifier. |

**Response:** Schema unknown.

**SDK:** `events.add_org()`.

## `/api/events/change_mainorg`

Transfer the main organizer role to `user_id`.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `user_id` | JSON | integer | User identifier. |

**Response:** Schema unknown.

**SDK:** `events.change_main_org()`.

## `/api/events/check_external_domain`

Check the domain entered in the event configuration UI.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `domain` | JSON | string | Domain entered in the event settings. |

**Response:** Schema unknown.

**Notes:** The UI discards stale results when the requested domain has changed.

## `/api/events/create_festival`

Create a festival from the portal's creation form.

**Method:** POST. **Access:** Portal UI; event-token support was observed for the listing/type reads only.

| Field | In | Type | Description |
|---|---|---|---|
| `create_method` | JSON | string | UI default: links. Choices: links, pages, copy. |
| `event_type_id` | JSON | identifier | UI initializes "1"; select options use event type ids. |
| `title` | JSON | string | Event title. |
| `short_title` | JSON | string | Short title. |
| `description` | JSON | string | Event description. |
| `site` | JSON | string | Existing event website. |
| `subdomain` | JSON | string | Requested event subdomain. |
| `domain` | JSON | string | Optional custom domain. |
| `city` | JSON | string | Event city. |
| `start_time` | JSON | string | DD.MM.YYYY. |
| `end_time` | JSON | string | DD.MM.YYYY. |
| `timezone` | JSON | object | Selected timezone option object; not just an IANA string. |
| `logo` | JSON | string | Filename returned by create_festival_logo. |

**Response:** Object with `new_event_id`: integer.

**SDK:** `events.create_festival()`.

## `/api/events/create_festival_logo`

Upload a creation-form logo and return its temporary filename.

**Method:** POST. **Access:** Portal UI; event-token support was observed for the listing/type reads only.

| Field | In | Type | Description |
|---|---|---|---|
| `mainlogo` | Multipart | file | Creation-form logo file. |

**Request content type:** `multipart/form-data`.

**Response:** Object with `logofilename`: string.

**SDK:** `events.create_festival_logo()`.

## `/api/events/delete_curator`

Remove `user_id` as a curator of `topic_id`.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `user_id` | JSON | integer | User identifier. |
| `topic_id` | JSON | integer | Topic identifier. |

**Response:** Schema unknown.

**SDK:** `events.delete_curator()`.

## `/api/events/delete_org`

Remove an organizer from the event.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `user_id` | JSON | integer | User identifier. |

**Response:** Schema unknown.

**SDK:** `events.delete_org()`.

## `/api/events/export_plan`

Download the planner export through browser navigation.

**Method:** GET.

**Response:** Spreadsheet download. File format, response headers and error representation are unverified.

## `/api/events/filter_list`

Portal events for the selected year.

**Method:** POST. **Access:** Portal UI; event-token support was observed for the listing/type reads only.

| Field | In | Type | Description |
|---|---|---|---|
| `active_year` | JSON | string | Year selector from the portal route. |

**Response:** Schema unknown.

**SDK:** `events.filter_list()`.

## `/api/events/get/{id}`

Look up an event by path id in the admin credential-scope selector.

**Method:** GET. **Access:** Platform administration browser UI.

| Field | In | Type | Description |
|---|---|---|---|
| `id` | Path | identifier | Event to look up. |

**Response:** Schema unknown.

## `/api/events/get_blank_by_id`

Render a printable report as HTML.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `blank_id` | JSON | string | Report identifier. |
| `req_approved` | JSON | boolean | Include approved requests. Client default: true. |
| `picture_height` | JSON | integer | Embedded image height in pixels. Client default: 80. |
| `req_disapproved` | JSON | boolean | Optional. Include rejected requests. Client default: false. |
| `req_other` | JSON | boolean | Optional. Include requests with other statuses. Client default: false. |
| `topic_url_code` | JSON | string | Optional UI report filter. |

**Response:** [Blank](../api-schemas.md#blank) object; or [TopicsRegistration](../api-schemas.md#topicsregistration) object; or [AlphabetRegistration](../api-schemas.md#alphabetregistration) object.

**Notes:** Report ids `reg_topics` and `reg_alphabet` return structured registration data; other reports return HTML plus titles. The UI can also send `topic_url_code` as a topic filter.

**Example:** `{"blank_id": "winners", "req_approved": true, "picture_height": 80}`

**SDK:** `events.get_blank()`, `events.get_reg_topics()`, `events.get_reg_alphabet()`.

## `/api/events/get_blank_xls`

Download a spreadsheet report using the selected report options.

**Method:** GET.

| Field | In | Type | Description |
|---|---|---|---|
| `blank_id` | Query | string | Report identifier. |
| `req_approved` | Query | flag | Include approved requests. |
| `req_disapproved` | Query | flag | Include rejected requests. |
| `req_other` | Query | flag | Include requests with other statuses. |
| `topic_url_code` | Query | string | Topic URL code. |
| `picture_height` | Query | integer | Embedded image height in pixels. |

**Response:** Spreadsheet report download. File format, response headers and error representation are unverified.

## `/api/events/get_buttons_state_1`

Read menu button visibility and countdown state.

**Method:** GET.

**Response:** Schema unknown.

## `/api/events/get_event_state`

Request counters for the whole event.

**Method:** GET.

**Response:** Object with `state`: [EventState](../api-schemas.md#eventstate) object.

**SDK:** `events.get_state()`.

## `/api/events/get_html_menu`

Render the event menu as an HTML template.

**Method:** GET.

**Response:** HTML menu template; not a JSON profile response.

## `/api/events/get_newrequest_state`

Read the request-creation availability state used by the submission UI.

**Method:** GET.

**Response:** Known JSON fields: `state`. Schema incomplete.

## `/api/events/get_orgs_curators`

Organizers, topic curators and the main organizer.

**Method:** GET.

**Response:** [EventStaff](../api-schemas.md#eventstaff) object.

**SDK:** `events.get_staff()`.

## `/api/events/get_plan`

The schedule tree built in the planner (days -> places -> blocks).

**Method:** GET.

**Response:** Object with `plan`: JSON-encoded string containing array of [PlanNode](../api-schemas.md#plannode) object.

**Notes:** The `plan` value is JSON encoded inside a string. Dates in the decoded tree are Unix milliseconds.

**SDK:** `events.get_plan()`.

## `/api/events/get_settings`

Event settings: title, dates, timezone, design, ...

**Method:** GET.

**Response:** Object with `event`: [Event](../api-schemas.md#event) object.

**SDK:** `events.get_settings()`.

## `/api/events/get_topics_state`

Deadlines of every topic, in the event's local time.

**Method:** GET.

**Response:** Object with `state`: array of [TopicState](../api-schemas.md#topicstate) object.

**SDK:** `events.get_topics_state()`.

## `/api/events/get_topics_statistic`

Request counters per topic.

**Method:** GET.

**Response:** Object with `stats`: array of [TopicStatistic](../api-schemas.md#topicstatistic) object.

**SDK:** `events.get_topics_statistic()`.

## `/api/events/get_types`

Portal event types.

**Method:** GET. **Access:** Portal UI; event-token support was observed for the listing/type reads only.

**Response:** Schema unknown.

**SDK:** `events.get_types()`.

## `/api/events/save_newevents_field`

Save one field of an event submission in the moderation screen.

**Method:** POST. **Access:** Platform administration browser UI.

| Field | In | Type | Description |
|---|---|---|---|
| `new_event_id` | JSON | identifier | Event submission identifier. |
| `field` | JSON | string | Name of the field to edit. |
| `data` | JSON | unknown | New field value; depends on the selected field. |

**Response:** Schema unknown.

## `/api/events/save_newevents_status`

Set an event submission moderation status.

**Method:** POST. **Access:** Platform administration browser UI.

| Field | In | Type | Description |
|---|---|---|---|
| `new_event_id` | JSON | identifier | Event submission identifier. |
| `event_status` | JSON | string | Moderation selector; inspect explicit options in the source. |

**Response:** Schema unknown.

## `/api/events/save_plan`

Replace the whole schedule tree, e.g. with an edited `get_plan`.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `plan` | JSON | string | Complete schedule tree, serialized as JSON. |

**Response:** Success: `{"message":"ok"}`.

**Notes:** Replaces the whole schedule tree; there is no single-node patch. The UI rebuilds request nodes before saving.

**Example:** `{"plan": "[]"}`

**SDK:** `events.save_plan()`.

## `/api/events/save_setting`

Set an event setting attribute.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `event_field` | JSON | string | Event setting name. |
| `data` | JSON | field-dependent JSON value | New field value; depends on the selected field. |

**Response:** Schema unknown.

**SDK:** `events.save_setting()`.

## `/api/events/search`

All Cosplay2 events whose title matches `query`.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `query` | JSON | string | Search text. |

**Response:** Object with `events`: array of [EventBrief](../api-schemas.md#eventbrief) object.

**SDK:** `events.search()`.

## `/api/events/set_gate`

Set a deadline of one topic, or the same deadline of several topics.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `topic_id` | JSON | integer | Single-topic form: topic to update. |
| `datetype` | JSON | [Deadline](../api-schemas.md#deadline) | Single-topic form: deadline to update. |
| `data` | JSON | string | Single-topic form: DD.MM.YY HH:MM in the event timezone. |
| `dates` | JSON | array of objects | Batch alternative to the three top-level fields: each item has topic_id, datetype and data in the same formats. |

**Response:** Schema unknown.

**Example:** `{"topic_id": 42, "datetype": "time_requests_open", "data": "01.11.26 12:00"}`

**SDK:** `events.set_deadline()`.

## `/api/events/winners`

Topics and winning requests of the event.

**Method:** GET.

**Response:** `EventWinners`: `topics` contains `Topic` objects and `winners`
contains `EventWinner` objects. See [response fields](../api-schemas.md#eventwinners).

**SDK:** `events.get_winners()`.
