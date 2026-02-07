
from typing import Any
from services.strategies.base_trade_strategy import BaseTradeStrategy


class AnalyzerService:
    def __init__(self, strategies: list[BaseTradeStrategy]) -> None:
        self.strategies = strategies


    def __call__(self) -> Any:
        pass