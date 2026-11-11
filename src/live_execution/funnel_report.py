from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from src.config import load_config


def _parse_utc(value: Any) -> datetime | None:
    if value in (None, ""):
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _table_exists(conn: sqlite3.Connection, name: str) -> bool:
    return conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",
        (name,),
    ).fetchone() is not None


def _cols(conn: sqlite3.Connection, table: str) -> set[str]:
    if not _table_exists(conn, table):
        return set()
    return {str(row[1]) for row in conn.execute(f"PRAGMA table_info({table})")}


def _group(conn: sqlite3.Connection, sql: str, params: tuple[Any, ...]) -> list[dict[str, Any]]:
    return [dict(row) for row in conn.execute(sql, params).fetchall()]


def _json_list(value: Any) -> list[str]:
    try:
        parsed = json.loads(str(value or "[]"))
    except json.JSONDecodeError:
        return []
    if not isinstance(parsed, list):
        return []
    return [str(item) for item in parsed]


def build_report(*, db: str | Path | None = None, hours: int = 24,
                 now: datetime | None = None, limit: int = 30) -> dict[str, Any]:
    now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    since = now - timedelta(hours=max(1, int(hours)))
    db_path = Path(db) if db else load_config().db_path
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        result: dict[str, Any] = {
            "generated_at": now.isoformat(),
            "since": since.isoformat(),
            "hours": hours,
            "proposed": [],
            "alerts": [],
            "close_alerts": [],
            "mexc_decisions": [],
            "mexc_rejection_reasons": [],
            "mexc_outbox": [],
            "mexc_orders": [],
            "recent_rejections": [],
        }

        proposed_cols = _cols(conn, "proposed_signals")
        if {"created_at", "asset_class", "mode"} <= proposed_cols:
            result["proposed"] = _group(
                conn,
                "SELECT COALESCE(asset_class,'?') asset_class,COALESCE(mode,'?') mode,COUNT(*) n "
                "FROM proposed_signals WHERE created_at>=? GROUP BY 1,2 ORDER BY n DESC",
                (since.isoformat(),),
            )

        alert_cols = _cols(conn, "signal_alerts")
        if {"sent_at", "asset_class", "mode", "telegram_status"} <= alert_cols:
            alert_type_filter = " AND alert_type='paper_entry'" if "alert_type" in alert_cols else ""
            result["alerts"] = _group(
                conn,
                "SELECT COALESCE(asset_class,'?') asset_class,COALESCE(mode,'?') mode,"
                "COALESCE(telegram_status,'?') telegram_status,COUNT(*) n "
                "FROM signal_alerts WHERE sent_at>=?" + alert_type_filter
                + " GROUP BY 1,2,3 ORDER BY n DESC",
                (since.isoformat(),),
            )
            if "alert_type" in alert_cols:
                result["close_alerts"] = _group(
                    conn,
                    "SELECT COALESCE(asset_class,'?') asset_class,COALESCE(mode,'?') mode,"
                    "alert_type,COALESCE(telegram_status,'?') telegram_status,COUNT(*) n "
                    "FROM signal_alerts WHERE sent_at>=? AND alert_type LIKE 'close_%' "
                    "GROUP BY 1,2,3,4 ORDER BY n DESC",
                    (since.isoformat(),),
                )

        decision_cols = _cols(conn, "mexc_canary_decisions")
        if {"captured_at", "mode", "entry_mode", "eligible", "state", "rejection_reasons_json"} <= decision_cols:
            result["mexc_decisions"] = _group(
                conn,
                "SELECT COALESCE(mode,'?') mode,COALESCE(entry_mode,'?') entry_mode,"
                "eligible,state,COUNT(*) n FROM mexc_canary_decisions WHERE captured_at>=? "
                "GROUP BY 1,2,3,4 ORDER BY n DESC",
                (since.isoformat(),),
            )
            reason_counts: dict[str, int] = {}
            for row in conn.execute(
                "SELECT rejection_reasons_json FROM mexc_canary_decisions WHERE captured_at>=?",
                (since.isoformat(),),
            ):
                for reason in _json_list(row[0]):
                    reason_counts[reason] = reason_counts.get(reason, 0) + 1
            result["mexc_rejection_reasons"] = [
                {"reason": reason, "n": n}
                for reason, n in sorted(reason_counts.items(), key=lambda item: (-item[1], item[0]))
            ]
            result["recent_rejections"] = [
                dict(row) for row in conn.execute(
                    "SELECT signal_id,symbol,mode,entry_mode,state,rejection_reasons_json,captured_at "
                    "FROM mexc_canary_decisions WHERE captured_at>=? AND eligible=0 "
                    "ORDER BY captured_at DESC LIMIT ?",
                    (since.isoformat(), int(limit)),
                ).fetchall()
            ]

        outbox_cols = _cols(conn, "mexc_canary_outbox")
        if {"created_at", "status"} <= outbox_cols:
            result["mexc_outbox"] = _group(
                conn,
                "SELECT status,COUNT(*) n FROM mexc_canary_outbox WHERE created_at>=? "
                "GROUP BY 1 ORDER BY n DESC",
                (since.isoformat(),),
            )

        order_cols = _cols(conn, "mexc_canary_orders")
        if {"updated_at", "status"} <= order_cols:
            result["mexc_orders"] = _group(
                conn,
                "SELECT status,COUNT(*) n FROM mexc_canary_orders WHERE updated_at>=? "
                "GROUP BY 1 ORDER BY n DESC",
                (since.isoformat(),),
            )
        return result
    finally:
        conn.close()


def _render_group(rows: list[dict[str, Any]], columns: list[str]) -> list[str]:
    if not rows:
        return ["_No rows._"]
    lines = ["| " + " | ".join(columns) + " |",
             "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(col, "")) for col in columns) + " |")
    return lines


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Live Funnel Report",
        "",
        f"- Generated: `{report['generated_at']}`",
        f"- Window: `{report['since']}` -> `{report['generated_at']}`",
        "",
        "## Proposed Signals",
        "",
        *_render_group(report["proposed"], ["asset_class", "mode", "n"]),
        "",
        "## Paper Entry Alerts",
        "",
        *_render_group(report["alerts"], ["asset_class", "mode", "telegram_status", "n"]),
        "",
        "## Close Alerts",
        "",
        *_render_group(report["close_alerts"],
                       ["asset_class", "mode", "alert_type", "telegram_status", "n"]),
        "",
        "## MEXC Decisions",
        "",
        *_render_group(report["mexc_decisions"], ["mode", "entry_mode", "eligible", "state", "n"]),
        "",
        "## MEXC Rejection Reasons",
        "",
        *_render_group(report["mexc_rejection_reasons"], ["reason", "n"]),
        "",
        "## MEXC Outbox",
        "",
        *_render_group(report["mexc_outbox"], ["status", "n"]),
        "",
        "## MEXC Orders",
        "",
        *_render_group(report["mexc_orders"], ["status", "n"]),
        "",
        "## Recent Rejections",
        "",
    ]
    if report["recent_rejections"]:
        lines.extend(_render_group(
            report["recent_rejections"],
            ["captured_at", "signal_id", "symbol", "mode", "entry_mode", "state", "rejection_reasons_json"],
        ))
    else:
        lines.append("_No rejected MEXC decisions in the window._")
    return "\n".join(lines) + "\n"


def write_report(*, db: str | Path | None = None, hours: int = 24,
                 out: str | Path | None = None,
                 now: datetime | None = None) -> Path:
    report = build_report(db=db, hours=hours, now=now)
    target = Path(out) if out else load_config().root / "reports" / "LIVE_FUNNEL_LATEST.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_markdown(report), encoding="utf-8")
    return target
