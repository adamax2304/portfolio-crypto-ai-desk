from __future__ import annotations

from src.execution.paper_entry_mode_policy import (
    disabled_shadow_reason,
    paper_promotion_reason,
)
from src.execution.paper_execution_accounting import build_record_from_signal


def test_entry_mode_policy_disables_requested_shadow_slices():
    assert disabled_shadow_reason(
        asset_class="crypto", trade_mode="scalp", entry_mode="BREAKOUT_CONTINUATION"
    )
    assert disabled_shadow_reason(
        asset_class="crypto", trade_mode="intraday", entry_mode="PULLBACK_LIMIT"
    )
    assert disabled_shadow_reason(
        asset_class="crypto", trade_mode="swing", entry_mode="LIMIT_THEN_TAKER_TIMEOUT"
    )
    assert disabled_shadow_reason(
        asset_class="stocks", trade_mode="intraday", entry_mode="MOMENTUM_TAKER_NOW"
    )
    assert disabled_shadow_reason(
        asset_class="stocks", trade_mode="intraday", entry_mode="LIMIT_THEN_TAKER_TIMEOUT"
    )


def test_entry_mode_policy_promotes_only_stock_intraday_pullback_and_breakout():
    assert paper_promotion_reason(
        asset_class="stocks", trade_mode="intraday", entry_mode="PULLBACK_LIMIT"
    )
    assert paper_promotion_reason(
        asset_class="stocks", trade_mode="intraday", entry_mode="BREAKOUT_CONTINUATION"
    )
    assert paper_promotion_reason(
        asset_class="crypto", trade_mode="intraday", entry_mode="BREAKOUT_CONTINUATION"
    ) is None
    assert paper_promotion_reason(
        asset_class="stocks", trade_mode="intraday", entry_mode="MOMENTUM_TAKER_NOW"
    ) is None


def test_paper_accounting_uses_actual_entry_price_when_present():
    sid, _key, rec = build_record_from_signal(
        {
            "signal_id": "sig_policy_entry",
            "symbol": "AAPL",
            "asset_class": "stocks",
            "mode": "intraday",
            "direction": "long",
            "tier": "B",
            "setup_type": "breakout",
            "created_at": "2026-07-07T13:30:00+00:00",
            "entry_trigger": 100.0,
            "suggested_entry": 100.0,
            "entry_low": 99.0,
            "invalidation": 98.0,
            "tp1": 104.0,
            "tp2": 106.0,
            "tp3": 108.0,
        },
        {
            "entry_triggered": 1,
            "entry_triggered_at": "2026-07-07T13:45:00+00:00",
            "entry_price_used": 102.0,
            "tp1_hit": 1,
            "tp2_hit": 0,
            "tp3_hit": 0,
            "stop_hit": 0,
            "final_outcome": "win",
            "max_favorable_excursion_r": 0.8,
        },
    )
    assert sid == "sig_policy_entry"
    # With entry_price_used=102 and stop=98, TP1=104 is +0.5R.
    # If the old 100 anchor were used, it would be +1.0R.
    assert rec["touch_r"] == 0.5
