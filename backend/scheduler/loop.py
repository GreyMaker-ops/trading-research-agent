"""APScheduler loop for running the research cycle."""

import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pandas as pd
from backend.graph.nodes.ingestion import PAIRS, fetch_candles
from backend.graph.nodes.indicators import compute_indicators
from backend.graph.nodes.social import fetch_social_metrics
from backend.graph.nodes.llm_scoring import score_signals
from backend.graph.nodes.evaluation import evaluate_signals
from backend.db.persistence import save_candles, save_indicators, save_signals

logger = logging.getLogger(__name__)


async def run_cycle() -> None:
    """Run one ingestion/scoring cycle."""
    candles = await fetch_candles(PAIRS)
    if not candles:
        return
    await save_candles(candles)
    df = pd.DataFrame([c.__dict__ for c in candles])
    sentiment = await fetch_social_metrics(PAIRS)
    indicators = compute_indicators(df, sentiment)
    await save_indicators(indicators)
    signals = await score_signals(indicators)
    await save_signals(signals)


async def check_hits() -> None:
    """Evaluate unresolved signals."""
    await evaluate_signals()


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
