# Project Notes

## Runtime and Composition

`src/main.py` composes the aiogram bot, Redis message service, middleware, routers, and background workers. Startup starts queued Telegram delivery plus SLA, SLA-delivery, and no-response-required report workers; shutdown stops them and closes bot and Redis sessions.

Normal local startup requires valid bot configuration, MSSQL connectivity, and Redis availability.

## Architecture

Expected application dependency flow:

`Telegram handler -> service -> repository -> database`

Telegram handlers should stay thin.

Services own business rules and orchestration.

Repositories own database access.

DTOs define data exchanged between layers where applicable.

Builders are responsible for presentation formatting.

Keyboards are responsible for Telegram controls.

Workers handle asynchronous/queued delivery where applicable.

`MessageSenderService` is the service-layer boundary for queued Telegram sends. It places `QueueMessage` values on Redis; `TelegramSenderWorker` consumes them, handles retryable Telegram failures, and moves unrecoverable messages to the dead-letter queue.

## User-facing Messages

Telegram messages may use HTML formatting.

Dynamic values inserted into HTML messages must be escaped.

Reusable static Russian display text belongs in:

`src/core/constants.py`

Avoid scattering identical display strings across builders and handlers.

## Employee Search

The `/employ` command uses an FSM prompt to look up an employee by an exact NEON number or by exactly two name parts. `UserQueryService` delegates to `UserRepository`, which returns only records with non-empty first and last names. Name lookups return at most two results so the handler can require a more specific query when a name is ambiguous.

## Database and Proxies

The project uses MSSQL.

Connection configuration is provided through environment configuration.

Repository code should isolate database operations from Telegram-specific code.

Database schema changes must be considered separately from ordinary application-code changes.

Telegram-binding authorization roles are stored in the `tg_binding_roles` catalog and linked to bindings through `tg_binding_role_assignments`. `TgBindingRoleRepository` reads active roles and manages assignment activation/deactivation; role lookups exclude inactive bindings, assignments, and catalog roles.

At session creation, the bot selects the first active proxy from the MSSQL `proxies` table. The session does not rotate proxies at runtime; proxy settings are database-managed rather than read directly from `PROXY_URL`.

## Redis

Redis is runtime infrastructure used by the bot for asynchronous Telegram delivery. The active queue and dead-letter queue are maintained by `RedisMessageService`.

When investigating queued/asynchronous message behavior, inspect the relevant bot worker and Redis integration before changing service logic.

Do not assume every Redis-related issue belongs to the business-service layer.

## SLA and Scheduled Work

`SLAChecker` obtains candidate tasks from the service layer, fetches working-day data from `isdayoff.ru`, caches the requested date range, and sends developer and escalation notifications through the message queue. `SLARepository` assigns each developer an SLA group from active Telegram-binding roles with priority `manager`, then `analyst`, then `developer`. Critical and director escalations select and de-duplicate lead recipients by those groups through `MANAGER_LEAD_IDS`, `ANALYTICS_LEAD_IDS`, and `TECH_LEAD_IDS`. Its schedule is controlled by the SLA settings in `src/config.py`.

The delivery checker reports failed SLA notifications on its configured daily schedule. The no-response-required worker sends its report on the configured weekday and time.

## Tests

There is no `tests/` directory at present. Add focused pytest tests for isolated new business rules where practical. `test_db.py` is a manual utility, not an automated pytest test, and must never contain active credentials.

## Packaging

Windows executable packaging uses:

`main.spec`

Packaging changes should be made only when application entry paths, bundled resources, imports, or packaging requirements change.

Validate normal Python execution before diagnosing PyInstaller-specific behavior.

## Development Principle

Prefer existing project patterns.

Avoid speculative abstractions.

When behavior crosses multiple layers, trace the complete path before editing:

`handler -> service -> repository -> database`

or:

`handler -> service -> builder -> Telegram response`

depending on the task.
