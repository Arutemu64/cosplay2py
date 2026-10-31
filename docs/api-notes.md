# Cosplay2 HTTP API

Unofficial reference for the HTTP API used by [Cosplay2.ru](https://cosplay2.ru/).
Includes browser and provider routes outside cosplay2py; coverage is not exhaustive.

## Start here

- [Endpoint index](api/index.md): find an operation by method or path.
- [Response fields and enums](api-schemas.md): HTTP field names, types and formats.
- [Workflows](api/workflows.md): request creation, uploads, schedules and profiles.
- [SDK normalization](api/sdk-normalization.md): Python aliases and conversions.

| Area | Reference |
|---|---|
| Event configuration, staff, reports and schedules | [Events](api/events.md) |
| Topics and form definitions | [Topics](api/topics.md) |
| Requests, values, comments and feedback | [Requests](api/requests.md) |
| Profiles, friends, notifications, login and ratings | [Users](api/users.md) |
| Event design and uploaded assets | [Design](api/event_design.md) |
| Pages and folders | [Pages](api/pages.md) |
| Photo albums | [Media](api/media.md) |
| Public participant cards | [Cards](api/cards.md) |
| Electronic ticket orders and payment providers | [Electronic tickets](api/etickets.md) |
| Audience voting tickets and prizes | [Voting tickets](api/tickets.md) |
| City and region lookup | [Geography](api/geo.md) |
| Platform administration | [Admin](api/admin.md), [API keys](api/api_keys.md), [IP blocks](api/blocked_ips.md) |
| Browser authorization and internal protocols | [VK ID](api/vk.md), [Notifications pool](api/pool.md), [Diagnostics](api/error.md) |

## Quick start

Use your event's HTTPS host, such as `https://example.cosplay2.ru`, as
`COSPLAY2_BASE_URL`. Event tokens are issued in organizer settings. Supply credentials
through environment variables rather than saved command examples.

```sh
curl "$COSPLAY2_BASE_URL/api/events/get_settings" \
  -H "X-API-Key: $COSPLAY2_API_KEY" \
  -H "X-API-Secret: $COSPLAY2_API_SECRET"

curl "$COSPLAY2_BASE_URL/api/topics/get_with_fields" \
  -H "X-API-Key: $COSPLAY2_API_KEY" \
  -H "X-API-Secret: $COSPLAY2_API_SECRET" \
  -H 'Content-Type: application/json' \
  --data '{"topic_url_code":"example"}'
```

## Authentication

Send both `X-API-Key` and `X-API-Secret` to the event's HTTPS host or custom domain.
Create tokens in organizer settings; the generation UI defaults to 30 days.

**Access** labels identify browser contexts, not guaranteed token permissions.
Portal, account, admin and payment routes may require separate authentication.
An **SDK** label identifies the corresponding Python method.

## Requests

- Use the listed method: some reads use POST and some GET calls change state.
- POST bodies are JSON unless another content type is listed. Tables identify
  JSON, query, path, form and multipart fields. Let the HTTP client set upload boundaries.
- Types and defaults describe frontend requests, not server validation requirements.
  Optional fields are sometimes omitted by the caller.
- Preserve each field's wire type, including stringified ids.
- Omit `wid` (the browser tab id) and AngularJS `$$hashKey` metadata.
- An omitted input section means no parameters were identified.

## Responses and errors

JSON may arrive as `text/html`; parse the body. Downloads and HTML responses are
listed separately. Response descriptions show raw HTTP values; see
[SDK normalization](api/sdk-normalization.md) for Python conversions.

Many object responses include a success marker alongside the payload:

```json
{"message":"ok","comments":[]}
```

The marker is not universal. Unknown or incomplete schemas are labeled explicitly;
a list of known fields does not specify a complete response.

Errors may return 4xx/5xx with Russian plain text or a JSON `message`.
Per-endpoint error schemas, pagination and rate limits are unknown unless listed.
Retry only repeatable operations; design deletions and feeds with `onlynew: 1`
can change state.

## Wire formats

| Value | HTTP representation | Context |
|---|---|---|
| UTC timestamp | `"YYYY-MM-DD HH:MM:SS"` string | Requests, topics, comments, feed avatar timestamps |
| Unix time | Integer seconds | Avatar timestamps in `requests/get_user`, `users/get`, `users/search` and ratings |
| Unix time | Integer milliseconds | User event dates, feed update/read times, planner dates |
| Local display time | `"DD.MM.YY HH:MM"` string | Event settings, topic state and deadline updates |
| Local date | `"DD.MM.YYYY"` string | Festival creation; profile birthday edits |
| Flag | Integer `0`/`1`, sometimes JSON boolean | Format varies by field; `requests/get.editEnabled` uses a boolean |
| Encoded JSON | String containing another JSON document | Event design, plans, some stored form values |
| Empty collection | Sometimes `null` rather than `[]` | Registration report participants |
| Unset optional enum | Sometimes `""` rather than `null` | Custom section/field `internal_name` |

Local times use `events/get_settings.event.timezone`. Geography also varies:
`geo/code_city` has returned string coordinates, while rating geography uses numbers.
Use endpoint-specific descriptions where they narrow this table.
