"""Tests for stocks signal tracking (audit fix #1).

Verifies that:
  - FileStore.load_stocks_ohlcv normalizes the yfinance-shaped CSV.
  - track_signal routes to data/raw/stocks/ when signal.asset_class == 'stocks'.
  - A stocks signal that registers entry / TP1 produces the correct outcome.
  - Crypto signals still resolve via the existing data/raw/ohlcv/ path.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import pytest

from src.config import ProjectConfig
from src.signals.config import SignalTrackingConfig
from src.signals.tracker import (
    _effective_expiry,
    _evaluate_signal_walk,
    _load_ohlcv_for_signal,
    _load_stocks_ohlcv_for_signal,
    _promoted_entry_mode,
    track_signal,
)
from src.storage.file_store import FileStore
from src.stocks.market_calendar import us_cash_session_close


def _make_config(tmp_path: Path) -> ProjectConfig:
    """Build a ProjectConfig rooted at a tmpdir so tests don't touch live data."""
    settings = {
        "data": {
            "raw_dir": "data/raw",
            "processed_dir": "data/processed",
            "reports_dir": "data/reports",
            "db_path": "db/test.sqlite",
        }
    }
    return ProjectConfig(
        root=tmp_path,
        settings=settings,
        watchlist={"exchange": "binance"},
        sources={},
        scoring={},
        universe={"enabled_exchanges": ["binance"], "anchor_exchange": "binance"},
        exchanges={},
    )


def _write_yfinance_style_csv(
    path: Path,
    *,
    start: datetime,
    bars: int,
    base_price: float = 100.0,
    price_step: float = 1.0,
) -> None:
    """Write a CSV that looks like what yfinance produces — a 'Date' (or
    'Datetime') index column, capitalized OHLCV columns. This is the shape
    StockOHLCVCollector caches."""
    path.parent.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []
    for i in range(bars):
        ts = start + timedelta(hours=i)
        open_ = base_price + i * price_step
        high = open_ + 0.6
        low = open_ - 0.4
        close = open_ + price_step * 0.5
        rows.append(
            {
                "Date": ts.isoformat(),
                "Open": open_,
                "High": high,
                "Low": low,
                "Close": close,
                "Volume": 1000 + i * 10,
            }
        )
    frame = pd.DataFrame(rows).set_index("Date")
    frame.to_csv(path)


def test_load_stocks_ohlcv_normalizes_shape(tmp_path):
    config = _make_config(tmp_path)
    fs = FileStore(config)
    start = datetime(2026, 5, 25, 13, 30, tzinfo=timezone.utc)
    csv_path = fs.stocks_ohlcv_path("NVDA", "1h")
    _write_yfinance_style_csv(csv_path, start=start, bars=10)

    frame = fs.load_stocks_ohlcv("NVDA", "1h")
    assert frame is not None
    assert not frame.empty
    # tracker requires a lowercase 'timestamp' column with UTC datetimes.
    assert "timestamp" in frame.columns
    assert {"open", "high", "low", "close", "volume"}.issubset(set(frame.columns))
    assert pd.api.types.is_datetime64_any_dtype(frame["timestamp"])
    assert frame["timestamp"].iloc[0] == pd.Timestamp(start)


def test_load_stocks_ohlcv_missing_returns_none(tmp_path):
    config = _make_config(tmp_path)
    fs = FileStore(config)
    assert fs.load_stocks_ohlcv("ZZZ_DOES_NOT_EXIST", "1h") is None


def test_load_stocks_for_signal_tries_multiple_timeframes(tmp_path):
    config = _make_config(tmp_path)
    fs = FileStore(config)
    start = datetime(2026, 5, 25, 13, 30, tzinfo=timezone.utc)
    _write_yfinance_style_csv(fs.stocks_ohlcv_path("AAPL", "1d"), start=start, bars=5)

    frame, exch, tf = _load_stocks_ohlcv_for_signal(fs, "AAPL", "swing")
    assert frame is not None
    assert exch == "stocks"
    assert tf in ("1h", "1d")  # picks first available


def test_track_signal_routes_stocks_path(tmp_path):
    config = _make_config(tmp_path)
    fs = FileStore(config)
    # Long stocks signal at entry 100, stop 95, TP1 110.
    start = datetime(2026, 5, 25, 13, 30, tzinfo=timezone.utc)
    # Write a rising series so the long entry triggers and TP1 hits.
    _write_yfinance_style_csv(
        fs.stocks_ohlcv_path("NVDA", "1h"),
        start=start,
        bars=30,
        base_price=99.0,
        price_step=0.6,
    )

    created_at = (start - timedelta(hours=1)).isoformat()
    signal = {
        "signal_id": "test_stocks_001",
        "symbol": "NVDA",
        "mode": "swing",  # uses 1h preference
        "direction": "long",
        "asset_class": "stocks",
        "exchange_focus": "US",
        "created_at": created_at,
        "expires_at": (start + timedelta(days=7)).isoformat(),
        "entry_low": 99.0,
        "entry_high": 100.5,
        "entry_trigger": 100.0,
        "suggested_entry": 100.0,
        "invalidation": 95.0,
        "tp1": 110.0,
        "tp2": 115.0,
        "tp3": 120.0,
        "risk_per_unit": 5.0,
        "status": "waiting_for_entry",
    }
    tracker_cfg = SignalTrackingConfig()
    result = track_signal(
        signal=signal,
        file_store=fs,
        project_config=config,
        tracker_config=tracker_cfg,
        now=start + timedelta(hours=29),
    )
    assert result is not None, "stocks signal should resolve via data/raw/stocks/"
    outcome, status = result
    assert outcome.entry_triggered is True
    assert outcome.tp1_hit is True
    assert "src=stocks/" in (outcome.notes or "")


def test_track_signal_crypto_path_unchanged(tmp_path):
    """Sanity: crypto signals still go through the per-exchange tree and
    are unaffected by the stocks routing."""
    config = _make_config(tmp_path)
    fs = FileStore(config)

    # Drop a crypto-style CSV (BTC/USDT @ 1h via the existing helper).
    start = datetime(2026, 5, 25, 13, 30, tzinfo=timezone.utc)
    crypto_path = fs.ohlcv_path("binance", "BTC/USDT", "1h")
    crypto_path.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for i in range(20):
        ts = start + timedelta(hours=i)
        rows.append(
            {
                "timestamp": ts.isoformat(),
                "open": 100.0,
                "high": 101.0,
                "low": 99.5,
                "close": 100.5,
                "volume": 50.0,
            }
        )
    pd.DataFrame(rows).to_csv(crypto_path, index=False)

    frame, exch, tf = _load_ohlcv_for_signal(
        fs, config, "BTC/USDT", "swing", exchange_focus="binance"
    )
    assert frame is not None
    assert exch == "binance"
    assert tf in ("1h", "4h", "1d")


def test_track_signal_no_cache_returns_none(tmp_path):
    """A stocks signal with no cached CSV returns None (skipped_no_ohlcv)."""
    config = _make_config(tmp_path)
    fs = FileStore(config)
    signal = {
        "signal_id": "test_stocks_missing",
        "symbol": "MISSING",
        "mode": "swing",
        "direction": "long",
        "asset_class": "stocks",
        "exchange_focus": "US",
        "created_at": "2026-05-25T00:00:00+00:00",
        "expires_at": "2026-06-01T00:00:00+00:00",
        "entry_low": 100, "entry_high": 101, "entry_trigger": 100.5,
        "suggested_entry": 100.5, "invalidation": 95.0,
        "tp1": 110.0, "tp2": 115.0, "tp3": 120.0,
        "risk_per_unit": 5.0,
        "status": "waiting_for_entry",
    }
    result = track_signal(
        signal=signal,
        file_store=fs,
        project_config=config,
        tracker_config=SignalTrackingConfig(),
    )
    assert result is None


def test_stock_intraday_disabled_entry_mode_cannot_fall_back_to_legacy_geometry(monkeypatch):
    """A disabled taker mode must become no-entry, never a legacy pullback."""
    import src.execution.entry_mode_classifier as classifier
    frame = pd.DataFrame({"timestamp": [pd.Timestamp("2026-07-08T14:00:00Z")],
                          "open": [100.0], "high": [101.0], "low": [99.0], "close": [100.5]})
    monkeypatch.setattr(classifier, "classify", lambda **_kw: {
        "entry_mode": "MOMENTUM_TAKER_NOW", "candles_used": 20,
    })
    out = _promoted_entry_mode(
        {"asset_class": "stocks", "mode": "intraday", "direction": "long",
         "created_at": "2026-07-08T14:00:00+00:00"}, frame,
    )
    assert out and out["blocked"] is True
    assert out["entry_mode"] == "MOMENTUM_TAKER_NOW"
    assert out["reason"] == "stocks_intraday_entry_mode_disabled_by_policy"


def test_stock_short_pullback_requires_bearish_rejection_not_just_zone_touch():
    candles = pd.DataFrame([
        # Price wicks through the short zone but closes green: this is an
        # ongoing squeeze/bounce, not a confirmed rejection.
        {"timestamp": "2026-07-29T18:37:00+00:00", "open": 193.41,
         "high": 193.84, "low": 193.35, "close": 193.76},
    ])
    no_entry = _evaluate_signal_walk(
        direction="short", entry_low=193.794, entry_high=195.002,
        entry_trigger=None, invalidation=196.211, tp1=190.16, tp2=188.0, tp3=185.0,
        candles=candles, same_candle_conservative=True,
        require_short_pullback_rejection=True,
    )
    assert no_entry.triggered is False

    candles.loc[0, "open"] = 194.10
    candles.loc[0, "close"] = 193.70
    confirmed = _evaluate_signal_walk(
        direction="short", entry_low=193.794, entry_high=195.002,
        entry_trigger=None, invalidation=196.211, tp1=190.16, tp2=188.0, tp3=185.0,
        candles=candles, same_candle_conservative=True,
        require_short_pullback_rejection=True,
    )
    assert confirmed.triggered is True


def test_stock_intraday_expires_at_same_day_close_not_next_session(tmp_path, monkeypatch):
    config = _make_config(tmp_path)
    fs = FileStore(config)
    created = datetime(2026, 7, 8, 19, 0, tzinfo=timezone.utc)  # 15:00 ET
    bars = pd.DataFrame([
        {"timestamp": "2026-07-08T19:15:00+00:00", "open": 100.0, "high": 100.5,
         "low": 99.0, "close": 100.0, "volume": 1_000},
        {"timestamp": "2026-07-09T13:30:00+00:00", "open": 100.5, "high": 110.0,
         "low": 100.0, "close": 109.0, "volume": 2_000},
    ])
    path = fs.stocks_ohlcv_path("AAPL", "15m")
    path.parent.mkdir(parents=True, exist_ok=True)
    bars.to_csv(path, index=False)
    monkeypatch.setattr(
        "src.signals.tracker._promoted_entry_mode",
        lambda *_args: {"entry_mode": "PULLBACK_LIMIT", "reason": "test",
                        "entry_low": 99.0, "entry_high": 100.0, "entry_trigger": None},
    )
    signal = {
        "signal_id": "same_day_only", "symbol": "AAPL", "mode": "intraday", "direction": "long",
        "asset_class": "stocks", "created_at": created.isoformat(),
        "expires_at": (created + timedelta(hours=24)).isoformat(),
        "entry_low": 99.0, "entry_high": 100.0, "suggested_entry": 100.0,
        "invalidation": 98.0, "tp1": 104.0, "tp2": 106.0, "tp3": 108.0,
        "risk_per_unit": 2.0, "status": "waiting_for_entry",
    }
    result = track_signal(signal=signal, file_store=fs, project_config=config,
                          tracker_config=SignalTrackingConfig(),
                          now=datetime(2026, 7, 9, 14, 0, tzinfo=timezone.utc))
    assert result is not None
    outcome, status = result
    assert outcome.entry_triggered is True
    assert outcome.tp1_hit is False and outcome.tp2_hit is False and outcome.tp3_hit is False
    assert status == "expired"


def test_early_close_uses_actual_nyse_session_end():
    # Black Friday 2026 is a 13:00 ET close, not the normal 16:00 close.
    close = us_cash_session_close(datetime(2026, 11, 27, 15, 0, tzinfo=timezone.utc))
    assert close == datetime(2026, 11, 27, 18, 0, tzinfo=timezone.utc)
def test_after_hours_stock_ignores_impossible_previous_close_expiry():
    signal = {
        "asset_class": "stocks",
        "mode": "intraday",
        "created_at": "2026-07-28T22:00:00+00:00",
        "expires_at": "2026-07-28T20:00:00+00:00",
    }
    assert _effective_expiry(signal) == datetime(
        2026, 7, 29, 20, 0, tzinfo=timezone.utc
    )

