from __future__ import annotations

import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from research_labs.technical_trend_reclaim.src.common import parameter_grid as shared_parameter_grid


LAB_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = LAB_ROOT / "config" / "crypto_v1.yaml"
ARTIFACT_ROOT = LAB_ROOT / "artifacts"
LEDGER_PATH = LAB_ROOT / "research.sqlite"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def stable_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)


def digest(value: Any) -> str:
    raw = value if isinstance(value, bytes) else stable_json(value).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def load_config(path: str | Path | None = None) -> dict[str, Any]:
    selected = Path(path) if path is not None else CONFIG_PATH
    return yaml.safe_load(selected.read_text(encoding="utf-8")) or {}


def parameter_grid(cfg: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    return shared_parameter_grid(cfg or load_config())


def _schema() -> str:
    return """
    PRAGMA journal_mode=WAL;
    CREATE TABLE IF NOT EXISTS experiment_runs (
      run_id TEXT PRIMARY KEY, created_at TEXT NOT NULL, stage TEXT NOT NULL,
      config_hash TEXT NOT NULL, code_hash TEXT NOT NULL, archive_hash TEXT NOT NULL,
      status TEXT NOT NULL, notes_json TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS parameter_sets (
      run_id TEXT NOT NULL, variant_id TEXT NOT NULL, parameter_hash TEXT NOT NULL,
      parameters_json TEXT NOT NULL, PRIMARY KEY(run_id,variant_id)
    );
    CREATE TABLE IF NOT EXISTS candidates (
      run_id TEXT NOT NULL, candidate_id TEXT NOT NULL, variant_id TEXT NOT NULL,
      fold_id TEXT NOT NULL, asset TEXT NOT NULL, symbol TEXT NOT NULL,
      direction TEXT NOT NULL, fvg_formed_at TEXT, decision_at TEXT, entry_at TEXT,
      status TEXT NOT NULL, rejection_reason TEXT, is_clean INTEGER NOT NULL,
      source_quality TEXT NOT NULL, features_json TEXT NOT NULL, geometry_json TEXT NOT NULL,
      PRIMARY KEY(run_id,candidate_id,variant_id,fold_id)
    );
    CREATE INDEX IF NOT EXISTS idx_rcc_candidates
      ON candidates(run_id,variant_id,fold_id,status,rejection_reason);
    CREATE TABLE IF NOT EXISTS trades (
      run_id TEXT NOT NULL, trade_id TEXT NOT NULL, candidate_id TEXT NOT NULL,
      variant_id TEXT NOT NULL, fold_id TEXT NOT NULL, asset TEXT NOT NULL,
      symbol TEXT NOT NULL, direction TEXT NOT NULL, entry_at TEXT NOT NULL,
      exit_at TEXT, entry_price REAL NOT NULL, stop_price REAL NOT NULL,
      exit_price REAL, close_reason TEXT, bars_held INTEGER NOT NULL,
      gross_r REAL, net_r REAL, gross_pnl_usd REAL, net_pnl_usd REAL,
      fees_usd REAL NOT NULL, slippage_usd REAL NOT NULL, funding_usd REAL NOT NULL,
      mfe_r REAL, mae_r REAL, highest_tp INTEGER NOT NULL,
      execution_quality TEXT, events_json TEXT NOT NULL,
      PRIMARY KEY(run_id,trade_id,variant_id,fold_id)
    );
    CREATE INDEX IF NOT EXISTS idx_rcc_trades
      ON trades(run_id,variant_id,fold_id,symbol,exit_at);
    CREATE TABLE IF NOT EXISTS fold_metrics (
      run_id TEXT NOT NULL, variant_id TEXT NOT NULL, fold_id TEXT NOT NULL,
      clean_closed INTEGER NOT NULL, net_pnl_usd REAL NOT NULL, net_r REAL NOT NULL,
      profit_factor REAL, winrate REAL, max_drawdown_r REAL NOT NULL,
      top5_profit_share REAL, max_symbol_profit_share REAL, rejection_counts_json TEXT NOT NULL,
      PRIMARY KEY(run_id,variant_id,fold_id)
    );
    CREATE TABLE IF NOT EXISTS selection_results (
      run_id TEXT NOT NULL, variant_id TEXT NOT NULL, verdict TEXT NOT NULL,
      reasons_json TEXT NOT NULL, pooled_metrics_json TEXT NOT NULL,
      bootstrap_p REAL, fdr_q REAL, plateau_ok INTEGER NOT NULL,
      selected INTEGER NOT NULL, PRIMARY KEY(run_id,variant_id)
    );
    CREATE TABLE IF NOT EXISTS forward_decisions (
      decision_id TEXT PRIMARY KEY, strategy_id TEXT NOT NULL, profile_hash TEXT NOT NULL,
      symbol TEXT NOT NULL, direction TEXT NOT NULL, formed_at TEXT NOT NULL,
      decision_at TEXT NOT NULL, observed_at TEXT NOT NULL, latency_seconds REAL NOT NULL,
      status TEXT NOT NULL, rejection_reason TEXT, is_clean INTEGER NOT NULL,
      entry_price REAL, stop_price REAL, targets_json TEXT NOT NULL,
      features_json TEXT NOT NULL, source_times_json TEXT NOT NULL,
      created_at TEXT NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_rcc_forward_decisions
      ON forward_decisions(strategy_id,decision_at,status,symbol);
    CREATE TABLE IF NOT EXISTS forward_outcomes (
      decision_id TEXT PRIMARY KEY, outcome_status TEXT NOT NULL, entry_at TEXT,
      exit_at TEXT, close_reason TEXT, gross_pnl_usd REAL, net_pnl_usd REAL,
      fees_usd REAL, slippage_usd REAL, funding_usd REAL, updated_at TEXT NOT NULL,
      FOREIGN KEY(decision_id) REFERENCES forward_decisions(decision_id)
    );
    CREATE TABLE IF NOT EXISTS forward_meta (
      key TEXT PRIMARY KEY, value_json TEXT NOT NULL, updated_at TEXT NOT NULL
    );
    """


def connect() -> sqlite3.Connection:
    LAB_ROOT.mkdir(parents=True, exist_ok=True)
    ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(LEDGER_PATH, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.executescript(_schema())
    return conn


def insert_many(conn: sqlite3.Connection, table: str, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    columns = list(rows[0])
    placeholders = ",".join("?" for _ in columns)
    conn.executemany(
        f"INSERT INTO {table} ({','.join(columns)}) VALUES ({placeholders})",
        [[row.get(column) for column in columns] for row in rows],
    )

