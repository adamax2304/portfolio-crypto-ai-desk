"""Hardening tests for the stocks INTRADAY paper/actionable system (2026-07-02).

Covers: the hard RR gate (rr<min can never be A/B), C-tier watchlist wording (never actionable),
sector/RS metadata persistence, the read-only rolling drawdown guards (long-cohort demotion +
stocks-intraday-only / crypto-untouched), the quality analytics block using paper_execution_r, and
that old stocks swing/invest stay removed. No network. Live is never touched.
"""
from __future__ import annotations

import copy
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace

import pytest

from src.config import load_config
from src.storage.file_store import FileStore
from src.storage.sqlite import SQLiteStore
from src.stocks import load_stocks_config, intraday_guards
from src.stocks.agents.trade_idea_agent import StockTradeIdeaAgent

# Market-open UTC (10:00 ET) so the market-closed gate does not interfere.
NOW = datetime(2026, 6, 4, 14, 0, tzinfo=timezone.utc)


@pytest.fixture(autouse=True)
def _isolate_actionability_gate(monkeypatch):
    """These tests target the RR / ATR / structural-TP tiering + rolling drawdown guard in ISOLATION.
    The SI-1..5 actionability gate has its own tests (test_intraday_gate_*.py); here it must not
    interfere. With real cached SPY/QQQ from a different calendar date than NOW it would legitimately
    demote on stale market context — so we neutralize it to a no-demote for this module only."""
    from types import SimpleNamespace
    from src.stocks import intraday_actionability_gates as _g
    monkeypatch.setattr(
        _g, "evaluate",
        lambda **k: SimpleNamespace(decision="AB", demote_reasons=[], fields={}))


def _agent(tmp_path):
    db = SQLiteStore(Path(tmp_path) / "t.sqlite")
    db.init_db()
    cfg = load_config()
    scfg = load_stocks_config()
    return StockTradeIdeaAgent(cfg, scfg, FileStore(cfg), db), db


def _payloads(*, rr=2.0, direction="long", symbol="NVDA", tier="A",
              tp1_source="structural", atr_extension=None, sector_payload=None):
    setup = {"symbol": symbol, "entry_low": 100.0, "entry_high": 101.0,
             "invalidation": 99.0, "tp1": 104.0, "tp2": 108.0, "tp3": 112.0,
             "rr_to_tp1": rr, "volume_ratio": 1.4, "tp1_source": tp1_source}
    if atr_extension is not None:
        setup["atr_extension"] = atr_extension
    return dict(
        scoring_payload={"scores": [{"symbol": symbol, "tier": tier, "direction": direction,
                                     "final_score": 88.0, "confidence": "high", "cap_reasons": []}]},
        technical_payload={"setups": [setup]},
        news_payload={"hits_by_symbol": {symbol: []}},
        earnings_payload={"risks": [{"symbol": symbol, "severity": "safe"}]},
        rs_payload={"rows": [{"symbol": symbol, "rs_vs_spy_20d": 6.0, "rs_vs_sector_20d": 2.0,
                              "sector": "Technology", "sector_etf": "XLK"}]},
        regime_payload={"regime": {"label": "bullish"}}, sector_payload=sector_payload or {},
        risk_payload={"by_symbol": {symbol: {"risk_level": "low", "flags": []}}})


# ---------------------------------------------------------------- 1. RR gate --
def test_rr_below_min_cannot_be_ab(tmp_path):
    agent, _ = _agent(tmp_path)
    out = agent.run(**_payloads(rr=1.0), mode="intraday", now=NOW)
    idea = out["ideas"][0]
    assert idea["tier"] == "C"                       # high score/news/regime cannot rescue a 1.0R
    assert "rr_below_min_required" in (idea.get("cap_reasons") or [])


def test_rr_at_or_above_min_stays_ab(tmp_path):
    agent, _ = _agent(tmp_path)
    out = agent.run(**_payloads(rr=2.0), mode="intraday", now=NOW)
    idea = out["ideas"][0]
    assert idea["tier"] == "A"                       # empty db → no rolling guard demotion
    assert "rr_below_min_required" not in (idea.get("cap_reasons") or [])


# ---------------------------------------------- 3. sector/RS metadata persists --
def test_sector_and_rs_metadata_persist(tmp_path):
    agent, _ = _agent(tmp_path)
    out = agent.run(**_payloads(rr=2.0), mode="intraday", now=NOW)
    raw = out["ideas"][0]["raw"]
    assert (raw.get("candidate") or {}).get("sector") == "Technology"     # → proposed_signals.sector
    st = raw.get("structured") or {}
    assert st.get("sector_etf") == "XLK" and st.get("rs_vs_spy") == 6.0
    assert st.get("volume_ratio") == 1.4 and st.get("rr_to_tp1") == 2.0


# ------------------------------------------------------- 2. report C-tier wording --
def test_report_c_tier_never_actionable():
    from src.stocks.pipelines.stocks_pipeline import StocksPipelineResult
    from src.stocks.reports.stocks_report_builder import build_stocks_report
    r = StocksPipelineResult(mode="intraday")
    r.regime = {"regime": {"label": "bullish", "bias": "long"}}
    r.sectors = {}
    r.scoring = {"scores": []}
    r.ideas_payload = {"ideas": [{
        "symbol": "NVDA", "direction": "long", "tier": "C", "score": 78.0,
        "cap_reasons": ["rr_below_min_required", "tier demoted A→C: rr_below_min_required (rr_to_tp1=1.00 < 1.50)"],
        "raw": {"setup": {}, "structured": {}}}]}
    text = build_stocks_report(r)
    assert "A/B Actionable Candidates" in text
    assert "C-tier Watchlist — NOT actionable" in text
    # the C idea shows as watchlist/not-actionable with its demote reason, never as actionable
    assert "watchlist / not actionable" in text
    assert "rr_below_min_required" in text


# --------------------------------------------- 4/5. rolling guard + crypto scope --
def _seed(store, *, direction, r, n, asset_class="stocks", mode="intraday", tier="A", days_ago=1, now=NOW):
    import sqlite3
    ts = (now - timedelta(days=days_ago)).isoformat()
    sids = []
    for i in range(n):                                # phase 1: signals (store owns its connection)
        sid = f"{asset_class}_{direction}_{i}_{days_ago}_{int(r*100)}"
        sids.append(sid)
        store.upsert_proposed_signal({
            "signal_id": sid, "created_at": ts, "updated_at": ts, "symbol": f"S{i}",
            "direction": direction, "mode": mode, "tier": tier, "asset_class": asset_class,
            "status": "closed"})
    conn = sqlite3.connect(str(store.db_path), timeout=30)   # phase 2: paper outcomes
    try:
        conn.execute("CREATE TABLE IF NOT EXISTS paper_execution_outcomes "
                     "(signal_id TEXT UNIQUE, paper_execution_r REAL)")
        conn.executemany(
            "INSERT OR REPLACE INTO paper_execution_outcomes (signal_id, paper_execution_r) VALUES (?,?)",
            [(s, r) for s in sids])
        conn.commit()
    finally:
        conn.close()


def test_rolling_guard_demotes_weak_long_cohort(tmp_path):
    store = SQLiteStore(Path(tmp_path) / "g.sqlite")
    store.init_db()
    # global 7d stays HEALTHY (winning shorts) but the LONG cohort is weak (losing longs).
    _seed(store, direction="long", r=-1.0, n=6)      # long cohort: net -6, PF 0
    _seed(store, direction="short", r=1.0, n=8)       # keeps global 7d net positive
    risk = copy.deepcopy(load_stocks_config().risk)
    risk["intraday_guards"].pop("reset_at_utc", None)
    long_reasons = intraday_guards.guard_cap_reasons(store, risk, direction="long",
                                                     long_confirmation_ok=False, now=NOW)
    short_reasons = intraday_guards.guard_cap_reasons(store, risk, direction="short",
                                                      long_confirmation_ok=False, now=NOW)
    assert intraday_guards.LONG_REASON in long_reasons          # weak long cohort → demote longs
    assert intraday_guards.CB_REASON not in long_reasons        # global cohort is healthy
    assert short_reasons == []                                  # healthy short cohort untouched


def test_opt_in_global_breaker_blocks_confirmed_long_without_bypass(tmp_path):
    # The global breaker remains available as an explicit safety opt-in.  Its
    # long_confirmation_bypass default is still false, so it blocks both sides
    # when enabled and both directions are weak.
    store = SQLiteStore(Path(tmp_path) / "cb_default.sqlite")
    store.init_db()
    _seed(store, direction="long", r=-1.0, n=6)
    _seed(store, direction="short", r=-1.0, n=6)   # both directions weak -> global breaker trips
    risk = copy.deepcopy(load_stocks_config().risk)
    risk["intraday_guards"].pop("reset_at_utc", None)
    risk["intraday_guards"]["global_guard_blocks_all_directions"] = True
    assert risk["intraday_guards"]["circuit_breaker"].get("long_confirmation_bypass", False) is False
    reasons = intraday_guards.guard_cap_reasons(store, risk, direction="long",
                                                long_confirmation_ok=True, now=NOW)
    assert intraday_guards.CB_REASON in reasons


def test_global_breaker_bypass_opt_in_for_confirmed_long_only(tmp_path):
    # With long_confirmation_bypass=true, a CONFIRMED long survives the global breaker too (reusing
    # the same strict long_extra_confirmation bar, not a new criterion). Shorts have no confirmation
    # concept and must remain fully blocked regardless of the flag.
    store = SQLiteStore(Path(tmp_path) / "cb_bypass.sqlite")
    store.init_db()
    _seed(store, direction="long", r=-1.0, n=6)
    _seed(store, direction="short", r=-1.0, n=6)
    risk = copy.deepcopy(load_stocks_config().risk)
    risk["intraday_guards"].pop("reset_at_utc", None)
    risk["intraday_guards"]["global_guard_blocks_all_directions"] = True
    risk["intraday_guards"]["circuit_breaker"]["long_confirmation_bypass"] = True

    confirmed_long = intraday_guards.guard_cap_reasons(store, risk, direction="long",
                                                       long_confirmation_ok=True, now=NOW)
    unconfirmed_long = intraday_guards.guard_cap_reasons(store, risk, direction="long",
                                                         long_confirmation_ok=False, now=NOW)
    short_reasons = intraday_guards.guard_cap_reasons(store, risk, direction="short",
                                                      long_confirmation_ok=True, now=NOW)
    assert intraday_guards.CB_REASON not in confirmed_long        # confirmed long bypasses global block
    assert intraday_guards.CB_REASON in unconfirmed_long          # unconfirmed long still blocked
    assert intraday_guards.CB_REASON in short_reasons             # shorts never bypass (no confirmation)


def test_global_breaker_can_be_disabled_without_disabling_side_guard(tmp_path):
    """Calibration may isolate directions, but it must retain the weak-side stop."""
    store = SQLiteStore(Path(tmp_path) / "cb_isolated.sqlite")
    store.init_db()
    _seed(store, direction="long", r=-1.0, n=6)
    _seed(store, direction="short", r=1.0, n=6)
    risk = copy.deepcopy(load_stocks_config().risk)
    risk["intraday_guards"].pop("reset_at_utc", None)
    risk["intraday_guards"]["global_guard_blocks_all_directions"] = False

    long_reasons = intraday_guards.guard_cap_reasons(
        store, risk, direction="long", long_confirmation_ok=False, now=NOW,
    )
    short_reasons = intraday_guards.guard_cap_reasons(
        store, risk, direction="short", long_confirmation_ok=False, now=NOW,
    )

    assert intraday_guards.CB_REASON not in long_reasons
    assert intraday_guards.LONG_REASON in long_reasons
    assert short_reasons == []


def test_rolling_guard_is_stocks_intraday_only_not_crypto(tmp_path):
    store = SQLiteStore(Path(tmp_path) / "c.sqlite")
    store.init_db()
    # a big crypto drawdown must NOT influence the stocks-intraday guard.
    _seed(store, direction="long", r=-5.0, n=20, asset_class="crypto")
    perf = intraday_guards.rolling_ab_performance(store, lookback_days=7, now=NOW)
    assert perf["n"] == 0                                       # crypto rows excluded
    risk = copy.deepcopy(load_stocks_config().risk)
    risk["intraday_guards"].pop("reset_at_utc", None)
    assert intraday_guards.guard_cap_reasons(store, risk, direction="long", now=NOW) == []


def test_profile_guard_does_not_mix_other_stock_intraday_profiles(tmp_path):
    """A weak pullback book must not block an unrelated breakout profile."""
    store = SQLiteStore(Path(tmp_path) / "profile_guard.sqlite")
    store.init_db()
    stamp = (NOW - timedelta(hours=2)).isoformat()
    rows = []
    for profile, result in (("stocks_intraday_breakout_1bar_paper_v1", -1.0),
                            ("stocks_intraday_pullback_vwap_paper_v1", 1.0)):
        for index in range(4):
            signal_id = f"{profile}_{index}"
            store.upsert_proposed_signal({
                "signal_id": signal_id, "created_at": stamp, "updated_at": stamp,
                "symbol": f"S{index}", "direction": "long", "mode": "intraday",
                "tier": "A", "asset_class": "stocks", "status": "closed",
            })
            rows.append((signal_id, result, stamp, "forward_postfreeze", "valid", "CLOSED", profile))
    with sqlite3.connect(store.db_path) as conn:
        conn.execute(
            "CREATE TABLE paper_execution_outcomes ("
            "signal_id TEXT, paper_execution_r REAL, computed_at TEXT, evidence_class TEXT, "
            "execution_validity TEXT, lifecycle_state TEXT, paper_entry_profile TEXT)"
        )
        conn.executemany("INSERT INTO paper_execution_outcomes VALUES(?,?,?,?,?,?,?)", rows)
        conn.commit()

    risk = copy.deepcopy(load_stocks_config().risk)
    risk["intraday_guards"].pop("reset_at_utc", None)
    risk["intraday_guards"]["global_guard_blocks_all_directions"] = True
    risk["intraday_guards"]["circuit_breaker"]["min_cohort_trades"] = 4
    risk["intraday_guards"]["direction_guard"]["min_cohort_trades"] = 4
    breakout = intraday_guards.rolling_ab_performance(
        store, paper_entry_profile="stocks_intraday_breakout_1bar_paper_v1",
        lookback_days=7, now=NOW, cfg_risk=risk,
    )
    pullback = intraday_guards.rolling_ab_performance(
        store, paper_entry_profile="stocks_intraday_pullback_vwap_paper_v1",
        lookback_days=7, now=NOW, cfg_risk=risk,
    )
    assert (breakout["n"], breakout["net_r"]) == (4, -4.0)
    assert (pullback["n"], pullback["net_r"]) == (4, 4.0)
    assert intraday_guards.CB_REASON in intraday_guards.guard_cap_reasons(
        store, risk, direction="long",
        paper_entry_profile="stocks_intraday_breakout_1bar_paper_v1", now=NOW,
    )
    assert intraday_guards.guard_cap_reasons(
        store, risk, direction="long",
        paper_entry_profile="stocks_intraday_pullback_vwap_paper_v1", now=NOW,
    ) == []


def test_rolling_guard_reset_epoch_ignores_old_drawdown_but_not_new(tmp_path):
    store = SQLiteStore(Path(tmp_path) / "reset.sqlite")
    store.init_db()
    # Old regime: enough losing A/B rows to trip the guard, but all before the reset epoch.
    _seed(store, direction="long", r=-1.0, n=6, days_ago=1, now=NOW)
    risk = copy.deepcopy(load_stocks_config().risk)
    risk["intraday_guards"]["reset_at_utc"] = (NOW - timedelta(hours=12)).isoformat()

    perf = intraday_guards.rolling_ab_performance(store, lookback_days=7, now=NOW, cfg_risk=risk)
    assert perf["n"] == 0
    assert intraday_guards.guard_cap_reasons(store, risk, direction="long", now=NOW) == []

    # New regime: losses after the reset epoch are counted normally, so the guard can re-arm.
    _seed(store, direction="long", r=-1.0, n=6, days_ago=0, now=NOW)
    perf = intraday_guards.rolling_ab_performance(store, lookback_days=7, now=NOW, cfg_risk=risk)
    assert perf["n"] == 6
    assert intraday_guards.LONG_REASON in intraday_guards.guard_cap_reasons(
        store, risk, direction="long", now=NOW)


# ------------------------------------------------- 6. analytics uses paper_execution_r --
def test_quality_section_uses_paper_execution_r_not_final_r(tmp_path):
    from src.stocks.reports.stocks_report_builder import _intraday_quality_section
    store = SQLiteStore(Path(tmp_path) / "q.sqlite")
    store.init_db()
    cfg = SimpleNamespace(db_path=store.db_path)
    text = _intraday_quality_section(cfg)
    assert "paper_execution_r" in text
    assert "NOT legacy final_r" in text
    assert "A/B by direction" in text


# ---------------------------------------------- 7. old stocks swing/invest stay off --
def test_old_stocks_swing_invest_pipeline_still_blocked():
    from src.stocks.pipelines.stocks_pipeline import StocksPipeline
    p = StocksPipeline(load_config())
    for m in ("swing", "invest"):
        with pytest.raises(ValueError) as ei:
            p.run_report(mode=m)
        assert "deprecated/removed" in str(ei.value)


# ============================================================================
# 2026-07-03 continuation hardening (items 1-6)
# ============================================================================

# ---- item 1: STRICT long_confirmation_ok — missing data is never confirmation ----
def test_long_confirmation_strict_missing_data_is_not_confirmation():
    risk = load_stocks_config().risk
    ok = intraday_guards.long_confirmation_ok
    base = {"rs_vs_spy": 5.0, "volume_ratio": 1.5, "sector_contradicts": False,
            "sector_weak": False, "atr_extension": 1.0}
    assert ok(base, risk) is True                      # all known & passing
    # missing relative volume → not confirmed (min_volume_ratio configured)
    m = dict(base); m["volume_ratio"] = None
    assert ok(m, risk) is False
    # sector completely unknown (both flags None) → not confirmed
    m = dict(base); m["sector_contradicts"] = None; m["sector_weak"] = None
    assert ok(m, risk) is False
    # missing ATR extension → not confirmed (max_atr_extension configured)
    m = dict(base); m["atr_extension"] = None
    assert ok(m, risk) is False
    # missing / non-positive RS → not confirmed
    m = dict(base); m["rs_vs_spy"] = None
    assert ok(m, risk) is False
    m = dict(base); m["rs_vs_spy"] = -0.1
    assert ok(m, risk) is False


# ---- item 3: split structural vs ATR TP1 (technical geometry) ----
def _tech_agent(tmp_path):
    from src.stocks.agents.technical_agent import StockTechnicalAgent
    db = SQLiteStore(Path(tmp_path) / "tt.sqlite")
    db.init_db()
    cfg = load_config()
    scfg = load_stocks_config()
    return StockTechnicalAgent(cfg, scfg, FileStore(cfg), db)


def _ohlcv(closes, vol=1_000_000):
    import pandas as pd
    return pd.DataFrame({"high": [c + 0.5 for c in closes], "low": [c - 0.5 for c in closes],
                         "close": list(closes), "volume": [vol] * len(closes)})


def test_technical_tp1_source_structural_vs_atr(tmp_path):
    import pandas as pd
    agent = _tech_agent(tmp_path)
    closes = [100 + i * 0.5 for i in range(60)]              # clean uptrend → long (ema50 needs ≥50)
    ctx, execf = _ohlcv(closes), _ohlcv(closes[-30:])
    last = closes[-1]
    frames = {"1h": ctx, "15m": execf}

    # structural: prior-day HIGH well above entry → tp1_source == "structural"
    frames["1d"] = pd.DataFrame({"high": [last + 10, last + 10], "low": [last - 5, last - 5],
                                 "close": [last, last], "volume": [1e6, 1e6]})
    loader = SimpleNamespace(load_cached=lambda s, tf: frames.get(tf))
    setup = agent._build("TEST", loader, "intraday")
    assert setup is not None and setup.direction == "long"
    assert setup.tp1_source == "structural"
    assert setup.rr_to_structural_tp1 is not None           # real structural RR

    # ATR-only: prior-day HIGH below entry → measured 1.5*ATR objective, NOT structural
    frames["1d"] = pd.DataFrame({"high": [last - 2, last - 2], "low": [last - 5, last - 5],
                                 "close": [last, last], "volume": [1e6, 1e6]})
    setup2 = agent._build("TEST", loader, "intraday")
    assert setup2.tp1_source == "atr_measured"
    assert setup2.rr_to_structural_tp1 is None              # no structural level exists
    assert setup2.rr_to_tp1 is not None                     # measured RR still computed


def test_atr_only_tp1_capped_to_B_without_confirmation(tmp_path):
    # A raw-A idea whose TP1 is only a measured ATR objective and which lacks extra confirmation
    # (atr_extension missing) must be capped A→B — it can never ship as a structural A.
    agent, _ = _agent(tmp_path)
    out = agent.run(**_payloads(rr=2.0, tp1_source="atr_measured"), mode="intraday", now=NOW)
    idea = out["ideas"][0]
    assert idea["tier"] == "B"
    assert "atr_only_tp1_capped_to_B" in (idea.get("cap_reasons") or [])


def test_structural_tp1_stays_A(tmp_path):
    agent, _ = _agent(tmp_path)
    out = agent.run(**_payloads(rr=2.0, tp1_source="structural"), mode="intraday", now=NOW)
    idea = out["ideas"][0]
    assert idea["tier"] == "A"
    assert "atr_only_tp1_capped_to_B" not in (idea.get("cap_reasons") or [])


def test_pre_gate_tier_persisted_in_raw(tmp_path):
    # An ATR-only A demoted to B still records its pre-gate tier for diagnostics.
    agent, _ = _agent(tmp_path)
    out = agent.run(**_payloads(rr=2.0, tp1_source="atr_measured"), mode="intraday", now=NOW)
    raw = out["ideas"][0]["raw"]
    assert raw.get("pre_gate_tier") == "A"
    assert raw.get("final_tier") == "B"
    # setup provenance surfaced for report/packet
    assert raw["setup"].get("tp1_source") == "atr_measured"


# ---- item 2: recovery_stats includes gate-demoted would-have-been-A/B ----
def _seed_raw(store, sid, *, tier, raw, r, days_ago=1, now=NOW, symbol="AAA",
              direction="long", extra=None):
    import sqlite3
    import json as _json
    ts = (now - timedelta(days=days_ago)).isoformat()
    row = {"signal_id": sid, "created_at": ts, "updated_at": ts, "symbol": symbol,
           "direction": direction, "mode": "intraday", "tier": tier, "asset_class": "stocks",
           "status": "closed", "raw_idea_json": _json.dumps(raw)}
    if extra:
        row.update(extra)
    store.upsert_proposed_signal(row)
    conn = sqlite3.connect(str(store.db_path), timeout=30)
    try:
        conn.execute("CREATE TABLE IF NOT EXISTS paper_execution_outcomes "
                     "(signal_id TEXT UNIQUE, paper_execution_r REAL)")
        conn.execute("INSERT OR REPLACE INTO paper_execution_outcomes "
                     "(signal_id, paper_execution_r) VALUES (?,?)", (sid, r))
        conn.commit()
    finally:
        conn.close()


def test_recovery_stats_includes_gate_demoted(tmp_path):
    store = SQLiteStore(Path(tmp_path) / "rec.sqlite")
    store.init_db()
    # a raw-A idea a gate demoted to C, then it printed a losing paper outcome
    _seed_raw(store, "dem_A", tier="C", r=-1.2,
              raw={"pre_gate_tier": "A", "final_tier": "C", "demoted_by_gate": True})
    # a genuinely-final B idea that won (still counts in the would-have-been pool)
    _seed_raw(store, "keep_B", tier="B", r=1.0, symbol="BBB",
              raw={"pre_gate_tier": "B", "final_tier": "B", "demoted_by_gate": False})
    rec = intraday_guards.recovery_stats(store, lookback_days=14, now=NOW)
    assert rec["n"] == 2
    assert rec["demoted_n"] == 1                    # only the demoted-to-C one
    assert rec["demoted_net_r"] == -1.2             # demoted cohort was a loser
    assert rec["net_r"] == round(-1.2 + 1.0, 3)


# ---- item 5: sector read-time fallback from raw_idea_json ----
def test_sector_read_time_fallback(tmp_path):
    # helper: column empty → structured.sector → candidate.sector → None
    assert intraday_guards._sector_from("", {"structured": {"sector": "Energy"}}) == "Energy"
    assert intraday_guards._sector_from(None, {"candidate": {"sector": "Health"}}) == "Health"
    assert intraday_guards._sector_from("Financials", {}) == "Financials"
    assert intraday_guards._sector_from(None, {}) is None
    # end-to-end: ab_breakdowns picks the sector from raw_idea_json when the column is blank
    store = SQLiteStore(Path(tmp_path) / "sec.sqlite")
    store.init_db()
    _seed_raw(store, "sec1", tier="A", r=1.5, symbol="ZZ",
              raw={"structured": {"sector": "Energy"}}, extra={"sector": ""})
    bd = intraday_guards.ab_breakdowns(store, lookback_days=30, now=NOW)
    assert "Energy" in bd["by_sector"]
    assert "unknown" not in bd["by_sector"]         # not mislabelled as unknown


# ---- item 4: report shows pre-gate vs final tier + summary from ideas + heading dedup ----
def test_report_summary_final_tiers_and_candidate_columns():
    from src.stocks.pipelines.stocks_pipeline import StocksPipelineResult
    from src.stocks.reports.stocks_report_builder import build_stocks_report
    r = StocksPipelineResult(mode="intraday")
    r.regime = {"regime": {"label": "risk_on", "bias": "long"}}
    r.sectors = {}
    syms = ["AA", "BB", "CC", "DD", "EE"]
    r.scoring = {"scores": [{"symbol": s, "direction": "long", "tier": "A", "final_score": 85.0,
                             "confidence": "high", "risk_penalty": 0} for s in syms]}
    r.ideas_payload = {"ideas": [{
        "symbol": s, "direction": "long", "tier": "C", "score": 85.0,
        "cap_reasons": ["stocks_intraday_7d_drawdown_guard",
                        "tier demoted A→C: rolling paper-R drawdown guard"],
        "raw": {"pre_gate_tier": "A", "final_tier": "C", "demoted_by_gate": True,
                "setup": {}, "structured": {}}} for s in syms]}
    text = build_stocks_report(r)
    # 5 raw A/B all demoted → final summary counts A/B=0, C=5 (from ideas, not raw scoring)
    assert "A/B=0" in text
    assert "C=5" in text
    assert "Demoted A/B→C by gates: 5" in text
    # Top Candidates shows BOTH raw tier and post-gate final tier with the demotion marker
    assert "| AA | long | A | C ⤵ |" in text
    # heading dedup: summary is now §10 (quality §9 lives elsewhere), no duplicate "## 9. Final Summary"
    assert "## 10. Final Summary" in text
    assert "## 9. Final Summary" not in text
    # C-tier watchlist shows the demoted-from tier compactly
    assert "(was A)" in text


# ---- item 6: enriched packet — fresh window + demoted near-A/B section ----
def test_packet_demoted_near_ab_and_fresh_window(tmp_path):
    from src.stocks.llm_packet import _intraday_ab_review_section
    import json as _json
    store = SQLiteStore(Path(tmp_path) / "pk.sqlite")
    store.init_db()
    fresh = (NOW - timedelta(hours=6)).isoformat()          # within 48h window
    stale = (NOW - timedelta(hours=80)).isoformat()         # outside 48h window
    # a fresh raw-A idea the guard demoted to C
    store.upsert_proposed_signal({
        "signal_id": "dem1", "created_at": fresh, "updated_at": fresh, "symbol": "DMT",
        "direction": "long", "mode": "intraday", "tier": "C", "asset_class": "stocks",
        "status": "waiting_for_entry", "sector": "Technology", "expected_rr_tp1": 1.8,
        "market_regime": "risk_on", "news_supported": 0,
        "raw_idea_json": _json.dumps({
            "pre_gate_tier": "A", "final_tier": "C", "demoted_by_gate": True, "score": 84.0,
            "cap_reasons": ["stocks_intraday_long_guard",
                            "tier demoted A→C: rolling paper-R drawdown guard"],
            "structured": {"sector": "Technology", "rs_vs_spy": 5.0, "volume_ratio": 1.3,
                           "rr_to_tp1": 1.8, "tp1_source": "atr_measured"}})})
    # a STALE open A/B (older than the window) must NOT show as a current open candidate
    store.upsert_proposed_signal({
        "signal_id": "old1", "created_at": stale, "updated_at": stale, "symbol": "OLD",
        "direction": "long", "mode": "intraday", "tier": "A", "asset_class": "stocks",
        "status": "waiting_for_entry", "sector": "Energy", "expected_rr_tp1": 2.2,
        "raw_idea_json": _json.dumps({"structured": {"sector": "Energy"}})})
    text = _intraday_ab_review_section(store, now=NOW)
    assert "Top demoted near-A/B candidates" in text
    assert "DMT" in text
    assert "was A→C" in text
    assert "stocks_intraday_long_guard" in text
    assert "atr_measured" in text
    assert "OLD" not in text                                # stale candidate excluded by 48h window


# ============================================================================
# 2026-07-03 nuance fixes (post-continuation)
# ============================================================================

# ---- nuance 1: long-confirmation caller passes sector as TRUE/FALSE/None tri-state ----
def test_sector_confirmation_state_tristate():
    from src.stocks.agents.trade_idea_agent import _sector_confirmation_state
    # unknown: sector name present but no sector-rotation snapshot / no flags → (None, None)
    sc, sw = _sector_confirmation_state({"sector": "Technology", "sector_etf": "XLK"}, {}, {}, [])
    assert sc is None and sw is None
    # known NOT weak: snapshot says status strong → sector_weak == False
    sp = {"sectors": [{"sector": "Technology", "etf": "XLK", "status": "strong"}]}
    sc, sw = _sector_confirmation_state({"sector": "Technology", "sector_etf": "XLK"}, {}, sp, [])
    assert sw is False
    # known weak: snapshot status weak → True
    sp = {"sectors": [{"sector": "Technology", "etf": "XLK", "status": "weak"}]}
    sc, sw = _sector_confirmation_state({"sector": "Technology", "sector_etf": "XLK"}, {}, sp, [])
    assert sw is True
    # explicit risk flag wins → contradicts True
    sc, sw = _sector_confirmation_state({}, {}, {}, ["sector_contradicts_direction"])
    assert sc is True


def test_atr_only_unknown_sector_caps_to_B(tmp_path):
    # RS+, volume ok, atr_extension ok, BUT sector genuinely unknown (empty sector_payload) → the
    # caller must NOT silently treat it as known-not-weak → confirmation fails → ATR-only A caps to B.
    agent, _ = _agent(tmp_path)
    out = agent.run(**_payloads(rr=2.0, tp1_source="atr_measured", atr_extension=1.0),
                    mode="intraday", now=NOW)
    idea = out["ideas"][0]
    assert idea["tier"] == "B"
    assert "atr_only_tp1_capped_to_B" in (idea.get("cap_reasons") or [])


def test_atr_only_known_not_weak_sector_stays_A(tmp_path):
    # Same ATR-only setup but the sector is KNOWN not-weak (rotation snapshot status=strong) and all
    # other confirmations hold → confirmation passes → ATR-only A is allowed to stay A.
    agent, _ = _agent(tmp_path)
    sp = {"sectors": [{"sector": "Technology", "etf": "XLK", "status": "strong",
                       "rs_vs_spy_20d": 5.0}]}
    out = agent.run(**_payloads(rr=2.0, tp1_source="atr_measured", atr_extension=1.0,
                                sector_payload=sp), mode="intraday", now=NOW)
    idea = out["ideas"][0]
    assert idea["tier"] == "A"
    assert "atr_only_tp1_capped_to_B" not in (idea.get("cap_reasons") or [])


# ---- nuance 2: packet Open A/B excludes legacy rr≈1.0 / missing tp1_source ----
def test_packet_open_ab_excludes_legacy(tmp_path):
    from src.stocks.llm_packet import _intraday_ab_review_section
    import json as _json
    store = SQLiteStore(Path(tmp_path) / "leg.sqlite")
    store.init_db()
    fresh = (NOW - timedelta(hours=6)).isoformat()
    # legacy: pre-hardening open A/B — rr≈1.0, no tp1_source, missing confirmation metrics
    store.upsert_proposed_signal({
        "signal_id": "leg1", "created_at": fresh, "updated_at": fresh, "symbol": "LEG",
        "direction": "long", "mode": "intraday", "tier": "A", "asset_class": "stocks",
        "status": "waiting_for_entry", "sector": "Technology", "expected_rr_tp1": 1.0,
        "raw_idea_json": _json.dumps({"structured": {"sector": "Technology"}})})
    # current: post-hardening open A/B — rr≥1.5 and a known structural tp1_source
    store.upsert_proposed_signal({
        "signal_id": "cur1", "created_at": fresh, "updated_at": fresh, "symbol": "CUR",
        "direction": "long", "mode": "intraday", "tier": "A", "asset_class": "stocks",
        "status": "waiting_for_entry", "sector": "Technology", "expected_rr_tp1": 2.0,
        "raw_idea_json": _json.dumps({"structured": {"sector": "Technology", "rs_vs_spy": 5.0,
                                                     "volume_ratio": 1.3, "tp1_source": "structural"}})})
    text = _intraday_ab_review_section(store, now=NOW)
    head, sep, tail = text.partition("### Legacy open A/B excluded by new hardening")
    assert sep, "legacy-excluded section must be present"
    # current appears under Open A/B (head); legacy does NOT
    assert "CUR" in head
    assert "LEG" not in head
    # legacy appears in the excluded section with a reason
    assert "LEG" in tail
    assert ("tp1_source missing" in tail) or ("< 1.50" in tail)


# ---- nuance 3: ATR-only Open A/B needs FULL confirmation (RS+vol+sector+atr_extension) ----
def test_packet_atr_only_semi_legacy_excluded(tmp_path):
    # rr≥1.5 and tp1_source=atr_measured and RS+volume present, BUT sector + atr_extension missing →
    # this is NOT a fully-confirmed current ATR-only A/B and must be excluded (not shown as current).
    from src.stocks.llm_packet import _intraday_ab_review_section
    import json as _json
    store = SQLiteStore(Path(tmp_path) / "semi.sqlite")
    store.init_db()
    fresh = (NOW - timedelta(hours=6)).isoformat()
    store.upsert_proposed_signal({
        "signal_id": "semi1", "created_at": fresh, "updated_at": fresh, "symbol": "SEMI",
        "direction": "long", "mode": "intraday", "tier": "A", "asset_class": "stocks",
        "status": "waiting_for_entry", "sector": "", "expected_rr_tp1": 1.5,
        "raw_idea_json": _json.dumps({"structured": {"rs_vs_spy": 5.0, "volume_ratio": 1.3,
                                                     "tp1_source": "atr_measured"}})})
    text = _intraday_ab_review_section(store, now=NOW)
    head, sep, tail = text.partition("### Legacy open A/B excluded by new hardening")
    assert sep
    assert "SEMI" not in head                              # not shown as current Open A/B
    assert "SEMI" in tail                                  # shown as excluded
    assert "sector missing for atr_measured confirmation" in tail
    assert "atr_extension missing for atr_measured confirmation" in tail
    # explanatory text is honest about the full confirmation set
    assert "RS+volume+sector+ATR-extension confirmation" in text


def test_packet_atr_only_full_confirmation_is_current(tmp_path):
    # ATR-only with rr≥1.5 AND RS + volume + sector + atr_extension (within max) → stays CURRENT.
    from src.stocks.llm_packet import _intraday_ab_review_section
    import json as _json
    store = SQLiteStore(Path(tmp_path) / "full.sqlite")
    store.init_db()
    fresh = (NOW - timedelta(hours=6)).isoformat()
    store.upsert_proposed_signal({
        "signal_id": "full1", "created_at": fresh, "updated_at": fresh, "symbol": "FULL",
        "direction": "long", "mode": "intraday", "tier": "A", "asset_class": "stocks",
        "status": "waiting_for_entry", "sector": "Technology", "expected_rr_tp1": 1.6,
        "raw_idea_json": _json.dumps({"structured": {"sector": "Technology", "rs_vs_spy": 5.0,
                                                     "volume_ratio": 1.3, "atr_extension": 1.0,
                                                     "tp1_source": "atr_measured"}})})
    text = _intraday_ab_review_section(store, now=NOW)
    head, sep, tail = text.partition("### Legacy open A/B excluded by new hardening")
    assert sep
    assert "FULL" in head                                 # fully-confirmed ATR-only → current
    assert "FULL" not in tail                              # not in the excluded section
