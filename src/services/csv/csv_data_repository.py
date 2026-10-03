from pathlib import Path
from datetime import datetime
import pandas as pd
from typing import Optional


class CsvDataRepository:
    MAX_ROWS = 800

    def _find_file(self, ticker: str, interval: str, folder: str, addtional_target: str = "") -> Optional[Path]:
        path_dir = Path(folder)
        if not path_dir.exists():
            return None

        files = list(path_dir.glob(f"{ticker}_{interval}_{addtional_target}*.csv"))
        if not files:
            return None

        return max(files, key=lambda p: p.stem.split("_")[-1])

    def get_last_begin_date(
        self,
        ticker: str,
        interval: str,
        folder: str
    ) -> Optional[datetime]:
        path = self._find_file(ticker, interval, folder)
        if not path:
            return None

        with path.open("rb") as file:
            file.seek(0, 2)
            pos = file.tell() - 1

            while pos > 0:
                file.seek(pos)
                if file.read(1) == b"\n":
                    break
                pos -= 1

            line = file.readline().decode().strip()

        if not line:
            return None

        return datetime.fromisoformat(line.split(",")[0])

    def load_by_ticker(
        self,
        ticker: str,
        interval: str,
        folder: str
    ) -> pd.DataFrame:
        path = self._find_file(ticker, interval, folder)
        if not path:
            return pd.DataFrame()

        df = pd.read_csv(path)
        if "begin" in df.columns:
            df["begin"] = pd.to_datetime(df["begin"])
        return df


    def load_all(
        self,
        ticker: str,
        interval: str,
        folder: str
    ) -> pd.DataFrame:
        path = self._find_file(ticker, interval, folder)
        if not path:
            return pd.DataFrame()

        df = pd.read_csv(path)
        df["begin"] = pd.to_datetime(df["begin"])
        return df

    def overwrite(
        self,
        df: pd.DataFrame,
        ticker: str,
        interval: str,
        folder: str,
        additional: str | None,
    ) -> None:
        if not additional:
            additional = ""

        df = df.sort_values("begin").tail(self.MAX_ROWS)

        from_date = df.begin.min().strftime("%Y-%m-%d")
        till_date = df.begin.max().strftime("%Y-%m-%d")

        path_dir = Path(folder)
        path_dir.mkdir(parents=True, exist_ok=True)

        # Удаляем только файлы текущей стратегии
        for f in path_dir.glob(f"{ticker}_{interval}_*.csv"):
            if additional:
                # Удаляем только файлы с таким же additional
                if f.name.endswith(f"_{additional}.csv"):
                    f.unlink()
            else:
                # Удаляем только файлы без additional (ровно 4 части: ticker, interval, from, till)
                parts = f.stem.split("_")
                if len(parts) == 4:
                    f.unlink()

        path = path_dir / f"{ticker}_{interval}_{from_date}_{till_date}_{additional}.csv"

        print(f"save to {path}")

        df.to_csv(path, index=False)
