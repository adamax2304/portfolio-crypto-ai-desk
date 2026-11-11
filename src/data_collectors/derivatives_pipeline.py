"""Keyless multi-venue derivatives collection and bounded public backfill."""
from __future__ import annotations

import hashlib
import sqlite3
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import requests

from src.config import load_config
from src.data_collectors import market_intelligence_store as mi


def _f(value: Any) -> float | None:
    try:
        return None if value in (None, "") else float(value)
    except (TypeError, ValueError):
        return None


def _iso_ms(value: Any, fallback: str) -> str:
    try:
        number = float(value)
        if number > 10_000_000_000:
            number /= 1000.0
        return datetime.fromtimestamp(number, tz=timezone.utc).isoformat()
    except (TypeError, ValueError, OSError):
        return fallback


def active_symbols(limit: int = 80, db_path: str | Path | None = None) -> list[str]:
    cfg = load_config()
    ordered = ["BTC/USDT", "ETH/USDT", "SOL/USDT"]
    path = Path(db_path or cfg.db_path)
    if path.exists():
        try:
            conn = sqlite3.connect(f"file:{path.as_posix()}?mode=ro", uri=True, timeout=2.0)
            since = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
            rows = conn.execute(
                "SELECT symbol,COUNT(*) n FROM proposed_signals WHERE asset_class='crypto' AND created_at>=? "
                "GROUP BY symbol ORDER BY n DESC", (since,),
            ).fetchall()
            conn.close()
            ordered.extend(str(r[0]) for r in rows if r[0])
        except sqlite3.Error:
            pass
    ordered.extend(cfg.symbols)
    result = []
    for symbol in ordered:
        canonical = str(symbol).upper()
        if "/" not in canonical and canonical.endswith("USDT"):
            canonical = f"{canonical[:-4]}/USDT"
        if canonical not in result:
            result.append(canonical)
    return result[:limit]


def _aliases(exchange: str, symbols: list[str]) -> dict[str, str]:
    cfg = load_config()
    source_aliases = (cfg.sources.get("derivatives_symbol_aliases") or {}).get(exchange, {}) or {}
    result = {}
    for symbol in symbols:
        native = source_aliases.get(symbol) or cfg.exchange_alias(exchange, symbol)
        if native == symbol:
            native = symbol.replace("/", "")
        result[str(native).upper()] = symbol
    return result


class DerivativesPipeline:
    def __init__(self, db_path: str | Path | None = None, session: requests.Session | None = None,
                 trading_db_path: str | Path | None = None):
        self.cfg = load_config()
        self.trading_db_path = Path(trading_db_path or self.cfg.db_path)
        self.db_path = Path(db_path or mi.default_db_path())
        self.session = session or requests.Session()
        endpoints = self.cfg.sources.get("public_endpoints", {}) or {}
        self.binance = endpoints.get("binance_futures", "https://fapi.binance.com")
        self.bybit = endpoints.get("bybit", "https://api.bybit.com")
        self.okx = endpoints.get("okx", "https://www.okx.com")
        self.mexc = endpoints.get("mexc_futures", "https://api.mexc.com")
        self.hyperliquid = "https://api.hyperliquid.xyz"

    def _get(self, base: str, path: str, params: dict | None = None) -> Any:
        response = self.session.get(f"{base}{path}", params=params, timeout=15)
        response.raise_for_status()
        payload = response.json()
        if base.rstrip("/") == self.bybit.rstrip("/") and isinstance(payload, dict):
            code = payload.get("retCode")
            if code not in (None, 0, "0"):
                raise RuntimeError(f"Bybit retCode={code}: {payload.get('retMsg') or 'unknown error'}")
        return payload

    def _post(self, base: str, path: str, payload: dict) -> Any:
        response = self.session.post(f"{base}{path}", json=payload, timeout=15)
        response.raise_for_status()
        return response.json()

    def refresh_current(self, symbols: list[str] | None = None) -> dict[str, Any]:
        selected = symbols or active_symbols(db_path=self.trading_db_path)
        result = {"symbols": len(selected), "written": 0, "sources": {}}
        # Migrate/create once before any network work. Per-source connections
        # below skip repeated DDL and hold only short data-write transactions.
        with mi.connect(self.db_path):
            pass
        for name, fetcher in (
            ("binance", self._current_binance), ("bybit", self._current_bybit),
            ("hyperliquid", self._current_hyperliquid), ("okx", self._current_okx),
            ("mexc", self._current_mexc),
        ):
            started = time.perf_counter()
            try:
                # Complete the network request before opening a write
                # transaction. This keeps the shared SQLite writer lock short.
                rows = fetcher(selected)
                latest = max((r.get("provider_ts") for r in rows), default=None)
                with mi.connect(self.db_path, ensure=False) as conn:
                    written = sum(1 for row in rows if mi.insert_derivative_snapshot(conn, **row))
                    mi.record_source_health(
                        conn, f"derivatives:{name}", status="ok" if rows else "empty",
                        success=bool(rows), records_written=written, latest_provider_ts=latest,
                        latency_ms=(time.perf_counter() - started) * 1000,
                        details={"requested_symbols": len(selected), "rows": len(rows)},
                    )
                    conn.commit()
                result["sources"][name] = {"rows": len(rows), "written": written}
                result["written"] += written
            except Exception as exc:
                # A temporary database lock or one failed venue must not kill
                # the daemon or prevent the other venues from refreshing.
                try:
                    with mi.connect(self.db_path, ensure=False) as conn:
                        mi.record_source_health(
                            conn, f"derivatives:{name}", status="error", success=False,
                            latency_ms=(time.perf_counter() - started) * 1000, error=str(exc)[:500],
                        )
                        conn.commit()
                except sqlite3.Error:
                    pass
                result["sources"][name] = {"error": str(exc)}
        return result

    def _current_binance(self, symbols: list[str]) -> list[dict]:
        aliases = _aliases("binance_futures", symbols)
        premium = self._get(self.binance, "/fapi/v1/premiumIndex")
        premium_map = {str(r.get("symbol", "")).upper(): r for r in premium if isinstance(r, dict)}
        rows = []

        def fetch_oi(native: str):
            return native, self._get(self.binance, "/fapi/v1/openInterest", {"symbol": native})

        oi_map = {}
        with ThreadPoolExecutor(max_workers=8) as pool:
            futures = [pool.submit(fetch_oi, native) for native in aliases if native in premium_map]
            for future in as_completed(futures):
                try:
                    native, payload = future.result()
                    oi_map[native] = payload
                except Exception:
                    continue
        received = mi.utc_now_iso()
        for native, symbol in aliases.items():
            p, oi = premium_map.get(native), oi_map.get(native, {})
            if not p:
                continue
            mark, index, oi_native = _f(p.get("markPrice")), _f(p.get("indexPrice")), _f(oi.get("openInterest"))
            rows.append({
                "provider_ts": _iso_ms(p.get("time"), received), "received_at": received,
                "exchange": "binance", "symbol": symbol, "instrument_id": native,
                "source_kind": "current_poll", "funding_rate": _f(p.get("lastFundingRate")),
                "funding_interval_hours": 8.0, "predicted_funding_rate": _f(p.get("interestRate")),
                "oi_native": oi_native, "oi_usd": oi_native * mark if oi_native and mark else None,
                "mark_price": mark, "index_price": index,
                "basis_bps": ((mark / index) - 1) * 10000 if mark and index else None,
                "raw_json": {"premium": p, "oi": oi},
            })
        return rows

    def _current_bybit(self, symbols: list[str]) -> list[dict]:
        aliases = _aliases("bybit", symbols)
        payload = self._get(self.bybit, "/v5/market/tickers", {"category": "linear"})
        intervals = self._bybit_funding_intervals(set(aliases))
        received = mi.utc_now_iso(); rows = []
        for item in (payload.get("result") or {}).get("list") or []:
            native = str(item.get("symbol", "")).upper()
            symbol = aliases.get(native)
            if not symbol:
                continue
            mark, index = _f(item.get("markPrice")), _f(item.get("indexPrice"))
            rows.append({
                "provider_ts": received, "received_at": received, "exchange": "bybit",
                "symbol": symbol, "instrument_id": native, "source_kind": "current_poll",
                "funding_rate": _f(item.get("fundingRate")),
                "funding_interval_hours": intervals.get(native, 8.0),
                "predicted_funding_rate": _f(item.get("predictedFundingRate")),
                "oi_native": _f(item.get("openInterest")), "oi_usd": _f(item.get("openInterestValue")),
                "mark_price": mark, "index_price": index,
                "basis_bps": ((mark / index) - 1) * 10000 if mark and index else None,
                "raw_json": item,
            })
        return rows

    def _bybit_funding_intervals(self, wanted: set[str] | None = None) -> dict[str, float]:
        """Return each linear instrument's funding interval in hours.

        Bybit exposes the interval in minutes through instruments-info and some
        contracts do not use the common eight-hour cadence. Pagination is kept
        bounded, and callers retain an explicit 8h fallback if this metadata
        endpoint is temporarily unavailable.
        """
        result: dict[str, float] = {}
        cursor: str | None = None
        for _ in range(3):
            params: dict[str, Any] = {"category": "linear", "limit": 1000}
            if cursor:
                params["cursor"] = cursor
            payload = self._get(self.bybit, "/v5/market/instruments-info", params)
            body = payload.get("result") or {}
            for row in body.get("list") or []:
                native = str(row.get("symbol") or "").upper()
                minutes = _f(row.get("fundingInterval"))
                if native and minutes and minutes > 0:
                    result[native] = minutes / 60.0
            if wanted and wanted.issubset(result):
                break
            cursor = str(body.get("nextPageCursor") or "") or None
            if not cursor:
                break
        return result

    def _current_hyperliquid(self, symbols: list[str]) -> list[dict]:
        wanted = {mi.base_symbol(s): s for s in symbols}
        payload = self._post(self.hyperliquid, "/info", {"type": "metaAndAssetCtxs"})
        if not isinstance(payload, list) or len(payload) < 2:
            return []
        universe = (payload[0] or {}).get("universe") or []
        contexts = payload[1] or []
        received = mi.utc_now_iso(); rows = []
        for meta, item in zip(universe, contexts):
            coin = str(meta.get("name", "")).upper()
            symbol = wanted.get(coin)
            if not symbol:
                continue
            mark, oracle, oi_native = _f(item.get("markPx")), _f(item.get("oraclePx")), _f(item.get("openInterest"))
            rows.append({
                "provider_ts": received, "received_at": received, "exchange": "hyperliquid",
                "symbol": symbol, "instrument_id": coin, "source_kind": "current_poll",
                "funding_rate": _f(item.get("funding")), "funding_interval_hours": 1.0,
                "oi_native": oi_native, "oi_usd": oi_native * mark if oi_native and mark else None,
                "mark_price": mark, "index_price": oracle,
                "basis_bps": ((mark / oracle) - 1) * 10000 if mark and oracle else None,
                "raw_json": {"meta": meta, "context": item},
            })
        return rows

    def _current_okx(self, symbols: list[str]) -> list[dict]:
        wanted = {f"{mi.base_symbol(s)}-USDT-SWAP": s for s in symbols}
        oi_payload = self._get(self.okx, "/api/v5/public/open-interest", {"instType": "SWAP"})
        oi_map = {str(r.get("instId")): r for r in oi_payload.get("data") or []}
        rows = []; received = mi.utc_now_iso()

        def funding(inst: str):
            return inst, self._get(self.okx, "/api/v5/public/funding-rate", {"instId": inst})

        funding_map = {}
        with ThreadPoolExecutor(max_workers=6) as pool:
            futures = [pool.submit(funding, inst) for inst in wanted if inst in oi_map]
            for future in as_completed(futures):
                try:
                    inst, payload = future.result()
                    funding_map[inst] = ((payload.get("data") or [{}])[0])
                except Exception:
                    continue
        for inst, symbol in wanted.items():
            oi, fund = oi_map.get(inst), funding_map.get(inst, {})
            if not oi and not fund:
                continue
            rows.append({
                "provider_ts": _iso_ms((fund or {}).get("ts") or (oi or {}).get("ts"), received),
                "received_at": received, "exchange": "okx", "symbol": symbol,
                "instrument_id": inst, "source_kind": "current_poll",
                "funding_rate": _f(fund.get("fundingRate")), "funding_interval_hours": 8.0,
                "predicted_funding_rate": _f(fund.get("nextFundingRate")),
                "oi_native": _f((oi or {}).get("oi")), "oi_usd": _f((oi or {}).get("oiUsd")),
                "raw_json": {"funding": fund, "oi": oi},
            })
        return rows

    def _current_mexc(self, symbols: list[str]) -> list[dict]:
        wanted = {s.replace("/", "_").upper(): s for s in symbols}
        payload = self._get(self.mexc, "/api/v1/contract/ticker")
        items = payload.get("data") if isinstance(payload, dict) else []
        items = items if isinstance(items, list) else [items]
        rows = []; received = mi.utc_now_iso()
        for item in items:
            native = str((item or {}).get("symbol", "")).upper()
            symbol = wanted.get(native)
            if not symbol:
                continue
            mark, oi_native = _f(item.get("lastPrice")), _f(item.get("holdVol"))
            rows.append({
                "provider_ts": _iso_ms(item.get("timestamp"), received), "received_at": received,
                "exchange": "mexc", "symbol": symbol, "instrument_id": native,
                "source_kind": "current_poll", "funding_rate": _f(item.get("fundingRate")),
                "funding_interval_hours": 8.0, "oi_native": oi_native,
                # holdVol is in exchange contract units. Without the contract
                # size, holdVol*price is not USD OI and can be orders of
                # magnitude wrong. Preserve native OI but leave USD unknown.
                "oi_usd": None, "mark_price": mark, "quality_status": "partial_contract_units",
                "raw_json": item,
            })
        return rows

    def backfill(self, symbols: list[str] | None = None, days: int = 30) -> dict[str, Any]:
        selected = (symbols or active_symbols(40, self.trading_db_path))[:40]
        # Binance documents roughly one month of OI history but rejects a
        # startTime exactly on the rolling 30-day boundary. Keep one day of
        # margin instead of turning normal retention into a source failure.
        start = datetime.now(timezone.utc) - timedelta(days=min(max(days, 1), 29))
        result = {"symbols": len(selected), "funding_events": 0, "oi_snapshots": 0, "errors": {}}
        hyperliquid_coins: set[str] = set()
        try:
            meta = self._post(self.hyperliquid, "/info", {"type": "meta"})
            hyperliquid_coins = {str(r.get("name") or "").upper() for r in (meta.get("universe") or [])}
        except Exception as exc:
            result["errors"]["hyperliquid:universe"] = str(exc)
        bybit_aliases = _aliases("bybit", selected)
        try:
            bybit_intervals = self._bybit_funding_intervals(set(bybit_aliases))
        except Exception as exc:
            bybit_intervals = {}
            result["errors"]["bybit:instruments"] = str(exc)
        with mi.connect(self.db_path) as conn:
            for symbol in selected:
                base = mi.base_symbol(symbol)
                native = symbol.replace("/", "")
                try:
                    events = self._get(self.binance, "/fapi/v1/fundingRate", {
                        "symbol": native, "startTime": int(start.timestamp() * 1000), "limit": 1000})
                    for row in events if isinstance(events, list) else []:
                        result["funding_events"] += int(mi.insert_funding_event(
                            conn, event_at=_iso_ms(row.get("fundingTime"), mi.utc_now_iso()),
                            exchange="binance", symbol=symbol, funding_rate=_f(row.get("fundingRate")),
                            funding_interval_hours=8.0, source_kind="settlement_history", raw_json=row))
                    oi_rows = self._get(self.binance, "/futures/data/openInterestHist", {
                        "symbol": native, "period": "1h", "limit": 500,
                        "startTime": int(start.timestamp() * 1000)})
                    for row in oi_rows if isinstance(oi_rows, list) else []:
                        result["oi_snapshots"] += int(mi.insert_derivative_snapshot(
                            conn, provider_ts=_iso_ms(row.get("timestamp"), mi.utc_now_iso()),
                            exchange="binance", symbol=symbol, instrument_id=native,
                            source_kind="oi_history_1h", oi_native=_f(row.get("sumOpenInterest")),
                            oi_usd=_f(row.get("sumOpenInterestValue")), raw_json=row))
                except Exception as exc:
                    result["errors"][f"binance:{symbol}"] = str(exc)
                try:
                    bybit_native = next((n for n, s in bybit_aliases.items() if s == symbol), native)
                    start_ms = int(start.timestamp() * 1000)
                    funding_end_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
                    for _ in range(6):
                        funding_payload = self._get(self.bybit, "/v5/market/funding/history", {
                            "category": "linear", "symbol": bybit_native, "limit": 200,
                            "startTime": start_ms, "endTime": funding_end_ms})
                        funding_rows = (funding_payload.get("result") or {}).get("list") or []
                        if not funding_rows:
                            break
                        oldest = funding_end_ms
                        for row in funding_rows:
                            ts_ms = int(float(row.get("fundingRateTimestamp") or funding_end_ms))
                            oldest = min(oldest, ts_ms)
                            if ts_ms < start_ms:
                                continue
                            result["funding_events"] += int(mi.insert_funding_event(
                                conn, event_at=_iso_ms(ts_ms, mi.utc_now_iso()),
                                exchange="bybit", symbol=symbol, funding_rate=_f(row.get("fundingRate")),
                                funding_interval_hours=bybit_intervals.get(bybit_native, 8.0),
                                source_kind="settlement_history", raw_json=row))
                        if oldest <= start_ms or oldest >= funding_end_ms:
                            break
                        funding_end_ms = oldest - 1
                    end_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
                    for _ in range(4):
                        oi_payload = self._get(self.bybit, "/v5/market/open-interest", {
                            "category": "linear", "symbol": bybit_native, "intervalTime": "1h",
                            "limit": 200, "endTime": end_ms})
                        oi_rows = (oi_payload.get("result") or {}).get("list") or []
                        if not oi_rows:
                            break
                        oldest = end_ms
                        for row in oi_rows:
                            ts_ms = int(float(row.get("timestamp") or end_ms))
                            oldest = min(oldest, ts_ms)
                            result["oi_snapshots"] += int(mi.insert_derivative_snapshot(
                                conn, provider_ts=_iso_ms(ts_ms, mi.utc_now_iso()), exchange="bybit",
                                symbol=symbol, instrument_id=bybit_native, source_kind="oi_history_1h",
                                oi_native=_f(row.get("openInterest")), raw_json=row))
                        if oldest <= int(start.timestamp() * 1000):
                            break
                        end_ms = oldest - 1
                except Exception as exc:
                    result["errors"][f"bybit:{symbol}"] = str(exc)
                try:
                    inst = f"{base}-USDT-SWAP"
                    okx_payload = self._get(self.okx, "/api/v5/public/funding-rate-history", {
                        "instId": inst, "limit": 100})
                    for row in okx_payload.get("data") or []:
                        event_at = _iso_ms(row.get("fundingTime"), mi.utc_now_iso())
                        parsed = datetime.fromisoformat(event_at)
                        if parsed >= start:
                            result["funding_events"] += int(mi.insert_funding_event(
                                conn, event_at=event_at, exchange="okx", symbol=symbol,
                                funding_rate=_f(row.get("realizedRate") or row.get("fundingRate")),
                                funding_interval_hours=8.0, source_kind="settlement_history", raw_json=row))
                except Exception as exc:
                    result["errors"][f"okx:{symbol}"] = str(exc)
                try:
                    if base not in hyperliquid_coins:
                        continue
                    rows = self._post(self.hyperliquid, "/info", {
                        "type": "fundingHistory", "coin": base,
                        "startTime": int(start.timestamp() * 1000),
                        "endTime": int(datetime.now(timezone.utc).timestamp() * 1000)})
                    for row in rows if isinstance(rows, list) else []:
                        result["funding_events"] += int(mi.insert_funding_event(
                            conn, event_at=_iso_ms(row.get("time"), mi.utc_now_iso()),
                            exchange="hyperliquid", symbol=symbol, funding_rate=_f(row.get("fundingRate")),
                            funding_interval_hours=1.0, source_kind="settlement_history", raw_json=row))
                except Exception as exc:
                    result["errors"][f"hyperliquid:{symbol}"] = str(exc)
            for source in ("binance", "bybit", "okx", "hyperliquid"):
                failures = {k: v for k, v in result["errors"].items() if k.startswith(source + ":")}
                mi.record_source_health(
                    conn, f"derivatives_backfill:{source}",
                    status="degraded" if failures else "ok", success=not failures,
                    records_written=result["funding_events"] + result["oi_snapshots"],
                    error="; ".join(failures.values())[:500] if failures else None,
                    details={"symbols": len(selected), "failures": len(failures)},
                )
            conn.commit()
        return result


def liquidation_event_id(exchange: str, payload: dict[str, Any]) -> str:
    raw = f"{exchange}|{payload.get('s')}|{payload.get('T')}|{payload.get('S')}|{payload.get('p')}|{payload.get('q')}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()
