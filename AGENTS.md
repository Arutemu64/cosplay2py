# AGENTS.md

Typed sync + async client for the undocumented Cosplay2.ru event API (`httpx2` + Pydantic 2).
User-facing docs live in `README.md`; this file is for working on the code.

## Commands

```shell
uv sync
uv run pytest                      # offline unit tests (live tests are deselected)
uv run ruff check && uv run ruff format --check
uv run ty check                    # warnings are errors
uv run --python 3.12 --resolution lowest-direct pytest   # verify dependency lower bounds
```

Run pytest, ruff and ty before calling a change done. Live tests (`uv run pytest -m live -rw`)
need `COSPLAY2_API_KEY`, `COSPLAY2_API_SECRET` and `COSPLAY2_BASE_URL`; only run them when
the user asks and has those set.

## Layout

```
src/cosplay2py/
  _base_client.py   Endpoint dataclass, BaseClient: URL/credential resolution,
                    response unwrapping + validation, retry policy (no I/O)
  _client.py        Cosplay2 / AsyncCosplay2: transport loop, retries, context managers
  _exceptions.py    error hierarchy, make_status_error()
  _types.py         UTCDateTime, LocalDateTime, JsonEncoded, EmptyAsNone normalizers
  models/           Pydantic response models, all re-exported from models/__init__.py
  resources/        one module per API area; a sync and an async class per resource
tests/unit/         offline tests using httpx2.MockTransport, one file per resource module
tests/live/         read-only smoke tests against a real event (marker `live`)
docs/api-notes.md   language-agnostic notes on the API: quirks, wire formats, endpoints
```

## How an endpoint is added

1. **Model** in the matching `models/*.py`, subclassing `Cosplay2Model` (`extra="allow"`,
   frozen). Add it to `models/__init__.py` imports and `__all__` (kept sorted).
2. **Endpoint builder** at module level in `resources/<area>.py`: a constant
   `Endpoint[T](...)` for argument-less calls, or a `_name(args) -> Endpoint[T]` function.
   Declare `idempotent=` explicitly; only repeatable reads use `True`.
   Use `key=` when the payload sits under a top-level key (`{"comments": [...]}`); the
   `{"message": "ok"}` marker is stripped automatically.
3. **Methods** on both the sync class and its `Async*` twin, with identical signatures and
   docstrings. They only call `self._request(...)`; no I/O or parsing in resources.
4. If it is a new resource class, wire it into both clients in `_client.py`
   (annotation + `__init__`) and export it from `resources/__init__.py`.
5. Update the resource table in `README.md`, add a unit test, and add the call to
   `tests/live/test_live.py` if it is safe and read-only.
6. Add the endpoint to the table in `docs/api-notes.md`. If you found a quirk (an odd
   format, a side effect, a body the site builds unusually), write it down there too:
   say what you observed and in which context, not what you guess.
7. Add a `CHANGELOG.md` entry under `[Unreleased]` (see Versioning).

## How to analyze frontend JS

1. Start with the relevant site's HTML: the event host for event features, or
   `https://cosplay2.ru/` for global portal features. Read inline scripts and `globals`,
   and follow the actual script URLs in the page. Bundle names contain changing hashes
   (for example, `/states.<hash>.js`, `/factories.<hash>.js`, `/zip/c2.<hash>.js`);
   discover current URLs instead of hard-coding an old hash.
2. Search downloaded sources with `rg` for the API path or feature name. AngularJS
   state definitions reveal `templateUrl`, resolves, and lazy-loaded controllers
   (`$ocLazyLoad`). Follow those references into `/js/` and `/html/`: templates often
   contain inline controllers and API calls that are absent from the main bundles.
   A bundle with no matches does not establish that an endpoint is unused.
3. Trace each `$http.get`, `$http.post`, or `$upload.upload` call through its callers.
   Record the HTTP method, path, query/body fields, defaults, omitted fields, and value
   conversions. For a posted form object, inspect its initialization, `ng-model`s,
   `ng-options`, radio values, watchers, and submit handler. For uploads, inspect
   `fileFormDataName`, accompanying form data, and the success handler. Exclude `wid`
   as described below.
4. Trace response consumers as well: distinguish `$http.then`'s `res.data` from
   `.success`'s response body, identify wrapper keys and returned ids, and inspect
   templates for fields and closed domain sets. Extract enums from explicit frontend
   constants/options; do not infer a closed set from a handful of example payloads.
5. Compare with local HAR response bodies when available. HAR entries can omit script
   content or encode it as base64; inspect `response.content.encoding` before reading
   `text`. Decode downloaded text as UTF-8 so Russian labels remain readable. Keep
   frontend evidence separate from observed API payloads: a field used in a template
   does not prove it is always present, and an unobserved response shape stays `Any`.
6. Record findings in `docs/api-notes.md`, including source paths, inspection date,
   relevant role/host/context, and any uncertainty. Add offline request-shape tests
   for both clients, including serialization, response unwrapping, and upload fields.
   Do not execute writes to discover their behavior; live tests still require the
   user's request and must remain read-only.

Use temporary files for downloaded HTML/JS and remove your downloads after analysis.
Never commit captures, session data, or copied personal information; use synthetic
values in fixtures. Fetch public frontend assets without attaching local credentials.

## Conventions

- Python 3.12+: PEP 695 generics (`class Foo[T]`, `def f[T]`), `X | None`, `Self`.
- No `from __future__ import annotations`; quote forward references instead
  (`"Cosplay2"` under `TYPE_CHECKING`).
- Absolute imports only (`ban-relative-imports = "all"`). Line length 88.
- Model fields keep the API's names; when renaming for readability use
  `Field(alias="apiName")` (`populate_by_name` is on). Normalize wire quirks with the types
  in `_types.py` instead of ad-hoc validators: `UTCDateTime` for server timestamps,
  `LocalDateTime` for `"DD.MM.YY HH:MM"` display strings, `Annotated[T, JsonEncoded]` for
  JSON packed into strings, `Annotated[E | None, EmptyAsNone]` when the API sends `""`
  for an unset optional enum. `0`/`1` flags are typed as `bool`.
- Closed domain sets (statuses, roles, categories, field/page/plan node types, template
  `internal_name`s) are extracted from the site's unminified AngularJS frontend (`index.html`
  `globals`, `/js/*.js`, and `/html/*.html` templates) and enforced as strict `StrEnum` /
  `IntEnum` types (no `Enum | str` open-union fallbacks) in both models and resource
  method parameters.
- For other fields, make them optional (`= None`) unless every observed payload has them,
  and use `Any` rather than guessing at a shape you haven't seen. Document non-obvious
  fields with an attribute docstring below the field.
- Request bodies mirror what the site sends, including stringified ids where it does
  (e.g. `{"request_id": str(request_id)}`).
  Two exceptions: leave out `wid`, a random per-tab id the site's `poolIdInjector`
  adds to every request body for its change-notification pool; and don't wrap
  `/api/pool/get`, that pool's 10-second polling endpoint for live UI updates.
- Docstrings are short, describe what is returned, and use reST (`:param x:`, double-backtick literals).
- Never put credentials in reprs, logs or exception messages.

## Tests

- One file per resource module (`test_events.py`, `test_misc.py`, ...); `test_client.py`
  covers configuration, errors, retries and sync/async parity (which checks that every
  `Async*` method mirrors its sync twin's signature and docstring).
- Unit tests build clients with `make_client(handler)` / `make_async_client(handler)` and a
  handler returning `json_response(...)` (the real API serves JSON as `text/html`).
  Fixtures in `tests/unit/conftest.py` clear `COSPLAY2_*` env vars and zero retry delays.
- To run a test against both clients, take the `api` fixture and call
  `await api(handler, lambda c: c.<resource>.<method>(...))`; prefer it for write
  endpoints. Tables of such lambdas (`test_writes`) cover the simple ``"ok"`` writes.
- Async tests use `@pytest.mark.anyio` (asyncio and Trio backends).
- Live tests must never create, modify or mark anything as read. `report_drift()` turns
  undeclared fields into `UnknownFieldsWarning`; when one shows up, add the field to the
  model.

## Versioning

SemVer, released as git tags (`vX.Y.Z`); the package is not published to PyPI and
consumers install from a tag. The version lives only in `pyproject.toml`
(`__version__` reads it via `importlib.metadata`), so never hard-code it elsewhere.

- While on `0.x`, **minor** = breaking: removing or renaming a method, parameter, model
  field or export, making a field required or narrowing its type, changing defaults or
  the exception raised.
- **Patch** = everything backward compatible: new endpoints, new optional fields, making
  a field optional, drift and bug fixes.
- Record user-visible library changes under `## [Unreleased]` in `CHANGELOG.md`, in the
  matching section (`Added`, `Changed`, `Fixed`, `Removed`); flag breaking ones with
  **Breaking:**.
- Omit documentation-only, tooling, CI, and release-process changes from the changelog.
- Releasing (only when the user asks): `uv version --bump patch|minor`, rename
  `[Unreleased]` to `[X.Y.Z] - YYYY-MM-DD` and open a new empty `[Unreleased]`, commit
  `chore(release): vX.Y.Z`, then `git tag vX.Y.Z`. The tag must match `pyproject.toml`;
  don't push without being asked. The first release is `0.1.0` as-is, without a bump.

## Commits

Commit titles follow [Conventional Commits](https://www.conventionalcommits.org/):
`type(scope): summary`, imperative and lowercase, no trailing period, e.g.
`feat(topics): add comment endpoints` or `fix(models): make drifting fields optional`.

- Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `build`, `ci`, `chore`.
- Scope is optional; use the resource or package area (`events`, `requests`, `topics`,
  `users`, `models`, `client`).
- Mark breaking changes with `!` (`feat(models)!: rename ...`) and a `BREAKING CHANGE:`
  footer, matching the **Breaking:** entry in `CHANGELOG.md`.

## Data hygiene

`*.har` captures in the repo root contain session cookies and personal data. They are
gitignored: use them to learn payload shapes, but never commit them, quote tokens or
cookies from them, or copy real names/contacts into fixtures. Use made-up values in tests.
