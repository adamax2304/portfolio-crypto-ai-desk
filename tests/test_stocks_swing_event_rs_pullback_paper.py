from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta, timezone

import pandas as pd

from src.execution import paper_actionability as pa
from src.execution import stocks_swing_event_rs_pullback_paper as strategy
from src.execution.paper_entry_provenance import execution_mode_for_signal
from src.models import TradeIdea
from src.signals.config import SignalTrackingConfig
from src.signals.registry import build_signal_from_idea
from src.signals import tracker


UTC = timezone.utc
QUALITY_PROFILE = "stocks_swing_event_rs_pullback_quality_paper_v1"
FLOW_PROFILE = "stocks_swing_event_rs_pullback_flow_paper_v1"


def _daily_frame() -> pd.DataFrame:
    rows = []
    start = datetime(2025, 1, 1, tzinfo=UTC)
    for i in range(230):
        close = 100.0
        rows.append({
            "timestamp": start + timedelta(days=i),
            "open": close,
            "high": close + 1.0,
            "low": close - 1.0,
            "close": close,
            "volume": 1_000_000,
            "atr14": 2.0,
            "atr14_prev": 2.0,
            "true_range": 2.0,
            "ret1": 0.0,
            "volume_ratio": 1.0,
            "dollar_volume_30d": 100_000_000.0,
            "rs20_spy": 0.05,
            "rs63_spy": 0.02,
            "rs20_sector": 0.02,
            "ema21": 100.0,
            "market_regime": "risk_on",
        })
    rows[222].update({"open": 100.0, "high": 107.0, "low": 99.0, "close": 106.0,
                      "ret1": 0.06, "true_range": 8.0, "volume_ratio": 2.0})
    rows[223].update({"open": 106.0, "high": 106.5, "low": 103.0, "close": 104.0})
    rows[224].update({"open": 104.0, "high": 105.0, "low": 101.0, "close": 103.0,
                      "ema21": 102.0})
    df = pd.DataFrame(rows)
    df.index = pd.to_datetime(df["timestamp"], utc=True)
    return df


def _signal(profile: str = QUALITY_PROFILE, size_weight: float = 0.5) -> dict:
    return {
        "signal_id": "stock-swing-event-rs",
        "asset_class": "stocks",
        "mode": "swing",
        "symbol": "MSFT",
        "direction": "long",
        "tier": "B",
        "score": 78.0,
        "created_at": datetime(2026, 9, 1, tzinfo=UTC).isoformat(),
        "entry_low": 100.0,
        "entry_high": 101.0,
        "entry_trigger": 101.0,
        "invalidation": 95.0,
        "tp1": 113.0,
        "tp2": 119.0,
        "tp3": 125.0,
        "raw_idea_json": json.dumps({
            "paper_entry_profile": profile,
            "paper_lane": "paper_stocks_swing_event_rs_pullback",
            "paper_execution_entry_mode": "EVENT_RS_PULLBACK",
            "paper_size_weight": size_weight,
            "validity_window_hours": 600,
            "setup": {
                "entry_low": 100.0,
                "entry_high": 101.0,
                "invalidation": 95.0,
                "tp1": 113.0,
                "tp2": 119.0,
                "tp3": 125.0,
            },
            "stock_swing_event_rs_pullback": {"size_weight": size_weight},
        }),
    }


def test_candidate_detector_finds_daily_event_rs_pullback():
    cfg = strategy.load_cfg()
    profile = next(p for p in cfg["profiles"] if p["profile_id"] == QUALITY_PROFILE)
    candidate = strategy._candidate_for_confirmation(
        symbol="MSFT",
        df=_daily_frame(),
        profile=profile,
        cfg=cfg,
        confirmation_idx=224,
        sector="technology",
    )
    assert candidate is not None
    assert candidate["profile_id"] == QUALITY_PROFILE
    assert candidate["entry_mode"] == "EVENT_RS_PULLBACK"
    assert candidate["size_weight"] == 1.0
    assert candidate["tier"] in {"A", "B"}


def test_stock_swing_event_rs_has_profile_provenance_and_validity():
    created = datetime(2026, 9, 1, tzinfo=UTC)
    idea = TradeIdea(
        symbol="MSFT", direction="long", score=78.0, confidence="medium",
        risk_level="medium", timeframe="1d", tier="B", mode="swing",
        asset_class="stocks", thesis="daily event RS pullback", evidence=[],
        counterarguments=[], entry_plan="100-101", invalidation="95",
        targets=["113", "119", "125"], what_to_monitor=[], avoid_conditions=[],
        data_sources_used=[], raw=json.loads(_signal()["raw_idea_json"]),
    )
    signal = build_signal_from_idea(
        idea, config=SignalTrackingConfig(), report_id="test",
        created_at=created.isoformat(),
    )
    raw = json.loads(signal.raw_idea_json)
    assert signal.validity_window_hours == 600
    assert signal.expires_at == (created + timedelta(hours=600)).strftime("%Y-%m-%dT%H:%M:%S+00:00")
    assert raw["paper_entry_profile"] == QUALITY_PROFILE
    assert raw["paper_execution_entry_mode"] == "EVENT_RS_PULLBACK"
    assert raw["paper_size_weight"] == 0.5


def test_stock_swing_event_rs_actionability_is_narrow_exception():
    conn = sqlite3.connect(":memory:")
    allowed = pa.resolve_paper_actionability(
        conn, "s1", "stocks", "swing", "B", signal=_signal(size_weight=0.5),
    )
    assert allowed["source"] == "stocks_swing_event_rs_profile"
    assert allowed["paper_action"] == "HALF_SIZE"
    assert allowed["size_weight"] == 0.5

    blocked = pa.resolve_paper_actionability(
        conn, "s2", "stocks", "swing", "B", signal={"raw_idea_json": json.dumps({})},
    )
    assert blocked["paper_action"] == "NOT_ACTIONABLE"
    assert blocked["size_weight"] == 0.0


def test_archived_stock_swing_event_rs_is_not_in_active_tracker_registry():
    assert tracker._stock_paper_profile_timeframe(_signal()) is None


def test_profile_execution_mode_mapping_includes_both_sleeves():
    for profile in (QUALITY_PROFILE, FLOW_PROFILE):
        provenance = execution_mode_for_signal({
            "paper_entry_profile": profile,
            "paper_execution_entry_mode": "EVENT_RS_PULLBACK",
        })
        assert provenance is not None
        assert provenance.entry_mode == "EVENT_RS_PULLBACK"
