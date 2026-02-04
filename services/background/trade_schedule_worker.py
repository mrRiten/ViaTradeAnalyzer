import asyncio
import pandas as pd
from models.trade_entity import INSTRUMENT_TIMEFRAME, InstumentType
from services.api.trade_api_facade import TradeApiFacade
from intarfaces.iinstrument_source import InstrumentSourceProtocol
from services.trade_service.csv_repository import CsvRepository


class TradeScheduleWorker:
    def __init__(self, facade: TradeApiFacade, repo: CsvRepository, source: InstrumentSourceProtocol):
        self.facade = facade
        self.repo = repo
        self.source = source
        self._semaphore = asyncio.Semaphore(5)  # max 5 parallel requests

    async def _process_ticker(self, instrument_type: InstumentType, ticker: str, timeframe):
        async with self._semaphore:
            df: pd.DataFrame = await self.facade.get_candles(
                instrument_type, ticker, timeframe, None, None
            )
            if df.empty:
                return
            print(f"saving {ticker}")

            self.repo.save(
                df,
                ticker,
                timeframe.name,
                df.begin.min().strftime("%Y-%m-%d"),
                df.begin.max().strftime("%Y-%m-%d"),
                f"data/{instrument_type.name.lower()}"
            )

    async def __call__(self):
        instruments = await self.source.get_instruments()

        tasks = []
        for instrument_type, tickers in instruments.items():
            timeframe = INSTRUMENT_TIMEFRAME[instrument_type]
            for ticker in tickers:
                tasks.append(self._process_ticker(instrument_type, ticker, timeframe))

        await asyncio.gather(*tasks)
