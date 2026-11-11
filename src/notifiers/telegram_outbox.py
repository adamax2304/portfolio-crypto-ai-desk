"""Durable retry queue for paper Telegram alerts.

Delivery-only infrastructure: it never creates signals, changes actionability,
or touches paper/live execution. Failed entry/close messages are persisted and
retried independently of the tracker lifecycle.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
import json
from typing import Any


_DDL = """
CREATE TABLE IF NOT EXISTS telegram_alert_outbox (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  dedupe_key TEXT NOT NULL UNIQUE,
  alert_id TEXT NOT NULL,
  signal_id TEXT NOT NULL,
  alert_type TEXT NOT NULL,
  message_text TEXT NOT NULL,
  parse_mode TEXT,
  status TEXT NOT NULL,
  attempts INTEGER NOT NULL DEFAULT 0,
  next_attempt_at TEXT,
  last_error TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  sent_at TEXT
);
"""


def _now() -> datetime:
    return datetime.now(timezone.utc)


def ensure_table(conn) -> None:
    conn.execute(_DDL)
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_telegram_outbox_due "
        "ON telegram_alert_outbox(status, next_attempt_at)"
    )


def stage_alert(
    store: Any,
    *,
    alert_id: str,
    signal_id: str,
    alert_type: str,
    asset_class: str,
    symbol: str,
    tier: str,
    sent_at: str,
    message: str,
    parse_mode: str = "",
    mode: str | None = None,
    score: float | None = None,
    direction: str | None = None,
    message_hash: str | None = None,
    payload: dict[str, Any] | None = None,
) -> bool:
    """Atomically persist a Paper decision and its Telegram delivery job.

    The queue row exists before any network call.  A worker crash after this
    transaction therefore cannot lose an already accepted Paper entry.
    """
    now = _now().isoformat()
    with store.connect() as conn:
        ensure_table(conn)
        conn.execute("BEGIN IMMEDIATE")
        existing = conn.execute(
            "SELECT 1 FROM signal_alerts WHERE signal_id=? AND alert_type=? LIMIT 1",
            (signal_id, alert_type),
        ).fetchone()
        if existing is not None:
            return False
        conn.execute(
            """
            INSERT INTO signal_alerts(
              alert_id,signal_id,asset_class,mode,symbol,tier,score,direction,
              sent_at,alert_type,telegram_status,message_hash,payload_json
            ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (alert_id, signal_id, asset_class, mode, symbol, tier, score,
             direction, sent_at, alert_type, "queued", message_hash,
             json.dumps(payload or {})),
        )
        conn.execute(
            """
            INSERT INTO telegram_alert_outbox(
              dedupe_key,alert_id,signal_id,alert_type,message_text,parse_mode,
              status,attempts,next_attempt_at,last_error,created_at,updated_at
            ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (f"{alert_id}:telegram", alert_id, signal_id, alert_type, message,
             parse_mode, "pending", 0, now, None, now, now),
        )
    return True


def mark_sent(store: Any, *, alert_id: str) -> None:
    sent_at = _now().isoformat()
    with store.connect() as conn:
        ensure_table(conn)
        conn.execute(
            "UPDATE telegram_alert_outbox SET status='sent',attempts=attempts+1,"
            "sent_at=?,updated_at=?,last_error=NULL WHERE alert_id=? AND status='pending'",
            (sent_at, sent_at, alert_id),
        )
        conn.execute(
            "UPDATE signal_alerts SET telegram_status='sent' WHERE alert_id=?",
            (alert_id,),
        )


def mark_error(store: Any, *, alert_id: str, error: str) -> None:
    now = _now()
    next_at = (now + timedelta(seconds=10)).isoformat()
    with store.connect() as conn:
        ensure_table(conn)
        conn.execute(
            "UPDATE telegram_alert_outbox SET attempts=attempts+1,next_attempt_at=?,"
            "last_error=?,updated_at=? WHERE alert_id=? AND status='pending'",
            (next_at, error, now.isoformat(), alert_id),
        )
        conn.execute(
            "UPDATE signal_alerts SET telegram_status=? WHERE alert_id=?",
            (f"queued:{error}", alert_id),
        )


def enqueue(store: Any, *, alert_id: str, signal_id: str, alert_type: str,
            message: str, parse_mode: str = "", error: str = "") -> bool:
    now = _now().isoformat()
    with store.connect() as conn:
        ensure_table(conn)
        cur = conn.execute(
            """
            INSERT OR IGNORE INTO telegram_alert_outbox(
              dedupe_key,alert_id,signal_id,alert_type,message_text,parse_mode,
              status,attempts,next_attempt_at,last_error,created_at,updated_at
            ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (f"{alert_id}:telegram", alert_id, signal_id, alert_type, message,
             parse_mode, "pending", 0, now, error or None, now, now),
        )
        return cur.rowcount > 0


def retry_pending(store: Any, notifier: Any, *, limit: int = 25,
                  now: datetime | None = None, max_attempts: int = 5) -> dict[str, int]:
    now = now or _now()
    now_iso = now.isoformat()
    with store.connect() as conn:
        ensure_table(conn)
        rows = conn.execute(
            """
            SELECT o.id,o.alert_id,o.message_text,o.parse_mode,o.attempts,
                   o.alert_type,a.payload_json
            FROM telegram_alert_outbox AS o
            LEFT JOIN signal_alerts AS a ON a.alert_id=o.alert_id
            WHERE o.status='pending' AND (o.next_attempt_at IS NULL OR o.next_attempt_at<=?)
            ORDER BY o.created_at ASC LIMIT ?
            """, (now_iso, int(limit)),
        ).fetchall()

    sent = failed = dead = 0
    for row in rows:
        oid, alert_id, message, parse_mode, attempts, alert_type, payload_json = tuple(row)
        if alert_type == "manual_paper_entry":
            try:
                expires_at = json.loads(payload_json or "{}").get("expires_at")
                expires = datetime.fromisoformat(str(expires_at).replace("Z", "+00:00"))
                if expires.tzinfo is None:
                    expires = expires.replace(tzinfo=timezone.utc)
                check_now = now if now.tzinfo else now.replace(tzinfo=timezone.utc)
                expired = expires <= check_now.astimezone(timezone.utc)
            except (TypeError, ValueError, json.JSONDecodeError):
                expired = True
            if expired:
                expired_at = _now().isoformat()
                with store.connect() as conn:
                    ensure_table(conn)
                    changed = conn.execute(
                        "UPDATE telegram_alert_outbox SET status='dead',last_error=?,"
                        "updated_at=? WHERE id=? AND status='pending'",
                        ("manual_signal_expired", expired_at, oid),
                    ).rowcount
                    if changed:
                        conn.execute(
                            "UPDATE signal_alerts SET telegram_status='expired' WHERE alert_id=?",
                            (alert_id,),
                        )
                dead += int(bool(changed))
                continue
        with store.connect() as conn:
            ensure_table(conn)
            claimed = conn.execute(
                "UPDATE telegram_alert_outbox SET status='sending',updated_at=? "
                "WHERE id=? AND status='pending'",
                (_now().isoformat(), oid),
            ).rowcount
        if not claimed:
            continue
        try:
            fast_send_impl = getattr(type(notifier), "send_fast", None)
            if callable(fast_send_impl):
                fast_send_impl(notifier, message, parse_mode=parse_mode or "")
            else:
                notifier.send(message, parse_mode=parse_mode or "")
            sent_at = _now().isoformat()
            with store.connect() as conn:
                ensure_table(conn)
                conn.execute(
                    "UPDATE telegram_alert_outbox SET status='sent',attempts=?,sent_at=?,"
                    "updated_at=?,last_error=NULL WHERE id=? AND status='sending'",
                    (int(attempts or 0) + 1, sent_at, sent_at, oid),
                )
                conn.execute(
                    "UPDATE signal_alerts SET telegram_status='sent' "
                    "WHERE alert_id=? AND telegram_status!='sent'",
                    (alert_id,),
                )
            sent += 1
        except Exception as exc:  # delivery must never affect tracker state
            n = int(attempts or 0) + 1
            is_dead = n >= max_attempts
            delay = min(60, 5 * (2 ** min(n, 4)))
            next_at = (now + timedelta(seconds=delay)).isoformat()
            with store.connect() as conn:
                ensure_table(conn)
                conn.execute(
                    "UPDATE telegram_alert_outbox SET status=?,attempts=?,next_attempt_at=?,"
                    "last_error=?,updated_at=? WHERE id=? AND status='sending'",
                    ("dead" if is_dead else "pending", n, next_at,
                     type(exc).__name__, _now().isoformat(), oid),
                )
            failed += 1
            dead += int(is_dead)
    return {"due": len(rows), "sent": sent, "failed": failed, "dead": dead}


__all__ = [
    "ensure_table", "enqueue", "stage_alert", "mark_sent", "mark_error",
    "retry_pending",
]
