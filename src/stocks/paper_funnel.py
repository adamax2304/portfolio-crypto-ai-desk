"""Point-in-time observability for the stocks intraday Paper funnel.

The stocks pipeline may legitimately recalculate an idea after the cash close.
That newer view must not rewrite what Paper knew when a signal was created.
This module stores an immutable decision snapshot plus an append-only funnel
event trail.  It is observability only: no score, signal geometry, ledger,
alert, or live-routing writes occur here.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from src.config import load_config

VERSION = "stocks_paper_funnel_v1"
PLAN_MARKER = "market_closed_intraday_planning_only"

_SNAPSHOT_DDL = """
CREATE TABLE IF NOT EXISTS stocks_paper_decision_snapshots (
    signal_id TEXT PRIMARY KEY,
    captured_at TEXT NOT NULL,
    decision_at TEXT NOT NULL,
    signal_created_at TEXT NOT NULL,
    symbol TEXT NOT NULL,
    direction TEXT NOT NULL,
    source_tier TEXT,
    pre_gate_tier TEXT,
    funnel_state TEXT NOT NULL,
    target_session_open_at TEXT,
    target_session_close_at TEXT,
    snapshot_json TEXT NOT NULL,
    version TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_stocks_paper_snapshot_state
ON stocks_paper_decision_snapshots(funnel_state, decision_at);
"""

_EVENT_DDL = """
CREATE TABLE IF NOT EXISTS stocks_paper_funnel_events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    signal_id TEXT NOT NULL,
    event_at TEXT NOT NULL,
    stage TEXT NOT NULL,
    reason TEXT,
    payload_json TEXT NOT NULL,
    version TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_stocks_paper_funnel_signal
ON stocks_paper_funnel_events(signal_id, event_at);
"""

_OBSERVATION_DDL = """
CREATE TABLE IF NOT EXISTS stocks_paper_candidate_observations (
    observation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    signal_id TEXT NOT NULL,
    observed_at TEXT NOT NULL,
    signal_created_at TEXT NOT NULL,
    symbol TEXT NOT NULL,
    direction TEXT NOT NULL,
    tier TEXT,
    score REAL,
    status TEXT,
    decision_state TEXT NOT NULL,
    cap_reasons_json TEXT NOT NULL,
    snapshot_json TEXT NOT NULL,
    version TEXT NOT NULL,
    UNIQUE(signal_id, observed_at)
);
CREATE INDEX IF NOT EXISTS idx_stocks_candidate_observation_time
ON stocks_paper_candidate_observations(observed_at, symbol, direction);
"""


def _utc(value: datetime | None = None) -> datetime:
    moment = value or datetime.now(timezone.utc)
    return moment.replace(tzinfo=timezone.utc) if moment.tzinfo is None else moment.astimezone(timezone.utc)


def _iso(value: datetime | None = None) -> str:
    return _utc(value).isoformat()


def _json(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return dict(value)
    try:
        parsed = json.loads(value or "{}")
        return parsed if isinstance(parsed, dict) else {}
    except (TypeError, ValueError, json.JSONDecodeError):
        return {}


def ensure_tables(conn: sqlite3.Connection) -> None:
    conn.executescript(_SNAPSHOT_DDL)
    conn.executescript(_EVENT_DDL)
    conn.executescript(_OBSERVATION_DDL)
    columns = {
        str(row[1]) for row in conn.execute(
            "PRAGMA table_info(stocks_paper_decision_snapshots)"
        )
    }
    for name in ("target_session_open_at", "target_session_close_at"):
        if name not in columns:
            conn.execute(
                f"ALTER TABLE stocks_paper_decision_snapshots ADD COLUMN {name} TEXT"
            )
    rows = conn.execute(
        "SELECT signal_id,signal_created_at FROM stocks_paper_decision_snapshots "
        "WHERE target_session_open_at IS NULL OR target_session_close_at IS NULL"
    ).fetchall()
    if rows:
        from src.stocks.market_calendar import stock_intraday_target_session

        for signal_id, created_at in rows:
            try:
                created = datetime.fromisoformat(
                    str(created_at).replace("Z", "+00:00")
                )
                opened, closed = stock_intraday_target_session(created)
            except (TypeError, ValueError):
                continue
            conn.execute(
                "UPDATE stocks_paper_decision_snapshots "
                "SET target_session_open_at=?,target_session_close_at=? "
                "WHERE signal_id=?",
                (opened.isoformat(), closed.isoformat(), signal_id),
            )


def _state(row: dict[str, Any], raw: dict[str, Any]) -> str:
    tier = str(row.get("tier") or "").upper()
    reasons = " ".join(str(item) for item in (raw.get("cap_reasons") or []))
    if PLAN_MARKER in reasons:
        return "PREOPEN_PLAN"
    if tier in {"A", "B"}:
        return "RTH_ELIGIBLE"
    return "REJECTED_AT_DECISION"


def snapshot_row(conn: sqlite3.Connection, row: dict[str, Any], *, now: datetime | None = None) -> bool:
    """Insert the first decision view for a signal. Never overwrite it."""
    ensure_tables(conn)
    signal_id = str(row.get("signal_id") or "")
    if not signal_id:
        return False
    raw = _json(row.get("raw_idea_json"))
    decision_at = str(raw.get("decision_at") or row.get("created_at") or _iso(now))
    payload = {
        "tier": row.get("tier"), "score": row.get("score"),
        "entry_low": row.get("entry_low"), "entry_high": row.get("entry_high"),
        "entry_trigger": row.get("entry_trigger"), "suggested_entry": row.get("suggested_entry"),
        "stop_loss": row.get("stop_loss"), "invalidation": row.get("invalidation"),
        "tp1": row.get("tp1"), "tp2": row.get("tp2"), "tp3": row.get("tp3"),
        "setup_type": row.get("setup_type"), "market_regime": row.get("market_regime"),
        "pre_gate_tier": raw.get("pre_gate_tier"),
        "cap_reasons": raw.get("cap_reasons") or [],
        "intraday_actionability": raw.get("intraday_actionability") or {},
        "news_influence_contract": raw.get("news_influence_contract") or {},
    }
    state = _state(row, raw)
    observed_at = _iso(now)
    conn.execute(
        "INSERT OR IGNORE INTO stocks_paper_candidate_observations("
        "signal_id,observed_at,signal_created_at,symbol,direction,tier,score,status,"
        "decision_state,cap_reasons_json,snapshot_json,version) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
        (
            signal_id, observed_at, str(row.get("created_at") or decision_at),
            str(row.get("symbol") or "").upper(), str(row.get("direction") or "").lower(),
            str(row.get("tier") or "").upper(), row.get("score"), row.get("status"), state,
            json.dumps(raw.get("cap_reasons") or [], sort_keys=True),
            json.dumps(payload, sort_keys=True), VERSION,
        ),
    )
    try:
        from src.stocks.market_calendar import stock_intraday_target_session

        session_open, session_close = stock_intraday_target_session(
            datetime.fromisoformat(
                str(row.get("created_at") or decision_at).replace("Z", "+00:00")
            )
        )
    except (TypeError, ValueError):
        session_open = session_close = None
    before = conn.execute(
        "SELECT 1 FROM stocks_paper_decision_snapshots WHERE signal_id=?", (signal_id,)
    ).fetchone()
    conn.execute(
        "INSERT OR IGNORE INTO stocks_paper_decision_snapshots("
        "signal_id,captured_at,decision_at,signal_created_at,symbol,direction,source_tier,"
        "pre_gate_tier,funnel_state,target_session_open_at,target_session_close_at,"
        "snapshot_json,version) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (signal_id, _iso(now), decision_at, str(row.get("created_at") or decision_at),
         str(row.get("symbol") or "").upper(), str(row.get("direction") or "").lower(),
         str(row.get("tier") or "").upper(), str(raw.get("pre_gate_tier") or "").upper(),
         state, session_open.isoformat() if session_open else None,
         session_close.isoformat() if session_close else None,
         json.dumps(payload, sort_keys=True), VERSION),
    )
    if before is None:
        record_event(conn, signal_id=signal_id, stage=state, now=now,
                     reason="initial_point_in_time_snapshot")
        return True
    return False


def snapshot_signals(db: str | Path | None, signal_ids: Iterable[str], *, now: datetime | None = None) -> int:
    """Capture newly registered stocks signals by idempotent signal id."""
    path = Path(db or load_config().db_path)
    ids = [str(value) for value in signal_ids if value]
    if not ids:
        return 0
    inserted = 0
    with sqlite3.connect(path, timeout=30.0) as conn:
        conn.row_factory = sqlite3.Row
        ensure_tables(conn)
        for signal_id in ids:
            row = conn.execute("SELECT * FROM proposed_signals WHERE signal_id=?", (signal_id,)).fetchone()
            if row is not None:
                inserted += int(snapshot_row(conn, dict(row), now=now))
        conn.commit()
    return inserted


def record_event(conn: sqlite3.Connection, *, signal_id: str, stage: str,
                 reason: str | None = None, payload: dict[str, Any] | None = None,
                 now: datetime | None = None) -> None:
    ensure_tables(conn)
    conn.execute(
        "INSERT INTO stocks_paper_funnel_events(signal_id,event_at,stage,reason,payload_json,version) "
        "VALUES(?,?,?,?,?,?)",
        (str(signal_id), _iso(now), str(stage), reason,
         json.dumps(payload or {}, sort_keys=True), VERSION),
    )


def record_event_for_db(db: str | Path | None, *, signal_id: str, stage: str,
                        reason: str | None = None, payload: dict[str, Any] | None = None,
                        now: datetime | None = None) -> None:
    """Best-effort funnel event; a diagnostic write never blocks tracking."""
    try:
        with sqlite3.connect(Path(db or load_config().db_path), timeout=0.25) as conn:
            conn.execute("PRAGMA busy_timeout=250")
            record_event(conn, signal_id=signal_id, stage=stage, reason=reason,
                         payload=payload, now=now)
            conn.commit()
    except Exception:
        pass


def active_eligible_signal_ids(db: str | Path | None) -> list[str]:
    """Return active signals that were A/B at their original RTH decision.

    A later end-of-day recalculation may cap the mutable signal row to C. This
    preserves the original RTH candidate for observation, but never promotes a
    pre-open plan or a candidate rejected by its contemporaneous gates.
    """
    path = Path(db or load_config().db_path)
    try:
        with sqlite3.connect(path, timeout=30.0) as conn:
            rows = conn.execute(
                "SELECT p.signal_id FROM proposed_signals p "
                "JOIN stocks_paper_decision_snapshots s ON s.signal_id=p.signal_id "
                "WHERE p.asset_class='stocks' AND p.mode='intraday' "
                "AND p.status IN ('generated','waiting_for_entry','triggered','tp1_hit','tp2_hit') "
                "AND s.funnel_state='RTH_ELIGIBLE' ORDER BY p.created_at DESC"
            ).fetchall()
        return [str(row[0]) for row in rows]
    except sqlite3.OperationalError:
        return []


def report(db: str | Path | None = None, *, limit: int = 30) -> dict[str, Any]:
    """Read-only daily operations view for the stock Paper funnel."""
    path = Path(db or load_config().db_path)
    out: dict[str, Any] = {"snapshot_states": {}, "tracker_states": {}, "recent": []}
    try:
        with sqlite3.connect(path, timeout=30.0) as conn:
            conn.row_factory = sqlite3.Row
            ensure_tables(conn)
            out["snapshot_states"] = dict(conn.execute(
                "SELECT funnel_state,COUNT(*) FROM stocks_paper_decision_snapshots "
                "GROUP BY funnel_state"
            ).fetchall())
            out["tracker_states"] = dict(conn.execute(
                "SELECT reason,COUNT(*) FROM stocks_paper_funnel_events WHERE stage='TRACKER_STATUS' "
                "GROUP BY reason"
            ).fetchall())
            signal_cols = {row[1] for row in conn.execute("PRAGMA table_info(proposed_signals)")}
            updated_expr = "p.updated_at" if "updated_at" in signal_cols else "NULL AS updated_at"
            out["recent"] = [dict(row) for row in conn.execute(
                "SELECT s.signal_id,s.symbol,s.direction,s.source_tier,s.pre_gate_tier,s.funnel_state,"
                f"p.status,{updated_expr},s.decision_at "
                "FROM stocks_paper_decision_snapshots s "
                "LEFT JOIN proposed_signals p ON p.signal_id=s.signal_id "
                "ORDER BY s.decision_at DESC LIMIT ?", (max(1, int(limit)),)
            )]
    except sqlite3.OperationalError as exc:
        out["error"] = type(exc).__name__
    return out


def render_markdown(data: dict[str, Any]) -> str:
    lines = ["# Stocks Paper Funnel", "",
             "Point-in-time snapshots are immutable; current mutable signal status is shown separately.", "",
             f"- decision states: `{json.dumps(data.get('snapshot_states') or {}, sort_keys=True)}`",
             f"- tracker terminal states: `{json.dumps(data.get('tracker_states') or {}, sort_keys=True)}`", "",
             "| decision at | symbol | side | original tier | current status | funnel state |",
             "|---|---|---|---|---|---|"]
    for row in data.get("recent") or []:
        lines.append(
            f"| {row.get('decision_at') or ''} | {row.get('symbol') or ''} | "
            f"{row.get('direction') or ''} | {row.get('source_tier') or ''} | "
            f"{row.get('status') or ''} | {row.get('funnel_state') or ''} |"
        )
    return "\n".join(lines) + "\n"


__all__ = [
    "VERSION", "PLAN_MARKER", "ensure_tables", "snapshot_row", "snapshot_signals",
    "record_event", "record_event_for_db", "active_eligible_signal_ids", "report", "render_markdown",
]
