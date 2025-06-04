import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from backend.graph.nodes.llm_scoring import SignalCandidate, score_signals


@pytest.mark.asyncio
async def test_score_signals(monkeypatch):
    df = pd.DataFrame(
        {
            "pair": ["BTC/USDT"],
            "ema_fast": [1.0],
            "ema_slow": [2.0],
            "rsi14": [50.0],
            "bb_width": [0.1],
        }
    )

    class DummyResponse:
        text = (
            '[{"pair": "BTC/USDT", "direction": "buy", '
            '"rationale": "breakout", "confidence": 0.8}]'
        )

    async def dummy_generate(self, *args, **kwargs):
        return DummyResponse()

    async def dummy_embed(*args, **kwargs):
        return {"embedding": [0.0] * 768}

    class DummyClient:
        def get_collection(self, name):
            raise Exception("missing")

        def recreate_collection(self, *args, **kwargs):
            pass

        def upsert(self, *args, **kwargs):
            pass

    monkeypatch.setattr(
        "backend.graph.nodes.llm_scoring.gen.GenerativeModel.generate_content_async",
        dummy_generate,
    )
    monkeypatch.setattr(
        "backend.graph.nodes.llm_scoring.gen.embed_content_async",
        dummy_embed,
    )
    monkeypatch.setattr(
        "backend.embeddings.qdrant_client.get_client",
        lambda: DummyClient(),
    )

    results = await score_signals(df)
    assert len(results) == 1
    cand = results[0]
    assert isinstance(cand, SignalCandidate)
    assert cand.pair == "BTC/USDT"
    assert cand.direction == "buy"
    assert cand.confidence == 0.8
