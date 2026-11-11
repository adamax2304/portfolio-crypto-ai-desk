"""Transport telemetry and alert state for the news ingest layer.

This module is deliberately operational only.  It records whether an RSS/API/
Telegram source was reachable and whether a collector run succeeded; it never
changes signals, scores, paper outcomes, or routing.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
import uuid
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.config import load_config


def _root() -> Path:
    return Path(__file__).resolve().parents[2]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def source_key(source_name: str, source_type: str) -> str:
    """Return one stable key shared by config, telemetry and health reports."""
    name = str(source_name or "").strip()
    stype = str(source_type or "rss").strip().lower()
    if stype == "telegram_collector":
        return "telegram:collector"
    if stype == "telegram":
        handle = name.removeprefix("t.me/").lstrip("@").lower()
        return f"telegram:t.me/{handle}"
    if stype in {"api", "edgar", "provider"}:
        return f"api:{name}"
    return f"rss:{name}"


def _connect(db: str | Path | None = None) -> sqlite3.Connection:
    path = Path(db) if db else Path(load_config().db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path), timeout=30.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA busy_timeout=30000")
    return conn


def ensure_tables(conn: sqlite3.Connection) -> None:
    """Create additive telemetry tables.  Existing data is never dropped."""
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS news_source_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id TEXT NOT NULL,
            source_key TEXT NOT NULL,
            source_name TEXT,
            source_type TEXT NOT NULL,
            asset_class TEXT,
            started_at TEXT NOT NULL,
            finished_at TEXT NOT NULL,
            status TEXT NOT NULL,
            item_count INTEGER NOT NULL DEFAULT 0,
            error_code TEXT,
            error_message TEXT,
            metadata_json TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_news_source_runs_key_finished
            ON news_source_runs(source_key, finished_at);
        CREATE INDEX IF NOT EXISTS idx_news_source_runs_status
            ON news_source_runs(status, finished_at);

        CREATE TABLE IF NOT EXISTS news_source_alert_state (
            source_key TEXT PRIMARY KEY,
            last_status TEXT,
            last_alert_at TEXT,
            last_error_hash TEXT,
            updated_at TEXT NOT NULL
        );
        """
    )


def append_error_event(
    *,
    source_key_value: str,
    status: str,
    message: str,
    source_type: str | None = None,
    run_id: str | None = None,
    metadata: dict[str, Any] | None = None,
    root: Path | None = None,
) -> Path:
    """Append one structured error to the durable JSONL journal."""
    base = root or _root()
    path = base / "data" / "diagnostics" / "news_source_errors.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": now_iso(),
        "source_key": source_key_value,
        "source_type": source_type,
        "status": status,
        "message": str(message)[:1000],
        "run_id": run_id,
        "metadata": metadata or {},
    }
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    return path


def record_source_run(
    *,
    source_name: str,
    source_type: str,
    status: str,
    started_at: str | None = None,
    finished_at: str | None = None,
    item_count: int = 0,
    asset_class: str | None = None,
    error_code: str | None = None,
    error_message: str | None = None,
    metadata: dict[str, Any] | None = None,
    run_id: str | None = None,
    db: str | Path | None = None,
    write_journal: bool = True,
) -> str:
    """Persist a source run and journal failures without raising into ingest."""
    rid = run_id or uuid.uuid4().hex
    started = started_at or now_iso()
    finished = finished_at or now_iso()
    key = source_key(source_name, source_type)
    try:
        with closing(_connect(db)) as conn:
            with conn:
                ensure_tables(conn)
                conn.execute(
                    """
                    INSERT INTO news_source_runs(
                        run_id, source_key, source_name, source_type, asset_class,
                        started_at, finished_at, status, item_count, error_code,
                        error_message, metadata_json
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (rid, key, source_name, source_type, asset_class, started, finished,
                     status, int(item_count or 0), error_code,
                     str(error_message)[:1000] if error_message else None,
                     json.dumps(metadata or {}, ensure_ascii=False, sort_keys=True)),
                )
    except Exception:
        # Observability must never take down a collector.  The caller still gets
        # its normal fetch result even if the DB is temporarily unavailable.
        pass
    if write_journal and status not in {"ok", "ok_empty", "heartbeat", "skipped", "disabled"}:
        try:
            append_error_event(
                source_key_value=key, status=status,
                message=error_message or status, source_type=source_type,
                run_id=rid, metadata=metadata,
            )
        except Exception:
            pass
    return rid


def latest_runs(db: str | Path | None = None) -> dict[str, dict[str, Any]]:
    """Return the newest telemetry row per source, or an empty map on old DBs."""
    try:
        with closing(_connect(db)) as conn:
            rows = conn.execute(
                """
                SELECT r.* FROM news_source_runs r
                JOIN (
                    SELECT source_key, MAX(id) AS max_id
                    FROM news_source_runs GROUP BY source_key
                ) x ON x.max_id = r.id
                """
            ).fetchall()
            return {str(r["source_key"]): dict(r) for r in rows}
    except Exception:
        return {}


def error_hash(status: str, message: str) -> str:
    return hashlib.sha256(f"{status}|{message}".encode("utf-8")).hexdigest()[:16]


def alert_state(db: str | Path | None = None) -> dict[str, dict[str, Any]]:
    try:
        with closing(_connect(db)) as conn:
            rows = conn.execute("SELECT * FROM news_source_alert_state").fetchall()
            return {str(r["source_key"]): dict(r) for r in rows}
    except Exception:
        return {}


def save_alert_state(
    source_key_value: str,
    *,
    status: str,
    last_alert_at: str | None = None,
    last_error_hash: str | None = None,
    db: str | Path | None = None,
) -> None:
    try:
        with closing(_connect(db)) as conn:
            with conn:
                ensure_tables(conn)
                conn.execute(
                    """
                    INSERT INTO news_source_alert_state(
                        source_key, last_status, last_alert_at, last_error_hash, updated_at
                    ) VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(source_key) DO UPDATE SET
                        last_status=excluded.last_status,
                        last_alert_at=excluded.last_alert_at,
                        last_error_hash=excluded.last_error_hash,
                        updated_at=excluded.updated_at
                    """,
                    (source_key_value, status, last_alert_at, last_error_hash, now_iso()),
                )
    except Exception:
        pass


def _notifier_for(root: Path):
    try:
        from src.notifiers.telegram import TelegramNotifier
        return TelegramNotifier(root / "config" / "notifications.yaml")
    except Exception:
        return None


def monitor(*, db: str | Path | None = None, root: Path | None = None,
            send_telegram: bool = False, now: datetime | None = None) -> dict[str, Any]:
    """Refresh health, journal state transitions and optionally notify Telegram.

    Alerts are transition-based: one alert on failure, one on recovery, and no
    per-cycle spam.  The scheduler may call this fail-open every cycle.
    """
    from src.news.source_health import compute_source_health

    base = root or _root()
    health = compute_source_health(str(db) if db else None, now=now)
    states = alert_state(db)
    sent: list[str] = []
    journaled: list[str] = []
    notifier = _notifier_for(base) if send_telegram else None
    # STALE means "quiet in the freshness window" and is not automatically a
    # transport failure. Only explicit transport errors and no-row DEAD states
    # notify; this prevents normal quiet Telegram channels from spamming the
    # operator while still catching a disconnected/unresolved channel.
    problematic = {"DEAD", "ERROR"}
    for row in health.get("sources", []):
        if not row.get("enabled"):
            continue
        key = source_key(str(row.get("source") or ""), str(row.get("source_type") or "rss"))
        current = str(row.get("stale_status") or "UNKNOWN")
        old = states.get(key, {}).get("last_status")
        transport_error = row.get("last_fetch_status") in {"error", "timeout", "unauthorized", "disconnected"}
        changed = old != current
        if current in problematic and (changed or transport_error and old not in problematic):
            msg = (f"[NEWS HEALTH] {current}: {row.get('source')}\n"
                   f"type={row.get('source_type')} 24h={row.get('rows_24h')} 72h={row.get('rows_72h')}\n"
                   f"{('; '.join(row.get('warnings') or []))[:650]}")
            try:
                append_error_event(source_key_value=key, status=current, message=msg,
                                   source_type=str(row.get("source_type") or ""), root=base)
                journaled.append(key)
            except Exception:
                pass
            sent_ok = False
            if notifier is not None and getattr(notifier, "enabled", False) and getattr(notifier, "chat_id", ""):
                try:
                    notifier.send(msg, parse_mode="")
                    sent_ok = True
                    sent.append(key)
                except Exception as exc:
                    try:
                        append_error_event(source_key_value="telegram:notifier", status="error",
                                           message=f"news health alert delivery failed: {exc}",
                                           source_type="telegram", root=base)
                    except Exception:
                        pass
            # State is updated even when Telegram is unavailable, preventing a
            # restart loop from spamming the same incident every cycle.
            save_alert_state(key, status=current, last_alert_at=now_iso() if sent_ok else states.get(key, {}).get("last_alert_at"),
                             last_error_hash=error_hash(current, msg), db=db)
        elif (current == "OK" or (
            current == "STALE" and row.get("last_fetch_status") in {"ok", "ok_empty", "heartbeat"}
        )) and old in problematic:
            msg = (f"[NEWS HEALTH] RECOVERED: {row.get('source')} "
                   f"(transport={row.get('last_fetch_status') or 'freshness'}, "
                   f"24h={row.get('rows_24h')}, 72h={row.get('rows_72h')})")
            sent_ok = False
            try:
                append_error_event(source_key_value=key, status="recovered", message=msg,
                                   source_type=str(row.get("source_type") or ""), root=base)
                journaled.append(key)
            except Exception:
                pass
            if notifier is not None and getattr(notifier, "enabled", False) and getattr(notifier, "chat_id", ""):
                try:
                    notifier.send(msg, parse_mode="")
                    sent_ok = True
                    sent.append(key)
                except Exception:
                    pass
            save_alert_state(key, status="OK", last_alert_at=now_iso() if sent_ok else states.get(key, {}).get("last_alert_at"),
                             last_error_hash=None, db=db)
        else:
            save_alert_state(key, status=current,
                             last_alert_at=states.get(key, {}).get("last_alert_at"),
                             last_error_hash=states.get(key, {}).get("last_error_hash"), db=db)
    return {"health": health, "alerts_sent": sent, "transitions_journaled": journaled,
            "journal_path": str(base / "data" / "diagnostics" / "news_source_errors.jsonl")}
