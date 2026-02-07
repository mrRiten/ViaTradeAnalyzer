
from abc import ABC, abstractmethod

import pandas as pd


class ITradeScrenner(ABC):
    @abstractmethod
    def screnne(self, ticker: str) -> pd.DataFrame:
        ...