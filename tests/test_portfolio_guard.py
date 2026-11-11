"""Portfolio-level risk guard (2026-07-13 audit) — the one REAL (non-diagnostic) kill-switch that
can actually pause new signal registration for BOTH crypto and stocks on a severe combined
drawdown. Read-only w.r.t. trading tables; never touches live/auto-live/manual-live.
"""
from __future__ import annotations

import sqlite3
from datetime import datetime, timedelta, timezone

from src.risk import portfolio_guard as pg

NOW = datetime(2026, 7, 13, 15, 0, tzinfo=timezone.utc)


def _rows(rs, asset_class="crypto"):
    return [{"asset_class": asset_class, "paper_execution_r": r} for r in rs]


# ---- pure evaluator -------------------------------------------------------------------------
def test_below_min_sample_never_blocks_even_on_deep_drawdown():
    cfg = {**pg._DEFAULT_CFG, "min_resolved_trades": 6}
    rows = _rows([-3.0, -3.0])  # only 2 trades, deeply negative
    state = pg.evaluate_portfolio_guard(rows, cfg=cfg)
    assert state.would_pause_new_signals is False
    assert state.resolved_trades == 2
    assert state.crypto_r == -6.0
    assert state.stocks_r == 0.0


def test_combined_drawdown_across_both_classes_blocks():
    cfg = {**pg._DEFAULT_CFG, "min_resolved_trades": 4, "pause_at_combined_r": -6.0}
    rows = _rows([-2.0, -2.0], "crypto") + _rows([-1.5, -1.5], "stocks")  # combined -7R, n=4
    state = pg.evaluate_portfolio_guard(rows, cfg=cfg)
    assert state.would_pause_new_signals is True
    assert state.combined_r == -7.0
    assert state.crypto_r == -4.0
    assert state.stocks_r == -3.0
    assert "combined" in state.reason


def test_healthy_combined_book_does_not_block():
    cfg = {**pg._DEFAULT_CFG, "min_resolved_trades": 4, "pause_at_combined_r": -6.0}
    rows = _rows([1.0, -0.5], "crypto") + _rows([0.5, 0.3], "stocks")
    state = pg.evaluate_portfolio_guard(rows, cfg=cfg)
    assert state.would_pause_new_signals is False


def test_one_asset_class_bleeding_but_combined_still_ok():
    # crypto alone would breach a per-asset -3R floor, but combined with a profitable stocks book
    # the aggregate stays above the combined threshold -- this guard judges the WHOLE book, not
    # either side alone (that's what the existing per-asset-class guards are for).
    cfg = {**pg._DEFAULT_CFG, "min_resolved_trades": 4, "pause_at_combined_r": -6.0}
    rows = _rows([-3.0, -1.0], "crypto") + _rows([2.0, 1.0], "stocks")  # combined -1R
    state = pg.evaluate_portfolio_guard(rows, cfg=cfg)
    assert state.would_pause_new_signals is False
    assert state.combined_r == -1.0


def test_disabled_config_never_blocks():
    cfg = {**pg._DEFAULT_CFG, "enabled": False}
    rows = _rows([-10.0] * 10)
    state = pg.evaluate_portfolio_guard(rows, cfg=cfg)
    assert state.would_pause_new_signals is False


def test_missing_r_values_are_skipped_not_treated_as_zero():
    cfg = {**pg._DEFAULT_CFG, "min_resolved_trades": 2}
    rows = [{"asset_class": "crypto", "paper_execution_r": None},
            {"asset_class": "crypto", "paper_execution_r": -5.0},
            {"asset_class": "stocks", "paper_execution_r": -5.0}]
    state = pg.evaluate_portfolio_guard(rows, cfg=cfg)
    assert state.resolved_trades == 2   # the None row doesn't count
    assert state.combined_r == -10.0


# ---- DB integration (real-shaped schema, temp file) -----------------------------------------
def _make_db(tmp_path):
    db = str(tmp_path / "pg.sqlite")
    c = sqlite3.connect(db)
    c.execute("CREATE TABLE proposed_signals (signal_id TEXT, asset_class TEXT, mode TEXT, "
              "created_at TEXT, tier TEXT)")
    c.execute("CREATE TABLE paper_execution_outcomes (signal_id TEXT, paper_execution_r REAL, "
              "close_reason TEXT, computed_at TEXT)")
    return db, c


def test_load_rows_joins_and_windows_by_signal_created_at(tmp_path):
    db, c = _make_db(tmp_path)
    fresh = (NOW - timedelta(hours=2)).isoformat()
    old = (NOW - timedelta(hours=48)).isoformat()
    c.execute("INSERT INTO proposed_signals VALUES ('s1','crypto','intraday',?,'B')", (fresh,))
    c.execute("INSERT INTO proposed_signals VALUES ('s2','stocks','intraday',?,'B')", (fresh,))
    c.execute("INSERT INTO proposed_signals VALUES ('s3','crypto','intraday',?,'B')", (old,))
    c.execute("INSERT INTO paper_execution_outcomes VALUES ('s1', -2.0, 'loss', ?)", (fresh,))
    c.execute("INSERT INTO paper_execution_outcomes VALUES ('s2', -1.0, 'loss', ?)", (fresh,))
    c.execute("INSERT INTO paper_execution_outcomes VALUES ('s3', -9.0, 'loss', ?)", (old,))
    c.commit(); c.close()

    cutoff = pg._cutoff_iso(24.0, NOW)
    rows = pg._load_rows(db, cutoff)
    assert len(rows) == 2  # the 48h-old row falls outside a 24h window
    assert round(sum(r["paper_execution_r"] for r in rows), 2) == -3.0


def test_load_rows_excludes_open_and_no_entry_trades(tmp_path):
    # 2026-07-13 review: must use the same canonical resolved-check as
    # crypto_overlay_counterfactual._closed_rows (close_reason NOT IN ('open','no_entry')), not
    # rely on paper_execution_r's null-ness alone.
    db, c = _make_db(tmp_path)
    fresh = (NOW - timedelta(hours=1)).isoformat()
    c.execute("INSERT INTO proposed_signals VALUES ('s1','crypto','intraday',?,'B')", (fresh,))
    c.execute("INSERT INTO proposed_signals VALUES ('s2','crypto','intraday',?,'B')", (fresh,))
    c.execute("INSERT INTO proposed_signals VALUES ('s3','crypto','intraday',?,'B')", (fresh,))
    c.execute("INSERT INTO paper_execution_outcomes VALUES ('s1', -9.0, 'loss', ?)", (fresh,))
    c.execute("INSERT INTO paper_execution_outcomes VALUES ('s2', -9.0, 'open', ?)", (fresh,))
    c.execute("INSERT INTO paper_execution_outcomes VALUES ('s3', -9.0, 'no_entry', ?)", (fresh,))
    c.commit(); c.close()

    cutoff = pg._cutoff_iso(24.0, NOW)
    rows = pg._load_rows(db, cutoff)
    assert len(rows) == 1
    assert rows[0]["paper_execution_r"] == -9.0


def test_portfolio_guard_state_end_to_end_blocks(tmp_path):
    db, c = _make_db(tmp_path)
    fresh = (NOW - timedelta(hours=1)).isoformat()
    for i in range(6):  # >= default min_resolved_trades
        sid = f"s{i}"
        c.execute("INSERT INTO proposed_signals VALUES (?,?,?,?,?)", (sid, "crypto", "intraday", fresh, "B"))
        c.execute("INSERT INTO paper_execution_outcomes VALUES (?, -2.0, 'loss', ?)", (sid, fresh))
    c.commit(); c.close()

    state = pg.portfolio_guard_state(db=db, now=NOW)
    assert state.would_pause_new_signals is True
    assert state.combined_r == -12.0

    should_block, reason = pg.blocks_new_signals(db=db, now=NOW)
    assert should_block is True
    assert "combined" in reason


def test_portfolio_guard_state_fails_open_on_missing_table(tmp_path):
    db = str(tmp_path / "empty.sqlite")
    sqlite3.connect(db).close()   # valid empty DB, no tables at all
    state = pg.portfolio_guard_state(db=db, now=NOW)
    assert state.would_pause_new_signals is False


def test_blocks_new_signals_appends_reconstructable_allow_audit(tmp_path):
    db, c = _make_db(tmp_path)
    fresh = (NOW - timedelta(hours=1)).isoformat()
    for i, r_value in enumerate((1.0, -0.5, 0.5, 0.25, -0.25, 1.0)):
        sid = f"a{i}"
        c.execute("INSERT INTO proposed_signals VALUES (?,?,?,?,?)", (sid, "crypto", "intraday", fresh, "B"))
        c.execute("INSERT INTO paper_execution_outcomes VALUES (?, ?, 'win', ?)",
                  (sid, r_value, fresh))
    c.commit(); c.close()

    blocked, _ = pg.blocks_new_signals(
        db=db, now=NOW,
        audit_context={"source": "test", "report_id": "r-allow", "candidate_count": 3,
                       "asset_classes": ["crypto", "stocks"]},
    )
    assert blocked is False
    c = sqlite3.connect(db)
    row = c.execute(
        "SELECT decision,candidate_count,skipped_candidate_count,report_id,combined_r,"
        "resolved_trades,asset_classes_json,guard_version FROM portfolio_guard_audit"
    ).fetchone()
    c.close()
    assert row[:4] == ("ALLOW", 3, 0, "r-allow")
    assert row[4] == 2.0 and row[5] == 6
    assert row[6] == '["crypto", "stocks"]'
    assert row[7] == "portfolio_guard_v3_actionable_sized_r"


def test_blocks_new_signals_audit_records_every_skipped_candidate(tmp_path):
    db, c = _make_db(tmp_path)
    fresh = (NOW - timedelta(hours=1)).isoformat()
    for i in range(6):
        sid = f"b{i}"
        c.execute("INSERT INTO proposed_signals VALUES (?,?,?,?,?)", (sid, "crypto", "intraday", fresh, "B"))
        c.execute("INSERT INTO paper_execution_outcomes VALUES (?, -2.0, 'loss', ?)", (sid, fresh))
    c.commit(); c.close()

    blocked, _ = pg.blocks_new_signals(
        db=db, now=NOW,
        audit_context={"report_id": "r-block", "candidate_count": 7,
                       "asset_classes": ["crypto"]},
    )
    assert blocked is True
    c = sqlite3.connect(db)
    row = c.execute(
        "SELECT decision,would_pause,candidate_count,skipped_candidate_count,combined_r "
        "FROM portfolio_guard_audit"
    ).fetchone()
    c.close()
    assert row == ("BLOCK", 1, 7, 7, -12.0)


def test_load_rows_uses_authoritative_actionability_and_size_weight(tmp_path):
    db, c = _make_db(tmp_path)
    fresh = (NOW - timedelta(hours=1)).isoformat()
    c.execute("CREATE TABLE signal_alerts (signal_id TEXT, telegram_status TEXT, payload_json TEXT, "
              "alert_type TEXT, sent_at TEXT)")
    candidates = [
        ("half", "crypto", "intraday", "B", -2.0),
        ("scalp", "crypto", "scalp", "B", -10.0),
        ("ctier", "stocks", "intraday", "C", -10.0),
        ("stock", "stocks", "intraday", "B", 2.0),
    ]
    for sid, asset, mode, tier, value in candidates:
        c.execute("INSERT INTO proposed_signals VALUES (?,?,?,?,?)", (sid, asset, mode, fresh, tier))
        c.execute("INSERT INTO paper_execution_outcomes VALUES (?, ?, 'loss', ?)", (sid, value, fresh))
    c.execute("INSERT INTO signal_alerts VALUES (?,?,?,?,?)",
              ("half", "sent", '{"cqo_quality_action":"HALF_SIZE","size_weight":0.5}',
               "paper_entry", fresh))
    c.execute("INSERT INTO signal_alerts VALUES (?,?,?,?,?)",
              ("scalp", "shadow_only", '{}', "paper_entry", fresh))
    c.execute("INSERT INTO signal_alerts VALUES (?,?,?,?,?)",
              ("stock", "sent", '{}', "paper_entry", fresh))
    c.commit(); c.close()

    rows = pg._load_rows(db, pg._cutoff_iso(24.0, NOW))

    assert len(rows) == 2
    assert round(sum(r["paper_execution_r"] for r in rows), 2) == 1.0
    half = next(r for r in rows if r["asset_class"] == "crypto")
    assert half["raw_paper_execution_r"] == -2.0
    assert half["paper_execution_r"] == -1.0
    assert half["size_weight"] == 0.5
