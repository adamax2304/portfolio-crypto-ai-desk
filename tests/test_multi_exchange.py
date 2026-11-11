from __future__ import annotations

from src.agents.exchange_fusion_agent import ExchangeFusionAgent
from src.config import load_config
from src.data_collectors.multi_exchange_universe_collector import MultiExchangeUniverseCollector
from src.storage.file_store import FileStore
from src.storage.sqlite import SQLiteStore


def _agent_kit():
    config = load_config()
    return config, FileStore(config), SQLiteStore(config.db_path)


def test_config_loads_exchanges_block() -> None:
    config = load_config()
    assert "binance" in config.exchanges
    assert config.exchange_role("binance") == "anchor"
    assert config.exchange_role("mexc") == "discovery"
    assert "mexc" in config.high_risk_exchanges


def test_exchange_alias_returns_native_symbol() -> None:
    config = load_config()
    assert config.exchange_alias("bybit", "PEPE/USDT") == "1000PEPE/USDT"
    assert config.exchange_alias("mexc", "PEPE/USDT") == "PEPE/USDT"
    assert config.exchange_alias("binance", "SOL/USDT") == "SOL/USDT"


def test_enabled_exchanges_contains_three_venues() -> None:
    config = load_config()
    assert {"binance", "bybit", "mexc"}.issubset(set(config.enabled_exchanges))


def test_multi_exchange_universe_collector_initialises() -> None:
    config, store, _ = _agent_kit()
    collector = MultiExchangeUniverseCollector(config, store)
    assert "binance" in collector.enabled_exchanges


def test_exchange_fusion_marks_mexc_only_setups() -> None:
    config, store, db = _agent_kit()
    agent = ExchangeFusionAgent(config, store, db)
    fused = [
        {
            "symbol": "SOMECOIN/USDT",
            "per_exchange": {
                "mexc": {
                    "exchange": "mexc",
                    "opportunity_score": 70,
                    "change_24h": 12.0,
                    "volume_anomaly": 1.8,
                    "liquidity_score": 30,
                }
            },
            "exchanges": ["mexc"],
        }
    ]
    confirmations = agent.run(fused)
    item = confirmations["SOMECOIN/USDT"]
    assert item.high_risk_only is True
    assert "mexc_only" in item.risk_flags
    assert item.anchor_listed is False
    assert "speculative" in item.interpretation.lower()


def test_exchange_fusion_marks_anchor_plus_derivatives_as_strongest() -> None:
    config, store, db = _agent_kit()
    agent = ExchangeFusionAgent(config, store, db)
    fused = [
        {
            "symbol": "BTC/USDT",
            "per_exchange": {
                "binance": {
                    "exchange": "binance",
                    "opportunity_score": 70,
                    "change_24h": 1.5,
                    "volume_anomaly": 1.0,
                    "liquidity_score": 95,
                },
                "bybit": {
                    "exchange": "bybit",
                    "opportunity_score": 65,
                    "change_24h": 1.6,
                    "volume_anomaly": 1.1,
                    "liquidity_score": 80,
                },
            },
            "exchanges": ["binance", "bybit"],
        }
    ]
    confirmations = agent.run(fused)
    item = confirmations["BTC/USDT"]
    assert item.anchor_listed is True
    assert item.derivatives_listed is True
    assert item.high_risk_only is False
    assert item.suggested_exchange_focus == "binance"
    assert item.confirmation_score >= 70
