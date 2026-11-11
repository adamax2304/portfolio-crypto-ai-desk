"""Tests for the Stocks Position Framework — SHADOW-ONLY (stocks_swing_growth_breakout).

No network. Synthetic OHLCV only. Covers: config load, feature math, detector gates, risk plan
(exact R), separate-shadow-table storage (never proposed_signals), and a CLI smoke test.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.stocks.position_framework import config as pf_config
from src.stocks.position_framework import features as pf_features
from src.stocks.position_framework import risk_plan as pf_risk
from src.stocks.position_framework import setup_detector as pf_detector
from src.stocks.position_framework import shadow_store as pf_store


# ----------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------
def _frame(n, start, slope, vol=1_000_000, last_vol_mult=1.5):
    idx = pd.date_range("2024-01-01", periods=n, freq="D")
    close = np.array([start + slope * i for i in range(n)], dtype=float)
    high = close * 1.01
    low = close * 0.99
    op = close * 0.999
    v = np.full(n, float(vol))
    v[-1] = vol * last_vol_mult
    return pd.DataFrame({"open": op, "high": high, "low": low, "close": close, "volume": v}, index=idx)


_MKT_OK = {"label": "risk_on", "spy_above_50d": True, "spy_above_200d": True,
           "qqq_above_50d": True, "vix": 15}
_SEC_OK = {"sector": "Technology", "sector_etf": "XLK", "sector_above_50d": True,
           "sector_rs_positive": True}


# ----------------------------------------------------------------------------
# 1. config
# ----------------------------------------------------------------------------
def test_config_loads_shadow_only_single_active_playbook():
    cfg = pf_config.load_config()
    assert pf_config.is_shadow_only(cfg) is True
    assert pf_config.active_playbooks(cfg) == ["stocks_swing_growth_breakout"]
    # disabled placeholders are present but NOT active
    disabled = cfg.get("disabled_playbooks") or {}
    assert "stocks_swing_earnings_drift" in disabled
    assert "stocks_invest_stage2_position" in disabled
    assert "stocks_swing_earnings_drift" not in pf_config.active_playbooks(cfg)
    assert cfg.get("write_proposed_signals") is False


# ----------------------------------------------------------------------------
# 2. features
# ----------------------------------------------------------------------------
def test_features_compute_core_indicators():
    df = _frame(260, 50, 0.2)
    spy = _frame(260, 400, 0.01)
    sector = _frame(260, 100, 0.05)
    feats = pf_features.compute_features(df, spy_df=spy, sector_df=sector)
    assert feats["available"] is True
    assert feats["sma50"] is not None and feats["sma200"] is not None
    assert feats["above_50d"] is True and feats["above_200d"] is True
    assert feats["atr14"] and feats["atr14"] > 0
    assert feats["volume_ratio"] and feats["volume_ratio"] > 1.0    # last bar volume is 1.5x
    # near-high: monotonic uptrend → last close within ~1% of the recent high
    nh = min(v for v in feats["near_high"].values() if v is not None)
    assert 0 <= nh <= 3
    assert feats["rs_spy"] is not None and feats["rs_spy"] > 0        # outperforming flat SPY


def test_features_insufficient_history_returns_none_not_fabricated():
    df = _frame(30, 50, 0.2)          # < 200 bars
    feats = pf_features.compute_features(df)
    assert feats["available"] is True
    assert feats["sma200"] is None    # not fabricated
    assert feats["above_200d"] is None


# ----------------------------------------------------------------------------
# 3. detector
# ----------------------------------------------------------------------------
def test_detector_strong_uptrend_passes():
    df = _frame(260, 50, 0.2)
    spy = _frame(260, 400, 0.01)
    sector = _frame(260, 100, 0.05)
    feats = pf_features.compute_features(df, spy_df=spy, sector_df=sector)
    cfg = pf_config.load_config()
    c = pf_detector.detect("TESTU", feats, market_ctx=_MKT_OK, sector_ctx=_SEC_OK,
                           cfg=cfg, equity_usd=5000)
    assert c["passed"] is True
    assert c["playbook"] == "stocks_swing_growth_breakout"
    assert c["mode"] == "swing" and c["asset_class"] == "stocks" and c["direction"] == "long"
    assert c["setup_variant"] in pf_detector.SETUP_VARIANTS
    assert 0 <= c["score"] <= 100
    assert (c["risk_plan"] or {}).get("stop_price") < c["entry_price"]


def test_detector_weak_below_200d_rejected():
    df = _frame(260, 100, -0.15)      # downtrend, below MAs
    spy = _frame(260, 400, 0.01)
    feats = pf_features.compute_features(df, spy_df=spy)
    cfg = pf_config.load_config()
    c = pf_detector.detect("WEAK", feats, market_ctx=_MKT_OK, sector_ctx=_SEC_OK,
                           cfg=cfg, equity_usd=5000)
    assert c["passed"] is False
    assert any("200D" in r or "50D" in r for r in c["rejection_reasons"])


def test_detector_vix_panic_and_spy_riskoff_block():
    df = _frame(260, 50, 0.2)
    spy = _frame(260, 400, 0.01)
    sector = _frame(260, 100, 0.05)
    feats = pf_features.compute_features(df, spy_df=spy, sector_df=sector)
    cfg = pf_config.load_config()
    panic = pf_detector.detect("TESTU", feats, market_ctx={**_MKT_OK, "vix": 35},
                               sector_ctx=_SEC_OK, cfg=cfg, equity_usd=5000)
    assert panic["passed"] is False and any("VIX" in r for r in panic["rejection_reasons"])
    riskoff = pf_detector.detect("TESTU", feats,
                                 market_ctx={**_MKT_OK, "spy_above_50d": False, "spy_above_200d": False},
                                 sector_ctx=_SEC_OK, cfg=cfg, equity_usd=5000)
    assert riskoff["passed"] is False and any("SPY" in r for r in riskoff["rejection_reasons"])


# ----------------------------------------------------------------------------
# 4. risk plan
# ----------------------------------------------------------------------------
def test_risk_plan_structural_stop_and_exact_r():
    rc = {"stop_atr_multiple_min": 1.5, "stop_atr_multiple_max": 2.5, "stop_buffer_atr": 0.25,
          "gap_risk_multiplier": 1.25, "reject_if_stop_distance_pct_above": 12, "paper_risk_pct": 0.0025}
    ec = {"partial_1_r": 2.0, "partial_2_r": 3.0, "partial_1_pct": 0.5, "partial_2_pct": 0.25}
    plan = pf_risk.build_risk_plan(entry=100, atr=2, swing_low=96, risk_cfg=rc, exits_cfg=ec, equity_usd=5000)
    assert plan["rejected"] is False
    assert plan["stop_price"] == pytest.approx(95.5)              # 96 - 0.25*2
    assert plan["risk_per_share"] == pytest.approx(4.5)
    assert plan["tp1"] == pytest.approx(109.0) and plan["tp1_r"] == pytest.approx(2.0)
    assert plan["tp2"] == pytest.approx(113.5) and plan["tp2_r"] == pytest.approx(3.0)
    assert plan["risk_usd"] == pytest.approx(12.5)                # 5000 * 0.0025


def test_risk_plan_rejects_too_wide_stop():
    rc = {"stop_atr_multiple_min": 1.5, "stop_atr_multiple_max": 2.5, "stop_buffer_atr": 0.25,
          "reject_if_stop_distance_pct_above": 12}
    plan = pf_risk.build_risk_plan(entry=100, atr=10, swing_low=80, risk_cfg=rc, exits_cfg={}, equity_usd=5000)
    assert plan["rejected"] is True
    assert "stop distance" in (plan["rejection_reason"] or "")


# ----------------------------------------------------------------------------
# 5. storage — separate shadow tables, never proposed_signals
# ----------------------------------------------------------------------------
def test_storage_writes_shadow_table_not_proposed_signals(tmp_path):
    db = tmp_path / "shadow_test.sqlite"
    df = _frame(260, 50, 0.2)
    spy = _frame(260, 400, 0.01)
    sector = _frame(260, 100, 0.05)
    feats = pf_features.compute_features(df, spy_df=spy, sector_df=sector)
    cfg = pf_config.load_config()
    cand = pf_detector.detect("TESTU", feats, market_ctx=_MKT_OK, sector_ctx=_SEC_OK,
                              cfg=cfg, equity_usd=5000)
    cand["status"] = "shadow_open"
    n = pf_store.insert_candidates([cand], created_at="2026-07-02T12:00:00+00:00", db_path=db)
    assert n == 1
    rows = pf_store.latest_candidates(limit=10, only_open=True, db_path=db)
    assert len(rows) == 1
    r = rows[0]
    assert r["symbol"] == "TESTU" and r["status"] == "shadow_open"
    assert r["playbook"] == "stocks_swing_growth_breakout" and r["mode"] == "swing"
    assert r["tp1_r"] is not None                        # exact R persisted
    # our code must NEVER create/write proposed_signals in this DB
    import sqlite3
    conn = sqlite3.connect(str(db))
    try:
        names = {row[0] for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
    finally:
        conn.close()
    assert "stocks_position_candidates" in names
    assert "proposed_signals" not in names               # shadow lane only

    # idempotent re-insert (same symbol + scan date) → still one row
    n2 = pf_store.insert_candidates([cand], created_at="2026-07-02T18:00:00+00:00", db_path=db)
    assert n2 == 1
    assert len(pf_store.latest_candidates(limit=10, db_path=db)) == 1

    # next-day duplicate thesis stays suppressed while the first candidate is still open.
    n3 = pf_store.insert_candidates([cand], created_at="2026-07-03T18:00:00+00:00", db_path=db)
    assert n3 == 0
    assert len(pf_store.latest_candidates(limit=10, db_path=db)) == 1

    # once the prior thesis has a terminal outcome, a fresh scan may create a new candidate.
    pf_store.upsert_outcome("spf_TESTU_2026-07-02", checked_at="2026-07-04T00:00:00+00:00",
                            status="no_entry", db_path=db)
    n4 = pf_store.insert_candidates([cand], created_at="2026-07-04T18:00:00+00:00", db_path=db)
    assert n4 == 1
    assert len(pf_store.latest_candidates(limit=10, db_path=db)) == 1


def test_lifecycle_reconciliation_supersedes_legacy_duplicate_without_fake_pnl(tmp_path):
    db = tmp_path / "lifecycle.sqlite"
    base = {
        "symbol": "AAPL", "asset_class": "stocks", "mode": "swing",
        "playbook": "stocks_swing_growth_breakout", "setup_variant": "breakout",
        "direction": "long", "score": 80, "passed": True,
        "risk_plan": {},
    }
    # Simulate the historical bug directly: an old canonical candidate plus a
    # later duplicate that never received an outcome row.
    assert pf_store.insert_candidates([base], created_at="2026-07-05T12:00:00+00:00", db_path=db) == 1
    import sqlite3
    conn = sqlite3.connect(str(db))
    try:
        conn.execute("INSERT INTO stocks_position_candidates "
                     "(candidate_id,created_at,symbol,asset_class,mode,playbook,setup_variant,direction,score,status) "
                     "VALUES (?,?,?,?,?,?,?,?,?,?)",
                     ("spf_AAPL_2026-07-06", "2026-07-06T12:00:00+00:00", "AAPL", "stocks", "swing",
                      "stocks_swing_growth_breakout", "breakout", "long", 81, "shadow_open"))
        conn.commit()
    finally:
        conn.close()
    repaired = pf_store.reconcile_open_candidate_lifecycle(
        db_path=db, checked_at="2026-07-07T00:00:00+00:00")
    assert repaired["duplicates_superseded"] == 1
    conn = sqlite3.connect(str(db))
    try:
        duplicate = conn.execute("SELECT status FROM stocks_position_candidates WHERE candidate_id=?",
                                 ("spf_AAPL_2026-07-06",)).fetchone()[0]
        outcome = conn.execute("SELECT status,close_reason,net_pnl_usd FROM stocks_position_outcomes "
                               "WHERE candidate_id=?", ("spf_AAPL_2026-07-06",)).fetchone()
    finally:
        conn.close()
    assert duplicate == "shadow_duplicate_superseded"
    assert outcome == ("no_entry", "superseded_duplicate", None)

def test_zero_candidate_scan_is_recorded_separately_from_candidates(tmp_path):
    db = tmp_path / "scan_runs.sqlite"
    assert pf_store.latest_scan_time(db_path=db) is None
    pf_store.record_scan_run(
        created_at="2026-07-13T01:40:37+00:00", universe_size=68, scanned=68,
        candidate_count=0, rejected_count=68, persisted=0, market_label="risk_on",
        db_path=db,
    )
    assert pf_store.latest_scan_time(db_path=db) == "2026-07-13T01:40:37+00:00"
    conn = __import__("sqlite3").connect(str(db))
    try:
        row = conn.execute(
            "SELECT universe_size,scanned,candidate_count,rejected_count,persisted,market_label "
            "FROM stocks_position_scan_runs"
        ).fetchone()
    finally:
        conn.close()
    assert row == (68, 68, 0, 68, 0, "risk_on")

# ----------------------------------------------------------------------------
# 6. CLI smoke — report command, SHADOW ONLY banner, no Telegram
# ----------------------------------------------------------------------------
def test_cli_position_report_smoke(tmp_path, monkeypatch):
    from typer.testing import CliRunner
    from src.cli import app
    from src.stocks.position_framework import report as pf_report

    monkeypatch.setattr(pf_store, "DEFAULT_DB_PATH", tmp_path / "cli.sqlite")
    monkeypatch.setattr(pf_report, "REPORT_PATH", tmp_path / "latest.md")
    result = CliRunner().invoke(app, ["stocks-position-report"])
    assert result.exit_code == 0, result.output
    assert "SHADOW ONLY" in result.output
    assert "stocks_swing_growth_breakout" in result.output
    assert (tmp_path / "latest.md").exists()


# ----------------------------------------------------------------------------
# 7. Old stocks swing/invest are fully retired — CLI no-op + pipeline hard guard
# ----------------------------------------------------------------------------
def test_cli_stocks_swing_report_deprecated_no_pipeline():
    from typer.testing import CliRunner
    from src.cli import app
    result = CliRunner().invoke(app, ["stocks-swing-report"])
    assert result.exit_code == 0, result.output
    assert "DEPRECATED/REMOVED" in result.output
    assert "stocks-position-scan" in result.output


def test_cli_stocks_invest_report_deprecated_no_pipeline():
    from typer.testing import CliRunner
    from src.cli import app
    result = CliRunner().invoke(app, ["stocks-invest-report"])
    assert result.exit_code == 0, result.output
    assert "DEPRECATED/REMOVED" in result.output
    assert "stocks-position-scan" in result.output


def test_pipeline_swing_blocked_before_side_effects(monkeypatch):
    """run_report(mode='swing') must raise BEFORE any fetch/save (no trade_ideas/proposed_signals)."""
    from src.config import load_config
    from src.stocks.pipelines.stocks_pipeline import StocksPipeline
    p = StocksPipeline(load_config())
    reached = {"update_data": False}
    monkeypatch.setattr(p, "update_data", lambda **k: reached.__setitem__("update_data", True))
    with pytest.raises(ValueError) as ei:
        p.run_report(mode="swing")
    assert "deprecated/removed" in str(ei.value)
    assert reached["update_data"] is False        # guard fired before any side effect


def test_pipeline_invest_blocked_before_side_effects(monkeypatch):
    from src.config import load_config
    from src.stocks.pipelines.stocks_pipeline import StocksPipeline
    p = StocksPipeline(load_config())
    reached = {"update_data": False}
    monkeypatch.setattr(p, "update_data", lambda **k: reached.__setitem__("update_data", True))
    with pytest.raises(ValueError) as ei:
        p.run_report(mode="invest")
    assert "deprecated/removed" in str(ei.value)
    assert reached["update_data"] is False


def test_pipeline_intraday_not_blocked_by_deprecation_guard(monkeypatch):
    """Intraday must PASS the guard and reach update_data (proven via a sentinel)."""
    from src.config import load_config
    from src.stocks.pipelines.stocks_pipeline import StocksPipeline

    class _Sentinel(Exception):
        pass

    p = StocksPipeline(load_config())

    def _boom(**k):
        raise _Sentinel()

    monkeypatch.setattr(p, "update_data", _boom)
    with pytest.raises(_Sentinel):
        p.run_report(mode="intraday")


# ----------------------------------------------------------------------------
# 8. Stricter missing-data gates — None (missing) rejects, not warns
# ----------------------------------------------------------------------------
def test_detector_rejects_missing_rs_and_regime():
    cfg = pf_config.load_config()
    df = _frame(260, 50, 0.2)          # valid daily; no spy_df → rs_spy None
    feats = pf_features.compute_features(df)   # rs_spy None, sector_df None
    # market regime data missing → reject (not caution)
    c = pf_detector.detect("TESTU", feats,
                           market_ctx={"label": "unknown", "spy_above_50d": None,
                                       "spy_above_200d": None, "vix": None},
                           sector_ctx={"sector": None, "sector_etf": None,
                                       "sector_above_50d": None, "sector_rs_positive": None},
                           cfg=cfg, equity_usd=5000)
    assert c["passed"] is False
    joined = " | ".join(c["rejection_reasons"])
    assert "regime data unavailable" in joined
    assert "RS vs SPY unavailable" in joined


# ----------------------------------------------------------------------------
# 9. Universe / sector-map completeness guard
# ----------------------------------------------------------------------------
def test_universe_and_sector_map_complete():
    from src.stocks.position_framework.config import (
        validate_universe, universe_symbols, sector_map, FETCHABLE_SECTOR_ETFS)
    assert validate_universe() == []
    syms, smap = universe_symbols(), sector_map()
    assert 50 <= len(syms) <= 75
    assert len(set(syms)) == len(syms)                      # no dupes
    assert all(s in smap for s in syms)                     # every symbol mapped
    assert set(smap.values()) <= FETCHABLE_SECTOR_ETFS      # only fetchable ETFs
    # cross-check against the collectors' actual sector ETF universe + SPY/QQQ/VIX availability
    from src.stocks.configs.loader import load_stocks_config
    sc = load_stocks_config()
    assert set(smap.values()) <= set(sc.sector_etfs.values())
    assert "SPY" in sc.indices and "QQQ" in sc.indices and sc.volatility_index


def test_validate_universe_flags_bad_config():
    from src.stocks.position_framework.config import validate_universe
    bad = {"universe": {"symbols": ["AAPL", "ZZZZ"]}, "sector_map": {"AAPL": "XLK", "ZZZZ": "NOPE"}}
    issues = validate_universe(bad)
    assert any("ZZZZ" in i and "non-fetchable" in i for i in issues)
    bad2 = {"universe": {"symbols": ["AAPL", "TSLA"]}, "sector_map": {"AAPL": "XLK"}}
    assert any("TSLA: missing from sector_map" in i for i in validate_universe(bad2))


# ----------------------------------------------------------------------------
# 10. Outcome engine (Phase 1, shadow, USD net) — realistic OHLC execution
# ----------------------------------------------------------------------------
def _bars(closes):
    idx = pd.date_range("2026-01-01", periods=len(closes), freq="D")
    close = np.array(closes, dtype=float)
    return pd.DataFrame({"open": close - 0.5, "high": close + 1.0, "low": close - 1.0,
                         "close": close, "volume": np.full(len(closes), 1e6)}, index=idx)


_EXEC = {"entry_valid_days": 5, "slippage_bps": 5, "commission_per_share": 0.0, "min_forward_bars": 2}


def test_outcome_engine_winner_hits_targets():
    from src.stocks.position_framework import outcome_engine as oe
    df = _bars([98, 100, 104, 108, 112, 116, 118, 120, 121, 122])
    plan = {"entry_price": 100, "stop_price": 95, "tp1": 110, "tp2": 115,
            "tp1_pct": 0.5, "tp2_pct": 0.25, "qty": 10, "max_holding_days": 8,
            "setup_variant": "breakout", "sector": "Technology", "symbol": "TESTU"}
    r = oe.simulate_trade(df, 1, plan, _EXEC)
    assert r["status"] == "closed"
    assert r["entry_px"] == 100.0
    assert r["net_usd"] > 0                                 # up-trend booked in USD net
    assert r["mfe_r"] > 0 and r["fees_usd"] is not None and r["slippage_usd"] > 0


def test_outcome_engine_loser_hits_stop():
    from src.stocks.position_framework import outcome_engine as oe
    df = _bars([99, 100, 97, 93, 92, 91])          # gaps/declines through the stop
    plan = {"entry_price": 100, "stop_price": 95, "tp1": 110, "tp2": 115,
            "qty": 10, "max_holding_days": 8, "setup_variant": "pullback_21d_50d",
            "sector": "Technology", "symbol": "TESTU"}
    r = oe.simulate_trade(df, 1, plan, _EXEC)
    assert r["status"] == "closed"
    assert r["exit_reason"] == "stop"
    assert r["net_usd"] < 0


def test_outcome_engine_no_entry_when_zone_never_crossed():
    from src.stocks.position_framework import outcome_engine as oe
    df = _bars([106, 107, 108, 109, 110, 111])     # never trades down to entry 100
    plan = {"entry_price": 100, "stop_price": 95, "tp1": 110, "qty": 10, "max_holding_days": 8}
    r = oe.simulate_trade(df, 0, plan, _EXEC)
    assert r["status"] == "no_entry"
    assert r["net_usd"] is None                    # no fabricated PnL


def test_outcome_engine_pending_when_insufficient_bars():
    from src.stocks.position_framework import outcome_engine as oe
    df = _bars([99, 100])                           # 1 forward bar < min_forward_bars
    plan = {"entry_price": 100, "stop_price": 95, "tp1": 110, "qty": 10}
    r = oe.simulate_trade(df, 1, plan, _EXEC)
    assert r["status"] == "pending"
    assert r["net_usd"] is None


def test_outcome_engine_finds_scan_date_in_string_index_with_dst_offsets():
    from src.stocks.position_framework import outcome_engine as oe
    df = _bars([98, 99, 100])
    df.index = ["2026-07-16 00:00:00-04:00", "2026-07-17 00:00:00-04:00",
                "2026-11-02 00:00:00-05:00"]
    # 01:04 UTC is still 21:04 on the July 16 US session.
    assert oe._start_idx_for(df, "2026-07-17T01:04:08+00:00") == 0
    assert oe._start_idx_for(df, "2026-07-17T14:00:00+00:00") == 1


def _ohlc(rows):
    """rows = list of (open, high, low, close). Explicit OHLC for gap scenarios."""
    idx = pd.date_range("2026-01-01", periods=len(rows), freq="D")
    df = pd.DataFrame(rows, columns=["open", "high", "low", "close"], index=idx)
    df["volume"] = 1e6
    return df


def test_outcome_engine_gap_up_through_entry_fills_at_open_not_no_entry():
    """Breakout buy-stop: bar gaps entirely above entry (low never touches it) → FILL at the open,
    not no_entry (the old bug)."""
    from src.stocks.position_framework import outcome_engine as oe
    # bar0 = history (below entry); bar1 gaps up above entry=100 (open 103, low 102 > 100)
    df = _ohlc([(98, 99, 97, 98), (103, 106, 102, 105), (106, 108, 104, 107), (108, 111, 107, 110),
                (110, 113, 109, 112), (112, 114, 111, 113)])
    plan = {"entry_price": 100, "stop_price": 95, "tp1": 110, "tp2": 115, "qty": 10,
            "max_holding_days": 8, "setup_variant": "breakout", "symbol": "GAPU"}
    r = oe.simulate_trade(df, 1, plan, _EXEC)
    assert r["status"] != "no_entry"
    assert r["entry_px"] == 103.0          # filled at the gap-up open, not 100


def test_outcome_engine_stop_exit_px_is_fill_not_bar_close():
    """Stop exit_px must be the actual stop (or gap-open), never the bar close."""
    from src.stocks.position_framework import outcome_engine as oe
    # entry fills at 100 on bar1; bar2 hits the stop with a normal (non-gap) bar: open 99 > stop 95
    df_norm = _ohlc([(99, 100, 98, 99), (99, 101, 99, 100), (99, 100, 94, 97)])
    plan = {"entry_price": 100, "stop_price": 95, "tp1": 120, "qty": 10, "max_holding_days": 8,
            "setup_variant": "pullback_21d_50d", "symbol": "STOPN"}
    r = oe.simulate_trade(df_norm, 1, plan, _EXEC)
    assert r["exit_reason"] == "stop"
    assert r["exit_px"] == 95.0            # the stop, NOT the bar close (97)
    # gap-down through the stop → exit at the OPEN, not the stop
    df_gap = _ohlc([(99, 100, 98, 99), (99, 101, 99, 100), (93, 94, 91, 92)])
    r2 = oe.simulate_trade(df_gap, 1, plan, _EXEC)
    assert r2["exit_reason"] == "stop"
    assert r2["exit_px"] == 93.0           # gap-open below the stop


def test_outcome_engine_terminal_flips_candidate_out_of_open(tmp_path):
    """A resolved (closed / no_entry) outcome must remove the candidate from the open list."""
    df = _frame(260, 50, 0.2); spy = _frame(260, 400, 0.01); sector = _frame(260, 100, 0.05)
    feats = pf_features.compute_features(df, spy_df=spy, sector_df=sector)
    cand = pf_detector.detect("TESTU", feats, market_ctx=_MKT_OK, sector_ctx=_SEC_OK,
                              cfg=pf_config.load_config(), equity_usd=5000)
    cand["status"] = "shadow_open"
    db = tmp_path / "consist.sqlite"
    pf_store.insert_candidates([cand], created_at="2026-07-02T12:00:00+00:00", db_path=db)
    cid = f"spf_TESTU_2026-07-02"
    assert len(pf_store.latest_candidates(only_open=True, db_path=db)) == 1
    # a terminal outcome alone excludes it (LEFT JOIN defence)
    pf_store.upsert_outcome(cid, checked_at="2026-07-10T00:00:00+00:00", status="closed",
                            fields={"net_pnl_usd": 12.3}, db_path=db)
    assert len(pf_store.latest_candidates(only_open=True, db_path=db)) == 0
    # and flipping the candidate status also excludes it
    pf_store.set_candidate_status(cid, "shadow_closed", db_path=db)
    assert len(pf_store.latest_candidates(only_open=True, db_path=db)) == 0
    assert len(pf_store.latest_candidates(only_open=False, db_path=db)) == 1   # still stored


def test_cli_position_report_windows_cp1252_safe():
    """`stocks-position-report` must exit 0 with a cp1252 (legacy Windows) stdout encoding —
    the full unicode Markdown goes to the FILE, stdout stays ASCII-safe."""
    import os
    import subprocess
    import sys
    env = dict(os.environ, PYTHONIOENCODING="cp1252", PYTHONUTF8="0")
    r = subprocess.run([sys.executable, "-m", "src.cli", "stocks-position-report", "--limit", "10"],
                       capture_output=True, env=env, timeout=240,
                       cwd=str(pf_config._ROOT))
    assert r.returncode == 0, (r.stdout[-400:], r.stderr[-400:])


def test_outcome_engine_aggregate_usd_net():
    from src.stocks.position_framework import outcome_engine as oe
    trades = [
        {"status": "closed", "net_usd": 30.0, "exit_date": "2026-01-05", "sector": "Tech", "setup_type": "breakout"},
        {"status": "closed", "net_usd": -10.0, "exit_date": "2026-01-06", "sector": "Fin", "setup_type": "pullback_21d_50d"},
        {"status": "closed", "net_usd": 20.0, "exit_date": "2026-01-07", "sector": "Tech", "setup_type": "breakout"},
        {"status": "pending", "net_usd": None}, {"status": "no_entry", "net_usd": None},
    ]
    a = oe.aggregate(trades)
    assert a["closed_trades"] == 3 and a["pending"] == 1 and a["no_entry"] == 1
    assert a["total_net_usd"] == 40.0
    assert a["winrate"] == round(2 / 3, 4)
    assert a["profit_factor"] == round(50.0 / 10.0, 3)
    assert a["max_drawdown_usd"] <= 0
    assert a["by_sector"]["Tech"]["net_usd"] == 50.0 and a["by_setup"]["breakout"]["n"] == 2
