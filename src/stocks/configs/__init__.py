"""Stocks-specific config loaders. Read config/stocks/*.yaml."""

from src.stocks.configs.loader import StocksConfig, load_stocks_config

__all__ = ["StocksConfig", "load_stocks_config"]
