"""Tests for EarningsRiskAgent. No network — uses canned EarningsEvent inputs."""

from __future__ import annotations

from dataclasses import replace
from datetime import date, timedelta
from pathlib import Path

from src.config import load_config
from src.storage.file_store import FileStore
from src.storage.sqlite import SQLiteStore
from src.stocks import load_stocks_config
from src.stocks.agents import EarningsRiskAgent
from src.stocks.data_collectors import EarningsEvent


def _kit(tmp_path: Path):
    config = replace(load_config(), root=tmp_path)
    scfg = load_stocks_config()
    fs = FileStore(config)
    db = SQLiteStore(config.db_path)
    db.init_db()
    return config, scfg, fs, db


def _event(symbol: str, days_ahead: int, today: date) -> EarningsEvent:
    target = today + timedelta(days=days_ahead)
    return EarningsEvent(
        date=target.isoformat(),
        symbol=symbol,
        report_time="AMC",
        source="manual",
    )


def test_swing_blocks_within_two_days(tmp_path):
    config, scfg, fs, db = _kit(tmp_path)
    agent = EarningsRiskAgent(config, scfg, fs, db)
    today = date(2026, 5, 25)
    events = [
        _event("NVDA", 1, today),   # blocks (≤2)
        _event("AAPL", 5, today),   # this_week, doesn't hard-block but penalizes
        _event("MSFT", 30, today),  # safe
    ]
    payload = agent.run(events, symbols=["NVDA", "AAPL", "MSFT"], mode="swing", today=today)
    blocks = payload["blocks_swing"]
    assert "NVDA" in blocks
    assert "AAPL" not in blocks
    assert "MSFT" not in blocks


def test_intraday_warns_but_does_not_block(tmp_path):
    config, scfg, fs, db = _kit(tmp_path)
    agent = EarningsRiskAgent(config, scfg, fs, db)
    today = date(2026, 5, 25)
    events = [_event("NVDA", 0, today)]  # earnings today
    payload = agent.run(events, symbols=["NVDA"], mode="intraday", today=today)
    risk = payload["risks"][0]
    assert risk["severity"] == "active"
    assert risk["intraday_high_risk"] is True
    # The blocks_swing flag is informational ("swing would reject this"),
    # set regardless of current mode. Downstream agents apply it only when
    # they're actually running in swing mode.
    assert risk["blocks_swing"] is True
    # The intraday-warnings list should always include this symbol.
    assert "NVDA" in payload["intraday_warnings"]


def test_unknown_when_no_event(tmp_path):
    config, scfg, fs, db = _kit(tmp_path)
    agent = EarningsRiskAgent(config, scfg, fs, db)
    today = date(2026, 5, 25)
    payload = agent.run([], symbols=["NVDA"], mode="swing", today=today)
    risk = payload["risks"][0]
    assert risk["severity"] == "unknown"
    assert risk["next_earnings_date"] is None


def test_picks_nearest_future_event(tmp_path):
    config, scfg, fs, db = _kit(tmp_path)
    agent = EarningsRiskAgent(config, scfg, fs, db)
    today = date(2026, 5, 25)
    events = [
        _event("NVDA", 10, today),
        _event("NVDA", 3, today),   # nearer — should win
        _event("NVDA", 100, today),
    ]
    payload = agent.run(events, symbols=["NVDA"], mode="swing", today=today)
    risk = payload["risks"][0]
    expected = (today + timedelta(days=3)).isoformat()
    assert risk["next_earnings_date"] == expected
    assert risk["days_ahead"] == 3
