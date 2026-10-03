from pandas.core.api import DataFrame as DataFrame
import pandas as pd
from intarfaces.itrade_screnner import ITradeScrenner
from models.trade_entity import TimeFrame
from services.csv.csv_data_repository import CsvDataRepository
from services.strategies.base_trade_strategy import BaseTradeStrategy


class RsiStrategy(BaseTradeStrategy):
    def __init__(
        self,
        screnners: list[ITradeScrenner],
        data_repository: CsvDataRepository
    ) -> None:
        super().__init__(screnners, data_repository)

    def process(self, ticker: str, interval: TimeFrame, folder: str) -> DataFrame:
        trade_data = self.data_repository.load_by_ticker(
            ticker,
            interval.name,
            folder
        )

        if trade_data.empty:
            return trade_data

        # Get indicators from screener
        indicators = self.screnners[0].screnne(trade_data)
        screnner_df = pd.concat([trade_data, indicators], axis=1)
        screnner_df.columns = [c.lower() for c in screnner_df.columns]

        # Save screener results
        screnner_folder = "data/result/screnner"
        self.data_repository.overwrite(
            screnner_df,
            ticker,
            interval.name,
            screnner_folder,
            __class__.__name__
        )

        # Extract RSI indicator
        rsi = screnner_df["rsi_14"]

        # Simple RSI levels
        # Buy when RSI < 30 (oversold zone)
        # Sell when RSI > 70 (overbought zone)
        buy_signal = rsi < 30
        sell_signal = rsi > 70

        # Handle NaN values
        buy_signal = buy_signal.fillna(False)
        sell_signal = sell_signal.fillna(False)

        # Form strategy DataFrame
        strategy_df = screnner_df[["begin", "close"]].copy()
        strategy_df["signal"] = "Hold"
        strategy_df.loc[buy_signal, "signal"] = "Buy"
        strategy_df.loc[sell_signal, "signal"] = "Sell"

        # Save strategy results
        strategy_folder = "data/result/strategy"
        self.data_repository.overwrite(
            strategy_df,
            ticker,
            interval.name,
            strategy_folder,
            __class__.__name__
        )

        return strategy_df