from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd


def _ensure_times(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    if "timestamp" not in out.columns and "bar_open_at" in out.columns:
        out["timestamp"] = out["bar_open_at"]
    if "bar_open_at" not in out.columns and "timestamp" in out.columns:
        out["bar_open_at"] = out["timestamp"]
    if "timestamp" not in out.columns:
        return pd.DataFrame()
    out["timestamp"] = pd.to_datetime(out["timestamp"], utc=True, errors="coerce")
    out["bar_open_at"] = pd.to_datetime(out["bar_open_at"], utc=True, errors="coerce")
    out = out.dropna(subset=["timestamp", "bar_open_at"]).sort_values("bar_open_at")
    if "bar_close_at" not in out.columns:
        step = out["bar_open_at"].diff().dropna().median()
        if pd.isna(step):
            step = pd.Timedelta(minutes=15)
        out["bar_close_at"] = out["bar_open_at"] + step - pd.Timedelta(milliseconds=1)
    else:
        out["bar_close_at"] = pd.to_datetime(out["bar_close_at"], utc=True, errors="coerce")
    return out.reset_index(drop=True)


def _rsi(close: pd.Series, period: int) -> pd.Series:
    delta = close.diff()
    gain = delta.clip(lower=0.0).ewm(alpha=1 / period, adjust=False, min_periods=period).mean()
    loss = (-delta.clip(upper=0.0)).ewm(alpha=1 / period, adjust=False, min_periods=period).mean()
    rs = gain / loss.replace(0.0, np.nan)
    return 100.0 - (100.0 / (1.0 + rs))


def _adx(high: pd.Series, low: pd.Series, close: pd.Series, tr: pd.Series, period: int) -> pd.Series:
    up = high.diff()
    down = -low.diff()
    plus_dm = pd.Series(np.where((up > down) & (up > 0), up, 0.0), index=high.index)
    minus_dm = pd.Series(np.where((down > up) & (down > 0), down, 0.0), index=high.index)
    tr_sum = tr.rolling(period, min_periods=period).sum().replace(0.0, np.nan)
    plus_di = 100.0 * plus_dm.rolling(period, min_periods=period).sum() / tr_sum
    minus_di = 100.0 * minus_dm.rolling(period, min_periods=period).sum() / tr_sum
    dx = (100.0 * (plus_di - minus_di).abs() / (plus_di + minus_di).replace(0.0, np.nan))
    return dx.rolling(period, min_periods=period).mean()


def add_indicators(frame: pd.DataFrame, strategy: dict[str, Any], session_vwap: bool = False) -> pd.DataFrame:
    out = _ensure_times(frame)
    if out.empty:
        return out
    for column in ("open", "high", "low", "close", "volume"):
        out[column] = pd.to_numeric(out.get(column), errors="coerce")
    high, low, close = out["high"], out["low"], out["close"]
    prev_close = close.shift(1)
    tr = pd.concat([(high - low), (high - prev_close).abs(), (low - prev_close).abs()], axis=1).max(axis=1)
    atr_period = int(strategy.get("atr_period", 14))
    out["atr"] = tr.rolling(atr_period, min_periods=max(2, atr_period // 2)).mean()
    fast = int(strategy.get("ema_fast", 20))
    slow = int(strategy.get("ema_slow", 50))
    out["ema_fast"] = close.ewm(span=fast, adjust=False, min_periods=max(2, fast // 2)).mean()
    out["ema_slow"] = close.ewm(span=slow, adjust=False, min_periods=max(2, slow // 2)).mean()
    slope_bars = int(strategy.get("ema_slope_bars", 8))
    out["ema_slope_atr"] = (out["ema_fast"] - out["ema_fast"].shift(slope_bars)) / out["atr"].replace(0.0, np.nan)
    out["adx"] = _adx(high, low, close, tr, int(strategy.get("adx_period", 14)))
    out["rsi"] = _rsi(close, int(strategy.get("rsi_period", 14)))
    rvol_period = int(strategy.get("rvol_period", 20))
    out["rvol"] = out["volume"] / out["volume"].rolling(rvol_period, min_periods=max(2, rvol_period // 2)).median().replace(0.0, np.nan)
    if session_vwap:
        typical = (high + low + close) / 3.0
        value = typical * out["volume"]
        out["session_vwap"] = value.cumsum() / out["volume"].cumsum().replace(0.0, np.nan)
    return out

