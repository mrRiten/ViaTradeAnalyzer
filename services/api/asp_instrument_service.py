from services.api.http_client_service import HttpClientService
from models.system import InstrumentsResponse
from models.trade_entity import InstumentType


class AspInstrumentSource:
    def __init__(
        self,
        http: HttpClientService,
        base_url: str
    ):
        self.http = http
        self.base_url = base_url

    # async def get_instruments(
    #     self
    # ) -> dict[InstumentType, list[str]]:
    #     async with self.http.create() as session:
    #         async with session.get(
    #             f"{self.base_url}/api/instruments/active"
    #         ) as resp:
    #             data: InstrumentsResponse = await resp.json()

    #     return {
    #         InstumentType.STOCKS: data["stocks"],
    #         InstumentType.FUTURES: data["futures"],
    #     }

    # Пока нет asp сервера
    async def get_instruments(
        self
    ) -> dict[InstumentType, list[str]]:
        return {
            InstumentType.STOCKS: ["GAZP", "MOEX", "T", "YDEX", "GMKN"],
            InstumentType.FUTURES: ["MMH5", "RBH6", "TBH6", "GKH6", "LKH6"],
        }