# Publishing

The `publish.yml` workflow builds and checks distributions when a `v*` tag is pushed.
The tag must match the version in `pyproject.toml`.

Before publishing, configure the PyPI trusted publisher for `cosplay2py` with
owner `Arutemu64`, repository `cosplay2py`, workflow `publish.yml`, and environment
`pypi`. Create the matching GitHub environment and configure any desired protection
rules. No API token is used by this workflow.

Prepare the release following `AGENTS.md`, then push the release commit and tag.
Check the GitHub Actions run for build, validation, and publication results.
