"""Clean-only evaluation for the active stocks-intraday forward shadow lane.

The generic entry-mode calibration intentionally excludes ``stocks_intraday``:
the live paper candidates have a separate fresh forward lane, while the legacy
stock A/B book is not valid evidence for it. This module closes that visibility
gap without changing how any candidate is scored, routed, alerted, or traded.

It reads ``paper_shadow_execution_outcomes`` and writes only its own additive
read-model table, report, and JSON diagnostic. USD PnL is authoritative; R is
secondary. Backfill and dirty/no-coverage rows are reported but never count as
edge evidence. A positive result is REVIEW_ONLY, never auto-promotion.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.execution.entry_mode_calibration import load_calibration_config

FORWARD = "forward_since_activation"
LANE = "stocks_intraday_forward"
BRANCH = "new_logic_shadow"
STOCK_FEE_PROFILE = "stock_etf_default"

_DDL = """
CREATE TABLE IF NOT EXISTS stocks_intraday_forward_shadow_evaluations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  generated_at TEXT NOT NULL,
  activated_at TEXT,
  entry_mode TEXT NOT NULL,
  forward_rows INTEGER NOT NULL DEFAULT 0,
  clean_rows INTEGER NOT NULL DEFAULT 0,
  dirty_rows INTEGER NOT NULL DEFAULT 0,
  clean_filled INTEGER NOT NULL DEFAULT 0,
  clean_closed INTEGER NOT NULL DEFAULT 0,
  dirty_closed INTEGER NOT NULL DEFAULT 0,
  net_pnl_usd REAL,
  net_r_sum REAL,
  profit_factor REAL,
  winrate REAL,
  max_drawdown_usd REAL,
  fees_usd REAL,
  slippage_usd REAL,
  forward_days REAL,
  verdict TEXT NOT NULL,
  reasons_json TEXT NOT NULL,
  direction_breakdown_json TEXT NOT NULL DEFAULT '{}',
  duplicate_rows_excluded INTEGER NOT NULL DEFAULT 0,
  legacy_evidence_reused INTEGER NOT NULL DEFAULT 0,
  config_json TEXT NOT NULL
);
"""
_INDEX = """CREATE INDEX IF NOT EXISTS idx_sifse_generated_mode
ON stocks_intraday_forward_shadow_evaluations(generated_at, entry_mode);"""
_COLS = (
    "generated_at", "activated_at", "entry_mode", "forward_rows", "clean_rows", "dirty_rows",
    "clean_filled", "clean_closed", "dirty_closed", "net_pnl_usd", "net_r_sum", "profit_factor",
    "winrate", "max_drawdown_usd", "fees_usd", "slippage_usd", "forward_days", "verdict",
    "reasons_json", "direction_breakdown_json", "duplicate_rows_excluded",
    "legacy_evidence_reused", "config_json",
)


def _root() -> Path:
    return Path(__file__).resolve().parents[2]


def _db_path(db: str | None) -> str:
    if db:
        return db
    from src.config import load_config
    return str(load_config().db_path)


def _table_exists(conn: sqlite3.Connection, table: str) -> bool:
    return bool(conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table,)
    ).fetchone())


def _parse_iso(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
    except (TypeError, ValueError):
        return None


def _max_drawdown(values: list[float]) -> float:
    peak = cumulative = drawdown = 0.0
    for value in values:
        cumulative += value
        peak = max(peak, cumulative)
        drawdown = max(drawdown, peak - cumulative)
    return round(drawdown, 4)


def load_evaluator_config() -> dict[str, Any]:
    cfg = load_calibration_config()
    raw = cfg.get("stocks_intraday_forward_evaluator") or {}
    lane = cfg.get("stocks_intraday_forward_shadow") or {}
    return {
        "enabled": bool(raw.get("enabled", True)),
        "shadow_lane": str(raw.get("shadow_lane", LANE)),
        "branch": str(raw.get("branch", BRANCH)),
        "entry_modes": [str(x).upper() for x in raw.get("entry_modes")
                        or lane.get("entry_modes") or ("PULLBACK_LIMIT", "BREAKOUT_CONTINUATION")],
        "fee_profile": str(raw.get("fee_profile", STOCK_FEE_PROFILE)),
        "min_forward_days": int(raw.get("min_forward_days", 28)),
        "min_clean_closed": int(raw.get("min_clean_closed", 30)),
        "min_profit_factor": float(raw.get("min_profit_factor", 1.25)),
        "require_positive_net_usd": bool(raw.get("require_positive_net_usd", True)),
        "activation_meta_key": str(lane.get(
            "activation_meta_key", "stocks_intraday_forward_shadow_activated_at")),
    }


def ensure_tables(conn: sqlite3.Connection) -> None:
    conn.execute(_DDL)
    columns = {row[1] for row in conn.execute("PRAGMA table_info(stocks_intraday_forward_shadow_evaluations)")}
    if "direction_breakdown_json" not in columns:
        conn.execute("ALTER TABLE stocks_intraday_forward_shadow_evaluations "
                     "ADD COLUMN direction_breakdown_json TEXT NOT NULL DEFAULT '{}'")
    if "duplicate_rows_excluded" not in columns:
        conn.execute("ALTER TABLE stocks_intraday_forward_shadow_evaluations "
                     "ADD COLUMN duplicate_rows_excluded INTEGER NOT NULL DEFAULT 0")
    conn.execute(_INDEX)
    conn.commit()


def _activation(conn: sqlite3.Connection, key: str) -> str | None:
    if not _table_exists(conn, "paper_shadow_meta"):
        return None
    row = conn.execute("SELECT v FROM paper_shadow_meta WHERE k=?", (key,)).fetchone()
    return str(row[0]) if row and row[0] else None


def _load_rows(conn: sqlite3.Connection, cfg: dict[str, Any]) -> list[dict[str, Any]]:
    if not _table_exists(conn, "paper_shadow_execution_outcomes"):
        return []
    columns = {r[1] for r in conn.execute("PRAGMA table_info(paper_shadow_execution_outcomes)")}
    required = {"shadow_lane", "is_clean_for_edge", "entry_mode", "window", "branch",
                "asset_class", "entry_fill_status", "net_pnl_usdt", "fee_profile"}
    if not required.issubset(columns):
        return []
    signal_columns = {r[1] for r in conn.execute("PRAGMA table_info(proposed_signals)")} \
        if _table_exists(conn, "proposed_signals") else set()
    select = [
        "s.signal_id", "s.asset_class", "s.entry_mode", "s.entry_fill_status", "s.net_pnl_usdt", "s.net_r",
        "s.fees_usdt", "s.slippage_usdt", "s.entry_fill_time", "s.created_at", "s.is_clean_for_edge",
        "s.fee_profile", "s.side AS execution_side" if "side" in columns else "NULL AS execution_side",
        ("s.economic_trade_key" if "economic_trade_key" in columns else "NULL AS economic_trade_key"),
        ("s.direction_changed" if "direction_changed" in columns else "NULL AS direction_changed"),
        ("p.direction AS source_direction" if "direction" in signal_columns else "NULL AS source_direction"),
        ("p.created_at AS source_created_at" if "created_at" in signal_columns else "NULL AS source_created_at"),
    ]
    for optional in ("outcome_status", "close_reason", "cost_model_status"):
        select.append(f"s.{optional}" if optional in columns else f"NULL AS {optional}")
    rows = conn.execute(
        "SELECT " + ", ".join(select) + " FROM paper_shadow_execution_outcomes s "
        "LEFT JOIN proposed_signals p ON p.signal_id=s.signal_id "
        "WHERE s.shadow_lane=? AND s.branch=? AND s.window=?",
        (cfg["shadow_lane"], cfg["branch"], FORWARD),
    ).fetchall()
    allowed = set(cfg["entry_modes"])
    result: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        if not str(item.get("asset_class") or "").lower().startswith(("stock", "equit")):
            continue
        mode = str(item.get("entry_mode") or "").upper()
        if mode not in allowed:
            continue
        # Each execution outcome can carry multiple fee profiles. Only the
        # stock paper profile is economically authoritative for this lane.
        if str(item.get("fee_profile") or "") != cfg["fee_profile"]:
            continue
        if str(item.get("cost_model_status") or "") == "stale_cost_model":
            continue
        item["entry_mode"] = mode
        result.append(item)
    # Repeated scans can create multiple signal_ids for the same economic
    # decision. Production admits only the first candidate per symbol/session,
    # so counting every duplicate here inflates both wins and losses. Keep the
    # earliest point-in-time signal for each immutable economic trade key.
    deduped: dict[str, dict[str, Any]] = {}
    for item in sorted(
        result,
        key=lambda row: (str(row.get("source_created_at") or ""), str(row.get("signal_id") or "")),
    ):
        key = str(item.get("economic_trade_key") or item.get("signal_id") or "")
        deduped.setdefault(key, item)
    return list(deduped.values())


def _is_closed(row: dict[str, Any]) -> bool:
    return (row.get("entry_fill_status") == "filled" and row.get("net_pnl_usdt") is not None
            and row.get("outcome_status") in ("closed", None))


def _direction_breakdown(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Separate the combined direction-model result from unchanged source-side evidence."""
    buckets: dict[str, list[dict[str, Any]]] = {"unchanged": [], "changed": [], "unknown": []}
    for row in rows:
        source = str(row.get("source_direction") or "").lower()
        execution = str(row.get("execution_side") or "").lower()
        changed_flag = row.get("direction_changed")
        if changed_flag is not None:
            bucket = "changed" if int(changed_flag) else "unchanged"
        elif source and execution:
            bucket = "changed" if source != execution else "unchanged"
        else:
            bucket = "unknown"
        buckets[bucket].append(row)
    result: dict[str, dict[str, Any]] = {}
    for name, bucket in buckets.items():
        closed = [row for row in bucket if _is_closed(row)]
        pnl = [float(row["net_pnl_usdt"]) for row in closed]
        wins = [value for value in pnl if value > 0]
        losses = [value for value in pnl if value < 0]
        result[name] = {
            "rows": len(bucket), "closed": len(closed), "net_pnl_usd": round(sum(pnl), 4),
            "profit_factor": (round(sum(wins) / abs(sum(losses)), 4) if losses
                              else (float("inf") if wins else None)),
        }
    return result


def _slice(entry_mode: str, rows: list[dict[str, Any]], *, forward_days: float,
           cfg: dict[str, Any], raw_mode_rows: int | None = None) -> dict[str, Any]:
    mode_rows = [row for row in rows if row.get("entry_mode") == entry_mode]
    clean = [row for row in mode_rows if int(row.get("is_clean_for_edge") or 0) == 1]
    dirty = [row for row in mode_rows if int(row.get("is_clean_for_edge") or 0) != 1]
    clean_filled = [row for row in clean if row.get("entry_fill_status") == "filled"]
    clean_closed = [row for row in clean if _is_closed(row)]
    dirty_closed = [row for row in dirty if _is_closed(row)]
    ordered = sorted(clean_closed, key=lambda row: str(row.get("entry_fill_time") or row.get("created_at") or ""))
    pnl = [float(row["net_pnl_usdt"]) for row in ordered]
    r_values = [float(row["net_r"]) for row in ordered if row.get("net_r") is not None]
    wins = [value for value in pnl if value > 0]
    losses = [value for value in pnl if value < 0]
    gross_loss = abs(sum(losses))
    pf = (round(sum(wins) / gross_loss, 4) if gross_loss else
          (float("inf") if wins else None))
    net_usd = round(sum(pnl), 4)
    min_closed = cfg["min_clean_closed"]
    reasons: list[str]
    if not mode_rows:
        verdict, reasons = "NO_FORWARD_EVIDENCE", ["no rows in the forward candidate lane"]
    elif len(clean_closed) < min_closed:
        verdict, reasons = "INSUFFICIENT_CLEAN_SAMPLE", [
            f"clean closed={len(clean_closed)} < {min_closed}",
            f"dirty closed={len(dirty_closed)} excluded from edge",
        ]
    elif forward_days < cfg["min_forward_days"]:
        verdict, reasons = "ACCUMULATING_FORWARD_DAYS", [
            f"forward days={forward_days:.1f} < {cfg['min_forward_days']}",
            "clean sample is sufficient but the post-activation window is still young",
        ]
    elif cfg["require_positive_net_usd"] and net_usd <= 0:
        verdict, reasons = "KEEP_SHADOW", [f"net USD={net_usd:.2f} is not positive"]
    elif pf is None or pf < cfg["min_profit_factor"]:
        verdict, reasons = "KEEP_SHADOW", [
            f"PF={'none' if pf is None else f'{pf:.2f}'} < {cfg['min_profit_factor']:.2f}",
        ]
    else:
        verdict, reasons = "REVIEW_ONLY", [
            "clean forward gates passed; operator review only, no automatic paper/live change",
        ]
    return {
        "entry_mode": entry_mode,
        "duplicate_rows_excluded": max(0, int(raw_mode_rows or len(mode_rows)) - len(mode_rows)),
        "forward_rows": len(mode_rows), "clean_rows": len(clean), "dirty_rows": len(dirty),
        "clean_filled": len(clean_filled), "clean_closed": len(clean_closed),
        "dirty_closed": len(dirty_closed), "net_pnl_usd": net_usd,
        "net_r_sum": round(sum(r_values), 4), "profit_factor": pf,
        "winrate": round(len(wins) / len(pnl), 4) if pnl else 0.0,
        "max_drawdown_usd": _max_drawdown(pnl),
        "fees_usd": round(sum(float(row["fees_usdt"]) for row in clean_filled
                              if row.get("fees_usdt") is not None), 4),
        "slippage_usd": round(sum(float(row["slippage_usdt"]) for row in clean_filled
                                  if row.get("slippage_usdt") is not None), 4),
        "forward_days": round(forward_days, 3), "verdict": verdict, "reasons": reasons,
        "direction_breakdown": _direction_breakdown(clean),
        "legacy_evidence_reused": False,
    }


def evaluate(*, db: str | None = None, persist: bool = True, now_iso: str | None = None,
             write_artifacts: bool | None = None, artifacts_dir: str | None = None) -> dict[str, Any]:
    """Evaluate the separate forward candidate lane; never promotes or alters source tables."""
    path = _db_path(db)
    now = _parse_iso(now_iso) or datetime.now(timezone.utc)
    cfg = load_evaluator_config()
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    try:
        activation = _activation(conn, cfg["activation_meta_key"])
        activated = _parse_iso(activation)
        forward_days = max(0.0, (now - activated).total_seconds() / 86400) if activated else 0.0
        rows = _load_rows(conn, cfg) if cfg["enabled"] else []
        # _load_rows already de-duplicates. Count raw rows separately so the
        # report exposes upstream scan duplication instead of hiding it.
        raw_counts: dict[str, int] = {}
        if cfg["enabled"] and _table_exists(conn, "paper_shadow_execution_outcomes"):
            raw_counts = {
                str(row[0]).upper(): int(row[1])
                for row in conn.execute(
                    "SELECT entry_mode,COUNT(*) FROM paper_shadow_execution_outcomes "
                    "WHERE shadow_lane=? AND branch=? AND window=? AND fee_profile=? "
                    "GROUP BY entry_mode",
                    (cfg["shadow_lane"], cfg["branch"], FORWARD, cfg["fee_profile"]),
                )
            }
        slices = [
            _slice(mode, rows, forward_days=forward_days, cfg=cfg,
                   raw_mode_rows=raw_counts.get(mode))
            for mode in cfg["entry_modes"]
        ]
        result = {
            "generated_at": now.isoformat(), "db_path": str(path), "enabled": cfg["enabled"],
            "activated_at": activation, "forward_days": round(forward_days, 3), "config": cfg,
            "slices": slices, "legacy_evidence_reused": False,
            "source_tables_read_only": ["paper_shadow_execution_outcomes", "paper_shadow_meta"],
        }
        if persist:
            ensure_tables(conn)
            sql = ("INSERT INTO stocks_intraday_forward_shadow_evaluations (" + ",".join(_COLS) + ") "
                   "VALUES (" + ",".join("?" for _ in _COLS) + ")")
            conn.executemany(sql, [tuple([
                result["generated_at"], activation, s["entry_mode"], s["forward_rows"], s["clean_rows"],
                s["dirty_rows"], s["clean_filled"], s["clean_closed"], s["dirty_closed"],
                s["net_pnl_usd"], s["net_r_sum"], s["profit_factor"], s["winrate"],
                s["max_drawdown_usd"], s["fees_usd"], s["slippage_usd"], s["forward_days"],
                s["verdict"], json.dumps(s["reasons"]), json.dumps(s["direction_breakdown"], sort_keys=True),
                s["duplicate_rows_excluded"], 0, json.dumps(cfg, sort_keys=True),
            ]) for s in slices])
            conn.commit()
    finally:
        conn.close()
    do_artifacts = (db is None) if write_artifacts is None else bool(write_artifacts)
    if do_artifacts:
        base = Path(artifacts_dir) if artifacts_dir else _root() / "data" / "diagnostics"
        base.mkdir(parents=True, exist_ok=True)
        (base / "stocks_intraday_forward_shadow_evaluation.json").write_text(
            json.dumps(result, indent=2, default=str), encoding="utf-8")
    return result


def _fmt(value: Any, digits: int = 2) -> str:
    if value is None:
        return "-"
    if value == float("inf"):
        return "inf"
    return f"{float(value):.{digits}f}"


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# Stocks Intraday Forward Shadow Evaluation", "",
        f"- generated_at: `{result['generated_at']}`",
        f"- activated_at: `{result.get('activated_at') or 'not set'}`; forward days: `{result['forward_days']:.1f}`",
        "- USD net PnL is authoritative; R is secondary. Only clean, closed, forward rows count as edge.",
        "- Dirty/no-coverage rows and historical backfill are diagnostics, not evidence.",
        "- `REVIEW_ONLY` never changes paper routing, actionability, sizing, or live status.", "",
        "| entry mode | unique rows | duplicates excluded | clean closed | dirty closed | net USD | PF | win% | max DD $ | fees $ | slip $ | verdict |",
        "|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|---|",
    ]
    for s in result["slices"]:
        lines.append(
            f"| {s['entry_mode']} | {s['forward_rows']} | {s['duplicate_rows_excluded']} | "
            f"{s['clean_closed']} | {s['dirty_closed']} | "
            f"{_fmt(s['net_pnl_usd'])} | {_fmt(s['profit_factor'])} | {_fmt(s['winrate'] * 100, 0)} | "
            f"{_fmt(s['max_drawdown_usd'])} | {_fmt(s['fees_usd'])} | {_fmt(s['slippage_usd'])} | {s['verdict']} |"
        )
        lines.append(f"  - {'; '.join(s['reasons'])}")
        lines.append(f"  - direction evidence: `{json.dumps(s['direction_breakdown'], sort_keys=True)}`")
    lines.extend(["", "## Guardrails", "",
                  "- `legacy_evidence_reused=False` for every slice.",
                  "- The evaluator reads shadow outcomes and writes only `stocks_intraday_forward_shadow_evaluations`.",
                  "- No automatic promotion: more clean forward evidence is required before any human decision."])
    return "\n".join(lines) + "\n"


def write_report(result: dict[str, Any], out_dir: str | None = None) -> str:
    base = Path(out_dir) if out_dir else _root() / "reports"
    base.mkdir(parents=True, exist_ok=True)
    out = base / "STOCKS_INTRADAY_FORWARD_SHADOW_EVALUATION.md"
    out.write_text(render_markdown(result), encoding="utf-8")
    return str(out)


__all__ = ["evaluate", "ensure_tables", "load_evaluator_config", "render_markdown", "write_report"]
