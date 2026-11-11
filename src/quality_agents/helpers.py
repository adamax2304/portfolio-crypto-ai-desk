from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta
from typing import Any

from src.news.freshness import supports_mode, usable_at

from .config import QualityAgentsConfig
from .schemas import AgentVerdict, SignalContext, Verdict, base_symbol, parse_utc
from .store import table_exists


def make_verdict(
    *,
    name: str,
    version: str,
    verdict: Verdict,
    confidence: float,
    reason_codes: list[str] | tuple[str, ...],
    evidence: dict[str, Any],
    context: SignalContext,
    cfg: QualityAgentsConfig,
    model: str = "deterministic",
    prompt_version: str | None = None,
) -> AgentVerdict:
    created = context.decision_at
    return AgentVerdict(
        agent_name=name,
        agent_version=version,
        verdict=verdict,
        confidence=max(0.0, min(1.0, float(confidence))),
        reason_codes=tuple(dict.fromkeys(str(code).upper() for code in reason_codes if code)),
        evidence=evidence,
        created_at=created,
        expires_at=created + timedelta(minutes=cfg.ttl_minutes(name)),
        model=model,
        prompt_version=prompt_version,
    )


def _symbol_set(value: Any) -> set[str]:
    try:
        rows = json.loads(value or "[]") if isinstance(value, str) else (value or [])
    except (TypeError, json.JSONDecodeError):
        rows = []
    return {base_symbol(item) for item in rows if base_symbol(item)}


def matching_news_events(
    conn: sqlite3.Connection,
    context: SignalContext,
    *,
    limit: int = 500,
) -> list[dict[str, Any]]:
    if not table_exists(conn, "news_canonical_events"):
        return []
    cache_key = f"matching_news_events:{max(1, int(limit))}"
    cached = context.runtime_cache.get(cache_key)
    if isinstance(cached, list):
        return cached
    wanted = base_symbol(context.symbol)
    earliest = (context.decision_at - timedelta(days=7)).isoformat()
    decision_at = context.decision_at.isoformat()
    try:
        # Filter by the canonical trusted-symbol array before applying the
        # point-in-time policy. A global "latest N news" slice loses valid
        # 6-hour/7-day events whenever the desk ingests a busy market window.
        rows = [dict(row) for row in conn.execute(
            "WITH recent AS ("
            " SELECT * FROM news_canonical_events "
            " WHERE available_at IS NOT NULL AND available_at>=? AND available_at<=?"
            " UNION ALL SELECT * FROM news_canonical_events "
            " WHERE available_at IS NULL AND effective_at IS NOT NULL "
            " AND effective_at>=? AND effective_at<=?"
            " UNION ALL SELECT * FROM news_canonical_events "
            " WHERE available_at IS NULL AND effective_at IS NULL "
            " AND published_at>=? AND published_at<=?"
            ") SELECT DISTINCT e.* FROM recent e "
            "JOIN json_each(COALESCE(e.trusted_symbols_json,'[]')) j "
            "WHERE (UPPER(CAST(j.value AS TEXT))=? "
            "OR UPPER(CAST(j.value AS TEXT)) LIKE ?) "
            "ORDER BY e.news_item_id DESC LIMIT ?",
            (
                earliest, decision_at, earliest, decision_at, earliest, decision_at,
                wanted, f"{wanted}/%", max(1, int(limit)),
            ),
        ).fetchall()]
    except sqlite3.OperationalError:
        # Compatibility for old/read-only SQLite builds without JSON1.
        rows = [dict(row) for row in conn.execute(
            "SELECT * FROM news_canonical_events "
            "WHERE COALESCE(available_at,effective_at,published_at)<=? "
            "AND COALESCE(available_at,effective_at,published_at)>=? "
            "ORDER BY news_item_id DESC LIMIT ?",
            (decision_at, earliest, max(1, int(limit) * 4)),
        ).fetchall()]
    matched: list[dict[str, Any]] = []
    for row in rows:
        symbols = _symbol_set(row.get("trusted_symbols_json"))
        if wanted not in symbols:
            continue
        available = parse_utc(
            row.get("available_at") or row.get("effective_at") or row.get("published_at")
        )
        published = parse_utc(row.get("published_at"))
        expires = parse_utc(row.get("expires_at"))
        if available is None or available > context.decision_at:
            continue
        if published is not None and published > context.decision_at:
            continue
        if expires is not None and expires < context.decision_at:
            continue
        if not usable_at(
            row.get("event_latency_class"),
            row.get("available_at") or row.get("effective_at") or row.get("published_at"),
            context.decision_at,
        ):
            continue
        row["supports_mode"] = supports_mode(row.get("event_latency_class"), context.mode)
        row["available_age_seconds"] = round(
            max(0.0, (context.decision_at - available).total_seconds()), 3,
        )
        row["trusted_symbols"] = sorted(symbols)
        matched.append(row)
    matched.sort(
        key=lambda row: (
            parse_utc(row.get("available_at") or row.get("effective_at") or row.get("published_at"))
            or datetime.min.replace(tzinfo=context.decision_at.tzinfo),
            float(row.get("confidence") or 0.0),
        ),
        reverse=True,
    )
    context.runtime_cache[cache_key] = matched
    return matched


def compact_event(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "event_id": row.get("event_id"),
        "title": str(row.get("title") or "")[:180],
        "source": row.get("source"),
        "published_at": row.get("published_at"),
        "available_at": row.get("available_at"),
        "event_latency_class": row.get("event_latency_class"),
        "event_type": row.get("event_type"),
        "direction_hint": row.get("direction_hint"),
        "source_quality": row.get("source_quality"),
        "confidence": row.get("confidence"),
        "linkage_allowed": bool(row.get("linkage_allowed")),
        "linkage_reason": row.get("linkage_reason"),
        "risk_action": row.get("risk_action"),
        "supports_mode": bool(row.get("supports_mode")),
        "available_age_seconds": row.get("available_age_seconds"),
    }
