from typing import Protocol

import pandas as pd


class CsvRepositoryProtocol(Protocol):
    def save(
        self,
        df: pd.DataFrame,
        ticker: str,
        interval: str,
        from_date: str,
        till_date: str,
        folder: str
    ) -> str: ...
