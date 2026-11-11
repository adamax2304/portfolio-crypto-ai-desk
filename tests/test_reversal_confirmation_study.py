from datetime import datetime, timezone
from pathlib import Path
import sqlite3
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.research_reversal_confirmation_study import (
    _clip_crypto_bar_window,
    _confirmation,
    _crypto_load_bar_frames,
    crypto_context_strategy,
)


def _bars(rows):
    frame = pd.DataFrame(rows, columns=["timestamp", "open", "high", "low", "close", "volume"])
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame["_rvol_confirm"] = 1.0
    return frame


def test_two_bar_hold_enters_only_after_two_adjacent_closed_minutes():
    decision = datetime(2026, 10, 1, 14, 0, tzinfo=timezone.utc)
    frame = _bars([
        ("2026-10-01T14:00:00Z", 100.0, 101.0, 99.8, 100.8, 1000),
        ("2026-10-01T14:01:00Z", 100.8, 101.3, 100.5, 101.1, 1000),
    ])
    result = _confirmation(frame, {"decision_at": decision, "reclaim_level": 100.0},
                           "base_held_2x1m", window_minutes=2, stock_clock=False)
    assert result is not None
    assert result["entry"] == 101.1
    assert result["entry_at"] == pd.Timestamp("2026-10-01T14:02:00Z")


def test_two_bar_hold_rejects_a_missing_minute():
    decision = datetime(2026, 10, 1, 14, 0, tzinfo=timezone.utc)
    frame = _bars([
        ("2026-10-01T14:00:00Z", 100.0, 101.0, 99.8, 100.8, 1000),
        ("2026-10-01T14:02:00Z", 100.8, 101.3, 100.5, 101.1, 1000),
    ])
    result = _confirmation(frame, {"decision_at": decision, "reclaim_level": 100.0},
                           "base_held_2x1m", window_minutes=3, stock_clock=False)
    assert result is None


def test_volume_confirm_uses_only_closed_bar_inside_window():
    decision = datetime(2026, 10, 1, 14, 0, tzinfo=timezone.utc)
    frame = _bars([
        ("2026-10-01T14:00:00Z", 100.0, 101.0, 99.8, 100.9, 1000),
        ("2026-10-01T14:01:00Z", 100.9, 101.4, 100.8, 101.3, 3000),
    ])
    frame.loc[1, "_rvol_confirm"] = 1.8
    result = _confirmation(frame, {"decision_at": decision, "reclaim_level": 100.0},
                           "vol_reclaim_1x1m", window_minutes=1, stock_clock=False)
    assert result is None
    result = _confirmation(frame, {"decision_at": decision, "reclaim_level": 100.0},
                           "vol_reclaim_1x1m", window_minutes=2, stock_clock=False)
    assert result is not None
    assert result["entry_at"] == pd.Timestamp("2026-10-01T14:02:00Z")


def test_crypto_archive_loader_keeps_exchange_symbol_format():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE ohlcv_1m(exchange,symbol,ts,open,high,low,close,volume)")
    conn.execute("INSERT INTO ohlcv_1m VALUES('bybit','BTC/USDT',1790863200000,100,101,99,100.5,12)")
    frame, venue = _crypto_load_bar_frames(conn, "BTC/USDT")
    assert venue == "bybit"
    assert len(frame) == 1
    assert frame.iloc[0]["close"] == 100.5
    conn.close()


def test_crypto_window_filter_handles_millisecond_precision_timestamps():
    frame = pd.DataFrame({
        "timestamp": pd.to_datetime([
            "2026-09-11T23:59:00Z", "2026-09-12T00:00:00Z", "2026-09-12T00:01:00Z",
        ], utc=True).as_unit("ms"),
        "open": [1.0, 1.0, 1.0], "high": [1.0, 1.0, 1.0],
        "low": [1.0, 1.0, 1.0], "close": [1.0, 1.0, 1.0], "volume": [1.0, 1.0, 1.0],
    })
    start_ms = int(pd.Timestamp("2026-09-12T00:00:00Z").timestamp() * 1000)
    end_ms = int(pd.Timestamp("2026-09-12T00:01:00Z").timestamp() * 1000)
    filtered = _clip_crypto_bar_window(frame, start_ms, end_ms)
    assert filtered["timestamp"].tolist() == frame["timestamp"].iloc[1:].tolist()


def test_crypto_replay_uses_existing_market_context_provider():
    assert callable(crypto_context_strategy._contexts)
