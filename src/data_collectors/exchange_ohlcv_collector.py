"""Generic ccxt-backed OHLCV collector reused by Bybit / MEXC / Binance.

The original ``BinanceOHLCVCollector`` predates the multi-exchange upgrade and
is kept for backward compatibility. New code should prefer this class so the
same fetch/normalize/cache pipeline runs for every venue.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pandas as pd

from src.config import ProjectConfig
from src.logger import get_logger
from src.storage.file_store import FileStore


@dataclass
class ExchangeCollectionSummary:
    exchange: str
    fetched: list[str] = field(default_factory=list)
    failed: dict[str, str] = field(default_factory=dict)
    skipped: list[str] = field(default_factory=list)


class ExchangeOHLCVCollector:
    """Fetch OHLCV from any ccxt-supported exchange and cache as CSV.

    Per-exchange behaviour (rate-limit, defaultType, symbol aliases) is read
    from ``config/exchanges.yaml`` so adding a new venue is mostly a config
    change.
    """

    def __init__(self, exchange: str, config: ProjectConfig, store: FileStore):
        self.exchange = exchange.lower()
        self.config = config
        self.store = store
        self.logger = get_logger(f"{self.__class__.__name__}[{self.exchange}]")

    @property
    def ccxt_id(self) -> str:
        return self.config.exchange_ccxt_id(self.exchange)

    def _build_exchange(self) -> Any:
        try:
            import ccxt
        except ImportError as exc:
            raise RuntimeError(
                "ccxt is not installed. Run `pip install -r requirements.txt` first."
            ) from exc

        exchange_class = getattr(ccxt, self.ccxt_id, None)
        if exchange_class is None:
            raise RuntimeError(
                f"ccxt does not expose an adapter for `{self.ccxt_id}`. "
                "Update config/exchanges.yaml or upgrade ccxt."
            )
        return exchange_class({"enableRateLimit": True, "options": {"defaultType": "spot"}})

    @staticmethod
    def _close_exchange(exchange: Any) -> None:
        try:
            close = getattr(exchange, "close", None)
            if callable(close):
                close()
        except Exception:
            pass

    @staticmethod
    def _frame_from_rows(rows: list[list[float]]) -> pd.DataFrame:
        frame = pd.DataFrame(
            rows, columns=["timestamp", "open", "high", "low", "close", "volume"]
        )
        frame["timestamp"] = pd.to_datetime(frame["timestamp"], unit="ms", utc=True)
        for column in ["open", "high", "low", "close", "volume"]:
            frame[column] = pd.to_numeric(frame[column], errors="coerce")
        return frame.dropna().sort_values("timestamp").reset_index(drop=True)

    def _resolve_symbol(self, symbol: str) -> str:
        return self.config.exchange_alias(self.exchange, symbol)

    def fetch(
        self,
        symbols: list[str] | None = None,
        timeframes: list[str] | None = None,
    ) -> ExchangeCollectionSummary:
        if not self.config.exchange_enabled(self.exchange):
            self.logger.info("Exchange %s is disabled in config; skipping fetch", self.exchange)
            return ExchangeCollectionSummary(exchange=self.exchange)

        selected_symbols = symbols or self.config.symbols
        selected_timeframes = timeframes or self.config.timeframes
        summary = ExchangeCollectionSummary(exchange=self.exchange)

        exchange = None
        try:
            exchange = self._build_exchange()
            exchange.load_markets()
        except Exception as exc:
            if exchange is not None:
                self._close_exchange(exchange)
            self.logger.warning("Could not initialise %s: %s", self.ccxt_id, exc)
            for symbol in selected_symbols:
                summary.failed[symbol] = f"exchange init failed: {exc}"
            return summary

        for symbol in selected_symbols:
            native = self._resolve_symbol(symbol)
            if native not in exchange.markets:
                summary.failed[symbol] = (
                    f"symbol not listed on {self.ccxt_id} spot market"
                )
                self.logger.info("%s skipped on %s: not listed", symbol, self.ccxt_id)
                continue

            for timeframe in selected_timeframes:
                limit = self.config.candle_limit(timeframe)
                key = f"{symbol} {timeframe}"
                try:
                    rows = exchange.fetch_ohlcv(native, timeframe=timeframe, limit=limit)
                    if not rows:
                        summary.failed[key] = "empty response"
                        continue
                    frame = self._frame_from_rows(rows)
                    self.store.save_ohlcv(self.exchange, symbol, timeframe, frame)
                    summary.fetched.append(key)
                    self.logger.info("Fetched %s %s candles for %s", self.exchange, timeframe, symbol)
                except Exception as exc:
                    summary.failed[key] = str(exc)
                    self.logger.warning("Failed %s on %s: %s", key, self.exchange, exc)

        self._close_exchange(exchange)
        return summary
