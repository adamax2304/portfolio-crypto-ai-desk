from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock

import pandas as pd

from src.signals.tracker import (
    _EntryObservation,
    _LevelTouches,
    _entry_observation,
    _load_ohlcv_for_signal,
    _load_stocks_ohlcv_for_signal,
    track_signal,
    track_active_signals,
)
from src.signals.config import SignalTrackingConfig


NOW = datetime(2026, 7, 17, 10, 45, tzinfo=timezone.utc)


def _frame(ts: str, close: float = 100.0) -> pd.DataFrame:
    return pd.DataFrame([{
        "timestamp": pd.Timestamp(ts), "open": close, "high": close + 1,
        "low": close - 1, "close": close, "volume": 10,
    }])


def _signal(**updates):
    row = {
        "direction": "long", "entry_low": 99.0, "entry_high": 101.0,
        "entry_trigger": 101.0, "invalidation": 95.0,
    }
    row.update(updates)
    return row


def test_current_crypto_hour_bar_uses_detection_time_not_bar_open():
    touches = _LevelTouches(triggered=True, triggered_at="2026-07-17T10:00:00+00:00",
                            entry_price=101.0)
    result = _entry_observation(
        signal=_signal(), promoted_entry=None, touches=touches,
        candles=_frame("2026-07-17T10:00:00Z"), timeframe="1h",
        now=NOW, asset_class="crypto")
    assert isinstance(result, _EntryObservation)
    assert result.currently_executable is True
    assert result.time_basis == "point_in_time_current_bar"
    assert result.observed_at == "2026-07-17T10:45:00+00:00"
    assert result.bar_open_at == "2026-07-17T10:00:00+00:00"


def test_historical_touch_cannot_authorize_current_entry():
    touches = _LevelTouches(triggered=True, triggered_at="2026-07-17T09:00:00+00:00",
                            entry_price=101.0)
    result = _entry_observation(
        signal=_signal(), promoted_entry=None, touches=touches,
        candles=_frame("2026-07-17T10:00:00Z", close=104.0), timeframe="1h",
        now=NOW, asset_class="crypto")
    assert result.currently_executable is False
    assert result.observed_at is None
    assert result.time_basis == "historical_not_currently_executable"


def test_stock_yfinance_observation_is_labeled_delayed_not_live_grade():
    touches = _LevelTouches(triggered=True, triggered_at="2026-07-17T10:40:00+00:00",
                            entry_price=100.0)
    result = _entry_observation(
        signal=_signal(), promoted_entry=None, touches=touches,
        candles=_frame("2026-07-17T10:40:00Z"), timeframe="1m",
        now=NOW, asset_class="stocks")
    assert result.currently_executable is True
    assert result.time_basis == "provider_delayed_current_bar"
    assert result.observed_at == "2026-07-17T10:41:00+00:00"


def test_fresh_fallback_exchange_beats_stale_focus_cache():
    class Store:
        frames = {
            ("mexc", "5m"): _frame("2026-07-17T09:00:00Z"),
            ("binance", "5m"): _frame("2026-07-17T10:40:00Z"),
        }

        def load_ohlcv(self, exchange, symbol, timeframe):
            return self.frames.get((exchange, timeframe))

    class Config:
        anchor_exchange = "binance"

    _, exchange, timeframe = _load_ohlcv_for_signal(
        Store(), Config(), "ABC/USDT", "scalp", "mexc")
    assert (exchange, timeframe) == ("binance", "5m")


def test_stale_one_minute_stock_cache_does_not_mask_fresh_15m():
    class Store:
        def load_stocks_ohlcv(self, symbol, timeframe):
            if timeframe == "1m":
                return _frame("2026-07-16T19:59:00Z")
            if timeframe == "15m":
                return _frame("2026-07-17T10:30:00Z")
            return None

    _, exchange, timeframe = _load_stocks_ohlcv_for_signal(Store(), "AAPL", "intraday")
    assert (exchange, timeframe) == ("stocks", "15m")


def _intraday_signal(**updates):
    signal = {
        "signal_id": "fresh-entry", "asset_class": "crypto", "mode": "intraday",
        "direction": "long", "created_at": "2026-07-17T10:40:00+00:00",
        "expires_at": "2026-07-17T12:00:00+00:00", "entry_low": 99.0,
        "entry_high": 101.0, "entry_trigger": 101.0, "suggested_entry": 100.0,
        "invalidation": 98.0, "tp1": 103.0, "tp2": 105.0, "tp3": 108.0,
        "risk_per_unit": 2.0, "status": "waiting_for_entry",
    }
    signal.update(updates)
    return signal


def test_crypto_intraday_enters_from_fresh_1m_not_15m_history(monkeypatch):
    structural = _frame("2026-07-17T10:30:00Z", close=104.0)
    fresh = _frame("2026-07-17T10:45:00Z", close=100.0)
    monkeypatch.setattr(
        "src.signals.tracker._load_ohlcv_for_signal",
        lambda *_args: (structural, "binance", "15m"),
    )
    monkeypatch.setattr(
        "src.signals.tracker._load_crypto_execution_ohlcv",
        lambda *_args: (fresh, "binance"),
    )
    outcome, status = track_signal(
        signal=_intraday_signal(), file_store=MagicMock(), project_config=MagicMock(),
        tracker_config=SignalTrackingConfig(), now=NOW,
    )
    assert status == "triggered"
    assert outcome.entry_triggered_at == "2026-07-17T10:45:00+00:00"
    assert outcome.entry_price_used == 100.0
    assert getattr(outcome, "_entry_currently_executable") is True
    assert "paper_execution_source=fresh_1m_point_in_time_entry" in outcome.notes


def test_forward_intraday_breakout_is_tagged_with_live_allowlisted_paper_profile(monkeypatch):
    now = datetime(2026, 8, 5, 14, 20, tzinfo=timezone.utc)
    structural = _frame("2026-08-05T14:15:00Z", close=104.0)
    fresh = _frame("2026-08-05T14:20:00Z", close=100.0)
    monkeypatch.setattr(
        "src.signals.tracker._load_ohlcv_for_signal",
        lambda *_args: (structural, "binance", "15m"),
    )
    monkeypatch.setattr(
        "src.signals.tracker._load_crypto_execution_ohlcv",
        lambda *_args: (fresh, "binance"),
    )
    monkeypatch.setattr("src.execution.entry_mode_classifier.classify", lambda **_kw: {
        "entry_mode": "BREAKOUT_CONTINUATION", "candles_used": 20,
    })
    outcome, status = track_signal(
        signal=_intraday_signal(
            signal_id="forward-breakout", created_at="2026-08-05T14:11:00+00:00",
            expires_at="2026-08-05T15:30:00+00:00",
        ),
        file_store=MagicMock(), project_config=MagicMock(),
        tracker_config=SignalTrackingConfig(), now=now,
    )
    assert status == "triggered"
    assert getattr(outcome, "_paper_entry_profile") == "crypto_intraday_breakout_paper_v1"
    assert getattr(outcome, "_paper_execution_entry_mode") == "BREAKOUT_CONTINUATION"
    assert getattr(outcome, "_paper_source_entry_mode") == "BREAKOUT_CONTINUATION"
    assert "paper_entry_profile=crypto_intraday_breakout_paper_v1" in outcome.notes


def test_forward_intraday_pullback_is_tagged_with_live_allowlisted_paper_profile(monkeypatch):
    now = datetime(2026, 9, 18, 10, 45, tzinfo=timezone.utc)
    monkeypatch.setattr(
        "src.execution.crypto_intraday_pullback_paper.load_cfg",
        lambda: {
            "enabled": True,
            "live_enabled": True,
            "profile_id": "crypto_intraday_pullback_paper_v1",
            "activated_at": "2026-09-18T00:00:00+00:00",
            "asset_class": "crypto",
            "mode": "intraday",
            "source_entry_mode": "PULLBACK_LIMIT",
        },
    )
    structural = _frame("2026-09-18T10:30:00Z", close=100.0)
    fresh = _frame("2026-09-18T10:45:00Z", close=100.0)
    monkeypatch.setattr(
        "src.signals.tracker._load_ohlcv_for_signal",
        lambda *_args: (structural, "binance", "15m"),
    )
    monkeypatch.setattr(
        "src.signals.tracker._load_crypto_execution_ohlcv",
        lambda *_args: (fresh, "binance"),
    )
    monkeypatch.setattr("src.execution.entry_mode_classifier.classify", lambda **_kw: {
        "entry_mode": "PULLBACK_LIMIT", "candles_used": 20,
    })
    monkeypatch.setattr(
        "src.signals.tracker._crypto_intraday_level_hold_plan",
        lambda *_args, **_kw: {"applied": False},
    )
    outcome, status = track_signal(
        signal=_intraday_signal(
            signal_id="forward-pullback", created_at="2026-09-18T10:40:00+00:00",
            expires_at="2026-09-18T12:00:00+00:00",
        ),
        file_store=MagicMock(), project_config=MagicMock(),
        tracker_config=SignalTrackingConfig(), now=now,
    )
    assert status == "triggered"
    assert getattr(outcome, "_paper_entry_profile") == "crypto_intraday_pullback_paper_v1"
    assert getattr(outcome, "_paper_execution_entry_mode") == "PULLBACK_LIMIT"
    assert getattr(outcome, "_paper_source_entry_mode") == "PULLBACK_LIMIT"
    assert "paper_entry_profile=crypto_intraday_pullback_paper_v1" in outcome.notes


def test_crypto_intraday_open_trade_does_not_replay_pre_entry_history(monkeypatch):
    structural = _frame("2026-07-17T10:30:00Z", close=104.0)
    execution = pd.DataFrame([
        {"timestamp": "2026-07-17T10:44:00Z", "open": 100.0, "high": 101.0,
         "low": 90.0, "close": 100.0, "volume": 10},  # before actual entry: ignored
        {"timestamp": "2026-07-17T10:46:00Z", "open": 100.0, "high": 101.0,
         "low": 97.0, "close": 98.0, "volume": 10},  # after actual entry: stop
    ])
    monkeypatch.setattr(
        "src.signals.tracker._load_ohlcv_for_signal",
        lambda *_args: (structural, "binance", "15m"),
    )
    monkeypatch.setattr(
        "src.signals.tracker._load_crypto_execution_ohlcv",
        lambda *_args: (execution, "binance"),
    )
    outcome, status = track_signal(
        signal=_intraday_signal(status="triggered"), file_store=MagicMock(), project_config=MagicMock(),
        tracker_config=SignalTrackingConfig(), now=datetime(2026, 7, 17, 10, 47, tzinfo=timezone.utc),
        active_paper_entry={"entry_at": "2026-07-17T10:45:00+00:00", "entry_price_used": 100.0},
    )
    assert status == "stopped"
    assert outcome.entry_triggered_at == "2026-07-17T10:45:00+00:00"
    assert outcome.stop_hit_at == "2026-07-17T10:46:00+00:00"


def test_tracker_persists_and_reuses_a_point_in_time_intraday_entry(tmp_path, monkeypatch):
    from src.storage.sqlite import SQLiteStore

    store = SQLiteStore(Path(tmp_path) / "tracker.sqlite")
    store.init_db()
    with store.connect() as conn:
        conn.execute(
            "INSERT INTO proposed_signals(signal_id,created_at,updated_at,symbol,direction,mode,"
            "tier,score,asset_class,status,entry_low,entry_high,entry_trigger,suggested_entry,"
            "invalidation,tp1,tp2,tp3,risk_per_unit,expires_at) "
            "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            ("point-in-time", "2026-07-17T10:40:00+00:00", "2026-07-17T10:40:00+00:00",
             "ETH/USDT", "long", "intraday", "A", 80.0, "crypto", "waiting_for_entry",
             99.0, 101.0, 101.0, 100.0, 98.0, 103.0, 105.0, 108.0, 2.0,
             "2026-07-17T12:00:00+00:00"),
        )
        conn.commit()

    structural = _frame("2026-07-17T10:30:00Z", close=104.0)
    first_execution = _frame("2026-07-17T10:45:00Z", close=100.0)
    later_execution = pd.DataFrame([
        {"timestamp": pd.Timestamp("2026-07-17T10:44:00Z"), "open": 100.0, "high": 101.0,
         "low": 90.0, "close": 100.0, "volume": 10},
        {"timestamp": pd.Timestamp("2026-07-17T10:46:00Z"), "open": 100.0, "high": 101.0,
         "low": 97.0, "close": 98.0, "volume": 10},
    ])
    monkeypatch.setattr("src.signals.tracker._load_ohlcv_for_signal",
                        lambda *_args: (structural, "binance", "15m"))
    execution_frames = iter((first_execution, later_execution))
    monkeypatch.setattr("src.signals.tracker._load_crypto_execution_ohlcv",
                        lambda *_args: (next(execution_frames), "binance"))
    clocks = iter((NOW, datetime(2026, 7, 17, 10, 47, tzinfo=timezone.utc)))
    monkeypatch.setattr("src.signals.tracker._now", lambda: next(clocks))

    class Config:
        root = tmp_path
        anchor_exchange = "binance"

    first = track_active_signals(
        store=store, file_store=MagicMock(), project_config=Config(),
        tracker_config=SignalTrackingConfig(), signal_ids=["point-in-time"],
    )
    assert first.checked == 1
    with store.connect() as conn:
        entry = conn.execute(
            "SELECT lifecycle_state,entry_at,entry_time_basis,current_price_revalidated "
            "FROM paper_execution_outcomes WHERE signal_id='point-in-time'"
        ).fetchone()
    assert tuple(entry) == ("OPEN", "2026-07-17T10:45:00+00:00", "point_in_time_current_bar", 1)

    second = track_active_signals(
        store=store, file_store=MagicMock(), project_config=Config(),
        tracker_config=SignalTrackingConfig(), signal_ids=["point-in-time"],
    )
    assert second.stopped == 1
    with store.connect() as conn:
        outcome = conn.execute(
            "SELECT status,entry_triggered_at,stop_hit_at FROM signal_outcomes "
            "WHERE signal_id='point-in-time' ORDER BY id DESC LIMIT 1"
        ).fetchone()
    assert tuple(outcome) == ("stopped", "2026-07-17T10:45:00+00:00", "2026-07-17T10:46:00+00:00")
