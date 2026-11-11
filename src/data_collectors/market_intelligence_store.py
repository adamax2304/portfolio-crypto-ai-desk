"""Canonical point-in-time storage for derivatives and on-chain intelligence.

The collectors in this project have deliberately different wire formats.  This
module is the narrow contract between those collectors and downstream paper
research: every observation keeps both the provider timestamp and the local
receipt timestamp, source provenance, and an explicit quality status.

Nothing in this module writes signals, outcomes, orders, or live state.
"""
from __future__ import annotations

import json
import os
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import median
from typing import Any, Iterable


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_symbol(symbol: str) -> str:
    value = str(symbol or "").upper().replace("-SWAP", "")
    for token in ("/", "-", "_", ":"):
        value = value.replace(token, "")
    return value


def base_symbol(symbol: str) -> str:
    value = str(symbol or "").upper().split(":", 1)[0]
    for quote in ("/USDT", "-USDT", "_USDT", "USDT", "/USD", "-USD", "USD"):
        if value.endswith(quote):
            return value[: -len(quote)]
    return value.split("/", 1)[0]


def normalize_funding_8h(rate: float | None, interval_hours: float | None) -> float | None:
    if rate is None:
        return None
    interval = float(interval_hours or 8.0)
    if interval <= 0:
        return None
    return float(rate) * 8.0 / interval


DDL = """
CREATE TABLE IF NOT EXISTS derivative_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider_ts TEXT NOT NULL,
    received_at TEXT NOT NULL,
    exchange TEXT NOT NULL,
    symbol TEXT NOT NULL,
    normalized_symbol TEXT NOT NULL,
    instrument_id TEXT,
    source_kind TEXT NOT NULL DEFAULT 'current',
    funding_rate REAL,
    funding_interval_hours REAL,
    funding_rate_8h REAL,
    predicted_funding_rate REAL,
    oi_native REAL,
    oi_usd REAL,
    mark_price REAL,
    index_price REAL,
    basis_bps REAL,
    long_short_ratio REAL,
    taker_buy_sell_ratio REAL,
    quality_status TEXT NOT NULL DEFAULT 'ok',
    raw_json TEXT,
    UNIQUE(exchange, normalized_symbol, provider_ts, source_kind)
);
CREATE INDEX IF NOT EXISTS idx_deriv_norm_ts
    ON derivative_snapshots(normalized_symbol, provider_ts);
CREATE INDEX IF NOT EXISTS idx_deriv_exchange_ts
    ON derivative_snapshots(exchange, provider_ts);
CREATE INDEX IF NOT EXISTS idx_deriv_norm_exchange_ts_id
    ON derivative_snapshots(normalized_symbol, exchange, provider_ts DESC, id DESC);

CREATE TABLE IF NOT EXISTS funding_rate_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_at TEXT NOT NULL,
    received_at TEXT NOT NULL,
    exchange TEXT NOT NULL,
    symbol TEXT NOT NULL,
    normalized_symbol TEXT NOT NULL,
    funding_rate REAL NOT NULL,
    funding_interval_hours REAL,
    funding_rate_8h REAL,
    source_kind TEXT NOT NULL DEFAULT 'settlement',
    raw_json TEXT,
    UNIQUE(exchange, normalized_symbol, event_at, source_kind)
);
CREATE INDEX IF NOT EXISTS idx_funding_event_norm_ts
    ON funding_rate_events(normalized_symbol, event_at);

CREATE TABLE IF NOT EXISTS liquidation_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exchange TEXT NOT NULL,
    event_id TEXT NOT NULL,
    event_at TEXT NOT NULL,
    received_at TEXT NOT NULL,
    symbol TEXT NOT NULL,
    normalized_symbol TEXT NOT NULL,
    side TEXT,
    price REAL,
    quantity REAL,
    notional_usd REAL,
    raw_json TEXT,
    UNIQUE(exchange, event_id)
);
CREATE INDEX IF NOT EXISTS idx_liq_norm_ts
    ON liquidation_events(normalized_symbol, event_at);

CREATE TABLE IF NOT EXISTS intelligence_source_health (
    source TEXT PRIMARY KEY,
    status TEXT NOT NULL,
    last_attempt_at TEXT,
    last_success_at TEXT,
    latest_provider_ts TEXT,
    consecutive_failures INTEGER NOT NULL DEFAULT 0,
    records_written INTEGER NOT NULL DEFAULT 0,
    latency_ms REAL,
    error TEXT,
    details_json TEXT,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS liquidity_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider_ts TEXT NOT NULL,
    received_at TEXT NOT NULL,
    exchange TEXT NOT NULL,
    symbol TEXT NOT NULL,
    normalized_symbol TEXT NOT NULL,
    best_bid REAL,
    best_ask REAL,
    mid_price REAL,
    spread_bps REAL,
    bid_depth_10bps_usd REAL,
    ask_depth_10bps_usd REAL,
    bid_depth_25bps_usd REAL,
    ask_depth_25bps_usd REAL,
    quality_status TEXT NOT NULL DEFAULT 'ok',
    raw_json TEXT,
    UNIQUE(exchange, normalized_symbol, provider_ts)
);
CREATE INDEX IF NOT EXISTS idx_liquidity_norm_ts
    ON liquidity_snapshots(normalized_symbol, provider_ts);
CREATE INDEX IF NOT EXISTS idx_liquidity_norm_exchange_ts_id
    ON liquidity_snapshots(normalized_symbol, exchange, provider_ts DESC, id DESC);

CREATE TABLE IF NOT EXISTS asset_contract_registry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_symbol TEXT NOT NULL,
    canonical_asset_id TEXT NOT NULL,
    chain TEXT NOT NULL,
    chain_id TEXT,
    contract_address TEXT NOT NULL,
    contract_type TEXT NOT NULL DEFAULT 'token',
    source_primary TEXT NOT NULL,
    source_secondary TEXT,
    verification_status TEXT NOT NULL DEFAULT 'candidate',
    verified_at TEXT,
    name TEXT,
    symbol_reported TEXT,
    ambiguity_reason TEXT,
    metadata_json TEXT,
    updated_at TEXT NOT NULL,
    UNIQUE(canonical_asset_id, chain, contract_address)
);
CREATE INDEX IF NOT EXISTS idx_contract_symbol
    ON asset_contract_registry(asset_symbol, verification_status);

CREATE TABLE IF NOT EXISTS onchain_metric_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider_ts TEXT NOT NULL,
    received_at TEXT NOT NULL,
    asset_symbol TEXT NOT NULL,
    canonical_asset_id TEXT,
    chain TEXT,
    metric_name TEXT NOT NULL,
    metric_value REAL,
    unit TEXT,
    provider TEXT NOT NULL,
    quality_status TEXT NOT NULL DEFAULT 'ok',
    raw_json TEXT,
    UNIQUE(provider, canonical_asset_id, chain, metric_name, provider_ts)
);
CREATE INDEX IF NOT EXISTS idx_onchain_metric_asset_ts
    ON onchain_metric_snapshots(asset_symbol, metric_name, provider_ts);

CREATE TABLE IF NOT EXISTS token_security_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider_ts TEXT NOT NULL,
    received_at TEXT NOT NULL,
    asset_symbol TEXT NOT NULL,
    canonical_asset_id TEXT NOT NULL,
    chain TEXT NOT NULL,
    contract_address TEXT NOT NULL,
    provider TEXT NOT NULL,
    is_honeypot INTEGER,
    sell_tax REAL,
    buy_tax REAL,
    is_mintable INTEGER,
    owner_change_balance INTEGER,
    is_blacklisted INTEGER,
    holder_count INTEGER,
    top10_holder_pct REAL,
    lp_locked_pct REAL,
    confidence TEXT NOT NULL DEFAULT 'unknown',
    quality_status TEXT NOT NULL DEFAULT 'ok',
    raw_json TEXT,
    UNIQUE(provider, chain, contract_address, provider_ts)
);
CREATE INDEX IF NOT EXISTS idx_token_sec_asset_ts
    ON token_security_snapshots(asset_symbol, provider_ts);

CREATE TABLE IF NOT EXISTS holder_concentration_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider_ts TEXT NOT NULL,
    received_at TEXT NOT NULL,
    asset_symbol TEXT NOT NULL,
    canonical_asset_id TEXT NOT NULL,
    chain TEXT NOT NULL,
    contract_address TEXT NOT NULL,
    provider TEXT NOT NULL,
    holder_count INTEGER,
    top1_pct REAL,
    top5_pct REAL,
    top10_pct REAL,
    top20_pct REAL,
    excluded_contracts INTEGER NOT NULL DEFAULT 0,
    quality_status TEXT NOT NULL DEFAULT 'ok',
    raw_json TEXT,
    UNIQUE(provider, chain, contract_address, provider_ts)
);

CREATE TABLE IF NOT EXISTS wallet_flow_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_at TEXT NOT NULL,
    received_at TEXT NOT NULL,
    chain TEXT NOT NULL,
    tx_hash TEXT NOT NULL,
    asset_symbol TEXT,
    contract_address TEXT,
    from_address TEXT,
    to_address TEXT,
    from_label TEXT,
    to_label TEXT,
    amount_native REAL,
    amount_usd REAL,
    provider TEXT NOT NULL,
    quality_status TEXT NOT NULL DEFAULT 'unverified',
    raw_json TEXT,
    UNIQUE(chain, tx_hash, contract_address, from_address, to_address)
);
"""


def ensure_tables(conn: sqlite3.Connection) -> None:
    conn.executescript(DDL)


def default_db_path() -> Path:
    """Dedicated WAL store for append-only market intelligence.

    The trading DB has long-running paper/report writers. Keeping high-cadence
    provider snapshots here prevents those transactions from delaying market
    context that must be available before a new paper-entry decision.
    """
    override = os.environ.get("MARKET_INTELLIGENCE_DB")
    if override:
        return Path(override).expanduser().resolve()
    from src.config import load_config

    return (Path(load_config().root) / "data" / "intelligence" /
            "market_intelligence.sqlite").resolve()


def connect(db_path: str | Path | None = None, *, ensure: bool = True) -> sqlite3.Connection:
    if db_path is None:
        db_path = default_db_path()
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path, timeout=30.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=30000")
    if ensure:
        ensure_tables(conn)
    return conn


def _json(value: Any, limit: int = 16000) -> str | None:
    if value is None:
        return None
    return json.dumps(value, default=str, separators=(",", ":"))[:limit]


def insert_derivative_snapshot(conn: sqlite3.Connection, **row: Any) -> bool:
    metrics = ("funding_rate", "predicted_funding_rate", "oi_native", "oi_usd", "mark_price", "index_price")
    if not any(row.get(key) is not None for key in metrics):
        return False
    interval = row.get("funding_interval_hours")
    rate = row.get("funding_rate")
    values = {
        "provider_ts": row.get("provider_ts") or utc_now_iso(),
        "received_at": row.get("received_at") or utc_now_iso(),
        "exchange": str(row.get("exchange") or "unknown").lower(),
        "symbol": str(row.get("symbol") or ""),
        "normalized_symbol": row.get("normalized_symbol") or normalize_symbol(row.get("symbol") or ""),
        "instrument_id": row.get("instrument_id"),
        "source_kind": row.get("source_kind") or "current",
        "funding_rate": rate,
        "funding_interval_hours": interval,
        "funding_rate_8h": row.get("funding_rate_8h", normalize_funding_8h(rate, interval)),
        "predicted_funding_rate": row.get("predicted_funding_rate"),
        "oi_native": row.get("oi_native"),
        "oi_usd": row.get("oi_usd"),
        "mark_price": row.get("mark_price"),
        "index_price": row.get("index_price"),
        "basis_bps": row.get("basis_bps"),
        "long_short_ratio": row.get("long_short_ratio"),
        "taker_buy_sell_ratio": row.get("taker_buy_sell_ratio"),
        "quality_status": row.get("quality_status") or "ok",
        "raw_json": _json(row.get("raw_json")),
    }
    columns = tuple(values)
    cur = conn.execute(
        f"INSERT OR IGNORE INTO derivative_snapshots({','.join(columns)}) VALUES({','.join('?' for _ in columns)})",
        tuple(values[c] for c in columns),
    )
    return cur.rowcount > 0


def insert_liquidity_snapshot(conn: sqlite3.Connection, **row: Any) -> bool:
    """Append a public order-book observation with an explicit column list."""
    best_bid, best_ask = row.get("best_bid"), row.get("best_ask")
    if best_bid is None or best_ask is None:
        return False
    values = {
        "provider_ts": row.get("provider_ts") or utc_now_iso(),
        "received_at": row.get("received_at") or utc_now_iso(),
        "exchange": str(row.get("exchange") or "unknown").lower(),
        "symbol": str(row.get("symbol") or ""),
        "normalized_symbol": row.get("normalized_symbol") or normalize_symbol(row.get("symbol") or ""),
        "best_bid": float(best_bid), "best_ask": float(best_ask),
        "mid_price": row.get("mid_price"), "spread_bps": row.get("spread_bps"),
        "bid_depth_10bps_usd": row.get("bid_depth_10bps_usd"),
        "ask_depth_10bps_usd": row.get("ask_depth_10bps_usd"),
        "bid_depth_25bps_usd": row.get("bid_depth_25bps_usd"),
        "ask_depth_25bps_usd": row.get("ask_depth_25bps_usd"),
        "quality_status": row.get("quality_status") or "ok",
        "raw_json": _json(row.get("raw_json")),
    }
    columns = tuple(values)
    cur = conn.execute(
        f"INSERT OR IGNORE INTO liquidity_snapshots({','.join(columns)}) VALUES({','.join('?' for _ in columns)})",
        tuple(values[column] for column in columns),
    )
    return cur.rowcount > 0


def insert_funding_event(conn: sqlite3.Connection, **row: Any) -> bool:
    rate = row.get("funding_rate")
    if rate is None:
        return False
    interval = row.get("funding_interval_hours")
    values = (
        row.get("event_at") or utc_now_iso(), row.get("received_at") or utc_now_iso(),
        str(row.get("exchange") or "unknown").lower(), str(row.get("symbol") or ""),
        row.get("normalized_symbol") or normalize_symbol(row.get("symbol") or ""), float(rate),
        interval, row.get("funding_rate_8h", normalize_funding_8h(float(rate), interval)),
        row.get("source_kind") or "settlement", _json(row.get("raw_json")),
    )
    cur = conn.execute(
        "INSERT OR IGNORE INTO funding_rate_events(event_at,received_at,exchange,symbol,"
        "normalized_symbol,funding_rate,funding_interval_hours,funding_rate_8h,source_kind,raw_json) "
        "VALUES(?,?,?,?,?,?,?,?,?,?)", values,
    )
    return cur.rowcount > 0


def insert_liquidation_event(conn: sqlite3.Connection, **row: Any) -> bool:
    price, quantity = row.get("price"), row.get("quantity")
    notional = row.get("notional_usd")
    if notional is None and price is not None and quantity is not None:
        notional = float(price) * float(quantity)
    values = (
        str(row.get("exchange") or "unknown").lower(), str(row.get("event_id") or ""),
        row.get("event_at") or utc_now_iso(), row.get("received_at") or utc_now_iso(),
        str(row.get("symbol") or ""), row.get("normalized_symbol") or normalize_symbol(row.get("symbol") or ""),
        row.get("side"), price, quantity, notional, _json(row.get("raw_json")),
    )
    if not values[1] or not values[4]:
        return False
    cur = conn.execute(
        "INSERT OR IGNORE INTO liquidation_events(exchange,event_id,event_at,received_at,symbol,"
        "normalized_symbol,side,price,quantity,notional_usd,raw_json) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
        values,
    )
    return cur.rowcount > 0


def record_source_health(conn: sqlite3.Connection, source: str, *, status: str,
                         success: bool, records_written: int = 0,
                         latest_provider_ts: str | None = None, latency_ms: float | None = None,
                         error: str | None = None, details: Any = None) -> None:
    now = utc_now_iso()
    conn.execute(
        "INSERT INTO intelligence_source_health(source,status,last_attempt_at,last_success_at,"
        "latest_provider_ts,consecutive_failures,records_written,latency_ms,error,details_json,updated_at) "
        "VALUES(?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT(source) DO UPDATE SET "
        "status=excluded.status,last_attempt_at=excluded.last_attempt_at,"
        "last_success_at=CASE WHEN ? THEN excluded.last_success_at ELSE intelligence_source_health.last_success_at END,"
        "latest_provider_ts=COALESCE(excluded.latest_provider_ts,intelligence_source_health.latest_provider_ts),"
        "consecutive_failures=CASE WHEN ? THEN 0 ELSE intelligence_source_health.consecutive_failures+1 END,"
        "records_written=excluded.records_written,latency_ms=excluded.latency_ms,error=excluded.error,"
        "details_json=excluded.details_json,updated_at=excluded.updated_at",
        (source, status, now, now if success else None, latest_provider_ts, 0 if success else 1,
         records_written, latency_ms, error, _json(details), now, int(success), int(success)),
    )


def _parse_ts(value: str | datetime | None) -> datetime | None:
    if isinstance(value, datetime):
        dt = value
    else:
        try:
            dt = datetime.fromisoformat(str(value or "").replace("Z", "+00:00"))
        except (TypeError, ValueError):
            return None
    return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt.astimezone(timezone.utc)


def latest_derivatives_context(conn: sqlite3.Connection, symbol: str, *,
                               as_of: datetime | str | None = None,
                               max_age_minutes: int = 30) -> dict[str, Any]:
    """Aggregate the latest point-in-time row per venue without lookahead."""
    now = _parse_ts(as_of) or datetime.now(timezone.utc)
    norm = normalize_symbol(symbol)
    fresh_after = (now - timedelta(minutes=max_age_minutes)).isoformat()
    rows = conn.execute(
        "SELECT * FROM (SELECT d.*, ROW_NUMBER() OVER (PARTITION BY exchange ORDER BY provider_ts DESC,id DESC) rn "
        "FROM derivative_snapshots d WHERE normalized_symbol=? AND provider_ts>=? AND provider_ts<=?) WHERE rn=1",
        (norm, fresh_after, now.isoformat()),
    ).fetchall()
    fresh = []
    for raw in rows:
        row = dict(raw)
        ts = _parse_ts(row.get("provider_ts"))
        if ts and timedelta(0) <= now - ts <= timedelta(minutes=max_age_minutes):
            fresh.append(row)
    funding = [float(r["funding_rate_8h"]) for r in fresh if r.get("funding_rate_8h") is not None]
    oi = [float(r["oi_usd"]) for r in fresh if r.get("oi_usd") is not None and float(r["oi_usd"]) > 0]
    mark = [float(r["mark_price"]) for r in fresh if r.get("mark_price") is not None]
    current_oi = sum(oi) if oi else None
    funding_med = median(funding) if funding else None
    funding_state = "unknown"
    if funding_med is not None:
        funding_state = ("extreme_long" if funding_med >= 0.001 else
                         "elevated_long" if funding_med >= 0.0005 else
                         "short_crowded" if funding_med <= -0.0005 else "normal")

    target = now - timedelta(hours=24)
    oi_changes, price_changes = [], []
    for row in fresh:
        old = conn.execute(
            "SELECT oi_usd,mark_price,provider_ts FROM derivative_snapshots WHERE normalized_symbol=? "
            "AND exchange=? AND provider_ts<=? ORDER BY provider_ts DESC,id DESC LIMIT 1",
            (norm, row["exchange"], target.isoformat()),
        ).fetchone()
        if not old:
            continue
        old_ts = _parse_ts(old[2])
        if old_ts is None or target - old_ts > timedelta(hours=6):
            continue
        if row.get("oi_usd") is not None and old[0] is not None and float(old[0]) > 0:
            oi_changes.append((float(row["oi_usd"]) / float(old[0])) - 1.0)
        if row.get("mark_price") is not None and old[1] is not None and float(old[1]) > 0:
            price_changes.append((float(row["mark_price"]) / float(old[1])) - 1.0)
    oi_change = median(oi_changes) if oi_changes else None
    mark_med = median(mark) if mark else None
    price_change = median(price_changes) if price_changes else None
    regime = "unknown"
    if oi_change is not None and price_change is not None:
        if oi_change >= 0.05 and price_change > 0.01:
            regime = "fresh_longs"
        elif oi_change >= 0.05 and price_change < -0.01:
            regime = "fresh_shorts"
        elif oi_change <= -0.05:
            regime = "deleveraging"
        else:
            regime = "neutral"
    latest_ts = max((r.get("provider_ts") for r in fresh), default=None)
    return {
        "symbol": symbol, "as_of": now.isoformat(), "status": "ok" if fresh else "unknown",
        "venue_count": len(fresh), "venues": sorted(r["exchange"] for r in fresh),
        "latest_provider_ts": latest_ts, "funding_rate_8h": funding_med,
        "funding_state": funding_state, "oi_usd": current_oi, "oi_change_24h": oi_change,
        "mark_price": mark_med, "price_change_24h": price_change, "oi_price_regime": regime,
        "oi_change_venue_count": len(oi_changes), "price_change_venue_count": len(price_changes),
        "cross_venue_funding_spread": (max(funding) - min(funding)) if len(funding) >= 2 else None,
    }


def latest_liquidity_context(conn: sqlite3.Connection, symbol: str, *,
                             as_of: datetime | str | None = None,
                             max_age_minutes: int = 10) -> dict[str, Any]:
    """Return fresh per-venue BBO/depth observations without looking ahead.

    This is observational context. Callers decide independently whether it is
    ready to become a routing rule; stale or missing books are never reported
    as a good liquidity signal.
    """
    now = _parse_ts(as_of) or datetime.now(timezone.utc)
    norm = normalize_symbol(symbol)
    fresh_after = (now - timedelta(minutes=max_age_minutes)).isoformat()
    rows = conn.execute(
        "SELECT * FROM (SELECT l.*, ROW_NUMBER() OVER (PARTITION BY exchange ORDER BY provider_ts DESC,id DESC) rn "
        "FROM liquidity_snapshots l WHERE normalized_symbol=? AND provider_ts>=? AND provider_ts<=?) WHERE rn=1",
        (norm, fresh_after, now.isoformat()),
    ).fetchall()
    fresh = []
    for raw in rows:
        row = dict(raw)
        ts = _parse_ts(row.get("provider_ts"))
        if ts and timedelta(0) <= now - ts <= timedelta(minutes=max_age_minutes):
            fresh.append(row)
    def _med(key: str) -> float | None:
        values = [float(row[key]) for row in fresh if row.get(key) is not None]
        return median(values) if values else None
    return {
        "symbol": symbol, "as_of": now.isoformat(),
        "status": "ok" if fresh else "unknown",
        "venue_count": len(fresh), "venues": sorted(str(row["exchange"]) for row in fresh),
        "latest_provider_ts": max((row.get("provider_ts") for row in fresh), default=None),
        "spread_bps": _med("spread_bps"),
        "bid_depth_10bps_usd": _med("bid_depth_10bps_usd"),
        "ask_depth_10bps_usd": _med("ask_depth_10bps_usd"),
        "bid_depth_25bps_usd": _med("bid_depth_25bps_usd"),
        "ask_depth_25bps_usd": _med("ask_depth_25bps_usd"),
    }


def actual_funding_cost(conn: sqlite3.Connection, *, symbol: str, exchange: str,
                        direction: str, notional_usdt: float,
                        entry_at: str | datetime, exit_at: str | datetime) -> dict[str, Any]:
    start, end = _parse_ts(entry_at), _parse_ts(exit_at)
    if start is None or end is None or end < start:
        return {"known": False, "funding_usdt": None, "events": 0, "source": "invalid_window"}
    rows = conn.execute(
        "SELECT funding_rate,event_at FROM funding_rate_events WHERE exchange=? AND normalized_symbol=? "
        "AND event_at>? AND event_at<=? ORDER BY event_at",
        (exchange.lower(), normalize_symbol(symbol), start.isoformat(), end.isoformat()),
    ).fetchall()
    if not rows:
        return {"known": False, "funding_usdt": None, "events": 0, "source": "no_actual_events"}
    side = 1.0 if str(direction).lower() != "short" else -1.0
    cost = sum(float(r[0]) * float(notional_usdt) * side for r in rows)
    return {"known": True, "funding_usdt": cost, "events": len(rows),
            "source": f"actual_{exchange.lower()}_funding_events",
            "first_event_at": rows[0][1], "last_event_at": rows[-1][1]}


def verified_contract(conn: sqlite3.Connection, asset_symbol: str) -> dict[str, Any] | None:
    rows = conn.execute(
        "SELECT * FROM asset_contract_registry WHERE asset_symbol=? AND verification_status='verified' "
        "ORDER BY verified_at DESC,id DESC", (base_symbol(asset_symbol),),
    ).fetchall()
    return dict(rows[0]) if len(rows) == 1 else None


def upsert_contract(conn: sqlite3.Connection, **row: Any) -> None:
    now = utc_now_iso()
    values = (
        base_symbol(row.get("asset_symbol") or ""), str(row.get("canonical_asset_id") or ""),
        str(row.get("chain") or ""), str(row.get("chain_id") or "") or None,
        str(row.get("contract_address") or "native").lower(), row.get("contract_type") or "token",
        row.get("source_primary") or "unknown", row.get("source_secondary"),
        row.get("verification_status") or "candidate", row.get("verified_at"), row.get("name"),
        row.get("symbol_reported"), row.get("ambiguity_reason"), _json(row.get("metadata_json")), now,
    )
    conn.execute(
        "INSERT INTO asset_contract_registry(asset_symbol,canonical_asset_id,chain,chain_id,contract_address,"
        "contract_type,source_primary,source_secondary,verification_status,verified_at,name,symbol_reported,"
        "ambiguity_reason,metadata_json,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) "
        "ON CONFLICT(canonical_asset_id,chain,contract_address) DO UPDATE SET "
        "asset_symbol=excluded.asset_symbol,chain_id=excluded.chain_id,source_secondary=excluded.source_secondary,"
        "verification_status=excluded.verification_status,verified_at=excluded.verified_at,name=excluded.name,"
        "symbol_reported=excluded.symbol_reported,ambiguity_reason=excluded.ambiguity_reason,"
        "metadata_json=excluded.metadata_json,updated_at=excluded.updated_at", values,
    )


def insert_onchain_metric(conn: sqlite3.Connection, **row: Any) -> bool:
    values = (
        row.get("provider_ts") or utc_now_iso(), row.get("received_at") or utc_now_iso(),
        base_symbol(row.get("asset_symbol") or ""), row.get("canonical_asset_id"), row.get("chain"),
        str(row.get("metric_name") or ""), row.get("metric_value"), row.get("unit"),
        str(row.get("provider") or "unknown"), row.get("quality_status") or "ok",
        _json(row.get("raw_json")),
    )
    if not values[5] or values[6] is None:
        return False
    cur = conn.execute(
        "INSERT OR IGNORE INTO onchain_metric_snapshots(provider_ts,received_at,asset_symbol,canonical_asset_id,"
        "chain,metric_name,metric_value,unit,provider,quality_status,raw_json) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
        values,
    )
    return cur.rowcount > 0


def insert_token_security(conn: sqlite3.Connection, **row: Any) -> bool:
    values = (
        row.get("provider_ts") or utc_now_iso(), row.get("received_at") or utc_now_iso(),
        base_symbol(row.get("asset_symbol") or ""), str(row.get("canonical_asset_id") or ""),
        str(row.get("chain") or ""), str(row.get("contract_address") or "").lower(),
        str(row.get("provider") or "unknown"), row.get("is_honeypot"), row.get("sell_tax"),
        row.get("buy_tax"), row.get("is_mintable"), row.get("owner_change_balance"),
        row.get("is_blacklisted"), row.get("holder_count"), row.get("top10_holder_pct"),
        row.get("lp_locked_pct"), row.get("confidence") or "unknown",
        row.get("quality_status") or "ok", _json(row.get("raw_json")),
    )
    if not values[3] or not values[4] or not values[5]:
        return False
    cur = conn.execute(
        "INSERT OR IGNORE INTO token_security_snapshots(provider_ts,received_at,asset_symbol,canonical_asset_id,"
        "chain,contract_address,provider,is_honeypot,sell_tax,buy_tax,is_mintable,owner_change_balance,"
        "is_blacklisted,holder_count,top10_holder_pct,lp_locked_pct,confidence,quality_status,raw_json) "
        "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", values,
    )
    return cur.rowcount > 0


def insert_holder_concentration(conn: sqlite3.Connection, **row: Any) -> bool:
    values = (
        row.get("provider_ts") or utc_now_iso(), row.get("received_at") or utc_now_iso(),
        base_symbol(row.get("asset_symbol") or ""), str(row.get("canonical_asset_id") or ""),
        str(row.get("chain") or ""), str(row.get("contract_address") or "").lower(),
        str(row.get("provider") or "unknown"), row.get("holder_count"), row.get("top1_pct"),
        row.get("top5_pct"), row.get("top10_pct"), row.get("top20_pct"),
        int(bool(row.get("excluded_contracts"))), row.get("quality_status") or "ok",
        _json(row.get("raw_json")),
    )
    if not values[3] or not values[4] or not values[5]:
        return False
    cur = conn.execute(
        "INSERT OR IGNORE INTO holder_concentration_snapshots(provider_ts,received_at,asset_symbol,"
        "canonical_asset_id,chain,contract_address,provider,holder_count,top1_pct,top5_pct,top10_pct,"
        "top20_pct,excluded_contracts,quality_status,raw_json) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        values,
    )
    return cur.rowcount > 0


def latest_onchain_context(conn: sqlite3.Connection, symbol: str, *,
                           as_of: datetime | str | None = None) -> dict[str, Any]:
    now = _parse_ts(as_of) or datetime.now(timezone.utc)
    base = base_symbol(symbol)
    contract = verified_contract(conn, base)
    out = {"asset_symbol": base, "status": "unknown", "contract_verified": bool(contract),
           "missing_reason": "no_unique_verified_contract" if not contract else "no_fresh_security"}
    security_rows = []
    if contract and contract.get("contract_type") != "native":
        security_rows = conn.execute(
            "SELECT * FROM (SELECT s.*,ROW_NUMBER() OVER(PARTITION BY provider ORDER BY provider_ts DESC,id DESC) rn "
            "FROM token_security_snapshots s WHERE canonical_asset_id=? AND chain=? "
            "AND contract_address=? AND provider_ts<=?) WHERE rn=1",
            (contract["canonical_asset_id"], contract["chain"], contract["contract_address"], now.isoformat()),
        ).fetchall()
    fresh_security = []
    for security in security_rows:
        sec = dict(security); ts = _parse_ts(sec.get("provider_ts"))
        age = (now - ts).total_seconds() if ts else None
        if age is not None and 0 <= age <= 36 * 3600:
            sec["security_age_sec"] = age
            fresh_security.append(sec)
    if fresh_security:
        def _max_field(name: str):
            values = [r[name] for r in fresh_security if r.get(name) is not None]
            return max(values) if values else None
        out.update({
            "status": "ok", "missing_reason": None,
            "security_age_sec": min(r["security_age_sec"] for r in fresh_security),
            "security_provider_count": len(fresh_security),
            "security_providers": sorted(r["provider"] for r in fresh_security),
            "honeypot_confirmations": sum(1 for r in fresh_security if bool(r.get("is_honeypot"))),
            "honeypot_clear_confirmations": sum(1 for r in fresh_security if r.get("is_honeypot") == 0),
            "blacklist_confirmations": sum(1 for r in fresh_security if bool(r.get("is_blacklisted"))),
            "extreme_sell_tax_confirmations": sum(1 for r in fresh_security
                                                  if r.get("sell_tax") is not None and float(r["sell_tax"]) >= 25.0),
            "is_honeypot": _max_field("is_honeypot"), "sell_tax": _max_field("sell_tax"),
            "buy_tax": _max_field("buy_tax"), "is_mintable": _max_field("is_mintable"),
            "owner_change_balance": _max_field("owner_change_balance"),
            "is_blacklisted": _max_field("is_blacklisted"),
            "holder_count": _max_field("holder_count"), "top10_holder_pct": _max_field("top10_holder_pct"),
            "security_rows": fresh_security,
        })
    metrics = conn.execute(
        "SELECT * FROM (SELECT m.*,ROW_NUMBER() OVER(PARTITION BY metric_name ORDER BY provider_ts DESC,id DESC) rn "
        "FROM onchain_metric_snapshots m WHERE asset_symbol=? AND provider_ts<=?) WHERE rn=1",
        (base, now.isoformat()),
    ).fetchall()
    out["metrics"] = {r["metric_name"]: r["metric_value"] for r in metrics}
    out["contract"] = contract
    if contract and contract.get("contract_type") == "native" and out["metrics"]:
        out.update({"status": "ok", "missing_reason": None})
    return out
