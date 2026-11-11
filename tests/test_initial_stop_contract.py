from __future__ import annotations

import json
import sqlite3
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import pytest

from src.execution.stop_contract import (
    build_initial_stop_contract,
    is_structural_stop_contract,
    stock_intraday_structural_stop_contract,
)
from src.execution.crypto_breakout_stop_profile import (
    PROFILE_VERSION as CRYPTO_BREAKOUT_STOP_PROFILE,
    apply_wider_125_if_crypto_breakout,
)
from src.live_execution.config import LiveCanaryConfig, load_live_canary_config
from src.live_execution.policy import evaluate_paper_candidate
from src.live_execution.sizing import rebase_filled_plan
from src.signals.config import SignalTrackingConfig


class FakeStore:
    def __init__(self, path: Path):
        self.db_path = path

    def connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn


def _cfg(**updates) -> LiveCanaryConfig:
    raw = deepcopy(load_live_canary_config().raw)
    raw.update({"submission_enabled": False, "execution_mode": "dry_run"})
    raw.update(updates)
    return LiveCanaryConfig(raw=raw)


def _store(path: Path) -> FakeStore:
    with sqlite3.connect(path) as conn:
        conn.executescript(
            """
            CREATE TABLE entry_latency_audit (
              signal_id TEXT PRIMARY KEY, cause TEXT, data_gap_min REAL
            );
            CREATE TABLE proposed_signals(signal_id TEXT PRIMARY KEY);
            CREATE TABLE signal_outcomes(id INTEGER PRIMARY KEY, final_r REAL);
            CREATE TABLE paper_portfolio_ledger(id INTEGER PRIMARY KEY);
            CREATE TABLE signal_alerts(alert_id TEXT PRIMARY KEY);
            """
        )
        conn.execute("INSERT INTO entry_latency_audit VALUES('sig-stop-contract','OK',0)")
    return FakeStore(path)


def test_crypto_support_stop_contract_is_structural():
    contract = build_initial_stop_contract(
        symbol="BTC/USDT",
        asset_class="crypto",
        mode="swing",
        direction="long",
        entry_price=100.0,
        stop_price=94.7,
        setup={
            "timeframe": "1h",
            "support": 95.0,
            "atr": 2.0,
            "stop_source": "support_resistance",
            "stop_model": "support_minus_atr_buffer_v1",
        },
    )
    assert contract["stop_source"] == "support_resistance"
    assert contract["geometry_valid"] is True
    assert is_structural_stop_contract(contract) is True


def test_stock_intraday_structural_stop_candidate_uses_nearby_level():
    frame = pd.DataFrame(
        {
            "high": [101.0, 102.0, 102.5, 103.0],
            "low": [98.0, 99.0, 99.5, 100.2],
            "close": [100.0, 101.0, 102.0, 102.4],
        }
    )
    contract = stock_intraday_structural_stop_contract(
        symbol="V",
        direction="long",
        entry_price=102.4,
        exec_frame=frame,
        atr_value=2.0,
        vwap=101.0,
    )
    assert contract["stop_source"] == "stock_intraday_structure"
    assert contract["stop_price"] < 102.4
    assert is_structural_stop_contract(contract) is True


def test_live_policy_carries_stop_contract(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "src.live_execution.policy.registered_route",
        lambda **kwargs: {"enabled": True},
    )
    stop_contract = build_initial_stop_contract(
        symbol="BTC/USDT",
        asset_class="crypto",
        mode="swing",
        direction="long",
        entry_price=100.0,
        stop_price=98.0,
        setup={
            "timeframe": "1h",
            "support": 98.3,
            "atr": 2.0,
            "stop_source": "support_resistance",
            "stop_model": "support_minus_atr_buffer_v1",
        },
    )
    signal = {
        "signal_id": "sig-stop-contract",
        "asset_class": "crypto",
        "mode": "swing",
        "direction": "long",
        "tier": "A",
        "score": 82,
        "symbol": "BTC/USDT",
        "created_at": "2026-08-17T00:00:00+00:00",
        "raw_idea_json": json.dumps({"initial_stop_contract": stop_contract}),
    }
    payload = {
        "entry_used": 100.0,
        "stop": 98.0,
        "tp1": 103.0,
        "tp2": 106.0,
        "tp3": 110.0,
        "entry_triggered_at": "2026-08-17T00:00:00+00:00",
        "entry_age_seconds": 10,
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
        "cqo_overlay_version": "cqo_v1",
        "cqo_overlay_config_hash": "abc123",
        "paper_entry_profile": "crypto_swing_paper_t130_v1",
    }
    record = evaluate_paper_candidate(
        signal=signal,
        payload=payload,
        cfg=_cfg(
            allowed_entry_modes=["BREAKOUT_CONTINUATION"],
            allowed_entry_modes_by_mode={"swing": ["BREAKOUT_CONTINUATION"]},
            allowed_strategy_versions_by_mode={
                "swing": ["crypto_swing_paper_t130_v1"],
            },
        ),
        store=_store(tmp_path / "live-policy.sqlite"),
        now=datetime(2026, 8, 17, 0, 0, 10, tzinfo=timezone.utc),
    )
    assert record["state"] == "QUEUED"
    frozen = json.loads(record["decision_json"])
    assert frozen["stop_contract"]["stop_source"] == "support_resistance"
    assert frozen["stop_label"]


def test_fill_rebase_preserves_structural_stop_when_budget_allows():
    plan = {
        "direction": "long",
        "limit_price": 100.0,
        "original_stop": 98.0,
        "tp1": 102.0,
        "tp2": 104.0,
        "tp3": 106.0,
        "volume_contracts": 2.0,
        "contract_size": 1.0,
        "price_tick": 0.01,
        "actual_risk_usdt": 6.0,
        "risk_budget_usdt": 6.0,
        "taker_fee_rate": 0.0,
        "slippage_rate": 0.0,
        "stop_contract": {
            "stop_source": "support_resistance",
            "stop_model": "support_minus_atr_buffer_v1",
            "fallback_used": False,
        },
    }
    rebased = rebase_filled_plan(plan, fill_price=100.5)
    assert rebased["original_stop"] == pytest.approx(98.0)
    assert rebased["fill_rebase_preserved_structural_stop"] is True
    assert rebased["tp1"] > 100.5


def test_crypto_breakout_wider_stop_reprices_r_ladder_long():
    signal = {
        "signal_id": "sig-wide-long",
        "asset_class": "crypto",
        "mode": "swing",
        "symbol": "ETH/USDT",
        "direction": "long",
        "entry_low": 99.0,
        "entry_high": 100.0,
        "entry_trigger": 100.0,
        "suggested_entry": 100.0,
        "stop_loss": 96.0,
        "invalidation": 96.0,
        "tp1": 104.0,
        "tp2": 108.0,
        "tp3": 112.0,
        "risk_per_unit": 4.0,
        "raw_idea_json": json.dumps({"raw_setup": {"invalidation": 96.0}}),
    }
    adjusted, meta = apply_wider_125_if_crypto_breakout(
        signal, entry_mode="BREAKOUT_CONTINUATION",
    )
    assert meta["applied"] is True
    assert adjusted["stop_loss"] == pytest.approx(95.0)
    assert adjusted["invalidation"] == pytest.approx(95.0)
    assert adjusted["tp1"] == pytest.approx(105.0)
    assert adjusted["tp2"] == pytest.approx(110.0)
    assert adjusted["tp3"] == pytest.approx(115.0)
    assert adjusted["risk_per_unit"] == pytest.approx(5.0)
    raw = json.loads(adjusted["raw_idea_json"])
    assert raw["crypto_breakout_stop_profile"]["version"] == CRYPTO_BREAKOUT_STOP_PROFILE
    assert raw["stop_contract"]["stop_price"] == pytest.approx(95.0)


def test_crypto_breakout_wider_stop_reprices_r_ladder_short():
    signal = {
        "signal_id": "sig-wide-short",
        "asset_class": "crypto",
        "mode": "swing",
        "symbol": "ETH/USDT",
        "direction": "short",
        "entry_low": 100.0,
        "entry_high": 101.0,
        "entry_trigger": 100.0,
        "suggested_entry": 100.0,
        "stop_loss": 104.0,
        "invalidation": 104.0,
        "tp1": 96.0,
        "tp2": 92.0,
        "tp3": 88.0,
        "risk_per_unit": 4.0,
        "raw_idea_json": "{}",
    }
    adjusted, meta = apply_wider_125_if_crypto_breakout(
        signal, entry_mode="BREAKOUT_CONTINUATION",
    )
    assert meta["applied"] is True
    assert adjusted["stop_loss"] == pytest.approx(105.0)
    assert adjusted["tp1"] == pytest.approx(95.0)
    assert adjusted["tp2"] == pytest.approx(90.0)
    assert adjusted["tp3"] == pytest.approx(85.0)


def test_wider_stop_does_not_apply_to_stocks_or_pullback():
    base = {
        "signal_id": "sig-no-wide",
        "asset_class": "crypto",
        "mode": "swing",
        "symbol": "ETH/USDT",
        "direction": "long",
        "entry_low": 99.0,
        "entry_high": 100.0,
        "stop_loss": 96.0,
        "invalidation": 96.0,
        "tp1": 104.0,
        "tp2": 108.0,
        "tp3": 112.0,
    }
    pullback, meta = apply_wider_125_if_crypto_breakout(
        base, entry_mode="PULLBACK_LIMIT",
    )
    assert meta["applied"] is False
    assert pullback["stop_loss"] == 96.0
    stocks = dict(base, asset_class="stocks")
    stock_adjusted, stock_meta = apply_wider_125_if_crypto_breakout(
        stocks, entry_mode="BREAKOUT_CONTINUATION",
    )
    assert stock_meta["applied"] is False
    assert stock_adjusted["stop_loss"] == 96.0


def test_tracker_uses_wider_crypto_breakout_stop(monkeypatch):
    from types import SimpleNamespace
    from src.signals import tracker

    now = datetime(2026, 8, 17, 1, 0, tzinfo=timezone.utc)
    frame = pd.DataFrame(
        [
            {
                "timestamp": pd.Timestamp("2026-08-17T00:00:00Z"),
                "open": 99.0,
                "high": 100.0,
                "low": 98.0,
                "close": 100.0,
            },
            {
                "timestamp": pd.Timestamp("2026-08-17T01:00:00Z"),
                "open": 100.0,
                "high": 102.0,
                "low": 95.5,
                "close": 101.0,
            },
        ]
    )
    monkeypatch.setattr(
        tracker,
        "_load_ohlcv_for_signal",
        lambda *_args, **_kwargs: (frame, "binance", "1h"),
    )
    monkeypatch.setattr(
        tracker,
        "_crypto_breakout_entry_mode_for_stop_profile",
        lambda *_args, **_kwargs: "BREAKOUT_CONTINUATION",
    )
    signal = {
        "signal_id": "sig-tracker-wide",
        "asset_class": "crypto",
        "mode": "swing",
        "symbol": "ETH/USDT",
        "direction": "long",
        "status": "waiting_for_entry",
        "created_at": "2026-08-17T00:00:00+00:00",
        "expires_at": "2026-08-24T00:00:00+00:00",
        "entry_low": 99.0,
        "entry_high": 100.0,
        "entry_trigger": 100.0,
        "suggested_entry": 100.0,
        "stop_loss": 96.0,
        "invalidation": 96.0,
        "tp1": 104.0,
        "tp2": 108.0,
        "tp3": 112.0,
        "risk_per_unit": 4.0,
        "raw_idea_json": "{}",
    }
    out = tracker.track_signal(
        signal=signal,
        file_store=SimpleNamespace(load_ohlcv=lambda *_a, **_kw: None),
        project_config=SimpleNamespace(anchor_exchange="binance"),
        tracker_config=SignalTrackingConfig(),
        now=now,
    )
    assert out is not None
    outcome, status = out
    assert status == "triggered"
    assert outcome.stop_hit is False
    overrides = getattr(outcome, "_execution_signal_overrides")
    assert overrides["stop_loss"] == pytest.approx(95.0)
    assert overrides["tp1"] == pytest.approx(105.0)
    assert CRYPTO_BREAKOUT_STOP_PROFILE in str(outcome.notes)
