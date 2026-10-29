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
  _types.py         UTCDateTime, LocalDateTime, JsonEncoded wire-format normalizers
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

## Conventions

- Python 3.12+: PEP 695 generics (`class Foo[T]`, `def f[T]`), `X | None`, `Self`.
- No `from __future__ import annotations`; quote forward references instead
  (`"Cosplay2"` under `TYPE_CHECKING`).
- Absolute imports only (`ban-relative-imports = "all"`). Line length 88.
- Model fields keep the API's names; when renaming for readability use
  `Field(alias="apiName")` (`populate_by_name` is on). Normalize wire quirks with the types
  in `_types.py` instead of ad-hoc validators: `UTCDateTime` for server timestamps,
  `LocalDateTime` for `"DD.MM.YY HH:MM"` display strings, `Annotated[T, JsonEncoded]` for
  JSON packed into strings. `0`/`1` flags are typed as `bool`.
- The API is undocumented and drifts: make fields optional (`= None`) unless every
  observed payload has them, and use `Any` rather than guessing at a shape you haven't
  seen. Document non-obvious fields with an attribute docstring below the field.
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
- Live tests must never create, modify or mark anything as read (that is why
  `users.get_feeds` is excluded). `report_drift()` turns undeclared fields into
  `UnknownFieldsWarning`; when one shows up, add the field to the model.

## Versioning

SemVer, released as git tags (`vX.Y.Z`); the package is not published to PyPI and
consumers install from a tag. The version lives only in `pyproject.toml`
(`__version__` reads it via `importlib.metadata`), so never hard-code it elsewhere.

- While on `0.x`, **minor** = breaking: removing or renaming a method, parameter, model
  field or export, making a field required or narrowing its type, changing defaults or
  the exception raised.
- **Patch** = everything backward compatible: new endpoints, new optional fields, making
  a field optional, drift and bug fixes.
- Record every user-visible change under `## [Unreleased]` in `CHANGELOG.md`, in the
  matching section (`Added`, `Changed`, `Fixed`, `Removed`); flag breaking ones with
  **Breaking:**.
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
