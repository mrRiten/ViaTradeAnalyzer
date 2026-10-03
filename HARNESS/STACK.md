# Technical Stack

Exact resolved versions below come from `uv.lock`; direct dependency constraints come from `pyproject.toml`.

## Runtime and Dependency Management

- Python 3.13 (`requires-python = ">=3.13"`; `.python-version` selects `3.13`)
- uv with `pyproject.toml` and `uv.lock`

## Direct Runtime Dependencies

- `aiohttp` 3.13.3 — asynchronous MOEX HTTP sessions and requests.
- `APScheduler` 3.11.2 — optional asynchronous scheduling infrastructure; not wired into the current entry point.
- `pandas` 2.3.3 — candle frames, CSV processing, indicators, and signal calculations.
- `pandas-ta` 0.4.71b0 — declared direct dependency, currently unused by source code.
- `requests` 2.32.5 — declared direct dependency, currently unused by source code.

## External Systems and Storage

- MOEX ISS public HTTP API — stock and futures candle source.
- Optional ASP/backend instrument endpoint — implementation is present only as commented code; the active source is hardcoded.
- CSV filesystem storage under `data/` — both market history and generated analysis results.

There is no database, cache/queue service, messaging framework, or executable-packaging configuration in the current project.

## Testing and Packaging

- No automated test framework is declared.
- No `tests/` directory is present.
- No executable-packaging specification is present.

## Maintenance

Update this file when the Python target, a direct architectural dependency, external integration, storage model, or runtime mode changes. Do not copy the full lock file here.
