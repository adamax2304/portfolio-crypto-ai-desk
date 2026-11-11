"""Tests for the PAPER execution accounting module (Model F).

Locks the early_mfe_protection_v1 formula + storage. PAPER/ACCOUNTING ONLY —
asserts signal_outcomes / final_r are never mutated.
"""
from __future__ import annotations

import sqlite3

import pytest

from src.execution.paper_live_exit_path import VERSION as LIVE_EXIT_PARITY_VERSION
from src.execution.paper_execution_accounting import (
    _effective_expiry,
    compute_paper_execution, ensure_table, upsert_outcome, backfill_all,
    r_multiple, DEFAULT_RISK_MODEL, build_record_from_signal,
    evidence_class_for, FROZEN_AT, EVIDENCE_FORWARD, EVIDENCE_BACKFILL, MODEL_VERSION,
    backfill_evidence_class_only,
    repair_specific_crypto_swing_profiles,
    record_paper_execution,
)
from datetime import datetime, timezone


def _long(**kw):
    base = dict(direction="long", entry=100.0, stop=99.0, tp1=101.0, tp2=102.0, tp3=103.0,
                reached_tp1=False, reached_tp2=False, reached_tp3=False, hit_stop=False,
                expired=False, entered=True, mfe_r=0.0)
    base.update(kw)
    return compute_paper_execution(**base)


def test_long_tp1_then_stop_be_at_0_6r():
    # Reached TP1 (touch +1R) then reversed to stop, MFE peaked +0.7R -> BE = 0R.
    r = _long(reached_tp1=True, hit_stop=True, mfe_r=0.7)
    assert r["touch_r"] == 1.0
    assert r["paper_execution_r"] == 0.0
    assert r["paper_execution_outcome"] == "breakeven"
    assert r["protection_armed"] is True and r["giveback"] is True


def test_long_tp1_then_stop_lock_at_1r():
    # MFE peaked +1.3R then reversed -> locked +0.5R.
    r = _long(reached_tp1=True, hit_stop=True, mfe_r=1.3)
    assert r["touch_r"] == 1.0
    assert r["paper_execution_r"] == 0.5
    assert r["lock_armed"] is True


def test_ambiguous_same_candle_cannot_arm_profit_lock_from_pre_entry_high():
    """A bar high can occur before a later limit fill, so it cannot credit +0.5R.

    The later original-stop touch is decisive. This is the exact failure mode
    that previously reported a profit lock for MMT despite the minute path
    entering after the candle high and then falling to the original stop.
    """
    r = _long(reached_tp1=True, hit_stop=True, mfe_r=1.8, same_candle_ambiguous=True)
    assert r["paper_execution_r"] == -1.0
    assert r["paper_execution_outcome"] == "loss"
    assert r["close_reason"] == "original_stop"
    assert r["close_event"] == "ambiguous_stop_first"
    assert r["lock_armed"] is False


def test_ambiguous_same_candle_without_later_stop_expires_flat():
    r = _long(reached_tp1=True, expired=True, mfe_r=1.8, same_candle_ambiguous=True)
    assert r["paper_execution_r"] == 0.0
    assert r["paper_execution_outcome"] == "expired"
    assert r["close_reason"] == "expired_flat"


def test_long_stop_before_protection_is_minus1():
    r = _long(hit_stop=True, mfe_r=0.3)
    assert r["paper_execution_r"] == -1.0
    assert r["paper_execution_outcome"] == "loss"
    assert r["protection_armed"] is False


def test_tp3_runner_still_captures():
    r = _long(reached_tp1=True, reached_tp2=True, reached_tp3=True, mfe_r=3.2)
    assert r["touch_r"] == 3.0
    assert r["paper_execution_r"] == 3.0
    assert r["paper_execution_outcome"] == "win"


def test_short_tp1_then_stop_be():
    # Short: entry 100, stop 101 (risk 1), tp1 99. Reached TP1 then stop, MFE +0.8R.
    r = compute_paper_execution(
        direction="short", entry=100.0, stop=101.0, tp1=99.0, tp2=98.0, tp3=97.0,
        reached_tp1=True, reached_tp2=False, reached_tp3=False, hit_stop=True,
        expired=False, entered=True, mfe_r=0.8)
    assert r["touch_r"] == 1.0          # short TP1 is +1R
    assert r["paper_execution_r"] == 0.0  # BE protection
    assert r_multiple(100.0, 101.0, 99.0, "short") == 1.0


def test_expired_after_entry_resolves_not_unresolved():
    # Entered, never hit TP/stop, expired. MFE 0.2R -> flat 0R (not left "open").
    r = _long(expired=True, mfe_r=0.2)
    assert r["paper_execution_r"] == 0.0
    assert r["paper_execution_outcome"] == "expired"


def test_not_entered_is_none():
    r = _long(entered=False)
    assert r["paper_execution_r"] is None
    assert r["paper_execution_outcome"] == "no_entry"


def test_storage_idempotent_upsert_and_no_signal_outcomes_mutation():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    # minimal signal_outcomes + proposed_signals so a mutation would be detectable
    conn.execute("CREATE TABLE signal_outcomes (signal_id TEXT, final_r REAL)")
    conn.execute("INSERT INTO signal_outcomes VALUES ('s1', 1.0)")
    before = conn.execute("SELECT final_r FROM signal_outcomes WHERE signal_id='s1'").fetchone()[0]
    ensure_table(conn)
    rec = _long(reached_tp1=True, hit_stop=True, mfe_r=0.7)
    upsert_outcome(conn, signal_id="s1", economic_trade_key="k1", computed_at="t0", record=rec)
    upsert_outcome(conn, signal_id="s1", economic_trade_key="k1", computed_at="t1", record=rec)  # idempotent
    rows = conn.execute("SELECT count(*) FROM paper_execution_outcomes").fetchall()
    assert rows[0][0] == 1                       # single row after two upserts
    pe = conn.execute("SELECT paper_execution_r FROM paper_execution_outcomes WHERE signal_id='s1'").fetchone()[0]
    assert pe == 0.0
    after = conn.execute("SELECT final_r FROM signal_outcomes WHERE signal_id='s1'").fetchone()[0]
    assert before == after == 1.0                # signal_outcomes.final_r UNTOUCHED


def test_realtime_entry_provenance_replaces_prior_historical_touch():
    """A later current-price observation must not inherit a stale entry time."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    ensure_table(conn)
    historical = _long()
    historical.update(
        lifecycle_state="OPEN", entry_at="2026-08-01T18:02:16+00:00",
        entry_price_used=100.0, decision_at=None, first_executable_price=None,
        entry_time_basis="historical_bar_range", current_price_revalidated=False,
    )
    upsert_outcome(conn, signal_id="provenance", economic_trade_key="k", computed_at="t0",
                   record=historical)
    current = _long()
    current.update(
        lifecycle_state="OPEN", entry_at="2026-08-01T21:44:17+00:00",
        entry_price_used=100.2, decision_at="2026-08-01T21:44:17+00:00",
        first_executable_price=100.2, entry_time_basis="point_in_time_current_bar",
        current_price_revalidated=True,
    )
    upsert_outcome(conn, signal_id="provenance", economic_trade_key="k", computed_at="t1",
                   record=current)
    row = conn.execute(
        "SELECT entry_at,entry_price_used,decision_at,first_executable_price,"
        "entry_time_basis,current_price_revalidated FROM paper_execution_outcomes "
        "WHERE signal_id='provenance'"
    ).fetchone()
    assert tuple(row) == (
        "2026-08-01T21:44:17+00:00", 100.2, "2026-08-01T21:44:17+00:00", 100.2,
        "point_in_time_current_bar", 1,
    )


def test_path_safety_repair_clears_stale_protection_flags():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    ensure_table(conn)
    optimistic = _long(reached_tp1=True, hit_stop=True, mfe_r=1.3)
    upsert_outcome(conn, signal_id="amb", economic_trade_key="k", computed_at="t0", record=optimistic)
    corrected = _long(reached_tp1=True, hit_stop=True, mfe_r=1.3, same_candle_ambiguous=True)
    upsert_outcome(conn, signal_id="amb", economic_trade_key="k", computed_at="t1", record=corrected, repair=True)
    row = conn.execute(
        "SELECT paper_execution_r, close_reason, protection_armed, lock_armed "
        "FROM paper_execution_outcomes WHERE signal_id='amb'"
    ).fetchone()
    assert tuple(row) == (-1.0, "original_stop", 0, 0)


def test_legacy_and_first_tp_models_available():
    legacy = _long(reached_tp1=True, hit_stop=True, mfe_r=0.7, risk_model="legacy_touch")
    assert legacy["paper_execution_r"] == 1.0    # touch counts TP1 win
    first = _long(reached_tp1=True, hit_stop=True, mfe_r=0.7, risk_model="first_tp_close")
    assert first["paper_execution_r"] == 1.0     # closed at TP1 before reversal


# ---- 2026-07-09 freeze/version + evidence_class ------------------------------------------------
def test_model_version_reflects_frozen_state():
    # any future re-tune must bump this string — a silent constant edit with the
    # same version string would hide that the frozen parameters changed.
    assert "frozen" in MODEL_VERSION.lower()


def test_evidence_class_before_and_after_freeze():
    before = "2026-06-24T10:00:00+00:00"
    after = "2026-07-09T12:00:00+00:00"
    exactly_at = FROZEN_AT
    assert evidence_class_for(before) == EVIDENCE_BACKFILL
    assert evidence_class_for(after) == EVIDENCE_FORWARD
    assert evidence_class_for(exactly_at) == EVIDENCE_FORWARD   # boundary is inclusive-forward


def test_evidence_class_defaults_to_backfill_when_undated():
    # missing/unparseable timestamps must never be credited as forward evidence
    assert evidence_class_for(None) == EVIDENCE_BACKFILL
    assert evidence_class_for("") == EVIDENCE_BACKFILL
    assert evidence_class_for("not-a-date") == EVIDENCE_BACKFILL


def test_compute_paper_execution_stamps_evidence_class_and_frozen_at():
    old = _long(reached_tp1=True, hit_stop=True, mfe_r=0.7, entry_ts="2026-05-01T00:00:00+00:00")
    new = _long(reached_tp1=True, hit_stop=True, mfe_r=0.7, entry_ts="2026-07-10T00:00:00+00:00")
    assert old["evidence_class"] == EVIDENCE_BACKFILL
    assert new["evidence_class"] == EVIDENCE_FORWARD
    assert old["frozen_at"] == new["frozen_at"] == FROZEN_AT
    # unresolved (no entry) trades still get an evidence_class — never left unlabeled
    unresolved = _long(entered=False, entry_ts="2026-07-10T00:00:00+00:00")
    assert unresolved["evidence_class"] == EVIDENCE_FORWARD


def test_build_record_from_signal_uses_real_entry_time_not_computed_at():
    """The classification must key off entry_triggered_at (falling back to
    created_at), never off computed_at — computed_at is always 'now' on every
    refresh and would make every row look like forward evidence forever."""
    signal = {
        "signal_id": "s-old", "direction": "long", "created_at": "2026-05-01T00:00:00+00:00",
        "invalidation": 99.0, "tp1": 101.0, "tp2": 102.0, "tp3": 103.0,
    }
    outcome_old = {
        "entry_triggered": True, "entry_triggered_at": "2026-05-01T00:05:00+00:00",
        "entry_price_used": 100.0, "tp1_hit": True, "stop_hit": True,
        "max_favorable_excursion_r": 0.7, "final_outcome": "loss",
    }
    _, _, rec_old = build_record_from_signal(signal, outcome_old)
    assert rec_old["evidence_class"] == EVIDENCE_BACKFILL   # entered in May, long before the freeze
    assert rec_old["entry_time_basis"] is None               # historical repair stays unclassified

    signal_new = dict(signal, signal_id="s-new")
    outcome_new = dict(outcome_old, entry_triggered_at="2026-07-10T00:05:00+00:00")
    _, _, rec_new = build_record_from_signal(signal_new, outcome_new)
    assert rec_new["evidence_class"] == EVIDENCE_FORWARD    # entered after the freeze


def test_crypto_historical_touch_is_not_an_executable_paper_entry():
    signal = {
        "signal_id": "crypto-historical", "asset_class": "crypto", "mode": "swing",
        "direction": "long", "created_at": "2026-09-20T00:00:00+00:00",
        "entry_trigger": 100.0, "invalidation": 90.0,
        "tp1": 110.0, "tp2": 120.0, "tp3": 130.0,
    }
    outcome = {
        "status": "triggered", "entry_triggered": True,
        "entry_triggered_at": "2026-09-20T00:05:00+00:00",
        "entry_price_used": 100.0,
    }
    _, _, record = build_record_from_signal(
        signal, outcome,
        entry_time_basis="historical_not_currently_executable",
        current_price_revalidated=False,
    )
    assert record["lifecycle_state"] == "INVALID"
    assert record["execution_validity"] == "invalid_crypto_entry_not_point_in_time"
    assert record["paper_execution_r"] is None


def test_crypto_current_price_entry_remains_valid():
    signal = {
        "signal_id": "crypto-current", "asset_class": "crypto", "mode": "intraday",
        "direction": "long", "created_at": "2026-09-20T00:00:00+00:00",
        "entry_trigger": 100.0, "invalidation": 90.0,
        "tp1": 110.0, "tp2": 120.0, "tp3": 130.0,
    }
    outcome = {
        "status": "triggered", "entry_triggered": True,
        "entry_triggered_at": "2026-09-20T00:05:00+00:00",
        "entry_price_used": 100.0,
    }
    _, _, record = build_record_from_signal(
        signal, outcome,
        decision_at="2026-09-20T00:05:20+00:00",
        first_executable_price=100.0,
        entry_time_basis="point_in_time_current_bar",
        current_price_revalidated=True,
    )
    assert record["lifecycle_state"] == "OPEN"
    assert record["execution_validity"] == "valid"


def test_live_exit_path_overrides_later_aggregate_tp3_touch():
    signal = {
        "signal_id": "s-path", "direction": "long",
        "created_at": "2026-09-20T00:00:00+00:00",
        "entry_trigger": 100.0, "invalidation": 90.0,
        "tp1": 110.0, "tp2": 120.0, "tp3": 130.0,
    }
    # Legacy tracking later sees TP3 and would credit the whole position +3R.
    outcome = {
        "status": "tp3_hit", "entry_triggered": True,
        "entry_triggered_at": "2026-09-20T00:01:00+00:00",
        "entry_price_used": 100.0, "tp1_hit": True,
        "tp2_hit": True, "tp3_hit": True, "max_favorable_excursion_r": 3.0,
    }
    path = {
        "version": LIVE_EXIT_PARITY_VERSION, "terminal": True,
        "paper_execution_r": 0.0, "paper_execution_outcome": "breakeven",
        "close_reason": "breakeven_stop", "close_event": "moved_stop",
        "exit_at": "2026-09-20T00:10:00+00:00",
        "exit_at_source": "closed_1m_path_stop_first",
        "highest_tp_touched": 0, "stop_current_r": 0.0,
        "protection_armed": True, "lock_armed": False,
        "same_candle_ambiguous": False,
    }
    _, _, record = build_record_from_signal(signal, outcome, execution_path=path)
    assert record["paper_execution_r"] == 0.0
    assert record["close_reason"] == "breakeven_stop"
    assert record["exit_at"] == path["exit_at"]
    assert record["version"] == LIVE_EXIT_PARITY_VERSION


def test_live_exit_path_gap_is_excluded_instead_of_using_aggregate_touch_result():
    signal = {
        "signal_id": "s-path-gap", "direction": "long",
        "created_at": "2026-09-20T00:00:00+00:00",
        "entry_trigger": 100.0, "invalidation": 90.0,
        "tp1": 110.0, "tp2": 120.0, "tp3": 130.0,
    }
    outcome = {
        "status": "tp3_hit", "entry_triggered": True,
        "entry_triggered_at": "2026-09-20T00:01:00+00:00",
        "entry_price_used": 100.0, "tp1_hit": True,
        "tp2_hit": True, "tp3_hit": True, "max_favorable_excursion_r": 3.0,
    }
    path = {
        "version": LIVE_EXIT_PARITY_VERSION, "terminal": False,
        "paper_execution_r": None, "paper_execution_outcome": "open",
        "path_data_quality": "gap", "path_gap_seconds": 600.0,
        "path_last_candle_at": "2026-09-20T00:05:00+00:00",
        "path_realized_r": 0.0, "path_remaining_fraction": 1.0,
        "stop_current_r": -1.0,
    }
    _, _, record = build_record_from_signal(signal, outcome, execution_path=path)
    assert record["lifecycle_state"] == "INVALID"
    assert record["execution_validity"] == "invalid_execution_path_gap"
    assert record["paper_execution_r"] is None
    assert record["close_reason"] == "invalid_execution_path_gap"


def test_expired_open_parity_path_closes_at_protected_level():
    signal = {
        "signal_id": "expiry-lock", "asset_class": "crypto", "direction": "long",
        "created_at": "2026-10-10T12:00:00+00:00", "expires_at": "2026-10-11T12:00:00+00:00",
        "entry_trigger": 100.0, "invalidation": 90.0,
        "tp1": 110.0, "tp2": 120.0, "tp3": 130.0,
    }
    outcome = {
        "status": "triggered", "entry_triggered": True,
        "entry_triggered_at": "2026-10-10T12:05:00+00:00", "entry_price_used": 100.0,
    }
    path = {
        "version": LIVE_EXIT_PARITY_VERSION, "terminal": False,
        "paper_execution_r": None, "paper_execution_outcome": "open",
        "path_data_quality": "complete", "path_realized_r": 0.33,
        "path_remaining_fraction": 0.67, "stop_current_r": 0.5,
        "protection_armed": True, "lock_armed": True,
    }
    _, _, record = build_record_from_signal(
        signal, outcome, as_of_iso="2026-10-13T10:00:00+00:00", execution_path=path,
    )
    assert record["paper_execution_r"] == 0.665
    assert record["paper_execution_outcome"] == "win"
    assert record["close_reason"] == "expiry_profit_lock"
    assert record["close_event"] == "expiry"
    assert record["exit_at"] == "2026-10-11T12:00:00+00:00"
    assert record["exit_at_source"] == "expires_at_protected"
    assert record["path_remaining_fraction"] == 0.0
    assert record["lifecycle_state"] == "CLOSED"


def test_record_paper_execution_passes_tracker_time_for_expiry():
    class Store:
        def __init__(self):
            self.conn = sqlite3.connect(":memory:")
            self.conn.row_factory = sqlite3.Row

        def connect(self):
            return self.conn

    store = Store()
    signal = {
        "signal_id": "tracker-expiry", "asset_class": "crypto", "direction": "long",
        "created_at": "2026-10-10T12:00:00+00:00", "expires_at": "2026-10-11T12:00:00+00:00",
        "entry_trigger": 100.0, "invalidation": 90.0,
        "tp1": 110.0, "tp2": 120.0, "tp3": 130.0,
    }
    outcome = {
        "status": "triggered", "entry_triggered": True,
        "entry_triggered_at": "2026-10-10T12:05:00+00:00", "entry_price_used": 100.0,
    }
    path = {
        "version": LIVE_EXIT_PARITY_VERSION, "terminal": False,
        "paper_execution_r": None, "paper_execution_outcome": "open",
        "path_data_quality": "complete", "path_realized_r": 0.0,
        "path_remaining_fraction": 1.0, "stop_current_r": 0.0,
        "protection_armed": True, "lock_armed": False,
    }
    assert record_paper_execution(
        store, signal=signal, outcome_row=outcome,
        now_iso="2026-10-13T10:00:00+00:00", execution_path=path,
    ) is True
    saved = store.conn.execute(
        "SELECT lifecycle_state,paper_execution_r,close_reason,exit_at "
        "FROM paper_execution_outcomes WHERE signal_id='tracker-expiry'"
    ).fetchone()
    assert tuple(saved) == (
        "CLOSED", 0.0, "expiry_breakeven", "2026-10-11T12:00:00+00:00",
    )


def test_expired_parity_path_without_persisted_state_is_quarantined_not_left_open():
    signal = {
        "signal_id": "expiry-missing-path", "asset_class": "crypto", "direction": "long",
        "created_at": "2026-10-10T12:00:00+00:00", "expires_at": "2026-10-11T12:00:00+00:00",
        "entry_trigger": 100.0, "invalidation": 90.0,
        "tp1": 110.0, "tp2": 120.0, "tp3": 130.0,
    }
    outcome = {
        "status": "triggered", "entry_triggered": True,
        "entry_triggered_at": "2026-10-10T12:05:00+00:00", "entry_price_used": 100.0,
    }
    path = {
        "version": LIVE_EXIT_PARITY_VERSION, "terminal": False,
        "paper_execution_r": None, "paper_execution_outcome": "open",
        "path_data_quality": "complete", "path_realized_r": None,
        "path_remaining_fraction": None, "stop_current_r": None,
    }
    _, _, record = build_record_from_signal(
        signal, outcome, as_of_iso="2026-10-13T10:00:00+00:00", execution_path=path,
    )
    assert record["lifecycle_state"] == "INVALID"
    assert record["execution_validity"] == "invalid_expired_execution_path_state"
    assert record["paper_execution_r"] is None


def test_full_refresh_rehydrates_open_parity_path_before_expiry_repair():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript("""
        CREATE TABLE proposed_signals (
            signal_id TEXT PRIMARY KEY, symbol TEXT, direction TEXT, mode TEXT, tier TEXT,
            asset_class TEXT, setup_type TEXT, created_at TEXT, suggested_entry REAL,
            entry_trigger REAL, entry_low REAL, stop_loss REAL, invalidation REAL,
            tp1 REAL, tp2 REAL, tp3 REAL, expires_at TEXT, raw_idea_json TEXT
        );
        CREATE TABLE signal_outcomes (
            id INTEGER PRIMARY KEY, signal_id TEXT, entry_triggered INTEGER,
            entry_triggered_at TEXT, entry_price_used REAL, status TEXT,
            tp1_hit INTEGER, tp2_hit INTEGER, tp3_hit INTEGER, stop_hit INTEGER,
            max_favorable_excursion_r REAL, notes TEXT, checked_at TEXT,
            final_r REAL, final_outcome TEXT
        );
        CREATE TABLE signal_entry_mode (
            signal_id TEXT PRIMARY KEY, entry_mode TEXT
        );
    """)
    ensure_table(conn)
    conn.execute(
        "INSERT INTO proposed_signals VALUES "
        "('refresh-expiry','BTC/USDT','long','intraday','B','crypto','test',"
        "'2026-10-10T12:00:00+00:00',100,100,100,90,90,110,120,130,"
        "'2026-10-11T12:00:00+00:00',NULL)"
    )
    conn.execute(
        "INSERT INTO signal_outcomes VALUES "
        "(1,'refresh-expiry',1,'2026-10-10T12:05:00+00:00',100,'triggered',"
        "0,0,0,0,0.2,NULL,'2026-10-10T12:06:00+00:00',7.0,'legacy-value')"
    )
    conn.execute(
        "INSERT INTO signal_entry_mode VALUES ('refresh-expiry','MOMENTUM_TAKER_NOW')"
    )
    signal = {
        "signal_id": "refresh-expiry", "symbol": "BTC/USDT", "asset_class": "crypto",
        "mode": "intraday", "direction": "long", "created_at": "2026-10-10T12:00:00+00:00",
        "entry_trigger": 100.0, "invalidation": 90.0, "tp1": 110.0, "tp2": 120.0,
        "tp3": 130.0, "expires_at": "2026-10-11T12:00:00+00:00",
        "paper_entry_profile": "crypto_intraday_breakout_paper_v1",
        "paper_execution_entry_mode": "BREAKOUT_CONTINUATION",
    }
    outcome = {
        "status": "triggered", "entry_triggered": True,
        "entry_triggered_at": "2026-10-10T12:05:00+00:00", "entry_price_used": 100.0,
    }
    open_path = {
        "version": LIVE_EXIT_PARITY_VERSION, "terminal": False,
        "paper_execution_r": None, "paper_execution_outcome": "open",
        "path_data_quality": "complete", "path_realized_r": 0.33,
        "path_remaining_fraction": 0.67, "stop_current_r": 0.5,
        "protection_armed": True, "lock_armed": True,
    }
    _, trade_key, open_record = build_record_from_signal(
        signal, outcome, as_of_iso="2026-10-10T12:06:00+00:00", execution_path=open_path,
    )
    upsert_outcome(
        conn, signal_id="refresh-expiry", economic_trade_key=trade_key,
        computed_at="2026-10-10T12:06:00+00:00", record=open_record,
    )
    conn.execute(
        "UPDATE paper_execution_outcomes SET lifecycle_state='INVALID',"
        "paper_execution_r=NULL,paper_execution_outcome='invalid_session',"
        "close_reason='invalid_paper_profile_entry_mode_mismatch',"
        "close_event='invalid_session',execution_validity='invalid_paper_profile_entry_mode_mismatch',"
        "path_realized_r=0.665,path_remaining_fraction=0,exit_at=NULL,exit_at_source=NULL "
        "WHERE signal_id='refresh-expiry'"
    )

    stats = backfill_all(
        conn, now_iso="2026-10-13T10:00:00+00:00", expired_only=True,
    )
    repaired = conn.execute(
        "SELECT lifecycle_state,paper_execution_r,close_reason,version "
        "FROM paper_execution_outcomes WHERE signal_id='refresh-expiry'"
    ).fetchone()
    untouched = conn.execute(
        "SELECT final_r,final_outcome FROM signal_outcomes WHERE signal_id='refresh-expiry'"
    ).fetchone()
    assert stats["errors"] == 0 and stats["resolved"] == 1
    assert stats["scanned"] == 1 and stats["mixed_geometry_quarantined"] == 0
    assert repaired["lifecycle_state"] == "CLOSED"
    assert repaired["paper_execution_r"] == 0.665
    assert repaired["close_reason"] == "expiry_profit_lock"
    assert repaired["version"] == LIVE_EXIT_PARITY_VERSION
    assert tuple(untouched) == (7.0, "legacy-value")


def test_build_record_from_signal_stamps_profile_and_entry_mode():
    signal = {
        "signal_id": "s-profile", "direction": "long",
        "created_at": "2026-07-20T00:00:00+00:00",
        "entry_trigger": 100.0, "invalidation": 98.0,
        "tp1": 103.0, "tp2": 106.0, "tp3": 110.0,
        "paper_entry_profile": "crypto_swing_paper_t130_v1",
        "paper_execution_entry_mode": "BREAKOUT_CONTINUATION",
    }
    outcome = {
        "status": "triggered", "entry_triggered": True,
        "entry_triggered_at": "2026-07-20T01:00:00+00:00",
        "entry_price_used": 100.0, "max_favorable_excursion_r": 0.2,
    }
    _, _, record = build_record_from_signal(signal, outcome)
    assert record["paper_entry_profile"] == "crypto_swing_paper_t130_v1"
    assert record["paper_execution_entry_mode"] == "BREAKOUT_CONTINUATION"


@pytest.mark.parametrize(("mode", "expected_profile"), [
    ("BREAKOUT_RECLAIM_V2", "crypto_swing_breakout_reclaim_paper_v2"),
    ("PULLBACK_CONFIRMED_RETEST", "crypto_swing_pullback_confirmed_retest_paper_v1"),
    ("FIB_IMPULSE_RETEST", "crypto_swing_fib_impulse_retest_paper_v1"),
])
def test_specific_crypto_swing_mode_overrides_generic_t130_profile(mode, expected_profile):
    signal = {
        "signal_id": f"specific-{mode}", "asset_class": "crypto", "mode": "swing",
        "direction": "long", "created_at": "2026-09-20T00:00:00+00:00",
        "entry_trigger": 100.0, "invalidation": 98.0,
        "tp1": 103.0, "tp2": 106.0, "tp3": 110.0,
        "paper_entry_profile": "crypto_swing_paper_t130_v1",
        "paper_execution_entry_mode": mode,
    }
    outcome = {"status": "triggered", "entry_triggered": True,
               "entry_triggered_at": "2026-09-20T01:00:00+00:00",
               "entry_price_used": 100.0, "max_favorable_excursion_r": 0.2}
    _, _, record = build_record_from_signal(signal, outcome)
    assert record["paper_entry_profile"] == expected_profile


def test_profile_repair_splits_existing_generic_crypto_swing_rows():
    conn = sqlite3.connect(":memory:")
    ensure_table(conn)
    for index, mode in enumerate((
        "BREAKOUT_RECLAIM_V2", "PULLBACK_CONFIRMED_RETEST", "FIB_IMPULSE_RETEST"
    )):
        conn.execute(
            "INSERT INTO paper_execution_outcomes "
            "(signal_id,paper_entry_profile,paper_execution_entry_mode) VALUES (?,?,?)",
            (f"s{index}", "crypto_swing_paper_t130_v1", mode),
        )
    repaired = repair_specific_crypto_swing_profiles(conn)
    assert repaired == {
        "BREAKOUT_RECLAIM_V2": 1,
        "PULLBACK_CONFIRMED_RETEST": 1,
        "FIB_IMPULSE_RETEST": 1,
    }
    profiles = {row[0] for row in conn.execute(
        "SELECT paper_entry_profile FROM paper_execution_outcomes")}
    assert profiles == {
        "crypto_swing_breakout_reclaim_paper_v2",
        "crypto_swing_pullback_confirmed_retest_paper_v1",
        "crypto_swing_fib_impulse_retest_paper_v1",
    }


def test_known_paper_profile_rejects_a_mismatched_executed_mode():
    signal = {
        "signal_id": "s-profile-mismatch", "direction": "long",
        "created_at": "2026-07-20T00:00:00+00:00",
        "entry_trigger": 100.0, "invalidation": 98.0,
        "tp1": 103.0, "tp2": 106.0, "tp3": 110.0,
        "paper_entry_profile": "crypto_intraday_level_hold_v2_paper_v1",
        "paper_execution_entry_mode": "LEVEL_HOLD_1BAR",
    }
    outcome = {
        "status": "stopped", "entry_triggered": True, "stop_hit": True,
        "entry_triggered_at": "2026-07-20T01:00:00+00:00",
        "entry_price_used": 100.0,
    }
    _, _, record = build_record_from_signal(signal, outcome)
    assert record["lifecycle_state"] == "INVALID"
    assert record["paper_execution_r"] is None
    assert record["execution_validity"] == "invalid_paper_profile_entry_mode_mismatch"


def test_verified_execution_freezes_detection_time_and_current_price():
    signal = {
        "signal_id": "s-live-like", "direction": "long",
        "created_at": "2026-07-17T10:00:00+00:00", "suggested_entry": 100.0,
        "invalidation": 98.0, "tp1": 103.0, "tp2": 106.0, "tp3": 110.0,
    }
    outcome = {
        "status": "triggered", "entry_triggered": True,
        "entry_triggered_at": "2026-07-17T10:00:00+00:00",
        "entry_price_used": 100.0, "max_favorable_excursion_r": 0.0,
    }
    _, _, rec = build_record_from_signal(
        signal, outcome, decision_at="2026-07-17T10:45:00+00:00",
        first_executable_price=100.2,
        entry_time_basis="point_in_time_current_bar",
        current_price_revalidated=True)
    assert rec["entry_at"] == "2026-07-17T10:45:00+00:00"
    assert rec["entry_price_used"] == 100.2
    assert rec["entry_bar_open_at"] == "2026-07-17T10:00:00+00:00"
    assert rec["entry_time_basis"] == "point_in_time_current_bar"
    assert rec["current_price_revalidated"] is True


def test_stock_intraday_delayed_bar_is_authoritative_when_price_is_revalidated():
    signal = {
        "signal_id": "s-stock-delayed", "asset_class": "stocks", "mode": "intraday",
        "direction": "short", "created_at": "2026-07-29T18:11:00+00:00",
        "suggested_entry": 100.0, "invalidation": 102.0,
        "tp1": 97.0, "tp2": 95.0, "tp3": 92.0,
    }
    outcome = {"status": "stopped", "entry_triggered": True,
               "entry_triggered_at": "2026-07-29T18:37:00+00:00",
               "entry_price_used": 100.0, "stop_hit": True,
               "stop_hit_at": "2026-07-29T19:01:00+00:00"}
    _, _, rec = build_record_from_signal(
        signal, outcome, decision_at="2026-07-29T18:38:00+00:00",
        first_executable_price=100.2,
        entry_time_basis="provider_delayed_current_bar",
        current_price_revalidated=True,
    )
    assert rec["paper_execution_r"] == -1.0
    assert rec["execution_validity"] == "valid"
    assert rec["entry_at"] == "2026-07-29T18:38:00+00:00"
    assert rec["entry_price_used"] == 100.2


def test_stock_intraday_delayed_bar_still_requires_current_price_revalidation():
    signal = {
        "signal_id": "s-stock-delayed-unverified", "asset_class": "stocks", "mode": "intraday",
        "direction": "long", "created_at": "2026-07-29T18:11:00+00:00",
        "suggested_entry": 100.0, "invalidation": 98.0,
        "tp1": 103.0, "tp2": 105.0, "tp3": 108.0,
    }
    outcome = {"status": "triggered", "entry_triggered": True,
               "entry_triggered_at": "2026-07-29T18:37:00+00:00",
               "entry_price_used": 100.0}
    _, _, rec = build_record_from_signal(
        signal, outcome, decision_at="2026-07-29T18:38:00+00:00",
        first_executable_price=100.2,
        entry_time_basis="provider_delayed_current_bar",
        current_price_revalidated=False,
    )
    assert rec["paper_execution_r"] is None
    assert rec["execution_validity"] == "invalid_stock_intraday_entry_not_point_in_time"


def test_ensure_table_migrates_pre_freeze_schema(tmp_path=None):
    """A DB created before evidence_class/frozen_at existed must gain the columns
    idempotently on the next ensure_table() call, with no row loss."""
    conn = sqlite3.connect(":memory:")
    conn.execute(
        """
        CREATE TABLE paper_execution_outcomes (
            signal_id TEXT PRIMARY KEY, economic_trade_key TEXT, risk_model TEXT,
            touch_r REAL, paper_execution_r REAL, paper_execution_outcome TEXT,
            close_reason TEXT, stop_initial REAL, stop_current_r REAL,
            protection_armed INTEGER, protection_level_r REAL, lock_armed INTEGER,
            lock_level_r REAL, highest_tp_touched INTEGER, first_event TEXT,
            close_event TEXT, giveback INTEGER, same_candle_ambiguous INTEGER,
            computed_at TEXT, version TEXT
        )
        """
    )
    conn.execute("INSERT INTO paper_execution_outcomes (signal_id, version) VALUES ('legacy1','old_v')")
    conn.commit()
    ensure_table(conn)   # idempotent migration
    ensure_table(conn)   # second call must not error or duplicate
    cols = {r[1] for r in conn.execute("PRAGMA table_info(paper_execution_outcomes)")}
    assert {
        "evidence_class", "frozen_at", "path_realized_r",
        "path_remaining_fraction", "path_last_candle_at", "path_tp1_filled",
        "path_tp2_filled", "path_tp3_filled", "path_max_mfe_r",
        "path_data_quality", "path_gap_seconds",
    } <= cols
    row = conn.execute("SELECT signal_id, version FROM paper_execution_outcomes").fetchall()
    assert row == [("legacy1", "old_v")]   # no row loss, no data mutation


# ---- 2026-07-09 follow-up: NULL evidence_class sweep (Part 3) ----------------------------------
def _minimal_schema(conn):
    conn.execute(
        "CREATE TABLE proposed_signals (signal_id TEXT PRIMARY KEY, symbol TEXT, direction TEXT, "
        "mode TEXT, tier TEXT, asset_class TEXT, setup_type TEXT, created_at TEXT, expires_at TEXT, "
        "suggested_entry REAL, entry_trigger REAL, entry_low REAL, stop_loss REAL, "
        "invalidation REAL, tp1 REAL, tp2 REAL, tp3 REAL)")
    conn.execute(
        "CREATE TABLE signal_outcomes (id INTEGER PRIMARY KEY, signal_id TEXT, checked_at TEXT, "
        "entry_triggered INTEGER, entry_triggered_at TEXT, entry_price_used REAL, tp1_hit INTEGER, "
        "tp2_hit INTEGER, tp3_hit INTEGER, stop_hit INTEGER, final_outcome TEXT, "
        "max_favorable_excursion_r REAL, notes TEXT, status TEXT, final_r REAL)")


def test_backfill_all_leaves_zero_null_evidence_class_rows():
    """After backfill_all() (the refresh entrypoint), NO paper_execution_outcomes row may have a NULL
    evidence_class — including rows OUTSIDE backfill_all's own join scope (here: 'orphan', whose
    signal_id no longer resolves through signal_outcomes/proposed_signals at all)."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    _minimal_schema(conn)
    ensure_table(conn)

    # in-scope signal: will be recomputed + classified normally by backfill_all's main query.
    conn.execute("INSERT INTO proposed_signals VALUES "
                 "('s-scope','BTC','long','intraday','A','crypto','breakout','2026-07-10T00:00:00+00:00',NULL,"
                 "100,100,100,99,99,101,102,103)")
    conn.execute("INSERT INTO signal_outcomes VALUES "
                 "(1,'s-scope','2026-07-10T00:10:00+00:00',1,'2026-07-10T00:00:00+00:00',100,1,0,0,1,"
                 "'loss',0.7,NULL,NULL,-1.0)")

    # orphan row: exists ONLY in paper_execution_outcomes (simulates a pruned/legacy row backfill_all's
    # JOIN can never reach) with evidence_class left NULL, as if written before the freeze column existed.
    conn.execute(
        "INSERT INTO paper_execution_outcomes (signal_id, economic_trade_key, risk_model, "
        "paper_execution_r, computed_at, version, evidence_class) VALUES "
        "('s-orphan','k-orphan','early_mfe_protection_v1',0.5,'2026-06-01T00:00:00+00:00','old_v',NULL)")

    # recoverable-but-unlinked row: signal_id NOT in proposed_signals, but a signal_outcomes row with a
    # real entry_triggered_at still exists -> evidence_class must be recovered from THAT, not defaulted.
    conn.execute("INSERT INTO signal_outcomes VALUES "
                 "(2,'s-recoverable','2026-07-10T01:00:00+00:00',1,'2026-07-10T00:30:00+00:00',50,1,0,0,0,"
                 "'win',1.2,NULL,NULL,1.0)")
    conn.execute(
        "INSERT INTO paper_execution_outcomes (signal_id, economic_trade_key, risk_model, "
        "paper_execution_r, computed_at, version, evidence_class) VALUES "
        "('s-recoverable','k-recoverable','early_mfe_protection_v1',0.5,'2026-06-01T00:00:00+00:00','old_v',NULL)")
    conn.commit()

    pre_final_r = conn.execute("SELECT signal_id, final_r FROM signal_outcomes ORDER BY signal_id").fetchall()

    stats = backfill_all(conn, now_iso="2026-07-10T02:00:00+00:00")

    remaining_null = conn.execute(
        "SELECT COUNT(*) FROM paper_execution_outcomes WHERE evidence_class IS NULL").fetchone()[0]
    assert remaining_null == 0

    by_sid = {r["signal_id"]: r["evidence_class"] for r in
              conn.execute("SELECT signal_id, evidence_class FROM paper_execution_outcomes")}
    assert by_sid["s-scope"] == EVIDENCE_FORWARD          # in-scope, entered post-freeze
    assert by_sid["s-orphan"] == EVIDENCE_BACKFILL         # unrecoverable -> safe default, never NULL
    assert by_sid["s-recoverable"] == EVIDENCE_FORWARD     # recovered via signal_outcomes, entered post-freeze

    # the orphan/unlinked fixup pass must NEVER touch signal_outcomes/final_r.
    post_final_r = conn.execute("SELECT signal_id, final_r FROM signal_outcomes ORDER BY signal_id").fetchall()
    assert pre_final_r == post_final_r

    assert stats["null_evidence_recovered"] == 1   # s-recoverable
    assert stats["null_evidence_defaulted"] == 1    # s-orphan


def test_backfill_evidence_class_only_is_idempotent_and_narrow():
    """A second sweep with nothing new to fix must be a no-op, and the fixup must only ever touch
    evidence_class/frozen_at — never paper_execution_r or any other accounting field."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    _minimal_schema(conn)
    ensure_table(conn)
    conn.execute(
        "INSERT INTO paper_execution_outcomes (signal_id, economic_trade_key, risk_model, "
        "paper_execution_r, touch_r, close_reason, computed_at, version, evidence_class) VALUES "
        "('s-x','k-x','early_mfe_protection_v1',0.5,1.0,'profit_lock_stop','2026-06-01T00:00:00+00:00','old_v',NULL)")
    conn.commit()

    first = backfill_evidence_class_only(conn, now_iso="2026-07-10T00:00:00+00:00")
    assert first["scanned"] == 1 and first["defaulted_backfill"] == 1
    row = conn.execute(
        "SELECT paper_execution_r, touch_r, close_reason, evidence_class FROM paper_execution_outcomes "
        "WHERE signal_id='s-x'").fetchone()
    assert (row["paper_execution_r"], row["touch_r"], row["close_reason"]) == (0.5, 1.0, "profit_lock_stop")
    assert row["evidence_class"] == EVIDENCE_BACKFILL

    second = backfill_evidence_class_only(conn, now_iso="2026-07-10T00:05:00+00:00")
    assert second["scanned"] == 0   # nothing left to fix -> no-op


def test_backfill_closes_entered_trade_when_later_revalidator_loses_entry_state():
    """A stale `entry_moved_away` row cannot erase a real historical entry.

    The tracker may append that non-entry state after a TP milestone. Backfill
    retains the first entry and resolves it at the original expiry with Model F.
    """
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    _minimal_schema(conn)
    ensure_table(conn)
    conn.execute(
        "INSERT INTO proposed_signals VALUES "
        "('s-expired','XLM','long','swing','A','crypto','breakout',"
        "'2026-07-10T00:00:00+00:00','2026-07-10T02:00:00+00:00',"
        "100,100,100,99,99,101,102,103)"
    )
    # Entry and TP1 were genuinely observed. The later row is a revalidation
    # result, not a lifecycle close, and therefore carries entry_triggered=0.
    conn.execute(
        "INSERT INTO signal_outcomes VALUES "
        "(1,'s-expired','2026-07-10T00:10:00+00:00',1,'2026-07-10T00:05:00+00:00',"
        "100,1,0,0,0,'open',0.7,NULL,'tp1_hit',NULL)"
    )
    conn.execute(
        "INSERT INTO signal_outcomes VALUES "
        "(2,'s-expired','2026-07-10T02:10:00+00:00',0,NULL,NULL,0,0,0,0,"
        "'no_entry',NULL,NULL,'entry_moved_away',NULL)"
    )
    before = conn.execute("SELECT id, final_r FROM signal_outcomes ORDER BY id").fetchall()

    stats = backfill_all(conn, now_iso="2026-07-10T03:00:00+00:00")
    row = conn.execute(
        "SELECT lifecycle_state, paper_execution_r, close_reason, exit_at, exit_at_source "
        "FROM paper_execution_outcomes WHERE signal_id='s-expired'"
    ).fetchone()
    assert stats["errors"] == 0 and stats["resolved"] == 1
    assert dict(row) == {
        "lifecycle_state": "CLOSED",
        "paper_execution_r": 0.0,
        "close_reason": "breakeven_stop",
        "exit_at": "2026-07-10T02:00:00+00:00",
        "exit_at_source": "expires_at_protected",
    }
    assert before == conn.execute("SELECT id, final_r FROM signal_outcomes ORDER BY id").fetchall()

    # A second refresh is deterministic and cannot reopen or mutate the source rows.
    again = backfill_all(conn, now_iso="2026-07-10T03:05:00+00:00")
    assert again["errors"] == 0
    assert conn.execute(
        "SELECT lifecycle_state FROM paper_execution_outcomes WHERE signal_id='s-expired'"
    ).fetchone()[0] == "CLOSED"


def test_backfill_keeps_unexpired_entered_trade_open():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    _minimal_schema(conn)
    ensure_table(conn)
    conn.execute(
        "INSERT INTO proposed_signals VALUES "
        "('s-active','BTC','long','swing','A','crypto','breakout',"
        "'2026-07-10T00:00:00+00:00','2026-07-11T00:00:00+00:00',"
        "100,100,100,99,99,101,102,103)"
    )
    conn.execute(
        "INSERT INTO signal_outcomes VALUES "
        "(1,'s-active','2026-07-10T00:10:00+00:00',1,'2026-07-10T00:05:00+00:00',"
        "100,0,0,0,0,'open',0.2,NULL,'triggered',NULL)"
    )
    backfill_all(conn, now_iso="2026-07-10T03:00:00+00:00")
    row = conn.execute(
        "SELECT lifecycle_state, paper_execution_r, close_reason FROM paper_execution_outcomes "
        "WHERE signal_id='s-active'"
    ).fetchone()
    assert dict(row) == {"lifecycle_state": "OPEN", "paper_execution_r": None, "close_reason": "open"}


def test_stock_intraday_next_session_touch_is_not_authoritative_paper_pnl():
    signal = {
        "signal_id": "overnight-stock", "symbol": "AAPL", "asset_class": "stocks", "mode": "intraday",
        "direction": "long", "created_at": "2026-07-08T19:00:00+00:00",
        "expires_at": "2026-07-09T19:00:00+00:00", "entry_trigger": 100.0,
        "invalidation": 98.0, "tp1": 104.0, "tp2": 106.0, "tp3": 108.0,
    }
    outcome = {
        "status": "tp3_hit", "checked_at": "2026-07-09T14:00:00+00:00",
        "entry_triggered": True, "entry_triggered_at": "2026-07-08T19:15:00+00:00",
        "entry_price_used": 100.0, "tp1_hit": True, "tp1_hit_at": "2026-07-09T13:30:00+00:00",
        "tp2_hit": True, "tp2_hit_at": "2026-07-09T13:30:00+00:00",
        "tp3_hit": True, "tp3_hit_at": "2026-07-09T13:30:00+00:00",
        "max_favorable_excursion_r": 4.0,
    }
    _, _, rec = build_record_from_signal(signal, outcome, as_of_iso="2026-07-09T14:00:00+00:00")
    assert rec["execution_validity"] == "invalid_stock_intraday_overnight_event"
    assert rec["lifecycle_state"] == "INVALID"
    assert rec["paper_execution_r"] is None
    assert rec["effective_expires_at"] == "2026-07-08T20:00:00+00:00"
def test_accounting_ignores_impossible_stock_expiry_before_creation():
    signal = {
        "asset_class": "stocks",
        "mode": "intraday",
        "created_at": "2026-07-28T22:00:00+00:00",
    }
    expiry = _effective_expiry(signal, "2026-07-28T20:00:00+00:00")
    assert expiry == datetime(2026, 7, 29, 20, 0, tzinfo=timezone.utc)
