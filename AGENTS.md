# Repository Guidelines

## Repository Scope

The repository root is the working directory.

Application source code lives under `src/`. Project configuration, HARNESS, dependency metadata, and packaging configuration may live outside `src/`.

Do not recursively scan the repository. Use HARNESS to locate the relevant subsystem, then inspect targeted source files.

Source code and configuration are authoritative if HARNESS is outdated.

## Agent Orchestration

Project agents:

* `explorer` — read-only investigation and implementation planning.
* `worker` — implementation and validation.
* `scribe` — post-implementation HARNESS reconciliation.

### Non-trivial tasks

For tasks requiring investigation, cross-module changes, business-rule changes, database/Redis behavior, shared interfaces, or unclear implementation location:

1. Delegate investigation to `explorer`.
2. Wait for its findings and implementation plan.
3. Delegate implementation to `worker`, passing the relevant explorer result.
4. Wait for implementation and validation.
5. Delegate to `scribe` when the completed change may affect durable project knowledge.

Do not start dependent stages in parallel.

### Trivial tasks

For clearly localized changes such as typos, known static strings, formatting, or obvious one-line fixes, `explorer` may be skipped and `worker` used directly.

Do not invoke `scribe` for trivial changes unless durable project knowledge changed.

### Context handoff

Pass to `worker` the explorer's:

* relevant files;
* verified findings;
* execution flow;
* implementation plan;
* risks;
* validation recommendations.

Pass to `scribe`:

* original task;
* implementation summary;
* changed files;
* validation results.

Agents must verify repository state when needed and must not blindly trust another agent's summary.

The parent Codex agent is responsible for orchestration and final reporting.

## HARNESS

Project navigation and durable knowledge live in `HARNESS/`:

* `README.md` — HARNESS protocol.
* `STRUCTURE.md` — compact repository map.
* `NOTES.md` — durable architectural and project-specific notes.
* `FORBIDDEN.md` — forbidden paths and actions.
* `HISTORY.md` — compact history of meaningful changes.
* `STACK.md` — runtime, infrastructure, libraries, and important versions.

Before source investigation, use at minimum:

* `HARNESS/STRUCTURE.md`
* `HARNESS/FORBIDDEN.md`

Read:

* `NOTES.md` for behavior, architecture, and integrations;
* `STACK.md` for dependencies, runtime, MSSQL, Redis, or packaging;
* `HISTORY.md` only when previous changes are relevant.

HARNESS is navigation and project memory, not a replacement for reading actual source code.

## Project Architecture

Entry point:

`src/main.py`

Main areas:

* `src/bot/` — Telegram handlers, builders, keyboards, workers, and delivery.
* `src/application/services/` — business rules and orchestration.
* `src/application/repositories/` — database access.
* `src/core/db/` — SQLAlchemy definitions.
* `src/core/dto/` — DTOs.
* `src/core/constants.py` — shared static user-visible text and display formats.

Expected dependency direction:

`handler -> service -> repository -> database`

Keep handlers thin.

Business rules belong in services.
Database access belongs in repositories.
Message formatting belongs in builders.
Keyboard construction belongs in keyboard modules.
Queued/Redis delivery belongs in worker infrastructure.

When modifying existing behavior, inspect the implementation, relevant callers, and direct dependencies before editing.

## Forbidden and Generated Paths

Do not use these as application source:

* `.venv/`
* `venv/`
* `logs/`
* `output/`
* `__pycache__/`
* `.pytest_cache/`
* `.mypy_cache/`
* `.ruff_cache/`
* `.git/`

Do not modify generated artifacts.

Do not inspect dependency source inside virtual environments during normal project exploration.

Never expose or commit secrets, including `.env`, tokens, connection strings, credentials, passwords, or private keys.

Do not disable TLS certificate verification as a workaround.

## Python and Application Conventions

Target Python 3.13.

Use:

* four-space indentation;
* type annotations for public APIs;
* `snake_case` for functions, variables, and modules;
* `PascalCase` for classes;
* `UPPER_SNAKE_CASE` for constants.

Prefer the smallest coherent change and existing project patterns.

Avoid unrelated refactoring and unnecessary abstractions.

Do not introduce new dependencies when the existing stack already provides the required functionality.

For Telegram HTML messages, escape dynamic values.

Reusable static Russian user-visible text belongs in `src/core/constants.py`.

Do not change database schema implicitly. Schema-impacting changes must be explicit and reflected in HARNESS when completed.

## Build and Validation

Run commands from the repository root.

Install dependencies:

`uv sync`

Start locally:

`.\.venv\Scripts\python.exe src\main.py`

Minimum validation after Python source changes:

`.\.venv\Scripts\python.exe -m compileall src`

Run relevant tests when present:

`uv run pytest`

Focused tests belong under `tests/` and should follow `test_<behavior>.py`.

`test_db.py` is a manual utility, not an automated test suite, and must never contain active credentials.

Do not claim validation succeeded unless the command was actually executed successfully.

Runtime requires valid bot, MSSQL, and Redis configuration. Redis must be available for normal local startup.

`main.spec` contains PyInstaller packaging configuration.

## HARNESS Maintenance

HARNESS describes the current project, not the current conversation.

Normally `scribe` owns HARNESS reconciliation after implementation.

Update only durable knowledge:

* structure/module responsibility change -> `STRUCTURE.md`
* runtime/dependency change -> `STACK.md`
* architectural or project-specific knowledge -> `NOTES.md`
* permanent restriction -> `FORBIDDEN.md`
* meaningful completed change -> `HISTORY.md`

Do not record trivial edits, raw diffs, logs, debugging notes, secrets, or conversation details.

No HARNESS update is required when durable project knowledge did not change.
