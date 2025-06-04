import datetime
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from backend.graph.nodes.ingestion import fetch_candles


@pytest.mark.asyncio
async def test_fetch_candles(monkeypatch):
    class DummyExchange:
        async def fetch_ohlcv(self, pair, timeframe="1m", limit=1):
            return [[1718138400000, 1.0, 2.0, 3.0, 4.0, 5.0]]
        async def close(self):
            pass
    monkeypatch.setattr(
        "backend.graph.nodes.ingestion.ccxt.binance", lambda: DummyExchange()
    )
    candles = await fetch_candles(["BTC/USDT"])
    assert len(candles) == 1
    c = candles[0]
    assert isinstance(c.ts, datetime.datetime)
    assert c.pair == "BTC/USDT"
    assert c.open == 1.0
    assert c.high == 2.0
    assert c.low == 3.0
    assert c.close == 4.0
    assert c.volume == 5.0
