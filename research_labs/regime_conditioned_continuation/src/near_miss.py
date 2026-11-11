from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable

import pandas as pd

from .common import ARTIFACT_ROOT, LAB_ROOT, digest, stable_json


NEAR_MISS_DB_PATH = LAB_ROOT / "near_miss.sqlite"
REPORT_PATH = ARTIFACT_ROOT / "CRYPTO_INVEST_NEAR_MISS_REPORT.md"
HORIZONS_HOURS = (4, 24, 72)


def _schema() -> str:
    return """
    PRAGMA journal_mode=WAL;
    CREATE TABLE IF NOT EXISTS near_miss_snapshots (
      snapshot_id TEXT PRIMARY KEY,
      strategy_id TEXT NOT NULL,
      profile_hash TEXT NOT NULL,
      frozen_run_id TEXT,
      candidate_id TEXT NOT NULL,
      symbol TEXT NOT NULL,
      direction TEXT NOT NULL,
      formed_at TEXT,
      decision_at TEXT NOT NULL,
      observed_at TEXT NOT NULL,
      stage_reached TEXT NOT NULL,
      failed_stage TEXT NOT NULL,
      rejection_reason TEXT NOT NULL,
      source_status TEXT NOT NULL,
      is_clean INTEGER NOT NULL,
      reference_at TEXT,
      reference_price REAL,
      reference_source TEXT,
      risk_unit_price REAL,
      risk_unit_source TEXT,
      targets_r_json TEXT NOT NULL,
      features_json TEXT NOT NULL,
      geometry_json TEXT NOT NULL,
      source_times_json TEXT NOT NULL,
      created_at TEXT NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_near_miss_snapshots_decision
      ON near_miss_snapshots(decision_at, failed_stage, rejection_reason, symbol);
    CREATE TABLE IF NOT EXISTS near_miss_outcomes (
      snapshot_id TEXT NOT NULL,
      horizon_hours INTEGER NOT NULL,
      outcome_status TEXT NOT NULL,
      first_event TEXT,
      first_event_at TEXT,
      final_price REAL,
      directional_return_r REAL,
      mfe_r REAL,
      mae_r REAL,
      official_metrics_excluded INTEGER NOT NULL,
      evaluated_at TEXT NOT NULL,
      PRIMARY KEY(snapshot_id, horizon_hours),
      FOREIGN KEY(snapshot_id) REFERENCES near_miss_snapshots(snapshot_id)
    );
    CREATE INDEX IF NOT EXISTS idx_near_miss_outcomes_status
      ON near_miss_outcomes(horizon_hours, outcome_status);
    """


def connect(db: str | Path | None = None) -> sqlite3.Connection:
    path = Path(db) if db is not None else NEAR_MISS_DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.executescript(_schema())
    return conn


def _json(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    try:
        decoded = json.loads(str(value or "{}"))
    except (TypeError, ValueError):
        return {}
    return decoded if isinstance(decoded, dict) else {}


def _float(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if pd.notna(number) and number > 0 else None


def _stage(reason: str) -> tuple[str, str]:
    """Return the last passed stage and the first stage that blocked entry."""
    if reason.startswith("FVG_"):
        return "TREND_CONTEXT", "FVG_QUALITY"
    if reason == "NO_FIRST_RETEST_BEFORE_EXPIRY":
        return "FVG_QUALITY", "FIRST_RETEST"
    if reason == "FVG_INVALIDATED_ON_FIRST_RETEST":
        return "FIRST_RETEST", "FVG_VALIDITY"
    if reason.startswith("BTC_") or reason.startswith("REGIME_CONTEXT"):
        return "VALID_FVG_RETEST", "BTC_REGIME"
    if reason == "RELATIVE_STRENGTH_BELOW":
        return "BTC_REGIME", "RELATIVE_STRENGTH"
    if reason.startswith("VOLATILITY_"):
        return "RELATIVE_STRENGTH", "VOLATILITY"
    if reason == "DERIVATIVES_CROWDING_VETO":
        return "REGIME_CONTEXT", "DERIVATIVES"
    if reason == "RSI_RESET_NOT_CONFIRMED":
        return "REGIME_AND_DERIVATIVES", "RSI_RESET"
    if reason in {"ENTRY_TIMEFRAME_UNAVAILABLE", "NO_CLOSED_RECLAIM_CONFIRMATION"}:
        return "RSI_RESET", "LOWER_TF_RECLAIM"
    if reason in {"ENTRY_DELAY_PATH_UNAVAILABLE", "ENTRY_CHASE_EXTENSION"}:
        return "LOWER_TF_RECLAIM", "ENTRY_GEOMETRY"
    if reason == "STOP_GEOMETRY_OUT_OF_BOUNDS":
        return "ENTRY_GEOMETRY", "STOP_GEOMETRY"
    if reason in {"DIRTY_OR_MISSING_EXECUTION_PATH", "FORWARD_EXECUTION_OR_LATENCY_DIRTY"}:
        return "EXECUTION_READY", "DATA_QUALITY"
    if reason == "SCHEDULER_LATE_DECISION":
        return "EXECUTION_READY", "LATENCY"
    if reason == "SYMBOL_POSITION_ALREADY_OPEN":
        return "EXECUTION_READY", "SYMBOL_EXPOSURE"
    return "CANDIDATE", "UNCLASSIFIED"


def _snapshot_row(row: dict[str, Any], *, frozen_run_id: str | None) -> dict[str, Any] | None:
    status = str(row.get("status") or "")
    reason = str(row.get("rejection_reason") or "")
    if status == "ELIGIBLE_FORWARD_ENTRY" or not reason:
        return None

    features = _json(row.get("features_json"))
    geometry = _json(row.get("geometry_json"))
    source_times = _json(row.get("source_times_json"))
    reference = features.get("near_miss_reference")
    reference = reference if isinstance(reference, dict) else {}
    zone = features.get("zone")
    zone = zone if isinstance(zone, dict) else {}
    targets_r = reference.get("targets_r")
    if not isinstance(targets_r, list) or not targets_r:
        targets_r = []

    reference_price = _float(reference.get("price"))
    risk_unit = _float(reference.get("risk_unit_price"))
    if risk_unit is None:
        risk_unit = _float(zone.get("atr"))
    stage_reached, failed_stage = _stage(reason)
    decision_at = str(row.get("decision_at") or row.get("observed_at") or row.get("created_at") or "")
    key = {
        "strategy_id": row.get("strategy_id"),
        "profile_hash": row.get("profile_hash"),
        "candidate_id": row.get("candidate_id") or row.get("decision_id"),
        "decision_at": decision_at,
        "reason": reason,
    }
    return {
        "snapshot_id": digest(key)[:32],
        "strategy_id": str(row.get("strategy_id") or "unknown"),
        "profile_hash": str(row.get("profile_hash") or "unknown"),
        "frozen_run_id": frozen_run_id,
        "candidate_id": str(row.get("candidate_id") or row.get("decision_id") or "unknown"),
        "symbol": str(row.get("symbol") or "unknown"),
        "direction": str(row.get("direction") or "unknown"),
        "formed_at": row.get("formed_at"),
        "decision_at": decision_at,
        "observed_at": str(row.get("observed_at") or decision_at),
        "stage_reached": stage_reached,
        "failed_stage": failed_stage,
        "rejection_reason": reason,
        "source_status": status,
        "is_clean": int(bool(row.get("is_clean"))),
        "reference_at": reference.get("at"),
        "reference_price": reference_price,
        "reference_source": reference.get("source"),
        "risk_unit_price": risk_unit,
        "risk_unit_source": reference.get("risk_unit_source") or ("zone_atr_proxy" if risk_unit else None),
        "targets_r_json": stable_json(targets_r),
        "features_json": stable_json(features),
        "geometry_json": stable_json(geometry),
        "source_times_json": stable_json(source_times),
        "created_at": str(row.get("created_at") or row.get("observed_at") or decision_at),
    }


def record_decisions(
    rows: Iterable[dict[str, Any]], *, frozen_run_id: str | None = None,
    db: str | Path | None = None,
) -> dict[str, int]:
    """Persist rejected forward candidates without altering the strategy ledger."""
    snapshots = [snapshot for row in rows if (snapshot := _snapshot_row(row, frozen_run_id=frozen_run_id))]
    if not snapshots:
        return {"seen": 0, "inserted": 0, "duplicate": 0}
    columns = list(snapshots[0])
    with connect(db) as conn:
        before = conn.total_changes
        conn.executemany(
            f"INSERT OR IGNORE INTO near_miss_snapshots ({','.join(columns)}) "
            f"VALUES ({','.join('?' for _ in columns)})",
            [[row[column] for column in columns] for row in snapshots],
        )
        inserted = conn.total_changes - before
    return {"seen": len(snapshots), "inserted": inserted, "duplicate": len(snapshots) - inserted}


def _as_timestamp(value: Any) -> pd.Timestamp | None:
    parsed = pd.to_datetime(value, utc=True, errors="coerce")
    return None if pd.isna(parsed) else pd.Timestamp(parsed)


def _targets(value: Any) -> list[float]:
    try:
        items = json.loads(str(value or "[]"))
    except (TypeError, ValueError):
        return []
    return [float(item) for item in items if _float(item) is not None]


def _path_metrics(
    row: dict[str, Any], bars: pd.DataFrame, *, horizon_hours: int,
) -> dict[str, Any]:
    reference = _float(row.get("reference_price"))
    unit = _float(row.get("risk_unit_price"))
    direction = str(row.get("direction"))
    if reference is None or unit is None or direction not in {"long", "short"}:
        return {"outcome_status": "NO_PROXY_GEOMETRY"}
    if bars.empty:
        return {"outcome_status": "DATA_UNAVAILABLE"}

    reference_at = _as_timestamp(row.get("reference_at"))
    if reference_at is None:
        return {"outcome_status": "NO_PROXY_GEOMETRY"}
    horizon_at = reference_at + pd.Timedelta(hours=horizon_hours)
    part = bars.copy()
    part["bar_open_at"] = pd.to_datetime(part["bar_open_at"], utc=True)
    part["bar_close_at"] = pd.to_datetime(part.get("bar_close_at", part["bar_open_at"]), utc=True)
    part = part[(part["bar_open_at"] > reference_at) & (part["bar_close_at"] <= horizon_at)]
    if part.empty or pd.to_datetime(part.iloc[-1]["bar_close_at"], utc=True) < horizon_at - pd.Timedelta(minutes=16):
        return {"outcome_status": "DATA_UNAVAILABLE"}

    long = direction == "long"
    target_r = _targets(row.get("targets_r_json"))
    target_r = target_r[0] if target_r else 1.0
    stop = reference - unit if long else reference + unit
    target = reference + target_r * unit if long else reference - target_r * unit
    first_event = None
    first_event_at = None
    mfe = 0.0
    mae = 0.0
    for _, bar in part.sort_values("bar_open_at").iterrows():
        high, low = float(bar["high"]), float(bar["low"])
        favorable = (high - reference) / unit if long else (reference - low) / unit
        adverse = (reference - low) / unit if long else (high - reference) / unit
        mfe = max(mfe, favorable)
        mae = min(mae, -adverse)
        stop_hit = low <= stop if long else high >= stop
        target_hit = high >= target if long else low <= target
        if first_event is None and (stop_hit or target_hit):
            first_event_at = pd.to_datetime(bar["bar_close_at"], utc=True).isoformat()
            if stop_hit and target_hit:
                first_event = "AMBIGUOUS_STOP_AND_TP1_SAME_BAR"
            elif stop_hit:
                first_event = "STOP_BEFORE_TP1"
            else:
                first_event = "TP1_BEFORE_STOP"
    final_price = float(part.iloc[-1]["close"])
    directional_return = (final_price - reference) / unit if long else (reference - final_price) / unit
    return {
        "outcome_status": "RESOLVED",
        "first_event": first_event or "NO_1R_EVENT",
        "first_event_at": first_event_at,
        "final_price": final_price,
        "directional_return_r": round(directional_return, 6),
        "mfe_r": round(mfe, 6),
        "mae_r": round(mae, 6),
    }


def refresh_outcomes(
    fetch_bars: Callable[[str, datetime], pd.DataFrame], *, now: datetime | None = None,
    db: str | Path | None = None,
) -> dict[str, int]:
    """Update diagnostic paths only; values are explicitly excluded from official PnL."""
    observed = now or datetime.now(timezone.utc)
    with connect(db) as conn:
        snapshots = [dict(row) for row in conn.execute(
            "SELECT * FROM near_miss_snapshots WHERE reference_price IS NOT NULL "
            "AND reference_at IS NOT NULL AND risk_unit_price IS NOT NULL "
            "AND (SELECT COUNT(*) FROM near_miss_outcomes o "
            "     WHERE o.snapshot_id=near_miss_snapshots.snapshot_id "
            "       AND o.outcome_status='RESOLVED') < 3"
        ).fetchall()]
    cached: dict[str, pd.DataFrame] = {}
    writes: list[dict[str, Any]] = []
    for snapshot in snapshots:
        reference_at = _as_timestamp(snapshot["reference_at"])
        if reference_at is None:
            continue
        try:
            bars = cached.setdefault(snapshot["symbol"], fetch_bars(snapshot["symbol"], observed))
        except Exception:
            bars = pd.DataFrame()
        for horizon in HORIZONS_HOURS:
            horizon_at = reference_at + pd.Timedelta(hours=horizon)
            if pd.Timestamp(observed) < horizon_at:
                result: dict[str, Any] = {"outcome_status": "PENDING"}
            else:
                result = _path_metrics(snapshot, bars, horizon_hours=horizon)
            writes.append({
                "snapshot_id": snapshot["snapshot_id"], "horizon_hours": horizon,
                "outcome_status": result["outcome_status"],
                "first_event": result.get("first_event"),
                "first_event_at": result.get("first_event_at"),
                "final_price": result.get("final_price"),
                "directional_return_r": result.get("directional_return_r"),
                "mfe_r": result.get("mfe_r"), "mae_r": result.get("mae_r"),
                "official_metrics_excluded": 1,
                "evaluated_at": observed.isoformat(),
            })
    if not writes:
        return {"snapshots": len(snapshots), "updated": 0}
    columns = list(writes[0])
    assignments = ",".join(f"{column}=excluded.{column}" for column in columns if column not in {"snapshot_id", "horizon_hours"})
    with connect(db) as conn:
        conn.executemany(
            f"INSERT INTO near_miss_outcomes ({','.join(columns)}) VALUES ({','.join('?' for _ in columns)}) "
            f"ON CONFLICT(snapshot_id,horizon_hours) DO UPDATE SET {assignments}",
            [[row[column] for column in columns] for row in writes],
        )
    return {"snapshots": len(snapshots), "updated": len(writes)}


def report(*, db: str | Path | None = None) -> dict[str, Any]:
    with connect(db) as conn:
        total = int(conn.execute("SELECT COUNT(*) FROM near_miss_snapshots").fetchone()[0])
        stages = [dict(row) for row in conn.execute(
            "SELECT failed_stage, rejection_reason, COUNT(*) AS n "
            "FROM near_miss_snapshots GROUP BY failed_stage,rejection_reason "
            "ORDER BY n DESC, failed_stage"
        ).fetchall()]
        outcomes = [dict(row) for row in conn.execute(
            "SELECT horizon_hours,outcome_status,first_event,COUNT(*) AS n "
            "FROM near_miss_outcomes GROUP BY horizon_hours,outcome_status,first_event "
            "ORDER BY horizon_hours,outcome_status,n DESC"
        ).fetchall()]
    return {"database": str(Path(db) if db is not None else NEAR_MISS_DB_PATH), "snapshots": total,
            "rejections": stages, "outcomes": outcomes, "official_metrics_excluded": True}


def write_report(*, db: str | Path | None = None, path: str | Path | None = None) -> Path:
    payload = report(db=db)
    target = Path(path) if path is not None else REPORT_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Crypto Invest Near-Miss Monitor",
        "",
        "This is an isolated diagnostic dataset. It never writes Paper, live, or official PnL tables.",
        f"- Database: `{payload['database']}`",
        f"- Recorded near-miss snapshots: {payload['snapshots']}",
        "- All counterfactual outcomes are diagnostic proxies and excluded from official metrics.",
        "",
        "## Rejection Funnel",
        "",
        "| Failed stage | Reason | Count |",
        "|---|---|---:|",
    ]
    lines.extend(f"| {row['failed_stage']} | {row['rejection_reason']} | {row['n']} |" for row in payload["rejections"])
    lines.extend(["", "## Proxy Outcomes", "", "| Horizon | Status | First event | Count |", "|---:|---|---|---:|"])
    lines.extend(
        f"| {row['horizon_hours']}h | {row['outcome_status']} | {row.get('first_event') or '-'} | {row['n']} |"
        for row in payload["outcomes"]
    )
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return target
