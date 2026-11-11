from __future__ import annotations

import json
import sqlite3
from copy import deepcopy
from datetime import datetime, timezone

import pytest

from src.live_execution.config import LiveCanaryConfig
from src.live_execution.sizing import PlanRejected, build_order_plan
from src.live_execution.stocks_breakout_bridge import (
    capture_standard_paper_breakouts,
    capture_filled_positions,
    load_stocks_live_bridge_config,
)


NOW = datetime(2026, 8, 12, 14, 0, tzinfo=timezone.utc)


def _live_cfg(*, execution_mode: str = "live") -> LiveCanaryConfig:
    return LiveCanaryConfig({
        "submission_enabled": True,
        "execution_mode": execution_mode,
        "allocated_equity_usdt": 100.0,
        "fixed_risk_per_trade_usdt": 10.0,
        "fixed_max_concurrent_risk_usdt": 50.0,
        "max_total_margin_usdt": 75.0,
        "max_gross_notional_usdt": 1000.0,
        "max_spread_bps_stock_futures": 50.0,
        "entry_limits_by_mode": {
            "stock_intraday": {
                "max_entry_age_seconds": {"BREAKOUT_CONTINUATION": 300},
                "max_entry_drift_bps": {"BREAKOUT_CONTINUATION": 100},
            },
        },
        "execution_limits_by_risk_bucket": {
            "stock_intraday_breakout": {
                "max_total_margin_usdt": 75.0,
                "max_gross_notional_usdt": 1000.0,
            },
        },
        "credentials": {
            "access_key_env": "TEST_MEXC_ACCESS",
            "secret_key_env": "TEST_MEXC_SECRET",
            "arm_env": "TEST_MEXC_ARM",
            "arm_value": "ARMED",
        },
    })


def _route_cfg() -> dict:
    return {
        "enabled": True,
        "route_id": "stocks_intraday_breakout_live_v1",
        "source_strategy_id": "stocks_mexc_preopen_news_v1",
        "allowed_source_profiles": ["stocks_intraday_breakout_1bar_paper_v1"],
        "allow_unprofiled_source": False,
        "allowed_entry_modes": ["BREAKOUT_CONTINUATION"],
        "allowed_directions": ["long", "short"],
        "min_score": 70,
        "fixed_risk_usdt": 5.0,
        "risk_multiplier": 0.5,
        "risk_bucket": "stock_intraday_breakout",
        "mode": "stock_intraday",
        "live_strategy_version": "stocks_intraday_breakout_live_v1",
        "decision_context_type": "point_in_time_stock_futures_fill",
        "max_capture_age_seconds": 300,
        "standard_paper_breakout": {
            "enabled": True,
            "route_id": "stocks_intraday_breakout_standard_paper_live_v1",
            "allowed_source_profiles": ["stocks_intraday_breakout_1bar_paper_v1"],
            "allowed_entry_modes": ["BREAKOUT_CONTINUATION"],
            "allowed_directions": ["long", "short"],
            "min_score": 70,
            "max_capture_age_seconds": 300,
        },
    }


def _dual_venue_live_cfg(monkeypatch) -> LiveCanaryConfig:
    raw = deepcopy(_live_cfg().raw)
    raw["venue_routing"] = {
        "enabled": True,
        "preference_order": ["mexc", "bybit"],
        "bybit": {
            "enabled": True,
            "submission_enabled": True,
            "require_explicit_stock_symbol": True,
            "stock_symbol_aliases": {"AAPL/USDT": "AAPLUSDT"},
            "credentials": {
                "access_key_env": "TEST_BYBIT_ACCESS",
                "secret_key_env": "TEST_BYBIT_SECRET",
                "arm_env": "TEST_BYBIT_ARM",
                "arm_value": "ARMED",
            },
        },
    }
    monkeypatch.setenv("TEST_BYBIT_ACCESS", "x")
    monkeypatch.setenv("TEST_BYBIT_SECRET", "y")
    monkeypatch.setenv("TEST_BYBIT_ARM", "ARMED")
    return LiveCanaryConfig(raw)


def _seed_stock_fill(conn: sqlite3.Connection, *, profile: str = "stocks_intraday_breakout_1bar_paper_v1") -> None:
    conn.executescript(
        """
        CREATE TABLE mexc_stock_futures_paper_orders (
          order_id TEXT PRIMARY KEY,
          source_pre_gate_tier TEXT,
          source_score REAL,
          decision_at TEXT,
          snapshot_json TEXT
        );
        CREATE TABLE mexc_stock_futures_paper_positions (
          position_id TEXT PRIMARY KEY,
          order_id TEXT,
          strategy_id TEXT,
          source_signal_id TEXT,
          ticker TEXT,
          mexc_symbol TEXT,
          direction TEXT,
          entry_mode TEXT,
          status TEXT,
          entry_at TEXT,
          entry_price REAL,
          stop_initial REAL,
          tp1 REAL,
          tp2 REAL,
          tp3 REAL,
          created_at TEXT
        );
        """
    )
    snapshot = {
        "source_signal": {
            "raw_context": {
                "paper_entry_profile": profile,
                "paper_lane": "paper_stocks_intraday_breakout_1bar",
            },
        },
    }
    conn.execute(
        "INSERT INTO mexc_stock_futures_paper_orders VALUES(?,?,?,?,?)",
        ("ord1", "A", 81.0, NOW.isoformat(), json.dumps(snapshot)),
    )
    conn.execute(
        "INSERT INTO mexc_stock_futures_paper_positions VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (
            "pos1", "ord1", "stocks_mexc_preopen_news_v1", "sig-stock-1",
            "AAPL", "AAPLSTOCK/USDT", "long", "BREAKOUT_CONTINUATION",
            "OPEN", NOW.isoformat(), 100.0, 98.0, 103.0, 106.0, 110.0,
            NOW.isoformat(),
        ),
    )
    conn.commit()


def test_stock_breakout_fill_queues_once_at_five_usdt_risk(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("TEST_MEXC_ACCESS", "x")
    monkeypatch.setenv("TEST_MEXC_SECRET", "y")
    monkeypatch.setenv("TEST_MEXC_ARM", "ARMED")
    db = tmp_path / "stock-live.sqlite"
    with sqlite3.connect(db) as conn:
        _seed_stock_fill(conn)

    first = capture_filled_positions(
        db=db, route_cfg=_route_cfg(), live_cfg=_live_cfg(), now=NOW,
    )
    second = capture_filled_positions(
        db=db, route_cfg=_route_cfg(), live_cfg=_live_cfg(), now=NOW,
    )
    assert first["status"] == "OK"
    assert first["queued"] == 1 and first["risk_usdt"] == 5.0
    assert second["duplicate"] == 1 and second["queued"] == 0

    with sqlite3.connect(db) as conn:
        decision = json.loads(conn.execute(
            "SELECT decision_json FROM mexc_canary_decisions"
        ).fetchone()[0])
    assert decision["asset_class"] == "stock_futures"
    assert decision["mode"] == "stock_intraday"
    assert decision["entry_mode"] == "BREAKOUT_CONTINUATION"
    assert decision["source_paper_profile"] == "stocks_intraday_breakout_1bar_paper_v1"
    assert decision["live_risk_multiplier"] == 0.5
    assert decision["risk_bucket"] == "stock_intraday_breakout"


def test_configured_stock_live_bridge_has_a_bounded_canary_route() -> None:
    """The checked-in route must stay explicitly versioned and risk-capped."""
    cfg = load_stocks_live_bridge_config()

    assert cfg["enabled"] is False
    assert cfg["source_strategy_id"] == "stocks_mexc_preopen_news_v1"
    assert cfg["allowed_source_profiles"] == ["stocks_intraday_breakout_1bar_paper_v1"]
    assert cfg["allow_unprofiled_source"] is True
    assert cfg["allowed_entry_modes"] == ["BREAKOUT_CONTINUATION"]
    assert cfg["allowed_directions"] == ["long"]
    assert cfg["min_score"] == 70
    assert cfg["risk_bucket"] == "stock_preus_news_long"
    assert cfg["fixed_risk_usdt"] == 5.0
    assert cfg["risk_multiplier"] == 0.5
    assert cfg["max_capture_age_seconds"] == 300
    assert cfg["allow_synthetic_bybit_stock_symbols"] is False
    assert cfg["live_quality_filter"]["enabled"] is True
    assert cfg["live_quality_filter"]["version"] == "stock_live_structural_alignment_v2"
    assert cfg["live_quality_filter"]["legacy_stop_policy"] == "block"
    assert cfg["live_quality_filter"]["require_structural_stop_for_live"] is True
    assert cfg["live_quality_filter"]["require_intraday_actionability"] is True
    assert cfg["live_quality_filter"]["block_against_intraday_broad"] is True
    assert cfg["live_quality_filter"]["block_low_confidence_stop_against_intraday_broad"] is True
    standard = cfg["standard_paper_breakout"]
    assert standard["enabled"] is False
    assert standard["allowed_source_profiles"] == ["stocks_intraday_breakout_1bar_paper_v1"]
    assert standard["allowed_entry_modes"] == ["BREAKOUT_CONTINUATION"]
    assert standard["min_score"] == 70
    assert standard["max_capture_age_seconds"] == 300


@pytest.mark.parametrize("profile", [
    "stocks_intraday_pullback_vwap_paper_v1",
    "stocks_intraday_pullback_vwap_paper_v2",
])
def test_stock_bridge_rejects_non_breakout_profile(tmp_path, monkeypatch, profile) -> None:
    monkeypatch.setenv("TEST_MEXC_ACCESS", "x")
    monkeypatch.setenv("TEST_MEXC_SECRET", "y")
    monkeypatch.setenv("TEST_MEXC_ARM", "ARMED")
    db = tmp_path / "stock-live-reject.sqlite"
    with sqlite3.connect(db) as conn:
        _seed_stock_fill(conn, profile=profile)

    result = capture_filled_positions(
        db=db, route_cfg=_route_cfg(), live_cfg=_live_cfg(), now=NOW,
    )
    assert result["queued"] == 0
    assert result["reasons"] == {"SOURCE_PROFILE_NOT_LIVE_ENABLED": 1}


def test_stock_live_canary_rejects_low_score_without_changing_paper(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("TEST_MEXC_ACCESS", "x")
    monkeypatch.setenv("TEST_MEXC_SECRET", "y")
    monkeypatch.setenv("TEST_MEXC_ARM", "ARMED")
    db = tmp_path / "stock-low-score.sqlite"
    with sqlite3.connect(db) as conn:
        _seed_stock_fill(conn)
        conn.execute("UPDATE mexc_stock_futures_paper_orders SET source_score=69.99")
        conn.commit()
    result = capture_filled_positions(
        db=db, route_cfg=_route_cfg(), live_cfg=_live_cfg(), now=NOW,
    )
    assert result["queued"] == 0
    assert result["reasons"] == {"SCORE_BELOW_LIVE_CANARY": 1}


def test_preus_route_accepts_unprofiled_fill_only_when_explicitly_enabled(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("TEST_MEXC_ACCESS", "x")
    monkeypatch.setenv("TEST_MEXC_SECRET", "y")
    monkeypatch.setenv("TEST_MEXC_ARM", "ARMED")
    db = tmp_path / "stock-live-unprofiled.sqlite"
    with sqlite3.connect(db) as conn:
        _seed_stock_fill(conn, profile="")

    rejected = capture_filled_positions(
        db=db, route_cfg=_route_cfg(), live_cfg=_live_cfg(), now=NOW,
    )
    assert rejected["reasons"] == {"SOURCE_PROFILE_NOT_LIVE_ENABLED": 1}

    route = _route_cfg()
    route["allow_unprofiled_source"] = True
    accepted = capture_filled_positions(
        db=db, route_cfg=route, live_cfg=_live_cfg(), now=NOW,
    )
    assert accepted["queued"] == 1


def _seed_standard_paper_breakout(
    conn: sqlite3.Connection,
    *,
    profile: str = "stocks_intraday_breakout_1bar_paper_v1",
    direction: str = "long",
    tier: str = "A",
    score: float = 88.0,
    market_regime: str = "risk_on",
    sector: str = "technology",
    setup_type: str = "continuation",
    news_supported: int = 0,
    payload_extra: dict | None = None,
) -> None:
    conn.executescript(
        """
        CREATE TABLE proposed_signals (
          signal_id TEXT PRIMARY KEY, symbol TEXT, direction TEXT, tier TEXT,
          score REAL, created_at TEXT, asset_class TEXT, mode TEXT,
          market_regime TEXT, sector TEXT, setup_type TEXT,
          news_supported INTEGER, telegram_supported INTEGER, raw_idea_json TEXT
        );
        CREATE TABLE signal_alerts (
          alert_id TEXT PRIMARY KEY, signal_id TEXT, asset_class TEXT, mode TEXT,
          alert_type TEXT, sent_at TEXT, payload_json TEXT
        );
        CREATE TABLE paper_execution_outcomes (
          signal_id TEXT, computed_at TEXT, lifecycle_state TEXT, execution_validity TEXT,
          entry_at TEXT, entry_price_used REAL, stop_initial REAL,
          paper_entry_profile TEXT, paper_execution_entry_mode TEXT,
          entry_time_basis TEXT, current_price_revalidated INTEGER, close_reason TEXT
        );
        CREATE TABLE mexc_stock_futures_contracts (
          ticker TEXT, mexc_symbol TEXT, state INTEGER, api_allowed INTEGER, snapshot_at TEXT
        );
        """
    )
    payload = {
        "entry_used": 100.0, "stop": 98.0, "tp1": 103.0, "tp2": 106.0, "tp3": 110.0,
        "entry_bar_open_at": NOW.isoformat(),
    }
    payload.update(payload_extra or {})
    conn.execute("INSERT INTO proposed_signals VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (
        "sig-standard-1", "AAPL", direction, tier, score, NOW.isoformat(),
        "stocks", "intraday", market_regime, sector, setup_type,
        news_supported, 0, "{}",
    ))
    conn.execute("INSERT INTO signal_alerts VALUES(?,?,?,?,?,?,?)", (
        "alert-standard-1", "sig-standard-1", "stocks", "intraday", "paper_entry",
        NOW.isoformat(), json.dumps(payload),
    ))
    conn.execute("INSERT INTO paper_execution_outcomes VALUES(?,?,?,?,?,?,?,?,?,?,?,?)", (
        "sig-standard-1", NOW.isoformat(), "OPEN", "valid", NOW.isoformat(), 100.0, 98.0,
        profile, "BREAKOUT_CONTINUATION", "point_in_time_current_bar", 1, "open",
    ))
    conn.execute("INSERT INTO mexc_stock_futures_contracts VALUES(?,?,?,?,?)", (
        "AAPL", "AAPLSTOCK/USDT", 0, 1, NOW.isoformat(),
    ))
    conn.commit()


def test_standard_paper_breakout_is_mirrored_once_at_five_usdt_risk(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("TEST_MEXC_ACCESS", "x")
    monkeypatch.setenv("TEST_MEXC_SECRET", "y")
    monkeypatch.setenv("TEST_MEXC_ARM", "ARMED")
    db = tmp_path / "standard-stock-live.sqlite"
    with sqlite3.connect(db) as conn:
        _seed_standard_paper_breakout(conn)

    first = capture_standard_paper_breakouts(
        db=db, route_cfg=_route_cfg(), live_cfg=_live_cfg(), now=NOW,
    )
    second = capture_standard_paper_breakouts(
        db=db, route_cfg=_route_cfg(), live_cfg=_live_cfg(), now=NOW,
    )
    assert first["status"] == "OK"
    assert first["queued"] == 1 and first["risk_usdt"] == 5.0
    assert second["duplicate"] == 1 and second["queued"] == 0
    with sqlite3.connect(db) as conn:
        decision = json.loads(conn.execute(
            "SELECT decision_json FROM mexc_canary_decisions"
        ).fetchone()[0])
    assert decision["source_signal_id"] == "sig-standard-1"
    assert decision["symbol"] == "AAPL/USDT"
    assert decision["venue_symbols"] == {"mexc": "AAPLSTOCK/USDT"}
    assert decision["bybit_stock_symbol_explicit"] is False
    assert decision["source_paper_profile"] == "stocks_intraday_breakout_1bar_paper_v1"
    assert decision["live_risk_multiplier"] == 0.5


def test_direct_stock_alert_handoff_waits_for_execution_materialization(tmp_path, monkeypatch) -> None:
    """A stock Paper alert cannot authorize live before the execution row commits."""
    monkeypatch.setenv("TEST_MEXC_ACCESS", "x")
    monkeypatch.setenv("TEST_MEXC_SECRET", "y")
    monkeypatch.setenv("TEST_MEXC_ARM", "ARMED")
    db = tmp_path / "standard-stock-direct-alert.sqlite"
    payload = {
        "entry_used": 100.0, "stop": 98.0, "tp1": 103.0, "tp2": 106.0, "tp3": 110.0,
        "entry_triggered_at": NOW.isoformat(), "entry_bar_open_at": NOW.isoformat(),
        "entry_time_basis": "point_in_time_current_bar", "current_price_revalidated": True,
        "paper_entry_profile": "stocks_intraday_breakout_1bar_paper_v1",
        "paper_execution_entry_mode": "BREAKOUT_CONTINUATION",
    }
    with sqlite3.connect(db) as conn:
        _seed_standard_paper_breakout(conn)
        conn.execute("DELETE FROM paper_execution_outcomes WHERE signal_id='sig-standard-1'")
        conn.commit()

    result = capture_standard_paper_breakouts(
        db=db, route_cfg=_route_cfg(), live_cfg=_live_cfg(), now=NOW,
        source_signal_id="sig-standard-1", payload_override=payload,
    )
    assert result["status"] == "OK"
    assert result["seen"] == 0 and result["queued"] == 0
    assert result["rejected"] == 1
    assert result["reasons"] == {"PAPER_EXECUTION_OUTCOME_NOT_MATERIALIZED": 1}


def test_standard_paper_breakout_rejects_non_revalidated_paper_contract(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("TEST_MEXC_ACCESS", "x")
    monkeypatch.setenv("TEST_MEXC_SECRET", "y")
    monkeypatch.setenv("TEST_MEXC_ARM", "ARMED")
    db = tmp_path / "standard-stock-non-revalidated.sqlite"
    with sqlite3.connect(db) as conn:
        _seed_standard_paper_breakout(conn)
        conn.execute(
            "UPDATE paper_execution_outcomes SET current_price_revalidated=0 "
            "WHERE signal_id='sig-standard-1'"
        )
        conn.commit()

    result = capture_standard_paper_breakouts(
        db=db, route_cfg=_route_cfg(), live_cfg=_live_cfg(), now=NOW,
    )

    assert result["queued"] == 0
    assert result["rejected"] == 1
    assert result["reasons"] == {"PAPER_EXECUTION_PRICE_NOT_REVALIDATED": 1}
    with sqlite3.connect(db) as conn:
        decision = conn.execute(
            "SELECT eligible,state,rejection_reasons_json FROM mexc_canary_decisions"
        ).fetchone()
    assert decision[0] == 0
    assert decision[1] == "REJECTED"
    assert json.loads(decision[2]) == [
        "PAPER_EXECUTION_PRICE_NOT_REVALIDATED"
    ]


def test_direct_stock_alert_rebases_a_valid_ladder_when_quote_is_above_trigger(tmp_path, monkeypatch) -> None:
    """A confirmed continuation must not retain TP1 below its actual entry."""
    monkeypatch.setenv("TEST_MEXC_ACCESS", "x")
    monkeypatch.setenv("TEST_MEXC_SECRET", "y")
    monkeypatch.setenv("TEST_MEXC_ARM", "ARMED")
    db = tmp_path / "standard-stock-rebase.sqlite"
    with sqlite3.connect(db) as conn:
        _seed_standard_paper_breakout(conn)
        conn.execute(
            "UPDATE paper_execution_outcomes SET entry_price_used=106.0 "
            "WHERE signal_id='sig-standard-1'"
        )
        conn.commit()
    payload = {
        "entry_used": 106.0,
        "entry_reference": 100.0,
        "stop": 98.0,
        "tp1": 103.0,
        "tp2": 106.0,
        "tp3": 110.0,
        "entry_triggered_at": NOW.isoformat(),
        "entry_time_basis": "point_in_time_current_bar",
        "current_price_revalidated": True,
        "paper_entry_profile": "stocks_intraday_breakout_1bar_paper_v1",
        "paper_execution_entry_mode": "BREAKOUT_CONTINUATION",
    }
    result = capture_standard_paper_breakouts(
        db=db, route_cfg=_route_cfg(), live_cfg=_live_cfg(), now=NOW,
        source_signal_id="sig-standard-1", payload_override=payload,
    )
    assert result["queued"] == 1
    with sqlite3.connect(db) as conn:
        decision = json.loads(conn.execute(
            "SELECT decision_json FROM mexc_canary_decisions"
        ).fetchone()[0])
    assert decision["live_geometry_rebased"] is True
    assert decision["original_stop"] < decision["entry_price"] < decision["tp1"] < decision["tp2"] < decision["tp3"]


def test_stock_bridges_dedupe_the_same_source_signal_across_lanes(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("TEST_MEXC_ACCESS", "x")
    monkeypatch.setenv("TEST_MEXC_SECRET", "y")
    monkeypatch.setenv("TEST_MEXC_ARM", "ARMED")
    db = tmp_path / "cross-lane-dedupe.sqlite"
    with sqlite3.connect(db) as conn:
        _seed_standard_paper_breakout(conn)
        conn.executescript("""
          CREATE TABLE mexc_stock_futures_paper_orders (
            order_id TEXT PRIMARY KEY, source_pre_gate_tier TEXT,
            source_score REAL, decision_at TEXT, snapshot_json TEXT
          );
          CREATE TABLE mexc_stock_futures_paper_positions (
            position_id TEXT PRIMARY KEY, order_id TEXT, strategy_id TEXT,
            source_signal_id TEXT, ticker TEXT, mexc_symbol TEXT, direction TEXT,
            entry_mode TEXT, status TEXT, entry_at TEXT, entry_price REAL,
            stop_initial REAL, tp1 REAL, tp2 REAL, tp3 REAL, created_at TEXT
          );
        """)
        snapshot = {"source_signal": {"raw_context": {
            "paper_entry_profile": "stocks_intraday_breakout_1bar_paper_v1",
        }}}
        conn.execute("INSERT INTO mexc_stock_futures_paper_orders VALUES(?,?,?,?,?)", (
            "ord-cross", "A", 88.0, NOW.isoformat(), json.dumps(snapshot),
        ))
        conn.execute(
            "INSERT INTO mexc_stock_futures_paper_positions VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            ("pos-cross", "ord-cross", "stocks_mexc_preopen_news_v1", "sig-standard-1",
             "AAPL", "AAPLSTOCK/USDT", "long", "BREAKOUT_CONTINUATION", "OPEN",
             NOW.isoformat(), 100.0, 98.0, 103.0, 106.0, 110.0, NOW.isoformat()),
        )
        conn.commit()

    standard = capture_standard_paper_breakouts(
        db=db, route_cfg=_route_cfg(), live_cfg=_live_cfg(), now=NOW,
    )
    preus = capture_filled_positions(
        db=db, route_cfg=_route_cfg(), live_cfg=_live_cfg(), now=NOW,
    )
    assert standard["queued"] == 1
    assert preus["queued"] == 0 and preus["duplicate"] == 1
    with sqlite3.connect(db) as conn:
        assert conn.execute("SELECT COUNT(*) FROM mexc_canary_decisions").fetchone()[0] == 1


def test_standard_paper_breakout_can_be_captured_directly_before_alert_row(
    tmp_path, monkeypatch
) -> None:
    """The Paper notifier must not depend on the later minute bridge poll."""
    monkeypatch.setenv("TEST_MEXC_ACCESS", "x")
    monkeypatch.setenv("TEST_MEXC_SECRET", "y")
    monkeypatch.setenv("TEST_MEXC_ARM", "ARMED")
    db = tmp_path / "standard-stock-direct-live.sqlite"
    with sqlite3.connect(db) as conn:
        _seed_standard_paper_breakout(conn)
        conn.execute("DELETE FROM signal_alerts")
        conn.commit()

    payload = {
        "entry_used": 100.0,
        "stop": 98.0,
        "tp1": 103.0,
        "tp2": 106.0,
        "tp3": 110.0,
        "entry_bar_open_at": NOW.isoformat(),
    }
    result = capture_standard_paper_breakouts(
        db=db,
        route_cfg=_route_cfg(),
        live_cfg=_live_cfg(),
        now=NOW,
        source_signal_id="sig-standard-1",
        payload_override=payload,
        paper_alert_id="alert-not-yet-persisted",
    )

    assert result["queued"] == 1
    with sqlite3.connect(db) as conn:
        row = conn.execute(
            "SELECT paper_alert_id,decision_json FROM mexc_canary_decisions"
        ).fetchone()
    assert row[0] == "alert-not-yet-persisted"
    assert json.loads(row[1])["source_signal_id"] == "sig-standard-1"


def test_stock_live_quality_rejects_risk_off_long_with_legacy_stop(
    tmp_path, monkeypatch
) -> None:
    monkeypatch.setenv("TEST_MEXC_ACCESS", "x")
    monkeypatch.setenv("TEST_MEXC_SECRET", "y")
    monkeypatch.setenv("TEST_MEXC_ARM", "ARMED")
    db = tmp_path / "standard-stock-live-quality-riskoff.sqlite"
    fallback_stop = {
        "version": "initial_stop_contract_v1",
        "stop_source": "legacy_atr_stop",
        "stop_model": "atr_distance_v1",
        "fallback_used": True,
        "confidence": "low",
    }
    with sqlite3.connect(db) as conn:
        _seed_standard_paper_breakout(
            conn,
            direction="long",
            tier="B",
            score=70.5,
            market_regime="risk_off",
            payload_extra={
                "initial_stop_contract": fallback_stop,
                "stocks_context_status": "stale",
                "stocks_context_reason": "options_context_stale",
            },
        )

    route = _route_cfg()
    route["live_quality_filter"] = {
        "enabled": True,
        "long_disallowed_market_regimes": ["risk_off"],
        "min_score_for_stale_legacy_stop": 83,
    }
    result = capture_standard_paper_breakouts(
        db=db, route_cfg=route, live_cfg=_live_cfg(), now=NOW,
    )

    assert result["queued"] == 0
    assert result["rejected"] == 1
    assert result["reasons"]["STOCK_LIVE_BROAD_MARKET_CONFLICT"] == 1
    assert result["reasons"]["STOCK_LIVE_STALE_CONTEXT_LEGACY_STOP"] == 1


def test_stock_live_quality_rejects_unconfirmed_transition_short(
    tmp_path, monkeypatch
) -> None:
    monkeypatch.setenv("TEST_MEXC_ACCESS", "x")
    monkeypatch.setenv("TEST_MEXC_SECRET", "y")
    monkeypatch.setenv("TEST_MEXC_ARM", "ARMED")
    db = tmp_path / "standard-stock-live-quality-transition-short.sqlite"
    with sqlite3.connect(db) as conn:
        _seed_standard_paper_breakout(
            conn,
            direction="short",
            tier="A",
            score=81.0,
            market_regime="transition",
            payload_extra={"stocks_context_status": "ok"},
        )
        conn.execute(
            "UPDATE paper_execution_outcomes SET entry_price_used=100.0,"
            "stop_initial=102.0 WHERE signal_id='sig-standard-1'"
        )
        payload = {
            "entry_used": 100.0, "stop": 102.0,
            "tp1": 97.0, "tp2": 94.0, "tp3": 90.0,
            "stocks_context_status": "ok",
        }
        conn.execute(
            "UPDATE signal_alerts SET payload_json=? WHERE signal_id='sig-standard-1'",
            (json.dumps(payload),),
        )
        conn.commit()

    route = _route_cfg()
    route["live_quality_filter"] = {
        "enabled": True,
        "short_needs_confirmation_market_regimes": ["transition"],
        "min_transition_short_score": 83,
    }
    result = capture_standard_paper_breakouts(
        db=db, route_cfg=route, live_cfg=_live_cfg(), now=NOW,
    )

    assert result["queued"] == 0
    assert result["rejected"] == 1
    assert result["reasons"] == {
        "STOCK_LIVE_SHORT_CONTEXT_NOT_CONFIRMED": 1,
        "STOCK_LIVE_SHORT_BROAD_NOT_BEARISH": 1,
    }


def test_stock_live_soft_filter_warns_on_legacy_stop_but_blocks_low_score_contra_broad(
    tmp_path, monkeypatch
) -> None:
    monkeypatch.setenv("TEST_MEXC_ACCESS", "x")
    monkeypatch.setenv("TEST_MEXC_SECRET", "y")
    monkeypatch.setenv("TEST_MEXC_ARM", "ARMED")
    db = tmp_path / "standard-stock-live-quality-soft.sqlite"
    fallback_stop = {
        "version": "initial_stop_contract_v1",
        "stop_source": "legacy_atr_stop",
        "stop_model": "atr_distance_v1",
        "fallback_used": True,
        "confidence": "low",
    }
    with sqlite3.connect(db) as conn:
        _seed_standard_paper_breakout(
            conn,
            direction="short",
            tier="B",
            score=82.0,
            market_regime="risk_off",
            payload_extra={
                "initial_stop_contract": fallback_stop,
                "intraday_actionability": {
                    "market_context_status": "ok",
                    "sector_confirmation_status": "confirmed",
                    "market_regime_intraday": "trend_up",
                    "spy_vs_vwap": "above",
                    "qqq_vs_vwap": "above",
                    "spy_rth_return_pct": 0.3,
                    "qqq_rth_return_pct": 0.2,
                },
                "stocks_context_status": "stale",
            },
        )
        conn.execute(
            "UPDATE paper_execution_outcomes SET entry_price_used=100.0,"
            "stop_initial=102.0 WHERE signal_id='sig-standard-1'"
        )
        payload = {
            "entry_used": 100.0, "stop": 102.0,
            "tp1": 97.0, "tp2": 94.0, "tp3": 90.0,
            "initial_stop_contract": fallback_stop,
            "intraday_actionability": {
                "market_context_status": "ok",
                "sector_confirmation_status": "confirmed",
                "market_regime_intraday": "trend_up",
                "spy_vs_vwap": "above",
                "qqq_vs_vwap": "above",
                "spy_rth_return_pct": 0.3,
                "qqq_rth_return_pct": 0.2,
            },
            "stocks_context_status": "stale",
        }
        conn.execute(
            "UPDATE signal_alerts SET payload_json=? WHERE signal_id='sig-standard-1'",
            (json.dumps(payload),),
        )
        conn.commit()

    route = _route_cfg()
    route["live_quality_filter"] = {
        "enabled": True,
        "legacy_stop_policy": "warn",
        "block_low_confidence_stop_against_intraday_broad": True,
        "min_score_for_low_conf_contra_broad": 83,
    }
    result = capture_standard_paper_breakouts(
        db=db, route_cfg=route, live_cfg=_live_cfg(), now=NOW,
    )

    assert result["queued"] == 0
    assert result["rejected"] == 1
    assert result["reasons"] == {
        "STOCK_LIVE_LOW_CONF_STOP_CONTRA_INTRADAY_BROAD": 1,
    }

    with sqlite3.connect(db) as conn:
        conn.execute("UPDATE proposed_signals SET score=85 WHERE signal_id='sig-standard-1'")
        conn.commit()
    result = capture_standard_paper_breakouts(
        db=db, route_cfg=route, live_cfg=_live_cfg(), now=NOW,
    )
    assert result["queued"] == 1


def test_stock_live_blocks_legacy_stop_when_policy_is_structural_only(
    tmp_path, monkeypatch
) -> None:
    monkeypatch.setenv("TEST_MEXC_ACCESS", "x")
    monkeypatch.setenv("TEST_MEXC_SECRET", "y")
    monkeypatch.setenv("TEST_MEXC_ARM", "ARMED")
    db = tmp_path / "standard-stock-live-quality-structural-only.sqlite"
    fallback_stop = {
        "version": "initial_stop_contract_v1",
        "stop_source": "legacy_atr_stop",
        "stop_model": "atr_distance_v1",
        "fallback_used": True,
        "confidence": "low",
    }
    with sqlite3.connect(db) as conn:
        _seed_standard_paper_breakout(
            conn,
            direction="long",
            tier="A",
            score=95.0,
            market_regime="risk_on",
            payload_extra={
                "initial_stop_contract": fallback_stop,
                "stocks_context_status": "ok",
            },
        )

    route = _route_cfg()
    route["live_quality_filter"] = {
        "enabled": True,
        "legacy_stop_policy": "block",
    }
    result = capture_standard_paper_breakouts(
        db=db, route_cfg=route, live_cfg=_live_cfg(), now=NOW,
    )

    assert result["queued"] == 0
    assert result["rejected"] == 1
    assert result["reasons"] == {"STOCK_LIVE_LEGACY_STOP_NOT_STRUCTURAL": 1}


def test_stock_live_requires_candidate_structural_stop_to_match_executable_stop(
    tmp_path, monkeypatch
) -> None:
    monkeypatch.setenv("TEST_MEXC_ACCESS", "x")
    monkeypatch.setenv("TEST_MEXC_SECRET", "y")
    monkeypatch.setenv("TEST_MEXC_ARM", "ARMED")
    db = tmp_path / "standard-stock-live-structural-match.sqlite"
    structural_candidate = {
        "version": "initial_stop_contract_v1",
        "stop_source": "stock_intraday_structure",
        "stop_model": "nearest_15m_level_vwap_buffer_v1",
        "stop_price": 96.0,
        "structure_level": 96.2,
        "fallback_used": False,
        "confidence": "medium",
    }
    with sqlite3.connect(db) as conn:
        _seed_standard_paper_breakout(
            conn,
            payload_extra={"candidate_structural_stop_contract": structural_candidate},
        )

    route = _route_cfg()
    route["live_quality_filter"] = {
        "enabled": True,
        "require_structural_stop_for_live": True,
        "candidate_structural_stop_tolerance_bps": 10,
    }
    rejected = capture_standard_paper_breakouts(
        db=db, route_cfg=route, live_cfg=_live_cfg(), now=NOW,
    )
    assert rejected["queued"] == 0
    assert rejected["rejected"] == 1
    assert rejected["reasons"] == {"STOCK_LIVE_STOP_NOT_STRUCTURAL": 1}

    structural_candidate["stop_price"] = 98.0
    with sqlite3.connect(db) as conn:
        payload = {
            "entry_used": 100.0, "stop": 98.0,
            "tp1": 103.0, "tp2": 106.0, "tp3": 110.0,
            "entry_bar_open_at": NOW.isoformat(),
            "candidate_structural_stop_contract": structural_candidate,
        }
        conn.execute(
            "UPDATE signal_alerts SET payload_json=? WHERE signal_id='sig-standard-1'",
            (json.dumps(payload),),
        )
        conn.commit()

    accepted = capture_standard_paper_breakouts(
        db=db, route_cfg=route, live_cfg=_live_cfg(), now=NOW,
    )
    assert accepted["queued"] == 1


def test_stock_live_blocks_long_against_intraday_broad_market(
    tmp_path, monkeypatch
) -> None:
    monkeypatch.setenv("TEST_MEXC_ACCESS", "x")
    monkeypatch.setenv("TEST_MEXC_SECRET", "y")
    monkeypatch.setenv("TEST_MEXC_ARM", "ARMED")
    db = tmp_path / "standard-stock-live-broad-intraday.sqlite"
    structural_stop = {
        "version": "initial_stop_contract_v1",
        "stop_source": "stock_intraday_structure",
        "stop_model": "nearest_15m_level_vwap_buffer_v1",
        "stop_price": 98.0,
        "structure_level": 98.2,
        "fallback_used": False,
        "confidence": "medium",
    }
    with sqlite3.connect(db) as conn:
        _seed_standard_paper_breakout(
            conn,
            direction="long",
            tier="A",
            score=90.0,
            market_regime="risk_on",
            payload_extra={
                "initial_stop_contract": structural_stop,
                "intraday_actionability": {
                    "market_context_status": "ok",
                    "sector_confirmation_status": "confirmed",
                    "market_regime_intraday": "trend_down",
                    "spy_vs_vwap": "below",
                    "qqq_vs_vwap": "below",
                    "spy_rth_return_pct": -0.25,
                    "qqq_rth_return_pct": -0.31,
                },
            },
        )

    route = _route_cfg()
    route["live_quality_filter"] = {
        "enabled": True,
        "block_against_intraday_broad": True,
        "min_broad_move_pct_for_low_conf_contra": 0.10,
    }
    result = capture_standard_paper_breakouts(
        db=db, route_cfg=route, live_cfg=_live_cfg(), now=NOW,
    )

    assert result["queued"] == 0
    assert result["rejected"] == 1
    assert result["reasons"] == {"STOCK_LIVE_BROAD_INTRADAY_AGAINST_DIRECTION": 1}


def test_exchange_rejected_stock_symbol_is_blocked_before_live_queue(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("TEST_MEXC_ACCESS", "x")
    monkeypatch.setenv("TEST_MEXC_SECRET", "y")
    monkeypatch.setenv("TEST_MEXC_ARM", "ARMED")
    db = tmp_path / "stock-symbol-block.sqlite"
    with sqlite3.connect(db) as conn:
        _seed_standard_paper_breakout(conn)
        conn.execute(
            "UPDATE mexc_stock_futures_contracts SET mexc_symbol='AVGOSTOCK/USDT'"
        )
        conn.commit()
    route = _route_cfg()
    route["blocked_mexc_symbols"] = ["AVGOSTOCK_USDT"]

    result = capture_standard_paper_breakouts(
        db=db, route_cfg=route, live_cfg=_live_cfg(), now=NOW,
    )

    assert result["queued"] == 0
    assert result["reasons"] == {"MEXC_SYMBOL_BLOCKED": 1}


def test_standard_stock_queues_for_bybit_when_mexc_contract_is_unavailable(
    tmp_path, monkeypatch
) -> None:
    monkeypatch.setenv("TEST_MEXC_ACCESS", "x")
    monkeypatch.setenv("TEST_MEXC_SECRET", "y")
    monkeypatch.setenv("TEST_MEXC_ARM", "ARMED")
    db = tmp_path / "stock-bybit-fallback.sqlite"
    with sqlite3.connect(db) as conn:
        _seed_standard_paper_breakout(conn)
        conn.execute(
            "UPDATE mexc_stock_futures_contracts SET state=1,api_allowed=0"
        )
        conn.commit()

    result = capture_standard_paper_breakouts(
        db=db, route_cfg=_route_cfg(),
        live_cfg=_dual_venue_live_cfg(monkeypatch), now=NOW,
    )

    assert result["queued"] == 1
    with sqlite3.connect(db) as conn:
        decision = json.loads(conn.execute(
            "SELECT decision_json FROM mexc_canary_decisions"
        ).fetchone()[0])
    assert decision["symbol"] == "AAPL/USDT"
    assert decision["venue_symbols"]["bybit"] == "AAPLUSDT"
    assert decision["bybit_stock_symbol_explicit"] is True
    assert decision["blocked_venues"] == ["mexc"]


def test_stock_bybit_route_requires_explicit_stock_alias_when_mexc_unavailable(
    tmp_path, monkeypatch
) -> None:
    monkeypatch.setenv("TEST_MEXC_ACCESS", "x")
    monkeypatch.setenv("TEST_MEXC_SECRET", "y")
    monkeypatch.setenv("TEST_MEXC_ARM", "ARMED")
    db = tmp_path / "stock-bybit-no-alias.sqlite"
    with sqlite3.connect(db) as conn:
        _seed_standard_paper_breakout(conn)
        conn.execute(
            "UPDATE mexc_stock_futures_contracts SET state=1,api_allowed=0"
        )
        conn.commit()

    raw = deepcopy(_live_cfg().raw)
    raw["venue_routing"] = {
        "enabled": True,
        "preference_order": ["mexc", "bybit"],
        "bybit": {
            "enabled": True,
            "submission_enabled": True,
            "require_explicit_stock_symbol": True,
            "credentials": {
                "access_key_env": "TEST_BYBIT_ACCESS",
                "secret_key_env": "TEST_BYBIT_SECRET",
                "arm_env": "TEST_BYBIT_ARM",
                "arm_value": "ARMED",
            },
        },
    }
    monkeypatch.setenv("TEST_BYBIT_ACCESS", "x")
    monkeypatch.setenv("TEST_BYBIT_SECRET", "y")
    monkeypatch.setenv("TEST_BYBIT_ARM", "ARMED")

    result = capture_standard_paper_breakouts(
        db=db, route_cfg=_route_cfg(),
        live_cfg=LiveCanaryConfig(raw), now=NOW,
    )

    assert result["queued"] == 0
    assert result["reasons"] == {"NO_STOCK_LIVE_VENUE": 1}


def _stock_contract() -> dict:
    return {
        "symbol": "AAPLSTOCK_USDT",
        "baseCoin": "AAPLSTOCK",
        "baseCoinName": "AAPL",
        "conceptPlate": ["Stock", "tradfi"],
        "state": 0,
        "apiAllowed": True,
        "futureType": 1,
        "quoteCoin": "USDT",
        "preMarket": True,
        "typeLabel": 7,
        "contractSize": 0.01,
        "priceUnit": 0.01,
        "volUnit": 1,
        "minVol": 1,
        "maxVol": 100000,
        "limitMaxVol": 100000,
        "minLeverage": 1,
        "maxLeverage": 100,
        "countryConfigContractMaxLeverage": 0,
        "makerFeeRate": 0.0,
        "takerFeeRate": 0.0002,
        "maintenanceMarginRate": 0.004,
        "liquidationFeeRate": 0.0004,
    }


def _depth() -> dict:
    return {"bids": [[99.95, 5000]], "asks": [[100.05, 5000]]}


def test_live_order_plan_accepts_mexc_stock_futures_contract() -> None:
    decision = {
        "decision_id": "stock-breakout",
        "signal_id": "stock_mexc:pos1",
        "symbol": "AAPLSTOCK/USDT",
        "asset_class": "stock_futures",
        "mode": "stock_intraday",
        "direction": "long",
        "entry_mode": "BREAKOUT_CONTINUATION",
        "entry_price": 100.0,
        "original_stop": 98.0,
        "tp1": 103.0,
        "tp2": 106.0,
        "tp3": 110.0,
        "live_risk_multiplier": 0.5,
        "risk_bucket": "stock_intraday_breakout",
    }
    plan = build_order_plan(
        decision=decision, contract=_stock_contract(), depth=_depth(), cfg=_live_cfg(execution_mode="dry_run"),
    )
    assert plan.symbol == "AAPLSTOCK_USDT"
    assert plan.risk_budget_usdt == pytest.approx(5.0)
    assert plan.actual_risk_usdt <= 5.0


def test_live_plan_caps_ioc_below_first_target_when_stock_drift_cap_is_wider() -> None:
    decision = {
        "decision_id": "stock-tight-target", "signal_id": "stock_mexc:tp1-cap",
        "symbol": "AAPLSTOCK/USDT", "asset_class": "stock_futures",
        "mode": "stock_intraday", "direction": "long",
        "entry_mode": "BREAKOUT_CONTINUATION", "entry_price": 142.51,
        "original_stop": 141.29, "tp1": 143.50, "tp2": 144.38, "tp3": 145.68,
        "live_risk_multiplier": 0.5, "risk_bucket": "stock_intraday_breakout",
    }
    live_cfg = _live_cfg(execution_mode="dry_run")
    live_cfg.raw["entry_limits_by_mode"] = {
        "stock_intraday": {"max_entry_drift_bps": {"BREAKOUT_CONTINUATION": 100}}
    }
    plan = build_order_plan(
        decision=decision,
        contract=_stock_contract(),
        depth={"bids": [[142.44, 5000]], "asks": [[142.51, 5000]]},
        cfg=live_cfg,
    )
    assert plan.limit_price == pytest.approx(143.49)
    assert plan.original_stop < plan.limit_price < plan.tp1 < plan.tp2 < plan.tp3


def test_live_short_plan_caps_ioc_above_first_target() -> None:
    decision = {
        "decision_id": "stock-short-tight-target", "signal_id": "stock_mexc:short-tp1-cap",
        "symbol": "AAPLSTOCK/USDT", "asset_class": "stock_futures",
        "mode": "stock_intraday", "direction": "short",
        "entry_mode": "BREAKOUT_CONTINUATION", "entry_price": 142.50,
        "original_stop": 143.72, "tp1": 141.51, "tp2": 140.63, "tp3": 139.33,
        "live_risk_multiplier": 0.5, "risk_bucket": "stock_intraday_breakout",
    }
    live_cfg = _live_cfg(execution_mode="dry_run")
    live_cfg.raw["entry_limits_by_mode"] = {
        "stock_intraday": {"max_entry_drift_bps": {"BREAKOUT_CONTINUATION": 100}}
    }
    plan = build_order_plan(
        decision=decision,
        contract=_stock_contract(),
        depth={"bids": [[142.49, 5000]], "asks": [[142.56, 5000]]},
        cfg=live_cfg,
    )
    assert plan.limit_price == pytest.approx(141.52)
    assert plan.tp3 < plan.tp2 < plan.tp1 < plan.limit_price < plan.original_stop


def test_live_plan_rejects_when_current_quote_has_reached_first_target() -> None:
    decision = {
        "decision_id": "stock-already-at-target", "signal_id": "stock_mexc:stale-at-tp1",
        "symbol": "AAPLSTOCK/USDT", "asset_class": "stock_futures",
        "mode": "stock_intraday", "direction": "long",
        "entry_mode": "BREAKOUT_CONTINUATION", "entry_price": 142.50,
        "original_stop": 141.29, "tp1": 143.50, "tp2": 144.38, "tp3": 145.68,
        "live_risk_multiplier": 0.5, "risk_bucket": "stock_intraday_breakout",
    }
    live_cfg = _live_cfg(execution_mode="dry_run")
    live_cfg.raw["entry_limits_by_mode"] = {
        "stock_intraday": {"max_entry_drift_bps": {"BREAKOUT_CONTINUATION": 100}}
    }
    with pytest.raises(PlanRejected) as exc:
        build_order_plan(
            decision=decision,
            contract=_stock_contract(),
            depth={"bids": [[143.49, 5000]], "asks": [[143.50, 5000]]},
            cfg=live_cfg,
        )
    assert str(exc.value) == "ENTRY_TICK_EXCEEDS_DRIFT_CAP"
