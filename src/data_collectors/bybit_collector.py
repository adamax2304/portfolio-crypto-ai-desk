"""Bybit OHLCV collector — thin wrapper around the generic ExchangeOHLCVCollector.

Bybit's ccxt id is ``bybit``. Spot markets cover the bulk of liquid USDT pairs
and double as derivatives-confirmation source via the dedicated
``MultiExchangeDerivativesCollector``.
"""

from __future__ import annotations

from src.config import ProjectConfig
from src.data_collectors.exchange_ohlcv_collector import (
    ExchangeCollectionSummary,
    ExchangeOHLCVCollector,
)
from src.storage.file_store import FileStore


class BybitOHLCVCollector(ExchangeOHLCVCollector):
    def __init__(self, config: ProjectConfig, store: FileStore):
        super().__init__("bybit", config, store)


__all__ = ["BybitOHLCVCollector", "ExchangeCollectionSummary"]
