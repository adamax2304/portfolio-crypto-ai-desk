"""Crypto quality/risk overlay — PAPER / READ-MODEL soft breaker. Tests: never touches live/final_r,
missing data ≠ good, entry-mode + cooldown + exposure rules, no global score threshold, counterfactual.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta, timezone

import pandas as pd

from src.data_collectors import market_intelligence_store as mi
from src.execution import crypto_quality_overlay as cqo
from src.execution import crypto_overlay_counterfactual as cf
from src.execution.paper_live_exit_path import VERSION as LIVE_EXIT_PARITY_VERSION

CFG = cqo.load_cfg()
NOW = datetime(2026, 7, 8, 15, 0, tzinfo=timezone.utc)   # US session


def _mkt(status="ok", regime="uptrend", r15=0.3, r1h=0.5, slope="up", eth="uptrend"):
    return {"status": status, "btc_regime_state": regime, "btc_15m_return": r15, "btc_1h_return": r1h,
            "btc_ema_slope_state": slope, "eth_confirm_state": eth}


def _sym(rvol=2.0, funding="normal", spread=4.0, oi=0.05):
    return {"volume_rvol": rvol, "oi_change": oi, "funding_state": funding, "spread_bps": spread,
            "estimated_slippage_bps": 2.0}


def _sess(bucket="us", quality="ok"):
    return {"session_bucket_utc": bucket, "session_quality_state": quality}


def _cand(**kw):
    d = {"signal_id": "s", "symbol": "DOGE/USDT", "mode": "intraday", "side": "long", "score": 71,
         "entry_mode": "PULLBACK_LIMIT", "news_supported": 0, "timestamp": NOW.isoformat()}
    d.update(kw)
    return d


def _ex():
    return {"intraday_open": 0, "by_symbol_mode": {}, "alt_long": 0, "alt_short": 0}


def _ev(cand, mkt=None, sym=None, sess=None, cds=None, ex=None):
    return cqo.evaluate(cand, mkt or _mkt(), sym or _sym(), sess or _sess(), cds or {}, ex or _ex(), CFG)


# ---- guardrails ---------------------------------------------------------------------------------
def test_module_is_read_model_only():
    import pathlib
    for mod in (cqo, cf):
        src = pathlib.Path(mod.__file__).read_text(encoding="utf-8").lower()
        for bad in ("create_order(", "auto_live", "final_r =", "update signal_outcomes",
                    "update proposed_signals", "insert into proposed_signals", "insert into signal_outcomes"):
            assert bad not in src, f"{mod.__name__}: {bad}"


def test_live_is_hard_off_in_config():
    assert CFG.get("live_enabled") is False


def test_batch_entry_mode_map_uses_only_valid_preentry_rows(tmp_path):
    c = sqlite3.connect(tmp_path / "modes.sqlite")
    c.execute("CREATE TABLE signal_entry_mode (signal_id TEXT, entry_mode TEXT)")
    c.execute("CREATE TABLE signal_entry_mode_preentry (signal_id TEXT, entry_mode TEXT, data_quality TEXT)")
    c.execute("INSERT INTO signal_entry_mode VALUES ('a','LIMIT_THEN_TAKER_TIMEOUT')")
    c.execute("INSERT INTO signal_entry_mode_preentry VALUES ('a','PULLBACK_LIMIT','ok')")
    c.execute("INSERT INTO signal_entry_mode_preentry VALUES ('b','BREAKOUT_CONTINUATION','thin')")
    assert cqo._entry_mode_for(c) == {"a": "PULLBACK_LIMIT"}
    c.close()


def test_point_in_time_snapshot_is_append_once(tmp_path):
    db = str(tmp_path / "snapshot.sqlite")
    d = cqo.OverlayDecision(signal_id="s1", symbol="BTC/USDT", mode="intraday",
                            entry_mode="PULLBACK_LIMIT", action="HALF_SIZE",
                            ctx={"entry_mode_source": "entry_path", "preentry_data_quality": "ok"})
    assert cqo.persist_point_in_time_decision(d, db=db) is True
    d.action = "SHADOW_ONLY"
    assert cqo.persist_point_in_time_decision(d, db=db) is False
    c = sqlite3.connect(db)
    row = c.execute("SELECT quality_action, entry_mode_source, preentry_data_quality "
                    "FROM crypto_quality_overlay_decision_snapshots WHERE signal_id='s1'").fetchone()
    c.close()
    assert row == ("HALF_SIZE", "entry_path", "ok")


def test_observed_intraday_features_use_only_fully_closed_bars_and_do_not_route(tmp_path):
    timestamps = pd.date_range(end=NOW, periods=32, freq="15min", tz="UTC")
    frame = pd.DataFrame({
        "timestamp": timestamps,
        "open": [100 + index * 0.1 for index in range(len(timestamps))],
        "high": [100.5 + index * 0.1 for index in range(len(timestamps))],
        "low": [99.5 + index * 0.1 for index in range(len(timestamps))],
        "close": [100.2 + index * 0.1 for index in range(len(timestamps))],
        "volume": [10 + index for index in range(len(timestamps))],
    })

    class FS:
        def load_ohlcv(self, exchange, symbol, timeframe):
            assert (exchange, symbol, timeframe) == ("binance", "DOGE/USDT", "15m")
            return frame

    intelligence = tmp_path / "intelligence.sqlite"
    with mi.connect(intelligence) as conn:
        mi.insert_liquidity_snapshot(
            conn, provider_ts=(NOW - timedelta(minutes=1)).isoformat(), exchange="binance",
            symbol="DOGE/USDT", best_bid=100, best_ask=100.1, mid_price=100.05,
            spread_bps=10, bid_depth_10bps_usd=500, ask_depth_10bps_usd=600,
        )
        conn.commit()
    observed = cqo.symbol_context(FS(), "DOGE/USDT", "intraday", CFG, as_of=NOW, db=str(intelligence))
    # The row stamped exactly at NOW is still forming.  Its 15m close is not
    # eligible; the latest observed close must be the prior bar's close.
    assert observed["observed_price_bar_closed_at"] == NOW.isoformat()
    assert observed["observed_price_feature_status"] == "ok"
    assert observed["observed_atr14_pct"] is not None
    assert observed["observed_rvol20"] is not None
    assert observed["observed_liquidity_status"] == "ok"
    baseline = _ev(_cand())
    enriched = _ev(_cand(), sym={**_sym(), **observed})
    assert enriched.action == baseline.action
    fields = enriched.fields()
    assert fields["observed_atr14_pct"] == observed["observed_atr14_pct"]
    assert fields["observed_spread_bps"] == 10


# ---- missing data is never "good" ---------------------------------------------------------------
def test_unknown_market_data_not_treated_as_good():
    # primary pullback with unknown data → stays tradeable (not strangled) but confidence drops.
    d = _ev(_cand(entry_mode="PULLBACK_LIMIT"), mkt=_mkt(status="unknown", r15=None, r1h=None, regime="unknown"))
    assert "market_data_unknown" in d.reasons
    assert d.verdict in ("OK", "WEAK", "TOXIC")            # never STRONG on unknown
    # a RISKY entry mode with unknown data must NOT be full-size (unknown must not upgrade risk).
    d2 = _ev(_cand(entry_mode="BREAKOUT_CONTINUATION"),
             mkt=_mkt(status="unknown", r15=None, r1h=None, regime="unknown"))
    assert d2.action in ("HALF_SIZE", "SHADOW_ONLY")


def test_unknown_regime_label_is_not_confirmed_btc_weakness():
    # A usable BTC price feed can still yield an unclassified dashboard label.
    # That is uncertainty, not evidence that BTC is weak, and must not combine
    # with an exposure cap to force a healthy signal into Shadow.
    unknown_label = _mkt(status="ok", regime="unknown", r15=0.07, r1h=0.18, slope="up", eth="uptrend")
    assert cqo._btc_weak_confirmed(unknown_label, CFG) is False
    # Defend the semantic invariant even if a stale deployment config contains
    # the historical erroneous value.
    old_style_cfg = {**CFG, "regime": {**CFG["regime"], "btc_weak_states": ["risk_off", "unknown"]}}
    assert cqo._btc_weak_confirmed(unknown_label, old_style_cfg) is False
    assert cqo._btc_weak_confirmed(_mkt(regime="risk_off", r15=-0.3, r1h=-0.6, slope="down"), CFG) is True


def test_limit_then_taker_intraday_is_cautious_half_size_in_clean_context():
    # 2026-08-10 recalibration: LIMIT_THEN_TAKER_TIMEOUT was hard shadow_only, but the
    # point-in-time audit (n=26, avg_r=+1.286) showed it earning real paper edge while
    # locked out of any real weight. Downgraded to `cautious` -- baseline HALF_SIZE in a
    # clean context, same treatment as MOMENTUM_TAKER_NOW -- not a full FULL_SIZE trust.
    d = _ev(_cand(entry_mode="LIMIT_THEN_TAKER_TIMEOUT", **_FRESH_CATALYST))
    assert d.action == "HALF_SIZE"
    assert any("LIMIT_THEN_TAKER_TIMEOUT_cautious" in r for r in d.reasons)


def test_limit_then_taker_intraday_still_shadowed_on_a_confirmed_failing_tape():
    # The entry-mode floor is softer now, but the independent failing-tape regime guard
    # still explicitly names this entry mode and still forces SHADOW_ONLY -- the safety
    # net around a genuinely bad tape did not weaken.
    d = _ev(_cand(entry_mode="LIMIT_THEN_TAKER_TIMEOUT"),
            mkt=_mkt(r15=-0.3, r1h=-0.2, slope="down"), sym=_sym(rvol=1.0),
            sess=_sess("asia", "weak"))
    assert d.action == "SHADOW_ONLY"
    assert "intraday_regime_guard_failing_tape" in d.reasons


# Fresh catalyst remains a quality booster. It is not a universal requirement for technical
# PULLBACK_LIMIT / STRUCTURAL_RETEST entries.
_FRESH_CATALYST = dict(news_supported=1, catalyst_freshness="fresh", catalyst_strength="strong",
                       source_quality="reputable", symbol_mapping="exact")


# ---- no global score threshold ------------------------------------------------------------------
def test_no_global_score_threshold_intraday():
    # identical clean context, score 65 vs 73 → SAME action (score is not an intraday cutoff).
    good = _ev(_cand(score=65, **_FRESH_CATALYST))
    hi = _ev(_cand(score=73, **_FRESH_CATALYST))
    assert good.action == hi.action == "FULL_SIZE"


def test_intraday_65_66_not_auto_blocked():
    assert _ev(_cand(score=66, **_FRESH_CATALYST)).action == "FULL_SIZE"


# ---- entry-mode rules ---------------------------------------------------------------------------
def test_breakout_requires_strong_confirmation():
    # weak-but-known regime + no rvol → BREAKOUT is not full size.
    d = _ev(_cand(entry_mode="BREAKOUT_CONTINUATION"),
            mkt=_mkt(regime="chop"), sym=_sym(rvol=1.0))
    assert d.action in ("HALF_SIZE", "SHADOW_ONLY")
    # full confirmation → FULL.
    d2 = _ev(_cand(entry_mode="BREAKOUT_CONTINUATION", score=75, **_FRESH_CATALYST),
             mkt=_mkt(), sym=_sym(rvol=2.0))
    assert d2.action == "FULL_SIZE"


def test_pullback_primary_full_in_good_context():
    assert _ev(_cand(entry_mode="PULLBACK_LIMIT", **_FRESH_CATALYST)).action == "FULL_SIZE"


def test_high_volatility_trend_is_reduced_size_not_blocked():
    d = _ev(_cand(
        mode="swing",
        entry_mode="PULLBACK_LIMIT",
        market_regime="high-volatility trend",
        **_FRESH_CATALYST,
    ))
    assert d.action == "HALF_SIZE"
    assert "high_volatility_trend_reduced_size" in d.reasons


def test_intraday_weak_session_is_half_size_without_fresh_catalyst():
    d = _ev(_cand(entry_mode="PULLBACK_LIMIT"), sym=_sym(rvol=0.8), sess=_sess("asia", "weak"))
    assert d.action == "HALF_SIZE"
    assert any("intraday_weak_session_asia" in r for r in d.reasons)


def test_intraday_weak_session_fresh_catalyst_can_full_size():
    d = _ev(_cand(entry_mode="PULLBACK_LIMIT", news_supported=1,
                 catalyst_freshness="fresh", catalyst_strength="strong",
                 source_quality="reputable", symbol_mapping="exact"),
            sym=_sym(rvol=0.8), sess=_sess("asia", "weak"))
    assert d.action == "FULL_SIZE"
    assert any("intraday_weak_session_asia_confirmed" in r for r in d.reasons)


def test_intraday_weak_session_missing_mapping_is_not_fresh_catalyst():
    d = _ev(_cand(entry_mode="PULLBACK_LIMIT", news_supported=1,
                 catalyst_freshness="fresh", catalyst_strength="strong",
                 source_quality="reputable", symbol_mapping=""),
            sym=_sym(rvol=0.8), sess=_sess("asia", "weak"))
    assert d.action == "HALF_SIZE"
    assert any("intraday_weak_session_asia" in r for r in d.reasons)


def test_confirmed_btc_risk_off_blocks_new_intraday_long_paper_entry():
    d = _ev(_cand(entry_mode="PULLBACK_LIMIT", **_FRESH_CATALYST),
            mkt=_mkt(regime="risk_off", r15=-0.4, r1h=-0.8, slope="down"))
    assert d.action == "BLOCK"
    assert "intraday_btc_risk_off_long_block" in d.reasons


def test_technical_downtrend_alias_is_a_confirmed_risk_off_long_block():
    d = _ev(_cand(entry_mode="PULLBACK_LIMIT", **_FRESH_CATALYST),
            mkt=_mkt(regime="downtrend", r15=-0.4, r1h=-0.8, slope="down"))
    assert d.action == "BLOCK"
    assert "intraday_btc_risk_off_long_block" in d.reasons


def test_risk_off_gate_does_not_block_intraday_short_or_unknown_market_data():
    short = _ev(_cand(side="short", entry_mode="PULLBACK_LIMIT"),
                mkt=_mkt(regime="risk_off", r15=-0.4, r1h=-0.8, slope="down"))
    unknown = _ev(_cand(entry_mode="PULLBACK_LIMIT"),
                  mkt=_mkt(status="unknown", regime="risk_off", r15=None, r1h=None))
    assert "intraday_btc_risk_off_long_block" not in short.reasons
    assert "intraday_btc_risk_off_long_block" not in unknown.reasons


def test_risk_off_gate_is_reversible_by_config():
    disabled = dict(CFG, intraday_risk_off_gate={**CFG["intraday_risk_off_gate"], "enabled": False})
    d = cqo.evaluate(_cand(entry_mode="PULLBACK_LIMIT", **_FRESH_CATALYST),
                     _mkt(regime="risk_off", r15=-0.4, r1h=-0.8, slope="down"),
                     _sym(), _sess(), {}, _ex(), disabled)
    assert d.action == "FULL_SIZE"
    assert "intraday_btc_risk_off_long_block" not in d.reasons


def test_no_squeeze_intraday_cannot_be_full_without_confirmation():
    d = _ev(_cand(entry_mode="PULLBACK_LIMIT", derivatives_label="no-squeeze"),
            sym=_sym(rvol=0.8))
    assert d.action == "HALF_SIZE"
    assert any("derivatives_no_squeeze" in r for r in d.reasons)
    assert not any("cohort_guard" in r for r in d.reasons)


# ---- narrow cohort guard: unconfirmed breakout only; warn until forward evidence ----------------
def test_cohort_guard_default_is_warn_not_routing():
    assert CFG["cohort_guard"]["mode"] == "warn"
    d = _ev(_cand(entry_mode="BREAKOUT_CONTINUATION"),
            mkt=_mkt(regime="uptrend"), sym=_sym(rvol=1.0))
    assert d.action == "HALF_SIZE"  # existing entry-mode policy, not cohort shadow routing
    assert any("cohort_guard_warn" in r for r in d.reasons)
    assert not any("cohort_guard_review" in r for r in d.reasons)


def test_cohort_guard_never_touches_clean_pullback_or_structural_retest():
    pullback = _ev(_cand(entry_mode="PULLBACK_LIMIT"))
    structural = _ev(_cand(entry_mode="STRUCTURAL_RETEST"))
    assert pullback.action == structural.action == "FULL_SIZE"
    assert not any("cohort_guard" in r for r in pullback.reasons + structural.reasons)


def test_cohort_guard_paper_review_only_requires_second_routing_key():
    routing_cfg = dict(CFG, cohort_guard={**CFG["cohort_guard"], "mode": "paper_review_only",
                                         "routing_enabled": False})
    d = cqo.evaluate(_cand(entry_mode="BREAKOUT_CONTINUATION"),
                     _mkt(regime="uptrend"), _sym(rvol=1.0), _sess(), {}, _ex(), routing_cfg)
    assert d.action == "HALF_SIZE"
    assert any("cohort_guard_warn" in r for r in d.reasons)
    assert not any("cohort_guard_review" in r for r in d.reasons)


def test_cohort_guard_paper_review_only_is_narrow_and_reversible():
    routing_cfg = dict(CFG, cohort_guard={**CFG["cohort_guard"], "mode": "paper_review_only",
                                         "routing_enabled": True})
    d = cqo.evaluate(_cand(entry_mode="BREAKOUT_CONTINUATION"),
                     _mkt(regime="uptrend"), _sym(rvol=1.0), _sess(), {}, _ex(), routing_cfg)
    assert d.action == "SHADOW_ONLY"
    assert any("cohort_guard_review" in r for r in d.reasons)
    pullback = cqo.evaluate(_cand(entry_mode="PULLBACK_LIMIT"), _mkt(), _sym(), _sess(), {}, _ex(), routing_cfg)
    assert pullback.action == "FULL_SIZE"
    assert not any("cohort_guard" in r for r in pullback.reasons)


def test_cohort_guard_escapes_with_fresh_catalyst_or_strong_confirmation():
    fresh = _ev(_cand(entry_mode="BREAKOUT_CONTINUATION", **_FRESH_CATALYST),
                mkt=_mkt(regime="chop"), sym=_sym(rvol=1.0))
    assert not any("cohort_guard" in r for r in fresh.reasons)
    d = _ev(_cand(entry_mode="BREAKOUT_CONTINUATION"))
    assert d.action == "FULL_SIZE"
    assert not any("cohort_guard" in r for r in d.reasons)


def test_no_chase_skip_stays_shadow_via_entry_policy():
    # NO_CHASE_SKIP is unaffected by the 2026-08-10 LIMIT_THEN_TAKER_TIMEOUT recalibration --
    # it remains hard shadow_only (no forward evidence justified relaxing it).
    d = _ev(_cand(entry_mode="NO_CHASE_SKIP", **_FRESH_CATALYST))
    assert d.action == "SHADOW_ONLY"
    assert not any("cohort_guard" in r for r in d.reasons)


def test_cohort_guard_never_touches_shorts():
    # PLAYBOOK_CRYPTO_INTRADAY (the cohort this guard targets) is long-only in playbooks.py --
    # intraday shorts get PLAYBOOK_CRYPTO_FAILED_BOUNCE_SHORT, a different, unrelated cohort.
    d = _ev(_cand(side="short", entry_mode="BREAKOUT_CONTINUATION"),
            mkt=_mkt(regime="chop"), sym=_sym(rvol=1.0))
    assert not any("cohort_guard" in r for r in d.reasons)


def test_cohort_guard_never_touches_swing():
    d = _ev(_cand(mode="swing", score=72, entry_mode="BREAKOUT_CONTINUATION"),
            mkt=_mkt(regime="chop"), sym=_sym(rvol=1.0))
    assert not any("cohort_guard" in r for r in d.reasons)


def test_cohort_guard_disabled_is_a_noop():
    disabled_cfg = dict(CFG, cohort_guard={**CFG["cohort_guard"], "enabled": False})
    d = cqo.evaluate(_cand(entry_mode="BREAKOUT_CONTINUATION"), _mkt(regime="chop"),
                     _sym(rvol=1.0), _sess(), {}, _ex(), disabled_cfg)
    assert not any("cohort_guard" in r for r in d.reasons)


def test_cohort_guard_metadata_is_available_for_point_in_time_snapshot():
    d = _ev(_cand(entry_mode="BREAKOUT_CONTINUATION"),
            mkt=_mkt(regime="uptrend"), sym=_sym(rvol=1.0))
    f = d.fields()
    assert f["cohort_guard_policy_version"] == "cohort_guard_v2"
    assert f["cohort_guard_mode"] == "warn"
    assert f["cohort_guard_routing_enabled"] is False
    assert f["cohort_guard_in_scope"] is True
    assert f["cohort_guard_would_demote"] is True
    assert f["fresh_catalyst_confirmed"] is False


def _cohort_evidence_db(tmp_path, *, n: int, r_value: float, evidence="forward_postfreeze"):
    conn = sqlite3.connect(tmp_path / "cohort_evidence.sqlite")
    conn.execute("CREATE TABLE proposed_signals (signal_id TEXT, created_at TEXT, asset_class TEXT, "
                 "mode TEXT, direction TEXT)")
    conn.execute("CREATE TABLE paper_execution_outcomes (signal_id TEXT, paper_execution_r REAL, "
                 "paper_execution_outcome TEXT, evidence_class TEXT, economic_trade_key TEXT)")
    conn.execute("CREATE TABLE crypto_quality_overlay_decision_snapshots "
                 "(signal_id TEXT, decision_json TEXT, decision_context_type TEXT)")
    for i in range(n):
        sid = f"s{i}"
        decision = {"entry_mode": "BREAKOUT_CONTINUATION", "fresh_catalyst_confirmed": False,
                    "cohort_guard_policy_version": "cohort_guard_v2",
                    "cohort_guard_in_scope": True, "cohort_guard_would_demote": True}
        conn.execute("INSERT INTO proposed_signals VALUES (?,?,?,?,?)",
                     (sid, NOW.isoformat(), "crypto", "intraday", "long"))
        outcome = "loss" if r_value < 0 else "win"
        conn.execute("INSERT INTO paper_execution_outcomes VALUES (?,?,?,?,?)",
                     (sid, r_value, outcome, evidence, f"trade-{i}"))
        conn.execute("INSERT INTO crypto_quality_overlay_decision_snapshots VALUES (?,?,?)",
                     (sid, json.dumps(decision), "point_in_time"))
    return conn


def test_cohort_guard_evidence_requires_30_resolved_forward_rows(tmp_path):
    conn = _cohort_evidence_db(tmp_path, n=29, r_value=-1.0)
    result = cqo._cohort_guard_evidence(conn, CFG)
    conn.close()
    assert result["target"]["resolved"] == 29
    assert result["activation_verdict"] == "INSUFFICIENT_FORWARD_SAMPLE"


def test_cohort_guard_evidence_can_only_recommend_operator_review(tmp_path):
    conn = _cohort_evidence_db(tmp_path, n=30, r_value=-1.0)
    result = cqo._cohort_guard_evidence(conn, CFG)
    conn.close()
    assert result["target"]["profit_factor"] == 0.0
    assert result["target"]["avg_r"] < 0
    assert result["activation_verdict"] == "ELIGIBLE_FOR_OPERATOR_REVIEW"


# ---- swing vs intraday use different regime guards ----------------------------------------------
def test_swing_not_hit_by_intraday_failing_tape():
    failing = _mkt(regime="uptrend", r15=-0.5, r1h=-0.2, slope="down")
    intraday = _ev(_cand(mode="intraday", entry_mode="BREAKOUT_CONTINUATION"),
                   mkt=failing, sym=_sym(rvol=1.0), sess=_sess("asia", "weak"))
    swing = _ev(_cand(mode="swing", entry_mode="PULLBACK_LIMIT", score=72),
                mkt=failing, sym=_sym(rvol=1.0), sess=_sess("asia", "weak"))
    assert intraday.action in ("SHADOW_ONLY", "HALF_SIZE")     # intraday guard fires
    assert swing.action == "FULL_SIZE"                          # swing untouched by intraday tape guard


# ---- exposure guard -----------------------------------------------------------------------------
def _create_signal_alerts(conn):
    conn.execute("CREATE TABLE signal_alerts (signal_id TEXT, alert_type TEXT, telegram_status TEXT, "
                 "sent_at TEXT, payload_json TEXT)")


def _paper_alert(conn, signal_id, *, status="sent", action="FULL_SIZE", size_weight=1.0, minute=0):
    payload = {"cqo_quality_action": action, "size_weight": size_weight}
    conn.execute("INSERT INTO signal_alerts VALUES (?,?,?,?,?)",
                 (signal_id, "paper_entry", status,
                  (NOW + timedelta(minutes=minute)).isoformat(), json.dumps(payload)))


def test_exposure_alt_beta_same_direction_soft_downgrade():
    ex = {"intraday_open": 1, "by_symbol_mode": {}, "alt_long": 3, "alt_short": 0}
    d = _ev(_cand(symbol="PEPE/USDT", side="long"), ex=ex)
    assert d.action == "HALF_SIZE"
    assert any("alt_beta" in r for r in d.reasons)


def test_exposure_alt_beta_same_direction_is_shadow_only_when_btc_regime_is_weak_for_intraday():
    # 2026-08-10 hour-19-UTC root-cause fix: exposure-cap + weak/unknown regime together is
    # the toxic combination (8 of 9 real losers had both at once) -- a plain exposure hit
    # in a healthy regime (test above) stays HALF_SIZE, but the same exposure hit under a
    # weak/unknown BTC tape must be stricter.
    ex = {"intraday_open": 1, "by_symbol_mode": {}, "alt_long": 2, "alt_short": 0}
    d = _ev(_cand(symbol="PEPE/USDT", side="long"), mkt=_mkt(regime="chop"), ex=ex)
    assert d.action == "SHADOW_ONLY"
    assert any("alt_beta" in r for r in d.reasons)


def test_exposure_alt_beta_same_direction_is_half_size_for_swing_when_btc_regime_is_weak():
    # Swing already waits for higher-timeframe confirmation.  Weak BTC still
    # reduces risk, but does not route an otherwise fresh swing setup to Shadow.
    ex = {"intraday_open": 1, "by_symbol_mode": {}, "alt_long": 2, "alt_short": 0}
    d = _ev(_cand(symbol="PEPE/USDT", mode="swing", side="long"),
            mkt=_mkt(regime="chop"), ex=ex)
    assert d.action == "HALF_SIZE"
    assert any("alt_beta" in r for r in d.reasons)


def test_exposure_max_open_intraday_is_shadow_only_when_btc_regime_is_weak():
    ex = {"intraday_open": 4, "by_symbol_mode": {}, "alt_long": 0, "alt_short": 0}
    healthy = _ev(_cand(symbol="PEPE/USDT"), ex=ex)
    weak = _ev(_cand(symbol="PEPE/USDT"), mkt=_mkt(regime="chop"), ex=ex)
    assert healthy.action == "HALF_SIZE"
    assert weak.action == "SHADOW_ONLY"
    assert "exposure_max_open_intraday" in healthy.reasons and "exposure_max_open_intraday" in weak.reasons


def test_exposure_same_symbol_mode_conflict_shadow():
    ex = {"intraday_open": 1, "by_symbol_mode": {("DOGE/USDT", "intraday"): 1}, "alt_long": 0, "alt_short": 0}
    d = _ev(_cand(symbol="DOGE/USDT"), ex=ex)
    assert d.action == "SHADOW_ONLY"


def test_open_exposure_excludes_current_signal_but_keeps_other_positions(tmp_path):
    conn = sqlite3.connect(tmp_path / "exposure.sqlite")
    conn.execute("CREATE TABLE proposed_signals (signal_id TEXT, symbol TEXT, mode TEXT, direction TEXT, asset_class TEXT)")
    conn.execute("CREATE TABLE paper_execution_outcomes (signal_id TEXT, close_reason TEXT)")
    _create_signal_alerts(conn)
    conn.executemany("INSERT INTO proposed_signals VALUES (?,?,?,?,?)", [
        ("current", "DOGE/USDT", "intraday", "long", "crypto"),
        ("other", "SOL/USDT", "intraday", "long", "crypto"),
    ])
    conn.executemany("INSERT INTO paper_execution_outcomes VALUES (?,?)", [
        ("current", "open"), ("other", "open"),
    ])
    _paper_alert(conn, "current")
    _paper_alert(conn, "other", minute=1)

    with_self = cqo.open_exposure(conn)
    before_entry = cqo._exposure_without_current_signal(with_self, "current")
    conn.close()

    assert with_self["by_symbol_mode"][("DOGE/USDT", "intraday")] == 1
    assert with_self["alt_long"] == 2
    assert ("DOGE/USDT", "intraday") not in before_entry["by_symbol_mode"]
    assert before_entry["alt_long"] == 1
    assert before_entry["by_symbol_mode"][("SOL/USDT", "intraday")] == 1

    self_counted = _ev(_cand(signal_id="current"), ex=with_self)
    corrected = _ev(_cand(signal_id="current"), ex=before_entry)
    assert self_counted.action == "SHADOW_ONLY"
    assert "exposure_same_symbol_mode_conflict" in self_counted.reasons
    assert corrected.action == "FULL_SIZE"
    assert "exposure_same_symbol_mode_conflict" not in corrected.reasons


def test_open_exposure_counts_only_accepted_paper_positions(tmp_path):
    conn = sqlite3.connect(tmp_path / "accepted.sqlite")
    conn.execute("CREATE TABLE proposed_signals (signal_id TEXT, symbol TEXT, mode TEXT, direction TEXT, "
                 "asset_class TEXT, status TEXT)")
    conn.execute("CREATE TABLE paper_execution_outcomes (signal_id TEXT, close_reason TEXT, lifecycle_state TEXT)")
    _create_signal_alerts(conn)
    signals = [
        ("paper", "SOL/USDT", "intraday", "long", "crypto", "triggered"),
        ("half", "INJ/USDT", "intraday", "long", "crypto", "triggered"),
        ("shadow", "DOGE/USDT", "intraday", "long", "crypto", "triggered"),
        ("late", "XRP/USDT", "intraday", "long", "crypto", "triggered"),
        ("terminal", "ADA/USDT", "intraday", "long", "crypto", "stopped"),
    ]
    conn.executemany("INSERT INTO proposed_signals VALUES (?,?,?,?,?,?)", signals)
    conn.executemany("INSERT INTO paper_execution_outcomes VALUES (?,?,?)",
                     [(row[0], "open", "OPEN") for row in signals])
    _paper_alert(conn, "paper", action="FULL_SIZE", size_weight=1.0)
    _paper_alert(conn, "half", action="HALF_SIZE", size_weight=0.5, minute=1)
    _paper_alert(conn, "shadow", status="shadow_crypto_quality", action="SHADOW_ONLY",
                 size_weight=0.0, minute=2)
    # Requested HALF must not override the actual non-actionable routing result.
    _paper_alert(conn, "late", status="late_shadow", action="HALF_SIZE", size_weight=0.0, minute=3)
    _paper_alert(conn, "terminal", action="FULL_SIZE", size_weight=1.0, minute=4)

    exposure = cqo.open_exposure(conn)
    conn.close()

    assert exposure["raw_open_outcomes"] == 5
    assert exposure["actionable_open"] == 2
    assert exposure["intraday_open"] == 2
    assert exposure["alt_long"] == 2
    assert exposure["excluded_nonactionable"] == 2
    assert exposure["excluded_terminal"] == 1
    assert set(exposure["by_symbol_mode"]) == {
        ("SOL/USDT", "intraday"), ("INJ/USDT", "intraday")}


def test_shadow_rows_do_not_trigger_max_open_or_symbol_conflict(tmp_path):
    conn = sqlite3.connect(tmp_path / "shadow.sqlite")
    conn.execute("CREATE TABLE proposed_signals (signal_id TEXT, symbol TEXT, mode TEXT, direction TEXT, asset_class TEXT)")
    conn.execute("CREATE TABLE paper_execution_outcomes (signal_id TEXT, close_reason TEXT)")
    _create_signal_alerts(conn)
    for idx in range(4):
        sid = f"shadow-{idx}"
        symbol = "DOGE/USDT" if idx == 0 else f"ALT{idx}/USDT"
        conn.execute("INSERT INTO proposed_signals VALUES (?,?,?,?,?)",
                     (sid, symbol, "intraday", "long", "crypto"))
        conn.execute("INSERT INTO paper_execution_outcomes VALUES (?,?)", (sid, "open"))
        _paper_alert(conn, sid, status="shadow_only", action="SHADOW_ONLY", size_weight=0.0, minute=idx)
    conn.execute("INSERT INTO proposed_signals VALUES (?,?,?,?,?)",
                 ("paper", "SOL/USDT", "intraday", "long", "crypto"))
    conn.execute("INSERT INTO paper_execution_outcomes VALUES (?,?)", ("paper", "open"))
    _paper_alert(conn, "paper", status="sent", action="FULL_SIZE", size_weight=1.0, minute=5)

    exposure = cqo.open_exposure(conn)
    conn.close()
    decision = _ev(_cand(symbol="DOGE/USDT"), ex=exposure)

    assert exposure["raw_open_outcomes"] == 5
    assert exposure["intraday_open"] == 1
    assert exposure["alt_long"] == 1
    assert decision.action == "FULL_SIZE"
    assert not any(reason.startswith("exposure_") for reason in decision.reasons)
    fields = decision.fields()
    assert fields["paper_exposure_intraday_open"] == 1
    assert fields["paper_exposure_raw_open_outcomes"] == 5
    assert fields["paper_exposure_excluded_nonactionable"] == 4


def test_four_accepted_paper_positions_still_trigger_intraday_limit(tmp_path):
    conn = sqlite3.connect(tmp_path / "limit.sqlite")
    conn.execute("CREATE TABLE proposed_signals (signal_id TEXT, symbol TEXT, mode TEXT, direction TEXT, asset_class TEXT)")
    conn.execute("CREATE TABLE paper_execution_outcomes (signal_id TEXT, close_reason TEXT)")
    _create_signal_alerts(conn)
    for idx, symbol in enumerate(("BTC/USDT", "ETH/USDT", "SOL/USDT", "XRP/USDT")):
        sid = f"paper-{idx}"
        conn.execute("INSERT INTO proposed_signals VALUES (?,?,?,?,?)",
                     (sid, symbol, "intraday", "long", "crypto"))
        conn.execute("INSERT INTO paper_execution_outcomes VALUES (?,?)", (sid, "open"))
        _paper_alert(conn, sid, status="sent", action="FULL_SIZE", size_weight=1.0, minute=idx)
    exposure = cqo.open_exposure(conn)
    conn.close()
    decision = _ev(_cand(symbol="DOGE/USDT"), ex=exposure)
    assert exposure["intraday_open"] == 4
    assert decision.action == "HALF_SIZE"
    assert "exposure_max_open_intraday" in decision.reasons


def test_terminal_lifecycle_is_excluded_even_if_signal_status_is_not_terminal(tmp_path):
    conn = sqlite3.connect(tmp_path / "terminal.sqlite")
    conn.execute("CREATE TABLE proposed_signals (signal_id TEXT, symbol TEXT, mode TEXT, direction TEXT, asset_class TEXT)")
    conn.execute("CREATE TABLE paper_execution_outcomes (signal_id TEXT, close_reason TEXT, lifecycle_state TEXT)")
    _create_signal_alerts(conn)
    conn.execute("INSERT INTO proposed_signals VALUES (?,?,?,?,?)",
                 ("closed", "SOL/USDT", "intraday", "long", "crypto"))
    conn.execute("INSERT INTO paper_execution_outcomes VALUES (?,?,?)", ("closed", "open", "CLOSED"))
    _paper_alert(conn, "closed")
    exposure = cqo.open_exposure(conn)
    conn.close()
    assert exposure["intraday_open"] == 0
    assert exposure["excluded_terminal"] == 1


def test_refresh_excludes_current_open_signal_from_candidate_exposure(tmp_path, monkeypatch):
    db = str(tmp_path / "refresh.sqlite")
    conn = sqlite3.connect(db)
    conn.execute("CREATE TABLE proposed_signals (signal_id TEXT, symbol TEXT, mode TEXT, direction TEXT, "
                 "score REAL, news_supported INT, asset_class TEXT, created_at TEXT)")
    conn.execute("CREATE TABLE paper_execution_outcomes (signal_id TEXT, close_reason TEXT)")
    _create_signal_alerts(conn)
    conn.execute("INSERT INTO proposed_signals VALUES (?,?,?,?,?,?,?,?)",
                 ("current", "DOGE/USDT", "intraday", "long", 71, 0, "crypto", NOW.isoformat()))
    conn.execute("INSERT INTO paper_execution_outcomes VALUES (?,?)", ("current", "open"))
    _paper_alert(conn, "current")
    conn.commit()
    conn.close()

    seen = {}
    monkeypatch.setattr(cqo, "refresh_cooldowns", lambda **_kwargs: {})
    monkeypatch.setattr(cqo, "read_cooldowns", lambda *_args, **_kwargs: {})
    monkeypatch.setattr(cqo, "market_context", lambda *_args, **_kwargs: _mkt())
    monkeypatch.setattr(cqo, "symbol_context", lambda *_args, **_kwargs: _sym())
    monkeypatch.setattr(cqo, "session_bucket", lambda *_args, **_kwargs: "us")
    monkeypatch.setattr(cqo, "session_quality", lambda *_args, **_kwargs: "ok")

    def fake_evaluate(cand, _mkt_ctx, _sym_ctx, _session, _cooldowns, exposure, _cfg):
        seen[cand["signal_id"]] = exposure
        return cqo.OverlayDecision(signal_id=cand["signal_id"], action="FULL_SIZE")

    monkeypatch.setattr(cqo, "evaluate", fake_evaluate)
    cqo.refresh(db=db, now_iso=NOW.isoformat(), persist=False)

    assert ("DOGE/USDT", "intraday") not in seen["current"]["by_symbol_mode"]
    assert seen["current"]["alt_long"] == 0


# ---- cooldown row logic -------------------------------------------------------------------------
def _recs(closes, r=-1.0, usd=-30.0, base=NOW):
    return [{"close": c, "r": (r if c == "original_stop" else 0.0), "usd": usd,
             "t": base - timedelta(minutes=10 * i)} for i, c in enumerate(closes)]


def test_session_cooldown_triggers_on_3_consecutive_stops_after_minimum_sample():
    recs = _recs(["original_stop", "original_stop", "original_stop", "breakeven_stop", "tp3_runner"], r=-0.2)
    recs[-1]["r"] = 1.5
    row = cqo._session_cooldown_row("intraday", "us", sorted(recs, key=lambda x: x["t"]),
                                    CFG["session_cooldown"], NOW.isoformat())
    assert row["cooldown_active"] == 1
    assert "streak_3_original_stops_last_5" in row["cooldown_reason"]
    assert row["cooldown_expires_at"] == (NOW + timedelta(hours=4)).isoformat()


def test_session_cooldown_does_not_trigger_on_three_stops_below_minimum_sample():
    recs = _recs(["original_stop", "original_stop", "original_stop"])
    row = cqo._session_cooldown_row("intraday", "us", sorted(recs, key=lambda x: x["t"]),
                                    CFG["session_cooldown"], NOW.isoformat())
    assert row["cooldown_active"] == 0


def test_symbol_cooldown_triggers_on_2_stops():
    recs = _recs(["original_stop", "tp3_runner", "original_stop"])
    row = cqo._symbol_cooldown_row("DOGE/USDT", "intraday", recs, CFG["symbol_cooldown"], NOW.isoformat())
    assert row["cooldown_active"] == 1


def test_symbol_cooldown_profitable_override_suppresses_cooldown():
    # 2026-07-13 audit: ETH/WLD/ALLO-style case -- meets the 2-stop trigger but the symbol is still
    # net-profitable overall (winners outweigh the stops), so it must NOT be cooled down.
    recs = [
        {"close": "original_stop", "r": -1.0, "usd": -30.0, "t": NOW - timedelta(minutes=10)},
        {"close": "original_stop", "r": -1.0, "usd": -30.0, "t": NOW - timedelta(minutes=20)},
        {"close": "tp3_runner", "r": 3.0, "usd": 200.0, "t": NOW - timedelta(minutes=30)},
    ]
    row = cqo._symbol_cooldown_row("ETH/USDT", "intraday", recs, CFG["symbol_cooldown"], NOW.isoformat())
    assert row["cooldown_active"] == 0
    assert row["recent_net_pnl_usd"] > 0


def test_symbol_cooldown_min_sample_suppresses_on_tiny_window():
    # 2 stops out of exactly 2 trades (n below min_sample=3) isn't enough signal yet to distinguish
    # a real problem from noise -- must not trigger.
    recs = [
        {"close": "original_stop", "r": -1.0, "usd": -30.0, "t": NOW - timedelta(minutes=10)},
        {"close": "original_stop", "r": -1.0, "usd": -30.0, "t": NOW - timedelta(minutes=20)},
    ]
    row = cqo._symbol_cooldown_row("NEWCOIN/USDT", "intraday", recs, CFG["symbol_cooldown"], NOW.isoformat())
    assert row["cooldown_active"] == 0
    assert row["recent_closed_count"] < int(CFG["symbol_cooldown"].get("min_sample", 3))


def test_session_bucket_off_key_is_string_not_boolean():
    # config/crypto_quality_overlay.yaml's unquoted `off:` key is a YAML 1.1 bareword-boolean trap
    # (parses to Python False, same family as on/yes/no) unless explicitly quoted "off". Assert the
    # loaded config and session_bucket()'s return value are both the real string "off".
    buckets = CFG["session"]["buckets"]
    assert "off" in buckets and all(isinstance(k, str) for k in buckets.keys())
    late = datetime(2026, 7, 8, 22, 0, tzinfo=timezone.utc)   # 22:00 UTC falls in the off bucket
    assert cqo.session_bucket(late, CFG) == "off"
    assert cqo.session_bucket(late, CFG) is not False


def test_session_cooldown_downgrades_new_signal():
    cds = {("session", "intraday", "us"): {"reason": "streak_3_original_stops_last_5", "expires": None}}
    d = _ev(_cand(), cds=cds)
    assert d.action == "HALF_SIZE"
    assert any("session_cooldown" in r for r in d.reasons)


def test_symbol_cooldown_downgrades_and_strong_confirmation_bypasses():
    cds = {("symbol", "DOGE/USDT", "intraday"): {"reason": "2_original_stops_in_window", "expires": None}}
    weak = _ev(_cand(score=66), mkt=_mkt(regime="chop"), sym=_sym(rvol=1.0), cds=cds)
    assert weak.action in ("HALF_SIZE", "SHADOW_ONLY")
    strong = _ev(_cand(score=75), mkt=_mkt(), sym=_sym(rvol=2.0), cds=cds)
    assert "cooldown_bypassed_by_strong_confirmation" in strong.reasons   # traded, reason recorded


def test_symbol_cooldown_three_stops_only_reduces_size_during_paper_testing():
    cds = {("symbol", "DOGE/USDT", "intraday"): {"reason": "3_original_stops_in_window", "expires": None}}
    d = _ev(_cand(score=75), mkt=_mkt(), sym=_sym(rvol=2.0), cds=cds)
    assert d.action == "HALF_SIZE"
    assert any("symbol_cooldown_severe" in r for r in d.reasons)


# ---- integration: refresh_cooldowns + counterfactual on a temp DB -------------------------------
def _seed_db(tmp_path):
    db = str(tmp_path / "cqo.sqlite")
    c = sqlite3.connect(db)
    c.execute("CREATE TABLE proposed_signals (signal_id TEXT, symbol TEXT, mode TEXT, direction TEXT, "
              "score REAL, news_supported INT, asset_class TEXT, created_at TEXT)")
    c.execute("CREATE TABLE paper_execution_outcomes (signal_id TEXT, economic_trade_key TEXT, close_reason TEXT, "
              "paper_execution_r REAL, paper_execution_outcome TEXT, computed_at TEXT, exit_at TEXT, "
              "evidence_class TEXT, execution_validity TEXT)")
    c.execute("CREATE TABLE paper_portfolio_ledger (signal_id TEXT, event_type TEXT, net_pnl_usdt REAL, "
              "timestamp TEXT, created_at TEXT, fee_profile TEXT)")
    base = NOW - timedelta(hours=2)
    for i, close in enumerate(["original_stop", "original_stop", "original_stop"]):
        sid = f"c{i}"
        ts = (base + timedelta(minutes=15 * i)).isoformat()
        c.execute("INSERT INTO proposed_signals VALUES (?,?,?,?,?,?,?,?)",
                  (sid, "DOGE/USDT", "intraday", "long", 68, 0, "crypto", ts))
        c.execute("INSERT INTO paper_execution_outcomes VALUES (?,?,?,?,?,?,?,?,?)",
                  (sid, sid, close, -1.0, "loss", NOW.isoformat(), ts, "forward_postfreeze", "valid"))
        c.execute("INSERT INTO paper_portfolio_ledger VALUES (?,?,?,?,?,?)",
                  (sid, "exit", -30.0, ts, None, "bybit_non_vip_usdt_perp"))
    c.commit(); c.close()
    return db


def test_refresh_cooldowns_writes_only_its_table_and_flags_symbol(tmp_path):
    db = _seed_db(tmp_path)
    res = cqo.refresh_cooldowns(db=db, now_iso=NOW.isoformat())
    assert res["symbols_on_cooldown"] >= 1                 # 3 stops on DOGE/intraday
    c = sqlite3.connect(db)
    # invariants: source tables untouched
    assert c.execute("SELECT COUNT(*) FROM proposed_signals").fetchone()[0] == 3
    assert c.execute("SELECT COUNT(*) FROM paper_execution_outcomes").fetchone()[0] == 3
    assert c.execute("SELECT 1 FROM sqlite_master WHERE name='crypto_quality_cooldowns'").fetchone()
    c.close()


def test_refresh_cooldowns_ignores_old_recomputed_and_backfill_rows_and_deduplicates_trade_keys(tmp_path):
    db = str(tmp_path / "cooldown_source.sqlite")
    c = sqlite3.connect(db)
    c.execute("CREATE TABLE proposed_signals (signal_id TEXT, symbol TEXT, mode TEXT, asset_class TEXT)")
    c.execute("CREATE TABLE paper_execution_outcomes (signal_id TEXT, economic_trade_key TEXT, close_reason TEXT, "
              "paper_execution_r REAL, exit_at TEXT, computed_at TEXT, evidence_class TEXT, execution_validity TEXT)")
    for index in range(3):
        sid = f"old{index}"
        c.execute("INSERT INTO proposed_signals VALUES (?,?,?,?)", (sid, "DOGE/USDT", "intraday", "crypto"))
        c.execute("INSERT INTO paper_execution_outcomes VALUES (?,?,?,?,?,?,?,?)",
                  (sid, sid, "original_stop", -1.0, (NOW - timedelta(days=3)).isoformat(), NOW.isoformat(),
                   "forward_postfreeze", "valid"))
    c.execute("INSERT INTO proposed_signals VALUES (?,?,?,?)", ("backfill", "ETH/USDT", "intraday", "crypto"))
    c.execute("INSERT INTO paper_execution_outcomes VALUES (?,?,?,?,?,?,?,?)",
              ("backfill", "backfill", "original_stop", -1.0, (NOW - timedelta(minutes=1)).isoformat(),
               NOW.isoformat(), "backfill_pretrained", "valid"))
    for index in range(5):
        sid = f"dupe{index}"
        c.execute("INSERT INTO proposed_signals VALUES (?,?,?,?)", (sid, "SOL/USDT", "intraday", "crypto"))
        c.execute("INSERT INTO paper_execution_outcomes VALUES (?,?,?,?,?,?,?,?)",
                  (sid, "one-economic-trade", "original_stop", -1.0,
                   (NOW - timedelta(minutes=index + 1)).isoformat(), NOW.isoformat(),
                   "forward_postfreeze", "valid"))
    c.commit(); c.close()

    res = cqo.refresh_cooldowns(db=db, now_iso=NOW.isoformat())
    assert res["session_cooldown"] is False
    assert res["symbols_on_cooldown"] == 0


def test_refresh_cooldowns_ignores_pre_incremental_paper_versions(tmp_path):
    db = str(tmp_path / "cooldown_version.sqlite")
    c = sqlite3.connect(db)
    c.execute("CREATE TABLE proposed_signals (signal_id TEXT, symbol TEXT, mode TEXT, asset_class TEXT)")
    c.execute(
        "CREATE TABLE paper_execution_outcomes (signal_id TEXT, economic_trade_key TEXT, "
        "close_reason TEXT, paper_execution_r REAL, exit_at TEXT, evidence_class TEXT, "
        "execution_validity TEXT, version TEXT)"
    )
    for index in range(5):
        sid = f"legacy{index}"
        c.execute("INSERT INTO proposed_signals VALUES (?,?,?,?)", (sid, "DOGE/USDT", "intraday", "crypto"))
        c.execute(
            "INSERT INTO paper_execution_outcomes VALUES (?,?,?,?,?,?,?,?)",
            (sid, sid, "original_stop", -1.0,
             (NOW - timedelta(minutes=index + 1)).isoformat(),
             "forward_postfreeze", "valid", "live_exit_parity_v2"),
        )
    c.commit()
    cfg = cqo.load_cfg()
    assert cqo.compute_cooldowns(c, cfg, NOW) == []
    c.execute("UPDATE paper_execution_outcomes SET version=?", (LIVE_EXIT_PARITY_VERSION,))
    current = cqo.compute_cooldowns(c, cfg, NOW)
    c.close()
    assert any(row["cooldown_active"] for row in current)


def test_counterfactual_computes_avoided_loss_and_missed_runner(tmp_path):
    db = str(tmp_path / "cf.sqlite")
    c = sqlite3.connect(db)
    c.execute("CREATE TABLE proposed_signals (signal_id TEXT, symbol TEXT, mode TEXT, direction TEXT, "
              "score REAL, news_supported INT, asset_class TEXT, created_at TEXT)")
    c.execute("CREATE TABLE paper_execution_outcomes (signal_id TEXT, close_reason TEXT, "
              "paper_execution_r REAL, paper_execution_outcome TEXT, computed_at TEXT)")
    c.execute("CREATE TABLE paper_portfolio_ledger (signal_id TEXT, event_type TEXT, net_pnl_usdt REAL, "
              "timestamp TEXT, created_at TEXT, fee_profile TEXT)")
    c.execute("CREATE TABLE signal_outcomes (signal_id TEXT, max_favorable_excursion_r REAL)")
    # a NO_CHASE_SKIP loser (still hard shadow_only -- unaffected by the 2026-08-10
    # LIMIT_THEN_TAKER_TIMEOUT recalibration below -- overlay SHADOWs -> avoids the full loss).
    # The batch overlay accepts only the pre-entry, valid label.
    c.execute("CREATE TABLE signal_entry_mode_preentry (signal_id TEXT, entry_mode TEXT, data_quality TEXT)")
    ts = (NOW - timedelta(hours=1)).isoformat()
    c.execute("INSERT INTO proposed_signals VALUES ('L','DOGE/USDT','intraday','long',70,0,'crypto',?)", (ts,))
    c.execute("INSERT INTO paper_execution_outcomes VALUES ('L','original_stop',-1.0,'loss',?)", (ts,))
    c.execute("INSERT INTO paper_portfolio_ledger VALUES ('L','exit',-40.0,?,NULL,'bybit_non_vip_usdt_perp')", (ts,))
    c.execute("INSERT INTO signal_entry_mode_preentry VALUES ('L','NO_CHASE_SKIP','ok')")
    c.commit(); c.close()
    res = cf.refresh(db=db, now_iso=NOW.isoformat())
    assert res["with_usd"] == 1
    # NO_CHASE_SKIP intraday → SHADOW → the −40 loss is avoided; net delta positive.
    assert res["avoided_loss_usd"] >= 40.0
    assert res["net_overlay_delta_usd"] >= 0
    c = sqlite3.connect(db)
    row = c.execute("SELECT overlay_action, avoided_loss_usd, overlay_would_have_reduced_loser "
                    "FROM crypto_quality_counterfactual WHERE signal_id='L'").fetchone()
    # invariant: source outcome untouched
    assert c.execute("SELECT paper_execution_r FROM paper_execution_outcomes WHERE signal_id='L'").fetchone()[0] == -1.0
    c.close()
    assert row[0] in ("SHADOW_ONLY", "BLOCK") and row[1] >= 40.0 and row[2] == 1


def test_counterfactual_limit_then_taker_now_only_partially_avoids_loss(tmp_path):
    # 2026-08-10 recalibration: LIMIT_THEN_TAKER_TIMEOUT is now `cautious` (HALF_SIZE
    # baseline), not hard shadow_only -- the counterfactual should reflect a partial
    # (size_weight=0.5), not full, avoided loss for this specific entry mode now.
    db = str(tmp_path / "cf2.sqlite")
    c = sqlite3.connect(db)
    c.execute("CREATE TABLE proposed_signals (signal_id TEXT, symbol TEXT, mode TEXT, direction TEXT, "
              "score REAL, news_supported INT, asset_class TEXT, created_at TEXT)")
    c.execute("CREATE TABLE paper_execution_outcomes (signal_id TEXT, close_reason TEXT, "
              "paper_execution_r REAL, paper_execution_outcome TEXT, computed_at TEXT)")
    c.execute("CREATE TABLE paper_portfolio_ledger (signal_id TEXT, event_type TEXT, net_pnl_usdt REAL, "
              "timestamp TEXT, created_at TEXT, fee_profile TEXT)")
    c.execute("CREATE TABLE signal_outcomes (signal_id TEXT, max_favorable_excursion_r REAL)")
    c.execute("CREATE TABLE signal_entry_mode_preentry (signal_id TEXT, entry_mode TEXT, data_quality TEXT)")
    ts = (NOW - timedelta(hours=1)).isoformat()
    c.execute("INSERT INTO proposed_signals VALUES ('L2','DOGE/USDT','intraday','long',70,0,'crypto',?)", (ts,))
    c.execute("INSERT INTO paper_execution_outcomes VALUES ('L2','original_stop',-1.0,'loss',?)", (ts,))
    c.execute("INSERT INTO paper_portfolio_ledger VALUES ('L2','exit',-40.0,?,NULL,'bybit_non_vip_usdt_perp')", (ts,))
    c.execute("INSERT INTO signal_entry_mode_preentry VALUES ('L2','LIMIT_THEN_TAKER_TIMEOUT','ok')")
    c.commit(); c.close()
    res = cf.refresh(db=db, now_iso=NOW.isoformat())
    assert res["with_usd"] == 1
    c = sqlite3.connect(db)
    row = c.execute("SELECT overlay_action, avoided_loss_usd FROM crypto_quality_counterfactual "
                    "WHERE signal_id='L2'").fetchone()
    c.close()
    assert row[0] == "HALF_SIZE"
    assert 0.0 < row[1] < 40.0


def test_counterfactual_slices_forward_usd_by_mode_side_and_reason():
    rows = [
        {"signal_id": "i1", "mode": "intraday", "side": "long", "bucket": "us",
         "reasons": ["btc_regime_weak"], "base_usd": -20.0, "over_usd": -10.0,
         "avoided": 10.0, "missed": 0.0, "delta": 10.0, "close": "original_stop",
         "overlay_action": "HALF_SIZE", "r": -1.0, "wspp": (0.0, 0.0, 0.0),
         "evidence_class": "forward_postfreeze", "t": NOW - timedelta(hours=2)},
        {"signal_id": "s1", "mode": "swing", "side": "short", "bucket": "us",
         "reasons": ["funding_against"], "base_usd": 30.0, "over_usd": 15.0,
         "avoided": 0.0, "missed": 15.0, "delta": -15.0, "close": "tp3_runner",
         "overlay_action": "HALF_SIZE", "r": 2.0, "wspp": (0.0, 0.0, 0.0),
         "evidence_class": "forward_postfreeze", "t": NOW - timedelta(hours=1)},
    ]
    result = cf._summary_with_slices(rows, NOW, 7)
    assert result["forward_net_overlay_delta_usd"] == -5.0
    assert result["by_mode_side"]["intraday:long"]["forward_net_overlay_delta_usd"] == 10.0
    assert result["by_mode_side"]["swing:short"]["forward_net_overlay_delta_usd"] == -15.0
    assert result["reason_effect_forward"]["btc_regime_weak"]["delta_usd"] == 10.0


def test_ui_report_data_returns_quality_fields(tmp_path):
    db = _seed_db(tmp_path)
    cqo.refresh(db=db, now_iso=NOW.isoformat())
    data = cqo.report_data(db=db, now_iso=NOW.isoformat())
    assert "action_mix" in data and "overlay_version" in data
    assert "active_symbol_cooldowns" in data
