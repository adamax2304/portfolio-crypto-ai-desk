from __future__ import annotations

import pandas as pd

from src.indicators.technicals import enrich_ohlcv


def atr_percentile(frame: pd.DataFrame, lookback: int = 100) -> float | None:
    enriched = enrich_ohlcv(frame)
    atr_values = enriched["atr14"].dropna().tail(lookback)
    if len(atr_values) < 20:
        return None
    latest = float(atr_values.iloc[-1])
    return float((atr_values <= latest).mean() * 100)


def range_expansion(frame: pd.DataFrame, lookback: int = 20) -> float | None:
    if len(frame) < lookback + 1:
        return None
    ranges = (frame["high"] - frame["low"]).tail(lookback)
    avg_range = float(ranges.iloc[:-1].mean())
    if avg_range == 0:
        return None
    return float(ranges.iloc[-1] / avg_range)
