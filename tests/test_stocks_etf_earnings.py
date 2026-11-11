"""PART 18 — ETFs must not trigger "earnings UNKNOWN" false-positive.

Pre-fix: every ETF (SPY/QQQ/IWM/DIA/SMH/XLK/etc.) was tagged
``severity='unknown'`` because yfinance's ``Ticker.calendar`` returns
nothing for index/sector ETFs. The trade-idea agent then surfaced
"earnings: UNKNOWN — calendar lookup missing" as a real risk flag,
weighing every ETF idea down with an undated-event-risk note.

PART 18 — :class:`StocksConfig.is_etf` recognises configured indices +
sector ETFs and the earnings-risk agent emits
``severity='not_applicable'`` for them. The trade-idea agent recognises
that and surfaces "earnings: N/A (ETF — does not report earnings)".
"""
from __future__ import annotations

from datetime import date

import pytest

from src.config import load_config
from src.stocks import load_stocks_config
from src.stocks.agents import EarningsRiskAgent
from src.stocks.data_collectors import EarningsEvent
from src.stocks.data_collectors.earnings_calendar_collector import EarningsCalendarCollector
from src.storage.file_store import FileStore
from src.storage.sqlite import SQLiteStore


@pytest.fixture(scope="module")
def cfg():
    return load_config()


@pytest.fixture(scope="module")
def scfg():
    return load_stocks_config()


# ---------------------------------------------------------------------------
# Config-level recognition
# ---------------------------------------------------------------------------


def test_indices_are_etfs(scfg):
    """SPY / QQQ / IWM / DIA are configured indices → ETFs."""
    for sym in ("SPY", "QQQ", "IWM", "DIA"):
        assert scfg.is_etf(sym), f"{sym} should be recognised as ETF"


def test_sector_etfs_are_etfs(scfg):
    """SMH / XLK / XLF / XLE / XLY / XLV are sector ETFs."""
    for sym in ("SMH", "XLK", "XLF", "XLE", "XLY", "XLV"):
        assert scfg.is_etf(sym), f"{sym} should be recognised as ETF"


def test_single_name_stocks_are_not_etfs(scfg):
    """AAPL / MSFT / AVGO / SMCI / NVDA / AMD must keep normal earnings logic."""
    for sym in ("AAPL", "MSFT", "AVGO", "SMCI", "NVDA", "AMD", "LLY"):
        assert not scfg.is_etf(sym), f"{sym} must NOT be classified as ETF"


def test_is_etf_is_case_insensitive(scfg):
    assert scfg.is_etf("spy") is True
    assert scfg.is_etf("SmH") is True
    assert scfg.is_etf("aapl") is False


def test_calendar_collector_does_not_call_yfinance_for_etfs(cfg, scfg, monkeypatch):
    called: list[str] = []

    def _calendar(symbol: str):
        called.append(symbol)
        return None

    monkeypatch.setattr(
        "src.stocks.data_collectors.earnings_calendar_collector.fetch_calendar",
        _calendar,
    )
    collector = EarningsCalendarCollector(cfg, scfg)
    events, failed = collector.fetch_yfinance(["SPY", "XLK", "AAPL"])

    assert events == []
    assert called == ["AAPL"]
    assert failed == ["AAPL"]


def test_calendar_collector_parallel_fast_path_keeps_complete_deterministic_results(
    cfg, scfg, monkeypatch
):
    """The bounded fast scan may parallelize requests without losing symbols."""
    payloads = {
        "AAPL": {"Earnings Date": ["2026-09-10"]},
        "MSFT": {"Earnings Date": ["2026-09-12"]},
    }
    monkeypatch.setattr(
        "src.stocks.data_collectors.earnings_calendar_collector.fetch_calendar",
        lambda symbol: payloads.get(symbol),
    )

    collector = EarningsCalendarCollector(cfg, scfg)
    events, failed = collector.fetch_yfinance(["MSFT", "SPY", "AAPL"], max_workers=2)

    assert [event.symbol for event in events] == ["AAPL", "MSFT"]
    assert failed == []


# ---------------------------------------------------------------------------
# EarningsRiskAgent path
# ---------------------------------------------------------------------------


@pytest.fixture
def earnings_agent(cfg, scfg, tmp_path):
    db = SQLiteStore(tmp_path / "test.sqlite")
    db.init_db()
    fs = FileStore(cfg)
    return EarningsRiskAgent(cfg, scfg, fs, db)


def _by_symbol(payload):
    return {r["symbol"]: r for r in payload["risks"]}


def test_etfs_get_not_applicable_severity(earnings_agent):
    """SPY / QQQ / SMH / XLK pulled with no calendar events → severity not_applicable."""
    payload = earnings_agent.run(
        events=[],
        symbols=["SPY", "QQQ", "SMH", "XLK"],
        mode="intraday",
        today=date(2026, 6, 3),
    )
    risks = _by_symbol(payload)
    for sym in ("SPY", "QQQ", "SMH", "XLK"):
        assert risks[sym]["severity"] == "not_applicable", risks[sym]
        assert risks[sym]["note"].lower().startswith("etf")
        assert risks[sym]["blocks_swing"] is False
        assert risks[sym]["intraday_high_risk"] is False


def test_single_name_with_no_calendar_still_unknown(earnings_agent):
    """AAPL with no events keeps severity=unknown (existing behaviour)."""
    payload = earnings_agent.run(
        events=[],
        symbols=["AAPL"],
        mode="intraday",
        today=date(2026, 6, 3),
    )
    risks = _by_symbol(payload)
    assert risks["AAPL"]["severity"] == "unknown"


def test_etf_with_misclassified_calendar_row_still_not_applicable(earnings_agent):
    """Defence-in-depth: even if a bad event row slipped in for SPY, the
    ETF gate must fire FIRST and still return not_applicable."""
    # Simulate a buggy upstream giving SPY an "earnings" row.
    bogus = EarningsEvent(
        date="2026-08-01", symbol="SPY", report_time="AMC", source="manual",
    )
    payload = earnings_agent.run(
        events=[bogus],
        symbols=["SPY"],
        mode="swing",
        today=date(2026, 6, 3),
    )
    risks = _by_symbol(payload)
    assert risks["SPY"]["severity"] == "not_applicable"
    assert risks["SPY"]["blocks_swing"] is False


# ---------------------------------------------------------------------------
# Evidence-line / counter-thesis surface
# ---------------------------------------------------------------------------


def test_earnings_evidence_line_for_etf():
    from src.stocks.agents.trade_idea_agent import _earnings_evidence_line
    line = _earnings_evidence_line(
        {"symbol": "SPY", "severity": "not_applicable",
         "next_earnings_date": None, "days_ahead": None}
    )
    assert "N/A" in line
    assert "ETF" in line
    assert "UNKNOWN" not in line


def test_earnings_evidence_line_still_unknown_for_single_name():
    """Regression — non-ETF with severity=unknown still says UNKNOWN."""
    from src.stocks.agents.trade_idea_agent import _earnings_evidence_line
    line = _earnings_evidence_line(
        {"symbol": "AAPL", "severity": "unknown",
         "next_earnings_date": None, "days_ahead": None}
    )
    assert "UNKNOWN" in line
