## What and why

<!-- What does this change and why? Link related issues: "Closes #123". -->

## How it was verified

<!-- Unit tests added? Live tests run (`uv run pytest -m live -rw`), and against which
     kind of event? For new endpoints: how you captured the payload shape. -->

## Checklist

- [ ] PR title follows Conventional Commits (`feat(topics): add comment endpoints`)
- [ ] `uv run pytest`, `uv run ruff check`, `uv run ruff format --check` and `uv run ty check` pass
- [ ] `CHANGELOG.md` has an entry under `[Unreleased]`; breaking changes are marked **Breaking:**
- [ ] New or changed endpoints: sync and async methods match, `README.md` resource table and `docs/api-notes.md` are updated
- [ ] No credentials, cookies or real personal data (names, contacts, HAR excerpts) in code, fixtures or this description
