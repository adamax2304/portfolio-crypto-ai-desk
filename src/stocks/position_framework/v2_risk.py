"""Pure risk and exit planning for Stocks Position Swing V2."""
from __future__ import annotations

from typing import Any


def _f(value: Any) -> float | None:
    try:
        return None if value in (None, "") else float(value)
    except (TypeError, ValueError):
        return None


def build_plan(
    *,
    entry: float,
    atr: float,
    structural_low: float,
    size_weight: float,
    risk_cfg: dict[str, Any],
    exits_cfg: dict[str, Any],
) -> dict[str, Any]:
    entry = _f(entry) or 0.0
    atr = _f(atr) or 0.0
    structural_low = _f(structural_low) or 0.0
    if entry <= 0 or atr <= 0 or structural_low <= 0 or structural_low >= entry:
        return {"rejected": True, "reason": "INVALID_ENTRY_ATR_OR_STRUCTURE"}

    stop_min_atr = float(risk_cfg.get("stop_atr_min", 1.0))
    stop_max_atr = float(risk_cfg.get("stop_atr_max", 2.5))
    buffer_atr = float(risk_cfg.get("stop_buffer_atr", 0.25))
    structural_stop = structural_low - buffer_atr * atr
    min_distance_stop = entry - stop_min_atr * atr
    stop = min(structural_stop, min_distance_stop)
    risk_per_share = entry - stop
    risk_atr = risk_per_share / atr
    stop_pct = risk_per_share / entry * 100.0

    if risk_atr > stop_max_atr:
        return {
            "rejected": True,
            "reason": "STRUCTURAL_STOP_TOO_WIDE",
            "risk_atr": round(risk_atr, 4),
        }
    if stop_pct > float(risk_cfg.get("max_stop_distance_pct", 12)):
        return {
            "rejected": True,
            "reason": "STOP_DISTANCE_PCT_TOO_WIDE",
            "stop_distance_pct": round(stop_pct, 4),
        }

    equity = float(risk_cfg.get("paper_equity_usd", 5000))
    risk_pct = float(risk_cfg.get("risk_pct", 0.0025))
    gap_mult = float(risk_cfg.get("gap_risk_multiplier", 1.25))
    size_weight = max(0.0, min(1.0, float(size_weight)))
    risk_usd = equity * risk_pct * size_weight
    effective_risk_per_share = risk_per_share * gap_mult
    qty = risk_usd / effective_risk_per_share if effective_risk_per_share > 0 else 0.0

    tp1_r = float(exits_cfg.get("tp1_r", 2.0))
    tp2_r = float(exits_cfg.get("tp2_r", 3.0))
    return {
        "rejected": False,
        "entry_price": round(entry, 6),
        "stop_price": round(stop, 6),
        "structural_low": round(structural_low, 6),
        "risk_per_share": round(risk_per_share, 6),
        "risk_atr": round(risk_atr, 4),
        "stop_distance_pct": round(stop_pct, 4),
        "risk_usd": round(risk_usd, 2),
        "risk_pct": risk_pct,
        "size_weight": size_weight,
        "qty": round(qty, 8),
        "gap_risk_multiplier": gap_mult,
        "tp1": round(entry + tp1_r * risk_per_share, 6),
        "tp1_r": tp1_r,
        "tp1_pct": float(exits_cfg.get("tp1_pct", 0.5)),
        "tp2": round(entry + tp2_r * risk_per_share, 6),
        "tp2_r": tp2_r,
        "tp2_pct": float(exits_cfg.get("tp2_pct", 0.25)),
        "trail_ema_days": int(exits_cfg.get("trail_ema_days", 21)),
        "hard_exit_sma_days": int(exits_cfg.get("hard_exit_sma_days", 50)),
        "max_holding_days": int(exits_cfg.get("max_holding_days", 40)),
    }
