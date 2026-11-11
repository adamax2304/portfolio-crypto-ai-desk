"""Intraday risk-off / long-bias VISIBILITY label (alert-only).

Computes a BTC-anchored risk-off context for crypto longs. It NEVER throttles,
half-sizes, or blocks — `would_throttle_long` is a diagnostic flag only.

Validation target (see INTRADAY_RISK_OFF_THROTTLE_DIAGNOSTIC.md): on the 06-15
BTC-up day (+0.89%) it must NOT trigger; on 06-16/06-17 BTC-down days
(~-0.99% / -0.96%) it must flag risk-off context.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

# BTC daily change at/under this (%) marks intraday risk-off. -0.75 cleanly
# separates the 06-15 up day from the 06-16/17 down days in the diagnostic.
RISK_OFF_DAY_PCT = -0.75

_FS_CACHE: list[Any] = []


def classify_risk_off(
    day_change_pct: float | None,
    h1_trend: str | None = None,
    h4_trend: str | None = None,
    *,
    threshold: float = RISK_OFF_DAY_PCT,
) -> dict[str, Any]:
    """Pure classifier. Risk-off when BTC day change <= threshold OR the 1h
    trend is down while the day is already negative. ``regime_context`` is a
    coarse btc_up / btc_flat / btc_risk_off label. Returns null-ish fields when
    inputs are unknown (never fabricates)."""
    if day_change_pct is None:
        return {
            "btc_day_change_pct": None,
            "btc_1h_trend": h1_trend,
            "btc_4h_trend": h4_trend,
            "btc_intraday_risk_off": None,
            "regime_context": "unknown",
            "would_throttle_long": False,
            "risk_off_diagnostic": "btc data unavailable",
            "diagnostic_only": True,
        }
    risk_off = (day_change_pct <= threshold) or (
        h1_trend == "down" and day_change_pct < 0)
    if risk_off:
        regime = "btc_risk_off"
    elif day_change_pct >= 0.5:
        regime = "btc_up"
    else:
        regime = "btc_flat"
    return {
        "btc_day_change_pct": round(day_change_pct, 2),
        "btc_1h_trend": h1_trend,
        "btc_4h_trend": h4_trend,
        "btc_intraday_risk_off": bool(risk_off),
        "regime_context": regime,
        "would_throttle_long": bool(risk_off),
        "risk_off_diagnostic": (
            f"BTC {day_change_pct:+.2f}% day"
            + (f", 1h {h1_trend}" if h1_trend else "")
            + (" → risk-off" if risk_off else "")
        ),
        "diagnostic_only": True,
    }


def _trend_from_frame(frame, lookback: int) -> str | None:
    """up/down/flat from close vs close `lookback` bars ago (±0.3% deadband)."""
    try:
        closes = frame["close"].astype(float).tolist()
        if len(closes) <= lookback:
            return None
        now_c, prev_c = closes[-1], closes[-1 - lookback]
        if prev_c == 0:
            return None
        chg = (now_c - prev_c) / prev_c * 100.0
        if chg > 0.3:
            return "up"
        if chg < -0.3:
            return "down"
        return "flat"
    except Exception:
        return None


def _day_change_from_frame(frame_1d) -> float | None:
    try:
        last = frame_1d.iloc[-1]
        o, c = float(last["open"]), float(last["close"])
        if o == 0:
            return None
        return (c - o) / o * 100.0
    except Exception:
        return None


def _file_store():
    if _FS_CACHE:
        return _FS_CACHE[0]
    from src.config import load_config
    from src.storage.file_store import FileStore
    fs = FileStore(load_config())
    _FS_CACHE.append(fs)
    return fs


def compute_risk_off(
    file_store: Any = None,
    *,
    now: datetime | None = None,
    anchor_exchange: str = "binance",
    symbol: str = "BTC/USDT",
) -> dict[str, Any]:
    """Build the risk-off fields from BTC OHLCV. Fails open to unknown.

    ``now`` is accepted for signature symmetry / future windowing; the label
    reflects the latest available BTC candles."""
    try:
        fs = file_store or _file_store()
        d1 = fs.load_ohlcv(anchor_exchange, symbol, "1d")
        h1 = fs.load_ohlcv(anchor_exchange, symbol, "1h")
        h4 = fs.load_ohlcv(anchor_exchange, symbol, "4h")
        day_pct = _day_change_from_frame(d1) if d1 is not None else None
        h1_trend = _trend_from_frame(h1, 6) if h1 is not None else None  # ~6h
        h4_trend = _trend_from_frame(h4, 6) if h4 is not None else None  # ~24h
        return classify_risk_off(day_pct, h1_trend, h4_trend)
    except Exception:
        return classify_risk_off(None)
