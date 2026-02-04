from services.moex.base_moex_client import BaseMoexClient


class StocksClient(BaseMoexClient):
    def __init__(self, session_factory):
        super().__init__("https://iss.moex.com/iss/engines/stock/markets/shares/securities", session_factory)
