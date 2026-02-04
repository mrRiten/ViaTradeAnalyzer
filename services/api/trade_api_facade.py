from typing import Dict, Optional
from intarfaces.iexchange_client import IExchangeClient
from services.api.http_client_service import HttpClientService
from services.moex.futures_service import FuturesClient
from services.moex.stocks_service import StocksClient
from models.trade_entity import InstumentType, TimeFrame


class TradeApiFacade:
    def __init__(self, clients: dict[InstumentType, IExchangeClient]):
        self.clients = clients

    async def get_all(self, instrument_type: InstumentType) -> list[str]:
        return await self.clients[instrument_type].get_all_instruments()

    async def get_candles(
        self,
        instrument_type: InstumentType,
        ticker: str,
        interval: TimeFrame,
        from_date: Optional[str],
        till_date: Optional[str]
    ):
        return await self.clients[instrument_type].get_candles(ticker, interval, from_date, till_date)
