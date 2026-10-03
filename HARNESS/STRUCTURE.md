# Repository Structure

## Root

- `src/main.py` — application entry point and one-shot composition of market-data loading and analysis.
- `pyproject.toml` — project metadata, Python constraint, and direct dependencies.
- `uv.lock` — resolved dependency versions.
- `.python-version` — local Python version selection.
- `README.md` — currently empty; do not rely on it for architecture.
- `data/` — tracked runtime CSV inputs and generated analysis outputs.

There is currently no automated `tests/` suite and no packaging specification.

## Application Source

- `src/models/system.py` — typed shape of an instruments response.
- `src/models/trade_entity.py` — candle, signal, instrument-type, timeframe, and MOEX response models.
- `src/models/exceptions.py` — project exception definitions.

- `src/intarfaces/` — protocols and abstract interfaces for instrument sources, exchange clients, CSV repositories, background tasks, and screeners. The directory name is intentionally documented with its current spelling.

- `src/services/api/http_client_service.py` — configured `aiohttp.ClientSession` factory.
- `src/services/api/asp_instrument_service.py` — instrument source; currently returns a hardcoded stock list while the HTTP implementation is commented out.
- `src/services/api/asp_notify_service.py` — notification stub with no implemented delivery.

- `src/services/moex/base_moex_client.py` — shared MOEX ISS candle pagination, retries, normalization, and record limits.
- `src/services/moex/stocks_service.py` — MOEX shares-market client.
- `src/services/moex/futures_service.py` — MOEX FORTS futures-market client.

- `src/services/background/exchange_client_manager.py` — maps instrument types to exchange clients.
- `src/services/background/trade_schedule_worker.py` — obtains instruments, loads candles concurrently, and updates CSV storage.
- `src/services/background/background_service.py` — APScheduler-compatible wrapper for an asynchronous task.
- `src/services/background/service_manager.py` — scheduler and registered-service coordinator; not used by the current entry point.

- `src/services/csv/csv_data_repository.py` — locates, reads, overwrites, and trims candle/result CSV files.
- `src/services/csv/csv_data_service.py` — CSV update orchestration and instrument discovery from stored files.
- `src/services/csv/csv_result_repository.py` — empty placeholder.
- `src/services/csv/csv_result_service.py` — empty placeholder.

- `src/services/strategies/analyzer_service.py` — runs configured strategies for instruments found in CSV storage.
- `src/services/strategies/base_trade_strategy.py` — strategy abstraction.
- `src/services/strategies/trend_following_strategy.py` — EMA/RSI trend and crossing signals.
- `src/services/strategies/rsi_strategy.py` — RSI overbought/oversold signals.
- `src/services/strategies/Screnners/deep_ema_rsi_screnner.py` — EMA 20/50/200 and RSI 14 calculation. The current directory and class/method spellings are part of the existing code.

## Data Layout

- `data/stocks/` — stock candle CSV files.
- `data/futures/` — futures candle CSV files.
- `data/result/screnner/` — indicator-enriched strategy inputs.
- `data/result/strategy/` — final strategy signal CSV files.

Treat files under `data/` as runtime/generated artifacts even though they are currently tracked.
