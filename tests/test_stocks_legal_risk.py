"""Regression tests for PART 3 fix — stocks legal/headline risk gate.

Cycle-2 of the 12h scheduler on 2026-05-29 rated **SMCI A-tier (82.52,
triggered)** purely on price/momentum despite an **active federal
indictment**, multiple securities class-action filings, and a prior E&Y
auditor resignation. The deterministic pipeline was structurally blind to
this category of risk.

This module pins three things:

1. ``detect_legal_risk`` recognises the SMCI-style headline categories
   (indictment, SEC/DOJ, auditor, class action) and marks them blocking.
2. The ``StockTradeIdeaAgent`` propagates the assessment into
   ``avoid_conditions``, ``cap_reasons``, and ``raw.legal_risk`` while
   keeping the underlying tier/score unchanged (the gate is hygiene, not
   scoring).
3. ``MaterialImprovementChecker`` blocks Telegram with
   ``alert_type='legal_block'`` when the ``proposed_signals`` row carries
   the marker.
"""

from __future__ import annotations

import json

from src.stocks.legal_risk import (
    AVOID_CONDITION_MARKER,
    BLOCKING_CATEGORIES,
    LegalRiskAssessment,
    detect_legal_risk,
    signal_has_legal_block,
)
from src.stocks.monitor import MaterialImprovementChecker


# ---------------------------------------------------------------------------
# Detection — fixture headlines reproducing the SMCI cycle-2 case
# ---------------------------------------------------------------------------


SMCI_HEADLINES = [
    {
        "title": "Super Micro hit with federal indictment over alleged AI server diversion to China",
        "source": "CNBC",
        "url": "https://www.cnbc.com/example/smci-indictment",
        "published_at": "2026-05-27",
    },
    {
        "title": "SMCI faces securities class-action lawsuit after Q3 revenue miss and disclosure delay",
        "source": "Yahoo Finance",
        "url": "https://finance.yahoo.com/example/smci-class-action",
        "published_at": "2026-05-26",
    },
    {
        "title": "Ernst & Young auditor resigned from Super Micro citing disclosure concerns",
        "source": "StockTitan",
        "url": "https://stocktitan.net/example/smci-ey-resigns",
        "published_at": "2026-05-20",
    },
]


def test_smci_headlines_detected_as_blocking_high_severity():
    assessment = detect_legal_risk(SMCI_HEADLINES)
    assert assessment.blocking is True
    assert assessment.severity == "high"
    assert "indictment" in assessment.categories
    assert "class_action" in assessment.categories
    assert "auditor" in assessment.categories
    assert assessment.avoid_condition is not None
    assert assessment.avoid_condition.startswith(AVOID_CONDITION_MARKER)
    assert "legal_headline_risk" in (assessment.cap_reason or "")
    assert assessment.counter_thesis is not None
    assert "ACTIVE LEGAL HEADLINE RISK" in assessment.counter_thesis


def test_routine_news_does_not_trigger_legal_risk():
    benign = [
        {"title": "AAPL launches new WWDC keynote with developer tools update"},
        {"title": "NVDA Q2 earnings beat estimates, stock rises 5%"},
        {"title": "LLY obesity drug shows strong Phase 3 results"},
    ]
    assessment = detect_legal_risk(benign)
    assert assessment.blocking is False
    assert assessment.severity == "none"
    assert assessment.categories == []
    assert assessment.avoid_condition is None
    assert assessment.cap_reason is None


def test_low_severity_news_is_advisory_not_blocking():
    """A standalone restatement note surfaces as advisory but does NOT
    block Telegram. We only auto-block on hard categories."""

    advisory = [
        {"title": "Company X files financial restatement for fiscal 2024"},
    ]
    assessment = detect_legal_risk(advisory)
    assert assessment.categories == ["restatement"]
    assert assessment.blocking is False
    assert assessment.severity == "medium"
    assert assessment.avoid_condition is None
    assert assessment.cap_reason is None
    # Counter-thesis advisory note still surfaces.
    assert assessment.counter_thesis is not None
    assert "Headline note" in assessment.counter_thesis


def test_sec_charges_alone_is_blocking():
    hits = [{"title": "SEC charges Acme Corp with accounting fraud"}]
    assessment = detect_legal_risk(hits)
    assert assessment.blocking is True
    assert "sec_doj" in assessment.categories
    assert "securities_fraud" in assessment.categories


def test_doj_probe_is_blocking():
    hits = [{"title": "DOJ launches investigation into Acme Corp executive trades"}]
    assessment = detect_legal_risk(hits)
    assert assessment.blocking is True
    assert "sec_doj" in assessment.categories


def test_going_concern_warning_is_blocking():
    hits = [{"title": "Acme Corp 10-Q discloses going concern doubt"}]
    assessment = detect_legal_risk(hits)
    assert assessment.blocking is True
    assert "going_concern" in assessment.categories or "auditor" in assessment.categories


def test_blocking_categories_set_is_strict():
    """Pin which categories auto-block to prevent silent expansion."""

    assert BLOCKING_CATEGORIES == frozenset({
        "indictment",
        "sec_doj",
        "securities_fraud",
        "auditor",
        "class_action",
        "going_concern",
    })


# ---------------------------------------------------------------------------
# Monitor integration — MaterialImprovementChecker blocks legal-flagged signals
# ---------------------------------------------------------------------------


def _smci_like_signal_row(*, tier: str = "A") -> dict:
    """A ``proposed_signals``-shaped dict reproducing the SMCI cycle-2
    state: A-tier triggered, full setup, with the legal-risk avoid
    marker persisted by the trade-idea agent."""

    avoid_marker = f"{AVOID_CONDITION_MARKER}: class_action,indictment,auditor"
    return {
        "signal_id": "sig_smci_test",
        "symbol": "SMCI",
        "asset_class": "stocks",
        "tier": tier,
        "score": 82.52,
        "direction": "long",
        "mode": "intraday",
        "invalidation": 28.5,
        "entry_low": 31.0,
        "entry_high": 32.0,
        "tp1": 35.0,
        "no_entry_conditions_json": json.dumps([
            "do not chase if price is > 2 ATR from planned entry",
            "do not enter against a clear SPY breakdown",
            avoid_marker,
        ]),
    }


def test_signal_has_legal_block_true_for_marker():
    assert signal_has_legal_block(_smci_like_signal_row()) is True


def test_signal_has_legal_block_false_without_marker():
    row = {
        "tier": "A",
        "invalidation": 28.5,
        "no_entry_conditions_json": json.dumps(["do not chase"]),
    }
    assert signal_has_legal_block(row) is False


def test_signal_has_legal_block_handles_missing_field():
    row = {"tier": "A", "invalidation": 28.5}
    assert signal_has_legal_block(row) is False


def test_signal_has_legal_block_handles_bad_json():
    row = {
        "tier": "A",
        "invalidation": 28.5,
        "no_entry_conditions_json": "not-json-at-all",
    }
    assert signal_has_legal_block(row) is False


def test_smci_new_signal_is_blocked_by_legal_gate():
    """The cycle-2 SMCI regression: A-tier brand-new signal should be
    suppressed by the gate even though it would otherwise be a
    ``new_signal`` alert."""

    checker = MaterialImprovementChecker()
    decision = checker.decide(
        current=_smci_like_signal_row(tier="A"),
        last_alert=None,
    )
    assert decision.should_send is False
    assert decision.alert_type == "legal_block"
    assert "legal headline risk" in decision.reason


def test_smci_tier_upgrade_is_blocked_by_legal_gate():
    """A B→A upgrade on a legally-flagged symbol must still be blocked."""

    checker = MaterialImprovementChecker()
    decision = checker.decide(
        current=_smci_like_signal_row(tier="A"),
        last_alert={
            "tier": "B",
            "score": 75.0,
            "payload_json": '{"invalidation": 28.5}',
        },
    )
    assert decision.should_send is False
    assert decision.alert_type == "legal_block"


def test_clean_a_tier_without_legal_flag_still_fires_new_signal():
    """Sanity: the gate doesn't break normal flow for clean A-tier names."""

    clean_row = {
        "tier": "A",
        "score": 88.0,
        "direction": "long",
        "invalidation": 100.0,
        "entry_low": 102.0,
        "entry_high": 103.0,
        "no_entry_conditions_json": json.dumps([
            "do not chase if price is > 2 ATR from planned entry"
        ]),
    }
    checker = MaterialImprovementChecker()
    decision = checker.decide(current=clean_row, last_alert=None)
    assert decision.should_send is True
    assert decision.alert_type == "new_signal"


# ---------------------------------------------------------------------------
# Trade-idea agent integration — SMCI ends up with the marker
# ---------------------------------------------------------------------------


def test_trade_idea_agent_propagates_legal_marker_to_avoid_conditions(tmp_path):
    """End-to-end inside the agent: given SMCI news + an A-tier score
    row, the produced TradeIdea must carry the avoid-condition marker
    and a cap_reason."""

    from src.stocks.agents.trade_idea_agent import StockTradeIdeaAgent
    from src.stocks.configs.loader import load_stocks_config
    from src.config import load_config
    from src.storage.file_store import FileStore
    from src.storage.sqlite import SQLiteStore

    config = load_config()
    stocks_config = load_stocks_config(config.root)
    file_store = FileStore(tmp_path)
    db = SQLiteStore(tmp_path / "desk.sqlite")
    db.init_db()
    agent = StockTradeIdeaAgent(config, stocks_config, file_store, db)

    payload = agent.run(
        scoring_payload={
            "scores": [
                {
                    "symbol": "SMCI",
                    "tier": "A",
                    "direction": "long",
                    "final_score": 82.52,
                    "confidence": "high",
                    "cap_reasons": [],
                }
            ]
        },
        technical_payload={
            "setups": [
                {
                    "symbol": "SMCI",
                    "entry_low": 31.0,
                    "entry_high": 32.0,
                    "invalidation": 28.5,
                    "tp1": 35.0,
                    "tp2": 38.0,
                    "trend": "uptrend",
                }
            ]
        },
        news_payload={"hits_by_symbol": {"SMCI": SMCI_HEADLINES}},
        earnings_payload={"risks": []},
        rs_payload={"rows": []},
        regime_payload={"regime": {"label": "bullish"}},
        sector_payload={},
        risk_payload={"by_symbol": {}},
        mode="intraday",
    )

    ideas = payload["ideas"]
    assert len(ideas) == 1
    smci = ideas[0]
    # PART 17 update — the gate now ACTIVELY demotes A/B → C when a
    # blocking legal flag is present. The score stays untouched for
    # auditability; the tier reflects the safety override.
    assert smci["tier"] == "C", smci["tier"]
    assert smci["score"] == 82.52
    # Marker reached avoid_conditions (→ persisted as no_entry_conditions).
    avoid = smci["avoid_conditions"]
    assert any(
        isinstance(c, str) and c.startswith(AVOID_CONDITION_MARKER) for c in avoid
    ), avoid
    # cap_reasons records the block reason.
    assert any(
        isinstance(c, str) and c.startswith("legal_headline_risk:")
        for c in smci["cap_reasons"]
    ), smci["cap_reasons"]
    # raw.legal_risk records the structured assessment for auditing.
    raw_legal = (smci.get("raw") or {}).get("legal_risk") or {}
    assert raw_legal.get("blocking") is True
    assert raw_legal.get("severity") == "high"
    assert {"indictment", "class_action", "auditor"} <= set(raw_legal.get("categories") or [])
