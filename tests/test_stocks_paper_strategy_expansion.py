from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone

import pandas as pd

from scripts.run_default_market_schedule import build_cycle_steps
from src.execution.paper_entry_provenance import execution_mode_for_signal
from src.execution import paper_strategy_registry
from src.execution import stocks_swing_event_rs_pullback_paper as stock_swing
from src.execution import stocks_catalyst_rs_paper as catalyst
from src.execution import stocks_intraday_pullback_paper as pullback
from src.news import quality_gate
from src.signals import tracker
from src.signals.config import SignalTrackingConfig


UTC = timezone.utc
START = datetime(2026, 8, 6, 13, 30, tzinfo=UTC)


def _pullback_signal() -> dict:
    cfg = pullback.load_cfg()
    return {
        "signal_id": "pullback-test", "asset_class": "stocks", "mode": "intraday",
        "symbol": "AAPL", "direction": "long", "created_at": START.isoformat(),
        "entry_low": 99.5, "entry_high": 100.0, "entry_trigger": 100.0,
        "invalidation": 98.5, "tp1": 101.5, "tp2": 103.0, "tp3": 104.5,
        "raw_idea_json": json.dumps({"paper_entry_profile": cfg["profile_id"],
                                       "paper_lane": cfg["paper_lane"]}),
    }


def test_pullback_waits_for_touch_then_closed_vwap_hold():
    bars = pd.DataFrame([
        {"timestamp": START, "open": 100.2, "high": 100.3, "low": 99.7, "close": 99.9, "volume": 1000},
        {"timestamp": START + timedelta(minutes=15), "open": 99.9, "high": 100.7,
         "low": 99.8, "close": 100.6, "volume": 1500},
    ])
    pending = pullback.resolve_entry(signal=_pullback_signal(), candles=bars,
                                     now=START + timedelta(minutes=29), timeframe_seconds=900)
    assert pending["applied"] is True and pending["ready"] is False
    ready = pullback.resolve_entry(signal=_pullback_signal(), candles=bars,
                                   now=START + timedelta(minutes=31), timeframe_seconds=900)
    assert ready["ready"] is True
    assert ready["entry_mode"] == "PULLBACK_LIMIT"
    assert ready["entry_price"] == 100.6
    assert ready["paper_size_weight"] == 0.5


def test_pullback_v2_waits_for_directional_reclaim_body():
    bars = pd.DataFrame([
        {"timestamp": START, "open": 100.2, "high": 100.3, "low": 99.7,
         "close": 99.9, "volume": 1000},
        # Price closes above the zone and VWAP, but the red body does not
        # confirm a long reclaim. V2 waits instead of buying this bar.
        {"timestamp": START + timedelta(minutes=15), "open": 100.8, "high": 100.9,
         "low": 100.4, "close": 100.6, "volume": 1200},
        {"timestamp": START + timedelta(minutes=30), "open": 100.5, "high": 101.0,
         "low": 100.4, "close": 100.8, "volume": 1200},
    ])
    still_waiting = pullback.resolve_entry(
        signal=_pullback_signal(), candles=bars,
        now=START + timedelta(minutes=31), timeframe_seconds=900,
    )
    assert still_waiting["ready"] is False
    ready = pullback.resolve_entry(
        signal=_pullback_signal(), candles=bars,
        now=START + timedelta(minutes=46), timeframe_seconds=900,
    )
    assert ready["ready"] is True
    assert ready["entry_price"] == 100.8
    assert ready["reason"] == "zone_touch_then_directional_closed_15m_vwap_hold"


def test_pullback_v2_full_size_requires_confirmation_quality():
    signal = _pullback_signal()
    raw = json.loads(signal["raw_idea_json"])
    raw.update({
        "structured": {"atr_extension": 2.0},
        "intraday_actionability": {"sector_confirmation_status": "confirmed"},
    })
    signal["raw_idea_json"] = json.dumps(raw)
    bars = pd.DataFrame([
        {"timestamp": START, "open": 100.2, "high": 100.3, "low": 99.7,
         "close": 99.9, "volume": 1000},
        {"timestamp": START + timedelta(minutes=15), "open": 99.9, "high": 100.8,
         "low": 99.8, "close": 100.6, "volume": 1200},
    ])
    ready = pullback.resolve_entry(
        signal=signal, candles=bars,
        now=START + timedelta(minutes=31), timeframe_seconds=900,
    )
    assert ready["ready"] is True
    assert ready["paper_size_weight"] == 1.0
    assert ready["paper_size_reason"] == "pullback_v2_full_quality"


def test_pullback_legacy_v1_keeps_old_confirmation_and_identity():
    signal = _pullback_signal()
    raw = json.loads(signal["raw_idea_json"])
    raw["paper_entry_profile"] = "stocks_intraday_pullback_vwap_paper_v1"
    signal["raw_idea_json"] = json.dumps(raw)
    bars = pd.DataFrame([
        {"timestamp": START, "open": 100.2, "high": 100.3, "low": 99.7,
         "close": 99.9, "volume": 1000},
        {"timestamp": START + timedelta(minutes=15), "open": 100.8, "high": 100.9,
         "low": 100.4, "close": 100.6, "volume": 1200},
    ])
    ready = pullback.resolve_entry(
        signal=signal, candles=bars,
        now=START + timedelta(minutes=31), timeframe_seconds=900,
    )
    assert ready["ready"] is True
    assert ready["profile_id"] == "stocks_intraday_pullback_vwap_paper_v1"
    assert ready["paper_size_weight"] == 1.0
    assert ready["paper_size_reason"] == "pullback_v1_legacy_full_size"


def test_pullback_v1_and_v2_have_authoritative_execution_provenance():
    for profile in (
        "stocks_intraday_pullback_vwap_paper_v1",
        "stocks_intraday_pullback_vwap_paper_v2",
    ):
        provenance = execution_mode_for_signal({
            "paper_entry_profile": profile,
            "paper_execution_entry_mode": "PULLBACK_LIMIT",
        })
        assert provenance is not None
        assert provenance.entry_mode == "PULLBACK_LIMIT"
        assert provenance.profile_id == profile


def test_pullback_v2_size_reaches_tracker_outcome(monkeypatch):
    bars = pd.DataFrame([
        {"timestamp": START, "open": 100.2, "high": 100.3, "low": 99.7,
         "close": 99.9, "volume": 1000},
        {"timestamp": START + timedelta(minutes=15), "open": 99.9, "high": 100.8,
         "low": 99.8, "close": 100.6, "volume": 1200},
        {"timestamp": START + timedelta(minutes=30), "open": 100.6, "high": 101.0,
         "low": 100.5, "close": 100.8, "volume": 1100},
    ])
    monkeypatch.setattr(
        tracker, "_load_stocks_ohlcv_for_signal",
        lambda *args, **kwargs: (bars, "stocks", "15m"),
    )
    monkeypatch.setattr(tracker, "_promoted_entry_mode", lambda *args, **kwargs: {
        "blocked": True, "entry_mode": "UNCLASSIFIED", "reason": "generic_policy",
    })
    observed_at = START + timedelta(minutes=35)
    monkeypatch.setattr(
        tracker, "_current_stock_breakout_entry",
        lambda **_kwargs: (
            tracker._LevelTouches(
                triggered=True, triggered_at=observed_at.isoformat(), entry_price=100.7,
            ),
            tracker._EntryObservation(
                observed_at.isoformat(), 100.7, "point_in_time_current_bar", True,
                "fresh test quote", (START + timedelta(minutes=30)).isoformat(), "quote",
            ),
            "finnhub",
        ),
    )
    signal = _pullback_signal()
    signal.update({"tier": "B", "score": 76.0, "status": "waiting_for_entry"})
    outcome, status = tracker.track_signal(
        signal=signal, file_store=object(), project_config=object(),
        tracker_config=SignalTrackingConfig(), now=observed_at,
    )
    assert status == "triggered"
    assert getattr(outcome, "_paper_entry_profile") == pullback.load_cfg()["profile_id"]
    assert getattr(outcome, "_paper_execution_entry_mode") == "PULLBACK_LIMIT"
    assert getattr(outcome, "_paper_size_weight") == 0.5


def test_after_hours_pullback_plan_rolls_to_next_rth_session():
    signal = _pullback_signal()
    signal["created_at"] = datetime(2026, 8, 5, 22, 0, tzinfo=UTC).isoformat()
    bars = pd.DataFrame([
        {"timestamp": START, "open": 100.2, "high": 100.3, "low": 99.7, "close": 99.9, "volume": 1000},
        {"timestamp": START + timedelta(minutes=15), "open": 99.9, "high": 100.7,
         "low": 99.8, "close": 100.6, "volume": 1500},
    ])
    ready = pullback.resolve_entry(signal=signal, candles=bars,
                                   now=START + timedelta(minutes=31), timeframe_seconds=900)
    assert ready["ready"] is True
    assert ready["confirmation_at"] == "2026-08-06T14:00:00+00:00"


def test_catalyst_paper_accepts_only_fresh_clean_confirmation():
    cfg = catalyst.load_cfg()
    row = {"entry_ts": (START - timedelta(minutes=5)).isoformat(),
           "eligibility_status": "eligible", "is_clean_for_edge": 1,
           "evidence_cohort": "strict_v1", "entry_price": 100.0, "stop_price": 98.0,
           "tp1": 102.0, "tp2": 104.0, "tp3": 106.0}
    assert catalyst._fresh_rows([row], now=START, cfg=cfg) == [row]
    assert catalyst._fresh_rows([{**row, "is_clean_for_edge": 0}], now=START, cfg=cfg) == []
    assert catalyst._fresh_rows([{**row, "entry_ts": (START - timedelta(hours=2)).isoformat()}],
                                now=START, cfg=cfg) == []


def test_catalyst_resolver_does_not_replay_stale_confirmation():
    cfg = catalyst.load_cfg()
    signal = {"asset_class": "stocks", "mode": "intraday", "entry_trigger": 100.0,
              "raw_idea_json": json.dumps({"paper_entry_profile": cfg["profile_id"],
                                             "paper_lane": cfg["paper_lane"],
                                             "confirmation_at": (START - timedelta(minutes=5)).isoformat(),
                                             "confirmation_price": 100.0})}
    assert catalyst.resolve_entry(signal=signal, candles=pd.DataFrame(), now=START,
                                  timeframe_seconds=900) == {"applied": False}


def test_registry_and_scheduler_keep_stock_lanes_separate():
    registry = paper_strategy_registry.load_registry()
    assert registry["valid"] is True
    stocks = next(group for group in registry["groups"]
                  if group["scope"] == "paper" and group["asset_class"] == "stocks")
    assert {item["entry_mode"] for item in stocks["strategies"]} == {
        "PULLBACK_LIMIT", "BREAKOUT_CONTINUATION", "LIQUIDITY_SHOCK_RECLAIM"}
    stock_swing_cfg = stock_swing.load_cfg()
    assert stock_swing_cfg["live_enabled"] is False
    labels = [step[0] for step in build_cycle_steps(
        now=START, crypto_only=False, include_long_horizon=False,
        monitor_minutes=1, skip_reports=False)]
    for label in (
        "stocks intraday pullback VWAP hold (versioned Paper lane)",
        "stocks intraday breakout one-bar (versioned Paper lane)",
    ):
        assert label in labels
    assert "stocks catalyst RS continuation (versioned Paper lane)" not in labels
    assert "stocks swing event RS pullback (versioned Paper lane)" not in labels
    assert "stocks earnings gap continuation (isolated shadow)" not in labels


def test_redundant_source_failure_is_warning_not_quality_block(monkeypatch):
    monkeypatch.setattr(quality_gate, "run_gold_cases", lambda: {"failed": 0, "cases": 1,
                                                                 "passed": 1, "failures": []})
    monkeypatch.setattr(quality_gate, "production_replay", lambda *args, **kwargs: {
        "unresolved_symbol_tagged_24h": 0, "source_error": 2, "source_dead": 1,
        "source_blocking_error_dead": 0, "unmapped_impact": 0,
        "resolver_pending_persist": 0, "canonical_rows": 1, "policy_coverage_pct": 1.0,
        "recent_news_rows_24h": 1, "resolution_latency_seconds": {"p95": 10},
    })
    assert quality_gate.evaluate()["ready"] is True
