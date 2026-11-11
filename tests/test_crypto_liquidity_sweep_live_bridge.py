from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone

from src.live_execution.config import LiveCanaryConfig
from src.live_execution.crypto_liquidity_sweep_bridge import capture_forward_sweeps
from src.live_execution.service import _maybe_reprice_swing_recovery


NOW = datetime(2026, 8, 28, 12, 0, tzinfo=timezone.utc)


def _live_cfg() -> LiveCanaryConfig:
    return LiveCanaryConfig({
        "capture_enabled": True,
        "submission_enabled": True,
        "execution_mode": "live",
        "allocated_equity_usdt": 100.0,
        "fixed_risk_per_trade_usdt": 10.0,
        "fixed_max_concurrent_risk_usdt": 50.0,
        "credentials": {
            "access_key_env": "TEST_MEXC_ACCESS",
            "secret_key_env": "TEST_MEXC_SECRET",
            "arm_env": "TEST_MEXC_ARM",
            "arm_value": "ARMED",
        },
    })


def _route_cfg() -> dict:
    return {
        "enabled": True,
        "route_id": "crypto_liquidity_sweep_live_v1",
        "source_strategy_id": "crypto_liquidity_sweep_v1",
        "source_profile_id": "crypto_liquidity_sweep_reversal_5m_v1",
        "source_shadow_lane": "shadow_crypto_liquidity_sweep",
        "live_strategy_version": "crypto_liquidity_sweep_reversal_5m_live_v1",
        "mode": "liquidity_sweep",
        "entry_mode": "LIQUIDITY_SWEEP",
        "risk_bucket": "crypto_liquidity_sweep",
        "risk_multiplier": 0.5,
        "fixed_risk_usdt": 10.0,
        "allowed_directions": ["long"],
        "market_regime_filter": {
            "enabled": True,
            "block_unknown": False,
            "blocked_regimes": ["risk_off", "bearish", "bearish_trend", "downtrend", "short"],
            "blocked_keywords": ["risk_off", "bearish", "downtrend", "short"],
        },
        "max_capture_age_seconds": 300,
        "required_data_status": "ok",
    }


def _row(**updates: object) -> dict:
    row = {
        "candidate_id": "clsv1-test",
        "strategy_id": "crypto_liquidity_sweep_v1",
        "profile_id": "crypto_liquidity_sweep_reversal_5m_v1",
        "shadow_lane": "shadow_crypto_liquidity_sweep",
        "eligibility_status": "eligible",
        "is_clean_for_edge": 1,
        "data_status": "ok",
        "symbol": "BTC/USDT",
        "direction": "long",
        "generated_at": NOW.isoformat(),
        "sweep_at": NOW.isoformat(),
        "decision_at": NOW.isoformat(),
        "entry_price": 100.0,
        "stop_price": 95.0,
        "tp1": 105.0,
        "tp2": 110.0,
        "tp3": 115.0,
    }
    row.update(updates)
    return row


def test_clean_fresh_sweep_queues_once(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("TEST_MEXC_ACCESS", "x")
    monkeypatch.setenv("TEST_MEXC_SECRET", "y")
    monkeypatch.setenv("TEST_MEXC_ARM", "ARMED")
    db = tmp_path / "sweep.sqlite"

    first = capture_forward_sweeps(
        [_row()], db=db, route_cfg=_route_cfg(), live_cfg=_live_cfg(), now=NOW,
    )
    second = capture_forward_sweeps(
        [_row()], db=db, route_cfg=_route_cfg(), live_cfg=_live_cfg(), now=NOW,
    )

    assert first["queued"] == 1 and first["risk_usdt"] == 5.0
    assert second["queued"] == 0 and second["duplicate"] == 1
    with sqlite3.connect(db) as conn:
        decision = json.loads(conn.execute(
            "SELECT decision_json FROM mexc_canary_decisions"
        ).fetchone()[0])
        assert decision["mode"] == "liquidity_sweep"
        assert decision["entry_mode"] == "LIQUIDITY_SWEEP"
        assert decision["risk_bucket"] == "crypto_liquidity_sweep"
        assert decision["live_risk_multiplier"] == 0.5
        assert decision["market_regime"] == "unknown"
        assert conn.execute("SELECT COUNT(*) FROM mexc_canary_outbox").fetchone()[0] == 1
        assert conn.execute(
            "SELECT COUNT(*) FROM mexc_canary_events WHERE event_type='LIQUIDITY_SWEEP_LIVE_CAPTURED'"
        ).fetchone()[0] == 1


def test_dirty_stale_or_wrong_profile_sweep_never_queues(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("TEST_MEXC_ACCESS", "x")
    monkeypatch.setenv("TEST_MEXC_SECRET", "y")
    monkeypatch.setenv("TEST_MEXC_ARM", "ARMED")
    result = capture_forward_sweeps(
        [
            _row(is_clean_for_edge=0),
            _row(candidate_id="stale", decision_at="2026-08-28T11:54:00+00:00"),
            _row(candidate_id="wrong", profile_id="unexpected"),
        ],
        db=tmp_path / "blocked.sqlite", route_cfg=_route_cfg(), live_cfg=_live_cfg(), now=NOW,
    )

    assert result["queued"] == 0 and result["rejected"] == 3
    assert result["reasons"] == {
        "NOT_CLEAN_ELIGIBLE": 1,
        "CAPTURE_TOO_OLD": 1,
        "PROFILE_ID_MISMATCH": 1,
    }


def test_sweep_live_canary_blocks_shorts_and_risk_off_or_short_regimes(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("TEST_MEXC_ACCESS", "x")
    monkeypatch.setenv("TEST_MEXC_SECRET", "y")
    monkeypatch.setenv("TEST_MEXC_ARM", "ARMED")
    result = capture_forward_sweeps(
        [
            _row(candidate_id="short-side", direction="short"),
            _row(candidate_id="risk-off", market_regime="risk_off"),
            _row(candidate_id="short-regime", crypto_market_mode="bearish trend"),
        ],
        db=tmp_path / "blocked-regime.sqlite",
        route_cfg=_route_cfg(),
        live_cfg=_live_cfg(),
        now=NOW,
    )

    assert result["queued"] == 0 and result["rejected"] == 3
    assert result["reasons"] == {
        "DIRECTION_NOT_ALLOWED": 1,
        "MARKET_REGIME_BLOCKED": 2,
    }


def test_liquidity_sweep_allows_normal_derivatives_processing_lag(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("TEST_MEXC_ACCESS", "x")
    monkeypatch.setenv("TEST_MEXC_SECRET", "y")
    monkeypatch.setenv("TEST_MEXC_ARM", "ARMED")

    result = capture_forward_sweeps(
        [_row(candidate_id="normal-processing-lag", decision_at="2026-08-28T11:57:55+00:00")],
        db=tmp_path / "processing-lag.sqlite",
        route_cfg=_route_cfg(),
        live_cfg=_live_cfg(),
        now=NOW,
    )

    assert result["queued"] == 1
    assert result["rejected"] == 0


def test_liquidity_sweep_reprices_small_venue_move_with_same_r_ladder() -> None:
    cfg = LiveCanaryConfig({
        "liquidity_sweep_live_recovery": {
            "enabled": True,
            "entry_modes": ["LIQUIDITY_SWEEP"],
            "max_adverse_drift_bps": {"LIQUIDITY_SWEEP": 75},
        },
        "entry_limits_by_mode": {
            "liquidity_sweep": {"max_reprice_adverse_drift_bps": {"LIQUIDITY_SWEEP": 75}}
        },
    })
    decision = {
        "asset_class": "crypto", "mode": "liquidity_sweep", "entry_mode": "LIQUIDITY_SWEEP",
        "direction": "long", "entry_price": 100.0, "original_stop": 98.0,
        "tp1": 101.0, "tp2": 102.0, "tp3": 103.0,
    }
    updated, recovery = _maybe_reprice_swing_recovery(
        decision=decision,
        contract={"priceUnit": 0.01},
        depth={"asks": [[100.5, 1]], "bids": [[100.45, 1]]},
        cfg=cfg,
    )

    assert recovery and recovery["reason"] == "liquidity_sweep_exchange_reprice"
    assert recovery["adverse_drift_bps"] == 50.0
    assert updated["original_stop"] == 98.49
    assert updated["tp1"] == 101.5
    assert updated["tp2"] == 102.51
    assert updated["tp3"] == 103.51
