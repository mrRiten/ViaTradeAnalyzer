import asyncio
import aiohttp
import pandas as pd
from datetime import datetime, timedelta, date
from typing import Optional, Dict, Any, List, Protocol
import logging

from intarfaces.iexchange_client import IExchangeClient
from models.trade_entity import JsonRow, MoexResponse, TimeFrame

logger = logging.getLogger(__name__)



class BaseMoexClient(IExchangeClient):
    MAX_RECORDS: int = 500
    RETRY_COUNT: int = 3
    RETRY_DELAY: int = 2

    def __init__(self, base_url: str, session_factory):
        self.base_url: str = base_url
        self._session_factory = session_factory

    async def _get(
        self,
        session: aiohttp.ClientSession,
        url: str,
        params: Optional[Dict[str, str]] = None
    ) -> MoexResponse:
        print(f"start {url}")
        for attempt in range(1, self.RETRY_COUNT + 1):
            try:
                async with session.get(url, params=params) as resp:
                    print(f"get {url} att {attempt}")
                    resp.raise_for_status()
                    res = await resp.json()
                    return res
            except (aiohttp.ClientError, asyncio.TimeoutError):
                if attempt == self.RETRY_COUNT:
                    print(f"Request failed: {url}")
                    logger.error("Request failed: %s", url)
                    return {}
                await asyncio.sleep(self.RETRY_DELAY)
        return {}

    async def get_all_instruments(self) -> List[str]:
        async with self._session_factory() as session:
            data: MoexResponse = await self._get(session, f"{self.base_url}.json")

            table = data.get("securities")
            if not table:
                return []

            columns: List[str] = table["columns"]
            rows: List[JsonRow] = table["data"]

            if "SECID" not in columns:
                return []

            idx: int = columns.index("SECID")
            return [str(row[idx]) for row in rows if row[idx] is not None]

    async def _load_candles_raw(
        self,
        session: aiohttp.ClientSession,
        ticker: str,
        interval: TimeFrame,
        start: date,
        end: date,
    ) -> pd.DataFrame:
        params: Dict[str, str] = {
            "from": start.strftime("%Y-%m-%d"),
            "till": end.strftime("%Y-%m-%d"),
            "interval": str(interval.value),
        }

        data: MoexResponse = await self._get(
            session,
            f"{self.base_url}/{ticker}/candles.json",
            params
        )

        table = data.get("candles")
        if not table:
            return pd.DataFrame()

        columns: List[str] = table["columns"]
        rows: List[JsonRow] = table["data"]

        if not rows:
            return pd.DataFrame()

        df = pd.DataFrame([{columns[i]: row[i] for i in range(len(columns))} for row in rows])

        if "begin" in df.columns:
            df["begin"] = pd.to_datetime(df["begin"])
        if "end" in df.columns:
            df["end"] = pd.to_datetime(df["end"])

        return df[["begin", "open", "close", "high", "low", "volume"]]


    async def get_candles(
        self,
        ticker: str,
        interval: TimeFrame,
        from_date: Optional[str] = None,
        till_date: Optional[str] = None,
    ) -> pd.DataFrame:
        async with self._session_factory() as session:
            till = datetime.strptime(till_date, "%Y-%m-%d").date() if till_date else datetime.now().date()
            start = datetime.strptime(from_date, "%Y-%m-%d").date() if from_date else (till - timedelta(days=180))

            frames = []
            cur_start = start

            while cur_start <= till:
                cur_end = min(cur_start + timedelta(days=self.MAX_RECORDS - 1), till)
                df = await self._load_candles_raw(session, ticker, interval, cur_start, cur_end)

                if df.empty:
                    cur_start = cur_end + timedelta(days=1)
                    continue

                frames.append(df)
                last_date = df['begin'].max().date()
                if last_date >= till:
                    break

                cur_start = last_date + timedelta(seconds=1)

            if not frames:
                return pd.DataFrame(columns=["begin", "open", "close", "high", "low", "volume"])

            df = pd.concat(frames, ignore_index=True)
            df = df.drop_duplicates(subset=["begin"], keep="last").sort_values("begin").reset_index(drop=True)

            return df

