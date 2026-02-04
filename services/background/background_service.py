import asyncio
from typing import Awaitable, Callable
from datetime import datetime

from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler

BackgroundTask = Callable[[], Awaitable[None]]


class BackgroundService:
    def __init__(
        self,
        name: str,
        func: BackgroundTask,
        cron: CronTrigger
    ):
        self.name: str = name
        self.func: BackgroundTask = func
        self.cron: CronTrigger = cron
        self.job_id: str = name

    async def run(self) -> None:
        try:
            await self.func()
        except asyncio.CancelledError:
            return
        except Exception as e:
            print(f"[{self.name}] error: {e}")

    def register(self, scheduler: AsyncIOScheduler) -> None:
        scheduler.add_job(self.run, self.cron, id=self.job_id)

    def force_run(self, scheduler: AsyncIOScheduler) -> None:
        job = scheduler.get_job(self.job_id)
        if job:
            scheduler.modify_job(job.id, next_run_time=datetime.now())
