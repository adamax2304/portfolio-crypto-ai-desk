from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from src.live_execution.config import LiveCanaryConfig
from src.live_execution import crypto_fallback_capture


NOW = datetime(2026, 9, 4, 12, 0, tzinfo=timezone.utc)


def _live_cfg() -> LiveCanaryConfig:
    return LiveCanaryConfig({
        "capture_enabled": True,
        "submission_enabled": False,
        "execution_mode": "dry_run",
        "allowed_asset_class": "crypto",
        "allowed_modes": ["swing"],
        "allowed_entry_modes": ["BREAKOUT_CONTINUATION"],
        "allowed_entry_modes_by_mode": {"swing": ["BREAKOUT_CONTINUATION"]},
        "allowed_strategy_versions_by_mode": {"swing": ["crypto_swing_paper_t130_v1"]},
        "allowed_directions": ["long", "short"],
        "allowed_tiers": ["A", "B"],
        "allowed_paper_actions": ["FULL_SIZE", "HALF_SIZE"],
        "required_preentry_sources": ["entry_path"],
        "required_preentry_data_quality": "ok",
        "entry_limits_by_mode": {
            "swing": {
                "max_entry_age_seconds": {"BREAKOUT_CONTINUATION": 300},
                "max_entry_drift_bps": {"BREAKOUT_CONTINUATION": 75},
            },
        },
    })


def _seed(db: Path, *, with_alert: bool = True) -> None:
    with sqlite3.connect(db) as conn:
        conn.executescript(
            """
            CREATE TABLE proposed_signals(
              signal_id TEXT PRIMARY KEY, created_at TEXT, symbol TEXT,
              direction TEXT, mode TEXT, tier TEXT, score REAL,
              asset_class TEXT, entry_type TEXT, raw_idea_json TEXT
            );
            CREATE TABLE paper_execution_outcomes(
              signal_id TEXT PRIMARY KEY, computed_at TEXT, lifecycle_state TEXT,
              execution_validity TEXT, entry_at TEXT, decision_at TEXT,
              entry_price_used REAL, stop_initial REAL, entry_time_basis TEXT,
              current_price_revalidated INTEGER, close_reason TEXT,
              paper_entry_profile TEXT, paper_execution_entry_mode TEXT
            );
            CREATE TABLE signal_alerts(
              alert_id TEXT PRIMARY KEY, signal_id TEXT, alert_type TEXT,
              sent_at TEXT, payload_json TEXT
            );
            """
        )
        conn.execute(
            "INSERT INTO proposed_signals VALUES(?,?,?,?,?,?,?,?,?,?)",
            (
                "sig-crypto-fallback", NOW.isoformat(), "BTC/USDT", "long",
                "swing", "A", 88.0, "crypto", "limit", "{}",
            ),
        )
        conn.execute(
            "INSERT INTO paper_execution_outcomes VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                "sig-crypto-fallback", NOW.isoformat(), "OPEN", "valid",
                NOW.isoformat(), NOW.isoformat(), 100.0, 98.0,
                "point_in_time_current_bar", 1, "open",
                "crypto_swing_paper_t130_v1", "BREAKOUT_CONTINUATION",
            ),
        )
        if with_alert:
            payload = {
                "entry_used": 100.0,
                "stop": 98.0,
                "tp1": 103.0,
                "tp2": 106.0,
                "tp3": 110.0,
                "entry_triggered_at": NOW.isoformat(),
                "entry_age_seconds": 5,
                "entry_time_basis": "point_in_time_current_bar",
                "current_price_revalidated": True,
                "telegram_channel": "telegram",
                "size_weight": 1.0,
                "cqo_quality_action": "FULL_SIZE",
                "crypto_swing_main_paper_action": "FULL_SIZE",
                "cqo_entry_mode": "BREAKOUT_CONTINUATION",
                "cqo_entry_mode_source": "entry_path",
                "cqo_preentry_data_quality": "ok",
                "cqo_snapshot_persisted": True,
                "paper_entry_profile": "crypto_swing_paper_t130_v1",
                "paper_execution_entry_mode": "BREAKOUT_CONTINUATION",
            }
            conn.execute(
                "INSERT INTO signal_alerts VALUES(?,?,?,?,?)",
                ("alert-1", "sig-crypto-fallback", "paper_entry", NOW.isoformat(), json.dumps(payload)),
            )
        conn.commit()


def test_crypto_live_fallback_replays_fresh_alert_payload(tmp_path, monkeypatch) -> None:
    db = tmp_path / "fallback.sqlite"
    _seed(db, with_alert=True)
    captured: list[dict] = []

    def fake_capture(**kwargs):
        captured.append(kwargs)
        return {"status": "QUEUED", "queued": True, "reasons": []}

    monkeypatch.setattr(crypto_fallback_capture, "capture_paper_candidate", fake_capture)
    monkeypatch.setattr(
        crypto_fallback_capture, "route",
        lambda **kwargs: {"enabled": True},
    )

    result = crypto_fallback_capture.capture_recent_missing(
        db=db, live_cfg=_live_cfg(), now=NOW,
    )

    assert result["seen"] == 1
    assert result["captured"] == 1
    assert result["queued"] == 1
    assert captured[0]["signal"]["signal_id"] == "sig-crypto-fallback"
    assert captured[0]["payload"]["paper_execution_entry_mode"] == "BREAKOUT_CONTINUATION"


def test_crypto_live_fallback_records_missing_alert_diagnostic(tmp_path, monkeypatch) -> None:
    db = tmp_path / "fallback-missing-alert.sqlite"
    _seed(db, with_alert=False)
    monkeypatch.setattr(
        crypto_fallback_capture, "route",
        lambda **kwargs: {"enabled": True},
    )

    result = crypto_fallback_capture.capture_recent_missing(
        db=db, live_cfg=_live_cfg(), now=NOW,
    )

    assert result["seen"] == 1
    assert result["missing_alert"] == 1
    assert result["rejected"] == 1
    with sqlite3.connect(db) as conn:
        row = conn.execute(
            "SELECT state,rejection_reasons_json FROM mexc_canary_decisions"
        ).fetchone()
    assert row[0] == "REJECTED_DIAGNOSTIC"
    assert json.loads(row[1]) == ["PAPER_ENTRY_ALERT_MISSING"]
