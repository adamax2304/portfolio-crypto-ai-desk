"""Versioned asset registry for news/entity resolution.

The registry separates assets the desk explicitly tracks from symbols merely
observed on an exchange.  Discovery is automatic, but DISCOVERED assets never
become trusted catalyst links or tradeable signals without a curated alias.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from src.config import load_config


REGISTRY_VERSION = "news_asset_registry_v1"
_ROOT = Path(__file__).resolve().parents[2]
_DDL = """
CREATE TABLE IF NOT EXISTS news_asset_registry (
    asset_key TEXT PRIMARY KEY,
    asset_class TEXT NOT NULL,
    ticker TEXT NOT NULL,
    canonical_name TEXT,
    aliases_json TEXT NOT NULL DEFAULT '[]',
    exchange_symbols_json TEXT NOT NULL DEFAULT '[]',
    contract_addresses_json TEXT NOT NULL DEFAULT '[]',
    chain TEXT,
    cik TEXT,
    status TEXT NOT NULL,
    verification_source TEXT,
    first_seen_at TEXT NOT NULL,
    last_seen_at TEXT NOT NULL,
    verified_at TEXT,
    registry_version TEXT NOT NULL
)
"""


def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception:
        return {}


def _cik_map() -> dict[str, str]:
    try:
        from src.news.edgar import load_cik_map
        return {str(t).upper(): str(c).zfill(10) for t, c in load_cik_map().items()}
    except Exception:
        return {}


def _dynamic_crypto_symbols() -> set[str]:
    try:
        from src.news.entity_resolver import _dynamic_crypto_tickers
        return set(_dynamic_crypto_tickers())
    except Exception:
        return set()


def ensure_table(conn: sqlite3.Connection) -> None:
    conn.execute(_DDL)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_news_asset_registry_ticker "
                 "ON news_asset_registry(asset_class, ticker, status)")


def refresh(db: str | None = None, *, now: datetime | None = None) -> dict[str, Any]:
    """Upsert curated TRACKED assets and exchange-observed DISCOVERED assets.

    Existing rows are never deleted.  An exchange observation cannot demote a
    TRACKED row, and cannot promote itself beyond DISCOVERED.
    """
    now = now or datetime.now(timezone.utc)
    stamp = now.isoformat()
    path = db or str(load_config().db_path)
    crypto = _load_yaml(_ROOT / "config" / "crypto_entity_aliases.yaml")
    stocks = _load_yaml(_ROOT / "config" / "stocks_entity_aliases.yaml")
    cik = _cik_map()
    records: list[dict[str, Any]] = []
    for asset_class, payload in (("crypto", crypto), ("stocks", stocks)):
        for ticker, info in payload.items():
            if not isinstance(info, dict):
                continue
            ticker = str(ticker).upper()
            aliases = sorted({str(a).strip() for a in (info.get("aliases") or []) if str(a).strip()})
            canonical = str(info.get("canonical_name") or ticker).strip()
            records.append({
                "asset_key": f"{asset_class}:{ticker}", "asset_class": asset_class,
                "ticker": ticker, "canonical_name": canonical, "aliases": aliases,
                "exchange_symbols": [f"{ticker}/USDT"] if asset_class == "crypto" else [],
                "cik": cik.get(ticker) if asset_class == "stocks" else None,
                "status": "TRACKED", "verification_source": "curated_entity_aliases",
                "verified_at": stamp,
            })
    tracked_crypto = {r["ticker"] for r in records if r["asset_class"] == "crypto"}
    for ticker in sorted(_dynamic_crypto_symbols() - tracked_crypto):
        records.append({
            "asset_key": f"crypto:{ticker}", "asset_class": "crypto", "ticker": ticker,
            "canonical_name": ticker, "aliases": [], "exchange_symbols": [f"{ticker}/USDT"],
            "cik": None, "status": "DISCOVERED", "verification_source": "local_exchange_universe",
            "verified_at": None,
        })

    conn = sqlite3.connect(path, timeout=30)
    try:
        ensure_table(conn)
        for r in records:
            conn.execute(
                """
                INSERT INTO news_asset_registry(
                    asset_key, asset_class, ticker, canonical_name, aliases_json,
                    exchange_symbols_json, contract_addresses_json, chain, cik, status,
                    verification_source, first_seen_at, last_seen_at, verified_at, registry_version
                ) VALUES(?,?,?,?,?,?,'[]',NULL,?,?,?,?,?,?,?)
                ON CONFLICT(asset_key) DO UPDATE SET
                    canonical_name=CASE WHEN excluded.status='TRACKED' THEN excluded.canonical_name
                                        ELSE news_asset_registry.canonical_name END,
                    aliases_json=CASE WHEN excluded.status='TRACKED' THEN excluded.aliases_json
                                      ELSE news_asset_registry.aliases_json END,
                    exchange_symbols_json=excluded.exchange_symbols_json,
                    cik=COALESCE(excluded.cik, news_asset_registry.cik),
                    status=CASE WHEN news_asset_registry.status='TRACKED' THEN 'TRACKED'
                                ELSE excluded.status END,
                    verification_source=CASE WHEN excluded.status='TRACKED' THEN excluded.verification_source
                                             ELSE news_asset_registry.verification_source END,
                    last_seen_at=excluded.last_seen_at,
                    verified_at=COALESCE(excluded.verified_at, news_asset_registry.verified_at),
                    registry_version=excluded.registry_version
                """,
                (r["asset_key"], r["asset_class"], r["ticker"], r["canonical_name"],
                 json.dumps(r["aliases"], ensure_ascii=False), json.dumps(r["exchange_symbols"]),
                 r["cik"], r["status"], r["verification_source"], stamp, stamp,
                 r["verified_at"], REGISTRY_VERSION),
            )
        conn.commit()
        counts = dict(conn.execute(
            "SELECT status, COUNT(*) FROM news_asset_registry GROUP BY status").fetchall())
        by_asset = {f"{a}:{s}": n for a, s, n in conn.execute(
            "SELECT asset_class, status, COUNT(*) FROM news_asset_registry GROUP BY asset_class,status")}
    finally:
        conn.close()
    return {"generated_at": stamp, "registry_version": REGISTRY_VERSION,
            "upserted": len(records), "counts": counts, "by_asset_status": by_asset,
            "note": "DISCOVERED is visibility only; only TRACKED assets may be trusted by news linkage."}


def write_report(result: dict[str, Any]) -> str:
    path = _ROOT / "reports" / "NEWS_ASSET_REGISTRY.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# News Asset Registry", "", f"Generated: {result['generated_at']}", "",
             f"Version: `{result['registry_version']}`", "",
             "| status | count |", "|---|---:|"]
    lines += [f"| {k} | {v} |" for k, v in sorted(result.get("counts", {}).items())]
    lines += ["", result["note"]]
    path.write_text("\n".join(lines), encoding="utf-8")
    return str(path)


__all__ = ["REGISTRY_VERSION", "ensure_table", "refresh", "write_report"]
