"""Position / leverage ADVISOR — label-only (operational deploy PART 7).

Shows the operator a recommended notional + a safe-leverage estimate derived from
stop distance and a risk budget. It is NOT execution, NOT auto-sizing, NOT auto-
leverage. It never places an order, never calls an exchange, never changes
`size_weight`. Every output carries `diagnostic_only=True`.

Model (deliberately simple + conservative):
  risk_usd            = equity * risk_pct
  stop_distance_pct   = |entry - stop| / entry * 100
  suggested_notional  = risk_usd / (stop_distance_pct / 100)
  liq_move_pct(L)     ≈ 100 / L                 (isolated-margin approximation)
  max_safe_leverage   = min(max_leverage, floor( 100 / (stop_distance_pct * (1 + buffer)) ))
A position is flagged UNSAFE if the stop is invalid, the liquidation buffer cannot be
met even at 1x, or reaching the suggested notional would require leverage above the
safe estimate.
"""
from __future__ import annotations

import math
from typing import Any

DEFAULT_ASSUMED_EQUITY = 10_000.0
DEFAULT_RISK_PCTS = (0.25, 0.5, 1.0)
DEFAULT_MAX_LEVERAGE = 10.0
DEFAULT_LIQ_BUFFER_MIN_PCT = 30.0  # liquidation must sit ≥30% beyond the stop


def _unknown(reason: str) -> dict[str, Any]:
    return {
        "position_advisor_status": "unknown",
        "position_advisor_reason": reason,
        "risk_budget_usd": None,
        "stop_distance_pct": None,
        "suggested_notional": None,
        "suggested_margin_at_1x": None,
        "suggested_margin_at_2x": None,
        "suggested_margin_at_3x": None,
        "suggested_margin_at_5x": None,
        "max_safe_leverage_estimate": None,
        "leverage_warning": None,
        "capital_efficiency_note": None,
        "by_risk_pct": [],
        "diagnostic_only": True,
    }


def position_leverage_advice(
    *,
    entry: float | None,
    stop: float | None,
    equity: float | None = None,
    risk_pcts: tuple[float, ...] = DEFAULT_RISK_PCTS,
    max_leverage: float = DEFAULT_MAX_LEVERAGE,
    liq_buffer_min_pct: float = DEFAULT_LIQ_BUFFER_MIN_PCT,
    atr: float | None = None,
    mode: str | None = None,
    tier: str | None = None,
    volatility_haircut: float = 1.0,
) -> dict[str, Any]:
    """Return a label-only sizing/leverage advisory. Fails to `unknown` on bad
    inputs. Pure — no side effects, no order, no exchange call."""
    try:
        if entry is None or stop is None:
            return _unknown("missing entry/stop")
        entry = float(entry)
        stop = float(stop)
        if entry <= 0 or stop <= 0 or entry == stop:
            return _unknown("invalid entry/stop")
        equity = float(equity) if equity is not None else DEFAULT_ASSUMED_EQUITY

        stop_distance_pct = abs(entry - stop) / entry * 100.0
        if stop_distance_pct <= 0:
            return _unknown("zero stop distance")

        # max safe leverage so the stop triggers well before liquidation
        buffer_frac = 1.0 + (liq_buffer_min_pct / 100.0)
        raw_safe = 100.0 / (stop_distance_pct * buffer_frac)
        max_safe_leverage = min(max_leverage, math.floor(raw_safe))
        # volatility haircut (optional): wider ATR → trim safe leverage
        if atr and entry and atr > 0:
            atr_pct = atr / entry * 100.0
            if atr_pct > stop_distance_pct:
                max_safe_leverage = max(1, math.floor(max_safe_leverage * volatility_haircut * 0.5))

        unsafe = max_safe_leverage < 1
        by_risk = []
        for rp in risk_pcts:
            risk_usd = equity * rp / 100.0
            notional = risk_usd / (stop_distance_pct / 100.0)
            req_lev = notional / equity if equity else None
            row = {
                "risk_pct": rp,
                "risk_budget_usd": round(risk_usd, 2),
                "suggested_notional": round(notional, 2),
                "required_leverage_full_equity": round(req_lev, 2) if req_lev else None,
                "exceeds_safe_leverage": bool(req_lev and not unsafe and req_lev > max_safe_leverage),
            }
            by_risk.append(row)

        # headline = the 0.5% (middle) risk budget, or the first available
        head = next((r for r in by_risk if r["risk_pct"] == 0.5), by_risk[0])
        notional = head["suggested_notional"]

        if unsafe:
            warning = (f"UNSAFE: stop {stop_distance_pct:.2f}% too tight for a "
                       f"{liq_buffer_min_pct:.0f}% liquidation buffer at any leverage ≤ {max_leverage:g}x")
            status = "unsafe"
        elif head["exceeds_safe_leverage"]:
            warning = (f"tight stop ({stop_distance_pct:.2f}%) → reaching notional needs "
                       f"{head['required_leverage_full_equity']:.1f}x > max safe {max_safe_leverage:g}x")
            status = "warning"
        else:
            warning = None
            status = "ok"

        return {
            "position_advisor_status": status,
            "position_advisor_reason": "",
            "risk_budget_usd": head["risk_budget_usd"],
            "stop_distance_pct": round(stop_distance_pct, 3),
            "suggested_notional": notional,
            "suggested_margin_at_1x": round(notional / 1.0, 2),
            "suggested_margin_at_2x": round(notional / 2.0, 2),
            "suggested_margin_at_3x": round(notional / 3.0, 2),
            "suggested_margin_at_5x": round(notional / 5.0, 2),
            "max_safe_leverage_estimate": max_safe_leverage,
            "leverage_warning": warning,
            "capital_efficiency_note": (
                f"notional ≈ {notional / equity:.1f}x equity (assumed equity ${equity:,.0f})"
                if equity else None),
            "by_risk_pct": by_risk,
            "diagnostic_only": True,
        }
    except Exception:
        return _unknown("computation error")


def advisor_line(adv: dict[str, Any]) -> str | None:
    """Compact Telegram line, or None if not useful."""
    if not adv or adv.get("position_advisor_status") == "unknown":
        return None
    sd = adv.get("stop_distance_pct")
    notion = adv.get("suggested_notional")
    lev = adv.get("max_safe_leverage_estimate")
    base = (f"Position advisor: stop {sd:.2f}%, risk 0.5% → notional ~${notion:,.0f}, "
            f"max safe leverage {lev:g}x — diagnostic only")
    if adv.get("leverage_warning"):
        base += f" · {adv['leverage_warning']}"
    return base
