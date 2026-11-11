from __future__ import annotations

import sqlite3

import pandas as pd

from scripts import crypto_swing_entry_sweep as sweep


def _row(action: str = "FULL_SIZE") -> dict:
    return {
        "quality_action": action,
        "quality_reasons_json": "symbol_cooldown" if action == "HALF_SIZE" else "",
        "latency_cause": "FAST",
        "data_gap_min": 10.0,
        "direction": "long",
        "ref_close": 100.0,
        "atr": 2.0,
        "tp1": 102.0,
        "tp2": 104.0,
        "tp3": 106.0,
    }


def test_shadow_target_variants_keep_native_control_and_t140_is_not_production():
    control = sweep._shadow_legacy_full_clean(_row())
    assert control is not None
    assert (control["tp1"], control["tp2"], control["tp3"]) == (102.0, 104.0, 106.0)

    t140 = sweep._shadow_t140(_row())
    assert t140 is not None
    assert (t140["tp1"], t140["tp2"], t140["tp3"]) == (102.8, 104.8, 107.6)
    assert "shadow_t140_full_clean" in sweep.POLICY_VARIANTS
    assert "production_t140_full_clean" not in sweep.POLICY_VARIANTS


def test_no_overlay_counterfactual_really_ignores_overlay_action_and_cooldown():
    half_with_cooldown = _row("HALF_SIZE")
    assert sweep._shadow_t140(half_with_cooldown)["force_skip"] is True

    no_overlay = sweep._shadow_no_overlay(half_with_cooldown)
    assert no_overlay is not None
    assert not no_overlay.get("force_skip")
    assert (no_overlay["tp1"], no_overlay["tp2"], no_overlay["tp3"]) == (102.8, 104.8, 107.6)


def test_shadow_summary_win_rate_uses_entered_trades_not_skipped_signals():
    rows = [
        {"variant": "shadow_t140_full_clean", "entered": True, "skipped": False, "net_usd": 5.0,
         "delta_usd": 5.0, "close_reason": "tp1", "tp3_runner": False, "current_net_usd": 0.0},
        {"variant": "shadow_t140_full_clean", "entered": False, "skipped": True, "net_usd": 0.0,
         "delta_usd": 0.0, "close_reason": "gate_skip", "tp3_runner": False, "current_net_usd": -1.0},
    ]
    got = sweep._agg(rows, lambda _: True)[0]
    assert got["entered"] == 1
    assert got["wr"] == 1.0


def test_counterfactual_persistence_marks_only_latest_snapshot_current(tmp_path):
    db = tmp_path / "counterfactual.sqlite"
    base = {
        "db_path": str(db), "generated_at": "2026-07-01T00:00:00+00:00",
        "records": [
            {"signal_id": "a", "variant": "shadow_t130_full_clean", "entered": True},
            {"signal_id": "b", "variant": "shadow_t130_full_clean", "entered": True},
        ],
    }
    assert sweep.persist_counterfactual(base) == 2
    second = {
        **base, "generated_at": "2026-07-02T00:00:00+00:00",
        "records": [base["records"][0]],
    }
    assert sweep.persist_counterfactual(second) == 1
    conn = sqlite3.connect(db)
    rows = conn.execute(
        "SELECT signal_id,snapshot_id,is_current_snapshot "
        "FROM crypto_swing_paper_counterfactual ORDER BY signal_id"
    ).fetchall()
    conn.close()
    assert rows == [
        ("a", "2026-07-02T00:00:00+00:00", 1),
        ("b", "2026-07-01T00:00:00+00:00", 0),
    ]


def _breakout_geom(direction: str = "long") -> dict:
    return {
        "direction": direction, "entry_trigger": 100.0, "entry_low": 99.5, "entry_high": 100.0,
        "stop": 98.0 if direction == "long" else 102.0,
        "tp1": 102.0 if direction == "long" else 98.0,
        "tp2": 104.0 if direction == "long" else 96.0,
        "tp3": 106.0 if direction == "long" else 94.0,
        "raw_idea_json": '{"raw_setup":{"atr":2.0}}',
    }


def test_long_breakout_refinement_requires_a_timely_closed_retest():
    candles = pd.DataFrame([
        {"timestamp": "2026-07-01T00:00:00Z", "open": 99.5, "high": 101.0, "low": 99.4, "close": 100.5},
        {"timestamp": "2026-07-01T01:00:00Z", "open": 99.8, "high": 100.7, "low": 99.9, "close": 100.5},
    ])
    entry, reason = sweep._reclaim_retest_entry(_breakout_geom(), candles)
    assert reason is None
    assert entry is not None and entry["idx"] == 1 and entry["entry"] == 100.5


def test_breakout_refinement_rejects_a_retest_after_its_window():
    candles = pd.DataFrame([
        {"timestamp": "2026-07-01T00:00:00Z", "open": 99.5, "high": 101.0, "low": 99.4, "close": 100.5},
        {"timestamp": "2026-07-01T01:00:00Z", "open": 100.7, "high": 101.2, "low": 100.4, "close": 101.0},
        {"timestamp": "2026-07-01T02:00:00Z", "open": 101.0, "high": 101.3, "low": 100.6, "close": 101.1},
        {"timestamp": "2026-07-01T03:00:00Z", "open": 99.8, "high": 100.7, "low": 99.9, "close": 100.5},
    ])
    entry, reason = sweep._reclaim_retest_entry(_breakout_geom(), candles, max_retest_bars=2)
    assert entry is None
    assert reason == "retest_not_confirmed_in_window"


def test_breakout_snapshot_quality_never_treats_missing_data_as_confirmation():
    ok, reason = sweep._breakout_snapshot_ok({"direction": "long", "snapshot": {}}, strict_rvol=False)
    assert ok is False
    assert reason == "overlay_not_actionable"


def test_breakout_refinement_excludes_missing_or_late_latency_evidence():
    assert sweep._breakout_clean_for_edge({"data_gap_min": 10, "latency_cause": "FAST"})
    assert not sweep._breakout_clean_for_edge({"data_gap_min": None, "latency_cause": "NO_AUDIT"})
    assert not sweep._breakout_clean_for_edge({"data_gap_min": 120, "latency_cause": "DATA_GAP_LATE"})
