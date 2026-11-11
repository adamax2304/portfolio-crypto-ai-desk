from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import requests

from src.config import ProjectConfig
from src.logger import get_logger
from src.storage.file_store import FileStore
from src.utils.symbols import symbol_to_exchange_symbol
from src.utils.time import utc_now


class NoDerivativesMarket(Exception):
    pass


@dataclass
class DerivativesCollectionSummary:
    fetched: list[str] = field(default_factory=list)
    failed: dict[str, str] = field(default_factory=dict)
    records: dict[str, dict[str, Any]] = field(default_factory=dict)


class BinanceDerivativesCollector:
    """Fetch public Binance USD-M futures positioning context.

    These endpoints do not require API keys. Missing symbols are expected for some
    spot listings, so failures are captured per symbol rather than raised.
    """

    def __init__(self, config: ProjectConfig, store: FileStore):
        self.config = config
        self.store = store
        self.base_url = config.sources.get("public_endpoints", {}).get(
            "binance_futures", "https://fapi.binance.com"
        )
        self.symbol_aliases = config.sources.get("derivatives_symbol_aliases", {}).get(
            "binance_futures", {}
        )
        self.logger = get_logger(self.__class__.__name__)

    def fetch(self, symbols: list[str] | None = None) -> DerivativesCollectionSummary:
        selected = symbols or self.config.symbols
        summary = DerivativesCollectionSummary()

        for symbol in selected:
            exchange_symbol = self._derivatives_symbol(symbol)
            record: dict[str, Any] = {
                "symbol": symbol,
                "exchange_symbol": exchange_symbol,
                "fetched_at": utc_now().isoformat(),
            }
            try:
                record["premium_index"] = self._get_json(
                    "/fapi/v1/premiumIndex", {"symbol": exchange_symbol}
                )
                record["open_interest"] = self._get_json(
                    "/fapi/v1/openInterest", {"symbol": exchange_symbol}
                )
                record["open_interest_hist"] = self._get_json(
                    "/futures/data/openInterestHist",
                    {"symbol": exchange_symbol, "period": "1h", "limit": 24},
                )
                record["long_short_ratio"] = self._get_json(
                    "/futures/data/globalLongShortAccountRatio",
                    {"symbol": exchange_symbol, "period": "1h", "limit": 1},
                )
                summary.fetched.append(symbol)
                summary.records[symbol] = record
                self.logger.info("Fetched futures context for %s", symbol)
            except NoDerivativesMarket as exc:
                summary.records[symbol] = {
                    **record,
                    "error": str(exc),
                    "data_available": False,
                }
                self.logger.info("No Binance futures market for %s", symbol)
            except Exception as exc:
                summary.failed[symbol] = str(exc)
                summary.records[symbol] = {
                    **record,
                    "error": str(exc),
                    "data_available": False,
                }
                self.logger.warning("Failed futures context for %s: %s", symbol, exc)

        self.store.save_json(
            Path("data") / "raw" / "open_interest" / "binance_futures_latest.json",
            {
                "fetched_at": utc_now().isoformat(),
                "fetched": summary.fetched,
                "failed": summary.failed,
                "records": summary.records,
            },
        )
        self.store.save_json(
            Path("data") / "raw" / "funding" / "binance_futures_latest.json",
            {
                "fetched_at": utc_now().isoformat(),
                "records": {
                    symbol: record.get("premium_index", {})
                    for symbol, record in summary.records.items()
                },
            },
        )
        return summary

    def _get_json(self, path: str, params: dict[str, Any]) -> Any:
        response = requests.get(
            f"{self.base_url}{path}", params=params, timeout=15
        )
        if response.status_code == 400:
            try:
                payload = response.json()
            except ValueError:
                payload = {}
            if payload.get("code") == -1121:
                raise NoDerivativesMarket("symbol not listed on Binance USD-M futures")
        response.raise_for_status()
        return response.json()

    def _derivatives_symbol(self, symbol: str) -> str:
        return str(self.symbol_aliases.get(symbol, symbol_to_exchange_symbol(symbol)))
