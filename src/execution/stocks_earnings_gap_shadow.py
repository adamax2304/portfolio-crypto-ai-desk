"""Isolated earnings-gap continuation Shadow lane.

It reuses the deterministic Catalyst RS evaluator with an earnings-only event
scope, then persists results in a separate table. It never registers signals.
"""
from __future__ import annotations

import json
import sqlite3
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import yaml

from src.config import load_config
from src.execution import stocks_catalyst_rs_shadow as base
from src.execution.shadow_strategy_common import ensure_columns


ROOT = Path(__file__).resolve().parents[2]
CFG_PATH = ROOT / "config" / "shadow" / "stocks" / "earnings_gap_continuation.yaml"
TABLE = "stocks_earnings_gap_shadow_outcomes"
META = "stocks_earnings_gap_shadow_meta"
NY = ZoneInfo("America/New_York")
DDL = f"""
CREATE TABLE IF NOT EXISTS {TABLE} (
  candidate_id TEXT PRIMARY KEY,
  strategy_id TEXT NOT NULL,
  profile_id TEXT NOT NULL,
  shadow_lane TEXT NOT NULL,
  window TEXT NOT NULL,
  generated_at TEXT NOT NULL,
  catalyst_at TEXT,
  symbol TEXT NOT NULL,
  eligibility_status TEXT,
  rejection_reason TEXT,
  is_clean_for_edge INTEGER NOT NULL DEFAULT 0,
  outcome_status TEXT,
  net_pnl_usd REAL,
  fees_usd REAL,
  slippage_usd REAL,
  funding_usd REAL,
  event_session_key TEXT,
  duplicate_of_candidate_id TEXT,
  dedupe_status TEXT NOT NULL DEFAULT 'unique',
  payload_json TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS {META} (k TEXT PRIMARY KEY, v TEXT NOT NULL);
"""
COLS = ("candidate_id", "strategy_id", "profile_id", "shadow_lane", "window", "generated_at",
        "catalyst_at", "symbol", "eligibility_status", "rejection_reason", "is_clean_for_edge",
        "outcome_status", "net_pnl_usd", "fees_usd", "slippage_usd", "funding_usd",
        "event_session_key", "duplicate_of_candidate_id", "dedupe_status", "payload_json")


def load_cfg() -> dict[str, Any]:
    cfg = deepcopy(base.load_strategy_config())
    raw = yaml.safe_load(CFG_PATH.read_text(encoding="utf-8")) or {}
    cfg.update(raw.get("stocks_earnings_gap_continuation") or {})
    return cfg


def _ensure(conn: sqlite3.Connection) -> None:
    conn.executescript(DDL)
    ensure_columns(conn, TABLE, {
        "event_session_key": "TEXT",
        "duplicate_of_candidate_id": "TEXT",
        "dedupe_status": "TEXT NOT NULL DEFAULT 'unique'",
    })


def _event_session_key(row: dict[str, Any]) -> str:
    """One earnings event may surface through several canonical sources.

    Only one executable observation is allowed per symbol and US session.  The
    key deliberately uses the entry session when it exists, otherwise the
    first point-in-time-visible catalyst session, so it cannot be reshaped by a
    later refresh.
    """
    stamp = base.parse_dt(row.get("entry_ts") or row.get("decision_at") or row.get("catalyst_at"))
    session = stamp.astimezone(NY).date().isoformat() if stamp else "unknown"
    return f"{str(row.get('symbol') or '').upper()}|earnings|{session}"


def _deduplicate_entries(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Keep the first deterministic eligible trade for each earnings session.

    Rejected observations remain visible as their original funnel result.  A
    duplicate *eligible* observation becomes an explicit non-executed row, so
    it cannot inflate PnL, trade count, or win rate.
    """
    groups: dict[str, list[dict[str, Any]]] = {}
    for item in rows:
        item["event_session_key"] = _event_session_key(item)
        item["duplicate_of_candidate_id"] = None
        item["dedupe_status"] = "unique"
        if str(item.get("eligibility_status") or "") == "eligible":
            groups.setdefault(item["event_session_key"], []).append(item)

    for members in groups.values():
        ordered = sorted(
            members,
            key=lambda item: (
                base.parse_dt(item.get("entry_ts") or item.get("decision_at") or item.get("catalyst_at"))
                or datetime.max.replace(tzinfo=timezone.utc),
                0 if str(item.get("evidence_cohort") or "") == "strict_v1" else 1,
                str(item.get("candidate_id") or ""),
            ),
        )
        winner = ordered[0]
        for duplicate in ordered[1:]:
            duplicate.update({
                "eligibility_status": "rejected",
                "rejection_reason": "EVENT_SESSION_DUPLICATE",
                "outcome_status": "skipped",
                "net_pnl_usd": 0.0,
                "fees_usd": 0.0,
                "slippage_usd": 0.0,
                "funding_usd": 0.0,
                "duplicate_of_candidate_id": winner["candidate_id"],
                "dedupe_status": "duplicate_skipped",
            })
    return rows


def _summary(rows: list[dict[str, Any]], activated_at: str) -> dict[str, Any]:
    closed = [row for row in rows if row.get("window") == "forward_post_activation"
              and int(row.get("is_clean_for_edge") or 0) == 1
              and str(row.get("outcome_status") or "").lower() == "closed"
              and str(row.get("dedupe_status") or "unique") != "duplicate_skipped"]
    pnl = sum(float(row.get("net_pnl_usd") or 0.0) for row in closed)
    gross_win = sum(max(0.0, float(row.get("net_pnl_usd") or 0.0)) for row in closed)
    gross_loss = abs(sum(min(0.0, float(row.get("net_pnl_usd") or 0.0)) for row in closed))
    return {"activated_at": activated_at, "clean_closed": len(closed), "net_pnl_usd": round(pnl, 2),
            "profit_factor": (round(gross_win / gross_loss, 4) if gross_loss else None),
            "verdict": "REVIEW_ONLY" if len(closed) >= 30 and pnl > 0 and gross_loss and gross_win / gross_loss >= 1.25
                       else "INSUFFICIENT_CLEAN_SAMPLE"}


def refresh(*, db: str | None = None, now: datetime | None = None,
            persist: bool = True) -> dict[str, Any]:
    cfg = load_cfg()
    moment = now or datetime.now(timezone.utc)
    if not cfg.get("feature_flag", False):
        return {"enabled": False, "rows": [], "summary": {}}
    path = Path(db) if db else Path(load_config().db_path)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    try:
        _ensure(conn)
        activation_key = f"activated_at:{cfg['profile_id']}"
        row = conn.execute(f"SELECT v FROM {META} WHERE k=?", (activation_key,)).fetchone()
        activated_at = str(row[0]) if row else moment.isoformat()
        if persist and not row:
            conn.execute(f"INSERT INTO {META}(k,v) VALUES (?,?)", (activation_key, activated_at))
            conn.commit()
    finally:
        conn.close()
    evaluated = base.refresh(db=str(path), persist=False, now=moment, cfg=cfg)
    activation = datetime.fromisoformat(activated_at.replace("Z", "+00:00"))
    rows: list[dict[str, Any]] = []
    for source in evaluated.get("rows") or []:
        item = dict(source)
        catalyst = base.parse_dt(item.get("catalyst_at"))
        item["window"] = "forward_post_activation" if catalyst and catalyst >= activation else "historical_backfill"
        item["strategy_id"], item["profile_id"], item["shadow_lane"] = (
            cfg["strategy_id"], cfg["profile_id"], cfg["shadow_lane"])
        rows.append(item)
    _deduplicate_entries(rows)
    if persist and rows:
        conn = sqlite3.connect(path)
        try:
            _ensure(conn)
            sql = f"INSERT OR REPLACE INTO {TABLE} ({','.join(COLS)}) VALUES ({','.join('?' for _ in COLS)})"
            conn.executemany(sql, [tuple(
                json.dumps(item, default=str, sort_keys=True) if col == "payload_json" else item.get(col)
                for col in COLS
            ) for item in rows])
            conn.commit()
        finally:
            conn.close()
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        stored = [dict(row) for row in conn.execute(
            f"SELECT * FROM {TABLE} WHERE profile_id=?", (cfg["profile_id"],)
        )]
    finally:
        conn.close()
    return {"enabled": True, "generated_at": moment.isoformat(), "rows": rows,
            "stored": len(stored), "summary": _summary(stored, activated_at),
            "strategy_id": cfg["strategy_id"], "shadow_lane": cfg["shadow_lane"]}


def write_report(result: dict[str, Any]) -> Path:
    summary = result.get("summary") or {}
    path = ROOT / "reports" / "STOCKS_EARNINGS_GAP_CONTINUATION_SHADOW.md"
    path.write_text("\n".join([
        "# Stocks Earnings Gap Continuation - Shadow", "",
        "Isolated earnings-only continuation experiment. It never writes Paper or live signals.", "",
        f"Generated: {result.get('generated_at')}",
        f"Stored observations: {result.get('stored', 0)}",
        f"Forward clean closed: {summary.get('clean_closed', 0)}",
        f"Net PnL USD: {summary.get('net_pnl_usd', 0):.2f}",
        f"Profit factor: {summary.get('profit_factor')}",
        f"Verdict: {summary.get('verdict', 'DISABLED')}",
    ]), encoding="utf-8")
    return path


__all__ = ["load_cfg", "refresh", "write_report"]
