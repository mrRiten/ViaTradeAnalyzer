
from abc import ABC, abstractmethod

import pandas as pd


class ITradeScrenner(ABC):
    @abstractmethod
    def screnne(self, trade_data: pd.DataFrame) -> pd.DataFrame:
        ...