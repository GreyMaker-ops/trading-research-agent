import sys
from pathlib import Path
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from backend.graph.nodes.social import fetch_social_metrics


@pytest.mark.asyncio
async def test_fetch_social_metrics(monkeypatch):
    class DummyResponse:
        status = 200
        async def json(self):
            return {"data": [{"text": "tweet"}]}
        async def __aenter__(self):
            return self
        async def __aexit__(self, exc_type, exc, tb):
            pass

    class DummyNewsResponse:
        status = 200
        async def json(self):
            return {"results": [{"votes": {"positive": 2, "negative": 1}}]}
        async def __aenter__(self):
            return self
        async def __aexit__(self, exc_type, exc, tb):
            pass

    async def dummy_get(url, *args, **kwargs):
        if "tweets" in url:
            return DummyResponse()
        return DummyNewsResponse()

    class DummySession:
        async def __aenter__(self):
            return self
        async def __aexit__(self, exc_type, exc, tb):
            pass
        async def get(self, url, *args, **kwargs):
            return await dummy_get(url, *args, **kwargs)

    monkeypatch.setattr("aiohttp.ClientSession", lambda: DummySession())

    df = await fetch_social_metrics(["BTC/USDT"])
    assert isinstance(df, pd.DataFrame)
    assert df.iloc[0]["tweet_z"] == 1.0
    assert df.iloc[0]["news_polarity"] == 1.0
