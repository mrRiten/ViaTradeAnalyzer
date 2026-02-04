from services.moex.base_moex_client import BaseMoexClient


class FuturesClient(BaseMoexClient):
    def __init__(self, session_factory):
        super().__init__("https://iss.moex.com/iss/engines/futures/markets/forts/securities", session_factory)
