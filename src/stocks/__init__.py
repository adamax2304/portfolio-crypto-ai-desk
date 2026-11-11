"""Stocks/indices analysis module.

This package mirrors the layout of the crypto-implicit src/ tree but with
stock-specific agents, collectors, scoring, and reports. It is intentionally
isolated — nothing here imports crypto agents or modifies crypto scoring,
and nothing in src/agents, src/data_collectors, or src/reports imports from
here. Shared infrastructure (storage, indicators, base_agent, signal
tracking core) is reused from the top-level src/ modules.

Status: Stages 1-4 (asset_class plumbing, configs, yfinance collectors,
agents). Stage 5 (reports + CLI + supervisor wiring) is not done yet.
"""

from src.stocks.configs.loader import StocksConfig, load_stocks_config

__all__ = ["StocksConfig", "load_stocks_config"]
