"""Conservative targeted recovery for genuinely unhealthy Telegram sources.

The live listener remains the primary path.  This helper only selects a channel
for a bounded catch-up when source-health reports an explicit transport error or
no publications at all in the 72h window.  A normally quiet channel is never
treated as failed merely because it has no new post in 24h.
"""
from __future__ import annotations

import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from src.config import load_config


COOLDOWN_HOURS = 6.0


def ensure_tables(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS telegram_recovery_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            attempted_at TEXT NOT NULL,
            status TEXT NOT NULL,
            detail TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_telegram_recovery_source_attempt
            ON telegram_recovery_attempts(source, attempted_at);
        """
    )


def _db_path(db: str | Path | None) -> Path:
    return Path(db) if db else Path(load_config().db_path)


def _recent_attempts(db: str | Path | None, *, now: datetime) -> dict[str, datetime]:
    path = _db_path(db)
    try:
        with sqlite3.connect(str(path)) as conn:
            ensure_tables(conn)
            rows = conn.execute(
                "SELECT source, MAX(attempted_at) AS attempted_at FROM telegram_recovery_attempts GROUP BY source"
            ).fetchall()
    except sqlite3.Error:
        return {}
    out: dict[str, datetime] = {}
    for source, value in rows:
        try:
            stamp = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
            out[str(source).lower()] = (stamp if stamp.tzinfo else stamp.replace(tzinfo=timezone.utc))
        except (TypeError, ValueError):
            continue
    return out


def latest_attempts(db: str | Path | None = None) -> dict[str, dict[str, str]]:
    """Latest targeted recovery result per channel, read-only for source-health diagnostics."""
    path = _db_path(db)
    try:
        with sqlite3.connect(str(path)) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                """
                SELECT a.source, a.attempted_at, a.status, a.detail
                FROM telegram_recovery_attempts a
                JOIN (
                    SELECT source, MAX(id) AS max_id
                    FROM telegram_recovery_attempts GROUP BY source
                ) latest ON latest.max_id = a.id
                """
            ).fetchall()
    except sqlite3.Error:
        return {}
    return {str(row["source"]).lower(): dict(row) for row in rows}


def select_recovery_targets(health: dict[str, Any], *, db: str | Path | None = None,
                            now: datetime | None = None, max_targets: int = 6,
                            cooldown_hours: float = COOLDOWN_HOURS) -> list[dict[str, Any]]:
    """Select only Telegram channels that warrant an actual recovery attempt."""
    now = now or datetime.now(timezone.utc)
    attempts = _recent_attempts(db, now=now)
    cutoff = now - timedelta(hours=float(cooldown_hours))
    candidates: list[dict[str, Any]] = []
    for row in health.get("sources") or []:
        if not row.get("enabled") or row.get("source_type") != "telegram":
            continue
        status = str(row.get("stale_status") or "").upper()
        transport = str(row.get("last_fetch_status") or "").lower()
        no_rows = int(row.get("rows_72h") or 0) == 0
        warrants_recovery = status in {"ERROR", "DEAD"} or (status == "STALE" and no_rows) or transport in {
            "error", "timeout", "unauthorized", "disconnected",
        }
        # STALE with some recent publication usually means a quiet editorial
        # channel, not a broken one.  Do not churn its Telethon history.
        if not warrants_recovery or (status == "STALE" and not no_rows):
            continue
        source = str(row.get("source") or "")
        handle = source.removeprefix("t.me/").lstrip("@")
        if not handle or (attempts.get(source.lower()) and attempts[source.lower()] >= cutoff):
            continue
        candidates.append({
            "source": source, "handle": handle, "status": status,
            "transport": transport or None, "rows_72h": int(row.get("rows_72h") or 0),
            "primary_source": bool(row.get("primary_source")),
        })
    rank = {"ERROR": 0, "DEAD": 1, "STALE": 2}
    candidates.sort(key=lambda item: (
        0 if item["primary_source"] else 1, rank.get(item["status"], 2), item["rows_72h"], item["source"].lower(),
    ))
    return candidates[: int(max_targets)]


def record_attempts(attempts: list[dict[str, Any]], *, db: str | Path | None = None,
                    now: datetime | None = None) -> None:
    """Persist recovery observability only; news rows are written by the collector."""
    if not attempts:
        return
    stamp = (now or datetime.now(timezone.utc)).replace(microsecond=0).isoformat()
    try:
        with sqlite3.connect(str(_db_path(db))) as conn:
            ensure_tables(conn)
            conn.executemany(
                "INSERT INTO telegram_recovery_attempts(source, attempted_at, status, detail) VALUES (?, ?, ?, ?)",
                [(str(item.get("source") or ""), stamp, str(item.get("status") or "unknown"),
                  str(item.get("detail") or "")[:500]) for item in attempts],
            )
    except sqlite3.Error:
        pass


__all__ = ["COOLDOWN_HOURS", "ensure_tables", "latest_attempts", "select_recovery_targets", "record_attempts"]
