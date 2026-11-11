"""Feature computation for the Stocks Position Framework (pure, no network).

Operates on a daily OHLCV pandas DataFrame with columns open/high/low/close/volume, sorted
ASCENDING by date (oldest first). The runner adapts whatever the collectors return into this
shape, so this module stays decoupled from collector APIs and fully unit-testable offline.
"""
from __future__ import annotations

from typing import Any

try:
    import pandas as pd
except Exception:  # pragma: no cover
    pd = None

_REQUIRED = ("open", "high", "low", "close", "volume")


def _ok(df) -> bool:
    return pd is not None and df is not None and len(df) > 0 and all(c in df.columns for c in _REQUIRED)


def _f(v) -> float | None:
    try:
        return None if v is None else float(v)
    except (TypeError, ValueError):
        return None


def sma(df, n: int) -> float | None:
    if not _ok(df) or len(df) < n:
        return None
    return _f(df["close"].tail(n).mean())


def ema(df, n: int) -> float | None:
    if not _ok(df) or len(df) < n:
        return None
    return _f(df["close"].ewm(span=n, adjust=False).mean().iloc[-1])


def atr14(df, n: int = 14) -> float | None:
    if not _ok(df) or len(df) < n + 1:
        return None
    h, l, c = df["high"], df["low"], df["close"]
    prev_c = c.shift(1)
    tr = pd.concat([(h - l), (h - prev_c).abs(), (l - prev_c).abs()], axis=1).max(axis=1)
    return _f(tr.tail(n).mean())


def volume_ratio(df, n: int = 20) -> float | None:
    if not _ok(df) or len(df) < n + 1:
        return None
    avg = df["volume"].iloc[-(n + 1):-1].mean()
    last = df["volume"].iloc[-1]
    if not avg or avg <= 0:
        return None
    return _f(last / avg)


def dollar_volume_30d(df, n: int = 30) -> float | None:
    if not _ok(df) or len(df) < 1:
        return None
    tail = df.tail(n)
    return _f((tail["close"] * tail["volume"]).mean())


def pct_below_high(df, lookback: int) -> float | None:
    """How far the last close sits below the highest HIGH over `lookback` bars (percent, >=0)."""
    if not _ok(df) or len(df) < 2:
        return None
    hi = df["high"].tail(lookback).max()
    last = df["close"].iloc[-1]
    if not hi or hi <= 0:
        return None
    return _f(max(0.0, (hi - last) / hi * 100.0))


def recent_swing_low(df, lookback: int = 10) -> float | None:
    if not _ok(df) or len(df) < 2:
        return None
    return _f(df["low"].tail(lookback).min())


def recent_high(df, lookback: int = 20) -> float | None:
    if not _ok(df) or len(df) < 1:
        return None
    return _f(df["high"].tail(lookback).max())


def _return_over(df, lookback: int) -> float | None:
    if not _ok(df) or len(df) < lookback + 1:
        return None
    a = df["close"].iloc[-(lookback + 1)]
    b = df["close"].iloc[-1]
    if not a or a <= 0:
        return None
    return _f(b / a - 1.0)


def rs_vs(df, bench_df, lookback: int = 63) -> float | None:
    """Relative strength = stock's return minus benchmark's return over `lookback` (fraction).
    Positive = outperforming. None if either series is too short."""
    r_stock = _return_over(df, lookback)
    r_bench = _return_over(bench_df, lookback)
    if r_stock is None or r_bench is None:
        return None
    return _f(r_stock - r_bench)


def is_above(price: float | None, level: float | None) -> bool | None:
    if price is None or level is None:
        return None
    return price > level


def trend_up(df, fast: int = 50, slow: int = 200) -> bool | None:
    """Simple trend proxy for an index/ETF: last close above its `fast` SMA."""
    c = _f(df["close"].iloc[-1]) if _ok(df) else None
    return is_above(c, sma(df, fast))


def weekly_features(wdf) -> dict[str, Any]:
    """Optional weekly-timeframe context (10W/30W). All None when weekly data is absent/short.

    Phase 1: informational only — the detector warns (does NOT block) when these are None.
    """
    out: dict[str, Any] = {"weekly_above_10w": None, "weekly_above_30w": None,
                           "weekly_30w_slope_positive": None, "weekly_bars": (len(wdf) if _ok(wdf) else 0)}
    if not _ok(wdf) or len(wdf) < 10:
        return out
    last = _f(wdf["close"].iloc[-1])
    out["weekly_above_10w"] = is_above(last, sma(wdf, 10))
    if len(wdf) >= 30:
        out["weekly_above_30w"] = is_above(last, sma(wdf, 30))
        if len(wdf) >= 34:
            ser = wdf["close"].rolling(30).mean()
            now, prior = ser.iloc[-1], ser.iloc[-5]     # 30W SMA now vs 4 weeks ago
            if pd.notna(now) and pd.notna(prior):
                out["weekly_30w_slope_positive"] = bool(now > prior)
    return out


def compute_features(df, *, spy_df=None, qqq_df=None, sector_df=None, weekly_df=None,
                     near_high_lookbacks=(63, 126, 252)) -> dict[str, Any]:
    """Full feature dict for one symbol. Missing inputs → None fields (never fabricated)."""
    if not _ok(df):
        return {"available": False, "reason": "no/invalid daily OHLCV"}
    last = _f(df["close"].iloc[-1])
    feats: dict[str, Any] = {
        "available": True,
        "last_close": last,
        "sma10": sma(df, 10), "ema21": ema(df, 21), "sma50": sma(df, 50), "sma200": sma(df, 200),
        "ema10": ema(df, 10), "ema50": ema(df, 50),
        "atr14": atr14(df),
        "volume_ratio": volume_ratio(df, 20),
        "dollar_volume_30d": dollar_volume_30d(df, 30),
        "swing_low_10": recent_swing_low(df, 10),
        "swing_low_20": recent_swing_low(df, 20),
        "high_20": recent_high(df, 20),
        "bars": len(df),
    }
    feats["above_50d"] = is_above(last, feats["sma50"])
    feats["above_200d"] = is_above(last, feats["sma200"])
    feats["dist_to_ema21_pct"] = (_f((last - feats["ema21"]) / feats["ema21"] * 100.0)
                                  if last and feats["ema21"] else None)
    feats["dist_to_sma50_pct"] = (_f((last - feats["sma50"]) / feats["sma50"] * 100.0)
                                  if last and feats["sma50"] else None)
    feats["near_high"] = {str(lb): pct_below_high(df, lb) for lb in near_high_lookbacks}
    feats["rs_spy"] = rs_vs(df, spy_df, 63) if spy_df is not None else None
    feats["rs_qqq"] = rs_vs(df, qqq_df, 63) if qqq_df is not None else None
    feats["rs_sector"] = rs_vs(df, sector_df, 63) if sector_df is not None else None
    feats["sector_trend_up"] = trend_up(sector_df, 50) if sector_df is not None else None
    feats.update(weekly_features(weekly_df))
    return feats
