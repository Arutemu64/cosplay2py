# Users API

[API overview](../api-notes.md) · [All endpoints](index.md) · [Schemas](../api-schemas.md)

Account operations use browser sessions. Search and ratings are also wrapped for event API credentials. Profile visibility depends on the viewer. See [authentication](../api-notes.md#authentication) for scope limitations.

JSON request bodies use `application/json` unless an entry specifies another content type.

| Method | Endpoint |
|---|---|
| GET | [`/api/users/calc_rating`](#apiuserscalc_rating) |
| POST | [`/api/users/check_code`](#apiuserscheck_code) |
| POST | [`/api/users/friend_add`](#apiusersfriend_add) |
| POST | [`/api/users/friend_invite_accept`](#apiusersfriend_invite_accept) |
| POST | [`/api/users/friend_invite_cancel`](#apiusersfriend_invite_cancel) |
| POST | [`/api/users/friend_invite_decline`](#apiusersfriend_invite_decline) |
| POST | [`/api/users/friend_remove`](#apiusersfriend_remove) |
| GET / POST | [`/api/users/get`](#apiusersget) |
| GET | [`/api/users/get/{id}`](#apiusersgetid) |
| POST | [`/api/users/get_events`](#apiusersget_events) |
| POST | [`/api/users/get_feeds`](#apiusersget_feeds) |
| GET | [`/api/users/get_friends`](#apiusersget_friends) |
| POST | [`/api/users/get_region_geo_id`](#apiusersget_region_geo_id) |
| POST | [`/api/users/login`](#apiuserslogin) |
| POST | [`/api/users/logincheck`](#apiuserslogincheck) |
| GET / POST | [`/api/users/logout`](#apiuserslogout) |
| POST | [`/api/users/make_avatar`](#apiusersmake_avatar) |
| POST | [`/api/users/mark_feeds_readed`](#apiusersmark_feeds_readed) |
| POST | [`/api/users/org_auth`](#apiusersorg_auth) |
| POST | [`/api/users/ratings_area`](#apiusersratings_area) |
| POST | [`/api/users/ratings_city`](#apiusersratings_city) |
| POST | [`/api/users/ratings_country`](#apiusersratings_country) |
| POST | [`/api/users/ratings_global`](#apiusersratings_global) |
| POST | [`/api/users/ratings_region`](#apiusersratings_region) |
| POST | [`/api/users/register`](#apiusersregister) |
| POST | [`/api/users/restore_password`](#apiusersrestore_password) |
| POST | [`/api/users/restore_password_sms`](#apiusersrestore_password_sms) |
| POST | [`/api/users/save`](#apiuserssave) |
| POST | [`/api/users/search`](#apiuserssearch) |
| POST | [`/api/users/upload_image`](#apiusersupload_image) |
| POST | [`/api/users/vk_link`](#apiusersvk_link) |
| POST | [`/api/users/vk_link_status`](#apiusersvk_link_status) |
| POST | [`/api/users/vk_logout`](#apiusersvk_logout) |
| POST | [`/api/users/vk_notify_set_enabled`](#apiusersvk_notify_set_enabled) |
| POST | [`/api/users/vk_notify_status`](#apiusersvk_notify_status) |
| POST | [`/api/users/vk_unlink`](#apiusersvk_unlink) |

## `/api/users/calc_rating`

Recalculate user ratings from the administration UI.

**Method:** GET. **Access:** Platform administration browser UI.

**Response:** Schema unknown.

**Notes:** Changes rating state despite using GET.

## `/api/users/check_code`

Submit the recovery confirmation code; the frontend reads a password from the response.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `code` | JSON | string | SMS confirmation code. |

**Response:** Known JSON fields: `password`. Schema incomplete.

## `/api/users/friend_add`

Send a friendship invitation.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `friend_id` | JSON | integer | Other user in the friendship action. |

**Response:** Success: `{"message":"ok"}`.

## `/api/users/friend_invite_accept`

Accept an incoming friendship invitation and reveal the friend profile.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `friend_id` | JSON | integer | Other user in the friendship action. |

**Response:** Object with `message: "ok"`, `user` and `friends`, matching the newly accessible friend profile.

## `/api/users/friend_invite_cancel`

Withdraw an outgoing friendship invitation.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `friend_id` | JSON | integer | Other user in the friendship action. |

**Response:** Success: `{"message":"ok"}`.

## `/api/users/friend_invite_decline`

Decline an incoming friendship invitation.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `friend_id` | JSON | integer | Other user in the friendship action. |

**Response:** Success: `{"message":"ok"}`.

## `/api/users/friend_remove`

Remove a friendship.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `friend_id` | JSON | integer | Other user in the friendship action. |

**Response:** Success: `{"message":"ok"}`.

## `/api/users/get`

Read a user profile and its visible friend data; visibility depends on the relationship.

**Method:** GET / POST.

| Field | In | Type | Description |
|---|---|---|---|
| `user_id` | Query | identifier | Profile to retrieve; no request body. |

**Response:** JSON object containing `user` and `friends`; profile fields depend on the relationship. See [profile visibility](workflows.md#profile-visibility).

## `/api/users/get/{id}`

Look up a user by path id in the admin credential-scope selector.

**Method:** GET. **Access:** Platform administration browser UI.

| Field | In | Type | Description |
|---|---|---|---|
| `id` | Path | identifier | User to look up in the admin key selector. |

**Response:** Schema unknown.

## `/api/users/get_events`

List the selected user’s events and event-role/request data.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `userId` | JSON | integer | User identifier. |
| `filter` | JSON | string | Top bar sends "actual"; profile view omits this field. |

**Response:** Known JSON fields: `data`, `events`. Schema incomplete.

## `/api/users/get_feeds`

Read profile notifications; the top-bar variant passes onlynew and a different limit.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `user_id` | JSON | integer | User identifier. |
| `limit` | JSON | integer | UI sends 30 in the top bar, 20 on the profile. |
| `onlynew` | JSON | integer | Top bar sends 1; profile omits it. May change read state. |

**Response:** Known JSON fields: `feeds`. Schema incomplete.

**Notes:** Treat `onlynew: 1` as potentially state-changing. Opening the notification menu also invokes `mark_feeds_readed`.

## `/api/users/get_friends`

Read friend candidates for the user-picker fallback.

**Method:** GET.

**Response:** Known JSON fields: `users`. Schema incomplete.

## `/api/users/get_region_geo_id`

Geographic identifier for a region.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `region` | JSON | string | Region name. |
| `country_code` | JSON | string | Country selector from the preceding ratings response. |

**Response:** Schema unknown.

**SDK:** `users.get_region_geo_id()`.

## `/api/users/login`

Submit a browser login form or start the login request used by the session service.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `name` | Form | string | Email or mobile login. |
| `password` | Form | string | Account password. |
| `rememberme` | Form | string | Browser form serialization of the selected remember-me value. |
| `returnto` | Form | string | URL to return to after login. |

**Request content type:** `application/x-www-form-urlencoded`.

**Response:** Schema unknown.

## `/api/users/logincheck`

Check entered credentials before the browser login form submission.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `name` | JSON | string | Email or mobile login. |
| `password` | JSON | string | Account password. |

**Response:** Known JSON fields: `message`, `user`. Schema incomplete.

## `/api/users/logout`

End the browser session; navigation and HTTP-client variants exist.

**Method:** GET / POST.

| Field | In | Type | Description |
|---|---|---|---|
| `returnto` | Query | string | Navigation variant only; encoded current page URL. |

**Response:** JSON variant: object with `user`, used to reset the current session. Navigation response and redirect behavior are unverified.

## `/api/users/make_avatar`

Regenerate the selected user’s avatar.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `user_id` | JSON | integer | User identifier. |

**Response:** Known JSON fields: `image_update_time`. Schema incomplete.

## `/api/users/mark_feeds_readed`

Mark the selected user’s feeds as read.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `user_id` | JSON | integer | User identifier. |

**Response:** Success: `{"message":"ok"}`.

## `/api/users/org_auth`

Invoke the organizer authentication action on the selected profile.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `user_id` | JSON | integer | User identifier. |

**Response:** Schema unknown.

**Notes:** The action is exposed on a selected user profile; its session effects and authorization requirements remain unverified.

## `/api/users/ratings_area`

Participant ratings for the area scope.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `category` | JSON | [RatingCategory](../api-schemas.md#ratingcategory) | Rating category. Client default: "total". |
| `area_url` | JSON | string | Area selector from the country ratings response. |

**Response:** [AreaRatings](../api-schemas.md#arearatings) object.

**SDK:** `users.ratings_area()`.

## `/api/users/ratings_city`

Participant ratings for the city scope.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `category` | JSON | [RatingCategory](../api-schemas.md#ratingcategory) | Rating category. Client default: "total". |
| `geo_id` | JSON | string | Region or city selector from the preceding ratings response. |

**Response:** [CityRatings](../api-schemas.md#cityratings) object.

**SDK:** `users.ratings_city()`.

## `/api/users/ratings_country`

Participant ratings for the country scope.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `category` | JSON | [RatingCategory](../api-schemas.md#ratingcategory) | Rating category. Client default: "total". |
| `country_code` | JSON | string | Country selector from the preceding ratings response. |

**Response:** [CountryRatings](../api-schemas.md#countryratings) object.

**SDK:** `users.ratings_country()`.

## `/api/users/ratings_global`

Participant ratings for the global scope.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `category` | JSON | [RatingCategory](../api-schemas.md#ratingcategory) | Rating category. Client default: "total". |

**Response:** [GlobalRatings](../api-schemas.md#globalratings) object.

**SDK:** `users.ratings_global()`.

## `/api/users/ratings_region`

Participant ratings for the region scope.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `category` | JSON | [RatingCategory](../api-schemas.md#ratingcategory) | Rating category. Client default: "total". |
| `geo_id` | JSON | string | Region or city selector from the preceding ratings response. |

**Response:** [RegionRatings](../api-schemas.md#regionratings) object.

**Example:** `{"category": "total", "geo_id": "42"}`

**SDK:** `users.ratings_region()`.

## `/api/users/register`

Register an account using the bound registration form, then submit the login form.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `displayName` | JSON | string | Public nickname. |
| `sex` | JSON | string | Radio options: male, female. |
| `password` | JSON | string | Account password. |
| `secondName` | JSON | string | Family name. |
| `firstName` | JSON | string | Given name. |
| `thirdName` | JSON | string | Patronymic. |
| `email` | JSON | string | Email address. |
| `mobile` | JSON | string | Mobile number. |
| `birth` | JSON | string | Birth date as entered in the form. |
| `city` | JSON | string | City; initialized to null. |
| `vk` | JSON | string | VK profile. |

**Response:** Known JSON fields: `message`. Schema incomplete.

## `/api/users/restore_password`

Request password recovery through email.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `email` | JSON | string | Recovery email. |

**Response:** Schema unknown.

## `/api/users/restore_password_sms`

Request password recovery through SMS.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `mobile` | JSON | string | Recovery mobile number. |

**Response:** Schema unknown.

## `/api/users/save`

Save one editable profile field.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `userId` | JSON | integer | User identifier. |
| `field` | JSON | string | first_name, second_name, third_name, sex, birthday, city, email, mobile or vk. |
| `data` | JSON | string | sex: male/female; birthday: DD.MM.YYYY. Other values are strings. |

**Response:** Success: `{"message":"ok"}`.

## `/api/users/search`

Users whose nickname contains `query`, as in the site's user picker.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `query` | JSON | string | Search text. |

**Response:** Object with `users`: array of [UserSearchResult](../api-schemas.md#usersearchresult) object.

**Notes:** Observed matches were case-insensitive nickname substrings. A two-letter query returned no matches where three letters did.

**Example:** `{"query": "example"}`

**Response example:** `{"users": []}`

**SDK:** `users.search()`.

## `/api/users/upload_image`

Upload a profile image and refresh the avatar timestamp.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `user_id` | Multipart | identifier | User identifier. |
| `uploaded_image` | Multipart | file | Profile image. |

**Request content type:** `multipart/form-data`.

**Response:** Known JSON fields: `image_update_time`. Schema incomplete.

## `/api/users/vk_link`

Link VK ID using the profile controller’s authorization data.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `code` | JSON | string | VK authorization code. |
| `state` | JSON | string | Authorization state. |

**Response:** Known JSON fields: `error`, `message`, `success`. Schema incomplete.

## `/api/users/vk_link_status`

Read VK account linking state.

**Method:** POST.

**Response:** Known JSON fields: `linked`, `success`, `vk_id`. Schema incomplete.

## `/api/users/vk_logout`

Invoke the VK logout action from the profile.

**Method:** POST.

**Response:** Known JSON fields: `error`, `message`, `success`. Schema incomplete.

## `/api/users/vk_notify_set_enabled`

Enable or disable VK notifications using an integer flag.

**Method:** POST.

| Field | In | Type | Description |
|---|---|---|---|
| `enabled` | JSON | integer | 1 enables notifications; 0 disables them. |

**Response:** Known JSON fields: `enabled`, `error`, `linked`, `message`, `messages_allowed`, `success`. Schema incomplete.

## `/api/users/vk_notify_status`

Read VK notification subscription state.

**Method:** POST.

**Response:** Known JSON fields: `allow_url`, `enabled`, `group_url`, `linked`, `message`, `messages_allowed`, `success`. Schema incomplete.

## `/api/users/vk_unlink`

Unlink VK ID from the account.

**Method:** POST.

**Response:** Known JSON fields: `error`, `message`, `success`. Schema incomplete.

