# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses
[Semantic Versioning](https://semver.org/spec/v2.0.0.html): while on `0.x`, a minor bump
means a breaking change.

## [Unreleased]

## [0.1.0] - 2026-10-29

### Added

- Initial release of typed sync (`Cosplay2`) and async (`AsyncCosplay2`) clients
  for the Cosplay2.ru API, with Pydantic models, safe retries and typed errors.
- Read and write resources for events, topics, requests, users, design, pages,
  media, electronic tickets and tickets.
- API reference notes, usage examples, and offline tests covering both clients
  and asyncio/Trio, with CI for Python 3.12-3.15 and package installation.

[Unreleased]: https://github.com/Arutemu64/cosplay2py/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Arutemu64/cosplay2py/releases/tag/v0.1.0
