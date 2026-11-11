from __future__ import annotations

import json
import sqlite3
import time
from datetime import timedelta
from pathlib import Path
from typing import Any

from src.config import load_config
from src.llm_router import (
    Complexity,
    FinancialReasoning,
    LLMRouter,
    LLMRouterError,
    LLMTaskContext,
    LLMTier,
    Stakes,
    get_llm_router,
)

from .config import QualityAgentsConfig, load_quality_agents_config
from .helpers import compact_event
from .schemas import base_symbol, content_hash, normalize_symbol, utc_now
from .store import connect, ensure_tables, record_llm_assessment, table_exists


PROMPT_VERSION = "openrouter_news_event_quality_v2_budgeted"
SYSTEM_PROMPT = """You are a trading-desk quality-control classifier.
Return strict JSON only. Do not create trades. Do not change sizing. Assess
whether the supplied point-in-time news/event context improves or hurts trade
quality for the supplied symbol.

Allowed verdict values: SUPPORT, PASS, CAUTION, BLOCK_HARD, INSUFFICIENT_DATA.
Allowed direction_hint values: bullish, bearish, neutral, mixed, unknown.
Allowed event_latency_class values: FAST_EVENT, CONTINUATION_EVENT, THESIS_EVENT, UNKNOWN.
Use BLOCK_HARD only for wrong-entity, halt/delisting, exchange/API impossibility,
or clearly material event risk that should not be traded automatically.
Use CAUTION for rumor, stale/chase, macro/event risk, sell-the-news, weak linkage,
or direction conflict. Keep reason_codes uppercase snake case.
"""

_DB_RETRY_DELAYS = (0.0, 0.5, 2.0, 5.0)
NEWS_EVENT_JSON_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "verdict": {
            "type": "string",
            "enum": ["SUPPORT", "PASS", "CAUTION", "BLOCK_HARD", "INSUFFICIENT_DATA"],
        },
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "reason_codes": {
            "type": "array", "items": {"type": "string"}, "maxItems": 8,
        },
        "direction_hint": {
            "type": "string", "enum": ["bullish", "bearish", "neutral", "mixed", "unknown"],
        },
        "event_type": {"type": "string", "maxLength": 80},
        "event_latency_class": {
            "type": "string",
            "enum": ["FAST_EVENT", "CONTINUATION_EVENT", "THESIS_EVENT", "UNKNOWN"],
        },
        "risk_action": {
            "type": "string",
            "enum": ["none", "operator_review", "no_catalyst_boost", "avoid_chase", "block_auto"],
        },
        "short_rationale": {"type": "string", "maxLength": 300},
    },
    "required": [
        "verdict", "confidence", "reason_codes", "direction_hint", "event_type",
        "event_latency_class", "risk_action", "short_rationale",
    ],
}


def _db_retry(operation):
    """Retry local SQLite work without ever repeating a paid model call."""
    for attempt, delay in enumerate(_DB_RETRY_DELAYS):
        if delay:
            time.sleep(delay)
        try:
            return operation()
        except sqlite3.OperationalError as exc:
            busy = "locked" in str(exc).lower() or "busy" in str(exc).lower()
            if not busy or attempt + 1 >= len(_DB_RETRY_DELAYS):
                raise
    raise RuntimeError("quality advisory DB retry exhausted")


def _ensure_llm_table(conn: sqlite3.Connection) -> None:
    """Avoid replaying the full DDL script on every scheduled cache read."""
    if not table_exists(conn, "quality_agent_llm_assessments"):
        ensure_tables(conn)


def _refresh_block(cfg: QualityAgentsConfig) -> dict[str, Any]:
    block = cfg.llm_advisory_refresh
    return block if isinstance(block, dict) else {}


def _is_budget_exhausted(error_type: Any) -> bool:
    return str(error_type or "").startswith("llm_daily_budget_exhausted:")


def _parse_symbols(value: Any, *, asset_class: str = "crypto") -> list[str]:
    try:
        rows = json.loads(value or "[]") if isinstance(value, str) else (value or [])
    except (TypeError, json.JSONDecodeError):
        rows = []
    symbols: list[str] = []
    seen: set[str] = set()
    for item in rows:
        symbol = normalize_symbol(item)
        if not symbol:
            continue
        if str(asset_class).lower() == "crypto" and "/" not in symbol and len(symbol) <= 10:
            symbol = f"{symbol}/USDT"
        key = symbol.upper()
        if key not in seen:
            symbols.append(key)
            seen.add(key)
    return symbols


def _sanitize_text(value: Any, *, limit: int = 600) -> str:
    text = " ".join(str(value or "").split())
    return text[:limit]


def _event_input(row: dict[str, Any], symbol: str) -> dict[str, Any]:
    compact = compact_event(row)
    asset_class = str(row.get("asset_class") or "crypto").lower()
    return {
        "task": "news_event_trade_quality_assessment",
        "symbol": symbol,
        "base_symbol": base_symbol(symbol),
        "asset_class": asset_class,
        "event": {
            **compact,
            "content_excerpt": _sanitize_text(
                row.get("content") or row.get("summary") or row.get("description"),
                limit=900,
            ),
            "trusted_symbols": _parse_symbols(row.get("trusted_symbols_json"), asset_class=asset_class),
            "related_symbols": _parse_symbols(row.get("related_symbols_json"), asset_class=asset_class),
            "importance": row.get("importance"),
        },
        "output_schema": {
            "verdict": "SUPPORT|PASS|CAUTION|BLOCK_HARD|INSUFFICIENT_DATA",
            "confidence": "0.0..1.0",
            "reason_codes": ["UPPER_SNAKE_CASE"],
            "direction_hint": "bullish|bearish|neutral|mixed|unknown",
            "event_type": "short taxonomy label",
            "event_latency_class": "FAST_EVENT|CONTINUATION_EVENT|THESIS_EVENT|UNKNOWN",
            "risk_action": "none|operator_review|no_catalyst_boost|avoid_chase|block_auto",
            "short_rationale": "one concise sentence",
        },
    }


def _normalized_assessment(raw: dict[str, Any]) -> dict[str, Any]:
    verdict = str(raw.get("verdict") or "INSUFFICIENT_DATA").upper()
    if verdict not in {"SUPPORT", "PASS", "CAUTION", "BLOCK_HARD", "INSUFFICIENT_DATA"}:
        verdict = "INSUFFICIENT_DATA"
    try:
        confidence = max(0.0, min(1.0, float(raw.get("confidence", 0.0))))
    except (TypeError, ValueError):
        confidence = 0.0
    reason_codes = raw.get("reason_codes") or []
    if isinstance(reason_codes, str):
        reason_codes = [reason_codes]
    clean_codes = []
    for code in reason_codes:
        normalized = "".join(
            ch if ch.isalnum() else "_" for ch in str(code).strip().upper()
        ).strip("_")
        if normalized:
            clean_codes.append(normalized[:80])
    if not clean_codes:
        clean_codes = ["LLM_NO_REASON_CODE"]
    return {
        "verdict": verdict,
        "confidence": round(confidence, 4),
        "reason_codes": list(dict.fromkeys(clean_codes))[:8],
        "direction_hint": str(raw.get("direction_hint") or "unknown").lower()[:40],
        "event_type": str(raw.get("event_type") or "unknown")[:80],
        "event_latency_class": str(raw.get("event_latency_class") or "UNKNOWN").upper()[:40],
        "risk_action": str(raw.get("risk_action") or "none").lower()[:80],
        "short_rationale": _sanitize_text(raw.get("short_rationale"), limit=300),
    }


def _active_candidate_index(
    conn: sqlite3.Connection,
    *,
    lookback_hours: float,
    statuses: list[str],
    tiers: list[str],
    excluded_modes: list[str],
    max_symbols: int,
) -> dict[tuple[str, str], dict[str, Any]]:
    """Return the active A/B symbols worth buying inference for.

    News collection remains broad and deterministic. This index only narrows
    the optional LLM overlay to signals that are still in the execution funnel.
    """
    if not table_exists(conn, "proposed_signals"):
        return {}
    clean_statuses = sorted({str(value).strip().lower() for value in statuses if value})
    clean_tiers = sorted({str(value).strip().upper() for value in tiers if value})
    if not clean_statuses or not clean_tiers:
        return {}
    cutoff = (utc_now() - timedelta(hours=max(1.0, float(lookback_hours)))).isoformat()
    status_slots = ",".join("?" for _ in clean_statuses)
    tier_slots = ",".join("?" for _ in clean_tiers)
    rows = [dict(row) for row in conn.execute(
        "SELECT signal_id,symbol,asset_class,mode,tier,status,score,created_at,updated_at "
        "FROM proposed_signals "
        f"WHERE LOWER(status) IN ({status_slots}) AND UPPER(tier) IN ({tier_slots}) "
        "AND COALESCE(updated_at,created_at)>=? "
        "ORDER BY COALESCE(score,0) DESC,COALESCE(updated_at,created_at) DESC LIMIT ?",
        (*clean_statuses, *clean_tiers, cutoff, max(1, int(max_symbols)) * 8),
    ).fetchall()]
    excluded = {str(value).strip().lower() for value in excluded_modes if value}
    indexed: dict[tuple[str, str], dict[str, Any]] = {}
    for row in rows:
        if str(row.get("mode") or "").lower() in excluded:
            continue
        symbol = normalize_symbol(row.get("symbol"))
        asset_class = str(row.get("asset_class") or "crypto").lower()
        key = (asset_class, base_symbol(symbol))
        if not key[1] or key in indexed:
            continue
        indexed[key] = row
        if len(indexed) >= max(1, int(max_symbols)):
            break
    return indexed


def _collect_news_targets(
    conn: sqlite3.Connection, *, lookback_hours: float, max_events: int,
    max_symbols_per_event: int, min_confidence: float,
    active_candidates: dict[tuple[str, str], dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    if not table_exists(conn, "news_canonical_events"):
        return []
    cutoff = (utc_now() - timedelta(hours=max(1.0, float(lookback_hours)))).isoformat()
    rows = [dict(row) for row in conn.execute(
        "SELECT * FROM news_canonical_events "
        "WHERE COALESCE(available_at,effective_at,published_at)>=? "
        "AND COALESCE(confidence,0)>=? "
        "ORDER BY COALESCE(available_at,effective_at,published_at) DESC, news_item_id DESC "
        "LIMIT ?",
        (cutoff, max(0.0, float(min_confidence)), max(1, int(max_events))),
    ).fetchall()]
    targets: list[dict[str, Any]] = []
    for row in rows:
        asset_class = str(row.get("asset_class") or "crypto").lower()
        symbols = _parse_symbols(row.get("trusted_symbols_json"), asset_class=asset_class)
        for symbol in symbols[:max(1, int(max_symbols_per_event))]:
            candidate = None
            if active_candidates is not None:
                candidate = active_candidates.get((asset_class, base_symbol(symbol)))
                if candidate is None:
                    continue
            event_key = str(row.get("event_id") or row.get("news_item_id") or "")
            if not event_key:
                continue
            targets.append({
                "scope": "canonical_news_event",
                "target_key": f"news:{event_key}:{symbol}",
                "signal_id": candidate.get("signal_id") if candidate else None,
                "asset_class": asset_class,
                "symbol": symbol,
                "source": str(row.get("source") or ""),
                "input_payload": _event_input(row, symbol),
            })
    return targets


def _fresh_assessment_exists(
    conn: sqlite3.Connection, *, target: dict[str, Any], model: str, input_hash: str,
) -> bool:
    if not table_exists(conn, "quality_agent_llm_assessments"):
        return False
    now = utc_now().isoformat()
    row = conn.execute(
        "SELECT 1 FROM quality_agent_llm_assessments "
        "WHERE scope=? AND target_key=? AND input_hash=? AND model=? "
        "AND prompt_version=? AND status='OK' AND expires_at>=? LIMIT 1",
        (
            target["scope"], target["target_key"], input_hash, model, PROMPT_VERSION, now,
        ),
    ).fetchone()
    return row is not None


def refresh_openrouter_advisory(
    *,
    db: str | Path | None = None,
    cfg: QualityAgentsConfig | None = None,
    lookback_hours: float | None = None,
    max_events: int | None = None,
    force: bool = False,
    router: LLMRouter | None = None,
) -> dict[str, Any]:
    quality_cfg = cfg or load_quality_agents_config()
    refresh = _refresh_block(quality_cfg)
    if not bool(refresh.get("enabled", False)):
        return {"status": "DISABLED", "reason": "LLM_ADVISORY_DISABLED"}
    ttl_minutes = max(5.0, float(refresh.get("ttl_minutes") or 360))
    db_path = Path(db or load_config().db_path)
    try:
        llm = router or get_llm_router(db_path=db_path)
    except Exception as exc:
        return {"status": "DISABLED", "reason": str(exc)}
    model = llm.cfg.model(LLMTier.ROUTINE).model_id
    provider = str(llm.cfg.raw.get("provider") or "openrouter")
    scope_stats = {"active_symbols": 0}
    def _load_targets() -> list[dict[str, Any]]:
        with connect(db_path, timeout_seconds=5.0) as conn:
            _ensure_llm_table(conn)
            candidate_scope = str(refresh.get("candidate_scope") or "active_ab").lower()
            active_candidates = None
            if candidate_scope == "active_ab":
                active_candidates = _active_candidate_index(
                    conn,
                    lookback_hours=float(refresh.get("candidate_lookback_hours") or 48),
                    statuses=list(refresh.get("candidate_statuses") or []),
                    tiers=list(refresh.get("candidate_tiers") or []),
                    excluded_modes=list(refresh.get("excluded_modes") or []),
                    max_symbols=int(refresh.get("max_active_symbols") or 80),
                )
                scope_stats["active_symbols"] = len(active_candidates)
            loaded = _collect_news_targets(
                conn,
                lookback_hours=float(lookback_hours or refresh.get("lookback_hours") or 8),
                max_events=int(max_events or refresh.get("max_events") or 24),
                max_symbols_per_event=int(refresh.get("max_symbols_per_event") or 3),
                min_confidence=float(refresh.get("min_confidence") or 0.0),
                active_candidates=active_candidates,
            )
            for target in loaded:
                input_payload = target["input_payload"]
                input_hash = content_hash(input_payload)
                target["input_hash"] = input_hash
                target["skip_fresh"] = bool(not force and _fresh_assessment_exists(
                    conn, target=target, model=model, input_hash=input_hash,
                ))
            return loaded

    targets = _db_retry(_load_targets)

    checked = len(targets)
    skipped = sum(bool(target.get("skip_fresh")) for target in targets)
    pending = [target for target in targets if not target.get("skip_fresh")]
    pending_total = len(pending)
    max_assessments = max(1, int(refresh.get("max_assessments_per_run") or 8))
    pending = pending[:max_assessments]
    deferred = max(0, pending_total - len(pending))
    outcomes: list[dict[str, Any]] = []
    errors = 0
    error_types: dict[str, int] = {}
    budget_paused = False
    for target in pending:
        input_payload = target["input_payload"]
        now = utc_now()
        router_request_id = None
        try:
            routed = llm.call(LLMTaskContext(
                agent_name="llm_cached_advisory",
                task_type="news_event_classification",
                system_prompt=SYSTEM_PROMPT,
                user_payload=input_payload,
                financial_reasoning=FinancialReasoning.DATA_PROCESSING,
                complexity=Complexity.LOW,
                stakes=Stakes.LOW,
                requires_structured_output=True,
                source_count=1,
                signal_id=target.get("signal_id"),
                asset_class=target.get("asset_class"),
                symbol=target.get("symbol"),
                metadata={
                    "prompt_version": PROMPT_VERSION,
                    "max_tokens": int(refresh.get("max_tokens") or 400),
                    "max_retries": int(refresh.get("max_retries") or 1),
                    "disable_reasoning": True,
                    "json_schema": NEWS_EVENT_JSON_SCHEMA,
                    "json_schema_name": "news_event_quality",
                },
            ))
            result = routed.primary
            assessment = _normalized_assessment(result.payload)
            latency_ms = result.latency_ms
            status = "OK"
            error_type = None
            actual_model = result.model or model
            router_request_id = result.request_id
        except LLMRouterError as exc:
            budget_paused = _is_budget_exhausted(exc)
            assessment = {
                "verdict": "INSUFFICIENT_DATA",
                "confidence": 0.0,
                "reason_codes": ["OPENROUTER_REQUEST_ERROR"],
                "error_type": str(exc),
            }
            latency_ms = 0.0
            status = "ERROR"
            error_type = str(exc)
            actual_model = model
            errors += 1
            error_types[error_type] = error_types.get(error_type, 0) + 1
        outcomes.append({
            "target": target,
            "now": now,
            "assessment": assessment,
            "latency_ms": latency_ms,
            "status": status,
            "error_type": error_type,
            "actual_model": actual_model,
            "router_request_id": router_request_id,
        })
        if budget_paused:
            break

    def _persist_outcomes() -> None:
        with connect(db_path, timeout_seconds=5.0) as conn:
            _ensure_llm_table(conn)
            for outcome in outcomes:
                target = outcome["target"]
                record_llm_assessment(
                    conn,
                    scope=target["scope"],
                    target_key=target["target_key"],
                    provider=provider,
                    model=outcome["actual_model"],
                    prompt_version=PROMPT_VERSION,
                    status=outcome["status"],
                    assessment=outcome["assessment"],
                    input_payload=target["input_payload"],
                    created_at=outcome["now"],
                    expires_at=outcome["now"] + timedelta(minutes=ttl_minutes),
                    latency_ms=outcome["latency_ms"],
                    signal_id=target.get("signal_id"),
                    asset_class=target.get("asset_class"),
                    symbol=target.get("symbol"),
                    source=target.get("source"),
                    error_type=outcome["error_type"],
                )
            conn.commit()

    _db_retry(_persist_outcomes)
    for outcome in outcomes:
        if outcome["router_request_id"]:
            llm.mark_downstream_action(
                outcome["router_request_id"], "quality_advisory_cache_written"
            )
    recorded = len(outcomes)
    budget_error_count = sum(
        count for error_type, count in error_types.items()
        if _is_budget_exhausted(error_type)
    )
    if errors == 0:
        status = "OK"
    elif budget_error_count == errors:
        status = "BUDGET_PAUSED"
    else:
        status = "DEGRADED"
    primary_error = next(iter(error_types), None)
    budget_skipped = max(0, len(pending) - recorded) if status == "BUDGET_PAUSED" else 0
    return {
        "status": status,
        "provider": provider,
        "model": model,
        "candidate_scope": str(refresh.get("candidate_scope") or "active_ab"),
        "active_symbols": scope_stats["active_symbols"],
        "targets": len(targets),
        "checked": checked,
        "skipped_fresh": skipped,
        "pending_before_cap": pending_total,
        "deferred": deferred + budget_skipped,
        "budget_skipped": budget_skipped,
        "recorded": recorded,
        "errors": errors,
        "error_types": error_types,
        "error": primary_error,
    }


__all__ = ["PROMPT_VERSION", "refresh_openrouter_advisory"]
