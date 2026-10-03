# Project Notes

## Runtime Flow

`src/main.py` builds an HTTP session factory, instrument source, exchange-client manager, CSV repository/service, and `TradeScheduleWorker`. After candle synchronization finishes, it constructs `DeepEmaRsiScrenner`, `TrendFollowingStrategy`, and `RsiStrategy`, then runs `AnalyzerService`.

The current entry point is a one-shot `asyncio.run` pipeline. `BackgroundService` and `ServiceManager` provide APScheduler integration but are not wired into `main.py`.

Running the entry point has external and filesystem side effects: it calls MOEX over HTTP and may replace tracked CSV files in `data/`.

## Instrument and Candle Loading

`AspInstrumentSource` currently returns a hardcoded list of stocks. Its backend HTTP implementation is commented out. Futures are supported by the models and exchange-client manager, but the active source does not return them.

If the instrument source fails or returns no data, `TradeScheduleWorker` reconstructs instrument lists from CSV filenames under `data/stocks/` and `data/futures/`.

The worker selects a client by `InstumentType`, limits concurrent ticker processing with a semaphore, and uses these fixed mappings:

- stocks -> `TimeFrame.DAY` with MOEX interval `24`;
- futures -> `TimeFrame.HOUR_1` with MOEX interval `60`.

`StocksClient` uses the MOEX shares endpoint. `FuturesClient` uses the MOEX FORTS endpoint.

`BaseMoexClient` returns at most 1,000 normalized candles, sizes each date window for a nominal maximum of 500 candles, and retries failed HTTP calls three times. `CsvDataRepository` retains the latest 800 rows when writing.

## Analysis and Output

`AnalyzerService` discovers instruments from stored CSV files and runs every configured strategy for each ticker.

`DeepEmaRsiScrenner` calculates EMA 20, EMA 50, EMA 200, and RSI 14. `TrendFollowingStrategy` combines EMA crossings, EMA direction, price relative to EMA 200, and RSI. `RsiStrategy` emits Buy below RSI 30 and Sell above RSI 70.

Indicator-enriched frames are written to `data/result/screnner/`; signal frames are written to `data/result/strategy/`. The strategy class name is used as the result identifier.

`AspNotifyService`, `csv_result_repository.py`, and `csv_result_service.py` are placeholders and currently contain no functional result-delivery path.

## Known Risks

- `TradeScheduleWorker` computes the stored last date plus one day and passes it as the third `get_candles` argument. `BaseMoexClient` interprets that argument as the upper `till` date, so incremental updates may query the wrong date range.
- Base candle writes currently produce filenames with a trailing underscore before `.csv`, while cleanup without an additional identifier deletes only names whose stem has exactly four underscore-separated parts. Older files can remain alongside new ones.
- `_find_file` chooses a match by the final underscore-separated stem token. For trailing-underscore base filenames that token is empty, so selection of the newest dated file is unreliable.
- Runtime CSV artifacts are tracked in Git, making ordinary pipeline runs capable of producing large working-tree changes.

These are documented implementation risks, not instructions to modify data files. Verify and fix source logic in a dedicated task.

## Naming Compatibility

The current code uses the spellings `intarfaces`, `Screnners`, `screnne`, and `InstumentType`. Preserve them in focused changes unless a coordinated rename is explicitly requested.

## Testing

There is currently no `tests/` directory or declared test framework. Add focused tests under `tests/` when changing isolated behavior where practical.
