"""MarketIndexCollector — pulls SPY/QQQ/IWM/DIA (+ VIX) bars.

Used by StocksMarketRegimeAgent to classify the broad market regime.
Thin wrapper around StockOHLCVCollector with the index list hardcoded
from config/stocks/universe.yaml.
"""

from __future__ import annotations

from src.config import ProjectConfig
from src.stocks.configs.loader import StocksConfig
from src.stocks.data_collectors.stock_ohlcv_collector import (
    StockOHLCVCollector,
    StockOHLCVSummary,
)


class MarketIndexCollector:
    name = "market_index_collector"

    def __init__(self, project_config: ProjectConfig, stocks_config: StocksConfig):
        self.project_config = project_config
        self.stocks_config = stocks_config
        self._ohlcv = StockOHLCVCollector(project_config, stocks_config)

    def collect(
        self,
        *,
        intervals: list[str] | None = None,
        include_vix: bool = True,
    ) -> StockOHLCVSummary:
        symbols = list(self.stocks_config.indices)
        if include_vix and self.stocks_config.volatility_index:
            symbols.append(self.stocks_config.volatility_index)
        intervals = intervals or ["1d", "1h"]
        return self._ohlcv.collect(symbols, intervals)
