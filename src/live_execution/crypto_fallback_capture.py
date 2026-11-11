from __future__ import annotations

import hashlib
import json
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.config import load_config
from src.storage.sqlite import SQLiteStore

from . import store as ls
from .config import LiveCanaryConfig, load_live_canary_config
from .routing_registry import route
from .service import capture_paper_candidate


def _parse(value: Any) -> datetime | None:
    if value in (None, ""):
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _loads(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return dict(value)
    try:
        parsed = json.loads(value or "{}")
        return parsed if isinstance(parsed, dict) else {}
    except (TypeError, ValueError, json.JSONDecodeError):
        return {}


def _stable_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)


def _hash(value: Any) -> str:
    return hashlib.sha256(_stable_json(value).encode("utf-8")).hexdigest()


def _table_exists(conn: sqlite3.Connection, name: str) -> bool:
    return bool(conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (name,)
    ).fetchone())


def _has_live_decision(conn: sqlite3.Connection, signal_id: str) -> bool:
    if not _table_exists(conn, "mexc_canary_decisions"):
        return False
    return bool(conn.execute(
        "SELECT 1 FROM mexc_canary_decisions "
        "WHERE signal_id=? OR json_extract(decision_json,'$.source_signal_id')=? "
        "LIMIT 1",
        (signal_id, signal_id),
    ).fetchone())


def _latest_paper_alert_payload(conn: sqlite3.Connection, signal_id: str) -> tuple[str | None, dict[str, Any]]:
    if not _table_exists(conn, "signal_alerts"):
        return None, {}
    row = conn.execute(
        "SELECT alert_id,payload_json FROM signal_alerts "
        "WHERE signal_id=? AND alert_type='paper_entry' "
        "ORDER BY sent_at DESC,rowid DESC LIMIT 1",
        (signal_id,),
    ).fetchone()
    if not row:
        return None, {}
    return str(row["alert_id"]), _loads(row["payload_json"])


def _diagnostic_rejection(
    conn: sqlite3.Connection,
    *,
    row: dict[str, Any],
    reason: str,
    live: LiveCanaryConfig,
    now: datetime,
) -> bool:
    signal_id = str(row.get("signal_id") or "")
    if not signal_id:
        return False
    diagnostic_signal_id = f"crypto_fallback_rejected:{signal_id}:{reason.lower()}"
    decision_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"mexc-live-crypto-fallback:{diagnostic_signal_id}"))
    symbol = str(row.get("symbol") or "")
    entry_mode = str(row.get("paper_execution_entry_mode") or row.get("entry_type") or "").upper()
    frozen = {
        "signal_id": diagnostic_signal_id,
        "source_signal_id": signal_id,
        "decision_context_type": "crypto_live_fallback_diagnostic",
        "captured_at": now.isoformat(),
        "signal_created_at": row.get("created_at"),
        "entry_triggered_at": row.get("entry_at") or row.get("decision_at"),
        "symbol": symbol,
        "asset_class": "crypto",
        "mode": str(row.get("mode") or ""),
        "direction": str(row.get("direction") or ""),
        "tier": str(row.get("tier") or ""),
        "score": row.get("score"),
        "entry_mode": entry_mode,
        "entry_price": row.get("entry_price_used"),
        "original_stop": row.get("stop_initial"),
        "strategy_version": row.get("paper_entry_profile"),
        "rejection_reasons": [reason],
    }
    record = {
        "decision_id": decision_id,
        "signal_id": diagnostic_signal_id,
        "captured_at": now.isoformat(),
        "paper_alert_id": None,
        "symbol": symbol,
        "mode": frozen["mode"],
        "entry_mode": entry_mode,
        "eligible": 0,
        "state": "REJECTED_DIAGNOSTIC",
        "rejection_reasons_json": json.dumps([reason]),
        "decision_json": _stable_json(frozen),
        "decision_hash": _hash(frozen),
        "config_hash": live.config_hash,
        "decision_context_type": frozen["decision_context_type"],
    }
    return bool(ls.insert_decision(conn, record, queue=False).get("inserted"))


def _candidate_rows(conn: sqlite3.Connection, *, since: datetime, limit: int) -> list[dict[str, Any]]:
    required = {"paper_execution_outcomes", "proposed_signals"}
    if not all(_table_exists(conn, table) for table in required):
        return []
    rows = conn.execute(
        """
        WITH latest_execution AS (
          SELECT o.*, ROW_NUMBER() OVER (
            PARTITION BY o.signal_id ORDER BY o.computed_at DESC,rowid DESC
          ) AS rn
          FROM paper_execution_outcomes o
        )
        SELECT
          p.signal_id,p.created_at,p.symbol,p.direction,p.mode,p.tier,p.score,
          p.asset_class,p.entry_type,p.raw_idea_json,
          e.entry_at,e.decision_at,e.entry_price_used,e.stop_initial,
          e.entry_time_basis,e.current_price_revalidated,e.execution_validity,
          e.lifecycle_state,e.close_reason,e.paper_entry_profile,
          e.paper_execution_entry_mode
        FROM latest_execution e
        JOIN proposed_signals p ON p.signal_id=e.signal_id
        WHERE e.rn=1
          AND lower(COALESCE(p.asset_class,''))='crypto'
          AND lower(COALESCE(p.mode,''))='swing'
          AND COALESCE(e.lifecycle_state,'')='OPEN'
          AND COALESCE(e.execution_validity,'')='valid'
          AND COALESCE(e.current_price_revalidated,0)=1
          AND COALESCE(e.entry_time_basis,'')='point_in_time_current_bar'
          AND COALESCE(e.entry_at,e.decision_at,p.created_at)>=?
        ORDER BY COALESCE(e.entry_at,e.decision_at,p.created_at) DESC
        LIMIT ?
        """,
        (since.isoformat(), int(limit)),
    ).fetchall()
    return [dict(row) for row in rows]


def capture_recent_missing(
    *,
    db: str | Path | None = None,
    max_age_seconds: int = 300,
    limit: int = 50,
    live_cfg: LiveCanaryConfig | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Safety-net capture for fresh crypto Paper entries missed by Telegram.

    The notifier remains the primary live handoff path. This fallback only
    handles fresh point-in-time Paper rows that are still inside the live entry
    window and have no live decision. It never turns historical backfills into
    live trades.
    """
    live = live_cfg or load_live_canary_config()
    now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    path = Path(db) if db else load_config().db_path
    store = SQLiteStore(path)
    since = datetime.fromtimestamp(now.timestamp() - max_age_seconds, tz=timezone.utc)
    counts: dict[str, Any] = {
        "seen": 0,
        "captured": 0,
        "queued": 0,
        "rejected": 0,
        "duplicate": 0,
        "missing_alert": 0,
        "not_live_route": 0,
        "reasons": {},
    }

    with ls.connect(path) as conn:
        ls.ensure_tables(conn)
        rows = _candidate_rows(conn, since=since, limit=limit)
        for row in rows:
            counts["seen"] += 1
            signal_id = str(row.get("signal_id") or "")
            entry_mode = str(row.get("paper_execution_entry_mode") or row.get("entry_type") or "").upper()
            routed = route(mode=str(row.get("mode") or ""), entry_mode=entry_mode, asset_class="crypto")
            if not routed or routed.get("enabled") is not True:
                counts["not_live_route"] += 1
                continue
            if _has_live_decision(conn, signal_id):
                counts["duplicate"] += 1
                continue
            alert_id, payload = _latest_paper_alert_payload(conn, signal_id)
            if not payload:
                counts["missing_alert"] += 1
                if _diagnostic_rejection(
                    conn, row=row, reason="PAPER_ENTRY_ALERT_MISSING", live=live, now=now,
                ):
                    counts["rejected"] += 1
                    counts["reasons"]["PAPER_ENTRY_ALERT_MISSING"] = (
                        counts["reasons"].get("PAPER_ENTRY_ALERT_MISSING", 0) + 1
                    )
                continue

            signal = {
                "signal_id": signal_id,
                "created_at": row.get("created_at"),
                "symbol": row.get("symbol"),
                "direction": row.get("direction"),
                "mode": row.get("mode"),
                "tier": row.get("tier"),
                "score": row.get("score"),
                "asset_class": "crypto",
                "raw_idea_json": row.get("raw_idea_json") or "{}",
            }
            result = capture_paper_candidate(
                store=store,
                signal=signal,
                payload=payload,
                paper_alert_id=alert_id,
                cfg=live,
                now=now,
            )
            counts["captured"] += 1
            if result.get("queued"):
                counts["queued"] += 1
            elif result.get("status") == "DUPLICATE":
                counts["duplicate"] += 1
            else:
                counts["rejected"] += 1
                for reason in result.get("reasons") or ["UNKNOWN_REJECTION"]:
                    reason = str(reason)
                    counts["reasons"][reason] = counts["reasons"].get(reason, 0) + 1
    counts["status"] = "OK"
    return counts
