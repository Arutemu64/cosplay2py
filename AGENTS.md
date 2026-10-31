# Working on cosplay2py

Typed sync + async client for the undocumented Cosplay2.ru API (`httpx2`, Pydantic 2).
User docs: [README.md](README.md). Tool settings: [pyproject.toml](pyproject.toml).

## Commands

```shell
uv sync
uv run pytest
uv run ruff check
uv run ruff format --check
uv run ty check
```

Run all checks before calling a change done; pytest is offline by default and ty
warnings are errors. Check dependency lower bounds when changing dependencies:
`uv run --python 3.12 --resolution lowest-direct pytest`.

Live tests require an explicit user request and `COSPLAY2_API_KEY`,
`COSPLAY2_API_SECRET`, `COSPLAY2_BASE_URL`: `uv run pytest -m live -rw`.
They must remain read-only, including never marking anything as read.

## Navigation

- `src/cosplay2py/_base_client.py`: endpoints, configuration, response unwrapping,
  validation and retry policy; no I/O. `_client.py`: sync/async transport and lifecycle.
- `_exceptions.py`: errors; `_types.py`: wire normalizers; `models/`: response models;
  `resources/`: one module per API area with paired sync/async classes.
- `tests/unit/`: offline MockTransport tests, one file per resource; `test_client.py`
  covers configuration, errors, retries and sync/async parity.
- `docs/api-notes.md`: HTTP conventions; `docs/api-schemas.md`: wire fields and enums;
  `docs/api/`: endpoint behavior and workflows.
- Before researching undocumented behavior, read [the research guide](docs/contributing-api.md).

## Endpoint changes

1. Add models inheriting frozen, extra-allowing `Cosplay2Model`; keep imports and
   `__all__` sorted in `models/__init__.py`.
2. Define module-level `Endpoint[T]` constants for argument-less calls or builders
   for parameterized calls. Declare `idempotent=` explicitly: only repeatable reads
   use `True`. Set `key=` for wrapped payloads; `{"message": "ok"}` is stripped automatically.
3. Add sync/async methods with identical signatures and docstrings, only calling
   `self._request(...)`; no parsing or I/O in resources. Wire new resources into both
   clients (annotations and initialization) and export from `resources/__init__.py`.
4. Test both clients offline: request serialization, response unwrapping and uploads.
   Add safe read-only calls to `tests/live/test_live.py` without running them.
5. Update the README resource table, `docs/api/index.md`, resource page and wire
   schemas as applicable. Document quirks and uncertainty, not research logs.
   Record user-visible library changes in `CHANGELOG.md`.

## Python and models

- Python 3.12+: PEP 695 generics, `X | None`, `Self`, absolute imports. No
  `from __future__ import annotations`; quote forward references under `TYPE_CHECKING`.
- Keep API field names; use `Field(alias="apiName")` for intentional renames.
  Reuse `_types.py`: `UTCDateTime` for server timestamps, `LocalDateTime` for
  `DD.MM.YY HH:MM`, `Annotated[T, JsonEncoded]` for JSON strings and
  `Annotated[E | None, EmptyAsNone]` for unset enums sent as `""`. Type 0/1 flags as bool.
- Enforce closed domains with `StrEnum`/`IntEnum` in models and resource parameters,
  without `Enum | str` fallbacks. Extract values from explicit frontend constants
  and options, not sample payloads. Other fields default to `None` unless present
  in every observed payload; unobserved shapes stay `Any`.
- Mirror frontend request bodies, including stringified IDs. Omit the per-tab `wid`
  notification identifier and do not wrap `/api/pool/get`.
- Use short reST docstrings (`:param x:`, double-backtick literals). Each public
  response model needs a class docstring explaining the object. Document non-obvious
  fields with attribute docstrings immediately below them: units, timezones, IDs,
  sentinels, normalization and endpoint-specific availability. Keep uncertainty explicit.
- Use `Field(description=...)` only for a concrete JSON Schema consumer, without
  duplicating attribute docs. Keep `use_attribute_docstrings` disabled for Pydantic
  2.4 support (it requires 2.7+ and runtime class source).

## Tests

- Use `make_client(handler)` / `make_async_client(handler)` and `json_response(...)`;
  the API serves JSON as `text/html`. Fixtures clear `COSPLAY2_*` and retry delays.
- Prefer `await api(handler, lambda c: c.resource.method(...))` for both clients,
  especially writes; use `test_writes` tables for simple `"ok"` responses.
- Async tests use `@pytest.mark.anyio` for asyncio and Trio. Preserve signature and
  docstring parity checks. Add fields reported by `report_drift()` as
  `UnknownFieldsWarning` to their models.

## Changes and releases

- Conventional Commits: `type(scope): imperative lowercase summary`, no final period.
  Breaking commits use `!` and a `BREAKING CHANGE:` footer.
- Record library changes under `[Unreleased]` (`Added`, `Changed`, `Fixed`, `Removed`);
  flag breaking changes with **Breaking:**. Omit docs, tooling, CI and release process.
- On 0.x, breaking changes require a minor bump: removals/renames, required fields,
  narrower types, changed defaults or exceptions. Compatible additions/fixes use patch.
- Version exists only in `pyproject.toml`; `__version__` reads installed metadata.
  Consumers install git tags, not PyPI releases.
- Release only when asked: `uv version --bump patch|minor`, date the released changelog
  section, open an empty `[Unreleased]`, commit `chore(release): vX.Y.Z`, then tag
  `vX.Y.Z` matching the project version. First release is 0.1.0 without a bump.
  Push only when asked.

## Data handling

Root `*.har` files contain cookies and personal data. Inspect locally only; never
commit captures/session data or copy real names/contacts into fixtures. Use synthetic
values. Never expose credentials in reprs, logs or exceptions. Fetch public frontend
assets without local credentials; use temporary downloads and remove them afterward.
