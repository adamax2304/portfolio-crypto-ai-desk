"""Fast liquidation flush/reclaim v3, isolated Paper-only evidence lane.

The lane detects a 5m downside impulse accompanied by long liquidations and an
OI contraction. Enabled confirmation profiles are Paper-only. The module has
no live bridge and never writes proposed signals or orders.
"""
from __future__ import annotations

import hashlib
import json
import math
import sqlite3
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from src.execution import crypto_liquidity_sweep_reclaim_paper as reclaim_v2
from src.execution import crypto_liquidity_sweep_shadow as sweep_v1
from src.execution.fees import trade_costs
from src.execution.shadow_strategy_common import (
    clean_forward_summary,
    json_text,
    load_yaml_block,
    normalize_frame,
    parse_dt,
    utc_now,
)


ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "config" / "paper" / "crypto" / "fast_flush_reclaim_v3.yaml"
STRATEGY_KEY = "crypto_fast_flush_reclaim_v3_paper"
_SCHEMA_READY_DATABASES: set[str] = set()

DEFAULTS: dict[str, Any] = {
    "feature_flag": True,
    "strategy_id": "crypto_fast_flush_reclaim_v3",
    "paper_lane": "paper_crypto_fast_flush_reclaim_v3",
    "base_timeframe": "5m",
    "primary_exchange": "bybit",
    "max_symbols": 60,
    "recent_scan_bars": 8,
    "liquidation_sources": ["binance", "bybit"],
    "liquidation_window_minutes": 5,
    "min_liquidation_notional_usd": 20_000.0,
    "min_liquidation_percentile": 0.70,
    "liquidation_percentile_lookback_days": 14,
    "min_liquidation_history_episodes": 10,
    "min_flush_atr": 1.25,
    "max_flush_atr": 5.0,
    "min_flush_pct": 0.45,
    "min_rvol": 1.0,
    "min_oi_drop_pct": 0.25,
    "max_oi_drop_pct": 5.0,
    "derivatives_freshness_minutes": 12,
    "liquidity_freshness_minutes": 12,
    "max_spread_bps": 18.0,
    "allowed_sessions": ["asia", "europe", "us"],
    "reclaim_fraction": 0.35,
    "stop_buffer_atr": 0.10,
    "min_stop_distance_pct": 0.005,
    "max_stop_distance_pct": 0.015,
    "target_r": [0.80, 1.35],
    "target_fractions": [0.70, 0.30],
    "move_stop_to_entry_after_tp1": True,
    "fixed_risk_usd": 10.0,
    "fee_profile": "bybit_non_vip_usdt_perp",
    "max_entry_latency_seconds": 90.0,
    "refresh_candidate_ohlcv": True,
    "max_candidate_refresh_symbols": 12,
    "manual_telegram_signals": {"enabled": False, "profile_ids": [], "max_age_seconds": 90},
    "confirmation_profiles": {
        "FAST_1M_RECLAIM": {
            "enabled": True,
            "profile_id": "crypto_fast_flush_reclaim_fast_1m_paper_v3",
            "confirmation_timeframe": "1m", "hold_bars": 1,
            "confirmation_window_bars": 8, "require_green": True,
            "require_progress": False, "max_holding_bars": 45,
        },
        "FAST_1M_EUROPE_MODERATE": {
            "enabled": False,
            "profile_id": "crypto_fast_flush_europe_moderate_1m_paper_v1",
            "research_role": "exploratory_europe_session_candidate",
            "activation_at": "2026-10-04T13:11:00+00:00",
            "confirmation_timeframe": "1m", "hold_bars": 1,
            "confirmation_window_bars": 8, "require_green": True,
            "require_progress": False, "max_holding_bars": 45,
            "min_flush_atr": 1.25, "max_flush_atr": 3.25,
            "min_flush_pct": 0.60, "max_flush_pct": 2.50,
            "min_rvol": 1.00, "min_oi_drop_pct": 0.25,
            "max_oi_drop_pct": 3.00, "min_liquidation_percentile": 0.80,
            "allowed_sessions": ["europe"],
            "min_stop_distance_pct": 0.0075, "max_stop_distance_pct": 0.015,
        },
        "FAST_1M_ATR_TARGETS": {
            "enabled": False,
            "profile_id": "crypto_fast_flush_reclaim_fast_1m_atr_targets_paper_v3",
            "activation_at": "2026-09-30T00:00:00+00:00",
            "confirmation_timeframe": "1m", "hold_bars": 1,
            "confirmation_window_bars": 8, "require_green": True,
            "require_progress": False, "max_holding_bars": 45,
            "min_flush_atr": 1.25, "max_flush_atr": 3.25,
            "min_flush_pct": 0.75, "max_flush_pct": 2.50,
            "min_rvol": 1.05, "min_oi_drop_pct": 0.50,
            "max_oi_drop_pct": 3.0, "min_liquidation_percentile": 0.90,
            "allowed_sessions": ["us"], "min_stop_distance_pct": 0.010,
            "max_stop_distance_pct": 0.015, "target_policy": "atr_multiple",
            "target_atr": [1.0, 2.0],
        },
        "FAST_1M_STRUCTURE_CONFIRM": {
            "enabled": False,
            "profile_id": "crypto_fast_flush_reclaim_structure_confirm_1m_paper_v1",
            "activation_at": "2026-10-12T21:27:20+00:00",
            "description": "Strict FAST 1m liquidation reclaim; higher-low, prior-high break and RVOL confirmation",
            "confirmation_timeframe": "1m", "confirmation_mode": "higher_low_break_vol",
            "confirmation_window_bars": 8, "confirmation_rvol_lookback_bars": 20,
            "confirmation_min_rvol": 1.20, "confirmation_min_history_bars": 5,
            "max_holding_bars": 45,
            "min_flush_atr": 1.25, "max_flush_atr": 3.25,
            "min_flush_pct": 0.75, "max_flush_pct": 2.50,
            "min_rvol": 1.05, "min_oi_drop_pct": 0.50,
            "max_oi_drop_pct": 3.00, "min_liquidation_percentile": 0.90,
            "allowed_sessions": ["us"], "min_stop_distance_pct": 0.010,
            "max_stop_distance_pct": 0.015,
        },
        "FAST_1M_BALANCED": {
            "enabled": False,
            "profile_id": "crypto_fast_flush_reclaim_balanced_1m_paper_v3",
            "activation_at": "2026-09-28T22:58:03+00:00",
            "confirmation_timeframe": "1m", "hold_bars": 1,
            "confirmation_window_bars": 8, "require_green": True,
            "require_progress": False, "max_holding_bars": 45,
            "min_flush_atr": 1.25, "max_flush_atr": 3.25,
            "min_flush_pct": 0.75, "max_flush_pct": 2.50,
            "min_rvol": 1.05, "min_oi_drop_pct": 0.25,
            "max_oi_drop_pct": 3.0, "min_liquidation_percentile": 0.90,
            "allowed_sessions": ["europe", "us"],
            "min_stop_distance_pct": 0.0075, "max_stop_distance_pct": 0.015,
        },
        "HELD_1M_RECLAIM": {
            "enabled": False,
            "profile_id": "crypto_fast_flush_reclaim_held_1m_paper_v3",
            "confirmation_timeframe": "1m", "hold_bars": 2,
            "confirmation_window_bars": 12, "require_green": True,
            "require_progress": True, "max_holding_bars": 60,
        },
        "CONTROL_5M_RECLAIM": {
            "enabled": False,
            "profile_id": "crypto_fast_flush_reclaim_control_5m_paper_v3",
            "confirmation_timeframe": "5m", "hold_bars": 1,
            "confirmation_window_bars": 4, "require_green": True,
            "require_progress": False, "max_holding_bars": 18,
        },
        "MEDIUM_DEEP_R_CONTROL": {
            "enabled": False,
            "profile_id": "crypto_fast_flush_medium_deep_r_control_paper_v1",
            "description": "Medium-deep 5m flush; fixed TP1 0.80R / TP2 1.35R control",
            "activation_at": "2026-09-29T16:30:45+00:00",
            "confirmation_timeframe": "1m", "hold_bars": 1,
            "confirmation_window_bars": 8, "require_green": True,
            "require_progress": False, "max_holding_bars": 45,
            "min_flush_atr": 2.0, "max_flush_atr": 5.0,
            "min_flush_pct": 1.5, "max_flush_pct": 2.75,
            "min_rvol": 1.0, "min_oi_drop_pct": 0.25, "max_oi_drop_pct": 5.0,
            "min_liquidation_percentile": 0.90, "allowed_sessions": ["europe", "us"],
            "min_stop_distance_pct": 0.0075, "max_stop_distance_pct": 0.015,
            "target_policy": "fixed_r", "target_r": [0.80, 1.35],
        },
        "MEDIUM_DEEP_R_EXTENDED": {
            "enabled": False,
            "profile_id": "crypto_fast_flush_medium_deep_r_extended_paper_v1",
            "description": "Medium-deep 5m flush; fixed TP1 1.00R / TP2 1.75R",
            "activation_at": "2026-09-29T16:30:45+00:00",
            "confirmation_timeframe": "1m", "hold_bars": 1,
            "confirmation_window_bars": 8, "require_green": True,
            "require_progress": False, "max_holding_bars": 45,
            "min_flush_atr": 2.0, "max_flush_atr": 5.0,
            "min_flush_pct": 1.5, "max_flush_pct": 2.75,
            "min_rvol": 1.0, "min_oi_drop_pct": 0.25, "max_oi_drop_pct": 5.0,
            "min_liquidation_percentile": 0.90, "allowed_sessions": ["europe", "us"],
            "min_stop_distance_pct": 0.0075, "max_stop_distance_pct": 0.015,
            "target_policy": "fixed_r", "target_r": [1.00, 1.75],
        },
        "MEDIUM_DEEP_STRUCTURE_HYBRID": {
            "enabled": False,
            "profile_id": "crypto_fast_flush_medium_deep_structure_hybrid_paper_v1",
            "description": "Medium-deep 5m flush; bounded 4h VWAP / pre-flush-close targets",
            "activation_at": "2026-09-29T16:30:45+00:00",
            "confirmation_timeframe": "1m", "hold_bars": 1,
            "confirmation_window_bars": 8, "require_green": True,
            "require_progress": False, "max_holding_bars": 45,
            "min_flush_atr": 2.0, "max_flush_atr": 5.0,
            "min_flush_pct": 1.5, "max_flush_pct": 2.75,
            "min_rvol": 1.0, "min_oi_drop_pct": 0.25, "max_oi_drop_pct": 5.0,
            "min_liquidation_percentile": 0.90, "allowed_sessions": ["europe", "us"],
            "min_stop_distance_pct": 0.0075, "max_stop_distance_pct": 0.015,
            "target_policy": "structure_hybrid_vwap_previous_close",
            "vwap_lookback_minutes": 240,
            "tp1_r_floor": 0.60, "tp1_r_cap": 1.00, "tp1_fallback_r": 0.80,
            "tp2_r_floor": 1.10, "tp2_r_cap": 1.80, "tp2_fallback_r": 1.35,
        },
    },
    "min_clean_closed": 30,
    "min_forward_days": 28,
    "min_profit_factor": 1.20,
    "max_review_drawdown_usd": 250.0,
    "report_path": "reports/CRYPTO_FAST_FLUSH_RECLAIM_V3_PAPER.md",
}

OUTCOME_TABLE = "crypto_fast_flush_reclaim_v3_paper_outcomes"
OBS_TABLE = "crypto_fast_flush_reclaim_v3_paper_observations"
EVAL_TABLE = "crypto_fast_flush_reclaim_v3_paper_evaluations"
META_TABLE = "crypto_fast_flush_reclaim_v3_paper_meta"
_FRAME_REFRESH_BUCKETS: dict[tuple[str, str], datetime] = {}

OUTCOME_DDL = f"""
CREATE TABLE IF NOT EXISTS {OUTCOME_TABLE} (
  candidate_id TEXT PRIMARY KEY, raw_event_id TEXT NOT NULL,
  strategy_id TEXT NOT NULL, profile_id TEXT NOT NULL, paper_lane TEXT NOT NULL,
  window TEXT NOT NULL, generated_at TEXT NOT NULL, decision_at TEXT NOT NULL,
  sweep_at TEXT NOT NULL, symbol TEXT NOT NULL, direction TEXT NOT NULL,
  entry_profile TEXT NOT NULL, confirmation_timeframe TEXT NOT NULL,
  session_bucket TEXT, liquidation_notional_usd REAL, liquidation_percentile REAL,
  oi_change_pct REAL, spread_bps REAL, flush_atr REAL, flush_pct REAL, rvol REAL,
  reclaim_level REAL, sweep_extreme REAL, eligibility_status TEXT NOT NULL,
  rejection_reason TEXT, data_status TEXT, is_clean_for_edge INTEGER NOT NULL DEFAULT 0,
  entry_ts TEXT, entry_price REAL, stop_price REAL, tp1 REAL, tp2 REAL,
  outcome_status TEXT NOT NULL, close_reason TEXT, exit_price REAL, exit_ts TEXT,
  gross_pnl_usd REAL, net_pnl_usd REAL, net_r REAL, fees_usd REAL,
  slippage_usd REAL, risk_usd REAL, mfe_r REAL, mae_r REAL,
  highest_tp_touched INTEGER, bars_held INTEGER, latency_seconds REAL,
  features_json TEXT, notes_json TEXT, last_checked_at TEXT
)
"""

OBS_DDL = f"""
CREATE TABLE IF NOT EXISTS {OBS_TABLE} (
  observation_id TEXT PRIMARY KEY, raw_event_id TEXT NOT NULL,
  evaluated_at TEXT NOT NULL, decision_at TEXT NOT NULL, symbol TEXT NOT NULL,
  rejection_reason TEXT NOT NULL, features_json TEXT, notes_json TEXT
)
"""

EVAL_DDL = f"""
CREATE TABLE IF NOT EXISTS {EVAL_TABLE} (
  generated_at TEXT NOT NULL, profile_id TEXT NOT NULL, clean_closed INTEGER,
  net_pnl_usd REAL, profit_factor REAL, winrate REAL, max_drawdown_usd REAL,
  forward_days REAL, verdict TEXT, config_json TEXT,
  PRIMARY KEY(generated_at, profile_id)
)
"""


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    out = dict(base)
    for key, value in override.items():
        out[key] = _deep_merge(dict(out[key]), value) if isinstance(value, dict) and isinstance(out.get(key), dict) else value
    return out


def load_strategy_config() -> dict[str, Any]:
    return _deep_merge(DEFAULTS, load_yaml_block(CONFIG_PATH, STRATEGY_KEY, DEFAULTS))


def active_confirmation_profiles(cfg: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Return only profiles that are allowed to consume forward resources."""
    return {
        str(name): dict(profile)
        for name, profile in dict(cfg.get("confirmation_profiles") or {}).items()
        if bool(profile.get("enabled", True))
    }


def _profile_activation_allows(setup: dict[str, Any], profile: dict[str, Any]) -> bool:
    activation = _dt(profile.get("activation_at"))
    decision_at = _dt(setup.get("decision_at"))
    return not (activation and decision_at and decision_at < activation)


def ensure_tables(conn: sqlite3.Connection) -> None:
    db_row = conn.execute("PRAGMA database_list").fetchone()
    db_path = str(db_row[2] if db_row and len(db_row) > 2 else "")
    db_key = db_path or f":memory:{id(conn)}"
    if db_key in _SCHEMA_READY_DATABASES:
        return
    required = {OUTCOME_TABLE, OBS_TABLE, EVAL_TABLE, META_TABLE}
    existing = {
        str(row[0]) for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
    }
    required_indexes = {"idx_ffr_v3_state", "idx_ffr_v3_profile", "idx_ffr_v3_symbol"}
    indexes = {
        str(row[0]) for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='index'"
        ).fetchall()
    }
    if required.issubset(existing) and required_indexes.issubset(indexes):
        _SCHEMA_READY_DATABASES.add(db_key)
        return
    conn.execute(OUTCOME_DDL)
    conn.execute(OBS_DDL)
    conn.execute(EVAL_DDL)
    conn.execute(f"CREATE TABLE IF NOT EXISTS {META_TABLE} (k TEXT PRIMARY KEY,v TEXT NOT NULL)")
    conn.execute(f"CREATE INDEX IF NOT EXISTS idx_ffr_v3_state ON {OUTCOME_TABLE}(outcome_status,entry_ts)")
    conn.execute(f"CREATE INDEX IF NOT EXISTS idx_ffr_v3_profile ON {OUTCOME_TABLE}(profile_id,outcome_status)")
    conn.execute(f"CREATE INDEX IF NOT EXISTS idx_ffr_v3_symbol ON {OUTCOME_TABLE}(symbol,decision_at)")
    _SCHEMA_READY_DATABASES.add(db_key)


def _f(value: Any) -> float | None:
    try:
        return None if value in (None, "") or pd.isna(value) else float(value)
    except (TypeError, ValueError):
        return None


def _dt(value: Any) -> datetime | None:
    parsed = parse_dt(value)
    return parsed.astimezone(timezone.utc) if parsed else None


def _canon(symbol: str) -> str:
    return sweep_v1._canon(symbol)  # noqa: SLF001


def _session(at: datetime) -> str:
    return sweep_v1._session(at)  # noqa: SLF001


def _minutes(timeframe: str) -> int:
    return reclaim_v2._minutes(timeframe)  # noqa: SLF001


def _atr(frame: pd.DataFrame, idx: int, periods: int = 14) -> float | None:
    return sweep_v1._atr(frame, idx, periods)  # noqa: SLF001


def _id(prefix: str, *parts: Any) -> str:
    return prefix + hashlib.sha256("|".join(str(p) for p in parts).encode()).hexdigest()[:22]


def _raw_event_id(cfg: dict[str, Any], symbol: str, decision_at: datetime) -> str:
    return _id("cffr3e_", cfg["strategy_id"], _canon(symbol), decision_at.isoformat())


def _candidate_id(cfg: dict[str, Any], symbol: str, decision_at: datetime, profile_id: str) -> str:
    return _id("cffr3_", cfg["strategy_id"], _canon(symbol), decision_at.isoformat(), profile_id)


def _load_frame(symbol: str, timeframe: str, cfg: dict[str, Any]) -> pd.DataFrame:
    if timeframe == str(cfg.get("base_timeframe") or "5m"):
        legacy = dict(cfg)
        legacy["base_sweep_timeframe"] = timeframe
        return reclaim_v2._load_base_frame(symbol, legacy)  # noqa: SLF001
    return reclaim_v2._load_confirmation_frame(symbol, timeframe, cfg)  # noqa: SLF001


def _episode_percentile(conn: sqlite3.Connection, symbol: str, at: datetime,
                        notional: float, cfg: dict[str, Any]) -> tuple[float | None, int]:
    """Percentile versus prior one-minute SELL liquidation episodes only."""
    from src.data_collectors.market_intelligence_store import normalize_symbol

    start = at - timedelta(days=float(cfg.get("liquidation_percentile_lookback_days", 14)))
    rows = conn.execute(
        "SELECT SUM(notional_usd) n FROM liquidation_events "
        "WHERE normalized_symbol=? AND side='SELL' AND event_at>=? AND event_at<? "
        "GROUP BY substr(event_at,1,16)",
        (normalize_symbol(symbol), start.isoformat(), at.isoformat()),
    ).fetchall()
    values = sorted(float(row[0] or 0.0) for row in rows if float(row[0] or 0.0) > 0)
    if not values:
        return None, 0
    rank = sum(value <= notional for value in values) / len(values)
    return rank, len(values)


def _episode_percentiles(
    conn: sqlite3.Connection,
    episodes_by_symbol: dict[str, list[tuple[datetime, list[dict[str, Any]], float]]],
    cfg: dict[str, Any],
) -> dict[tuple[str, str], tuple[float | None, int]]:
    """Fetch percentile history in one indexed query, then rank in memory."""
    from src.data_collectors.market_intelligence_store import normalize_symbol

    if not episodes_by_symbol:
        return {}
    lookback = float(cfg.get("liquidation_percentile_lookback_days", 14))
    symbols = {normalize_symbol(symbol): symbol for symbol in episodes_by_symbol}
    decisions = [decision_at for episodes in episodes_by_symbol.values()
                 for decision_at, _events, _notional in episodes]
    earliest = min(decisions) - timedelta(days=lookback)
    latest = max(decisions)
    placeholders = ",".join("?" for _ in symbols)
    rows = conn.execute(
        "SELECT normalized_symbol,substr(event_at,1,16) minute,SUM(notional_usd) n "
        "FROM liquidation_events WHERE normalized_symbol IN (" + placeholders + ") "
        "AND side='SELL' AND event_at>=? AND event_at<? "
        "GROUP BY normalized_symbol,substr(event_at,1,16)",
        (*symbols.keys(), earliest.isoformat(), latest.isoformat()),
    ).fetchall()
    history: dict[str, list[tuple[str, float]]] = {}
    for row in rows:
        value = float(row["n"] or 0.0)
        if value > 0:
            history.setdefault(str(row["normalized_symbol"]), []).append(
                (str(row["minute"]), value),
            )
    for values in history.values():
        values.sort(key=lambda item: item[0])

    result: dict[tuple[str, str], tuple[float | None, int]] = {}
    for normalized, symbol in symbols.items():
        symbol_history = history.get(normalized, [])
        for decision_at, _events, notional in episodes_by_symbol[symbol]:
            start_minute = (decision_at - timedelta(days=lookback)).strftime("%Y-%m-%dT%H:%M")
            decision_minute = decision_at.strftime("%Y-%m-%dT%H:%M")
            values = [value for minute, value in symbol_history
                      if start_minute <= minute < decision_minute]
            count = len(values)
            percentile = (sum(value <= notional for value in values) / count) if count else None
            result[(symbol, decision_at.isoformat())] = (percentile, count)
    return result


def _recent_event_rows(conn: sqlite3.Connection, symbol: str, now: datetime,
                       cfg: dict[str, Any]) -> list[dict[str, Any]]:
    """Load the whole recovery horizon once per symbol, not once per 5m bar."""
    from src.data_collectors.market_intelligence_store import normalize_symbol

    exchanges = [str(value).lower() for value in cfg.get("liquidation_sources") or []]
    if not exchanges:
        return []
    minutes = 5 * int(cfg.get("recent_scan_bars", 5)) + int(cfg.get("liquidation_window_minutes", 5))
    start = (now - timedelta(minutes=minutes)).isoformat()
    placeholders = ",".join("?" for _ in exchanges)
    rows = conn.execute(
        "SELECT exchange,event_id,event_at,side,notional_usd FROM liquidation_events "
        f"WHERE normalized_symbol=? AND exchange IN ({placeholders}) AND side='SELL' "
        "AND event_at>=? AND event_at<=?",
        (normalize_symbol(symbol), *exchanges, start, now.isoformat()),
    ).fetchall()
    return [dict(row) for row in rows]


def _recent_event_rows_by_symbol(
    conn: sqlite3.Connection, symbols: list[str], now: datetime, cfg: dict[str, Any],
) -> dict[str, list[dict[str, Any]]]:
    """Load recent liquidation tape for the whole universe in one indexed read."""
    from src.data_collectors.market_intelligence_store import normalize_symbol

    exchanges = [str(value).lower() for value in cfg.get("liquidation_sources") or []]
    normalized = list(dict.fromkeys(normalize_symbol(symbol) for symbol in symbols))
    if not exchanges or not normalized:
        return {}
    minutes = 5 * int(cfg.get("recent_scan_bars", 5)) + int(cfg.get("liquidation_window_minutes", 5))
    start = (now - timedelta(minutes=minutes)).isoformat()
    symbol_placeholders = ",".join("?" for _ in normalized)
    exchange_placeholders = ",".join("?" for _ in exchanges)
    rows = conn.execute(
        "SELECT normalized_symbol,exchange,event_id,event_at,side,notional_usd "
        "FROM liquidation_events WHERE normalized_symbol IN (" + symbol_placeholders + ") "
        "AND exchange IN (" + exchange_placeholders + ") AND side='SELL' "
        "AND event_at>=? AND event_at<=?",
        (*normalized, *exchanges, start, now.isoformat()),
    ).fetchall()
    by_normalized: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        item = dict(row)
        by_normalized.setdefault(str(item.pop("normalized_symbol")), []).append(item)
    return {
        symbol: by_normalized.get(normalize_symbol(symbol), [])
        for symbol in symbols
    }


def _connect_intelligence_readonly(db_path: str | Path | None = None) -> sqlite3.Connection:
    """Open the append-only market-intelligence DB without changing its pragmas."""
    from src.data_collectors.market_intelligence_store import default_db_path

    path = Path(db_path) if db_path else default_db_path()
    conn = sqlite3.connect(f"{path.resolve().as_uri()}?mode=ro", uri=True, timeout=1.5)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA query_only=ON")
    conn.execute("PRAGMA busy_timeout=1500")
    return conn


def _price_window_passes(frame: pd.DataFrame, idx: int, cfg: dict[str, Any]) -> bool:
    """Cheaply gate a normalized 5m candle before querying liquidation history."""
    if frame.empty or idx < 21:
        return False
    row = frame.iloc[idx]
    sweep_at = _dt(row.get("timestamp"))
    if sweep_at is None:
        return False
    decision_at = sweep_at + timedelta(minutes=5)
    open_, high, low, close, volume = (_f(row.get(k)) for k in ("open", "high", "low", "close", "volume"))
    prior_close = _f(frame.iloc[idx - 1].get("close"))
    atr = _atr(frame, idx - 1)
    if None in (open_, high, low, close, volume, prior_close, atr) or float(atr or 0) <= 0:
        return False
    span = float(high) - float(low)
    flush_atr = max(float(prior_close) - float(low), span) / float(atr)
    flush_pct = max(0.0, (float(prior_close) - float(low)) / float(prior_close) * 100.0)
    prior_volume = _f(frame.iloc[max(0, idx - 20):idx]["volume"].median()) or 0.0
    rvol = float(volume) / prior_volume if prior_volume else 0.0
    return (
        _session(decision_at) in set(cfg.get("allowed_sessions") or [])
        and float(cfg["min_flush_atr"]) <= flush_atr <= float(cfg["max_flush_atr"])
        and flush_pct >= float(cfg["min_flush_pct"])
        and rvol >= float(cfg["min_rvol"])
    )


def _candidate_price_windows(
    frame: pd.DataFrame, now: datetime, cfg: dict[str, Any],
) -> list[tuple[datetime, int]]:
    frame = normalize_frame(frame)
    if frame.empty:
        return []
    index_by_open = {pd.Timestamp(value): int(index)
                     for index, value in zip(frame.index, frame["timestamp"])}
    latest_decision = now.replace(minute=now.minute - now.minute % 5, second=0, microsecond=0)
    candidates: list[tuple[datetime, int]] = []
    for offset in range(int(cfg.get("recent_scan_bars", 5))):
        decision_at = latest_decision - timedelta(minutes=5 * offset)
        idx = index_by_open.get(pd.Timestamp(decision_at - timedelta(minutes=5)))
        if idx is not None and _price_window_passes(frame, idx, cfg):
            candidates.append((decision_at, idx))
    return candidates


def _fast_source_status(conn: sqlite3.Connection, cfg: dict[str, Any], now: datetime) -> dict[str, Any]:
    """Health-only status; avoid full-table COUNTs on the hot append-only tape."""
    wanted = [f"liquidations:{str(exchange).lower()}_ws"
              for exchange in cfg.get("liquidation_sources") or []]
    if not wanted:
        return {"status": "DISABLED", "feed_available": False, "sources": {}}
    placeholders = ",".join("?" for _ in wanted)
    rows = conn.execute(
        f"SELECT source,status,last_success_at,latest_provider_ts,error FROM intelligence_source_health "
        f"WHERE source IN ({placeholders})", wanted,
    ).fetchall()
    sources = {str(row["source"]): dict(row) for row in rows}
    cutoff = now - timedelta(minutes=15)
    active = [row for row in sources.values()
              if row.get("status") in {"ok", "degraded"}
              and (_dt(row.get("last_success_at")) or datetime.min.replace(tzinfo=timezone.utc)) >= cutoff]
    latest = max((str(row.get("latest_provider_ts") or "") for row in sources.values()), default=None)
    return {"status": "HEALTHY" if active else "STALE", "feed_available": bool(active),
            "transport_status": "ok" if active else "stale", "latest_event_at": latest,
            "event_count": None, "sources": sources}


def detect_flush(frame: pd.DataFrame, idx: int, events: list[dict[str, Any]],
                 context: dict[str, Any] | None, cfg: dict[str, Any],
                 *, liquidation_percentile: float | None = None,
                 liquidation_history_count: int = 0) -> dict[str, Any]:
    """Detect a downside impulse worth testing as a fast mean-reversion setup."""
    frame = normalize_frame(frame)
    if frame.empty or idx < 21:
        return {"ok": False, "reason": "CANDLES_MISSING"}
    row = frame.iloc[idx]
    sweep_at = _dt(row.get("timestamp"))
    if sweep_at is None:
        return {"ok": False, "reason": "CANDLES_MISSING"}
    decision_at = sweep_at + timedelta(minutes=5)
    open_, high, low, close, volume = (_f(row.get(k)) for k in ("open", "high", "low", "close", "volume"))
    prior_close = _f(frame.iloc[idx - 1].get("close"))
    atr = _atr(frame, idx - 1)
    if None in (open_, high, low, close, volume, prior_close, atr) or float(atr or 0) <= 0:
        return {"ok": False, "reason": "CANDLES_MISSING", "decision_at": decision_at}
    span = float(high) - float(low)
    flush_range = max(float(prior_close) - float(low), span)
    flush_atr = flush_range / float(atr)
    flush_pct = max(0.0, (float(prior_close) - float(low)) / float(prior_close) * 100.0)
    prior_volume = _f(frame.iloc[max(0, idx - 20):idx]["volume"].median()) or 0.0
    rvol = float(volume) / prior_volume if prior_volume else 0.0
    facts = {
        "decision_at": decision_at, "sweep_at": sweep_at, "direction": "long",
        "sweep_extreme": float(low), "sweep_close": float(close),
        "prior_close": float(prior_close), "atr": float(atr),
        "flush_atr": flush_atr, "flush_pct": flush_pct, "rvol": rvol,
    }
    if _session(decision_at) not in set(cfg.get("allowed_sessions") or []):
        return {**facts, "ok": False, "reason": "SESSION_NOT_ALLOWED"}
    if flush_atr < float(cfg["min_flush_atr"]):
        return {**facts, "ok": False, "reason": "FLUSH_TOO_SMALL"}
    if flush_atr > float(cfg["max_flush_atr"]):
        return {**facts, "ok": False, "reason": "UNCONTROLLED_CASCADE"}
    if flush_pct < float(cfg["min_flush_pct"]):
        return {**facts, "ok": False, "reason": "FLUSH_PCT_TOO_SMALL"}
    if rvol < float(cfg["min_rvol"]):
        return {**facts, "ok": False, "reason": "RVOL_TOO_WEAK"}
    matched = [event for event in events if str(event.get("side") or "").upper() == "SELL"]
    notional = sum(float(event.get("notional_usd") or 0.0) for event in matched)
    facts.update(liquidation_notional_usd=notional,
                 liquidation_percentile=liquidation_percentile,
                 liquidation_history_count=liquidation_history_count,
                 event_ids=[str(event.get("event_id") or "") for event in matched])
    if notional < float(cfg["min_liquidation_notional_usd"]):
        return {**facts, "ok": False, "reason": "LIQUIDATION_NOTIONAL_TOO_SMALL"}
    history_min = int(cfg.get("min_liquidation_history_episodes", 10))
    if liquidation_history_count >= history_min and (
        liquidation_percentile is None or liquidation_percentile < float(cfg["min_liquidation_percentile"])
    ):
        return {**facts, "ok": False, "reason": "LIQUIDATION_INTENSITY_TOO_LOW"}
    if context is None:
        return {**facts, "ok": False, "reason": "CONTEXT_REQUIRED"}
    if not context.get("ok"):
        return {**facts, "ok": False, "reason": str(context.get("reason") or "CONTEXT_MISSING")}
    oi_change = _f(context.get("oi_change_pct"))
    facts.update(oi_change_pct=oi_change, spread_bps=context.get("spread_bps"))
    if oi_change is None or oi_change > -float(cfg["min_oi_drop_pct"]):
        return {**facts, "ok": False, "reason": "OI_NOT_FLUSHING"}
    if oi_change < -float(cfg["max_oi_drop_pct"]):
        return {**facts, "ok": False, "reason": "OI_CASCADE_TOO_DEEP"}
    reclaim_level = float(low) + (float(prior_close) - float(low)) * float(cfg["reclaim_fraction"])
    stop = float(low) - float(atr) * float(cfg["stop_buffer_atr"])
    return {**facts, "ok": True, "reclaim_level": reclaim_level, "stop": stop}


def detect_confirmation(frame: pd.DataFrame, setup: dict[str, Any], now: datetime,
                        profile: dict[str, Any]) -> dict[str, Any]:
    timeframe = str(profile.get("confirmation_timeframe") or "1m")
    frame = normalize_frame(frame)
    if frame.empty:
        return {"status": "pending"}
    decision_at = _dt(setup.get("decision_at")) if not isinstance(setup.get("decision_at"), datetime) else setup["decision_at"]
    if decision_at is None:
        return {"status": "pending"}
    minutes = _minutes(timeframe)
    closed = frame[frame["timestamp"] + pd.Timedelta(minutes=minutes) <= pd.Timestamp(now)].copy()
    closed["_close_at"] = closed["timestamp"] + pd.Timedelta(minutes=minutes)
    end = decision_at + timedelta(minutes=minutes * int(profile.get("confirmation_window_bars", 8)))
    closed = closed[(closed["_close_at"] > pd.Timestamp(decision_at)) & (closed["_close_at"] <= pd.Timestamp(end))]
    level = float(setup["reclaim_level"])
    confirmation_mode = str(profile.get("confirmation_mode") or "").lower()
    if confirmation_mode == "higher_low_break_vol":
        sweep_extreme = _f(setup.get("sweep_extreme"))
        if sweep_extreme is None or minutes != 1:
            return {"status": "skipped", "reason": "CONFIRMATION_DATA_INVALID"}
        lookback = max(1, int(profile.get("confirmation_rvol_lookback_bars", 20)))
        min_history = max(1, int(profile.get("confirmation_min_history_bars", 5)))
        min_rvol = float(profile.get("confirmation_min_rvol", 1.20))
        for _, candle in closed.iterrows():
            open_, high, low, close, volume = (
                _f(candle.get(key)) for key in ("open", "high", "low", "close", "volume")
            )
            if None in (open_, high, low, close, volume):
                continue
            candle_at = pd.Timestamp(candle["timestamp"])
            position = int(frame["timestamp"].searchsorted(candle_at, side="left"))
            if position <= 0 or position >= len(frame):
                continue
            previous = frame.iloc[position - 1]
            previous_at = pd.Timestamp(previous["timestamp"])
            previous_high = _f(previous.get("high"))
            if (previous_high is None
                    or previous_at + pd.Timedelta(minutes=1) != candle_at):
                continue
            prior_volumes = pd.to_numeric(
                frame.iloc[max(0, position - lookback):position]["volume"], errors="coerce",
            ).dropna()
            if len(prior_volumes) < min_history:
                continue
            median_volume = float(prior_volumes.median())
            if median_volume <= 0:
                continue
            rvol = float(volume) / median_volume
            close_location = (float(close) - float(low)) / max(float(high) - float(low), 1e-12)
            valid = (
                float(close) > float(open_)
                and float(close) >= level
                and float(low) > float(sweep_extreme)
                and float(close) > float(previous_high)
                and close_location >= 0.65
                and rvol >= min_rvol
            )
            if not valid:
                continue
            close_at = _dt(candle["_close_at"])
            if close_at is None:
                continue
            return {
                "status": "entry", "entry": float(close), "entry_at": close_at,
                "confirmation_bars": 1, "confirmation_rvol": rvol,
                "previous_high": float(previous_high), "close_location": close_location,
                "sweep_extreme": float(sweep_extreme),
            }
        if now >= end:
            return {"status": "skipped", "reason": "RECLAIM_WINDOW_EXPIRED"}
        return {"status": "pending"}

    holds: list[tuple[int, float, datetime]] = []
    previous_high: float | None = None
    for index, candle in closed.iterrows():
        open_, high, low, close = (_f(candle.get(k)) for k in ("open", "high", "low", "close"))
        if None in (open_, high, low, close):
            continue
        green = float(close) > float(open_)
        upper_close = (float(close) - float(low)) / max(float(high) - float(low), 1e-12) >= 0.60
        valid = float(close) >= level and upper_close
        if profile.get("require_green", True):
            valid = valid and green
        if profile.get("require_progress") and previous_high is not None:
            valid = valid and float(close) > previous_high
        if not valid:
            holds = []
            previous_high = float(high)
            continue
        close_at = _dt(candle["_close_at"])
        if close_at is None:
            continue
        holds.append((int(index), float(close), close_at))
        previous_high = float(high)
        required = int(profile.get("hold_bars", 1))
        if len(holds) >= required:
            recent = holds[-required:]
            if required == 1 or all(recent[i][0] == recent[i - 1][0] + 1 for i in range(1, required)):
                return {"status": "entry", "entry": recent[-1][1], "entry_at": recent[-1][2],
                        "confirmation_bars": required}
    if now >= end:
        return {"status": "skipped", "reason": "RECLAIM_WINDOW_EXPIRED"}
    return {"status": "pending"}


def _rolling_vwap(frame: pd.DataFrame | None, entry_at: datetime | None,
                  lookback_minutes: int) -> float | None:
    if frame is None or entry_at is None:
        return None
    work = normalize_frame(frame)
    if work.empty:
        return None
    end = pd.Timestamp(entry_at)
    start = end - pd.Timedelta(minutes=max(1, int(lookback_minutes)))
    work = work[(work["timestamp"] < end) & (work["timestamp"] >= start)]
    if work.empty:
        return None
    volume = pd.to_numeric(work["volume"], errors="coerce").fillna(0.0)
    if float(volume.sum()) <= 0:
        return None
    typical = (
        pd.to_numeric(work["high"], errors="coerce")
        + pd.to_numeric(work["low"], errors="coerce")
        + pd.to_numeric(work["close"], errors="coerce")
    ) / 3.0
    return float((typical * volume).sum() / volume.sum())


def _bounded_target_r(raw_price: float | None, *, entry: float, risk: float,
                      floor: float, cap: float, fallback: float) -> tuple[float, float]:
    raw_r = fallback if raw_price is None or raw_price <= entry else (raw_price - entry) / risk
    bounded_r = min(max(raw_r, floor), cap)
    return entry + bounded_r * risk, bounded_r


def _target_prices(setup: dict[str, Any], entry: float, risk: float, cfg: dict[str, Any],
                   profile: dict[str, Any] | None = None,
                   frame: pd.DataFrame | None = None,
                   entry_at: datetime | None = None) -> tuple[list[float], dict[str, Any]]:
    profile = profile or {}
    policy = str(profile.get("target_policy") or "fixed_r").lower()
    if policy == "atr_multiple":
        atr = _f(setup.get("atr"))
        multiples = [float(value) for value in profile.get("target_atr") or [1.0, 2.0]]
        if atr is None or atr <= 0 or len(multiples) < 2:
            return [], {"target_policy": policy, "target_error": "ATR_UNAVAILABLE"}
        targets = [entry + atr * multiples[0], entry + atr * multiples[1]]
        return targets, {
            "target_policy": policy,
            "target_atr": multiples[:2],
            "target_r": [round((price - entry) / risk, 6) for price in targets],
        }
    if policy == "structure_hybrid_vwap_previous_close":
        vwap = _rolling_vwap(frame, entry_at, int(profile.get("vwap_lookback_minutes", 240)))
        tp1, tp1_r = _bounded_target_r(
            vwap, entry=entry, risk=risk,
            floor=float(profile.get("tp1_r_floor", 0.60)),
            cap=float(profile.get("tp1_r_cap", 1.00)),
            fallback=float(profile.get("tp1_fallback_r", 0.80)),
        )
        prior_close = _f(setup.get("prior_close"))
        tp2, tp2_r = _bounded_target_r(
            prior_close, entry=entry, risk=risk,
            floor=float(profile.get("tp2_r_floor", 1.10)),
            cap=float(profile.get("tp2_r_cap", 1.80)),
            fallback=float(profile.get("tp2_fallback_r", 1.35)),
        )
        if tp2 <= tp1:
            tp2_r = min(float(profile.get("tp2_r_cap", 1.80)), max(
                float(profile.get("tp2_r_floor", 1.10)), tp1_r + 0.20,
            ))
            tp2 = entry + tp2_r * risk
        return [tp1, tp2], {
            "target_policy": policy, "vwap": vwap, "prior_close": prior_close,
            "target_r": [round(tp1_r, 6), round(tp2_r, 6)],
        }
    target_r = [float(value) for value in profile.get("target_r") or cfg["target_r"]]
    return [entry + risk * value for value in target_r], {
        "target_policy": "fixed_r", "target_r": target_r,
    }


def entry_geometry(setup: dict[str, Any], entry: float, cfg: dict[str, Any],
                   *, profile: dict[str, Any] | None = None,
                   frame: pd.DataFrame | None = None,
                   entry_at: datetime | None = None) -> dict[str, Any]:
    stop = float(setup["stop"])
    risk = entry - stop
    if risk <= 0:
        return {"ok": False, "reason": "INVALID_STOP_GEOMETRY"}
    stop_pct = risk / entry
    if stop_pct < float(cfg["min_stop_distance_pct"]):
        return {"ok": False, "reason": "STOP_TOO_TIGHT_FOR_COSTS", "stop_distance_pct": round(stop_pct, 8)}
    if stop_pct > float(cfg["max_stop_distance_pct"]):
        return {"ok": False, "reason": "STOP_TOO_WIDE", "stop_distance_pct": round(stop_pct, 8)}
    targets, target_meta = _target_prices(
        setup, entry, risk, cfg, profile=profile, frame=frame, entry_at=entry_at,
    )
    if len(targets) < 2 or targets[0] <= entry or targets[1] <= targets[0]:
        return {"ok": False, "reason": str(target_meta.get("target_error") or "INVALID_TARGET_GEOMETRY")}
    return {"ok": True, "stop": stop, "tp1": targets[0], "tp2": targets[1],
            "risk": risk, "stop_distance_pct": round(stop_pct, 8), **target_meta}


def _profile_gate_reason(setup: dict[str, Any], profile: dict[str, Any]) -> str | None:
    checks = (
        ("flush_atr", "min_flush_atr", "max_flush_atr", "PROFILE_FLUSH_ATR"),
        ("flush_pct", "min_flush_pct", "max_flush_pct", "PROFILE_FLUSH_PCT"),
    )
    for value_key, minimum_key, maximum_key, reason in checks:
        value = _f(setup.get(value_key))
        minimum = _f(profile.get(minimum_key))
        maximum = _f(profile.get(maximum_key))
        if value is None or (minimum is not None and value < minimum) or (maximum is not None and value > maximum):
            return reason
    rvol = _f(setup.get("rvol"))
    if rvol is None or rvol < float(profile.get("min_rvol", 0.0)):
        return "PROFILE_RVOL"
    oi_change = _f(setup.get("oi_change_pct"))
    min_oi = _f(profile.get("min_oi_drop_pct"))
    max_oi = _f(profile.get("max_oi_drop_pct"))
    if oi_change is None or (min_oi is not None and oi_change > -min_oi) or (max_oi is not None and oi_change < -max_oi):
        return "PROFILE_OI_RANGE"
    percentile = _f(setup.get("liquidation_percentile"))
    if percentile is None or percentile < float(profile.get("min_liquidation_percentile", 0.0)):
        return "PROFILE_LIQUIDATION_PERCENTILE"
    if _session(setup["decision_at"]) not in set(profile.get("allowed_sessions") or []):
        return "PROFILE_SESSION"
    return None


def simulate_two_target(*, entry: float, stop: float, tp1: float, tp2: float,
                        candles: pd.DataFrame, symbol: str, cfg: dict[str, Any],
                        bar_minutes: int, force_close: bool = True) -> dict[str, Any]:
    frame = normalize_frame(candles)
    if frame.empty:
        return {"outcome_status": "open"}
    risk_distance = entry - stop
    if risk_distance <= 0:
        return {"outcome_status": "skipped", "close_reason": "invalid_geometry"}
    fractions = [float(value) for value in cfg.get("target_fractions") or [0.7, 0.3]]
    target_r = [(tp1 - entry) / risk_distance, (tp2 - entry) / risk_distance]
    remaining, gross_r, highest = 1.0, 0.0, 0
    mfe, mae, bars = 0.0, 0.0, 0
    active_stop = stop
    exits: list[tuple[float, float, str]] = []
    exit_ts: datetime | None = None
    close_reason: str | None = None
    for _, candle in frame.iterrows():
        high, low, close = (_f(candle.get(k)) for k in ("high", "low", "close"))
        if None in (high, low, close):
            continue
        bars += 1
        candle_at = _dt(candle.get("timestamp"))
        candle_close = candle_at + timedelta(minutes=bar_minutes) if candle_at else None
        if float(low) <= active_stop:
            stop_r = (active_stop - entry) / risk_distance
            gross_r += remaining * stop_r
            exits.append((remaining, active_stop, "taker"))
            remaining = 0.0
            exit_ts = candle_close
            close_reason = "breakeven_stop" if math.isclose(active_stop, entry) else "original_stop"
            break
        mfe = max(mfe, (float(high) - entry) / risk_distance)
        mae = min(mae, (float(low) - entry) / risk_distance)
        if highest < 1 and float(high) >= tp1:
            fraction = min(fractions[0], remaining)
            gross_r += fraction * target_r[0]
            exits.append((fraction, tp1, "maker"))
            remaining -= fraction
            highest = 1
            exit_ts = candle_close
        if highest < 2 and float(high) >= tp2:
            fraction = remaining
            gross_r += fraction * target_r[1]
            exits.append((fraction, tp2, "maker"))
            remaining = 0.0
            highest = 2
            exit_ts = candle_close
            close_reason = "tp2"
            break
        if highest >= 1 and cfg.get("move_stop_to_entry_after_tp1", True):
            active_stop = entry
    if remaining > 1e-9:
        if not force_close:
            return {"outcome_status": "open", "net_r": round(gross_r, 4),
                    "mfe_r": round(mfe, 4), "mae_r": round(mae, 4),
                    "highest_tp_touched": highest, "bars_held": bars}
        last = frame.iloc[-1]
        final = float(last["close"])
        gross_r += remaining * ((final - entry) / risk_distance)
        exits.append((remaining, final, "taker"))
        remaining = 0.0
        candle_at = _dt(last.get("timestamp"))
        exit_ts = candle_at + timedelta(minutes=bar_minutes) if candle_at else None
        close_reason = "time_exit"
    risk_usd = float(cfg.get("fixed_risk_usd", 10.0))
    qty = risk_usd / risk_distance
    notional = qty * entry
    weighted_exit = sum(frac * price for frac, price, _ in exits)
    costs = trade_costs(
        notional_usdt=notional, exit_notional_usdt=qty * weighted_exit,
        symbol=symbol, fee_profile=str(cfg["fee_profile"]), entry_order_type="taker",
        exit_order_type="taker", exit_slices=[(frac, order_type) for frac, _, order_type in exits],
    )
    gross = gross_r * risk_usd
    return {
        "outcome_status": "closed", "close_reason": close_reason,
        "exit_price": round(weighted_exit, 10),
        "exit_ts": exit_ts.isoformat() if exit_ts else None,
        "gross_pnl_usd": round(gross, 4),
        "net_pnl_usd": round(gross - costs.total_cost_usdt, 4),
        "net_r": round(gross_r - costs.total_cost_usdt / risk_usd, 4),
        "fees_usd": costs.fee_usdt, "slippage_usd": costs.slippage_usdt,
        "risk_usd": risk_usd, "mfe_r": round(mfe, 4), "mae_r": round(mae, 4),
        "highest_tp_touched": highest, "bars_held": bars,
    }


def _activation(conn: sqlite3.Connection, now: datetime, persist: bool) -> datetime:
    row = conn.execute(f"SELECT v FROM {META_TABLE} WHERE k='activated_at'").fetchone()
    activated = _dt(row[0]) if row else None
    if activated:
        return activated
    if persist:
        conn.execute(f"INSERT OR REPLACE INTO {META_TABLE}(k,v) VALUES('activated_at',?)", (now.isoformat(),))
    return now


def _row(cfg: dict[str, Any], symbol: str, setup: dict[str, Any], profile_name: str,
         profile: dict[str, Any], now: datetime, status: str, reason: str | None) -> dict[str, Any]:
    decision_at = setup["decision_at"]
    profile_id = str(profile["profile_id"])
    return {
        "candidate_id": _candidate_id(cfg, symbol, decision_at, profile_id),
        "raw_event_id": _raw_event_id(cfg, symbol, decision_at),
        "strategy_id": cfg["strategy_id"], "profile_id": profile_id,
        "paper_lane": cfg["paper_lane"], "window": "forward_post_activation",
        "generated_at": now.isoformat(), "decision_at": decision_at.isoformat(),
        "sweep_at": setup["sweep_at"].isoformat(), "symbol": _canon(symbol), "direction": "long",
        "entry_profile": profile_name,
        "confirmation_timeframe": str(profile["confirmation_timeframe"]),
        "session_bucket": _session(decision_at),
        "liquidation_notional_usd": setup.get("liquidation_notional_usd"),
        "liquidation_percentile": setup.get("liquidation_percentile"),
        "oi_change_pct": setup.get("oi_change_pct"), "spread_bps": setup.get("spread_bps"),
        "flush_atr": setup.get("flush_atr"), "flush_pct": setup.get("flush_pct"),
        "rvol": setup.get("rvol"), "reclaim_level": setup.get("reclaim_level"),
        "sweep_extreme": setup.get("sweep_extreme"), "eligibility_status": status,
        "rejection_reason": reason, "data_status": "ok" if status == "eligible" else "pending" if status == "pending" else "dirty",
        "is_clean_for_edge": int(status == "eligible"),
        "outcome_status": "open" if status == "eligible" else "pending" if status == "pending" else "skipped",
        "features_json": json_text({key: setup.get(key) for key in (
            "prior_close", "atr", "flush_atr", "flush_pct", "rvol", "liquidation_history_count")}),
        "notes_json": json_text({"paper_only": True, "live_locked": True,
                                 "entry_logic": "5m flush -> liquidation/OI gate -> closed reclaim",
                                 "profile_description": profile.get("description"),
                                 "target_policy": profile.get("target_policy") or "fixed_r",
                                 "target_r": profile.get("target_r") or cfg.get("target_r")}),
        "last_checked_at": now.isoformat(),
    }


def _upsert(conn: sqlite3.Connection, row: dict[str, Any]) -> None:
    columns = [item[1] for item in conn.execute(f"PRAGMA table_info({OUTCOME_TABLE})")]
    values = [row.get(column) for column in columns]
    updates = ",".join(f"{column}=excluded.{column}" for column in columns if column != "candidate_id")
    conn.execute(
        f"INSERT INTO {OUTCOME_TABLE}({','.join(columns)}) VALUES({','.join('?' for _ in columns)}) "
        f"ON CONFLICT(candidate_id) DO UPDATE SET {updates}", values,
    )


def _record_observation(conn: sqlite3.Connection, cfg: dict[str, Any], symbol: str,
                        setup: dict[str, Any], reason: str, now: datetime) -> None:
    decision_at = setup.get("decision_at")
    if not isinstance(decision_at, datetime):
        return
    raw_id = _raw_event_id(cfg, symbol, decision_at)
    obs_id = _id("cffr3o_", raw_id, reason)
    features = {key: setup.get(key) for key in (
        "flush_atr", "flush_pct", "rvol", "liquidation_notional_usd",
        "liquidation_percentile", "oi_change_pct", "spread_bps")}
    conn.execute(
        f"INSERT OR REPLACE INTO {OBS_TABLE} VALUES(?,?,?,?,?,?,?,?)",
        (obs_id, raw_id, now.isoformat(), decision_at.isoformat(), _canon(symbol), reason,
         json_text(features), json_text({"paper_only": True})),
    )


def _process_profile(conn: sqlite3.Connection, cfg: dict[str, Any], symbol: str,
                     setup: dict[str, Any], profile_name: str, profile: dict[str, Any],
                     now: datetime, persist: bool,
                     frame_cache: dict[tuple[str, str], pd.DataFrame] | None = None,
                     ) -> dict[str, Any] | None:
    cid = _candidate_id(cfg, symbol, setup["decision_at"], str(profile["profile_id"]))
    existing = conn.execute(f"SELECT * FROM {OUTCOME_TABLE} WHERE candidate_id=?", (cid,)).fetchone()
    if existing and existing["outcome_status"] not in {"pending"}:
        return None
    if not _profile_activation_allows(setup, profile):
        return None
    profile_reason = _profile_gate_reason(setup, profile)
    if profile_reason:
        row = _row(cfg, symbol, setup, profile_name, profile, now, "rejected", profile_reason)
        if persist:
            _upsert(conn, row)
        return row
    timeframe = str(profile["confirmation_timeframe"])
    cache_key = (_canon(symbol), timeframe)
    if frame_cache is not None and cache_key in frame_cache:
        frame = frame_cache[cache_key]
    else:
        frame = _load_frame(symbol, timeframe, cfg)
        if frame_cache is not None:
            frame_cache[cache_key] = frame
    confirmation = detect_confirmation(frame, setup, now, profile)
    if confirmation["status"] == "pending":
        row = _row(cfg, symbol, setup, profile_name, profile, now, "pending", None)
    elif confirmation["status"] == "skipped":
        row = _row(cfg, symbol, setup, profile_name, profile, now, "rejected", str(confirmation["reason"]))
    else:
        age = max(0.0, (now - confirmation["entry_at"]).total_seconds())
        if age > float(cfg["max_entry_latency_seconds"]):
            row = _row(cfg, symbol, setup, profile_name, profile, now, "rejected", "STALE_RECLAIM_ENTRY")
        else:
            geometry = entry_geometry(
                setup, float(confirmation["entry"]), cfg, profile=profile,
                frame=frame, entry_at=confirmation["entry_at"],
            )
            if geometry.get("ok"):
                stop_pct = float(geometry["stop_distance_pct"])
                if stop_pct < float(profile.get("min_stop_distance_pct", cfg["min_stop_distance_pct"])):
                    geometry = {"ok": False, "reason": "PROFILE_STOP_TOO_TIGHT"}
                elif stop_pct > float(profile.get("max_stop_distance_pct", cfg["max_stop_distance_pct"])):
                    geometry = {"ok": False, "reason": "PROFILE_STOP_TOO_WIDE"}
            if not geometry["ok"]:
                row = _row(cfg, symbol, setup, profile_name, profile, now, "rejected", str(geometry["reason"]))
            else:
                row = _row(cfg, symbol, setup, profile_name, profile, now, "eligible", None)
                row.update(entry_ts=confirmation["entry_at"].isoformat(), entry_price=confirmation["entry"],
                           stop_price=geometry["stop"], tp1=geometry["tp1"], tp2=geometry["tp2"],
                           latency_seconds=age)
                if confirmation.get("confirmation_rvol") is not None:
                    features = json.loads(row["features_json"] or "{}")
                    features["confirmation"] = {
                        key: confirmation.get(key) for key in (
                            "confirmation_rvol", "previous_high", "close_location", "sweep_extreme",
                        )
                    }
                    row["features_json"] = json_text(features)
                    notes = json.loads(row["notes_json"] or "{}")
                    notes["entry_logic"] = (
                        "5m liquidation flush -> strict OI/intensity gates -> 1m reclaim, "
                        "higher low, prior-high break and RVOL confirmation"
                    )
                    notes["confirmation_rvol_min"] = profile.get("confirmation_min_rvol")
                    row["notes_json"] = json_text(notes)
    if persist:
        _upsert(conn, row)
    return row


def _expire_stale_pending(conn: sqlite3.Connection, cfg: dict[str, Any], now: datetime,
                          *, persist: bool) -> int:
    """Close confirmation records whose bounded reclaim window has elapsed.

    A pending setup can fall out of the recent liquidation-event scan after a
    monitor restart. It must still become a terminal rejection rather than
    remain pending forever and distort the forward sample.
    """
    profiles = dict(cfg.get("confirmation_profiles") or {})
    rows = conn.execute(
        f"SELECT candidate_id,entry_profile,decision_at,confirmation_timeframe "
        f"FROM {OUTCOME_TABLE} WHERE outcome_status='pending'"
    ).fetchall()
    expired = 0
    for row in rows:
        profile = profiles.get(str(row["entry_profile"]))
        decision_at = _dt(row["decision_at"])
        if decision_at is None:
            continue
        timeframe = str((profile or {}).get("confirmation_timeframe")
                        or row["confirmation_timeframe"] or "1m")
        window_bars = int((profile or {}).get("confirmation_window_bars") or 8)
        deadline = decision_at + timedelta(minutes=_minutes(timeframe) * window_bars)
        if now < deadline:
            continue
        expired += 1
        if persist:
            conn.execute(
                f"UPDATE {OUTCOME_TABLE} SET eligibility_status='rejected', "
                "rejection_reason='RECLAIM_WINDOW_EXPIRED', data_status='dirty', "
                "is_clean_for_edge=0, outcome_status='skipped', last_checked_at=? "
                "WHERE candidate_id=? AND outcome_status='pending'",
                (now.isoformat(), row["candidate_id"]),
            )
    return expired


def _mature_open(conn: sqlite3.Connection, cfg: dict[str, Any], now: datetime,
                 frame_cache: dict[tuple[str, str], pd.DataFrame] | None = None) -> int:
    profiles = active_confirmation_profiles(cfg)
    closed = 0
    for raw in conn.execute(f"SELECT * FROM {OUTCOME_TABLE} WHERE outcome_status='open'").fetchall():
        row = dict(raw)
        profile = profiles.get(row["entry_profile"])
        entry_at = _dt(row.get("entry_ts"))
        if not profile or entry_at is None:
            continue
        timeframe = str(profile["confirmation_timeframe"])
        cache_key = (_canon(str(row["symbol"])), timeframe)
        if frame_cache is not None and cache_key in frame_cache:
            frame = frame_cache[cache_key]
        else:
            frame = _load_frame(str(row["symbol"]), timeframe, cfg)
            if frame_cache is not None:
                frame_cache[cache_key] = frame
        future = frame[frame["timestamp"] >= pd.Timestamp(entry_at)]
        max_bars = int(profile["max_holding_bars"])
        if future.empty:
            continue
        sim = simulate_two_target(
            entry=float(row["entry_price"]), stop=float(row["stop_price"]),
            tp1=float(row["tp1"]), tp2=float(row["tp2"]), candles=future.iloc[:max_bars],
            symbol=str(row["symbol"]), cfg=cfg, bar_minutes=_minutes(timeframe),
            force_close=len(future) >= max_bars,
        )
        row.update(sim)
        row["last_checked_at"] = now.isoformat()
        _upsert(conn, row)
        closed += int(row.get("outcome_status") == "closed")
    return closed


def _refresh_candidate_frames(symbols: list[str], cfg: dict[str, Any],
                              now: datetime) -> dict[str, Any]:
    """Refresh only symbols that have a recent sweep or an open Paper trade.

    The broader derivatives collector remains on its normal cadence. This
    small event-driven refresh closes the gap between a 1m candle close and
    the next Paper decision without downloading the full universe every tick.
    """
    unique = list(dict.fromkeys(_canon(symbol) for symbol in symbols if symbol))
    unique = unique[:max(1, int(cfg.get("max_candidate_refresh_symbols", 12)))]
    if not cfg.get("refresh_candidate_ohlcv", True) or not unique:
        return {"attempted": 0, "fetched": 0, "failed": 0, "timeframes": {}}
    from concurrent.futures import ThreadPoolExecutor, as_completed
    from src.execution.crypto_derivreset_v3_shadow import _shadow_ohlcv_store

    due_by_timeframe: dict[str, tuple[list[str], datetime]] = {}
    for timeframe in sorted({
        str(cfg.get("base_timeframe") or "5m"),
        *(str(profile.get("confirmation_timeframe") or "1m")
          for profile in active_confirmation_profiles(cfg).values()),
    }):
        minutes = _minutes(timeframe)
        bucket = now.replace(
            minute=now.minute - now.minute % minutes, second=0, microsecond=0,
        )
        due = [symbol for symbol in unique
               if _FRAME_REFRESH_BUCKETS.get((symbol, timeframe)) != bucket]
        due_by_timeframe[timeframe] = (due, bucket)

    details: dict[str, dict[str, Any]] = {}
    with ThreadPoolExecutor(max_workers=max(1, len(due_by_timeframe)),
                            thread_name_prefix="fast-flush-bars") as pool:
        futures = {
            pool.submit(_refresh_bybit_public, due, timeframe): (timeframe, due, bucket)
            for timeframe, (due, bucket) in due_by_timeframe.items() if due
        }
        for timeframe, (due, _bucket) in due_by_timeframe.items():
            if not due:
                details[timeframe] = {
                    "attempted": 0, "fetched": 0, "failed": 0, "failed_symbols": [],
                }
        for future in as_completed(futures):
            timeframe, due, bucket = futures[future]
            try:
                frames, failed = future.result()
            except Exception as exc:  # noqa: BLE001 - public market-data boundary
                frames, failed = {}, {symbol: type(exc).__name__ for symbol in due}
            store = _shadow_ohlcv_store()
            fetched: list[str] = []
            for symbol, frame in frames.items():
                try:
                    store.save_ohlcv("bybit_linear", symbol, timeframe, frame)
                    fetched.append(symbol)
                except Exception as exc:  # noqa: BLE001 - isolated cache write
                    failed[symbol] = f"cache:{type(exc).__name__}"
            for symbol in fetched:
                _FRAME_REFRESH_BUCKETS[(symbol, timeframe)] = bucket
            details[timeframe] = {
                "attempted": len(due), "fetched": len(fetched), "failed": len(failed),
                "failed_symbols": sorted(failed)[:5],
            }
    return {
        "attempted": sum(item["attempted"] for item in details.values()),
        "fetched": sum(item["fetched"] for item in details.values()),
        "failed": sum(item["failed"] for item in details.values()),
        "timeframes": details,
    }


def _refresh_bybit_public(symbols: list[str], timeframe: str) -> tuple[dict[str, pd.DataFrame],
                                                                       dict[str, str]]:
    """Fetch candidate bars directly from Bybit without loading all markets."""
    from concurrent.futures import ThreadPoolExecutor, as_completed
    import requests
    from src.config import load_config

    interval = {"1m": "1", "3m": "3", "5m": "5", "15m": "15",
                "30m": "30", "1h": "60", "2h": "120", "4h": "240"}.get(timeframe)
    if interval is None:
        return {}, {symbol: "unsupported timeframe" for symbol in symbols}
    limit = min(1000, max(50, int(load_config().candle_limit(timeframe))))

    def fetch_one(symbol: str) -> tuple[str, pd.DataFrame | None, str | None]:
        native = f"{_canon(symbol).split('/', 1)[0]}USDT"
        try:
            response = requests.get(
                "https://api.bybit.com/v5/market/kline",
                params={"category": "linear", "symbol": native,
                        "interval": interval, "limit": limit},
                timeout=8,
            )
            response.raise_for_status()
            payload = response.json() or {}
            if int(payload.get("retCode", -1)) != 0:
                return symbol, None, str(payload.get("retMsg") or "Bybit rejected request")[:160]
            rows = ((payload.get("result") or {}).get("list") or [])
            if not rows:
                return symbol, None, "empty response"
            frame = pd.DataFrame(
                rows,
                columns=["timestamp", "open", "high", "low", "close", "volume", "turnover"],
            )
            frame["timestamp"] = pd.to_datetime(
                pd.to_numeric(frame["timestamp"], errors="coerce"), unit="ms", utc=True,
            )
            for column in ("open", "high", "low", "close", "volume"):
                frame[column] = pd.to_numeric(frame[column], errors="coerce")
            frame = frame.dropna(subset=["timestamp", "open", "high", "low", "close", "volume"])
            frame = frame[["timestamp", "open", "high", "low", "close", "volume"]]
            frame = frame.drop_duplicates("timestamp").sort_values("timestamp").reset_index(drop=True)
            return symbol, frame, None if not frame.empty else "all rows invalid"
        except Exception as exc:  # noqa: BLE001 - public market-data boundary
            return symbol, None, f"{type(exc).__name__}: {str(exc)[:120]}"

    frames: dict[str, pd.DataFrame] = {}
    failed: dict[str, str] = {}
    with ThreadPoolExecutor(max_workers=min(6, max(1, len(symbols))),
                            thread_name_prefix=f"bybit-{timeframe}") as pool:
        futures = [pool.submit(fetch_one, symbol) for symbol in symbols]
        for future in as_completed(futures):
            symbol, frame, error = future.result()
            if frame is not None and not frame.empty:
                frames[symbol] = frame
            else:
                failed[symbol] = error or "unknown error"
    return frames, failed


def tick(*, db: str | None = None, persist: bool = True, now: datetime | None = None,
         cfg: dict[str, Any] | None = None) -> dict[str, Any]:
    tick_started = time.perf_counter()
    live_clock = now is None
    cfg, now = cfg or load_strategy_config(), now or utc_now()
    if not cfg.get("feature_flag"):
        return {"enabled": False, "rows": [], "summary_by_profile": {}}
    from src.config import load_config
    path = Path(db) if db else load_config().db_path
    # The lane runs every 15 seconds. A bounded lock wait lets the next
    # idempotent tick replay recent episodes instead of repeating a full scan.
    trading = sqlite3.connect(path, timeout=1.5)
    trading.row_factory = sqlite3.Row
    trading.execute("PRAGMA busy_timeout=1500")
    intelligence = _connect_intelligence_readonly()
    try:
        timings_ms: dict[str, float] = {}
        funnel: dict[str, Any] = {
            "symbols_scanned": 0,
            "symbols_with_recent_liquidations": 0,
            "event_windows_examined": 0,
            "windows_over_min_liquidation": 0,
            "base_flush_pass": 0,
            "base_rejections": {},
            "missing_base_frames": 0,
            "profile_results": {},
        }

        def count_reason(bucket: dict[str, int], reason: str) -> None:
            bucket[reason] = bucket.get(reason, 0) + 1

        frame_cache: dict[tuple[str, str], pd.DataFrame] = {}
        phase_started = time.perf_counter()
        ensure_tables(trading)
        activated = _activation(trading, now, persist)
        if persist:
            trading.commit()
        timings_ms["database_setup"] = round((time.perf_counter() - phase_started) * 1000, 1)

        phase_started = time.perf_counter()
        source = _fast_source_status(intelligence, cfg, now)
        timings_ms["liquidation_feed_health"] = round((time.perf_counter() - phase_started) * 1000, 1)
        phase_started = time.perf_counter()
        symbols = reclaim_v2._symbols(intelligence, now, cfg)  # noqa: SLF001
        funnel["symbols_scanned"] = len(symbols)
        timings_ms["universe_selection"] = round((time.perf_counter() - phase_started) * 1000, 1)

        phase_started = time.perf_counter()
        open_symbols = [str(row[0]) for row in trading.execute(
            f"SELECT DISTINCT symbol FROM {OUTCOME_TABLE} WHERE outcome_status='open'"
        ).fetchall()]
        previously_open_ids = [str(row[0]) for row in trading.execute(
            f"SELECT candidate_id FROM {OUTCOME_TABLE} WHERE outcome_status='open'"
        ).fetchall()]
        price_windows: dict[str, list[tuple[datetime, int]]] = {}
        candle_load_ms = 0.0
        scan_bars = int(cfg.get("recent_scan_bars", 5))
        funnel["event_windows_examined"] = len(symbols) * scan_bars
        for symbol in symbols:
            frame_key = (_canon(symbol), "5m")
            load_started = time.perf_counter()
            frame_cache[frame_key] = _load_frame(symbol, "5m", cfg)
            candle_load_ms += (time.perf_counter() - load_started) * 1000
            if frame_cache[frame_key].empty:
                funnel["missing_base_frames"] += 1
                continue
            candidates = _candidate_price_windows(frame_cache[frame_key], now, cfg)
            if candidates:
                price_windows[symbol] = candidates
        funnel["price_candidate_windows"] = sum(len(items) for items in price_windows.values())
        timings_ms["base_candle_load"] = round(candle_load_ms, 1)
        timings_ms["price_candidate_scan"] = round((time.perf_counter() - phase_started) * 1000, 1)

        phase_started = time.perf_counter()
        candidate_refresh = _refresh_candidate_frames(
            [*open_symbols, *price_windows.keys()], cfg, now,
        )
        for symbol in list(price_windows):
            frame_key = (_canon(symbol), "5m")
            frame_cache[frame_key] = _load_frame(symbol, "5m", cfg)
            refreshed_candidates = _candidate_price_windows(frame_cache[frame_key], now, cfg)
            if refreshed_candidates:
                price_windows[symbol] = refreshed_candidates
            else:
                del price_windows[symbol]
        timings_ms["candidate_frame_refresh"] = round((time.perf_counter() - phase_started) * 1000, 1)

        phase_started = time.perf_counter()
        episodes_by_symbol: dict[str, list[tuple[datetime, list[dict[str, Any]], float]]] = {}
        recent_by_symbol = _recent_event_rows_by_symbol(
            intelligence, list(price_windows), now, cfg,
        )
        funnel["symbols_with_recent_liquidations"] = sum(bool(rows) for rows in recent_by_symbol.values())
        for symbol, candidates in price_windows.items():
            recent_events = recent_by_symbol.get(symbol, [])
            if not recent_events:
                continue
            episodes: list[tuple[datetime, list[dict[str, Any]], float]] = []
            for decision_at, _idx in candidates:
                start_at = decision_at - timedelta(minutes=float(cfg["liquidation_window_minutes"]))
                events = [event for event in recent_events
                          if (event_at := _dt(event.get("event_at"))) is not None
                          and start_at <= event_at <= decision_at]
                notional = sum(float(event.get("notional_usd") or 0.0) for event in events
                               if str(event.get("side") or "").upper() == "SELL")
                if notional >= float(cfg["min_liquidation_notional_usd"]):
                    funnel["windows_over_min_liquidation"] += 1
                    episodes.append((decision_at, events, notional))
            if episodes:
                episodes_by_symbol[symbol] = episodes
        funnel["price_candidate_windows"] = sum(len(items) for items in price_windows.values())
        timings_ms["liquidation_tape_read"] = round((time.perf_counter() - phase_started) * 1000, 1)

        phase_started = time.perf_counter()
        percentile_by_episode = _episode_percentiles(intelligence, episodes_by_symbol, cfg)
        timings_ms["liquidation_percentiles"] = round((time.perf_counter() - phase_started) * 1000, 1)

        phase_started = time.perf_counter()
        matured = _mature_open(trading, cfg, now, frame_cache)
        expired_pending = _expire_stale_pending(trading, cfg, now, persist=persist)
        if persist:
            trading.commit()
        timings_ms["refresh_and_mature"] = round((time.perf_counter() - phase_started) * 1000, 1)

        phase_started = time.perf_counter()
        inserted: list[dict[str, Any]] = []
        context_ms = 0.0
        for symbol, episodes in episodes_by_symbol.items():
            frame_key = (_canon(symbol), "5m")
            if frame_key not in frame_cache:
                frame_cache[frame_key] = _load_frame(symbol, "5m", cfg)
            frame = frame_cache[frame_key]
            if frame.empty:
                funnel["missing_base_frames"] += len(episodes)
                continue
            for decision_at, events, notional in episodes:
                sweep_at = decision_at - timedelta(minutes=5)
                indices = frame.index[frame["timestamp"] == pd.Timestamp(sweep_at)].tolist()
                if not indices:
                    continue
                idx = int(indices[-1])
                percentile, history_count = percentile_by_episode.get(
                    (symbol, decision_at.isoformat()), (None, 0),
                )
                setup = detect_flush(frame, idx, events, None, cfg,
                                     liquidation_percentile=percentile,
                                     liquidation_history_count=history_count)
                if setup.get("reason") == "CONTEXT_REQUIRED":
                    context_started = time.perf_counter()
                    context = sweep_v1._contexts(
                        intelligence, symbol, decision_at, cfg,
                    )  # noqa: SLF001
                    context_ms += (time.perf_counter() - context_started) * 1000
                    setup = detect_flush(frame, idx, events, context, cfg,
                                         liquidation_percentile=percentile,
                                         liquidation_history_count=history_count)
                if not setup.get("ok"):
                    count_reason(funnel["base_rejections"], str(setup.get("reason") or "UNKNOWN"))
                    if setup.get("decision_at") and setup.get("reason") not in {"FLUSH_TOO_SMALL", "FLUSH_PCT_TOO_SMALL"}:
                        _record_observation(trading, cfg, symbol, setup, str(setup["reason"]), now)
                    continue
                funnel["base_flush_pass"] += 1
                for profile_name, profile in active_confirmation_profiles(cfg).items():
                    profile_now = datetime.now(timezone.utc) if live_clock else now
                    result = _process_profile(
                        trading, cfg, symbol, setup, profile_name, dict(profile), profile_now, persist,
                        frame_cache,
                    )
                    if result:
                        inserted.append(result)
                        profile_counts = funnel["profile_results"].setdefault(
                            profile_name, {"eligible": 0, "pending": 0, "rejected": {}},
                        )
                        status = str(result.get("eligibility_status") or "unknown")
                        if status == "rejected":
                            count_reason(profile_counts["rejected"],
                                         str(result.get("rejection_reason") or "UNKNOWN"))
                        elif status in {"eligible", "pending"}:
                            profile_counts[status] += 1
            if persist:
                trading.commit()
        timings_ms["derivative_context_lookups"] = round(context_ms, 1)
        timings_ms["flush_and_profile_evaluation"] = round((time.perf_counter() - phase_started) * 1000, 1)

        phase_started = time.perf_counter()
        rows = [dict(row) for row in trading.execute(f"SELECT * FROM {OUTCOME_TABLE}")]
        summaries: dict[str, dict[str, Any]] = {}
        for name, profile in active_confirmation_profiles(cfg).items():
            selected = [row for row in rows if row["profile_id"] == profile["profile_id"]]
            profile_activation = _dt(profile.get("activation_at")) or activated
            summaries[name] = clean_forward_summary(
                selected, activated_at=profile_activation.isoformat(), now=now,
                min_closed=int(cfg["min_clean_closed"]), min_days=float(cfg["min_forward_days"]),
                min_pf=float(cfg["min_profit_factor"]),
                max_review_drawdown_usd=float(cfg["max_review_drawdown_usd"]),
            )
            if persist:
                summary = summaries[name]
                conn_profile = str(profile["profile_id"])
                trading.execute(f"DELETE FROM {EVAL_TABLE} WHERE profile_id=?", (conn_profile,))
                trading.execute(
                    f"INSERT OR REPLACE INTO {EVAL_TABLE} VALUES(?,?,?,?,?,?,?,?,?,?)",
                    (now.isoformat(), profile["profile_id"], summary["clean_closed"],
                     summary["net_pnl_usd"], summary["profit_factor"], summary["winrate"],
                     summary["max_drawdown_usd"], summary["forward_days"], summary["verdict"],
                     json_text(cfg)),
                )
        if persist:
            trading.commit()
        telegram_signals = {"sent": 0, "queued": 0, "skipped": 0, "stale": 0}
        telegram_closes = {"sent": 0, "queued": 0, "skipped": 0}
        telegram_cfg = dict(cfg.get("manual_telegram_signals") or {})
        if persist and telegram_cfg.get("enabled"):
            from src.notifiers.manual_paper_signal import (
                latest_closed_minute, send_manual_paper_close, send_manual_paper_entry,
            )

            selected_ids = {str(value) for value in telegram_cfg.get("profile_ids") or []}
            profile_labels = dict(telegram_cfg.get("profile_labels") or {})
            for candidate_id in previously_open_ids:
                row = trading.execute(
                    f"SELECT * FROM {OUTCOME_TABLE} WHERE candidate_id=? "
                    "AND outcome_status='closed' AND eligibility_status='eligible'",
                    (candidate_id,),
                ).fetchone()
                if row is None or str(row["profile_id"]) not in selected_ids:
                    continue
                signal_id = f"manual-paper:crypto:{candidate_id}"
                entry_alert = trading.execute(
                    "SELECT telegram_status FROM signal_alerts "
                    "WHERE signal_id=? AND alert_type='manual_paper_entry' "
                    "ORDER BY sent_at DESC,rowid DESC LIMIT 1",
                    (signal_id,),
                ).fetchone()
                if entry_alert is None or str(entry_alert["telegram_status"]) != "sent":
                    telegram_closes["skipped"] += 1
                    continue
                try:
                    result = send_manual_paper_close(
                        root=ROOT, db_path=path, signal_id=signal_id,
                        asset_class="crypto", symbol=str(row["symbol"]),
                        direction=str(row["direction"]),
                        title="Fast 1m Liquidity Reclaim · Paper",
                        variants=[{
                            "label": profile_labels.get(str(row["profile_id"]), "FAST 1m"),
                            "outcome_status": row["outcome_status"],
                            "close_reason": row["close_reason"],
                            "highest_tp_touched": row["highest_tp_touched"],
                            "net_pnl_usd": row["net_pnl_usd"],
                            "net_r": row["net_r"],
                            "exit_price": row["exit_price"],
                        }],
                        now=now,
                    )
                except Exception:
                    telegram_closes["skipped"] += 1
                    continue
                key = ("sent" if result.get("sent") else
                       "queued" if str(result.get("status", "")).startswith("queued:") else "skipped")
                telegram_closes[key] += 1

            for row in inserted:
                if (str(row.get("profile_id")) not in selected_ids
                        or row.get("eligibility_status") != "eligible"
                        or row.get("outcome_status") != "open"):
                    continue
                symbol = str(row["symbol"])
                signal_now = datetime.now(timezone.utc) if live_clock else now
                max_age_seconds = int(telegram_cfg.get("max_age_seconds", 90))
                entry_at = _dt(row.get("entry_ts"))
                if entry_at is None or (signal_now - entry_at).total_seconds() > max_age_seconds:
                    telegram_signals["stale"] += 1
                    continue
                frame_key = (_canon(symbol), "1m")
                if frame_key not in frame_cache:
                    frame_cache[frame_key] = _load_frame(symbol, "1m", cfg)
                quote = latest_closed_minute(frame_cache[frame_key], now=signal_now)
                if quote is None:
                    telegram_signals["skipped"] += 1
                    continue
                try:
                    result = send_manual_paper_entry(
                        root=ROOT, db_path=path,
                        signal_id=f"manual-paper:crypto:{row['candidate_id']}",
                        asset_class="crypto", symbol=symbol,
                        direction=row["direction"],
                        title="Fast 1m Liquidity Reclaim · Paper",
                        entry_at=row["entry_ts"], reference_price=quote[0],
                        reference_at=quote[1],
                        variants=[{"label": profile_labels.get(str(row["profile_id"]), "FAST 1m"),
                                   "entry": row["entry_price"],
                                   "stop": row["stop_price"], "tp1": row["tp1"],
                                   "tp2": row["tp2"]}],
                        now=signal_now, max_age_seconds=max_age_seconds,
                    )
                except Exception:
                    telegram_signals["skipped"] += 1
                    continue
                key = ("sent" if result.get("sent") else
                       "queued" if str(result.get("status", "")).startswith("queued:") else "skipped")
                telegram_signals[key] += 1
        timings_ms["summary_and_persist"] = round((time.perf_counter() - phase_started) * 1000, 1)
        timings_ms["total"] = round((time.perf_counter() - tick_started) * 1000, 1)
        return {"enabled": True, "rows": inserted, "closed_matured": matured,
                "expired_pending": expired_pending,
                "symbol_count": len(symbols), "summary_by_profile": summaries,
                "liquidation_source": source, "candidate_refresh": candidate_refresh,
                "funnel": funnel, "timings_ms": timings_ms,
                "manual_telegram_signals": telegram_signals,
                "manual_telegram_closes": telegram_closes}
    finally:
        intelligence.close()
        trading.close()


def render_markdown(result: dict[str, Any]) -> str:
    lines = ["# Crypto Fast Flush Reclaim v3 - Paper", "",
             "Strong 5m liquidation flush -> OI/intensity gate -> 1m or 5m confirmed reclaim.",
             "This lane is Paper-only and has no live bridge.", "",
             f"- enabled: `{result.get('enabled')}`",
             f"- symbols scanned: `{result.get('symbol_count', 0)}`",
             f"- new/updated candidates: `{len(result.get('rows') or [])}`",
             f"- matured: `{result.get('closed_matured', 0)}`",
             f"- Telegram close notices: `{result.get('manual_telegram_closes', {})}`"]
    for name, summary in (result.get("summary_by_profile") or {}).items():
        lines.extend(["", f"## {name}", "",
                      f"- verdict: **{summary.get('verdict')}**",
                      f"- clean closed: `{summary.get('clean_closed', 0)}`",
                      f"- net: `${summary.get('net_pnl_usd', 0.0):.2f}` · PF: `{summary.get('profit_factor')}`"])
    funnel = result.get("funnel") or {}
    if funnel:
        lines.extend([
            "", "## Latest scan funnel", "",
            f"- source status: `{(result.get('liquidation_source') or {}).get('status')}`",
            f"- symbols with recent liquidation events: `{funnel.get('symbols_with_recent_liquidations', 0)}` / `{funnel.get('symbols_scanned', 0)}`",
            f"- 5m windows examined / above liquidation floor: `{funnel.get('event_windows_examined', 0)}` / `{funnel.get('windows_over_min_liquidation', 0)}`",
            f"- base flushes passing all shared gates: `{funnel.get('base_flush_pass', 0)}`",
            f"- shared-gate rejections: `{funnel.get('base_rejections', {})}`",
            f"- profile rejections: `{funnel.get('profile_results', {})}`",
            f"- expired pending confirmations: `{result.get('expired_pending', 0)}`",
            f"- tick stage ms: `{result.get('timings_ms', {})}`",
        ])
    return "\n".join(lines)


def write_report(result: dict[str, Any], path: str | None = None) -> str:
    target = ROOT / (path or load_strategy_config()["report_path"])
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_markdown(result) + "\n", encoding="utf-8")
    return str(target)


__all__ = [
    "OUTCOME_TABLE", "OBS_TABLE", "detect_flush", "detect_confirmation",
    "entry_geometry", "simulate_two_target", "ensure_tables", "load_strategy_config",
    "active_confirmation_profiles", "tick", "write_report",
]
