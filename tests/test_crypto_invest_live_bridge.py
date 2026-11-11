from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone

from src.live_execution.config import LiveCanaryConfig
from src.live_execution.crypto_invest_bridge import capture_forward_decisions
from src.live_execution.service import _daily_loss_guard_applies
from research_labs.regime_conditioned_continuation.src.forward_shadow import _mexc_quote, _native


NOW = datetime(2026, 8, 7, 12, 0, tzinfo=timezone.utc)
PROFILE = "profile-hash"


def _live_cfg() -> LiveCanaryConfig:
    return LiveCanaryConfig({
        "submission_enabled": True, "execution_mode": "live",
        "allocated_equity_usdt": 100.0, "fixed_risk_per_trade_usdt": 10.0,
        "fixed_max_concurrent_risk_usdt": 50.0,
        "daily_loss_exempt_risk_buckets": ["crypto_invest"],
        "credentials": {
            "access_key_env": "TEST_MEXC_ACCESS", "secret_key_env": "TEST_MEXC_SECRET",
            "arm_env": "TEST_MEXC_ARM", "arm_value": "ARMED",
        },
    })


def _route_cfg() -> dict:
    return {
        "enabled": True, "route_id": "route", "source_strategy_id": "strategy",
        "source_profile_hash": PROFILE, "live_strategy_version": "crypto_invest_v1",
        "mode": "invest", "entry_mode": "REGIME_RECLAIM", "risk_bucket": "crypto_invest",
        "risk_multiplier": 1.0, "fixed_risk_usdt": 10.0,
        "allowed_directions": ["long", "short"], "max_capture_age_seconds": 180,
        "max_mexc_spread_bps": 20,
    }


def _row(**updates: object) -> dict:
    row = {
        "decision_id": "source-1", "strategy_id": "strategy", "profile_hash": PROFILE,
        "symbol": "BTC/USDT", "direction": "long", "formed_at": NOW.isoformat(),
        "decision_at": NOW.isoformat(), "observed_at": NOW.isoformat(),
        "latency_seconds": 0.5, "status": "ELIGIBLE_FORWARD_ENTRY", "is_clean": 1,
        "entry_price": 100.0, "stop_price": 95.0,
        "targets_json": json.dumps([106.5, 111.5, 118.0]),
        "features_json": json.dumps({"mexc_quote": {"status": "ok", "spread_bps": 4.0}}),
    }
    row.update(updates)
    return row


def test_clean_forward_decision_queues_exactly_once(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("TEST_MEXC_ACCESS", "x")
    monkeypatch.setenv("TEST_MEXC_SECRET", "y")
    monkeypatch.setenv("TEST_MEXC_ARM", "ARMED")
    db = tmp_path / "bridge.sqlite"
    first = capture_forward_decisions(
        [_row()], db=db, route_cfg=_route_cfg(), live_cfg=_live_cfg(),
        universe=["BTC/USDT"], now=NOW,
    )
    second = capture_forward_decisions(
        [_row()], db=db, route_cfg=_route_cfg(), live_cfg=_live_cfg(),
        universe=["BTC/USDT"], now=NOW,
    )
    assert first["queued"] == 1 and first["risk_usdt"] == 10.0
    assert second["duplicate"] == 1 and second["queued"] == 0
    with sqlite3.connect(db) as conn:
        decision = json.loads(conn.execute(
            "SELECT decision_json FROM mexc_canary_decisions"
        ).fetchone()[0])
        assert decision["mode"] == "invest"
        assert decision["risk_bucket"] == "crypto_invest"
        assert decision["live_risk_multiplier"] == 1.0
        assert conn.execute("SELECT COUNT(*) FROM mexc_canary_outbox").fetchone()[0] == 1


def test_dirty_or_unreviewed_decisions_never_queue(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("TEST_MEXC_ACCESS", "x")
    monkeypatch.setenv("TEST_MEXC_SECRET", "y")
    monkeypatch.setenv("TEST_MEXC_ARM", "ARMED")
    result = capture_forward_decisions(
        [_row(is_clean=0), _row(decision_id="source-2", symbol="OTHER/USDT")],
        db=tmp_path / "blocked.sqlite", route_cfg=_route_cfg(), live_cfg=_live_cfg(),
        universe=["BTC/USDT"], now=NOW,
    )
    assert result["queued"] == 0 and result["rejected"] == 2
    assert result["reasons"] == {
        "NOT_CLEAN_ELIGIBLE": 1, "SYMBOL_NOT_IN_REVIEWED_UNIVERSE": 1,
    }


def test_crypto_invest_only_is_exempt_from_mode_daily_loss_guard() -> None:
    cfg = _live_cfg()
    assert _daily_loss_guard_applies({"risk_bucket": "crypto_invest"}, cfg) is False
    assert _daily_loss_guard_applies({"risk_bucket": "default"}, cfg) is True


def test_mexc_symbol_does_not_reuse_binance_1000_alias() -> None:
    assert _native("SHIB/USDT") == "1000SHIBUSDT"
    quote = _mexc_quote("PEPE/USDT", {
        "PEPE_USDT": {"symbol": "PEPE_USDT", "bid1": 1.0, "ask1": 1.001,
                      "fairPrice": 1.0005},
    })
    assert quote["status"] == "ok"
    assert quote["contract"] == "PEPE_USDT"
