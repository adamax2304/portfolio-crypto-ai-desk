from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import MagicMock

import pandas as pd

from src.execution.crypto_swing_pullback_paper import (
    CONFIRMED_RETEST_MODE,
    CONFIRMED_RETEST_PROFILE,
    FIB_IMPULSE_MODE,
    FIB_IMPULSE_PROFILE,
    load_cfg,
    resolve_entry,
)
from src.signals.config import SignalTrackingConfig
from src.signals.tracker import track_signal


UTC = timezone.utc


def _signal(**updates) -> dict:
    row = {
        "signal_id": "swing-pullback-v2",
        "asset_class": "crypto",
        "mode": "swing",
        "status": "waiting_for_entry",
        "direction": "long",
        "symbol": "TEST/USDT",
        "created_at": "2026-09-02T00:00:00+00:00",
        "expires_at": "2026-09-03T00:00:00+00:00",
        "entry_low": 97.0,
        "entry_high": 99.0,
        "entry_trigger": None,
        "suggested_entry": 99.0,
        "invalidation": 94.0,
        "stop_loss": 94.0,
        "tp1": 105.5,
        "tp2": 110.5,
        "tp3": 117.0,
        "risk_per_unit": 5.0,
        "raw_idea_json": "{}",
    }
    row.update(updates)
    return row


def _dt_frame(rows: list[dict]) -> pd.DataFrame:
    frame = pd.DataFrame(rows)
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    return frame


def _confirmed_retest_candles() -> pd.DataFrame:
    return _dt_frame([
        {"timestamp": "2026-09-02T01:00:00Z", "open": 105.0, "high": 106.0,
         "low": 100.0, "close": 104.0, "volume": 100.0},
        {"timestamp": "2026-09-02T02:00:00Z", "open": 100.0, "high": 101.0,
         "low": 98.5, "close": 99.5, "volume": 90.0},
        {"timestamp": "2026-09-02T03:00:00Z", "open": 100.2, "high": 100.8,
         "low": 98.8, "close": 100.4, "volume": 95.0},
        {"timestamp": "2026-09-02T04:00:00Z", "open": 100.4, "high": 101.2,
         "low": 99.6, "close": 100.8, "volume": 105.0},
    ])


def _cfg(**updates) -> dict:
    cfg = load_cfg()
    cfg["activated_at"] = "2026-09-01T00:00:00+00:00"
    cfg["profiles"]["fib_impulse_retest"]["enabled"] = False
    for key, value in updates.items():
        cfg[key] = value
    return cfg


def test_confirmed_retest_waits_for_defended_zone_then_retest():
    out = resolve_entry(
        signal=_signal(),
        source_entry_mode="PULLBACK_LIMIT",
        candles=_confirmed_retest_candles(),
        all_candles=_confirmed_retest_candles(),
        now=datetime(2026, 9, 2, 6, 0, tzinfo=UTC),
        timeframe_seconds=3600,
        cfg=_cfg(),
    )
    assert out["applied"] is True
    assert out["ready"] is True
    assert out["entry_mode"] == CONFIRMED_RETEST_MODE
    assert out["profile_id"] == CONFIRMED_RETEST_PROFILE
    assert out["confirmation_at"] == "2026-09-02T02:00:00+00:00"
    assert out["candles"].iloc[0]["timestamp"] == pd.Timestamp("2026-09-02T03:00:00Z")
    assert out["signal_updates"]["entry_low"] == 97.0
    assert out["signal_updates"]["entry_high"] == 99.0
    assert out["signal_updates"]["stop_loss"] == 94.0
    assert out["signal_updates"]["tp1"] == 105.5
    assert out["profile_gate"]["entry_after_confirmation"] is True


def test_fib_impulse_profile_takes_priority_when_impulse_is_present():
    frame = _dt_frame([
        {"timestamp": "2026-09-02T00:00:00Z", "open": 100.0, "high": 101.0,
         "low": 99.5, "close": 100.0, "volume": 100.0},
        {"timestamp": "2026-09-02T01:00:00Z", "open": 100.0, "high": 105.0,
         "low": 99.8, "close": 104.0, "volume": 220.0},
        {"timestamp": "2026-09-02T02:00:00Z", "open": 104.0, "high": 120.0,
         "low": 103.0, "close": 118.0, "volume": 240.0},
        {"timestamp": "2026-09-02T04:00:00Z", "open": 117.0, "high": 117.5,
         "low": 111.0, "close": 112.0, "volume": 120.0},
        {"timestamp": "2026-09-02T05:00:00Z", "open": 111.0, "high": 112.0,
         "low": 108.0, "close": 110.2, "volume": 160.0},
        {"timestamp": "2026-09-02T06:00:00Z", "open": 111.0, "high": 112.2,
         "low": 109.0, "close": 111.8, "volume": 150.0},
    ])
    candles = frame.loc[frame["timestamp"] >= pd.Timestamp("2026-09-02T03:00:00Z")].reset_index(drop=True)
    cfg = load_cfg()
    cfg["activated_at"] = "2026-09-01T00:00:00+00:00"
    out = resolve_entry(
        signal=_signal(
            created_at="2026-09-02T03:00:00+00:00",
            suggested_entry=109.75,
            entry_low=107.331,
            entry_high=109.75,
            invalidation=99.0,
            stop_loss=99.0,
        ),
        source_entry_mode="PULLBACK_LIMIT",
        candles=candles,
        all_candles=frame,
        now=datetime(2026, 9, 2, 8, 0, tzinfo=UTC),
        timeframe_seconds=3600,
        cfg=cfg,
    )
    assert out["applied"] is True
    assert out["ready"] is True
    assert out["entry_mode"] == FIB_IMPULSE_MODE
    assert out["profile_id"] == FIB_IMPULSE_PROFILE
    assert out["profile_gate"]["fib_entry_shallow"] == 0.5
    assert out["profile_gate"]["fib_entry_deep"] == 0.618
    assert out["signal_updates"]["entry_low"] < out["signal_updates"]["entry_high"]
    assert out["candles"].iloc[0]["timestamp"] == pd.Timestamp("2026-09-02T06:00:00Z")


def test_tracker_records_new_swing_pullback_profile_instead_of_old_blind_touch(monkeypatch):
    frame = _confirmed_retest_candles()
    pre = _dt_frame([
        {"timestamp": "2026-09-01T23:00:00Z", "open": 104.0, "high": 105.0,
         "low": 103.0, "close": 104.5, "volume": 100.0},
        {"timestamp": "2026-09-02T00:00:00Z", "open": 104.5, "high": 105.2,
         "low": 103.5, "close": 104.0, "volume": 100.0},
    ])
    frame = pd.concat([pre, frame], ignore_index=True)
    monkeypatch.setattr("src.signals.tracker._load_ohlcv_for_signal", lambda *_args: (frame, "binance", "1h"))
    monkeypatch.setattr("src.execution.entry_mode_classifier.classify", lambda **_kw: {
        "entry_mode": "PULLBACK_LIMIT", "candles_used": 20,
    })
    monkeypatch.setattr("src.execution.crypto_swing_pullback_paper.load_cfg", _cfg)
    outcome, status = track_signal(
        signal=_signal(),
        file_store=MagicMock(),
        project_config=MagicMock(),
        tracker_config=SignalTrackingConfig(),
        now=datetime(2026, 9, 2, 6, 0, tzinfo=UTC),
    )
    assert status == "triggered"
    assert outcome.entry_triggered is True
    assert outcome.entry_price_used == 99.0
    assert "paper_entry_mode=PULLBACK_CONFIRMED_RETEST" in outcome.notes
    assert "paper_entry_profile=crypto_swing_pullback_confirmed_retest_paper_v1" in outcome.notes
    assert getattr(outcome, "_paper_entry_profile") == CONFIRMED_RETEST_PROFILE
    assert getattr(outcome, "_paper_execution_entry_mode") == CONFIRMED_RETEST_MODE
    assert getattr(outcome, "_paper_source_entry_mode") == "PULLBACK_LIMIT"
