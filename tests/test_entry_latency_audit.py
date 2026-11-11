"""PART 6 — entry-latency root-cause classifier tests (read-only diagnostic). No network."""
from __future__ import annotations

import pandas as pd

from src.signals.entry_latency_audit import classify
from src.signals import entry_latency_audit as audit


def _bars(start, n, low, high, step_min=15):
    ts = pd.date_range(start, periods=n, freq=f"{step_min}min")
    return pd.DataFrame({"timestamp": ts, "low": [low] * n, "high": [high] * n,
                         "open": [low] * n, "close": [high] * n})


def test_data_gap_late_when_first_bar_far_after_creation():
    # signal created 09:35; first available bar is 13:30 (already in band) → coverage gap
    df = _bars("2026-06-18 13:30", 8, low=113.0, high=117.7)
    c = classify(created_at="2026-06-18 09:35", entry_triggered_at="2026-06-18 13:30",
                 entry_low=116.41, entry_high=117.83, candles_df=df)
    assert c["cause"] == "DATA_GAP_LATE"
    assert c["in_band_before_recorded"] == 0
    assert c["data_gap_min"] and c["data_gap_min"] > 60


def test_detection_latency_when_in_band_before_recorded():
    # continuous data from creation; price in band at 10:00 but recorded entry at 12:00 → bug
    df = _bars("2026-06-18 10:00", 12, low=116.5, high=117.5)
    c = classify(created_at="2026-06-18 10:00", entry_triggered_at="2026-06-18 12:00",
                 entry_low=116.41, entry_high=117.83, candles_df=df)
    assert c["cause"] == "DETECTION_LATENCY"
    assert c["in_band_before_recorded"] == 1


def test_fast_when_quick():
    df = _bars("2026-06-18 10:00", 4, low=116.5, high=117.5)
    c = classify(created_at="2026-06-18 10:00", entry_triggered_at="2026-06-18 10:10",
                 entry_low=116.41, entry_high=117.83, candles_df=df)
    assert c["cause"] == "FAST"


def test_no_data():
    c = classify(created_at="2026-06-18 10:00", entry_triggered_at="2026-06-18 12:00",
                 entry_low=116.0, entry_high=117.0, candles_df=None)
    assert c["cause"] == "NO_DATA"


def test_point_in_time_revalidated_entry_with_missing_ohlcv_is_not_no_data():
    c = classify(created_at="2026-06-18 10:00", entry_triggered_at="2026-06-18 10:05",
                 entry_low=116.0, entry_high=117.0, candles_df=None,
                 latency_truth="point_in_time")
    assert c["cause"] == "FAST_POINT_IN_TIME_REVALIDATED"


def test_entry_transition_snapshot_is_frozen(tmp_path, monkeypatch):
    db = str(tmp_path / "latency.sqlite")
    signal = {"signal_id": "s1", "symbol": "BTC/USDT", "asset_class": "crypto", "mode": "intraday",
              "created_at": "2026-06-18T10:00:00+00:00", "entry_low": 99.0, "entry_high": 101.0}
    out = {"entry_triggered_at": "2026-06-18T10:10:00+00:00",
           "entry_time_basis": "point_in_time_current_bar", "current_price_revalidated": True}
    monkeypatch.setattr(audit, "_load", lambda *a, **k: _bars("2026-06-18 10:00", 4, 99, 101))
    assert audit.capture_entry_snapshot(signal=signal, outcome_row=out, db=db) is True
    monkeypatch.setattr(audit, "_load", lambda *a, **k: None)
    assert audit.capture_entry_snapshot(signal=signal, outcome_row=out, db=db) is False
    import sqlite3
    c = sqlite3.connect(db)
    row = c.execute("SELECT cause, snapshot_kind, latency_truth FROM entry_latency_audit WHERE signal_id='s1'").fetchone()
    c.close()
    assert row == ("FAST", "entry_transition", "point_in_time")


def test_historical_reconstruction_is_not_reported_as_fast():
    df = _bars("2026-06-18 10:00", 4, low=116.5, high=117.5)
    c = classify(created_at="2026-06-18 10:00", entry_triggered_at="2026-06-18 10:10",
                 entry_low=116.41, entry_high=117.83, candles_df=df,
                 latency_truth="historical_reconstruction")
    assert c["cause"] == "HISTORICAL_RECONSTRUCTION"


def test_legitimate_late_when_band_reached_late_in_continuous_data():
    # continuous data, but price only enters the band in the last bar (not before recorded)
    ts = pd.date_range("2026-06-18 10:00", periods=10, freq="15min")
    low = [120.0] * 9 + [116.5]
    high = [121.0] * 9 + [117.5]
    df = pd.DataFrame({"timestamp": ts, "low": low, "high": high, "open": low, "close": high})
    rec = str(ts[-1])
    c = classify(created_at="2026-06-18 10:00", entry_triggered_at=rec,
                 entry_low=116.41, entry_high=117.83, candles_df=df)
    assert c["cause"] == "LEGITIMATE_LATE"
    assert c["in_band_before_recorded"] == 0
def test_stock_swing_overnight_gap_is_not_intraday_data_gap():
    import pandas as pd
    bars = pd.DataFrame({
        "timestamp": pd.to_datetime(["2026-07-06T13:30:00Z", "2026-07-07T13:30:00Z"]),
        "open": [100, 101], "high": [101, 102], "low": [99, 100], "close": [100.5, 101.5],
    })
    r = classify(created_at="2026-07-06T01:00:00Z", entry_triggered_at="2026-07-06T13:30:00Z",
                 entry_low=100, entry_high=101, candles_df=bars,
                 mode="swing", asset_class="stocks")
    assert r["cause"] == "LEGITIMATE_LATE"


def test_stock_intraday_in_session_gap_stays_dirty():
    import pandas as pd
    bars = pd.DataFrame({
        "timestamp": pd.to_datetime(["2026-07-06T15:00:00Z"]),
        "open": [100], "high": [101], "low": [99], "close": [100.5],
    })
    r = classify(created_at="2026-07-06T14:00:00Z", entry_triggered_at="2026-07-06T15:00:00Z",
                 entry_low=100, entry_high=101, candles_df=bars,
                 mode="intraday", asset_class="stocks")
    assert r["cause"] == "DATA_GAP_LATE"


def test_stock_intraday_outside_session_is_session_gap_not_data_gap():
    bars = pd.DataFrame({
        "timestamp": pd.to_datetime(["2026-07-13T13:30:00Z"]),
        "open": [100], "high": [101], "low": [99], "close": [100.5],
    })
    r = classify(created_at="2026-07-13T01:00:00Z", entry_triggered_at="2026-07-13T13:30:00Z",
                 entry_low=100, entry_high=101, candles_df=bars,
                 mode="intraday", asset_class="stocks")
    assert r["cause"] == "SESSION_GAP"
