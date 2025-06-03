"""Data ingestion node for market data and news."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Candle:
    ts: str
    pair: str
    open: float
    high: float
    low: float
    close: float
    volume: float


async def fetch_candles() -> list[Candle]:
    """Placeholder for candle fetch logic."""
    return []
