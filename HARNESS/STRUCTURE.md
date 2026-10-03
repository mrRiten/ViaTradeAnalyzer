# Repository Structure

## Root

- `src/main.py` — application composition, router registration, lifecycle hooks, and background-worker startup.
- `src/config.py` — Pydantic settings loaded from environment configuration.
- `src/proxy_module.py` — Telegram session creation and active-proxy lookup from MSSQL.
- `src/logging_config.py` — application logging setup.
- `pyproject.toml` and `uv.lock` — dependency declarations and resolved versions.
- `main.spec` — PyInstaller packaging configuration.
- `test_db.py` — manual database/bot utility; it is not an automated test.

## Application Source

- `src/bot/handlers/` — aiogram routers for commands, menu actions, tickets, attendance, SLA, employee search, and help.
- `src/bot/builders/` — Telegram message formatting only.
- `src/bot/keyboards/` — inline and reply keyboard construction.
- `src/bot/middlewares/` — Telegram-user binding and access checks.
- `src/bot/commands/` — Telegram command registration.
- `src/bot/redis/` — Redis client, queue message model, and queue operations.
- `src/bot/workers/` — asynchronous queued Telegram delivery and sender configuration.

- `src/application/services/` — business operations for tickets, attendance, bot start, SLA, and no-response-required records.
- `src/application/repositories/` — synchronous SQLAlchemy access to HelpDesk tables, including Telegram-binding role catalog and assignment access.
- `src/application/jobs/` — scheduled SLA, SLA-delivery, and no-response-required report checks.
- `src/application/client/` — external calendar client used by SLA checks.
- `src/application/utils/sla/` — working-hours calculation.

- `src/core/db/` — SQLAlchemy Core table definitions for existing MSSQL tables, including Telegram-binding roles and assignments.
- `src/core/dto/` — dataclasses used between repositories, services, and builders, including role catalog values.
- `src/core/constants.py` — reusable static display text and formats.
