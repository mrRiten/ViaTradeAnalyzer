# Trade Models
from dataclasses import dataclass
from typing import TypedDict, List, Union
from enum import Enum

# Base Trade Models
class SignalType(Enum):
    BUY = "Buy"
    SELL = "Sell"
    HOLD = "Hold"

@dataclass
class Candle:
    open: float
    close: float
    high: float
    low: float
    volume: float

class InstumentType(Enum):
    STOCKS = "stocks"
    FUTURES = "futures"


# Moex Models
class TimeFrame(Enum):
    HOUR_1 = 60
    DAY = 24


INSTRUMENT_TIMEFRAME: dict[InstumentType, TimeFrame] = {
    InstumentType.STOCKS: TimeFrame.DAY,
    InstumentType.FUTURES: TimeFrame.HOUR_1,
}

JsonScalar = Union[str, int, float, None]
JsonRow = List[JsonScalar]


class MoexTable(TypedDict):
    columns: List[str]
    data: List[JsonRow]


class MoexResponse(TypedDict, total=False):
    securities: MoexTable
    candles: MoexTable

# Screner Models
