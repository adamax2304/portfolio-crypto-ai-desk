from __future__ import annotations

import numpy as np
import pandas as pd


def ema(series: pd.Series, period: int) -> pd.Series:
    return series.ewm(span=period, adjust=False, min_periods=period).mean()


def true_range(frame: pd.DataFrame) -> pd.Series:
    prev_close = frame["close"].shift(1)
    ranges = pd.concat(
        [
            frame["high"] - frame["low"],
            (frame["high"] - prev_close).abs(),
            (frame["low"] - prev_close).abs(),
        ],
        axis=1,
    )
    return ranges.max(axis=1)


def atr(frame: pd.DataFrame, period: int = 14) -> pd.Series:
    return true_range(frame).rolling(period, min_periods=period).mean()


def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(period, min_periods=period).mean()
    loss = (-delta.clip(upper=0)).rolling(period, min_periods=period).mean()
    rs = gain / loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def enrich_ohlcv(frame: pd.DataFrame) -> pd.DataFrame:
    output = frame.copy()
    output["ema20"] = ema(output["close"], 20)
    output["ema50"] = ema(output["close"], 50)
    output["ema200"] = ema(output["close"], 200)
    output["atr14"] = atr(output, 14)
    output["rsi14"] = rsi(output["close"], 14)
    output["volume_sma20"] = output["volume"].rolling(20, min_periods=20).mean()
    output["return_1"] = output["close"].pct_change() * 100
    return output


def pct_return(frame: pd.DataFrame, periods: int) -> float | None:
    if len(frame) <= periods:
        return None
    start = float(frame["close"].iloc[-periods - 1])
    end = float(frame["close"].iloc[-1])
    if start == 0:
        return None
    return (end / start - 1) * 100


def recent_range(frame: pd.DataFrame, lookback: int = 20) -> tuple[float | None, float | None]:
    if len(frame) < lookback + 1:
        return None, None
    window = frame.iloc[-lookback - 1 : -1]
    return float(window["high"].max()), float(window["low"].min())


def trend_label(frame: pd.DataFrame) -> str:
    enriched = enrich_ohlcv(frame)
    last = enriched.iloc[-1]
    close = float(last["close"])
    ema20_v = float(last["ema20"]) if pd.notna(last["ema20"]) else close
    ema50_v = float(last["ema50"]) if pd.notna(last["ema50"]) else close
    if close > ema20_v > ema50_v:
        return "uptrend"
    if close < ema20_v < ema50_v:
        return "downtrend"
    if close > ema50_v and ema20_v < ema50_v:
        return "transition_up"
    if close < ema50_v and ema20_v > ema50_v:
        return "transition_down"
    return "range"
