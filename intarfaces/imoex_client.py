from typing import Protocol

import aiohttp
import pandas as pd

from models.trade_entity import TimeFrame


class MoexClient(Protocol):
    async def get_all_instruments(
        self,
        session: aiohttp.ClientSession
    ) -> list[str]: ...

    async def get_candles(
        self,
        session: aiohttp.ClientSession,
        ticker: str,
        interval: TimeFrame,
        from_date: str | None,
        till_date: str | None,
    ) -> pd.DataFrame: ...