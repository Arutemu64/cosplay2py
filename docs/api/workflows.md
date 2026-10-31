# API workflows

[API overview](../api-notes.md) · [Endpoint index](index.md)

## Create a request

1. Read the topic form with `topics/get_with_fields`, sending its `topic_url_code`.
2. POST `requests/create` with the numeric `topic_id`. Read `requestId` from the response.
3. Call `requests/create_reqsection` once per form section, using the new request id
   and the topic section id. Repeated sections use separate instances.
4. Save values with `requests/save_field`, using the returned request section instance
   id and the form's `topic_field_id`. Uploads use the separate flow below.
5. Read the assembled request with `requests/get`.

New requests have been returned with status `"new"`. See [request contracts](requests.md).

## Upload a request image or file

Use `requests/upload_image` for an image field and `requests/upload_file` for a file
field. Both send `request_id`, `request_section_id`, `topic_field_id` and `value_id`
as multipart text fields. Use `value_id` 0 for an empty field. File parts are named
`uploaded_image` and `uploaded_file`, respectively.

```sh
curl "$COSPLAY2_BASE_URL/api/requests/upload_image" \
  -H "X-API-Key: $COSPLAY2_API_KEY" \
  -H "X-API-Secret: $COSPLAY2_API_SECRET" \
  -F 'request_id=5001' \
  -F 'request_section_id=12' \
  -F 'topic_field_id=7' \
  -F 'value_id=0' \
  -F 'uploaded_image=@example.png'
```

The image response contains `id` and `value`; replace the empty value id with the
returned id. The image value includes `filename`, `original` dimensions and resized
variants such as `large` and `medium`. In subsequent request reads, this object has
been stored as JSON inside a string. 

Deletion uses JSON with the same four ids, not multipart. Observed image deletion
stringifies `request_section_id` and `value_id`. For ordinary form fields, send a
string, a numeric picked-user id, or null to clear. A file link is sent through
`save_field` as a JSON-encoded string such as `"{\"link\":\"https://example.invalid/file\"}"`.

## Save a schedule

Read `events/get_plan`, then decode its `plan` string as JSON. Edit the complete
tree and serialize it back into the `plan` field for `events/save_plan`. Node dates
and times use Unix milliseconds. Saving replaces the whole tree.

Refresh request data before saving an old snapshot. Saving may overwrite concurrent
changes; no conflict-control protocol is documented.

## Choose a report

`events/get_blank_by_id` normally returns `html`, `blank_title` and `file_title`.
The registration reports `reg_topics` and `reg_alphabet` instead return `title` and
structured `data`. The UI supplies the report id, inclusion flags, image height and
an optional topic filter. It omits `req_disapproved` and `req_other` unless selected.
For spreadsheet downloads, use the separately documented `events/get_blank_xls` URL.

## Profile visibility

`users/get` accepts the profile id in the query string, including its POST variant:
`/api/users/get?user_id=42`. The response includes `user` and `friends`.

Observed nonfriend profiles omitted full-name fields, birthday, email and mobile;
`friend_status` was `"none"`. Friend profiles included those details and used
`"friend"`. The `friends` collection was populated on the viewer's own profile and
empty for other viewed users. These observations are not a universal access policy.

Friend entries use their own keys, including `friend_id`, `friend_title`,
`friend_city` and `invitetome` (`"0"`/`"1"`). Accepting an invitation returns the newly
accessible profile; the other friendship actions returned the success marker.

## Read notifications

The top bar sends `user_id`, `limit: 30` and `onlynew: 1` to `users/get_feeds`;
the profile sends `limit: 20` and omits `onlynew`. Treat the former as potentially
state-changing. Opening the notification dropdown also calls `users/mark_feeds_readed`.

Feed update and view times use Unix milliseconds; view time is null while unread.
Avatar time uses a UTC timestamp string. `feed_data` contains HTML and `href` is the
destination. Observed feed kinds include `FRIENDS_INVITE_IN`, `EVENT_ORG_NEW`,
`EVENT_ORG_ADD` and `REQUEST_STATUS`; this is not an established closed set.
