# Cosplay2 API notes

Field notes on the undocumented JSON API behind [Cosplay2.ru](https://cosplay2.ru) event
sites, collected while building cosplay2py. They are for anyone talking to the API,
whatever the language.

> [!NOTE]
> This is not an official spec. It describes what the site's own frontend sends and what
> the API has returned so far (observed in 2026 with an organizer's token).
> Responses can depend on your role and the event's settings, and the API changes
> without notice. If something here is wrong or out of date, please open an issue.

The [Pydantic models](../src/cosplay2py/models) are the reference for response fields,
and the [resources](../src/cosplay2py/resources) show the exact request bodies. This
page covers what the code alone doesn't tell you.

## Basics

- **One event per site.** Every event has its own site, `https://<subdomain>.cosplay2.ru`
  or a custom domain, and the API lives under `/api/` on that host. All calls are
  scoped to that event.
- **Auth.** API tokens are issued per event (*Орги → Настройка → API токены*). Send them
  as the `X-API-Key` and `X-API-Secret` headers. The secret is shown only once and tokens
  expire after 30 days.
- **Methods.** Reads with no arguments are `GET`. Everything that takes arguments is a
  `POST` with a JSON body, reads included. `/api/topics/get_list` accepts both: `GET`
  for the plain list, `POST` when you pass options.

## Responses

- **JSON served as `text/html`.** Successful responses are JSON with
  `Content-Type: text/html; charset=UTF-8`. Parse the body whatever the header says.
- **The `"message": "ok"` marker.** Many responses put `"message": "ok"` next to the
  payload, e.g. `{"message": "ok", "id": 7}`. Writes often return nothing else.
- **Payloads under a key.** Many endpoints wrap the payload in one top-level key, e.g.
  `{"comments": [...]}`, `{"state": {...}}`. The key is listed in the table below.
- **Errors.** Errors come back with a 4xx/5xx status and, usually, a plain-text message
  in Russian (the frontend shows `data.message` if the body is JSON, otherwise the raw
  text). For example, deleting a folder that still has pages in it returns `400` with
  `Прежде чем удалить группу, удалите или переместите из неё все дочерние элементы.`
- **No pagination** has been seen: list endpoints return everything at once.

## Data formats

The same kind of value comes in different shapes depending on the endpoint:

| What                     | Wire format                                   | Seen in                                       |
|--------------------------|-----------------------------------------------|-----------------------------------------------|
| Server timestamp         | `"YYYY-MM-DD HH:MM:SS"`, in **UTC**           | topics, requests, comments                    |
|                          | Unix **seconds**                              | `requests/get_user`, `users/get`, `users/search` (`image_update_time`) |
|                          | Unix **milliseconds**                         | `users/get_events` (`start_time`, `end_time`) |
| Display date/time        | `"DD.MM.YY HH:MM"`, in the event's timezone   | `events/get_topics_state`, `get_settings`     |
| Flag                     | `0` / `1` integers                            | most models (`voting_public`, `card_enabled`) |
|                          | real `true` / `false`                         | e.g. `requests/get` (`editEnabled`)           |
| Nested object            | a JSON document packed into a string          | `Event.design`, `events/get_plan`             |
| Empty list               | sometimes `null` instead of `[]`              | `participants` in registration reports        |
| Unset optional enum      | sometimes `""` instead of `null`              | custom `TopicSection`/`TopicField` `internal_name` |

The event's timezone is `timezone` in `events/get_settings`.

Requests go the other way: `events/set_gate` takes deadlines as `"DD.MM.YY HH:MM"` in
the event's timezone, the same format the site displays.

### Request body quirks

- **Stringified ids.** Some endpoints get ids as strings and others as numbers, sometimes
  both in one body: `requests/get_user` sends `{"user_id": "42", "request_id": 5001}`.
  Whether the other form also works hasn't been tested, so cosplay2py sends exactly
  what the site sends.
- **Optional flags are left out**, not sent as `false`. The site only adds
  `req_disapproved` / `req_other` to `events/get_blank_by_id` when their checkbox is
  ticked.
- **`wid`.** The frontend adds a random per-tab id `wid` to every request body. It feeds
  the change-notification pool (below) and isn't needed for the API to work. It
  sometimes ends up saved in data (e.g. inside `Event.design`).
- **`$$hashKey`.** The plan editor saves AngularJS bookkeeping keys along with the plan.
  Ignore them.

## Endpoint behaviour

- **`events/get_blank_by_id`** renders printable reports (`blank_id`) as HTML in
  `{"html", "blank_title", "file_title"}`. The two registration reports, `reg_topics`
  and `reg_alphabet`, return structured data instead (`{"title", "data": [...]}`).
- **`topics/add`** doesn't return the new topic's id. The new topic has the url code
  `"new"` until renamed, so fetch it with `topics/get_with_fields`
  (`{"topic_url_code": "new"}`).
- **Creating a request** is two steps on the site: `requests/create` returns
  `{"requestId": ...}`, then `requests/create_reqsection` is called once per form section.
  Read back with `requests/get` right after these two calls, the request had status
  `"new"`, a value not seen in any other listing.
- **Form field values.** `requests/save_field` sends `data` as the site stores it: a
  string for most fields, the picked user's id as a number for a `user` field (found
  with `users/search`), and `null` when a field is cleared. Images don't go through
  `save_field`: see below.
- **Images** are uploaded with `requests/upload_image`, the only multipart call seen:
  form fields `request_id`, `request_section_id`, `topic_field_id` and `value_id` (`0`
  for an empty field) plus the file as `uploaded_image`. It returns `{"id": "<value
  id>", "value": {"filename": ..., "original": {"width", "height"}, "large": ...,
  "medium": ...}}`, and that `value` object is what the field's `reqvalues` entry then
  holds, as a JSON string. `filename` is a number that matched the upload time in
  Unix seconds. `requests/delete_image` removes it, taking the same ids as JSON with
  `request_section_id` and `value_id` as strings.
- **`requests/get_value_history`** lists the saved versions of one value
  (`{"request_id": 5001, "value_id": "9"}`) under `value_history`: `update_time`, the
  value and who saved it. Here `image_update_time` is a `"YYYY-MM-DD HH:MM:SS"` string,
  not Unix seconds as elsewhere.
- **`users/search`** (`{"query": ...}`) backs the user picker of `user` fields and
  returns `{"users": [...]}` without the `ok` marker. Matches were case-insensitive
  substrings of the nickname; a two-letter query returned no users where three
  letters found several.
- **`requests/change_topic`** does nothing unless the target topic has all the sections
  and fields of the request. Pass `"forceflag": "force"` to move it anyway, dropping
  what doesn't fit.
- **`users/get_feeds` with `onlynew: 1`** may mark notifications as read for the token's
  owner. Treat it as a write.
- **`users/get`** is a `POST` with no body: the site passes the user id in the query
  string, `/api/users/get?user_id=42`. The response holds `user` (the profile) and
  `friends`, whose entries use their own field names (`friend_id`, `friend_title`,
  `friend_city`, `invitetome` as a `"0"`/`"1"` string). What you get depends on who
  you look at: for another user who isn't your friend, `first_name`, `second_name`,
  `third_name`, `birthday`, `email` and `mobile` are left out and `friend_status` is
  `"none"`; for a friend they are included and `friend_status` is `"friend"`.
  `friends` came back empty for other users, friends included, and was only filled
  in on your own profile.
- **Friends.** The profile page's buttons call `users/friend_add` (send an
  invitation), `users/friend_invite_cancel` (withdraw it) and `users/friend_remove`,
  each with `{"friend_id": 42}` and returning just the `ok` marker. Accepting an
  incoming invitation wasn't captured.
- **`users/save`** edits one profile field per call: `{"userId": 42, "field": ...,
  "data": ...}`. From the profile page the site sends `first_name`, `second_name`,
  `third_name`, `sex` (`"male"`/`"female"`), `birthday` (`"DD.MM.YYYY"`), `city`,
  `email`, `mobile` and `vk`, always as strings. The nickname (`title`) wasn't
  editable there.
- **`events/save_plan`** is how the planner saves the schedule: `{"plan": "<JSON
  string>"}` holding the whole tree in the shape `events/get_plan` returns it
  (timestamps in Unix milliseconds), and it returns just the `ok` marker. The site sends
  the full tree on every save, not just the changed node. Before saving, it rebuilds the
  `request` nodes from current data: in one capture a request's `status` and its parent
  nodes' `approved_count`/`other_count` differed from what `get_plan` had returned, and
  every member had a new `uid`.
- **`/api/pool/get`** is polled by the frontend every 10 seconds for live UI updates. It
  isn't useful to API clients and cosplay2py doesn't wrap it.

## Endpoints

The calls cosplay2py wraps. "Key" is the top-level key that holds the payload, if any.

| Method | Path | Key | cosplay2py |
|--------|------|-----|------------|
| `GET` | `/api/events/get_settings` | `event` | `events.get_settings()` |
| `GET` | `/api/events/get_event_state` | `state` | `events.get_state()` |
| `GET` | `/api/events/get_topics_state` | `state` | `events.get_topics_state()` |
| `GET` | `/api/events/get_topics_statistic` | `stats` | `events.get_topics_statistic()` |
| `GET` | `/api/events/get_buttons_state_1` |  | `events.get_buttons_state()` |
| `GET` | `/api/events/get_orgs_curators` |  | `events.get_staff()` |
| `GET` | `/api/events/get_plan` | `plan` | `events.get_plan()` |
| `POST` | `/api/events/save_plan` |  | `events.save_plan()` |
| `POST` | `/api/events/get_blank_by_id` |  | `events.get_blank()`, `events.get_reg_topics()`, `events.get_reg_alphabet()` |
| `POST` | `/api/events/check_external_domain` |  | `events.check_external_domain()` |
| `POST` | `/api/events/search` | `events` | `events.search()` |
| `POST` | `/api/events/set_gate` |  | `events.set_deadline()` |
| `GET`/`POST` | `/api/topics/get_list` |  | `topics.get_list()` |
| `POST` | `/api/topics/get_requests` |  | `topics.get_requests()` |
| `POST` | `/api/topics/get_all_requests` |  | `topics.get_all_requests()` |
| `GET` | `/api/topics/get_req_for_planner` |  | `topics.get_requests_for_planner()` |
| `POST` | `/api/topics/get_with_fields` |  | `topics.get_form()` |
| `POST` | `/api/topics/add` |  | `topics.create()` |
| `POST` | `/api/topics/topic_delete` |  | `topics.delete()` |
| `POST` | `/api/topics/topic_reorder` |  | `topics.reorder()` |
| `POST` | `/api/topics/fill_from_template` |  | `topics.fill_from_template()` |
| `POST` | `/api/topics/fill_from_topic` |  | `topics.fill_from_topic()` |
| `POST` | `/api/topics/section_add` |  | `topics.add_section()` |
| `POST` | `/api/topics/save_section_field` |  | `topics.save_section()` |
| `POST` | `/api/topics/section_delete` |  | `topics.delete_section()` |
| `POST` | `/api/topics/field_add` |  | `topics.add_field()` |
| `POST` | `/api/requests/get` |  | `requests.get()` |
| `POST` | `/api/requests/get_comments` | `comments` | `requests.get_comments()` |
| `POST` | `/api/requests/get_orgcomments` | `comments` | `requests.get_org_comments()` |
| `POST` | `/api/requests/add_comment` |  | `requests.add_comment()` |
| `POST` | `/api/requests/del_comment` |  | `requests.delete_comment()` |
| `POST` | `/api/requests/save_field` | `id` | `requests.save_field()` |
| `POST` | `/api/requests/get_value_history` | `value_history` | `requests.get_value_history()` |
| `POST` | `/api/requests/upload_image` |  | `requests.upload_image()` |
| `POST` | `/api/requests/delete_image` |  | `requests.delete_image()` |
| `POST` | `/api/requests/get_user` |  | `requests.get_user()` |
| `POST` | `/api/requests/set_status` |  | `requests.set_status()` |
| `POST` | `/api/requests/save_data` |  | `requests.save_data()` |
| `POST` | `/api/requests/create` | `requestId` | `requests.create()` |
| `POST` | `/api/requests/create_reqsection` |  | `requests.create_section()` |
| `POST` | `/api/requests/change_topic` |  | `requests.change_topic()` |
| `POST` | `/api/requests/generate_card_title` | `text` | `requests.generate_card_title()` |
| `POST` | `/api/requests/generate_card_announcement` | `text` | `requests.generate_card_announcement()` |
| `POST` | `/api/requests/generate_card_diplom` | `text` | `requests.generate_card_diplom()` |
| `POST` | `/api/users/get` |  | `users.get()` |
| `POST` | `/api/users/save` |  | `users.save_field()` |
| `POST` | `/api/users/friend_add` |  | `users.add_friend()` |
| `POST` | `/api/users/friend_invite_cancel` |  | `users.cancel_friend_invite()` |
| `POST` | `/api/users/friend_remove` |  | `users.remove_friend()` |
| `POST` | `/api/users/get_events` |  | `users.get_events()` |
| `POST` | `/api/users/get_feeds` | `feeds` | `users.get_feeds()` |
| `POST` | `/api/users/search` | `users` | `users.search()` |
| `GET` | `/api/users/get_friends` | `users` | `users.get_friends()` |
| `GET` | `/api/event_design/get` | `design` | `design.get()` |
| `GET` | `/api/event_design/get_eventimages` | `eventimages` | `design.get_images()` |
| `GET` | `/api/pages/get_list` |  | `pages.get_list()` |
| `POST` | `/api/pages/get_page` |  | `pages.get()` |
| `POST` | `/api/pages/add_page` | `page_id` | `pages.create()` |
| `POST` | `/api/pages/save_page_field` |  | `pages.save_field()` |
| `POST` | `/api/pages/save_page_fields` |  | `pages.save_fields()` |
| `POST` | `/api/pages/delete_page` |  | `pages.delete()` |
| `GET` | `/api/media/get_data` |  | `media.get_data()` |
| `GET` | `/api/etickets/get_list` | `etickets` | `etickets.get_list()` |
| `GET` | `/api/etickets/get_types` | `etickets_types` | `etickets.get_types()` |
| `GET` | `/api/etickets/get_paymethods` | `etickets_paymethods` | `etickets.get_paymethods()` |
| `GET` | `/api/etickets/dictionary-yookassa-vat` |  | `etickets.get_vat_dictionary()` |
| `GET` | `/api/tickets/get_statistic` |  | `tickets.get_statistic()` |
| `GET` | `/api/tickets/get_voting_statistics` |  | `tickets.get_voting_statistics()` |

| `POST` | `/api/requests/add_orgcomment` |  | `requests.add_org_comment()` |
| `POST` | `/api/requests/del_orgcomment` |  | `requests.delete_org_comment()` |
| `POST` | `/api/requests/feedbacks_get` | feedbacks | `requests.get_feedbacks()` |
| `POST` | `/api/requests/feedbacks_add` | feedbacks | `requests.add_feedback()` |
| `POST` | `/api/requests/feedbacks_del` | feedbacks | `requests.delete_feedback()` |
| `POST` | `/api/topics/field_delete` |  | `topics.delete_field()` |
| `POST` | `/api/topics/save_field_field` |  | `topics.save_field()` |
| `POST` | `/api/topics/save_topic_field` |  | `topics.save_topic()` |
| `POST` | `/api/topics/section_reorder` |  | `topics.reorder_section()` |
| `POST` | `/api/event_design/save_design` |  | `design.save()` |
| `POST` | `/api/event_design/upload_image` | eventimages | `design.upload_image()` |
| `POST` | `/api/event_design/delete_eventimage` | eventimages | `design.delete_image()` |
| `POST` | `/api/pages/page_reorder` |  | `pages.reorder()` |
| `POST` | `/api/media/photoalbum_add` |  | `media.add_album()` |

## Additional observations (2026-10-29 HAR)

- Organizer feedback writes return the updated `feedbacks` list; marks are sent as
  strings (`"-1"`, `"0"`, `"1"`) and returned as integers. Feedback timestamps use
  server timestamp strings and organizer avatar timestamps use Unix seconds.
- Design saves send partial objects: palette, header settings, and CSS were saved
  separately. Image uploads use multipart field `eventimage`; deletion sends the
  image file name as a string. Both return the updated image mapping.
- Page reordering was captured at the top level with both parent ids null; moving
  between folders was not observed.
- Topic field editing changed `title`; topic editing changed `card_name_rule`.
- `requests/add_comment` also returned `sms_result: null`; its non-null shape is unknown.
- `media/photoalbum_add` returned HTTP 500 when called with an empty body (`{}`), and
  succeeded (`{"message": "ok"}`) with `{"user_title": ..., "url": ...}`.

## Missing captures and untyped payloads

The AngularJS frontend bundle (`/js/*.js`, `/html/*.html`, `index.html`) references
additional fields and endpoints that have not yet been observed with populated server
payloads in HAR captures:

### Wrapped endpoints with empty list payloads in captures

These endpoints are wrapped in cosplay2py, but their list fields came back as `[]` in
all captured responses and are kept as `Any` / `dict[str, Any]` until a populated
response is observed:

- `etickets.get_list()` (`/api/etickets/get_list`, key `etickets`) — sold e-tickets in
  *Орги → Электронные билеты → Управление*.
- `etickets.get_types()` (`/api/etickets/get_types`, key `etickets_types`) — ticket
  tiers in *Орги → Электронные билеты → Типы билетов* (template shows `id`, `title`,
  `type`, `price`, `max_count`, `short_desc`, `full_desc`, `img_href`, `time_sell_start`,
  `time_sell_end`, where `type` is one of `"for_all"`, `"for_members"`,
  `"for_scene_members"`, `"for_outscene_members"`, `"for_disapproved_scene_members"`).
- `tickets.get_statistic()` (`TicketStatistic.test_tickets`) — test voting tickets in
  *Орги → Голосование → Билеты* (template shows `number`).
- `tickets.get_voting_statistics()` (`VotingStatistics.votes_by_source`,
  `topics_activity`, `prizes`, `prizes_winners`) — live voting monitor in
  *Орги → Голосование → Мониторинг*.
- `users.get_feeds()` (`/api/users/get_feeds`, key `feeds`) — notification dropdown
  items (template shows `update_time_utc` in Unix milliseconds, `href`, `feed_data`).
- `topics.get_list(with_group_text=True)` (`Topic.child_topics`) — grouped topics.

### Uncaptured event-scoped endpoints in the frontend

- **Public cards (`cards`):** `/api/cards/get_topics_and_cards`, `/api/cards/get_card`,
  `/api/cards/get_topics_and_requests`, `/api/cards/get_request` (public participant
  showcase and public request list).
- **Event settings & staff (`events`):** `/api/events/save_setting`,
  `/api/events/add_org`, `/api/events/delete_org`, `/api/events/add_curator`,
  `/api/events/delete_curator`, `/api/events/change_mainorg`, `/api/events/winners`,
  `/api/events/get_newrequest_state`, `/api/events/get_html_menu`,
  `/api/events/export_plan`, `/api/events/get_blank_xls`.
- **Topics (`topics`):** `/api/topics/field_reorder`, `/api/topics/field_move`,
  `/api/topics/section_move`, `/api/topics/topic_move`,
  `/api/topics/generate_cards_title`, `/api/topics/reorder_requests`,
  `/api/topics/get_with_groups`, `/api/topics/add_child_topic`,
  `/api/topics/del_child_topic`, `/api/topics/download_files`.
- **Requests (`requests`):** `/api/requests/delete_reqsection`,
  `/api/requests/generate_voting_num`, `/api/requests/search`.
- **Media (`media`):** `/api/media/save_photoalbum_field`,
  `/api/media/photoalbum_delete`, `/api/media/recalc_photo`.
- **Design (`event_design`):** `/api/event_design/delete_header_logo`,
  `/api/event_design/delete_panel_logo`, `/api/event_design/delete_site_background`.
- **E-tickets (`etickets`):** organizer writes (`/api/etickets/eticketstypes_add`,
  `eticketstypes_delete`, `eticketstypes_reorder`, `save_eticketstypes_field`,
  `save_eticket_field`, `save_paymethods_field`, `delete`, `excel`) and buyer flow
  (`create_ticket`, `get_ticket`, `get_ticket_status`, `save_personal_data`,
  `printform`, `init-yookassa-payment`).
- **Audience voting (`tickets`):** organizer writes (`/api/tickets/create`,
  `clear_votes`, `get_txt`, `prize_add`, `prize_del`, `save_prize_field`,
  `save_prize_handed`) and voter flow (`get_ticket`, `check_for_voting`,
  `get_voting_data`, `get_cards`, `select_winner`).
- **User profile (`users`):** `/api/users/friend_invite_accept`,
  `/api/users/friend_invite_decline`, `/api/users/mark_feeds_readed`,
  `/api/users/upload_image`, `/api/users/make_avatar`.

### Out-of-scope portal, session and admin endpoints

The frontend bundle also contains calls for the global `cosplay2.ru` portal, browser
session authentication, and the platform superadmin panel (`user.role == 100`), which
are outside the per-event token API:

- **Browser auth & VK ID (`users`):** `login`, `logincheck`, `logout`, `register`,
  `restore_password`, `restore_password_sms`, `check_code`, `org_auth`, `vk_link`,
  `vk_link_status`, `vk_unlink`, `vk_logout`, `vk_notify_status`,
  `vk_notify_set_enabled`.
- **Global portal & ratings:** `events/create_festival`, `events/create_festival_logo`,
  `events/filter_list`, `events/get_types`, `users/ratings_global`,
  `users/ratings_country`, `users/ratings_area`, `users/ratings_region`,
  `users/ratings_city`, `users/get_region_geo_id`, `geo/code_city`.
- **Superadmin (`admin`, `api_keys`, `blocked_ips`):** `admin/events_list`,
  `admin/calc_size`, `admin/del_files`, `api_keys/list`, `api_keys/generate`,
  `api_keys/deactivate`, `blocked_ips/*`, `users/calc_rating`, `events/get`.
- **Frontend internals:** `/api/pool/get` (tab polling), `/api/error/handle`, and
  payment provider webhooks (`etickets/yandex_confirm`,
  `etickets/yookassa-postback-handler`).

## How these were found

By watching the event site's own frontend in the browser dev tools (HAR captures),
inspecting the site's unminified AngularJS scripts (`/js/*.js`), view templates
(`/html/*.html`) and inline `globals` in `index.html` for hardcoded enums and constants,
and checking every read-only call against a real event with the live tests in
`tests/live`. They warn about fields the models don't declare yet, which is how API
changes get noticed.

When you find something new, write down what you saw and in which context (role,
event settings), not what you guess the API does in general.
