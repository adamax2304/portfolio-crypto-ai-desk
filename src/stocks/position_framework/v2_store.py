"""Isolated SQLite storage for Stocks Position Swing V2 shadow evidence."""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .v2_config import ROOT

DEFAULT_DB_PATH = ROOT / "db" / "crypto_ai_desk.sqlite"

CANDIDATE_TABLE = "stocks_position_v2_candidates"
OUTCOME_TABLE = "stocks_position_v2_outcomes"
SCAN_TABLE = "stocks_position_v2_scan_runs"
REVIEW_TABLE = "stocks_position_v2_reviews"

_CANDIDATE_DDL = f"""
CREATE TABLE IF NOT EXISTS {CANDIDATE_TABLE} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_id TEXT UNIQUE NOT NULL,
    created_at TEXT NOT NULL,
    scan_session_date TEXT NOT NULL,
    strategy_id TEXT NOT NULL,
    shadow_lane TEXT NOT NULL,
    profile_version TEXT NOT NULL,
    evidence_window TEXT NOT NULL DEFAULT 'forward_post_activation',
    symbol TEXT NOT NULL,
    asset_class TEXT NOT NULL DEFAULT 'stocks',
    mode TEXT NOT NULL DEFAULT 'swing',
    direction TEXT NOT NULL DEFAULT 'long',
    setup_variant TEXT NOT NULL,
    score REAL,
    market_regime TEXT,
    sector TEXT,
    sector_etf TEXT,
    entry_price REAL,
    entry_low REAL,
    entry_high REAL,
    trigger_level REAL,
    confirmation_date TEXT,
    reclaim_level TEXT,
    stop_price REAL,
    structural_low REAL,
    risk_per_share REAL,
    risk_atr REAL,
    stop_distance_pct REAL,
    risk_usd REAL,
    size_weight REAL,
    qty REAL,
    tp1 REAL,
    tp1_r REAL,
    tp1_pct REAL,
    tp2 REAL,
    tp2_r REAL,
    tp2_pct REAL,
    max_holding_days INTEGER,
    rs_spy REAL,
    rs_sector REAL,
    volume_ratio REAL,
    setup_volume_ratio REAL,
    atr14 REAL,
    dollar_volume_30d REAL,
    near_high_pct REAL,
    earnings_days INTEGER,
    event_types_json TEXT,
    data_clean INTEGER NOT NULL DEFAULT 1,
    coverage_status TEXT NOT NULL DEFAULT 'CLEAN_AT_SCAN',
    thesis TEXT,
    counter_thesis TEXT,
    decision_json TEXT,
    status TEXT NOT NULL DEFAULT 'shadow_open'
);
"""

_OUTCOME_DDL = f"""
CREATE TABLE IF NOT EXISTS {OUTCOME_TABLE} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_id TEXT UNIQUE NOT NULL,
    checked_at TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    entry_date TEXT,
    exit_date TEXT,
    entry_px REAL,
    exit_px REAL,
    close_reason TEXT,
    qty REAL,
    notional_usd REAL,
    gross_pnl_usd REAL,
    fees_usd REAL,
    slippage_usd REAL,
    funding_usd REAL NOT NULL DEFAULT 0,
    net_pnl_usd REAL,
    net_pct REAL,
    max_favorable_excursion_r REAL,
    max_adverse_excursion_r REAL,
    holding_days INTEGER,
    gap_loss_r REAL,
    data_clean INTEGER NOT NULL DEFAULT 1,
    coverage_status TEXT NOT NULL DEFAULT 'CLEAN',
    same_bar_ambiguous INTEGER NOT NULL DEFAULT 0,
    notes_json TEXT
);
"""

_SCAN_DDL = f"""
CREATE TABLE IF NOT EXISTS {SCAN_TABLE} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL,
    strategy_id TEXT NOT NULL,
    profile_version TEXT NOT NULL,
    universe_size INTEGER NOT NULL DEFAULT 0,
    scanned INTEGER NOT NULL DEFAULT 0,
    candidate_count INTEGER NOT NULL DEFAULT 0,
    rejected_count INTEGER NOT NULL DEFAULT 0,
    persisted INTEGER NOT NULL DEFAULT 0,
    market_regime TEXT,
    rejection_counts_json TEXT,
    data_notes_json TEXT,
    dry_run INTEGER NOT NULL DEFAULT 0
);
"""

_REVIEW_DDL = f"""
CREATE TABLE IF NOT EXISTS {REVIEW_TABLE} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_id TEXT NOT NULL,
    review_cycle TEXT NOT NULL,
    created_at TEXT NOT NULL,
    verdict TEXT NOT NULL,
    confidence REAL,
    reasons_json TEXT NOT NULL DEFAULT '[]',
    key_news_json TEXT NOT NULL DEFAULT '[]',
    risk_notes_json TEXT NOT NULL DEFAULT '[]',
    source_report_path TEXT,
    raw_json TEXT NOT NULL,
    UNIQUE(candidate_id, review_cycle)
);
"""

_CANDIDATE_COLS = (
    "candidate_id", "created_at", "scan_session_date", "strategy_id", "shadow_lane",
    "profile_version", "evidence_window", "symbol", "asset_class", "mode", "direction",
    "setup_variant", "score", "market_regime", "sector", "sector_etf", "entry_price",
    "entry_low", "entry_high", "trigger_level", "confirmation_date", "reclaim_level",
    "stop_price", "structural_low", "risk_per_share", "risk_atr", "stop_distance_pct",
    "risk_usd", "size_weight", "qty", "tp1", "tp1_r", "tp1_pct", "tp2", "tp2_r",
    "tp2_pct", "max_holding_days", "rs_spy", "rs_sector", "volume_ratio",
    "setup_volume_ratio", "atr14", "dollar_volume_30d", "near_high_pct", "earnings_days",
    "event_types_json", "data_clean", "coverage_status", "thesis", "counter_thesis",
    "decision_json", "status",
)

_OUTCOME_COLS = (
    "candidate_id", "checked_at", "status", "entry_date", "exit_date", "entry_px",
    "exit_px", "close_reason", "qty", "notional_usd", "gross_pnl_usd", "fees_usd",
    "slippage_usd", "funding_usd", "net_pnl_usd", "net_pct",
    "max_favorable_excursion_r", "max_adverse_excursion_r", "holding_days",
    "gap_loss_r", "data_clean", "coverage_status", "same_bar_ambiguous", "notes_json",
)


def connect(db_path: str | Path | None = None) -> sqlite3.Connection:
    path = Path(db_path) if db_path else DEFAULT_DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path), timeout=30)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_tables(db_path: str | Path | None = None) -> None:
    conn = connect(db_path)
    try:
        conn.execute(_CANDIDATE_DDL)
        conn.execute(_OUTCOME_DDL)
        conn.execute(_SCAN_DDL)
        conn.execute(_REVIEW_DDL)
        conn.execute(
            f"CREATE INDEX IF NOT EXISTS idx_spv2_open "
            f"ON {CANDIDATE_TABLE}(status,created_at)"
        )
        conn.execute(
            f"CREATE INDEX IF NOT EXISTS idx_spv2_symbol "
            f"ON {CANDIDATE_TABLE}(symbol,setup_variant)"
        )
        conn.execute(
            f"CREATE INDEX IF NOT EXISTS idx_spv2_outcome_status "
            f"ON {OUTCOME_TABLE}(status,data_clean)"
        )
        conn.execute(
            f"CREATE INDEX IF NOT EXISTS idx_spv2_review_candidate "
            f"ON {REVIEW_TABLE}(candidate_id,created_at)"
        )
        conn.commit()
    finally:
        conn.close()


def _candidate_id(candidate: dict[str, Any], created_at: str) -> str:
    day = str(candidate.get("confirmation_date") or created_at)[:10]
    setup = str(candidate.get("setup_variant") or "UNKNOWN").lower()
    return f"spv2_{candidate.get('symbol')}_{day}_{setup}"


def flatten(candidate: dict[str, Any], created_at: str) -> dict[str, Any]:
    plan = candidate.get("risk_plan") or {}
    decision = {
        "rejection_reasons": candidate.get("rejection_reasons") or [],
        "warnings": candidate.get("warnings") or [],
        "profile_version": candidate.get("profile_version"),
    }
    return {
        "candidate_id": _candidate_id(candidate, created_at),
        "created_at": created_at,
        "scan_session_date": str(candidate.get("confirmation_date") or created_at)[:10],
        "strategy_id": candidate.get("strategy_id"),
        "shadow_lane": candidate.get("shadow_lane"),
        "profile_version": candidate.get("profile_version"),
        "evidence_window": "forward_post_activation",
        "symbol": candidate.get("symbol"),
        "asset_class": "stocks",
        "mode": "swing",
        "direction": "long",
        "setup_variant": candidate.get("setup_variant"),
        "score": candidate.get("score"),
        "market_regime": candidate.get("market_regime"),
        "sector": candidate.get("sector"),
        "sector_etf": candidate.get("sector_etf"),
        "entry_price": candidate.get("entry_price"),
        "entry_low": candidate.get("entry_low"),
        "entry_high": candidate.get("entry_high"),
        "trigger_level": candidate.get("trigger_level"),
        "confirmation_date": candidate.get("confirmation_date"),
        "reclaim_level": candidate.get("reclaim_level"),
        "stop_price": plan.get("stop_price"),
        "structural_low": plan.get("structural_low"),
        "risk_per_share": plan.get("risk_per_share"),
        "risk_atr": plan.get("risk_atr"),
        "stop_distance_pct": plan.get("stop_distance_pct"),
        "risk_usd": plan.get("risk_usd"),
        "size_weight": plan.get("size_weight"),
        "qty": plan.get("qty"),
        "tp1": plan.get("tp1"),
        "tp1_r": plan.get("tp1_r"),
        "tp1_pct": plan.get("tp1_pct"),
        "tp2": plan.get("tp2"),
        "tp2_r": plan.get("tp2_r"),
        "tp2_pct": plan.get("tp2_pct"),
        "max_holding_days": plan.get("max_holding_days"),
        "rs_spy": candidate.get("rs_spy"),
        "rs_sector": candidate.get("rs_sector"),
        "volume_ratio": candidate.get("volume_ratio"),
        "setup_volume_ratio": candidate.get("setup_volume_ratio"),
        "atr14": candidate.get("atr14"),
        "dollar_volume_30d": candidate.get("dollar_volume_30d"),
        "near_high_pct": candidate.get("near_high_pct"),
        "earnings_days": candidate.get("earnings_days"),
        "event_types_json": json.dumps(candidate.get("event_types") or []),
        "data_clean": int(bool(candidate.get("data_clean", True))),
        "coverage_status": "CLEAN_AT_SCAN" if candidate.get("data_clean", True) else "DIRTY_AT_SCAN",
        "thesis": candidate.get("thesis"),
        "counter_thesis": candidate.get("counter_thesis"),
        "decision_json": json.dumps(decision),
        "status": "shadow_open",
    }


def insert_candidates(
    candidates: Iterable[dict[str, Any]],
    *,
    created_at: str,
    db_path: str | Path | None = None,
) -> int:
    ensure_tables(db_path)
    rows = [flatten(c, created_at) for c in candidates if c.get("passed")]
    if not rows:
        return 0
    conn = connect(db_path)
    try:
        accepted: list[dict[str, Any]] = []
        for row in rows:
            duplicate = conn.execute(
                f"SELECT 1 FROM {CANDIDATE_TABLE} c "
                f"LEFT JOIN {OUTCOME_TABLE} o ON o.candidate_id=c.candidate_id "
                "WHERE c.status='shadow_open' AND c.symbol=? AND c.setup_variant=? "
                "AND (o.status IS NULL OR o.status IN ('pending','open')) LIMIT 1",
                (row["symbol"], row["setup_variant"]),
            ).fetchone()
            if not duplicate:
                accepted.append(row)
        if not accepted:
            return 0
        placeholders = ",".join("?" for _ in _CANDIDATE_COLS)
        updates = ",".join(
            f"{col}=excluded.{col}" for col in _CANDIDATE_COLS if col != "candidate_id"
        )
        conn.executemany(
            f"INSERT INTO {CANDIDATE_TABLE} ({','.join(_CANDIDATE_COLS)}) "
            f"VALUES ({placeholders}) ON CONFLICT(candidate_id) DO UPDATE SET {updates}",
            [tuple(row[col] for col in _CANDIDATE_COLS) for row in accepted],
        )
        conn.commit()
        return len(accepted)
    finally:
        conn.close()


def open_candidates(db_path: str | Path | None = None) -> list[dict[str, Any]]:
    ensure_tables(db_path)
    conn = connect(db_path)
    try:
        return [
            dict(row)
            for row in conn.execute(
                f"SELECT c.* FROM {CANDIDATE_TABLE} c "
                f"LEFT JOIN {OUTCOME_TABLE} o ON o.candidate_id=c.candidate_id "
                "WHERE c.status='shadow_open' "
                "AND (o.status IS NULL OR o.status IN ('pending','open')) "
                "ORDER BY c.created_at,c.candidate_id"
            )
        ]
    finally:
        conn.close()


def latest_candidates(
    *,
    limit: int = 100,
    db_path: str | Path | None = None,
) -> list[dict[str, Any]]:
    ensure_tables(db_path)
    conn = connect(db_path)
    try:
        return [
            dict(row)
            for row in conn.execute(
                f"SELECT * FROM {CANDIDATE_TABLE} ORDER BY created_at DESC,score DESC LIMIT ?",
                (int(limit),),
            )
        ]
    finally:
        conn.close()


def upsert_outcome(
    candidate_id: str,
    *,
    checked_at: str,
    status: str,
    fields: dict[str, Any],
    db_path: str | Path | None = None,
) -> None:
    ensure_tables(db_path)
    row = {col: None for col in _OUTCOME_COLS}
    row.update(
        candidate_id=candidate_id,
        checked_at=checked_at,
        status=status,
        funding_usd=0.0,
        data_clean=int(bool(fields.get("data_clean", True))),
        coverage_status=fields.get("coverage_status", "CLEAN"),
        same_bar_ambiguous=int(bool(fields.get("same_bar_ambiguous", False))),
        notes_json=json.dumps(fields.get("notes") or {}),
    )
    for col in _OUTCOME_COLS:
        if col in fields and col not in {
            "candidate_id", "checked_at", "status", "notes_json"
        }:
            row[col] = fields[col]
    conn = connect(db_path)
    try:
        placeholders = ",".join("?" for _ in _OUTCOME_COLS)
        updates = ",".join(
            f"{col}=excluded.{col}" for col in _OUTCOME_COLS if col != "candidate_id"
        )
        conn.execute(
            f"INSERT INTO {OUTCOME_TABLE} ({','.join(_OUTCOME_COLS)}) "
            f"VALUES ({placeholders}) ON CONFLICT(candidate_id) DO UPDATE SET {updates}",
            tuple(row[col] for col in _OUTCOME_COLS),
        )
        if status in {"closed", "no_entry", "invalid"}:
            candidate_status = {
                "closed": "shadow_closed",
                "no_entry": "shadow_no_entry",
                "invalid": "shadow_invalid",
            }[status]
            conn.execute(
                f"UPDATE {CANDIDATE_TABLE} SET status=? WHERE candidate_id=?",
                (candidate_status, candidate_id),
            )
        conn.commit()
    finally:
        conn.close()


def latest_outcomes(
    *,
    limit: int = 100000,
    db_path: str | Path | None = None,
) -> list[dict[str, Any]]:
    ensure_tables(db_path)
    conn = connect(db_path)
    try:
        return [
            dict(row)
            for row in conn.execute(
                f"SELECT o.*,c.symbol,c.setup_variant,c.market_regime,c.sector,c.profile_version "
                f"FROM {OUTCOME_TABLE} o JOIN {CANDIDATE_TABLE} c "
                "ON c.candidate_id=o.candidate_id "
                "ORDER BY o.checked_at DESC LIMIT ?",
                (int(limit),),
            )
        ]
    finally:
        conn.close()


def record_scan(
    *,
    created_at: str,
    cfg: dict[str, Any],
    universe_size: int,
    scanned: int,
    candidate_count: int,
    rejected_count: int,
    persisted: int,
    market_regime: str,
    rejection_counts: dict[str, int],
    data_notes: list[str],
    dry_run: bool,
    db_path: str | Path | None = None,
) -> None:
    if dry_run:
        return
    ensure_tables(db_path)
    conn = connect(db_path)
    try:
        conn.execute(
            f"INSERT INTO {SCAN_TABLE} "
            "(created_at,strategy_id,profile_version,universe_size,scanned,candidate_count,"
            "rejected_count,persisted,market_regime,rejection_counts_json,data_notes_json,dry_run) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                created_at,
                cfg.get("strategy_id"),
                cfg.get("profile_version"),
                universe_size,
                scanned,
                candidate_count,
                rejected_count,
                persisted,
                market_regime,
                json.dumps(rejection_counts, sort_keys=True),
                json.dumps(data_notes),
                int(dry_run),
            ),
        )
        conn.commit()
    finally:
        conn.close()


_REVIEW_VERDICTS = {
    "KEEP_TRACKING",
    "WAIT",
    "REJECT_EVENT_RISK",
    "REJECT_THESIS_BROKEN",
    "NEEDS_DATA",
}


def ingest_reviews(
    reviews: Iterable[dict[str, Any]],
    *,
    review_cycle: str,
    source_report_path: str | None = None,
    db_path: str | Path | None = None,
) -> dict[str, Any]:
    """Persist advisory V2 reviews without mutating candidates or execution."""
    ensure_tables(db_path)
    conn = connect(db_path)
    inserted = 0
    rejected: list[dict[str, str]] = []
    try:
        for review in reviews:
            candidate_id = str(review.get("candidate_id") or "").strip()
            verdict = str(review.get("verdict") or "").strip().upper()
            if not candidate_id or verdict not in _REVIEW_VERDICTS:
                rejected.append({"candidate_id": candidate_id, "reason": "INVALID_REVIEW"})
                continue
            exists = conn.execute(
                f"SELECT 1 FROM {CANDIDATE_TABLE} WHERE candidate_id=?",
                (candidate_id,),
            ).fetchone()
            if not exists:
                rejected.append({"candidate_id": candidate_id, "reason": "UNKNOWN_CANDIDATE"})
                continue
            try:
                confidence = float(review.get("confidence"))
            except (TypeError, ValueError):
                confidence = None
            if confidence is not None:
                confidence = max(0.0, min(1.0, confidence))
            created_at = datetime.now(timezone.utc).isoformat()
            conn.execute(
                f"INSERT INTO {REVIEW_TABLE} "
                "(candidate_id,review_cycle,created_at,verdict,confidence,reasons_json,"
                "key_news_json,risk_notes_json,source_report_path,raw_json) "
                "VALUES (?,?,?,?,?,?,?,?,?,?) "
                "ON CONFLICT(candidate_id,review_cycle) DO UPDATE SET "
                "created_at=excluded.created_at,verdict=excluded.verdict,"
                "confidence=excluded.confidence,reasons_json=excluded.reasons_json,"
                "key_news_json=excluded.key_news_json,risk_notes_json=excluded.risk_notes_json,"
                "source_report_path=excluded.source_report_path,raw_json=excluded.raw_json",
                (
                    candidate_id,
                    review_cycle,
                    created_at,
                    verdict,
                    confidence,
                    json.dumps(review.get("reasons") or []),
                    json.dumps(review.get("key_news") or []),
                    json.dumps(review.get("risk_notes") or []),
                    source_report_path,
                    json.dumps(review, sort_keys=True),
                ),
            )
            inserted += 1
        conn.commit()
    finally:
        conn.close()
    return {"ingested": inserted, "rejected": rejected}


def latest_reviews(
    *, limit: int = 100, db_path: str | Path | None = None
) -> list[dict[str, Any]]:
    ensure_tables(db_path)
    conn = connect(db_path)
    try:
        return [
            dict(row)
            for row in conn.execute(
                f"SELECT * FROM {REVIEW_TABLE} ORDER BY created_at DESC,id DESC LIMIT ?",
                (int(limit),),
            )
        ]
    finally:
        conn.close()


def readiness(
    cfg: dict[str, Any],
    db_path: str | Path | None = None,
) -> dict[str, Any]:
    ensure_tables(db_path)
    conn = connect(db_path)
    try:
        candidate_count = int(
            conn.execute(f"SELECT COUNT(*) FROM {CANDIDATE_TABLE}").fetchone()[0]
        )
        outcomes = [
            dict(row)
            for row in conn.execute(
                f"SELECT o.*,c.setup_variant,c.created_at FROM {OUTCOME_TABLE} o "
                f"JOIN {CANDIDATE_TABLE} c ON c.candidate_id=o.candidate_id"
            )
        ]
        latest_scan = conn.execute(f"SELECT MAX(created_at) FROM {SCAN_TABLE}").fetchone()[0]
    finally:
        conn.close()
    clean_closed = [
        row
        for row in outcomes
        if row.get("status") == "closed"
        and int(row.get("data_clean") or 0) == 1
        and row.get("net_pnl_usd") is not None
    ]
    nets = [float(row["net_pnl_usd"]) for row in clean_closed]
    wins = [value for value in nets if value > 0]
    losses = [value for value in nets if value < 0]
    gross_loss = abs(sum(losses))
    pf = sum(wins) / gross_loss if gross_loss else (float("inf") if wins else None)
    equity = float((cfg.get("risk") or {}).get("paper_equity_usd", 5000))
    running = equity
    peak = equity
    max_drawdown_usd = 0.0
    for row in sorted(
        clean_closed,
        key=lambda item: (str(item.get("exit_date") or ""), str(item.get("candidate_id") or "")),
    ):
        running += float(row["net_pnl_usd"])
        peak = max(peak, running)
        max_drawdown_usd = max(max_drawdown_usd, peak - running)
    max_drawdown_pct = max_drawdown_usd / equity * 100 if equity > 0 else None
    by_setup: dict[str, int] = {}
    for row in clean_closed:
        key = str(row.get("setup_variant") or "unknown")
        by_setup[key] = by_setup.get(key, 0) + 1
    dates = [
        str(row.get("created_at"))[:10]
        for row in outcomes
        if row.get("created_at")
    ]
    forward_days = 0
    if dates:
        try:
            first = datetime.fromisoformat(min(dates)).date()
            forward_days = (datetime.now(timezone.utc).date() - first).days
        except Exception:
            forward_days = 0
    gate = cfg.get("evidence_gate") or {}
    enough_total = len(clean_closed) >= int(gate.get("min_clean_closed_trades", 30))
    enough_setup = all(
        by_setup.get(name, 0) >= int(gate.get("min_clean_closed_per_setup", 10))
        for name in ("BREAKOUT_RETEST", "TREND_PULLBACK_RECLAIM")
    )
    drawdown_ok = (
        not gate.get("require_max_drawdown_acceptable", True)
        or (
            max_drawdown_pct is not None
            and max_drawdown_pct <= float(gate.get("max_drawdown_pct_of_equity", 8))
        )
    )
    gate_passed = bool(
        enough_total
        and enough_setup
        and forward_days >= int(gate.get("min_forward_days", 28))
        and sum(nets) > 0
        and pf is not None
        and pf >= float(gate.get("min_profit_factor", 1.25))
        and drawdown_ok
    )
    return {
        "candidate_count": candidate_count,
        "latest_scan": latest_scan,
        "clean_closed": len(clean_closed),
        "pending": sum(1 for row in outcomes if row.get("status") == "pending"),
        "no_entry": sum(1 for row in outcomes if row.get("status") == "no_entry"),
        "net_pnl_usd": round(sum(nets), 2),
        "profit_factor": None if pf is None else round(pf, 3),
        "winrate": None if not nets else round(len(wins) / len(nets), 4),
        "max_drawdown_usd": round(max_drawdown_usd, 2),
        "max_drawdown_pct": None if max_drawdown_pct is None else round(max_drawdown_pct, 3),
        "drawdown_ok": drawdown_ok,
        "by_setup": by_setup,
        "forward_days": forward_days,
        "gate_passed": gate_passed,
        "verdict": "REVIEW_ONLY" if gate_passed else "INSUFFICIENT_FORWARD_EVIDENCE",
    }
