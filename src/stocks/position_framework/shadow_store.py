"""SQLite storage for the Stocks Position Framework — SEPARATE shadow tables.

Deliberately self-contained: creates and reads its own `stocks_position_candidates` /
`stocks_position_outcomes` tables via CREATE TABLE IF NOT EXISTS (migration-safe, additive). It
NEVER writes to `proposed_signals` and NEVER touches `signal_outcomes` — this is a shadow lane.
Outcomes are recorded honestly: a row with no fill/close stays `pending` with NULL PnL rather than
fabricating numbers.
"""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any, Iterable
from datetime import datetime, timezone

from . import SOURCE_VERSION
from .config import DEFAULT_DB_PATH

_CANDIDATES_DDL = """
CREATE TABLE IF NOT EXISTS stocks_position_candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_id TEXT UNIQUE,
    created_at TEXT,
    symbol TEXT,
    asset_class TEXT,
    mode TEXT,
    playbook TEXT,
    setup_variant TEXT,
    direction TEXT,
    score REAL,
    data_confidence REAL,
    entry_price REAL,
    entry_low REAL,
    entry_high REAL,
    stop_price REAL,
    stop_reason TEXT,
    risk_pct REAL,
    risk_usd REAL,
    tp1 REAL,
    tp1_r REAL,
    tp2 REAL,
    tp2_r REAL,
    trail_rule TEXT,
    max_holding_days INTEGER,
    market_regime TEXT,
    sector TEXT,
    sector_etf TEXT,
    rs_spy REAL,
    rs_sector REAL,
    volume_ratio REAL,
    atr14 REAL,
    dollar_volume_30d REAL,
    near_high_pct REAL,
    earnings_risk TEXT,
    insider_cluster_confirmed INTEGER,
    insider_unique_insiders INTEGER,
    insider_purchase_value_usd REAL,
    insider_context_ts TEXT,
    insider_context_json TEXT,
    thesis TEXT,
    counter_thesis TEXT,
    reasons_json TEXT,
    warnings_json TEXT,
    rejection_reasons_json TEXT,
    status TEXT DEFAULT 'shadow_open',
    source_version TEXT
);
"""

_OUTCOMES_DDL = """
CREATE TABLE IF NOT EXISTS stocks_position_outcomes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_id TEXT,
    checked_at TEXT,
    status TEXT DEFAULT 'pending',
    close_reason TEXT,
    last_price REAL,
    unrealized_pnl_usd REAL,
    realized_pnl_usd REAL,
    net_pnl_usd REAL,
    paper_execution_r REAL,
    max_favorable_excursion_r REAL,
    max_adverse_excursion_r REAL,
    holding_days INTEGER,
    gap_loss_r REAL,
    notes_json TEXT,
    UNIQUE(candidate_id)
);
"""

_REVIEWS_DDL = """
CREATE TABLE IF NOT EXISTS stocks_position_reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_id TEXT UNIQUE,
    reviewed_at TEXT,
    reviewer TEXT,
    source TEXT,
    verdict TEXT,
    confidence REAL,
    reasons_json TEXT,
    key_news_json TEXT,
    risk_notes_json TEXT,
    raw_review_json TEXT,
    markdown_path TEXT
);
"""

_SCAN_RUNS_DDL = """
CREATE TABLE IF NOT EXISTS stocks_position_scan_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL,
    universe_size INTEGER NOT NULL DEFAULT 0,
    scanned INTEGER NOT NULL DEFAULT 0,
    candidate_count INTEGER NOT NULL DEFAULT 0,
    rejected_count INTEGER NOT NULL DEFAULT 0,
    persisted INTEGER NOT NULL DEFAULT 0,
    market_label TEXT,
    dry_run INTEGER NOT NULL DEFAULT 0,
    data_notes_json TEXT
);
"""

# Recognised review verdicts (shadow research only — NEVER actionability / live / paper promotion).
REVIEW_VERDICTS = (
    "approve_shadow", "wait_pullback", "reject_news_risk", "reject_earnings_risk",
    "reject_legal_risk", "needs_more_data",
)

_INDEXES = (
    "CREATE INDEX IF NOT EXISTS idx_spc_created ON stocks_position_candidates(created_at);",
    "CREATE INDEX IF NOT EXISTS idx_spc_symbol ON stocks_position_candidates(symbol);",
    "CREATE INDEX IF NOT EXISTS idx_spc_status ON stocks_position_candidates(status);",
    "CREATE INDEX IF NOT EXISTS idx_spr_candidate ON stocks_position_reviews(candidate_id);",
)

# Column order for candidate inserts (matches the flattened candidate dict below).
_CAND_COLS = (
    "candidate_id", "created_at", "symbol", "asset_class", "mode", "playbook", "setup_variant",
    "direction", "score", "data_confidence", "entry_price", "entry_low", "entry_high",
    "stop_price", "stop_reason", "risk_pct", "risk_usd", "tp1", "tp1_r", "tp2", "tp2_r",
    "trail_rule", "max_holding_days", "market_regime", "sector", "sector_etf", "rs_spy",
    "rs_sector", "volume_ratio", "atr14", "dollar_volume_30d", "near_high_pct", "earnings_risk",
    "insider_cluster_confirmed", "insider_unique_insiders", "insider_purchase_value_usd",
    "insider_context_ts", "insider_context_json",
    "thesis", "counter_thesis", "reasons_json", "warnings_json", "rejection_reasons_json",
    "status", "source_version",
)


def _connect(db_path: str | Path | None) -> sqlite3.Connection:
    p = Path(db_path) if db_path else DEFAULT_DB_PATH
    p.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(p), timeout=30)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_tables(db_path: str | Path | None = None) -> None:
    conn = _connect(db_path)
    try:
        conn.execute(_CANDIDATES_DDL)
        conn.execute(_OUTCOMES_DDL)
        conn.execute(_REVIEWS_DDL)
        conn.execute(_SCAN_RUNS_DDL)
        existing = {str(row[1]) for row in conn.execute("PRAGMA table_info(stocks_position_candidates)")}
        additions = {
            "insider_cluster_confirmed": "INTEGER", "insider_unique_insiders": "INTEGER",
            "insider_purchase_value_usd": "REAL", "insider_context_ts": "TEXT",
            "insider_context_json": "TEXT",
        }
        for name, sql_type in additions.items():
            if name not in existing:
                conn.execute(f"ALTER TABLE stocks_position_candidates ADD COLUMN {name} {sql_type}")
        for stmt in _INDEXES:
            conn.execute(stmt)
        conn.commit()
    finally:
        conn.close()


def _flatten(candidate: dict[str, Any], *, created_at: str) -> dict[str, Any]:
    """Flatten a detector candidate (with nested risk_plan) into a candidates-table row."""
    plan = candidate.get("risk_plan") or {}
    cid = f"spf_{candidate.get('symbol')}_{created_at[:10]}"
    return {
        "candidate_id": cid,
        "created_at": created_at,
        "symbol": candidate.get("symbol"),
        "asset_class": candidate.get("asset_class"),
        "mode": candidate.get("mode"),
        "playbook": candidate.get("playbook"),
        "setup_variant": candidate.get("setup_variant"),
        "direction": candidate.get("direction", "long"),
        "score": candidate.get("score"),
        "data_confidence": candidate.get("data_confidence"),
        "entry_price": candidate.get("entry_price"),
        "entry_low": candidate.get("entry_low"),
        "entry_high": candidate.get("entry_high"),
        "stop_price": plan.get("stop_price"),
        "stop_reason": plan.get("stop_reason"),
        "risk_pct": plan.get("risk_pct_of_price"),
        "risk_usd": plan.get("risk_usd"),
        "tp1": plan.get("tp1"), "tp1_r": plan.get("tp1_r"),
        "tp2": plan.get("tp2"), "tp2_r": plan.get("tp2_r"),
        "trail_rule": plan.get("trail_rule"),
        "max_holding_days": plan.get("max_holding_days"),
        "market_regime": candidate.get("market_regime"),
        "sector": candidate.get("sector"),
        "sector_etf": candidate.get("sector_etf"),
        "rs_spy": candidate.get("rs_spy"),
        "rs_sector": candidate.get("rs_sector"),
        "volume_ratio": candidate.get("volume_ratio"),
        "atr14": candidate.get("atr14"),
        "dollar_volume_30d": candidate.get("dollar_volume_30d"),
        "near_high_pct": candidate.get("near_high_pct"),
        "earnings_risk": candidate.get("earnings_risk"),
        "insider_cluster_confirmed": int(bool((candidate.get("insider_context") or {}).get("cluster_confirmed"))),
        "insider_unique_insiders": (candidate.get("insider_context") or {}).get("unique_insiders"),
        "insider_purchase_value_usd": (candidate.get("insider_context") or {}).get("purchase_value_usd"),
        "insider_context_ts": (candidate.get("insider_context") or {}).get("context_ts"),
        "insider_context_json": json.dumps(candidate.get("insider_context") or {}),
        "thesis": candidate.get("thesis"),
        "counter_thesis": candidate.get("counter_thesis"),
        "reasons_json": json.dumps(candidate.get("reasons") or []),
        "warnings_json": json.dumps(candidate.get("warnings") or []),
        "rejection_reasons_json": json.dumps(candidate.get("rejection_reasons") or []),
        "status": candidate.get("status", "shadow_open"),
        "source_version": candidate.get("source_version", SOURCE_VERSION),
    }


def insert_candidates(candidates: Iterable[dict[str, Any]], *, created_at: str,
                      db_path: str | Path | None = None) -> int:
    """Upsert passed candidates into stocks_position_candidates. Returns rows written.

    Idempotent per (symbol, scan-date): re-running a same-day scan updates in place. Also suppresses
    duplicate open theses across days: if the same symbol/playbook/setup/direction is already open and
    has no terminal outcome, a new scan does not create a second open clone.
    """
    rows = [_flatten(c, created_at=created_at) for c in candidates if c.get("passed")]
    if not rows:
        ensure_tables(db_path)
        return 0
    ensure_tables(db_path)
    conn = _connect(db_path)
    try:
        filtered: list[dict[str, Any]] = []
        for r in rows:
            duplicate = conn.execute(
                """
                SELECT c.candidate_id
                FROM stocks_position_candidates c
                LEFT JOIN stocks_position_outcomes o ON o.candidate_id = c.candidate_id
                WHERE c.status = 'shadow_open'
                  AND COALESCE(o.status, '') NOT IN ('closed', 'no_entry')
                  AND c.candidate_id <> ?
                  AND c.symbol = ?
                  AND COALESCE(c.playbook, '') = COALESCE(?, '')
                  AND COALESCE(c.setup_variant, '') = COALESCE(?, '')
                  AND COALESCE(c.direction, '') = COALESCE(?, '')
                LIMIT 1
                """,
                (r["candidate_id"], r["symbol"], r["playbook"], r["setup_variant"], r["direction"]),
            ).fetchone()
            if duplicate:
                continue
            filtered.append(r)
        if not filtered:
            return 0
        placeholders = ", ".join("?" for _ in _CAND_COLS)
        updates = ", ".join(f"{c}=excluded.{c}" for c in _CAND_COLS if c != "candidate_id")
        sql = (f"INSERT INTO stocks_position_candidates ({', '.join(_CAND_COLS)}) "
               f"VALUES ({placeholders}) "
               f"ON CONFLICT(candidate_id) DO UPDATE SET {updates}")
        conn.executemany(sql, [tuple(r[c] for c in _CAND_COLS) for r in filtered])
        conn.commit()
        return len(filtered)
    finally:
        conn.close()


# Candidate.status values written once an outcome resolves (so an open list never shows them).
TERMINAL_CANDIDATE_STATUSES = (
    "shadow_closed", "shadow_no_entry", "shadow_duplicate_superseded",
)
# Outcome.status values that mean the trade is finished (used to exclude via LEFT JOIN as defence).
TERMINAL_OUTCOME_STATUSES = ("closed", "no_entry")


def _thesis_key(row: dict[str, Any]) -> tuple[str, str, str, str]:
    return (
        str(row.get("symbol") or ""),
        str(row.get("playbook") or ""),
        str(row.get("setup_variant") or ""),
        str(row.get("direction") or ""),
    )


def _dedupe_open_theses(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Keep one open row per symbol/playbook/setup/direction thesis.

    Historical duplicate rows remain in the DB for auditability, but open candidate reads and outcome
    refreshes should not double-count the same still-open thesis.
    """
    out: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str, str]] = set()
    for row in sorted(rows, key=lambda r: str(r.get("created_at") or "")):
        key = _thesis_key(row)
        if key in seen:
            continue
        seen.add(key)
        out.append(row)
    return sorted(out, key=lambda r: (str(r.get("created_at") or ""), float(r.get("score") or 0)), reverse=True)


def reconcile_open_candidate_lifecycle(*, db_path: str | Path | None = None,
                                       checked_at: str | None = None) -> dict[str, int]:
    """Repair legacy Position Framework lifecycle gaps without inventing execution.

    Historical scans could leave two open rows for the same thesis or an open
    candidate without its required pending outcome.  Keep the oldest thesis as
    the canonical record, mark later duplicates terminal for auditability, and
    create a *pending* outcome only for a unique canonical orphan.  No PnL,
    fill, or actionability is created by this reconciliation.
    """
    ensure_tables(db_path)
    at = checked_at or datetime.now(timezone.utc).isoformat()
    result = {
        "duplicates_superseded": 0,
        "pending_outcomes_created": 0,
        "superseded_outcomes_created": 0,
    }
    conn = _connect(db_path)
    try:
        legacy_superseded = [dict(r) for r in conn.execute(
            "SELECT c.candidate_id FROM stocks_position_candidates c "
            "LEFT JOIN stocks_position_outcomes o ON o.candidate_id=c.candidate_id "
            "WHERE c.status='shadow_duplicate_superseded' AND o.candidate_id IS NULL"
        )]
        for row in legacy_superseded:
            conn.execute(
                "INSERT OR IGNORE INTO stocks_position_outcomes "
                "(candidate_id,checked_at,status,close_reason,notes_json) VALUES (?,?,?,?,?)",
                (row["candidate_id"], at, "no_entry", "superseded_duplicate",
                 json.dumps({
                     "lifecycle_reconciled": True,
                     "reconciled_at": at,
                     "reason": "legacy_duplicate_superseded_without_outcome",
                 })),
            )
            result["superseded_outcomes_created"] += int(
                conn.execute("SELECT changes()").fetchone()[0]
            )
        rows = [dict(r) for r in conn.execute(
            "SELECT c.*, o.status AS outcome_status FROM stocks_position_candidates c "
            "LEFT JOIN stocks_position_outcomes o ON o.candidate_id=c.candidate_id "
            "WHERE c.status='shadow_open' "
            "AND (o.status IS NULL OR o.status IN ('pending','open')) "
            "ORDER BY c.created_at ASC, c.candidate_id ASC"
        )]
        canonical: list[dict[str, Any]] = []
        seen: set[tuple[str, str, str, str]] = set()
        for row in rows:
            key = _thesis_key(row)
            if key in seen:
                conn.execute(
                    "UPDATE stocks_position_candidates SET status='shadow_duplicate_superseded' "
                    "WHERE candidate_id=?", (row["candidate_id"],),
                )
                conn.execute(
                    "INSERT OR IGNORE INTO stocks_position_outcomes "
                    "(candidate_id,checked_at,status,close_reason,notes_json) VALUES (?,?,?,?,?)",
                    (row["candidate_id"], at, "no_entry", "superseded_duplicate",
                     json.dumps({
                         "lifecycle_reconciled": True,
                         "reconciled_at": at,
                         "reason": "open_duplicate_superseded",
                         "canonical_thesis_key": list(key),
                     })),
                )
                result["superseded_outcomes_created"] += int(
                    conn.execute("SELECT changes()").fetchone()[0]
                )
                result["duplicates_superseded"] += 1
                continue
            seen.add(key)
            canonical.append(row)
        for row in canonical:
            if row.get("outcome_status") is not None:
                continue
            conn.execute(
                "INSERT OR IGNORE INTO stocks_position_outcomes "
                "(candidate_id,checked_at,status,close_reason,notes_json) VALUES (?,?,?,?,?)",
                (row["candidate_id"], at, "pending", "awaiting_outcome_refresh",
                 json.dumps({"lifecycle_reconciled": True, "reconciled_at": at})),
            )
            result["pending_outcomes_created"] += int(conn.execute("SELECT changes()").fetchone()[0])
        conn.commit()
        return result
    finally:
        conn.close()


def latest_candidates(*, limit: int = 25, only_open: bool = True,
                      db_path: str | Path | None = None) -> list[dict[str, Any]]:
    """Latest candidates. With only_open=True this returns genuinely OPEN candidates: status is
    still `shadow_open` AND there is no terminal (closed/no_entry) outcome — belt-and-suspenders so
    a resolved candidate never lingers in the open list."""
    reconcile_open_candidate_lifecycle(db_path=db_path)
    conn = _connect(db_path)
    try:
        if only_open:
            sql = ("SELECT c.* FROM stocks_position_candidates c "
                   "LEFT JOIN stocks_position_outcomes o ON o.candidate_id = c.candidate_id "
                   "WHERE c.status = 'shadow_open' "
                   "AND (o.status IS NULL OR o.status NOT IN ('closed','no_entry')) "
                   "ORDER BY c.created_at DESC, c.score DESC LIMIT ?")
        else:
            sql = ("SELECT * FROM stocks_position_candidates "
                   "ORDER BY created_at DESC, score DESC LIMIT ?")
        fetch_limit = max(int(limit) * 5, 100) if only_open else int(limit)
        cur = conn.execute(sql, (fetch_limit,))
        rows = [dict(r) for r in cur.fetchall()]
        if only_open:
            rows = _dedupe_open_theses(rows)
        return rows[: int(limit)]
    finally:
        conn.close()


def set_candidate_status(candidate_id: str, status: str,
                         db_path: str | Path | None = None) -> None:
    """Mark a candidate terminal (shadow_closed / shadow_no_entry) after its outcome resolves."""
    ensure_tables(db_path)
    conn = _connect(db_path)
    try:
        conn.execute("UPDATE stocks_position_candidates SET status=? WHERE candidate_id=?",
                     (status, candidate_id))
        conn.commit()
    finally:
        conn.close()


def latest_scan_time(db_path: str | Path | None = None) -> str | None:
    ensure_tables(db_path)
    conn = _connect(db_path)
    try:
        cur = conn.execute(
            "SELECT COALESCE((SELECT MAX(created_at) FROM stocks_position_scan_runs), "
            "(SELECT MAX(created_at) FROM stocks_position_candidates)) AS t"
        )
        row = cur.fetchone()
        return row["t"] if row else None
    finally:
        conn.close()


def record_scan_run(*, created_at: str, universe_size: int, scanned: int,
                    candidate_count: int, rejected_count: int, persisted: int,
                    market_label: str | None = None, dry_run: bool = False,
                    data_notes: Iterable[str] | None = None,
                    db_path: str | Path | None = None) -> None:
    """Persist scan telemetry, including zero-candidate scans, in the shadow lane only."""
    if dry_run:
        return
    ensure_tables(db_path)
    conn = _connect(db_path)
    try:
        conn.execute(
            "INSERT INTO stocks_position_scan_runs "
            "(created_at,universe_size,scanned,candidate_count,rejected_count,persisted,"
            "market_label,dry_run,data_notes_json) VALUES (?,?,?,?,?,?,?,?,?)",
            (created_at, int(universe_size), int(scanned), int(candidate_count),
             int(rejected_count), int(persisted), market_label, 0,
             json.dumps(list(data_notes or []))),
        )
        conn.commit()
    finally:
        conn.close()


def candidates_on_date(scan_date: str, db_path: str | Path | None = None) -> list[dict[str, Any]]:
    ensure_tables(db_path)
    conn = _connect(db_path)
    try:
        cur = conn.execute(
            "SELECT * FROM stocks_position_candidates WHERE substr(created_at,1,10)=? "
            "ORDER BY score DESC", (scan_date[:10],))
        return [dict(r) for r in cur.fetchall()]
    finally:
        conn.close()


def open_candidates(db_path: str | Path | None = None) -> list[dict[str, Any]]:
    """Candidates that have no terminal outcome yet (for the outcome-refresh skeleton)."""
    reconcile_open_candidate_lifecycle(db_path=db_path)
    conn = _connect(db_path)
    try:
        cur = conn.execute(
            "SELECT c.* FROM stocks_position_candidates c "
            "LEFT JOIN stocks_position_outcomes o ON o.candidate_id = c.candidate_id "
            "WHERE c.status = 'shadow_open' "
            "AND (o.status IS NULL OR o.status IN ('pending','open')) "
            "ORDER BY c.created_at DESC")
        return _dedupe_open_theses([dict(r) for r in cur.fetchall()])
    finally:
        conn.close()


def upsert_outcome(candidate_id: str, *, checked_at: str, status: str = "pending",
                   fields: dict[str, Any] | None = None,
                   db_path: str | Path | None = None) -> None:
    """Record/refresh an outcome row. Honest by default: unset PnL stays NULL (no fake fills)."""
    ensure_tables(db_path)
    fields = dict(fields or {})
    cols = ["candidate_id", "checked_at", "status", "close_reason", "last_price",
            "unrealized_pnl_usd", "realized_pnl_usd", "net_pnl_usd", "paper_execution_r",
            "max_favorable_excursion_r", "max_adverse_excursion_r", "holding_days",
            "gap_loss_r", "notes_json"]
    vals = {
        "candidate_id": candidate_id, "checked_at": checked_at, "status": status,
        "close_reason": fields.get("close_reason"), "last_price": fields.get("last_price"),
        "unrealized_pnl_usd": fields.get("unrealized_pnl_usd"),
        "realized_pnl_usd": fields.get("realized_pnl_usd"),
        "net_pnl_usd": fields.get("net_pnl_usd"),
        "paper_execution_r": fields.get("paper_execution_r"),
        "max_favorable_excursion_r": fields.get("max_favorable_excursion_r"),
        "max_adverse_excursion_r": fields.get("max_adverse_excursion_r"),
        "holding_days": fields.get("holding_days"), "gap_loss_r": fields.get("gap_loss_r"),
        "notes_json": json.dumps(fields.get("notes") or {}),
    }
    conn = _connect(db_path)
    try:
        ph = ", ".join("?" for _ in cols)
        upd = ", ".join(f"{c}=excluded.{c}" for c in cols if c != "candidate_id")
        conn.execute(
            f"INSERT INTO stocks_position_outcomes ({', '.join(cols)}) VALUES ({ph}) "
            f"ON CONFLICT(candidate_id) DO UPDATE SET {upd}",
            tuple(vals[c] for c in cols))
        conn.commit()
    finally:
        conn.close()


def latest_outcomes(*, limit: int = 50, db_path: str | Path | None = None) -> list[dict[str, Any]]:
    ensure_tables(db_path)
    conn = _connect(db_path)
    try:
        cur = conn.execute(
            "SELECT * FROM stocks_position_outcomes ORDER BY checked_at DESC LIMIT ?", (int(limit),))
        return [dict(r) for r in cur.fetchall()]
    finally:
        conn.close()


def candidate_exists(candidate_id: str, db_path: str | Path | None = None) -> bool:
    ensure_tables(db_path)
    conn = _connect(db_path)
    try:
        row = conn.execute(
            "SELECT 1 FROM stocks_position_candidates WHERE candidate_id=? LIMIT 1",
            (candidate_id,)).fetchone()
        return row is not None
    finally:
        conn.close()


_REVIEW_COLS = ("candidate_id", "reviewed_at", "reviewer", "source", "verdict", "confidence",
                "reasons_json", "key_news_json", "risk_notes_json", "raw_review_json", "markdown_path")


def upsert_review(candidate_id: str, *, reviewed_at: str, verdict: str,
                  reviewer: str | None = "opus_enriched_review", source: str | None = None,
                  confidence: float | None = None, reasons: Any = None, key_news: Any = None,
                  risk_notes: Any = None, raw_review: Any = None, markdown_path: str | None = None,
                  db_path: str | Path | None = None) -> None:
    """Insert/update a shadow REVIEW row. This is a research annotation only — it NEVER changes the
    candidate, never writes proposed_signals/signal_outcomes/paper_*, never makes anything
    actionable or live."""
    ensure_tables(db_path)
    vals = {
        "candidate_id": candidate_id, "reviewed_at": reviewed_at, "reviewer": reviewer,
        "source": source, "verdict": verdict,
        "confidence": (None if confidence is None else float(confidence)),
        "reasons_json": json.dumps(reasons if reasons is not None else []),
        "key_news_json": json.dumps(key_news if key_news is not None else []),
        "risk_notes_json": json.dumps(risk_notes if risk_notes is not None else []),
        "raw_review_json": (raw_review if isinstance(raw_review, str) else json.dumps(raw_review or {})),
        "markdown_path": markdown_path,
    }
    conn = _connect(db_path)
    try:
        ph = ", ".join("?" for _ in _REVIEW_COLS)
        upd = ", ".join(f"{c}=excluded.{c}" for c in _REVIEW_COLS if c != "candidate_id")
        conn.execute(
            f"INSERT INTO stocks_position_reviews ({', '.join(_REVIEW_COLS)}) VALUES ({ph}) "
            f"ON CONFLICT(candidate_id) DO UPDATE SET {upd}",
            tuple(vals[c] for c in _REVIEW_COLS))
        conn.commit()
    finally:
        conn.close()


def review_for(candidate_id: str, db_path: str | Path | None = None) -> dict[str, Any] | None:
    ensure_tables(db_path)
    conn = _connect(db_path)
    try:
        row = conn.execute(
            "SELECT * FROM stocks_position_reviews WHERE candidate_id=?", (candidate_id,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def reviews_by_candidate(db_path: str | Path | None = None) -> dict[str, dict[str, Any]]:
    ensure_tables(db_path)
    conn = _connect(db_path)
    try:
        cur = conn.execute("SELECT * FROM stocks_position_reviews")
        return {r["candidate_id"]: dict(r) for r in cur.fetchall()}
    finally:
        conn.close()


def readiness_summary(db_path: str | Path | None = None,
                      cfg: dict[str, Any] | None = None) -> dict[str, Any]:
    """SHADOW-ONLY readiness read-model for the framework. Reports latest scan time, candidate count,
    closed/pending/no_entry outcome counts, net USD, and sample-vs-evidence-gate — WITHOUT ever
    touching proposed_signals / actionability / live. Honest: with 0 candidates it says 'no evidence
    yet' rather than implying a result."""
    from .config import load_config as _load_pf
    cfg = cfg or _load_pf()
    gate = (cfg.get("evidence_gate") or {})
    min_trades = int(gate.get("min_forward_trades", 30))
    min_days = int(gate.get("min_forward_days", 28))
    ensure_tables(db_path)
    conn = _connect(db_path)
    try:
        n_cand = conn.execute("SELECT COUNT(*) FROM stocks_position_candidates").fetchone()[0]
        oc = {r[0] or "unknown": r[1] for r in conn.execute(
            "SELECT status, COUNT(*) FROM stocks_position_outcomes GROUP BY status").fetchall()}
        net_usd = conn.execute(
            "SELECT COALESCE(SUM(net_pnl_usd),0) FROM stocks_position_outcomes "
            "WHERE status='closed'").fetchone()[0]
        # CLEAN closed = data-clean outcomes (no data-gap loss at entry). Only clean outcomes count
        # toward the evidence gate — a gappy entry is a coverage artifact, never edge (S3/S4).
        clean_closed = conn.execute(
            "SELECT COUNT(*) FROM stocks_position_outcomes WHERE status='closed' "
            "AND (gap_loss_r IS NULL OR gap_loss_r = 0)").fetchone()[0]
        clean_net_usd = conn.execute(
            "SELECT COALESCE(SUM(net_pnl_usd),0) FROM stocks_position_outcomes WHERE status='closed' "
            "AND (gap_loss_r IS NULL OR gap_loss_r = 0)").fetchone()[0]
        latest = conn.execute(
            "SELECT MAX(created_at) FROM stocks_position_candidates").fetchone()[0]
    finally:
        conn.close()
    closed = int(oc.get("closed", 0))
    clean_closed = int(clean_closed)
    dirty_closed = max(0, closed - clean_closed)
    pending = int(oc.get("pending", 0)) + int(oc.get("open", 0))
    no_entry = int(oc.get("no_entry", 0))
    has_evidence = n_cand > 0
    # verdict is CLEAN-sample based and can never conclude good/bad until clean evidence is sufficient
    if not has_evidence:
        verdict = "NO_EVIDENCE"
    elif clean_closed < min_trades:
        verdict = "INSUFFICIENT_CLEAN_SAMPLE"
    elif (clean_net_usd or 0) > 0:
        verdict = "GATE_MET_REVIEW"
    else:
        verdict = "ACCUMULATING"
    if not has_evidence:
        msg = "no evidence yet — run `stocks-position-scan` to accumulate shadow candidates"
    elif verdict == "INSUFFICIENT_CLEAN_SAMPLE":
        msg = (f"INSUFFICIENT CLEAN SAMPLE — only {clean_closed}/{min_trades} CLEAN closed shadow "
               f"outcomes (dirty/gappy excluded: {dirty_closed}); clean sample still insufficient, "
               "NO good/bad conclusion allowed yet (shadow-only, never promoted)")
    else:
        msg = (f"accumulating: {clean_closed}/{min_trades} CLEAN closed shadow outcomes toward the "
               f"evidence gate (dirty/gappy excluded: {dirty_closed}; shadow-only, never promoted)")
    return {
        "shadow_only": True, "scheduler_enabled": bool(cfg.get("scheduler_enabled", False)),
        "write_proposed_signals": bool(cfg.get("write_proposed_signals", False)),
        "latest_scan_time": latest, "candidates_count": int(n_cand),
        "outcomes": {"closed": closed, "clean_closed": clean_closed, "dirty_closed": dirty_closed,
                     "pending": pending, "no_entry": no_entry},
        "net_usd_closed": round(float(net_usd or 0.0), 2),
        "net_usd_clean_closed": round(float(clean_net_usd or 0.0), 2),
        "evidence_gate": {"min_forward_trades": min_trades, "min_forward_days": min_days,
                          "closed_sample": closed, "clean_closed_sample": clean_closed,
                          "sample_meets_gate": clean_closed >= min_trades},
        "has_evidence": has_evidence,
        # this framework is evaluated INDEPENDENTLY — it never reuses legacy stocks swing/invest evidence
        "legacy_evidence_reused": False,
        "evidence_note": ("evaluated independently on its OWN clean shadow outcomes; legacy "
                          "stocks swing/invest evidence is NOT valid here"),
        "message": msg,
        "verdict": verdict,
    }


def render_readiness(db_path: str | Path | None = None, cfg: dict[str, Any] | None = None) -> str:
    """Compact Markdown for the readiness command. Shadow-only; changes nothing."""
    r = readiness_summary(db_path, cfg)
    lines = ["## Stocks Position Framework — shadow readiness (NOT live / NOT actionable)"]
    lines.append(f"- Mode: shadow_only={r['shadow_only']} · write_proposed_signals="
                 f"{r['write_proposed_signals']} · scheduler_enabled={r['scheduler_enabled']}")
    if not r["has_evidence"]:
        lines.append(f"- **{r['message']}**")
        return "\n".join(lines)
    o = r["outcomes"]
    g = r["evidence_gate"]
    lines.append(f"- Latest scan: {r['latest_scan_time']} · candidates {r['candidates_count']}")
    lines.append(f"- Outcomes: closed {o['closed']} · pending {o['pending']} · no_entry {o['no_entry']} "
                 f"· net USD (closed) {r['net_usd_closed']}")
    lines.append(f"- Evidence gate: {g['closed_sample']}/{g['min_forward_trades']} closed "
                 f"(≥{g['min_forward_days']}d) → sample_meets_gate={g['sample_meets_gate']}")
    lines.append(f"- Verdict: **{r['verdict']}** — {r['message']}")
    return "\n".join(lines)
