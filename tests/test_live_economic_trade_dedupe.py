from __future__ import annotations

import json
import uuid

from src.live_execution import store as ls


def _record(signal_id: str, *, key: str, parent: str | None = None) -> dict:
    decision_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"test:{signal_id}"))
    return {
        "decision_id": decision_id,
        "signal_id": signal_id,
        "captured_at": "2026-08-30T12:00:00+00:00",
        "paper_alert_id": None,
        "symbol": "ETH/USDT",
        "mode": "swing",
        "entry_mode": "BREAKOUT_CONTINUATION",
        "eligible": 1,
        "state": "QUEUED",
        "rejection_reasons_json": "[]",
        "decision_json": json.dumps({"signal_id": signal_id, "economic_trade_key": key}),
        "decision_hash": signal_id,
        "config_hash": "cfg",
        "decision_context_type": "point_in_time",
        "economic_trade_key": key,
        "parent_decision_id": parent,
        "recovery_sequence": 1 if parent else 0,
    }


def test_second_signal_for_same_economic_trade_is_not_queued(tmp_path):
    db = tmp_path / "live.sqlite"
    with ls.connect(db) as conn:
        first = _record("signal-1", key="ETH|swing|breakout|2026-08-30")
        second = _record("signal-2", key="ETH|swing|breakout|2026-08-30")
        assert ls.insert_decision(conn, first, queue=True)["queued"]
        result = ls.insert_decision(conn, second, queue=True)
        assert not result["queued"]
        assert result["duplicate_economic_trade"]
        row = conn.execute(
            "SELECT state,rejection_reasons_json FROM mexc_canary_decisions WHERE signal_id='signal-2'"
        ).fetchone()
        assert row["state"] == "REJECTED_DUPLICATE_ECONOMIC_TRADE"
        assert "DUPLICATE_ECONOMIC_TRADE" in json.loads(row["rejection_reasons_json"])


def test_one_explicit_recovery_can_bypass_only_its_parent(tmp_path):
    db = tmp_path / "live.sqlite"
    key = "ETH|swing|breakout|2026-08-30"
    with ls.connect(db) as conn:
        source = _record("source", key=key)
        assert ls.insert_decision(conn, source, queue=True)["queued"]
        recovery = _record("recovery-1", key=key, parent=source["decision_id"])
        assert ls.insert_decision(conn, recovery, queue=True)["queued"]
        second = _record("recovery-2", key=key, parent=source["decision_id"])
        result = ls.insert_decision(conn, second, queue=True)
        assert not result["queued"]
        assert result["duplicate_economic_trade"]
