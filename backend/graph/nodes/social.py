"""Social sentiment ingestion nodes."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Iterable, List

import aiohttp
import pandas as pd


@dataclass
class SocialMetrics:
    """Aggregated social sentiment metrics for a trading pair."""

    pair: str
    tweet_z: float
    news_polarity: float


async def _fetch_tweets(pair: str, session: aiohttp.ClientSession) -> List[str]:
    """Fetch recent tweets mentioning the given pair."""
    token = os.getenv("TWITTER_BEARER_TOKEN", "")
    if not token:
        return []
    symbol = pair.split("/")[0]
    url = "https://api.twitter.com/2/tweets/search/recent"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"query": symbol, "max_results": "50"}
    async with session.get(url, headers=headers, params=params) as resp:
        if resp.status != 200:
            return []
        data = await resp.json()
        return [t.get("text", "") for t in data.get("data", [])]


async def _fetch_news(pair: str, session: aiohttp.ClientSession) -> List[dict]:
    """Fetch recent CryptoPanic news for the pair."""
    token = os.getenv("CRYPTOPANIC_TOKEN", "")
    if not token:
        return []
    symbol = pair.split("/")[0].lower()
    url = "https://cryptopanic.com/api/v1/posts/"
    params = {"auth_token": token, "currencies": symbol}
    async with session.get(url, params=params) as resp:
        if resp.status != 200:
            return []
        data = await resp.json()
        return data.get("results", [])


async def fetch_social_metrics(pairs: Iterable[str]) -> pd.DataFrame:
    """Return social metrics for each pair."""
    async with aiohttp.ClientSession() as session:
        records: List[SocialMetrics] = []
        for pair in pairs:
            tweets = await _fetch_tweets(pair, session)
            news = await _fetch_news(pair, session)
            tweet_z = float(len(tweets))
            polarity = 0.0
            for item in news:
                votes = item.get("votes", {})
                polarity += float(votes.get("positive", 0)) - float(votes.get("negative", 0))
            metrics = SocialMetrics(pair=pair, tweet_z=tweet_z, news_polarity=polarity)
            records.append(metrics)
    return pd.DataFrame([m.__dict__ for m in records])
