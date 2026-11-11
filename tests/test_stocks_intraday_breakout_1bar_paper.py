from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta, timezone

import pandas as pd

from scripts.run_default_market_schedule import build_cycle_steps
from src.execution import stocks_intraday_breakout_1bar_paper as profile
from src.models import TradeIdea
from src.signals import tracker
from src.signals.config import SignalTrackingConfig
from src.signals.registry import _safe_idea_payload


UTC = timezone.utc
START = datetime(2026, 7, 14, 13, 30, tzinfo=UTC)  # 09:30 New York


def _bars() -> pd.DataFrame:
    rows = [
        (100.0, 100.3, 99.8, 100.0),
        (100.2, 101.1, 100.0, 100.7),
        (100.7, 102.1, 100.6, 101.6),  # first close above trigger + VWAP
        (101.6, 102.0, 101.3, 101.7),
    ]
    return pd.DataFrame([
        {"timestamp": START + timedelta(minutes=15 * i), "open": o, "high": h,
         "low": l, "close": c, "volume": 1000.0 + i * 100}
        for i, (o, h, l, c) in enumerate(rows)
    ])


def _signal() -> dict:
    cfg = profile.load_cfg()
    return {
        "signal_id": "onebar-test", "asset_class": "stocks", "mode": "intraday",
        "symbol": "TEST", "direction": "long", "tier": "A", "status": "waiting_for_entry",
        "created_at": START.isoformat(), "entry_low": 100.0, "entry_high": 101.0,
        "entry_trigger": 101.0, "suggested_entry": 101.0, "invalidation": 99.0,
        "tp1": 103.0, "tp2": 104.0, "tp3": 105.0, "risk_per_unit": 2.0,
        "raw_idea_json": json.dumps({"paper_entry_profile": cfg["profile_id"],
                                       "paper_lane": cfg["paper_lane"]}),
    }


def _idea(tier: str = "A") -> TradeIdea:
    return TradeIdea(
        symbol="TEST", direction="long", score=80, confidence="high", risk_level="low",
        timeframe="15m", tier=tier, mode="intraday", asset_class="stocks", thesis="breakout continuation",
        evidence=[], counterarguments=[], entry_plan="entry", invalidation="99", targets=[],
        what_to_monitor=[], avoid_conditions=[], data_sources_used=[],
        raw={"pre_gate_tier": "A", "setup": {"entry_low": 100.0, "entry_high": 101.0,
             "invalidation": 99.0, "tp1": 103.0, "tp2": 104.0, "tp3": 105.0}},
    )


def test_profile_waits_for_completed_15m_confirmation_then_enters_at_close():
    pending = profile.resolve_entry(signal=_signal(), candles=_bars(), now=START + timedelta(minutes=43),
                                    timeframe_seconds=900)
    assert pending["applied"] is True and pending["ready"] is False

    ready = profile.resolve_entry(signal=_signal(), candles=_bars(), now=START + timedelta(minutes=46),
                                  timeframe_seconds=900)
    assert ready["ready"] is True
    assert ready["entry_price"] == 101.6
    assert ready["confirmation_at"] == "2026-07-14T14:15:00+00:00"
    # Exit simulation begins after the closed confirmation bar, never inside it.
    assert ready["candles"].iloc[0]["timestamp"] == START + timedelta(minutes=45)


def test_after_hours_plan_waits_for_next_rth_session_not_the_old_day():
    signal = _signal()
    signal["created_at"] = datetime(2026, 7, 13, 22, 0, tzinfo=UTC).isoformat()  # after NY close
    ready = profile.resolve_entry(signal=signal, candles=_bars(),
                                  now=START + timedelta(minutes=46), timeframe_seconds=900)
    assert ready["ready"] is True
    assert ready["confirmation_at"] == "2026-07-14T14:15:00+00:00"


def test_profile_marker_survives_registry_payload_and_selection_is_narrow():
    cfg = profile.load_cfg()
    tagged = profile.tag_idea(_idea(), cfg)
    payload = _safe_idea_payload(tagged)
    assert payload["paper_entry_profile"] == cfg["profile_id"]
    assert payload["paper_lane"] == cfg["paper_lane"]

    cfg = {**cfg, "symbols": ["TEST"]}
    assert [item.symbol for item in profile.select_ideas([_idea()], cfg)] == ["TEST"]
    blocked_c = _idea("C")
    blocked_c.raw["pre_gate_tier"] = "C"
    assert profile.select_ideas([blocked_c], cfg) == []

    legal_only_c = _idea("C")
    legal_only_c.raw["pre_gate_tier"] = "A"
    legal_only_c.raw["cap_reasons"] = ["legal_headline_risk: class_action"]
    assert profile.select_ideas([legal_only_c], cfg) == []

    preopen_c = _idea("C")
    preopen_c.raw["pre_gate_tier"] = "A"
    preopen_c.raw["cap_reasons"] = ["market_closed_intraday_planning_only"]
    assert [item.symbol for item in profile.select_ideas([preopen_c], cfg)] == ["TEST"]


def test_preopen_plan_does_not_consume_the_rth_executable_slot():
    cfg = profile.load_cfg()
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE proposed_signals (created_at TEXT, tier TEXT, raw_idea_json TEXT, "
        "asset_class TEXT, mode TEXT, symbol TEXT)"
    )
    plan_raw = {
        "paper_entry_profile": cfg["profile_id"],
        "pre_gate_tier": "A",
        "cap_reasons": ["market_closed_intraday_planning_only"],
    }
    conn.execute(
        "INSERT INTO proposed_signals VALUES (?,?,?,?,?,?)",
        (START.isoformat(), "C", json.dumps(plan_raw), "stocks", "intraday", "TEST"),
    )
    session = profile._session_key(START.isoformat())

    assert profile._already_registered(
        conn, symbol="TEST", session=session, profile_id=cfg["profile_id"],
        candidate_tier="C", candidate_raw=plan_raw,
    ) is True
    assert profile._already_registered(
        conn, symbol="TEST", session=session, profile_id=cfg["profile_id"],
        candidate_tier="A", candidate_raw={"pre_gate_tier": "A"},
    ) is False

    conn.execute(
        "INSERT INTO proposed_signals VALUES (?,?,?,?,?,?)",
        (START.isoformat(), "A", json.dumps({"paper_entry_profile": cfg["profile_id"]}),
         "stocks", "intraday", "TEST"),
    )
    assert profile._already_registered(
        conn, symbol="TEST", session=session, profile_id=cfg["profile_id"],
        candidate_tier="A", candidate_raw={"pre_gate_tier": "A"},
    ) is True
    conn.close()


def test_tracker_uses_profile_confirmation_even_if_generic_classifier_would_block(monkeypatch):
    monkeypatch.setattr(tracker, "_load_stocks_ohlcv_for_signal", lambda *args, **kwargs: (_bars(), "stocks", "15m"))
    monkeypatch.setattr(tracker, "_promoted_entry_mode", lambda *args, **kwargs: {
        "blocked": True, "entry_mode": "UNCLASSIFIED", "reason": "generic_policy"
    })
    observed_at = START + timedelta(minutes=50)
    monkeypatch.setattr(
        tracker, "_current_stock_breakout_entry",
        lambda **_kwargs: (
            tracker._LevelTouches(triggered=True, triggered_at=observed_at.isoformat(), entry_price=101.2),
            tracker._EntryObservation(
                observed_at.isoformat(), 101.2, "point_in_time_current_bar", True,
                "fresh test quote", (START + timedelta(minutes=45)).isoformat(), "quote",
            ),
            "finnhub",
        ),
    )
    outcome, status = tracker.track_signal(
        signal=_signal(), file_store=object(), project_config=object(), tracker_config=SignalTrackingConfig(),
        now=START + timedelta(minutes=50),
    )
    assert outcome.entry_triggered is True
    assert outcome.entry_price_used == 101.2
    assert status == "triggered"
    assert getattr(outcome, "_entry_time_basis") == "point_in_time_current_bar"
    assert getattr(outcome, "_paper_entry_profile") == profile.load_cfg()["profile_id"]


def test_tracker_requires_fresh_quote_after_onebar_confirmation(monkeypatch):
    monkeypatch.setattr(tracker, "_load_stocks_ohlcv_for_signal", lambda *args, **kwargs: (_bars(), "stocks", "15m"))
    monkeypatch.setattr(tracker, "_promoted_entry_mode", lambda *args, **kwargs: {
        "blocked": True, "entry_mode": "UNCLASSIFIED", "reason": "generic_policy"
    })
    monkeypatch.setattr(
        tracker, "_current_stock_breakout_entry",
        lambda **_kwargs: (None, tracker._EntryObservation(
            None, None, "stock_quote_unavailable", False, "quote unavailable", None, "quote"), "finnhub"),
    )
    outcome, status = tracker.track_signal(
        signal=_signal(), file_store=object(), project_config=object(), tracker_config=SignalTrackingConfig(),
        now=START + timedelta(minutes=50),
    )
    assert outcome.entry_triggered is False
    assert status == "waiting_for_entry"


def test_quote_revalidation_accepts_only_fresh_price_inside_no_chase_window(monkeypatch):
    moment = START + timedelta(minutes=50)
    monkeypatch.setattr("src.stocks.market_calendar.is_us_cash_session_open", lambda _now: True)
    monkeypatch.setattr("src.stocks.realtime_provider.finnhub_quote", lambda _symbol: {
        "ok": True, "source": "finnhub", "price": 101.2, "observed_at": moment.isoformat(),
    })
    touches, observation, source = tracker._current_stock_breakout_entry(
        signal=_signal(), promoted_entry={"entry_trigger": 101.0},
        confirmation_at=(START + timedelta(minutes=45)).isoformat(), now=moment,
    )
    assert source == "finnhub"
    assert touches is not None and touches.entry_price == 101.2
    assert observation.currently_executable is True
    assert observation.time_basis == "point_in_time_current_bar"


def test_llm_packet_labels_profile_and_default_cycle_keeps_preus_handoff_separate(tmp_path):
    db = tmp_path / "reviews.sqlite"
    conn = sqlite3.connect(db)
    conn.execute("CREATE TABLE proposed_signals (signal_id TEXT, symbol TEXT, direction TEXT, tier TEXT, created_at TEXT, raw_idea_json TEXT, asset_class TEXT, mode TEXT)")
    conn.execute("INSERT INTO proposed_signals VALUES (?,?,?,?,?,?,?,?)", (
        "onebar-test", "TEST", "long", "A", "2026-07-31T10:00:00+00:00",
        _signal()["raw_idea_json"], "stocks", "intraday"))
    conn.commit()
    conn.close()
    from src.stocks import intraday_llm_review
    text = (tmp_path / "packet.md")
    result = intraday_llm_review.build_packet(db=str(db), out_dir=str(tmp_path), lookback_hours=999999)
    assert "profile=stocks_intraday_breakout_1bar_paper_v1" in open(result, encoding="utf-8").read()

    steps = build_cycle_steps(now=datetime(2026, 7, 15, 12, tzinfo=UTC), crypto_only=False,
                              include_long_horizon=False, monitor_minutes=1, skip_reports=False)
    labels = [step[0] for step in steps]
    assert "stocks intraday breakout one-bar (versioned Paper lane)" in labels
    # The exact pre-US snapshot is intentionally built by the dedicated 09:00
    # ET hand-off.  A regular cycle must not overwrite it after its review
    # deadline; its cadence is verified in test_preus_schedule_dst.py.
    assert "stocks pre-US review candidate bundle (advisory)" not in labels
