
from pandas import DataFrame
from intarfaces.itrade_screnner import ITradeScrenner


class DeepEmaRsiScrenner(ITradeScrenner):
    def screnne(self, trade_data: DataFrame) -> DataFrame:
        df = trade_data.copy()

        df["EMA_20"] = df["close"].ewm(span=20, adjust=False).mean()
        df["EMA_50"] = df["close"].ewm(span=50, adjust=False).mean()
        df["EMA_200"] = df["close"].ewm(span=200, adjust=False).mean()

        delta = df["close"].diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()

        rs = avg_gain / avg_loss
        df["RSI_14"] = 100 - (100 / (1 + rs))

        return df[["EMA_20", "EMA_50", "EMA_200", "RSI_14"]]