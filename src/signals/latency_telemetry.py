"""Execution-latency telemetry read-model (additive, 2026-07-05) — WRITE-ONLY event log.

A single append-only table (`execution_latency_events`) that records *when* each step of the
paper-entry lifecycle happened, so latency can be measured as a first-class risk metric instead of
being hidden inside paper PnL. This is pure observability:

  * it NEVER places an order, NEVER changes score / tier / actionability / TP / SL / sizing,
  * it NEVER promotes anything to live/paper,
  * every write is fail-open — a telemetry error can never block the tracker, monitor, or an alert.

Event types (the paper-entry lifecycle):
    signal_created, pending_tracker_seen, market_data_refreshed, entry_condition_detected,
    paper_entry_alert_sent, paper_entry_alert_failed, close_detected, close_alert_sent

The table self-creates on first write (mirrors src/signals/entry_latency_audit.py), so no change to
SQLiteStore.init_db is required.
"""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from typing import Any

from src.config import load_config

# Telemetry is useful only when it never sits on the order/alert path behind a
# busy SQLite writer.  Fail open quickly; the next monitor cycle can record a
# later diagnostic event without delaying an execution decision.
_WRITE_TIMEOUT_SECONDS = 0.25

EVENT_TYPES: tuple[str, ...] = (
    "signal_created",
    "pending_signal_discovered",
    "pending_tracker_seen",
    "market_data_refreshed",
    "strategy_entry_ready",
    "entry_condition_detected",
    "paper_entry_decision_completed",
    "paper_entry_alert_sent",
    "paper_entry_alert_queued",
    "paper_entry_alert_skipped",
    "paper_entry_alert_failed",
    "close_detected",
    "close_alert_sent",
    "pending_tracker_db_retry",
    "pending_tracker_db_locked",
    "pending_tracker_lock_retry",
    "pending_tracker_stale_data_blocked",
    "pending_monitor_tick_gap",
    "entry_observed_late",
    "mexc_decision_captured",
    "mexc_decision_rejected",
    "mexc_preflight_started",
    "mexc_preflight_passed",
    "mexc_preflight_rejected",
    "mexc_order_submitted",
    "mexc_order_submission_unknown",
)

# Per-signal transition events: at most ONE per (signal_id, event_type, source). Use emit_once for
# these so a repeated tracker tick can't flood the table with identical rows. The rest
# (signal_created / pending_tracker_seen / market_data_refreshed) are legitimately repeatable → emit.
TRANSITION_EVENTS: frozenset[str] = frozenset({
    "pending_signal_discovered", "strategy_entry_ready",
    "entry_condition_detected", "paper_entry_alert_sent", "paper_entry_alert_skipped",
    "paper_entry_alert_queued",
    "paper_entry_decision_completed",
    "paper_entry_alert_failed", "close_detected", "close_alert_sent", "entry_observed_late",
    "mexc_decision_captured", "mexc_decision_rejected", "mexc_preflight_started",
    "mexc_preflight_passed", "mexc_preflight_rejected", "mexc_order_submitted",
    "mexc_order_submission_unknown",
})

_CREATE = """
CREATE TABLE IF NOT EXISTS execution_latency_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_at TEXT NOT NULL,
    event_type TEXT NOT NULL,
    signal_id TEXT,
    symbol TEXT,
    asset_class TEXT,
    mode TEXT,
    source TEXT,
    market_data_timestamp TEXT,
    market_data_age_sec REAL,
    scheduler_cycle_id TEXT,
    worker_id TEXT,
    latency_from_signal_sec REAL,
    latency_from_entry_touch_sec REAL,
    latency_from_bar_open_sec REAL,
    entry_bar_open_at TEXT,
    entry_time_basis TEXT,
    current_price_revalidated INTEGER,
    strategy_ready_at TEXT,
    latency_from_strategy_ready_sec REAL,
    stage_runtime_ms REAL,
    note TEXT
);
"""
_INDEXES = (
    "CREATE INDEX IF NOT EXISTS idx_ele_event_type ON execution_latency_events(event_type)",
    "CREATE INDEX IF NOT EXISTS idx_ele_signal ON execution_latency_events(signal_id)",
    "CREATE INDEX IF NOT EXISTS idx_ele_event_at ON execution_latency_events(event_at)",
)


def _db_path(db: Any) -> str:
    if db is None:
        return str(load_config().db_path)
    # accept a SQLiteStore, a Path, or a str
    return str(getattr(db, "db_path", db))


def _now_iso(now: datetime | None = None) -> str:
    return (now or datetime.now(timezone.utc)).isoformat()


def _ensure(conn) -> None:
    conn.execute(_CREATE)
    existing = {r[1] for r in conn.execute("PRAGMA table_info(execution_latency_events)")}
    for name, typ in (
        ("latency_from_bar_open_sec", "REAL"),
        ("entry_bar_open_at", "TEXT"),
        ("entry_time_basis", "TEXT"),
        ("current_price_revalidated", "INTEGER"),
        ("strategy_ready_at", "TEXT"),
        ("latency_from_strategy_ready_sec", "REAL"),
        ("stage_runtime_ms", "REAL"),
    ):
        if name not in existing:
            conn.execute(f"ALTER TABLE execution_latency_events ADD COLUMN {name} {typ}")
    for idx in _INDEXES:
        conn.execute(idx)


def emit(
    db: Any = None,
    *,
    event_type: str,
    signal_id: str | None = None,
    symbol: str | None = None,
    asset_class: str | None = None,
    mode: str | None = None,
    source: str | None = None,
    market_data_timestamp: str | None = None,
    market_data_age_sec: float | None = None,
    scheduler_cycle_id: str | None = None,
    worker_id: str | None = None,
    latency_from_signal_sec: float | None = None,
    latency_from_entry_touch_sec: float | None = None,
    latency_from_bar_open_sec: float | None = None,
    entry_bar_open_at: str | None = None,
    entry_time_basis: str | None = None,
    current_price_revalidated: bool | None = None,
    strategy_ready_at: str | None = None,
    latency_from_strategy_ready_sec: float | None = None,
    stage_runtime_ms: float | None = None,
    event_at: str | None = None,
    note: str | None = None,
) -> bool:
    """Append one latency event. FAIL-OPEN: returns False on any error, never raises — a telemetry
    write must never block the tracker/monitor/alert path. `db` may be a SQLiteStore, path, or None
    (default DB). Unknown `event_type` values are still written (forward-compatible) but the caller
    should use one of EVENT_TYPES."""
    try:
        conn = sqlite3.connect(_db_path(db), timeout=_WRITE_TIMEOUT_SECONDS)
        try:
            conn.execute("PRAGMA busy_timeout=250")
            _ensure(conn)
            conn.execute(
                "INSERT INTO execution_latency_events (event_at, event_type, signal_id, symbol, "
                "asset_class, mode, source, market_data_timestamp, market_data_age_sec, "
                "scheduler_cycle_id, worker_id, latency_from_signal_sec, latency_from_entry_touch_sec, "
                "latency_from_bar_open_sec, entry_bar_open_at, entry_time_basis, "
                "current_price_revalidated, strategy_ready_at, latency_from_strategy_ready_sec, "
                "stage_runtime_ms, note) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (event_at or _now_iso(), str(event_type), signal_id, symbol, asset_class, mode, source,
                 market_data_timestamp, market_data_age_sec, scheduler_cycle_id, worker_id,
                 latency_from_signal_sec, latency_from_entry_touch_sec,
                 latency_from_bar_open_sec, entry_bar_open_at, entry_time_basis,
                 None if current_price_revalidated is None else int(bool(current_price_revalidated)),
                 strategy_ready_at, latency_from_strategy_ready_sec, stage_runtime_ms, note),
            )
            conn.commit()
        finally:
            conn.close()
        return True
    except Exception:
        return False


def emit_discovered(db: Any, signal: dict[str, Any], *, source: str,
                    worker_id: str | None = None, now: datetime | None = None) -> bool:
    """Record the first time a fast monitor roster contained this signal."""
    now = now or datetime.now(timezone.utc)
    created = None
    try:
        created = datetime.fromisoformat(str(signal.get("created_at") or "").replace("Z", "+00:00"))
        if created.tzinfo is None:
            created = created.replace(tzinfo=timezone.utc)
    except (TypeError, ValueError):
        created = None
    latency = round((now - created).total_seconds(), 3) if created is not None else None
    return emit_once(
        db,
        event_type="pending_signal_discovered",
        signal_id=str(signal.get("signal_id") or "") or None,
        symbol=str(signal.get("symbol") or "") or None,
        asset_class=str(signal.get("asset_class") or "crypto"),
        mode=str(signal.get("mode") or "") or None,
        source=source,
        worker_id=worker_id,
        latency_from_signal_sec=latency,
        event_at=now.isoformat(),
    )


def emit_once(db: Any = None, *, event_type: str, signal_id: str | None = None,
              source: str | None = None, **kwargs) -> bool:
    """Emit an event at most ONCE per (signal_id, event_type, source) — a best-effort read-before-
    insert (no schema change / unique index, so it's safe on the existing table). Returns True if a
    new row was written, False if a matching row already existed or on any error (FAIL-OPEN).

    Use for per-signal transition events (entry_condition_detected / paper_entry_alert_sent / …) so a
    repeated tracker tick can't create duplicate rows. Concurrency: a rare race can still write two
    rows; the `latency-telemetry-clean` helper reconciles those after the fact."""
    try:
        conn = sqlite3.connect(_db_path(db), timeout=_WRITE_TIMEOUT_SECONDS)
        try:
            conn.execute("PRAGMA busy_timeout=250")
            _ensure(conn)
            existing = conn.execute(
                "SELECT 1 FROM execution_latency_events WHERE event_type=? AND "
                "COALESCE(signal_id,'')=? AND COALESCE(source,'')=? LIMIT 1",
                (str(event_type), signal_id or "", source or "")).fetchone()
            if existing:
                return False
        finally:
            conn.close()
    except Exception:
        # if the pre-check fails, fall through to a plain emit (never lose a real event silently)
        pass
    return emit(db, event_type=event_type, signal_id=signal_id, source=source, **kwargs)


def clean_duplicate_transition_events(db: Any = None, *, apply: bool = False) -> dict:
    """Remove duplicate TRANSITION telemetry rows — same (signal_id, event_type, source), keeping the
    EARLIEST (min id). Only touches `execution_latency_events`; never signals/outcomes/alerts.
    Dry-run by default (apply=False → report only). Read-only for every other table."""
    result = {"table": "execution_latency_events", "apply": apply, "duplicate_groups": 0,
              "rows_to_delete": 0, "by_event_type": {}, "deleted": 0}
    try:
        conn = sqlite3.connect(_db_path(db), timeout=30.0)
        conn.row_factory = sqlite3.Row
        try:
            conn.execute("PRAGMA busy_timeout=30000")
            _ensure(conn)
            placeholders = ",".join("?" for _ in TRANSITION_EVENTS)
            rows = conn.execute(
                f"SELECT id, event_type, COALESCE(signal_id,'') AS sid, COALESCE(source,'') AS src "
                f"FROM execution_latency_events WHERE event_type IN ({placeholders}) "
                f"ORDER BY id", tuple(sorted(TRANSITION_EVENTS))).fetchall()
            group_counts: dict[tuple, int] = {}
            dup_ids: list[int] = []
            by_type: dict[str, int] = {}
            for r in rows:
                if not r["sid"]:
                    continue  # never dedup rows with no signal_id (can't be sure they're the same event)
                key = (r["sid"], r["event_type"], r["src"])
                group_counts[key] = group_counts.get(key, 0) + 1
                if group_counts[key] > 1:      # every occurrence after the earliest (min id) is a dup
                    dup_ids.append(r["id"])
                    by_type[r["event_type"]] = by_type.get(r["event_type"], 0) + 1
            result["duplicate_groups"] = sum(1 for v in group_counts.values() if v > 1)
            result["rows_to_delete"] = len(dup_ids)
            result["by_event_type"] = by_type
            if apply and dup_ids:
                conn.executemany("DELETE FROM execution_latency_events WHERE id=?",
                                 [(i,) for i in dup_ids])
                conn.commit()
                result["deleted"] = len(dup_ids)
        finally:
            conn.close()
    except Exception as exc:
        result["error"] = str(exc)
    return result


def load_events(db: Any = None, *, recent_days: int | None = None, now: datetime | None = None,
                event_types: tuple[str, ...] | None = None) -> list[dict]:
    """Read events (optionally the last `recent_days`). Read-only; [] if the table doesn't exist."""
    try:
        conn = sqlite3.connect(_db_path(db), timeout=30.0)
        conn.row_factory = sqlite3.Row
        try:
            rows = [dict(r) for r in conn.execute(
                "SELECT * FROM execution_latency_events ORDER BY event_at").fetchall()]
        finally:
            conn.close()
    except sqlite3.OperationalError:
        return []
    except Exception:
        return []
    if recent_days is not None:
        from datetime import timedelta
        cutoff = ((now or datetime.now(timezone.utc)) - timedelta(days=int(recent_days))).isoformat()
        rows = [r for r in rows if str(r.get("event_at") or "") >= cutoff]
    if event_types:
        rows = [r for r in rows if r.get("event_type") in event_types]
    return rows
