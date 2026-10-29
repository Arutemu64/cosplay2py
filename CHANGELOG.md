# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses
[Semantic Versioning](https://semver.org/spec/v2.0.0.html): while on `0.x`, a minor bump
means a breaking change.

## [Unreleased]

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

[Unreleased]: https://github.com/Arutemu64/cosplay2py/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Arutemu64/cosplay2py/releases/tag/v0.1.0
