from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone

from src.stocks import paper_funnel
from src.stocks.monitor import StocksMonitorSession
from src.config import ProjectConfig
from src.signals.pending_monitor import leader_lock


UTC = timezone.utc


def _db(tmp_path):
    path = tmp_path / "desk.sqlite"
    conn = sqlite3.connect(path)
    conn.execute(
        "CREATE TABLE proposed_signals ("
        "signal_id TEXT PRIMARY KEY, asset_class TEXT, mode TEXT, symbol TEXT, direction TEXT,"
        "created_at TEXT, tier TEXT, status TEXT, raw_idea_json TEXT, score REAL,"
        "entry_low REAL,entry_high REAL,entry_trigger REAL,suggested_entry REAL,"
        "stop_loss REAL,invalidation REAL,tp1 REAL,tp2 REAL,tp3 REAL,setup_type TEXT,market_regime TEXT)"
    )
    return path, conn


def _insert(conn, *, signal_id="s1", tier="B", caps=None, status="waiting_for_entry"):
    conn.execute(
        "INSERT INTO proposed_signals VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (signal_id, "stocks", "intraday", "AAPL", "long", "2026-07-27T14:00:00+00:00",
         tier, status, json.dumps({"decision_at": "2026-07-27T14:00:00+00:00",
                                   "pre_gate_tier": "B", "cap_reasons": caps or []}),
         75.0, 99.0, 100.0, 100.0, 100.0, 98.0, 98.0, 102.0, 104.0, 106.0,
         "pullback", "trend_up"),
    )
    conn.commit()


def test_rth_snapshot_is_immutable_after_postclose_mutation(tmp_path):
    path, conn = _db(tmp_path)
    _insert(conn)
    row = dict(zip([x[1] for x in conn.execute("PRAGMA table_info(proposed_signals)")],
                   conn.execute("SELECT * FROM proposed_signals WHERE signal_id='s1'").fetchone()))
    assert paper_funnel.snapshot_row(conn, row, now=datetime(2026, 7, 27, 14, 0, tzinfo=UTC))
    conn.execute(
        "UPDATE proposed_signals SET tier='C',raw_idea_json=? WHERE signal_id='s1'",
        (json.dumps({"pre_gate_tier": "B", "cap_reasons": [
            "market_closed_intraday_planning_only"]}),),
    )
    changed = dict(zip([x[1] for x in conn.execute("PRAGMA table_info(proposed_signals)")],
                       conn.execute("SELECT * FROM proposed_signals WHERE signal_id='s1'").fetchone()))
    assert not paper_funnel.snapshot_row(conn, changed)
    snap = conn.execute(
        "SELECT source_tier,funnel_state,snapshot_json FROM stocks_paper_decision_snapshots WHERE signal_id='s1'"
    ).fetchone()
    assert snap[0] == "B" and snap[1] == "RTH_ELIGIBLE"
    assert json.loads(snap[2])["cap_reasons"] == []
    conn.close()
    assert paper_funnel.active_eligible_signal_ids(path) == ["s1"]


def test_preopen_plan_never_becomes_fast_tracker_candidate(tmp_path):
    path, conn = _db(tmp_path)
    _insert(conn, caps=["market_closed_intraday_planning_only"], tier="C")
    row = dict(zip([x[1] for x in conn.execute("PRAGMA table_info(proposed_signals)")],
                   conn.execute("SELECT * FROM proposed_signals WHERE signal_id='s1'").fetchone()))
    paper_funnel.snapshot_row(conn, row)
    conn.close()
    assert paper_funnel.active_eligible_signal_ids(path) == []


def test_funnel_event_is_append_only(tmp_path):
    path, conn = _db(tmp_path)
    _insert(conn)
    row = dict(zip([x[1] for x in conn.execute("PRAGMA table_info(proposed_signals)")],
                   conn.execute("SELECT * FROM proposed_signals WHERE signal_id='s1'").fetchone()))
    paper_funnel.snapshot_row(conn, row)
    paper_funnel.record_event(conn, signal_id="s1", stage="TOUCH_OBSERVED", reason="current_price_ok")
    paper_funnel.record_event(conn, signal_id="s1", stage="PAPER_ENTERED")
    # Initial snapshot writes its own funnel-state event, followed by the two
    # explicit lifecycle events above.
    assert conn.execute("SELECT COUNT(*) FROM stocks_paper_funnel_events").fetchone()[0] == 3
    conn.commit()
    data = paper_funnel.report(path)
    assert data["snapshot_states"] == {"RTH_ELIGIBLE": 1}
    assert "AAPL" in paper_funnel.render_markdown(data)


def test_stock_monitor_declines_a_second_leader(tmp_path):
    config = ProjectConfig(
        root=tmp_path,
        settings={"data": {"db_path": "db/desk.sqlite"}}, watchlist={}, sources={},
        scoring={}, universe={}, exchanges={},
    )
    with leader_lock(tmp_path, "stocks", worker_id="first", ttl_sec=180) as heartbeat:
        assert heartbeat is not None
        session = StocksMonitorSession(config, minutes=0, send_telegram=False)
        result = session.run()
    assert len(result) == 1
    assert result[0].decisions[0]["reason"] == "leader_active"
