"""Stocks data-quality gating (S1-S8): DGL never edge, legacy not promotable, position framework
independent, insufficient clean sample blocks, coverage gap → DATA_QUALITY_BLOCKED, clean daily/
weekly position data accrues separately. All read-model / paper — no live, no proposed_signals."""
from __future__ import annotations

import sqlite3
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pandas as pd

from src.execution import entry_mode_calibration as cal
from src.stocks import coverage_gate as cg


def _row(sid, usd, r=1.0, status="filled", outcome="closed"):
    return {"signal_id": sid, "entry_fill_status": status, "net_pnl_usdt": usd, "net_r": r,
            "outcome_status": outcome, "gross_r": r, "fees_usdt": 0.0, "slippage_usdt": 0.0}


# ---- S4: DATA_GAP_LATE never counted as edge -------------------------------------------------
def test_dgl_excluded_from_edge_metrics():
    rows = [_row("a", 100), _row("b", 100), _row("dirty", -500)]
    latency = {"dirty": {"cause": "DATA_GAP_LATE"}}
    m = cal._slice_metrics(rows, latency)
    assert m["net_pnl_usd"] == 200.0          # dirty −$500 NOT in edge (would be −$300 if counted)
    assert m["clean_closed"] == 2 and m["dirty_closed_dgl"] == 1
    assert m["clean_trades"] == 2 and m["dirty_trades_dgl"] == 1


# ---- S1: legacy stocks swing/invest not promotable -------------------------------------------
def _cfg():
    return {"verdicts": {"min_clean_trades_for_verdict": 30, "data_gap_late_block_pct": 0.30,
                         "disable": {"net_pnl_usd_max": 0.0, "profit_factor_min": 1.15}}}


def test_legacy_stocks_swing_invest_not_promotable():
    for mode in ("swing", "invest"):
        v, _ = cal.slice_verdict(asset_class="stocks", mode=mode, entry_mode="PULLBACK_LIMIT",
                                 window=cal.FORWARD, metrics={"closed": 200, "profit_factor": 3.0,
                                 "net_pnl_usd": 5000}, paired_delta_usd=500, old_max_dd_usd=100, cfg=_cfg())
        assert v == "UNSUPPORTED_LEGACY"       # never promotable even with great (legacy) numbers


# ---- S3: insufficient CLEAN sample blocks any conclusion -------------------------------------
def test_insufficient_clean_sample_blocks_conclusion():
    v, _ = cal.slice_verdict(asset_class="stocks", mode="intraday", entry_mode="STRUCTURAL_RETEST",
                             window=cal.FORWARD, metrics={"closed": 5, "profit_factor": 9.0,
                             "net_pnl_usd": 9999, "dirty_closed_dgl": 40}, paired_delta_usd=999,
                             old_max_dd_usd=100, cfg=_cfg())
    assert v == "INSUFFICIENT_CLEAN_SAMPLE"    # 5 clean < 30 → blocked despite huge (thin) PnL
    assert v in cal.BLOCKED_VERDICTS


# ---- S5 coverage gap → DATA_QUALITY_BLOCKED --------------------------------------------------
def test_high_dgl_share_blocks():
    v, _ = cal.slice_verdict(asset_class="stocks", mode="intraday", entry_mode="STRUCTURAL_RETEST",
                             window=cal.FORWARD, metrics={"closed": 200, "data_gap_late_share": 0.55,
                             "profit_factor": 2.0, "net_pnl_usd": 500}, paired_delta_usd=100,
                             old_max_dd_usd=100, cfg=_cfg())
    assert v == "DATA_QUALITY_BLOCKED"


# ---- S2/S6 coverage classifier: intraday gap dirty; clean daily ok ---------------------------
def _daily(n, last):
    ts = pd.date_range(end=last, periods=n, freq="D", tz="UTC")
    return pd.DataFrame({"timestamp": ts, "open": 1, "high": 1, "low": 1, "close": 1, "volume": 1})


def test_coverage_intraday_gap_is_dirty():
    now = datetime(2026, 7, 7, 20, 0, tzinfo=timezone.utc)
    # first 15m bar at 15:30 UTC = 2h after 13:30 open → DATA_GAP_LATE, not clean
    ts = pd.date_range("2026-07-07 15:30", periods=20, freq="15min", tz="UTC")
    df = pd.DataFrame({"timestamp": ts, "open": 1, "high": 1, "low": 1, "close": 1, "volume": 1})
    c = cg.classify_series(df, "15m", "intraday", now=now)
    assert c["status"] == "DATA_GAP_LATE" and c["is_clean"] is False


def test_coverage_closed_complete_rth_is_clean_and_dst_aware():
    now = datetime(2026, 7, 13, 21, 0, tzinfo=timezone.utc)
    ts = pd.date_range("2026-07-13 13:30", periods=26, freq="15min", tz="UTC")
    df = pd.DataFrame({"timestamp": ts, "open": 1, "high": 1, "low": 1, "close": 1, "volume": 1})
    c = cg.classify_series(df, "15m", "intraday", now=now)
    assert c["status"] == "DATA_OK_CLOSED_SESSION"
    assert c["is_clean"] is True and c["missing_bars"] == 0


def test_coverage_missing_rth_bar_is_not_clean():
    now = datetime(2026, 7, 13, 21, 0, tzinfo=timezone.utc)
    ts = pd.date_range("2026-07-13 13:30", periods=26, freq="15min", tz="UTC").delete(8)
    df = pd.DataFrame({"timestamp": ts, "open": 1, "high": 1, "low": 1, "close": 1, "volume": 1})
    c = cg.classify_series(df, "15m", "intraday", now=now)
    assert c["status"] == "PARTIAL_DATA"
    assert c["is_clean"] is False and c["missing_bars"] == 1


def test_coverage_clean_daily_position_accrues():
    last = datetime(2026, 7, 7, tzinfo=timezone.utc)
    c = cg.classify_series(_daily(40, last), "1d", "position", now=last + timedelta(hours=6))
    assert c["status"] == "DATA_OK" and c["is_clean"] is True and c["bars"] == 40


def test_coverage_stale_daily_not_clean():
    old = datetime(2026, 5, 1, tzinfo=timezone.utc)              # last bar ~2 months old
    c = cg.classify_series(_daily(40, old), "1d", "position", now=datetime(2026, 7, 7, tzinfo=timezone.utc))
    assert c["is_clean"] is False and c["status"] == "STALE"


def test_coverage_archives_live_grade_provider_data(tmp_path, monkeypatch):
    """A named primary provider must populate the durable OHLCV cache.

    The old implementation archived only a synthetic ``provider`` source,
    while real adapters identify themselves as ``alpaca``/``polygon``.  That
    left the next cache-only cycle with no data even after a clean prewarm.
    """
    now = datetime(2026, 7, 13, 21, 0, tzinfo=timezone.utc)
    ts = pd.date_range("2026-07-13 13:30", periods=26, freq="15min", tz="UTC")
    frame = pd.DataFrame(
        {"timestamp": ts, "open": 1, "high": 1, "low": 1, "close": 1, "volume": 1}
    )

    from src.stocks.data_collectors import yf_client

    monkeypatch.setattr(
        yf_client,
        "fetch_ohlcv",
        lambda symbol, timeframe: SimpleNamespace(dataframe=frame, source="alpaca"),
    )

    class FakeStore:
        def load_stocks_ohlcv(self, symbol, timeframe):
            return None

        def stocks_ohlcv_path(self, symbol, timeframe):
            return tmp_path / symbol / f"{timeframe}.csv"

    result = cg._fetch_with_fallback(
        "AAPL", "intraday", FakeStore(), archive=True, fetch=True, now=now
    )
    archived = tmp_path / "AAPL" / "15m.csv"

    assert result["is_clean"] is True
    assert result["source"] == "alpaca"
    assert archived.exists()
    assert "timestamp" in pd.read_csv(archived).columns


# ---- S1/S3: position framework independent + clean-gated -------------------------------------
def test_position_framework_independent_and_clean_gated(tmp_path):
    from src.stocks.position_framework import shadow_store as ss
    db = str(tmp_path / "pf.sqlite")
    ss.ensure_tables(db)
    c = sqlite3.connect(db)
    c.execute("INSERT INTO stocks_position_candidates (candidate_id, created_at, symbol, asset_class, mode, playbook) "
              "VALUES ('spf_AAPL_2026-07-05','2026-07-05','AAPL','stocks','swing','stocks_swing_growth_breakout')")
    # one CLEAN closed (gap_loss_r NULL) + one DIRTY closed (gap_loss_r>0 → excluded)
    c.execute("INSERT INTO stocks_position_outcomes (candidate_id, status, net_pnl_usd, gap_loss_r) "
              "VALUES ('spf_AAPL_2026-07-05','closed', 50.0, NULL)")
    c.execute("INSERT INTO stocks_position_outcomes (candidate_id, status, net_pnl_usd, gap_loss_r) "
              "VALUES ('spf_DIRTY_2026-07-05','closed', 300.0, 1.2)")
    c.commit(); c.close()
    r = ss.readiness_summary(db_path=db)
    assert r["legacy_evidence_reused"] is False            # never reuses legacy stocks swing/invest
    assert r["outcomes"]["clean_closed"] == 1 and r["outcomes"]["dirty_closed"] == 1
    assert r["verdict"] == "INSUFFICIENT_CLEAN_SAMPLE"     # 1 clean < gate → no good/bad conclusion
    assert r["net_usd_clean_closed"] == 50.0               # dirty $300 excluded from clean edge


def test_missing_coverage_row_blocks_edge(tmp_path):
    # a stock shadow outcome with NO stock_coverage_by_mode row → conservatively NOT clean.
    from src.execution.paper_shadow_engine import ensure_tables
    db = str(tmp_path / "cov.sqlite")
    c = sqlite3.connect(db)
    ensure_tables(c)                                       # creates outcomes + coverage columns
    c.execute("CREATE TABLE proposed_signals (signal_id TEXT, symbol TEXT, asset_class TEXT, mode TEXT)")
    c.execute("INSERT INTO proposed_signals VALUES ('s1','AAPL','stocks','swing')")
    c.execute("INSERT INTO paper_shadow_execution_outcomes (signal_id, branch, symbol, asset_class, "
              "fee_profile) VALUES ('s1','new_logic_shadow','AAPL','stocks','stock_etf_default')")
    c.commit(); c.close()
    res = cg.mark_outcome_coverage(db=db)                  # no latency, no coverage row for (AAPL, swing)
    assert res["updated"] == 1
    c = sqlite3.connect(db)
    status, clean = c.execute("SELECT data_coverage_status, is_clean_for_edge "
                              "FROM paper_shadow_execution_outcomes WHERE signal_id='s1'").fetchone()
    c.close()
    assert status == "NO_COVERAGE_ROW" and clean == 0      # missing coverage → not clean, never edge


def test_coverage_module_is_read_model_only():
    import pathlib
    src = pathlib.Path(cg.__file__).read_text(encoding="utf-8").lower()
    for bad in ("update proposed_signals", "insert into proposed_signals", "final_r =",
                "update signal_outcomes", "insert into signal_outcomes", "create_order", "auto_live"):
        assert bad not in src, bad
