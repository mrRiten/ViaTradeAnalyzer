from typing import TypedDict, List


class InstrumentsResponse(TypedDict):
    stocks: List[str]
    futures: List[str]
