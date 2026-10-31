# Response fields and enum values

[API overview](api-notes.md) · [Endpoint index](api/index.md)

Tables use HTTP keys and wire types. Extra fields may occur; fields can vary by
role and event. ?Observed? means required by the SDK model; ?Optional? means the
model accepts absence. Neither label specifies server validation or defaults.

See [wire formats](api-notes.md#wire-formats) for dates and flags, and
[SDK normalization](api/sdk-normalization.md) for Python aliases and conversions.

## Contents

- [EventRole](#eventrole)
- [EventTime](#eventtime)
- [RequestStatus](#requeststatus)
- [UserBrief](#userbrief)
- [EventDesign](#eventdesign)
- [PlanIntersection](#planintersection)
- [PlanMember](#planmember)
- [PlanNodeType](#plannodetype)
- [PlanNode](#plannode)
- [EventStatus](#eventstatus)
- [FestivalCreateMethod](#festivalcreatemethod)
- [Event](#event)
- [EventState](#eventstate)
- [TopicState](#topicstate)
- [Deadline](#deadline)
- [TopicStatistic](#topicstatistic)
- [Curator](#curator)
- [EventStaff](#eventstaff)
- [EventBrief](#eventbrief)
- [BlankId](#blankid)
- [Blank](#blank)
- [RegistrationRequest](#registrationrequest)
- [RegistrationParticipant](#registrationparticipant)
- [AlphabetParticipant](#alphabetparticipant)
- [TopicParticipants](#topicparticipants)
- [TopicsRegistration](#topicsregistration)
- [AlphabetRegistration](#alphabetregistration)
- [PageType](#pagetype)
- [Page](#page)
- [PageDetails](#pagedetails)
- [MediaAlbum](#mediaalbum)
- [MediaPhoto](#mediaphoto)
- [MediaData](#mediadata)
- [TicketKind](#ticketkind)
- [TicketCreateMode](#ticketcreatemode)
- [VotingType](#votingtype)
- [TicketStatistic](#ticketstatistic)
- [VotingStatistics](#votingstatistics)
- [Request](#request)
- [TopicSection](#topicsection)
- [TopicFieldType](#topicfieldtype)
- [TopicField](#topicfield)
- [TopicForm](#topicform)
- [RequestSection](#requestsection)
- [RequestValue](#requestvalue)
- [FileValue](#filevalue)
- [ImageSize](#imagesize)
- [ImageValue](#imagevalue)
- [UploadedFile](#uploadedfile)
- [UploadedImage](#uploadedimage)
- [ValueChange](#valuechange)
- [NewRequestSection](#newrequestsection)
- [TopicChange](#topicchange)
- [RequestSearchResult](#requestsearchresult)
- [RequestScore](#requestscore)
- [RequestDetails](#requestdetails)
- [Comment](#comment)
- [RequestUser](#requestuser)
- [OtherRequest](#otherrequest)
- [StatusChange](#statuschange)
- [FeedbackMark](#feedbackmark)
- [Feedback](#feedback)
- [RequestUserInfo](#requestuserinfo)
- [CardField](#cardfield)
- [TopicCategory](#topiccategory)
- [PublicRequest](#publicrequest)
- [TopicsAndRequests](#topicsandrequests)
- [PublicRequestDetails](#publicrequestdetails)
- [PublicRequests](#publicrequests)
- [TopicTemplate](#topictemplate)
- [SectionTemplate](#sectiontemplate)
- [FieldTemplate](#fieldtemplate)
- [Topic](#topic)
- [TopicGroup](#topicgroup)
- [TopicGroupLink](#topicgrouplink)
- [TopicRequest](#topicrequest)
- [TopicRequests](#topicrequests)
- [EventRequest](#eventrequest)
- [PlannerRequest](#plannerrequest)
- [PlannerMember](#plannermember)
- [PlannerData](#plannerdata)
- [RatingCategory](#ratingcategory)
- [UserSearchResult](#usersearchresult)
- [RatingUser](#ratinguser)
- [RatingGroup](#ratinggroup)
- [RatingGeo](#ratinggeo)
- [RatingRegion](#ratingregion)
- [GlobalRatings](#globalratings)
- [CountryRatings](#countryratings)
- [AreaRatings](#arearatings)
- [RegionRatings](#regionratings)
- [CityRatings](#cityratings)
- [CityGeodata](#citygeodata)
- [Plan](#plan)

## EventRole

Numeric role / permission level in an event (`globals.ER` on the site).

| Name | Wire value |
|---|---|
| GUEST | `0` |
| USER | `1` |
| REQ_MEMBER | `2` |
| REQ_AUTHOR | `3` |
| CURATOR | `4` |
| ORG | `5` |
| MAINORG | `6` |
| GOD | `100` |

Definition: [models/common.py](../src/cosplay2py/models/common.py).

## EventTime

Whether an event is currently running, upcoming, or over.

| Name | Wire value |
|---|---|
| ACTIVE | `"active"` |
| FUTURE | `"future"` |
| PAST | `"past"` |

Definition: [models/common.py](../src/cosplay2py/models/common.py).

## RequestStatus

Lifecycle status of a request (an application to take part in a topic).

| Name | Wire value |
|---|---|
| NEW | `"new"` |
| PENDING | `"pending"` |
| WAITING | `"waiting"` |
| MATERIALS | `"materials"` |
| REVIEW | `"review"` |
| APPROVED | `"approved"` |
| DISAPPROVED | `"disapproved"` |

Definition: [models/common.py](../src/cosplay2py/models/common.py).

## UserBrief

A short public user profile, as embedded in many responses.

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `user_id` | integer | Observed. |
| `title` | string or null | Optional. The user's nickname. |
| `city` | string or null | Optional. |
| `image_update_time` | timestamp (see wire formats) or null | Optional. When the avatar was last changed; useful as a cache buster. |

Definition: [models/common.py](../src/cosplay2py/models/common.py).

## EventDesign

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `panel_background_color` | string or null | Optional. |
| `panel_text_color` | string or null | Optional. |
| `panel_small_text_color` | string or null | Optional. |
| `panel_buttons_color` | string or null | Optional. |
| `panel_buttons_active_color` | string or null | Optional. |
| `back_background_color` | string or null | Optional. |
| `userpanel_background_color` | string or null | Optional. |
| `userpanel_text_color` | string or null | Optional. |
| `header_height` | string or null | Optional. |
| `header_background_color` | string or null | Optional. |
| `content_background_color` | string or null | Optional. |
| `content_text_color` | string or null | Optional. |
| `content_link_color` | string or null | Optional. |
| `content_opacity` | number or null | Optional. |
| `custom_css` | string or null | Optional. |

Definition: [models/events.py](../src/cosplay2py/models/events.py).

## PlanIntersection

An overlapping performance of the same participant in the schedule.

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `uid` | string or null | Optional. |
| `request_id` | integer | Observed. |
| `title` | string or null | Optional. |
| `status` | [RequestStatus](#requeststatus) or null | Optional. |
| `topic_id` | integer or null | Optional. |
| `card_code` | string or null | Optional. |
| `distance` | integer or null | Optional. Signed time difference in milliseconds between the two performances. |

Definition: [models/events.py](../src/cosplay2py/models/events.py).

## PlanMember

Includes [PlannerMember](#plannermember) fields.

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `uid` | string or null | Optional. |
| `distance` | integer or null | Optional. |
| `intersections` | array of [PlanIntersection](#planintersection) object | Optional. Other plan entries this member overlaps with. |

Definition: [models/events.py](../src/cosplay2py/models/events.py).

## PlanNodeType

Kind of a node in the schedule tree.

| Name | Wire value |
|---|---|
| DAY | `"day"` |
| PLACE | `"place"` |
| TOPIC | `"topic"` |
| REQUEST | `"request"` |
| EVENT | `"event"` |
| BREAK | `"break"` |

Definition: [models/events.py](../src/cosplay2py/models/events.py).

## PlanNode

A node of the schedule tree: day -> place -> event (performance block).

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `type` | [PlanNodeType](#plannodetype) | Observed. |
| `title` | string or null | Optional. |
| `uid` | string or null | Optional. |
| `nodes` | array of [PlanNode](#plannode) object | Optional. |
| `date_start` | integer (Unix milliseconds) or null | Optional. |
| `time_start` | integer (Unix milliseconds) or null | Optional. |
| `time_end` | integer (Unix milliseconds) or null | Optional. |
| `request_length` | number or null | Optional. Duration in minutes. |
| `sum_count` | integer or null | Optional. |
| `sum_length` | number or null | Optional. |
| `approved_count` | integer or null | Optional. |
| `approved_length` | number or null | Optional. |
| `other_count` | integer or null | Optional. |
| `other_length` | number or null | Optional. |
| `topic_id` | integer or null | Optional. |
| `distance` | integer or null | Optional. |
| `collapsed` | flag (boolean or 0/1; see wire formats) or null | Optional. |
| `total_requests_count` | integer or null | Optional. |
| `request_id` | integer or null | Optional. |
| `card_code` | string or null | Optional. |
| `status` | [RequestStatus](#requeststatus) or null | Optional. |
| `request_length_text` | string or null | Optional. `request_length` formatted for display, e.g. `"10 мин."`. |
| `members` | array of [PlanMember](#planmember) object | Optional. |

Definition: [models/events.py](../src/cosplay2py/models/events.py).

## EventStatus

Visibility of an event site.

| Name | Wire value |
|---|---|
| PRIVATE | `"private"` |
| PUBLIC | `"public"` |

Definition: [models/events.py](../src/cosplay2py/models/events.py).

## FestivalCreateMethod

Initial site setup mode when submitting a new festival request.

| Name | Wire value |
|---|---|
| LINKS | `"links"` |
| PAGES | `"pages"` |
| COPY | `"copy"` |

Definition: [models/events.py](../src/cosplay2py/models/events.py).

## Event

Event (festival) settings.

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `id` | integer | Observed. |
| `event_type_id` | integer | Observed. |
| `title` | string | Observed. |
| `short_title` | string or null | Optional. |
| `description` | string or null | Optional. |
| `subdomain` | string | Observed. |
| `domain` | string or null | Optional. Custom domain, if the event is served from one. |
| `user_id` | integer | Observed. The main organizer. |
| `city` | string or null | Optional. |
| `geo_id` | integer or null | Optional. |
| `region` | string or null | Optional. |
| `country` | string or null | Optional. |
| `start_time` | local date/time string or null | Optional. |
| `end_time` | local date/time string or null | Optional. |
| `timezone` | string | Observed. |
| `status` | [EventStatus](#eventstatus) | Observed. |
| `event_status` | [EventTime](#eventtime) or null | Optional. |
| `design` | JSON-encoded string containing [EventDesign](#eventdesign) object or null | Optional. |
| `plan` | JSON-encoded string containing array of [PlanNode](#plannode) object or null | Optional. |
| `ad` | integer or null | Optional. |
| `sms_price` | decimal value (number or numeric string) or null | Optional. |
| `prize_step` | integer or null | Optional. |
| `files_url` | string or null | Optional. |

Definition: [models/events.py](../src/cosplay2py/models/events.py).

## EventState

Request counters for the whole event.

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `topics_count` | integer | Observed. |
| `requests_pending` | integer | Observed. |
| `requests_waiting` | integer | Observed. |
| `requests_materials` | integer | Observed. |
| `requests_review` | integer | Observed. |
| `requests_approved` | integer | Observed. |
| `requests_disapproved` | integer | Observed. |
| `tickets_voting` | integer | Observed. |
| `sms_cost` | decimal value (number or numeric string) or null | Optional. |

Definition: [models/events.py](../src/cosplay2py/models/events.py).

## TopicState

Topic deadlines, formatted in the event's timezone.

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `id` | integer | Observed. |
| `title` | string | Observed. |
| `voting_group` | integer | Observed. |
| `voting_public` | flag (boolean or 0/1; see wire formats) | Observed. |
| `voting_jury` | flag (boolean or 0/1; see wire formats) | Observed. |
| `card_enabled` | flag (boolean or 0/1; see wire formats) | Observed. |
| `time_requests_open` | local date/time string or null | Optional. |
| `time_requests_close` | local date/time string or null | Optional. |
| `time_addons_close` | local date/time string or null | Optional. |
| `time_cards_open` | local date/time string or null | Optional. |
| `time_voting_open` | local date/time string or null | Optional. |
| `time_voting_close` | local date/time string or null | Optional. |

Definition: [models/events.py](../src/cosplay2py/models/events.py).

## Deadline

The topic dates ("гейты") that `events.set_deadline()` can change.

| Name | Wire value |
|---|---|
| REQUESTS_OPEN | `"time_requests_open"` |
| REQUESTS_CLOSE | `"time_requests_close"` |
| ADDONS_CLOSE | `"time_addons_close"` |
| CARDS_OPEN | `"time_cards_open"` |
| VOTING_OPEN | `"time_voting_open"` |
| VOTING_CLOSE | `"time_voting_close"` |

Definition: [models/events.py](../src/cosplay2py/models/events.py).

## TopicStatistic

Request counters for one topic.

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `id` | integer | Observed. |
| `title` | string | Observed. |
| `card_code` | string | Observed. |
| `url_code` | string | Observed. |
| `count_pending` | integer | Observed. |
| `count_waiting` | integer | Observed. |
| `count_materials` | integer | Observed. |
| `count_review` | integer | Observed. |
| `count_approved` | integer | Observed. |
| `count_disapproved` | integer | Observed. |

Definition: [models/events.py](../src/cosplay2py/models/events.py).

## Curator

Includes [UserBrief](#userbrief) fields.

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `topic_id` | integer | Observed. |
| `card_code` | string | Observed. |
| `topic_title` | string | Observed. |

Definition: [models/events.py](../src/cosplay2py/models/events.py).

## EventStaff

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `orgs` | array of [UserBrief](#userbrief) object | Observed. |
| `curators` | array of [Curator](#curator) object | Observed. |
| `mainorg` | [UserBrief](#userbrief) object | Observed. |

Definition: [models/events.py](../src/cosplay2py/models/events.py).

## EventBrief

An event as found by `events.search`.

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `id` | integer | Observed. |
| `title` | string | Observed. |

Definition: [models/events.py](../src/cosplay2py/models/events.py).

## BlankId

Printable reports ("бланки") available to organizers.

| Name | Wire value |
|---|---|
| WINNERS | `"winners"` |
| REG_TOPICS | `"reg_topics"` |
| REG_ALPHABET | `"reg_alphabet"` |
| GEO | `"geo"` |
| TECH_HELPERS | `"tech_helpers"` |
| FOR_PROGRAMM | `"for_programm"` |
| ANNOUNCEMENT | `"announcement"` |
| JURY | `"jury"` |
| BADGES | `"badges"` |
| FOR_SIGNING_PRIZES | `"for_signing_prizes"` |

Definition: [models/events.py](../src/cosplay2py/models/events.py).

## Blank

A rendered printable report.

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `html` | string | Observed. |
| `blank_title` | string | Observed. |
| `file_title` | string | Observed. |

Definition: [models/events.py](../src/cosplay2py/models/events.py).

## RegistrationRequest

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `request_id` | integer | Observed. |
| `number` | integer | Observed. The request's number within its topic. |

Definition: [models/events.py](../src/cosplay2py/models/events.py).

## RegistrationParticipant

A row of a registration table: one person and their requests.

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `user_id` | integer | Observed. |
| `display_name` | string | Observed. |
| `fio` | string | Observed. Full name, as entered by the participant (`"-"` when left out). |
| `city` | string or null | Optional. |
| `phone` | string or null | Optional. |
| `requests` | array of [RegistrationRequest](#registrationrequest) object | Optional. |

Definition: [models/events.py](../src/cosplay2py/models/events.py).

## AlphabetParticipant

Includes [RegistrationParticipant](#registrationparticipant) fields.

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `onscene_count` | integer | Observed. |
| `offscene_count` | integer | Observed. |

Definition: [models/events.py](../src/cosplay2py/models/events.py).

## TopicParticipants

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `topic_id` | integer | Observed. |
| `topic_name` | string | Observed. |
| `participants` | array of [RegistrationParticipant](#registrationparticipant) object or null | Optional. |

Definition: [models/events.py](../src/cosplay2py/models/events.py).

## TopicsRegistration

The `reg_topics` report: participants grouped by topic.

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `title` | string | Observed. |
| `data` | array of [TopicParticipants](#topicparticipants) object | Observed. |

Definition: [models/events.py](../src/cosplay2py/models/events.py).

## AlphabetRegistration

The `reg_alphabet` report: every participant once, in alphabetical order.

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `title` | string | Observed. |
| `data` | array of [AlphabetParticipant](#alphabetparticipant) object | Observed. |

Definition: [models/events.py](../src/cosplay2py/models/events.py).

## PageType

Kind of an entry in the event site's page tree.

| Name | Wire value |
|---|---|
| PAGE | `"page"` |
| FOLDER | `"folder"` |
| LINK | `"link"` |

Definition: [models/misc.py](../src/cosplay2py/models/misc.py).

## Page

A text page of the event site.

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `id` | integer | Observed. |
| `parent_id` | integer or null | Optional. The folder the page sits in, or `None` at the top level. |
| `path` | string | Observed. URL slug of the page; the target URL for a `link`. |
| `type` | [PageType](#pagetype) | Observed. |
| `title` | string | Observed. |
| `menu_title` | string or null | Optional. |
| `show_in_menu` | flag (boolean or 0/1; see wire formats) | Observed. |
| `right` | [EventRole](#eventrole) | Observed. Minimum role required to view the page. |

Definition: [models/misc.py](../src/cosplay2py/models/misc.py).

## PageDetails

A page with its content, as returned by `pages.get`.

Includes [Page](#page) fields.

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `event_id` | integer or null | Optional. |
| `order` | integer or null | Optional. Position among the pages of the same folder. |
| `source` | string or null | Optional. HTML as written in the page editor. |
| `content` | string or null | Optional. HTML shown on the site. |

Definition: [models/misc.py](../src/cosplay2py/models/misc.py).

## MediaAlbum

A photo album linked to the event.

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `id` | integer | Observed. |
| `event_id` | integer or null | Optional. |
| `user_id` | integer or null | Optional. |
| `user_title` | string or null | Optional. Photographer's name. |
| `url` | string or null | Optional. |
| `time_add` | timestamp (see wire formats) or null | Optional. |
| `count` | integer or null | Optional. |
| `likes` | integer or null | Optional. |
| `recalc_time` | timestamp (see wire formats) or null | Optional. |
| `recalc_message` | string or null | Optional. |

Definition: [models/misc.py](../src/cosplay2py/models/misc.py).

## MediaPhoto

A photo from a linked album.

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `id` | integer or null | Optional. |
| `photoalbum_id` | integer or null | Optional. |
| `user_title` | string or null | Optional. |
| `likes` | integer or null | Optional. |
| `src` | string or null | Optional. |
| `photo_url` | string or null | Optional. |

Definition: [models/misc.py](../src/cosplay2py/models/misc.py).

## MediaData

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `albums` | array of [MediaAlbum](#mediaalbum) object | Optional. |
| `photos` | array of [MediaPhoto](#mediaphoto) object | Optional. |

Definition: [models/misc.py](../src/cosplay2py/models/misc.py).

## TicketKind

Kind of voting tickets created by `tickets.create`.

| Name | Wire value |
|---|---|
| TEST | `1` |
| WORK | `2` |

Definition: [models/misc.py](../src/cosplay2py/models/misc.py).

## TicketCreateMode

Whether `tickets.create` adds to existing tickets or replaces them.

| Name | Wire value |
|---|---|
| ADD | `"add"` |
| REPLACE | `"replace"` |

Definition: [models/misc.py](../src/cosplay2py/models/misc.py).

## VotingType

Whether a voting call is for live audience voting or test voting.

| Name | Wire value |
|---|---|
| NORMAL | `"normal"` |
| TEST | `"test"` |

Definition: [models/misc.py](../src/cosplay2py/models/misc.py).

## TicketStatistic

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `active_count` | integer | Observed. |
| `test_tickets` | array of unknown | Optional. |

Definition: [models/misc.py](../src/cosplay2py/models/misc.py).

## VotingStatistics

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `votes_accepted` | integer | Observed. |
| `votes_by_source` | array of unknown | Optional. |
| `active_tickets` | integer | Observed. |
| `topics_activity` | array of unknown | Optional. |
| `prizes` | array of unknown | Optional. |
| `prizes_winners` | array of unknown | Optional. |
| `prize_step` | integer or null | Optional. |
| `prize_step_recommend` | integer or null | Optional. |
| `votes_to_next_prize` | integer or null | Optional. |

Definition: [models/misc.py](../src/cosplay2py/models/misc.py).

## Request

A request (application) to take part in a topic.

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `id` | integer | Observed. |
| `event_id` | integer | Observed. |
| `topic_id` | integer | Observed. |
| `user_id` | integer | Observed. |
| `number` | integer | Observed. |
| `status` | [RequestStatus](#requeststatus) | Observed. |
| `creation_time` | timestamp (see wire formats) or null | Optional. |
| `update_time` | timestamp (see wire formats) or null | Optional. |
| `comment_time` | timestamp (see wire formats) or null | Optional. |
| `voting_number` | integer or null | Optional. |
| `voting_title` | string or null | Optional. |
| `announcement_title` | string or null | Optional. |
| `diplom_title` | string or null | Optional. |
| `program_title` | string or null | Optional. |
| `win` | `1`, `2`, `3` or null | Optional. |
| `win_title` | string or null | Optional. |
| `notes` | string or null | Optional. |
| `score` | integer or null | Optional. |
| `edit_enabled` | flag (boolean or 0/1; see wire formats) or null | Optional. |
| `friendedit_enabled` | flag (boolean or 0/1; see wire formats) or null | Optional. |
| `ER` | [EventRole](#eventrole) or null | Optional. The current user's role relative to this request. |

Definition: [models/requests.py](../src/cosplay2py/models/requests.py).

## TopicSection

A section of a topic's form (e.g. "Performance", "Participant").

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `id` | integer | Observed. |
| `topic_id` | integer | Observed. |
| `title` | string | Observed. |
| `kogo_title` | string or null | Optional. |
| `order` | integer | Observed. |
| `max_repeat` | integer | Observed. How many times the section may repeat (e.g. several participants). |
| `visible_to_all` | flag (boolean or 0/1; see wire formats) | Observed. |
| `registration_blanks` | flag (boolean or 0/1; see wire formats) | Observed. |
| `internal_name` | [SectionTemplate](#sectiontemplate) or null; empty string also observed | Optional. |

Definition: [models/requests.py](../src/cosplay2py/models/requests.py).

## TopicFieldType

Kind of a field in a topic's form.

| Name | Wire value |
|---|---|
| TEXT | `"text"` |
| TEXTAREA | `"textarea"` |
| NUM | `"num"` |
| SELECT | `"select"` |
| CHECKBOX | `"checkbox"` |
| FILE | `"file"` |
| IMAGE | `"image"` |
| LINK | `"link"` |
| PHONE | `"phone"` |
| DURATION | `"duration"` |
| USER | `"user"` |

Definition: [models/requests.py](../src/cosplay2py/models/requests.py).

## TopicField

A field of a topic's form.

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `id` | integer | Observed. |
| `section_id` | integer | Observed. |
| `title` | string | Observed. |
| `type` | [TopicFieldType](#topicfieldtype) | Observed. |
| `order` | integer | Observed. |
| `hint` | string or null | Optional. |
| `data` | string or null | Optional. Field configuration; for `select` fields, a JSON array of options. |
| `visible_to_all` | flag (boolean or 0/1; see wire formats) | Observed. |
| `internal_name` | [FieldTemplate](#fieldtemplate) or null; empty string also observed | Optional. |
| `topic_title` | string or null | Optional. Title of the field's section; only sent by `requests.change_topic`. |

Definition: [models/requests.py](../src/cosplay2py/models/requests.py).

## TopicForm

A topic with its form: the sections and fields a request fills in.

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `topic` | [Topic](#topic) object | Observed. |
| `topic_sections` | array of [TopicSection](#topicsection) object | Observed. |
| `topic_fields` | array of [TopicField](#topicfield) object | Observed. |
| `requests_count` | integer | Observed. |

Definition: [models/requests.py](../src/cosplay2py/models/requests.py).

## RequestSection

An instance of a `TopicSection` filled in a specific request.

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `id` | integer | Observed. |
| `request_id` | integer | Observed. |
| `topic_section_id` | integer | Observed. |
| `order` | integer | Observed. |

Definition: [models/requests.py](../src/cosplay2py/models/requests.py).

## RequestValue

A value of a `TopicField` within a `RequestSection`.

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `id` | integer | Observed. |
| `request_id` | integer | Observed. |
| `request_section_id` | integer | Observed. |
| `topic_field_id` | integer | Observed. |
| `value` | string or null | Optional. |
| `update_time` | timestamp (see wire formats) or null | Optional. |
| `user_id` | integer or null | Optional. |
| `changed` | integer or null | Optional. |

Definition: [models/requests.py](../src/cosplay2py/models/requests.py).

## ImageSize

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `width` | integer | Observed. |
| `height` | integer | Observed. |

Definition: [models/requests.py](../src/cosplay2py/models/requests.py).

## ImageValue

An image uploaded to an `image` field.

`RequestValue.value` of such a field holds this object as a JSON string.

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `filename` | integer | Observed. Name of the stored file; it matched the upload time in Unix seconds. |
| `original` | [ImageSize](#imagesize) object or null | Optional. |
| `large` | [ImageSize](#imagesize) object or null | Optional. |
| `medium` | [ImageSize](#imagesize) object or null | Optional. |

Definition: [models/requests.py](../src/cosplay2py/models/requests.py).

## FileValue

A file uploaded to a `file` field. Stored as a JSON string in `RequestValue.value`.

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `filename` | string | Observed. Stored file name. |
| `filesize` | integer | Observed. File size in bytes. |
| `fileext` | string | Observed. File extension; no closed domain established. |

Definition: [models/requests.py](../src/cosplay2py/models/requests.py).

## UploadedFile

A file just stored in a request's form field.

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `id` | numeric string | Observed. `RequestValue.id`; normalized to an integer. |
| `value` | [FileValue](#filevalue) object | Observed. |

Definition: [models/requests.py](../src/cosplay2py/models/requests.py).

## UploadedImage

An image just stored in a request's form field.

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `id` | numeric string | Observed. `RequestValue.id` of the stored value. |
| `value` | [ImageValue](#imagevalue) object | Observed. |

Definition: [models/requests.py](../src/cosplay2py/models/requests.py).

## ValueChange

A saved version of a request's form value and the user who saved it.

Includes [UserBrief](#userbrief) fields.

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `update_time` | timestamp (see wire formats) | Observed. |
| `value` | string or null | Optional. The value as stored, e.g. an `ImageValue` JSON string for images. |

Definition: [models/requests.py](../src/cosplay2py/models/requests.py).

## NewRequestSection

A section just added to a request, with the values the site prefilled.

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `id` | integer | Observed. `RequestSection.id` of the new section. |
| `values` | array of [RequestValue](#requestvalue) object | Optional. Values filled in from the user's profile (e.g. nickname, contacts). |

Definition: [models/requests.py](../src/cosplay2py/models/requests.py).

## TopicChange

The outcome of moving a request to another topic.

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `message` | `"ok"`, `"target_not_found"` | Optional. `ok` once moved; `target_not_found` when some sections or fields have no     counterpart in the target topic and nothing was changed. |
| `error_sections` | array of [TopicSection](#topicsection) object | Optional. Sections that would be lost by the move. |
| `error_fields` | array of [TopicField](#topicfield) object | Optional. Fields that would be lost by the move. |

Definition: [models/requests.py](../src/cosplay2py/models/requests.py).

## RequestScore

An organizer's rating of a request.

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `user_id` | integer | Observed. |
| `user_title` | string or null | Optional. |
| `score` | integer | Observed. |

Definition: [models/requests.py](../src/cosplay2py/models/requests.py).

## RequestDetails

A request with its topic, form schema and filled-in values.

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `request` | [Request](#request) object | Observed. |
| `author` | [UserBrief](#userbrief) object | Observed. |
| `topic` | [Topic](#topic) object | Observed. |
| `sections` | array of [TopicSection](#topicsection) object | Observed. |
| `fields` | array of [TopicField](#topicfield) object | Observed. |
| `reqsections` | array of [RequestSection](#requestsection) object | Observed. |
| `reqvalues` | array of [RequestValue](#requestvalue) object | Observed. |
| `scores` | array of [RequestScore](#requestscore) object | Optional. |
| `editEnabled` | flag (boolean or 0/1; see wire formats) or null | Optional. |
| `friendeditEnabled` | flag (boolean or 0/1; see wire formats) or null | Optional. |

Definition: [models/requests.py](../src/cosplay2py/models/requests.py).

## Comment

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `id` | integer | Observed. |
| `user_id` | integer | Observed. |
| `user_title` | string or null | Optional. |
| `content` | string | Observed. |
| `creation_time` | timestamp (see wire formats) | Observed. |
| `creationtime` | local date/time string or null | Optional. `creation_time` as shown on the site, in the event's local time. |
| `sms` | flag (boolean or 0/1; see wire formats) or null | Optional. Whether the comment was also sent by SMS. |
| `email` | flag (boolean or 0/1; see wire formats) or null | Optional. Whether the comment was also sent by email. |
| `changed` | integer or null | Optional. |

Definition: [models/requests.py](../src/cosplay2py/models/requests.py).

## RequestUser

Includes [UserBrief](#userbrief) fields.

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `id` | integer | Observed. |
| `age` | integer or null | Optional. |

Definition: [models/requests.py](../src/cosplay2py/models/requests.py).

## OtherRequest

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `request_id` | integer | Observed. |
| `status` | [RequestStatus](#requeststatus) | Observed. |
| `card` | string or null | Optional. |

Definition: [models/requests.py](../src/cosplay2py/models/requests.py).

## StatusChange

The numbers a request holds after its status was changed.

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `request_number` | integer or null | Optional. |
| `voting_number` | integer or null | Optional. |

Definition: [models/requests.py](../src/cosplay2py/models/requests.py).

## FeedbackMark

Rating on organizer feedback about a participant.

| Name | Wire value |
|---|---|
| NEGATIVE | `-1` |
| NEUTRAL | `0` |
| POSITIVE | `1` |

Definition: [models/requests.py](../src/cosplay2py/models/requests.py).

## Feedback

Organizer feedback about a participant.

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `id` | integer or null | Optional. |
| `create_time` | timestamp (see wire formats) or null | Optional. |
| `org_id` | integer or null | Optional. |
| `user_id` | integer or null | Optional. |
| `event_id` | integer or null | Optional. |
| `mark` | [FeedbackMark](#feedbackmark) or null | Optional. |
| `info` | string or null | Optional. |
| `event_title` | string or null | Optional. |
| `event_subdomain` | string or null | Optional. |
| `org_title` | string or null | Optional. |
| `org_city` | string or null | Optional. |
| `org_image_update_time` | timestamp (see wire formats) or null | Optional. |

Definition: [models/requests.py](../src/cosplay2py/models/requests.py).

## RequestUserInfo

A request participant plus their other requests in this event.

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `user` | [RequestUser](#requestuser) object | Observed. |
| `another_requests` | array of [OtherRequest](#otherrequest) object | Optional. |
| `feedbacks` | array of [Feedback](#feedback) object | Optional. |

Definition: [models/requests.py](../src/cosplay2py/models/requests.py).

## CardField

Which generated card field to rebuild with `topics.generate_card_titles`.

| Name | Wire value |
|---|---|
| VOTING_TITLE | `1` |
| ANNOUNCEMENT_TITLE | `2` |
| DIPLOM_TITLE | `3` |

Definition: [models/topics.py](../src/cosplay2py/models/topics.py).

## TopicCategory

Category of a topic (`globals.topicCategories` on the site).

| Name | Wire value |
|---|---|
| SCENE | `"scene"` |
| DEFILE | `"defile"` |
| KARAOKE | `"karaoke"` |
| DANCE | `"dance"` |
| ART | `"art"` |
| PHOTO | `"photo"` |
| VIDEO | `"video"` |
| AMV | `"amv"` |
| GAME | `"game"` |
| VNEKONKURS | `"vnekonkurs"` |
| OTHER | `"other"` |
| NORATING | `"norating"` |

Definition: [models/topics.py](../src/cosplay2py/models/topics.py).

## PublicRequests

Whether a topic's request list is publicly visible.

| Name | Wire value |
|---|---|
| NO | `"NO"` |
| WITHOUT_STATUS | `"WITHOUTSTATUS"` |
| WITH_STATUS | `"WITHSTATUS"` |

Definition: [models/topics.py](../src/cosplay2py/models/topics.py).

## TopicTemplate

Predefined topic form templates used by `topics.fill_from_template`.

| Name | Wire value |
|---|---|
| STAGE | `"stage"` |
| DEFILE_SOLO | `"defile_solo"` |
| DEFILE_GROUP | `"defile_group"` |
| KARAOKE | `"karaoke"` |
| DANCE | `"dance"` |
| ART | `"art"` |
| PHOTOCOSPLAY | `"photocosplay"` |
| VIDEO | `"video"` |
| AMV | `"amv"` |
| VNEKONKURS | `"vnekonkurs"` |
| SMI | `"smi"` |
| VOLUNTEERS | `"volunteers"` |
| FAIR | `"fair"` |

Definition: [models/topics.py](../src/cosplay2py/models/topics.py).

## SectionTemplate

Predefined section templates (`TopicSection.internal_name`).

| Name | Wire value |
|---|---|
| COMMON | `"common"` |
| COMMON_SIMPLE | `"common_simple"` |
| COMMON_VIDEO | `"common_video"` |
| IMAGE_MAIN | `"image_main"` |
| AUTHOR | `"author"` |
| AUTHOR_COSPLAY | `"author_cosplay"` |
| AUTHOR_IMAGE | `"author_image"` |
| MEMBERS | `"members"` |
| MEMBERS_COSPLAY | `"members_cosplay"` |
| MEMBERS_ROLE | `"members_role"` |
| HELPERS | `"helpers"` |
| LINKS | `"links"` |
| IMAGE_GALLERY | `"image_gallery"` |
| FILES | `"files"` |

Definition: [models/topics.py](../src/cosplay2py/models/topics.py).

## FieldTemplate

Predefined field templates (`TopicField.internal_name`).

| Name | Wire value |
|---|---|
| FIO | `"fio"` |
| SECOND_NAME | `"second_name"` |
| FIRST_NAME | `"first_name"` |
| THIRD_NAME | `"third_name"` |
| NAME | `"name"` |
| CITY | `"city"` |
| DURATION | `"duration"` |
| TITLE | `"title"` |
| TEAM | `"team"` |
| ABOUT | `"about"` |
| WISHES | `"wishes"` |
| ABOUT_TEXT | `"about_text"` |
| ABOUT_FAIR | `"about_fair"` |
| IMAGE | `"image"` |
| IMAGE_MAIN | `"image_main"` |
| IMAGE_SELF | `"image_self"` |
| CHARACTER | `"character"` |
| FANDOM | `"fandom"` |
| ROLE | `"role"` |
| USER | `"user"` |
| PHONE | `"phone"` |
| VK | `"vk"` |
| LINK | `"link"` |
| VIDEO_LINK | `"video_link"` |
| UPLOADED_FILE | `"uploaded_file"` |

Definition: [models/topics.py](../src/cosplay2py/models/topics.py).

## Topic

A nomination/category requests are submitted to (e.g. "Solo cosplay").

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `id` | integer | Observed. |
| `event_id` | integer | Observed. |
| `url_code` | string | Observed. |
| `card_code` | string | Observed. |
| `title` | string | Observed. |
| `category` | [TopicCategory](#topiccategory) or null; empty string also observed | Optional. |
| `description` | string or null | Optional. |
| `intro` | string or null | Optional. |
| `order` | integer | Observed. |
| `voting_group` | integer | Observed. |
| `voting_public` | flag (boolean or 0/1; see wire formats) | Observed. |
| `voting_jury` | flag (boolean or 0/1; see wire formats) | Observed. |
| `print_badges` | flag (boolean or 0/1; see wire formats) | Observed. |
| `card_enabled` | flag (boolean or 0/1; see wire formats) | Observed. |
| `default_duration` | number | Observed. |
| `public_requests` | [PublicRequests](#publicrequests) | Observed. |
| `time_requests_open` | timestamp (see wire formats) or null | Optional. |
| `time_requests_close` | timestamp (see wire formats) or null | Optional. |
| `time_addons_close` | timestamp (see wire formats) or null | Optional. |
| `time_cards_open` | timestamp (see wire formats) or null | Optional. |
| `time_voting_open` | timestamp (see wire formats) or null | Optional. |
| `time_voting_close` | timestamp (see wire formats) or null | Optional. |
| `card_name_rule` | string or null | Optional. |
| `card_announcement_rule` | string or null | Optional. |
| `card_diplom_rule` | string or null | Optional. |
| `child_topics` | string or null | Optional grouping display text from `with_group_text=True`. |

Definition: [models/topics.py](../src/cosplay2py/models/topics.py).

## TopicRequest

A request as shown in a topic's request list.

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `id` | integer | Observed. |
| `number` | integer | Observed. |
| `status` | [RequestStatus](#requeststatus) | Observed. |
| `user_id` | integer | Observed. |
| `user_title` | string or null | Optional. |
| `city` | string or null | Optional. |
| `image_update_time` | timestamp (see wire formats) or null | Optional. |
| `voting_number` | integer or null | Optional. |
| `voting_title` | string or null | Optional. |
| `update_time` | string or null | Optional. Display-formatted, without a year (e.g. `"10 Aug 16:05"`). |
| `comment_time` | timestamp (see wire formats) or null | Optional. |
| `notes` | string or null | Optional. |
| `new_comments` | integer or null | Optional. |
| `new_updates` | integer or null | Optional. |
| `win` | `1`, `2`, `3` or null | Optional. |
| `win_title` | string or null | Optional. |
| `score` | integer or null | Optional. |

Definition: [models/topics.py](../src/cosplay2py/models/topics.py).

## TopicRequests

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `topic` | [Topic](#topic) object | Observed. |
| `requests` | array of [TopicRequest](#topicrequest) object | Observed. |

Definition: [models/topics.py](../src/cosplay2py/models/topics.py).

## EventRequest

A request as shown in the event-wide request list.

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `id` | integer | Observed. |
| `topic_id` | integer | Observed. |
| `number` | integer | Observed. |
| `status` | [RequestStatus](#requeststatus) | Observed. |
| `user_id` | integer | Observed. |
| `user_title` | string or null | Optional. |
| `update_time` | local date/time string or null | Optional. |
| `comment_time` | timestamp (see wire formats) or null | Optional. |
| `image_update_time` | timestamp (see wire formats) or null | Optional. |
| `voting_number` | integer or null | Optional. |
| `voting_title` | string or null | Optional. |
| `new_comments` | integer or null | Optional. |
| `new_updates` | integer or null | Optional. |

Definition: [models/topics.py](../src/cosplay2py/models/topics.py).

## PlannerRequest

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `id` | integer | Observed. |
| `topic_id` | integer | Observed. |
| `number` | integer | Observed. |
| `status` | [RequestStatus](#requeststatus) | Observed. |
| `user_id` | integer | Observed. |
| `user_title` | string or null | Optional. |
| `image_update_time` | timestamp (see wire formats) or null | Optional. |
| `voting_number` | integer or null | Optional. |
| `voting_title` | string or null | Optional. |
| `duration` | number or null | Optional. Performance duration in minutes. |
| `score` | integer or null | Optional. |

Definition: [models/topics.py](../src/cosplay2py/models/topics.py).

## PlannerMember

A participant of a request (a request may have several members).

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `request_id` | integer | Observed. |
| `user_id` | integer or null | Optional. |
| `title` | string or null | Optional. |
| `fio` | string or null | Optional. Full legal name. |
| `city` | string or null | Optional. |

Definition: [models/topics.py](../src/cosplay2py/models/topics.py).

## PlannerData

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `requests` | array of [PlannerRequest](#plannerrequest) object | Observed. |
| `members` | array of [PlannerMember](#plannermember) object | Observed. |

Definition: [models/topics.py](../src/cosplay2py/models/topics.py).

## RatingCategory

Participant rating category (`globals.ratingCategories` on the site).

| Name | Wire value |
|---|---|
| TOTAL | `"total"` |
| SCENE | `"scene"` |
| DEFILE | `"defile"` |
| KARAOKE | `"karaoke"` |
| DANCE | `"dance"` |
| ART | `"art"` |
| PHOTO | `"photo"` |
| VIDEO | `"video"` |
| AMV | `"amv"` |
| GAME | `"game"` |
| VNEKONKURS | `"vnekonkurs"` |
| SMI | `"smi"` |
| FAIR | `"fair"` |
| VOLUNTEERS | `"volunteers"` |
| ORGS | `"orgs"` |

Definition: [models/users.py](../src/cosplay2py/models/users.py).

## UserSearchResult

Includes [UserBrief](#userbrief) fields.

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `id` | integer or null | Optional. Same as `user_id`. |
| `friends_boost` | integer or null | Optional. `0` in every result seen so far. |

Definition: [models/users.py](../src/cosplay2py/models/users.py).

## RatingUser

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `id` | integer or null | Optional. |
| `title` | string or null | Optional. |
| `city` | string or null | Optional. |
| `image_update_time` | timestamp (see wire formats) or null | Optional. |
| `rating` | integer or null | Optional. |
| `rating_code` | string or null | Optional. |

Definition: [models/users.py](../src/cosplay2py/models/users.py).

## RatingGroup

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `geo_id` | integer or null | Optional. |
| `country` | string or null | Optional. |
| `country_code` | string or null | Optional. |
| `area_short` | string or null | Optional. |
| `area_url` | string or null | Optional. |
| `region` | string or null | Optional. |
| `city` | string or null | Optional. |
| `sum_rating` | string or null | Optional. |
| `users_count` | integer or null | Optional. |
| `topusers` | array of [RatingUser](#ratinguser) object or null | Optional. |

Definition: [models/users.py](../src/cosplay2py/models/users.py).

## RatingGeo

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `id` | integer or null | Optional. |
| `country` | string or null | Optional. |
| `country_code` | string or null | Optional. |
| `region` | string or null | Optional. |
| `city` | string or null | Optional. |
| `bounds` | string or null | Optional. |
| `viewport` | string or null | Optional. |
| `location_lat` | number or null | Optional. |
| `location_lng` | number or null | Optional. |

Definition: [models/users.py](../src/cosplay2py/models/users.py).

## RatingRegion

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `region_id` | integer or null | Optional. |
| `region` | string or null | Optional. |
| `area` | string or null | Optional. |
| `area_short` | string or null | Optional. |
| `area_url` | string or null | Optional. |

Definition: [models/users.py](../src/cosplay2py/models/users.py).

## GlobalRatings

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `topusers` | array of [RatingUser](#ratinguser) object or null | Optional. |
| `countries` | array of [RatingGroup](#ratinggroup) object or null | Optional. |

Definition: [models/users.py](../src/cosplay2py/models/users.py).

## CountryRatings

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `topusers` | array of [RatingUser](#ratinguser) object or null | Optional. |
| `areas` | array of [RatingGroup](#ratinggroup) object or null | Optional. |
| `regions` | array of [RatingGroup](#ratinggroup) object or null | Optional. |

Definition: [models/users.py](../src/cosplay2py/models/users.py).

## AreaRatings

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `topusers` | array of [RatingUser](#ratinguser) object or null | Optional. |
| `regions` | array of [RatingGroup](#ratinggroup) object or null | Optional. |

Definition: [models/users.py](../src/cosplay2py/models/users.py).

## RegionRatings

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `geo` | [RatingGeo](#ratinggeo) object or null | Optional. |
| `region` | [RatingRegion](#ratingregion) object or null | Optional. |
| `topusers` | array of [RatingUser](#ratinguser) object or null | Optional. |
| `cities` | array of [RatingGroup](#ratinggroup) object or null | Optional. |

Definition: [models/users.py](../src/cosplay2py/models/users.py).

## CityRatings

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `geo` | [RatingGeo](#ratinggeo) object or null | Optional. |
| `region` | [RatingRegion](#ratingregion) object or null | Optional. |
| `userlist` | array of [RatingUser](#ratinguser) object or null | Optional. |

Definition: [models/users.py](../src/cosplay2py/models/users.py).

## CityGeodata

| HTTP field | Wire type | Presence / description |
|---|---|---|
| `country_code` | string or null | Optional. |
| `country` | string or null | Optional. |
| `region` | string or null | Optional. |
| `city` | string or null | Optional. |
| `bounds` | string or null | Optional. |
| `viewport` | string or null | Optional. |
| `location_lng` | string or null | Optional. |
| `location_lat` | string or null | Optional. |

Definition: [models/users.py](../src/cosplay2py/models/users.py).

## Plan

A JSON-encoded string containing an array of [PlanNode](#plannode) objects.
`events/get_plan` returns it under the `plan` key; `events/save_plan` sends the
whole tree in the same field. Schedule dates and times use Unix milliseconds.

## EventWinners

GET `/api/events/winners`.

| Field | Wire type | Meaning |
|---|---|---|
| `topics` | array of Topic | Event topics; uses the existing Topic schema. |
| `winners` | array of EventWinner | Winning requests. |

## EventWinner

| Field | Wire type | Meaning |
|---|---|---|
| `id` | integer | Request identifier. |
| `topic_id` | integer | Topic identifier. |
| `number` | integer | Request number within the topic. |
| `voting_number` | integer | Voting number. |
| `voting_title` | string | Display title. |
| `win` | integer | Award placement. |
| `win_title` | string or null | Optional; all captured values are null. String type follows existing request models. |

## Participant card schemas

Timestamps use UTC.

| Model | Wire fields and types |
|---|---|
| `CardTopic` | `id`: integer; `url_code`, `card_code`, `title`: string |
| `CardRequest` | `id`, `topic_id`: integer; `voting_number`, `win`, `user_id`: nullable integer; `voting_title`: nullable string; `image`: nullable `ImageValue` object |
| `TopicsAndCards` | `topics`: `CardTopic` array; `requests`: `CardRequest` array |
| `CardBadge` | `request_section_id`: integer; `card`: string; `another_requests`: nullable display string |
| `CardUser` | `id`: integer; `title`: nullable string; `image_update_time`: nullable Unix timestamp |
| `CardDetails` | `request`: `Request`; `topic`: `Topic`; `sections`: `TopicSection` array; `fields`: `TopicField` array; `reqsections`: `RequestSection` array; `reqvalues`: `RequestValue` array; `badges`: `CardBadge` array; `users`: `CardUser` array |

`TopicSection.image_section` and `TopicSection.user_section` are optional nullable
booleans, observed as string flags `"0"` and `"1"` in card responses. Optional
card row fields default to null. `reqsections` and `reqvalues` are exposed as
`request_sections` and `values`, respectively.

## TopicGroup

Group editor response.

| Wire field | Wire type | Meaning |
|---|---|---|
| `topic` | [Topic](#topic) object | Group topic. |
| `topics` | array of [Topic](#topic) objects | All event topics. |
| `child_topics` | array of [TopicGroupLink](#topicgrouplink) objects | Linked children; may be empty. |

## TopicGroupLink

Group membership row returned by group read and add/delete child calls;
present in populated responses.

| Wire field | Wire type | Meaning |
|---|---|---|
| `group_topic_id` | integer | Parent group topic identifier. |
| `child_topic_id` | integer | Linked child topic identifier. |


## RequestSearchResult

A search result from POST `/api/requests/search`, key `requests`.
All fields were present and non-null in all 15 observed rows.

| Wire field | Wire type | Meaning |
|---|---|---|
| `id` | integer | Request identifier. |
| `topic_id` | integer | Topic identifier. |
| `number` | integer | Request number. |
| `status` | [RequestStatus](#requeststatus) | Request status. |
| `voting_number` | integer | Voting number. |
| `voting_title` | string | Voting title. |
| `user_title` | string | Author display title. |
| `city` | string | City display text. |
| `card_code` | string | Card code. |


## PublicRequest

Public request list row.

| Wire field | Wire type | Meaning |
|---|---|---|
| `id` | integer | Request identifier. |
| `topic_id` | integer | Topic identifier. |
| `user_id` | integer | Author identifier. |
| `number` | integer | Request number. |
| `status` | [RequestStatus](#requeststatus) | Request status. |
| `public_requests` | [PublicRequests](#publicrequests) | Topic visibility setting. |
| `voting_number` | integer or null | Optional voting number. |
| `voting_title` | string or null | Optional voting title. |

All fields were present in the capture; nullable voting fields default to null.

## TopicsAndRequests

GET `/api/cards/get_topics_and_requests`.

| Wire field | Wire type |
|---|---|
| `topics` | array of `CardTopic` |
| `requests` | array of [PublicRequest](#publicrequest) |

Both arrays are required and may be empty.

## PublicRequestDetails

GET `/api/cards/get_request`.

| Wire field | Wire type |
|---|---|
| `request` | [Request](#request) |
| `topic` | [Topic](#topic) |
| `sections` | array of [TopicSection](#topicsection) |
| `fields` | array of [TopicField](#topicfield) |
| `reqsections` | array of [RequestSection](#requestsection) |
| `reqvalues` | array of [RequestValue](#requestvalue) |
| `users` | array of `CardUser` |

All fields are required. `reqsections` and `reqvalues` are exposed as
`request_sections` and `values`. The `message: "ok"` marker is stripped by
the client. Unlike `CardDetails`, this response has no badge collection.
