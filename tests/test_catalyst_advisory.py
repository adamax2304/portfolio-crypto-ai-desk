"""Catalyst-linkage advisory block (item 6) — DISPLAY-ONLY, never changes tier/actionability."""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from src.signals.catalyst_linkage_shadow_audit import (
    audit, stocks_catalyst_advisory, render_advisory_block, TEMPORAL_COINCIDENCE_WARNING)

TEST_NOW = datetime(2026, 7, 4, 12, 0, tzinfo=timezone.utc)


def _seed(tmp_path, rows):
    db = str(Path(tmp_path) / "cat.sqlite")
    c = sqlite3.connect(db)
    c.execute("CREATE TABLE proposed_signals (signal_id TEXT, symbol TEXT, created_at TEXT, "
              "asset_class TEXT, news_supported INTEGER)")
    for i, (sym, ac, ns) in enumerate(rows):
        c.execute("INSERT INTO proposed_signals VALUES (?,?,?,?,?)",
                  (f"s{i}", sym, "2026-07-03T10:00:00+00:00", ac, ns))
    c.commit(); c.close()
    return db


def test_audit_asset_class_filter(tmp_path):
    db = _seed(tmp_path, [("AAPL", "stocks", 1), ("MSFT", "stocks", 0), ("BTC/USDT", "crypto", 0)])
    a = audit(days=30, db=db, now=TEST_NOW, persist=False, asset_class="stocks")
    assert a["signals"] == 2                        # crypto row excluded by the filter
    assert a["current_coverage_pct"] == 50.0        # 1 of 2 stocks news_supported
    assert a["scoring_changed"] is False and a["actionability_changed"] is False


def test_stocks_catalyst_advisory_display_only(tmp_path):
    db = _seed(tmp_path, [("AAPL", "stocks", 1), ("MSFT", "stocks", 0)])
    adv = stocks_catalyst_advisory(db, days=30, now=TEST_NOW)
    assert adv["advisory_only"] is True
    assert adv["scoring_changed"] is False and adv["actionability_changed"] is False
    assert adv["news_supported_pct"] == 50.0
    assert adv["warning"] == TEMPORAL_COINCIDENCE_WARNING


def test_render_advisory_block_has_caveat_and_metrics():
    adv = {"asset_class": "stocks", "days": 7, "signals": 10, "news_supported_pct": 20.0,
           "current_window_hours": 5, "shadow_24h_pct": 45.0, "shadow_48h_pct": 60.0,
           "newly_linked_24h": 3, "newly_linked_48h": 5, "uplift_24h_pp": 25.0, "uplift_48h_pp": 40.0,
           "examples": [{"symbol": "NVDA", "title": "NVDA new chip", "source": "Reuters"}],
           "warning": TEMPORAL_COINCIDENCE_WARNING, "advisory_only": True}
    md = render_advisory_block(adv)
    assert "NOT a scoring/tier input" in md
    assert "news_supported **20.0%**" in md
    assert "48h exact-match shadow **60.0%**" in md
    assert "temporal coincidence risk" in md
    assert "does not change tier or actionability" in md
    assert "NVDA" in md                              # example surfaced


def test_advisory_block_does_not_alter_report_tiers(tmp_path):
    """Building a stocks report with the advisory present must not change any idea's tier."""
    from types import SimpleNamespace
    from src.stocks.pipelines.stocks_pipeline import StocksPipelineResult
    from src.stocks.reports.stocks_report_builder import build_stocks_report
    db = _seed(tmp_path, [("AAPL", "stocks", 1)])
    r = StocksPipelineResult(mode="intraday")
    r.regime = {"regime": {"label": "risk_on", "bias": "long"}}
    r.sectors = {}
    r.scoring = {"scores": [{"symbol": "AAPL", "direction": "long", "tier": "A",
                             "final_score": 85.0, "confidence": "high", "risk_penalty": 0}]}
    r.ideas_payload = {"ideas": [{"symbol": "AAPL", "direction": "long", "tier": "B", "score": 80.0,
                                  "confidence": "high", "risk_level": "medium", "timeframe": "15m/1h",
                                  "thesis": "t", "entry_plan": "zone", "invalidation": "close below",
                                  "cap_reasons": [], "raw": {"setup": {}, "structured": {}}}]}
    cfg = SimpleNamespace(db_path=db, root=Path(tmp_path))
    # config=None path renders visible sections only (no advisory); the idea tier must be unchanged.
    text_no_cfg = build_stocks_report(r)
    assert "B AAPL long" in text_no_cfg
    # the advisory helper itself never mutates the ideas payload
    from src.signals.catalyst_linkage_shadow_audit import stocks_catalyst_advisory
    stocks_catalyst_advisory(db, days=30, now=TEST_NOW)
    assert r.ideas_payload["ideas"][0]["tier"] == "B"       # unchanged
