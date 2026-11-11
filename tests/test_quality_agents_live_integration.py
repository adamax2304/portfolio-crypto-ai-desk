from __future__ import annotations

import hashlib
import json

from src.live_execution import store as live_store


def _record() -> dict:
    frozen = {
        "signal_id": "sig_live_quality_1",
        "symbol": "BTC/USDT",
        "asset_class": "crypto",
        "mode": "intraday",
        "direction": "long",
        "tier": "B",
        "score": 72,
        "entry_mode": "BREAKOUT_CONTINUATION",
        "entry_price": 100.0,
        "original_stop": 99.0,
        "tp1": 101.0,
        "tp2": 102.0,
        "tp3": 103.0,
        "entry_age_seconds": 2.0,
        "entry_time_basis": "point_in_time_current_bar",
        "current_price_revalidated": True,
        "paper_size_weight": 0.5,
        "live_risk_multiplier": 0.5,
        "economic_trade_key": "quality-live-key",
    }
    body = json.dumps(frozen, sort_keys=True, separators=(",", ":"))
    return {
        "decision_id": "decision-quality-1",
        "signal_id": frozen["signal_id"],
        "captured_at": "2026-09-19T12:00:00+00:00",
        "paper_alert_id": None,
        "symbol": frozen["symbol"],
        "mode": frozen["mode"],
        "entry_mode": frozen["entry_mode"],
        "eligible": 1,
        "state": "QUEUED",
        "rejection_reasons_json": "[]",
        "decision_json": json.dumps(frozen, sort_keys=True),
        "decision_hash": hashlib.sha256(body.encode()).hexdigest(),
        "config_hash": "cfg",
        "decision_context_type": "point_in_time",
        "economic_trade_key": frozen["economic_trade_key"],
        "parent_decision_id": None,
        "recovery_sequence": 0,
    }


def test_every_live_insert_captures_quality_snapshot_without_blocking(tmp_path) -> None:
    db = tmp_path / "live.sqlite"
    with live_store.connect(db) as conn:
        result = live_store.insert_decision(conn, _record(), queue=True)
        assert result["queued"] is True
        row = conn.execute(
            "SELECT decision_json FROM mexc_canary_decisions WHERE decision_id='decision-quality-1'"
        ).fetchone()
        frozen = json.loads(row[0])
        assert frozen["quality_agents"]["applied_action"] == "ALLOW"
        assert frozen["quality_agents"]["recommended_action"] in {
            "ALLOW", "ALLOW_HALF_SIZE", "ALLOW_NO_CATALYST_BOOST", "REVIEW_ONLY",
        }
        assert conn.execute("SELECT COUNT(*) FROM quality_agent_signal_verdicts").fetchone()[0] == 5
        assert conn.execute("SELECT COUNT(*) FROM mexc_canary_outbox").fetchone()[0] == 1
