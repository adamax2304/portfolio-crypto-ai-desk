from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import MagicMock

import pandas as pd

from src.execution.crypto_swing_breakout_reclaim_paper import ENTRY_MODE, PROFILE_ID, load_cfg, resolve_entry
from src.signals.config import SignalTrackingConfig
from src.signals.tracker import track_signal


UTC = timezone.utc


def _signal(**updates) -> dict:
    row = {
        "signal_id": "swing-breakout-reclaim-v2",
        "asset_class": "crypto",
        "mode": "swing",
        "status": "waiting_for_entry",
        "direction": "long",
        "symbol": "TEST/USDT",
        "created_at": "2026-09-16T00:00:00+00:00",
        "expires_at": "2026-09-17T00:00:00+00:00",
        "entry_low": None,
        "entry_high": None,
        "entry_trigger": 100.0,
        "suggested_entry": 100.0,
        "invalidation": 96.0,
        "stop_loss": 96.0,
        "tp1": 105.2,
        "tp2": 109.2,
        "tp3": 114.4,
        "risk_per_unit": 4.0,
        "raw_idea_json": "{}",
    }
    row.update(updates)
    return row


def _frame(rows: list[dict]) -> pd.DataFrame:
    frame = pd.DataFrame(rows)
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    return frame


def _reclaim_frame() -> pd.DataFrame:
    return _frame([
        {"timestamp": "2026-09-16T00:00:00Z", "open": 98.5, "high": 99.8,
         "low": 98.0, "close": 99.5, "volume": 100.0},
        {"timestamp": "2026-09-16T01:00:00Z", "open": 100.1, "high": 101.2,
         "low": 99.95, "close": 100.7, "volume": 130.0},
        {"timestamp": "2026-09-16T02:00:00Z", "open": 100.5, "high": 100.8,
         "low": 99.9, "close": 100.2, "volume": 120.0},
        {"timestamp": "2026-09-16T03:00:00Z", "open": 100.2, "high": 101.1,
         "low": 100.1, "close": 100.9, "volume": 110.0},
    ])


def _cfg(**updates) -> dict:
    cfg = load_cfg()
    cfg["activated_at"] = "2026-09-15T00:00:00+00:00"
    cfg["block_confirmed_btc_countertrend"] = False
    for key, value in updates.items():
        cfg[key] = value
    return cfg


def test_breakout_reclaim_waits_for_closed_hold_then_retest_zone():
    out = resolve_entry(
        signal=_signal(),
        source_entry_mode="BREAKOUT_CONTINUATION",
        candles=_reclaim_frame(),
        now=datetime(2026, 9, 16, 4, 0, tzinfo=UTC),
        timeframe_seconds=3600,
        cfg=_cfg(),
    )

    assert out["applied"] is True
    assert out["ready"] is True
    assert out["entry_mode"] == ENTRY_MODE
    assert out["profile_id"] == PROFILE_ID
    assert out["confirmation_at"] == "2026-09-16T01:00:00+00:00"
    assert out["entry_low"] < 100.0 < out["entry_high"]
    assert out["candles"].iloc[0]["timestamp"] == pd.Timestamp("2026-09-16T02:00:00Z")
    assert out["profile_gate"]["entry_after_confirmation"] is True


def test_breakout_reclaim_rejects_failed_first_touch():
    frame = _frame([
        {"timestamp": "2026-09-16T00:00:00Z", "open": 99.0, "high": 101.2,
         "low": 98.7, "close": 99.3, "volume": 100.0},
        {"timestamp": "2026-09-16T01:00:00Z", "open": 99.2, "high": 99.8,
         "low": 98.9, "close": 99.5, "volume": 90.0},
    ])

    out = resolve_entry(
        signal=_signal(),
        source_entry_mode="BREAKOUT_CONTINUATION",
        candles=frame,
        now=datetime(2026, 9, 16, 3, 0, tzinfo=UTC),
        timeframe_seconds=3600,
        cfg=_cfg(),
    )

    assert out["applied"] is True
    assert out["ready"] is False
    assert out["reason"] == "breakout_reclaim_first_touch_rejected"


def test_tracker_records_breakout_reclaim_profile_instead_of_raw_breakout(monkeypatch):
    frame = _frame([
        {"timestamp": "2026-09-15T23:00:00Z", "open": 98.0, "high": 99.0,
         "low": 97.5, "close": 98.5, "volume": 100.0},
        *_reclaim_frame().to_dict("records"),
    ])
    monkeypatch.setattr("src.signals.tracker._load_ohlcv_for_signal", lambda *_args: (frame, "binance", "1h"))
    monkeypatch.setattr("src.execution.entry_mode_classifier.classify", lambda **_kw: {
        "entry_mode": "BREAKOUT_CONTINUATION",
        "suggested_entry": 100.0,
        "candles_used": 20,
    })
    monkeypatch.setattr("src.execution.crypto_swing_breakout_reclaim_paper.load_cfg", _cfg)
    monkeypatch.setattr(
        "src.execution.crypto_swing_breakout_reclaim_paper._btc_countertrend_block",
        lambda *_args, **_kwargs: (False, {}),
    )

    outcome, status = track_signal(
        signal=_signal(),
        file_store=MagicMock(),
        project_config=MagicMock(anchor_exchange="binance"),
        tracker_config=SignalTrackingConfig(),
        now=datetime(2026, 9, 16, 4, 0, tzinfo=UTC),
    )

    assert status == "triggered"
    assert outcome.entry_triggered is True
    assert "paper_entry_mode=BREAKOUT_RECLAIM_V2" in outcome.notes
    assert "paper_entry_profile=crypto_swing_breakout_reclaim_paper_v2" in outcome.notes
    assert getattr(outcome, "_paper_entry_profile") == PROFILE_ID
    assert getattr(outcome, "_paper_execution_entry_mode") == ENTRY_MODE
    assert getattr(outcome, "_paper_source_entry_mode") == "BREAKOUT_CONTINUATION"
