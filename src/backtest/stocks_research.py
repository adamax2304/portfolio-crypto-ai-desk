"""Point-in-time stock catalyst research harness.

This is intentionally separate from Paper and live execution.  It replays only
canonical events that were available at the simulated decision time against a
separate deep RTH archive, then stores results in ``stocks_research_*`` tables.
It is a parameter-screening and walk-forward tool, never a promotion mechanism.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from src.config import load_config
from src.execution import stocks_catalyst_rs_shadow as catalyst
from src.utils.symbols import symbol_to_filename


ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "config" / "research" / "stocks_catalyst_research.yaml"
RUNS_TABLE = "stocks_research_backtest_runs"
RESULTS_TABLE = "stocks_research_backtest_results"

DDL = f"""
CREATE TABLE IF NOT EXISTS {RUNS_TABLE} (
  run_id TEXT PRIMARY KEY,
  generated_at TEXT NOT NULL,
  study_start TEXT NOT NULL,
  study_end TEXT NOT NULL,
  status TEXT NOT NULL,
  config_json TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS {RESULTS_TABLE} (
  run_id TEXT NOT NULL,
  variant_id TEXT NOT NULL,
  family TEXT NOT NULL,
  candidate_id TEXT NOT NULL,
  event_session_key TEXT NOT NULL,
  decision_at TEXT,
  symbol TEXT,
  eligibility_status TEXT,
  rejection_reason TEXT,
  data_status TEXT,
  is_clean_for_edge INTEGER NOT NULL DEFAULT 0,
  outcome_status TEXT,
  net_pnl_usd REAL,
  net_r REAL,
  evidence_cohort TEXT,
  payload_json TEXT NOT NULL,
  PRIMARY KEY (run_id, variant_id, candidate_id)
);
"""

DEFAULTS: dict[str, Any] = {
    "enabled": True,
    "history_root": "data/history/stocks",
    "parquet_roots": [
        "research_labs/technical_trend_reclaim/data/stocks/yahoo",
        "research_labs/technical_trend_reclaim/data/stocks/mexc_contract",
    ],
    "timeframe": "15m",
    "daily_timeframe": "1d",
    "minimum_history_days": 180,
    "train_days": 252,
    "test_days": 63,
    "step_days": 63,
    "minimum_train_closed": 20,
    "minimum_train_pf": 1.10,
    "variants": [],
}


def load_research_config(path: str | Path | None = None) -> dict[str, Any]:
    cfg = dict(DEFAULTS)
    file_path = Path(path) if path else CONFIG_PATH
    if file_path.exists():
        raw = yaml.safe_load(file_path.read_text(encoding="utf-8")) or {}
        supplied = raw.get("stocks_catalyst_research") or {}
        if isinstance(supplied, dict):
            cfg.update(supplied)
    return cfg


def _utc(value: datetime | str) -> datetime:
    parsed = pd.Timestamp(value)
    if parsed.tzinfo is None:
        parsed = parsed.tz_localize("UTC")
    else:
        parsed = parsed.tz_convert("UTC")
    return parsed.to_pydatetime()


def _history_root(cfg: dict[str, Any]) -> Path:
    configured = Path(str(cfg["history_root"]))
    return configured if configured.is_absolute() else ROOT / configured


def load_history(cfg: dict[str, Any], symbol: str, timeframe: str) -> pd.DataFrame:
    path = _history_root(cfg) / timeframe / f"{symbol_to_filename(symbol)}.csv"
    frame = pd.DataFrame()
    if path.exists():
        try:
            frame = pd.read_csv(path)
        except (OSError, pd.errors.ParserError, UnicodeDecodeError):
            frame = pd.DataFrame()
    if frame.empty:
        for configured in cfg.get("parquet_roots") or []:
            root = Path(str(configured))
            root = root if root.is_absolute() else ROOT / root
            parquet = root / symbol_to_filename(symbol) / f"{timeframe}.parquet"
            if not parquet.exists():
                continue
            try:
                frame = pd.read_parquet(parquet)
            except (OSError, ValueError, ImportError):
                frame = pd.DataFrame()
            if not frame.empty:
                break
    if frame.empty:
        return frame
    if "timestamp" not in frame.columns and "bar_open_at" in frame.columns:
        frame = frame.rename(columns={"bar_open_at": "timestamp"})
    return catalyst.normalize_frame(frame)


def _event_session_key(row: dict[str, Any]) -> str:
    stamp = catalyst.parse_dt(row.get("entry_ts") or row.get("decision_at") or row.get("catalyst_at"))
    if stamp is None:
        session = "unknown"
    else:
        session = stamp.astimezone(catalyst.NY).date().isoformat()
    return f"{str(row.get('symbol') or '').upper()}|{str(row.get('catalyst_type') or '').lower()}|{session}"


def _dedupe(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Prevent repeated source rows from becoming repeated historical trades."""
    groups: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        row["event_session_key"] = _event_session_key(row)
        if str(row.get("eligibility_status")) == "eligible":
            groups.setdefault(row["event_session_key"], []).append(row)
    for members in groups.values():
        members.sort(key=lambda row: (
            catalyst.parse_dt(row.get("entry_ts") or row.get("decision_at"))
            or datetime.max.replace(tzinfo=timezone.utc),
            str(row.get("candidate_id") or ""),
        ))
        for duplicate in members[1:]:
            duplicate.update({
                "eligibility_status": "rejected",
                "rejection_reason": "EVENT_SESSION_DUPLICATE",
                "outcome_status": "skipped",
                "net_pnl_usd": 0.0,
                "net_r": 0.0,
            })
    return rows


def _closed(rows: list[dict[str, Any]], start: datetime, end: datetime) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for row in rows:
        decision = catalyst.parse_dt(row.get("decision_at"))
        if not decision or not (start <= decision < end):
            continue
        if (str(row.get("eligibility_status")) == "eligible"
                and str(row.get("outcome_status")) == "closed"
                and int(row.get("is_clean_for_edge") or 0) == 1):
            selected.append(row)
    return selected


def metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    values = [float(row.get("net_pnl_usd") or 0.0) for row in rows]
    wins = [value for value in values if value > 0]
    losses = [value for value in values if value < 0]
    gross_loss = abs(sum(losses))
    equity = 0.0
    peak = 0.0
    drawdown = 0.0
    for value in values:
        equity += value
        peak = max(peak, equity)
        drawdown = min(drawdown, equity - peak)
    return {
        "closed": len(values),
        "net_pnl_usd": round(sum(values), 2),
        "profit_factor": (round(sum(wins) / gross_loss, 4) if gross_loss else None),
        "winrate": (round(len(wins) / len(values), 4) if values else None),
        "max_drawdown_usd": round(abs(drawdown), 2),
    }


def _variant_cfg(variant: dict[str, Any]) -> dict[str, Any]:
    cfg = catalyst.load_strategy_config()
    cfg.update(variant.get("overrides") or {})
    cfg["feature_flag"] = True
    cfg["strategy_id"] = f"research_{variant['variant_id']}"
    cfg["profile_id"] = f"research_{variant['variant_id']}"
    cfg["shadow_lane"] = "research_stocks_backtest"
    return cfg


def _replay_variant(
    conn: sqlite3.Connection, *, variant: dict[str, Any], study_start: datetime, study_end: datetime,
    history_cfg: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    cfg = _variant_cfg(variant)
    symbols, sector_by_symbol, etf_by_sector = catalyst._universe(cfg)
    candidates, funnel = catalyst._event_candidates(
        conn, cfg, study_end, symbols, sector_by_symbol, etf_by_sector, start_at=study_start,
    )
    cache: dict[tuple[str, str], pd.DataFrame] = {}

    def frame(symbol: str, timeframe: str) -> pd.DataFrame:
        key = (symbol, timeframe)
        if key not in cache:
            cache[key] = load_history(history_cfg, symbol, timeframe)
        return cache[key]

    rows: list[dict[str, Any]] = []
    for spec in candidates:
        event = spec["event"]
        symbol = str(spec["symbol"])
        row = catalyst.evaluate_candidate(
            event=event,
            symbol=symbol,
            stock_bars=frame(symbol, str(history_cfg["timeframe"])),
            daily_bars=frame(symbol, str(history_cfg["daily_timeframe"])),
            spy_bars=frame("SPY", str(history_cfg["timeframe"])),
            sector_bars=frame(str(spec["sector_etf"]), str(history_cfg["timeframe"])),
            sector=str(spec["sector"]),
            sector_etf=str(spec["sector_etf"]),
            coverage_clean=None,
            cfg=cfg,
            window="historical_research",
            generated_at=study_end,
        )
        rows.append(row)
    return _dedupe(rows), funnel


def walk_forward(
    rows_by_variant: dict[str, list[dict[str, Any]]], variants: list[dict[str, Any]], *,
    study_start: datetime, study_end: datetime, cfg: dict[str, Any],
) -> list[dict[str, Any]]:
    """Choose only on an earlier window; score the chosen variant later."""
    train_days, test_days, step_days = (int(cfg["train_days"]), int(cfg["test_days"]), int(cfg["step_days"]))
    minimum_closed, minimum_pf = int(cfg["minimum_train_closed"]), float(cfg["minimum_train_pf"])
    variants_by_family: dict[str, list[dict[str, Any]]] = {}
    for variant in variants:
        variants_by_family.setdefault(str(variant.get("family") or "catalyst"), []).append(variant)
    folds: list[dict[str, Any]] = []
    train_start = study_start
    while train_start + timedelta(days=train_days + test_days) <= study_end:
        train_end = train_start + timedelta(days=train_days)
        test_end = train_end + timedelta(days=test_days)
        for family, family_variants in variants_by_family.items():
            ranked: list[tuple[dict[str, Any], dict[str, Any]]] = []
            for variant in family_variants:
                stat = metrics(_closed(rows_by_variant[variant["variant_id"]], train_start, train_end))
                if (stat["closed"] >= minimum_closed and stat["net_pnl_usd"] > 0
                        and stat["profit_factor"] is not None and stat["profit_factor"] >= minimum_pf):
                    ranked.append((variant, stat))
            chosen, train_stat = (max(ranked, key=lambda item: (item[1]["profit_factor"], item[1]["net_pnl_usd"]))
                                  if ranked else (None, None))
            folds.append({
                "family": family,
                "train_start": train_start.isoformat(), "train_end": train_end.isoformat(),
                "test_end": test_end.isoformat(),
                "selected_variant": chosen["variant_id"] if chosen else None,
                "train": train_stat,
                "test": (metrics(_closed(rows_by_variant[chosen["variant_id"]], train_end, test_end))
                         if chosen else None),
            })
        train_start += timedelta(days=step_days)
    return folds


def _history_status(cfg: dict[str, Any], variants: list[dict[str, Any]]) -> dict[str, Any]:
    # SPY is required by every catalyst family; it is an early, cheap coverage gate.
    frame = load_history(cfg, "SPY", str(cfg["timeframe"]))
    if frame.empty:
        return {"status": "INSUFFICIENT_HISTORY", "reason": "SPY_TIMEFRAME_MISSING", "days": 0}
    days = (frame["timestamp"].max() - frame["timestamp"].min()).total_seconds() / 86400.0
    required = int(cfg["minimum_history_days"])
    return {
        "status": "OK" if days >= required else "INSUFFICIENT_HISTORY",
        "reason": None if days >= required else "SPY_HISTORY_TOO_SHORT",
        "days": round(days, 1), "required_days": required, "variants": len(variants),
    }


def run(
    *, db: str | None = None, study_start: datetime | str, study_end: datetime | str,
    config_path: str | Path | None = None, persist: bool = True,
) -> dict[str, Any]:
    cfg = load_research_config(config_path)
    start, end = _utc(study_start), _utc(study_end)
    if end <= start:
        raise ValueError("study_end must be later than study_start")
    variants = [dict(item) for item in cfg.get("variants") or [] if item.get("enabled", True)]
    if not variants:
        raise ValueError("no enabled research variants configured")
    for variant in variants:
        if not variant.get("variant_id"):
            raise ValueError("each research variant needs variant_id")
    history = _history_status(cfg, variants)
    generated_at = datetime.now(timezone.utc).isoformat()
    fingerprint = json.dumps({"cfg": cfg, "start": start.isoformat(), "end": end.isoformat()}, sort_keys=True)
    run_id = hashlib.sha256(fingerprint.encode()).hexdigest()[:20]
    result: dict[str, Any] = {
        "run_id": run_id, "generated_at": generated_at, "study_start": start.isoformat(),
        "study_end": end.isoformat(), "history": history, "persisted": False,
        "variants": {}, "walk_forward": [], "status": history["status"],
    }
    if history["status"] != "OK":
        return result

    path = Path(db) if db else load_config().db_path
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        rows_by_variant: dict[str, list[dict[str, Any]]] = {}
        for variant in variants:
            rows, funnel = _replay_variant(conn, variant=variant, study_start=start, study_end=end, history_cfg=cfg)
            rows_by_variant[variant["variant_id"]] = rows
            result["variants"][variant["variant_id"]] = {
                "family": variant.get("family") or "catalyst",
                "funnel": funnel,
                "all": metrics(_closed(rows, start, end)),
                "rows": rows,
            }
    finally:
        conn.close()
    result["walk_forward"] = walk_forward(rows_by_variant, variants, study_start=start, study_end=end, cfg=cfg)
    result["status"] = "RESEARCH_ONLY"

    if persist:
        conn = sqlite3.connect(path)
        try:
            conn.executescript(DDL)
            conn.execute(
                f"INSERT OR REPLACE INTO {RUNS_TABLE} (run_id,generated_at,study_start,study_end,status,config_json) "
                "VALUES (?,?,?,?,?,?)",
                (run_id, generated_at, start.isoformat(), end.isoformat(), result["status"], json.dumps(cfg, sort_keys=True)),
            )
            conn.execute(f"DELETE FROM {RESULTS_TABLE} WHERE run_id=?", (run_id,))
            for variant_id, summary in result["variants"].items():
                for row in summary["rows"]:
                    conn.execute(
                        f"INSERT INTO {RESULTS_TABLE} (run_id,variant_id,family,candidate_id,event_session_key,decision_at,"
                        "symbol,eligibility_status,rejection_reason,data_status,is_clean_for_edge,outcome_status,net_pnl_usd,"
                        "net_r,evidence_cohort,payload_json) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        (run_id, variant_id, str(summary["family"]), str(row.get("candidate_id")),
                         str(row.get("event_session_key")), row.get("decision_at"), row.get("symbol"),
                         row.get("eligibility_status"), row.get("rejection_reason"), row.get("data_status"),
                         int(row.get("is_clean_for_edge") or 0), row.get("outcome_status"), row.get("net_pnl_usd"),
                         row.get("net_r"), row.get("evidence_cohort"), json.dumps(row, default=str, sort_keys=True)),
                    )
            conn.commit()
        finally:
            conn.close()
        result["persisted"] = True
    return result


def render_markdown(result: dict[str, Any]) -> str:
    history = result["history"]
    lines = ["# Stocks Research Backtest", "",
             "> Research-only. It cannot create Paper signals, alter any ledger, or route live orders.", "",
             f"- Study: `{result['study_start']}` to `{result['study_end']}`",
             f"- History gate: **{history['status']}** ({history.get('reason') or 'satisfied'})"]
    if history["status"] != "OK":
        lines += ["", "No parameter result is produced until the separate deep RTH archive meets the coverage gate."]
        return "\n".join(lines)
    lines += ["", "| Variant | Closed clean | Net USD | PF | Win rate | Max DD |",
              "|---|---:|---:|---:|---:|---:|"]
    for variant_id, item in sorted(result["variants"].items()):
        stat = item["all"]
        lines.append(f"| `{variant_id}` | {stat['closed']} | {stat['net_pnl_usd']:.2f} | "
                     f"{stat['profit_factor']} | {stat['winrate']} | {stat['max_drawdown_usd']:.2f} |")
    lines += ["", "## Walk-forward selections", ""]
    for fold in result["walk_forward"]:
        selected = fold["selected_variant"] or "no eligible variant"
        lines.append(f"- {fold['family']} | train {fold['train_start'][:10]}–{fold['train_end'][:10]} "
                     f"| test to {fold['test_end'][:10]} | selected: `{selected}`")
    return "\n".join(lines)


def write_report(result: dict[str, Any], out_dir: str | Path | None = None) -> Path:
    path = Path(out_dir) if out_dir else ROOT / "reports"
    path.mkdir(parents=True, exist_ok=True)
    report = path / "STOCKS_RESEARCH_BACKTEST.md"
    report.write_text(render_markdown(result), encoding="utf-8")
    return report


__all__ = ["load_research_config", "load_history", "metrics", "run", "walk_forward", "write_report"]
