# Contributing

Thanks for helping out. Cosplay2.ru has no public API documentation, so the most useful
contributions are new endpoints, fixes for API drift and notes on quirks you ran into.

## Reporting a problem

Open an issue with the method you called, what you expected and what happened. If a live
call raised `UnknownFieldsWarning` or a validation error, include the field names and the
shape of the value, with real names, contacts and ids replaced by made-up ones.

## Setting up

You need [uv](https://docs.astral.sh/uv/). Then:

```shell
uv sync
uv run pytest
uv run ruff check && uv run ruff format --check
uv run ty check
```

All four must pass before a pull request is merged. Live tests against a real event are
optional and need an API token; see [Testing against the real site](README.md#testing-against-the-real-site).

## Making a change

Code conventions, the step-by-step for adding an endpoint and the versioning rules live in
[AGENTS.md](AGENTS.md). It is written for AI coding agents but applies to everyone. In
short:

- Add sync and async methods with identical signatures, a model, a unit test, a row in
  the `README.md` resource table and in `docs/api-notes.md`.
- Keep model fields optional unless every observed payload has them.
- Add a `CHANGELOG.md` entry under `[Unreleased]`.
- Use [Conventional Commits](https://www.conventionalcommits.org/) for commit and PR
  titles, e.g. `fix(models): make drifting fields optional`. Mark breaking changes with `!`.

Keep pull requests focused on one thing; separate refactors from behaviour changes.

## Privacy

Browser HAR captures and real API responses contain session cookies and personal data of
event participants. Use them to learn payload shapes, but never commit them or paste them
into issues or pull requests. Tests use made-up values only.

## Validation and release checks

Offline tests exercise both asyncio and Trio and both clients. Assert the wire
request as well as the parsed result; use synthetic identities and credentials.
Add cases for absent/null/unknown fields, empty collections and observed alternate
wire formats. Keep transport errors, retry limits and cancellation deterministic.

For an observed payload regression, record the endpoint, observation date, role,
event configuration and transformation notes beside a sanitized fixture. Replace
identities, contacts, free text and secrets before saving it. Do not label invented
examples as captures. Mock tests verify recorded contracts; only opt-in read-only
live tests establish that the current service still matches them. Review drift
warnings before changing models. Never run live writes as release checks.

CI checks Python 3.12–3.15, dependency lower bounds, lint, formatting, typing and
clean installation of both wheel and sdist. Before a release, run:

```shell
uv run --python 3.12 --resolution lowest-direct pytest
uv sync --locked
uv build
```

Install the artifacts into a fresh environment and run `scripts/check_package.py`.
Before the first public push, inspect tracked files and all Git history for HARs,
credentials and personal data. Ignoring a file does not remove it from history.
Use a dedicated test event for deliberate read-only live checks; do not upload raw
responses or logs as CI artifacts.
