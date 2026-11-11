"""SI-1..SI-5 stocks-intraday actionability gates — pure, fail-conservative, demote-only."""
from __future__ import annotations

from datetime import datetime, timezone, timedelta

from src.stocks import intraday_actionability_gates as g

CFG = {"index_return_conflict_pct": 0.15, "sector_return_conflict_pct": 0.15, "min_rvol": 1.5,
       "min_dollar_volume": 20_000_000, "max_spread_bps": 25, "allow_unknown_spread_for_liquid_names": False,
       "catalyst_max_age_minutes": 1440, "allow_pure_technical_ab": True,
       "catalyst_strong_types": ["earnings", "fda", "mna"], "catalyst_medium_types": ["analyst_action"]}


def _et(hh, mm, weekday=2):  # a Wednesday in EDT
    # 2026-07-08 is a Wednesday; ET = UTC-4 (EDT) → add 4h to get UTC
    return datetime(2026, 7, 8, hh + 4, mm, tzinfo=timezone.utc)


# ---- session_phase ----
def test_session_phase_buckets():
    assert g.session_phase(_et(6, 0)) == g.PREMARKET
    assert g.session_phase(_et(9, 35)) == g.FIRST_15M
    assert g.session_phase(_et(10, 30)) == g.MORNING
    assert g.session_phase(_et(12, 0)) == g.LUNCH
    assert g.session_phase(_et(14, 0)) == g.AFTERNOON
    assert g.session_phase(_et(15, 45)) == g.LAST_30M
    assert g.session_phase(_et(17, 0)) == g.OUTSIDE_RTH
    # weekend
    assert g.session_phase(datetime(2026, 7, 11, 15, 0, tzinfo=timezone.utc)) == g.OUTSIDE_RTH


def test_session_phase_respects_early_close():
    # 18:05 UTC is 13:05 ET on Black Friday 2026, after the 13:00 close.
    assert g.session_phase(datetime(2026, 11, 27, 18, 5, tzinfo=timezone.utc)) == g.OUTSIDE_RTH


# ---- SI-1 market context ----
def test_market_context_unknown_demotes():
    s, r = g.market_context_gate(direction="long", market_ctx={"status": "unknown"}, cfg=CFG)
    assert s == "unknown" and r == "market_context_unknown_or_stale"


def test_market_context_long_conflict_in_downtrend():
    ctx = {"status": "ok", "regime": "trend_down", "spy_rth_return_pct": -0.5, "qqq_rth_return_pct": -0.6,
           "spy_vs_vwap": "below", "qqq_vs_vwap": "below"}
    s, r = g.market_context_gate(direction="long", market_ctx=ctx, cfg=CFG)
    assert s == "conflict" and r == "market_context_conflict"


def test_market_context_long_ok_in_uptrend():
    ctx = {"status": "ok", "regime": "trend_up", "spy_rth_return_pct": 0.4, "qqq_rth_return_pct": 0.5,
           "spy_vs_vwap": "above", "qqq_vs_vwap": "above"}
    assert g.market_context_gate(direction="long", market_ctx=ctx, cfg=CFG) == ("ok", None)


def test_market_context_risk_off_blocks_long_not_short():
    ctx = {"status": "ok", "regime": "risk_off"}
    assert g.market_context_gate(direction="long", market_ctx=ctx, cfg=CFG)[0] == "conflict"
    assert g.market_context_gate(direction="short", market_ctx=ctx, cfg=CFG)[0] == "ok"


# ---- SI-2 sector ----
def test_classify_sector_conflict_and_confirmed():
    assert g.classify_sector(direction="long", sector_rth_return_pct=-0.5, sector_vs_vwap="below",
                             rs_vs_spy=1.0, rs_vs_sector=1.0, cfg=CFG) == "conflict"
    assert g.classify_sector(direction="long", sector_rth_return_pct=0.4, sector_vs_vwap="above",
                             rs_vs_spy=1.0, rs_vs_sector=0.5, cfg=CFG) == "confirmed"
    assert g.classify_sector(direction="long", sector_rth_return_pct=0.4, sector_vs_vwap="above",
                             rs_vs_spy=-1.0, rs_vs_sector=-0.5, cfg=CFG) == "weak"
    assert g.classify_sector(direction="long", sector_rth_return_pct=None, sector_vs_vwap="unknown",
                             rs_vs_spy=1.0, rs_vs_sector=1.0, cfg=CFG) == "unknown"


def test_sector_gate_weak_needs_catalyst():
    assert g.sector_confirmation_gate(direction="long", sector_ctx={"status": "weak"},
                                      catalyst_strong=False, cfg=CFG)[1] == "sector_confirmation_weak_or_unknown"
    assert g.sector_confirmation_gate(direction="long", sector_ctx={"status": "weak"},
                                      catalyst_strong=True, cfg=CFG)[1] is None
    assert g.sector_confirmation_gate(direction="long", sector_ctx={"status": "conflict"},
                                      catalyst_strong=True, cfg=CFG)[1] == "sector_confirmation_conflict"


def test_unknown_sector_can_use_bounded_pure_technical_route_but_weak_cannot():
    cfg = {**CFG, "allow_unknown_sector_for_pure_technical_ab": True}
    assert g.sector_confirmation_gate(direction="long", sector_ctx={"status": "unknown"},
                                      catalyst_strong=False, cfg=cfg) == ("provisional", None)
    assert g.sector_confirmation_gate(direction="long", sector_ctx={"status": "weak"},
                                      catalyst_strong=False, cfg=cfg)[1] == "sector_confirmation_weak_or_unknown"


# ---- SI-3 session ----
def test_session_gate_rules():
    assert g.session_gate(phase=g.OUTSIDE_RTH, setup_type="x", rvol_strong=True, catalyst_strong=True,
                          trend_continuation=True, cfg=CFG)[1] == "outside_rth"
    assert g.session_gate(phase=g.PREMARKET, setup_type="orb", rvol_strong=True, catalyst_strong=True,
                          trend_continuation=True, cfg=CFG)[1] == "premarket_watchlist_only"
    assert g.session_gate(phase=g.FIRST_15M, setup_type="pullback", rvol_strong=True, catalyst_strong=True,
                          trend_continuation=True, cfg=CFG)[1] == "first_15m_requires_orb_or_opening_drive"
    assert g.session_gate(phase=g.FIRST_15M, setup_type="opening_drive", rvol_strong=True,
                          catalyst_strong=False, trend_continuation=False, cfg=CFG) == ("ok", None)
    assert g.session_gate(phase=g.LUNCH, setup_type="x", rvol_strong=False, catalyst_strong=True,
                          trend_continuation=True, cfg=CFG)[1] == "lunch_requires_strong_confirmation"
    assert g.session_gate(phase=g.LAST_30M, setup_type="x", rvol_strong=True, catalyst_strong=True,
                          trend_continuation=False, cfg=CFG)[1] == "last_30m_requires_trend_continuation"
    assert g.session_gate(phase=g.MORNING, setup_type="x", rvol_strong=False, catalyst_strong=False,
                          trend_continuation=False, cfg=CFG) == ("ok", None)


# ---- SI-4 liquidity ----
def _liq(**kw):
    base = {"rvol": 2.0, "dollar_volume": 50_000_000, "spread_bps_est": 10,
            "data_freshness_status": "fresh", "data_gap_late": False}
    base.update(kw)
    return base


def test_liquidity_gate():
    assert g.liquidity_gate(liquidity=_liq(), cfg=CFG) == ("ok", None)
    assert g.liquidity_gate(liquidity=_liq(data_gap_late=True), cfg=CFG)[1] == "liquidity_data_gap_late"
    assert g.liquidity_gate(liquidity=_liq(data_freshness_status="stale"), cfg=CFG)[1] == "liquidity_data_stale"
    assert g.liquidity_gate(liquidity=_liq(rvol=1.0), cfg=CFG)[1] == "liquidity_rvol_below_min"
    assert g.liquidity_gate(liquidity=_liq(dollar_volume=1_000_000), cfg=CFG)[1] == "liquidity_dollar_volume_below_min"
    assert g.liquidity_gate(liquidity=_liq(spread_bps_est=None), cfg=CFG)[1] == "liquidity_spread_unknown"
    assert g.liquidity_gate(liquidity=_liq(spread_bps_est=100), cfg=CFG)[1] == "liquidity_spread_too_wide"
    # unknown spread allowed only when whitelisted AND config allows
    cfg2 = {**CFG, "allow_unknown_spread_for_liquid_names": True}
    assert g.liquidity_gate(liquidity=_liq(spread_bps_est=None, liquidity_whitelisted=True), cfg=cfg2) == ("ok", None)


# ---- SI-5 catalyst ----
def test_classify_catalyst_quality():
    assert g.classify_catalyst_quality(primary_type="earnings", age_minutes=30, source_count=2,
                                       source_quality="high", cfg=CFG) == "strong"
    assert g.classify_catalyst_quality(primary_type="analyst_action", age_minutes=30, source_count=1,
                                       source_quality="medium", cfg=CFG) == "medium"
    assert g.classify_catalyst_quality(primary_type="vague", age_minutes=30, source_count=1,
                                       source_quality="low", cfg=CFG) == "weak"
    assert g.classify_catalyst_quality(primary_type=None, age_minutes=None, source_count=0,
                                       source_quality="unknown", cfg=CFG) == "none"
    assert g.classify_catalyst_quality(primary_type="earnings", age_minutes=5000, source_count=2,
                                       source_quality="high", cfg=CFG) == "stale"


def test_catalyst_gate_rules():
    assert g.catalyst_gate(catalyst_quality="strong", market_confirmed=False, sector_confirmed=False,
                           rvol_strong=False, cfg=CFG) == ("ok", None)
    assert g.catalyst_gate(catalyst_quality="medium", market_confirmed=True, sector_confirmed=True,
                           rvol_strong=True, cfg=CFG) == ("ok", None)
    assert g.catalyst_gate(catalyst_quality="medium", market_confirmed=False, sector_confirmed=True,
                           rvol_strong=True, cfg=CFG)[1] == "catalyst_medium_without_full_confirmation"
    assert g.catalyst_gate(catalyst_quality="none", market_confirmed=True, sector_confirmed=True,
                           rvol_strong=True, cfg=CFG) == ("ok", None)
    assert g.catalyst_gate(catalyst_quality="weak", market_confirmed=False, sector_confirmed=True,
                           rvol_strong=True, cfg=CFG)[1].startswith("catalyst_weak")
    assert g.catalyst_gate(
        catalyst_quality="none", market_confirmed=True, sector_confirmed=True, rvol_strong=True,
        direction="short", setup_type="pullback", catalyst_direction_hint=None,
        catalyst_age_minutes=None, cfg=CFG,
    )[1] == "short_pullback_requires_fresh_bearish_catalyst"
    assert g.catalyst_gate(
        catalyst_quality="medium", market_confirmed=True, sector_confirmed=True, rvol_strong=True,
        direction="short", setup_type="pullback", catalyst_direction_hint="bearish",
        catalyst_age_minutes=20, cfg=CFG,
    ) == ("ok", None)


# ---- composer ----
def _clean_inputs():
    return dict(direction="long", phase=g.MORNING, setup_type="pullback",
                market_ctx={"status": "ok", "regime": "trend_up", "spy_rth_return_pct": 0.3,
                            "qqq_rth_return_pct": 0.4, "spy_vs_vwap": "above", "qqq_vs_vwap": "above"},
                sector_ctx={"status": "confirmed", "sector_etf": "XLK", "sector_rth_return_pct": 0.5,
                            "sector_vs_vwap": "above", "rs_vs_spy": 1.0, "rs_vs_sector": 0.5},
                liquidity={"rvol": 2.0, "dollar_volume": 60_000_000, "spread_bps_est": 8,
                           "data_freshness_status": "fresh", "data_gap_late": False},
                catalyst={"catalyst_quality": "strong", "catalyst_age_minutes": 20,
                          "catalyst_source_count": 2, "catalyst_primary_type": "earnings"})


def test_composer_clean_stays_ab():
    r = g.evaluate(**_clean_inputs(), cfg=CFG)
    assert r.decision == "AB" and r.demote_reasons == []
    assert r.fields["market_context_status"] == "ok" and r.fields["sector_confirmation_status"] == "confirmed"


def test_composer_market_conflict_demotes_to_c():
    inp = _clean_inputs()
    inp["market_ctx"] = {"status": "ok", "regime": "trend_down", "spy_rth_return_pct": -0.5,
                         "qqq_rth_return_pct": -0.6, "spy_vs_vwap": "below", "qqq_vs_vwap": "below"}
    r = g.evaluate(**inp, cfg=CFG)
    assert r.decision == "C" and "market_context_conflict" in r.demote_reasons


def test_composer_unknown_data_fails_conservative():
    inp = _clean_inputs()
    inp["market_ctx"] = {"status": "unknown"}
    inp["liquidity"] = {"data_freshness_status": "unknown"}
    r = g.evaluate(**inp, cfg=CFG)
    assert r.decision == "C"
    assert "market_context_unknown_or_stale" in r.demote_reasons


def test_composer_allows_clean_technical_when_only_sector_telemetry_is_unknown():
    inp = _clean_inputs()
    inp["catalyst"] = {"catalyst_quality": "none"}
    inp["sector_ctx"] = {"status": "unknown"}
    cfg = {**CFG, "allow_unknown_sector_for_pure_technical_ab": True}
    r = g.evaluate(**inp, cfg=cfg)
    assert r.decision == "AB"
    assert r.fields["sector_confirmation_status"] == "provisional"


def test_module_never_promotes_or_touches_live():
    # pure module: no DB, no orders, no live — check for actual CODE patterns (not docstring prose)
    import pathlib
    src = pathlib.Path(g.__file__).read_text(encoding="utf-8").lower()
    for bad in ("create_order(", "place_order(", "sqlite", ".execute(", "final_r =",
                "insert into", "update proposed_signals"):
        assert bad not in src, bad
