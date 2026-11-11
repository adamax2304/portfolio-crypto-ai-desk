"""Fee-aware paper execution filter/adjuster (PAPER ONLY).

Quantifies, per paper trade, how much of the risk the round-trip costs eat
(`fee_r_cost`), the break-even move, the minimum viable TP1, and a survival
label. Drives a paper-only skip/cap/warn decision. No live, no production change.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

from src.execution.fees import trade_costs


@dataclass
class FeeAware:
    fee_profile: str
    fee_r_cost: float                 # round-trip cost / risk_usdt
    break_even_move_pct: float
    min_viable_tp1_r: float
    fee_drag_pct_of_gross: float | None
    expected_net_edge_r: float | None
    fee_survival_label: str           # OK | HIGH_FEE_DRAG | EXTREME_FEE_DRAG | FEE_SURVIVAL_FAIL | TP1_NOT_WORTH_FEES | TIGHT_STOP_FEE_DRAG | EXCHANGE_SENSITIVE
    action: str                        # ok | warn_and_cap | paper_skipped_fee_drag
    reasons: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def assess_fees(
    *,
    notional_usdt: float,
    exit_notional_usdt: float | None,
    risk_usdt: float,
    symbol: str = "",
    fee_profile: str = "bybit_non_vip_usdt_perp",
    entry_order_type: str = "taker",
    exit_order_type: str = "taker",
    slip_cfg: dict | None = None,
    majors: list | None = None,
    tp1_r: float | None = None,
    stop_distance_pct: float | None = None,
    expected_gross_r: float | None = None,
    max_fee_r_cost: float = 0.35,
    skip_extreme_fee_drag: bool = True,
    skip_fail_fee_survival: bool = False,
) -> FeeAware:
    cost = trade_costs(notional_usdt=notional_usdt, exit_notional_usdt=exit_notional_usdt,
                       symbol=symbol, fee_profile=fee_profile, entry_order_type=entry_order_type,
                       exit_order_type=exit_order_type, slip_cfg=slip_cfg, majors=majors)
    fee_r = round(cost.total_cost_usdt / risk_usdt, 4) if risk_usdt > 0 else 999.0
    be_move = round((cost.total_cost_usdt / notional_usdt) if notional_usdt > 0 else 0.0, 6)
    min_tp1 = round(fee_r + 0.30, 3)   # need to clear costs + a margin
    reasons: list[str] = []
    label = "OK"
    if fee_r > 0.20:
        label = "HIGH_FEE_DRAG"
    if fee_r > max_fee_r_cost:
        label = "EXTREME_FEE_DRAG"
        reasons.append(f"fee_r_cost {fee_r} > {max_fee_r_cost}")
    if tp1_r is not None and tp1_r <= fee_r + 0.30:
        label = "TP1_NOT_WORTH_FEES"
        reasons.append(f"TP1 {tp1_r}R <= fees+0.3R ({min_tp1}R)")
    if stop_distance_pct is not None and stop_distance_pct < 0.0035 and fee_r > 0.20:
        label = "TIGHT_STOP_FEE_DRAG"
        reasons.append(f"tight stop {stop_distance_pct*100:.2f}% inflates notional/fees")
    net_edge = round(expected_gross_r - fee_r, 4) if expected_gross_r is not None else None
    drag = round(cost.total_cost_usdt / abs(expected_gross_r * risk_usdt), 4) \
        if (expected_gross_r and risk_usdt and expected_gross_r > 0) else None
    if net_edge is not None and net_edge <= 0:
        label = "FEE_SURVIVAL_FAIL"
        reasons.append(f"expected net edge {net_edge}R <= 0 after fees")

    action = "ok"
    if label in ("EXTREME_FEE_DRAG", "TIGHT_STOP_FEE_DRAG") and skip_extreme_fee_drag:
        action = "paper_skipped_fee_drag"
    elif label == "FEE_SURVIVAL_FAIL" and skip_fail_fee_survival:
        action = "paper_skipped_fee_drag"
    elif label != "OK":
        action = "warn_and_cap"

    return FeeAware(cost.fee_profile, fee_r, be_move, min_tp1, drag, net_edge,
                    label, action, reasons)
