from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import MagicMock

import pandas as pd

from src.execution.crypto_intraday_level_hold_paper import load_cfg, resolve_entry
from src.signals.config import SignalTrackingConfig
from src.signals.tracker import (
    _EntryObservation,
    _LevelTouches,
    _crypto_intraday_level_hold_plan,
    track_signal,
)

UTC = timezone.utc


def _signal(**updates) -> dict:
    row = {
        "signal_id": "level-hold-1", "asset_class": "crypto", "mode": "intraday",
        "status": "waiting_for_entry", "direction": "long", "created_at": "2026-07-20T00:00:00+00:00",
        "expires_at": "2026-07-20T02:00:00+00:00", "entry_low": 99.0, "entry_high": 100.0,
        "entry_trigger": 100.0, "suggested_entry": 100.0, "invalidation": 98.0,
        "tp1": 103.0, "tp2": 105.0, "tp3": 108.0, "risk_per_unit": 2.0,
    }
    row.update(updates)
    return row


def _candles() -> pd.DataFrame:
    return pd.DataFrame([
        {"timestamp": "2026-07-20T00:00:00Z", "open": 101.0, "high": 101.2,
         "low": 99.0, "close": 100.0, "volume": 100.0},
        {"timestamp": "2026-07-20T00:15:00Z", "open": 99.8, "high": 100.8,
         "low": 99.5, "close": 100.5, "volume": 120.0},
        {"timestamp": "2026-07-20T00:30:00Z", "open": 100.4, "high": 101.0,
         "low": 99.6, "close": 100.0, "volume": 130.0},
    ])


def _v2_cfg(**updates) -> dict:
    cfg = {
        **load_cfg(),
        "activated_at": "2026-07-19T00:00:00+00:00",
        "profile_id": "crypto_intraday_level_hold_v2_paper_v1",
        "confirmation_kind": "level_hold_v2",
        "v2": {
            "max_zone_penetration_fraction": 0.25,
            "min_confirmation_volume_ratio": 0.75,
            "max_retest_bars": 3,
            "market": {"enabled": False},
        },
    }
    cfg.update(updates)
    return cfg


def test_level_hold_requires_a_closed_confirmation_before_retest_can_enter():
    cfg = _v2_cfg()
    out = resolve_entry(
        signal=_signal(), source_entry_mode="PULLBACK_LIMIT", candles=_candles(),
        now=datetime(2026, 7, 20, 0, 20, tzinfo=UTC), timeframe_seconds=15 * 60, cfg=cfg,
    )
    assert out["applied"] is True
    assert out["ready"] is False
    assert out["reason"] == "no_closed_confirmation_bar"


def test_level_hold_returns_only_bars_after_the_confirmed_hold():
    cfg = _v2_cfg()
    out = resolve_entry(
        signal=_signal(), source_entry_mode="PULLBACK_LIMIT", candles=_candles(),
        now=datetime(2026, 7, 20, 0, 46, tzinfo=UTC), timeframe_seconds=15 * 60, cfg=cfg,
    )
    assert out["applied"] is True and out["ready"] is True
    assert out["entry_mode"] == "LEVEL_HOLD_V2"
    assert out["profile_id"] == "crypto_intraday_level_hold_v2_paper_v1"
    assert out["candles"].iloc[0]["timestamp"] == "2026-07-20T00:30:00Z"
    assert out["entry_expires_at"] == "2026-07-20T01:15:00+00:00"
    assert out["profile_gate"]["confirmation_volume_ratio"] == 1.2
    assert load_cfg()["live_enabled"] is False


def test_level_hold_v2_rejects_a_deep_zone_excursion_before_the_reclaim():
    candles = _candles()
    candles.loc[0, "low"] = 98.6
    out = resolve_entry(
        signal=_signal(invalidation=98.0), source_entry_mode="PULLBACK_LIMIT", candles=candles,
        now=datetime(2026, 7, 20, 0, 46, tzinfo=UTC), timeframe_seconds=15 * 60, cfg=_v2_cfg(),
    )
    assert out["applied"] is True and out["ready"] is False
    assert out["reason"] == "v2_zone_penetration_excessive"


def test_level_hold_v2_rejects_an_invalidation_before_entry():
    out = resolve_entry(
        signal=_signal(invalidation=99.0), source_entry_mode="PULLBACK_LIMIT", candles=_candles(),
        now=datetime(2026, 7, 20, 0, 46, tzinfo=UTC), timeframe_seconds=15 * 60, cfg=_v2_cfg(),
    )
    assert out["applied"] is True and out["ready"] is False
    assert out["reason"] == "v2_pre_confirmation_invalidation"


def test_level_hold_v2_rejects_only_confirmed_btc_countertrend(monkeypatch):
    monkeypatch.setattr("src.execution.crypto_quality_overlay.market_context", lambda *_args, **_kw: {
        "status": "ok", "btc_15m_return": -0.30, "btc_1h_return": -0.10,
    })
    out = resolve_entry(
        signal=_signal(), source_entry_mode="PULLBACK_LIMIT", candles=_candles(),
        now=datetime(2026, 7, 20, 0, 46, tzinfo=UTC), timeframe_seconds=15 * 60,
        cfg=_v2_cfg(v2={
            "max_zone_penetration_fraction": 0.25,
            "min_confirmation_volume_ratio": 0.75,
            "max_retest_bars": 3,
            "market": {
                "enabled": True,
                "max_countertrend_btc_15m_return_pct": 0.25,
                "max_countertrend_btc_1h_return_pct": 0.50,
            },
        }),
    )
    assert out["applied"] is True and out["ready"] is False
    assert out["reason"] == "v2_btc_countertrend"


def test_level_hold_v2_does_not_rewrite_a_signal_created_before_activation():
    out = resolve_entry(
        signal=_signal(), source_entry_mode="PULLBACK_LIMIT", candles=_candles(),
        now=datetime(2026, 7, 20, 0, 46, tzinfo=UTC), timeframe_seconds=15 * 60,
    )
    assert out == {"applied": False}


def test_crypto_intraday_level_hold_plan_never_returns_none_for_a_pending_signal():
    """Regression: a copy/paste split once left this function's body stranded
    in a different function, so any pending crypto-intraday signal that
    didn't hit the early-exit guard fell through to an implicit `return None`.
    track_signal() then crashed on `level_hold_plan.get("applied")` — this
    broke `track-signals --all --revalidate-pending` on every scheduler cycle."""
    frame = _candles()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    out = _crypto_intraday_level_hold_plan(
        _signal(), frame, _candles(), now=datetime(2026, 7, 20, 0, 46, tzinfo=UTC), timeframe="15m",
    )
    assert isinstance(out, dict)
    assert "applied" in out


def test_tracker_marks_confirmed_level_hold_entry_with_its_paper_profile(monkeypatch):
    frame = _candles()
    frame = pd.concat([
            pd.DataFrame([{"timestamp": "2026-07-21T23:45:00Z", "open": 100.0, "high": 100.5,
                       "low": 99.5, "close": 100.0, "volume": 100.0}]),
        frame,
    ], ignore_index=True)
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    monkeypatch.setattr("src.signals.tracker._load_ohlcv_for_signal", lambda *_args: (frame, "binance", "15m"))
    monkeypatch.setattr("src.execution.entry_mode_classifier.classify", lambda **_kw: {
        "entry_mode": "PULLBACK_LIMIT", "candles_used": 20,
    })
    monkeypatch.setattr("src.execution.crypto_intraday_level_hold_paper.load_cfg", _v2_cfg)
    monkeypatch.setattr("src.signals.tracker._current_crypto_intraday_entry", lambda **_kw: (
        _LevelTouches(triggered=True, triggered_at="2026-07-22T00:46:00+00:00", entry_price=100.0),
        _EntryObservation(
            "2026-07-22T00:46:00+00:00", 100.0, "point_in_time_current_bar", True,
            "current price is inside the entry zone", "2026-07-22T00:46:00+00:00", "1m",
        ),
        "binance",
    ))
    signal = _signal(signal_id="level-hold-forward", created_at="2026-07-22T00:00:00+00:00",
                     expires_at="2026-07-22T02:00:00+00:00")
    frame["timestamp"] = frame["timestamp"] + pd.Timedelta(days=2)
    outcome, status = track_signal(
        signal=signal, file_store=MagicMock(), project_config=MagicMock(),
        tracker_config=SignalTrackingConfig(), now=datetime(2026, 7, 22, 0, 46, tzinfo=UTC),
    )
    assert status == "triggered"
    assert outcome.entry_triggered is True
    assert outcome.entry_price_used == 100.0
    assert "paper_entry_mode=LEVEL_HOLD_V2" in outcome.notes
    assert "paper_entry_profile=crypto_intraday_level_hold_v2_paper_v1" in outcome.notes
    assert "level_hold_retest_expires_at=2026-07-22T01:15:00+00:00" in outcome.notes
    assert getattr(outcome, "_paper_entry_profile") == "crypto_intraday_level_hold_v2_paper_v1"
    assert getattr(outcome, "_paper_execution_entry_mode") == "LEVEL_HOLD_V2"


def test_tracker_never_reconstructs_a_v2_entry_after_its_retest_window(monkeypatch):
    frame = _candles()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    monkeypatch.setattr("src.signals.tracker._load_ohlcv_for_signal", lambda *_args: (frame, "binance", "15m"))
    monkeypatch.setattr("src.execution.entry_mode_classifier.classify", lambda **_kw: {
        "entry_mode": "PULLBACK_LIMIT", "candles_used": 20,
    })
    monkeypatch.setattr("src.execution.crypto_intraday_level_hold_paper.load_cfg", _v2_cfg)
    monkeypatch.setattr("src.signals.tracker._current_crypto_intraday_entry", lambda **_kw: (
        (_ for _ in ()).throw(AssertionError("V2 expiry must skip a fresh-entry probe"))
    ))
    outcome, status = track_signal(
        signal=_signal(created_at="2026-07-20T00:00:00+00:00", expires_at="2026-07-20T02:00:00+00:00"),
        file_store=MagicMock(), project_config=MagicMock(), tracker_config=SignalTrackingConfig(),
        now=datetime(2026, 7, 20, 1, 30, tzinfo=UTC),
    )
    assert status == "missed_no_entry"
    assert outcome.entry_triggered is False
    assert "level_hold_v2_retest_window_expired" in outcome.notes
