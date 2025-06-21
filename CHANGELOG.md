# Changelog

## [Unreleased]

### Added

- Working mode: `normal|whitelist|blacklist`
- Chat control to avoid usage from blacklisted groups/users, or only allow whitelisted groups/users depending on working mode

### Removed

- Removed unused functions on domain section related to suscription management.
  - This is replaced by logic directly implemented over memory/database logic.

## [1.1.1] - 2025-06-21

### Fixed

- Suscription report generation fix.

## [1.1.0] - 2025-06-21

### Added

- On `app/communications`, now `notify_suscribers` returns the result of each notification as an array.
  - This is further used in `app/actions` to control and correctly process situations like user blocks, which lead to suscription pruning.

### Changed

- Refactor handlers to perform actions like `unsuscribe` in separate functions,  not tangled with the interface logic.

## [1.0.0] - 2024-11-10

### Added

- Included `version.txt`
- Included `CHANGELOG.md`
- Included `Makefile`
- Implemented `app/domain/infra` layer division.
- Included `tests`
  - For infrastructure layer
  - For domain layer
  - For app layer
- Included `utils` module at `app` level
- Bot features
  - Included inline menu for `add|del|list` actions.
- Using `apscheduler` to schedule tasks, added it as dependency.
- Basic configuration and files with translation for languages.
  - Setup by default to `es_ES`, selected on startup.
- `docker-compose` file for deployment
- `MIT License`
- `coverage_percentage.txt` and `publish_data.json` files for reference and badge mechanics.

### Changed

- Switched from `python-telegram-bot` to `pyrogram`
- Updated `Dockerfile`
  - Updated from `python:3.9.5` to `python:3.12-slim-buster`
  - References from `python3` to `python` alias
- Updated `Readme.md`
- Bot message changes
- Bot domain model now based on [`suscription`, `chat`, `manga`, `chapter`]
- Extracted messages into language JSON files. Available:
  - `es_ES`
  - `en_US`
- ...

### Removed

- Removed `DeployBot.sh`
- Removed `PrivateData` from `.gitignore`, as switched to `.env` approach to load `bot token`
