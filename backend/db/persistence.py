from __future__ import annotations

from typing import Iterable, List

import pandas as pd

from backend.graph.nodes.ingestion import Candle as CandleDTO
from backend.graph.nodes.llm_scoring import SignalCandidate
from .models import Candle, Indicator, Signal
from .session import session_scope


async def save_candles(candles: Iterable[CandleDTO]) -> None:
    """Persist candles fetched from the exchange."""
    records: List[Candle] = [
        Candle(
            ts=c.ts,
            pair=c.pair,
            open=c.open,
            high=c.high,
            low=c.low,
            close=c.close,
            volume=c.volume,
        )
        for c in candles
    ]
    async with session_scope() as session:
        session.add_all(records)


async def save_indicators(df: pd.DataFrame) -> None:
    """Persist computed indicator rows."""
    records: List[Indicator] = []
    for _, row in df.iterrows():
        records.append(
            Indicator(
                ts=row["ts"],
                pair=row["pair"],
                ema_fast=row.get("ema_fast"),
                ema_slow=row.get("ema_slow"),
                rsi14=row.get("rsi14"),
                bb_width=row.get("bb_width"),
                tweet_z=row.get("tweet_z"),
                news_polarity=row.get("news_polarity"),
            )
        )
    async with session_scope() as session:
        session.add_all(records)


async def save_signals(signals: Iterable[SignalCandidate]) -> None:
    """Persist generated signals to Timescale."""
    records = [
        Signal(
            id=str(s.id),
            ts=s.ts,
            pair=s.pair,
            direction=s.direction,
            rationale=s.rationale,
            confidence=s.confidence,
        )
        for s in signals
    ]
    async with session_scope() as session:
        session.add_all(records)
