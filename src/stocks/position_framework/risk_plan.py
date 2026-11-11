"""Risk / stop / exit planning for the Stocks Position Framework (pure math, USD-net oriented).

Long-only, Phase 1. Stops sit BELOW structure (recent swing low) with an ATR buffer, clamped to a
[min, max] ATR-multiple band; too-wide stops are rejected. TP levels store EXACT R multiples (never
a nominal "+1R" label). Sizing is gap-risk-aware. No live orders, no fake fills.
"""
from __future__ import annotations

from typing import Any


def _f(v) -> float | None:
    try:
        return None if v in (None, "") else float(v)
    except (TypeError, ValueError):
        return None


def build_risk_plan(*, entry: float, atr: float, swing_low: float | None,
                    risk_cfg: dict[str, Any], exits_cfg: dict[str, Any],
                    equity_usd: float) -> dict[str, Any]:
    """Return a full risk/exit plan for a long entry. `rejected=True` when the stop is unusable."""
    warnings: list[str] = []
    entry = _f(entry) or 0.0
    atr = _f(atr) or 0.0
    if entry <= 0 or atr <= 0:
        return {"rejected": True, "rejection_reason": "invalid entry/atr", "warnings": warnings}

    min_mult = float(risk_cfg.get("stop_atr_multiple_min", 1.5))
    max_mult = float(risk_cfg.get("stop_atr_multiple_max", 2.5))
    buffer_atr = float(risk_cfg.get("stop_buffer_atr", 0.25))
    gap_mult = float(risk_cfg.get("gap_risk_multiplier", 1.25))
    max_stop_dist_pct = float(risk_cfg.get("reject_if_stop_distance_pct_above", 12))
    paper_risk_pct = float(risk_cfg.get("paper_risk_pct", 0.0025))

    # tightest (closest to entry) and widest (furthest) allowed stop PRICES for a long
    tight_stop = entry - min_mult * atr          # min ATR distance
    wide_stop = entry - max_mult * atr           # max ATR distance

    sl = _f(swing_low)
    if sl is not None and sl > 0:
        structural = sl - buffer_atr * atr
        stop_reason = f"below swing low {sl:.2f} − {buffer_atr}·ATR"
    else:
        structural = wide_stop
        stop_reason = f"no swing low → {max_mult}·ATR below entry"
        warnings.append("no structural swing low available; used ATR stop")

    stop = structural
    if stop > tight_stop:            # too tight (< min ATR) → widen to the min-ATR floor
        stop = tight_stop
        stop_reason += f" (widened to {min_mult}·ATR min)"
    if stop < wide_stop:             # structure beyond max ATR → cap width, flag
        stop = wide_stop
        stop_reason += f" (capped at {max_mult}·ATR max; structure is wider)"
        warnings.append("structural stop beyond max ATR band; capped (structure not fully covered)")

    risk_per_share = entry - stop
    if risk_per_share <= 0:
        return {"rejected": True, "rejection_reason": "non-positive risk per share", "warnings": warnings}
    stop_distance_pct = risk_per_share / entry * 100.0
    rejected = stop_distance_pct > max_stop_dist_pct
    rejection_reason = (f"stop distance {stop_distance_pct:.1f}% > {max_stop_dist_pct}% cap"
                        if rejected else None)

    # gap-aware sizing: inflate per-share risk by gap_mult so the position is smaller
    risk_usd = round(equity_usd * paper_risk_pct, 2)
    eff_risk_per_share = risk_per_share * gap_mult
    qty = risk_usd / eff_risk_per_share if eff_risk_per_share > 0 else 0.0
    notional = qty * entry

    # exits — EXACT R multiples (tp = entry + R·risk_per_share → its R is exactly that multiple)
    p1r = float(exits_cfg.get("partial_1_r", 2.0))
    p2r = float(exits_cfg.get("partial_2_r", 3.0))
    tp1 = entry + p1r * risk_per_share
    tp2 = entry + p2r * risk_per_share
    trail_days = int(exits_cfg.get("trail_ema_days", 21))
    hard_sma = int(exits_cfg.get("hard_exit_below_sma_days", 50))
    max_hold = int(exits_cfg.get("max_holding_days", 40))
    trail_rule = (f"partial {int(exits_cfg.get('partial_1_pct', 0.5)*100)}% @ +{p1r:g}R · "
                  f"partial {int(exits_cfg.get('partial_2_pct', 0.25)*100)}% @ +{p2r:g}R · "
                  f"trail {trail_days}D EMA · hard exit below {hard_sma}D SMA · "
                  f"exit on sector breakdown · max {max_hold} holding days")

    return {
        "rejected": bool(rejected), "rejection_reason": rejection_reason,
        "entry": round(entry, 4), "stop_price": round(stop, 4), "stop_reason": stop_reason,
        "risk_per_share": round(risk_per_share, 4), "stop_distance_pct": round(stop_distance_pct, 3),
        "risk_pct_of_price": round(risk_per_share / entry, 5),
        "risk_usd": risk_usd, "paper_risk_pct": paper_risk_pct,
        "qty": round(qty, 6), "notional_usd": round(notional, 2), "gap_risk_multiplier": gap_mult,
        "tp1": round(tp1, 4), "tp1_r": round(p1r, 4), "tp1_pct": float(exits_cfg.get("partial_1_pct", 0.5)),
        "tp2": round(tp2, 4), "tp2_r": round(p2r, 4), "tp2_pct": float(exits_cfg.get("partial_2_pct", 0.25)),
        "trail_rule": trail_rule, "max_holding_days": max_hold,
        "warnings": warnings,
    }
