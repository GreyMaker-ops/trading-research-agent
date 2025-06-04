import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from backend.graph.nodes.indicators import compute_indicators


def test_compute_indicators_basic():
    data = {
        "close": list(range(1, 31))
    }
    df = pd.DataFrame(data)
    out = compute_indicators(df)
    assert "ema_fast" in out
    assert "ema_slow" in out
    assert "rsi14" in out
    assert "bb_width" in out
    # Ensure last row has numeric values for indicators
    last = out.iloc[-1]
    assert pd.notnull(last["ema_fast"])
    assert pd.notnull(last["ema_slow"])
    assert pd.notnull(last["rsi14"])
    assert pd.notnull(last["bb_width"])
