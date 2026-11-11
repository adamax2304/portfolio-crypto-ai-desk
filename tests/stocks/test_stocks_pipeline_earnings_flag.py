"""Guard tests for the stocks earnings refresh contract.

The full/pre-open pipeline must refresh yfinance earnings, while a fast RTH
pass must use the already-persisted calendar so a slow quoteSummary endpoint
does not make a valid intraday entry stale.
"""
from __future__ import annotations

import re
from pathlib import Path
from types import SimpleNamespace

from src.stocks.pipelines.stocks_pipeline import StocksPipeline


PIPELINE_FILE = (
    Path(__file__).resolve().parents[2]
    / "src" / "stocks" / "pipelines" / "stocks_pipeline.py"
)


def _run_report_body() -> str:
    src = PIPELINE_FILE.read_text(encoding="utf-8")
    match = re.search(
        r"def run_report\(\s*self.*?(?=\n    def\s)",
        src,
        flags=re.DOTALL,
    )
    assert match is not None, "could not locate run_report() in pipeline file"
    return match.group(0)


def test_pipeline_refreshes_or_uses_persisted_earnings_explicitly():
    """Normal refresh remains network-backed; fast RTH has a cache branch."""
    body = _run_report_body()
    assert "if refresh_earnings:" in body
    assert "self._cached_earnings_events(symbols)" in body
    collect_calls = re.findall(
        r"ec\.collect\([^)]*\)",
        body,
        flags=re.DOTALL,
    )
    assert collect_calls, "no earnings refresh call found in run_report"
    assert any("include_yfinance=True" in call for call in collect_calls)


def test_fast_earnings_cache_does_not_disable_scheduled_refresh():
    """Cached fast reads may not silently turn off the normal yfinance path."""
    body = _run_report_body()
    block = re.search(
        r"if refresh_earnings:.*?result\.earnings = earnings_agent\.run",
        body,
        flags=re.DOTALL,
    )
    assert block is not None, "earnings-seeding block missing"
    assert "include_yfinance=True" in block.group(0)
    assert "events=self._cached_earnings_events(symbols)" in block.group(0)


def test_cached_earnings_only_admits_matching_stock_rows():
    pipeline = object.__new__(StocksPipeline)
    pipeline.db = SimpleNamespace(load_events=lambda limit: [
        {
            "asset_class": "stocks", "event_type": "earnings", "ticker": "NVDA",
            "event_date": "2026-09-02",
            "raw_json": ('{"event_date":"2026-09-02","report_time":"AMC",'
                         '"source":"yfinance"}'),
        },
        {
            "asset_class": "crypto", "event_type": "earnings", "ticker": "NVDA",
            "event_date": "2026-09-03", "raw_json": "{}",
        },
        {
            "asset_class": "stocks", "event_type": "earnings", "ticker": "MSFT",
            "event_date": "2026-09-04", "raw_json": "{}",
        },
    ])

    events = pipeline._cached_earnings_events(["NVDA"])

    assert [(event.symbol, event.date, event.report_time) for event in events] == [
        ("NVDA", "2026-09-02", "AMC")
    ]
