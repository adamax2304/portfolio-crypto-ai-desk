"""Stocks-specific data collectors. Built on yfinance for the MVP.

yfinance documented limits:
  - intraday 15m: 60 days max history per request
  - intraday 1h: 729 days (one-day safety margin under Yahoo's ~730d cap)
  - 1d: effectively unbounded
  - rate-limited and unofficial; throttle between calls (see throttle_seconds)
"""

from src.stocks.data_collectors.earnings_calendar_collector import (
    EarningsCalendarCollector,
    EarningsCollectionSummary,
    EarningsEvent,
)
from src.stocks.data_collectors.market_index_collector import MarketIndexCollector
from src.stocks.data_collectors.sector_etf_collector import SectorETFCollector
from src.stocks.data_collectors.stock_ohlcv_collector import (
    StockOHLCVCollector,
    StockOHLCVSummary,
)
from src.stocks.data_collectors.yf_client import OHLCVResult, fetch_calendar, fetch_ohlcv

__all__ = [
    "EarningsCalendarCollector",
    "EarningsCollectionSummary",
    "EarningsEvent",
    "MarketIndexCollector",
    "OHLCVResult",
    "SectorETFCollector",
    "StockOHLCVCollector",
    "StockOHLCVSummary",
    "fetch_calendar",
    "fetch_ohlcv",
]
