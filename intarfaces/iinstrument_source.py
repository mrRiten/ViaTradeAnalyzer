from typing import Protocol
from models.trade_entity import InstumentType


class InstrumentSourceProtocol(Protocol):
    async def get_instruments(self) -> dict[InstumentType, list[str]]: ...
