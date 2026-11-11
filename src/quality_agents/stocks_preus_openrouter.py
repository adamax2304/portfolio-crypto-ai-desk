from __future__ import annotations

import json
import math
import sqlite3
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from src.config import load_config
from src.execution import stocks_preus_review as preus
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

from .schemas import content_hash
from .store import (
    assign_experiment_cohorts,
    connect,
    ensure_tables,
    record_llm_assessment,
)


PROMPT_VERSION = "stocks_preus_openrouter_review_v2_budgeted"
SCOPE = "stocks_preus_openrouter_review"
SYSTEM_PROMPT = """You are the pre-US risk and context reviewer for an automated
stock-trading desk. Review one EXISTING overnight/pre-market candidate. Do not
invent a trade, assign a tier, change entry/stop/targets, or decide order size.
Deterministic code owns eligibility, score clamps, geometry, and execution.

Judge whether the candidate's point-in-time evidence still supports evaluation
at the US cash open. Use only the supplied data. Pay special attention to exact
entity linkage, catalyst direction and freshness, SPY/sector alignment,
relative strength, material event risk, and obvious stale/chase conditions.

Return one strict JSON object with exactly these fields:
verdict: SUPPORT|NEUTRAL|CAUTION|BLOCK|INSUFFICIENT_DATA
confidence: number from 0 to 1
requested_adjustment: number from -7 to 5
reason_codes: array of short UPPER_SNAKE_CASE strings
short_rationale: one concise sentence

SUPPORT means multiple independent supplied facts align. BLOCK is reserved for
clear wrong-entity, halt/delisting, material legal/event risk, or an explicit
directional contradiction. Missing data alone is INSUFFICIENT_DATA, not BLOCK.
Never claim that a fact was verified unless it appears in deterministic_evidence.
"""

_ALLOWED_VERDICTS = {"SUPPORT", "NEUTRAL", "CAUTION", "BLOCK", "INSUFFICIENT_DATA"}
PREUS_JSON_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "verdict": {"type": "string", "enum": sorted(_ALLOWED_VERDICTS)},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "requested_adjustment": {"type": "number", "minimum": -7, "maximum": 5},
        "reason_codes": {
            "type": "array", "items": {"type": "string"}, "maxItems": 8,
        },
        "short_rationale": {"type": "string", "maxLength": 400},
    },
    "required": [
        "verdict", "confidence", "requested_adjustment", "reason_codes",
        "short_rationale",
    ],
}


def _utc(value: datetime | None = None) -> datetime:
    moment = value or datetime.now(timezone.utc)
    if moment.tzinfo is None:
        return moment.replace(tzinfo=timezone.utc)
    return moment.astimezone(timezone.utc)


def _json_obj(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return dict(value)
    try:
        decoded = json.loads(value or "{}")
    except (TypeError, ValueError, json.JSONDecodeError):
        return {}
    return decoded if isinstance(decoded, dict) else {}


def _json_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return list(value)
    try:
        decoded = json.loads(value or "[]")
    except (TypeError, ValueError, json.JSONDecodeError):
        return []
    return decoded if isinstance(decoded, list) else []


def _clean_reason_code(value: Any) -> str:
    code = "".join(
        char if char.isalnum() else "_" for char in str(value or "").strip().upper()
    ).strip("_")
    return code[:80]


def _compact_raw_signal(raw: dict[str, Any]) -> dict[str, Any]:
    structured = _json_obj(raw.get("structured"))
    score = _json_obj(raw.get("raw_score"))
    setup = _json_obj(raw.get("raw_setup"))
    stop = _json_obj(raw.get("initial_stop_contract") or raw.get("stop_contract"))
    return {
        "thesis": str(raw.get("thesis") or "")[:400],
        "evidence": [str(item)[:220] for item in (raw.get("evidence") or [])[:8]],
        "counterarguments": [
            str(item)[:220] for item in (raw.get("counterarguments") or [])[:8]
        ],
        "structured": {
            key: structured.get(key)
            for key in (
                "sector", "sector_etf", "rs_vs_spy", "rs_vs_sector",
                "volume_ratio", "rr_to_tp1", "tp1_source", "atr_extension",
            )
        },
        "score_components": _json_obj(score.get("components")),
        "risk_penalty": score.get("risk_penalty"),
        "score_blocks": score.get("blocks") or [],
        "setup": {
            key: setup.get(key)
            for key in (
                "entry_low", "entry_high", "invalidation", "tp1", "tp2", "tp3",
                "rr_to_tp1", "volume_ratio",
            )
        },
        "stop": {
            key: stop.get(key)
            for key in (
                "stop_source", "stop_model", "structure_timeframe", "structure_level",
                "fallback_used", "confidence", "stop_distance_pct", "geometry_valid",
            )
        },
    }


def _latest_agent_context(conn: sqlite3.Connection, signal_id: str) -> dict[str, Any]:
    try:
        rows = conn.execute(
            "SELECT agent_name,verdict,confidence,reason_codes_json,evidence_json,"
            "created_at,expires_at FROM quality_agent_signal_verdicts "
            "WHERE signal_id=? AND stage='stocks_preus_candidate' "
            "ORDER BY created_at DESC,rowid DESC",
            (signal_id,),
        ).fetchall()
    except sqlite3.OperationalError:
        return {}
    latest: dict[str, Any] = {}
    for row in rows:
        item = dict(row)
        name = str(item.get("agent_name") or "")
        if not name or name in latest:
            continue
        latest[name] = {
            "verdict": item.get("verdict"),
            "confidence": item.get("confidence"),
            "reason_codes": _json_list(item.get("reason_codes_json")),
            "evidence": _json_obj(item.get("evidence_json")),
            "created_at": item.get("created_at"),
            "expires_at": item.get("expires_at"),
        }
    return latest


def _directional_rs_confirmed(raw: dict[str, Any], direction: str) -> bool:
    structured = _json_obj(raw.get("structured"))
    try:
        rs_spy = float(structured.get("rs_vs_spy"))
        rs_sector = float(structured.get("rs_vs_sector"))
    except (TypeError, ValueError):
        return False
    if direction.lower() == "short":
        return rs_spy < 0 and rs_sector < 0
    return rs_spy > 0 and rs_sector > 0


def _server_evidence(
    *, candidate: dict[str, Any], raw: dict[str, Any], agents: dict[str, Any],
    preus_cfg: dict[str, Any],
) -> dict[str, Any]:
    news = agents.get("news_entity") or {}
    news_evidence = _json_obj(news.get("evidence"))
    events = [item for item in (news_evidence.get("events") or []) if isinstance(item, dict)]
    linked = [
        item for item in events
        if bool(item.get("linkage_allowed")) and bool(item.get("supports_mode"))
    ]
    max_catalyst_age = float(preus_cfg.get("catalyst_max_age_hours", 24)) * 3600.0
    fresh_linked = [
        item for item in linked
        if item.get("available_age_seconds") is not None
        and 0 <= float(item.get("available_age_seconds")) <= max_catalyst_age
    ]

    market = agents.get("market_regime") or {}
    market_evidence = _json_obj(market.get("evidence"))
    try:
        market_age = float(market_evidence.get("snapshot_age_minutes"))
    except (TypeError, ValueError):
        market_age = float("inf")
    market_fresh = (
        str(market.get("verdict") or "").upper() != "INSUFFICIENT_DATA"
        and market_age <= float(preus_cfg.get("market_context_max_age_minutes", 45))
    )

    hard_agent_block = any(
        str(item.get("verdict") or "").upper() == "BLOCK_HARD"
        for item in agents.values()
    )
    raw_score = _json_obj(raw.get("raw_score"))
    no_hard_cap = not hard_agent_block and not bool(raw_score.get("blocks"))
    relative_strength = _directional_rs_confirmed(
        raw, str(candidate.get("direction") or raw.get("direction") or "long")
    )
    return {
        # These exact five booleans are the only fields accepted by the
        # existing positive-adjustment gate in stocks_preus_review.py.
        "catalyst_entity_resolved": bool(linked),
        "catalyst_fresh": bool(fresh_linked),
        "market_context_fresh": bool(market_fresh),
        "no_hard_cap": bool(no_hard_cap),
        "relative_strength_confirmed": bool(relative_strength),
        "matched_news_count": int(news_evidence.get("matched_event_count") or 0),
        "fresh_linked_news_count": len(fresh_linked),
        "market_snapshot_age_minutes": None if market_age == float("inf") else market_age,
        "quality_agent_verdicts": {
            name: {
                "verdict": item.get("verdict"),
                "confidence": item.get("confidence"),
                "reason_codes": item.get("reason_codes") or [],
            }
            for name, item in agents.items()
        },
    }


def _candidate_input(
    conn: sqlite3.Connection, candidate: dict[str, Any], *, now: datetime,
    preus_cfg: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    signal_id = str(candidate.get("signal_id") or "")
    row = conn.execute(
        "SELECT * FROM proposed_signals WHERE signal_id=?", (signal_id,)
    ).fetchone()
    signal = dict(row) if row is not None else {}
    raw = _json_obj(signal.get("raw_idea_json"))
    agents = _latest_agent_context(conn, signal_id)
    evidence = _server_evidence(
        candidate=candidate, raw=raw, agents=agents, preus_cfg=preus_cfg,
    )
    payload = {
        "task": "review_existing_stock_preus_candidate",
        "as_of": now.isoformat(),
        "candidate": {
            key: candidate.get(key)
            for key in (
                "signal_id", "symbol", "direction", "tier", "pre_gate_tier",
                "base_score", "funnel_state", "promotable", "created_at",
                "entry_trigger", "stop_loss", "cap_reasons", "paper_entry_profile",
                "paper_entry_confirmation",
            )
        },
        "signal_context": _compact_raw_signal(raw),
        "deterministic_evidence": evidence,
        "quality_agent_details": agents,
        "constraints": {
            "model_may_not_create_trade": True,
            "model_may_not_assign_tier": True,
            "model_may_not_change_geometry_or_size": True,
            "positive_adjustment_requires_all_server_flags": list(
                preus_cfg.get("support_requires") or []
            ),
        },
    }
    return payload, evidence


def _cached_successful_assessment(
    conn: sqlite3.Connection,
    *,
    target_key: str,
    model: str,
    now: datetime,
) -> dict[str, Any] | None:
    """Resume a same-session review without paying for completed candidates."""
    row = conn.execute(
        "SELECT model,assessment_json,created_at,expires_at FROM "
        "quality_agent_llm_assessments "
        "WHERE scope=? AND target_key=? AND model=? AND prompt_version=? "
        "AND status='OK' AND expires_at>? ORDER BY created_at DESC LIMIT 1",
        (SCOPE, target_key, model, PROMPT_VERSION, now.isoformat()),
    ).fetchone()
    if row is None:
        return None
    assessment = _json_obj(row["assessment_json"])
    if not assessment or str(assessment.get("verdict") or "").upper() not in _ALLOWED_VERDICTS:
        return None
    return {
        "model": str(row["model"]),
        "assessment": assessment,
        "created_at": str(row["created_at"]),
        "expires_at": str(row["expires_at"]),
    }


def _failed_attempt_count(
    conn: sqlite3.Connection,
    *,
    target_key: str,
    model: str,
) -> int:
    row = conn.execute(
        "SELECT COUNT(*) FROM quality_agent_llm_assessments "
        "WHERE scope=? AND target_key=? AND model=? AND prompt_version=? "
        "AND status='ERROR'",
        (SCOPE, target_key, model, PROMPT_VERSION),
    ).fetchone()
    return int(row[0] or 0) if row is not None else 0


def _normalized_model_verdict(
    raw: dict[str, Any], *, server_evidence: dict[str, Any],
) -> dict[str, Any]:
    verdict = str(raw.get("verdict") or "INSUFFICIENT_DATA").upper()
    if verdict == "BLOCK_HARD":
        verdict = "BLOCK"
    if verdict not in _ALLOWED_VERDICTS:
        verdict = "INSUFFICIENT_DATA"
    try:
        confidence = max(0.0, min(1.0, float(raw.get("confidence", 0.0))))
    except (TypeError, ValueError):
        confidence = 0.0

    if verdict == "BLOCK" and confidence < 0.8:
        verdict = "CAUTION"
    if verdict == "SUPPORT" and confidence < 0.65:
        verdict = "NEUTRAL"

    if verdict == "SUPPORT":
        requested = 5.0 if confidence >= 0.85 else 3.0 if confidence >= 0.75 else 2.0
    elif verdict == "CAUTION":
        requested = -5.0 if confidence >= 0.85 else -3.0
    else:
        requested = 0.0
    try:
        model_requested = float(raw.get("requested_adjustment"))
    except (TypeError, ValueError):
        model_requested = requested
    if verdict == "SUPPORT":
        requested = max(0.0, min(requested, model_requested, 5.0))
    elif verdict == "CAUTION":
        requested = max(-7.0, min(-3.0, model_requested))

    codes = raw.get("reason_codes") or []
    if isinstance(codes, str):
        codes = [codes]
    reason_codes = list(dict.fromkeys(
        code for code in (_clean_reason_code(item) for item in codes) if code
    ))[:8]
    if not reason_codes:
        reason_codes = ["OPENROUTER_PREUS_NO_REASON"]
    rationale = " ".join(str(raw.get("short_rationale") or "").split())[:400]
    evidence = {
        **server_evidence,
        "llm_confidence": round(confidence, 4),
        "llm_short_rationale": rationale,
        "llm_verdict_raw": str(raw.get("verdict") or ""),
    }
    return {
        "verdict": verdict,
        "confidence": round(confidence, 4),
        "requested_adjustment": requested,
        "reason_codes": reason_codes,
        "short_rationale": rationale,
        "evidence": evidence,
    }


def _evidence_conflict(server_evidence: dict[str, Any]) -> bool:
    def confidence(item: dict[str, Any]) -> float:
        try:
            return float(item.get("confidence") or 0.0)
        except (TypeError, ValueError):
            return 0.0

    rows = [
        item for item in (server_evidence.get("quality_agent_verdicts") or {}).values()
        if isinstance(item, dict)
    ]
    strong_support = any(
        str(item.get("verdict") or "").upper() == "SUPPORT"
        and confidence(item) >= 0.75
        for item in rows
    )
    material_opposition = any(
        str(item.get("verdict") or "").upper() in {"BLOCK", "BLOCK_HARD"}
        or (
            str(item.get("verdict") or "").upper() == "CAUTION"
            and confidence(item) >= 0.85
        )
        for item in rows
    )
    return strong_support and material_opposition


def _is_budget_exhausted(error_type: Any) -> bool:
    return str(error_type or "").startswith("llm_daily_budget_exhausted:")


def _call_one(
    *, router: LLMRouter, candidate: dict[str, Any], payload: dict[str, Any],
    server_evidence: dict[str, Any], max_tokens: int = 400,
) -> dict[str, Any]:
    signal_id = str(candidate.get("signal_id") or "")
    try:
        conflict = _evidence_conflict(server_evidence)
        routed = router.call(LLMTaskContext(
            agent_name="stocks_preus_review",
            task_type="preus_trade_setup_analysis",
            system_prompt=SYSTEM_PROMPT,
            user_payload=payload,
            financial_reasoning=FinancialReasoning.SYNTHESIS,
            complexity=Complexity.HIGH,
            stakes=Stakes.HIGH,
            ambiguity="high" if conflict else "medium",
            evidence_conflict=conflict,
            requires_structured_output=True,
            source_count=max(
                1,
                int(server_evidence.get("matched_news_count") or 0)
                + len(server_evidence.get("quality_agent_verdicts") or {}),
            ),
            signal_id=signal_id,
            asset_class="stocks",
            symbol=str(candidate.get("symbol") or ""),
            mode="intraday",
            metadata={
                "prompt_version": PROMPT_VERSION,
                "max_tokens": max(200, min(500, int(max_tokens))),
                # One financial analysis only. Transport/format failures fall
                # back to the deterministic baseline; malformed envelopes may
                # receive one cheap routine-tier formatting repair in Router v1.
                "max_retries": 0,
                "json_schema": PREUS_JSON_SCHEMA,
                "json_schema_name": "stocks_preus_review",
            },
        ))
        result = routed.primary
        normalized = _normalized_model_verdict(
            result.payload, server_evidence=server_evidence,
        )
        if routed.model_disagreement:
            normalized["reason_codes"] = list(dict.fromkeys(
                [*normalized["reason_codes"], "MODEL_DISAGREEMENT"]
            ))[:8]
            normalized["evidence"]["model_disagreement"] = True
            normalized["evidence"]["disagreement_fields"] = list(
                routed.disagreement_fields
            )
        router.mark_downstream_action(result.request_id, "preus_review_pending_ingest")
        return {
            "signal_id": signal_id,
            "status": "OK",
            "model": result.model,
            "latency_ms": result.latency_ms,
            "router_request_id": result.request_id,
            "input_payload": payload,
            "assessment": normalized,
            "error_type": None,
        }
    except LLMRouterError as exc:
        return {
            "signal_id": signal_id,
            "status": "ERROR",
            "model": router.cfg.model(LLMTier.ANALYST).model_id,
            "latency_ms": 0.0,
            "router_request_id": None,
            "input_payload": payload,
            "assessment": {
                "verdict": "INSUFFICIENT_DATA",
                "confidence": 0.0,
                "requested_adjustment": 0.0,
                "reason_codes": ["OPENROUTER_PREUS_REQUEST_ERROR"],
                "short_rationale": "",
                "evidence": server_evidence,
            },
            "error_type": str(exc),
        }


def run_preus_openrouter_review(
    *, db: str | Path | None = None, now: datetime | None = None,
    force: bool = False, router: LLMRouter | None = None,
) -> dict[str, Any]:
    """Build, baseline, and optionally add advisory LLM context to a pre-US session.

    The deterministic baseline is always persisted before any network call.
    In advisory-only mode OpenRouter cannot overwrite that baseline, veto a
    trade, or write any Paper/live permission. Its structured assessment stays
    in the quality-agent evidence ledger for later evaluation.
    """
    moment = _utc(now)
    db_path = Path(db or load_config().db_path)
    preus_cfg = preus.load_cfg()
    agent_cfg = preus_cfg.get("llm_agent") or {}
    bundle = preus.select_candidates(db=db_path, now=moment, cfg=preus_cfg)
    handoff = preus.record_candidate_bundle(bundle, db=db_path, now=moment)
    saved_ids = set(_json_list(handoff.get("eligible_signal_ids_json")))
    candidates = [
        row for row in bundle.get("eligible", [])
        if str(row.get("signal_id") or "") in saved_ids
    ]
    current_ids = {str(row.get("signal_id") or "") for row in candidates}
    missing_saved_ids = sorted(saved_ids - current_ids)

    baseline = preus.record_baseline_revalidations(
        candidates, db=db_path, now=moment, cfg=preus_cfg,
    )
    if missing_saved_ids:
        excluded_by_id = {
            str(row.get("signal_id") or ""): str(row.get("reason") or "")
            for row in bundle.get("excluded", [])
        }
        preus.record_verdicts([
            {
                "signal_id": signal_id,
                "verdict": "BLOCK",
                "reason_codes": [
                    "PREUS_CANDIDATE_REVALIDATION_FAILED",
                    excluded_by_id.get(signal_id) or "NO_LONGER_ELIGIBLE",
                ],
                "evidence": {"server_revalidated": True},
                "model": "deterministic-preus-revalidation",
                "prompt_version": PROMPT_VERSION,
                "available_at": moment.isoformat(),
            }
            for signal_id in missing_saved_ids
        ], review_cycle="preus_openrouter", db=db_path, now=moment, cfg=preus_cfg)

    if not bool(agent_cfg.get("enabled", True)):
        health = preus.review_health(db=db_path, now=moment, cfg=preus_cfg)
        return {
            "status": "DISABLED",
            "reason": (
                "PREUS_OPENROUTER_AGENT_DISABLED"
                if not bool(agent_cfg.get("enabled", True)) else "LLM_ROUTER_DISABLED"
            ),
            "session_date": handoff.get("session_date"),
            "eligible": len(saved_ids),
            "reviewed": 0,
            "baseline_reviewed": len(baseline),
            "errors": 0,
            "health": health,
        }

    if not candidates:
        health = preus.review_health(db=db_path, now=moment, cfg=preus_cfg)
        return {
            "status": "OK" if not saved_ids else "DEGRADED",
            "session_date": handoff.get("session_date"),
            "eligible": len(saved_ids),
            "reviewed": 0,
            "baseline_reviewed": len(baseline),
            "errors": len(missing_saved_ids),
            "health": health,
        }

    try:
        llm = router or get_llm_router(db_path=db_path)
    except Exception as exc:
        health = preus.review_health(db=db_path, now=moment, cfg=preus_cfg)
        return {
            "status": "DEGRADED",
            "reason": str(exc),
            "session_date": handoff.get("session_date"),
            "eligible": len(candidates),
            "reviewed": 0,
            "baseline_reviewed": len(baseline),
            "errors": len(candidates),
            "health": health,
        }

    max_candidates = max(1, int(agent_cfg.get("max_candidates") or 10))
    # Spend analyst inference on the candidates where it can change the
    # hand-off. Promotable overnight plans lead, then the strongest remaining
    # A/B candidates; deterministic baseline coverage still includes all rows.
    ranked_candidates = sorted(
        candidates,
        key=lambda row: (
            int(bool(row.get("promotable"))),
            int(str(row.get("pre_gate_tier") or row.get("tier") or "").upper() in {"A", "B"}),
            float(row.get("base_score") or row.get("score") or 0.0),
            str(row.get("created_at") or ""),
        ),
        reverse=True,
    )
    experiment_pool = ranked_candidates[:max_candidates]
    ab_cfg = agent_cfg.get("ab_test") or {}
    experiment_enabled = bool(ab_cfg.get("enabled", False))
    experiment_name = str(ab_cfg.get("experiment_name") or "stocks_preus_gemini_v1")
    session_key = str(handoff.get("session_date") or moment.date().isoformat())
    assignments: dict[str, str] = {}
    if experiment_enabled:
        share = max(0.0, min(1.0, float(ab_cfg.get("treatment_share") or 0.5)))
        paid_cap = max(0, int(ab_cfg.get("max_paid_candidates") or 5))
        treatment_count = min(
            paid_cap,
            max(1, int(math.ceil(len(experiment_pool) * share))) if experiment_pool else 0,
        )
        metadata = {
            str(row.get("signal_id") or ""): {
                "rank": rank,
                "symbol": row.get("symbol"),
                "base_score": row.get("base_score") or row.get("score"),
                "promotable": bool(row.get("promotable")),
            }
            for rank, row in enumerate(experiment_pool, start=1)
        }
        with connect(db_path, timeout_seconds=30.0) as conn:
            assignments = assign_experiment_cohorts(
                conn,
                experiment_name=experiment_name,
                session_key=session_key,
                signal_ids=[str(row.get("signal_id") or "") for row in experiment_pool],
                treatment_count=treatment_count,
                assigned_at=moment,
                assignment_salt=str(ab_cfg.get("assignment_salt") or ""),
                metadata_by_signal=metadata,
            )
            conn.commit()
        candidates = [
            row for row in experiment_pool
            if assignments.get(str(row.get("signal_id") or "")) == "treatment"
        ]
    else:
        candidates = experiment_pool
    analyst_model = llm.cfg.model(LLMTier.ANALYST).model_id
    max_attempts = max(1, int(agent_cfg.get("max_attempts_per_candidate_per_session") or 2))
    calls: list[dict[str, Any]] = []
    pending: list[tuple[dict[str, Any], dict[str, Any], dict[str, Any]]] = []
    with connect(db_path, timeout_seconds=30.0) as conn:
        ensure_tables(conn)
        for candidate in candidates:
            payload, evidence = _candidate_input(
                conn, candidate, now=moment, preus_cfg=preus_cfg,
            )
            signal_id = str(candidate.get("signal_id") or "")
            if experiment_enabled:
                evidence = {
                    **evidence,
                    "llm_experiment": {
                        "name": experiment_name,
                        "session_key": session_key,
                        "cohort": "treatment",
                    },
                }
                payload = {**payload, "experiment": evidence["llm_experiment"]}
            target_key = f"{handoff.get('session_date')}:{signal_id}"
            cached = None if force else _cached_successful_assessment(
                conn,
                target_key=target_key,
                model=analyst_model,
                now=moment,
            )
            if cached is not None:
                calls.append({
                    "signal_id": signal_id,
                    "status": "OK",
                    "model": cached["model"],
                    "latency_ms": 0.0,
                    "router_request_id": None,
                    "input_payload": payload,
                    "assessment": cached["assessment"],
                    "error_type": None,
                    "reused": True,
                })
            elif not force and _failed_attempt_count(
                conn, target_key=target_key, model=analyst_model,
            ) >= max_attempts:
                calls.append({
                    "signal_id": signal_id,
                    "status": "ERROR",
                    "model": analyst_model,
                    "latency_ms": 0.0,
                    "router_request_id": None,
                    "input_payload": payload,
                    "assessment": {
                        "verdict": "INSUFFICIENT_DATA",
                        "confidence": 0.0,
                        "requested_adjustment": 0.0,
                        "reason_codes": ["OPENROUTER_PREUS_RETRY_BUDGET_EXHAUSTED"],
                        "short_rationale": "",
                        "evidence": evidence,
                    },
                    "error_type": "retry_budget_exhausted",
                    "retry_suppressed": True,
                })
            else:
                pending.append((candidate, payload, evidence))

    max_workers = max(1, min(6, int(agent_cfg.get("max_workers") or 3)))
    max_tokens = max(200, min(500, int(agent_cfg.get("max_tokens") or 400)))
    if pending:
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            futures = [
                pool.submit(
                    _call_one, router=llm, candidate=candidate,
                    payload=payload, server_evidence=evidence, max_tokens=max_tokens,
                )
                for candidate, payload, evidence in pending
            ]
            for future in as_completed(futures):
                calls.append(future.result())
    calls.sort(key=lambda item: item["signal_id"])

    ttl = timedelta(minutes=float(preus_cfg.get("review_ttl_minutes", 90)))
    provider = str(llm.cfg.raw.get("provider") or "openrouter")
    with connect(db_path, timeout_seconds=30.0) as conn:
        ensure_tables(conn)
        for call in calls:
            if call.get("reused") or call.get("retry_suppressed"):
                continue
            candidate = next(
                row for row in candidates
                if str(row.get("signal_id") or "") == call["signal_id"]
            )
            record_llm_assessment(
                conn,
                scope=SCOPE,
                target_key=f"{handoff.get('session_date')}:{call['signal_id']}",
                provider=provider,
                model=str(call.get("model") or llm.cfg.model(LLMTier.ANALYST).model_id),
                prompt_version=PROMPT_VERSION,
                status=str(call.get("status") or "ERROR"),
                assessment=call["assessment"],
                input_payload=call["input_payload"],
                created_at=moment,
                expires_at=moment + ttl,
                latency_ms=float(call.get("latency_ms") or 0.0),
                signal_id=call["signal_id"],
                asset_class="stocks",
                symbol=str(candidate.get("symbol") or ""),
                source="preus_candidate_bundle",
                error_type=call.get("error_type"),
            )
        conn.commit()

    successful = [row for row in calls if row["status"] == "OK"]
    verdict_items = [
        {
            "signal_id": row["signal_id"],
            "verdict": row["assessment"]["verdict"],
            "reason_codes": row["assessment"]["reason_codes"],
            "evidence": row["assessment"]["evidence"],
            "requested_adjustment": row["assessment"]["requested_adjustment"],
            "model": row["model"],
            "prompt_version": PROMPT_VERSION,
            "published_at": moment.isoformat(),
            "available_at": moment.isoformat(),
        }
        for row in successful
    ]
    advisory_only = bool(agent_cfg.get("advisory_only", True))
    ingested = [] if advisory_only else (
        preus.record_verdicts(
            verdict_items,
            review_cycle="preus_openrouter",
            db=db_path,
            now=moment,
            cfg=preus_cfg,
        ) if verdict_items else []
    )
    for row in successful:
        if row.get("router_request_id"):
            llm.mark_downstream_action(
                str(row["router_request_id"]),
                (
                    "preus_advisory_recorded_no_trading_effect"
                    if advisory_only else "preus_structured_verdict_ingested"
                ),
            )
    health = preus.review_health(db=db_path, now=moment, cfg=preus_cfg)
    errors = len(calls) - len(successful)
    error_types = sorted({
        str(row.get("error_type")) for row in calls if row.get("error_type")
    })
    budget_errors = sum(
        1 for row in calls if _is_budget_exhausted(row.get("error_type"))
    )
    if errors == 0:
        status = "OK"
    elif budget_errors == errors:
        status = "BUDGET_PAUSED"
    else:
        status = "DEGRADED"
    return {
        "status": status,
        "session_date": handoff.get("session_date"),
        "bundle_hash": content_hash(sorted(saved_ids)),
        "eligible": len(saved_ids),
        "submitted": len(pending),
        "reused": sum(1 for row in calls if row.get("reused")),
        "retry_suppressed": sum(
            1 for row in calls if row.get("retry_suppressed")
        ),
        "reviewed": len(successful),
        "baseline_reviewed": len(baseline),
        "experiment": experiment_name if experiment_enabled else None,
        "experiment_pool": len(experiment_pool),
        "treatment": sum(value == "treatment" for value in assignments.values()),
        "control": sum(value == "control" for value in assignments.values()),
        "baseline_only": max(0, len(saved_ids) - len(experiment_pool)),
        "ingested": len(ingested),
        "advisory_only": advisory_only,
        "errors": errors + len(missing_saved_ids),
        "error_types": error_types,
        "error": error_types[0] if error_types else None,
        "verdicts": {
            verdict: sum(
                1 for row in successful if row["assessment"]["verdict"] == verdict
            )
            for verdict in sorted(_ALLOWED_VERDICTS)
        },
        "health": health,
    }


__all__ = [
    "PROMPT_VERSION", "SCOPE", "SYSTEM_PROMPT", "run_preus_openrouter_review",
]
