import asyncio
from services.api.http_client_service import HttpClientService
from services.api.trade_api_facade import TradeApiFacade
from services.api.asp_instrument_service import AspInstrumentSource
from services.background.trade_schedule_worker import TradeScheduleWorker
from services.trade_service.csv_repository import CsvRepository
from services.moex.futures_service import FuturesClient
from services.moex.stocks_service import StocksClient
from models.trade_entity import InstumentType

async def main():
    http = HttpClientService(timeout=60)

    clients = {
        InstumentType.FUTURES: FuturesClient(session_factory=http.create),
        InstumentType.STOCKS: StocksClient(session_factory=http.create)
    }

    facade = TradeApiFacade(clients=clients)
    repo = CsvRepository()

    source = AspInstrumentSource(http=http, base_url="test")

    worker = TradeScheduleWorker(
        facade=facade,
        repo=repo,
        source=source
    )

    await worker()

asyncio.run(main())
