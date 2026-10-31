# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses
[Semantic Versioning](https://semver.org/spec/v2.0.0.html): while on `0.x`, a minor bump
means a breaking change.

## [Unreleased]

## [0.4.0] - 2026-11-01

### Fixed

- **Breaking:** Type `Topic.child_topics` as `str | None` using the observed
  grouping display text from `topics.get_list(with_group_text=True)`, replacing
  the unverified `Any` type.

### Added

- Typed request upload response models `UploadedFile` and `FileValue`.

- Typed public request list and detail models: `PublicRequest`,
  `TopicsAndRequests`, and `PublicRequestDetails`.

- Typed request search result model `RequestSearchResult`.

- Typed topic group and child-link response models.

- Typed participant card models and optional topic section image/user flags.

### Changed

- **Breaking:** `requests.upload_file()` returns `UploadedFile` instead of a
  dictionary.

- **Breaking:** `cards.get_topics_and_requests()` and `cards.get_request()`
  return `TopicsAndRequests` and `PublicRequestDetails` models instead of dictionaries.

- **Breaking:** `requests.search()` returns `RequestSearchResult` models instead
  of dictionaries.

- **Breaking:** `topics.get_with_groups()` returns `TopicGroup` instead of a
  dictionary; `topics.add_child_topic()` and `topics.delete_child_topic()`
  return `TopicGroupLink` models instead of dictionaries.

- **Breaking:** `cards.get_topics_and_cards()` and `cards.get_card()` return
  `TopicsAndCards` and `CardDetails` models instead of dictionaries.

- **Breaking:** `events.get_winners()` returns `EventWinners` with typed `Topic`
  and `EventWinner` lists instead of a dictionary.

## [0.3.0] - 2026-10-30

### Added

- Tag-triggered PyPI publishing through GitHub Actions trusted publishing; see
  [publishing setup](docs/publishing.md).

- Global portal event creation, listing, types, geographic lookup and ratings endpoints.

- `cards` resource (`Cards` / `AsyncCards`): `get_topics_and_cards()`, `get_card()`,
  `get_topics_and_requests()`, and `get_request()`.
- Event settings, staff, and winners endpoints on `events`: `save_setting()`,
  `add_org()`, `delete_org()`, `change_main_org()`, `add_curator()`,
  `delete_curator()`, and `get_winners()`.
- Topic form, group, and request management endpoints on `topics`: `reorder_field()`,
  `generate_card_titles()` (with `CardField`), `reorder_requests()`,
  `get_with_groups()`, `add_child_topic()`, and `delete_child_topic()`.
- Request section, file, voting number, and search endpoints on `requests`:
  `delete_section()`, `upload_file()`, `delete_file()`, `generate_voting_number()`,
  and `search()`.
- Photo album management on `media`: `save_album_field()` and `delete_album()`.
- Logo and background removal on `design`: `delete_panel_logo()`,
  `delete_header_logo()`, and `delete_site_background()`.
- Electronic ticket management and buyer endpoints on `etickets`: `get_types(i_can_buy=)`,
  `add_type()`, `delete_type()`, `reorder_type()`, `save_type_field()`, `save_field()`,
  `delete()`, `create()`, `get()`, `get_status()`, and `save_personal_data()`.
- Audience voting and prize endpoints on `tickets`: `create()` (with `TicketKind` and
  `TicketCreateMode`), `clear_votes()`, `add_prize()`, `delete_prize()`,
  `save_prize_field()`, `save_prize_handed()`, `get_ticket()`, `check_for_voting()`,
  `get_voting_data()`, `get_cards()`, and `select_winner()` (with `VotingType`).

### Changed

- **Breaking:** All five `users.ratings_*()` methods now return typed response
  models instead of dictionaries. `geo.code_city()` returns `CityGeodata`.
  Rating timestamps normalize to UTC datetimes.
- Expand package keywords and clarify the package description.

### Removed

- **Breaking:** Removed frontend UI helper endpoints `events.get_buttons_state()`,
  `events.check_external_domain()`, and `etickets.get_vat_dictionary()`, along with
  models `ButtonsState`, `ButtonState`, `ButtonStateCode`, and `DomainCheck`.
- **Breaking:** Removed personal account, profile, friend, and notification endpoints
  from `users` (`get`, `get_events`, `save_field`, `add_friend`, `cancel_friend_invite`,
  `remove_friend`, `get_friends`, and `get_feeds`), along with models `UserDetails`,
  `UserProfile`, `Friendship`, `FriendStatus`, `Sex`, `UserEvents`, `UserEvent`,
  `UserEventRole`, `UserEventRoleType`, and `Friend`.
- **Breaking:** Removed external payment configuration endpoint
  `etickets.get_paymethods()` and model `PayMethods`.

## [0.2.0] - 2026-10-29

### Added

- Domain enums `ButtonStateCode`, `EventRole`, `EventStatus`, `EventTime`,
  `FeedbackMark`, `FieldTemplate`, `FriendStatus`, `PlanNodeType`, `PublicRequests`,
  `SectionTemplate`, `Sex`, `TopicCategory`, `TopicFieldType`, `TopicTemplate`, and
  `UserEventRoleType` exported from `cosplay2py.models`.
- Nested response models `MediaAlbum`, `MediaPhoto`, `PlanIntersection`, and
  `RequestScore` exported from `cosplay2py.models`.
- `media.add_album()` (`POST /api/media/photoalbum_add`).
- Optional fields on `ButtonState` (`timer`), `UserEventRole` (curator and participant
  fields), and `PayMethods` (YooKassa, YooMoney, and manual transfer settings).

### Changed

- **Breaking:** Tightened response models to enforce closed enums and nested models
  (`Event.status`, `Event.event_status`, `ButtonState.state`, `PlanNode.type`,
  `PlanMember.intersections`, `Page.type`, `Page.right`, `MediaData.albums`,
  `MediaData.photos`, `Topic.category`, `Topic.public_requests`,
  `TopicSection.internal_name`, `TopicField.type`, `TopicField.internal_name`,
  `Request.er`, `Request.win`, `Request.score`, `TopicRequest.win`,
  `TopicRequest.score`, `PlannerRequest.score`, `RequestDetails.scores`,
  `TopicChange.message`, `Feedback.mark`, `UserProfile.sex`,
  `UserProfile.friend_status`, `UserEvent.time`, `UserEventRole.er`). Empty strings on
  optional enum fields normalize to `None`.
- **Breaking:** Tightened resource method signatures and runtime validation to require
  enums (`events.get_blank`, `events.set_deadline`, `topics.fill_from_template`,
  `topics.add_section`, `topics.add_field`, `requests.set_status`,
  `requests.add_feedback`, `pages.create`).

### Changed

- **Breaking:** All five `users.ratings_*()` methods now return typed response
  models instead of dictionaries. `geo.code_city()` returns `CityGeodata`.
  Rating timestamps normalize to UTC datetimes.
- Expand package keywords and clarify the package description.

### Removed

- **Breaking:** Removed frontend-injected noise fields `EventDesign.wid` and
  `PlanMember.hash_key` (`$$hashKey`); both keys are now stripped automatically on
  model validation.

## [0.1.0] - 2026-10-29

### Added

- Initial release of typed sync (`Cosplay2`) and async (`AsyncCosplay2`) clients
  for the Cosplay2.ru API, with Pydantic models, safe retries and typed errors.
- Read and write resources for events, topics, requests, users, design, pages,
  media, electronic tickets and tickets.
- API reference notes, usage examples, and offline tests covering both clients
  and asyncio/Trio, with CI for Python 3.12-3.15 and package installation.

[Unreleased]: https://github.com/Arutemu64/cosplay2py/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/Arutemu64/cosplay2py/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/Arutemu64/cosplay2py/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/Arutemu64/cosplay2py/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/Arutemu64/cosplay2py/releases/tag/v0.1.0
