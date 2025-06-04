"""APScheduler loop for running the research cycle."""

import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from backend.graph.nodes.ingestion import PAIRS, fetch_candles

logger = logging.getLogger(__name__)


async def run_cycle() -> None:
    """Fetch candles for all pairs and log the results."""
    candles = await fetch_candles(PAIRS)
    for candle in candles:
        logger.info(
            "%s %s o=%s h=%s l=%s c=%s v=%s",
            candle.ts.isoformat(),
            candle.pair,
            candle.open,
            candle.high,
            candle.low,
            candle.close,
            candle.volume,
        )


async def check_hits() -> None:
    """Evaluate unresolved signals (placeholder)."""
    return None


def start() -> None:
    """Start the APScheduler event loop."""
    scheduler = AsyncIOScheduler()
    scheduler.add_job(run_cycle, "cron", second=0)
    scheduler.add_job(check_hits, "cron", second=10)
    scheduler.start()
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        scheduler.shutdown()
