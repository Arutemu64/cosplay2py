# cosplay2py

Unofficial typed sync and async client for the [Cosplay2.ru](https://cosplay2.ru) API, built on
[httpx2](https://github.com/pydantic/httpx2) and [Pydantic](https://docs.pydantic.dev).

> [!WARNING]
> This project is AI-generated: most of the code, tests and documentation were written
> with an AI assistant. Review it before relying on it, and expect rough edges.

## Installing

Requires Python 3.12 or newer. Install from PyPI with uv:

```shell
uv add cosplay2py
```

Or with pip:

```shell
pip install cosplay2py
```

To install a specific release directly from GitHub:

```shell
uv add "cosplay2py @ git+https://github.com/Arutemu64/cosplay2py" --tag v0.3.0
```

Versions follow SemVer. On `0.x`, a minor bump (`0.1` → `0.2`) may break things and a
patch bump never does. See [CHANGELOG.md](CHANGELOG.md).

## Authentication

API tokens are issued **per event**: on the event site open *Орги → Настройка → API токены*
and create a token. You get an API key and an API secret (the secret is shown once;
tokens expire after 30 days). The client sends them as `X-API-Key` / `X-API-Secret`.

## Usage

```python
from cosplay2py import Cosplay2
from cosplay2py.models import BlankId, RequestStatus

with Cosplay2(subdomain="ff26summer", api_key="...", api_secret="...") as c2:
    event = c2.events.get_settings()
    print(event.title, event.timezone)

    for topic in c2.topics.get_list():
        listing = c2.topics.get_requests(topic.url_code)
        approved = [r for r in listing.requests if r.status is RequestStatus.APPROVED]
        print(topic.title, len(approved))

    details = c2.requests.get(687475)
    print(details.values_by_field())

    jury_sheet = c2.events.get_blank(BlankId.JURY).html
```

Async (asyncio or trio):

```python
from cosplay2py import AsyncCosplay2

async with AsyncCosplay2(subdomain="ff26summer") as c2:
    state = await c2.events.get_state()
    print(state.requests_total)
```

Events on a custom domain: `Cosplay2(base_url="https://fancom.info", ...)`.

Any argument left out falls back to the environment: `COSPLAY2_API_KEY`,
`COSPLAY2_API_SECRET`, `COSPLAY2_BASE_URL`.

### Resources

| Attribute     | Methods |
|---------------|---------|
| `events`      | `get_settings`, `save_setting`, `get_state`, `get_topics_state`, `get_topics_statistic`, `get_staff`, `add_org`, `delete_org`, `change_main_org`, `add_curator`, `delete_curator`, `get_winners`, `get_plan`, `save_plan`, `get_blank`, `get_reg_topics`, `get_reg_alphabet`, `search`, `set_deadline` |
| `topics`      | `get_list`, `get_requests`, `get_all_requests`, `get_requests_for_planner`, `get_form`, `get_with_groups`, `add_child_topic`, `delete_child_topic`, `create`, `delete`, `reorder`, `fill_from_template`, `fill_from_topic`, `add_section`, `save_section`, `delete_section`, `add_field`, `delete_field`, `save_field`, `save_topic`, `reorder_section`, `reorder_field`, `generate_card_titles`, `reorder_requests` |
| `requests`    | `get`, `get_comments`, `get_org_comments`, `get_user`, `generate_card_title`, `generate_card_announcement`, `generate_card_diplom`, `generate_voting_number`, `search`, `get_value_history`, `add_comment`, `delete_comment`, `save_field`, `upload_image`, `delete_image`, `upload_file`, `delete_file`, `save_data`, `set_status`, `create`, `create_section`, `delete_section`, `change_topic`, `add_org_comment`, `delete_org_comment`, `get_feedbacks`, `add_feedback`, `delete_feedback` |
| `users`       | `search` |
| `design`      | `get`, `get_images`, `save`, `upload_image`, `delete_image`, `delete_panel_logo`, `delete_header_logo`, `delete_site_background` |
| `pages`       | `get_list`, `get`, `create`, `save_field`, `save_fields`, `delete`, `reorder` |
| `media`       | `get_data`, `add_album`, `save_album_field`, `delete_album` |
| `cards`       | `get_topics_and_cards`, `get_card`, `get_topics_and_requests`, `get_request` |
| `etickets`    | `get_list`, `get_types`, `add_type`, `delete_type`, `reorder_type`, `save_type_field`, `save_field`, `delete`, `create`, `get`, `get_status`, `save_personal_data` |
| `tickets`     | `get_statistic`, `get_voting_statistics`, `create`, `clear_votes`, `add_prize`, `delete_prize`, `save_prize_field`, `save_prize_handed`, `get_ticket`, `check_for_voting`, `get_voting_data`, `get_cards`, `select_winner` |

### Data conventions

- Server timestamps become timezone-aware UTC `datetime`s, whether the API sent
  `"YYYY-MM-DD HH:MM:SS"`, Unix seconds or Unix milliseconds.
- Display strings like `"22.08.26 03:00"` (`TopicState`, `Event.start_time`) become
  naive `datetime`s, as the site shows them.
- `0`/`1` flags become `bool`. JSON packed into strings (`Event.design`, the plan) is parsed.
- Closed domain sets (`RequestStatus`, `TopicFieldType`, `PageType`, `PlanNodeType`,
  `EventRole`, `EventStatus`, `EventTime`, `TopicCategory`,
  `PublicRequests`, `TopicTemplate`, `SectionTemplate`, `FieldTemplate`, `FeedbackMark`,
  `CardField`, `TicketKind`, `TicketCreateMode`, `VotingType`, `BlankId`, `Deadline`) are
  validated strictly as `StrEnum` / `IntEnum` members (empty strings on optional fields
  normalize to `None`).
- Unknown fields are kept rather than rejected. Read them via `model.model_extra`.

Talking to the API without this library? [docs/api-notes.md](docs/api-notes.md)
describes its endpoints, wire formats and quirks.

### Errors

```
Cosplay2Error
└── APIError
    ├── APIConnectionError
    │   └── APITimeoutError
    ├── APIResponseValidationError   # 2xx, but not the expected JSON
    └── APIStatusError               # non-2xx; .status_code, .body, .response
        ├── BadRequestError (400)
        ├── AuthenticationError (401)
        ├── PermissionDeniedError (403)
        ├── NotFoundError (404)
        ├── RateLimitError (429)
        └── InternalServerError (5xx)
```

Repeatable reads retry transport failures and 429/502/503/504 responses, with
exponential backoff and jitter (2 retries by default, configurable with
`max_retries`). Writes retry only connection failures (`ConnectError`), never
HTTP responses or read/write timeouts. An ambiguous failure may mean a write
succeeded; check the service before repeating it yourself.

`Retry-After` supports seconds and HTTP dates. If the server asks for more than
30 seconds, the error is returned immediately instead of retrying early.
Error messages omit response bodies and validation inputs. Inspect `.response`
or `.body` explicitly when debugging; these can contain personal data.

### Customizing HTTP

Pass `timeout=` (seconds or `httpx2.Timeout`), extra `headers=`, or a fully configured
`http_client=httpx2.Client(...)` / `httpx2.AsyncClient(...)` for proxies, custom
transports or testing with `httpx2.MockTransport`. A client you pass in is not closed by
the wrapper. Its timeout and default headers apply; wrapper headers override
matching defaults, and redirects are always disabled. `timeout=` applies only to a
client created by the wrapper. Timeouts limit network phases, not the total time
across retries. Use HTTPS for event credentials; HTTP is supported for local testing.
Base URLs cannot contain userinfo, query strings or fragments.

This client follows observed site behavior, which can change without notice.
Enable `logging.getLogger("cosplay2py")` at `DEBUG` to see requests.

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to propose changes.

```shell
uv sync
uv run prek install           # install Git hooks once per clone
uv run pytest                 # offline unit tests (default)
uv run prek run --all-files    # lint, format, and type-check
```

### Testing against the real site

`tests/live` holds read-only smoke tests that are deselected by default. They need a token
for the event (PowerShell shown):

```powershell
$env:COSPLAY2_API_KEY = "..."
$env:COSPLAY2_API_SECRET = "..."
$env:COSPLAY2_BASE_URL = "https://ff26summer.cosplay2.ru"
uv run pytest -m live -rw
```

`-rw` lists warnings: fields the API returns that the models don't declare yet show up
as `UnknownFieldsWarning`, an early sign of API drift.

Portal reads work with the configured event base URL (verified with event API
credentials); `https://cosplay2.ru` returned HTTP 403 with those credentials. Methods: `events.filter_list()`,
`events.get_types()`, `events.create_festival()`, `events.create_festival_logo()`,
`users.ratings_global()` and the country/area/region/city variants,
`users.get_region_geo_id()`, and `geo.code_city()`. Unobserved response shapes
are returned as JSON data.
