"""Maker-first paper execution model (PAPER ONLY).

Chooses per-side order types to reduce fees while staying safe + conservative on
fills (no free maker fills). Default plan: MAKER_WHEN_SAFE_TAKER_WHEN_URGENT.
Stops are always taker (safety). No live, no real orders.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

PLANS = (
    "ALWAYS_TAKER", "MAKER_TP_ONLY", "MAKER_ENTRY_AND_TP", "LIMIT_THEN_TAKER_TIMEOUT",
    "TAKER_ENTRY_MAKER_TP", "MAKER_WHEN_SAFE_TAKER_WHEN_URGENT",
)
_PULLBACK = {"crypto_swing_narrative_rs_momentum", "crypto_failed_bounce_short",
             "stocks_swing_watchlist_rs_rotation"}
_MOMENTUM = {"crypto_intraday_catalyst_or_momentum", "stocks_intraday_rth_momentum",
             "crypto_scalp_momentum"}


@dataclass
class ExecutionPlan:
    plan: str
    entry_order_type: str             # maker | taker
    exit_order_type: str              # representative TP/exit side
    tp_order_type: str
    stop_order_type: str              # always taker
    expired_close_type: str
    maker_fill_status: str            # n/a | maker_filled | maker_missed_taker_fallback
    maker_entry_missed: bool
    maker_tp_filled: bool
    taker_fallback_used: bool
    maker_first_reason: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def plan_for(
    *,
    playbook: str | None = None,
    setup_is_pullback: bool | None = None,
    is_urgent: bool = False,
    reached_tp: bool = False,
    expired: bool = False,
    invalid_or_stale: bool = False,
    maker_entry_touched_again: bool = True,    # conservative: did a later candle trade at the limit?
    tp_level_rested_before_touch: bool = True,  # conservative maker-TP fill rule
    plan: str = "MAKER_WHEN_SAFE_TAKER_WHEN_URGENT",
    entry_timeout_candles: int = 2,
    allow_taker_fallback: bool = True,
) -> ExecutionPlan:
    pb = playbook or ""
    pullback = setup_is_pullback if setup_is_pullback is not None else (pb in _PULLBACK)
    momentum = pb in _MOMENTUM or is_urgent

    # ENTRY: maker for pullback/retest (rests at structure), taker for momentum/chase.
    if plan == "ALWAYS_TAKER":
        entry_ot = "taker"
    elif pullback and not momentum:
        entry_ot = "maker"
    else:
        entry_ot = "taker"

    maker_missed = False
    taker_fallback = False
    fill_status = "n/a"
    if entry_ot == "maker":
        if maker_entry_touched_again:
            fill_status = "maker_filled"
        else:
            maker_missed = True
            if allow_taker_fallback:
                entry_ot = "taker"
                taker_fallback = True
                fill_status = "maker_missed_taker_fallback"
            else:
                fill_status = "maker_missed_no_fill"

    # TP: maker/post-only preferred; only counts as maker fill under the conservative rule.
    tp_ot = "maker" if (reached_tp and tp_level_rested_before_touch) else ("maker" if reached_tp else "taker")
    maker_tp_filled = bool(reached_tp and tp_ot == "maker" and tp_level_rested_before_touch)

    stop_ot = "taker"   # always taker for safety
    expired_ot = "taker" if invalid_or_stale else "maker"
    # representative exit order type for fee accounting
    if expired:
        exit_ot = expired_ot
    elif reached_tp:
        exit_ot = tp_ot
    else:
        exit_ot = stop_ot   # closed by stop

    reason = (f"plan={plan}; entry={'maker(pullback)' if entry_ot=='maker' else 'taker(momentum/urgent)'}; "
              f"TP={'maker' if maker_tp_filled else 'taker'}; stop=taker; "
              f"expired={'maker' if (expired and not invalid_or_stale) else 'taker'}")

    return ExecutionPlan(
        plan=plan, entry_order_type=entry_ot, exit_order_type=exit_ot, tp_order_type=tp_ot,
        stop_order_type=stop_ot, expired_close_type=expired_ot, maker_fill_status=fill_status,
        maker_entry_missed=maker_missed, maker_tp_filled=maker_tp_filled,
        taker_fallback_used=taker_fallback, maker_first_reason=reason,
    )
