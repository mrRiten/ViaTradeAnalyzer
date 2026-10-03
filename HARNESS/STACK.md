# Technical Stack

This file describes important runtime and development dependencies.

Exact versions must be synchronized with `pyproject.toml` and `uv.lock`.

Do not guess versions.

## Runtime

- Language: Python
- Target version: Python 3.13

## Dependency Management

- Package/project manager: uv
- Direct dependency configuration: `pyproject.toml`
- Resolved dependency versions: `uv.lock`

`uv.lock` is authoritative for resolved package versions.

## Telegram

- Telegram bot framework: aiogram 3.31.0
- Proxy session: aiogram aiohttp session with database-selected proxies

## Database

- Database: Microsoft SQL Server
- ORM/database layer: SQLAlchemy 2.0.52
- ODBC driver: pyodbc 5.3.0
- Connection configuration: `MSSQL_CONNECTION_STRING`

## Cache / Queue

- Infrastructure: Redis
- Redis client/library: redis-py 8.1.0 (`redis.asyncio`)

## Packaging

- Packaging tool: PyInstaller 6.22.2
- Configuration: `main.spec`

## Testing

- Automated test framework: not declared in project dependencies

## Important Dependencies

Maintain only dependencies that affect architecture or development decisions.

Format:

| Dependency | Version | Purpose |
|---|---|---|
| Python | 3.13 | Runtime |
| aiogram | 3.31.0 | Telegram Bot API integration |
| SQLAlchemy | 2.0.52 | ORM and database access |
| pyodbc | 5.3.0 | MSSQL ODBC connectivity |
| redis | 8.1.0 | Asynchronous Redis queue integration |
| pydantic-settings | 2.15.0 | Environment-based settings |
| aiohttp-socks | 0.12.0 | SOCKS proxy support |
| PyInstaller | 6.22.2 | Windows executable packaging |

Do not copy the complete dependency lock into this file.

## Maintenance

Update this file when:

- Python target changes;
- an architectural dependency is added or removed;
- a major dependency version changes;
- database/cache infrastructure changes;
- packaging tooling changes.

Patch-level transitive dependency changes do not require a HISTORY entry unless they affect application behavior.
