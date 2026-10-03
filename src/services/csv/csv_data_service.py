from pathlib import Path
import pandas as pd
from typing import Dict, Optional
from models.trade_entity import InstumentType
from services.csv.csv_data_repository import CsvDataRepository


class CsvDataService:
    def __init__(self, repo: CsvDataRepository):
        self.repo = repo

    def get_last_date(
        self,
        ticker: str,
        interval: str,
        folder: str
    ) -> Optional[str]:
        last = self.repo.get_last_begin_date(ticker, interval, folder)
        if not last:
            return None
        return last.strftime("%Y-%m-%d")

    def get_all_instruments_from_files(
        self,
        base_folder: str = "data"
    ) -> Dict[InstumentType, list[str]]:
        temp: Dict[InstumentType, set[str]] = {}

        base = Path(base_folder)
        if not base.exists():
            return {}

        for instrument_dir in base.iterdir():
            if not instrument_dir.is_dir():
                continue

            try:
                instrument_type = InstumentType[instrument_dir.name.upper()]
            except KeyError:
                continue

            tickers: set[str] = set()

            for file in instrument_dir.glob("*.csv"):
                parts = file.stem.split("_")
                if len(parts) < 2:
                    continue
                tickers.add(parts[0])

            if tickers:
                temp[instrument_type] = tickers

        return {
            instrument_type: list(tickers)
            for instrument_type, tickers in temp.items()
        }


    def append_and_trim(
        self,
        ticker: str,
        interval: str,
        folder: str,
        new_df: pd.DataFrame
    ) -> None:
        if new_df.empty:
            return

        old_df = self.repo.load_all(ticker, interval, folder)

        df = (
            pd.concat([old_df, new_df], ignore_index=True)
            if not old_df.empty else new_df
        )

        df = df.drop_duplicates(subset=["begin"], keep="last")

        self.repo.overwrite(
            df,
            ticker,
            interval,
            folder,
            None
        )
