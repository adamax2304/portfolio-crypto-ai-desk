import json
import sqlite3
from datetime import datetime, timedelta, timezone

from src.stocks.preopen_lifecycle import repair_bug_expired_actionable_plans


UTC = timezone.utc


def _database(tmp_path):
    path = tmp_path / "preopen-lifecycle.sqlite"
    now = datetime.now(UTC)
    created = now - timedelta(minutes=30)
    bad_expiry = created - timedelta(hours=4)
    target_open = now - timedelta(minutes=5)
    target_close = now + timedelta(hours=6)
    with sqlite3.connect(path) as conn:
        conn.executescript("""
            CREATE TABLE proposed_signals (
                signal_id TEXT PRIMARY KEY, created_at TEXT, updated_at TEXT,
                status TEXT, asset_class TEXT, mode TEXT
            );
            CREATE TABLE stocks_preus_actionability (
                signal_id TEXT PRIMARY KEY, decision TEXT, valid_until TEXT,
                target_session_close_at TEXT, reactivated INTEGER DEFAULT 0
            );
            CREATE TABLE stocks_paper_decision_snapshots (
                signal_id TEXT PRIMARY KEY, captured_at TEXT NOT NULL,
                decision_at TEXT NOT NULL, signal_created_at TEXT NOT NULL,
                symbol TEXT NOT NULL, direction TEXT NOT NULL, source_tier TEXT,
                pre_gate_tier TEXT, funnel_state TEXT NOT NULL,
                target_session_open_at TEXT, target_session_close_at TEXT,
                snapshot_json TEXT NOT NULL, version TEXT NOT NULL
            );
            CREATE TABLE paper_execution_outcomes (
                signal_id TEXT PRIMARY KEY, effective_expires_at TEXT
            );
        """)
        conn.execute(
            "INSERT INTO proposed_signals VALUES (?,?,?,?,?,?)",
            ("plan-1", created.isoformat(), created.isoformat(),
             "missed_no_entry", "stocks", "intraday"),
        )
        conn.execute(
            "INSERT INTO stocks_preus_actionability VALUES (?,?,?,?,0)",
            ("plan-1", "ACTIONABLE", target_close.isoformat(), target_close.isoformat()),
        )
        conn.execute(
            "INSERT INTO stocks_paper_decision_snapshots VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                "plan-1", created.isoformat(), created.isoformat(), created.isoformat(),
                "AAPL", "long", "C", "B", "PREOPEN_PLAN",
                target_open.isoformat(), target_close.isoformat(),
                json.dumps({"pre_gate_tier": "B"}), "test",
            ),
        )
        conn.execute(
            "INSERT INTO paper_execution_outcomes VALUES (?,?)",
            ("plan-1", bad_expiry.isoformat()),
        )
        conn.commit()
    return path, now


def test_only_proven_impossible_expiry_is_reactivated(tmp_path):
    path, now = _database(tmp_path)
    result = repair_bug_expired_actionable_plans(path, now=now)
    assert result["signal_ids"] == ["plan-1"]
    with sqlite3.connect(path) as conn:
        assert conn.execute(
            "SELECT status FROM proposed_signals WHERE signal_id='plan-1'"
        ).fetchone()[0] == "waiting_for_entry"
        assert conn.execute(
            "SELECT reactivated FROM stocks_preus_actionability WHERE signal_id='plan-1'"
        ).fetchone()[0] == 1
        assert conn.execute(
            "SELECT COUNT(*) FROM stocks_paper_funnel_events "
            "WHERE stage='PREOPEN_PLAN_REACTIVATED'"
        ).fetchone()[0] == 1
        conn.execute(
            "UPDATE proposed_signals SET status='missed_no_entry' "
            "WHERE signal_id='plan-1'"
        )
        conn.commit()
    second = repair_bug_expired_actionable_plans(path, now=now)
    assert second["repaired"] == 0
    with sqlite3.connect(path) as conn:
        assert conn.execute(
            "SELECT status FROM proposed_signals WHERE signal_id='plan-1'"
        ).fetchone()[0] == "missed_no_entry"


def test_valid_expiry_is_never_reactivated(tmp_path):
    path, now = _database(tmp_path)
    with sqlite3.connect(path) as conn:
        created = conn.execute(
            "SELECT created_at FROM proposed_signals WHERE signal_id='plan-1'"
        ).fetchone()[0]
        conn.execute(
            "UPDATE paper_execution_outcomes SET effective_expires_at=?",
            ((datetime.fromisoformat(created) + timedelta(hours=6)).isoformat(),),
        )
        conn.commit()
    result = repair_bug_expired_actionable_plans(path, now=now)
    assert result["repaired"] == 0
    with sqlite3.connect(path) as conn:
        assert conn.execute(
            "SELECT status FROM proposed_signals WHERE signal_id='plan-1'"
        ).fetchone()[0] == "missed_no_entry"
