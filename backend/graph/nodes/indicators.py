"""Technical indicator computation."""

import pandas as pd
import numpy as np

# pandas-ta expects numpy.NaN to exist, but this constant was removed in newer
# numpy versions. Add it back for compatibility if missing.
if not hasattr(np, "NaN"):
    np.NaN = np.nan  # type: ignore[attr-defined]

import pandas_ta as ta


def compute_indicators(
    df: pd.DataFrame, sentiment: pd.DataFrame | None = None
) -> pd.DataFrame:
    """Compute EMA, RSI, Bollinger Bands, and merge sentiment metrics."""
    df = df.copy()
    df["ema_fast"] = ta.ema(df["close"], length=5)
    df["ema_slow"] = ta.ema(df["close"], length=13)
    df["rsi14"] = ta.rsi(df["close"], length=14)
    bb = ta.bbands(df["close"], length=20)
    df["bb_width"] = bb["BBB_20_2.0"] - bb["BBL_20_2.0"]
    if sentiment is not None:
        df = df.merge(sentiment, on="pair", how="left")
    return df
