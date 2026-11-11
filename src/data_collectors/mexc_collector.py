"""MEXC OHLCV collector — early momentum / discovery layer.

MEXC lists more small-cap / new pairs than Binance, which makes it a good
"early radar" venue. The trade-off is noise and liquidity: MEXC-only setups
are downgraded in scoring (see ScoringAgent + ExchangeFusionAgent).
"""

from __future__ import annotations

from src.config import ProjectConfig
from src.data_collectors.exchange_ohlcv_collector import (
    ExchangeCollectionSummary,
    ExchangeOHLCVCollector,
)
from src.storage.file_store import FileStore


class MEXCOHLCVCollector(ExchangeOHLCVCollector):
    def __init__(self, config: ProjectConfig, store: FileStore):
        super().__init__("mexc", config, store)


__all__ = ["MEXCOHLCVCollector", "ExchangeCollectionSummary"]
