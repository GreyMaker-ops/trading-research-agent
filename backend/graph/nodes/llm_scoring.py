"""LLM-based scoring for signals."""

from typing import List


class SignalCandidate(dict):
    pass


async def score_signals(indicator_batch) -> List[SignalCandidate]:
    """Placeholder for Gemini scoring logic."""
    return []
