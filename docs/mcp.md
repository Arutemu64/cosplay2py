# Optional MCP server

Install the extra and start the local stdio server:

```shell
uv sync --extra mcp
uv run --extra mcp cosplay2py-mcp
```

For an installed package use `pip install 'cosplay2py[mcp]'`, followed by
`cosplay2py-mcp`. `python -m cosplay2py.mcp` is equivalent.
The normal library installation does not depend on FastMCP.

After a release containing the MCP extra is published, run it without a checkout
or permanent installation using [uvx](https://docs.astral.sh/uv/guides/tools/#requesting-extras)
from PyPI or a pinned GitHub release tag:

```shell
uvx --from "cosplay2py[mcp]" cosplay2py-mcp
uvx --from "cosplay2py[mcp] @ git+https://github.com/Arutemu64/cosplay2py@v0.5.0" cosplay2py-mcp
```

`--from` selects the package and its optional extra; `cosplay2py-mcp` is the
executable it provides. Always pin a version (`cosplay2py[mcp]==X.Y.Z` or
`@vX.Y.Z`) when configuring long-lived hosts so background tool refreshes stay
reproducible.

Configure `COSPLAY2_BASE_URL`, `COSPLAY2_API_KEY`, and `COSPLAY2_API_SECRET` in the
MCP host's environment. Tokens belong to one event. Never put credentials in tool
arguments or commit a populated MCP configuration. No API call runs on import.

## Host configuration

See the [universal `mcpServers` JSON example](../README.md#optional-mcp-server)
for `uvx`. How hosts load configuration and secrets varies:

| Host | Configuration file / root key | Passing secrets safely |
|---|---|---|
| Claude Desktop, Cursor, Antigravity, Windsurf | User config file (`mcpServers`) | Set `COSPLAY2_*` in `"env"` inside your user-local config (never in a committed repo file) |
| Claude Code | `.mcp.json` (`mcpServers`) or `claude mcp add` | Expand from the shell environment via `"COSPLAY2_API_KEY": "${COSPLAY2_API_KEY}"` |
| VS Code (GitHub Copilot) | `.vscode/mcp.json` (`servers`) | Use `"${env:COSPLAY2_API_KEY}"` or `inputs` prompts (`"${input:cosplay2_api_key}"`) |
| OpenAI Codex CLI | `~/.codex/config.toml` (`[mcp_servers.cosplay2]`) | Pass `env_vars = ["COSPLAY2_BASE_URL", "COSPLAY2_API_KEY", "COSPLAY2_API_SECRET"]` |

For the current checkout, run via `uv --directory` (replace the absolute project path):

```json
{
  "mcpServers": {
    "cosplay2": {
      "command": "uv",
      "args": ["--directory", "C:/path/to/cosplay2py", "run", "--extra", "mcp", "cosplay2py-mcp"]
    }
  }
}
```

The host must pass the three environment variables to the process. Set secrets
through the host's secret storage where available. To inspect tools interactively
from a terminal, use `npx @modelcontextprotocol/inspector uv run --extra mcp cosplay2py-mcp`.

## Available tools

These are MCP tools discovered through `tools/list` and invoked through
`tools/call`, rather than separate REST routes.

| Workflow | Tools | Underlying client methods |
|---|---|---|
| Event overview | `cosplay2_get_event_settings`, `cosplay2_get_event_state`, `cosplay2_list_topic_deadlines`, `cosplay2_list_topic_statistics` | `events.get_settings`, `events.get_state`, `events.get_topics_state`, `events.get_topics_statistic` |
| Nomination discovery | `cosplay2_list_topics`, `cosplay2_get_topic_form` | `topics.get_list`, `topics.get_form` |
| Applications | `cosplay2_list_topic_requests`, `cosplay2_list_all_requests`, `cosplay2_search_requests`, `cosplay2_get_request`, `cosplay2_list_request_comments` | `topics.get_requests`, `topics.get_all_requests`, `requests.search`, `requests.get`, `requests.get_comments` |
| Site pages | `cosplay2_list_pages`, `cosplay2_get_page` | `pages.get_list`, `pages.get` |
| Program and results | `cosplay2_get_schedule`, `cosplay2_get_winners` | `events.get_plan`, `events.get_winners` |

List/search tools accept `offset` (default 0) and `limit` (default 50, maximum 100).
They return `items`, `total`, and `next_offset` (`null` when finished).
`cosplay2_list_topic_requests` and `cosplay2_list_all_requests` accept an optional
`status` filter (`RequestStatus`); `cosplay2_list_all_requests` also accepts an
optional `topic_id` filter. Pagination and filtering are local: each call fetches
the upstream list, whose contents can change between calls.
`cosplay2_get_event_settings` clears `plan` and `design` to avoid duplicating the
schedule tree or CSS in overview calls. Schedule and winners return their complete
nested objects. Detail responses can be large. Datetimes and field aliases follow
the library models; event start/end times and nomination deadlines use the event's
local time.

### Joining application form sections and values

`cosplay2_get_request` returns a [`RequestDetails`](api-schemas.md#requestdetails)
object where the form schema and filled values are normalized into four sibling
arrays so repeating sections (for example, multiple participants or helpers in
one application) preserve their section instance boundaries without duplicating
schema metadata:

- `reqvalues[].topic_field_id` → `fields[].id`: resolves the field's `title`,
  `type` (`TopicFieldType`), and `internal_name` (`FieldTemplate`). For `select`
  fields, `fields[].data` holds a JSON-encoded list of allowed option strings;
  for `image` and `file` fields, `reqvalues[].value` holds a JSON-encoded
  [`ImageValue`](api-schemas.md#imagevalue) or [`FileValue`](api-schemas.md#filevalue) object.
- `reqvalues[].request_section_id` → `reqsections[].id`: groups values belonging
  to the same filled section instance (ordered by `reqsections[].order` when a
  section repeats).
- `reqsections[].topic_section_id` → `sections[].id` (and `fields[].section_id` →
  `sections[].id`): resolves the section definition's `title`, `order`,
  `max_repeat`, and `internal_name` (`SectionTemplate`).

Similarly, `cosplay2_get_topic_form` returns `topic_sections` and `topic_fields`,
joined by `topic_fields[].section_id` → `topic_sections[].id`.

This initial tool set is deliberately read-only. It excludes writes, generated
voting numbers, notifications, internal organizer comments (`get_org_comments`),
participant reputation feedback (`get_feedbacks`), bulk participant reports,
ticket/barcode workflows, uploads and arbitrary API forwarding. Nothing marks
notifications or applications as read. Read-only tools can still return personal
data; grant access only to trusted local hosts.

Future write tools should be a separately enabled capability set, with narrow
arguments, accurate mutation annotations and host confirmation. An annotation is
a hint, not an authorization boundary. No write opt-in is implemented here.

## Design guidance checked on 2026-11-02

The current [MCP specification is 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28).
The extra targets standalone FastMCP 4 (`>=4.0.0,<5`), tested initially with 4.1.5.
The framework handles protocol negotiation; the adapter does not hardcode wire
messages or advertise additional capabilities.

1. Use a small, explicit tool catalog with typed input/output schemas, useful
   descriptions, validated arguments and truthful read/idempotency hints. These
   are the capabilities agents need for discovery and execution, as described by
   the [MCP tools specification](https://modelcontextprotocol.io/specification/2026-07-28/server/tools).
2. Reuse one asynchronous API client through a server lifespan and close it at
   shutdown. See [FastMCP lifespans](https://gofastmcp.com/servers/lifespan).
3. Return structured model data and bound list results. Mask unexpected errors;
   translate API failures into a generic tool error without returning response
   bodies, headers or validation payloads. See [FastMCP tools](https://gofastmcp.com/servers/tools).
4. Use stdio for a local subprocess, reserving stdout for protocol messages.
   Streamable HTTP is the option for a future remote deployment; legacy SSE is
   unnecessary here. See [FastMCP transports](https://gofastmcp.com/deployment/running-server).
5. Keep credentials at the server boundary and treat participant text as untrusted
   data. A remote deployment needs its own authentication and authorization,
   HTTPS, origin validation and per-user access design; do not expose this
   single-event server directly to a network. See the
   [MCP security guidance](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices).

Tools suffice for this version. Resources and prompts can be added for concrete
host workflows; duplicating every tool as a resource adds no capability here.

## Offline verification

```shell
uv run --extra mcp pytest
uv run --extra mcp ruff check
uv run --extra mcp ruff format --check
uv run --extra mcp ty check
uv run --extra mcp --python 3.12 --resolution lowest-direct pytest
```

MCP tests use FastMCP's in-process client and HTTP mock transports; no credentials
or live API calls are needed. Without the extra, those tests are skipped.
