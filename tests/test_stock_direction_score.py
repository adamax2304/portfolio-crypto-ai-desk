"""PART 5 — multi-factor stock direction score tests (paper-only). No network/live."""
from __future__ import annotations

import sqlite3

import pandas as pd

from src.stocks.stock_direction_score import (
    score_direction, ensure_table, _upsert, _closed_bars_as_of,
)


def test_all_factors_agree_long_is_confirmed():
    r = score_direction(close=110, ema20=105, ema50=100, vwap=108,
                        prev_day_high=109, prev_day_low=95, mom_ret=0.02, rs_spy=0.03,
                        symbol="AAPL", btc_trend=0)
    assert r["direction"] == "long"
    assert r["dir_label"] == "MULTI_FACTOR_CONFIRMED"
    assert r["factors_used"] >= 4


def test_conflict_when_factors_split():
    # ema up, but below VWAP, below prior-day-low, negative momentum, weak RS → mixed
    r = score_direction(close=100, ema20=99, ema50=98, vwap=102,
                        prev_day_high=105, prev_day_low=101, mom_ret=-0.01, rs_spy=-0.02,
                        symbol="AAPL", btc_trend=0)
    assert r["dir_label"] == "MULTI_FACTOR_CONFLICT"
    assert any(v > 0 for v in r["votes"].values()) and any(v < 0 for v in r["votes"].values())


def test_mstr_btc_factor_only_for_mstr():
    base = dict(close=100, ema20=100, ema50=100, vwap=100, prev_day_high=100,
                prev_day_low=100, mom_ret=0.0, rs_spy=0.0)
    non = score_direction(symbol="AAPL", btc_trend=-1, **base)
    mstr = score_direction(symbol="MSTR", btc_trend=-1, **base)
    assert non["votes"]["mstr_btc"] == 0
    assert mstr["votes"]["mstr_btc"] == -1           # BTC down → MSTR short tilt
    assert mstr["direction_score"] < non["direction_score"]


def test_stock_direction_refresh_report_tolerates_missing_btc_trend(monkeypatch, capsys):
    from src.cli import stock_direction_refresh
    from src.stocks import stock_direction_score

    monkeypatch.setattr(stock_direction_score, "refresh", lambda **_: {
        "processed": 0,
        "multi_factor": 0,
        "would_flip_vs_production": 0,
        "by_label": {},
    })

    stock_direction_refresh()

    assert "btc_trend=unavailable" in capsys.readouterr().out


def test_neutral_when_no_signal():
    r = score_direction(close=None, ema20=None, ema50=None, vwap=None, prev_day_high=None,
                        prev_day_low=None, mom_ret=None, rs_spy=None, symbol="AAPL", btc_trend=0)
    assert r["direction"] == "neutral"
    assert r["factors_used"] == 0


def test_table_roundtrip():
    rec = {"signal_id": "sig_sd", "symbol": "MSTR", "mode": "intraday",
           "production_direction": "long", "direction": "short", "direction_score": -5.6,
           "dir_label": "MULTI_FACTOR_CONFIRMED", "vote_ema": -1, "vote_vwap": -1,
           "vote_pdhl": -1, "vote_momentum": -1, "vote_rs_spy": -1, "vote_mstr_btc": -1,
           "factors_used": 6, "agreement": 6, "agrees_with_production": 0,
           "rs_spy_20d": -0.05, "vwap": 1.0, "prev_day_high": 2.0, "prev_day_low": 1.0,
           "candles_used": 100, "reason": "test", "computed_at": "2026-06-25T00:00:00Z"}
    conn = sqlite3.connect(":memory:"); conn.row_factory = sqlite3.Row
    ensure_table(conn); _upsert(conn, rec); conn.commit()
    row = dict(conn.execute("SELECT * FROM stock_direction_score WHERE signal_id=?", ("sig_sd",)).fetchone())
    assert row["direction"] == "short" and row["vote_mstr_btc"] == -1
    _upsert(conn, rec); conn.commit()
    assert conn.execute("SELECT count(*) FROM stock_direction_score").fetchone()[0] == 1


def test_point_in_time_slice_excludes_open_and_future_bars():
    frame = pd.DataFrame({
        "timestamp": pd.to_datetime([
            "2026-09-01T14:00:00Z", "2026-09-01T14:15:00Z", "2026-09-01T14:30:00Z"
        ]),
        "open": [1, 2, 3], "high": [2, 3, 4], "low": [0, 1, 2],
        "close": [1.5, 2.5, 3.5], "volume": [10, 10, 10],
    })
    out = _closed_bars_as_of(
        frame, pd.Timestamp("2026-09-01T14:29:59Z"), timeframe="15m")
    assert list(out["close"]) == [1.5]


def test_ensure_table_migrates_point_in_time_columns():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE stock_direction_score (signal_id TEXT PRIMARY KEY, direction TEXT)")
    ensure_table(conn)
    columns = {row[1] for row in conn.execute("PRAGMA table_info(stock_direction_score)")}
    assert {"as_of_at", "data_cutoff_at", "is_point_in_time", "version"} <= columns
