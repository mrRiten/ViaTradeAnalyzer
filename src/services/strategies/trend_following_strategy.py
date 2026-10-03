from pandas.core.api import DataFrame as DataFrame
import pandas as pd
from intarfaces.itrade_screnner import ITradeScrenner
from models.trade_entity import TimeFrame
from services.csv.csv_data_repository import CsvDataRepository
from services.strategies.base_trade_strategy import BaseTradeStrategy


class TrendFollowingStrategy(BaseTradeStrategy):
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

        # Индикаторы от скриннера
        indicators = self.screnners[0].screnne(trade_data)
        screnner_df = pd.concat([trade_data, indicators], axis=1)
        screnner_df.columns = [c.lower() for c in screnner_df.columns]

        # Результаты скриннера
        screnner_folder = "data/result/screnner"
        self.data_repository.overwrite(
            screnner_df,
            ticker,
            interval.name,
            screnner_folder,
            __class__.__name__
        )

        # Индикаторы
        ema20 = screnner_df["ema_20"]
        ema50 = screnner_df["ema_50"]
        ema200 = screnner_df["ema_200"]
        rsi = screnner_df["rsi_14"]
        close = screnner_df["close"]

        # Направление EMA
        ema20_up = (ema20.diff() > 0).fillna(False)
        ema50_up = (ema50.diff() > 0).fillna(False)
        ema20_down = (ema20.diff() < 0).fillna(False)
        ema50_down = (ema50.diff() < 0).fillna(False)

        # Классическое пересечение EMA20/50
        cross_up = ((ema20.shift(1) <= ema50.shift(1)) & (ema20 > ema50)).fillna(False)
        cross_down = ((ema20.shift(1) >= ema50.shift(1)) & (ema20 < ema50)).fillna(False)

        buy_base = (
            cross_up
            & (close > ema200)
            & ema20_up
            & ema50_up
            & (rsi > 50)
        )

        sell_base = (
            cross_down
            & (close < ema200)
            & ema20_down
            & ema50_down
            & (rsi < 50)
        )

        # Пересечение свечи с EMA200
        close_prev = close.shift(1)
        cross_ema200_up = ((close_prev < ema200) & (close > ema200)).fillna(False)
        cross_ema200_down = ((close_prev > ema200) & (close < ema200)).fillna(False)

        buy_cross = (
            cross_ema200_up
            & ema20_up
            & ema50_up
            & (rsi > 50)
        )

        sell_cross = (
            cross_ema200_down
            & ema20_down
            & ema50_down
            & (rsi < 50)
        )

        # Финальные сигналы с проверкой пересечений
        buy_final = buy_base | buy_cross
        sell_final = sell_base | sell_cross

        # Обнуляем сигналы на первой строке, чтобы не было ложных сигналов
        buy_final.iloc[0] = False
        sell_final.iloc[0] = False

        # Формируем DataFrame стратегии
        strategy_df = screnner_df[["begin", "close"]].copy()
        strategy_df["signal"] = "Hold"
        strategy_df.loc[buy_final, "signal"] = "Buy"
        strategy_df.loc[sell_final, "signal"] = "Sell"

        # Сохраняем минималистично для стратегии
        strategy_folder = "data/result/strategy"
        test: str = __class__.__name__
        self.data_repository.overwrite(
            strategy_df,
            ticker,
            interval.name,
            strategy_folder,
            test
        )

        return strategy_df
