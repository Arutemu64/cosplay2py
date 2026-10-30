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
- **Auth.** API tokens are issued per event (*РћСЂРіРё в†’ РќР°СЃС‚СЂРѕР№РєР° в†’ API С‚РѕРєРµРЅС‹*). Send them
  as the `X-API-Key` and `X-API-Secret` headers. The secret is shown only once and tokens
  expire after 30 days.
- **Methods.** Reads with no arguments are `GET`. Everything that takes arguments is a
  `POST` with a JSON body, reads included. `/api/topics/get_list` accepts both: `GET`
  for the plain list, `POST` when you pass options.

## Responses

### Ratings response inspection (2026-10-30)

Read-only probes on the configured event host with organizer API credentials:
`ratings_global` returns `topusers` and `countries`; `ratings_country` returns
`topusers`, `areas`, and nullable `regions`; `ratings_area` returns `topusers` and
`regions`; `ratings_region` returns `geo`, `region`, `topusers`, and `cities`;
`ratings_city` returns `geo`, `region`, and `userlist`.
Selectors for area, region, and city were taken from the preceding response.
Group `sum_rating` values are strings, while user `rating` and `users_count` are
integers. User `image_update_time` values are Unix seconds. Rating `geo` coordinates
are numbers; `/api/geo/code_city` returns string coordinates instead. These are
observed payload shapes, not guarantees for other roles or categories. Empty
electronic-ticket responses do not establish their item shapes. No captures or
personal values are retained.

- **JSON served as `text/html`.** Successful responses are JSON with
  `Content-Type: text/html; charset=UTF-8`. Parse the body whatever the header says.
- **The `"message": "ok"` marker.** Many responses put `"message": "ok"` next to the
  payload, e.g. `{"message": "ok", "id": 7}`. Writes often return nothing else.
- **Payloads under a key.** Many endpoints wrap the payload in one top-level key, e.g.
  `{"comments": [...]}`, `{"state": {...}}`. The key is listed in the table below.
- **Errors.** Errors come back with a 4xx/5xx status and, usually, a plain-text message
  in Russian (the frontend shows `data.message` if the body is JSON, otherwise the raw
  text). For example, deleting a folder that still has pages in it returns `400` with
  `РџСЂРµР¶РґРµ С‡РµРј СѓРґР°Р»РёС‚СЊ РіСЂСѓРїРїСѓ, СѓРґР°Р»РёС‚Рµ РёР»Рё РїРµСЂРµРјРµСЃС‚РёС‚Рµ РёР· РЅРµС‘ РІСЃРµ РґРѕС‡РµСЂРЅРёРµ СЌР»РµРјРµРЅС‚С‹.`
- **No pagination** has been seen: list endpoints return everything at once.

## Data formats

The same kind of value comes in different shapes depending on the endpoint:

| What                     | Wire format                                   | Seen in                                       |
|--------------------------|-----------------------------------------------|-----------------------------------------------|
| Server timestamp         | `"YYYY-MM-DD HH:MM:SS"`, in **UTC**           | topics, requests, comments, `users/get_feeds` (`image_update_time`) |
|                          | Unix **seconds**                              | `requests/get_user`, `users/get`, `users/search` (`image_update_time`) |
|                          | Unix **milliseconds**                         | `users/get_events` (`start_time`, `end_time`), `users/get_feeds` (`update_time_utc`, `view_time_utc`) |
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

Observed in public frontend bundles and templates on 2026-10-30. A read-only
comparison on the same date using event API credentials confirmed that all nine
read endpoints work on the configured event host: event types/listing, city
coding, region lookup, and all five rating scopes. The same calls to
`https://cosplay2.ru` with those credentials returned HTTP 403. Use the configured
event base URL; the global portal URL is not required. This observation covers one
event credential pair, not every host or authentication mode. Festival creation and
logo upload were not executed. Response shapes remain `Any` where not yet modeled.

Ratings POST category and scope selectors; region/city ids are URL parameter strings.
Festival creation posts the form verbatim (default create_method `links`, event_type_id
`1`); logo upload uses multipart `mainlogo` and returns `logofilename`. Creation returns
`new_event_id`. City coding unwraps `geodata`. Event types use GET.


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
- **`users/get_feeds` and `users/mark_feeds_readed`.** The top bar calls `users/get_feeds`
  with `onlynew: 1` and `limit: 30`; the profile page omits `onlynew` and passes
  `limit: 20`. Each feed entry has `update_time_utc` and `view_time_utc` (`null` while
  unread) in Unix milliseconds, `image_update_time` as a `"YYYY-MM-DD HH:MM:SS"` UTC
  string, `feed_type` (seen: `"FRIENDS_INVITE_IN"`, `"EVENT_ORG_NEW"`,
  `"EVENT_ORG_ADD"`, `"REQUEST_STATUS"`), an HTML `feed_data` snippet and `href`.
  Opening the notification dropdown sends `users/mark_feeds_readed` (`{"user_id": 42}`),
  which returns the `ok` marker and sets `view_time_utc` on unread items. Treat
  `users/get_feeds` with `onlynew: 1` as a write as well.
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
  invitation), `users/friend_invite_accept` (accept an incoming invitation),
  `users/friend_invite_decline` (decline it), `users/friend_invite_cancel` (withdraw
  your outgoing invitation) and `users/friend_remove`, each with `{"friend_id": 42}`.
  All return just the `ok` marker except `friend_invite_accept`, which returns
  `{"message": "ok", "user": {...}, "friends": []}` in the same shape as `users/get`
  with the newly unlocked friend profile (`friend_status: "friend"`, full name,
  `birthday`, `email`, `mobile`).
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
| `POST` | `/api/events/save_setting` |  | `events.save_setting()` |
| `GET` | `/api/events/get_event_state` | `state` | `events.get_state()` |
| `GET` | `/api/events/get_topics_state` | `state` | `events.get_topics_state()` |
| `GET` | `/api/events/get_topics_statistic` | `stats` | `events.get_topics_statistic()` |
| `GET` | `/api/events/get_orgs_curators` |  | `events.get_staff()` |
| `POST` | `/api/events/add_org` |  | `events.add_org()` |
| `POST` | `/api/events/delete_org` |  | `events.delete_org()` |
| `POST` | `/api/events/change_mainorg` |  | `events.change_main_org()` |
| `POST` | `/api/events/add_curator` |  | `events.add_curator()` |
| `POST` | `/api/events/delete_curator` |  | `events.delete_curator()` |
| `GET` | `/api/events/winners` |  | `events.get_winners()` |
| `GET` | `/api/events/get_plan` | `plan` | `events.get_plan()` |
| `POST` | `/api/events/save_plan` |  | `events.save_plan()` |
| `POST` | `/api/events/get_blank_by_id` |  | `events.get_blank()`, `events.get_reg_topics()`, `events.get_reg_alphabet()` |
| `POST` | `/api/events/search` | `events` | `events.search()` |
| `POST` | `/api/events/filter_list` | `—` | `events.filter_list()` |
| `GET` | `/api/events/get_types` | `—` | `events.get_types()` |
| `POST` | `/api/events/create_festival` | `new_event_id` | `events.create_festival()` |
| `POST` | `/api/events/create_festival_logo` | `logofilename` | `events.create_festival_logo()` |
| `POST` | `/api/events/set_gate` |  | `events.set_deadline()` |
| `GET`/`POST` | `/api/topics/get_list` |  | `topics.get_list()` |
| `POST` | `/api/topics/get_requests` |  | `topics.get_requests()` |
| `POST` | `/api/topics/get_all_requests` |  | `topics.get_all_requests()` |
| `GET` | `/api/topics/get_req_for_planner` |  | `topics.get_requests_for_planner()` |
| `POST` | `/api/topics/get_with_fields` |  | `topics.get_form()` |
| `POST` | `/api/topics/get_with_groups` |  | `topics.get_with_groups()` |
| `POST` | `/api/topics/add_child_topic` | `child_topics` | `topics.add_child_topic()` |
| `POST` | `/api/topics/del_child_topic` | `child_topics` | `topics.delete_child_topic()` |
| `POST` | `/api/topics/add` |  | `topics.create()` |
| `POST` | `/api/topics/topic_delete` |  | `topics.delete()` |
| `POST` | `/api/topics/topic_reorder` |  | `topics.reorder()` |
| `POST` | `/api/topics/fill_from_template` |  | `topics.fill_from_template()` |
| `POST` | `/api/topics/fill_from_topic` |  | `topics.fill_from_topic()` |
| `POST` | `/api/topics/section_add` |  | `topics.add_section()` |
| `POST` | `/api/topics/save_section_field` |  | `topics.save_section()` |
| `POST` | `/api/topics/section_delete` |  | `topics.delete_section()` |
| `POST` | `/api/topics/section_reorder` |  | `topics.reorder_section()` |
| `POST` | `/api/topics/field_add` |  | `topics.add_field()` |
| `POST` | `/api/topics/field_delete` |  | `topics.delete_field()` |
| `POST` | `/api/topics/save_field_field` |  | `topics.save_field()` |
| `POST` | `/api/topics/field_reorder` |  | `topics.reorder_field()` |
| `POST` | `/api/topics/save_topic_field` |  | `topics.save_topic()` |
| `POST` | `/api/topics/generate_cards_title` | `requests` | `topics.generate_card_titles()` |
| `POST` | `/api/topics/reorder_requests` |  | `topics.reorder_requests()` |
| `POST` | `/api/requests/get` |  | `requests.get()` |
| `POST` | `/api/requests/get_comments` | `comments` | `requests.get_comments()` |
| `POST` | `/api/requests/get_orgcomments` | `comments` | `requests.get_org_comments()` |
| `POST` | `/api/requests/add_comment` |  | `requests.add_comment()` |
| `POST` | `/api/requests/del_comment` |  | `requests.delete_comment()` |
| `POST` | `/api/requests/add_orgcomment` |  | `requests.add_org_comment()` |
| `POST` | `/api/requests/del_orgcomment` |  | `requests.delete_org_comment()` |
| `POST` | `/api/requests/save_field` | `id` | `requests.save_field()` |
| `POST` | `/api/requests/get_value_history` | `value_history` | `requests.get_value_history()` |
| `POST` | `/api/requests/upload_image` |  | `requests.upload_image()` |
| `POST` | `/api/requests/delete_image` |  | `requests.delete_image()` |
| `POST` | `/api/requests/upload_file` |  | `requests.upload_file()` |
| `POST` | `/api/requests/delete_file` |  | `requests.delete_file()` |
| `POST` | `/api/requests/get_user` |  | `requests.get_user()` |
| `POST` | `/api/requests/set_status` |  | `requests.set_status()` |
| `POST` | `/api/requests/save_data` |  | `requests.save_data()` |
| `POST` | `/api/requests/create` | `requestId` | `requests.create()` |
| `POST` | `/api/requests/create_reqsection` |  | `requests.create_section()` |
| `POST` | `/api/requests/delete_reqsection` |  | `requests.delete_section()` |
| `POST` | `/api/requests/change_topic` |  | `requests.change_topic()` |
| `POST` | `/api/requests/generate_card_title` | `text` | `requests.generate_card_title()` |
| `POST` | `/api/requests/generate_card_announcement` | `text` | `requests.generate_card_announcement()` |
| `POST` | `/api/requests/generate_card_diplom` | `text` | `requests.generate_card_diplom()` |
| `POST` | `/api/requests/generate_voting_num` | `voting_number` | `requests.generate_voting_number()` |
| `POST` | `/api/requests/search` | `requests` | `requests.search()` |
| `POST` | `/api/requests/feedbacks_get` | `feedbacks` | `requests.get_feedbacks()` |
| `POST` | `/api/requests/feedbacks_add` | `feedbacks` | `requests.add_feedback()` |
| `POST` | `/api/requests/feedbacks_del` | `feedbacks` | `requests.delete_feedback()` |
| `POST` | `/api/users/search` | `users` | `users.search()` |
| `POST` | `/api/geo/code_city` | `geodata` | `geo.code_city()` |
| `POST` | `/api/users/ratings_global` | `—` | `users.ratings_global()` |
| `POST` | `/api/users/ratings_country` | `—` | `users.ratings_country()` |
| `POST` | `/api/users/ratings_area` | `—` | `users.ratings_area()` |
| `POST` | `/api/users/ratings_region` | `—` | `users.ratings_region()` |
| `POST` | `/api/users/ratings_city` | `—` | `users.ratings_city()` |
| `POST` | `/api/users/get_region_geo_id` | `—` | `users.get_region_geo_id()` |
| `GET` | `/api/event_design/get` | `design` | `design.get()` |
| `GET` | `/api/event_design/get_eventimages` | `eventimages` | `design.get_images()` |
| `POST` | `/api/event_design/save_design` |  | `design.save()` |
| `POST` | `/api/event_design/upload_image` | `eventimages` | `design.upload_image()` |
| `POST` | `/api/event_design/delete_eventimage` | `eventimages` | `design.delete_image()` |
| `GET` | `/api/event_design/delete_panel_logo` |  | `design.delete_panel_logo()` |
| `GET` | `/api/event_design/delete_header_logo` |  | `design.delete_header_logo()` |
| `GET` | `/api/event_design/delete_site_background` |  | `design.delete_site_background()` |
| `GET` | `/api/pages/get_list` |  | `pages.get_list()` |
| `POST` | `/api/pages/get_page` |  | `pages.get()` |
| `POST` | `/api/pages/add_page` | `page_id` | `pages.create()` |
| `POST` | `/api/pages/save_page_field` |  | `pages.save_field()` |
| `POST` | `/api/pages/save_page_fields` |  | `pages.save_fields()` |
| `POST` | `/api/pages/delete_page` |  | `pages.delete()` |
| `POST` | `/api/pages/page_reorder` |  | `pages.reorder()` |
| `GET` | `/api/media/get_data` |  | `media.get_data()` |
| `POST` | `/api/media/photoalbum_add` |  | `media.add_album()` |
| `POST` | `/api/media/save_photoalbum_field` |  | `media.save_album_field()` |
| `POST` | `/api/media/photoalbum_delete` |  | `media.delete_album()` |
| `GET` | `/api/cards/get_topics_and_cards` |  | `cards.get_topics_and_cards()` |
| `GET` | `/api/cards/get_card` |  | `cards.get_card()` |
| `GET` | `/api/cards/get_topics_and_requests` |  | `cards.get_topics_and_requests()` |
| `GET` | `/api/cards/get_request` |  | `cards.get_request()` |
| `GET` | `/api/etickets/get_list` | `etickets` | `etickets.get_list()` |
| `GET`/`POST` | `/api/etickets/get_types` | `etickets_types` | `etickets.get_types()` |
| `POST` | `/api/etickets/eticketstypes_add` |  | `etickets.add_type()` |
| `POST` | `/api/etickets/eticketstypes_delete` |  | `etickets.delete_type()` |
| `POST` | `/api/etickets/eticketstypes_reorder` |  | `etickets.reorder_type()` |
| `POST` | `/api/etickets/save_eticketstypes_field` |  | `etickets.save_type_field()` |
| `POST` | `/api/etickets/save_eticket_field` | `eticket` | `etickets.save_field()` |
| `POST` | `/api/etickets/delete` |  | `etickets.delete()` |
| `POST` | `/api/etickets/create_ticket` | `eticket_id` | `etickets.create()` |
| `POST` | `/api/etickets/get_ticket` |  | `etickets.get()` |
| `POST` | `/api/etickets/get_ticket_status` | `eticket_status` | `etickets.get_status()` |
| `POST` | `/api/etickets/save_personal_data` |  | `etickets.save_personal_data()` |
| `GET` | `/api/tickets/get_statistic` |  | `tickets.get_statistic()` |
| `GET` | `/api/tickets/get_voting_statistics` |  | `tickets.get_voting_statistics()` |
| `POST` | `/api/tickets/create` |  | `tickets.create()` |
| `POST` | `/api/tickets/clear_votes` |  | `tickets.clear_votes()` |
| `POST` | `/api/tickets/prize_add` |  | `tickets.add_prize()` |
| `POST` | `/api/tickets/prize_del` |  | `tickets.delete_prize()` |
| `POST` | `/api/tickets/save_prize_field` |  | `tickets.save_prize_field()` |
| `POST` | `/api/tickets/save_prize_handed` |  | `tickets.save_prize_handed()` |
| `GET` | `/api/tickets/get_ticket` |  | `tickets.get_ticket()` |
| `POST` | `/api/tickets/check_for_voting` |  | `tickets.check_for_voting()` |
| `POST` | `/api/tickets/get_voting_data` |  | `tickets.get_voting_data()` |
| `GET` | `/api/tickets/get_cards` | `requests` | `tickets.get_cards()` |
| `POST` | `/api/tickets/select_winner` |  | `tickets.select_winner()` |

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

### Wrapped endpoints with uncaptured or empty payloads in captures

These endpoints are wrapped in cosplay2py using the request shapes in the frontend
templates, and their responses (or inner list fields that came back as `[]` in captures)
are kept as `Any` / `dict[str, Any]` until a populated response is observed:

- `events.get_winners()` (`/api/events/winners`) вЂ” topics and winning requests in
  *РћСЂРіРё в†’ Р—Р°СЏРІРєРё в†’ РџРѕР±РµРґРёС‚РµР»Рё*.
- `topics.get_list(with_group_text=True)` (`Topic.child_topics`),
  `topics.get_with_groups()`, `topics.add_child_topic()`, `topics.delete_child_topic()` вЂ”
  grouped topics.
- `requests.upload_file()` (`/api/requests/upload_file`) and `requests.search()`
  (`/api/requests/search`, key `requests`).
- `cards.*` (`/api/cards/get_topics_and_cards`, `/api/cards/get_card`,
  `/api/cards/get_topics_and_requests`, `/api/cards/get_request`) вЂ” public participant
  showcase and public request list.
- `etickets.get_list()`, `etickets.get_types()`, `etickets.save_field()`, `etickets.get()`,
  `etickets.get_status()` вЂ” electronic ticket tiers and orders (template shows `id`,
  `title`, `type`, `price`, `max_count`, `short_desc`, `full_desc`, `img_href`,
  `time_sell_start`, `time_sell_end` on tiers, where `type` is one of `"for_all"`,
  `"for_members"`, `"for_scene_members"`, `"for_outscene_members"`,
  `"for_disapproved_scene_members"`).
- `tickets.get_statistic()` (`TicketStatistic.test_tickets`),
  `tickets.get_voting_statistics()` (`VotingStatistics.votes_by_source`,
  `topics_activity`, `prizes`, `prizes_winners`), `tickets.add_prize()`,
  `tickets.delete_prize()`, `tickets.get_ticket()`, `tickets.get_voting_data()`,
  `tickets.get_cards()`, `tickets.select_winner()` вЂ” audience voting and voter raffle.

### Out-of-scope account, session, payment and admin endpoints

The frontend bundle also contains unsupported calls for personal account management,
browser session authentication, external payment providers, file download links, and
the platform superadmin panel (`user.role == 100`).

- **Personal account, profile, friends & notifications (`users`):** `get`, `get_events`,
  `save`, `upload_image`, `make_avatar`, `get_friends`, `friend_add`,
  `friend_invite_accept`, `friend_invite_decline`, `friend_invite_cancel`,
  `friend_remove`, `get_feeds`, `mark_feeds_readed`.
- **Browser auth & VK ID (`users`):** `login`, `logincheck`, `logout`, `register`,
  `restore_password`, `restore_password_sms`, `check_code`, `org_auth`, `vk_link`,
  `vk_link_status`, `vk_unlink`, `vk_logout`, `vk_notify_status`,
  `vk_notify_set_enabled`.
- **External payment providers (`etickets`):** `get_paymethods`,
  `save_paymethods_field`, `dictionary-yookassa-vat`, `init-yookassa-payment`,
  `yandex_confirm`, `yookassa-postback-handler`.
- **Browser file downloads & HTML views:** `events/export_plan`, `events/get_blank_xls`,
  `events/get_html_menu`, `topics/download_files`, `etickets/excel`,
  `etickets/printform`, `tickets/get_txt`, `media/recalc_photo`.
- **Superadmin (`admin`, `api_keys`, `blocked_ips`):** `admin/events_list`,
  `admin/calc_size`, `admin/del_files`, `api_keys/list`, `api_keys/generate`,
  `api_keys/deactivate`, `blocked_ips/*`, `users/calc_rating`, `events/get`.
- **Frontend internals & unused legacy endpoints:** `/api/pool/get` (tab polling),
  `/api/events/get_buttons_state_1` (menu bar button states and countdown timers),
  `/api/events/check_external_domain` (DNS check button in settings),
  `/api/events/get_newrequest_state`, `/api/topics/topic_move`,
  `/api/topics/section_move`, `/api/topics/field_move`, `/api/error/handle`.

## How these were found

By watching the event site's own frontend in the browser dev tools (HAR captures),
inspecting the site's unminified AngularJS scripts (`/js/*.js`), view templates
(`/html/*.html`) and inline `globals` in `index.html` for hardcoded enums and constants,
and checking every read-only call against a real event with the live tests in
`tests/live`. They warn about fields the models don't declare yet, which is how API
changes get noticed.

When you find something new, write down what you saw and in which context (role,
event settings), not what you guess the API does in general.
