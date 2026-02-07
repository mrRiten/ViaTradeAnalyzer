import asyncio
import pandas as pd
from datetime import timedelta
from typing import Dict
from models.trade_entity import InstumentType, INSTRUMENT_TIMEFRAME
from intarfaces.iinstrument_source import InstrumentSourceProtocol
from services.background.exchange_client_manager import ExchangeClientManager
from services.csv.csv_data_service import CsvDataService


class TradeScheduleWorker:
    def __init__(
        self,
        csv_service: CsvDataService,
        source: InstrumentSourceProtocol,
        client_manager: ExchangeClientManager,
        max_parallel: int = 5
    ):
        self.csv_service = csv_service
        self.source = source
        self.client_manager = client_manager
        self._semaphore = asyncio.Semaphore(max_parallel)

    async def _process(
        self,
        instrument_type: InstumentType,
        ticker: str,
        timeframe
    ):
        async with self._semaphore:
            folder = f"data/{instrument_type.name.lower()}"
            client = self.client_manager.get_client(instrument_type)

            last_date = self.csv_service.get_last_date(
                ticker,
                timeframe.name,
                folder
            )

            from_date = (
                (pd.to_datetime(last_date) + timedelta(days=1)).strftime("%Y-%m-%d")
                if last_date else None
            )

            new_df = await client.get_candles(
                ticker,
                timeframe,
                from_date
            )

            self.csv_service.append_and_trim(
                ticker,
                timeframe.name,
                folder,
                new_df
            )

    async def _get_instruments(self) -> Dict[InstumentType, list[str]]:
        try:
            instruments = await self.client_manager.get_all_instruments_from_db(self.source)
            if instruments:
                return instruments
        except Exception:
            pass

        return self.csv_service.get_all_instruments_from_files()

    async def __call__(self):
        instruments = await self._get_instruments()

        tasks = []
        for instrument_type, tickers in instruments.items():
            timeframe = INSTRUMENT_TIMEFRAME[instrument_type]
            for ticker in tickers:
                tasks.append(
                    self._process(instrument_type, ticker, timeframe)
                )

        await asyncio.gather(*tasks)
