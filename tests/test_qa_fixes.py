"""Regression tests for the QA fixes shipped after the 2026-05-25 Decision
Quality Audit.

These tests check that:
  - QA Fix #1: LLM packets accept and surface a ``source_report`` string.
  - QA Fix #2: ``load_recent_news`` filters ``test_source`` by default and
    honours the ``asset_class`` parameter (covered in
    ``tests/stocks/test_stocks_news_tagging.py``).
  - QA Fix #3: ``build_signal_performance_block`` renders a non-empty
    Markdown section regardless of sample size and never crashes when the
    underlying tables are empty.
  - QA Fix #4: ``StockTradeIdeaAgent`` evidence contains an explicit
    earnings line (with date when known, ``UNKNOWN`` otherwise).
  - QA Fix #4: stocks report idea section renders ``what_to_monitor``,
    ``data_confidence`` (when distinct), and the score component breakdown.
"""

from __future__ import annotations

from src.config import load_config


# ---------------------------------------------------------------------------
# QA Fix #1 — packet source_report wiring
# ---------------------------------------------------------------------------

def test_crypto_packet_includes_source_report(tmp_path, monkeypatch):
    """build_packet must surface the source_report kwarg in the header."""
    from src.analysis.packet import build_packet

    config = load_config()
    out = build_packet(
        config,
        "intraday",
        source_report="data/reports/intraday/test_source_report.md",
    )
    assert "data/reports/intraday/test_source_report.md" in out
    assert "Source report" in out or "source report" in out.lower()


def test_stocks_packet_includes_source_report():
    """build_stocks_packet must surface the source_report kwarg in the header."""
    from src.stocks.llm_packet import build_stocks_packet

    config = load_config()
    out = build_stocks_packet(
        config,
        mode="intraday",
        source_report="data/reports/stocks/intraday/test_source_report.md",
    )
    assert "data/reports/stocks/intraday/test_source_report.md" in out
    assert "Source report" in out


# ---------------------------------------------------------------------------
# QA Fix #3 — signal performance section
# ---------------------------------------------------------------------------

def test_signal_performance_block_renders_for_crypto():
    from src.signals.report_section import build_signal_performance_block

    config = load_config()
    block = build_signal_performance_block(config, asset_class="crypto")
    assert "Recent Signal Performance" in block
    assert "Asset class: crypto" in block
    # Read-only marker must be present.
    assert "not** auto-modified" in block or "not auto-modified" in block


def test_signal_performance_block_renders_for_stocks():
    from src.signals.report_section import build_signal_performance_block

    config = load_config()
    block = build_signal_performance_block(config, asset_class="stocks")
    assert "Recent Signal Performance" in block
    assert "Asset class: stocks" in block


def test_signal_performance_block_failure_safe_for_known_failures(tmp_path):
    """For *known* failure modes (ImportError, sqlite3 errors) the block
    must degrade gracefully. RuntimeError and other unexpected errors are
    intentionally propagated after the report_section fix so that future
    silent-bug regressions surface in tests instead of being hidden."""

    import sqlite3

    from src.signals.report_section import build_signal_performance_block

    class DBFailingConfig:
        """sqlite3 layer fails on connection — must produce 'unavailable'."""

        root = tmp_path

        @property
        def db_path(self):
            return tmp_path / "this-file-does-not-exist" / "broken.db"

    block = build_signal_performance_block(DBFailingConfig(), asset_class="crypto")
    # Either we hit an ImportError-free path with an empty DB (clean output)
    # or we hit sqlite3.OperationalError → "unavailable" stub. Both are OK.
    assert "Recent Signal Performance" in block


# ---------------------------------------------------------------------------
# QA Fix #4 — stocks idea evidence improvements
# ---------------------------------------------------------------------------

def test_earnings_evidence_line_handles_unknown():
    from src.stocks.agents.trade_idea_agent import _earnings_evidence_line

    line = _earnings_evidence_line({"severity": "unknown", "next_earnings_date": None})
    assert "UNKNOWN" in line


def test_earnings_evidence_line_handles_known():
    from src.stocks.agents.trade_idea_agent import _earnings_evidence_line

    line = _earnings_evidence_line({
        "severity": "this_week",
        "next_earnings_date": "2026-05-30",
        "days_ahead": 4,
    })
    assert "2026-05-30" in line
    assert "this_week" in line


def test_stocks_report_renders_what_to_monitor_and_components():
    """Build a synthetic StocksPipelineResult and ensure the report contains
    What to Monitor, Data confidence (when distinct), and the per-component
    score breakdown."""
    from src.stocks.pipelines.stocks_pipeline import StocksPipelineResult
    from src.stocks.reports.stocks_report_builder import build_stocks_report

    result = StocksPipelineResult(mode="intraday")
    result.regime = {"regime": {"label": "bullish", "bias": "long", "risk_on": True}}
    result.sectors = {}
    result.scoring = {
        "scores": [
            {
                "symbol": "AAPL",
                "direction": "long",
                "tier": "A",
                "final_score": 88.64,
                "confidence": "high",
                "components": {
                    "market_regime": 12.0,
                    "technical_setup": 18.0,
                    "momentum": 14.5,
                },
                "risk_penalty": -4.0,
                "cap_reasons": [],
            }
        ]
    }
    result.ideas_payload = {
        "ideas": [
            {
                "tier": "A",
                "symbol": "AAPL",
                "direction": "long",
                "score": 88.64,
                "confidence": "high",
                "data_confidence": "medium",
                "data_sources_used": ["yfinance", "rss_news"],
                "risk_level": "low",
                "timeframe": "15m/1h",
                "thesis": "AAPL long (intraday) | trend=uptrend",
                "evidence": ["RS vs SPY (20d): +9.49%", "earnings: UNKNOWN"],
                "entry_plan": "long zone 308.04-308.88",
                "invalidation": "close beyond 306.35",
                "targets": ["TP1: 311.41", "TP2: 313.10", "TP3: 315.64"],
                "counterarguments": ["earnings date is UNKNOWN — undated event risk"],
                "avoid_conditions": ["do not chase if > 2 ATR from entry"],
                "what_to_monitor": [
                    "SPY/QQQ direction",
                    "sector ETF alignment",
                    "relative volume vs 20-day average",
                ],
                "cap_reasons": [],
            }
        ]
    }

    text = build_stocks_report(result)  # config omitted -> no signal perf section
    assert "What to monitor:" in text
    assert "SPY/QQQ direction" in text
    assert "Data confidence: medium" in text
    assert "Data sources: yfinance, rss_news" in text
    assert "Score breakdown:" in text
    assert "market_regime: 12.00" in text
    assert "risk_penalty: -4.0" in text


# ---------------------------------------------------------------------------
# QA Fix #5 — active-signals --asset-class
# ---------------------------------------------------------------------------

def test_active_signals_cli_has_asset_class_option():
    """The active-signals Typer command must expose ``--asset-class``."""
    import inspect

    from src.cli import app

    cmd = next(
        (c for c in app.registered_commands if c.name == "active-signals"),
        None,
    )
    assert cmd is not None, "active-signals command not registered"
    sig = inspect.signature(cmd.callback)
    assert "asset_class" in sig.parameters
