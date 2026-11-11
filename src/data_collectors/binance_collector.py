from __future__ import annotations

from dataclasses import dataclass, field
from threading import Lock
from typing import Any

import pandas as pd

from src.config import ProjectConfig
from src.logger import get_logger
from src.storage.file_store import FileStore


_MARKETS_CACHE: dict[str, dict[str, Any]] = {}
_MARKETS_LOCK = Lock()


@dataclass
class CollectionSummary:
    exchange: str
    fetched: list[str] = field(default_factory=list)
    failed: dict[str, str] = field(default_factory=dict)
    skipped: list[str] = field(default_factory=list)


class BinanceOHLCVCollector:
    def __init__(self, config: ProjectConfig, store: FileStore):
        self.config = config
        self.store = store
        self.logger = get_logger(self.__class__.__name__)

    def _build_exchange(self) -> Any:
        try:
            import ccxt
        except ImportError as exc:
            raise RuntimeError(
                "ccxt is not installed. Run `pip install -r requirements.txt` first."
            ) from exc

        exchange_class = getattr(ccxt, self.config.exchange_id)
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

    def fetch(
        self,
        symbols: list[str] | None = None,
        timeframes: list[str] | None = None,
    ) -> CollectionSummary:
        exchange_id = self.config.exchange_id
        exchange = self._build_exchange()
        try:
            with _MARKETS_LOCK:
                cached = _MARKETS_CACHE.get(exchange_id)
                if cached is None:
                    cached = exchange.load_markets()
                    _MARKETS_CACHE[exchange_id] = cached
                else:
                    set_markets = getattr(exchange, "set_markets", None)
                    if callable(set_markets):
                        set_markets(cached)
                    else:
                        exchange.load_markets()
        except Exception:
            self._close_exchange(exchange)
            raise

        selected_symbols = symbols or self.config.symbols
        selected_timeframes = timeframes or self.config.timeframes
        summary = CollectionSummary(exchange=exchange_id)

        for symbol in selected_symbols:
            if symbol not in exchange.markets:
                msg = "symbol not listed on exchange spot market"
                self.logger.warning("%s skipped: %s", symbol, msg)
                summary.failed[symbol] = msg
                continue

            for timeframe in selected_timeframes:
                limit = self.config.candle_limit(timeframe)
                key = f"{symbol} {timeframe}"
                try:
                    rows = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
                    if not rows:
                        summary.failed[key] = "empty response"
                        continue
                    frame = self._frame_from_rows(rows)
                    self.store.save_ohlcv(exchange_id, symbol, timeframe, frame)
                    summary.fetched.append(key)
                    self.logger.info("Fetched %s candles for %s", timeframe, symbol)
                except Exception as exc:
                    summary.failed[key] = str(exc)
                    self.logger.warning("Failed %s: %s", key, exc)

        self._close_exchange(exchange)
        return summary
