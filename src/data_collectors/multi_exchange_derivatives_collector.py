from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import requests

from src.config import ProjectConfig
from src.logger import get_logger
from src.storage.file_store import FileStore
from src.utils.symbols import symbol_to_exchange_symbol, symbol_to_ticker
from src.utils.time import utc_now


class NoExternalDerivativesMarket(Exception):
    pass


@dataclass
class MultiExchangeDerivativesCollectionSummary:
    fetched: list[str] = field(default_factory=list)
    failed: dict[str, str] = field(default_factory=dict)
    records: dict[str, dict[str, Any]] = field(default_factory=dict)


class MultiExchangeDerivativesCollector:
    """Collect public Bybit / OKX / MEXC funding and OI context.

    Binance remains the main derivatives source. This collector adds exchange
    agreement/disagreement so the report can see when one venue may be noisy.
    PART 14b (2026-06) added MEXC as a third fallback — MEXC lists almost
    every alt that ever made a wave, so its inclusion eliminates most
    "derivatives data unavailable" rejections for low-cap alts.
    """

    def __init__(self, config: ProjectConfig, store: FileStore):
        self.config = config
        self.store = store
        endpoints = config.sources.get("public_endpoints", {})
        self.bybit_base = endpoints.get("bybit", "https://api.bybit.com")
        self.okx_base = endpoints.get("okx", "https://www.okx.com")
        self.mexc_base = endpoints.get("mexc_futures", "https://contract.mexc.com")
        self.symbol_aliases = config.sources.get("derivatives_symbol_aliases", {})
        self.logger = get_logger(self.__class__.__name__)

    def fetch(self, symbols: list[str] | None = None) -> MultiExchangeDerivativesCollectionSummary:
        selected = symbols or self.config.symbols
        summary = MultiExchangeDerivativesCollectionSummary()

        for symbol in selected:
            record: dict[str, Any] = {"symbol": symbol, "fetched_at": utc_now().isoformat(), "exchanges": {}}
            errors: dict[str, str] = {}
            try:
                record["exchanges"]["bybit"] = self._fetch_bybit(symbol)
            except NoExternalDerivativesMarket:
                pass
            except Exception as exc:
                errors["bybit"] = str(exc)
            try:
                record["exchanges"]["okx"] = self._fetch_okx(symbol)
            except NoExternalDerivativesMarket:
                pass
            except Exception as exc:
                errors["okx"] = str(exc)
            try:
                record["exchanges"]["mexc"] = self._fetch_mexc(symbol)
            except NoExternalDerivativesMarket:
                pass
            except Exception as exc:
                errors["mexc"] = str(exc)

            if record["exchanges"]:
                summary.fetched.append(symbol)
                self.logger.info("Fetched external futures context for %s", symbol)
            if errors:
                summary.failed[symbol] = "; ".join(f"{key}: {value}" for key, value in errors.items())
                record["errors"] = errors
            if not record["exchanges"] and not errors:
                record["data_available"] = False
            summary.records[symbol] = record

        self.store.save_json(
            Path("data") / "raw" / "open_interest" / "multi_exchange_derivatives_latest.json",
            {
                "fetched_at": utc_now().isoformat(),
                "fetched": summary.fetched,
                "failed": summary.failed,
                "records": summary.records,
            },
        )
        return summary

    def _fetch_bybit(self, symbol: str) -> dict[str, Any]:
        params = {"category": "linear", "symbol": self._derivatives_symbol("bybit", symbol)}
        data = self._get_json(self.bybit_base, "/v5/market/tickers", params)
        if data.get("retCode") == 10001:
            raise NoExternalDerivativesMarket("symbol not listed on Bybit linear futures")
        rows = data.get("result", {}).get("list", [])
        if not rows:
            raise NoExternalDerivativesMarket("empty Bybit ticker response")
        row = rows[0]
        return {
            "funding_rate": self._to_float(row.get("fundingRate")),
            "open_interest": self._to_float(row.get("openInterest")),
            "open_interest_value": self._to_float(row.get("openInterestValue")),
            "price_24h_pct": self._to_float(row.get("price24hPcnt")),
            "volume_24h": self._to_float(row.get("volume24h")),
        }

    def _fetch_mexc(self, symbol: str) -> dict[str, Any]:
        """Fetch funding + open interest from MEXC contract API.

        MEXC contract symbols use ``BASE_QUOTE`` style (e.g. ``BTC_USDT``).
        The ticker endpoint returns both ``fundingRate`` and ``holdVol``
        (open interest) plus ``riseFallRate`` (24h change pct), so a
        single round-trip per symbol is enough.
        """
        contract_symbol = self._mexc_contract_symbol(symbol)
        ticker = self._get_json(
            self.mexc_base, "/api/v1/contract/ticker",
            {"symbol": contract_symbol},
        )
        if not isinstance(ticker, dict) or not ticker.get("success"):
            raise NoExternalDerivativesMarket(
                f"MEXC ticker failure for {contract_symbol}"
            )
        data = ticker.get("data") or {}
        if isinstance(data, list):
            data = data[0] if data else {}
        if not data:
            raise NoExternalDerivativesMarket(
                f"empty MEXC ticker for {contract_symbol}"
            )
        funding_rate = self._to_float(data.get("fundingRate"))
        hold_vol = self._to_float(data.get("holdVol"))
        last_price = self._to_float(data.get("lastPrice"))
        return {
            "funding_rate": funding_rate,
            "open_interest": hold_vol,
            # holdVol is contract-count OI and amount24 is traded volume, not
            # OI USD. A USD conversion requires the contract size metadata.
            "open_interest_value": None,
            "open_interest_unit": "contracts",
            "price_24h_pct": self._to_float(data.get("riseFallRate")),
            "last_price": last_price,
        }

    def _mexc_contract_symbol(self, symbol: str) -> str:
        """MEXC contract symbols use ``BASE_QUOTE`` (with underscore).

        ``symbol_to_exchange_symbol`` strips the slash so we can't reuse
        it here — operate directly on the canonical ``BASE/QUOTE`` form.
        """
        aliases = self.symbol_aliases.get("mexc", {})
        if symbol in aliases:
            return str(aliases[symbol])
        if "/" in symbol:
            return symbol.replace("/", "_")
        # Already in MEXC form (BTC_USDT) or stripped (BTCUSDT) — return as-is.
        return symbol

    def _fetch_okx(self, symbol: str) -> dict[str, Any]:
        inst_id = self._okx_inst_id(symbol)
        oi_payload = self._get_json(
            self.okx_base, "/api/v5/public/open-interest", {"instType": "SWAP", "instId": inst_id}
        )
        funding_payload = self._get_json(
            self.okx_base, "/api/v5/public/funding-rate", {"instId": inst_id}
        )
        oi_row = (oi_payload.get("data") or [{}])[0]
        funding_row = (funding_payload.get("data") or [{}])[0]
        if not oi_row and not funding_row:
            raise NoExternalDerivativesMarket("empty OKX derivatives response")
        return {
            "funding_rate": self._to_float(funding_row.get("fundingRate")),
            "open_interest": self._to_float(oi_row.get("oi")),
            "open_interest_ccy": self._to_float(oi_row.get("oiCcy")),
            "open_interest_usd": self._to_float(oi_row.get("oiUsd")),
        }

    @staticmethod
    def _get_json(base_url: str, path: str, params: dict[str, Any]) -> Any:
        response = requests.get(f"{base_url}{path}", params=params, timeout=15)
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

    def _derivatives_symbol(self, exchange: str, symbol: str) -> str:
        aliases = self.symbol_aliases.get(exchange, {})
        return str(aliases.get(symbol, symbol_to_exchange_symbol(symbol)))

    def _okx_inst_id(self, symbol: str) -> str:
        aliases = self.symbol_aliases.get("okx", {})
        if symbol in aliases:
            return str(aliases[symbol])
        return f"{symbol_to_ticker(symbol)}-USDT-SWAP"
