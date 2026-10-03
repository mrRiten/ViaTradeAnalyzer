from typing import Dict
from intarfaces.iinstrument_source import InstrumentSourceProtocol
from models.trade_entity import InstumentType, TimeFrame
from intarfaces.iexchange_client import IExchangeClient
from services.api.asp_instrument_service import AspInstrumentSource
from services.moex.futures_service import FuturesClient
from services.moex.stocks_service import StocksClient


class ExchangeClientManager:
    """
    Manager clietns for STOCKS and FUTURES.
    Constains data InstumentType -> IExchangeClient
    """

    def __init__(self, session_factory):
        self._clients: Dict[InstumentType, IExchangeClient] = {
            InstumentType.STOCKS: StocksClient(session_factory),
            InstumentType.FUTURES: FuturesClient(session_factory),
        }

    def get_client(self, instrument_type: InstumentType) -> IExchangeClient:
        return self._clients[instrument_type]

    async def get_all_instruments_from_db(self, source: InstrumentSourceProtocol) -> Dict[InstumentType, list[str]]:
        """
        Get list of actual in instruments from Db by http to backend service
        """
        return await source.get_instruments()
