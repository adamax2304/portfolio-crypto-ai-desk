from __future__ import annotations

import json
import sqlite3
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable

from .schemas import AgentVerdict, ReducedDecision, SignalContext, canonical_json, content_hash


DDL = """
CREATE TABLE IF NOT EXISTS quality_agent_runs (
  run_id TEXT PRIMARY KEY,
  agent_name TEXT NOT NULL,
  agent_version TEXT NOT NULL,
  scope TEXT NOT NULL,
  signal_id TEXT,
  started_at TEXT NOT NULL,
  completed_at TEXT NOT NULL,
  status TEXT NOT NULL,
  latency_ms REAL NOT NULL,
  error_type TEXT,
  input_hash TEXT NOT NULL,
  output_hash TEXT,
  model TEXT,
  prompt_version TEXT
);
CREATE INDEX IF NOT EXISTS idx_quality_agent_runs_time
  ON quality_agent_runs(agent_name, completed_at);
CREATE INDEX IF NOT EXISTS idx_quality_agent_runs_signal
  ON quality_agent_runs(signal_id, completed_at);

CREATE TABLE IF NOT EXISTS quality_agent_signal_verdicts (
  verdict_id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL UNIQUE,
  signal_id TEXT NOT NULL,
  asset_class TEXT NOT NULL,
  symbol TEXT NOT NULL,
  mode TEXT,
  entry_mode TEXT,
  stage TEXT NOT NULL,
  agent_name TEXT NOT NULL,
  agent_version TEXT NOT NULL,
  verdict TEXT NOT NULL,
  confidence REAL NOT NULL,
  reason_codes_json TEXT NOT NULL,
  evidence_json TEXT NOT NULL,
  created_at TEXT NOT NULL,
  expires_at TEXT NOT NULL,
  input_hash TEXT NOT NULL,
  output_hash TEXT NOT NULL,
  model TEXT,
  prompt_version TEXT,
  FOREIGN KEY(run_id) REFERENCES quality_agent_runs(run_id)
);
CREATE INDEX IF NOT EXISTS idx_quality_signal_latest
  ON quality_agent_signal_verdicts(signal_id, agent_name, created_at);
CREATE INDEX IF NOT EXISTS idx_quality_signal_outcome
  ON quality_agent_signal_verdicts(agent_name, verdict, created_at);

CREATE TABLE IF NOT EXISTS quality_agent_market_verdicts (
  market_verdict_id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL UNIQUE,
  signal_id TEXT,
  asset_class TEXT NOT NULL,
  market_mode TEXT,
  market_regime TEXT,
  verdict TEXT NOT NULL,
  confidence REAL NOT NULL,
  reason_codes_json TEXT NOT NULL,
  evidence_json TEXT NOT NULL,
  snapshot_at TEXT,
  created_at TEXT NOT NULL,
  expires_at TEXT NOT NULL,
  FOREIGN KEY(run_id) REFERENCES quality_agent_runs(run_id)
);
CREATE INDEX IF NOT EXISTS idx_quality_market_latest
  ON quality_agent_market_verdicts(asset_class, created_at);

CREATE TABLE IF NOT EXISTS quality_agent_execution_incidents (
  incident_id TEXT PRIMARY KEY,
  incident_key TEXT NOT NULL UNIQUE,
  decision_id TEXT,
  signal_id TEXT,
  symbol TEXT,
  stage TEXT NOT NULL,
  incident_type TEXT NOT NULL,
  severity TEXT NOT NULL,
  status TEXT NOT NULL,
  objective INTEGER NOT NULL DEFAULT 0,
  detail_json TEXT NOT NULL,
  first_seen_at TEXT NOT NULL,
  last_seen_at TEXT NOT NULL,
  recovered_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_quality_incidents_active
  ON quality_agent_execution_incidents(status, severity, last_seen_at);

CREATE TABLE IF NOT EXISTS quality_agent_reducer_decisions (
  reducer_decision_id TEXT PRIMARY KEY,
  signal_id TEXT NOT NULL,
  context_hash TEXT NOT NULL,
  stage TEXT NOT NULL,
  recommended_action TEXT NOT NULL,
  applied_action TEXT NOT NULL,
  operation_mode TEXT NOT NULL,
  reason_codes_json TEXT NOT NULL,
  verdict_ids_json TEXT NOT NULL,
  created_at TEXT NOT NULL,
  UNIQUE(signal_id, context_hash, stage)
);
CREATE INDEX IF NOT EXISTS idx_quality_reducer_signal
  ON quality_agent_reducer_decisions(signal_id, created_at);

CREATE TABLE IF NOT EXISTS quality_agent_post_trade_diagnostics (
  diagnostic_id TEXT PRIMARY KEY,
  signal_id TEXT NOT NULL,
  source_book TEXT NOT NULL,
  outcome_hash TEXT NOT NULL,
  asset_class TEXT,
  mode TEXT,
  entry_mode TEXT,
  outcome TEXT NOT NULL,
  result_r REAL,
  result_usdt REAL,
  primary_category TEXT NOT NULL,
  secondary_categories_json TEXT NOT NULL,
  evidence_json TEXT NOT NULL,
  agent_version TEXT NOT NULL,
  created_at TEXT NOT NULL,
  UNIQUE(signal_id, source_book, outcome_hash, agent_version)
);
CREATE INDEX IF NOT EXISTS idx_quality_post_trade_category
  ON quality_agent_post_trade_diagnostics(primary_category, created_at);

CREATE TABLE IF NOT EXISTS quality_agent_llm_assessments (
  assessment_id TEXT PRIMARY KEY,
  scope TEXT NOT NULL,
  target_key TEXT NOT NULL,
  signal_id TEXT,
  asset_class TEXT,
  symbol TEXT,
  source TEXT,
  provider TEXT NOT NULL,
  model TEXT NOT NULL,
  prompt_version TEXT NOT NULL,
  status TEXT NOT NULL,
  verdict TEXT,
  confidence REAL,
  reason_codes_json TEXT NOT NULL,
  assessment_json TEXT NOT NULL,
  input_hash TEXT NOT NULL,
  output_hash TEXT,
  error_type TEXT,
  latency_ms REAL NOT NULL,
  created_at TEXT NOT NULL,
  expires_at TEXT NOT NULL,
  UNIQUE(scope, target_key, input_hash, model, prompt_version)
);
CREATE INDEX IF NOT EXISTS idx_quality_llm_symbol_latest
  ON quality_agent_llm_assessments(asset_class, symbol, created_at);
CREATE INDEX IF NOT EXISTS idx_quality_llm_signal_latest
  ON quality_agent_llm_assessments(signal_id, created_at);
CREATE INDEX IF NOT EXISTS idx_quality_llm_target_latest
  ON quality_agent_llm_assessments(scope, target_key, created_at);

CREATE TABLE IF NOT EXISTS quality_agent_experiment_assignments (
  experiment_name TEXT NOT NULL,
  session_key TEXT NOT NULL,
  signal_id TEXT NOT NULL,
  cohort TEXT NOT NULL,
  assigned_at TEXT NOT NULL,
  metadata_json TEXT NOT NULL,
  PRIMARY KEY(experiment_name, session_key, signal_id)
);
CREATE INDEX IF NOT EXISTS idx_quality_experiment_signal
  ON quality_agent_experiment_assignments(signal_id, assigned_at);
CREATE INDEX IF NOT EXISTS idx_quality_experiment_session
  ON quality_agent_experiment_assignments(experiment_name, session_key, cohort);
"""


def connect(db: str | Path, *, timeout_seconds: float = 5.0) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db), timeout=max(0.0, timeout_seconds))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA busy_timeout=5000")
    return conn


def ensure_tables(conn: sqlite3.Connection) -> None:
    conn.executescript(DDL)


def table_exists(conn: sqlite3.Connection, table: str) -> bool:
    return bool(conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table,),
    ).fetchone())


def _stable_id(prefix: str, *parts: Any) -> str:
    body = ":".join(str(part or "") for part in parts)
    return f"{prefix}_{uuid.uuid5(uuid.NAMESPACE_URL, body).hex}"


def assign_experiment_cohorts(
    conn: sqlite3.Connection,
    *,
    experiment_name: str,
    session_key: str,
    signal_ids: list[str],
    treatment_count: int,
    assigned_at: datetime,
    assignment_salt: str = "",
    metadata_by_signal: dict[str, dict[str, Any]] | None = None,
) -> dict[str, str]:
    """Persist a stable, auditable treatment/control split for one session."""
    ensure_tables(conn)
    ordered_ids = list(dict.fromkeys(str(value) for value in signal_ids if value))
    if not ordered_ids:
        return {}
    placeholders = ",".join("?" for _ in ordered_ids)
    existing_rows = conn.execute(
        "SELECT signal_id,cohort FROM quality_agent_experiment_assignments "
        "WHERE experiment_name=? AND session_key=? "
        f"AND signal_id IN ({placeholders})",
        (experiment_name, session_key, *ordered_ids),
    ).fetchall()
    assignments = {str(row["signal_id"]): str(row["cohort"]) for row in existing_rows}
    target_treatment = max(0, min(len(ordered_ids), int(treatment_count)))
    treatment_left = max(
        0,
        target_treatment - sum(value == "treatment" for value in assignments.values()),
    )
    unassigned = [signal_id for signal_id in ordered_ids if signal_id not in assignments]
    unassigned.sort(key=lambda signal_id: content_hash({
        "experiment": experiment_name,
        "session": session_key,
        "signal_id": signal_id,
        "salt": assignment_salt,
    }))
    treatment_ids = set(unassigned[:treatment_left])
    metadata_by_signal = metadata_by_signal or {}
    for signal_id in unassigned:
        cohort = "treatment" if signal_id in treatment_ids else "control"
        conn.execute(
            "INSERT OR IGNORE INTO quality_agent_experiment_assignments(" 
            "experiment_name,session_key,signal_id,cohort,assigned_at,metadata_json) "
            "VALUES(?,?,?,?,?,?)",
            (
                experiment_name,
                session_key,
                signal_id,
                cohort,
                assigned_at.isoformat(),
                canonical_json(metadata_by_signal.get(signal_id) or {}),
            ),
        )
        assignments[signal_id] = cohort
    return {signal_id: assignments[signal_id] for signal_id in ordered_ids}


def record_run_and_verdict(
    conn: sqlite3.Connection,
    *,
    context: SignalContext,
    verdict: AgentVerdict,
    started_at: datetime,
    completed_at: datetime,
    status: str = "OK",
    error_type: str | None = None,
) -> tuple[str, str]:
    input_hash = context.input_hash
    run_id = _stable_id(
        "qarun", verdict.agent_name, verdict.agent_version, context.signal_id,
        context.stage, input_hash,
    )
    verdict_id = _stable_id("qav", run_id, verdict.output_hash)
    latency_ms = max(0.0, (completed_at - started_at).total_seconds() * 1000.0)
    conn.execute(
        "INSERT INTO quality_agent_runs(" 
        "run_id,agent_name,agent_version,scope,signal_id,started_at,completed_at,status,"
        "latency_ms,error_type,input_hash,output_hash,model,prompt_version) "
        "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT(run_id) DO UPDATE SET "
        "completed_at=excluded.completed_at,status=excluded.status,latency_ms=excluded.latency_ms,"
        "error_type=excluded.error_type,output_hash=excluded.output_hash",
        (
            run_id, verdict.agent_name, verdict.agent_version, context.stage,
            context.signal_id or None, started_at.isoformat(), completed_at.isoformat(),
            status, round(latency_ms, 3), error_type, input_hash, verdict.output_hash,
            verdict.model, verdict.prompt_version,
        ),
    )
    conn.execute(
        "INSERT INTO quality_agent_signal_verdicts(" 
        "verdict_id,run_id,signal_id,asset_class,symbol,mode,entry_mode,stage,agent_name,"
        "agent_version,verdict,confidence,reason_codes_json,evidence_json,created_at,expires_at,"
        "input_hash,output_hash,model,prompt_version) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) "
        "ON CONFLICT(verdict_id) DO UPDATE SET expires_at=excluded.expires_at,"
        "evidence_json=excluded.evidence_json,confidence=excluded.confidence",
        (
            verdict_id, run_id, context.signal_id, context.asset_class, context.symbol,
            context.mode, context.entry_mode, context.stage, verdict.agent_name,
            verdict.agent_version, verdict.verdict.value, verdict.confidence,
            canonical_json(list(verdict.reason_codes)), canonical_json(verdict.evidence),
            verdict.created_at.isoformat(), verdict.expires_at.isoformat(), input_hash,
            verdict.output_hash, verdict.model, verdict.prompt_version,
        ),
    )
    if verdict.agent_name == "market_regime":
        evidence = verdict.evidence
        market_id = _stable_id("qamkt", verdict_id)
        conn.execute(
            "INSERT INTO quality_agent_market_verdicts(" 
            "market_verdict_id,run_id,signal_id,asset_class,market_mode,market_regime,verdict,"
            "confidence,reason_codes_json,evidence_json,snapshot_at,created_at,expires_at) "
            "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT(market_verdict_id) DO UPDATE SET "
            "evidence_json=excluded.evidence_json,expires_at=excluded.expires_at",
            (
                market_id, run_id, context.signal_id, context.asset_class,
                evidence.get("market_mode"), evidence.get("market_regime"),
                verdict.verdict.value, verdict.confidence,
                canonical_json(list(verdict.reason_codes)), canonical_json(evidence),
                evidence.get("snapshot_at"), verdict.created_at.isoformat(),
                verdict.expires_at.isoformat(),
            ),
        )
    return run_id, verdict_id


def record_reducer_decision(
    conn: sqlite3.Connection,
    *,
    context: SignalContext,
    decision: ReducedDecision,
) -> str:
    reducer_id = _stable_id("qared", context.signal_id, context.stage, context.input_hash)
    conn.execute(
        "INSERT INTO quality_agent_reducer_decisions(" 
        "reducer_decision_id,signal_id,context_hash,stage,recommended_action,applied_action,"
        "operation_mode,reason_codes_json,verdict_ids_json,created_at) VALUES(?,?,?,?,?,?,?,?,?,?) "
        "ON CONFLICT(signal_id,context_hash,stage) DO UPDATE SET "
        "recommended_action=excluded.recommended_action,applied_action=excluded.applied_action,"
        "reason_codes_json=excluded.reason_codes_json,verdict_ids_json=excluded.verdict_ids_json,"
        "created_at=excluded.created_at",
        (
            reducer_id, context.signal_id, context.input_hash, context.stage,
            decision.recommended_action.value, decision.applied_action.value,
            decision.operation_mode, canonical_json(list(decision.reason_codes)),
            canonical_json(list(decision.verdict_ids)), decision.created_at.isoformat(),
        ),
    )
    return reducer_id


def upsert_execution_incident(
    conn: sqlite3.Connection,
    *,
    incident_key: str,
    incident_type: str,
    severity: str,
    stage: str,
    detail: dict[str, Any],
    signal_id: str | None = None,
    decision_id: str | None = None,
    symbol: str | None = None,
    objective: bool = False,
    status: str = "ACTIVE",
    now: datetime | None = None,
) -> str:
    moment = (now or datetime.now(timezone.utc)).isoformat()
    status_value = str(status or "ACTIVE").upper()
    if status_value not in {"ACTIVE", "OBSERVED", "RECOVERED"}:
        raise ValueError("invalid execution incident status")
    incident_id = _stable_id("qainc", incident_key)
    conn.execute(
        "INSERT INTO quality_agent_execution_incidents(" 
        "incident_id,incident_key,decision_id,signal_id,symbol,stage,incident_type,severity,status,"
        "objective,detail_json,first_seen_at,last_seen_at,recovered_at) "
        "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,NULL) ON CONFLICT(incident_key) DO UPDATE SET "
        "decision_id=excluded.decision_id,signal_id=excluded.signal_id,symbol=excluded.symbol,"
        "stage=excluded.stage,incident_type=excluded.incident_type,severity=excluded.severity,"
        "status=excluded.status,objective=excluded.objective,detail_json=excluded.detail_json,"
        "last_seen_at=excluded.last_seen_at,recovered_at=excluded.recovered_at",
        (
            incident_id, incident_key, decision_id, signal_id, symbol, stage,
            incident_type, severity.upper(), status_value, int(bool(objective)),
            canonical_json(detail), moment, moment,
        ),
    )
    return incident_id


def recover_execution_incident(
    conn: sqlite3.Connection, incident_key: str, *, now: datetime | None = None,
) -> None:
    moment = (now or datetime.now(timezone.utc)).isoformat()
    conn.execute(
        "UPDATE quality_agent_execution_incidents SET status='RECOVERED',last_seen_at=?,"
        "recovered_at=? WHERE incident_key=? AND status='ACTIVE'",
        (moment, moment, incident_key),
    )


def record_post_trade_diagnostic(
    conn: sqlite3.Connection,
    *,
    signal_id: str,
    source_book: str,
    outcome_payload: dict[str, Any],
    asset_class: str | None,
    mode: str | None,
    entry_mode: str | None,
    outcome: str,
    result_r: float | None,
    result_usdt: float | None,
    primary_category: str,
    secondary_categories: Iterable[str],
    evidence: dict[str, Any],
    agent_version: str,
    created_at: datetime | None = None,
) -> str:
    outcome_hash = content_hash(outcome_payload)
    diagnostic_id = _stable_id(
        "qapost", signal_id, source_book, outcome_hash, agent_version,
    )
    moment = (created_at or datetime.now(timezone.utc)).isoformat()
    # A recomputed Paper/live outcome replaces the previous diagnosis for the
    # same agent version. Keeping every intermediate outcome hash would double
    # count one trade in effectiveness reports and grow the main database on
    # every accounting refresh.
    conn.execute(
        "DELETE FROM quality_agent_post_trade_diagnostics "
        "WHERE signal_id=? AND source_book=? AND agent_version=? AND outcome_hash<>?",
        (signal_id, source_book, agent_version, outcome_hash),
    )
    conn.execute(
        "INSERT INTO quality_agent_post_trade_diagnostics(" 
        "diagnostic_id,signal_id,source_book,outcome_hash,asset_class,mode,entry_mode,outcome,"
        "result_r,result_usdt,primary_category,secondary_categories_json,evidence_json,"
        "agent_version,created_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) "
        "ON CONFLICT(signal_id,source_book,outcome_hash,agent_version) DO UPDATE SET "
        "primary_category=excluded.primary_category,secondary_categories_json=excluded.secondary_categories_json,"
        "evidence_json=excluded.evidence_json,created_at=excluded.created_at",
        (
            diagnostic_id, signal_id, source_book, outcome_hash, asset_class, mode,
            entry_mode, outcome, result_r, result_usdt, primary_category,
            canonical_json(list(secondary_categories)), canonical_json(evidence),
            agent_version, moment,
        ),
    )
    return diagnostic_id


def record_llm_assessment(
    conn: sqlite3.Connection,
    *,
    scope: str,
    target_key: str,
    provider: str,
    model: str,
    prompt_version: str,
    status: str,
    assessment: dict[str, Any],
    input_payload: dict[str, Any],
    created_at: datetime,
    expires_at: datetime,
    latency_ms: float,
    signal_id: str | None = None,
    asset_class: str | None = None,
    symbol: str | None = None,
    source: str | None = None,
    error_type: str | None = None,
) -> str:
    input_hash = content_hash(input_payload)
    output_hash = content_hash(assessment) if assessment else None
    assessment_id = _stable_id(
        "qallm", scope, target_key, input_hash, model, prompt_version,
    )
    verdict = str(assessment.get("verdict") or "").upper() or None
    confidence_raw = assessment.get("confidence")
    try:
        confidence = None if confidence_raw in (None, "") else float(confidence_raw)
    except (TypeError, ValueError):
        confidence = None
    conn.execute(
        "INSERT INTO quality_agent_llm_assessments("
        "assessment_id,scope,target_key,signal_id,asset_class,symbol,source,provider,model,"
        "prompt_version,status,verdict,confidence,reason_codes_json,assessment_json,"
        "input_hash,output_hash,error_type,latency_ms,created_at,expires_at"
        ") VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) "
        "ON CONFLICT(scope,target_key,input_hash,model,prompt_version) DO UPDATE SET "
        "status=excluded.status,verdict=excluded.verdict,confidence=excluded.confidence,"
        "reason_codes_json=excluded.reason_codes_json,assessment_json=excluded.assessment_json,"
        "output_hash=excluded.output_hash,error_type=excluded.error_type,"
        "latency_ms=excluded.latency_ms,created_at=excluded.created_at,expires_at=excluded.expires_at",
        (
            assessment_id, scope, target_key, signal_id, asset_class, symbol, source,
            provider, model, prompt_version, status.upper(), verdict, confidence,
            canonical_json(list(assessment.get("reason_codes") or [])),
            canonical_json(assessment), input_hash, output_hash, error_type,
            round(max(0.0, float(latency_ms)), 3), created_at.isoformat(),
            expires_at.isoformat(),
        ),
    )
    return assessment_id


def latest_llm_assessments(
    conn: sqlite3.Connection,
    *,
    signal_id: str | None,
    asset_class: str,
    symbol: str,
    decision_at: datetime,
    limit: int = 5,
) -> list[dict[str, Any]]:
    if not table_exists(conn, "quality_agent_llm_assessments"):
        return []
    params: list[Any] = [
        decision_at.isoformat(), decision_at.isoformat(),
        asset_class.lower(), symbol.upper(),
    ]
    signal_clause = ""
    if signal_id:
        signal_clause = " OR signal_id=?"
        params.append(signal_id)
    params.append(max(1, int(limit)))
    rows = conn.execute(
        "SELECT * FROM quality_agent_llm_assessments "
        "WHERE status='OK' AND created_at<=? AND expires_at>=? "
        f"AND ((LOWER(asset_class)=? AND UPPER(symbol)=?){signal_clause}) "
        "ORDER BY CASE WHEN signal_id IS NOT NULL AND signal_id<>'' THEN 0 ELSE 1 END,"
        "created_at DESC LIMIT ?",
        tuple(params),
    ).fetchall()
    return [dict(row) for row in rows]


def prune(conn: sqlite3.Connection, retention: dict[str, Any]) -> dict[str, int]:
    now = datetime.now(timezone.utc)
    specs = (
        ("quality_agent_runs", "completed_at", "runs_days", 30),
        ("quality_agent_signal_verdicts", "created_at", "signal_verdict_days", 180),
        ("quality_agent_market_verdicts", "created_at", "market_verdict_days", 90),
        ("quality_agent_reducer_decisions", "created_at", "reducer_days", 180),
        ("quality_agent_post_trade_diagnostics", "created_at", "post_trade_days", 730),
        ("quality_agent_llm_assessments", "created_at", "llm_assessment_days", 180),
        (
            "quality_agent_experiment_assignments", "assigned_at",
            "experiment_assignment_days", 365,
        ),
    )
    removed: dict[str, int] = {}
    for table, column, key, default in specs:
        days = max(1, int(retention.get(key, default)))
        cutoff = (now - timedelta(days=days)).isoformat()
        cur = conn.execute(f"DELETE FROM {table} WHERE {column}<?", (cutoff,))
        removed[table] = max(0, int(cur.rowcount or 0))
    days = max(1, int(retention.get("resolved_incident_days", 90)))
    cutoff = (now - timedelta(days=days)).isoformat()
    cur = conn.execute(
        "DELETE FROM quality_agent_execution_incidents "
        "WHERE (status='RECOVERED' AND recovered_at<?) "
        "OR (status='OBSERVED' AND last_seen_at<?)", (cutoff, cutoff),
    )
    removed["quality_agent_execution_incidents"] = max(0, int(cur.rowcount or 0))
    return removed
