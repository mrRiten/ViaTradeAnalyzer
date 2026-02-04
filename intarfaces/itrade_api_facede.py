from typing import Protocol

import pandas as pd

from models.trade_entity import TimeFrame


class TradeApiFacadeProtocol(Protocol):
    async def get_all(self, instrument_type: str) -> list[str]: ...
    async def get_candles(
        self,
        instrument: str,
        ticker: str,
        interval: TimeFrame,
        from_date: str | None,
        till_date: str | None
    ) -> pd.DataFrame: ...
