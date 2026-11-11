from __future__ import annotations

import json
import hashlib
import sqlite3
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


_INITIALIZED_DATABASES: set[str] = set()
_PRAGMA_DATABASES: set[str] = set()


DDL = """
CREATE TABLE IF NOT EXISTS mexc_canary_decisions (
  decision_id TEXT PRIMARY KEY,
  signal_id TEXT NOT NULL UNIQUE,
  captured_at TEXT NOT NULL,
  paper_alert_id TEXT,
  symbol TEXT NOT NULL,
  mode TEXT NOT NULL,
  entry_mode TEXT,
  eligible INTEGER NOT NULL,
  state TEXT NOT NULL,
  rejection_reasons_json TEXT NOT NULL,
  decision_json TEXT NOT NULL,
  decision_hash TEXT NOT NULL,
  config_hash TEXT NOT NULL,
  decision_context_type TEXT NOT NULL,
  economic_trade_key TEXT,
  parent_decision_id TEXT,
  recovery_sequence INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_mexc_canary_decisions_state
  ON mexc_canary_decisions(state, captured_at);

CREATE TABLE IF NOT EXISTS mexc_canary_outbox (
  outbox_id TEXT PRIMARY KEY,
  decision_id TEXT NOT NULL UNIQUE,
  created_at TEXT NOT NULL,
  available_at TEXT NOT NULL,
  status TEXT NOT NULL,
  attempt_count INTEGER NOT NULL DEFAULT 0,
  claimed_at TEXT,
  completed_at TEXT,
  last_error TEXT,
  result_json TEXT,
  FOREIGN KEY(decision_id) REFERENCES mexc_canary_decisions(decision_id)
);
CREATE INDEX IF NOT EXISTS idx_mexc_canary_outbox_status
  ON mexc_canary_outbox(status, available_at);

CREATE TABLE IF NOT EXISTS mexc_canary_risk_reservations (
  reservation_id TEXT PRIMARY KEY,
  decision_id TEXT NOT NULL UNIQUE,
  symbol TEXT NOT NULL,
  status TEXT NOT NULL,
  risk_usdt REAL NOT NULL,
  margin_usdt REAL,
  notional_usdt REAL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  release_reason TEXT,
  venue TEXT NOT NULL DEFAULT 'mexc',
  FOREIGN KEY(decision_id) REFERENCES mexc_canary_decisions(decision_id)
);
CREATE INDEX IF NOT EXISTS idx_mexc_canary_risk_status
  ON mexc_canary_risk_reservations(status);

CREATE TABLE IF NOT EXISTS mexc_canary_orders (
  order_row_id TEXT PRIMARY KEY,
  decision_id TEXT NOT NULL UNIQUE,
  external_oid TEXT NOT NULL UNIQUE,
  exchange_order_id TEXT,
  symbol TEXT NOT NULL,
  status TEXT NOT NULL,
  submitted_at TEXT,
  updated_at TEXT NOT NULL,
  plan_json TEXT NOT NULL,
  exchange_json TEXT,
  last_error TEXT,
  venue TEXT NOT NULL DEFAULT 'mexc',
  FOREIGN KEY(decision_id) REFERENCES mexc_canary_decisions(decision_id)
);

CREATE TABLE IF NOT EXISTS mexc_canary_positions (
  position_row_id TEXT PRIMARY KEY,
  decision_id TEXT NOT NULL UNIQUE,
  exchange_position_id TEXT,
  symbol TEXT NOT NULL,
  direction TEXT NOT NULL DEFAULT 'long',
  status TEXT NOT NULL,
  entry_price REAL NOT NULL,
  original_stop REAL NOT NULL,
  current_stop REAL NOT NULL,
  tp3 REAL NOT NULL,
  volume_contracts REAL NOT NULL,
  notional_usdt REAL NOT NULL,
  risk_usdt REAL NOT NULL,
  leverage INTEGER NOT NULL,
  liquidation_price REAL,
  highest_price REAL,
  favorable_price REAL,
  max_favorable_r REAL NOT NULL DEFAULT 0,
  protection_stage TEXT NOT NULL DEFAULT 'ORIGINAL_STOP',
  tpsl_order_id TEXT,
  opened_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  last_reconciled_at TEXT,
  last_price_at TEXT,
  last_monitor_error_at TEXT,
  monitor_error_count INTEGER NOT NULL DEFAULT 0,
  closed_at TEXT,
  realized_pnl_usdt REAL,
  fees_usdt REAL,
  funding_usdt REAL,
  exchange_json TEXT,
  venue TEXT NOT NULL DEFAULT 'mexc',
  FOREIGN KEY(decision_id) REFERENCES mexc_canary_decisions(decision_id)
);
CREATE INDEX IF NOT EXISTS idx_mexc_canary_positions_status
  ON mexc_canary_positions(status, symbol);

CREATE TABLE IF NOT EXISTS mexc_canary_exit_legs (
  decision_id TEXT NOT NULL,
  leg_index INTEGER NOT NULL,
  exchange_tpsl_id TEXT,
  exchange_order_id TEXT,
  external_oid TEXT,
  order_kind TEXT NOT NULL DEFAULT 'LEGACY_TPSL',
  target_price REAL NOT NULL,
  stop_price REAL NOT NULL,
  volume_contracts REAL NOT NULL,
  status TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  exchange_json TEXT NOT NULL,
  venue TEXT NOT NULL DEFAULT 'mexc',
  PRIMARY KEY(decision_id, leg_index),
  FOREIGN KEY(decision_id) REFERENCES mexc_canary_decisions(decision_id)
);
CREATE INDEX IF NOT EXISTS idx_mexc_canary_exit_legs_status
  ON mexc_canary_exit_legs(status, decision_id);

CREATE TABLE IF NOT EXISTS mexc_canary_events (
  event_id INTEGER PRIMARY KEY AUTOINCREMENT,
  event_at TEXT NOT NULL,
  decision_id TEXT,
  event_type TEXT NOT NULL,
  severity TEXT NOT NULL,
  payload_json TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_mexc_canary_events_at
  ON mexc_canary_events(event_at, event_type);

-- One row per real routing/preflight/submission attempt. The decision record
-- stays immutable; this append-only table makes a rejected venue and fallback
-- visible instead of leaving an empty decision-level rejection list.
CREATE TABLE IF NOT EXISTS mexc_canary_venue_attempts (
  attempt_id TEXT PRIMARY KEY,
  decision_id TEXT NOT NULL,
  attempted_at TEXT NOT NULL,
  venue TEXT NOT NULL,
  stage TEXT NOT NULL,
  status TEXT NOT NULL,
  reason TEXT,
  diagnostic_json TEXT NOT NULL,
  FOREIGN KEY(decision_id) REFERENCES mexc_canary_decisions(decision_id)
);
CREATE INDEX IF NOT EXISTS idx_mexc_canary_venue_attempts_decision
  ON mexc_canary_venue_attempts(decision_id, attempted_at);
CREATE INDEX IF NOT EXISTS idx_mexc_canary_venue_attempts_status
  ON mexc_canary_venue_attempts(venue, stage, status, attempted_at);

-- Delivery queue for exchange-confirmed lifecycle messages.  This is separate
-- from Paper signal alerts: a Paper alert says a candidate was accepted, while
-- this queue is created only after the exchange has confirmed a real fill.
CREATE TABLE IF NOT EXISTS mexc_canary_notification_outbox (
  notification_id TEXT PRIMARY KEY,
  decision_id TEXT NOT NULL,
  notification_kind TEXT NOT NULL,
  message_text TEXT NOT NULL,
  status TEXT NOT NULL,
  attempts INTEGER NOT NULL DEFAULT 0,
  next_attempt_at TEXT,
  last_error TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  sent_at TEXT,
  UNIQUE(decision_id, notification_kind),
  FOREIGN KEY(decision_id) REFERENCES mexc_canary_decisions(decision_id)
);
CREATE INDEX IF NOT EXISTS idx_mexc_canary_notification_outbox_due
  ON mexc_canary_notification_outbox(status, next_attempt_at);

CREATE TABLE IF NOT EXISTS mexc_canary_control (
  control_key TEXT PRIMARY KEY,
  control_value TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS mexc_canary_parity_plans (
  decision_id TEXT PRIMARY KEY,
  signal_id TEXT NOT NULL,
  symbol TEXT NOT NULL,
  plan_json TEXT NOT NULL,
  validation_json TEXT NOT NULL DEFAULT '{}',
  clean INTEGER NOT NULL DEFAULT 0,
  evidence_class TEXT NOT NULL DEFAULT 'historical_backfill',
  source TEXT NOT NULL,
  captured_at TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY(decision_id) REFERENCES mexc_canary_decisions(decision_id)
);

CREATE TABLE IF NOT EXISTS mexc_canary_parity_outcomes (
  decision_id TEXT NOT NULL,
  profile_id TEXT NOT NULL,
  signal_id TEXT NOT NULL,
  symbol TEXT NOT NULL,
  entry_at TEXT NOT NULL,
  entry_price REAL NOT NULL,
  original_stop REAL NOT NULL,
  tp1 REAL,
  tp2 REAL,
  tp3 REAL NOT NULL,
  risk_usdt REAL,
  closed INTEGER NOT NULL,
  clean INTEGER NOT NULL,
  status TEXT NOT NULL,
  close_at TEXT,
  close_price REAL,
  close_reason TEXT,
  gross_pnl_usdt REAL,
  fees_usdt REAL,
  slippage_usdt REAL,
  funding_usdt REAL,
  net_pnl_usdt REAL,
  max_favorable_r REAL,
  evidence_class TEXT NOT NULL DEFAULT 'historical_backfill',
  execution_json TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  PRIMARY KEY(decision_id, profile_id),
  FOREIGN KEY(decision_id) REFERENCES mexc_canary_decisions(decision_id)
);
CREATE INDEX IF NOT EXISTS idx_mexc_canary_parity_outcomes_profile
  ON mexc_canary_parity_outcomes(profile_id, status, updated_at);

CREATE TABLE IF NOT EXISTS mexc_canary_parity_candles (
  symbol TEXT NOT NULL,
  interval TEXT NOT NULL,
  candle_at INTEGER NOT NULL,
  open REAL NOT NULL,
  high REAL NOT NULL,
  low REAL NOT NULL,
  close REAL NOT NULL,
  captured_at TEXT NOT NULL,
  PRIMARY KEY(symbol, interval, candle_at)
);
CREATE INDEX IF NOT EXISTS idx_mexc_canary_parity_candles_range
  ON mexc_canary_parity_candles(symbol, interval, candle_at);
"""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def connect(
    db: str | Path,
    *,
    timeout_seconds: float = 5.0,
    busy_timeout_ms: int = 5000,
) -> sqlite3.Connection:
    # The live monitor ticks every three seconds. Waiting 30 seconds behind a
    # scheduler write made heartbeat and position reconciliation stale. Retry
    # the whole idempotent tick after a short bounded wait instead.
    conn = sqlite3.connect(str(db), timeout=max(0.0, float(timeout_seconds)))
    conn.row_factory = sqlite3.Row
    _apply_connection_pragmas(conn, busy_timeout_ms=busy_timeout_ms)
    return conn


def _apply_connection_pragmas(conn: sqlite3.Connection, *, busy_timeout_ms: int) -> None:
    """Set low-risk pragmas on every live connection.

    ``ensure_tables`` intentionally avoids write work when the schema is
    current, but short-lived CLI commands still need sane busy handling. WAL is
    attempted once per process/db and treated as best-effort; a busy database
    should not crash a read-only status command or a live monitor tick.
    """
    conn.execute(f"PRAGMA busy_timeout={max(0, int(busy_timeout_ms))}")
    # Keep compatibility with the existing live journal write order: some
    # risk and notification diagnostics are intentionally staged before a full
    # decision row exists. Lock-related pragmas are safe here; foreign-key
    # enforcement is not.
    for pragma in ("PRAGMA temp_store=MEMORY", "PRAGMA synchronous=NORMAL"):
        try:
            conn.execute(pragma)
        except sqlite3.DatabaseError:
            pass
    db_row = conn.execute("PRAGMA database_list").fetchone()
    db_path = str(db_row[2] if db_row and len(db_row) > 2 else ":memory:")
    if db_path in _PRAGMA_DATABASES:
        return
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        _PRAGMA_DATABASES.add(db_path)
    except sqlite3.DatabaseError:
        pass


def ensure_tables(conn: sqlite3.Connection) -> None:
    """Bootstrap the canary schema once per database/process.

    ``journal_mode=WAL`` and DDL both need a write lock.  They are correct at
    bootstrap, but doing them on every 3-second worker tick made an idle live
    monitor contend with the scheduler and exit on a transient lock.
    """
    db_row = conn.execute("PRAGMA database_list").fetchone()
    db_path = str(db_row[2] if db_row and len(db_row) > 2 else ":memory:")
    if db_path in _INITIALIZED_DATABASES:
        return
    # Most CLI commands and every monitor are separate processes, so the
    # in-memory cache above cannot by itself prevent repeated DDL/UPDATE work.
    # A fully migrated database must remain genuinely read-only on first use
    # in a new process; otherwise status/dashboard reads contend with the
    # tracker and the three-second live reconciliation loop.
    if _schema_is_current(conn):
        _INITIALIZED_DATABASES.add(db_path)
        return
    existing = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name='mexc_canary_control'"
    ).fetchone()
    if not existing:
        conn.execute("PRAGMA journal_mode=WAL")
    conn.executescript(DDL)
    _migrate_schema(conn)
    _reconcile_decision_states(conn)
    conn.execute(
        "INSERT OR IGNORE INTO mexc_canary_control(control_key,control_value,updated_at) VALUES(?,?,?)",
        ("kill_switch", "CLEAR", utc_now()),
    )
    conn.commit()
    _INITIALIZED_DATABASES.add(db_path)


def _schema_is_current(conn: sqlite3.Connection) -> bool:
    required_tables = {
        "mexc_canary_decisions", "mexc_canary_outbox",
        "mexc_canary_risk_reservations", "mexc_canary_orders",
        "mexc_canary_positions", "mexc_canary_exit_legs",
        "mexc_canary_events", "mexc_canary_venue_attempts",
        "mexc_canary_notification_outbox", "mexc_canary_control",
        "mexc_canary_parity_plans", "mexc_canary_parity_outcomes",
        "mexc_canary_parity_candles",
    }
    tables = {
        str(row[0]) for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
    }
    if not required_tables <= tables:
        return False

    required_columns = {
        "mexc_canary_decisions": {
            "economic_trade_key", "parent_decision_id", "recovery_sequence",
        },
        "mexc_canary_positions": {
            "direction", "favorable_price", "last_reconciled_at",
            "last_price_at", "last_monitor_error_at", "monitor_error_count", "venue",
        },
        "mexc_canary_parity_plans": {
            "validation_json", "clean", "evidence_class",
        },
        "mexc_canary_parity_outcomes": {"evidence_class"},
        "mexc_canary_exit_legs": {"order_kind", "exchange_order_id", "external_oid", "venue"},
    }
    for table, wanted in required_columns.items():
        present = {
            str(row[1]) for row in conn.execute(f"PRAGMA table_info({table})").fetchall()
        }
        if not wanted <= present:
            return False
    indexes = {
        str(row[1]) for row in conn.execute(
            "PRAGMA index_list(mexc_canary_decisions)"
        ).fetchall()
    }
    if "idx_mexc_canary_decisions_economic_key" not in indexes:
        return False
    return conn.execute(
        "SELECT 1 FROM mexc_canary_control WHERE control_key='kill_switch'"
    ).fetchone() is not None


def _reconcile_decision_states(conn: sqlite3.Connection) -> None:
    """Repair old capture-state rows from their authoritative outbox state.

    The decision payload itself is immutable.  Its state is operational
    telemetry, so a completed queue item must not remain labelled ``QUEUED``
    in the dashboard.  This migration is idempotent and changes no order,
    position, Paper, or signal data.
    """
    conn.execute(
        "UPDATE mexc_canary_decisions SET state=("
        "SELECT o.status FROM mexc_canary_outbox o "
        "WHERE o.decision_id=mexc_canary_decisions.decision_id) "
        "WHERE state IN ('QUEUED','PROCESSING') AND EXISTS("
        "SELECT 1 FROM mexc_canary_outbox o "
        "WHERE o.decision_id=mexc_canary_decisions.decision_id "
        "AND o.status NOT IN ('QUEUED','PROCESSING'))"
    )


def _migrate_schema(conn: sqlite3.Connection) -> None:
    """Idempotently upgrade databases created before monitor observability.

    A live database may predate these columns.  Never rebuild or delete a
    table: add nullable diagnostics in place, then keep all existing positions
    and audit records intact.
    """
    rows = conn.execute("PRAGMA table_info(mexc_canary_positions)").fetchall()
    columns = {str(row[1]) for row in rows}
    additions = (
        ("direction", "TEXT NOT NULL DEFAULT 'long'"),
        ("favorable_price", "REAL"),
        ("last_reconciled_at", "TEXT"),
        ("last_price_at", "TEXT"),
        ("last_monitor_error_at", "TEXT"),
        ("monitor_error_count", "INTEGER NOT NULL DEFAULT 0"),
    )
    for name, definition in additions:
        if name not in columns:
            conn.execute(f"ALTER TABLE mexc_canary_positions ADD COLUMN {name} {definition}")

    decision_columns = {
        str(row[1]) for row in conn.execute("PRAGMA table_info(mexc_canary_decisions)").fetchall()
    }
    for name, definition in (
        ("economic_trade_key", "TEXT"),
        ("parent_decision_id", "TEXT"),
        ("recovery_sequence", "INTEGER NOT NULL DEFAULT 0"),
    ):
        if name not in decision_columns:
            conn.execute(f"ALTER TABLE mexc_canary_decisions ADD COLUMN {name} {definition}")
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_mexc_canary_decisions_economic_key "
        "ON mexc_canary_decisions(economic_trade_key,captured_at)"
    )

    venue_tables = (
        "mexc_canary_risk_reservations", "mexc_canary_orders",
        "mexc_canary_positions", "mexc_canary_exit_legs",
    )
    for table in venue_tables:
        table_columns = {
            str(row[1]) for row in conn.execute(f"PRAGMA table_info({table})").fetchall()
        }
        if "venue" not in table_columns:
            conn.execute(
                f"ALTER TABLE {table} ADD COLUMN venue TEXT NOT NULL DEFAULT 'mexc'"
            )

    plan_columns = {str(row[1]) for row in conn.execute(
        "PRAGMA table_info(mexc_canary_parity_plans)"
    ).fetchall()}
    for name, definition in (
        ("validation_json", "TEXT NOT NULL DEFAULT '{}'"),
        ("clean", "INTEGER NOT NULL DEFAULT 0"),
        ("evidence_class", "TEXT NOT NULL DEFAULT 'historical_backfill'"),
    ):
        if name not in plan_columns:
            conn.execute(f"ALTER TABLE mexc_canary_parity_plans ADD COLUMN {name} {definition}")
    outcome_columns = {str(row[1]) for row in conn.execute(
        "PRAGMA table_info(mexc_canary_parity_outcomes)"
    ).fetchall()}
    if "evidence_class" not in outcome_columns:
        conn.execute(
            "ALTER TABLE mexc_canary_parity_outcomes ADD COLUMN evidence_class "
            "TEXT NOT NULL DEFAULT 'historical_backfill'"
        )
    exit_columns = {str(row[1]) for row in conn.execute(
        "PRAGMA table_info(mexc_canary_exit_legs)"
    ).fetchall()}
    for name, definition in (
        ("exchange_order_id", "TEXT"),
        ("external_oid", "TEXT"),
        ("order_kind", "TEXT NOT NULL DEFAULT 'LEGACY_TPSL'"),
    ):
        if name not in exit_columns:
            conn.execute(f"ALTER TABLE mexc_canary_exit_legs ADD COLUMN {name} {definition}")


def set_monitor_heartbeat(conn: sqlite3.Connection, *, status: str, live_armed: bool,
                          active_positions: int, detail: dict[str, Any] | None = None) -> None:
    """Persist the most recent supervising tick without emitting a row per tick."""
    now = utc_now()
    payload = {
        "at": now,
        "status": str(status),
        "live_armed": bool(live_armed),
        "active_positions": int(active_positions),
        "detail": detail or {},
    }
    conn.execute(
        "INSERT INTO mexc_canary_control(control_key,control_value,updated_at) VALUES(?,?,?) "
        "ON CONFLICT(control_key) DO UPDATE SET control_value=excluded.control_value,updated_at=excluded.updated_at",
        ("monitor_heartbeat", json.dumps(payload, sort_keys=True), now),
    )


def monitor_heartbeat(conn: sqlite3.Connection) -> dict[str, Any] | None:
    row = conn.execute(
        "SELECT control_value,updated_at FROM mexc_canary_control WHERE control_key='monitor_heartbeat'"
    ).fetchone()
    if not row:
        return None
    try:
        payload = json.loads(str(row[0]))
    except (TypeError, json.JSONDecodeError):
        payload = {"status": "INVALID"}
    payload["updated_at"] = str(row[1])
    return payload


def _parse_control_time(value: Any) -> datetime | None:
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def try_claim_control_lease(
    conn: sqlite3.Connection, *, key: str, owner: str, ttl_seconds: float
) -> bool:
    """Claim a short-lived control lease without blocking other monitor work."""
    now_dt = datetime.now(timezone.utc)
    expires_at = (now_dt + timedelta(seconds=max(1.0, float(ttl_seconds)))).isoformat()
    conn.execute("BEGIN IMMEDIATE")
    row = conn.execute(
        "SELECT control_value FROM mexc_canary_control WHERE control_key=?",
        (key,),
    ).fetchone()
    if row:
        try:
            payload = json.loads(str(row[0]))
        except (TypeError, json.JSONDecodeError):
            payload = {}
        current_owner = str(payload.get("owner") or "")
        current_expires = _parse_control_time(payload.get("expires_at"))
        if current_owner and current_owner != owner and current_expires and current_expires > now_dt:
            conn.commit()
            return False
    payload = {"owner": owner, "expires_at": expires_at}
    conn.execute(
        "INSERT INTO mexc_canary_control(control_key,control_value,updated_at) VALUES(?,?,?) "
        "ON CONFLICT(control_key) DO UPDATE SET "
        "control_value=excluded.control_value,updated_at=excluded.updated_at",
        (key, json.dumps(payload, sort_keys=True), now_dt.isoformat()),
    )
    conn.commit()
    return True


def release_control_lease(conn: sqlite3.Connection, *, key: str, owner: str) -> None:
    """Release a lease only when the caller still owns it."""
    conn.execute("BEGIN IMMEDIATE")
    row = conn.execute(
        "SELECT control_value FROM mexc_canary_control WHERE control_key=?",
        (key,),
    ).fetchone()
    if row:
        try:
            payload = json.loads(str(row[0]))
        except (TypeError, json.JSONDecodeError):
            payload = {}
        if str(payload.get("owner") or "") == owner:
            conn.execute("DELETE FROM mexc_canary_control WHERE control_key=?", (key,))
    conn.commit()


def upsert_parity_plan(conn: sqlite3.Connection, *, decision_id: str, signal_id: str,
                       symbol: str, plan: dict[str, Any], source: str,
                       captured_at: str, validation: dict[str, Any] | None = None,
                       clean: bool = False,
                       evidence_class: str = "historical_backfill") -> None:
    """Store a MEXC-validated plan for isolated parity simulation only."""
    now = utc_now()
    cols = (
        "decision_id", "signal_id", "symbol", "plan_json", "validation_json", "clean",
        "evidence_class", "source", "captured_at", "created_at", "updated_at",
    )
    values = (
        decision_id, signal_id, symbol, json.dumps(plan, sort_keys=True),
        json.dumps(validation or {}, sort_keys=True), int(bool(clean)), evidence_class,
        source, captured_at, now, now,
    )
    conn.execute(
        f"INSERT INTO mexc_canary_parity_plans({','.join(cols)}) VALUES({','.join('?' for _ in cols)}) "
        "ON CONFLICT(decision_id) DO UPDATE SET plan_json=excluded.plan_json,"
        "validation_json=excluded.validation_json,clean=excluded.clean,"
        "evidence_class=excluded.evidence_class,source=excluded.source,"
        "captured_at=excluded.captured_at,updated_at=excluded.updated_at",
        values,
    )


def is_database_busy(exc: BaseException) -> bool:
    """Whether SQLite rejected an operation because another writer holds the DB."""
    text = str(exc).lower()
    return isinstance(exc, sqlite3.OperationalError) and (
        "database is locked" in text or "database is busy" in text or "database schema is locked" in text
    )


def event(conn: sqlite3.Connection, event_type: str, *, decision_id: str | None = None,
          severity: str = "INFO", payload: dict[str, Any] | None = None) -> None:
    conn.execute(
        "INSERT INTO mexc_canary_events(event_at,decision_id,event_type,severity,payload_json) "
        "VALUES(?,?,?,?,?)",
        (utc_now(), decision_id, event_type, severity, json.dumps(payload or {}, sort_keys=True)),
    )


def record_venue_attempt(
    conn: sqlite3.Connection,
    *,
    decision_id: str,
    venue: str,
    stage: str,
    status: str,
    reason: str | None = None,
    diagnostic: dict[str, Any] | None = None,
) -> str:
    """Persist one exchange-routing fact without altering the decision."""
    attempt_id = str(uuid.uuid4())
    conn.execute(
        "INSERT INTO mexc_canary_venue_attempts("
        "attempt_id,decision_id,attempted_at,venue,stage,status,reason,diagnostic_json"
        ") VALUES(?,?,?,?,?,?,?,?)",
        (
            attempt_id,
            str(decision_id),
            utc_now(),
            str(venue).lower(),
            str(stage).upper(),
            str(status).upper(),
            str(reason or "")[:500] or None,
            json.dumps(diagnostic or {}, sort_keys=True, default=str),
        ),
    )
    return attempt_id


def event_if_due(
    conn: sqlite3.Connection,
    event_type: str,
    *,
    decision_id: str | None = None,
    severity: str = "INFO",
    payload: dict[str, Any] | None = None,
    cooldown_seconds: float = 60.0,
) -> bool:
    """Write a recurring operational event only once per cooldown window.

    Reconciliation itself must stay fast: an MEXC timeout is retried on the
    next tick. This helper only prevents one unchanged outage from flooding the
    event journal and obscuring the first actionable alert.
    """
    if decision_id is None:
        row = conn.execute(
            "SELECT event_at FROM mexc_canary_events "
            "WHERE event_type=? AND decision_id IS NULL ORDER BY event_at DESC LIMIT 1",
            (event_type,),
        ).fetchone()
    else:
        row = conn.execute(
            "SELECT event_at FROM mexc_canary_events "
            "WHERE event_type=? AND decision_id=? ORDER BY event_at DESC LIMIT 1",
            (event_type, decision_id),
        ).fetchone()
    previous = _parse_control_time(row[0]) if row else None
    now = datetime.now(timezone.utc)
    if previous is not None and (now - previous).total_seconds() < max(0.0, cooldown_seconds):
        return False
    event(conn, event_type, decision_id=decision_id, severity=severity, payload=payload)
    return True


def enqueue_notification(conn: sqlite3.Connection, *, decision_id: str,
                         notification_kind: str, message_text: str) -> bool:
    """Durably stage one operator notification per real lifecycle transition."""
    now = utc_now()
    inserted = conn.execute(
        "INSERT OR IGNORE INTO mexc_canary_notification_outbox("
        "notification_id,decision_id,notification_kind,message_text,status,attempts,"
        "next_attempt_at,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?)",
        (str(uuid.uuid4()), decision_id, notification_kind, message_text, "PENDING", 0,
         now, now, now),
    ).rowcount == 1
    return inserted


def claim_next_notification(conn: sqlite3.Connection, *, now: str | None = None) -> dict[str, Any] | None:
    """Claim a due Telegram delivery.  Claiming never touches execution state."""
    now = now or utc_now()
    conn.execute("BEGIN IMMEDIATE")
    row = conn.execute(
        "SELECT * FROM mexc_canary_notification_outbox "
        "WHERE status='PENDING' AND (next_attempt_at IS NULL OR next_attempt_at<=?) "
        "ORDER BY created_at LIMIT 1",
        (now,),
    ).fetchone()
    if row is None:
        conn.commit()
        return None
    changed = conn.execute(
        "UPDATE mexc_canary_notification_outbox SET status='SENDING',updated_at=? "
        "WHERE notification_id=? AND status='PENDING'",
        (now, row["notification_id"]),
    ).rowcount
    conn.commit()
    return dict(row) if changed == 1 else None


def complete_notification(conn: sqlite3.Connection, *, notification_id: str) -> None:
    now = utc_now()
    conn.execute(
        "UPDATE mexc_canary_notification_outbox SET status='SENT',attempts=attempts+1,"
        "sent_at=?,updated_at=?,last_error=NULL WHERE notification_id=? AND status='SENDING'",
        (now, now, notification_id),
    )


def defer_notification(conn: sqlite3.Connection, *, notification_id: str,
                       attempts: int, error: str, max_attempts: int = 5) -> str:
    """Return the terminal delivery state after a bounded, delivery-only retry."""
    next_attempts = int(attempts or 0) + 1
    state = "DEAD" if next_attempts >= max(1, int(max_attempts)) else "PENDING"
    delay_seconds = min(300, 5 * (2 ** min(next_attempts, 5)))
    now_dt = datetime.now(timezone.utc)
    next_at = (now_dt + timedelta(seconds=delay_seconds)).isoformat()
    conn.execute(
        "UPDATE mexc_canary_notification_outbox SET status=?,attempts=?,next_attempt_at=?,"
        "last_error=?,updated_at=? WHERE notification_id=? AND status='SENDING'",
        (state, next_attempts, next_at, str(error)[:240], now_dt.isoformat(), notification_id),
    )
    return state


def kill_switch_state(conn: sqlite3.Connection) -> str:
    row = conn.execute(
        "SELECT control_value FROM mexc_canary_control WHERE control_key='kill_switch'"
    ).fetchone()
    return str(row[0] if row else "TRIPPED").upper()


def set_kill_switch(conn: sqlite3.Connection, state: str, reason: str) -> None:
    value = str(state).upper()
    if value not in {"CLEAR", "TRIPPED"}:
        raise ValueError("kill switch state must be CLEAR or TRIPPED")
    now = utc_now()
    conn.execute(
        "INSERT INTO mexc_canary_control(control_key,control_value,updated_at) VALUES(?,?,?) "
        "ON CONFLICT(control_key) DO UPDATE SET control_value=excluded.control_value,updated_at=excluded.updated_at",
        ("kill_switch", value, now),
    )
    event(conn, "KILL_SWITCH_CHANGED", severity="CRITICAL" if value == "TRIPPED" else "WARNING",
          payload={"state": value, "reason": reason})
    conn.commit()


def insert_decision(conn: sqlite3.Connection, record: dict[str, Any], *, queue: bool) -> dict[str, Any]:
    ensure_tables(conn)
    economic_key = str(record.get("economic_trade_key") or "").strip()
    parent_decision_id = str(record.get("parent_decision_id") or "").strip()
    duplicate = None
    if queue and economic_key:
        params: list[Any] = [economic_key, str(record.get("decision_id") or "")]
        parent_clause = ""
        if parent_decision_id:
            parent_clause = " AND d.decision_id<>?"
            params.append(parent_decision_id)
        duplicate = conn.execute(
            "SELECT d.decision_id,d.signal_id,d.state FROM mexc_canary_decisions d "
            "WHERE d.economic_trade_key=? AND d.decision_id<>?" + parent_clause + " AND ("
            "d.state IN ('QUEUED','PROCESSING','SUBMITTED','SUBMISSION_UNKNOWN') OR "
            "EXISTS(SELECT 1 FROM mexc_canary_orders o WHERE o.decision_id=d.decision_id "
            "AND o.status IN ('SUBMITTING','SUBMITTED','PENDING','SUBMISSION_UNKNOWN','FILLED')) OR "
            "EXISTS(SELECT 1 FROM mexc_canary_positions p WHERE p.decision_id=d.decision_id)) "
            "ORDER BY d.captured_at DESC LIMIT 1",
            params,
        ).fetchone()
    if duplicate is not None:
        record = dict(record)
        reasons = json.loads(str(record.get("rejection_reasons_json") or "[]"))
        reasons.append("DUPLICATE_ECONOMIC_TRADE")
        record["eligible"] = 0
        record["state"] = "REJECTED_DUPLICATE_ECONOMIC_TRADE"
        record["rejection_reasons_json"] = json.dumps(sorted(set(reasons)))
        queue = False
    # Every live route (standard Paper, stocks bridge, crypto invest and
    # liquidity sweep) converges here. Capture one common quality snapshot
    # before the outbox row is created. The configured evidence phase is
    # fail-open: an agent failure is journalled and never delays or cancels the
    # deterministic live policy.
    try:
        from src.quality_agents.runner import evaluate_signal_on_connection

        frozen = json.loads(str(record.get("decision_json") or "{}"))
        quality_signal = {
            "signal_id": record.get("signal_id") or frozen.get("signal_id"),
            "symbol": record.get("symbol") or frozen.get("symbol"),
            "asset_class": frozen.get("asset_class") or "crypto",
            "mode": record.get("mode") or frozen.get("mode"),
            "direction": frozen.get("direction"),
            "tier": frozen.get("tier"),
            "score": frozen.get("score"),
            "paper_execution_entry_mode": record.get("entry_mode") or frozen.get("entry_mode"),
        }
        quality_payload = {
            "signal_id": quality_signal["signal_id"],
            "decision_at": record.get("captured_at") or frozen.get("captured_at"),
            "entry_used": frozen.get("entry_price"),
            "stop": frozen.get("original_stop"),
            "tp1": frozen.get("tp1"),
            "tp2": frozen.get("tp2"),
            "tp3": frozen.get("tp3"),
            "entry_age_seconds": frozen.get("entry_age_seconds"),
            "entry_time_basis": frozen.get("entry_time_basis"),
            "current_price_revalidated": frozen.get("current_price_revalidated"),
            "size_weight": frozen.get("live_risk_multiplier") or frozen.get("paper_size_weight"),
            "paper_execution_entry_mode": quality_signal["paper_execution_entry_mode"],
            "news_supported": frozen.get("news_supported"),
        }
        quality = evaluate_signal_on_connection(
            conn, quality_signal, quality_payload, stage="live_decision_insert",
        )
        quality_summary = {
            "status": quality.get("status"),
            "reducer_decision_id": quality.get("reducer_decision_id"),
            "recommended_action": quality.get("recommended_action"),
            "applied_action": quality.get("applied_action"),
            "reason_codes": quality.get("reason_codes") or [],
            "verdict_ids": [
                item.get("verdict_id") for item in (quality.get("verdicts") or [])
                if item.get("verdict_id")
            ],
        }
        frozen["quality_agents"] = quality_summary
        applied = str(quality.get("applied_action") or "ALLOW")
        if applied == "BLOCK_HARD":
            reasons = json.loads(str(record.get("rejection_reasons_json") or "[]"))
            reasons.extend(["QUALITY_AGENT_BLOCK_HARD", *(quality.get("reason_codes") or [])])
            record["eligible"] = 0
            record["state"] = "REJECTED_QUALITY_AGENT"
            record["rejection_reasons_json"] = json.dumps(sorted(set(reasons)))
            queue = False
        elif applied == "ALLOW_HALF_SIZE":
            current = float(frozen.get("live_risk_multiplier") or 1.0)
            frozen["live_risk_multiplier"] = min(current, 0.5)
        elif applied == "ALLOW_NO_CATALYST_BOOST":
            frozen["quality_agent_catalyst_boost_allowed"] = False
        record["decision_json"] = json.dumps(frozen, sort_keys=True)
        body = json.dumps(frozen, sort_keys=True, separators=(",", ":"), default=str)
        record["decision_hash"] = hashlib.sha256(body.encode("utf-8")).hexdigest()
        conn.execute(
            "UPDATE quality_agent_execution_incidents SET decision_id=? "
            "WHERE signal_id=? AND stage='live_decision_insert' AND decision_id IS NULL",
            (record.get("decision_id"), record.get("signal_id")),
        )
    except Exception as exc:
        event(
            conn, "QUALITY_AGENT_CAPTURE_FAILED", decision_id=record.get("decision_id"),
            severity="WARNING", payload={"error_type": type(exc).__name__},
        )
    cols = (
        "decision_id", "signal_id", "captured_at", "paper_alert_id", "symbol", "mode",
        "entry_mode", "eligible", "state", "rejection_reasons_json", "decision_json",
        "decision_hash", "config_hash", "decision_context_type", "economic_trade_key",
        "parent_decision_id", "recovery_sequence",
    )
    values = [
        0 if c == "recovery_sequence" and record.get(c) is None else record.get(c)
        for c in cols
    ]
    cur = conn.execute(
        f"INSERT OR IGNORE INTO mexc_canary_decisions({','.join(cols)}) "
        f"VALUES({','.join('?' for _ in cols)})",
        values,
    )
    inserted = cur.rowcount == 1
    if inserted and queue:
        now = utc_now()
        conn.execute(
            "INSERT INTO mexc_canary_outbox(outbox_id,decision_id,created_at,available_at,status) "
            "VALUES(?,?,?,?,?)",
            (str(uuid.uuid4()), record["decision_id"], now, now, "QUEUED"),
        )
    if inserted:
        event(conn, "DECISION_CAPTURED", decision_id=record["decision_id"],
              severity="INFO" if record.get("eligible") else "WARNING",
              payload={"eligible": bool(record.get("eligible")), "state": record.get("state")})
    conn.commit()
    return {"inserted": inserted, "decision_id": record["decision_id"],
            "queued": bool(inserted and queue),
            "duplicate_economic_trade": bool(duplicate is not None)}


def claim_next(conn: sqlite3.Connection) -> dict[str, Any] | None:
    conn.execute("BEGIN IMMEDIATE")
    row = conn.execute(
        "SELECT o.*,d.decision_json,d.config_hash,d.captured_at AS decision_captured_at "
        "FROM mexc_canary_outbox o "
        "JOIN mexc_canary_decisions d ON d.decision_id=o.decision_id "
        "WHERE o.status='QUEUED' AND o.available_at<=? ORDER BY o.created_at LIMIT 1",
        (utc_now(),),
    ).fetchone()
    if not row:
        conn.commit()
        return None
    now = utc_now()
    changed = conn.execute(
        "UPDATE mexc_canary_outbox SET status='PROCESSING',claimed_at=?,attempt_count=attempt_count+1 "
        "WHERE outbox_id=? AND status='QUEUED'",
        (now, row["outbox_id"]),
    ).rowcount
    if changed == 1:
        conn.execute(
            "UPDATE mexc_canary_decisions SET state='PROCESSING' "
            "WHERE decision_id=? AND state='QUEUED'",
            (row["decision_id"],),
        )
    conn.commit()
    return dict(row) if changed == 1 else None


def complete_outbox(conn: sqlite3.Connection, outbox_id: str, status: str,
                    result: dict[str, Any] | None = None, error: str | None = None) -> None:
    conn.execute(
        "UPDATE mexc_canary_outbox SET status=?,completed_at=?,last_error=?,result_json=? "
        "WHERE outbox_id=?",
        (status, utc_now(), error, json.dumps(result or {}, sort_keys=True), outbox_id),
    )
    conn.execute(
        "UPDATE mexc_canary_decisions SET state=? WHERE decision_id=("
        "SELECT decision_id FROM mexc_canary_outbox WHERE outbox_id=?) "
        "AND state IN ('QUEUED','PROCESSING')",
        (status, outbox_id),
    )
    conn.commit()


def defer_outbox(conn: sqlite3.Connection, outbox_id: str, *, delay_seconds: float,
                 result: dict[str, Any] | None = None, error: str | None = None) -> None:
    """Return a transiently untradable quote to the queue without changing its decision.

    The immutable entry snapshot and its expiry still govern the next attempt;
    this only gives a briefly widened order book a chance to normalize.
    """
    delay = max(0.1, float(delay_seconds))
    available_at = (datetime.now(timezone.utc) + timedelta(seconds=delay)).isoformat()
    conn.execute(
        "UPDATE mexc_canary_outbox SET status='QUEUED',available_at=?,claimed_at=NULL,"
        "completed_at=NULL,last_error=?,result_json=? WHERE outbox_id=?",
        (available_at, error, json.dumps(result or {}, sort_keys=True), outbox_id),
    )
    conn.execute(
        "UPDATE mexc_canary_decisions SET state='QUEUED' WHERE decision_id=("
        "SELECT decision_id FROM mexc_canary_outbox WHERE outbox_id=?) AND state='PROCESSING'",
        (outbox_id,),
    )
    conn.commit()


def _base_symbol(symbol: Any) -> str:
    return str(symbol or "").upper().replace("_", "/").split("/", 1)[0]


def reserve_risk(conn: sqlite3.Connection, *, decision_id: str, symbol: str, risk_usdt: float,
                 margin_usdt: float, notional_usdt: float, max_risk_usdt: float,
                 max_margin_usdt: float | None, max_notional_usdt: float | None,
                 max_open_same_symbol: int | None = None,
                 venue: str = "mexc",
                 allow_rebind_released: bool = False) -> dict[str, Any]:
    conn.execute("BEGIN IMMEDIATE")
    duplicate = conn.execute(
        "SELECT * FROM mexc_canary_risk_reservations WHERE decision_id=?", (decision_id,)
    ).fetchone()
    if duplicate and not (
        allow_rebind_released and str(duplicate["status"] or "").upper() == "RELEASED"
    ):
        conn.commit()
        return {"ok": False, "reason": "duplicate_reservation"}
    row = conn.execute(
        "SELECT COALESCE(SUM(risk_usdt),0),COALESCE(SUM(margin_usdt),0),"
        "COALESCE(SUM(notional_usdt),0) FROM mexc_canary_risk_reservations "
        "WHERE status IN ('RESERVED','OPEN')"
    ).fetchone()
    active_risk, active_margin, active_notional = map(float, row)
    reason = None
    if active_risk + risk_usdt > max_risk_usdt + 1e-9:
        reason = "max_concurrent_risk"
    elif max_margin_usdt is not None and active_margin + margin_usdt > max_margin_usdt + 1e-9:
        reason = "max_total_margin"
    elif (max_notional_usdt is not None
          and active_notional + notional_usdt > max_notional_usdt + 1e-9):
        reason = "max_gross_notional"
    # Enforce the same-symbol cap inside this IMMEDIATE transaction so two
    # rapidly queued decisions cannot both observe an empty live book.
    if reason is None and max_open_same_symbol is not None:
        active = conn.execute(
            "SELECT r.symbol FROM mexc_canary_risk_reservations r "
            "WHERE r.status IN ('RESERVED','OPEN')"
        ).fetchall()
        candidate = _base_symbol(symbol)
        same_symbol = sum(1 for row in active if _base_symbol(row[0]) == candidate)
        if same_symbol >= int(max_open_same_symbol):
            reason = "max_open_same_symbol"
    if reason:
        conn.commit()
        return {"ok": False, "reason": reason, "active_risk_usdt": active_risk}
    now = utc_now()
    if duplicate:
        conn.execute(
            "UPDATE mexc_canary_risk_reservations SET symbol=?,status='RESERVED',risk_usdt=?,"
            "margin_usdt=?,notional_usdt=?,updated_at=?,release_reason=NULL,venue=? "
            "WHERE decision_id=? AND status='RELEASED'",
            (symbol, risk_usdt, margin_usdt, notional_usdt, now,
             str(venue).lower(), decision_id),
        )
        event_type = "RISK_REBOUND_TO_FALLBACK_VENUE"
    else:
        conn.execute(
            "INSERT INTO mexc_canary_risk_reservations(" 
            "reservation_id,decision_id,symbol,status,risk_usdt,margin_usdt,notional_usdt,created_at,updated_at,venue) "
            "VALUES(?,?,?,?,?,?,?,?,?,?)",
            (str(uuid.uuid4()), decision_id, symbol, "RESERVED", risk_usdt, margin_usdt,
             notional_usdt, now, now, str(venue).lower()),
        )
        event_type = "RISK_RESERVED"
    event(conn, event_type, decision_id=decision_id,
          payload={"risk_usdt": risk_usdt, "active_risk_before": active_risk})
    conn.commit()
    return {"ok": True, "active_risk_before": active_risk,
            "active_risk_after": active_risk + risk_usdt}


def release_risk(conn: sqlite3.Connection, decision_id: str, reason: str) -> None:
    conn.execute(
        "UPDATE mexc_canary_risk_reservations SET status='RELEASED',updated_at=?,release_reason=? "
        "WHERE decision_id=? AND status IN ('RESERVED','OPEN')",
        (utc_now(), reason, decision_id),
    )
    event(conn, "RISK_RELEASED", decision_id=decision_id, payload={"reason": reason})
    conn.commit()
