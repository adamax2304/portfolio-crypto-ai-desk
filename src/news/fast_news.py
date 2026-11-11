"""Fast, point-in-time Finnhub news ingest.

This is a transport layer, not a trading strategy. It observes market/company
news frequently, records exactly when the desk first saw an item, and hands the
normal saved rows to the existing resolver/canonical-event pipeline. A failed
poll is explicitly visible in source telemetry but never blocks a strategy.
"""
from __future__ import annotations

import json
import os
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import requests
import yaml

from src.config import load_config
from src.data_collectors.rss_news_collector import RSSNewsCollector
from src.models import NewsItem
from src.news.freshness import classify_observation
from src.news.source_telemetry import now_iso, record_source_run
from src.storage.sqlite import SQLiteStore
from src.storage.file_store import FileStore

ROOT = Path(__file__).resolve().parents[2]
STATE_TABLE = "fast_news_provider_state"
FINNHUB_MARKET_SOURCE = "Finnhub market-news"
FINNHUB_COMPANY_SOURCE = "Finnhub company-news"


def _load_settings() -> dict[str, Any]:
    path = ROOT / "config" / "news_latency.yaml"
    try:
        with path.open("r", encoding="utf-8") as handle:
            return (yaml.safe_load(handle) or {}).get("fast_news") or {}
    except (OSError, yaml.YAMLError):
        return {}


def _load_local_env() -> None:
    """Scheduler subprocesses do not automatically import .env."""
    try:
        from dotenv import load_dotenv
        load_dotenv(ROOT / ".env", override=False)
    except Exception:
        pass


def _iso_from_unix(value: Any) -> str | None:
    try:
        return datetime.fromtimestamp(float(value), tz=timezone.utc).replace(microsecond=0).isoformat()
    except (TypeError, ValueError, OSError):
        return None


def _safe_error(exc: Exception) -> str:
    """Do not journal request URLs because they may contain credentials."""
    response = getattr(exc, "response", None)
    code = getattr(response, "status_code", None)
    return f"http_{code}" if code else type(exc).__name__


def _ensure_state(conn: sqlite3.Connection) -> None:
    conn.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {STATE_TABLE} (
            state_key TEXT PRIMARY KEY,
            state_value TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )


def _next_company_symbols(db_path: Path, *, limit: int) -> list[str]:
    """Round-robin the curated stocks universe across fast polls.

    The free endpoint remains well below its rate limit while every tracked
    stock receives a company-news refresh in roughly one short rotation.
    """
    try:
        from src.stocks import load_stocks_config
        symbols = sorted({str(s).upper() for s in load_stocks_config(ROOT).default_symbols if str(s).strip()})
    except Exception:
        symbols = []
    if not symbols or limit <= 0:
        return []
    with sqlite3.connect(str(db_path), timeout=30.0) as conn:
        _ensure_state(conn)
        row = conn.execute(
            f"SELECT state_value FROM {STATE_TABLE} WHERE state_key='finnhub_company_cursor'"
        ).fetchone()
        try:
            start = int(row[0]) % len(symbols) if row else 0
        except (TypeError, ValueError):
            start = 0
        count = min(int(limit), len(symbols))
        selected = [symbols[(start + offset) % len(symbols)] for offset in range(count)]
        conn.execute(
            f"""
            INSERT INTO {STATE_TABLE}(state_key,state_value,updated_at) VALUES('finnhub_company_cursor',?,?)
            ON CONFLICT(state_key) DO UPDATE SET state_value=excluded.state_value, updated_at=excluded.updated_at
            """,
            (str((start + count) % len(symbols)), now_iso()),
        )
    return selected


def _symbols(value: Any, fallback: str | None = None) -> list[str]:
    values = str(value or "").replace(",", " ").split()
    if fallback:
        values.append(fallback)
    return sorted({token.upper() for token in values if token and token.replace(".", "").isalnum()})


def _news_item(payload: dict[str, Any], *, source: str, available_at: str,
               fallback_symbol: str | None = None) -> NewsItem | None:
    title = " ".join(str(payload.get("headline") or payload.get("title") or "").split())
    if not title:
        return None
    url = str(payload.get("url") or "").strip()
    identifier = str(payload.get("id") or payload.get("news_id") or "").strip()
    if not url:
        if not identifier:
            return None
        url = f"finnhub://news/{source.replace(' ', '_').lower()}/{identifier}"
    published_at = _iso_from_unix(payload.get("datetime") or payload.get("published_at"))
    timing = classify_observation(published_at, available_at)
    summary = str(payload.get("summary") or payload.get("content") or "").strip()
    detected = _symbols(payload.get("related"), fallback_symbol)
    provider_symbols = _symbols(None, fallback_symbol) if fallback_symbol else []
    importance = 1.25 + min(len(detected), 3) * 0.45
    return NewsItem(
        title=title,
        source=source,
        url=url,
        published_at=published_at,
        content=summary or None,
        summary=summary or None,
        available_at=available_at,
        ingested_at=available_at,
        first_seen_at=available_at,
        event_latency_class=timing.event_latency_class,
        source_observation_delay_seconds=timing.source_observation_delay_seconds,
        provider_symbols=provider_symbols,
        provider_symbol_provenance="finnhub_company_query" if provider_symbols else None,
        detected_symbols=detected,
        importance=round(importance, 2),
        verification_status="single_source",
        source_category="fast_api",
    )


def _fetch(session: requests.Session, base_url: str, path: str, token: str,
           timeout: float, params: dict[str, Any]) -> list[dict[str, Any]]:
    response = session.get(
        f"{base_url.rstrip('/')}/{path.lstrip('/')}",
        params=params,
        headers={"X-Finnhub-Token": token, "User-Agent": "crypto-ai-desk/fast-news"},
        timeout=timeout,
    )
    response.raise_for_status()
    payload = response.json()
    return payload if isinstance(payload, list) else []


def _save(store: SQLiteStore, items: list[NewsItem]) -> int:
    return store.save_news_items(items, asset_class="stocks") if items else 0


def _refresh_fast_rss(cfg: dict[str, Any], store: SQLiteStore) -> dict[str, Any]:
    names = {str(name) for name in cfg.get("fast_rss_sources") or [] if str(name).strip()}
    if not names:
        return {"status": "skipped", "sources": [], "seen": 0, "failed": []}
    collector = RSSNewsCollector(load_config(), FileStore(load_config()), store)
    summary = collector.fetch(
        limit_per_source=10,
        source_names=names,
        request_timeout=float(cfg.get("fast_rss_timeout_seconds", 7)),
        write_snapshot=False,
    )
    return {
        "status": "ok" if not summary.failed_sources else "partial",
        "sources": summary.fetched_sources,
        "seen": len(summary.items),
        "failed": sorted(summary.failed_sources),
    }


def refresh(*, now: datetime | None = None, session: requests.Session | None = None) -> dict[str, Any]:
    """Poll Finnhub without allowing a failure to affect trading.

    Returns safe aggregate diagnostics only; API credentials and URL query
    strings never enter the result, telemetry, or error journal.
    """
    cfg = _load_settings()
    finnhub = cfg.get("finnhub") or {}
    ref = (now or datetime.now(timezone.utc)).astimezone(timezone.utc).replace(microsecond=0)
    available_at = ref.isoformat()
    result: dict[str, Any] = {
        "enabled": bool(cfg.get("enabled", True) and finnhub.get("enabled", True)),
        "at": available_at,
        "market": {"saved": 0, "seen": 0, "status": "skipped"},
        "company": {"saved": 0, "seen": 0, "symbols": [], "status": "skipped"},
        "rss": {"status": "skipped", "sources": [], "seen": 0, "failed": []},
    }
    if not result["enabled"]:
        return result
    _load_local_env()
    token = str(os.getenv(str(finnhub.get("key_env") or "FINNHUB_API_KEY")) or "").strip()
    if not token:
        for source in (FINNHUB_MARKET_SOURCE, FINNHUB_COMPANY_SOURCE):
            record_source_run(source_name=source, source_type="api", asset_class="stocks", status="disabled",
                              item_count=0, error_code="missing_api_key", error_message="Finnhub key is not configured")
        result["market"]["status"] = result["company"]["status"] = "disabled"
        return result

    timeout = float(cfg.get("request_timeout_seconds", 10))
    base_url = str(finnhub.get("base_url") or "https://finnhub.io/api/v1")
    client = session or requests.Session()
    store = SQLiteStore(load_config().db_path)

    # Fast RSS items use the same NewsItem availability contract and normal
    # resolver/canonical pipeline as Finnhub. A slow source becomes thesis
    # context automatically; it cannot gain a FAST_EVENT label.
    try:
        result["rss"] = _refresh_fast_rss(cfg, store)
    except Exception as exc:
        result["rss"] = {"status": type(exc).__name__, "sources": [], "seen": 0, "failed": []}

    started = now_iso()
    try:
        payload = _fetch(client, base_url, "news", token, timeout, {
            "category": str(finnhub.get("global_category") or "general"),
        })
        max_items = int(finnhub.get("global_limit", 80))
        items = [item for raw in payload[:max_items]
                 if (item := _news_item(raw, source=FINNHUB_MARKET_SOURCE, available_at=available_at))]
        result["market"] = {"saved": _save(store, items), "seen": len(payload), "status": "ok"}
        record_source_run(source_name=FINNHUB_MARKET_SOURCE, source_type="api", asset_class="stocks",
                          status="ok" if payload else "ok_empty", started_at=started, item_count=len(items),
                          metadata={"category": str(finnhub.get("global_category") or "general")})
    except Exception as exc:  # fail-open transport boundary
        safe = _safe_error(exc)
        result["market"] = {"saved": 0, "seen": 0, "status": safe}
        record_source_run(source_name=FINNHUB_MARKET_SOURCE, source_type="api", asset_class="stocks",
                          status="error", started_at=started, error_code=safe, error_message=safe)

    symbols = _next_company_symbols(
        load_config().db_path, limit=int(finnhub.get("company_symbols_per_tick", 8))
    )
    result["company"]["symbols"] = symbols
    all_items: list[NewsItem] = []
    company_seen = 0
    failures = 0
    start_date = (ref - timedelta(days=int(finnhub.get("company_lookback_days", 1)))).date().isoformat()
    end_date = ref.date().isoformat()
    started = now_iso()
    for symbol in symbols:
        try:
            payload = _fetch(client, base_url, "company-news", token, timeout, {
                "symbol": symbol, "from": start_date, "to": end_date,
            })
            company_seen += len(payload)
            cap = int(finnhub.get("max_company_items_per_symbol", 20))
            all_items.extend(
                item for raw in payload[:cap]
                if (item := _news_item(raw, source=FINNHUB_COMPANY_SOURCE,
                                       available_at=available_at, fallback_symbol=symbol))
            )
        except Exception:
            failures += 1
    try:
        saved = _save(store, all_items)
        status = "ok" if failures == 0 else "partial"
        result["company"] = {"saved": saved, "seen": company_seen, "symbols": symbols, "status": status}
        record_source_run(source_name=FINNHUB_COMPANY_SOURCE, source_type="api", asset_class="stocks",
                          status="ok" if failures == 0 else "error", started_at=started, item_count=len(all_items),
                          error_code="partial_fetch" if failures else None,
                          error_message=f"{failures} symbol requests failed" if failures else None,
                          metadata={"symbols_requested": len(symbols), "failures": failures})
    except Exception as exc:
        safe = _safe_error(exc)
        result["company"] = {"saved": 0, "seen": company_seen, "symbols": symbols, "status": safe}
        record_source_run(source_name=FINNHUB_COMPANY_SOURCE, source_type="api", asset_class="stocks",
                          status="error", started_at=started, error_code=safe, error_message=safe)
    return result


def write_diagnostics(result: dict[str, Any]) -> Path:
    path = ROOT / "data" / "diagnostics" / "fast_news_latest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    return path


__all__ = ["FINNHUB_MARKET_SOURCE", "FINNHUB_COMPANY_SOURCE", "refresh", "write_diagnostics"]
