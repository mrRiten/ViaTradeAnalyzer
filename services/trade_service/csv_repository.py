from pathlib import Path
import pandas as pd


class CsvRepository:
    def save(
        self,
        df: pd.DataFrame,
        ticker: str,
        interval: str,
        from_date: str,
        till_date: str,
        folder: str
    ) -> str:
        path_dir = Path(folder)
        path_dir.mkdir(parents=True, exist_ok=True)

        path = path_dir / f"{ticker}_{interval}_{from_date}_{till_date}.csv"
        df.to_csv(path, index=False)
        return str(path)
