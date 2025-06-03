"""APScheduler loop for running the research cycle."""

import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler


async def run_cycle():
    pass


async def check_hits():
    pass


def start():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(run_cycle, "cron", second=0)
    scheduler.add_job(check_hits, "cron", second=10)
    scheduler.start()
    asyncio.get_event_loop().run_forever()
