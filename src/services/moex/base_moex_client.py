import asyncio
import aiohttp
import pandas as pd
from datetime import datetime, timedelta, date
from math import ceil
from typing import Optional, Dict
import logging

from intarfaces.iexchange_client import IExchangeClient
from models.trade_entity import MoexResponse, TimeFrame

logger = logging.getLogger(__name__)


class BaseMoexClient(IExchangeClient):
    MAX_REQUEST_RECORDS = 500
    MAX_TOTAL_RECORDS = 1000

    RETRY_COUNT = 3
    RETRY_DELAY = 2

    CANDLES_PER_DAY = {
        TimeFrame.HOUR_1: 16,
        TimeFrame.DAY: 1,
    }

    def __init__(self, base_url: str, session_factory):
        self.base_url = base_url
        self._session_factory = session_factory

    async def get_candles(
        self,
        ticker: str,
        interval: TimeFrame,
        till_date: Optional[str]
    ) -> pd.DataFrame:
        async with self._session_factory() as session:
            till = self._resolve_till_date(till_date)
            date_limit = self._calculate_date_limit(till, interval)
            days_per_request = self._calculate_days_per_request(interval)

            frames = await self._collect_frames(
                session,
                ticker,
                interval,
                till,
                date_limit,
                days_per_request
            )

            return self._merge_and_trim(frames)

    def _resolve_till_date(self, till_date: Optional[str]) -> date:
        return (
            datetime.strptime(till_date, "%Y-%m-%d").date()
            if till_date
            else datetime.now().date()
        )

    def _calculate_date_limit(self, till: date, interval: TimeFrame) -> date:
        per_day = self.CANDLES_PER_DAY.get(interval)
        if not per_day:
            raise ValueError("Unsupported timeframe")
        days = ceil(self.MAX_TOTAL_RECORDS / per_day)
        return till - timedelta(days=days)

    def _calculate_days_per_request(self, interval: TimeFrame) -> int:
        per_day = self.CANDLES_PER_DAY[interval]
        return max(1, self.MAX_REQUEST_RECORDS // per_day)

    async def _collect_frames(
        self,
        session: aiohttp.ClientSession,
        ticker: str,
        interval: TimeFrame,
        till: date,
        date_limit: date,
        days_per_request: int
    ) -> list[pd.DataFrame]:
        frames = []
        cur_end = till

        while self._can_continue(frames):
            cur_start = max(cur_end - timedelta(days=days_per_request), date_limit)

            df = await self._load_candles_raw(
                session,
                ticker,
                interval,
                cur_start,
                cur_end
            )

            if df.empty:
                break

            frames.append(df)

            earliest = df["begin"].min().date()
            if earliest <= date_limit:
                break

            cur_end = earliest - timedelta(days=1)

        return frames

    def _can_continue(self, frames: list[pd.DataFrame]) -> bool:
        if not frames:
            return True
        return sum(len(f) for f in frames) < self.MAX_TOTAL_RECORDS

    async def _load_candles_raw(
        self,
        session: aiohttp.ClientSession,
        ticker: str,
        interval: TimeFrame,
        start: date,
        end: date,
    ) -> pd.DataFrame:
        params = {
            "from": start.strftime("%Y-%m-%d"),
            "till": end.strftime("%Y-%m-%d"),
            "interval": str(interval.value),
        }

        data = await self._get(
            session,
            f"{self.base_url}/{ticker}/candles.json",
            params
        )

        table = data.get("candles")
        if not table or not table.get("data"):
            return pd.DataFrame()

        df = pd.DataFrame(
            [{table["columns"][i]: row[i] for i in range(len(table["columns"]))}
             for row in table["data"]]
        )

        df["begin"] = pd.to_datetime(df["begin"])
        df["end"] = pd.to_datetime(df["end"])

        return df[["begin", "open", "close", "high", "low", "volume"]]

    async def _get(
        self,
        session: aiohttp.ClientSession,
        url: str,
        params: Optional[Dict[str, str]] = None
    ) -> MoexResponse:
        for attempt in range(self.RETRY_COUNT):
            try:
                async with session.get(url, params=params) as resp:
                    resp.raise_for_status()
                    return await resp.json()
            except (aiohttp.ClientError, asyncio.TimeoutError):
                if attempt + 1 == self.RETRY_COUNT:
                    logger.error("Request failed: %s", url)
                    return {}
                await asyncio.sleep(self.RETRY_DELAY)

        return {}

    def _merge_and_trim(self, frames: list[pd.DataFrame]) -> pd.DataFrame:
        if not frames:
            return pd.DataFrame(columns=["begin", "open", "close", "high", "low", "volume"])

        df = pd.concat(frames, ignore_index=True)
        df = df.drop_duplicates(subset=["begin"], keep="last")
        df = df.sort_values("begin", ascending=False)
        df = df.head(self.MAX_TOTAL_RECORDS)
        df = df.sort_values("begin").reset_index(drop=True)

        return df
