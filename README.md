# cosplay2py

Unofficial typed sync and async client for the [Cosplay2.ru](https://cosplay2.ru) event API, built on
[httpx2](https://github.com/pydantic/httpx2) and [Pydantic](https://docs.pydantic.dev).

> [!WARNING]
> This project is AI-generated: most of the code, tests and documentation were written
> with an AI assistant. Review it before relying on it, and expect rough edges.

## Installing

The package is not on PyPI. Install it from a release tag:

```shell
uv add "cosplay2py @ git+https://github.com/Arutemu64/cosplay2py" --tag v0.1.0
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
| `events`      | `get_settings`, `get_state`, `get_topics_state`, `get_topics_statistic`, `get_buttons_state`, `get_staff`, `get_plan`, `save_plan`, `get_blank`, `get_reg_topics`, `get_reg_alphabet`, `check_external_domain`, `search`, `set_deadline` |
| `topics`      | `get_list`, `get_requests`, `get_all_requests`, `get_requests_for_planner`, `get_form`, `create`, `delete`, `reorder`, `fill_from_template`, `fill_from_topic`, `add_section`, `save_section`, `delete_section`, `add_field`, `delete_field`, `save_field`, `save_topic`, `reorder_section` |
| `requests`    | `get`, `get_comments`, `get_org_comments`, `get_user`, `generate_card_title`, `generate_card_announcement`, `generate_card_diplom`, `get_value_history`, `add_comment`, `delete_comment`, `save_field`, `upload_image`, `delete_image`, `save_data`, `set_status`, `create`, `create_section`, `change_topic`, `add_org_comment`, `delete_org_comment`, `get_feedbacks`, `add_feedback`, `delete_feedback` |
| `users`       | `get`, `save_field`, `add_friend`, `cancel_friend_invite`, `remove_friend`, `get_events`, `get_feeds`, `get_friends`, `search` |
| `design`      | `get`, `get_images`, `save`, `upload_image`, `delete_image` |
| `pages`       | `get_list`, `get`, `create`, `save_field`, `save_fields`, `delete`, `reorder` |
| `media`       | `get_data` |
| `etickets`    | `get_list`, `get_types`, `get_paymethods`, `get_vat_dictionary` |
| `tickets`     | `get_statistic`, `get_voting_statistics` |

### Data conventions

- Server timestamps become timezone-aware UTC `datetime`s, whether the API sent
  `"YYYY-MM-DD HH:MM:SS"`, Unix seconds or Unix milliseconds.
- Display strings like `"22.08.26 03:00"` (`TopicState`, `Event.start_time`) become
  naive `datetime`s, as the site shows them.
- `0`/`1` flags become `bool`. JSON packed into strings (`Event.design`, the plan) is parsed.
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
`max_retries`). Writes and `users.get_feeds()` retry only connection failures
(`ConnectError`), never HTTP responses or read/write timeouts. An ambiguous failure
may mean a write succeeded; check the service before repeating it yourself.

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
