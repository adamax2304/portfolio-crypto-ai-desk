"""Public, point-in-time order-book telemetry for crypto intraday research.

The collector is deliberately separate from routing and execution.  It records
only observable Binance Futures, Bybit Linear and MEXC Futures top-of-book/depth snapshots in
the market-intelligence sidecar so later Shadow research can distinguish a bad
signal from a bad fill environment without reconstructing liquidity after the
fact.
"""
from __future__ import annotations

import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests

from src.config import load_config
from src.data_collectors import market_intelligence_store as mi
from src.data_collectors.derivatives_pipeline import active_symbols


def _num(value: Any) -> float | None:
    try:
        value = float(value)
        return value if value >= 0 else None
    except (TypeError, ValueError):
        return None


def _iso_ms(value: Any, fallback: str) -> str:
    try:
        raw = float(value)
        if raw > 10_000_000_000:
            raw /= 1000.0
        return datetime.fromtimestamp(raw, tz=timezone.utc).isoformat()
    except (TypeError, ValueError, OSError):
        return fallback


def _levels(raw: Any) -> list[tuple[float, float]]:
    values: list[tuple[float, float]] = []
    for level in raw or []:
        if isinstance(level, dict):
            price, quantity = _num(level.get("price") or level.get("p")), _num(
                level.get("quantity") or level.get("vol") or level.get("v")
            )
        elif isinstance(level, (list, tuple)) and len(level) >= 2:
            price, quantity = _num(level[0]), _num(level[1])
        else:
            continue
        if price is not None and price > 0 and quantity is not None and quantity >= 0:
            values.append((price, quantity))
    return values


def book_metrics(
    bids: Any,
    asks: Any,
    *,
    quantity_multiplier: float | None = 1.0,
) -> dict[str, float | str | None]:
    """Return BBO and visible depth inside +/-10/25 bps.

    A MEXC contract quantity is only converted to USD when a positive contract
    multiplier was supplied.  Otherwise the BBO remains useful but depth is
    explicitly unavailable rather than mislabeled as dollar liquidity.
    """
    bid_rows = sorted(_levels(bids), key=lambda row: row[0], reverse=True)
    ask_rows = sorted(_levels(asks), key=lambda row: row[0])
    if not bid_rows or not ask_rows:
        return {"quality_status": "missing_bbo", "best_bid": None, "best_ask": None,
                "mid_price": None, "spread_bps": None, "bid_depth_10bps_usd": None,
                "ask_depth_10bps_usd": None, "bid_depth_25bps_usd": None,
                "ask_depth_25bps_usd": None}
    best_bid, best_ask = bid_rows[0][0], ask_rows[0][0]
    if best_bid <= 0 or best_ask <= 0 or best_bid > best_ask:
        return {"quality_status": "invalid_bbo", "best_bid": best_bid, "best_ask": best_ask,
                "mid_price": None, "spread_bps": None, "bid_depth_10bps_usd": None,
                "ask_depth_10bps_usd": None, "bid_depth_25bps_usd": None,
                "ask_depth_25bps_usd": None}
    mid = (best_bid + best_ask) / 2.0
    multiplier = _num(quantity_multiplier)
    quality = "ok" if multiplier and multiplier > 0 else "bbo_only_multiplier_unknown"

    def depth(rows: list[tuple[float, float]], side: str, bps: float) -> float | None:
        if not multiplier or multiplier <= 0:
            return None
        edge = mid * (1.0 - bps / 10_000.0) if side == "bid" else mid * (1.0 + bps / 10_000.0)
        selected = (row for row in rows if row[0] >= edge) if side == "bid" else (row for row in rows if row[0] <= edge)
        return sum(price * quantity * multiplier for price, quantity in selected)

    return {
        "quality_status": quality, "best_bid": best_bid, "best_ask": best_ask,
        "mid_price": mid, "spread_bps": ((best_ask / best_bid) - 1.0) * 10_000.0,
        "bid_depth_10bps_usd": depth(bid_rows, "bid", 10.0),
        "ask_depth_10bps_usd": depth(ask_rows, "ask", 10.0),
        "bid_depth_25bps_usd": depth(bid_rows, "bid", 25.0),
        "ask_depth_25bps_usd": depth(ask_rows, "ask", 25.0),
    }


class LiquidityCollector:
    """Keyless, bounded public BBO/depth collector.

    Binance and Bybit Linear quantities are base-asset quantities. MEXC Futures depth is a
    contract count, so its contract metadata is fetched first and a missing
    multiplier is represented as ``bbo_only_multiplier_unknown``.
    """

    def __init__(
        self,
        db_path: str | Path | None = None,
        *,
        trading_db_path: str | Path | None = None,
        session: requests.Session | None = None,
    ):
        self.db_path = Path(db_path or mi.default_db_path())
        self.trading_db_path = Path(trading_db_path) if trading_db_path else None
        self.session = session or requests.Session()
        endpoints = load_config().sources.get("public_endpoints", {}) or {}
        self.binance_base = "https://fapi.binance.com"
        self.bybit_base = str(endpoints.get("bybit") or "https://api.bybit.com").rstrip("/")
        # MEXC's current public contract API is served from api.mexc.com in
        # this environment.  Read only the configured public base; do not
        # inherit a private/live client endpoint or credentials.
        self.mexc_base = str(endpoints.get("mexc_futures") or "https://api.mexc.com").rstrip("/")
        self.derivatives_aliases = (
            (load_config().sources.get("derivatives_symbol_aliases") or {}).get("bybit", {}) or {}
        )

    @staticmethod
    def _binance_symbol(symbol: str) -> str:
        return mi.normalize_symbol(symbol)

    @staticmethod
    def _mexc_symbol(symbol: str) -> str:
        normal = str(symbol or "").upper().replace(":USDT", "")
        return normal.replace("/", "_").replace("-", "_")

    def _bybit_symbol(self, symbol: str) -> str:
        """Return the linear instrument, including 1000-token aliases."""
        native = self.derivatives_aliases.get(symbol)
        if not native:
            native = load_config().exchange_alias("bybit", symbol)
        value = str(native or symbol).upper().replace(":USDT", "")
        return value.replace("/", "").replace("-", "")

    def _get(self, base: str, path: str, params: dict[str, Any] | None = None) -> Any:
        response = self.session.get(f"{base}{path}", params=params, timeout=12)
        response.raise_for_status()
        return response.json()

    def _binance_row(self, symbol: str) -> dict[str, Any] | None:
        received = mi.utc_now_iso()
        payload = self._get(self.binance_base, "/fapi/v1/depth", {
            "symbol": self._binance_symbol(symbol), "limit": 20,
        })
        metrics = book_metrics(payload.get("bids"), payload.get("asks"), quantity_multiplier=1.0)
        if metrics.get("best_bid") is None:
            return None
        return {
            "provider_ts": _iso_ms(payload.get("E") or payload.get("T"), received),
            "received_at": received, "exchange": "binance", "symbol": symbol,
            "raw_json": payload, **metrics,
        }

    def _bybit_row(self, symbol: str) -> dict[str, Any] | None:
        received = mi.utc_now_iso()
        payload = self._get(self.bybit_base, "/v5/market/orderbook", {
            "category": "linear", "symbol": self._bybit_symbol(symbol), "limit": 25,
        })
        if int(payload.get("retCode") or 0) != 0:
            raise RuntimeError(f"Bybit orderbook retCode={payload.get('retCode')}")
        book = payload.get("result") if isinstance(payload, dict) else None
        book = book if isinstance(book, dict) else {}
        metrics = book_metrics(book.get("b"), book.get("a"), quantity_multiplier=1.0)
        if metrics.get("best_bid") is None:
            return None
        return {
            "provider_ts": _iso_ms(book.get("ts") or payload.get("time"), received),
            "received_at": received, "exchange": "bybit", "symbol": symbol,
            "raw_json": payload, **metrics,
        }

    def _mexc_contract_multiplier(self, native_symbol: str) -> float | None:
        payload = self._get(self.mexc_base, "/api/v1/contract/detail", {"symbol": native_symbol})
        data = payload.get("data") if isinstance(payload, dict) else None
        rows = data if isinstance(data, list) else [data] if isinstance(data, dict) else []
        row = next((item for item in rows if isinstance(item, dict)), {})
        return _num(row.get("contractSize") or row.get("contract_size"))

    def _mexc_row(self, symbol: str) -> dict[str, Any] | None:
        received = mi.utc_now_iso()
        native = self._mexc_symbol(symbol)
        multiplier = self._mexc_contract_multiplier(native)
        payload = self._get(self.mexc_base, f"/api/v1/contract/depth/{native}", {"limit": 20})
        data = payload.get("data") if isinstance(payload, dict) else None
        book = data if isinstance(data, dict) else payload if isinstance(payload, dict) else {}
        metrics = book_metrics(book.get("bids"), book.get("asks"), quantity_multiplier=multiplier)
        if metrics.get("best_bid") is None:
            return None
        return {
            "provider_ts": _iso_ms(book.get("timestamp") or payload.get("timestamp"), received),
            "received_at": received, "exchange": "mexc", "symbol": symbol,
            "raw_json": {"depth": payload, "contract_multiplier": multiplier}, **metrics,
        }

    def _collect_exchange(self, name: str, symbols: list[str]) -> tuple[list[dict[str, Any]], list[str]]:
        getters = {"binance": self._binance_row, "bybit": self._bybit_row, "mexc": self._mexc_row}
        getter = getters[name]
        rows: list[dict[str, Any]] = []
        errors: list[str] = []
        with ThreadPoolExecutor(max_workers=min(12, max(1, len(symbols)))) as pool:
            futures = {pool.submit(getter, symbol): symbol for symbol in symbols}
            for future in as_completed(futures):
                symbol = futures[future]
                try:
                    row = future.result()
                    if row:
                        rows.append(row)
                except Exception as exc:
                    errors.append(f"{symbol}:{type(exc).__name__}")
        return rows, errors

    def refresh(self, symbols: list[str] | None = None, *, limit: int = 60) -> dict[str, Any]:
        selected = list(symbols or active_symbols(limit, db_path=self.trading_db_path))[:limit]
        result: dict[str, Any] = {"symbols": len(selected), "written": 0, "sources": {}}
        with mi.connect(self.db_path):
            pass
        for name in ("binance", "bybit", "mexc"):
            started = time.perf_counter()
            try:
                rows, errors = self._collect_exchange(name, selected)
                with mi.connect(self.db_path, ensure=False) as conn:
                    written = sum(int(mi.insert_liquidity_snapshot(conn, **row)) for row in rows)
                    latest = max((row.get("provider_ts") for row in rows), default=None)
                    mi.record_source_health(
                        conn, f"liquidity:{name}", status="ok" if rows else "empty",
                        success=bool(rows), records_written=written, latest_provider_ts=latest,
                        latency_ms=(time.perf_counter() - started) * 1000,
                        details={"requested_symbols": len(selected), "rows": len(rows),
                                 "errors": errors[:20]},
                    )
                    conn.commit()
                result["sources"][name] = {"rows": len(rows), "written": written, "errors": errors}
                result["written"] += written
            except Exception as exc:
                with mi.connect(self.db_path, ensure=False) as conn:
                    mi.record_source_health(
                        conn, f"liquidity:{name}", status="error", success=False,
                        latency_ms=(time.perf_counter() - started) * 1000, error=str(exc)[:500],
                    )
                    conn.commit()
                result["sources"][name] = {"error": str(exc)}
        return result
