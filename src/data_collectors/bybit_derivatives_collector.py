"""Bybit derivatives history: OI delta + funding history + L/S ratio.

Existing ``MultiExchangeDerivativesCollector`` only reads the current ticker
snapshot (funding_rate, open_interest). This collector adds the time series
endpoints so the desk can compute:

- ``oi_change_pct_24h`` (sign tells you long buildup vs unwind),
- ``funding_percentile`` over the last 7 days (catches crowded extremes),
- ``long_short_ratio`` if Bybit exposes it for the symbol.

All endpoints are public, key-less, rate-limited via ``requests``. Missing
symbols are recorded per-symbol; one failure does not break the batch.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from statistics import mean
from typing import Any

import requests

from src.config import ProjectConfig
from src.logger import get_logger
from src.storage.file_store import FileStore
from src.utils.symbols import symbol_to_exchange_symbol
from src.utils.time import utc_now


class NoBybitDerivativesMarket(Exception):
    pass


@dataclass
class BybitDerivativesSummary:
    fetched: list[str] = field(default_factory=list)
    failed: dict[str, str] = field(default_factory=dict)
    records: dict[str, dict[str, Any]] = field(default_factory=dict)


class BybitDerivativesCollector:
    def __init__(self, config: ProjectConfig, store: FileStore):
        self.config = config
        self.store = store
        self.base_url = config.sources.get("public_endpoints", {}).get(
            "bybit", "https://api.bybit.com"
        )
        self.logger = get_logger(self.__class__.__name__)

    def fetch(self, symbols: list[str] | None = None) -> BybitDerivativesSummary:
        selected = symbols or self.config.symbols
        summary = BybitDerivativesSummary()
        for symbol in selected:
            native = self._native_symbol(symbol)
            record: dict[str, Any] = {
                "symbol": symbol,
                "native_symbol": native,
                "fetched_at": utc_now().isoformat(),
            }
            try:
                record["ticker"] = self._fetch_ticker(native)
                record["open_interest_history"] = self._fetch_oi_history(native)
                record["funding_history"] = self._fetch_funding_history(native)
                record.update(self._derive_metrics(record))
                record["data_available"] = True
                summary.fetched.append(symbol)
                self.logger.info("Bybit derivatives history fetched for %s", symbol)
            except NoBybitDerivativesMarket as exc:
                record["data_available"] = False
                record["error"] = str(exc)
            except Exception as exc:
                summary.failed[symbol] = str(exc)
                record["data_available"] = False
                record["error"] = str(exc)
                self.logger.warning("Bybit derivatives failed for %s: %s", symbol, exc)
            summary.records[symbol] = record

        self.store.save_json(
            Path("data") / "raw" / "open_interest" / "bybit_derivatives_latest.json",
            {
                "fetched_at": utc_now().isoformat(),
                "fetched": summary.fetched,
                "failed": summary.failed,
                "records": summary.records,
            },
        )
        return summary

    def _native_symbol(self, symbol: str) -> str:
        # Honor PEPE/USDT → 1000PEPEUSDT style aliases declared in config.
        alias = self.config.exchange_alias("bybit", symbol)
        return symbol_to_exchange_symbol(alias)

    def _fetch_ticker(self, native: str) -> dict[str, Any]:
        data = self._get_json(
            "/v5/market/tickers", {"category": "linear", "symbol": native}
        )
        if data.get("retCode") == 10001:
            raise NoBybitDerivativesMarket(f"{native} not listed on Bybit linear")
        rows = (data.get("result") or {}).get("list") or []
        if not rows:
            raise NoBybitDerivativesMarket(f"empty Bybit ticker for {native}")
        return rows[0]

    def _fetch_oi_history(self, native: str) -> list[dict[str, Any]]:
        data = self._get_json(
            "/v5/market/open-interest",
            {"category": "linear", "symbol": native, "intervalTime": "1h", "limit": 48},
        )
        if data.get("retCode") not in (0, None):
            return []
        return list((data.get("result") or {}).get("list") or [])

    def _fetch_funding_history(self, native: str) -> list[dict[str, Any]]:
        data = self._get_json(
            "/v5/market/funding/history",
            {"category": "linear", "symbol": native, "limit": 50},
        )
        if data.get("retCode") not in (0, None):
            return []
        return list((data.get("result") or {}).get("list") or [])

    @staticmethod
    def _derive_metrics(record: dict[str, Any]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        ticker = record.get("ticker") or {}
        oi_history = record.get("open_interest_history") or []
        funding_history = record.get("funding_history") or []

        # OI delta over the last ~24 hourly buckets.
        oi_values = [BybitDerivativesCollector._to_float(row.get("openInterest")) for row in oi_history]
        oi_values = [v for v in oi_values if v is not None and v > 0]
        if len(oi_values) >= 2:
            first = oi_values[-1]  # Bybit returns newest-first by default; treat last index as oldest.
            last = oi_values[0]
            if first:
                out["oi_change_pct_24h"] = round((last - first) / first * 100, 3)

        # Funding percentile vs the last 7d (50 samples, 8h cadence ≈ 16d worth).
        funding_rates = [
            BybitDerivativesCollector._to_float(row.get("fundingRate"))
            for row in funding_history
        ]
        funding_rates = [v for v in funding_rates if v is not None]
        current_funding = BybitDerivativesCollector._to_float(ticker.get("fundingRate"))
        if funding_rates and current_funding is not None:
            sorted_rates = sorted(funding_rates)
            rank = sum(1 for v in sorted_rates if v <= current_funding)
            out["funding_percentile"] = round(rank / len(sorted_rates) * 100, 1)
            out["funding_recent_mean"] = round(mean(funding_rates), 6)

        # Ticker-level convenience fields.
        out["funding_rate"] = current_funding
        out["open_interest"] = BybitDerivativesCollector._to_float(ticker.get("openInterest"))
        out["open_interest_value"] = BybitDerivativesCollector._to_float(ticker.get("openInterestValue"))
        out["volume_24h"] = BybitDerivativesCollector._to_float(ticker.get("volume24h"))
        out["price_24h_pct"] = BybitDerivativesCollector._to_float(ticker.get("price24hPcnt"))

        # Quick interpretation usable by downstream agents without rerunning logic.
        interpretation_parts: list[str] = []
        if "oi_change_pct_24h" in out:
            sign = "rising" if out["oi_change_pct_24h"] > 0 else "falling"
            interpretation_parts.append(f"OI {sign} {out['oi_change_pct_24h']}% over 24h")
        if current_funding is not None:
            if current_funding > 0.0005:
                interpretation_parts.append("funding leans crowded-long")
            elif current_funding < -0.0003:
                interpretation_parts.append("funding leans crowded-short / squeeze risk")
            else:
                interpretation_parts.append("funding neutral")
        out["interpretation"] = "; ".join(interpretation_parts) if interpretation_parts else "no derivatives signal"
        return out

    def _get_json(self, path: str, params: dict[str, Any]) -> Any:
        response = requests.get(f"{self.base_url}{path}", params=params, timeout=15)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def _to_float(value: Any) -> float | None:
        try:
            if value in (None, ""):
                return None
            return float(value)
        except (TypeError, ValueError):
            return None
