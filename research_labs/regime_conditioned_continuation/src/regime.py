from __future__ import annotations

from typing import Any

import pandas as pd

from research_labs.technical_trend_reclaim.src.engine import Bundle


def _asof_index(frame: pd.DataFrame, at: pd.Timestamp) -> int | None:
    if frame.empty:
        return None
    index = int(frame["bar_close_at"].searchsorted(at, side="right") - 1)
    return index if index >= 0 else None


def conditioned_gate(
    bundle: Bundle, btc_context: pd.DataFrame, at: pd.Timestamp,
    direction: str, variant: dict[str, Any], strategy: dict[str, Any],
) -> tuple[bool, str | None, dict[str, Any]]:
    features = regime_snapshot(bundle, btc_context, at, direction, strategy)
    reason = classify_snapshot(features, variant)
    return reason is None, reason, features


def regime_snapshot(
    bundle: Bundle, btc_context: pd.DataFrame, at: pd.Timestamp,
    direction: str, strategy: dict[str, Any],
) -> dict[str, Any]:
    symbol_context = bundle.context
    symbol_idx = _asof_index(symbol_context, at)
    btc_idx = _asof_index(btc_context, at)
    lookback = int(strategy["regime_rs_lookback_4h_bars"])
    median_bars = int(strategy["regime_vol_median_4h_bars"])
    min_history = int(strategy["regime_vol_min_history_4h_bars"])
    if symbol_idx is None or btc_idx is None or symbol_idx < lookback or btc_idx < lookback:
        return {"status": "missing", "at": at.isoformat()}

    symbol_row = symbol_context.iloc[symbol_idx]
    btc_row = btc_context.iloc[btc_idx]
    required = ("close", "ema_fast", "ema_slow", "ema_slope_atr", "adx", "atr")
    if any(pd.isna(btc_row.get(key)) for key in required) or any(pd.isna(symbol_row.get(key)) for key in ("close", "atr")):
        return {"status": "incomplete", "at": at.isoformat()}

    btc_close = float(btc_row["close"])
    btc_fast = float(btc_row["ema_fast"])
    btc_slow = float(btc_row["ema_slow"])
    btc_slope = float(btc_row["ema_slope_atr"])
    btc_adx = float(btc_row["adx"])
    aligned = (
        btc_close > btc_slow and btc_fast > btc_slow and btc_slope > 0
        if direction == "long"
        else btc_close < btc_slow and btc_fast < btc_slow and btc_slope < 0
    )
    symbol_return = float(symbol_row["close"]) / float(symbol_context.iloc[symbol_idx - lookback]["close"]) - 1.0
    btc_return = btc_close / float(btc_context.iloc[btc_idx - lookback]["close"]) - 1.0
    rs = symbol_return - btc_return
    directional_rs = rs if direction == "long" else -rs

    atr_pct = float(symbol_row["atr"]) / float(symbol_row["close"])
    start = max(0, symbol_idx - median_bars + 1)
    history = symbol_context.iloc[start:symbol_idx + 1]
    history_atr_pct = history["atr"].astype(float) / history["close"].astype(float)
    valid_history = history_atr_pct.dropna()
    median_atr_pct = float(valid_history.median()) if len(valid_history) >= min_history else 0.0
    vol_ratio = atr_pct / median_atr_pct if median_atr_pct > 0 else None

    return {
        "status": "available", "at": at.isoformat(), "btc_close": btc_close,
        "btc_ema_fast": btc_fast, "btc_ema_slow": btc_slow,
        "btc_slope_atr": btc_slope, "btc_adx": btc_adx,
        "symbol_return_24h": symbol_return, "btc_return_24h": btc_return,
        "relative_strength_24h": rs, "directional_rs_24h": directional_rs,
        "symbol_atr_pct": atr_pct, "symbol_atr_pct_median_30d": median_atr_pct,
        "vol_ratio": vol_ratio, "aligned": aligned,
    }


def classify_snapshot(features: dict[str, Any], variant: dict[str, Any]) -> str | None:
    status = features.get("status")
    if status == "missing":
        return "REGIME_CONTEXT_MISSING"
    if status != "available":
        return "REGIME_CONTEXT_INCOMPLETE"
    if not features.get("aligned"):
        return "BTC_REGIME_NOT_ALIGNED"
    btc_slope = float(features["btc_slope_atr"])
    btc_adx = float(features["btc_adx"])
    if abs(btc_slope) < float(variant["btc_slope_min_atr"]) or btc_adx < float(variant["btc_adx_min"]):
        return "BTC_TREND_STRENGTH_BELOW"
    if float(features["directional_rs_24h"]) * 100.0 < float(variant["rs_24h_min_pct"]):
        return "RELATIVE_STRENGTH_BELOW"
    vol_ratio = features.get("vol_ratio")
    if vol_ratio is None:
        return "VOLATILITY_HISTORY_MISSING"
    if vol_ratio < float(variant["vol_ratio_min"]):
        return "VOLATILITY_COMPRESSED"
    return None
