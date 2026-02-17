
from abc import ABC, abstractmethod

import pandas as pd

from intarfaces.itrade_screnner import ITradeScrenner
from models.trade_entity import TimeFrame
from services.csv.csv_data_repository import CsvDataRepository


class BaseTradeStrategy(ABC):
    def __init__(self, screnners: list[ITradeScrenner], data_repository: CsvDataRepository) -> None:
        self.screnners = screnners
        self.data_repository = data_repository
    
    @abstractmethod
    def process(self, ticker: str, interval: TimeFrame, folder: str) -> pd.DataFrame:
        ...
