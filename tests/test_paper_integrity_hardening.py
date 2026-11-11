from __future__ import annotations

from copy import deepcopy

import pandas as pd

from src.execution.crypto_quality_overlay import config_hash, load_cfg
from src.execution.paper_execution_accounting import (
    build_record_from_signal, ensure_table, quarantine_mixed_execution_geometry,
    record_paper_execution, upsert_outcome,
)
from src.execution.paper_portfolio import simulate_portfolio
from src.notifiers.close_alert import has_existing_close_alert
from src.notifiers.telegram_outbox import enqueue, retry_pending
from src.signals.entry_latency_audit import classify
from src.storage.sqlite import SQLiteStore


def _signal_row(status="waiting_for_entry", entry=100.0):
    return {
        "signal_id": "s1", "created_at": "2026-07-16T10:00:00+00:00",
        "updated_at": "2026-07-16T10:00:00+00:00", "symbol": "BTC/USDT",
        "direction": "long", "mode": "intraday", "tier": "A", "asset_class": "crypto",
        "status": status, "entry_trigger": entry, "suggested_entry": entry,
        "entry_low": entry, "entry_high": entry, "stop_loss": 99.0,
        "invalidation": 99.0, "tp1": 101.0, "tp2": 102.0, "tp3": 103.0,
    }


def test_reregister_cannot_rewind_or_rewrite_entered_signal(tmp_path):
    store = SQLiteStore(tmp_path / "lifecycle.sqlite")
    store.init_db()
    store.upsert_proposed_signal(_signal_row())
    assert store.update_signal_status("s1", status="triggered", updated_at="t1") is True
    store.upsert_proposed_signal(_signal_row(status="waiting_for_entry", entry=110.0))
    row = store.load_signal("s1")
    assert row["status"] == "triggered"
    assert row["entry_trigger"] == 100.0
    assert store.update_signal_status("s1", status="waiting_for_entry", updated_at="t2") is False
    assert store.update_signal_status("s1", status="tp1_hit", updated_at="t3") is True
    assert store.update_signal_status("s1", status="triggered", updated_at="t4") is False
    assert store.update_signal_status("s1", status="stopped", updated_at="t5") is True
    assert store.update_signal_status("s1", status="tp3_hit", updated_at="t6") is False


def test_reregister_cannot_rewrite_geometry_when_paper_entered_before_status_tick(tmp_path):
    store = SQLiteStore(tmp_path / "paper-owned.sqlite")
    store.init_db()
    store.upsert_proposed_signal(_signal_row())
    with store.connect() as conn:
        ensure_table(conn)
        conn.execute(
            "INSERT INTO paper_execution_outcomes "
            "(signal_id,lifecycle_state,signal_snapshot_json) VALUES (?,?,?)",
            ("s1", "OPEN", '{"entry_trigger":100.0,"stop_loss":99.0}'),
        )
    # The proposal still says waiting_for_entry, but Paper already owns the
    # execution plan. A scanner refresh must not move it to a fresh setup.
    store.upsert_proposed_signal(_signal_row(entry=110.0))
    row = store.load_signal("s1")
    assert row["status"] == "waiting_for_entry"
    assert row["entry_trigger"] == 100.0
    assert row["suggested_entry"] == 100.0


def test_realtime_accounting_invalidates_geometry_mutation_after_entry(tmp_path):
    store = SQLiteStore(tmp_path / "accounting-freeze.sqlite")
    store.init_db()
    signal = _signal_row()
    outcome = {
        "status": "triggered", "entry_triggered": True,
        "entry_triggered_at": "2026-07-16T10:01:00+00:00",
        "entry_price_used": 100.0, "max_favorable_excursion_r": 0.1,
    }
    assert record_paper_execution(
        store, signal=signal, outcome_row=outcome,
        now_iso="2026-07-16T10:01:00+00:00",
    )
    moved = dict(signal, entry_trigger=110.0, suggested_entry=110.0,
                 entry_low=110.0, entry_high=110.0, stop_loss=109.0,
                 invalidation=109.0, tp1=111.0, tp2=112.0, tp3=113.0)
    assert record_paper_execution(
        store, signal=moved, outcome_row=outcome,
        now_iso="2026-07-16T10:02:00+00:00",
    )
    with store.connect() as conn:
        row = conn.execute(
            "SELECT lifecycle_state,execution_validity,paper_execution_r,stop_initial "
            "FROM paper_execution_outcomes WHERE signal_id='s1'"
        ).fetchone()
    assert tuple(row) == (
        "INVALID", "invalid_signal_geometry_mutated_after_entry", None, 99.0,
    )


def test_quarantine_removes_proven_mixed_geometry_from_paper_evidence():
    import sqlite3
    conn = sqlite3.connect(":memory:")
    ensure_table(conn)
    conn.execute(
        "INSERT INTO paper_execution_outcomes "
        "(signal_id,lifecycle_state,paper_execution_r,paper_execution_outcome,"
        "stop_initial,signal_snapshot_json,execution_validity) VALUES (?,?,?,?,?,?,?)",
        ("mixed", "CLOSED", 66.0, "win", 98.0,
         '{"invalidation":99.0,"stop_loss":99.0}', "valid"),
    )
    assert quarantine_mixed_execution_geometry(conn) == 1
    row = conn.execute(
        "SELECT lifecycle_state,paper_execution_r,execution_validity "
        "FROM paper_execution_outcomes WHERE signal_id='mixed'"
    ).fetchone()
    assert tuple(row) == (
        "INVALID", None, "invalid_signal_geometry_mutated_after_entry",
    )


def test_tp1_tp2_are_open_and_first_terminal_record_wins():
    import sqlite3
    conn = sqlite3.connect(":memory:"); conn.row_factory = sqlite3.Row
    ensure_table(conn)
    signal = _signal_row()
    tp1 = {"status": "tp1_hit", "entry_triggered": 1, "entry_triggered_at": "e",
           "entry_price_used": 100.0, "tp1_hit": 1, "max_favorable_excursion_r": 1.0}
    sid, key, open_rec = build_record_from_signal(signal, tp1)
    assert open_rec["lifecycle_state"] == "OPEN"
    assert open_rec["paper_execution_r"] is None
    assert open_rec["lock_armed"] is True
    upsert_outcome(conn, signal_id=sid, economic_trade_key=key, computed_at="t1", record=open_rec)

    stopped = dict(tp1, status="stopped", stop_hit=1, stop_hit_at="x")
    _, _, closed_rec = build_record_from_signal(signal, stopped)
    upsert_outcome(conn, signal_id=sid, economic_trade_key=key, computed_at="t2", record=closed_rec)
    assert tuple(conn.execute(
        "SELECT lifecycle_state,close_reason FROM paper_execution_outcomes").fetchone()) == \
        ("CLOSED", "profit_lock_stop")

    later_tp = dict(tp1, status="tp3_hit", tp2_hit=1, tp3_hit=1, tp3_hit_at="later")
    _, _, conflicting = build_record_from_signal(signal, later_tp)
    upsert_outcome(conn, signal_id=sid, economic_trade_key=key, computed_at="t3", record=conflicting)
    assert tuple(conn.execute(
        "SELECT close_reason,exit_at FROM paper_execution_outcomes").fetchone()) == \
        ("profit_lock_stop", "x")


class _FailOnceNotifier:
    def __init__(self):
        self.calls = 0

    def send(self, message, parse_mode=""):
        self.calls += 1
        if self.calls == 1:
            raise TimeoutError("temporary")


def test_telegram_outbox_retries_and_marks_original_alert_sent(tmp_path):
    store = SQLiteStore(tmp_path / "outbox.sqlite"); store.init_db()
    store.record_signal_alert(
        alert_id="a1", signal_id="s1", asset_class="crypto", symbol="BTC/USDT",
        tier="A", sent_at="2026-07-16T10:00:00+00:00", alert_type="paper_entry",
        telegram_status="error:ReadTimeout")
    assert enqueue(store, alert_id="a1", signal_id="s1", alert_type="paper_entry",
                   message="hello", error="error:ReadTimeout") is True
    assert enqueue(store, alert_id="a1", signal_id="s1", alert_type="paper_entry",
                   message="hello", error="error:ReadTimeout") is False
    notifier = _FailOnceNotifier()
    first = retry_pending(store, notifier)
    assert first["failed"] == 1
    with store.connect() as conn:
        conn.execute("UPDATE telegram_alert_outbox SET next_attempt_at='2000-01-01T00:00:00+00:00'")
    second = retry_pending(store, notifier)
    assert second["sent"] == 1
    with store.connect() as conn:
        assert conn.execute("SELECT telegram_status FROM signal_alerts WHERE alert_id='a1'").fetchone()[0] == "sent"


def test_crypto_bar_cadence_and_impossible_backfill_are_distinguished():
    hourly = pd.DataFrame({
        "timestamp": pd.date_range("2026-07-16T11:00:00Z", periods=3, freq="1h"),
        "open": [100] * 3, "high": [101] * 3, "low": [99] * 3, "close": [100] * 3,
    })
    normal = classify(
        created_at="2026-07-16T10:28:00Z", entry_triggered_at="2026-07-16T11:00:00Z",
        entry_low=99, entry_high=101, candles_df=hourly, mode="swing", asset_class="crypto")
    assert normal["cause"] == "LEGITIMATE_LATE"

    stale = hourly.copy()
    stale["timestamp"] = pd.date_range("2026-07-19T11:00:00Z", periods=3, freq="1h")
    impossible = classify(
        created_at="2026-07-16T10:28:00Z", entry_triggered_at="2026-07-16T10:33:00Z",
        entry_low=99, entry_high=101, candles_df=stale, mode="intraday", asset_class="crypto")
    assert impossible["cause"] == "DATA_GAP_LATE"


def test_overlay_hash_changes_when_effective_config_changes():
    cfg = load_cfg()
    changed = deepcopy(cfg)
    changed["default_unknown_data_action"] = "SHADOW_ONLY"
    assert config_hash(cfg) != config_hash(changed)


def test_ledger_realizes_on_exit_time_and_carries_execution_context():
    trade = {
        "signal_id": "s1", "economic_trade_key": "k1", "symbol": "BTC/USDT",
        "asset_class": "crypto", "mode": "intraday", "direction": "long",
        "entry": 100.0, "stop": 99.0, "paper_execution_r": 1.0,
        "close_reason": "tp3_runner", "entry_at": "2026-07-15T10:00:00+00:00",
        "exit_at": "2026-07-16T12:00:00+00:00", "exit_at_source": "tp3_hit_at",
        "decision_at": "2026-07-15T10:01:00+00:00", "first_executable_price": 100.1,
        "entry_drift_bps": 10.0, "size_weight": 1.0, "overlay_config_hash": "cfg123",
    }
    row = simulate_portfolio([trade], fee_profile="zero")["ledger"][0]
    assert row["timestamp"] == trade["exit_at"]
    assert row["entry_at"] == trade["entry_at"]
    assert row["exit_at_source"] == "tp3_hit_at"
    assert row["overlay_config_hash"] == "cfg123"


def test_any_prior_close_type_dedupes_future_close(tmp_path):
    store = SQLiteStore(tmp_path / "close.sqlite"); store.init_db()
    store.record_signal_alert(
        alert_id="c1", signal_id="s1", asset_class="crypto", symbol="BTC/USDT",
        tier="A", sent_at="2026-07-16T10:00:00+00:00", alert_type="close_stop",
        telegram_status="sent")
    assert has_existing_close_alert(store, "s1", "close_tp") is True
