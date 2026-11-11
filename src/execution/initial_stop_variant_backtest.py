from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from src.config import load_config
from src.execution.paper_shadow_engine import _load_candles, _walk
from src.execution.stop_contract import (
    backfill_signal_initial_stop_plans,
    entry_anchor,
    stop_contract_label,
)
from src.storage.file_store import FileStore


TABLE = "initial_stop_variant_backtest"
VARIANTS = ("current", "wider_125", "structural_candidate")


def _f(value: Any, default: float | None = None) -> float | None:
    try:
        return default if value in (None, "") else float(value)
    except (TypeError, ValueError):
        return default


def _loads(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    try:
        parsed = json.loads(value or "{}")
        return parsed if isinstance(parsed, dict) else {}
    except Exception:
        return {}


def ensure_table(conn: sqlite3.Connection) -> None:
    conn.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {TABLE} (
            signal_id TEXT NOT NULL,
            variant_id TEXT NOT NULL,
            symbol TEXT,
            asset_class TEXT,
            mode TEXT,
            entry_mode TEXT,
            direction TEXT,
            stop_price REAL,
            stop_source TEXT,
            stop_label TEXT,
            risk_factor REAL,
            tp1 REAL,
            tp2 REAL,
            tp3 REAL,
            entered INTEGER,
            entry_price REAL,
            entry_time TEXT,
            close_reason TEXT,
            outcome_status TEXT,
            gross_r REAL,
            mfe_r REAL,
            mae_r REAL,
            bars_used INTEGER,
            computed_at TEXT NOT NULL,
            notes TEXT,
            PRIMARY KEY(signal_id, variant_id)
        )
        """
    )
    conn.execute(
        f"CREATE INDEX IF NOT EXISTS idx_{TABLE}_mode "
        f"ON {TABLE}(asset_class, mode, entry_mode, variant_id)"
    )


def _entry_mode(row: dict[str, Any], raw: dict[str, Any]) -> str:
    explicit = (
        row.get("paper_execution_entry_mode")
        or raw.get("paper_execution_entry_mode")
        or raw.get("cqo_entry_mode")
        or raw.get("paper_source_entry_mode")
    )
    text = str(explicit or "").upper().strip()
    if text:
        return text
    setup_type = str(row.get("setup_type") or "").lower()
    if "break" in setup_type or "continuation" in setup_type:
        return "BREAKOUT_CONTINUATION"
    return "PULLBACK_LIMIT"


def _target_r_multipliers(direction: str, entry: float, stop: float,
                          targets: tuple[float | None, float | None, float | None]) -> list[float] | None:
    risk = abs(entry - stop)
    if risk <= 0 or any(target is None for target in targets):
        return None
    if direction == "long":
        values = [(float(target) - entry) / risk for target in targets]
    else:
        values = [(entry - float(target)) / risk for target in targets]
    if any(value <= 0 for value in values):
        return None
    return values


def _reprice_targets(direction: str, entry: float, stop: float,
                     multipliers: list[float]) -> tuple[float, float, float]:
    risk = abs(entry - stop)
    if direction == "long":
        return tuple(entry + risk * value for value in multipliers)  # type: ignore[return-value]
    return tuple(entry - risk * value for value in multipliers)  # type: ignore[return-value]


def _variant_stops(row: dict[str, Any], raw: dict[str, Any],
                   entry: float, current_stop: float) -> dict[str, tuple[float, str, str]]:
    direction = str(row.get("direction") or "").lower()
    risk = abs(entry - current_stop)
    if risk <= 0:
        return {}
    out = {
        "current": (
            current_stop,
            str(row.get("stop_source") or "current"),
            str(row.get("stop_label") or row.get("stop_source") or "current stop"),
        )
    }
    out["wider_125"] = (
        entry - 1.25 * risk if direction == "long" else entry + 1.25 * risk,
        "wider_125",
        "1.25x current risk stop",
    )
    candidate = raw.get("candidate_structural_stop_contract") or {}
    if isinstance(candidate, dict):
        structural_stop = _f(candidate.get("stop_price"))
        if structural_stop is not None:
            valid = (
                structural_stop < entry
                if direction == "long" else structural_stop > entry
            )
            if valid:
                out["structural_candidate"] = (
                    structural_stop,
                    str(candidate.get("stop_source") or "structural_candidate"),
                    stop_contract_label(candidate),
                )
    return out


def _load_rows(conn: sqlite3.Connection, *, days: int, limit: int) -> list[dict[str, Any]]:
    since = (datetime.now(timezone.utc) - timedelta(days=max(1, int(days)))).isoformat()
    return [
        dict(row) for row in conn.execute(
            """
            SELECT p.signal_id, p.symbol, p.asset_class, p.mode, p.direction,
                   p.created_at, p.expires_at, p.validity_window_hours,
                   p.exchange_focus, p.setup_type, p.entry_low, p.entry_high,
                   p.entry_trigger, p.suggested_entry, p.stop_loss,
                   p.invalidation, p.tp1, p.tp2, p.tp3, p.raw_idea_json,
                   s.stop_source, s.contract_json,
                   o.entry_at, o.entry_price_used, o.paper_execution_entry_mode,
                   o.paper_execution_r, o.close_reason, o.evidence_class
            FROM paper_execution_outcomes o
            JOIN proposed_signals p ON p.signal_id = o.signal_id
            LEFT JOIN signal_initial_stop_plan s ON s.signal_id = p.signal_id
            WHERE p.created_at >= ?
              AND o.paper_execution_r IS NOT NULL
              AND o.entry_price_used IS NOT NULL
              AND COALESCE(o.paper_execution_outcome, '') NOT IN ('open', 'no_entry')
            ORDER BY p.created_at DESC
            LIMIT ?
            """,
            (since, int(limit)),
        ).fetchall()
    ]


def run_backtest(*, db: str | Path | None = None, days: int = 14,
                 limit: int = 800, write_report: bool = True) -> dict[str, Any]:
    cfg = load_config()
    path = Path(db or cfg.db_path)
    fs = FileStore(cfg)
    backfill = backfill_signal_initial_stop_plans(path, days=days, limit=max(limit * 3, limit))
    computed_at = datetime.now(timezone.utc).isoformat()
    records: list[dict[str, Any]] = []
    skipped: dict[str, int] = {}

    with sqlite3.connect(path) as conn:
        conn.row_factory = sqlite3.Row
        ensure_table(conn)
        rows = _load_rows(conn, days=days, limit=limit)
        for row in rows:
            raw = _loads(row.get("raw_idea_json"))
            signal_id = str(row.get("signal_id") or "")
            direction = str(row.get("direction") or "").lower()
            if direction not in {"long", "short"}:
                skipped["direction"] = skipped.get("direction", 0) + 1
                continue
            entry = entry_anchor(
                direction,
                row.get("entry_low"),
                row.get("entry_high"),
                row.get("entry_trigger") or row.get("suggested_entry") or row.get("entry_price_used"),
            )
            current_stop = _f(row.get("stop_loss") or row.get("invalidation"))
            targets = (_f(row.get("tp1")), _f(row.get("tp2")), _f(row.get("tp3")))
            if entry is None or current_stop is None:
                skipped["missing_geometry"] = skipped.get("missing_geometry", 0) + 1
                continue
            multipliers = _target_r_multipliers(direction, entry, current_stop, targets)
            if multipliers is None:
                skipped["invalid_targets"] = skipped.get("invalid_targets", 0) + 1
                continue
            candles, _tf = _load_candles(
                fs,
                cfg,
                row.get("symbol"),
                row.get("mode"),
                row.get("asset_class"),
                row.get("exchange_focus") or "",
                row.get("created_at"),
            )
            if candles is None or getattr(candles, "empty", True):
                skipped["no_candles"] = skipped.get("no_candles", 0) + 1
                continue
            entry_mode = _entry_mode(row, raw)
            variants = _variant_stops(row, raw, entry, current_stop)
            for variant_id, (stop_price, stop_source, stop_label) in variants.items():
                variant_targets = (
                    targets if variant_id == "current"
                    else _reprice_targets(direction, entry, stop_price, multipliers)
                )
                if any(value is None for value in variant_targets):
                    continue
                walk = _walk(
                    direction=direction,
                    entry_mode=entry_mode,
                    entry_low=_f(row.get("entry_low")),
                    entry_high=_f(row.get("entry_high")),
                    entry_trigger=_f(row.get("entry_trigger")),
                    suggested=_f(row.get("suggested_entry")),
                    tp1=float(variant_targets[0]),
                    tp2=float(variant_targets[1]),
                    tp3=float(variant_targets[2]),
                    stop0=float(stop_price),
                    stop_after_tp1=None,
                    stop_after_tp2=None,
                    candles=candles,
                    entry_deadline=None,
                )
                risk_factor = abs(entry - float(stop_price)) / max(abs(entry - current_stop), 1e-12)
                rec = {
                    "signal_id": signal_id,
                    "variant_id": variant_id,
                    "symbol": row.get("symbol"),
                    "asset_class": row.get("asset_class"),
                    "mode": row.get("mode"),
                    "entry_mode": entry_mode,
                    "direction": direction,
                    "stop_price": float(stop_price),
                    "stop_source": stop_source,
                    "stop_label": stop_label,
                    "risk_factor": round(risk_factor, 6),
                    "tp1": float(variant_targets[0]),
                    "tp2": float(variant_targets[1]),
                    "tp3": float(variant_targets[2]),
                    "entered": 1 if walk.entered else 0,
                    "entry_price": walk.entry_px,
                    "entry_time": walk.entry_ts,
                    "close_reason": walk.close_reason,
                    "outcome_status": walk.outcome,
                    "gross_r": round(walk.realized_r, 4),
                    "mfe_r": round(walk.mfe_r, 4),
                    "mae_r": round(walk.mae_r, 4),
                    "bars_used": len(candles),
                    "computed_at": computed_at,
                    "notes": "research_only_no_live_no_paper_mutation",
                }
                records.append(rec)
                cols = list(rec.keys())
                conn.execute(
                    f"INSERT OR REPLACE INTO {TABLE} ({','.join(cols)}) "
                    f"VALUES ({','.join('?' for _ in cols)})",
                    [rec[col] for col in cols],
                )
        conn.commit()
        summary_rows = conn.execute(
            f"""
            SELECT asset_class, mode, entry_mode, variant_id,
                   COUNT(*) AS n,
                   SUM(CASE WHEN entered=1 THEN 1 ELSE 0 END) AS entries,
                   SUM(gross_r) AS total_r,
                   AVG(gross_r) AS avg_r,
                   SUM(CASE WHEN gross_r > 0 THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS win_rate,
                   SUM(CASE WHEN close_reason IN ('stopped_full', 'stop') THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS stop_rate,
                   SUM(CASE WHEN gross_r > 0 THEN gross_r ELSE 0 END) AS pos_r,
                   ABS(SUM(CASE WHEN gross_r < 0 THEN gross_r ELSE 0 END)) AS neg_r
            FROM {TABLE}
            WHERE computed_at = ?
            GROUP BY asset_class, mode, entry_mode, variant_id
            ORDER BY asset_class, mode, entry_mode, variant_id
            """,
            (computed_at,),
        ).fetchall()

    summaries = []
    for row in summary_rows:
        d = dict(row)
        neg = _f(d.get("neg_r"), 0.0) or 0.0
        pos = _f(d.get("pos_r"), 0.0) or 0.0
        d["profit_factor"] = None if neg <= 0 else round(pos / neg, 4)
        summaries.append(d)
    report_path = None
    if write_report:
        report_path = _write_report(path, days, computed_at, summaries, backfill, skipped)
    return {
        "db_path": str(path),
        "days": int(days),
        "limit": int(limit),
        "computed_at": computed_at,
        "records": len(records),
        "skipped": skipped,
        "backfill": backfill,
        "summaries": summaries,
        "report_path": str(report_path) if report_path else None,
    }


def _fmt(value: Any, digits: int = 2) -> str:
    number = _f(value)
    if number is None:
        return ""
    return f"{number:.{digits}f}"


def _write_report(path: Path, days: int, computed_at: str, summaries: list[dict[str, Any]],
                  backfill: dict[str, Any], skipped: dict[str, int]) -> Path:
    report_dir = Path("reports")
    report_dir.mkdir(parents=True, exist_ok=True)
    out = report_dir / "INITIAL_STOP_VARIANT_BACKTEST_latest.md"
    lines = [
        "# Initial Stop Variant Backtest",
        "",
        f"- DB: `{path}`",
        f"- Window: last {int(days)} days",
        f"- Computed at: `{computed_at}`",
        "- Scope: research-only; no paper/live trades changed.",
        "- Method: same signal entry rules and R ladder; variants alter only initial stop distance.",
        "",
        "## Backfill",
        "",
        f"- Processed stop contracts: {backfill.get('processed', 0)}",
        f"- By source: `{json.dumps(backfill.get('by_stop_source') or {}, ensure_ascii=False)}`",
        f"- Skipped: `{json.dumps(skipped, ensure_ascii=False)}`",
        "",
        "## Summary",
        "",
    ]
    if summaries:
        lines += [
            "| Asset | Mode | Entry mode | Variant | N | Entries | Total R | Avg R | WR | Stop Rate | PF |",
            "|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|",
        ]
        for row in summaries:
            lines.append(
                f"| {row.get('asset_class') or ''} | {row.get('mode') or ''} | "
                f"{row.get('entry_mode') or ''} | {row.get('variant_id') or ''} | "
                f"{int(row.get('n') or 0)} | {int(row.get('entries') or 0)} | "
                f"{_fmt(row.get('total_r'))} | {_fmt(row.get('avg_r'), 3)} | "
                f"{_fmt((_f(row.get('win_rate'), 0.0) or 0.0) * 100, 1)}% | "
                f"{_fmt((_f(row.get('stop_rate'), 0.0) or 0.0) * 100, 1)}% | "
                f"{_fmt(row.get('profit_factor'))} |"
            )
    else:
        lines.append("No rows were eligible for variant backtest.")
    lines += [
        "",
        "## Decision Rule",
        "",
        "Do not promote a variant just because it improves one small cell. Prefer it only if it improves total R/PF, does not cut entries materially, and lowers stop-rate across the relevant live mode.",
    ]
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out
