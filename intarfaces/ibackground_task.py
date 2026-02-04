from typing import Awaitable, Protocol


class BackgroundTask(Protocol):
    async def __call__(self) -> Awaitable[None]:
        ...