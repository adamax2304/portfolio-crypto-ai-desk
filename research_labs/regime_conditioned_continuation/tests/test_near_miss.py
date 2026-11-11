from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone

import pandas as pd

from research_labs.regime_conditioned_continuation.src import near_miss


NOW = datetime(2026, 8, 25, 12, 0, tzinfo=timezone.utc)


def _row(**updates: object) -> dict[str, object]:
    reference_at = "2026-08-25T00:00:00+00:00"
    row: dict[str, object] = {
        "decision_id": "decision-1",
        "candidate_id": "candidate-1",
        "strategy_id": "crypto_regime_conditioned_continuation_v2",
        "profile_hash": "profile",
        "symbol": "TEST/USDT",
        "direction": "long",
        "formed_at": "2026-08-24T20:00:00+00:00",
        "decision_at": reference_at,
        "observed_at": reference_at,
        "created_at": reference_at,
        "status": "REJECTED",
        "rejection_reason": "RSI_RESET_NOT_CONFIRMED",
        "is_clean": 1,
        "features_json": json.dumps({
            "zone": {"atr": 1.0},
            "near_miss_reference": {
                "at": reference_at,
                "price": 100.0,
                "source": "last_closed_15m_close",
                "risk_unit_price": 1.0,
                "risk_unit_source": "zone_atr_proxy",
                "targets_r": [1.3, 2.3, 3.6],
            },
        }),
        "geometry_json": "{}",
        "source_times_json": "{}",
    }
    row.update(updates)
    return row


def test_record_is_idempotent_and_labels_failure_stage(tmp_path) -> None:
    db = tmp_path / "near_miss.sqlite"
    first = near_miss.record_decisions([_row()], frozen_run_id="run-1", db=db)
    second = near_miss.record_decisions([_row()], frozen_run_id="run-1", db=db)

    assert first == {"seen": 1, "inserted": 1, "duplicate": 0}
    assert second == {"seen": 1, "inserted": 0, "duplicate": 1}
    with sqlite3.connect(db) as conn:
        stage = conn.execute(
            "SELECT stage_reached,failed_stage,rejection_reason FROM near_miss_snapshots"
        ).fetchone()
    assert stage == ("REGIME_AND_DERIVATIVES", "RSI_RESET", "RSI_RESET_NOT_CONFIRMED")


def test_outcomes_are_proxy_only_and_use_first_event_order(tmp_path) -> None:
    db = tmp_path / "near_miss.sqlite"
    near_miss.record_decisions([_row()], db=db)
    opened = pd.date_range("2026-08-25T00:15:00Z", periods=16, freq="15min")
    bars = pd.DataFrame({
        "bar_open_at": opened,
        "bar_close_at": opened + pd.Timedelta(minutes=15) - pd.Timedelta(milliseconds=1),
        "open": [100.0] * len(opened),
        "high": [101.5] + [101.0] * (len(opened) - 1),
        "low": [99.5] * len(opened),
        "close": [101.0] * len(opened),
    })
    result = near_miss.refresh_outcomes(lambda _symbol, _now: bars, now=NOW, db=db)

    assert result == {"snapshots": 1, "updated": 3}
    with sqlite3.connect(db) as conn:
        rows = conn.execute(
            "SELECT horizon_hours,outcome_status,first_event,official_metrics_excluded "
            "FROM near_miss_outcomes ORDER BY horizon_hours"
        ).fetchall()
    assert rows == [
        (4, "RESOLVED", "TP1_BEFORE_STOP", 1),
        (24, "PENDING", None, 1),
        (72, "PENDING", None, 1),
    ]


def test_legacy_rows_without_an_asof_price_stay_funnel_only(tmp_path) -> None:
    db = tmp_path / "near_miss.sqlite"
    row = _row(features_json=json.dumps({"zone": {"atr": 1.0}}))
    near_miss.record_decisions([row], db=db)
    refreshed = near_miss.refresh_outcomes(lambda _symbol, _now: pd.DataFrame(), now=NOW, db=db)

    assert refreshed == {"snapshots": 0, "updated": 0}
    with sqlite3.connect(db) as conn:
        assert conn.execute("SELECT COUNT(*) FROM near_miss_outcomes").fetchone()[0] == 0
