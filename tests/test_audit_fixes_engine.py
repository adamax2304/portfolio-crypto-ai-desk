"""Audit-fix engine tests (paper/read-model only; final_r untouched; no live).
#6 look-ahead-safe overlay candles, #8 DATA_GAP_LATE excluded from forward edge, #9 stop sanity flag."""
from __future__ import annotations

import sqlite3

import pandas as pd
import pytest


# ---- #6: overlay context candles are filtered to timestamp <= created_at ----
def test_candles_for_excludes_future_bars(monkeypatch):
    from src.execution import signal_paper_tp as sp

    df = pd.DataFrame({
        "timestamp": pd.to_datetime(
            ["2026-06-01T00:00:00Z", "2026-06-02T00:00:00Z",  # before created_at
             "2026-06-03T00:00:00Z", "2026-06-04T00:00:00Z"], utc=True),  # AFTER created_at
        "open": [1, 2, 3, 4], "high": [1, 2, 3, 4], "low": [1, 2, 3, 4], "close": [1, 2, 3, 4],
    })
    monkeypatch.setattr("src.signals.tracker._load_ohlcv_for_signal",
                        lambda *a, **k: (df.copy(), "binance", "5m"))
    out = sp._candles_for(None, None, "BTC/USDT", "intraday", "crypto", "",
                          created_at="2026-06-02T12:00:00Z")
    # only the 2 pre-created_at bars survive; the 2 future bars are dropped (no look-ahead)
    assert out is not None and len(out) == 2
    # without a cutoff the old behaviour (all bars) is preserved
    allbars = sp._candles_for(None, None, "BTC/USDT", "intraday", "crypto", "", created_at=None)
    assert len(allbars) == 4


# ---- #9: absurd stop-after-TP R is flagged for review ----
def test_stop_plan_sanity_flag(monkeypatch):
    from src.execution import signal_stop_plan as ssp

    class _M:
        def __init__(self, r):
            self.new_stop = 100.0
            self.protection_r = r
            self.structure_used = "higher_low"

    # absurd 25R protection → sanity_review=1
    monkeypatch.setattr(ssp, "_candles_for", lambda *a, **k: [{"open": 1, "high": 1, "low": 1, "close": 1}])
    monkeypatch.setattr(ssp, "structural_stop_after_tp", lambda **k: _M(25.0))
    rec = ssp.compute_record({"signal_id": "x", "symbol": "AAA", "entry": 100, "stop": 99,
                              "direction": "long"}, {"mode": "intraday"}, None, None)
    assert rec["sanity_review"] == 1 and "REVIEW" in rec["reason"]

    monkeypatch.setattr(ssp, "structural_stop_after_tp", lambda **k: _M(2.0))
    rec2 = ssp.compute_record({"signal_id": "y", "symbol": "AAA", "entry": 100, "stop": 99,
                               "direction": "long"}, {"mode": "intraday"}, None, None)
    assert rec2["sanity_review"] == 0


# ---- #8: DATA_GAP_LATE cohort excluded from forward edge metrics ----
def _mk_shadow_db(path: str):
    c = sqlite3.connect(path)
    c.execute("""CREATE TABLE paper_shadow_execution_outcomes (
        signal_id TEXT, branch TEXT, window TEXT, entry_fill_status TEXT, entry_fill_time TEXT,
        net_r REAL, gross_r REAL, net_pnl_usdt REAL, fees_usdt REAL, entry_order_type TEXT,
        close_reason TEXT, outcome_status TEXT, direction_changed INTEGER,
        maker_entry_posted INTEGER, maker_entry_filled INTEGER, maker_entry_missed INTEGER,
        taker_fallback_used INTEGER)""")
    c.execute("CREATE TABLE paper_shadow_meta (k TEXT, v TEXT)")
    c.execute("INSERT INTO paper_shadow_meta VALUES ('activated_at','2026-06-25T00:00:00+00:00')")
    c.execute("CREATE TABLE entry_latency_audit (signal_id TEXT, cause TEXT)")
    # clean signal (both branches) + a DATA_GAP_LATE dirty one
    def ins(sid, br, r):
        c.execute("INSERT INTO paper_shadow_execution_outcomes (signal_id,branch,window,"
                  "entry_fill_status,net_r,gross_r,net_pnl_usdt,fees_usdt) VALUES (?,?,?,?,?,?,?,?)",
                  (sid, br, "forward_since_activation", "filled", r, r, r * 100, 1.0))
    ins("clean", "old_paper", -1.0); ins("clean", "new_logic_shadow", 1.0)
    ins("dirty", "old_paper", -5.0); ins("dirty", "new_logic_shadow", 5.0)
    c.execute("INSERT INTO entry_latency_audit VALUES ('dirty','DATA_GAP_LATE')")
    c.commit(); c.close()


def test_forward_quality_excludes_data_gap_late(tmp_path):
    from src.execution.paper_shadow_monitor import forward_quality
    db = str(tmp_path / "s.sqlite"); _mk_shadow_db(db)
    fq = forward_quality(db)
    assert fq["available"]
    assert fq["data_gap_late_excluded_signals"] == 1
    assert fq["forward_signals"] == 1 and fq["forward_signals_total"] == 2
    # the dirty +5R B trade is excluded → clean B net_r is the +1.0 only, not +6.0
    assert fq["B"]["net_r"] == pytest.approx(1.0)


# ---- #3-compute: stocks priced with the equity/ETF model, NOT the crypto-perp profile ----
def _trade(sid, sym, asset, mode, entry, stop, per):
    return {"signal_id": sid, "economic_trade_key": sid, "symbol": sym, "asset_class": asset,
            "mode": mode, "direction": "long", "entry": entry, "stop": stop,
            "paper_execution_r": per, "close_reason": "tp_win", "stop_current_r": 0.0,
            "entry_at": "2026-06-30T00:00:00Z"}


def test_stocks_use_stock_profile_not_crypto_perp():
    from src.execution.paper_portfolio import simulate_portfolio
    run = simulate_portfolio(
        [_trade("s1", "AAPL", "stocks", "intraday", 100.0, 99.0, 1.0),
         _trade("c1", "BTC/USDT", "crypto", "intraday", 100.0, 99.0, 1.0)],
        fee_profile="bybit_non_vip_usdt_perp")
    led = {r["signal_id"]: r for r in run["ledger"]}
    # same notional/geometry → the stock's exchange fee must be MUCH lower than the crypto-perp one
    assert led["s1"]["fees_usdt"] < led["c1"]["fees_usdt"]
    assert "equity" in led["s1"]["fee_source"].lower() or "etf" in led["s1"]["fee_source"].lower()
    assert "perp" in led["c1"]["fee_source"].lower() or "bybit" in led["c1"]["fee_source"].lower()


# ---- #10: crypto perps carry an (approximate) funding cost; stocks carry none ----
def test_funding_applied_to_crypto_not_stocks():
    from src.execution.paper_portfolio import simulate_portfolio
    run = simulate_portfolio(
        [_trade("s1", "AAPL", "stocks", "intraday", 100.0, 99.0, 1.0),
         _trade("c1", "BTC/USDT", "crypto", "intraday", 100.0, 99.0, 1.0)],
        fee_profile="bybit_non_vip_usdt_perp")
    led = {r["signal_id"]: r for r in run["ledger"]}
    assert led["c1"]["funding_usdt"] > 0        # crypto intraday crosses a funding interval
    assert led["s1"]["funding_usdt"] == 0        # equities have no perp funding
    assert run["summary"]["total_funding_usdt"] > 0


# ---- #4: slice-aware exit — TP partials fill maker (cheaper), stop/expiry taker ----
def test_trade_costs_exit_slices_blended():
    from src.execution.fees import trade_costs
    kw = dict(notional_usdt=1000, exit_notional_usdt=1000, symbol="BTC/USDT",
              fee_profile="bybit_non_vip_usdt_perp")
    taker = trade_costs(**kw)
    maker = trade_costs(**kw, exit_slices=[(1.0, "maker")])
    blended = trade_costs(**kw, exit_slices=[(0.5, "maker"), (0.5, "taker")])
    assert maker.close_fee_usdt < blended.close_fee_usdt < taker.close_fee_usdt


def test_portfolio_exit_maker_fraction():
    from src.execution.paper_portfolio import simulate_portfolio
    win = _trade("w", "BTC/USDT", "crypto", "intraday", 100.0, 99.0, 3.0)
    win.update({"tp1_hit": 1, "tp2_hit": 1, "tp3_hit": 1, "close_reason": "tp3_runner"})
    lose = _trade("l", "BTC/USDT", "crypto", "intraday", 100.0, 99.0, -1.0)
    lose.update({"tp1_hit": 0, "tp2_hit": 0, "tp3_hit": 0, "close_reason": "original_stop"})
    led = {r["signal_id"]: r for r in
           simulate_portfolio([win, lose], fee_profile="bybit_non_vip_usdt_perp")["ledger"]}
    assert led["w"]["exit_maker_fraction"] == pytest.approx(1.0)   # all TPs hit → full maker exit
    assert led["l"]["exit_maker_fraction"] == 0.0                  # stopped → full taker exit


# ---- #7: maker limit fills only on TRADE-THROUGH, not a mere touch ----
def test_maker_fill_requires_trade_through():
    from src.execution.paper_shadow_engine import _entry_fill
    kw = dict(long=True, entry_low=99.0, entry_high=100.0, entry_trigger=None,
              suggested=None, is_first=False)
    # bar that only kisses the top edge (low == z_hi) → post-only MISS
    price, ot, _at_open = _entry_fill("PULLBACK_LIMIT", {"high": 101, "low": 100.0, "open": 101, "close": 101}, **kw)
    assert price is None
    # bar that trades THROUGH the buy limit → maker fill
    price, ot, _at_open = _entry_fill("PULLBACK_LIMIT", {"high": 101, "low": 99.9, "open": 101, "close": 100.5}, **kw)
    assert price == 100.0 and ot == "maker"
    # opened inside the zone → fills at open (maker)
    price, ot, _at_open = _entry_fill("PULLBACK_LIMIT", {"high": 101, "low": 98, "open": 99.5, "close": 100}, **kw)
    assert price == 99.5 and ot == "maker"


# ---- RE-AUDIT #1: entry_mode_classifier.compute_record is look-ahead-safe ----
def test_entry_mode_compute_record_excludes_future_bars(monkeypatch):
    from src.execution import entry_mode_classifier as emc

    df = pd.DataFrame({
        "timestamp": pd.to_datetime(
            ["2026-06-01T00:00:00Z", "2026-06-02T00:00:00Z",     # at/before created_at
             "2026-06-03T00:00:00Z", "2026-06-04T00:00:00Z"], utc=True),  # AFTER created_at
        "open": [10, 11, 12, 13], "high": [10, 11, 20, 21],
        "low": [9, 10, 11, 12], "close": [10, 11, 19, 20]})
    monkeypatch.setattr("src.signals.tracker._load_ohlcv_for_signal",
                        lambda *a, **k: (df.copy(), "binance", "5m"))
    trade = {"signal_id": "e1", "symbol": "BTC/USDT", "direction": "long", "asset_class": "crypto",
             "entry": 11.0, "stop": 10.0, "entry_low": 10.5, "entry_high": 11.0,
             "created_at": "2026-06-02T12:00:00Z"}
    rec = emc.compute_record(trade, {"mode": "intraday", "exchange_focus": ""}, None, None)
    # only the 2 bars at/before created_at may inform the label — the 2 future breakout bars must
    # be invisible; if they leaked in, candles_used would be 4 (backfill seeing the future).
    assert rec["candles_used"] == 2
    trade2 = dict(trade); trade2["created_at"] = None
    rec2 = emc.compute_record(trade2, {"mode": "intraday", "exchange_focus": ""}, None, None)
    assert rec2["candles_used"] == 4     # guards against the cutoff silently no-op'ing


# ---- RE-AUDIT #2: B-book prices stocks with the equity/ETF model, NOT the Bybit perp ----
def test_b_book_stocks_not_bybit_perp_fee_source():
    from src.execution.paper_portfolio import load_cfg
    from scripts.structural_maker_backfill import simulate_b
    cfg = load_cfg()
    trades = [
        {"signal_id": "s1", "economic_trade_key": "s1", "symbol": "AAPL", "asset_class": "stocks",
         "mode": "intraday", "direction": "long", "entry": 100.0, "stop": 99.0, "tp1": 101.0,
         "paper_execution_r": 1.0, "close_reason": "tp_win", "stop_current_r": 0.0,
         "entry_at": "2026-06-30T00:00:00Z", "playbook": "stocks_swing_watchlist_rs_rotation", "regime": ""},
        {"signal_id": "c1", "economic_trade_key": "c1", "symbol": "BTC/USDT", "asset_class": "crypto",
         "mode": "intraday", "direction": "long", "entry": 100.0, "stop": 99.0, "tp1": 101.0,
         "paper_execution_r": 1.0, "close_reason": "tp_win", "stop_current_r": 0.0,
         "entry_at": "2026-06-30T00:00:00Z", "playbook": "crypto_swing_narrative_rs_momentum", "regime": ""},
    ]
    led = {r["signal_id"]: r for r in
           simulate_b(trades, cfg, "bybit_non_vip_usdt_perp", "2026-07-02T00:00:00Z")["ledger"]}
    assert "s1" in led and "c1" in led
    s_src = (led["s1"]["fee_source"] or "").lower()
    # stock priced with the equity/ETF model, NOT Bybit. (Do NOT assert "perp" absence — the stock
    # source-note literally reads "NOT a crypto-perp profile".)
    assert "bybit" not in s_src and ("equity" in s_src or "etf" in s_src)
    assert led["s1"]["fee_source"] != led["c1"]["fee_source"]
    assert led["s1"]["funding_usdt"] == 0                    # equities: no perp funding
    c_src = (led["c1"]["fee_source"] or "").lower()
    assert "bybit" in c_src or "perp" in c_src                # crypto still a perp


# ---- RE-AUDIT #9: cohort allocator read-model weights (paper-only; not live) ----
def test_cohort_allocator_weights():
    from src.execution.cohort_allocator import allocate
    # crypto swing pullback → full candidate weight
    a = allocate("crypto", "swing", "long", setup_type="crypto_swing_narrative_rs_momentum")
    assert a.weight == 1.0 and a.status == "candidate"
    # crypto intraday short breakdown → half weight
    b = allocate("crypto", "intraday", "short", setup_type="failed_bounce_breakdown")
    assert b.weight == 0.5 and b.status == "candidate_reduced"
    # crypto intraday long pullback → disabled
    c = allocate("crypto", "intraday", "long", setup_type="pullback_limit")
    assert c.weight == 0.0 and c.status == "disabled"
    # stocks intraday long continuation → disabled
    d = allocate("stocks", "intraday", "long", setup_type="momentum_continuation")
    assert d.weight == 0.0 and d.status == "disabled"
    # crypto scalp → shadow only
    e = allocate("crypto", "scalp", "long", setup_type="whatever")
    assert e.weight == 0.0 and e.status == "shadow_only"
    # stocks short continuation → research/shadow
    f = allocate("stocks", "swing", "short", setup_type="short_continuation")
    assert f.weight == 0.0 and f.status == "research_shadow"


# ---- LEGACY-R PURGE: an actual TP2 R of 1.6667 must NOT be booked as a nominal 2R ----
def test_paper_execution_keeps_tp2_runner_open():
    from src.execution.paper_execution_accounting import compute_paper_execution
    # entry 100, stop 98.5 → risk 1.5; tp2 = 102.5 → +1.6667R (NOT a rounded 2R)
    rec = compute_paper_execution(
        direction="long", entry=100.0, stop=98.5, tp1=101.5, tp2=102.5, tp3=104.5,
        reached_tp1=True, reached_tp2=True, reached_tp3=False, hit_stop=False,
        expired=False, entered=True, mfe_r=2.0)
    assert rec["paper_execution_r"] is None
    assert rec["paper_execution_outcome"] == "open"
    assert rec["paper_execution_r"] != 2.0


def test_analytics_excludes_open_tp2_runner_from_realized_r():
    """A TP2 milestone remains open under Model F and is not realized as legacy +2R."""
    from src.signals.analytics import _paper_execution_r
    signal = {"direction": "long", "entry_low": 100.0, "invalidation": 98.5,
              "tp1": 101.5, "tp2": 102.5, "tp3": 104.5}
    outcome = {"tp1_hit": 1, "tp2_hit": 1, "tp3_hit": 0, "stop_hit": 0,
               "final_outcome": "win", "max_favorable_excursion_r": 2.0, "final_r": 2.0}
    pe = _paper_execution_r(signal, outcome, triggered=True)
    assert pe is None
    assert pe != 2.0
