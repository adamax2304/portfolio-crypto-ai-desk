"""PART 1 — stock intraday coverage classifier tests (no network/live)."""
from __future__ import annotations

import pandas as pd

from src.config import ProjectConfig
from src.stocks import intraday_coverage as coverage
from src.stocks.data_collectors.yf_client import OHLCVResult
from src.stocks.intraday_coverage import classify


def _session(date, start_hour=13, start_min=30, n=26):
    ts = pd.date_range(f"{date} {start_hour:02d}:{start_min:02d}", periods=n, freq="15min", tz="UTC")
    return pd.DataFrame({"timestamp": ts, "open": [10] * n, "high": [11] * n, "low": [9] * n, "close": [10] * n})


def test_no_intraday_data():
    assert classify(None)["status"] == "NO_INTRADAY_DATA"
    assert classify(pd.DataFrame())["status"] == "NO_INTRADAY_DATA"


def test_data_ok_full_session():
    df = pd.concat([_session("2026-06-23"), _session("2026-06-24")], ignore_index=True)
    c = classify(df)
    assert c["status"] == "DATA_OK"
    assert c["first_bar_gap_min"] == 0.0 and c["sessions"] == 2


def test_data_gap_late_when_first_bar_after_open():
    # first bar at 16:30 UTC (3h after the 13:30 open) → DATA_GAP_LATE
    df = _session("2026-06-24", start_hour=16, start_min=30, n=10)
    c = classify(df)
    assert c["status"] == "DATA_GAP_LATE"
    assert c["first_bar_gap_min"] >= 60


def test_partial_data_when_few_bars_per_session():
    df = pd.concat([_session("2026-06-23", n=5), _session("2026-06-24", n=4)], ignore_index=True)
    c = classify(df)
    assert c["status"] == "PARTIAL_DATA"


def test_backfill_uses_shared_provider_and_writes_tracker_cache_atomically(monkeypatch, tmp_path):
    config = ProjectConfig(root=tmp_path, settings={"data": {"raw_dir": "raw", "db_path": "db/test.sqlite"}},
                           watchlist={}, sources={}, scoring={}, universe={}, exchanges={})
    frame = _session("2026-06-24", n=3).set_index("timestamp")
    result = OHLCVResult("AAPL", "15m", len(frame), 10.0, str(frame.index[-1]), frame, "finnhub")

    monkeypatch.setattr(coverage, "load_config", lambda: config)
    from src.stocks.data_collectors import yf_client
    monkeypatch.setattr(yf_client, "fetch_ohlcv", lambda *args, **kwargs: result)

    outcome = coverage.backfill(["AAPL"], lookback_days=2)

    cached = tmp_path / "raw" / "stocks" / "15m" / "AAPL.csv"
    assert outcome["count"] == 1 and outcome["fetched"]["AAPL"]["source"] == "finnhub"
    assert cached.exists()
    assert "timestamp" in pd.read_csv(cached).columns
