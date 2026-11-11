"""Paginated deep-history OHLCV backfill (offline / backtest only).

Unlike the live ``ExchangeOHLCVCollector`` — which issues a single
``fetch_ohlcv(limit=N)`` and therefore only ever sees the most-recent ~9 days —
this backfiller pages backwards with ccxt's ``since`` cursor, looping until the
cursor reaches "now" (NOT breaking on a partial page, which is where a naive
pager stops early on venues that return <limit rows per call). Results are
merged into the SEPARATE deep-history store (``src.backtest.historical_store``);
the live rolling cache and the live collectors are never touched.

This exists purely to give the offline settings-replay months of real price
paths. It performs no trading and writes no signal/outcome/live table.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

import pandas as pd

from src.backtest import historical_store as hist
from src.config import ProjectConfig
from src.logger import get_logger

# Exchange fallback order mirrors tracker._load_ohlcv_for_signal so the deep
# loader can find whatever the backfiller stored.
DEFAULT_EXCHANGES = ("binance", "mexc", "bybit")
DEFAULT_TIMEFRAMES = ("5m", "15m", "1h")

_TF_MS = {
    "1m": 60_000, "3m": 180_000, "5m": 300_000, "15m": 900_000, "30m": 1_800_000,
    "1h": 3_600_000, "2h": 7_200_000, "4h": 14_400_000, "1d": 86_400_000,
}


@dataclass
class BackfillSummary:
    days: int
    exchanges: list[str]
    timeframes: list[str]
    fetched: dict[str, dict] = field(default_factory=dict)   # "SYM TF" -> merge summary
    unlisted: list[str] = field(default_factory=list)        # symbols on no exchange
    failed: dict[str, str] = field(default_factory=dict)     # "SYM TF" -> error

    def as_dict(self) -> dict:
        return {
            "days": self.days,
            "exchanges": self.exchanges,
            "timeframes": self.timeframes,
            "symbols_fetched": len({k.split(" ")[0] for k in self.fetched}),
            "series_fetched": len(self.fetched),
            "bars_added": sum(v.get("added", 0) for v in self.fetched.values()),
            "unlisted": self.unlisted,
            "failed": self.failed,
        }


class HistoricalOHLCVBackfiller:
    def __init__(
        self,
        config: ProjectConfig,
        exchanges: tuple[str, ...] = DEFAULT_EXCHANGES,
        max_requests_per_series: int = 400,
    ):
        self.config = config
        self.exchanges = tuple(e.lower() for e in exchanges)
        self.max_requests_per_series = max_requests_per_series
        self.logger = get_logger(self.__class__.__name__)
        self._ex_cache: dict[str, Any] = {}

    # ------------------------------------------------------------------ ccxt
    def _build_exchange(self, exchange: str) -> Any:
        if exchange in self._ex_cache:
            return self._ex_cache[exchange]
        import ccxt

        ccxt_id = self.config.exchange_ccxt_id(exchange)
        klass = getattr(ccxt, ccxt_id, None)
        if klass is None:
            raise RuntimeError(f"ccxt has no adapter for `{ccxt_id}`")
        ex = klass({"enableRateLimit": True, "options": {"defaultType": "spot"}})
        ex.load_markets()
        self._ex_cache[exchange] = ex
        return ex

    def _fetch_paged(self, ex: Any, native: str, timeframe: str, since_ms: int,
                     until_ms: int) -> list[list[float]]:
        """Page from since_ms forward until the newest bar reaches until_ms.

        Does NOT stop on a partial page — only when the response is empty or the
        cursor fails to advance (true end of stream) or the request cap is hit.
        """
        step = _TF_MS.get(timeframe, 900_000)
        out: list[list[float]] = []
        cur = since_ms
        last_seen: int | None = None
        reqs = 0
        while reqs < self.max_requests_per_series:
            rows = ex.fetch_ohlcv(native, timeframe=timeframe, since=cur, limit=1000)
            reqs += 1
            if not rows:
                break
            out.extend(rows)
            newest = int(rows[-1][0])
            if last_seen is not None and newest <= last_seen:
                break                                   # cursor not advancing → end
            last_seen = newest
            if newest >= until_ms:
                break
            cur = newest + step                          # next window starts after last bar
        return out

    # -------------------------------------------------------------- backfill
    def backfill(
        self,
        symbols: list[str],
        timeframes: tuple[str, ...] = DEFAULT_TIMEFRAMES,
        days: int = 60,
        now_ms: int | None = None,
    ) -> BackfillSummary:
        now_ms = now_ms if now_ms is not None else int(time.time() * 1000)
        since_ms = now_ms - days * 86_400_000
        summary = BackfillSummary(days=days, exchanges=list(self.exchanges),
                                  timeframes=list(timeframes))

        for symbol in symbols:
            venue = None
            native = None
            for exchange in self.exchanges:
                try:
                    ex = self._build_exchange(exchange)
                except Exception as exc:
                    self.logger.warning("init %s failed: %s", exchange, exc)
                    continue
                candidate = self.config.exchange_alias(exchange, symbol)
                if candidate in ex.markets:
                    venue, native = exchange, candidate
                    break
            if venue is None:
                summary.unlisted.append(symbol)
                continue

            ex = self._build_exchange(venue)
            for timeframe in timeframes:
                key = f"{symbol} {timeframe}"
                try:
                    rows = self._fetch_paged(ex, native, timeframe, since_ms, now_ms)
                    if not rows:
                        summary.failed[key] = "empty"
                        continue
                    frame = pd.DataFrame(rows, columns=["timestamp", "open", "high",
                                                        "low", "close", "volume"])
                    frame["timestamp"] = pd.to_datetime(frame["timestamp"], unit="ms", utc=True)
                    merged = hist.save_merge(self.config, venue, symbol, timeframe, frame)
                    summary.fetched[key] = {**merged, "venue": venue}
                    self.logger.info("backfilled %s on %s: +%d bars (%d total)",
                                     key, venue, merged["added"], merged["rows_after"])
                except Exception as exc:
                    summary.failed[key] = str(exc)
                    self.logger.warning("backfill %s on %s failed: %s", key, venue, exc)
        return summary


def crypto_symbols_from_signals(db_path: str) -> list[str]:
    """Distinct crypto symbols that actually appear in proposed_signals (read-only)."""
    import sqlite3

    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        rows = conn.execute(
            "SELECT DISTINCT symbol FROM proposed_signals "
            "WHERE asset_class='crypto' AND symbol IS NOT NULL ORDER BY symbol"
        ).fetchall()
    finally:
        conn.close()
    return [r[0] for r in rows]
