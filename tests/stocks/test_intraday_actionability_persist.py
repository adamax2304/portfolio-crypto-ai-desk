"""Integration-bug fix #3 — the SI-1..SI-5 gate fields must persist into
proposed_signals.raw_idea_json (via registry._safe_idea_payload) so the SI-7 post-trade classifier,
the SI-6 LLM packet, and the report/UI can read exactly why a stocks-intraday A/B was demoted.
"""
from __future__ import annotations

import json

from src.models import TradeIdea
from src.signals.config import SignalTrackingConfig
from src.signals.registry import _safe_idea_payload, build_signal_from_idea


def _idea(mode="intraday", tier="A", asset_class="stocks", with_gate=True):
    raw = {"setup": {"entry_low": 99.0, "entry_high": 100.0, "invalidation": 97.0, "tp1": 103.0},
           "pre_gate_tier": "A", "final_tier": tier, "demoted_by_gate": tier != "A"}
    if with_gate:
        raw["intraday_actionability"] = {
            "market_context_status": "conflict", "market_context_reason": "market_context_conflict",
            "session_phase": "morning", "demote_reasons": ["market_context_conflict"]}
    return TradeIdea(symbol="NVDA", direction="long", score=88.0, confidence="high",
                     risk_level="medium", timeframe="15m", tier=tier, mode=mode,
                     asset_class=asset_class, thesis="t", evidence=["e"], counterarguments=["c"],
                     entry_plan="p", invalidation="97", targets=["103"], what_to_monitor=["m"],
                     avoid_conditions=["a"], data_sources_used=["yfinance"], raw=raw)


def test_intraday_actionability_in_payload():
    payload = _safe_idea_payload(_idea())
    assert payload["intraday_actionability"]["market_context_reason"] == "market_context_conflict"
    assert payload["intraday_actionability"]["demote_reasons"] == ["market_context_conflict"]


def test_intraday_actionability_round_trips_into_raw_idea_json():
    sig = build_signal_from_idea(_idea(), config=SignalTrackingConfig(), report_id="r1",
                                 asset_class="stocks")
    assert sig is not None
    d = json.loads(sig.raw_idea_json)
    assert d["intraday_actionability"]["session_phase"] == "morning"
    assert d["intraday_actionability"]["demote_reasons"] == ["market_context_conflict"]


def test_idea_without_gate_fields_is_empty_not_error():
    # crypto / non-gated ideas simply carry {} — never KeyError / None.
    payload = _safe_idea_payload(_idea(mode="scalp", asset_class="crypto", with_gate=False))
    assert payload["intraday_actionability"] == {}
