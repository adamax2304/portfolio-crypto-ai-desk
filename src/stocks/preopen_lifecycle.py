"""Narrow lifecycle repair for pre-open stock plans.

Only repairs the historical expiry bug where an after-hours plan was assigned
the already-finished cash-session close. It never changes score, tier,
geometry, outcomes, Paper accounting, or live routing.
"""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.config import load_config
from src.stocks.paper_funnel import record_event

VERSION = "stocks_preopen_lifecycle_repair_v1"
_RECOVERABLE = {
    "expired", "missed_no_entry", "stale_before_entry", "entry_moved_away",
}


def _utc(value: datetime | None = None) -> datetime:
    moment = value or datetime.now(timezone.utc)
    return (
        moment.replace(tzinfo=timezone.utc)
        if moment.tzinfo is None
        else moment.astimezone(timezone.utc)
    )


def _parse(value: Any) -> datetime | None:
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None
    return (
        parsed.replace(tzinfo=timezone.utc)
        if parsed.tzinfo is None
        else parsed.astimezone(timezone.utc)
    )


def _table_exists(conn: sqlite3.Connection, table: str) -> bool:
    return conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",
        (table,),
    ).fetchone() is not None


def repair_bug_expired_actionable_plans(
    db: str | Path | None = None,
    *,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Reactivate only provably premature no-entry terminal plans."""
    moment = _utc(now)
    path = Path(db or load_config().db_path)
    repaired: list[str] = []
    skipped: dict[str, str] = {}
    with sqlite3.connect(path, timeout=30.0) as conn:
        conn.row_factory = sqlite3.Row
        if not (
            _table_exists(conn, "stocks_preus_actionability")
            and _table_exists(conn, "stocks_paper_decision_snapshots")
            and _table_exists(conn, "proposed_signals")
        ):
            return {"status": "tables_missing", "repaired": 0, "signal_ids": []}

        signal_columns = {
            str(row[1]) for row in conn.execute("PRAGMA table_info(proposed_signals)")
        }
        updated_assignment = ",updated_at=?" if "updated_at" in signal_columns else ""
        rows = conn.execute(
            "SELECT p.signal_id,p.created_at,p.status,a.valid_until,"
            "a.target_session_close_at,s.funnel_state,s.pre_gate_tier "
            "FROM proposed_signals p "
            "JOIN stocks_preus_actionability a ON a.signal_id=p.signal_id "
            "JOIN stocks_paper_decision_snapshots s ON s.signal_id=p.signal_id "
            "WHERE p.asset_class='stocks' AND p.mode='intraday' "
            "AND a.decision='ACTIONABLE' AND a.valid_until>=? "
            "AND a.reactivated=0 "
            "AND s.funnel_state='PREOPEN_PLAN'",
            (moment.isoformat(),),
        ).fetchall()
        for raw in rows:
            row = dict(raw)
            signal_id = str(row["signal_id"])
            if str(row.get("pre_gate_tier") or "").upper() not in {"A", "B"}:
                skipped[signal_id] = "pre_gate_not_ab"
                continue
            if str(row.get("status") or "") not in _RECOVERABLE:
                skipped[signal_id] = "status_not_recoverable"
                continue
            created = _parse(row.get("created_at"))
            target_close = _parse(row.get("target_session_close_at"))
            if created is None or target_close is None or moment > target_close:
                skipped[signal_id] = "target_session_closed_or_unknown"
                continue

            bad_expiry = None
            if _table_exists(conn, "paper_execution_outcomes"):
                bad_expiry = conn.execute(
                    "SELECT effective_expires_at FROM paper_execution_outcomes "
                    "WHERE signal_id=?",
                    (signal_id,),
                ).fetchone()
            effective = _parse(bad_expiry[0]) if bad_expiry else None
            if effective is None or effective >= created:
                skipped[signal_id] = "no_impossible_expiry_proof"
                continue

            if _table_exists(conn, "signal_alerts") and conn.execute(
                "SELECT 1 FROM signal_alerts WHERE signal_id=? "
                "AND alert_type='paper_entry' LIMIT 1",
                (signal_id,),
            ).fetchone():
                skipped[signal_id] = "paper_entry_already_alerted"
                continue
            if _table_exists(conn, "paper_portfolio_ledger") and conn.execute(
                "SELECT 1 FROM paper_portfolio_ledger WHERE signal_id=? "
                "AND event_type='entry' LIMIT 1",
                (signal_id,),
            ).fetchone():
                skipped[signal_id] = "paper_entry_already_in_ledger"
                continue

            params: list[Any] = ["waiting_for_entry"]
            if updated_assignment:
                params.append(moment.isoformat())
            params.append(signal_id)
            conn.execute(
                f"UPDATE proposed_signals SET status=?{updated_assignment} "
                "WHERE signal_id=?",
                tuple(params),
            )
            conn.execute(
                "UPDATE stocks_preus_actionability SET reactivated=1 WHERE signal_id=?",
                (signal_id,),
            )
            record_event(
                conn,
                signal_id=signal_id,
                stage="PREOPEN_PLAN_REACTIVATED",
                reason="repaired_impossible_previous_session_expiry",
                payload={
                    "old_status": row.get("status"),
                    "bad_effective_expires_at": effective.isoformat(),
                    "target_session_close_at": target_close.isoformat(),
                    "repair_version": VERSION,
                },
                now=moment,
            )
            repaired.append(signal_id)
        conn.commit()
    return {
        "status": "ok",
        "repaired": len(repaired),
        "signal_ids": repaired,
        "skipped": skipped,
        "version": VERSION,
    }


__all__ = ["VERSION", "repair_bug_expired_actionable_plans"]
