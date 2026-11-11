from __future__ import annotations

import numpy as np
import pandas as pd

from src.agents import market_regime_agent as regime_module
from src.agents.market_regime_agent import MarketRegimeAgent
from src.config import load_config
from src.storage.file_store import FileStore
from src.storage.sqlite import SQLiteStore


def _frame() -> pd.DataFrame:
    # A large, recent directional move makes the 24h return exceed the regime
    # threshold while leaving enough history for every indicator calculation.
    closes = np.concatenate([np.full(72, 100.0), np.linspace(100.0, 110.0, 8)])
    return pd.DataFrame({
        "timestamp": pd.date_range("2026-01-01", periods=len(closes), freq="4h", tz="UTC"),
        "open": closes,
        "high": closes * 1.01,
        "low": closes * 0.99,
        "close": closes,
        "volume": np.full(len(closes), 1_000_000.0),
    })


def _agent(tmp_path) -> MarketRegimeAgent:
    cfg = load_config()
    db = SQLiteStore(tmp_path / "regime.sqlite")
    db.init_db()
    agent = MarketRegimeAgent(cfg, FileStore(cfg), db)
    agent.save_output = lambda _payload: None
    return agent


def test_broad_volatile_uptrend_is_not_labelled_danger(tmp_path, monkeypatch):
    agent = _agent(tmp_path)
    monkeypatch.setattr(regime_module, "atr_percentile", lambda _frame: 100.0)
    monkeypatch.setattr(agent, "_symbol_trend", lambda _frame: "uptrend")
    market_data = {symbol: {"4h": _frame()} for symbol in (
        "BTC/USDT", "ETH/USDT", "SOL/USDT", "XRP/USDT", "LINK/USDT", "AVAX/USDT",
    )}

    regime = agent.run(market_data)

    assert regime.label == "high-volatility trend"
    assert regime.risk_mode == "cautious-risk-on"
    assert regime.volatility["state"] == "elevated_trending"


def test_high_volatility_without_major_confirmation_stays_danger(tmp_path, monkeypatch):
    agent = _agent(tmp_path)
    monkeypatch.setattr(regime_module, "atr_percentile", lambda _frame: 100.0)
    btc, eth = _frame(), _frame()
    monkeypatch.setattr(
        agent,
        "_symbol_trend",
        lambda frame: "uptrend" if frame is btc else "downtrend" if frame is eth else "uptrend",
    )
    market_data = {
        "BTC/USDT": {"4h": btc},
        "ETH/USDT": {"4h": eth},
        "SOL/USDT": {"4h": _frame()},
        "XRP/USDT": {"4h": _frame()},
    }

    regime = agent.run(market_data)

    assert regime.label == "high-volatility danger"
    assert regime.risk_mode == "danger"


def test_tiny_breadth_sample_cannot_unlock_volatile_trend(tmp_path, monkeypatch):
    agent = _agent(tmp_path)
    monkeypatch.setattr(regime_module, "atr_percentile", lambda _frame: 100.0)
    monkeypatch.setattr(agent, "_symbol_trend", lambda _frame: "uptrend")
    market_data = {symbol: {"4h": _frame()} for symbol in (
        "BTC/USDT", "ETH/USDT", "SOL/USDT", "XRP/USDT",
    )}

    regime = agent.run(market_data)

    assert regime.label == "high-volatility danger"
    assert regime.confidence <= 70.0
    assert any("breadth sample is too small" in item for item in regime.warnings)
