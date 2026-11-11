from __future__ import annotations

import pandas as pd


def volume_ratio(frame: pd.DataFrame, period: int = 20) -> float | None:
    if len(frame) < period + 1:
        return None
    avg_volume = float(frame["volume"].tail(period + 1).iloc[:-1].mean())
    latest = float(frame["volume"].iloc[-1])
    if avg_volume <= 0:
        return None
    return latest / avg_volume


def quote_volume(frame: pd.DataFrame) -> float | None:
    if frame.empty:
        return None
    last = frame.iloc[-1]
    return float(last["close"] * last["volume"])
