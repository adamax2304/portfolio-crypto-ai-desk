"""Tests for the canonical display-status taxonomy (display semantics only).

These assert presentation mapping; they never touch trading logic. They also
guard the two semantics the operator was confused by: `expired` is split by
entry_triggered, and `+0R` is never shown bare for an unresolved expiry.
"""
from __future__ import annotations

import copy

from src.status.display_status import (
    CLOSED_FLAT,
    CLOSED_LOSS,
    CLOSED_WIN,
    ENTERED_UNRESOLVED_EXPIRED,
    NO_ENTRY_EXPIRED,
    OPEN_ACTIVE,
    REVIEW_ONLY_SHADOW,
    WAITING_FOR_ENTRY,
    derive_display_status,
    format_paper_monitor_status,
    format_r_with_lifecycle,
    summarize_display_states,
)


def test_expired_after_entry():
    d = derive_display_status(
        {"status": "expired", "entry_triggered": 1, "tier": "B", "mode": "intraday",
         "asset_class": "crypto", "final_r": 0}
    )
    assert d["display_group"] == ENTERED_UNRESOLVED_EXPIRED
    assert "entered" in d["operator_label"].lower()
    assert d["is_no_entry_miss"] is False
    assert d["is_entered_unresolved"] is True
    # R must NOT imply profit or a flat trade.
    assert d["r_display_policy"] == "unresolved_expiry"
    rs = format_r_with_lifecycle({"status": "expired", "entry_triggered": 1, "final_r": 0,
                                  "tier": "B", "mode": "intraday", "asset_class": "crypto"})
    assert "0R" in rs and "unresolved" in rs.lower()
    assert "flat" not in rs.lower() or "not a flat" in rs.lower()


def test_expired_after_entry_with_authoritative_paper_expiry_is_closed_flat():
    row = {"status": "expired", "entry_triggered": 1, "tier": "B", "mode": "intraday",
           "asset_class": "crypto", "final_r": 0, "final_outcome": "expired",
           "paper_execution_r": 0.0, "paper_execution_outcome": "expired",
           "paper_close_reason": "expired_flat"}
    d = derive_display_status(row)
    assert d["display_group"] == CLOSED_FLAT
    assert d["paper_outcome_authoritative"] is True
    assert d["display_r_source"] == "paper execution"
    assert format_r_with_lifecycle(row) == "CLOSED FLAT 0R"


def test_legacy_ambiguous_is_reconciled_by_authoritative_paper_breakeven():
    d = derive_display_status({
        "status": "ambiguous", "entry_triggered": 1, "tier": "C", "mode": "intraday",
        "asset_class": "stocks", "final_r": -1.0, "final_outcome": "ambiguous",
        "paper_execution_r": 0.0, "paper_execution_outcome": "breakeven",
        "paper_close_reason": "breakeven_stop",
    })
    assert d["display_group"] == CLOSED_FLAT
    assert "paper execution" in d["display_reason"]


def test_expired_legacy_status_can_be_closed_win_by_paper_protection():
    d = derive_display_status({
        "status": "expired", "entry_triggered": 1, "tier": "C", "mode": "invest",
        "asset_class": "stocks", "final_r": 0.0, "final_outcome": "expired",
        "paper_execution_r": 0.5, "paper_execution_outcome": "win",
        "paper_close_reason": "profit_lock_stop",
    })
    assert d["display_group"] == CLOSED_WIN
    assert "+0.5R (paper execution)" in d["operator_label"]


def test_stale_before_entry_no_touch():
    d = derive_display_status(
        {"status": "stale_before_entry", "entry_triggered": 0, "tier": "B",
         "mode": "swing", "asset_class": "stocks"}
    )
    assert d["display_group"] == NO_ENTRY_EXPIRED
    assert "stale" in d["display_reason"].lower()
    assert d["is_no_entry_miss"] is True


def test_entry_moved_away():
    d = derive_display_status(
        {"status": "entry_moved_away", "entry_triggered": 0, "tier": "B",
         "mode": "scalp", "asset_class": "crypto"}
    )
    assert d["display_group"] == NO_ENTRY_EXPIRED
    assert "moved away" in d["display_reason"].lower() or "ran away" in d["display_reason"].lower()


def test_waiting_actionable():
    d = derive_display_status(
        {"status": "waiting_for_entry", "entry_triggered": 0, "tier": "A",
         "mode": "intraday", "asset_class": "crypto"}
    )
    assert d["display_group"] == WAITING_FOR_ENTRY
    assert d["is_waiting_for_entry"] is True
    assert d["should_show_in_waiting_monitor"] is True


def test_stock_swing_event_rs_waiting_is_actionable():
    d = derive_display_status(
        {"status": "waiting_for_entry", "entry_triggered": 0, "tier": "B",
         "mode": "swing", "asset_class": "stocks",
         "raw_idea_json": '{"paper_entry_profile":"stocks_swing_event_rs_pullback_flow_paper_v1"}'}
    )
    assert d["display_group"] == WAITING_FOR_ENTRY
    assert d["is_actionable"] is True
    assert d["is_shadow_or_review"] is False


def test_c_tier_review_only_not_active():
    d = derive_display_status(
        {"status": "waiting_for_entry", "entry_triggered": 0, "tier": "C",
         "mode": "intraday", "asset_class": "stocks"}
    )
    assert d["display_group"] == REVIEW_ONLY_SHADOW
    assert d["is_active_for_operator"] is False
    assert d["should_show_in_active_monitor"] is False
    assert d["is_shadow_or_review"] is True


def test_crypto_scalp_is_shadow():
    d = derive_display_status(
        {"status": "triggered", "entry_triggered": 1, "tier": "B",
         "mode": "scalp", "asset_class": "crypto"}
    )
    assert d["display_group"] == REVIEW_ONLY_SHADOW
    assert d["is_active_for_operator"] is False


def test_stopped_loss():
    d = derive_display_status(
        {"status": "stopped", "entry_triggered": 1, "tier": "B", "mode": "intraday",
         "asset_class": "crypto", "final_r": -1.0, "final_outcome": "loss"}
    )
    assert d["display_group"] == CLOSED_LOSS
    assert "-1.0R" in d["operator_label"]


def test_tp_win():
    d = derive_display_status(
        {"status": "tp3_hit", "entry_triggered": 1, "tier": "B", "mode": "intraday",
         "asset_class": "crypto", "final_r": 2.4, "final_outcome": "win"}
    )
    assert d["display_group"] == CLOSED_WIN
    assert "+2.4R" in d["operator_label"]


def test_true_flat_close():
    d = derive_display_status(
        {"status": "tp1_hit", "entry_triggered": 1, "tier": "B", "mode": "intraday",
         "asset_class": "crypto", "final_r": 0.0, "final_outcome": "win"}
    )
    # final_outcome present + final_r==0 → genuine flat close (not expiry).
    assert d["display_group"] == CLOSED_FLAT
    assert d["r_display_policy"] == "terminal_flat"


def test_inconsistent_no_entry_but_triggered():
    d = derive_display_status(
        {"status": "stale_before_entry", "entry_triggered": 1, "tier": "B",
         "mode": "intraday", "asset_class": "crypto"}
    )
    assert d["display_group"] == "UNKNOWN_INCONSISTENT"


def test_invalid_paper_session_overrides_late_legacy_tp_label():
    d = derive_display_status({
        "status": "tp2_hit", "entry_triggered": 0, "tier": "B", "mode": "intraday",
        "asset_class": "stocks", "final_outcome": "not_triggered", "final_r": 0.0,
        "paper_execution_outcome": "invalid_session",
        "paper_close_reason": "invalid_stock_intraday_entry_not_point_in_time",
    })
    assert d["display_group"] == "NO_ENTRY_EXPIRED"
    assert "invalidated before execution" in d["display_reason"]


def test_telegram_summary_not_just_no_active():
    rows = [
        {"symbol": "AAA", "status": "waiting_for_entry", "entry_triggered": 0, "tier": "A",
         "mode": "intraday", "asset_class": "crypto"},
        {"symbol": "BBB", "status": "waiting_for_entry", "entry_triggered": 0, "tier": "C",
         "mode": "intraday", "asset_class": "stocks"},
    ]
    msg = format_paper_monitor_status(rows)
    assert "Open actionable: 0" in msg
    # Must NOT be a bare "no active trades" — must mention waiting/review.
    assert "waiting" in msg.lower()
    assert "review/shadow" in msg.lower()


def test_telegram_expired_split_not_single_count():
    rows = [
        {"symbol": "ETH", "status": "expired", "entry_triggered": 1, "tier": "B",
         "mode": "scalp", "asset_class": "crypto"},  # entered-unresolved (shadow scalp, but expired wins precedence)
        {"symbol": "SUI", "status": "stale_before_entry", "entry_triggered": 0, "tier": "B",
         "mode": "intraday", "asset_class": "crypto"},  # no-entry
    ]
    msg = format_paper_monitor_status(rows)
    assert "Expired after entry" in msg
    assert "No-entry / stale / moved-away" in msg
    # never a single raw "Expired: N" line
    assert "Expired: 2" not in msg


def test_missing_fields_do_not_crash():
    # Control-Plane-ish row with almost nothing.
    d = derive_display_status({})
    assert d["display_group"] in {"UNKNOWN_INCONSISTENT"}
    assert d["entry_touched"] == "unknown"
    assert d["is_actionable"] == "unknown"


def test_mapping_does_not_mutate_input():
    row = {"status": "expired", "entry_triggered": 1, "tier": "B", "mode": "intraday",
           "asset_class": "crypto", "final_r": 0}
    snapshot = copy.deepcopy(row)
    derive_display_status(row)
    summarize_display_states([row])
    assert row == snapshot, "display layer must never mutate the input row"


def test_win_label_with_negative_r_is_not_closed_win():
    # final_outcome=win but final_r=-1 → must NOT be CLOSED_WIN (no "+-1.0R").
    d = derive_display_status(
        {"status": "tp1_hit", "entry_triggered": 1, "tier": "B", "mode": "intraday",
         "asset_class": "crypto", "final_outcome": "win", "final_r": -1.0}
    )
    assert d["display_group"] in {"UNKNOWN_INCONSISTENT", CLOSED_LOSS}
    assert d["display_group"] != CLOSED_WIN
    assert "+-" not in d["operator_label"]


def test_loss_label_with_positive_r_is_not_closed_loss():
    d = derive_display_status(
        {"status": "stopped", "entry_triggered": 1, "tier": "B", "mode": "intraday",
         "asset_class": "crypto", "final_outcome": "loss", "final_r": 1.0}
    )
    assert d["display_group"] in {"UNKNOWN_INCONSISTENT", CLOSED_WIN}
    assert d["display_group"] != CLOSED_LOSS


def test_no_double_sign_in_labels_and_r():
    win = derive_display_status({"status": "tp3_hit", "entry_triggered": 1, "tier": "B",
                                 "mode": "intraday", "asset_class": "crypto",
                                 "final_outcome": "win", "final_r": 1.0})
    loss = derive_display_status({"status": "stopped", "entry_triggered": 1, "tier": "B",
                                  "mode": "intraday", "asset_class": "crypto",
                                  "final_outcome": "loss", "final_r": -1.0})
    assert win["operator_label"] == "✅ CLOSED WIN +1.0R (legacy touch)"
    assert loss["operator_label"] == "🔴 CLOSED LOSS -1.0R (legacy touch)"
    assert "+-" not in win["operator_label"] and "+-" not in loss["operator_label"]


def test_no_double_sign_in_telegram_output():
    # rows that previously produced "✅ CLOSED WIN +-1.0R"
    rows = [
        {"symbol": "X", "status": "tp1_hit", "entry_triggered": 1, "tier": "B",
         "mode": "intraday", "asset_class": "crypto", "final_outcome": "win", "final_r": -1.0},
        {"symbol": "Y", "status": "stopped", "entry_triggered": 1, "tier": "B",
         "mode": "intraday", "asset_class": "crypto", "final_outcome": "loss", "final_r": -1.0},
        {"symbol": "Z", "status": "tp3_hit", "entry_triggered": 1, "tier": "B",
         "mode": "intraday", "asset_class": "crypto", "final_outcome": "win", "final_r": 2.0},
    ]
    msg = format_paper_monitor_status(rows)
    assert "+-" not in msg


def test_summary_counts():
    rows = [
        {"status": "expired", "entry_triggered": 1, "tier": "B", "mode": "intraday", "asset_class": "crypto"},
        {"status": "stale_before_entry", "entry_triggered": 0, "tier": "B", "mode": "intraday", "asset_class": "crypto"},
        {"status": "waiting_for_entry", "entry_triggered": 0, "tier": "A", "mode": "intraday", "asset_class": "crypto"},
        {"status": "stopped", "entry_triggered": 1, "tier": "B", "mode": "intraday", "asset_class": "crypto", "final_r": -1, "final_outcome": "loss"},
    ]
    s = summarize_display_states(rows)
    assert s["expired_after_entry_count"] == 1
    assert s["no_entry_expired_count"] == 1
    assert s["waiting_for_entry_count"] == 1
    assert s["closed_loss_count"] == 1
