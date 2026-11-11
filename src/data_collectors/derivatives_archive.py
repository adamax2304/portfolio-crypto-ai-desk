"""Best-effort archival adapter for all public derivatives collectors.

Legacy ``funding_snapshots``/``oi_snapshots`` remain populated for existing
reports.  In parallel, every non-empty observation is normalized into the
canonical point-in-time tables in ``market_intelligence_store``.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.data_collectors import market_intelligence_store as mi


def _f(value: Any) -> float | None:
    try:
        if value in (None, ""):
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _iso_ms(value: Any, fallback: str) -> str:
    try:
        numeric = float(value)
        if numeric > 10_000_000_000:
            numeric /= 1000.0
        return datetime.fromtimestamp(numeric, tz=timezone.utc).isoformat()
    except (TypeError, ValueError, OSError):
        return fallback


def _basis_bps(mark: float | None, index: float | None) -> float | None:
    return ((mark / index) - 1.0) * 10_000.0 if mark and index else None


def _legacy_write(store: Any, *, fetched_at: str, exchange: str, symbol: str,
                  funding_rate: float | None, next_funding_time: str | None,
                  mark_price: float | None, index_price: float | None,
                  oi_native: float | None, oi_usd: float | None,
                  oi_change_pct: float | None, long_short_ratio: float | None,
                  crowding_label: str | None, raw: Any,
                  source_file: str | None, out: dict[str, int]) -> None:
    norm = mi.normalize_symbol(symbol)
    if any(v is not None for v in (funding_rate, mark_price, index_price, long_short_ratio)):
        try:
            if store.record_funding_snapshot(
                fetched_at=fetched_at, exchange=exchange, symbol=symbol,
                normalized_symbol=norm, funding_rate=funding_rate,
                next_funding_time=next_funding_time, mark_price=mark_price,
                index_price=index_price, long_short_ratio=long_short_ratio,
                crowding_label=crowding_label,
                raw_json=json.dumps(raw, default=str)[:4000] if raw else None,
                source_file=source_file,
            ):
                out["funding"] += 1
        except Exception:
            out["errors"] += 1
    if any(v is not None for v in (oi_native, oi_usd, oi_change_pct, long_short_ratio)):
        try:
            if store.record_oi_snapshot(
                fetched_at=fetched_at, exchange=exchange, symbol=symbol,
                normalized_symbol=norm, oi_value=oi_native, oi_value_usd=oi_usd,
                oi_change_pct=oi_change_pct, long_short_ratio=long_short_ratio,
                crowding_label=crowding_label,
                raw_json=json.dumps(raw, default=str)[:4000] if raw else None,
                source_file=source_file,
            ):
                out["oi"] += 1
        except Exception:
            out["errors"] += 1


def _canonical_current(conn: Any, *, fetched_at: str, exchange: str, symbol: str,
                       instrument_id: str | None, funding_rate: float | None,
                       funding_interval_hours: float | None, oi_native: float | None,
                       oi_usd: float | None, mark_price: float | None,
                       index_price: float | None, long_short_ratio: float | None,
                       raw: Any) -> bool:
    return mi.insert_derivative_snapshot(
        conn, provider_ts=fetched_at, received_at=mi.utc_now_iso(), exchange=exchange,
        symbol=symbol, instrument_id=instrument_id, source_kind="current",
        funding_rate=funding_rate, funding_interval_hours=funding_interval_hours,
        oi_native=oi_native, oi_usd=oi_usd, mark_price=mark_price,
        index_price=index_price, basis_bps=_basis_bps(mark_price, index_price),
        long_short_ratio=long_short_ratio, raw_json=raw,
    )


def _archive_binance(store: Any, conn: Any, symbol: str, rec: dict[str, Any],
                     exchange: str, source_file: str | None, out: dict[str, int]) -> None:
    fetched_at = str(rec.get("fetched_at") or "")
    premium = rec.get("premium_index") or {}
    oi = rec.get("open_interest") or {}
    lsr_rows = rec.get("long_short_ratio") or []
    lsr = _f((lsr_rows[-1] if isinstance(lsr_rows, list) and lsr_rows else lsr_rows or {}).get("longShortRatio"))
    funding = _f(premium.get("lastFundingRate"))
    mark = _f(premium.get("markPrice"))
    index = _f(premium.get("indexPrice"))
    oi_native = _f(oi.get("openInterest"))
    oi_usd = _f(oi.get("openInterestValue"))
    if oi_usd is None and oi_native is not None and mark is not None:
        oi_usd = oi_native * mark
    hist = rec.get("open_interest_hist") or []
    oi_change = None
    if isinstance(hist, list) and len(hist) >= 2:
        first = _f(hist[0].get("sumOpenInterest")); last = _f(hist[-1].get("sumOpenInterest"))
        if first and last:
            oi_change = (last - first) / first * 100.0
    _legacy_write(
        store, fetched_at=fetched_at, exchange=exchange, symbol=symbol,
        funding_rate=funding, next_funding_time=str(premium.get("nextFundingTime") or "") or None,
        mark_price=mark, index_price=index, oi_native=oi_native, oi_usd=oi_usd,
        oi_change_pct=oi_change, long_short_ratio=lsr,
        crowding_label=str(rec.get("crowding_risk") or "") or None,
        raw=rec, source_file=source_file, out=out,
    )
    if _canonical_current(
        conn, fetched_at=fetched_at, exchange=exchange, symbol=symbol,
        instrument_id=rec.get("exchange_symbol"), funding_rate=funding,
        funding_interval_hours=8.0, oi_native=oi_native, oi_usd=oi_usd,
        mark_price=mark, index_price=index, long_short_ratio=lsr, raw=rec,
    ):
        out["canonical"] += 1
    # Binance's OI history is useful point-in-time data even though funding is absent.
    for row in hist if isinstance(hist, list) else []:
        ts = _iso_ms(row.get("timestamp"), fetched_at)
        native = _f(row.get("sumOpenInterest"))
        usd = _f(row.get("sumOpenInterestValue"))
        if mi.insert_derivative_snapshot(
            conn, provider_ts=ts, received_at=mi.utc_now_iso(), exchange=exchange,
            symbol=symbol, instrument_id=rec.get("exchange_symbol"), source_kind="oi_history_1h",
            oi_native=native, oi_usd=usd, raw_json=row,
        ):
            out["canonical"] += 1


def _archive_multi(store: Any, conn: Any, symbol: str, rec: dict[str, Any],
                   source_file: str | None, out: dict[str, int]) -> None:
    fetched_at = str(rec.get("fetched_at") or "")
    for venue, raw in (rec.get("exchanges") or {}).items():
        if not isinstance(raw, dict):
            continue
        funding = _f(raw.get("funding_rate"))
        oi_native = _f(raw.get("open_interest")) or _f(raw.get("open_interest_ccy"))
        oi_usd = (_f(raw.get("open_interest_value")) or _f(raw.get("open_interest_usd"))
                  or _f(raw.get("oiUsd")))
        mark = _f(raw.get("mark_price")) or _f(raw.get("last_price"))
        if str(venue).lower() != "mexc" and oi_usd is None and oi_native is not None and mark is not None:
            oi_usd = oi_native * mark
        if not any(v is not None for v in (funding, oi_native, oi_usd, mark)):
            continue
        # Legacy snapshot methods use their own connection. Release any
        # canonical write transaction from the previous venue first, otherwise
        # SQLite correctly serializes us behind our own 30-second busy timeout.
        conn.commit()
        _legacy_write(
            store, fetched_at=fetched_at, exchange=str(venue).lower(), symbol=symbol,
            funding_rate=funding, next_funding_time=None, mark_price=mark, index_price=None,
            oi_native=oi_native, oi_usd=oi_usd, oi_change_pct=None,
            long_short_ratio=None, crowding_label=None, raw=raw,
            source_file=source_file, out=out,
        )
        if _canonical_current(
            conn, fetched_at=fetched_at, exchange=str(venue).lower(), symbol=symbol,
            instrument_id=None, funding_rate=funding, funding_interval_hours=8.0,
            oi_native=oi_native, oi_usd=oi_usd, mark_price=mark,
            index_price=None, long_short_ratio=None, raw=raw,
        ):
            out["canonical"] += 1


def _archive_bybit_history(store: Any, conn: Any, symbol: str, rec: dict[str, Any],
                           source_file: str | None, out: dict[str, int]) -> None:
    fetched_at = str(rec.get("fetched_at") or "")
    ticker = rec.get("ticker") or {}
    funding = _f(ticker.get("fundingRate"))
    oi_native = _f(ticker.get("openInterest"))
    oi_usd = _f(ticker.get("openInterestValue"))
    mark = _f(ticker.get("markPrice")) or _f(ticker.get("lastPrice"))
    index = _f(ticker.get("indexPrice"))
    if oi_usd is None and oi_native is not None and mark is not None:
        oi_usd = oi_native * mark
    _legacy_write(
        store, fetched_at=fetched_at, exchange="bybit", symbol=symbol,
        funding_rate=funding, next_funding_time=str(ticker.get("nextFundingTime") or "") or None,
        mark_price=mark, index_price=index, oi_native=oi_native, oi_usd=oi_usd,
        oi_change_pct=_f(rec.get("oi_change_pct_24h")), long_short_ratio=None,
        crowding_label=None, raw=rec, source_file=source_file, out=out,
    )
    if _canonical_current(
        conn, fetched_at=fetched_at, exchange="bybit", symbol=symbol,
        instrument_id=rec.get("native_symbol"), funding_rate=funding,
        funding_interval_hours=8.0, oi_native=oi_native, oi_usd=oi_usd,
        mark_price=mark, index_price=index, long_short_ratio=None, raw=rec,
    ):
        out["canonical"] += 1
    for row in rec.get("open_interest_history") or []:
        if mi.insert_derivative_snapshot(
            conn, provider_ts=_iso_ms(row.get("timestamp"), fetched_at), received_at=mi.utc_now_iso(),
            exchange="bybit", symbol=symbol, instrument_id=rec.get("native_symbol"),
            source_kind="oi_history_1h", oi_native=_f(row.get("openInterest")), raw_json=row,
        ):
            out["canonical"] += 1
    for row in rec.get("funding_history") or []:
        if mi.insert_funding_event(
            conn, event_at=_iso_ms(row.get("fundingRateTimestamp"), fetched_at),
            received_at=mi.utc_now_iso(), exchange="bybit", symbol=symbol,
            funding_rate=_f(row.get("fundingRate")), funding_interval_hours=8.0,
            source_kind="settlement_history", raw_json=row,
        ):
            out["funding_events"] += 1


def archive_derivatives_records(store: Any, records: dict[str, Any] | None, *,
                                exchange: str, source_file: str | None = None) -> dict[str, int]:
    """Archive a collector's records. Never raises into the report path."""
    out = {"funding": 0, "oi": 0, "canonical": 0, "funding_events": 0, "errors": 0}
    if not records or store is None:
        return out
    conn = None
    try:
        store_path = Path(getattr(store, "db_path", "")).resolve()
        try:
            from src.config import load_config
            trading_path = Path(load_config().db_path).resolve()
        except Exception:
            trading_path = None
        # Production legacy rows stay in the trading DB through ``store``;
        # canonical high-cadence rows go to the independent intelligence DB.
        # A temp/test store remains self-contained.
        conn = mi.connect(None if trading_path and store_path == trading_path else store_path)
        for symbol, rec in records.items():
            if not isinstance(rec, dict) or rec.get("data_available") is False or rec.get("error"):
                continue
            if not rec.get("fetched_at"):
                continue
            if isinstance(rec.get("exchanges"), dict):
                _archive_multi(store, conn, symbol, rec, source_file, out)
            elif "ticker" in rec or "funding_history" in rec or "open_interest_history" in rec:
                _archive_bybit_history(store, conn, symbol, rec, source_file, out)
            else:
                _archive_binance(store, conn, symbol, rec, exchange.lower(), source_file, out)
        conn.commit()
    except Exception:
        out["errors"] += 1
        if conn is not None:
            try:
                conn.rollback()
            except Exception:
                pass
    finally:
        if conn is not None:
            conn.close()
    return out
