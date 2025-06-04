"""LLM-based scoring for signals."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import List, Sequence
from uuid import UUID, uuid4

import backend.embeddings.qdrant_client as qc
import google.generativeai as gen
import pandas as pd
from qdrant_client.http import models as qmodels


@dataclass
class SignalCandidate:
    """Represents a proposed trading signal."""

    id: UUID
    ts: datetime
    pair: str
    direction: str
    rationale: str
    confidence: float


async def _ensure_collection(client) -> None:
    """Ensure that the signal_vectors collection exists."""
    name = "signal_vectors"
    try:
        client.get_collection(name)
    except Exception:
        client.recreate_collection(
            name,
            vectors_config=qmodels.VectorParams(size=768, distance=qmodels.Distance.COSINE),
        )


def _indicators_to_csv(df: pd.DataFrame) -> str:
    """Convert indicators to a CSV string for the prompt."""
    return df.to_csv(index=False)


async def score_signals(indicator_batch: pd.DataFrame) -> List[SignalCandidate]:
    """Generate trading signal candidates using Gemini."""
    gen.configure(api_key=os.getenv("GEMINI_API_KEY", ""))
    model = gen.GenerativeModel("gemini-pro")
    csv_snapshot = _indicators_to_csv(indicator_batch)
    prompt = (
        "You are a trading assistant. "
        "Analyze the following indicator snapshot and suggest up to three trade signals. "
        "Respond with a JSON array where each item has keys 'pair', 'direction' (buy/sell), "
        "'rationale', and 'confidence' (0-1).\n" + csv_snapshot
    )
    resp = await model.generate_content_async(prompt)
    text = resp.text
    start = text.find("[")
    if start == -1:
        return []
    try:
        data: Sequence[dict] = json.loads(text[start:])
    except json.JSONDecodeError:
        return []

    client = qc.get_client()
    await _ensure_collection(client)
    results: List[SignalCandidate] = []
    for item in data:
        try:
            candidate = SignalCandidate(
                id=uuid4(),
                ts=datetime.now(tz=UTC),
                pair=item["pair"],
                direction=item["direction"],
                rationale=item["rationale"],
                confidence=float(item["confidence"]),
            )
        except KeyError:
            continue
        emb_resp = await gen.embed_content_async("models/embedding-001", candidate.rationale)
        vector = emb_resp["embedding"]
        client.upsert(
            "signal_vectors",
            [
                {
                    "id": str(candidate.id),
                    "vector": vector,
                    "payload": {
                        "pair": candidate.pair,
                        "direction": candidate.direction,
                        "ts": candidate.ts.isoformat(),
                    },
                }
            ],
        )
        results.append(candidate)
    return results
