# Forbidden Paths and Actions

## Secret Files

Do not inspect, print, copy, summarize, or commit secret values from:

- `.env`
- `.env.*`
- credential files
- private keys
- token files

Configuration variable names may be referenced when necessary.
Secret values must not be exposed.

## Dependency Environments

Do not recursively inspect:

- `.venv/`
- `venv/`

Installed dependency source code is not part of the application.

Do not modify files inside virtual environments.

## Generated Files

Do not treat the following as source:

- `logs/`
- `output/`
- `__pycache__/`
- `.pytest_cache/`
- `.mypy_cache/`
- `.ruff_cache/`
- PyInstaller build output
- generated executables

Do not modify generated artifacts to implement application behavior.

## Repository Internals

Do not inspect or modify `.git/` internals during normal development tasks.

Git history may be inspected through Git commands when historical context is explicitly required.

## Security

Never:

- commit credentials;
- hardcode bot tokens;
- hardcode database credentials;
- expose connection strings;
- expose Redis credentials;
- expose proxy credentials;
- disable TLS certificate verification to bypass connection errors.

## Architecture

Do not place SQL/database access directly in Telegram handlers.

Do not place substantial business logic directly in Telegram handlers.

Do not turn builders into business-logic services.

Do not duplicate static Russian user-facing strings in builders when they belong in shared constants.

Do not introduce new architectural layers without a concrete requirement.

## Exploration

Do not recursively scan the whole repository by default.

Start from HARNESS and inspect targeted source paths.

Do not read unrelated files merely to increase context.

Do not inspect generated directories or dependency environments while searching for application code.

## Changes

Do not perform unrelated refactoring during a focused task.

Do not silently change public behavior outside the task scope.

Do not change dependency versions unless required by the task.

Do not change database schema implicitly.

Do not modify `main.spec` unless packaging behavior is relevant.

## Validation

Do not report a command, test, build, or validation as successful unless it was actually executed successfully.

## HARNESS

Never store secrets in HARNESS.

Do not store:

- raw logs;
- raw diffs;
- complete source files;
- temporary debugging notes;
- speculative conclusions.

HARNESS must contain durable project knowledge only.