from __future__ import annotations

import json
import sqlite3
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from src.config import load_config
from src.execution.paper_live_exit_path import VERSION as LIVE_EXIT_PARITY_VERSION


REJECTION_DDL = """
CREATE TABLE IF NOT EXISTS live_rejection_counterfactuals (
  decision_id TEXT PRIMARY KEY,
  signal_id TEXT,
  symbol TEXT,
  asset_class TEXT,
  mode TEXT,
  entry_mode TEXT,
  captured_at TEXT,
  rejection_stage TEXT NOT NULL,
  reasons_json TEXT NOT NULL,
  paper_lifecycle_state TEXT,
  paper_execution_r REAL,
  paper_close_reason TEXT,
  refreshed_at TEXT NOT NULL,
  paper_version TEXT,
  paper_execution_validity TEXT,
  paper_comparable INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_live_rejection_counterfactuals_mode
ON live_rejection_counterfactuals(mode,entry_mode,paper_lifecycle_state);
"""


def _db_path(db: str | Path | None) -> Path:
    return Path(db) if db else Path(load_config().db_path)


def _json_dict(value: Any) -> dict[str, Any]:
    try:
        decoded = json.loads(value or "{}")
        return decoded if isinstance(decoded, dict) else {}
    except (TypeError, ValueError, json.JSONDecodeError):
        return {}


def _json_list(value: Any) -> list[str]:
    try:
        decoded = json.loads(value or "[]")
        return [str(item) for item in decoded] if isinstance(decoded, list) else []
    except (TypeError, ValueError, json.JSONDecodeError):
        return []


def refresh_rejection_counterfactuals(
    *, db: str | Path | None = None, days: int = 30,
    now: datetime | None = None,
) -> dict[str, Any]:
    path = _db_path(db)
    moment = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    cutoff = (moment - timedelta(days=max(1, days))).isoformat()
    with sqlite3.connect(path, timeout=30.0) as conn:
        conn.row_factory = sqlite3.Row
        conn.executescript(REJECTION_DDL)
        existing = {
            row[1] for row in conn.execute(
                "PRAGMA table_info(live_rejection_counterfactuals)"
            )
        }
        for column, column_type in (
            ("paper_version", "TEXT"),
            ("paper_execution_validity", "TEXT"),
            ("paper_comparable", "INTEGER NOT NULL DEFAULT 0"),
        ):
            if column not in existing:
                conn.execute(
                    f"ALTER TABLE live_rejection_counterfactuals "
                    f"ADD COLUMN {column} {column_type}"
                )
        rows = conn.execute(
            "SELECT d.*,o.status AS outbox_status,o.result_json,p.lifecycle_state,"
            "p.paper_execution_r,p.close_reason AS paper_close_reason,"
            "p.version AS paper_version,p.execution_validity AS paper_execution_validity "
            "FROM mexc_canary_decisions d "
            "LEFT JOIN mexc_canary_outbox o ON o.decision_id=d.decision_id "
            "LEFT JOIN paper_execution_outcomes p ON p.signal_id=COALESCE("
            "json_extract(d.decision_json,'$.source_signal_id'),"
            "CASE WHEN d.signal_id LIKE 'stock_paper:%' THEN substr(d.signal_id,13) "
            "ELSE d.signal_id END) "
            "WHERE d.captured_at>=? AND (d.eligible=0 OR o.status LIKE 'REJECTED%')",
            (cutoff,),
        ).fetchall()
        for raw in rows:
            row = dict(raw)
            frozen = _json_dict(row.get("decision_json"))
            reasons = _json_list(row.get("rejection_reasons_json"))
            result = _json_dict(row.get("result_json"))
            if result.get("reason"):
                reasons.append(str(result["reason"]))
            stage = "capture" if int(row.get("eligible") or 0) == 0 else "preflight"
            paper_comparable = int(
                str(row.get("paper_version") or "") == LIVE_EXIT_PARITY_VERSION
                and str(row.get("paper_execution_validity") or "valid") == "valid"
                and str(row.get("lifecycle_state") or "") == "CLOSED"
                and row.get("paper_execution_r") is not None
            )
            payload = (
                str(row.get("decision_id")), str(row.get("signal_id") or ""),
                str(row.get("symbol") or ""), str(frozen.get("asset_class") or "crypto"),
                str(row.get("mode") or ""), str(row.get("entry_mode") or ""),
                str(row.get("captured_at") or ""), stage,
                json.dumps(sorted(set(reasons)), sort_keys=True),
                row.get("lifecycle_state"), row.get("paper_execution_r"),
                row.get("paper_close_reason"), moment.isoformat(),
                row.get("paper_version"), row.get("paper_execution_validity"),
                paper_comparable,
            )
            conn.execute(
                "INSERT INTO live_rejection_counterfactuals("
                "decision_id,signal_id,symbol,asset_class,mode,entry_mode,captured_at,"
                "rejection_stage,reasons_json,paper_lifecycle_state,paper_execution_r,"
                "paper_close_reason,refreshed_at,paper_version,paper_execution_validity,"
                "paper_comparable) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) "
                "ON CONFLICT(decision_id) DO UPDATE SET "
                "rejection_stage=excluded.rejection_stage,reasons_json=excluded.reasons_json,"
                "paper_lifecycle_state=excluded.paper_lifecycle_state,"
                "paper_execution_r=excluded.paper_execution_r,"
                "paper_close_reason=excluded.paper_close_reason,refreshed_at=excluded.refreshed_at,"
                "paper_version=excluded.paper_version,"
                "paper_execution_validity=excluded.paper_execution_validity,"
                "paper_comparable=excluded.paper_comparable",
                payload,
            )
        conn.commit()
        summary_rows = conn.execute(
            "SELECT mode,entry_mode,rejection_stage,COUNT(*) n,"
            "SUM(CASE WHEN paper_comparable=1 THEN 1 ELSE 0 END) closed_n,"
            "SUM(CASE WHEN paper_comparable=1 AND paper_execution_r>0 THEN 1 ELSE 0 END) winners,"
            "SUM(CASE WHEN paper_comparable=1 THEN COALESCE(paper_execution_r,0) ELSE 0 END) paper_r "
            "FROM live_rejection_counterfactuals WHERE captured_at>=? "
            "GROUP BY mode,entry_mode,rejection_stage ORDER BY n DESC",
            (cutoff,),
        ).fetchall()
        reason_rows = conn.execute(
            "SELECT reasons_json,paper_lifecycle_state,paper_execution_r,paper_comparable "
            "FROM live_rejection_counterfactuals WHERE captured_at>=?",
            (cutoff,),
        ).fetchall()
    reasons: dict[str, dict[str, Any]] = {}
    for row in reason_rows:
        labels = _json_list(row["reasons_json"]) or ["UNCLASSIFIED_REJECTION"]
        for label in labels:
            item = reasons.setdefault(label, {
                "reason": label, "rejected": 0, "closed": 0, "winners": 0, "paper_r": 0.0,
            })
            comparable = bool(row["paper_comparable"])
            value = row["paper_execution_r"] if comparable else None
            item["rejected"] += 1
            item["closed"] += comparable
            item["winners"] += value is not None and float(value) > 0
            item["paper_r"] += float(value or 0.0)
    ordered_reasons = sorted(reasons.values(), key=lambda item: item["rejected"], reverse=True)
    for item in ordered_reasons:
        item["paper_r"] = round(float(item["paper_r"]), 3)
    return {
        "status": "ok", "refreshed": len(rows),
        "rows": [dict(row) for row in summary_rows], "reasons": ordered_reasons,
    }


def live_fill_parity(
    *, db: str | Path | None = None, days: int = 30,
    now: datetime | None = None,
) -> dict[str, Any]:
    path = _db_path(db)
    moment = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    cutoff = (moment - timedelta(days=max(1, days))).isoformat()
    with sqlite3.connect(f"file:{path}?mode=ro", uri=True, timeout=30.0) as conn:
        conn.row_factory = sqlite3.Row
        paper_columns = {
            row[1] for row in conn.execute("PRAGMA table_info(paper_execution_outcomes)")
        }
        paper_version_expr = "e.version" if "version" in paper_columns else "NULL"
        validity_expr = (
            "e.execution_validity" if "execution_validity" in paper_columns else "NULL"
        )
        rows = conn.execute(
            "SELECT p.*,d.signal_id,d.mode,d.entry_mode,d.decision_json,"
            f"e.paper_execution_r,e.paper_entry_profile,{paper_version_expr} AS paper_version,"
            f"{validity_expr} AS paper_execution_validity "
            "FROM mexc_canary_positions p JOIN mexc_canary_decisions d "
            "ON d.decision_id=p.decision_id "
            "LEFT JOIN paper_execution_outcomes e ON e.signal_id=COALESCE("
            "json_extract(d.decision_json,'$.source_signal_id'),"
            "CASE WHEN d.signal_id LIKE 'stock_paper:%' THEN substr(d.signal_id,13) "
            "ELSE d.signal_id END) "
            "WHERE p.status='CLOSED' AND p.opened_at>=? ORDER BY p.opened_at",
            (cutoff,),
        ).fetchall()
    trades: list[dict[str, Any]] = []
    groups: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for raw in rows:
        row = dict(raw)
        # ``realized_pnl_usdt`` is persisted from the exchange's net realized
        # field. MEXC's ``realised`` already equals close PnL - totalFee +
        # holdFee, and Bybit's ``closedPnl`` is likewise the settled result.
        # fees/funding remain separate audit dimensions; subtracting/adding
        # them here a second time made the parity report disagree with both the
        # venue and the authoritative live-position ledger.
        live_net = float(row.get("realized_pnl_usdt") or 0.0)
        risk = abs(float(row.get("risk_usdt") or 0.0))
        live_r = live_net / risk if risk > 0 else None
        paper_comparable = (
            str(row.get("paper_version") or "") == LIVE_EXIT_PARITY_VERSION
            and str(row.get("paper_execution_validity") or "valid") == "valid"
        )
        paper_r = row.get("paper_execution_r") if paper_comparable else None
        item = {
            "decision_id": row["decision_id"], "signal_id": row.get("signal_id"),
            "symbol": row.get("symbol"), "mode": row.get("mode"),
            "entry_mode": row.get("entry_mode"), "venue": row.get("venue") or "mexc",
            "live_net_usd": round(live_net, 4),
            "live_r": round(live_r, 4) if live_r is not None else None,
            "paper_r": float(paper_r) if paper_r is not None else None,
            "r_delta": round(live_r - float(paper_r), 4)
            if live_r is not None and paper_r is not None else None,
        }
        trades.append(item)
        groups[(str(item["mode"]), str(item["entry_mode"]), str(item["venue"]))].append(item)
    summary = []
    for (mode, entry_mode, venue), members in sorted(groups.items()):
        comparable = [row for row in members if row["r_delta"] is not None]
        summary.append({
            "mode": mode, "entry_mode": entry_mode, "venue": venue,
            "closed": len(members), "live_net_usd": round(sum(row["live_net_usd"] for row in members), 2),
            "comparable": len(comparable),
            "avg_r_delta": round(sum(row["r_delta"] for row in comparable) / len(comparable), 4)
            if comparable else None,
        })
    return {"status": "ok", "days": days, "closed": len(trades), "summary": summary, "trades": trades}


def render_markdown(parity: dict[str, Any], rejected: dict[str, Any]) -> str:
    lines = ["# Live Execution Evidence", "", "## Fill parity", "",
             "| mode | entry | venue | closed | live net USD | comparable | avg live-paper R |",
             "|---|---|---|---:|---:|---:|---:|"]
    for row in parity.get("summary") or []:
        lines.append(
            f"| {row['mode']} | {row['entry_mode']} | {row['venue']} | {row['closed']} | "
            f"{row['live_net_usd']} | {row['comparable']} | {row['avg_r_delta']} |"
        )
    lines.extend(["", "## Rejected counterfactuals", "",
                  f"Only closed `valid` rows produced by `{LIVE_EXIT_PARITY_VERSION}` are counted as comparable.",
                  "", "| mode | entry | stage | rejected | audited closed | winners | paper R |",
                  "|---|---|---|---:|---:|---:|---:|"])
    for row in rejected.get("rows") or []:
        lines.append(
            f"| {row['mode']} | {row['entry_mode']} | {row['rejection_stage']} | {row['n']} | "
            f"{row['closed_n']} | {row['winners']} | {round(float(row['paper_r'] or 0), 3)} |"
        )
    lines.extend(["", "## Rejection reasons", "",
                  "| reason | rejected | audited closed | winners | paper R |",
                  "|---|---:|---:|---:|---:|"])
    for row in (rejected.get("reasons") or [])[:25]:
        lines.append(
            f"| {row['reason']} | {row['rejected']} | {row['closed']} | "
            f"{row['winners']} | {row['paper_r']} |"
        )
    return "\n".join(lines) + "\n"


__all__ = ["live_fill_parity", "refresh_rejection_counterfactuals", "render_markdown"]
