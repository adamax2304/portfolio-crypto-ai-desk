"""Append-only point-in-time storage for optional market/risk contexts.

This database is deliberately separate from the trading SQLite. Collectors can
poll frequently without contending with signal/outcome writers. Nothing in this
module writes signals, paper ledgers, or live state.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
from pathlib import Path
from typing import Any

from src.data_collectors import market_intelligence_store as mi


DDL = """
CREATE TABLE IF NOT EXISTS token_unlock_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source TEXT NOT NULL,
  source_event_id TEXT NOT NULL,
  observed_at TEXT NOT NULL,
  asset_symbol TEXT NOT NULL,
  unlock_at TEXT NOT NULL,
  unlock_tokens REAL,
  unlock_usd REAL,
  pct_circulating REAL,
  avg_daily_volume_usd REAL,
  unlock_adv_days REAL,
  recipient_type TEXT,
  unlock_type TEXT,
  quality_status TEXT NOT NULL DEFAULT 'ok',
  content_hash TEXT NOT NULL,
  raw_json TEXT,
  UNIQUE(source, source_event_id, content_hash)
);
CREATE INDEX IF NOT EXISTS idx_unlock_asset_time
  ON token_unlock_events(asset_symbol, unlock_at, observed_at);

CREATE TABLE IF NOT EXISTS stablecoin_peg_snapshots (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  provider_ts TEXT NOT NULL,
  received_at TEXT NOT NULL,
  exchange TEXT NOT NULL,
  stablecoin TEXT NOT NULL,
  quote_currency TEXT NOT NULL DEFAULT 'USD',
  bid REAL,
  ask REAL,
  mid REAL,
  quality_status TEXT NOT NULL DEFAULT 'ok',
  raw_json TEXT,
  UNIQUE(exchange, stablecoin, provider_ts)
);
CREATE INDEX IF NOT EXISTS idx_peg_asset_time
  ON stablecoin_peg_snapshots(stablecoin, provider_ts);

CREATE TABLE IF NOT EXISTS cross_exchange_quote_snapshots (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  provider_ts TEXT NOT NULL,
  received_at TEXT NOT NULL,
  exchange TEXT NOT NULL,
  symbol TEXT NOT NULL,
  bid REAL,
  ask REAL,
  mid REAL,
  mark_price REAL,
  index_price REAL,
  quote_volume_24h REAL,
  quality_status TEXT NOT NULL DEFAULT 'ok',
  raw_json TEXT,
  UNIQUE(exchange, symbol, provider_ts)
);
CREATE INDEX IF NOT EXISTS idx_xquote_symbol_time
  ON cross_exchange_quote_snapshots(symbol, provider_ts);

CREATE TABLE IF NOT EXISTS options_context_snapshots (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  provider_ts TEXT NOT NULL,
  received_at TEXT NOT NULL,
  asset_class TEXT NOT NULL,
  underlying TEXT NOT NULL,
  source TEXT NOT NULL,
  context_type TEXT NOT NULL,
  spot_price REAL,
  iv30 REAL,
  rv30 REAL,
  iv_rank REAL,
  vrp REAL,
  net_gex REAL,
  gamma_flip REAL,
  call_wall REAL,
  put_wall REAL,
  zero_dte_share REAL,
  oi_as_of TEXT,
  quality_status TEXT NOT NULL DEFAULT 'unknown',
  raw_json TEXT,
  UNIQUE(source, underlying, context_type, provider_ts)
);
CREATE INDEX IF NOT EXISTS idx_options_underlying_time
  ON options_context_snapshots(asset_class, underlying, provider_ts);

CREATE TABLE IF NOT EXISTS insider_transactions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  accession_number TEXT NOT NULL,
  filing_at TEXT NOT NULL,
  transaction_at TEXT,
  issuer_cik TEXT,
  ticker TEXT NOT NULL,
  owner_cik TEXT,
  owner_name TEXT,
  owner_relationship TEXT,
  owner_title TEXT,
  transaction_code TEXT,
  acquired_disposed TEXT,
  shares REAL,
  price_per_share REAL,
  transaction_value_usd REAL,
  shares_owned_after REAL,
  direct_indirect TEXT,
  is_10b5_1 INTEGER,
  source TEXT NOT NULL DEFAULT 'SEC',
  raw_json TEXT,
  UNIQUE(accession_number, owner_cik, transaction_at, transaction_code, shares, price_per_share)
);
CREATE INDEX IF NOT EXISTS idx_insider_ticker_time
  ON insider_transactions(ticker, filing_at);

CREATE TABLE IF NOT EXISTS context_filter_decisions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  signal_id TEXT NOT NULL,
  filter_name TEXT NOT NULL,
  filter_version TEXT NOT NULL,
  decision_at TEXT NOT NULL,
  context_ts TEXT,
  action TEXT NOT NULL,
  reason TEXT,
  shadow_only INTEGER NOT NULL DEFAULT 1,
  features_json TEXT,
  UNIQUE(signal_id, filter_name, filter_version)
);
"""


def connect(db_path: str | Path | None = None) -> sqlite3.Connection:
    conn = mi.connect(db_path)
    conn.executescript(DDL)
    return conn


def _json(value: Any) -> str | None:
    if value is None:
        return None
    return json.dumps(value, default=str, separators=(",", ":"))[:32000]


def _hash(value: Any) -> str:
    raw = json.dumps(value, default=str, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:20]


def insert_unlock(conn: sqlite3.Connection, row: dict[str, Any]) -> bool:
    payload = dict(row)
    payload.setdefault("content_hash", _hash({k: v for k, v in payload.items() if k != "observed_at"}))
    payload.setdefault("quality_status", "ok")
    payload["raw_json"] = _json(payload.pop("raw_json", None))
    cols = ("source", "source_event_id", "observed_at", "asset_symbol", "unlock_at",
            "unlock_tokens", "unlock_usd", "pct_circulating", "avg_daily_volume_usd",
            "unlock_adv_days", "recipient_type", "unlock_type", "quality_status",
            "content_hash", "raw_json")
    cur = conn.execute(
        f"INSERT OR IGNORE INTO token_unlock_events({','.join(cols)}) VALUES({','.join('?' for _ in cols)})",
        tuple(payload.get(c) for c in cols),
    )
    return cur.rowcount > 0


def insert_named(conn: sqlite3.Connection, table: str, row: dict[str, Any], columns: tuple[str, ...]) -> bool:
    if table not in {"stablecoin_peg_snapshots", "cross_exchange_quote_snapshots",
                     "options_context_snapshots", "insider_transactions",
                     "context_filter_decisions"}:
        raise ValueError(f"unsupported context table: {table}")
    values = dict(row)
    if "raw_json" in columns:
        values["raw_json"] = _json(values.get("raw_json"))
    if "features_json" in columns:
        values["features_json"] = _json(values.get("features_json"))
    cur = conn.execute(
        f"INSERT OR REPLACE INTO {table}({','.join(columns)}) VALUES({','.join('?' for _ in columns)})",
        tuple(values.get(c) for c in columns),
    )
    return cur.rowcount > 0


__all__ = ["connect", "insert_unlock", "insert_named", "DDL"]

