"""Focused crypto intraday experiments: strict source and guardrail tests."""
from __future__ import annotations

import sqlite3

import pandas as pd

from src.execution import crypto_intraday_idea_sweep as sweep


def _candles(with_volume=True):
    rows = [
        {"timestamp": "2026-07-13T12:00:00Z", "open": 101, "high": 101, "low": 99.4, "close": 100,
         "volume": 10 if with_volume else None},
        {"timestamp": "2026-07-13T12:05:00Z", "open": 100, "high": 101, "low": 99.8, "close": 100.2,
         "volume": 20 if with_volume else None},
        {"timestamp": "2026-07-13T12:10:00Z", "open": 100.2, "high": 101.5, "low": 100.1, "close": 101.2,
         "volume": 30 if with_volume else None},
    ]
    return pd.DataFrame(rows)


def _geom():
    return {"direction": "long", "entry_low": 99.5, "entry_high": 100.5,
            "entry_trigger": 100.5, "entry": 100.0, "stop": 98.0,
            "tp1": 104.0, "tp2": 106.0, "tp3": 110.0,
            "entry_mode": "PULLBACK_LIMIT", "symbol": "BTC/USDT"}


def test_confirmation_starts_after_closed_confirmation_bar():
    out = sweep.pullback_confirmation_gate(_geom(), _candles(), "level_hold")
    assert out["eligible"] is True
    # first bar touches, second bar confirms, third bar is the first simulated entry bar
    assert out["start_index"] == 2


def test_level_hold_1bar_public_variant_is_supported():
    out = sweep.pullback_confirmation_gate(_geom(), _candles(), "level_hold_1bar")
    assert out["eligible"] is True
    assert out["reason"] == "confirmed"
    assert out["confirmation_price"] == 100.2
    assert out["confirmation_at"] == "2026-07-13T12:10:00+00:00"


def test_level_hold_v2_requires_a_strong_mid_zone_reclaim():
    candles = _candles()
    candles.loc[1, ["open", "high", "low", "close"]] = [99.8, 100.9, 99.7, 100.7]
    out = sweep.pullback_confirmation_gate(_geom(), candles, "level_hold_v2")
    assert out["eligible"] is True
    assert out["max_retest_bars"] == 3


def test_vwap_requires_volume():
    out = sweep.pullback_confirmation_gate(_geom(), _candles(with_volume=False), "vwap_hold_1bar")
    assert out == {"eligible": False, "start_index": None, "reason": "vwap_volume_unavailable"}


def test_vwap_confirm_close_is_distinct_from_confirm_then_retest():
    candles = pd.DataFrame([
        {"timestamp": "2026-07-13T12:00:00Z", "open": 101.0, "high": 101.0,
         "low": 99.4, "close": 100.0, "volume": 10},
        {"timestamp": "2026-07-13T12:05:00Z", "open": 100.0, "high": 101.2,
         "low": 99.8, "close": 101.0, "volume": 20},
        # No later pullback-zone retest, but a confirmation-close entry reaches all targets.
        {"timestamp": "2026-07-13T12:10:00Z", "open": 101.1, "high": 111.0,
         "low": 100.8, "close": 110.0, "volume": 30},
    ])
    close_entry = sweep._simulate(
        _geom(), candles, "vwap_confirm_close", fee_profile="bybit_non_vip_usdt_perp", size_weight=1.0)
    later_retest = sweep._simulate(
        _geom(), candles, "vwap_hold_1bar", fee_profile="bybit_non_vip_usdt_perp", size_weight=1.0)
    assert close_entry["status"] == "resolved"
    assert close_entry["entry_rule"] == "confirmation_close_taker"
    assert close_entry["entry_price"] == 101.0
    assert close_entry["entry_bar_at"] == "2026-07-13T12:10:00+00:00"
    assert later_retest["status"] == "skipped"
    assert later_retest["skip_reason"] == "no_fill"
    assert later_retest["entry_rule"] == "confirmation_then_limit_retest"


def test_vwap_confirm_close_rejects_targets_already_behind_entry():
    geom = _geom()
    geom.update(tp1=100.5, tp2=100.8, tp3=101.0)
    candles = _candles()
    candles.loc[1, "close"] = 101.0
    out = sweep._simulate(
        geom, candles, "vwap_confirm_close",
        fee_profile="bybit_non_vip_usdt_perp", size_weight=1.0)
    assert out["status"] == "skipped"
    assert out["skip_reason"] == "invalid_confirmed_close_geometry"


def test_strict_level_hold_requires_mid_zone_body_and_short_retest_window():
    candles = _candles()
    # The touch is followed by a weak reclaim inside the zone: strict midpoint
    # confirmation must reject it instead of crediting a later limit fill.
    candles.loc[1, ["open", "high", "low", "close"]] = [100.1, 100.6, 99.8, 100.2]
    gate = sweep.pullback_confirmation_gate(_geom(), candles, "level_hold_mid_zone_retest_2bar")
    assert gate["eligible"] is False
    assert gate["reason"] in {"confirmation_failed", "confirmation_candle_too_weak"}


def test_strict_hold_retest_expires_instead_of_filling_late():
    candles = pd.DataFrame([
        {"timestamp": f"2026-07-13T12:{minute:02d}:00Z", "open": 101.0, "high": 101.5,
         "low": low, "close": close, "volume": 100.0}
        for minute, low, close in ((0, 99.4, 100.0), (5, 99.8, 100.9), (10, 101.0, 101.2),
                                       (15, 101.0, 101.3), (20, 101.0, 101.4), (25, 100.0, 101.1))
    ])
    candles.loc[1, "open"] = 99.9
    out = sweep._simulate(
        _geom(), candles, "level_hold_mid_zone_retest_2bar",
        fee_profile="bybit_non_vip_usdt_perp", size_weight=1.0,
    )
    assert out["status"] == "skipped"
    assert out["skip_reason"] == "retest_expired"


def test_light_quality_gate_fails_closed_on_missing_snapshot_fields():
    allowed, reason = sweep._light_hold_quality({"direction": "long", "quality_action": "FULL_SIZE"})
    assert allowed is False
    assert reason == "btc_slope_not_aligned"


def test_shadow_filter_variants_only_exclude_explicit_bad_states():
    assert sweep._shadow_filter_state({"btc_regime_state": "risk_off"}, "risk_off_veto_shadow") == (
        "exclude", "shadow_btc_risk_off")
    assert sweep._shadow_filter_state({"btc_regime_state": "uptrend"}, "risk_off_veto_shadow") == ("pass", None)
    assert sweep._shadow_filter_state({}, "risk_off_veto_shadow") == ("unavailable", "btc_regime_feature_unavailable")
    assert sweep._shadow_filter_state(
        {"derivatives_status": "ok", "oi_price_regime": "unknown"}, "oi_unknown_veto_shadow"
    ) == ("exclude", "shadow_oi_regime_unclassified")
    assert sweep._shadow_filter_state(
        {"observed_price_feature_status": "ok", "observed_atr14_pct": 2.51}, "high_atr_veto_shadow"
    ) == ("exclude", "shadow_atr14_over_2_5pct")
    assert sweep._shadow_filter_state(
        {"observed_price_feature_status": "ok", "observed_rvol20": 0.49}, "low_rvol_veto_shadow"
    ) == ("exclude", "shadow_rvol20_below_0_5")
    assert sweep._shadow_filter_state(
        {"strong_confirmation": 1, "direction": "long", "btc_ema_slope_state": "up",
         "observed_vwap20_distance_pct": 0.05},
        "breakout_15m_vwap_btc_quality_shadow",
    ) == ("pass", None)
    assert sweep._shadow_filter_state(
        {"strong_confirmation": 1, "direction": "long", "btc_ema_slope_state": "up",
         "observed_vwap20_distance_pct": -0.2},
        "breakout_15m_vwap_btc_quality_shadow",
    ) == ("exclude", "breakout_lost_vwap_support")
    assert sweep._shadow_filter_state(
        {"strong_confirmation": 1, "direction": "long", "btc_ema_slope_state": "unknown"},
        "breakout_15m_vwap_btc_quality_shadow",
    ) == ("unavailable", "btc_slope_feature_unavailable")


def test_depth_variants_record_distinct_geometry():
    shallow = sweep._simulate(
        _geom(), _candles(), "shallow", fee_profile="bybit_non_vip_usdt_perp", size_weight=1.0)
    deeper = sweep._simulate(
        _geom(), _candles(), "deeper", fee_profile="bybit_non_vip_usdt_perp", size_weight=1.0)
    assert shallow["geometry_changed"] == 1 and deeper["geometry_changed"] == 1
    assert shallow["entry_low_used"] > deeper["entry_low_used"]
    assert shallow["entry_rule"] == "shallow_pullback_limit"
    assert deeper["entry_rule"] == "deeper_pullback_limit"


def test_signal_expiry_blocks_a_later_limit_fill():
    candles = pd.DataFrame([
        {"timestamp": "2026-07-13T12:00:00Z", "open": 101.0, "high": 101.2,
         "low": 100.7, "close": 101.0, "volume": 10},
        # This bar would touch the limit, but only closes after the signal deadline.
        {"timestamp": "2026-07-13T12:05:00Z", "open": 101.0, "high": 101.1,
         "low": 99.4, "close": 100.0, "volume": 10},
    ])
    out = sweep._simulate(
        _geom(), candles, "current", fee_profile="bybit_non_vip_usdt_perp", size_weight=1.0,
        entry_expires_at="2026-07-13T12:05:00Z",
    )
    assert out["status"] == "skipped"
    assert out["skip_reason"] == "entry_after_signal_expiry"


def test_valid_entry_can_be_managed_after_signal_expiry():
    candles = pd.DataFrame([
        {"timestamp": "2026-07-13T12:00:00Z", "open": 101.0, "high": 101.2,
         "low": 99.4, "close": 100.0, "volume": 10},
        # Exit monitoring remains valid after the entry deadline.
        {"timestamp": "2026-07-13T12:05:00Z", "open": 100.0, "high": 111.0,
         "low": 100.0, "close": 110.0, "volume": 10},
    ])
    out = sweep._simulate(
        _geom(), candles, "current", fee_profile="bybit_non_vip_usdt_perp", size_weight=1.0,
        entry_expires_at="2026-07-13T12:05:00Z",
    )
    assert out["status"] == "resolved"
    assert out["entry_bar_at"] == "2026-07-13T12:00:00+00:00"


def test_missing_preentry_v2_schema_is_conservatively_empty(tmp_path):
    p = str(tmp_path / "x.sqlite")
    conn = sqlite3.connect(p)
    conn.execute("CREATE TABLE paper_shadow_execution_outcomes (signal_id TEXT)")
    conn.execute("CREATE TABLE proposed_signals (signal_id TEXT)")
    conn.execute("CREATE TABLE signal_entry_mode_preentry (signal_id TEXT)")
    assert sweep._load_samples(conn, 100) == []
    conn.close()


def _seed_refresh_db(path):
    conn = sqlite3.connect(path)
    conn.execute("CREATE TABLE proposed_signals (signal_id TEXT, symbol TEXT, direction TEXT, mode TEXT, "
                 "asset_class TEXT, exchange_focus TEXT, created_at TEXT, entry_low REAL, entry_high REAL, "
                 "entry_trigger REAL, suggested_entry REAL, stop_loss REAL, invalidation REAL, "
                 "tp1 REAL, tp2 REAL, tp3 REAL, expires_at TEXT)")
    conn.execute("CREATE TABLE signal_entry_mode_preentry (signal_id TEXT, entry_mode TEXT, data_quality TEXT)")
    conn.execute("CREATE TABLE paper_shadow_execution_outcomes (signal_id TEXT, branch TEXT, window TEXT, "
                 "entry_mode TEXT, entry_mode_version TEXT, skipped_shadow_reason TEXT)")
    conn.execute("CREATE TABLE crypto_quality_overlay_decision_snapshots (signal_id TEXT, decision_json TEXT, "
                 "decision_context_type TEXT)")
    conn.execute("INSERT INTO proposed_signals VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                 ("pb", "BTC/USDT", "long", "intraday", "crypto", "", "2026-07-13T12:00:00Z",
                  99.5, 100.5, 100.5, 100.0, 98.0, 98.0, 104.0, 106.0, 110.0,
                  "2026-07-14T12:00:00Z"))
    conn.execute("INSERT INTO signal_entry_mode_preentry VALUES (?,?,?)", ("pb", "PULLBACK_LIMIT", "ok"))
    conn.execute("INSERT INTO paper_shadow_execution_outcomes VALUES (?,?,?,?,?,?)",
                 ("pb", "new_logic_shadow", "forward_since_activation", "PULLBACK_LIMIT", "preentry_v2", None))
    conn.commit(); conn.close()


def test_refresh_is_forward_only_and_reports_disabled_lane(tmp_path, monkeypatch):
    p = str(tmp_path / "x.sqlite")
    _seed_refresh_db(p)
    monkeypatch.setattr("src.execution.paper_shadow_engine._load_candles",
                        lambda *args, **kwargs: (_candles(), "5m"))
    out = sweep.refresh(db=p, persist=True, limit=10)
    assert out["signals_sampled"] == 1
    modes = {(x["entry_mode"], x["variant"]): x for x in out["variants"]}
    assert modes[("LIMIT_THEN_TAKER_TIMEOUT", "disabled")]["status"] == "DISABLED_BY_TEST_PLAN"
    assert all("LIMIT_THEN_TAKER_TIMEOUT" not in x["entry_mode"]
                for x in out["variants"] if x["entry_mode"] != "LIMIT_THEN_TAKER_TIMEOUT")
    assert modes[("PULLBACK_LIMIT", "level_hold_1bar")]["status"] == "INSUFFICIENT_FORWARD_SAMPLE"
    assert modes[("PULLBACK_LIMIT", "high_atr_veto_shadow")]["status"] == "AWAITING_POINT_IN_TIME_FEATURE_COVERAGE"
    assert modes[("PULLBACK_LIMIT", "risk_off_veto_shadow")]["size_action"] == "SHADOW_ONLY_COUNTERFACTUAL"
    conn = sqlite3.connect(p)
    assert conn.execute("SELECT count(*) FROM crypto_intraday_idea_sweep_results").fetchone()[0] == len(out["variants"])
    trade_cols = {row[1] for row in conn.execute("PRAGMA table_info(crypto_intraday_idea_sweep_trades)")}
    assert {"entry_price", "entry_bar_at", "entry_low_used", "entry_high_used",
            "bars_to_entry", "entry_rule", "geometry_changed"}.issubset(trade_cols)
    conn.close()


def test_refresh_preserves_append_only_run_history(tmp_path, monkeypatch):
    p = str(tmp_path / "x.sqlite")
    _seed_refresh_db(p)
    monkeypatch.setattr("src.execution.paper_shadow_engine._load_candles",
                        lambda *args, **kwargs: (_candles(), "5m"))
    first = sweep.refresh(db=p, persist=True, limit=10)
    second = sweep.refresh(db=p, persist=True, limit=10)
    assert first["run_id"] != second["run_id"]
    conn = sqlite3.connect(p)
    assert conn.execute("SELECT count(*) FROM crypto_intraday_idea_sweep_runs").fetchone()[0] == 2
    assert conn.execute("SELECT count(*) FROM crypto_intraday_idea_sweep_results_history").fetchone()[0] == len(first["variants"]) * 2
    cols = {row[1] for row in conn.execute("PRAGMA table_info(crypto_intraday_idea_sweep_trades_history)")}
    assert {"signal_session", "entry_session", "signal_expires_at", "entry_within_validity"}.issubset(cols)
    conn.close()


def test_sweep_migrates_old_summary_tables_additively(tmp_path):
    conn = sqlite3.connect(tmp_path / "old.sqlite")
    conn.execute("CREATE TABLE crypto_intraday_idea_sweep_results (version TEXT)")
    conn.execute("CREATE TABLE crypto_intraday_idea_sweep_results_history (run_id TEXT)")
    sweep.ensure_tables(conn)
    for table in ("crypto_intraday_idea_sweep_results", "crypto_intraday_idea_sweep_results_history"):
        columns = {row[1] for row in conn.execute(f"PRAGMA table_info({table})")}
        assert {"filter_excluded", "feature_unavailable"}.issubset(columns)
    conn.close()


def test_module_has_no_production_writes():
    text = open(sweep.__file__, encoding="utf-8").read().lower()
    for bad in ("update proposed_signals", "update signal_outcomes", "final_r =",
                "create_order", "place_order", "auto_live", "manual_live"):
        assert bad not in text
