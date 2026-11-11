"""Pre-US deterministic hand-off plus optional advisory LLM context.

Runs from the autonomous ``stocks_preus_openrouter_review`` scheduled task (the
same packet/ingest pattern as ``src/stocks/intraday_llm_review.py``'s SI-6
flow. The deterministic baseline is authoritative; configured external model
reviews are stored elsewhere as advisory evidence and cannot alter it. Two
core entry points:

  * ``select_candidates`` — deterministic code builds the eligible/excluded
    candidate bundle for the LLM to read. All hard-gate exclusions (legal,
    earnings, stale context, unresolved catalyst, expired catalyst, risk-guard
    block) are decided here, in code — the LLM never decides an exclusion.
  * ``record_verdict`` — deterministic code ingests ONE deterministic verdict.
    All numeric enforcement (adjustment clamp, hard-block re-check, score
    clamp, tier recompute via ``src.signals.tier_policy.tier_from_score``,
    TTL, idempotency) happens here — the LLM supplies only a verdict enum,
    reason codes, and evidence text.

Invariants (never violated by this module):
  * Never writes to ``proposed_signals``, ``signal_outcomes``, any Paper
    ledger table, or anything under ``src/live_execution``.
  * Never assigns a tier directly — tier is always recomputed from
    ``review_adjusted_score`` by the shared threshold function.
  * A C-tier signal is only ever eligible for promotion when its funnel state
    is ``PREOPEN_PLAN`` (pre-gate tier A/B, demoted ONLY for
    ``market_closed_intraday_planning_only``) — a substantively-rejected C
    (``REJECTED_AT_DECISION``) can never receive a positive adjustment path.
  * All timestamps are point-in-time: ``published_at`` / ``ingested_at`` /
    ``available_at`` / ``reviewed_at`` / ``review_expires_at`` are recorded,
    never backdated or inferred after the fact.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from src.config import load_config
from src.signals.tier_policy import tier_from_score
from src.stocks.paper_funnel import PLAN_MARKER

VERSION = "stocks_preus_review_v1"
ACTIONABILITY_VERSION = "stocks_preus_actionability_v2"
REVIEW_HEALTH_VERSION = "stocks_preus_review_health_v1"
BASELINE_REVIEW_MODEL = "deterministic-preus-baseline"
NY = ZoneInfo("America/New_York")

VERDICTS = ("SUPPORT", "NEUTRAL", "CAUTION", "BLOCK", "INSUFFICIENT_DATA")

# Candidate-selection exclusion reason enum (spec: "для каждого исключённого
# кандидата сохранить понятный enum reason").
EXCLUDE_LEGAL_RISK = "LEGAL_RISK"
EXCLUDE_EARNINGS_BLACKOUT = "EARNINGS_BLACKOUT"
EXCLUDE_STALE_MARKET_CONTEXT = "STALE_MARKET_CONTEXT"
EXCLUDE_NO_ENTITY_RESOLVED_CATALYST = "NO_ENTITY_RESOLVED_CATALYST"
EXCLUDE_UNCONFIRMED_TICKER_OR_CONFLICT = "UNCONFIRMED_TICKER_OR_ENTITY_CONFLICT"
EXCLUDE_EXPIRED_CATALYST = "EXPIRED_CATALYST"
EXCLUDE_HARD_RISK_GUARD_BLOCK = "HARD_RISK_GUARD_BLOCK"
EXCLUDE_TERMINAL_OR_EXPIRED = "TERMINAL_OR_EXPIRED_PLAN"
EXCLUDE_STALE_PLAN = "STALE_PLAN_TOO_OLD"
EXCLUDE_INVALID_GEOMETRY = "INVALID_ENTRY_GEOMETRY"
EXCLUDE_DATA_ERROR = "DATA_ERROR_FAIL_CONSERVATIVE"

_ACTIVE_STATUSES = ("generated", "waiting_for_entry", "triggered")

_DEFAULTS: dict[str, Any] = {
    "enabled": True,
    "max_candidate_age_hours": 20,
    "review_ttl_minutes": 90,
    "block_ttl_minutes": 240,
    # The short pre-US handoff is intentionally separate from the full
    # enriched review. It starts at 08:50 ET and leaves a structured,
    # ingestible verdict before the 09:15 ET Paper decision window.
    "review_target_et": "08:50",
    "review_deadline_et": "09:12",
    "review_freshness_minutes": 30,
    "adjustments": {
        "SUPPORT": {"min": 0, "max": 5},
        "NEUTRAL": {"min": 0, "max": 0},
        "CAUTION": {"min": -7, "max": -3},
        "INSUFFICIENT_DATA": {"min": 0, "max": 0},
    },
    "score_floor": 0,
    "score_ceiling": 100,
    "support_requires": [
        "catalyst_entity_resolved", "catalyst_fresh", "market_context_fresh",
        "no_hard_cap", "relative_strength_confirmed",
    ],
    "catalyst_max_age_hours": 24,
    "market_context_max_age_minutes": 45,
    "llm_agent": {
        "enabled": True,
        "advisory_only": True,
        "apply_to_score": False,
        "apply_to_actionability": False,
        "max_candidates": 10,
        "ab_test": {
            "enabled": True,
            "experiment_name": "stocks_preus_gemini_v1",
            "treatment_share": 0.50,
            "max_paid_candidates": 5,
            "assignment_salt": "preus-gemini-v1",
        },
        "max_workers": 3,
        "max_tokens": 400,
    },
}

_DDL = """
CREATE TABLE IF NOT EXISTS stocks_preus_review (
  signal_id TEXT PRIMARY KEY,
  symbol TEXT NOT NULL,
  base_score REAL NOT NULL,
  review_score_adjustment REAL NOT NULL,
  review_adjusted_score REAL NOT NULL,
  review_verdict TEXT NOT NULL,
  review_tier TEXT NOT NULL,
  review_reason_codes_json TEXT NOT NULL,
  review_evidence_json TEXT NOT NULL,
  published_at TEXT,
  ingested_at TEXT,
  available_at TEXT,
  reviewed_at TEXT NOT NULL,
  review_expires_at TEXT NOT NULL,
  review_model TEXT,
  review_prompt_version TEXT,
  review_cycle TEXT,
  version TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_stocks_preus_review_expires
ON stocks_preus_review(review_expires_at);

CREATE TABLE IF NOT EXISTS stocks_preus_review_blocks (
  signal_id TEXT PRIMARY KEY,
  symbol TEXT NOT NULL,
  blocked_at TEXT NOT NULL,
  block_expires_at TEXT NOT NULL,
  reason_codes_json TEXT NOT NULL,
  evidence_json TEXT NOT NULL,
  review_model TEXT,
  review_prompt_version TEXT,
  review_cycle TEXT,
  version TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS stocks_preus_actionability (
  signal_id TEXT PRIMARY KEY,
  target_session_open_at TEXT NOT NULL,
  target_session_close_at TEXT NOT NULL,
  evaluated_at TEXT NOT NULL,
  decision TEXT NOT NULL,
  effective_score REAL,
  effective_tier TEXT,
  reason_codes_json TEXT NOT NULL,
  review_expires_at TEXT,
  valid_until TEXT,
  current_signal_updated_at TEXT,
  source_fingerprint TEXT,
  geometry_json TEXT NOT NULL,
  reactivated INTEGER NOT NULL DEFAULT 0,
  version TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_stocks_preus_actionability_valid
ON stocks_preus_actionability(decision, valid_until);

CREATE TABLE IF NOT EXISTS stocks_preus_review_bundles (
  session_date TEXT PRIMARY KEY,
  generated_at TEXT NOT NULL,
  eligible_signal_ids_json TEXT NOT NULL,
  excluded_count INTEGER NOT NULL,
  status TEXT NOT NULL,
  version TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS stocks_preus_review_health (
  session_date TEXT PRIMARY KEY,
  checked_at TEXT NOT NULL,
  eligible_count INTEGER NOT NULL,
  reviewed_count INTEGER NOT NULL,
  missing_count INTEGER NOT NULL,
  status TEXT NOT NULL,
  reason TEXT,
  alerted_at TEXT,
  version TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS stocks_preus_review_health_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_date TEXT NOT NULL,
  checked_at TEXT NOT NULL,
  eligible_count INTEGER NOT NULL,
  reviewed_count INTEGER NOT NULL,
  missing_count INTEGER NOT NULL,
  status TEXT NOT NULL,
  reason TEXT,
  alerted_at TEXT,
  version TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_stocks_preus_review_health_history_session
ON stocks_preus_review_health_history(session_date, checked_at);

CREATE TABLE IF NOT EXISTS stocks_preus_actionability_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  signal_id TEXT NOT NULL,
  target_session_open_at TEXT NOT NULL,
  target_session_close_at TEXT NOT NULL,
  evaluated_at TEXT NOT NULL,
  decision TEXT NOT NULL,
  effective_score REAL,
  effective_tier TEXT,
  reason_codes_json TEXT NOT NULL,
  review_expires_at TEXT,
  valid_until TEXT,
  current_signal_updated_at TEXT,
  source_fingerprint TEXT,
  geometry_json TEXT NOT NULL,
  reactivated INTEGER NOT NULL DEFAULT 0,
  snapshot_json TEXT NOT NULL,
  version TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_stocks_preus_actionability_history_signal
ON stocks_preus_actionability_history(signal_id, evaluated_at);
CREATE INDEX IF NOT EXISTS idx_stocks_preus_actionability_history_decision
ON stocks_preus_actionability_history(decision, evaluated_at);
"""


def _utc(value: datetime | None = None) -> datetime:
    moment = value or datetime.now(timezone.utc)
    return moment.replace(tzinfo=timezone.utc) if moment.tzinfo is None else moment.astimezone(timezone.utc)


def _iso(value: datetime | None = None) -> str:
    return _utc(value).isoformat()


def _parse(value: Any) -> datetime | None:
    if isinstance(value, datetime):
        return _utc(value)
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return _utc(parsed)
    except (TypeError, ValueError):
        return None


def _json_obj(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return dict(value)
    try:
        decoded = json.loads(value or "{}")
        return decoded if isinstance(decoded, dict) else {}
    except (TypeError, ValueError, json.JSONDecodeError):
        return {}


def load_cfg(project_root: Path | None = None) -> dict[str, Any]:
    """Load `preus_review` from config/stocks/preus_review.yaml. Fails safe to
    the conservative built-in defaults (never disables hard gates)."""
    cfg = json.loads(json.dumps(_DEFAULTS))  # deep copy
    try:
        from src.config import load_yaml
        root = project_root or load_config().root
        raw = load_yaml(Path(root) / "config" / "stocks" / "preus_review.yaml") or {}
        section = raw.get("preus_review") or {}
        if isinstance(section, dict):
            for key, value in section.items():
                if key == "adjustments" and isinstance(value, dict):
                    cfg["adjustments"].update(value)
                else:
                    cfg[key] = value
    except Exception:
        pass
    return cfg


def ensure_tables(conn: sqlite3.Connection) -> None:
    # This module is hit by the one-minute stocks monitor.  Re-running even
    # `CREATE TABLE IF NOT EXISTS` takes a schema/write lock in SQLite, which
    # made a read-model health check contend with active execution writers.
    # Only acquire that lock when an install/migration is actually required.
    required = {
        "stocks_preus_review",
        "stocks_preus_review_blocks",
        "stocks_preus_actionability",
        "stocks_preus_review_bundles",
        "stocks_preus_review_health",
        "stocks_preus_review_health_history",
        "stocks_preus_actionability_history",
    }
    existing = {
        str(row[0]) for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
    }
    actionability_columns = _table_columns(conn, "stocks_preus_actionability")
    if required.issubset(existing) and "source_fingerprint" in actionability_columns:
        # Older databases pre-date the global bounded-news index. Create it
        # once here so the 08:50 ET pre-US path cannot scan the whole archive.
        try:
            news_indexes = {
                str(row[1]) for row in conn.execute("PRAGMA index_list(news_items)")
            }
            if "idx_news_items_published_at" not in news_indexes:
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_news_items_published_at "
                    "ON news_items(published_at)"
                )
        except sqlite3.OperationalError:
            # A minimal/test DB may not include the shared news table.
            pass
        return
    conn.executescript(_DDL)
    actionability_columns = _table_columns(conn, "stocks_preus_actionability")
    if "source_fingerprint" not in actionability_columns:
        conn.execute(
            "ALTER TABLE stocks_preus_actionability "
            "ADD COLUMN source_fingerprint TEXT"
        )


def _table_columns(conn: sqlite3.Connection, table: str) -> set[str]:
    try:
        return {str(row[1]) for row in conn.execute(f"PRAGMA table_info({table})")}
    except sqlite3.OperationalError:
        return set()


def _snapshot_for_signal(conn: sqlite3.Connection, signal_id: str) -> dict[str, Any]:
    columns = _table_columns(conn, "stocks_paper_decision_snapshots")
    if not columns:
        return {}
    wanted = [
        name for name in (
            "signal_id", "funnel_state", "pre_gate_tier", "signal_created_at",
            "decision_at", "target_session_open_at", "target_session_close_at",
            "snapshot_json",
        ) if name in columns
    ]
    if not wanted:
        return {}
    row = conn.execute(
        f"SELECT {','.join(wanted)} FROM stocks_paper_decision_snapshots WHERE signal_id=?",
        (signal_id,),
    ).fetchone()
    return dict(row) if row is not None else {}


def _session_cap_only(row: dict[str, Any], snapshot: dict[str, Any]) -> tuple[bool, str]:
    snap_payload = _json_obj(snapshot.get("snapshot_json"))
    cap_reasons = [
        str(value) for value in (
            snap_payload.get("cap_reasons") or _cap_reasons(row)
        ) if value
    ]
    pre_gate = str(
        snapshot.get("pre_gate_tier")
        or snap_payload.get("pre_gate_tier")
        or _pre_gate_tier(row)
        or ""
    ).upper()
    has_marker = any(PLAN_MARKER in reason for reason in cap_reasons)
    substantive = [
        reason for reason in cap_reasons
        if PLAN_MARKER not in reason and not reason.lower().startswith("tier demoted")
    ]
    state = str(snapshot.get("funnel_state") or "")
    valid = (
        pre_gate in {"A", "B"}
        and not substantive
        and (state == "PREOPEN_PLAN" or has_marker)
    )
    return valid, pre_gate


def _target_session(row: dict[str, Any], snapshot: dict[str, Any]) -> tuple[datetime, datetime] | None:
    anchor = _parse(
        snapshot.get("signal_created_at")
        or snapshot.get("decision_at")
        or row.get("created_at")
    )
    if anchor is None:
        return None
    try:
        from src.stocks.market_calendar import stock_intraday_target_session
        return stock_intraday_target_session(anchor)
    except Exception:
        return None


def _geometry(row: dict[str, Any]) -> dict[str, Any]:
    return {
        key: row.get(key) for key in (
            "entry_low", "entry_high", "entry_trigger", "suggested_entry",
            "stop_loss", "invalidation", "tp1", "tp2", "tp3",
        )
    }


def source_decision_fingerprint(row: dict[str, Any]) -> str:
    """Hash only decision-relevant source fields for a pre-US permission.

    `proposed_signals.updated_at` is also touched by harmless lifecycle and
    reporting work. Treating that timestamp as a trading-input change caused
    valid plans to be rejected at the open. This fingerprint intentionally
    ignores status/timestamps and covers the actual decision geometry instead.
    """
    def number(value: Any) -> float | None:
        try:
            return round(float(value), 8)
        except (TypeError, ValueError):
            return None

    payload = {
        "version": 2,
        "symbol": str(row.get("symbol") or "").upper(),
        "direction": str(row.get("direction") or "").lower(),
        "setup_type": str(row.get("setup_type") or "").lower(),
        "geometry": {key: number(value) for key, value in _geometry(row).items()},
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


_ACTIONABILITY_HISTORY_COLS = (
    "signal_id", "target_session_open_at", "target_session_close_at", "evaluated_at",
    "decision", "effective_score", "effective_tier", "reason_codes_json",
    "review_expires_at", "valid_until", "current_signal_updated_at",
    "source_fingerprint", "geometry_json", "reactivated", "snapshot_json", "version",
)


def _record_actionability_history(
    conn: sqlite3.Connection,
    payload: dict[str, Any],
    *,
    row: dict[str, Any],
    snapshot: dict[str, Any],
    session_cap_only: bool,
    pre_gate_tier: str,
    reasons: list[str],
) -> None:
    """Append the point-in-time decision before the materialized row expires.

    `stocks_preus_actionability` is intentionally a current permission table:
    after the window it becomes BLOCKED/expired. This history table preserves
    what was true at the decision moment so later MEXC Paper fills cannot look
    contradictory in audits.
    """
    raw = _json_obj(row.get("raw_idea_json"))
    context = {
        "source_signal": {
            "signal_id": row.get("signal_id"),
            "symbol": row.get("symbol"),
            "direction": row.get("direction"),
            "mode": row.get("mode"),
            "status": row.get("status"),
            "tier": row.get("tier"),
            "score": row.get("score"),
            "setup_type": row.get("setup_type"),
            "created_at": row.get("created_at"),
            "updated_at": row.get("updated_at"),
            "pre_gate_tier": pre_gate_tier,
            "cap_reasons": _cap_reasons(row),
        },
        "funnel_snapshot": {
            "signal_id": snapshot.get("signal_id"),
            "funnel_state": snapshot.get("funnel_state"),
            "pre_gate_tier": snapshot.get("pre_gate_tier"),
            "signal_created_at": snapshot.get("signal_created_at"),
            "decision_at": snapshot.get("decision_at"),
        },
        "raw_context": {
            "structured": raw.get("structured"),
            "setup": raw.get("setup"),
            "intraday_actionability": raw.get("intraday_actionability"),
            "catalyst_meta": raw.get("catalyst_meta"),
            "paper_entry_profile": raw.get("paper_entry_profile"),
            "paper_entry_confirmation": raw.get("paper_entry_confirmation"),
        },
        "session_cap_only": session_cap_only,
        "reasons": sorted(set(reasons)),
    }
    values = dict(payload)
    values["snapshot_json"] = json.dumps(context, sort_keys=True)
    conn.execute(
        "INSERT INTO stocks_preus_actionability_history("
        + ",".join(_ACTIONABILITY_HISTORY_COLS)
        + ") VALUES ("
        + ",".join("?" for _ in _ACTIONABILITY_HISTORY_COLS)
        + ")",
        tuple(values.get(column) for column in _ACTIONABILITY_HISTORY_COLS),
    )


def refresh_actionability(
    db: str | Path | None = None,
    *,
    now: datetime | None = None,
    cfg: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Materialize the bounded Paper permission for reviewed pre-open plans.

    This remains a review/read-model write: it never changes the source
    signal, execution accounting, Paper ledger, or live routing. The monitor
    consumes only fresh ``ACTIONABLE`` rows from this table.
    """
    cfg = cfg or load_cfg()
    moment = _utc(now)
    path = Path(db or load_config().db_path)
    rows_out: list[dict[str, Any]] = []
    lookback_hours = float(cfg.get("actionability_refresh_lookback_hours", 48))
    since = moment - timedelta(hours=max(1.0, lookback_hours))
    with sqlite3.connect(path, timeout=30.0) as conn:
        conn.row_factory = sqlite3.Row
        ensure_tables(conn)
        signal_columns = _table_columns(conn, "proposed_signals")
        updated_expr = "p.updated_at" if "updated_at" in signal_columns else "NULL AS updated_at"
        rows = conn.execute(
            "SELECT p.*,r.review_adjusted_score,r.review_verdict,r.review_tier,"
            "r.review_reason_codes_json,r.reviewed_at,r.review_expires_at,"
            f"{updated_expr} "
            "FROM proposed_signals p JOIN stocks_preus_review r ON r.signal_id=p.signal_id "
            "WHERE p.asset_class='stocks' AND p.mode='intraday' "
            "AND (p.created_at>=? OR r.reviewed_at>=?)",
            (_iso(since), _iso(since)),
        ).fetchall()
        rows_as_dicts = [dict(raw_row) for raw_row in rows]
        hard_gate_context = _preload_hard_gate_context(
            conn, rows_as_dicts, now=moment, cfg=cfg
        )
        for row in rows_as_dicts:
            signal_id = str(row.get("signal_id") or "")
            snapshot = _snapshot_for_signal(conn, signal_id)
            target = _target_session(row, snapshot)
            reasons: list[str] = []
            decision = "BLOCKED"
            valid_until: datetime | None = None

            session_cap_only, _pre_gate = _session_cap_only(row, snapshot)
            if not session_cap_only:
                reasons.append("NOT_SESSION_CAP_ONLY")
            if target is None:
                reasons.append("TARGET_SESSION_UNAVAILABLE")
                opened = closed = moment
            else:
                opened, closed = target
                if moment > closed:
                    reasons.append("TARGET_SESSION_CLOSED")

            # A review that lands after the pre-US deadline is useful as an
            # audit artifact, but must never retroactively make a plan
            # actionable. The comparison is against the reviewed timestamp,
            # not the later materialization time, so an on-time review can
            # continue to serve the RTH decision window after the deadline.
            reviewed_at = _parse(row.get("reviewed_at"))
            if reviewed_at is None or reviewed_at > _review_deadline_at(opened, cfg):
                reasons.append("REVIEW_INGEST_AFTER_DEADLINE")

            review_expires = _parse(row.get("review_expires_at"))
            if review_expires is None or moment > review_expires:
                reasons.append("REVIEW_EXPIRED")
            review_verdict = str(row.get("review_verdict") or "").upper()
            if review_verdict == "BLOCK":
                reasons.append("REVIEW_BLOCK")
            # A reviewer explicitly saying that evidence is insufficient must
            # never reopen a session-capped plan merely because its old base
            # score was A/B before the market-closed cap.
            if review_verdict == "INSUFFICIENT_DATA":
                reasons.append("REVIEW_INSUFFICIENT_DATA")
            if str(row.get("review_tier") or "").upper() not in {"A", "B"}:
                reasons.append("REVIEW_TIER_NOT_AB")

            if active_block(path, signal_id, now=moment) is not None:
                reasons.append("FRESH_BLOCK_ACTIVE")
            hard_reason = _hard_gate_reason(
                conn, row, now=moment, cfg=cfg, preloaded=hard_gate_context
            )
            if hard_reason is not None:
                reasons.append(hard_reason)
            if not _has_valid_geometry(row):
                reasons.append(EXCLUDE_INVALID_GEOMETRY)

            current_caps = _cap_reasons(row)
            current_substantive = [
                reason for reason in current_caps
                if PLAN_MARKER not in reason and not reason.lower().startswith("tier demoted")
            ]
            if current_substantive:
                reasons.append("CURRENT_SUBSTANTIVE_CAP")

            if not reasons and review_expires is not None and target is not None:
                valid_until = min(review_expires, closed)
                if moment <= valid_until:
                    decision = "ACTIONABLE"

            existing_actionability = conn.execute(
                "SELECT reactivated FROM stocks_preus_actionability WHERE signal_id=?",
                (signal_id,),
            ).fetchone()
            payload = {
                "signal_id": signal_id,
                "target_session_open_at": _iso(opened),
                "target_session_close_at": _iso(closed),
                "evaluated_at": _iso(moment),
                "decision": decision,
                "effective_score": row.get("review_adjusted_score"),
                "effective_tier": row.get("review_tier"),
                "reason_codes_json": json.dumps(sorted(set(reasons))),
                "review_expires_at": row.get("review_expires_at"),
                "valid_until": _iso(valid_until) if valid_until else None,
                "current_signal_updated_at": row.get("updated_at"),
                "source_fingerprint": source_decision_fingerprint(row),
                "geometry_json": json.dumps(_geometry(row), sort_keys=True),
                "reactivated": (
                    int(existing_actionability[0])
                    if existing_actionability is not None else 0
                ),
                "version": ACTIONABILITY_VERSION,
            }
            columns = tuple(payload)
            conn.execute(
                f"INSERT INTO stocks_preus_actionability ({','.join(columns)}) "
                f"VALUES ({','.join('?' for _ in columns)}) "
                "ON CONFLICT(signal_id) DO UPDATE SET "
                + ",".join(
                    f"{column}=excluded.{column}" for column in columns
                    if column not in {"signal_id", "reactivated"}
                ),
                tuple(payload[column] for column in columns),
            )
            _record_actionability_history(
                conn,
                payload,
                row=row,
                snapshot=snapshot,
                session_cap_only=session_cap_only,
                pre_gate_tier=_pre_gate,
                reasons=reasons,
            )
            # This table is a materialized permission/read model. Keep every
            # write lease short so a large overnight review set cannot stall
            # the minute-level Paper tracker.
            conn.commit()
            rows_out.append(payload)
        conn.commit()
    return {
        "status": "ok",
        "evaluated": len(rows_out),
        "actionable": sum(row["decision"] == "ACTIONABLE" for row in rows_out),
        "blocked": sum(row["decision"] != "ACTIONABLE" for row in rows_out),
        "rows": rows_out,
    }


def active_actionability(
    db: str | Path | None,
    signal_id: str,
    *,
    now: datetime | None = None,
) -> dict[str, Any] | None:
    moment = _utc(now)
    path = Path(db or load_config().db_path)
    try:
        conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT * FROM stocks_preus_actionability WHERE signal_id=?",
            (str(signal_id),),
        ).fetchone()
    except sqlite3.OperationalError:
        return None
    finally:
        try:
            conn.close()
        except Exception:
            pass
    if row is None:
        return None
    result = dict(row)
    valid_until = _parse(result.get("valid_until"))
    if (
        result.get("decision") != "ACTIONABLE"
        or valid_until is None
        or moment > valid_until
    ):
        return None
    return result


def active_actionable_signal_ids(
    db: str | Path | None,
    *,
    now: datetime | None = None,
) -> list[str]:
    moment = _utc(now)
    path = Path(db or load_config().db_path)
    try:
        with sqlite3.connect(f"file:{path}?mode=ro", uri=True) as conn:
            rows = conn.execute(
                "SELECT a.signal_id FROM stocks_preus_actionability a "
                "JOIN proposed_signals p ON p.signal_id=a.signal_id "
                "LEFT JOIN stocks_paper_decision_snapshots s ON s.signal_id=p.signal_id "
                "WHERE a.decision='ACTIONABLE' AND a.valid_until>=? "
                "AND p.asset_class='stocks' AND p.mode='intraday' "
                "AND (p.status IN ('generated','waiting_for_entry','triggered') "
                "OR s.funnel_state='PREOPEN_PLAN')",
                (_iso(moment),),
            ).fetchall()
        return [str(row[0]) for row in rows]
    except sqlite3.OperationalError:
        return []


# ---------------------------------------------------------------------------
# Candidate selection (hard gates decided in code, never by the LLM)
# ---------------------------------------------------------------------------

def _cap_reasons(row: dict[str, Any]) -> list[str]:
    raw = _json_obj(row.get("raw_idea_json"))
    return [str(v) for v in (raw.get("cap_reasons") or []) if v]


def _pre_gate_tier(row: dict[str, Any]) -> str:
    return str(_json_obj(row.get("raw_idea_json")).get("pre_gate_tier") or "").upper()


def _has_valid_geometry(row: dict[str, Any]) -> bool:
    entry = row.get("entry_trigger") or row.get("suggested_entry") or row.get("entry_low") or row.get("entry_high")
    stop = row.get("stop_loss") or row.get("invalidation")
    return entry not in (None, "") and stop not in (None, "")


def _preload_hard_gate_context(
    conn: sqlite3.Connection,
    rows: list[dict[str, Any]],
    *,
    now: datetime,
    cfg: dict[str, Any],
) -> dict[str, Any]:
    """Load expensive news-backed gates once for a complete pre-US bundle."""
    symbols = sorted({str(row.get("symbol") or "") for row in rows if row.get("symbol")})
    context: dict[str, Any] = {
        "legal_blocked": set(),
        "earnings_symbols": set(),
        "catalyst_symbols": set(),
        "legal_error": False,
        "earnings_error": False,
        "catalyst_error": False,
    }
    if not symbols:
        return context
    try:
        from src.stocks.legal_risk import detect_legal_risk, load_active_legal_news
        from src.storage.sqlite import SQLiteStore

        store = SQLiteStore(Path(conn.execute("PRAGMA database_list").fetchone()[2]))
        legal_hits = load_active_legal_news(store, symbols, lookback_days=90, now=now)
        context["legal_blocked"] = {
            symbol for symbol, hits in legal_hits.items()
            if hits and detect_legal_risk(hits).blocking
        }
    except Exception:
        context["legal_error"] = True
    try:
        from src.stocks.earnings_freshness import load_recent_earnings_news
        from src.storage.sqlite import SQLiteStore

        store = SQLiteStore(Path(conn.execute("PRAGMA database_list").fetchone()[2]))
        context["earnings_symbols"] = set(
            load_recent_earnings_news(store, symbols, lookback_hours=36, now=now)
        )
    except Exception:
        context["earnings_error"] = True
    try:
        from src.catalysts.collector import CATALYST_MIN_IMPORTANCE, news_catalyst_symbols

        context["catalyst_symbols"] = news_catalyst_symbols(
            conn,
            lookback_hours=int(cfg.get("catalyst_max_age_hours", 24)),
            min_importance=CATALYST_MIN_IMPORTANCE,
            now=now,
        )
    except Exception:
        context["catalyst_error"] = True
    return context


def _hard_gate_reason(conn: sqlite3.Connection, row: dict[str, Any], *, now: datetime,
                      cfg: dict[str, Any], preloaded: dict[str, Any] | None = None) -> str | None:
    """Return an exclusion reason code, or None if the candidate clears every
    hard gate. Any internal check failure excludes conservatively rather than
    silently passing the candidate through."""
    symbol = str(row.get("symbol") or "")
    base = symbol.split("/")[0].upper()
    if not _has_valid_geometry(row):
        return EXCLUDE_INVALID_GEOMETRY

    created = _parse(row.get("created_at"))
    max_age = timedelta(hours=float(cfg.get("max_candidate_age_hours", 20)))
    if created is None:
        return EXCLUDE_STALE_PLAN
    snapshot_state = str(row.get("snapshot_funnel_state") or "")
    target_open = _parse(row.get("snapshot_target_session_open_at"))
    target_close = _parse(row.get("snapshot_target_session_close_at"))
    if snapshot_state == "PREOPEN_PLAN" and target_open is not None and target_close is not None:
        if now > target_close:
            return EXCLUDE_STALE_PLAN
        age_anchor = max(created, target_open)
        if now >= target_open and (now - age_anchor) > max_age:
            return EXCLUDE_STALE_PLAN
    elif (now - created) > max_age:
        return EXCLUDE_STALE_PLAN

    if preloaded is not None:
        if preloaded.get("legal_error"):
            return EXCLUDE_DATA_ERROR
        if base in preloaded.get("legal_blocked", set()):
            return EXCLUDE_LEGAL_RISK
    else:
        try:
            from src.stocks.legal_risk import detect_legal_risk, load_active_legal_news
            from src.storage.sqlite import SQLiteStore
            store = SQLiteStore(Path(conn.execute("PRAGMA database_list").fetchone()[2]))
            legal_hits = load_active_legal_news(store, [symbol], lookback_days=90, now=now).get(base) or []
            if legal_hits and detect_legal_risk(legal_hits).blocking:
                return EXCLUDE_LEGAL_RISK
        except Exception:
            return EXCLUDE_DATA_ERROR

    if preloaded is not None:
        if preloaded.get("earnings_error"):
            return EXCLUDE_DATA_ERROR
        if base in preloaded.get("earnings_symbols", set()):
            return EXCLUDE_EARNINGS_BLACKOUT
    else:
        try:
            from src.stocks.earnings_freshness import load_recent_earnings_news
            from src.storage.sqlite import SQLiteStore
            store = SQLiteStore(Path(conn.execute("PRAGMA database_list").fetchone()[2]))
            recent_earnings = load_recent_earnings_news(store, [symbol], lookback_hours=36, now=now)
            if base in recent_earnings:
                return EXCLUDE_EARNINGS_BLACKOUT
        except Exception:
            return EXCLUDE_DATA_ERROR
    if any("earnings" in reason.lower() for reason in _cap_reasons(row)):
        return EXCLUDE_EARNINGS_BLACKOUT

    if preloaded is not None:
        if preloaded.get("catalyst_error"):
            return EXCLUDE_DATA_ERROR
        if base not in preloaded.get("catalyst_symbols", set()):
            return EXCLUDE_NO_ENTITY_RESOLVED_CATALYST
    else:
        try:
            from src.catalysts.integrity import catalyst_integrity_for_signal
            integ = catalyst_integrity_for_signal(conn, row, lookback_hours=int(cfg.get("catalyst_max_age_hours", 24)))
            if integ.get("catalyst_integrity_status") == "no_direct_news_catalyst":
                return EXCLUDE_NO_ENTITY_RESOLVED_CATALYST
        except Exception:
            return EXCLUDE_DATA_ERROR

    # Entity-mapping conflict: `catalyst_integrity_for_signal` above already
    # requires a direct, high-importance news_items hit for THIS symbol via
    # the entity-resolved `news_catalyst_symbols` path (src/catalysts/collector.py),
    # which itself only trusts entity-resolved rows (src/news/entity_resolver.py).
    # A conflicting/unconfirmed mapping surfaces there as "no_direct_news_catalyst"
    # (EXCLUDE_NO_ENTITY_RESOLVED_CATALYST above) rather than needing a second,
    # separate check here.

    if any(reason in ("hard_risk_guard", "circuit_breaker", "exposure_block") for reason in _cap_reasons(row)):
        return EXCLUDE_HARD_RISK_GUARD_BLOCK

    return None


def select_candidates(
    db: str | Path | None = None,
    *,
    now: datetime | None = None,
    cfg: dict[str, Any] | None = None,
    timeout_seconds: float = 30.0,
) -> dict[str, Any]:
    """Deterministic candidate bundle: {"eligible": [...], "excluded": [...]}.

    Eligible entries carry the base_score + funnel_state + pre_gate_tier the
    LLM needs; excluded entries carry the enum reason and nothing else."""
    cfg = cfg or load_cfg()
    moment = _utc(now)
    path = Path(db or load_config().db_path)
    eligible: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []
    if not cfg.get("enabled", True):
        return {"eligible": eligible, "excluded": excluded, "generated_at": _iso(moment), "status": "disabled"}
    since = moment - timedelta(hours=float(cfg.get("max_candidate_age_hours", 20)))
    with sqlite3.connect(path, timeout=timeout_seconds) as conn:
        conn.execute(f"PRAGMA busy_timeout={max(0, int(timeout_seconds * 1000))}")
        conn.row_factory = sqlite3.Row
        ensure_tables(conn)
        try:
            snapshot_columns = _table_columns(conn, "stocks_paper_decision_snapshots")
            has_target_open = "target_session_open_at" in snapshot_columns
            has_target_close = "target_session_close_at" in snapshot_columns
            snapshot_select = ["s.funnel_state AS snapshot_funnel_state"]
            snapshot_select.append(
                "s.target_session_open_at AS snapshot_target_session_open_at"
                if has_target_open else "NULL AS snapshot_target_session_open_at"
            )
            snapshot_select.append(
                "s.target_session_close_at AS snapshot_target_session_close_at"
                if has_target_close else "NULL AS snapshot_target_session_close_at"
            )
            if has_target_close:
                age_window = (
                    "(p.created_at >= ? OR "
                    "(s.funnel_state='PREOPEN_PLAN' AND s.target_session_close_at>=?))"
                )
                params = (since.isoformat(), moment.isoformat())
            else:
                age_window = "p.created_at >= ?"
                params = (since.isoformat(),)
            rows = [dict(r) for r in conn.execute(
                "SELECT p.*, " + ",".join(snapshot_select) + " "
                "FROM proposed_signals p "
                "LEFT JOIN stocks_paper_decision_snapshots s ON s.signal_id = p.signal_id "
                "WHERE p.asset_class='stocks' AND p.mode='intraday' "
                f"AND {age_window} "
                # A pre-open plan is deliberately saved before RTH.  The
                # historical tracker can later label its hypothetical path
                # missed/expired; that must not erase the still-valid plan
                # before the scheduled pre-US review can revalidate it.
                "AND (p.status IN ('generated','waiting_for_entry','triggered') "
                "     OR s.funnel_state='PREOPEN_PLAN') "
                "ORDER BY p.created_at DESC",
                params,
            ).fetchall()]
        except sqlite3.OperationalError:
            rows = []
        hard_gate_context = _preload_hard_gate_context(conn, rows, now=moment, cfg=cfg)
        for row in rows:
            signal_id = str(row.get("signal_id") or "")
            raw_payload = _json_obj(row.get("raw_idea_json"))
            funnel_state = row.get("snapshot_funnel_state")
            tier = str(row.get("tier") or "").upper()
            pre_gate = _pre_gate_tier(row)
            is_preopen_plan = (
                funnel_state == "PREOPEN_PLAN"
                or (tier == "C" and PLAN_MARKER in " ".join(_cap_reasons(row)) and pre_gate in {"A", "B"})
            )
            is_rth_eligible = funnel_state == "RTH_ELIGIBLE" or (funnel_state is None and tier in {"A", "B"})
            if not (is_preopen_plan or is_rth_eligible):
                excluded.append({
                    "signal_id": signal_id, "symbol": row.get("symbol"),
                    "reason": EXCLUDE_TERMINAL_OR_EXPIRED,
                })
                continue
            reason = _hard_gate_reason(
                conn, row, now=moment, cfg=cfg, preloaded=hard_gate_context
            )
            if reason is not None:
                excluded.append({"signal_id": signal_id, "symbol": row.get("symbol"), "reason": reason})
                continue
            eligible.append({
                "signal_id": signal_id,
                "symbol": row.get("symbol"),
                "direction": row.get("direction"),
                "tier": tier,
                "pre_gate_tier": pre_gate or tier,
                "base_score": float(row.get("score") or 0.0),
                "funnel_state": funnel_state or ("RTH_ELIGIBLE" if tier in {"A", "B"} else "UNKNOWN"),
                "promotable": bool(
                    is_preopen_plan and tier == "C" and pre_gate in {"A", "B"}
                ),
                "created_at": row.get("created_at"),
                "entry_trigger": row.get("entry_trigger") or row.get("suggested_entry"),
                "stop_loss": row.get("stop_loss") or row.get("invalidation"),
                "cap_reasons": _cap_reasons(row),
                # Provenance only: lets the scheduled Enriched Review explain
                # that this is the versioned closed-bar Paper profile.  It
                # never relaxes any hard gate or changes the score itself.
                "paper_entry_profile": raw_payload.get("paper_entry_profile"),
                "paper_entry_confirmation": raw_payload.get("paper_entry_confirmation"),
            })
    return {"eligible": eligible, "excluded": excluded, "generated_at": _iso(moment), "status": "ok"}


# ---------------------------------------------------------------------------
# Operational review hand-off health
# ---------------------------------------------------------------------------

def _et_minutes(value: str) -> int:
    hour, minute = str(value).split(":", 1)
    return int(hour) * 60 + int(minute)


def _review_deadline_at(session_time: datetime, cfg: dict[str, Any]) -> datetime:
    """Return the configured review deadline for ``session_time``'s NY date."""
    local = session_time.astimezone(NY)
    deadline = _et_minutes(str(cfg.get("review_deadline_et") or "09:12"))
    return local.replace(
        hour=deadline // 60,
        minute=deadline % 60,
        second=0,
        microsecond=0,
    ).astimezone(timezone.utc)


def record_candidate_bundle(
    bundle: dict[str, Any],
    db: str | Path | None = None,
    *,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Persist the exact candidate set supplied to the external routine."""
    moment = _utc(now)
    path = Path(db or load_config().db_path)
    candidate_ids = sorted({
        str(row.get("signal_id") or "") for row in bundle.get("eligible", [])
        if str(row.get("signal_id") or "")
    })
    generated_at = _parse(bundle.get("generated_at")) or moment
    row = {
        "session_date": moment.astimezone(NY).date().isoformat(),
        "generated_at": _iso(generated_at),
        "eligible_signal_ids_json": json.dumps(candidate_ids),
        "excluded_count": len(bundle.get("excluded") or []),
        "status": str(bundle.get("status") or "ok"),
        "version": REVIEW_HEALTH_VERSION,
    }
    local = moment.astimezone(NY)
    deadline_hour, deadline_minute = map(
        int, str(load_cfg().get("review_deadline_et") or "09:12").split(":", 1)
    )
    deadline_at = local.replace(
        hour=deadline_hour,
        minute=deadline_minute,
        second=0,
        microsecond=0,
    ).astimezone(timezone.utc)
    is_late = moment > deadline_at
    with sqlite3.connect(path, timeout=5.0) as conn:
        conn.execute("PRAGMA busy_timeout=5000")
        ensure_tables(conn)
        existing = conn.execute(
            "SELECT generated_at,eligible_signal_ids_json,excluded_count,status,version "
            "FROM stocks_preus_review_bundles WHERE session_date=?",
            (row["session_date"],),
        ).fetchone()
        # The pre-US hand-off is a same-session snapshot. A later generic
        # refresh must never replace it, otherwise it severs the link between
        # the candidate list and the verdicts already being produced by the
        # LLM. Newer ideas remain available to the normal RTH pipeline.
        if existing is not None:
            conn.commit()
            return {
                "session_date": row["session_date"],
                "generated_at": existing[0],
                "eligible_signal_ids_json": existing[1],
                "excluded_count": int(existing[2] or 0),
                "status": existing[3],
                "version": existing[4],
                "eligible_count": len(json.loads(existing[1] or "[]")),
                "preserved_existing_snapshot": True,
            }
        if is_late:
            row["status"] = "late"
        columns = tuple(row)
        conn.execute(
            "INSERT INTO stocks_preus_review_bundles(" + ",".join(columns) + ") "
            "VALUES(?,?,?,?,?,?) ON CONFLICT(session_date) DO UPDATE SET "
            "generated_at=excluded.generated_at,"
            "eligible_signal_ids_json=excluded.eligible_signal_ids_json,"
            "excluded_count=excluded.excluded_count,status=excluded.status,"
            "version=excluded.version",
            tuple(row[column] for column in columns),
        )
        conn.commit()
    quality_agents = None
    try:
        from src.quality_agents.runner import evaluate_preus_bundle
        quality_agents = evaluate_preus_bundle(
            list(bundle.get("eligible") or []), db=path,
        )
    except Exception as exc:
        # The pre-US bundle is authoritative and must remain available even if
        # a diagnostic overlay is temporarily unavailable.
        quality_agents = {"status": "DEGRADED", "error_type": type(exc).__name__}
    return {**row, "eligible_count": len(candidate_ids), "quality_agents": quality_agents}


def review_health(
    db: str | Path | None = None,
    *,
    now: datetime | None = None,
    cfg: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Materialize readiness using the pre-US routine's saved snapshot.

    The minute monitor must not rerun the expensive candidate hard gates.  A
    recorded bundle makes the routine -> validated-ingest boundary explicit
    and lets this check complete within the monitor's one-second DB budget.
    """
    cfg = cfg or load_cfg()
    moment = _utc(now)
    path = Path(db or load_config().db_path)
    session_date = moment.astimezone(NY).date().isoformat()
    candidate_ids: list[str] = []
    reviewed_ids: set[str] = set()
    bundle_generated_at: datetime | None = None

    try:
        with sqlite3.connect(path, timeout=1.0) as conn:
            conn.execute("PRAGMA busy_timeout=1000")
            conn.row_factory = sqlite3.Row
            ensure_tables(conn)
            bundle = conn.execute(
                "SELECT generated_at,eligible_signal_ids_json,status "
                "FROM stocks_preus_review_bundles WHERE session_date=?",
                (session_date,),
            ).fetchone()
            if bundle is not None:
                try:
                    candidate_ids = sorted({
                        str(item) for item in json.loads(
                            bundle["eligible_signal_ids_json"] or "[]"
                        ) if str(item)
                    })
                except (TypeError, ValueError, json.JSONDecodeError):
                    candidate_ids = []
                bundle_generated_at = _parse(bundle["generated_at"])
                bundle_status = str(bundle["status"] or "")
            else:
                bundle_status = None
            reviewed_at_by_id: dict[str, datetime] = {}
            review_model_by_id: dict[str, str] = {}
            if candidate_ids and bundle_generated_at is not None:
                placeholders = ",".join("?" for _ in candidate_ids)
                rows = conn.execute(
                    "SELECT signal_id,reviewed_at,review_model FROM stocks_preus_review "
                    f"WHERE signal_id IN ({placeholders}) "
                    "AND review_cycle LIKE 'preus%' AND reviewed_at>=?",
                    (*candidate_ids, _iso(bundle_generated_at)),
                ).fetchall()
                reviewed_at_by_id = {
                    str(item["signal_id"]): _parse(item["reviewed_at"])
                    for item in rows
                }
                review_model_by_id = {
                    str(item["signal_id"]): str(item["review_model"] or "")
                    for item in rows
                }
                reviewed_ids = set(reviewed_at_by_id)

            local = moment.astimezone(NY)
            deadline = _et_minutes(str(cfg.get("review_deadline_et") or "09:12"))
            minute_of_day = local.hour * 60 + local.minute
            deadline_at = _review_deadline_at(moment, cfg)
            missing_ids = sorted(set(candidate_ids) - reviewed_ids)
            bundle_late = bundle_generated_at is not None and bundle_generated_at > deadline_at
            late_review_ids = sorted(
                signal_id for signal_id, reviewed_at in reviewed_at_by_id.items()
                if reviewed_at is not None and reviewed_at > deadline_at
            )
            baseline_ids = sorted(
                signal_id for signal_id in reviewed_ids
                if review_model_by_id.get(signal_id) == BASELINE_REVIEW_MODEL
            )
            ab_cfg = ((cfg.get("llm_agent") or {}).get("ab_test") or {})
            advisory_only = bool((cfg.get("llm_agent") or {}).get("advisory_only", True))
            experiment_enabled = bool(ab_cfg.get("enabled", False))
            treatment_ids: set[str] = set()
            control_ids: set[str] = set()
            if experiment_enabled and candidate_ids:
                experiment_table = conn.execute(
                    "SELECT 1 FROM sqlite_master WHERE type='table' "
                    "AND name='quality_agent_experiment_assignments'"
                ).fetchone()
                if experiment_table is not None:
                    experiment_name = str(
                        ab_cfg.get("experiment_name") or "stocks_preus_gemini_v1"
                    )
                    cohort_rows = conn.execute(
                        "SELECT signal_id,cohort FROM quality_agent_experiment_assignments "
                        "WHERE experiment_name=? AND session_key=?",
                        (experiment_name, session_date),
                    ).fetchall()
                    treatment_ids = {
                        str(item["signal_id"]) for item in cohort_rows
                        if str(item["cohort"]) == "treatment"
                    }
                    control_ids = {
                        str(item["signal_id"]) for item in cohort_rows
                        if str(item["cohort"]) == "control"
                    }
            llm_reviewed_ids = {
                signal_id for signal_id in reviewed_ids
                if review_model_by_id.get(signal_id) != BASELINE_REVIEW_MODEL
            }
            llm_assessment_table = conn.execute(
                "SELECT 1 FROM sqlite_master WHERE type='table' "
                "AND name='quality_agent_llm_assessments'"
            ).fetchone()
            if llm_assessment_table is not None and bundle_generated_at is not None:
                llm_rows = conn.execute(
                    "SELECT signal_id FROM quality_agent_llm_assessments "
                    "WHERE scope='stocks_preus_openrouter_review' AND status='OK' "
                    "AND target_key LIKE ? AND created_at>=?",
                    (f"{session_date}:%", _iso(bundle_generated_at)),
                ).fetchall()
                llm_reviewed_ids.update(
                    str(item["signal_id"]) for item in llm_rows if item["signal_id"]
                )
            experiment_active = bool(treatment_ids or control_ids)
            missing_treatment_ids = sorted(treatment_ids - llm_reviewed_ids)
            if bundle is None:
                status = "BUNDLE_PENDING" if minute_of_day < deadline else "BUNDLE_MISSING"
                reason = "structured_preus_candidate_bundle_not_recorded"
            elif bundle_status == "late" or bundle_late:
                status, reason = "BUNDLE_LATE", "structured_preus_candidate_bundle_recorded_after_deadline"
            elif bundle_status != "ok":
                status, reason = "BUNDLE_FAILED", "structured_preus_candidate_bundle_failed"
            elif not candidate_ids:
                status, reason = "NO_ELIGIBLE", None
            elif late_review_ids:
                status, reason = "REVIEW_LATE", "structured_preus_review_recorded_after_deadline"
            elif not missing_ids:
                if advisory_only:
                    status, reason = "READY_ADVISORY_OPTIONAL", "deterministic_preus_baseline_authoritative"
                elif (
                    (missing_treatment_ids or (baseline_ids and not experiment_active))
                    and minute_of_day < deadline
                ):
                    status, reason = "PENDING_DEADLINE", "structured_preus_review_not_yet_due"
                elif missing_treatment_ids:
                    status, reason = (
                        "PARTIAL_REVIEW_MISSING",
                        "experiment_treatment_missing_structured_verdict",
                    )
                elif baseline_ids and not experiment_active:
                    status, reason = "BASELINE_READY_LLM_MISSING", "deterministic_preus_baseline_used"
                else:
                    status, reason = "READY", None
            elif minute_of_day < deadline:
                status, reason = "PENDING_DEADLINE", "structured_preus_review_not_yet_due"
            elif reviewed_ids:
                status, reason = "PARTIAL_REVIEW_MISSING", "eligible_candidates_missing_structured_verdict"
            else:
                status, reason = "REVIEW_MISSING", "no_fresh_structured_preus_review"

            previous = conn.execute(
                "SELECT alerted_at FROM stocks_preus_review_health WHERE session_date=?",
                (session_date,),
            ).fetchone()
            alert_statuses = {
                "BUNDLE_MISSING", "BUNDLE_FAILED", "BUNDLE_LATE", "REVIEW_LATE",
                "REVIEW_MISSING", "PARTIAL_REVIEW_MISSING",
            }
            alerted_at = previous["alerted_at"] if previous and status in alert_statuses else None
            row = {
                "session_date": session_date,
                "checked_at": _iso(moment),
                "eligible_count": len(candidate_ids),
                "reviewed_count": len(reviewed_ids),
                "missing_count": len(missing_ids),
                "status": status,
                "reason": reason,
                "alerted_at": alerted_at,
                "version": REVIEW_HEALTH_VERSION,
                "missing_signal_ids": missing_ids,
                "missing_treatment_signal_ids": missing_treatment_ids,
                "late_review_signal_ids": late_review_ids,
                "baseline_signal_ids": baseline_ids,
                "experiment_treatment_signal_ids": sorted(treatment_ids),
                "experiment_control_signal_ids": sorted(control_ids),
                "fresh_since": _iso(bundle_generated_at) if bundle_generated_at else None,
            }
            columns = (
                "session_date", "checked_at", "eligible_count", "reviewed_count",
                "missing_count", "status", "reason", "alerted_at", "version",
            )
            conn.execute(
                "INSERT INTO stocks_preus_review_health(" + ",".join(columns) + ") "
                "VALUES(?,?,?,?,?,?,?,?,?) ON CONFLICT(session_date) DO UPDATE SET "
                "checked_at=excluded.checked_at,eligible_count=excluded.eligible_count,"
                "reviewed_count=excluded.reviewed_count,missing_count=excluded.missing_count,"
                "status=excluded.status,reason=excluded.reason,alerted_at=excluded.alerted_at,"
                "version=excluded.version",
                tuple(row[column] for column in columns),
            )
            conn.execute(
                "INSERT INTO stocks_preus_review_health_history(" + ",".join(columns) + ") "
                "VALUES(?,?,?,?,?,?,?,?,?)",
                tuple(row[column] for column in columns),
            )
            conn.commit()
    except sqlite3.Error as exc:
        return {
            "session_date": session_date,
            "checked_at": _iso(moment),
            "eligible_count": 0,
            "reviewed_count": 0,
            "missing_count": 0,
            "status": "HEALTH_UNAVAILABLE",
            "reason": f"sqlite:{type(exc).__name__}",
            "alerted_at": None,
            "version": REVIEW_HEALTH_VERSION,
            "missing_signal_ids": [],
            "missing_treatment_signal_ids": [],
            "baseline_signal_ids": [],
            "experiment_treatment_signal_ids": [],
            "experiment_control_signal_ids": [],
            "fresh_since": None,
        }
    return row


def consume_new_review_health_alert(
    db: str | Path | None = None,
    *,
    health: dict[str, Any],
    now: datetime | None = None,
) -> list[dict[str, Any]]:
    """Return one post-deadline alert for an incomplete review hand-off."""
    alert_statuses = {
        "BUNDLE_MISSING", "BUNDLE_FAILED", "BUNDLE_LATE", "REVIEW_LATE",
        "REVIEW_MISSING", "PARTIAL_REVIEW_MISSING",
    }
    if health.get("status") not in alert_statuses:
        return []
    if health.get("alerted_at"):
        return []
    moment = _utc(now)
    path = Path(db or load_config().db_path)
    with sqlite3.connect(path, timeout=1.0) as conn:
        conn.execute("PRAGMA busy_timeout=1000")
        updated = conn.execute(
            "UPDATE stocks_preus_review_health SET alerted_at=? "
            "WHERE session_date=? AND alerted_at IS NULL "
            "AND status IN ('BUNDLE_MISSING','BUNDLE_FAILED','BUNDLE_LATE','REVIEW_LATE',"
            "'REVIEW_MISSING','PARTIAL_REVIEW_MISSING')",
            (_iso(moment), health["session_date"]),
        ).rowcount
        conn.commit()
    if not updated:
        return []
    row = dict(health)
    row["alerted_at"] = _iso(moment)
    return [row]


# ---------------------------------------------------------------------------
# Verdict ingestion (all numeric enforcement lives here, not in the prompt)
# ---------------------------------------------------------------------------

def _clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def _is_deterministic_review_model(model: str | None) -> bool:
    value = str(model or "").strip().lower()
    # Empty is the legacy/manual deterministic ingest path. Every in-process
    # LLM caller supplies an explicit concrete model ID through the router.
    return not value or value == BASELINE_REVIEW_MODEL or value.startswith("deterministic-")


def record_verdict(
    *,
    signal_id: str,
    verdict: str,
    reason_codes: list[str] | None = None,
    evidence: dict[str, Any] | None = None,
    requested_adjustment: float = 0.0,
    model: str | None = None,
    prompt_version: str | None = None,
    review_cycle: str | None = None,
    published_at: str | None = None,
    available_at: str | None = None,
    db: str | Path | None = None,
    now: datetime | None = None,
    cfg: dict[str, Any] | None = None,
    refresh_after: bool = True,
    preloaded: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Ingest ONE candidate's LLM verdict. Idempotent (INSERT OR REPLACE keyed
    by signal_id) — re-running the same review window overwrites, never
    duplicates. Re-derives eligibility server-side; never trusts the caller's
    claim that a candidate is eligible or that a hard gate has cleared."""
    cfg = cfg or load_cfg()
    moment = _utc(now)
    verdict = str(verdict or "").upper()
    if verdict not in VERDICTS:
        return {"status": "REJECTED", "reason": "invalid_verdict"}
    if (
        bool((cfg.get("llm_agent") or {}).get("advisory_only", True))
        and model not in (None, "")
        and not _is_deterministic_review_model(model)
    ):
        return {
            "status": "ADVISORY_ONLY_NOT_APPLIED",
            "reason": "llm_cannot_change_score_veto_or_actionability",
            "verdict": verdict,
            "model": model,
        }
    path = Path(db or load_config().db_path)
    reason_codes = [str(r) for r in (reason_codes or [])]
    evidence = dict(evidence or {})

    with sqlite3.connect(path, timeout=30.0) as conn:
        conn.row_factory = sqlite3.Row
        ensure_tables(conn)
        signal_row = conn.execute(
            "SELECT * FROM proposed_signals WHERE signal_id=? AND asset_class='stocks' AND mode='intraday'",
            (signal_id,),
        ).fetchone()
        if signal_row is None:
            return {"status": "REJECTED", "reason": "unknown_signal_id"}
        signal_row = dict(signal_row)
        symbol = str(signal_row.get("symbol") or "")
        base_score = float(signal_row.get("score") or 0.0)
        hard_reason = _hard_gate_reason(
            conn, signal_row, now=moment, cfg=cfg, preloaded=preloaded
        )

        # The baseline revalidation may have completed before the deadline
        # while an external LLM call finishes afterwards. A late non-veto
        # opinion must not erase that timely decision and strand the plan.
        # A late BLOCK is intentionally still accepted: a newly discovered
        # risk can only reduce actionability, never create it.
        target = _target_session(signal_row, _snapshot_for_signal(conn, signal_id))
        deadline_at = _review_deadline_at(target[0], cfg) if target is not None else None
        if verdict != "BLOCK" and deadline_at is not None and moment > deadline_at:
            existing_review = conn.execute(
                "SELECT reviewed_at FROM stocks_preus_review WHERE signal_id=?", (signal_id,)
            ).fetchone()
            existing_at = _parse(existing_review[0]) if existing_review is not None else None
            if existing_at is not None and existing_at <= deadline_at:
                return {
                    "status": "IGNORED_LATE_PRESERVED_TIMELY_REVIEW",
                    "reason": "review_deadline_passed",
                    "preserved_reviewed_at": _iso(existing_at),
                }

        review_cycle = review_cycle or "preus"
        block_ttl = timedelta(minutes=float(cfg.get("block_ttl_minutes", 240)))
        review_ttl = timedelta(minutes=float(cfg.get("review_ttl_minutes", 90)))

        # The deterministic baseline is created before the external review
        # starts.  ``INSUFFICIENT_DATA`` means that the reviewer could not add
        # evidence; it is not a veto.  Do not let that non-decision erase a
        # timely baseline that has already re-checked all server-side hard
        # gates.  A real BLOCK is handled below and always wins.
        #
        # This is deliberately limited to a baseline row and never promotes a
        # C-tier plan: the baseline itself is only created from an immutable
        # pre-gate A/B session-cap-only candidate.
        if verdict == "INSUFFICIENT_DATA":
            existing = conn.execute(
                "SELECT review_verdict,review_tier,review_model,reviewed_at,review_expires_at "
                "FROM stocks_preus_review WHERE signal_id=?",
                (signal_id,),
            ).fetchone()
            existing_at = _parse(existing["reviewed_at"]) if existing is not None else None
            existing_expires = (
                _parse(existing["review_expires_at"]) if existing is not None else None
            )
            timely_baseline = bool(
                existing is not None
                and str(existing["review_model"] or "") == BASELINE_REVIEW_MODEL
                and str(existing["review_verdict"] or "").upper() == "NEUTRAL"
                and existing_at is not None
                and (deadline_at is None or existing_at <= deadline_at)
                and (existing_expires is None or moment <= existing_expires)
            )
            if timely_baseline:
                return {
                    "status": "IGNORED_INSUFFICIENT_PRESERVED_BASELINE",
                    "reason": "timely_deterministic_baseline_remains_authoritative",
                    "verdict": "INSUFFICIENT_DATA",
                    "preserved_reviewed_at": _iso(existing_at),
                    "preserved_tier": str(existing["review_tier"] or "").upper(),
                }

        if verdict == "BLOCK":
            conn.execute(
                "INSERT INTO stocks_preus_review_blocks(signal_id,symbol,blocked_at,block_expires_at,"
                "reason_codes_json,evidence_json,review_model,review_prompt_version,review_cycle,version) "
                "VALUES(?,?,?,?,?,?,?,?,?,?) "
                "ON CONFLICT(signal_id) DO UPDATE SET blocked_at=excluded.blocked_at,"
                "block_expires_at=excluded.block_expires_at,reason_codes_json=excluded.reason_codes_json,"
                "evidence_json=excluded.evidence_json,review_model=excluded.review_model,"
                "review_prompt_version=excluded.review_prompt_version,review_cycle=excluded.review_cycle",
                (signal_id, symbol, _iso(moment), _iso(moment + block_ttl),
                 json.dumps(reason_codes, sort_keys=True), json.dumps(evidence, sort_keys=True),
                 model, prompt_version, review_cycle, VERSION),
            )
            conn.execute(
                "INSERT INTO stocks_preus_review(signal_id,symbol,base_score,review_score_adjustment,"
                "review_adjusted_score,review_verdict,review_tier,review_reason_codes_json,review_evidence_json,"
                "published_at,ingested_at,available_at,reviewed_at,review_expires_at,review_model,"
                "review_prompt_version,review_cycle,version) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) "
                "ON CONFLICT(signal_id) DO UPDATE SET base_score=excluded.base_score,"
                "review_score_adjustment=excluded.review_score_adjustment,"
                "review_adjusted_score=excluded.review_adjusted_score,review_verdict=excluded.review_verdict,"
                "review_tier=excluded.review_tier,review_reason_codes_json=excluded.review_reason_codes_json,"
                "review_evidence_json=excluded.review_evidence_json,ingested_at=excluded.ingested_at,"
                "available_at=excluded.available_at,reviewed_at=excluded.reviewed_at,"
                "review_expires_at=excluded.review_expires_at,review_model=excluded.review_model,"
                "review_prompt_version=excluded.review_prompt_version,review_cycle=excluded.review_cycle",
                (signal_id, symbol, base_score, 0.0, base_score, "BLOCK", str(signal_row.get("tier") or "").upper(),
                 json.dumps(reason_codes, sort_keys=True), json.dumps(evidence, sort_keys=True),
                 published_at, _iso(moment), available_at, _iso(moment), _iso(moment + block_ttl),
                 model, prompt_version, review_cycle, VERSION),
            )
            conn.execute(
                "UPDATE stocks_preus_actionability SET decision='BLOCKED',"
                "reason_codes_json=?,valid_until=NULL,evaluated_at=? WHERE signal_id=?",
                (json.dumps(["REVIEW_BLOCK"]), _iso(moment), signal_id),
            )
            conn.commit()
            return {"status": "OK", "verdict": "BLOCK", "adjustment": 0.0, "adjusted_score": base_score,
                    "block_expires_at": _iso(moment + block_ttl)}

        # Non-BLOCK verdicts: compute + clamp the adjustment.
        allowed = cfg.get("adjustments", {}).get(verdict) or {"min": 0, "max": 0}
        adjustment = _clamp(float(requested_adjustment or 0.0), float(allowed["min"]), float(allowed["max"]))
        clamped_by_gate = False
        if adjustment > 0 and hard_reason is not None:
            adjustment = 0.0
            clamped_by_gate = True
            reason_codes = [*reason_codes, "server_clamped_hard_block", hard_reason]
        if adjustment > 0:
            support_requires = set(cfg.get("support_requires") or [])
            evidence_flags = {k for k, v in evidence.items() if v is True}
            missing = support_requires - evidence_flags
            if missing:
                adjustment = 0.0
                clamped_by_gate = True
                reason_codes = [*reason_codes, "server_clamped_missing_precondition",
                                *(f"missing:{m}" for m in sorted(missing))]

        floor = float(cfg.get("score_floor", 0))
        ceiling = float(cfg.get("score_ceiling", 100))
        adjusted_score = _clamp(base_score + adjustment, floor, ceiling)
        review_tier = tier_from_score(adjusted_score)

        conn.execute(
            "INSERT INTO stocks_preus_review(signal_id,symbol,base_score,review_score_adjustment,"
            "review_adjusted_score,review_verdict,review_tier,review_reason_codes_json,review_evidence_json,"
            "published_at,ingested_at,available_at,reviewed_at,review_expires_at,review_model,"
            "review_prompt_version,review_cycle,version) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) "
            "ON CONFLICT(signal_id) DO UPDATE SET base_score=excluded.base_score,"
            "review_score_adjustment=excluded.review_score_adjustment,"
            "review_adjusted_score=excluded.review_adjusted_score,review_verdict=excluded.review_verdict,"
            "review_tier=excluded.review_tier,review_reason_codes_json=excluded.review_reason_codes_json,"
            "review_evidence_json=excluded.review_evidence_json,ingested_at=excluded.ingested_at,"
            "available_at=excluded.available_at,reviewed_at=excluded.reviewed_at,"
            "review_expires_at=excluded.review_expires_at,review_model=excluded.review_model,"
            "review_prompt_version=excluded.review_prompt_version,review_cycle=excluded.review_cycle",
            (signal_id, symbol, base_score, adjustment, adjusted_score, verdict, review_tier,
             json.dumps(reason_codes, sort_keys=True), json.dumps(evidence, sort_keys=True),
             published_at, _iso(moment), available_at, _iso(moment), _iso(moment + review_ttl),
             model, prompt_version, review_cycle, VERSION),
        )
        conn.commit()
    if refresh_after:
        _refresh_actionability_best_effort(path, now=moment, cfg=cfg)
    return {
        "status": "OK", "verdict": verdict, "adjustment": adjustment, "base_score": base_score,
        "adjusted_score": adjusted_score, "tier": review_tier, "clamped_by_gate": clamped_by_gate,
        "review_expires_at": _iso(moment + review_ttl),
    }


def _refresh_actionability_best_effort(
    path: Path,
    *,
    now: datetime,
    cfg: dict[str, Any],
) -> None:
    """Materialize a completed review without making ingest availability depend on it."""
    try:
        refresh_actionability(path, now=now, cfg=cfg)
        from src.stocks.preopen_lifecycle import repair_bug_expired_actionable_plans

        repair_bug_expired_actionable_plans(path, now=now)
    except Exception:
        # The verdict remains durable. The minute monitor retries deterministic
        # materialization without delaying or invalidating the review itself.
        pass


def record_verdicts(
    items: list[dict[str, Any]],
    *,
    review_cycle: str = "preus",
    db: str | Path | None = None,
    now: datetime | None = None,
    cfg: dict[str, Any] | None = None,
    retry_attempts: int = 3,
) -> list[dict[str, Any]]:
    """Ingest a complete structured review with one final materialization.

    A pre-US review often contains dozens of candidates. Refreshing the whole
    actionability table after every row amplified SQLite write contention and
    made a correctly-produced review miss the trading window. Each verdict
    remains independently idempotent, but the derived refresh runs once after
    the batch is durable.
    """
    cfg = cfg or load_cfg()
    moment = _utc(now)
    path = Path(db or load_config().db_path)
    attempts = max(1, int(retry_attempts))
    results: list[dict[str, Any]] = []
    # The structured hand-off can contain dozens of symbols.  Re-use one
    # snapshot of its legal / earnings / catalyst gates; otherwise every row
    # performs the same 90-day legal-news scan and can miss the open.
    try:
        signal_ids = [str(item.get("signal_id") or "") for item in items]
        signal_ids = [signal_id for signal_id in signal_ids if signal_id]
        if signal_ids:
            with sqlite3.connect(path, timeout=5.0) as conn:
                conn.execute("PRAGMA busy_timeout=5000")
                conn.row_factory = sqlite3.Row
                placeholders = ",".join("?" for _ in signal_ids)
                rows = [dict(row) for row in conn.execute(
                    "SELECT * FROM proposed_signals WHERE signal_id IN (" + placeholders + ") "
                    "AND asset_class='stocks' AND mode='intraday'",
                    signal_ids,
                ).fetchall()]
                preloaded = _preload_hard_gate_context(conn, rows, now=moment, cfg=cfg)
        else:
            preloaded = None
    except sqlite3.Error:
        preloaded = None

    for item in items:
        signal_id = str(item.get("signal_id") or "")
        last_error: sqlite3.OperationalError | None = None
        for attempt in range(attempts):
            try:
                result = record_verdict(
                    signal_id=signal_id,
                    verdict=str(item.get("verdict") or ""),
                    reason_codes=item.get("reason_codes") or [],
                    evidence=item.get("evidence") or {},
                    requested_adjustment=float(item.get("requested_adjustment") or 0.0),
                    model=item.get("model"),
                    prompt_version=item.get("prompt_version"),
                    review_cycle=review_cycle,
                    published_at=item.get("published_at"),
                    available_at=item.get("available_at"),
                    db=path,
                    now=moment,
                    cfg=cfg,
                    refresh_after=False,
                    preloaded=preloaded,
                )
                results.append({"signal_id": signal_id, **result})
                last_error = None
                break
            except sqlite3.OperationalError as exc:
                last_error = exc
                if "locked" not in str(exc).lower() or attempt + 1 >= attempts:
                    raise
                time.sleep(0.25 * (2 ** attempt))
        if last_error is not None:
            raise last_error

    _refresh_actionability_best_effort(path, now=moment, cfg=cfg)
    return results


def record_baseline_revalidations(
    candidates: list[dict[str, Any]],
    *,
    db: str | Path | None = None,
    now: datetime | None = None,
    cfg: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Persist a zero-adjustment fallback for a freshly built pre-US bundle.

    The fallback is deliberately not an LLM opinion. It merely re-runs the
    server-side hard gates and makes the original pre-gate A/B score available
    for a session-cap-only candidate if the LLM worker is unavailable. Its
    distinct provenance is visible in health/Telegram, and a real on-time LLM
    review may replace it later in the same review window.
    """
    moment = _utc(now)
    items = [
        {
            "signal_id": str(candidate.get("signal_id") or ""),
            "verdict": "NEUTRAL",
            "requested_adjustment": 0.0,
            "reason_codes": ["deterministic_preus_revalidation", "llm_review_unavailable"],
            "evidence": {"deterministic_hard_gates_rechecked": True},
            "model": BASELINE_REVIEW_MODEL,
            "prompt_version": "preus-baseline-v1",
            "available_at": _iso(moment),
        }
        for candidate in candidates
        if str(candidate.get("signal_id") or "")
    ]
    return record_verdicts(
        items,
        review_cycle="preus_baseline",
        db=db,
        now=moment,
        cfg=cfg,
    )


# ---------------------------------------------------------------------------
# Read-only lookups used by the Paper pre-open decision path
# ---------------------------------------------------------------------------

def active_review(db: str | Path | None, signal_id: str, *, now: datetime | None = None) -> dict[str, Any] | None:
    """Fresh (non-expired) review row for signal_id, or None. Read-only-safe."""
    moment = _utc(now)
    path = Path(db or load_config().db_path)
    try:
        conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT * FROM stocks_preus_review WHERE signal_id=?", (signal_id,)
        ).fetchone()
    except sqlite3.OperationalError:
        return None
    finally:
        try:
            conn.close()
        except Exception:
            pass
    if row is None:
        return None
    expires = _parse(row["review_expires_at"])
    if expires is None or moment > expires:
        return None
    return dict(row)


def active_block(db: str | Path | None, signal_id: str, *, now: datetime | None = None) -> dict[str, Any] | None:
    """Fresh (non-expired) BLOCK row for signal_id, or None. Read-only-safe."""
    moment = _utc(now)
    path = Path(db or load_config().db_path)
    try:
        conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT * FROM stocks_preus_review_blocks WHERE signal_id=?", (signal_id,)
        ).fetchone()
    except sqlite3.OperationalError:
        return None
    finally:
        try:
            conn.close()
        except Exception:
            pass
    if row is None:
        return None
    if (
        bool((load_cfg().get("llm_agent") or {}).get("advisory_only", True))
        and not _is_deterministic_review_model(row["review_model"])
    ):
        return None
    expires = _parse(row["block_expires_at"])
    if expires is None or moment > expires:
        return None
    return dict(row)


def is_review_supported_for_preopen(
    db: str | Path | None, signal: dict[str, Any], *, now: datetime | None = None,
) -> tuple[bool, str]:
    """Narrow override check for the stocks paper-entry tier gate.

    Returns (True, "") only when ALL of the following hold:
      * the signal's CURRENT tier is C, AND its raw cap_reasons show it was
        demoted ONLY by market_closed_intraday_planning_only with a pre-gate
        tier of A/B (i.e. a genuinely session-cap-only C, never a
        substantively-rejected one);
      * no fresh BLOCK exists for this signal;
      * a fresh (non-expired) review exists with verdict != BLOCK;
      * the review's recomputed tier is A or B.

    Any failure returns (False, reason) and the caller MUST fall back to the
    unmodified deterministic path — this function never raises."""
    try:
        signal_id = str(signal.get("signal_id") or "")
        if not signal_id:
            return False, "no_signal_id"
        tier = str(signal.get("tier") or "").upper()
        if tier != "C":
            return False, "not_a_session_cap_candidate"
        path = Path(db or load_config().db_path)
        try:
            with sqlite3.connect(f"file:{path}?mode=ro", uri=True) as conn:
                conn.row_factory = sqlite3.Row
                snapshot = _snapshot_for_signal(conn, signal_id)
        except sqlite3.OperationalError:
            snapshot = {}
        session_cap_only, _pre_gate = _session_cap_only(signal, snapshot)
        if not session_cap_only:
            return False, "not_market_closed_session_cap"
        block = active_block(db, signal_id, now=now)
        if block is not None:
            return False, "fresh_block_active"
        actionability = active_actionability(db, signal_id, now=now)
        if actionability is None:
            return False, "no_fresh_review"
        if str(actionability.get("effective_tier") or "").upper() not in {"A", "B"}:
            return False, "actionability_tier_not_ab"
        return True, "review_supported"
    except Exception:
        return False, "lookup_error"


__all__ = [
    "VERSION", "ACTIONABILITY_VERSION", "REVIEW_HEALTH_VERSION", "BASELINE_REVIEW_MODEL", "VERDICTS", "load_cfg", "ensure_tables",
    "select_candidates", "record_candidate_bundle", "record_verdict", "record_verdicts", "record_baseline_revalidations", "refresh_actionability",
    "active_review", "active_block", "active_actionability",
    "active_actionable_signal_ids", "is_review_supported_for_preopen",
    "review_health", "consume_new_review_health_alert",
    "EXCLUDE_LEGAL_RISK", "EXCLUDE_EARNINGS_BLACKOUT", "EXCLUDE_STALE_MARKET_CONTEXT",
    "EXCLUDE_NO_ENTITY_RESOLVED_CATALYST", "EXCLUDE_UNCONFIRMED_TICKER_OR_CONFLICT",
    "EXCLUDE_EXPIRED_CATALYST", "EXCLUDE_HARD_RISK_GUARD_BLOCK", "EXCLUDE_TERMINAL_OR_EXPIRED",
    "EXCLUDE_STALE_PLAN", "EXCLUDE_INVALID_GEOMETRY", "EXCLUDE_DATA_ERROR",
]
