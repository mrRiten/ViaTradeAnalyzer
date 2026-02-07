
from abc import ABC, abstractmethod

import pandas as pd

from intarfaces.itrade_screnner import ITradeScrenner


class BaseTradeStrategy(ABC):
    def __init__(self, screnners: list[ITradeScrenner]) -> None:
        self.screnners = screnners
    
    @abstractmethod
    def process(self, ticker: str):
        ...
