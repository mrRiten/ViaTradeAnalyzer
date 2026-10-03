from abc import ABC, abstractmethod
from typing import List, Optional
import pandas as pd
from datetime import date
from models.trade_entity import TimeFrame

class IExchangeClient(ABC):
    @abstractmethod
    async def get_candles(
        self, 
        ticker: str, 
        interval: TimeFrame, 
        till_date: str | None
    ) -> pd.DataFrame:
        ...
