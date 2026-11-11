"""RTH stock liquidity-shock reclaim, isolated Paper-only evidence lane.

The strategy observes a measurable event rather than claiming knowledge of
hidden stops: a liquid stock breaks a recent RTH low on abnormal range and
volume, while the broad market/sector is not in the same cascade.  A trade is
recorded only after a closed 1m candle reclaims the calculated level. Only
the structural-target HELD profile is active; retired variants remain defined
for evidence review.

This module never creates a generic proposed signal and has no execution
adapter. Profile outcomes remain isolated; selected Paper entries can emit
manual-only Telegram notices without creating or routing an order.
"""
from __future__ import annotations

import hashlib
import json
import math
import sqlite3
import time as time_module
from copy import deepcopy
from datetime import datetime, time, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import pandas as pd

from src.execution.fees import trade_costs
from src.execution.structural_tp_engine import generate_structural_tps
from src.execution.shadow_strategy_common import (
    clean_forward_summary,
    json_text,
    load_yaml_block,
    normalize_frame,
    parse_dt,
    utc_now,
)


ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "config" / "paper" / "stocks" / "liquidity_shock_reclaim_v1.yaml"
STRATEGY_KEY = "stocks_liquidity_shock_reclaim_v1_paper"
NY = ZoneInfo("America/New_York")
_FRAME_CACHE: dict[str, tuple[int, int, pd.DataFrame]] = {}
_LAST_BASE_REFRESH_SLOT: datetime | None = None
_LAST_OPEN_POSITION_REFRESH: dict[str, datetime] = {}
_SCHEMA_READY_DATABASES: set[str] = set()
_CANDIDATE_REFRESH_OFFSET = 0

DEFAULTS: dict[str, Any] = {
    "feature_flag": True,
    "live_enabled": False,
    "strategy_id": "stocks_liquidity_shock_reclaim_v1",
    "paper_lane": "paper_stocks_liquidity_shock_reclaim_v1",
    "base_timeframe": "15m",
    "confirmation_timeframe": "1m",
    "use_default_universe": True,
    "recent_scan_bars": 4,
    "refresh_candidate_1m": True,
    "max_candidate_refresh_symbols": 24,
    "refresh_open_position_1m": True,
    "open_position_refresh_interval_seconds": 30,
    "open_position_stale_after_seconds": 180,
    "refresh_base_15m_on_close": True,
    "base_refresh_delay_seconds": 5,
    "allowed_windows_et": ["09:45-11:30", "13:30-15:15"],
    "level_lookback_bars": 8,
    "atr_periods": 14,
    "volume_lookback_bars": 20,
    "min_flush_atr": 1.10,
    "max_flush_atr": 3.50,
    "min_flush_pct": 0.80,
    "min_rvol": 1.20,
    "min_level_breach_atr": 0.15,
    "min_idiosyncratic_drop_pct": 0.20,
    "max_market_drop_pct": 0.60,
    "max_sector_drop_pct": 1.10,
    "min_avg_dollar_volume_30d": 25_000_000.0,
    "min_bar_dollar_volume": 1_500_000.0,
    "min_price": 5.0,
    "blocked_news_lookback_hours": 36.0,
    "blocked_event_types": ["earnings", "guidance", "legal_risk", "offering_dilution",
                            "fda_clinical", "management_change"],
    "blocked_risk_actions": ["block", "review"],
    "reclaim_fraction": 0.40,
    "stop_buffer_atr": 0.10,
    "min_stop_distance_pct": 0.0035,
    "max_stop_distance_pct": 0.035,
    "target_r": [0.80, 1.35],
    "target_fractions": [0.70, 0.30],
    "move_stop_to_entry_after_tp1": True,
    "fixed_risk_usd": 10.0,
    "fee_profile": "stock_etf_default",
    "stock_slippage": {"major": 0.0003, "liquid_alt": 0.0005, "illiquid_alt": 0.0010},
    "max_entry_latency_seconds": 1200.0,
    "clean_entry_latency_seconds": 180.0,
    "manual_telegram_signals": {"enabled": False, "profile_ids": [], "max_age_seconds": 180},
    "confirmation_profiles": {
        "FAST_1M_RECLAIM": {
            "enabled": False,
            "profile_id": "stocks_liquidity_shock_fast_1m_paper_v1",
            "research_role": "speed_control",
            "hold_bars": 1, "confirmation_window_bars": 8,
            "require_green": True, "require_progress": False,
            "max_holding_bars": 45,
            "min_flush_atr": 1.50, "max_flush_atr": 3.50,
            "min_flush_pct": 0.80, "min_rvol": 1.70,
            "min_idiosyncratic_drop_pct": 0.30,
            "max_market_drop_pct": 0.60, "max_sector_drop_pct": 1.10,
            "min_level_breach_atr": 0.15,
        },
        "HELD_1M_RECLAIM": {
            "enabled": False,
            "profile_id": "stocks_liquidity_shock_held_1m_paper_v1",
            "research_role": "primary_candidate",
            "hold_bars": 2, "confirmation_window_bars": 12,
            "require_green": True, "require_progress": True,
            "max_holding_bars": 60,
            "min_flush_atr": 1.10, "max_flush_atr": 3.50,
            "min_flush_pct": 0.80, "min_rvol": 1.20,
            "min_idiosyncratic_drop_pct": 0.20,
            "max_market_drop_pct": 0.60, "max_sector_drop_pct": 1.10,
            "min_level_breach_atr": 0.15,
        },
        "HELD_1M_STRUCTURE_TARGETS": {
            "enabled": True,
            "profile_id": "stocks_liquidity_shock_held_1m_structure_targets_paper_v1",
            "research_role": "structural_target_candidate",
            "activation_at": "2026-09-30T00:00:00+00:00",
            "hold_bars": 2, "confirmation_window_bars": 12,
            "require_green": True, "require_progress": True,
            "max_holding_bars": 60,
            "min_flush_atr": 1.10, "max_flush_atr": 3.50,
            "min_flush_pct": 0.80, "min_rvol": 1.20,
            "min_idiosyncratic_drop_pct": 0.20,
            "max_market_drop_pct": 0.60, "max_sector_drop_pct": 1.10,
            "min_level_breach_atr": 0.15, "target_policy": "pure_structure",
        },
        "HELD_1M_WIDER_STOP_015": {
            "enabled": False,
            "profile_id": "stocks_liquidity_shock_held_1m_buffer_015_paper_v1",
            "research_role": "exploratory_wider_structural_stop",
            "activation_at": "2026-10-05T13:30:00+00:00",
            "hold_bars": 2, "confirmation_window_bars": 12,
            "require_green": True, "require_progress": True,
            "max_holding_bars": 60,
            "min_flush_atr": 1.10, "max_flush_atr": 3.50,
            "min_flush_pct": 0.80, "min_rvol": 1.20,
            "min_idiosyncratic_drop_pct": 0.20,
            "max_market_drop_pct": 0.60, "max_sector_drop_pct": 1.10,
            "min_level_breach_atr": 0.15, "stop_buffer_atr": 0.15,
        },
    },
    "min_clean_closed": 30,
    "min_forward_days": 30,
    "min_profit_factor": 1.20,
    "max_review_drawdown_usd": 150.0,
    "report_path": "reports/STOCKS_LIQUIDITY_SHOCK_RECLAIM_V1_PAPER.md",
}

OUTCOME_TABLE = "stocks_liquidity_shock_reclaim_v1_paper_outcomes"
OBS_TABLE = "stocks_liquidity_shock_reclaim_v1_paper_observations"
EVAL_TABLE = "stocks_liquidity_shock_reclaim_v1_paper_evaluations"
META_TABLE = "stocks_liquidity_shock_reclaim_v1_paper_meta"

OUTCOME_DDL = f"""
CREATE TABLE IF NOT EXISTS {OUTCOME_TABLE} (
  candidate_id TEXT PRIMARY KEY, raw_event_id TEXT NOT NULL,
  strategy_id TEXT NOT NULL, profile_id TEXT NOT NULL, paper_lane TEXT NOT NULL,
  window TEXT NOT NULL, generated_at TEXT NOT NULL, decision_at TEXT NOT NULL,
  shock_at TEXT NOT NULL, symbol TEXT NOT NULL, direction TEXT NOT NULL,
  entry_profile TEXT NOT NULL, confirmation_timeframe TEXT NOT NULL,
  session_bucket TEXT, sector_etf TEXT, avg_dollar_volume_30d REAL,
  bar_dollar_volume REAL, flush_atr REAL, flush_pct REAL, rvol REAL,
  level_breach_atr REAL, market_drop_pct REAL, sector_drop_pct REAL,
  idiosyncratic_drop_pct REAL, close_location REAL, reclaim_level REAL,
  shock_extreme REAL, news_status TEXT, news_event_type TEXT,
  eligibility_status TEXT NOT NULL, rejection_reason TEXT, data_status TEXT,
  is_clean_for_edge INTEGER NOT NULL DEFAULT 0,
  entry_ts TEXT, entry_price REAL, stop_price REAL, tp1 REAL, tp2 REAL,
  outcome_status TEXT NOT NULL, close_reason TEXT, exit_price REAL, exit_ts TEXT,
  gross_pnl_usd REAL, net_pnl_usd REAL, net_r REAL, fees_usd REAL,
  slippage_usd REAL, funding_usd REAL DEFAULT 0, risk_usd REAL, mfe_r REAL,
  mae_r REAL, highest_tp_touched INTEGER, bars_held INTEGER,
  latency_seconds REAL, features_json TEXT, notes_json TEXT, last_checked_at TEXT
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
  PRIMARY KEY(generated_at,profile_id)
)
"""


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    out = deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = _deep_merge(dict(out[key]), value)
        else:
            out[key] = value
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


def _select_candidate_refresh_symbols(
    setups: list[tuple[str, dict[str, Any], pd.DataFrame]], limit: int,
) -> list[str]:
    """Round-robin eligible symbols so a capped batch does not favor alphabetically early tickers."""
    global _CANDIDATE_REFRESH_OFFSET
    candidates = sorted({str(symbol) for symbol, _, _ in setups})
    cap = max(0, int(limit))
    if not candidates or cap == 0:
        return []
    if len(candidates) <= cap:
        return candidates
    start = _CANDIDATE_REFRESH_OFFSET % len(candidates)
    rotated = candidates[start:] + candidates[:start]
    selected = rotated[:cap]
    _CANDIDATE_REFRESH_OFFSET = (start + cap) % len(candidates)
    return selected


def _profile_activation_allows(setup: dict[str, Any], profile: dict[str, Any]) -> bool:
    activation = _dt(profile.get("activation_at"))
    decision_at = _dt(setup.get("decision_at"))
    return not (activation and decision_at and decision_at < activation)


def _profile_geometry_setup(setup: dict[str, Any], profile: dict[str, Any]) -> dict[str, Any] | None:
    buffer_atr = _f(profile.get("stop_buffer_atr"))
    if buffer_atr is None:
        return setup
    shock_low = _f(setup.get("shock_extreme"))
    atr = _f(setup.get("atr"))
    if shock_low is None or atr is None or atr <= 0 or buffer_atr < 0:
        return None
    geometry_setup = dict(setup)
    geometry_setup["stop"] = shock_low - atr * buffer_atr
    return geometry_setup


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
    required_indexes = {"idx_stock_lsr_state", "idx_stock_lsr_profile", "idx_stock_lsr_symbol"}
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
    conn.execute(f"CREATE INDEX IF NOT EXISTS idx_stock_lsr_state ON {OUTCOME_TABLE}(outcome_status,entry_ts)")
    conn.execute(f"CREATE INDEX IF NOT EXISTS idx_stock_lsr_profile ON {OUTCOME_TABLE}(profile_id,outcome_status)")
    conn.execute(f"CREATE INDEX IF NOT EXISTS idx_stock_lsr_symbol ON {OUTCOME_TABLE}(symbol,decision_at)")
    _SCHEMA_READY_DATABASES.add(db_key)


def _f(value: Any) -> float | None:
    try:
        return None if value in (None, "") or pd.isna(value) else float(value)
    except (TypeError, ValueError):
        return None


def _dt(value: Any) -> datetime | None:
    parsed = parse_dt(value)
    return parsed.astimezone(timezone.utc) if parsed else None


def _id(prefix: str, *parts: Any) -> str:
    return prefix + hashlib.sha256("|".join(str(part) for part in parts).encode()).hexdigest()[:22]


def _raw_event_id(cfg: dict[str, Any], symbol: str, decision_at: datetime) -> str:
    return _id("slsr1e_", cfg["strategy_id"], symbol.upper(), decision_at.isoformat())


def _candidate_id(cfg: dict[str, Any], symbol: str, decision_at: datetime,
                  profile_id: str) -> str:
    return _id("slsr1_", cfg["strategy_id"], symbol.upper(), decision_at.isoformat(), profile_id)


def _cache_frame(symbol: str, timeframe: str) -> pd.DataFrame:
    path = ROOT / "data" / "raw" / "stocks" / timeframe / f"{symbol.upper()}.csv"
    if not path.exists():
        return pd.DataFrame()
    try:
        stat = path.stat()
        cache_key = str(path)
        cached = _FRAME_CACHE.get(cache_key)
        if cached and cached[0] == stat.st_mtime_ns and cached[1] == stat.st_size:
            return cached[2]
    except OSError:
        return pd.DataFrame()
    try:
        frame = pd.read_csv(path)
    except Exception:
        return pd.DataFrame()
    if frame.empty:
        return frame
    if "timestamp" not in {str(column).lower() for column in frame.columns}:
        frame = frame.rename(columns={str(frame.columns[0]): "timestamp"})
    clean = normalize_frame(frame)
    _FRAME_CACHE[cache_key] = (stat.st_mtime_ns, stat.st_size, clean)
    return clean


def configured_symbols(cfg: dict[str, Any] | None = None) -> list[str]:
    cfg = cfg or load_strategy_config()
    explicit = [str(value).upper() for value in cfg.get("symbols") or []]
    if explicit:
        return explicit
    from src.stocks.configs.loader import load_stocks_config

    stocks = load_stocks_config(ROOT)
    return [symbol for symbol in stocks.default_symbols if not stocks.is_etf(symbol)]


def _atr(frame: pd.DataFrame, idx: int, periods: int) -> float | None:
    if idx < periods or frame.empty:
        return None
    prior = frame.iloc[max(0, idx - periods):idx + 1].copy()
    previous_close = prior["close"].shift(1)
    tr = pd.concat([
        prior["high"] - prior["low"],
        (prior["high"] - previous_close).abs(),
        (prior["low"] - previous_close).abs(),
    ], axis=1).max(axis=1).dropna()
    return float(tr.iloc[-periods:].mean()) if len(tr) >= periods else None


def _parse_clock(value: str) -> time:
    hour, minute = str(value).split(":", 1)
    return time(int(hour), int(minute))


def _allowed_window(at: datetime, cfg: dict[str, Any]) -> bool:
    local = at.astimezone(NY)
    if local.weekday() >= 5:
        return False
    clock = local.timetz().replace(tzinfo=None)
    for raw in cfg.get("allowed_windows_et") or []:
        start, end = str(raw).split("-", 1)
        if _parse_clock(start) <= clock <= _parse_clock(end):
            return True
    return False


def _drop_at(frame: pd.DataFrame, bar_at: datetime) -> float | None:
    work = normalize_frame(frame)
    if work.empty:
        return None
    matches = work.index[work["timestamp"] == pd.Timestamp(bar_at)].tolist()
    if not matches:
        return None
    idx = int(matches[-1])
    if idx < 1:
        return None
    prior = _f(work.iloc[idx - 1].get("close"))
    low = _f(work.iloc[idx].get("low"))
    if prior is None or low is None or prior <= 0:
        return None
    return max(0.0, (prior - low) / prior * 100.0)


def liquidity_snapshot(symbol: str, at: datetime) -> dict[str, Any]:
    daily = _cache_frame(symbol, "1d")
    if daily.empty:
        return {"ok": False, "reason": "DAILY_LIQUIDITY_MISSING"}
    visible = daily[daily["timestamp"] < pd.Timestamp(at)].tail(30)
    if len(visible) < 10:
        return {"ok": False, "reason": "DAILY_LIQUIDITY_MISSING"}
    dollar = (visible["close"] * visible["volume"]).dropna()
    return {"ok": bool(len(dollar)), "avg_dollar_volume_30d": float(dollar.mean()) if len(dollar) else None}


def detect_shock(frame: pd.DataFrame, idx: int, market_frame: pd.DataFrame,
                 sector_frame: pd.DataFrame, liquidity: dict[str, Any],
                 cfg: dict[str, Any]) -> dict[str, Any]:
    work = normalize_frame(frame)
    minimum = max(int(cfg["level_lookback_bars"]), int(cfg["atr_periods"]),
                  int(cfg["volume_lookback_bars"]))
    if work.empty or idx < minimum:
        return {"ok": False, "reason": "CANDLES_MISSING"}
    row = work.iloc[idx]
    shock_at = _dt(row.get("timestamp"))
    if shock_at is None:
        return {"ok": False, "reason": "CANDLES_MISSING"}
    decision_at = shock_at + timedelta(minutes=15)
    values = {key: _f(row.get(key)) for key in ("open", "high", "low", "close", "volume")}
    prior_close = _f(work.iloc[idx - 1].get("close"))
    atr = _atr(work, idx - 1, int(cfg["atr_periods"]))
    facts: dict[str, Any] = {"decision_at": decision_at, "shock_at": shock_at,
                            "direction": "long", "prior_close": prior_close, "atr": atr}
    if any(value is None for value in values.values()) or prior_close is None or not atr or atr <= 0:
        return {**facts, "ok": False, "reason": "CANDLES_MISSING"}
    open_, high, low, close, volume = (float(values[key]) for key in ("open", "high", "low", "close", "volume"))
    prior = work.iloc[idx - int(cfg["level_lookback_bars"]):idx]
    structural_level = float(prior["low"].min())
    flush_distance = max(0.0, prior_close - low)
    flush_atr = flush_distance / atr
    flush_pct = flush_distance / prior_close * 100.0
    median_volume = float(work.iloc[idx - int(cfg["volume_lookback_bars"]):idx]["volume"].median())
    rvol = volume / median_volume if median_volume > 0 else 0.0
    level_breach_atr = max(0.0, structural_level - low) / atr
    market_drop = _drop_at(market_frame, shock_at)
    sector_drop = _drop_at(sector_frame, shock_at) if not sector_frame.empty else None
    context_drop = max(float(market_drop or 0.0), float(sector_drop or 0.0))
    idiosyncratic = flush_pct - context_drop
    close_location = (close - low) / max(high - low, 1e-12)
    bar_dollar = close * volume
    facts.update(
        shock_extreme=low, shock_close=close, structural_level=structural_level,
        flush_atr=flush_atr, flush_pct=flush_pct, rvol=rvol,
        level_breach_atr=level_breach_atr, market_drop_pct=market_drop,
        sector_drop_pct=sector_drop, idiosyncratic_drop_pct=idiosyncratic,
        close_location=close_location, bar_dollar_volume=bar_dollar,
        avg_dollar_volume_30d=liquidity.get("avg_dollar_volume_30d"),
    )
    if not _allowed_window(decision_at, cfg):
        return {**facts, "ok": False, "reason": "RTH_WINDOW_NOT_ALLOWED"}
    if not liquidity.get("ok"):
        return {**facts, "ok": False, "reason": str(liquidity.get("reason") or "DAILY_LIQUIDITY_MISSING")}
    if close < float(cfg["min_price"]):
        return {**facts, "ok": False, "reason": "PRICE_TOO_LOW"}
    if float(liquidity.get("avg_dollar_volume_30d") or 0.0) < float(cfg["min_avg_dollar_volume_30d"]):
        return {**facts, "ok": False, "reason": "ADV_TOO_LOW"}
    if bar_dollar < float(cfg["min_bar_dollar_volume"]):
        return {**facts, "ok": False, "reason": "BAR_LIQUIDITY_TOO_LOW"}
    if flush_atr < float(cfg["min_flush_atr"]):
        return {**facts, "ok": False, "reason": "FLUSH_TOO_SMALL"}
    if flush_atr > float(cfg["max_flush_atr"]):
        return {**facts, "ok": False, "reason": "UNCONTROLLED_CASCADE"}
    if flush_pct < float(cfg["min_flush_pct"]):
        return {**facts, "ok": False, "reason": "FLUSH_PCT_TOO_SMALL"}
    if rvol < float(cfg["min_rvol"]):
        return {**facts, "ok": False, "reason": "RVOL_TOO_WEAK"}
    if level_breach_atr < float(cfg["min_level_breach_atr"]):
        return {**facts, "ok": False, "reason": "NO_STRUCTURAL_SWEEP"}
    if market_drop is None:
        return {**facts, "ok": False, "reason": "MARKET_CONTEXT_MISSING"}
    if market_drop > float(cfg["max_market_drop_pct"]):
        return {**facts, "ok": False, "reason": "BROAD_MARKET_CASCADE"}
    if sector_drop is not None and sector_drop > float(cfg["max_sector_drop_pct"]):
        return {**facts, "ok": False, "reason": "SECTOR_CASCADE"}
    if idiosyncratic < float(cfg["min_idiosyncratic_drop_pct"]):
        return {**facts, "ok": False, "reason": "NOT_IDIOSYNCRATIC"}
    reclaim = max(structural_level, low + (prior_close - low) * float(cfg["reclaim_fraction"]))
    stop = low - atr * float(cfg["stop_buffer_atr"])
    return {**facts, "ok": True, "reclaim_level": reclaim, "stop": stop}


def news_risk(conn: sqlite3.Connection, symbol: str, at: datetime,
              cfg: dict[str, Any]) -> dict[str, Any]:
    exists = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name='news_canonical_events'"
    ).fetchone()
    if not exists:
        return {"blocked": False, "status": "unavailable", "event_type": None}
    cutoff = at - timedelta(hours=float(cfg["blocked_news_lookback_hours"]))
    rows = conn.execute(
        "SELECT trusted_symbols_json,event_type,direction_hint,risk_action,available_at,effective_at,published_at "
        "FROM news_canonical_events WHERE lower(COALESCE(asset_class,''))='stocks' "
        "AND is_cluster_primary=1 AND available_at IS NOT NULL "
        "AND available_at>=? AND available_at<=?",
        (cutoff.isoformat(), at.isoformat()),
    ).fetchall()
    blocked_types = {str(value).lower() for value in cfg.get("blocked_event_types") or []}
    blocked_actions = {str(value).lower() for value in cfg.get("blocked_risk_actions") or []}
    seen = False
    for raw in rows:
        row = dict(raw)
        try:
            symbols = {str(value).upper() for value in json.loads(row.get("trusted_symbols_json") or "[]")}
        except (TypeError, ValueError, json.JSONDecodeError):
            symbols = set()
        if symbol.upper() not in symbols:
            continue
        seen = True
        event_type = str(row.get("event_type") or "unknown").lower()
        bearish = str(row.get("direction_hint") or "").lower() in {"bearish", "negative"}
        risky = str(row.get("risk_action") or "").lower() in blocked_actions
        if bearish or risky or event_type in blocked_types:
            return {"blocked": True, "status": "negative_fundamental_catalyst",
                    "event_type": event_type}
    return {"blocked": False, "status": "clear" if seen else "no_recent_symbol_news",
            "event_type": None}


def detect_confirmation(frame: pd.DataFrame, setup: dict[str, Any], now: datetime,
                        profile: dict[str, Any]) -> dict[str, Any]:
    work = normalize_frame(frame)
    if work.empty:
        return {"status": "pending"}
    decision_at = setup.get("decision_at")
    if not isinstance(decision_at, datetime):
        decision_at = _dt(decision_at)
    if decision_at is None:
        return {"status": "pending"}
    closed = work[work["timestamp"] + pd.Timedelta(minutes=1) <= pd.Timestamp(now)].copy()
    closed["_close_at"] = closed["timestamp"] + pd.Timedelta(minutes=1)
    end = decision_at + timedelta(minutes=int(profile.get("confirmation_window_bars", 8)))
    closed = closed[(closed["_close_at"] > pd.Timestamp(decision_at))
                    & (closed["_close_at"] <= pd.Timestamp(end))]
    level = float(setup["reclaim_level"])
    holds: list[tuple[int, float, float, datetime]] = []
    for index, candle in closed.iterrows():
        open_, high, low, close = (_f(candle.get(key)) for key in ("open", "high", "low", "close"))
        if None in (open_, high, low, close):
            continue
        close_location = (float(close) - float(low)) / max(float(high) - float(low), 1e-12)
        valid = float(close) >= level and close_location >= 0.60
        if profile.get("require_green", True):
            valid = valid and float(close) > float(open_)
        if profile.get("require_progress") and holds:
            valid = valid and float(close) > holds[-1][1] and float(high) >= holds[-1][2]
        if not valid:
            holds = []
            continue
        close_at = _dt(candle.get("_close_at"))
        if close_at is None:
            continue
        holds.append((int(index), float(close), float(high), close_at))
        required = int(profile.get("hold_bars", 1))
        if len(holds) >= required:
            recent = holds[-required:]
            if required == 1 or all(recent[pos][0] == recent[pos - 1][0] + 1
                                    for pos in range(1, required)):
                return {"status": "entry", "entry": recent[-1][1],
                        "entry_at": recent[-1][3], "confirmation_bars": required}
    if now >= end:
        return {"status": "skipped", "reason": "RECLAIM_WINDOW_EXPIRED"}
    return {"status": "pending"}


def entry_geometry(setup: dict[str, Any], entry: float,
                   cfg: dict[str, Any], *, profile: dict[str, Any] | None = None,
                   history: pd.DataFrame | None = None) -> dict[str, Any]:
    stop = float(setup["stop"])
    risk = entry - stop
    if risk <= 0:
        return {"ok": False, "reason": "INVALID_STOP_GEOMETRY"}
    stop_pct = risk / entry
    if stop_pct < float(cfg["min_stop_distance_pct"]):
        return {"ok": False, "reason": "STOP_TOO_TIGHT_FOR_COSTS",
                "stop_distance_pct": round(stop_pct, 8)}
    if stop_pct > float(cfg["max_stop_distance_pct"]):
        return {"ok": False, "reason": "STOP_TOO_WIDE",
                "stop_distance_pct": round(stop_pct, 8)}
    profile = profile or {}
    policy = str(profile.get("target_policy") or "fixed_r").lower()
    targets = [entry + risk * float(value) for value in cfg["target_r"]]
    target_meta: dict[str, Any] = {"target_policy": "fixed_r"}
    if policy == "pure_structure":
        structural = generate_structural_tps(
            entry=entry, stop=stop, direction="long",
            candles=(history.to_dict("records") if history is not None and not history.empty else []),
            atr=_f(setup.get("atr")), market_regime="reversal_reclaim",
            playbook="stocks_liquidity_shock_reclaim_v1",
            mechanical_tp1=targets[0], mechanical_tp2=targets[1],
            mechanical_tp3=entry + 2.0 * risk,
        )
        if (structural.tp1 is None or structural.tp2 is None
                or structural.tp1_source.startswith("atr_")
                or structural.tp2_source.startswith("atr_")):
            return {"ok": False, "reason": "NO_PURE_STRUCTURAL_TARGETS"}
        targets = [float(structural.tp1), float(structural.tp2)]
        target_meta = {
            "target_policy": policy,
            "tp1_source": structural.tp1_source,
            "tp2_source": structural.tp2_source,
            "target_r": [structural.tp1_r, structural.tp2_r],
        }
    if targets[0] <= entry or targets[1] <= targets[0]:
        return {"ok": False, "reason": "INVALID_TARGET_GEOMETRY"}
    return {"ok": True, "stop": stop, "tp1": targets[0], "tp2": targets[1],
            "risk": risk, "stop_distance_pct": round(stop_pct, 8), **target_meta}


def _profile_gate_reason(setup: dict[str, Any], profile: dict[str, Any]) -> str | None:
    ranges = (
        ("flush_atr", "min_flush_atr", "max_flush_atr", "PROFILE_FLUSH_ATR"),
        ("flush_pct", "min_flush_pct", None, "PROFILE_FLUSH_PCT"),
        ("rvol", "min_rvol", None, "PROFILE_RVOL"),
        ("idiosyncratic_drop_pct", "min_idiosyncratic_drop_pct", None, "PROFILE_IDIOSYNCRATIC"),
        ("level_breach_atr", "min_level_breach_atr", None, "PROFILE_LEVEL_BREACH"),
    )
    for value_key, minimum_key, maximum_key, reason in ranges:
        value = _f(setup.get(value_key))
        minimum = _f(profile.get(minimum_key))
        maximum = _f(profile.get(maximum_key)) if maximum_key else None
        if value is None or (minimum is not None and value < minimum) or (
                maximum is not None and value > maximum):
            return reason
    market = _f(setup.get("market_drop_pct"))
    if market is None or market > float(profile.get("max_market_drop_pct", float("inf"))):
        return "PROFILE_MARKET_CASCADE"
    sector = _f(setup.get("sector_drop_pct"))
    if sector is not None and sector > float(profile.get("max_sector_drop_pct", float("inf"))):
        return "PROFILE_SECTOR_CASCADE"
    return None


def simulate_two_target(*, entry: float, stop: float, tp1: float, tp2: float,
                        candles: pd.DataFrame, symbol: str, cfg: dict[str, Any],
                        force_close: bool = True) -> dict[str, Any]:
    work = normalize_frame(candles)
    if work.empty:
        return {"outcome_status": "open"}
    risk_distance = entry - stop
    if risk_distance <= 0:
        return {"outcome_status": "skipped", "close_reason": "invalid_geometry"}
    fractions = [float(value) for value in cfg.get("target_fractions") or [0.70, 0.30]]
    target_r = [(tp1 - entry) / risk_distance, (tp2 - entry) / risk_distance]
    remaining, gross_r, highest = 1.0, 0.0, 0
    mfe, mae, bars = 0.0, 0.0, 0
    active_stop = stop
    exits: list[tuple[float, float, str]] = []
    exit_ts: datetime | None = None
    close_reason: str | None = None
    for _, candle in work.iterrows():
        high, low, close = (_f(candle.get(key)) for key in ("high", "low", "close"))
        if None in (high, low, close):
            continue
        bars += 1
        candle_at = _dt(candle.get("timestamp"))
        candle_close = candle_at + timedelta(minutes=1) if candle_at else None
        # Conservative ambiguity rule: a stop and target in the same minute is a stop.
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
        final = float(work.iloc[-1]["close"])
        gross_r += remaining * ((final - entry) / risk_distance)
        exits.append((remaining, final, "taker"))
        candle_at = _dt(work.iloc[-1].get("timestamp"))
        exit_ts = candle_at + timedelta(minutes=1) if candle_at else None
        close_reason = "time_exit"
    risk_usd = float(cfg.get("fixed_risk_usd", 10.0))
    qty = risk_usd / risk_distance
    weighted_exit = sum(fraction * price for fraction, price, _ in exits)
    costs = trade_costs(
        notional_usdt=qty * entry,
        exit_notional_usdt=qty * weighted_exit,
        symbol=symbol,
        fee_profile=str(cfg["fee_profile"]),
        entry_order_type="taker",
        exit_order_type="taker",
        exit_slices=[(fraction, order_type) for fraction, _, order_type in exits],
        slip_cfg=dict(cfg.get("stock_slippage") or {}),
        majors=[],
    )
    gross = gross_r * risk_usd
    return {
        "outcome_status": "closed", "close_reason": close_reason,
        "exit_price": round(weighted_exit, 8),
        "exit_ts": exit_ts.isoformat() if exit_ts else None,
        "gross_pnl_usd": round(gross, 4),
        "net_pnl_usd": round(gross - costs.total_cost_usdt, 4),
        "net_r": round(gross_r - costs.total_cost_usdt / risk_usd, 4),
        "fees_usd": costs.fee_usdt, "slippage_usd": costs.slippage_usdt,
        "funding_usd": 0.0, "risk_usd": risk_usd,
        "mfe_r": round(mfe, 4), "mae_r": round(mae, 4),
        "highest_tp_touched": highest, "bars_held": bars,
    }


def _activation(conn: sqlite3.Connection, now: datetime, persist: bool) -> datetime:
    row = conn.execute(f"SELECT v FROM {META_TABLE} WHERE k='activated_at'").fetchone()
    activated = _dt(row[0]) if row else None
    if activated:
        return activated
    if persist:
        conn.execute(f"INSERT OR REPLACE INTO {META_TABLE}(k,v) VALUES('activated_at',?)",
                     (now.isoformat(),))
    return now


def _row(cfg: dict[str, Any], symbol: str, setup: dict[str, Any], profile_name: str,
         profile: dict[str, Any], now: datetime, status: str,
         reason: str | None) -> dict[str, Any]:
    decision_at = setup["decision_at"]
    profile_id = str(profile["profile_id"])
    latency = setup.get("latency_seconds")
    clean = bool(status == "eligible" and latency is not None
                 and float(latency) <= float(cfg["clean_entry_latency_seconds"]))
    return {
        "candidate_id": _candidate_id(cfg, symbol, decision_at, profile_id),
        "raw_event_id": _raw_event_id(cfg, symbol, decision_at),
        "strategy_id": cfg["strategy_id"], "profile_id": profile_id,
        "paper_lane": cfg["paper_lane"], "window": "forward_post_activation",
        "generated_at": now.isoformat(), "decision_at": decision_at.isoformat(),
        "shock_at": setup["shock_at"].isoformat(), "symbol": symbol.upper(),
        "direction": "long", "entry_profile": profile_name,
        "confirmation_timeframe": str(cfg["confirmation_timeframe"]),
        "session_bucket": decision_at.astimezone(NY).strftime("%H:%M"),
        "sector_etf": setup.get("sector_etf"),
        "avg_dollar_volume_30d": setup.get("avg_dollar_volume_30d"),
        "bar_dollar_volume": setup.get("bar_dollar_volume"),
        "flush_atr": setup.get("flush_atr"), "flush_pct": setup.get("flush_pct"),
        "rvol": setup.get("rvol"), "level_breach_atr": setup.get("level_breach_atr"),
        "market_drop_pct": setup.get("market_drop_pct"),
        "sector_drop_pct": setup.get("sector_drop_pct"),
        "idiosyncratic_drop_pct": setup.get("idiosyncratic_drop_pct"),
        "close_location": setup.get("close_location"),
        "reclaim_level": setup.get("reclaim_level"), "shock_extreme": setup.get("shock_extreme"),
        "news_status": setup.get("news_status"), "news_event_type": setup.get("news_event_type"),
        "eligibility_status": status, "rejection_reason": reason,
        "data_status": "ok" if clean else "delayed" if status == "eligible" else "pending" if status == "pending" else "dirty",
        "is_clean_for_edge": int(clean),
        "outcome_status": "open" if status == "eligible" else "pending" if status == "pending" else "skipped",
        "latency_seconds": latency,
        "features_json": json_text({key: setup.get(key) for key in (
            "prior_close", "atr", "structural_level", "flush_atr", "flush_pct", "rvol",
            "level_breach_atr", "market_drop_pct", "sector_drop_pct", "idiosyncratic_drop_pct")}),
        "notes_json": json_text({"paper_only": True, "live_locked": True,
                                  "entry_logic": "15m RTH liquidity shock -> 1m closed reclaim",
                                  "target_policy": profile.get("target_policy") or "fixed_r"}),
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
    observation_id = _id("slsr1o_", raw_id, reason)
    features = {key: setup.get(key) for key in (
        "flush_atr", "flush_pct", "rvol", "level_breach_atr", "market_drop_pct",
        "sector_drop_pct", "idiosyncratic_drop_pct")}
    conn.execute(
        f"INSERT OR REPLACE INTO {OBS_TABLE} VALUES(?,?,?,?,?,?,?,?)",
        (observation_id, raw_id, now.isoformat(), decision_at.isoformat(), symbol.upper(),
         reason, json_text(features), json_text({"paper_only": True})),
    )


def _process_profile(conn: sqlite3.Connection, cfg: dict[str, Any], symbol: str,
                     setup: dict[str, Any], profile_name: str, profile: dict[str, Any],
                     now: datetime, persist: bool,
                     history: pd.DataFrame | None = None) -> dict[str, Any] | None:
    candidate_id = _candidate_id(cfg, symbol, setup["decision_at"], str(profile["profile_id"]))
    existing = conn.execute(f"SELECT * FROM {OUTCOME_TABLE} WHERE candidate_id=?",
                            (candidate_id,)).fetchone()
    if existing and existing["outcome_status"] != "pending":
        return None
    if not _profile_activation_allows(setup, profile):
        return None
    profile_reason = _profile_gate_reason(setup, profile)
    if profile_reason:
        row = _row(cfg, symbol, setup, profile_name, profile, now, "rejected", profile_reason)
        if persist:
            _upsert(conn, row)
        return row
    confirmation = detect_confirmation(_cache_frame(symbol, "1m"), setup, now, profile)
    if confirmation["status"] == "pending":
        row = _row(cfg, symbol, setup, profile_name, profile, now, "pending", None)
    elif confirmation["status"] == "skipped":
        row = _row(cfg, symbol, setup, profile_name, profile, now, "rejected",
                   str(confirmation["reason"]))
    else:
        latency = max(0.0, (now - confirmation["entry_at"]).total_seconds())
        setup = dict(setup)
        setup["latency_seconds"] = latency
        if latency > float(cfg["max_entry_latency_seconds"]):
            row = _row(cfg, symbol, setup, profile_name, profile, now, "rejected",
                       "STALE_RECLAIM_ENTRY")
        else:
            geometry_setup = _profile_geometry_setup(setup, profile)
            if geometry_setup is None:
                row = _row(cfg, symbol, setup, profile_name, profile, now,
                           "rejected", "PROFILE_STOP_INPUT_MISSING")
                if persist:
                    _upsert(conn, row)
                return row
            geometry = entry_geometry(
                geometry_setup, float(confirmation["entry"]), cfg,
                profile=profile, history=history,
            )
            if not geometry["ok"]:
                row = _row(cfg, symbol, setup, profile_name, profile, now, "rejected",
                           str(geometry["reason"]))
            else:
                row = _row(cfg, symbol, setup, profile_name, profile, now, "eligible", None)
                row.update(entry_ts=confirmation["entry_at"].isoformat(),
                           entry_price=confirmation["entry"], stop_price=geometry["stop"],
                           tp1=geometry["tp1"], tp2=geometry["tp2"])
                notes = json.loads(str(row.get("notes_json") or "{}"))
                notes.update({key: geometry.get(key) for key in (
                    "target_policy", "tp1_source", "tp2_source", "target_r",
                ) if geometry.get(key) is not None})
                if profile.get("stop_buffer_atr") is not None:
                    notes["stop_buffer_atr"] = float(profile["stop_buffer_atr"])
                row["notes_json"] = json_text(notes)
    if persist:
        _upsert(conn, row)
    return row


def _expire_stale_pending(conn: sqlite3.Connection, cfg: dict[str, Any], now: datetime,
                          *, persist: bool = True) -> int:
    """Terminalize unentered reclaims once disabled or outside their finite window."""
    profiles = dict(cfg.get("confirmation_profiles") or {})
    rows = conn.execute(
        f"SELECT * FROM {OUTCOME_TABLE} WHERE outcome_status='pending' AND entry_ts IS NULL"
    ).fetchall()
    expired = 0
    for raw in rows:
        row = dict(raw)
        profile = profiles.get(str(row.get("entry_profile") or ""))
        if profile is None or not bool(profile.get("enabled", True)):
            reason = "PROFILE_ARCHIVED_NO_ENTRY"
        else:
            decision_at = _dt(row.get("decision_at"))
            if decision_at is None:
                reason = "PENDING_DECISION_TIME_MISSING"
            else:
                timeframe = str(profile.get("confirmation_timeframe")
                                 or row.get("confirmation_timeframe") or "1m").strip().lower()
                try:
                    minutes_per_bar = max(1, int(timeframe[:-1])) if timeframe.endswith("m") else 1
                except (TypeError, ValueError):
                    minutes_per_bar = 1
                window_bars = max(1, int(profile.get("confirmation_window_bars") or 8))
                deadline = decision_at + timedelta(minutes=minutes_per_bar * window_bars)
                if now <= deadline:
                    continue
                reason = "RECLAIM_WINDOW_EXPIRED"

        expired += 1
        row.update(
            eligibility_status="rejected", rejection_reason=reason,
            data_status="dirty", is_clean_for_edge=0,
            outcome_status="skipped", last_checked_at=now.isoformat(),
        )
        try:
            notes = json.loads(str(row.get("notes_json") or "{}"))
        except (TypeError, ValueError, json.JSONDecodeError):
            notes = {}
        notes["pending_terminal_reason"] = reason
        row["notes_json"] = json_text(notes)
        if persist:
            _upsert(conn, row)
    return expired


def _open_position_symbols(conn: sqlite3.Connection) -> list[str]:
    return [str(row[0]).upper() for row in conn.execute(
        f"SELECT DISTINCT symbol FROM {OUTCOME_TABLE} WHERE outcome_status='open' "
        "ORDER BY symbol"
    ).fetchall()]


def _refresh_open_position_frames(conn: sqlite3.Connection, cfg: dict[str, Any],
                                  now: datetime, db_key: str) -> dict[str, Any]:
    symbols = _open_position_symbols(conn)
    if not symbols:
        return {"status": "no_open_positions", "attempted": 0, "fetched": 0, "failed": 0}
    if not cfg.get("refresh_open_position_1m", True):
        return {"status": "disabled", "attempted": 0, "fetched": 0, "failed": 0}

    interval = max(1, int(cfg.get("open_position_refresh_interval_seconds", 30)))
    previous = _LAST_OPEN_POSITION_REFRESH.get(db_key)
    if previous is not None and now >= previous and (now - previous).total_seconds() < interval:
        return {"status": "throttled", "attempted": len(symbols), "fetched": 0,
                "failed": 0, "symbols": symbols}

    _LAST_OPEN_POSITION_REFRESH[db_key] = now
    try:
        result = _refresh_candidates(symbols)
    except Exception as exc:  # stale positions must remain open, never be guessed closed
        return {"status": "unavailable", "attempted": len(symbols), "fetched": 0,
                "failed": len(symbols), "symbols": symbols,
                "error": type(exc).__name__}
    return {"status": "ok" if result["fetched"] else "unavailable",
            **result, "symbols": symbols}


def _set_tracking_state(row: dict[str, Any], status: str, now: datetime,
                        latest_bar_close: datetime | None = None,
                        reason: str | None = None) -> None:
    row["data_status"] = status
    row["last_checked_at"] = now.isoformat()
    try:
        notes = json.loads(str(row.get("notes_json") or "{}"))
    except (TypeError, ValueError, json.JSONDecodeError):
        notes = {}
    tracking: dict[str, Any] = {"status": status, "checked_at": now.isoformat()}
    if latest_bar_close is not None:
        tracking["latest_bar_close"] = latest_bar_close.isoformat()
    if reason:
        tracking["reason"] = reason
    notes["tracking"] = tracking
    row["notes_json"] = json_text(notes)


def _mature_open(conn: sqlite3.Connection, cfg: dict[str, Any], now: datetime,
                 *, persist: bool = True) -> int:
    # Disabled profiles stop receiving new candidates, but existing Paper rows
    # still need their configured exit and outcome tracking.
    profiles = {str(name): dict(profile) for name, profile in
                dict(cfg.get("confirmation_profiles") or {}).items()}
    closed = 0
    for raw in conn.execute(f"SELECT * FROM {OUTCOME_TABLE} WHERE outcome_status='open'").fetchall():
        row = dict(raw)
        profile = profiles.get(row["entry_profile"])
        entry_at = _dt(row.get("entry_ts"))
        if not profile or entry_at is None:
            reason = "profile_missing" if not profile else "entry_timestamp_missing"
            _set_tracking_state(row, "tracking_stale", now, reason=reason)
            if persist:
                _upsert(conn, row)
            continue
        frame = _cache_frame(str(row["symbol"]), "1m")
        max_bars = int(profile["max_holding_bars"])
        try:
            from src.stocks.market_calendar import us_cash_session_close

            session_close = us_cash_session_close(entry_at)
        except Exception:
            session_close = None

        if not frame.empty:
            closed_bars = frame[frame["timestamp"] + pd.Timedelta(minutes=1) <= pd.Timestamp(now)]
            future = closed_bars[closed_bars["timestamp"] >= pd.Timestamp(entry_at)]
        else:
            future = frame
        if session_close is not None and not future.empty:
            future = future[future["timestamp"] < pd.Timestamp(session_close)]
        latest_bar_close: datetime | None = None
        if not future.empty:
            latest_bar_close = _dt(future.iloc[-1]["timestamp"] + pd.Timedelta(minutes=1))

        reached_bar_limit = len(future) >= max_bars
        session_ended = bool(session_close and now >= session_close)
        session_data_complete = bool(
            session_ended and latest_bar_close is not None and latest_bar_close >= session_close
        )
        force = reached_bar_limit or session_data_complete

        if future.empty:
            _set_tracking_state(row, "tracking_stale", now, latest_bar_close,
                                "no_closed_bars_since_entry")
            if persist:
                _upsert(conn, row)
            continue

        simulation = simulate_two_target(
            entry=float(row["entry_price"]), stop=float(row["stop_price"]),
            tp1=float(row["tp1"]), tp2=float(row["tp2"]),
            candles=future.iloc[:max_bars], symbol=str(row["symbol"]), cfg=cfg,
            force_close=force,
        )
        row.update(simulation)
        if row.get("outcome_status") == "closed":
            _set_tracking_state(row, "closed_complete", now, latest_bar_close)
        else:
            local = now.astimezone(NY)
            in_rth = local.weekday() < 5 and time(9, 30) <= local.timetz().replace(tzinfo=None) < time(16, 0)
            stale_after = max(60, int(cfg.get("open_position_stale_after_seconds", 180)))
            stale = latest_bar_close is None
            if latest_bar_close is not None and in_rth:
                stale = (now - latest_bar_close).total_seconds() > stale_after
            if session_ended and not session_data_complete:
                stale = True
            tracking_reason = (
                "session_bars_incomplete" if session_ended and not session_data_complete else
                "minute_data_stale" if stale else None
            )
            _set_tracking_state(row, "tracking_stale" if stale else "tracking",
                                now, latest_bar_close, tracking_reason)
        if persist:
            _upsert(conn, row)
        closed += int(row.get("outcome_status") == "closed")
    return closed


def _open_tracking_summary(conn: sqlite3.Connection) -> dict[str, Any]:
    rows = conn.execute(
        f"SELECT symbol,candidate_id,data_status FROM {OUTCOME_TABLE} "
        "WHERE outcome_status='open' ORDER BY symbol,candidate_id"
    ).fetchall()
    stale = [dict(row) for row in rows if str(row["data_status"] or "") == "tracking_stale"]
    return {
        "open": len(rows),
        "stale": len(stale),
        "symbols": sorted({str(row["symbol"]).upper() for row in rows}),
        "stale_symbols": sorted({str(row["symbol"]).upper() for row in stale}),
    }


def _send_manual_paper_close_alerts(
    conn: sqlite3.Connection, cfg: dict[str, Any], db_path: str | Path,
    previously_open_ids: list[str], now: datetime,
) -> dict[str, int]:
    counts = {"sent": 0, "queued": 0, "skipped": 0}
    telegram_cfg = dict(cfg.get("manual_telegram_signals") or {})
    selected_ids = [str(value) for value in telegram_cfg.get("profile_ids") or []]
    if not telegram_cfg.get("enabled") or not selected_ids or not previously_open_ids:
        return counts

    closed_marks = ",".join("?" for _ in previously_open_ids)
    just_closed = conn.execute(
        f"SELECT DISTINCT raw_event_id FROM {OUTCOME_TABLE} "
        f"WHERE outcome_status='closed' AND candidate_id IN ({closed_marks})",
        previously_open_ids,
    ).fetchall()
    labels = dict(telegram_cfg.get("profile_labels") or {})
    profile_marks = ",".join("?" for _ in selected_ids)
    from src.notifiers.manual_paper_signal import send_manual_paper_close

    for event in just_closed:
        raw_event_id = str(event["raw_event_id"])
        signal_id = f"manual-paper:stocks:{raw_event_id}"
        entry_alert = conn.execute(
            "SELECT telegram_status,payload_json FROM signal_alerts "
            "WHERE signal_id=? AND alert_type='manual_paper_entry' "
            "ORDER BY sent_at DESC,rowid DESC LIMIT 1",
            (signal_id,),
        ).fetchone()
        if entry_alert is None or str(entry_alert["telegram_status"]) != "sent":
            counts["skipped"] += 1
            continue
        try:
            entry_payload = json.loads(str(entry_alert["payload_json"] or "{}"))
            expected = [str(item.get("label") or "Paper")
                        for item in entry_payload.get("variants") or []]
        except (TypeError, ValueError, json.JSONDecodeError):
            expected = []
        if not expected:
            counts["skipped"] += 1
            continue

        rows = conn.execute(
            f"SELECT * FROM {OUTCOME_TABLE} WHERE raw_event_id=? "
            f"AND profile_id IN ({profile_marks}) AND eligibility_status='eligible'",
            (raw_event_id, *selected_ids),
        ).fetchall()
        by_label = {str(labels.get(str(row["profile_id"]), row["profile_id"])): row
                    for row in rows}
        matched = [by_label[label] for label in expected if label in by_label]
        if len(matched) != len(expected) or any(
                str(row["outcome_status"]) != "closed" for row in matched):
            continue
        variants = [{
            "label": str(labels.get(str(row["profile_id"]), row["profile_id"])),
            "outcome_status": row["outcome_status"],
            "close_reason": row["close_reason"],
            "highest_tp_touched": row["highest_tp_touched"],
            "net_pnl_usd": row["net_pnl_usd"],
            "net_r": row["net_r"],
            "exit_price": row["exit_price"],
        } for row in matched]
        first = matched[0]
        try:
            result = send_manual_paper_close(
                root=ROOT, db_path=db_path, signal_id=signal_id,
                asset_class="stocks", symbol=str(first["symbol"]),
                direction=str(first["direction"]),
                title="Liquidity Shock Reclaim · Paper",
                variants=variants, now=now,
            )
        except Exception:
            counts["skipped"] += 1
            continue
        key = ("sent" if result.get("sent") else
               "queued" if str(result.get("status", "")).startswith("queued:") else "skipped")
        counts[key] += 1
    return counts


def _refresh_candidates(symbols: list[str]) -> dict[str, int]:
    if not symbols:
        return {"attempted": 0, "fetched": 0, "failed": 0}
    from src.config import load_config
    from src.stocks.configs.loader import load_stocks_config
    from src.stocks.data_collectors.stock_ohlcv_collector import StockOHLCVCollector

    project = load_config(ROOT)
    collector = StockOHLCVCollector(project, load_stocks_config(ROOT))
    result = collector.collect_fast_batch(symbols, "1m", period="5d")
    fetched_symbols = {key.split("@", 1)[0] for key in result.fetched}
    missing = [symbol for symbol in symbols if str(symbol).upper() not in fetched_symbols]
    if missing:
        fallback = collector.collect(
            missing, ["1m"], period="5d", throttle_seconds=0.0, max_workers=4,
        )
        result.fetched.update(fallback.fetched)
        for key in list(result.failed):
            if key in fallback.fetched:
                result.failed.pop(key, None)
        result.failed.update(fallback.failed)
    return {"attempted": len(symbols), "fetched": len(result.fetched), "failed": len(result.failed)}


def _refresh_base_frames_if_due(symbols: list[str], stock_cfg: Any,
                                cfg: dict[str, Any], now: datetime) -> dict[str, Any]:
    """Batch-refresh the 15m universe immediately after each bar closes."""
    global _LAST_BASE_REFRESH_SLOT
    if not cfg.get("refresh_base_15m_on_close", True):
        return {"status": "disabled", "attempted": 0, "fetched": 0, "failed": 0}
    local = now.astimezone(NY)
    if local.weekday() >= 5 or not (time(9, 30) <= local.time() < time(16, 0)):
        return {"status": "outside_rth", "attempted": 0, "fetched": 0, "failed": 0}
    delay = max(0, int(cfg.get("base_refresh_delay_seconds", 5)))
    if local.minute % 15 == 0 and local.second < delay:
        return {"status": "bar_settling", "attempted": 0, "fetched": 0, "failed": 0}
    slot = now.replace(minute=now.minute - now.minute % 15, second=0, microsecond=0)
    if _LAST_BASE_REFRESH_SLOT == slot:
        return {"status": "not_due", "slot": slot.isoformat(),
                "attempted": 0, "fetched": 0, "failed": 0}

    universe = list(dict.fromkeys([
        *symbols, "SPY",
        *(stock_cfg.sector_etf_for(symbol) for symbol in symbols
          if stock_cfg.sector_etf_for(symbol)),
    ]))
    from src.config import load_config
    from src.stocks.data_collectors.stock_ohlcv_collector import StockOHLCVCollector

    started = time_module.monotonic()
    collector = StockOHLCVCollector(load_config(ROOT), stock_cfg)
    result = collector.collect_fast_batch(universe, "15m", period="5d")
    _LAST_BASE_REFRESH_SLOT = slot
    return {
        "status": "ok" if result.fetched else "batch_unavailable",
        "slot": slot.isoformat(), "attempted": len(universe),
        "fetched": len(result.fetched), "failed": len(result.failed),
        "elapsed_seconds": round(time_module.monotonic() - started, 3),
    }


def tick(*, db: str | None = None, persist: bool = True, now: datetime | None = None,
         cfg: dict[str, Any] | None = None, refresh_candidates: bool = True) -> dict[str, Any]:
    cfg, now = cfg or load_strategy_config(), now or utc_now()
    if not cfg.get("feature_flag"):
        return {"enabled": False, "rows": [], "summary_by_profile": {}}
    if cfg.get("live_enabled"):
        raise RuntimeError("stocks liquidity-shock v1 is Paper-only")
    from src.config import load_config
    from src.stocks.configs.loader import load_stocks_config

    stock_cfg = load_stocks_config(ROOT)
    universe = configured_symbols(cfg)
    base_refresh = (
        _refresh_base_frames_if_due(universe, stock_cfg, cfg, now)
        if persist and refresh_candidates else
        {"status": "skipped", "attempted": 0, "fetched": 0, "failed": 0}
    )
    path = Path(db) if db else load_config(ROOT).db_path
    # The dedicated 15-second Paper lane is idempotent. Do not let a slower
    # report writer turn one confirmation check into a 30-second stall.
    conn = sqlite3.connect(path, timeout=2.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA busy_timeout=2000")
    try:
        ensure_tables(conn)
        activated = _activation(conn, now, persist)
        expired_pending = _expire_stale_pending(conn, cfg, now, persist=persist)
        open_refresh = (
            _refresh_open_position_frames(conn, cfg, now, str(path.resolve()))
            if persist else
            {"status": "read_only", "attempted": 0, "fetched": 0, "failed": 0}
        )
        previously_open_ids = [str(row[0]) for row in conn.execute(
            f"SELECT candidate_id FROM {OUTCOME_TABLE} WHERE outcome_status='open'"
        ).fetchall()]
        matured = _mature_open(conn, cfg, now, persist=persist)
        open_tracking = _open_tracking_summary(conn)
        market = _cache_frame("SPY", "15m")
        sector_frames: dict[str, pd.DataFrame] = {}
        setups: list[tuple[str, dict[str, Any], pd.DataFrame]] = []
        scanned = 0
        for symbol in universe:
            frame = _cache_frame(symbol, "15m")
            if frame.empty:
                continue
            closed = frame[frame["timestamp"] + pd.Timedelta(minutes=15) <= pd.Timestamp(now)]
            if closed.empty:
                continue
            scanned += 1
            sector_etf = stock_cfg.sector_etf_for(symbol)
            if sector_etf and sector_etf not in sector_frames:
                sector_frames[sector_etf] = _cache_frame(sector_etf, "15m")
            sector = sector_frames.get(sector_etf, pd.DataFrame())
            liquidity = liquidity_snapshot(symbol, closed.iloc[-1]["timestamp"].to_pydatetime())
            first = max(0, len(closed) - int(cfg["recent_scan_bars"]))
            for idx in range(first, len(closed)):
                setup = detect_shock(closed, idx, market, sector, liquidity, cfg)
                decision_at = setup.get("decision_at")
                if not isinstance(decision_at, datetime) or decision_at < activated:
                    continue
                if not setup.get("ok"):
                    if setup.get("reason") not in {"FLUSH_TOO_SMALL", "FLUSH_PCT_TOO_SMALL", "RVOL_TOO_WEAK"}:
                        _record_observation(conn, cfg, symbol, setup, str(setup.get("reason")), now)
                    continue
                setup["sector_etf"] = sector_etf or None
                news = news_risk(conn, symbol, decision_at, cfg)
                setup["news_status"] = news["status"]
                setup["news_event_type"] = news.get("event_type")
                if news["blocked"]:
                    _record_observation(conn, cfg, symbol, setup, "NEGATIVE_FUNDAMENTAL_CATALYST", now)
                    continue
                history = closed.iloc[max(0, idx - 100):idx + 1].copy()
                setups.append((symbol, setup, history))
            # Observation rows are diagnostic only. Release their transaction
            # before scanning the next cached symbol so a 91-symbol Paper pass
            # cannot hold the live ledger's WAL writer lock for a full cycle.
            if persist and conn.in_transaction:
                conn.commit()

        candidate_cap = max(0, int(cfg.get("max_candidate_refresh_symbols", 24)))
        refresh = {
            "attempted": 0, "fetched": 0, "failed": 0,
            "eligible_symbols": 0, "selected_symbols": 0,
            "deferred_symbols": 0, "cap": candidate_cap,
        }
        if refresh_candidates and cfg.get("refresh_candidate_1m") and setups:
            eligible_symbols = {symbol for symbol, _, _ in setups}
            candidates = _select_candidate_refresh_symbols(
                setups, candidate_cap,
            )
            refresh = _refresh_candidates(candidates)
            refresh.update({
                "eligible_symbols": len(eligible_symbols),
                "selected_symbols": len(candidates),
                "deferred_symbols": max(0, len(eligible_symbols) - len(candidates)),
                "cap": candidate_cap,
            })
            try:
                from src.data_collectors.stocks_liquidity_shock_research_store import archive_runtime_frames

                archive_runtime_frames(candidates, ("1m", "15m"), root=ROOT)
            except Exception:
                pass

        inserted: list[dict[str, Any]] = []
        for symbol, setup, history in setups:
            for profile_name, profile in active_confirmation_profiles(cfg).items():
                result = _process_profile(conn, cfg, symbol, setup, profile_name,
                                          dict(profile), now, persist, history)
                if result:
                    inserted.append(result)
        rows = [dict(row) for row in conn.execute(f"SELECT * FROM {OUTCOME_TABLE}")]
        summaries: dict[str, dict[str, Any]] = {}
        for name, profile in active_confirmation_profiles(cfg).items():
            selected = [row for row in rows if row["profile_id"] == profile["profile_id"]]
            profile_activation = _dt(profile.get("activation_at")) or activated
            summary = clean_forward_summary(
                selected, activated_at=profile_activation.isoformat(), now=now,
                min_closed=int(cfg["min_clean_closed"]), min_days=float(cfg["min_forward_days"]),
                min_pf=float(cfg["min_profit_factor"]),
                max_review_drawdown_usd=float(cfg["max_review_drawdown_usd"]),
            )
            summaries[name] = summary
            if persist:
                # Keep one current evaluation per profile. Per-minute history
                # belongs in the immutable outcome rows; duplicating an
                # unchanged aggregate forever would only grow the main DB.
                conn.execute(f"DELETE FROM {EVAL_TABLE} WHERE profile_id=?",
                             (profile["profile_id"],))
                conn.execute(
                    f"INSERT OR REPLACE INTO {EVAL_TABLE} VALUES(?,?,?,?,?,?,?,?,?,?)",
                    (now.isoformat(), profile["profile_id"], summary["clean_closed"],
                     summary["net_pnl_usd"], summary["profit_factor"], summary["winrate"],
                     summary["max_drawdown_usd"], summary["forward_days"], summary["verdict"],
                     json_text(cfg)),
                )
        if persist:
            conn.commit()
        telegram_signals = {"sent": 0, "queued": 0, "skipped": 0}
        telegram_closes = {"sent": 0, "queued": 0, "skipped": 0}
        telegram_cfg = dict(cfg.get("manual_telegram_signals") or {})
        if persist and telegram_cfg.get("enabled"):
            from src.notifiers.manual_paper_signal import (
                latest_closed_minute, send_manual_paper_entry,
            )

            telegram_closes = _send_manual_paper_close_alerts(
                conn, cfg, path, previously_open_ids, now,
            )
            selected_ids = {str(value) for value in telegram_cfg.get("profile_ids") or []}
            labels = dict(telegram_cfg.get("profile_labels") or {})
            eligible_by_event: dict[str, list[dict[str, Any]]] = {}
            for row in inserted:
                if (str(row.get("profile_id")) in selected_ids
                        and row.get("eligibility_status") == "eligible"
                        and row.get("outcome_status") == "open"):
                    eligible_by_event.setdefault(str(row["raw_event_id"]), []).append(row)
            for raw_event_id, event_rows in eligible_by_event.items():
                symbol = str(event_rows[0]["symbol"])
                quote = latest_closed_minute(_cache_frame(symbol, "1m"), now=now)
                if quote is None:
                    telegram_signals["skipped"] += 1
                    continue
                variants = [{
                    "label": labels.get(str(row["profile_id"]),
                                         str(row.get("entry_profile") or "Paper")),
                    "entry": row["entry_price"], "stop": row["stop_price"],
                    "tp1": row["tp1"], "tp2": row["tp2"],
                } for row in event_rows]
                try:
                    result = send_manual_paper_entry(
                        root=ROOT, db_path=path,
                        signal_id=f"manual-paper:stocks:{raw_event_id}",
                        asset_class="stocks", symbol=symbol,
                        direction=event_rows[0]["direction"],
                        title="Liquidity Shock Reclaim · Paper",
                        entry_at=max(str(row["entry_ts"]) for row in event_rows),
                        reference_price=quote[0], reference_at=quote[1], variants=variants,
                        now=now, max_age_seconds=int(telegram_cfg.get("max_age_seconds", 180)),
                    )
                except Exception:
                    telegram_signals["skipped"] += 1
                    continue
                key = ("sent" if result.get("sent") else
                       "queued" if str(result.get("status", "")).startswith("queued:") else "skipped")
                telegram_signals[key] += 1
        return {"enabled": True, "paper_only": True, "symbols_scanned": scanned,
                "setups": len(setups), "rows": inserted, "closed_matured": matured,
                "pending_expired": expired_pending,
                "open_position_refresh": open_refresh,
                "open_tracking": open_tracking,
                "base_refresh": base_refresh, "candidate_refresh": refresh,
                "manual_telegram_signals": telegram_signals,
                "manual_telegram_closes": telegram_closes,
                "summary_by_profile": summaries}
    finally:
        conn.close()


def render_markdown(result: dict[str, Any]) -> str:
    lines = ["# Stocks Liquidity Shock Reclaim v1 - Paper", "",
             "Liquid RTH stock shock -> structural level breach -> market/sector/news gate -> closed 1m reclaim.",
             "Profiles are isolated Paper evidence and have no live route.", "",
             f"- enabled: `{result.get('enabled')}`",
             f"- symbols scanned: `{result.get('symbols_scanned', 0)}`",
             f"- qualifying events: `{result.get('setups', 0)}`",
             f"- new/updated rows: `{len(result.get('rows') or [])}`",
             f"- matured: `{result.get('closed_matured', 0)}`",
             f"- open positions: `{(result.get('open_tracking') or {}).get('open', 0)}`",
             f"- stale tracking: `{(result.get('open_tracking') or {}).get('stale', 0)}`",
             f"- Telegram close notices: `{result.get('manual_telegram_closes', {})}`"]
    for name, summary in (result.get("summary_by_profile") or {}).items():
        lines.extend(["", f"## {name}", "", f"- verdict: **{summary.get('verdict')}**",
                      f"- clean closed: `{summary.get('clean_closed', 0)}`",
                      f"- net: `${summary.get('net_pnl_usd', 0.0):.2f}`; PF: `{summary.get('profit_factor')}`"])
    return "\n".join(lines)


def write_report(result: dict[str, Any], path: str | None = None) -> str:
    target = ROOT / (path or load_strategy_config()["report_path"])
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_markdown(result) + "\n", encoding="utf-8")
    return str(target)


__all__ = [
    "OUTCOME_TABLE", "OBS_TABLE", "configured_symbols", "detect_shock",
    "detect_confirmation", "entry_geometry", "ensure_tables", "liquidity_snapshot",
    "active_confirmation_profiles", "load_strategy_config", "news_risk",
    "simulate_two_target", "tick", "write_report",
]
