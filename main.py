import asyncio
from services.api.http_client_service import HttpClientService
from services.api.asp_instrument_service import AspInstrumentSource
from services.background.exchange_client_manager import ExchangeClientManager
from services.background.trade_schedule_worker import TradeScheduleWorker
from services.csv.csv_data_repository import CsvDataRepository
from services.csv.csv_data_service import CsvDataService



async def main():
    http = HttpClientService(timeout=60)

    source = AspInstrumentSource(
        http=http,
        base_url="test"
    )

    client_manager = ExchangeClientManager(
        session_factory=http.create
    )

    repo = CsvDataRepository()
    csv_service = CsvDataService(repo)

    worker = TradeScheduleWorker(
        csv_service=csv_service,
        source=source,
        client_manager=client_manager
    )

    await worker()


if __name__ == "__main__":
    asyncio.run(main())
