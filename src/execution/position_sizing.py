"""Paper position sizing + SAFE 2x leverage policy (PAPER / ACCOUNTING ONLY).

KEY PRINCIPLE: **leverage does NOT define risk.** Risk = stop distance × position
size. Leverage only sets the margin requirement and the liquidation distance. The
engine picks the MINIMUM leverage needed to keep margin within the cap, clamped at
`max_leverage` (default 2). If 0.5% risk cannot fit under the caps, the position is
REDUCED (risk_capped) — never levered up.

Why max 2x: 2x liquidation (~50% adverse) is far from any normal technical stop
(0.5–8%), so there is no liquidation risk and no fake leverage edge. If a setup
only "works" at 5x it is not robust.

No real orders, no exchange calls, no production TP/SL change.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class SizingResult:
    target_risk_usdt: float
    actual_risk_usdt: float
    actual_risk_pct: float
    risk_utilization_pct: float            # actual_risk / target_risk
    qty: float
    desired_notional_usdt: float
    capped_notional_usdt: float
    notional_usdt: float
    margin_used_usdt: float
    leverage_used: int
    leverage_policy: str
    leverage_reason: str
    margin_cap_reason: str | None
    stop_distance_pct: float
    liquidation_price: float | None
    liquidation_buffer_distance_pct: float
    liquidation_buffer_ok: bool
    liquidation_buffer_fail: bool
    skip_recommended: bool
    risk_capped: bool
    too_tight_stop: bool
    too_wide_stop: bool
    sizing_warning: str | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _empty(target_risk: float, policy: str, warn: str) -> SizingResult:
    return SizingResult(
        target_risk_usdt=target_risk, actual_risk_usdt=0.0, actual_risk_pct=0.0,
        risk_utilization_pct=0.0, qty=0.0, desired_notional_usdt=0.0,
        capped_notional_usdt=0.0, notional_usdt=0.0, margin_used_usdt=0.0,
        leverage_used=1, leverage_policy=policy, leverage_reason="no position",
        margin_cap_reason=None, stop_distance_pct=0.0, liquidation_price=None,
        liquidation_buffer_distance_pct=0.0, liquidation_buffer_ok=True,
        liquidation_buffer_fail=False, skip_recommended=True,
        risk_capped=True, too_tight_stop=False, too_wide_stop=False, sizing_warning=warn)


def size_position(
    *,
    equity_usdt: float,
    entry_price: float,
    stop_price: float,
    direction: str = "long",
    risk_pct: float = 0.005,
    max_leverage: int = 5,
    max_margin_pct: float = 0.25,
    max_notional_pct: float = 1.50,
    liquidation_buffer_to_stop: float = 3.0,
    leverage_policy: str = "max_5x_safe",
    too_tight_stop_pct: float = 0.0035,
    too_wide_stop_pct: float = 0.08,
    risk_capped_threshold: float = 0.8,
    skip_if_liquidation_too_close: bool = True,
) -> SizingResult:
    long = str(direction).lower() != "short"
    target_risk = round(equity_usdt * risk_pct, 4)
    stop_dist = abs(entry_price - stop_price)
    if entry_price <= 0 or stop_dist <= 0:
        return _empty(target_risk, leverage_policy, "invalid geometry (entry<=0 or stop==entry)")
    stop_dist_pct = stop_dist / entry_price
    too_tight = stop_dist_pct < too_tight_stop_pct
    too_wide = stop_dist_pct > too_wide_stop_pct

    max_margin_usdt = equity_usdt * max_margin_pct
    notional_cap = min(max_margin_usdt * max_leverage, equity_usdt * max_notional_pct)
    cap_reason = ("max_notional_pct" if equity_usdt * max_notional_pct <= max_margin_usdt * max_leverage
                  else "max_margin_x_leverage")

    desired_notional = target_risk / stop_dist_pct
    notional = min(desired_notional, notional_cap)
    risk_capped = notional < desired_notional - 1e-9

    qty = notional / entry_price
    actual_risk = qty * stop_dist
    actual_risk_pct = actual_risk / equity_usdt if equity_usdt else 0.0
    risk_util = actual_risk / target_risk if target_risk else 0.0
    if risk_util < risk_capped_threshold:
        risk_capped = True

    leverage_used = max(1, math.ceil(notional / max_margin_usdt - 1e-9)) if max_margin_usdt > 0 else max_leverage
    leverage_used = min(leverage_used, max_leverage)

    # LIQUIDATION SAFETY: liq distance (1/leverage) must be >= buffer × stop distance.
    # If it isn't, cap leverage to the safe maximum and REDUCE notional to fit (never
    # widen risk). skip_recommended only if even 1x can't clear the buffer (stop ~>33%).
    liq_buffer_fail = False
    skip_recommended = False
    safe_lev_cap = int(1.0 / (stop_dist_pct * liquidation_buffer_to_stop)) if stop_dist_pct > 0 else max_leverage
    if safe_lev_cap < 1:
        skip_recommended = True
        liq_buffer_fail = True
    elif leverage_used > safe_lev_cap:
        liq_buffer_fail = True
        leverage_used = max(1, min(leverage_used, safe_lev_cap))
        notional = min(notional, max_margin_usdt * leverage_used)
        qty = notional / entry_price
        actual_risk = qty * stop_dist
        actual_risk_pct = actual_risk / equity_usdt if equity_usdt else 0.0
        risk_util = actual_risk / target_risk if target_risk else 0.0
        if risk_util < risk_capped_threshold:
            risk_capped = True
    margin_used = notional / leverage_used if leverage_used else notional

    liq_dist_pct = 1.0 / leverage_used
    liq_buffer_ok = liq_dist_pct >= stop_dist_pct * liquidation_buffer_to_stop
    liq_price = entry_price * (1.0 - liq_dist_pct) if long else entry_price * (1.0 + liq_dist_pct)
    if liq_buffer_fail and skip_if_liquidation_too_close and skip_recommended:
        skip_recommended = True

    lev_reason = (f"min leverage for margin cap (ceil {notional:.0f}/{max_margin_usdt:.0f}), "
                  f"clamped <= {max_leverage}x ({leverage_policy})"
                  + (f"; reduced to {leverage_used}x for liq buffer ({liquidation_buffer_to_stop}× stop)"
                     if liq_buffer_fail and not skip_recommended else ""))
    warn = None
    if skip_recommended:
        warn = (f"liquidation too close: stop {stop_dist_pct*100:.1f}% × {liquidation_buffer_to_stop} "
                f"exceeds even 1x liq distance — skip")
    elif risk_capped:
        warn = (f"risk capped: stop {stop_dist_pct*100:.2f}% → notional hit cap {notional_cap:.0f} "
                f"({cap_reason}); actual risk {actual_risk:.2f} < target {target_risk:.2f} "
                f"({risk_util*100:.0f}% of target)")
    elif too_tight:
        warn = f"stop very tight ({stop_dist_pct*100:.2f}% < {too_tight_stop_pct*100:.2f}%) — fees will dominate"
    elif too_wide:
        warn = f"stop wide ({stop_dist_pct*100:.1f}% > {too_wide_stop_pct*100:.0f}%) — small position / maybe not intraday"
    elif not liq_buffer_ok:
        warn = f"liquidation buffer thin: liq {liq_dist_pct*100:.0f}% vs {liquidation_buffer_to_stop}x stop"

    return SizingResult(
        target_risk_usdt=round(target_risk, 4), actual_risk_usdt=round(actual_risk, 4),
        actual_risk_pct=round(actual_risk_pct, 6), risk_utilization_pct=round(risk_util, 4),
        qty=round(qty, 10), desired_notional_usdt=round(desired_notional, 4),
        capped_notional_usdt=round(notional_cap, 4), notional_usdt=round(notional, 4),
        margin_used_usdt=round(margin_used, 4), leverage_used=int(leverage_used),
        leverage_policy=leverage_policy, leverage_reason=lev_reason,
        margin_cap_reason=cap_reason if risk_capped else None,
        stop_distance_pct=round(stop_dist_pct, 6), liquidation_price=round(liq_price, 10),
        liquidation_buffer_distance_pct=round(liq_dist_pct, 6), liquidation_buffer_ok=bool(liq_buffer_ok),
        liquidation_buffer_fail=bool(liq_buffer_fail), skip_recommended=bool(skip_recommended),
        risk_capped=bool(risk_capped), too_tight_stop=bool(too_tight), too_wide_stop=bool(too_wide),
        sizing_warning=warn,
    )
