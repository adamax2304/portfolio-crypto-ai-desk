"""SectorETFCollector — pulls XLK/SMH/XLF/etc.

Used by SectorRotationAgent to score sector strength. Thin wrapper around
StockOHLCVCollector with the sector ETF list pulled from
config/stocks/universe.yaml's sector_etfs map.
"""

from __future__ import annotations

from src.config import ProjectConfig
from src.stocks.configs.loader import StocksConfig
from src.stocks.data_collectors.stock_ohlcv_collector import (
    StockOHLCVCollector,
    StockOHLCVSummary,
)


class SectorETFCollector:
    name = "sector_etf_collector"

    def __init__(self, project_config: ProjectConfig, stocks_config: StocksConfig):
        self.project_config = project_config
        self.stocks_config = stocks_config
        self._ohlcv = StockOHLCVCollector(project_config, stocks_config)

    def collect(
        self,
        *,
        intervals: list[str] | None = None,
    ) -> StockOHLCVSummary:
        symbols = sorted(set(self.stocks_config.sector_etfs.values()))
        intervals = intervals or ["1d"]
        return self._ohlcv.collect(symbols, intervals)
