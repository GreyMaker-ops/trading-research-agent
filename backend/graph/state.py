"""State objects for the trading workflow."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

import pandas as pd

from .nodes.ingestion import Candle
from .nodes.llm_scoring import SignalCandidate


@dataclass
class TradingState:
    """State passed between workflow nodes."""

    candles: Optional[List[Candle]] = None
    indicators_df: Optional[pd.DataFrame] = None
    signals: Optional[List[SignalCandidate]] = None
