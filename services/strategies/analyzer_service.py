
from typing import Any, Dict
from models.trade_entity import INSTRUMENT_TIMEFRAME, InstumentType
from services.csv.csv_data_service import CsvDataService
from services.strategies.base_trade_strategy import BaseTradeStrategy


class AnalyzerService:
    def __init__(
        self,
        strategies: list[BaseTradeStrategy],
        data_service: CsvDataService
    ):
        self.strategies = strategies
        self.data_service = data_service


    def __call__(self) -> None:
        instruments: Dict[InstumentType, list[str]] = (
            self.data_service.get_all_instruments_from_files()
        )

        for instrument_type, tickers in instruments.items():
            interval = INSTRUMENT_TIMEFRAME[instrument_type]
            folder = f"data/{instrument_type.name.lower()}"

            for ticker in tickers:
                for strategy in self.strategies:
                    print(f"process {ticker} - {strategy.__class__.__name__}")
                    strategy.process(
                        ticker=ticker,
                        interval=interval,
                        folder=folder
                    )
        
        
