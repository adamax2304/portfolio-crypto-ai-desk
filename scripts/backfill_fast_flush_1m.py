"""Backfill Binance and Bybit 1m candles around recorded liquidation episodes.

The event-window design retains six hours before and three hours after every
candidate while avoiding a full-market minute archive. It is resumable and
never writes a trading database.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from src.data_collectors.fast_flush_research_store import connect, insert_rows


ROOT = Path(__file__).resolve().parents[1]
INTELLIGENCE_DB = ROOT / "data" / "intelligence" / "market_intelligence.sqlite"
TRADING_DB = ROOT / "db" / "crypto_ai_desk.sqlite"


def _dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def _canon(value: str) -> str:
    symbol = value.upper().replace("_", "/").replace("-", "/")
    if "/" not in symbol and symbol.endswith("USDT"):
        symbol = symbol[:-4] + "/USDT"
    return symbol


def _native(symbol: str) -> str:
    return _canon(symbol).replace("/", "")


def _json(url: str, attempts: int = 4) -> Any:
    error: Exception | None = None
    for attempt in range(attempts):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "crypto-ai-desk-research/1"})
            with urllib.request.urlopen(request, timeout=20) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception as exc:  # network boundary
            error = exc
            # Public endpoints may answer 429/418 after a burst. Back off
            # aggressively so an offline backfill cannot disturb live polling.
            text = str(exc)
            delay = 15.0 * (attempt + 1) if "429" in text or "418" in text else 0.6 * (attempt + 1)
            time.sleep(delay)
    raise RuntimeError(f"request failed after {attempts} attempts: {error}")


def _fetch_binance(symbol: str, start_ms: int, end_ms: int) -> list[tuple]:
    query = urllib.parse.urlencode({"symbol": _native(symbol), "interval": "1m",
                                    "startTime": start_ms, "endTime": end_ms, "limit": 1500})
    data = _json("https://fapi.binance.com/fapi/v1/klines?" + query)
    if isinstance(data, dict):
        raise RuntimeError(str(data.get("msg") or data))
    return [(int(row[0]), float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]))
            for row in data]


def _fetch_bybit(symbol: str, start_ms: int, end_ms: int) -> list[tuple]:
    query = urllib.parse.urlencode({"category": "linear", "symbol": _native(symbol),
                                    "interval": "1", "start": start_ms, "end": end_ms, "limit": 1000})
    data = _json("https://api.bybit.com/v5/market/kline?" + query)
    if int(data.get("retCode", -1)) != 0:
        raise RuntimeError(str(data.get("retMsg") or data))
    rows = data.get("result", {}).get("list", [])
    return sorted((int(row[0]), float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]))
                  for row in rows)


def _source_symbols() -> list[str]:
    conn = sqlite3.connect(TRADING_DB)
    try:
        return [_canon(row[0]) for row in conn.execute(
            "SELECT DISTINCT symbol FROM crypto_liquidity_sweep_v1_shadow_outcomes ORDER BY symbol"
        )]
    finally:
        conn.close()


def liquidation_candidates(*, minimum_notional: float, minimum_percentile: float,
                           limit_per_symbol: int) -> list[dict[str, Any]]:
    """Build point-in-time five-minute episodes independently of price outcomes."""
    conn = sqlite3.connect(INTELLIGENCE_DB)
    conn.row_factory = sqlite3.Row
    candidates: list[dict[str, Any]] = []
    try:
        for symbol in _source_symbols():
            native = _native(symbol)
            rows = conn.execute(
                "SELECT event_at,notional_usd FROM liquidation_events "
                "WHERE normalized_symbol=? AND side='SELL' ORDER BY event_at", (native,),
            ).fetchall()
            buckets: dict[datetime, float] = {}
            for row in rows:
                at = _dt(row["event_at"])
                bucket = at.replace(minute=at.minute - at.minute % 5, second=0, microsecond=0)
                buckets[bucket] = buckets.get(bucket, 0.0) + float(row["notional_usd"] or 0.0)
            values = sorted(buckets.values())
            if not values:
                continue
            selected = []
            for at, notional in buckets.items():
                percentile = sum(value <= notional for value in values) / len(values)
                if notional >= minimum_notional and percentile >= minimum_percentile:
                    selected.append((at, notional, percentile))
            selected.sort(key=lambda item: item[1], reverse=True)
            for at, notional, percentile in sorted(selected[:limit_per_symbol]):
                event_id = "ffevt_" + hashlib.sha256(f"{native}|{at.isoformat()}".encode()).hexdigest()[:20]
                candidates.append({"event_id": event_id, "symbol": symbol, "event_at": at,
                                   "liquidation_notional_usd": notional,
                                   "liquidation_percentile": percentile,
                                   "source": "liquidation_tape_5m"})
    finally:
        conn.close()
    return sorted(candidates, key=lambda item: item["event_at"])


def _merge_windows(events: list[dict[str, Any]], before_hours: float, after_hours: float) -> list[tuple[str, int, int]]:
    by_symbol: dict[str, list[tuple[int, int]]] = {}
    for event in events:
        at = event["event_at"]
        start = int((at - timedelta(hours=before_hours)).timestamp() * 1000)
        end = int((at + timedelta(hours=after_hours)).timestamp() * 1000)
        by_symbol.setdefault(event["symbol"], []).append((start, end))
    merged: list[tuple[str, int, int]] = []
    for symbol, windows in by_symbol.items():
        current_start, current_end = sorted(windows)[0]
        for start, end in sorted(windows)[1:]:
            if start <= current_end + 60_000:
                current_end = max(current_end, end)
            else:
                merged.append((symbol, current_start, current_end))
                current_start, current_end = start, end
        merged.append((symbol, current_start, current_end))
    return merged


def _pages(exchange: str, symbol: str, start_ms: int, end_ms: int) -> tuple[str, str, list[tuple], str | None]:
    fetch = _fetch_binance if exchange == "binance" else _fetch_bybit
    limit_minutes = 1499 if exchange == "binance" else 999
    cursor, rows = start_ms, []
    try:
        while cursor <= end_ms:
            page_end = min(end_ms, cursor + limit_minutes * 60_000)
            batch = fetch(symbol, cursor, page_end)
            rows.extend(batch)
            if not batch:
                break
            newest = max(row[0] for row in batch)
            if newest < cursor:
                break
            cursor = newest + 60_000
            time.sleep(0.20 if exchange == "binance" else 0.08)
        return exchange, symbol, rows, None
    except Exception as exc:
        return exchange, symbol, rows, f"{type(exc).__name__}: {exc}"


def run(*, minimum_notional: float = 20_000.0, minimum_percentile: float = 0.50,
        limit_per_symbol: int = 80, before_hours: float = 6.0,
        after_hours: float = 3.0, workers: int = 2) -> dict[str, Any]:
    events = liquidation_candidates(minimum_notional=minimum_notional,
                                    minimum_percentile=minimum_percentile,
                                    limit_per_symbol=limit_per_symbol)
    windows = _merge_windows(events, before_hours, after_hours)
    store = connect()
    for event in events:
        store.execute(
            "INSERT OR REPLACE INTO candidate_events VALUES(?,?,?,?,?,?,?)",
            (event["event_id"], event["symbol"], event["event_at"].isoformat(),
             event["liquidation_notional_usd"], event["liquidation_percentile"], event["source"],
             json.dumps({"before_hours": before_hours, "after_hours": after_hours})),
        )
    store.commit()
    added, failures = 0, []
    tasks = [(exchange, symbol, start, end) for symbol, start, end in windows
             for exchange in ("binance", "bybit")]
    try:
        with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
            futures = [pool.submit(_pages, *task) for task in tasks]
            for index, future in enumerate(as_completed(futures), start=1):
                exchange, symbol, rows, error = future.result()
                if rows:
                    added += insert_rows(store, exchange, symbol, rows)
                    store.commit()
                if error:
                    failures.append({"exchange": exchange, "symbol": symbol, "error": error})
                if index % 25 == 0:
                    print(f"completed {index}/{len(tasks)} tasks; added={added}; failures={len(failures)}", flush=True)
        counts = dict(store.execute("SELECT exchange,COUNT(*) FROM ohlcv_1m GROUP BY exchange").fetchall())
        result = {"events": len(events), "windows": len(windows), "tasks": len(tasks),
                  "rows_added": added, "rows_by_exchange": counts, "failures": failures}
        report = ROOT / "research_labs" / "fast_flush_reclaim_v3" / "backfill_summary.json"
        report.write_text(json.dumps(result, indent=2), encoding="utf-8")
        return result
    finally:
        store.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--minimum-notional", type=float, default=20_000.0)
    parser.add_argument("--minimum-percentile", type=float, default=0.50)
    parser.add_argument("--limit-per-symbol", type=int, default=80)
    parser.add_argument("--before-hours", type=float, default=6.0)
    parser.add_argument("--after-hours", type=float, default=3.0)
    parser.add_argument("--workers", type=int, default=2)
    args = parser.parse_args()
    print(json.dumps(run(**vars(args)), indent=2, default=str))


if __name__ == "__main__":
    main()
