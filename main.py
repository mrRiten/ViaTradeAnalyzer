# import asyncio
# from services.api.http_client_service import HttpClientService
# from services.api.asp_instrument_service import AspInstrumentSource
# from services.background.exchange_client_manager import ExchangeClientManager
# from services.background.trade_schedule_worker import TradeScheduleWorker
# from services.csv.csv_data_repository import CsvDataRepository
# from services.csv.csv_data_service import CsvDataService



# async def main():
#     http = HttpClientService(timeout=60)

#     source = AspInstrumentSource(
#         http=http,
#         base_url="test"
#     )

#     client_manager = ExchangeClientManager(
#         session_factory=http.create
#     )

#     repo = CsvDataRepository()
#     csv_service = CsvDataService(repo)

#     worker = TradeScheduleWorker(
#         csv_service=csv_service,
#         source=source,
#         client_manager=client_manager
#     )

#     await worker()


# if __name__ == "__main__":
#     asyncio.run(main())


from services.csv.csv_data_service import CsvDataService
from services.csv.csv_data_repository import CsvDataRepository
from services.strategies.Screnners.deep_ema_rsi_screnner import DeepEmaRsiScrenner
from services.strategies.analyzer_service import AnalyzerService
from services.strategies.trend_following_strategy import TrendFollowingStrategy


def main() -> None:
    data_repository = CsvDataRepository()
    data_service = CsvDataService(repo=data_repository)

    screnner = DeepEmaRsiScrenner()

    strategy = TrendFollowingStrategy(
        screnners=[screnner],
        data_repository=data_repository
    )

    analyzer = AnalyzerService(
        strategies=[strategy],
        data_service=data_service
    )

    analyzer()


if __name__ == "__main__":
    main()
