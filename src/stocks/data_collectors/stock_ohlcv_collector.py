"""StockOHLCVCollector — fetch and cache stock OHLCV bars to CSV.

Cached files land under data/raw/stocks/{interval}/{SYMBOL}.csv, parallel
to data/raw/ohlcv for crypto. Each row preserves the source timestamp;
callers downstream are responsible for re-tz-ing if needed.
"""

from __future__ import annotations

import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd

from src.config import ProjectConfig
from src.logger import get_logger
from src.stocks.configs.loader import StocksConfig
from src.stocks.data_collectors.yf_client import OHLCVResult, fetch_ohlcv, fetch_ohlcv_batch

_LOG = get_logger("stocks.ohlcv_collector")


@dataclass
class StockOHLCVSummary:
    fetched: dict[str, OHLCVResult] = field(default_factory=dict)
    failed: dict[str, str] = field(default_factory=dict)
    cache_dir: Path | None = None

    @property
    def ok(self) -> int:
        return len(self.fetched)

    @property
    def fail(self) -> int:
        return len(self.failed)


class StockOHLCVCollector:
    """Pulls OHLCV through the configured stocks provider chain and caches its bars."""

    name = "stock_ohlcv_collector"

    def __init__(self, project_config: ProjectConfig, stocks_config: StocksConfig):
        self.project_config = project_config
        self.stocks_config = stocks_config

    def cache_root(self, interval: str) -> Path:
        # Mirror crypto layout: data/raw/{kind}/{tf}/{SYMBOL}.csv
        root = self.project_config.raw_dir / "stocks" / interval
        root.mkdir(parents=True, exist_ok=True)
        return root

    def cache_path(self, symbol: str, interval: str) -> Path:
        return self.cache_root(interval) / f"{symbol.upper()}.csv"

    def load_cached(self, symbol: str, interval: str) -> pd.DataFrame | None:
        path = self.cache_path(symbol, interval)
        if not path.exists():
            return None
        try:
            frame = pd.read_csv(path, index_col=0, parse_dates=True)
            if frame.empty:
                return None
            return frame
        except Exception as exc:  # noqa: BLE001
            _LOG.warning("failed to read cache %s: %s", path, exc)
            return None

    def collect(
        self,
        symbols: list[str],
        intervals: list[str],
        *,
        period: str | None = None,
        throttle_seconds: float = 0.5,
        max_workers: int = 1,
    ) -> StockOHLCVSummary:
        """Fetch OHLCV for each symbol × interval and write CSVs to cache.

        The normal archival path remains sequential and rate-limited.  The
        intraday monitor may opt into a small bounded pool so a 100-symbol
        scan does not turn its advertised fast cadence into a fifteen-minute
        wait.  Every request and cache file stays independent, so one failed
        provider response cannot poison another symbol.
        """

        summary = StockOHLCVSummary()
        tasks = [(symbol, interval) for symbol in symbols for interval in intervals]

        def _fetch_one(symbol: str, interval: str) -> tuple[str, OHLCVResult | None, str | None]:
            key = f"{symbol}@{interval}"
            result = fetch_ohlcv(symbol, interval, period=period)
            if result is None:
                return key, None, "configured provider chain returned no data"
            target = self.cache_path(symbol, interval)
            try:
                result.dataframe.to_csv(target, index=True)
            except Exception as exc:  # noqa: BLE001
                return key, None, f"cache write failed: {exc}"
            return key, result, None

        workers = max(1, int(max_workers))
        if workers == 1:
            for symbol, interval in tasks:
                key, result, error = _fetch_one(symbol, interval)
                if error:
                    summary.failed[key] = error
                elif result is not None:
                    summary.fetched[key] = result
                if throttle_seconds:
                    time.sleep(throttle_seconds)
        else:
            # Keep this intentionally small: yfinance remains a free fallback
            # and should not be hammered just to make the monitor look fast.
            with ThreadPoolExecutor(max_workers=workers, thread_name_prefix="stocks-ohlcv") as pool:
                futures = [pool.submit(_fetch_one, symbol, interval) for symbol, interval in tasks]
                for future in as_completed(futures):
                    key, result, error = future.result()
                    if error:
                        summary.failed[key] = error
                    elif result is not None:
                        summary.fetched[key] = result
        summary.cache_dir = self.project_config.raw_dir / "stocks"
        return summary

    def collect_default_universe(
        self,
        *,
        mode: str = "intraday",
        period: str | None = None,
    ) -> StockOHLCVSummary:
        """Convenience: collect the configured default universe for a mode."""

        symbols = list(self.stocks_config.default_symbols)
        intervals = self.stocks_config.timeframes_for(mode)
        return self.collect(symbols, intervals, period=period)

    def collect_fast_batch(
        self,
        symbols: list[str],
        interval: str,
        *,
        period: str = "5d",
    ) -> StockOHLCVSummary:
        """Use the configured provider's bounded batch API when available."""
        summary = StockOHLCVSummary()
        results = fetch_ohlcv_batch(symbols, interval, period=period)
        for symbol, result in results.items():
            key = f"{symbol}@{interval}"
            try:
                result.dataframe.to_csv(self.cache_path(symbol, interval), index=True)
                summary.fetched[key] = result
            except Exception as exc:  # noqa: BLE001
                summary.failed[key] = f"cache write failed: {exc}"
        for symbol in symbols:
            key = f"{str(symbol).upper()}@{interval}"
            if key not in summary.fetched and key not in summary.failed:
                summary.failed[key] = "batch provider returned no data"
        summary.cache_dir = self.project_config.raw_dir / "stocks"
        return summary
