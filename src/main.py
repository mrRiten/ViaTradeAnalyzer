import asyncio

from services.api.asp_instrument_service import AspInstrumentSource

from services.background.exchange_client_manager import ExchangeClientManager
from services.background.trade_schedule_worker import TradeScheduleWorker

from services.csv.csv_data_repository import CsvDataRepository
from services.csv.csv_data_service import CsvDataService

from services.strategies.Screnners.deep_ema_rsi_screnner import DeepEmaRsiScrenner
from services.strategies.analyzer_service import AnalyzerService
from services.strategies.rsi_strategy import RsiStrategy
from services.strategies.trend_following_strategy import TrendFollowingStrategy
from services.api.http_client_service import HttpClientService


async def run_data_pipeline() -> None:
    http = HttpClientService(timeout=60)

    source = AspInstrumentSource(
        http=http,
        base_url="test"
    )

    client_manager = ExchangeClientManager(
        session_factory=http.create
    )

    repository = CsvDataRepository()

    csv_service = CsvDataService(
        repo=repository
    )

    parser_worker = TradeScheduleWorker(
        csv_service=csv_service,
        source=source,
        client_manager=client_manager
    )

    await parser_worker()

    screnner = DeepEmaRsiScrenner()

    trend_follow_strategy = TrendFollowingStrategy(
        screnners=[screnner],
        data_repository=repository
    )

    rsi_strategy = RsiStrategy(
        screnners=[screnner],
        data_repository=repository
    )

    analyzer = AnalyzerService(
        strategies=[trend_follow_strategy, rsi_strategy],
        data_service=csv_service
    )

    analyzer()


def main() -> None:
    asyncio.run(run_data_pipeline())


if __name__ == "__main__":
    main()