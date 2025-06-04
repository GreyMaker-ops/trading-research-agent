"""Data ingestion node for market data and news."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Iterable, List

import ccxt.async_support as ccxt

PAIRS = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "DOGE/USDT"]


@dataclass
class Candle:
    """Represents a single 1-minute candle."""

    ts: datetime
    pair: str
    open: float
    high: float
    low: float
    close: float
    volume: float


async def fetch_candles(pairs: Iterable[str]) -> List[Candle]:
    """Fetch the latest 1-minute candle for each pair using ccxt."""
    exchange = ccxt.binance()
    candles: List[Candle] = []
    try:
        for pair in pairs:
            data = await exchange.fetch_ohlcv(pair, timeframe="1m", limit=1)
            if not data:
                continue
            ts, open_, high, low, close, volume = data[-1]
            candles.append(
                Candle(
                    ts=datetime.fromtimestamp(ts / 1000, tz=UTC),
                    pair=pair,
                    open=open_,
                    high=high,
                    low=low,
                    close=close,
                    volume=volume,
                )
            )
    finally:
        await exchange.close()
    return candles
