from __future__ import annotations

import sqlite3
import time
from datetime import timedelta
from pathlib import Path
from typing import Any

from src.config import load_config

from .config import QualityAgentsConfig, load_quality_agents_config
from .helpers import make_verdict
from .post_trade_forensics_agent import PostTradeForensicsAgent
from .reducer import reduce_verdicts
from .registry import build_registry
from .schemas import AgentVerdict, SignalContext, Verdict, utc_now
from .store import (
    connect,
    ensure_tables,
    prune,
    record_reducer_decision,
    record_run_and_verdict,
    recover_execution_incident,
    upsert_execution_incident,
)


_WATCHDOG_INCIDENT_TYPES = {
    "stale_outbox": "ENTRY_WINDOW_EXPIRED",
    "stuck_processing": "EXECUTION_WORKER_STALLED",
    "position_reconcile_stale": "RECONCILIATION_STALE",
    "position_monitor_errors": "RECONCILIATION_ERROR",
    "position_tp_legs_incomplete": "PROTECTIVE_TPS_INCOMPLETE",
    "position_stop_missing": "PROTECTIVE_STOP_MISSING",
    "eligible_without_outbox": "OUTBOX_MISSING",
    "submitted_without_order": "ORDER_LEDGER_MISSING",
    "filled_without_position": "POSITION_LEDGER_MISSING",
    "active_risk_over_cap": "RISK_CAP_EXCEEDED",
    "current_reconcile_degraded": "RECONCILIATION_DEGRADED",
}


def record_watchdog_observations(
    conn: sqlite3.Connection, issues: list[dict[str, Any]],
) -> dict[str, int]:
    """Mirror objective post-ack defects into the agent evidence ledger.

    The live watchdog remains the sole alert owner. These rows are evidence for
    effectiveness/forensics and therefore must not create a second Telegram
    alert for the same stop, TP, ledger, or reconciliation problem.
    """
    ensure_tables(conn)
    active_keys: set[str] = set()
    recorded = 0
    for issue in issues:
        if issue.get("active", True) is False:
            continue
        raw_key = str(issue.get("key") or "").strip()
        prefix = raw_key.split(":", 1)[0]
        incident_type = _WATCHDOG_INCIDENT_TYPES.get(prefix)
        if incident_type is None:
            continue
        decision_id = str(issue.get("decision_id") or "").strip() or None
        signal_id = None
        symbol = str(issue.get("symbol") or "").strip() or None
        if decision_id:
            row = conn.execute(
                "SELECT signal_id,symbol FROM mexc_canary_decisions WHERE decision_id=?",
                (decision_id,),
            ).fetchone()
            if row:
                signal_id = str(row["signal_id"] or "").strip() or None
                symbol = symbol or (str(row["symbol"] or "").strip() or None)
        incident_key = f"live_post_ack:{raw_key}"
        active_keys.add(incident_key)
        upsert_execution_incident(
            conn,
            incident_key=incident_key,
            incident_type=incident_type,
            severity=str(issue.get("severity") or "WARNING"),
            stage="live_post_ack",
            signal_id=signal_id,
            decision_id=decision_id,
            symbol=symbol,
            objective=True,
            status="ACTIVE",
            detail={
                "watchdog_key": raw_key,
                "title": issue.get("title"),
                "detail": issue.get("detail"),
                "payload": issue.get("payload") or {},
            },
        )
        recorded += 1
    existing = conn.execute(
        "SELECT incident_key FROM quality_agent_execution_incidents "
        "WHERE stage='live_post_ack' AND status='ACTIVE'"
    ).fetchall()
    recovered = 0
    for row in existing:
        key = str(row["incident_key"])
        if key not in active_keys:
            recover_execution_incident(conn, key)
            recovered += 1
    return {"recorded": recorded, "recovered": recovered}


def evaluate_signal(
    signal: dict[str, Any],
    payload: dict[str, Any] | None = None,
    *,
    db: str | Path | None = None,
    stage: str = "live_capture",
    agent_names: set[str] | None = None,
    cfg: QualityAgentsConfig | None = None,
) -> dict[str, Any]:
    quality_cfg = cfg or load_quality_agents_config()
    context = SignalContext.from_records(signal, payload, stage=stage)
    if not quality_cfg.enabled:
        return {"status": "DISABLED", "signal_id": context.signal_id}
    if not context.signal_id:
        return {"status": "SKIPPED", "reason": "SIGNAL_ID_MISSING"}
    db_path = Path(db or load_config().db_path)
    with connect(db_path) as conn:
        result = evaluate_signal_on_connection(
            conn, signal, payload, stage=stage, agent_names=agent_names, cfg=quality_cfg,
        )
        conn.commit()
    return result


def evaluate_signal_on_connection(
    conn: sqlite3.Connection,
    signal: dict[str, Any],
    payload: dict[str, Any] | None = None,
    *,
    stage: str = "live_capture",
    agent_names: set[str] | None = None,
    cfg: QualityAgentsConfig | None = None,
) -> dict[str, Any]:
    quality_cfg = cfg or load_quality_agents_config()
    context = SignalContext.from_records(signal, payload, stage=stage)
    if not quality_cfg.enabled:
        return {"status": "DISABLED", "signal_id": context.signal_id}
    if not context.signal_id:
        return {"status": "SKIPPED", "reason": "SIGNAL_ID_MISSING"}
    verdict_rows: list[tuple[str, AgentVerdict]] = []
    errors: list[dict[str, str]] = []
    ensure_tables(conn)
    for agent in build_registry(quality_cfg, names=agent_names):
        started = utc_now()
        started_perf = time.perf_counter()
        error_type = None
        status = "OK"
        try:
            verdict = agent.evaluate(conn, context, quality_cfg)
        except Exception as exc:  # fail-open and preserve the evidence gap
            error_type = type(exc).__name__
            status = "ERROR"
            errors.append({"agent": agent.name, "error_type": error_type})
            verdict = make_verdict(
                name=agent.name, version=agent.version, verdict=Verdict.ERROR,
                confidence=0.0, reason_codes=["AGENT_EVALUATION_ERROR"],
                evidence={"error_type": error_type}, context=context, cfg=quality_cfg,
            )
        completed = utc_now()
        elapsed = max(0.0, time.perf_counter() - started_perf)
        if completed <= started:
            completed = started + timedelta(seconds=elapsed)
        _, verdict_id = record_run_and_verdict(
            conn, context=context, verdict=verdict, started_at=started,
            completed_at=completed, status=status, error_type=error_type,
        )
        verdict_rows.append((verdict_id, verdict))
        if agent.name == "execution_sanity":
            active_codes = {
                code for code in verdict.reason_codes
                if verdict.verdict == Verdict.BLOCK_HARD
            }
            existing = conn.execute(
                "SELECT incident_key,incident_type FROM quality_agent_execution_incidents "
                "WHERE signal_id=? AND stage=? AND status='ACTIVE'",
                (context.signal_id, context.stage),
            ).fetchall()
            for row in existing:
                if str(row["incident_type"]) not in active_codes:
                    recover_execution_incident(conn, str(row["incident_key"]))
            for code in active_codes:
                upsert_execution_incident(
                    conn,
                    incident_key=f"{context.stage}:{context.signal_id}:{code}",
                    incident_type=code,
                    severity="CRITICAL" if code in quality_cfg.hard_block_allowlist else "WARNING",
                    stage=context.stage,
                    signal_id=context.signal_id,
                    symbol=context.symbol,
                    objective=code in quality_cfg.hard_block_allowlist,
                    status="OBSERVED",
                    detail={"verdict_id": verdict_id, "evidence": verdict.evidence},
                )
    reduced = reduce_verdicts(verdict_rows, quality_cfg)
    reducer_id = record_reducer_decision(conn, context=context, decision=reduced)
    return {
        "status": "OK" if not errors else "DEGRADED",
        "signal_id": context.signal_id,
        "stage": context.stage,
        "reducer_decision_id": reducer_id,
        **reduced.as_dict(),
        "verdicts": [
            {"verdict_id": verdict_id, **verdict.output_payload()}
            for verdict_id, verdict in verdict_rows
        ],
        "errors": errors,
    }


def evaluate_preus_bundle(
    candidates: list[dict[str, Any]], *, db: str | Path | None = None,
) -> dict[str, Any]:
    db_path = Path(db or load_config().db_path)
    results: list[dict[str, Any]] = []
    with connect(db_path, timeout_seconds=30.0) as conn:
        for candidate in candidates:
            if not str(candidate.get("signal_id") or ""):
                continue
            results.append(evaluate_signal_on_connection(
                conn,
                {**candidate, "asset_class": "stocks", "mode": "intraday"},
                {"signal_id": candidate.get("signal_id")},
                stage="stocks_preus_candidate",
                agent_names={"news_entity", "event_risk", "market_regime"},
            ))
        conn.commit()
    return {
        "evaluated": len(results),
        "degraded": sum(1 for row in results if row.get("status") == "DEGRADED"),
        "actions": {
            action: sum(1 for row in results if row.get("recommended_action") == action)
            for action in sorted({str(row.get("recommended_action")) for row in results})
        },
    }


def refresh_post_trade_diagnostics(
    *, db: str | Path | None = None, cfg: QualityAgentsConfig | None = None,
) -> dict[str, Any]:
    quality_cfg = cfg or load_quality_agents_config()
    if not quality_cfg.agent_enabled("post_trade_forensics"):
        return {"status": "DISABLED"}
    db_path = Path(db or load_config().db_path)
    with connect(db_path, timeout_seconds=30.0) as conn:
        ensure_tables(conn)
        result = PostTradeForensicsAgent().refresh(conn)
        removed = prune(conn, quality_cfg.get("retention", {}) or {})
        conn.commit()
    return {"status": "OK", **result, "retention_removed": removed}


__all__ = [
    "evaluate_preus_bundle", "evaluate_signal", "evaluate_signal_on_connection",
    "record_watchdog_observations", "refresh_post_trade_diagnostics",
]
