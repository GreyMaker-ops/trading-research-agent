"""Technical indicator computation."""

import pandas as pd
import pandas_ta as ta


def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Compute EMA, RSI, and Bollinger Bands."""
    df = df.copy()
    df["ema_fast"] = ta.ema(df["close"], length=5)
    df["ema_slow"] = ta.ema(df["close"], length=13)
    df["rsi14"] = ta.rsi(df["close"], length=14)
    bb = ta.bbands(df["close"], length=20)
    df["bb_width"] = bb["BBB_20_2.0"] - bb["BBL_20_2.0"]
    return df
