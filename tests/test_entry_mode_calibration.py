"""Entry-mode calibration + profit-protection + parameter-sweep + pre-entry classifier tests.

Covers: slice aggregation, paired old/new, forward-vs-backfill separation, verdict thresholds,
DATA_GAP_LATE blocking, USD-as-primary, policy matrix/integrity, per-entry-mode profit protection,
pre-entry lookahead safety, parameter-sweep read-only, and the hard read-only guardrails
(no writes to proposed_signals / signal_outcomes / final_r; no live/order surface).
"""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import pytest

from src.execution import entry_mode_calibration as cal
from src.execution import profit_protection as pp
from src.execution.profit_protection import WalkResult

ROOT = Path(__file__).resolve().parents[1]


# ============================ profit protection ============================

def _prot(mfe, hit_stop=False, expired=False, t1=False, t2=False, t3=False, em=None, amb=False):
    wr = WalkResult(entered=True, entry_price=100.0, mfe_r=mfe, hit_stop=hit_stop, expired=expired,
                    reached_tp1=t1, reached_tp2=t2, reached_tp3=t3, same_candle_ambiguous=amb)
    return pp.protect(direction="long", entry=100.0, stop=98.0, tp1=104.0, tp2=106.0, tp3=110.0,
                      walk_result=wr, symbol="ETH/USDT", fee_profile="bybit_non_vip_usdt_perp", entry_mode=em)


def test_protection_06R_reverse_not_full_loss():
    r = _prot(mfe=0.7, hit_stop=True)
    assert r.close_reason == "breakeven_stop" and r.net_r == 0.0 and r.protection_armed and r.giveback


def test_protection_10R_reverse_locks_half():
    r = _prot(mfe=1.3, hit_stop=True)
    assert r.close_reason == "profit_lock_stop" and r.net_r == 0.5 and r.lock_armed


def test_protection_no_excursion_full_stop():
    r = _prot(mfe=0.3, hit_stop=True)
    assert r.close_reason == "original_stop" and r.net_r == -1.0


def test_protection_expired_after_entry_closes_at_protected_level():
    r = _prot(mfe=0.8, expired=True)   # armed BE, expired -> 0R (not open, not -1)
    assert r.close_reason == "breakeven_stop" and r.net_r == 0.0
    r2 = _prot(mfe=1.5, expired=True)  # locked, expired -> +0.5R
    assert r2.close_reason == "profit_lock_stop" and r2.net_r == 0.5


def test_protection_tp3_runner():
    r = _prot(mfe=5.0, t1=True, t2=True, t3=True)
    assert r.tp3_runner and r.close_reason == "tp3_runner" and r.net_r and r.net_r > 3


def test_no_chase_skip_has_no_pnl():
    r = _prot(mfe=1.0, t1=True, em="NO_CHASE_SKIP")
    assert r.skipped and r.net_r is None and r.net_usd is None


def test_protection_reports_realistic_net_usd_and_delta():
    r = _prot(mfe=0.7, hit_stop=True)
    assert r.net_usd is not None and r.net_usd < 0            # fees make a 0R exit slightly negative USD
    assert r.risk_usd == 25.0
    assert r.delta_vs_no_protection_r == 1.0                  # 0R protected vs -1R no-protection
    assert r.delta_vs_no_protection_usd == 25.0
    assert r.protection_model == "early_mfe_protection_v1"


def test_same_candle_ambiguous_below_arm_is_full_loss():
    r = _prot(mfe=0.4, hit_stop=True, t1=True, amb=True)      # ambiguous, MFE<0.6 -> -1R conservative
    assert r.net_r == -1.0


def test_all_entry_modes_use_protection_in_sim():
    # a candle path that goes +0.7R then reverses to the original stop for every entry mode
    candles = [{"open": 100, "high": 100, "low": 100, "close": 100},
               {"open": 100, "high": 101.4, "low": 100, "close": 101.4},   # +0.7R (risk=2)
               {"open": 101, "high": 101, "low": 97.9, "close": 98}]        # reverse to stop 98
    for em in ("PULLBACK_LIMIT", "STRUCTURAL_RETEST", "BREAKOUT_CONTINUATION",
               "MOMENTUM_TAKER_NOW", "LIMIT_THEN_TAKER_TIMEOUT"):
        res = pp.simulate_from_geometry(direction="long", entry_low=99.5, entry_high=100.5,
                                        entry_trigger=100.0, stop=98.0, tp1=104, tp2=106, tp3=110,
                                        candles=candles, entry_mode=em, symbol="X/USDT")
        assert res.entered, em
        # protection armed at +0.7R -> reversal ends at breakeven, NOT -1R
        assert res.close_reason == "breakeven_stop" and res.net_r == 0.0, (em, res.close_reason, res.net_r)


# ============================ verdict thresholds ============================

def _cfg():
    return cal.load_calibration_config()


def _metrics(closed=50, pf=1.4, net_usd=300.0, dgl=0.0, max_dd_r=3.0, max_dd_usd=100.0):
    return {"closed": closed, "profit_factor": pf, "net_pnl_usd": net_usd,
            "data_gap_late_share": dgl, "max_drawdown_r": max_dd_r, "max_drawdown_usd": max_dd_usd}


def test_verdict_insufficient_clean_sample():
    # too few CLEAN closed trades → blocks any good/bad conclusion (was NEED_MORE_DATA; the sample
    # gate is now clean-based and can never read as KEEP/PROMOTE/DISABLE).
    v, _ = cal.slice_verdict(asset_class="crypto", mode="intraday", entry_mode="STRUCTURAL_RETEST",
                             window=cal.FORWARD, metrics=_metrics(closed=10), paired_delta_usd=100,
                             old_max_dd_usd=200, cfg=_cfg())
    assert v == "INSUFFICIENT_CLEAN_SAMPLE"


def test_verdict_data_quality_blocked():
    v, _ = cal.slice_verdict(asset_class="crypto", mode="intraday", entry_mode="STRUCTURAL_RETEST",
                             window=cal.FORWARD, metrics=_metrics(dgl=0.5), paired_delta_usd=100,
                             old_max_dd_usd=200, cfg=_cfg())
    assert v == "DATA_QUALITY_BLOCKED"


def test_verdict_disable_on_negative_usd_even_if_r_ok():
    # USD authoritative: PF>1 but net USD <= 0 -> DISABLE
    v, _ = cal.slice_verdict(asset_class="crypto", mode="intraday", entry_mode="STRUCTURAL_RETEST",
                             window=cal.FORWARD, metrics=_metrics(pf=1.4, net_usd=-10.0),
                             paired_delta_usd=100, old_max_dd_usd=200, cfg=_cfg())
    assert v == "DISABLE"


def test_verdict_paper_candidate_and_promote_review():
    cand, _ = cal.slice_verdict(asset_class="crypto", mode="intraday", entry_mode="STRUCTURAL_RETEST",
                                window=cal.FORWARD, metrics=_metrics(closed=50, pf=1.30, net_usd=200),
                                paired_delta_usd=100, old_max_dd_usd=500, cfg=_cfg())
    assert cand == "PAPER_CANDIDATE"
    prom, _ = cal.slice_verdict(asset_class="crypto", mode="intraday", entry_mode="STRUCTURAL_RETEST",
                                window=cal.FORWARD, metrics=_metrics(closed=120, pf=1.5, net_usd=800,
                                                                     max_dd_usd=100),
                                paired_delta_usd=300, old_max_dd_usd=500, cfg=_cfg())
    assert prom == "PROMOTE_REVIEW"


def test_verdict_promote_blocked_if_drawdown_worse_than_old():
    v, _ = cal.slice_verdict(asset_class="crypto", mode="intraday", entry_mode="STRUCTURAL_RETEST",
                             window=cal.FORWARD, metrics=_metrics(closed=120, pf=1.5, net_usd=800,
                                                                  max_dd_usd=900),
                             paired_delta_usd=300, old_max_dd_usd=200, cfg=_cfg())
    assert v == "PAPER_CANDIDATE"   # falls back — DD worse than old blocks PROMOTE_REVIEW


def test_verdict_backfill_never_promotable():
    v, _ = cal.slice_verdict(asset_class="crypto", mode="intraday", entry_mode="STRUCTURAL_RETEST",
                             window=cal.BACKFILL, metrics=_metrics(closed=200, pf=2.0, net_usd=2000),
                             paired_delta_usd=999, old_max_dd_usd=999, cfg=_cfg())
    assert v == "KEEP_SHADOW"       # hypothesis-only — never PROMOTE/CANDIDATE


def test_verdict_legacy_stocks_swing_invest_unsupported():
    for m in ("swing", "invest"):
        v, r = cal.slice_verdict(asset_class="stocks", mode=m, entry_mode="PULLBACK_LIMIT",
                                 window=cal.FORWARD, metrics=_metrics(closed=50, pf=3.0, net_usd=5000),
                                 paired_delta_usd=999, old_max_dd_usd=999, cfg=_cfg())
        assert v == "UNSUPPORTED_LEGACY" and r    # never promotable regardless of PF/net
    # crypto swing is NOT legacy
    v2, _ = cal.slice_verdict(asset_class="crypto", mode="swing", entry_mode="PULLBACK_LIMIT",
                              window=cal.FORWARD, metrics=_metrics(closed=50, pf=1.4, net_usd=300),
                              paired_delta_usd=100, old_max_dd_usd=500, cfg=_cfg())
    assert v2 != "UNSUPPORTED_LEGACY"
    v3, _ = cal.slice_verdict(asset_class="stocks", mode="swing", entry_mode="EVENT_RS_PULLBACK",
                              window=cal.FORWARD, metrics=_metrics(closed=5, pf=1.4, net_usd=300),
                              paired_delta_usd=100, old_max_dd_usd=500, cfg=_cfg())
    assert v3 != "UNSUPPORTED_LEGACY"


def test_verdict_no_chase_skip_is_skip_policy():
    v, r = cal.slice_verdict(asset_class="crypto", mode="intraday", entry_mode="NO_CHASE_SKIP",
                             window=cal.FORWARD, metrics=_metrics(closed=50, pf=3.0, net_usd=9999),
                             paired_delta_usd=999, old_max_dd_usd=999, cfg=_cfg())
    assert v == "SKIP_POLICY" and r


def test_data_quality_gate_runs_before_min_trades():
    # thin (below min) AND gappy -> must be DATA_QUALITY_BLOCKED, not NEED_MORE_DATA
    v, r = cal.slice_verdict(asset_class="crypto", mode="intraday", entry_mode="STRUCTURAL_RETEST",
                             window=cal.FORWARD, metrics=_metrics(closed=5, dgl=0.6, net_usd=300),
                             paired_delta_usd=100, old_max_dd_usd=200, cfg=_cfg())
    assert v == "DATA_QUALITY_BLOCKED"


def test_temp_db_refresh_does_not_touch_production_diagnostics(tmp_path):
    prod = ROOT / "data" / "diagnostics" / "entry_mode_calibration.json"
    before = prod.read_bytes() if prod.exists() else None
    p = str(tmp_path / "cal.sqlite")
    _seed(p)
    cal.refresh(db=p, persist=True)              # custom db -> must NOT write global artifacts
    after = prod.read_bytes() if prod.exists() else None
    assert after == before


def test_verdict_disabled_by_policy_crypto_scalp():
    v, r = cal.slice_verdict(asset_class="crypto", mode="scalp", entry_mode="PULLBACK_LIMIT",
                             window=cal.FORWARD, metrics=_metrics(pf=3.0, net_usd=5000),
                             paired_delta_usd=999, old_max_dd_usd=999, cfg=_cfg())
    assert v == "DISABLED_BY_POLICY" and r


# ============================ policy matrix / integrity ============================

def test_policy_forbids_disabled_modes_from_promoted_paper():
    from src.execution.paper_entry_mode_policy import disabled_shadow_reason, paper_promotion_reason
    forbidden = [
        ("crypto", "scalp", "PULLBACK_LIMIT"),
        ("crypto", "intraday", "PULLBACK_LIMIT"),
        ("crypto", "intraday", "LIMIT_THEN_TAKER_TIMEOUT"),
        ("stocks", "intraday", "MOMENTUM_TAKER_NOW"),
        ("stocks", "intraday", "LIMIT_THEN_TAKER_TIMEOUT"),
    ]
    for ac, m, em in forbidden:
        assert disabled_shadow_reason(asset_class=ac, trade_mode=m, entry_mode=em), (ac, m, em)
        # a disabled combo must NOT simultaneously be promoted-to-paper
        assert not (disabled_shadow_reason(asset_class=ac, trade_mode=m, entry_mode=em)
                    and paper_promotion_reason(asset_class=ac, trade_mode=m, entry_mode=em)), (ac, m, em)


# ============================ seeded DB: aggregation / paired / guardrails ============================

def _seed(path, *, window="forward_since_activation", dgl_share=0.0, add_protection=True):
    c = sqlite3.connect(path)
    c.execute("CREATE TABLE proposed_signals (signal_id TEXT, symbol TEXT, direction TEXT, mode TEXT, "
              "asset_class TEXT, exchange_focus TEXT, market_regime TEXT, news_supported INTEGER, "
              "entry_low REAL, entry_high REAL, entry_trigger REAL, suggested_entry REAL, stop_loss REAL, "
              "tp1 REAL, tp2 REAL, tp3 REAL, created_at TEXT)")
    c.execute("CREATE TABLE signal_outcomes (signal_id TEXT, final_r REAL, entry_triggered INTEGER)")
    c.execute("""CREATE TABLE paper_shadow_execution_outcomes (
      signal_id TEXT, branch TEXT, window TEXT, entry_mode TEXT, asset_class TEXT, playbook TEXT,
      entry_fill_status TEXT, skipped_shadow_reason TEXT, net_r REAL, net_pnl_usdt REAL, gross_r REAL,
      fees_usdt REAL, slippage_usdt REAL, mfe_r REAL, mae_r REAL, missed_move_r REAL, tp1_r REAL,
      close_reason TEXT, outcome_status TEXT, maker_entry_posted INT, maker_entry_filled INT,
      maker_entry_missed INT, taker_fallback_used INT, maker_tp_fills INT, cost_model_status TEXT,
      entry_fill_time TEXT, fee_profile TEXT, created_at TEXT)""")
    c.execute("CREATE TABLE paper_shadow_meta (k TEXT PRIMARY KEY, v TEXT)")
    c.execute("INSERT INTO paper_shadow_meta VALUES ('activated_at','2026-06-01T00:00:00+00:00')")
    c.execute("CREATE TABLE signal_entry_mode (signal_id TEXT PRIMARY KEY, entry_mode TEXT)")
    c.execute("CREATE TABLE entry_latency_audit (signal_id TEXT PRIMARY KEY, cause TEXT, recorded_latency_min REAL)")
    if add_protection:
        c.execute("CREATE TABLE paper_execution_outcomes (signal_id TEXT, touch_r REAL, paper_execution_r REAL, "
                  "protection_armed INT, lock_armed INT, giveback INT, close_reason TEXT, "
                  "highest_tp_touched INT, same_candle_ambiguous INT, risk_model TEXT)")
    n = 40
    for i in range(n):
        sid = f"s{i}"
        c.execute("INSERT INTO proposed_signals VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                  (sid, "AAA", "long", "intraday", "stocks", "", "bull", 0, 99.5, 100.5, 100.0, 100.0, 98.0,
                   104, 106, 110, "2026-06-05T12:00:00+00:00"))
        c.execute("INSERT INTO signal_outcomes VALUES (?,?,?)", (sid, 0.5, 1))
        c.execute("INSERT INTO signal_entry_mode VALUES (?,?)", (sid, "BREAKOUT_CONTINUATION"))
        if i < int(n * dgl_share):
            c.execute("INSERT INTO entry_latency_audit VALUES (?,?,?)", (sid, "DATA_GAP_LATE", 900.0))
        else:
            c.execute("INSERT INTO entry_latency_audit VALUES (?,?,?)", (sid, "OK", 5.0))
        nnet, onet = (30.0 if i % 3 else -25.0), (-25.0 if i % 3 else 10.0)
        for br, net in (("new_logic_shadow", nnet), ("old_paper", onet)):
            c.execute("INSERT INTO paper_shadow_execution_outcomes VALUES "
                      "(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                      (sid, br, window, "BREAKOUT_CONTINUATION", "stocks", "breakout", "filled", None,
                       net / 25, net, net / 25, 1.0, 0.5, 1.2 if net > 0 else 0.4, -0.5, None, 1.5,
                       "closed_win" if net > 0 else "stopped_full", "closed", 1, 1, 0, 0,
                       2 if net > 0 else 0, "current", "2026-06-05T12:30:00+00:00",
                       "stock_etf_default", "2026-06-05T12:00:00+00:00"))
        if add_protection:
            c.execute("INSERT INTO paper_execution_outcomes VALUES (?,?,?,?,?,?,?,?,?,?)",
                      (sid, 1.2 if i % 3 else -1.0, 0.5 if i % 3 else 0.0, 1, 1 if i % 3 else 0, 1,
                       "profit_lock_stop" if i % 3 else "breakeven_stop", 0, 0, "early_mfe_protection_v1"))
    c.commit()
    c.close()


def test_calibration_aggregation_and_paired(tmp_path):
    p = str(tmp_path / "cal.sqlite")
    _seed(p)
    res = cal.refresh(db=p, persist=True)
    new = [s for s in res["slices"] if s["branch"] == cal.BRANCH_NEW]
    assert len(new) == 1
    s = new[0]
    assert s["closed"] == 40 and s["profit_factor"] and s["profit_factor"] > 1.15
    assert s["net_pnl_usd"] > 0 and s["verdict"] == "PAPER_CANDIDATE"
    assert s["protection_model"] == "early_mfe_protection_v1"
    assert s["giveback_rate"] is not None
    pr = res["paired"][0]
    assert pr["executed_common"] == 40 and pr["new_better_count"] + pr["old_better_count"] + pr["flat_count"] == 40
    assert "with_skips_common" in pr and "avoided_bad_count" in pr and "missed_good_count" in pr


def test_protection_coverage_uses_only_clean_closed_slice_rows(tmp_path):
    p = str(tmp_path / "coverage.sqlite")
    _seed(p)
    c = sqlite3.connect(p)
    c.execute("UPDATE paper_shadow_execution_outcomes SET entry_fill_status='skipped', net_pnl_usdt=NULL, "
              "outcome_status='skipped' WHERE signal_id='s0' AND branch='new_logic_shadow'")
    c.commit(); c.close()
    res = cal.refresh(db=p, persist=False)
    s = [x for x in res["slices"] if x["branch"] == cal.BRANCH_NEW][0]
    assert s["closed"] == 39
    assert s["protection_trades"] == 39
    assert s["protection_coverage"] == 1.0


def test_data_gap_late_blocks_verdict(tmp_path):
    p = str(tmp_path / "dgl.sqlite")
    _seed(p, dgl_share=0.5)
    res = cal.refresh(db=p, persist=True)
    s = [x for x in res["slices"] if x["branch"] == cal.BRANCH_NEW][0]
    assert s["data_gap_late_share"] >= 0.5 and s["verdict"] == "DATA_QUALITY_BLOCKED"


def test_backfill_reported_separately(tmp_path):
    p = str(tmp_path / "bf.sqlite")
    _seed(p, window="historical_backfill")
    res = cal.refresh(db=p, persist=True)
    s = [x for x in res["slices"] if x["branch"] == cal.BRANCH_NEW][0]
    assert s["window"] == "historical_backfill" and s["verdict"] == "KEEP_SHADOW"


def test_calibration_is_read_only_on_production(tmp_path):
    p = str(tmp_path / "ro.sqlite")
    _seed(p)
    c = sqlite3.connect(p)
    ps_before = c.execute("SELECT count(*) FROM proposed_signals").fetchone()[0]
    fr_before = c.execute("SELECT signal_id, final_r FROM signal_outcomes ORDER BY signal_id").fetchall()
    c.close()
    cal.refresh(db=p, persist=True)
    c = sqlite3.connect(p)
    ps_after = c.execute("SELECT count(*) FROM proposed_signals").fetchone()[0]
    fr_after = c.execute("SELECT signal_id, final_r FROM signal_outcomes ORDER BY signal_id").fetchall()
    tables = [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'")]
    c.close()
    assert ps_after == ps_before                       # no rows added/removed
    assert fr_after == fr_before                       # final_r untouched
    # only the calibration read-model tables were added
    assert "entry_mode_calibration_slices" in tables and "entry_mode_calibration_paired" in tables


def test_policy_summary_integrity(tmp_path):
    p = str(tmp_path / "pol.sqlite")
    _seed(p)
    res = cal.refresh(db=p, persist=False)
    pol = cal.policy_summary(res)
    # stocks/intraday/BREAKOUT_CONTINUATION is a promoted slice and NOT disabled -> integrity ok
    assert pol["integrity_ok"] is True
    assert any(x["entry_mode"] == "BREAKOUT_CONTINUATION" for x in pol["promoted_slices"])


# ============================ eligible vs policy-disabled headline (item A) ============================

def test_render_headline_counts_only_eligible():
    def _slice(asset, mode, em, verdict, net, disabled_reason=None):
        return {"branch": cal.BRANCH_NEW, "window": cal.FORWARD, "asset_class": asset, "mode": mode,
                "entry_mode": em, "verdict": verdict, "verdict_reasons": [], "net_pnl_usd": net,
                "trades": 40, "filled": 40, "closed": 40, "policy_disabled_reason": disabled_reason,
                "policy_promoted_reason": None}
    result = {
        "generated_at": "2026-07-07T00:00:00+00:00", "activated_at": "2026-06-25T00:00:00+00:00",
        "risk_usd_per_trade": 25.0, "paired": [],
        "slices": [
            _slice("crypto", "intraday", "STRUCTURAL_RETEST", "NEED_MORE_DATA", 100),          # eligible
            _slice("crypto", "scalp", "PULLBACK_LIMIT", "DISABLED_BY_POLICY", 500,
                   disabled_reason="crypto_scalp_disabled_by_policy"),                          # policy-disabled
            _slice("stocks", "swing", "PULLBACK_LIMIT", "UNSUPPORTED_LEGACY", 300),             # legacy
            _slice("crypto", "intraday", "NO_CHASE_SKIP", "SKIP_POLICY", 0),                    # skip
        ],
    }
    md = cal.render_markdown(result)
    # headline counts + sums ONLY the eligible slice
    assert "eligible forward slices: **1**" in md
    assert "eligible forward net USD: **$100**" in md          # NOT 100+500+300
    # each non-eligible bucket has its own section
    assert "Policy-disabled diagnostics" in md
    assert "APPENDIX — legacy stocks swing/invest" in md
    assert "Skip-policy diagnostics" in md
    # the disabled slice (scalp) is NOT in the eligible evidence table headline count
    elig_section = md.split("Eligible forward evidence")[1].split("##")[0]
    assert "STRUCTURAL_RETEST" in elig_section and "scalp" not in elig_section


# ============================ paired executed vs with-skips (item 7) ============================

def test_paired_executed_vs_with_skips_split():
    def row(sid, branch, fill, net):
        return {"signal_id": sid, "branch": branch, "fee_profile": "fp", "asset_class": "crypto",
                "trade_mode": "intraday", "entry_mode": "BREAKOUT_CONTINUATION",
                "window": "forward_since_activation", "entry_fill_status": fill,
                "net_pnl_usdt": net, "net_r": (net / 25 if net is not None else None),
                "close_reason": "x", "skipped_shadow_reason": None}
    rows = [
        row("A", "old_paper", "filled", -5), row("A", "new_logic_shadow", "filled", 10),   # both filled: exec +15
        row("B", "old_paper", "filled", -20), row("B", "new_logic_shadow", "skipped", None),  # avoided bad -20
        row("C", "old_paper", "filled", 30), row("C", "new_logic_shadow", "skipped", None),   # missed good +30
    ]
    p = cal._paired(rows)[0]
    assert p["executed_common"] == 1 and p["executed_sum_delta_usd"] == 15.0    # verdict uses this
    assert p["avoided_bad_count"] == 1 and p["avoided_bad_usd"] == 20.0
    assert p["missed_good_count"] == 1 and p["missed_good_usd"] == 30.0
    assert p["with_skips_sum_delta_usd"] == 5.0                                 # 15 + 20 - 30


# ============================ pre-entry lookahead safety ============================

def test_preentry_classifier_is_lookahead_safe(monkeypatch):
    import pandas as pd
    from src.execution import preentry_classifier as pe
    created = "2026-06-05T12:00:00+00:00"
    # bars: 3 before created_at, 3 after. Only the pre bars may be used.
    ts = ["2026-06-05T09:00:00+00:00", "2026-06-05T10:00:00+00:00", "2026-06-05T11:00:00+00:00",
          "2026-06-05T13:00:00+00:00", "2026-06-05T14:00:00+00:00", "2026-06-05T15:00:00+00:00"]
    df = pd.DataFrame({"timestamp": ts, "open": [100]*6, "high": [101]*6, "low": [99]*6, "close": [100]*6})
    monkeypatch.setattr("src.signals.tracker._load_ohlcv_for_signal", lambda *a, **k: (df, "binance", "1h"))

    captured = {}
    real_classify = pe.classify

    def _spy_classify(**kw):
        captured["n"] = len(kw.get("candles") or [])
        return real_classify(**kw)
    monkeypatch.setattr(pe, "classify", _spy_classify)

    candles = pe._candles_le_created(fs=None, cfg=None, symbol="X/USDT", mode="intraday",
                                     asset_class="crypto", exchange_focus="", created_at=created)
    assert len(candles) == 3   # only the 3 bars at/<=created_at survive the guard
    pe.classify_preentry_from_candles(direction="long", entry_low=99, entry_high=101,
                                      entry=100, stop=98, candles=candles)
    assert captured["n"] == 3


def test_preentry_data_quality_labels():
    from src.execution import preentry_classifier as pe
    thin = pe.classify_preentry_from_candles(direction="long", entry_low=99, entry_high=101,
                                             entry=100, stop=98, candles=[{"open":1,"high":1,"low":1,"close":1}])
    assert thin["data_quality"] == "thin"
    none = pe.classify_preentry_from_candles(direction="long", entry_low=99, entry_high=101,
                                             entry=100, stop=98, candles=[])
    assert none["data_quality"] == "no_data"


# ============================ parameter sweep read-only ============================

def test_parameter_sweep_is_read_only_and_uses_protection():
    from src.execution import entry_mode_parameter_sweep as sw
    cfg = cal.load_calibration_config()
    candles = [{"open": 100, "high": 100, "low": 100, "close": 100},
               {"open": 100, "high": 101.4, "low": 100, "close": 101.4},
               {"open": 101, "high": 101, "low": 97.9, "close": 98}]
    geom = {"direction": "long", "entry_low": 99.5, "entry_high": 100.5, "entry_trigger": 100.0,
            "entry": 100.0, "stop": 98.0, "tp1": 104, "tp2": 106, "tp3": 110,
            "entry_mode": "BREAKOUT_CONTINUATION", "symbol": "X/USDT"}
    out = sw.sweep_signal(geom, candles, cfg)
    assert "structural_stop_atr_buffer" in out and "current" in out["structural_stop_atr_buffer"]
    # the sweep uses Model-F protection: +0.7R then reverse -> breakeven, not -1R
    cur = out["structural_stop_atr_buffer"]["current"]
    assert cur["close_reason"] == "breakeven_stop" and cur["net_r"] == 0.0


def test_sweep_variant_geometry_widens_stop():
    from src.execution.entry_mode_parameter_sweep import _variant_geometry
    geom = {"direction": "long", "entry": 100.0, "stop": 98.0}
    g, kw = _variant_geometry("structural_stop_atr_buffer", 0.5, geom)
    assert g["stop"] < 98.0   # wider stop for a long
    # maker_trade_through_bps now affects the FILL condition, not a cost subtraction
    _g, kw2 = _variant_geometry("maker_trade_through_bps", 10, geom)
    assert "maker_trade_through_bps" in kw2 and _g["stop"] == 98.0


# ============================ protection evidence status (resolved, not n) =================

def _prot_dict(fwd_n, fwd_resolved, protection_trades=None):
    return {"protection_trades": protection_trades if protection_trades is not None else max(fwd_n, 1),
            "evidence_forward_postfreeze": {"n": fwd_n, "resolved": fwd_resolved}}


def test_protection_evidence_status_gates_on_resolved_not_n():
    # n=30 (>= threshold) but only 5 resolved -> must NOT be FORWARD_VALIDATED.
    prot = _prot_dict(fwd_n=30, fwd_resolved=5)
    assert cal.protection_evidence_status(prot) == "INSUFFICIENT_FORWARD_SAMPLE"


def test_protection_evidence_status_forward_validated_on_resolved():
    prot = _prot_dict(fwd_n=30, fwd_resolved=30)
    assert cal.protection_evidence_status(prot) == "FORWARD_VALIDATED"


def test_protection_evidence_status_no_forward_evidence_when_n_zero():
    prot = _prot_dict(fwd_n=0, fwd_resolved=0)
    assert cal.protection_evidence_status(prot) == "NO_FORWARD_EVIDENCE"


def test_protection_evidence_status_no_protection_data():
    assert cal.protection_evidence_status({}) == "NO_PROTECTION_DATA"
    assert cal.protection_evidence_status(None) == "NO_PROTECTION_DATA"


# ============================ module guardrails ============================

def test_calibration_modules_have_no_live_order_surface():
    import src.execution.entry_mode_calibration as m1
    import src.execution.profit_protection as m2
    import src.execution.entry_mode_parameter_sweep as m3
    import src.execution.preentry_classifier as m4
    for mod in (m1, m2, m3, m4):
        src = Path(mod.__file__).read_text(encoding="utf-8").lower()
        for bad in ("create_order", "place_order", "submit_order", "auto_live", "manual_live",
                    "update proposed_signals", "update signal_outcomes", "final_r ="):
            assert bad not in src, f"{mod.__name__} must be read-model only: {bad!r}"
