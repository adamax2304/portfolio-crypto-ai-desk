"""Liquidity Sweep/Reclaim v2, isolated Paper evidence lane.

The v1 sweep entered as soon as the 5m liquidation-sweep candle closed.  This
version waits for a confirmed reclaim/hold near a higher-timeframe level before
it records a Paper entry.  It never queues live decisions or calls an exchange.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from src.execution import crypto_htf_liquidity_reclaim_shadow as htf
from src.execution import crypto_liquidity_sweep_shadow as v1
from src.execution.shadow_strategy_common import (
    clean_forward_summary,
    diagnostics_markdown,
    ensure_columns,
    json_text,
    load_yaml_block,
    normalize_frame,
    parse_dt,
    simulate_confirmed_close_entry,
    strategy_diagnostics,
    utc_now,
)


ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "config" / "paper" / "crypto" / "liquidity_sweep_reclaim_v2.yaml"
STRATEGY_KEY = "crypto_liquidity_sweep_reclaim_v2_paper"

DEFAULTS: dict[str, Any] = {
    "feature_flag": True,
    "strategy_id": "crypto_liquidity_sweep_reclaim_v2",
    "paper_lane": "paper_crypto_liquidity_sweep_reclaim_v2",
    "base_sweep_timeframe": "5m",
    "primary_exchange": "bybit",
    "max_symbols": 40,
    "recent_sweep_scan_bars": 24,
    "level_lookback_bars": 36,
    "level_touch_tolerance_bps": 12.0,
    "min_sweep_bps": 8.0,
    "min_wick_share": 0.45,
    "min_close_location": 0.60,
    "min_rvol": 1.20,
    "liquidation_window_minutes": 10,
    "min_liquidation_notional_usd": 50_000.0,
    "liquidation_sources": ["binance", "bybit"],
    "liquidation_observation_sources": ["binance", "bybit", "okx"],
    "min_oi_drop_pct": 0.25,
    "derivatives_freshness_minutes": 10,
    "liquidity_freshness_minutes": 10,
    "max_spread_bps": 22.0,
    "sessions": {"blocked": ["asia", "off"], "strict": ["europe"], "preferred": ["us"]},
    "europe_strict": {
        "min_liquidation_notional_usd_multiplier": 1.50,
        "min_rvol_multiplier": 1.15,
        "min_oi_drop_pct_multiplier": 1.25,
        "require_two_htf_timeframes": False,
    },
    "htf": {
        "enabled": True,
        "timeframes": ["1h", "4h"],
        "lookback_bars": 90,
        "pivot_left_bars": 3,
        "pivot_right_bars": 3,
        "zone_width_atr": 0.35,
        "max_distance_bps": 90.0,
    },
    "confirmation_profiles": {
        "RECLAIM_HOLD_5M_2BAR": {
            "profile_id": "crypto_liquidity_sweep_reclaim_5m_hold2_paper_v2",
            "confirmation_timeframe": "5m",
            "hold_bars": 2,
            "confirmation_window_bars": 6,
            "level_hold_buffer_atr": 0.08,
            "min_reclaim_close_distance_atr": 0.02,
            "min_progress_atr": 0.03,
            "strict_europe": True,
        },
        "RECLAIM_HOLD_15M_1BAR": {
            "profile_id": "crypto_liquidity_sweep_reclaim_15m_hold1_paper_v2",
            "confirmation_timeframe": "15m",
            "hold_bars": 1,
            "confirmation_window_bars": 4,
            "level_hold_buffer_atr": 0.08,
            "min_reclaim_close_distance_atr": 0.03,
            "min_progress_atr": 0.04,
            "strict_europe": True,
        },
    },
    "stop_buffer_atr": 0.14,
    "max_stop_distance_pct": 0.045,
    "target_r": [1.0, 2.0, 3.0],
    "max_entry_latency_seconds": 180.0,
    "max_holding_bars_by_profile": {"RECLAIM_HOLD_5M_2BAR": 72, "RECLAIM_HOLD_15M_1BAR": 48},
    "fee_profile": "bybit_non_vip_usdt_perp",
    "min_clean_closed": 30,
    "min_forward_days": 28,
    "min_profit_factor": 1.25,
    "max_review_drawdown_usd": 250.0,
    "report_path": "reports/CRYPTO_LIQUIDITY_SWEEP_RECLAIM_V2_PAPER.md",
}

OUTCOME_TABLE = "crypto_liquidity_sweep_reclaim_v2_paper_outcomes"
EVAL_TABLE = "crypto_liquidity_sweep_reclaim_v2_paper_evaluations"
OBS_TABLE = "crypto_liquidity_sweep_reclaim_v2_paper_observations"
META_TABLE = "crypto_liquidity_sweep_reclaim_v2_paper_meta"

OUTCOME_COLUMNS = (
    "candidate_id", "raw_event_id", "strategy_id", "profile_id", "paper_lane", "window",
    "generated_at", "decision_at", "sweep_at", "symbol", "direction", "entry_profile",
    "confirmation_timeframe", "confirmation_bars", "session_bucket", "level_price",
    "sweep_extreme", "sweep_close", "htf_timeframes_json", "htf_level_price",
    "htf_level_kind", "htf_pivot_at", "htf_distance_bps", "liquidation_notional_usd",
    "liquidation_event_ids_json", "oi_change_pct", "spread_bps", "eligibility_status",
    "rejection_reason", "data_status", "is_clean_for_edge", "entry_ts", "entry_price",
    "stop_price", "tp1", "tp2", "tp3", "outcome_status", "close_reason", "exit_price",
    "exit_ts", "gross_pnl_usd", "net_pnl_usd", "net_r", "fees_usd", "slippage_usd",
    "funding_usd", "funding_source", "funding_estimated", "funding_event_count",
    "risk_usd", "mfe_r", "mae_r", "protection_armed", "lock_armed",
    "highest_tp_touched", "bars_held", "latency_seconds", "features_json", "notes_json",
    "last_checked_at",
)

OBSERVATION_COLUMNS = (
    "observation_id", "raw_event_id", "strategy_id", "paper_lane", "evaluated_at",
    "decision_at", "sweep_at", "symbol", "direction", "entry_profile",
    "session_bucket", "level_price", "liquidation_notional_usd",
    "liquidation_event_ids_json", "rejection_reason", "features_json", "notes_json",
)

OUTCOME_DDL = f"""
CREATE TABLE IF NOT EXISTS {OUTCOME_TABLE} (
  candidate_id TEXT PRIMARY KEY, raw_event_id TEXT NOT NULL, strategy_id TEXT NOT NULL,
  profile_id TEXT NOT NULL, paper_lane TEXT NOT NULL, window TEXT NOT NULL,
  generated_at TEXT NOT NULL, decision_at TEXT NOT NULL, sweep_at TEXT NOT NULL,
  symbol TEXT NOT NULL, direction TEXT NOT NULL, entry_profile TEXT NOT NULL,
  confirmation_timeframe TEXT NOT NULL, confirmation_bars INTEGER, session_bucket TEXT,
  level_price REAL, sweep_extreme REAL, sweep_close REAL, htf_timeframes_json TEXT,
  htf_level_price REAL, htf_level_kind TEXT, htf_pivot_at TEXT, htf_distance_bps REAL,
  liquidation_notional_usd REAL, liquidation_event_ids_json TEXT, oi_change_pct REAL,
  spread_bps REAL, eligibility_status TEXT NOT NULL, rejection_reason TEXT,
  data_status TEXT, is_clean_for_edge INTEGER NOT NULL DEFAULT 0, entry_ts TEXT,
  entry_price REAL, stop_price REAL, tp1 REAL, tp2 REAL, tp3 REAL,
  outcome_status TEXT NOT NULL, close_reason TEXT, exit_price REAL, exit_ts TEXT,
  gross_pnl_usd REAL, net_pnl_usd REAL, net_r REAL, fees_usd REAL, slippage_usd REAL,
  funding_usd REAL, funding_source TEXT, funding_estimated INTEGER,
  funding_event_count INTEGER, risk_usd REAL, mfe_r REAL, mae_r REAL,
  protection_armed INTEGER, lock_armed INTEGER, highest_tp_touched INTEGER,
  bars_held INTEGER, latency_seconds REAL, features_json TEXT, notes_json TEXT,
  last_checked_at TEXT
)
"""

EVAL_DDL = f"""
CREATE TABLE IF NOT EXISTS {EVAL_TABLE} (
  generated_at TEXT NOT NULL, profile_id TEXT NOT NULL, strategy_id TEXT NOT NULL,
  activated_at TEXT, forward_rows INTEGER, clean_rows INTEGER, dirty_rows INTEGER,
  clean_closed INTEGER, net_pnl_usd REAL, net_r REAL, fees_usd REAL,
  slippage_usd REAL, funding_usd REAL, profit_factor REAL, winrate REAL,
  max_drawdown_usd REAL, forward_days REAL, verdict TEXT, diagnostics_json TEXT,
  config_json TEXT, PRIMARY KEY(generated_at, profile_id)
)
"""

OBSERVATION_DDL = f"""
CREATE TABLE IF NOT EXISTS {OBS_TABLE} (
  observation_id TEXT PRIMARY KEY, raw_event_id TEXT NOT NULL, strategy_id TEXT NOT NULL,
  paper_lane TEXT NOT NULL, evaluated_at TEXT NOT NULL, decision_at TEXT NOT NULL,
  sweep_at TEXT NOT NULL, symbol TEXT NOT NULL, direction TEXT NOT NULL,
  entry_profile TEXT, session_bucket TEXT, level_price REAL,
  liquidation_notional_usd REAL, liquidation_event_ids_json TEXT,
  rejection_reason TEXT NOT NULL, features_json TEXT, notes_json TEXT
)
"""
META_DDL = f"CREATE TABLE IF NOT EXISTS {META_TABLE} (k TEXT PRIMARY KEY, v TEXT NOT NULL)"


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    out = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = _deep_merge(dict(out[key]), value)
        else:
            out[key] = value
    return out


def load_strategy_config() -> dict[str, Any]:
    loaded = load_yaml_block(CONFIG_PATH, STRATEGY_KEY, DEFAULTS)
    return _deep_merge(DEFAULTS, loaded)


def ensure_tables(conn: sqlite3.Connection) -> None:
    conn.execute(OUTCOME_DDL)
    conn.execute(EVAL_DDL)
    conn.execute(OBSERVATION_DDL)
    conn.execute(META_DDL)
    text = {
        "raw_event_id", "strategy_id", "profile_id", "paper_lane", "window", "generated_at",
        "decision_at", "sweep_at", "symbol", "direction", "entry_profile",
        "confirmation_timeframe", "session_bucket", "htf_timeframes_json", "htf_level_kind",
        "htf_pivot_at", "liquidation_event_ids_json", "eligibility_status", "rejection_reason",
        "data_status", "entry_ts", "outcome_status", "close_reason", "exit_ts",
        "funding_source", "features_json", "notes_json", "last_checked_at",
    }
    integer = {
        "confirmation_bars", "is_clean_for_edge", "funding_estimated", "funding_event_count",
        "protection_armed", "lock_armed", "highest_tp_touched", "bars_held",
    }
    ensure_columns(conn, OUTCOME_TABLE, {
        col: "TEXT" if col in text else "INTEGER" if col in integer else "REAL"
        for col in OUTCOME_COLUMNS if col != "candidate_id"
    })
    conn.execute(f"CREATE INDEX IF NOT EXISTS idx_lsr_v2_state ON {OUTCOME_TABLE}(outcome_status,entry_ts)")
    conn.execute(f"CREATE INDEX IF NOT EXISTS idx_lsr_v2_symbol ON {OUTCOME_TABLE}(symbol,decision_at)")
    conn.execute(f"CREATE INDEX IF NOT EXISTS idx_lsr_v2_profile ON {OUTCOME_TABLE}(profile_id,outcome_status)")
    conn.execute(f"CREATE INDEX IF NOT EXISTS idx_lsr_v2_obs_reason ON {OBS_TABLE}(rejection_reason,decision_at)")


def _f(value: Any) -> float | None:
    try:
        return None if value in (None, "") or pd.isna(value) else float(value)
    except (TypeError, ValueError):
        return None


def _dt(value: Any) -> datetime | None:
    parsed = parse_dt(value)
    return parsed.astimezone(timezone.utc) if parsed else None


def _canon(symbol: str) -> str:
    return v1._canon(symbol)  # noqa: SLF001


def _minutes(timeframe: str) -> int:
    return htf._minutes(timeframe)  # noqa: SLF001


def _delta(timeframe: str) -> timedelta:
    return timedelta(minutes=_minutes(timeframe))


def _session(at: datetime) -> str:
    return v1._session(at)  # noqa: SLF001


def _atr(frame: pd.DataFrame, idx: int, periods: int = 14) -> float | None:
    return htf._atr(frame, idx, periods)  # noqa: SLF001


def _latest_closed_index(frame: pd.DataFrame, now: datetime, timeframe: str) -> int | None:
    return htf._latest_closed_index(frame, now, timeframe)  # noqa: SLF001


def _candidate_id(cfg: dict[str, Any], symbol: str, at: datetime, direction: str, profile_id: str) -> str:
    raw = f"{cfg['strategy_id']}|{_canon(symbol)}|{at.isoformat()}|{direction}|{profile_id}"
    return "clsrp2_" + hashlib.sha256(raw.encode()).hexdigest()[:22]


def _raw_event_id(cfg: dict[str, Any], symbol: str, at: datetime, direction: str) -> str:
    raw = f"raw|{cfg['strategy_id']}|{_canon(symbol)}|{at.isoformat()}|{direction}"
    return "clsr2e_" + hashlib.sha256(raw.encode()).hexdigest()[:22]


def _observation_id(cfg: dict[str, Any], symbol: str, at: datetime, direction: str, reason: str,
                    profile: str | None = None) -> str:
    raw = f"obs|{cfg['strategy_id']}|{_canon(symbol)}|{at.isoformat()}|{direction}|{profile or '-'}|{reason}"
    return "clsr2o_" + hashlib.sha256(raw.encode()).hexdigest()[:22]


def _json_cell(value: Any) -> Any:
    return value if isinstance(value, str) else json_text(value)


def _load_base_frame(symbol: str, cfg: dict[str, Any]) -> pd.DataFrame:
    legacy_cfg = dict(cfg)
    legacy_cfg["timeframe"] = cfg.get("base_sweep_timeframe") or "5m"
    return normalize_frame(v1._load_frame(symbol, legacy_cfg))  # noqa: SLF001


def _load_confirmation_frame(symbol: str, timeframe: str, cfg: dict[str, Any]) -> pd.DataFrame:
    if str(timeframe).lower() == str(cfg.get("base_sweep_timeframe") or "5m").lower():
        return _load_base_frame(symbol, cfg)
    return normalize_frame(htf._load_frame(symbol, timeframe))  # noqa: SLF001


def _symbols(conn: sqlite3.Connection, now: datetime, cfg: dict[str, Any]) -> list[str]:
    rows = v1._symbols(conn, now, cfg)  # noqa: SLF001
    if rows:
        return rows
    try:
        from src.data_collectors.crypto_invest_universe import load_selected_symbols

        return load_selected_symbols()[:int(cfg.get("max_symbols", 40))]
    except Exception:
        return []


def _event_rows(conn: sqlite3.Connection, symbol: str, at: datetime, cfg: dict[str, Any]) -> list[dict[str, Any]]:
    return v1._event_rows(conn, symbol, at, cfg)  # noqa: SLF001


def _contexts(conn: sqlite3.Connection, symbol: str, at: datetime, cfg: dict[str, Any]) -> dict[str, Any]:
    return v1._contexts(conn, symbol, at, cfg)  # noqa: SLF001


def _liquidation_source_status(conn: sqlite3.Connection, cfg: dict[str, Any], now: datetime) -> dict[str, Any]:
    return v1._liquidation_source_status(conn, cfg, now)  # noqa: SLF001


def _profile_items(cfg: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    return [(str(name), dict(profile)) for name, profile in dict(cfg.get("confirmation_profiles") or {}).items()]


def _funding_events(conn: sqlite3.Connection | None, symbol: str, entry_at: datetime,
                    now: datetime) -> list[dict[str, Any]]:
    return v1._funding_events(conn, symbol, entry_at, now)  # noqa: SLF001


def _decorate_setup(frame: pd.DataFrame, idx: int, setup: dict[str, Any]) -> dict[str, Any]:
    row = frame.iloc[idx]
    low, high, close = (_f(row.get(key)) for key in ("low", "high", "close"))
    if low is not None and high is not None:
        setup["sweep_extreme"] = low if setup.get("direction") == "long" else high
    if close is not None:
        setup["sweep_close"] = close
    return setup


def _htf_cfg(cfg: dict[str, Any], timeframe: str) -> dict[str, Any]:
    block = dict(cfg.get("htf") or {})
    return {
        "structure_timeframe": timeframe,
        "structure_lookback_bars": int(block.get("lookback_bars", 90)),
        "pivot_left_bars": int(block.get("pivot_left_bars", 3)),
        "pivot_right_bars": int(block.get("pivot_right_bars", 3)),
        "zone_width_atr": float(block.get("zone_width_atr", 0.35)),
    }


def _htf_matches(symbol: str, setup: dict[str, Any], cfg: dict[str, Any]) -> list[dict[str, Any]]:
    block = dict(cfg.get("htf") or {})
    if not block.get("enabled", True):
        return [{"timeframe": "disabled", "level": setup.get("level"), "kind": "range"}]
    decision_at = setup.get("decision_at")
    if not isinstance(decision_at, datetime):
        return []
    direction = str(setup.get("direction") or "")
    wanted_kind = "support" if direction == "long" else "resistance"
    level_price = _f(setup.get("level"))
    extreme = _f(setup.get("sweep_extreme"))
    reclaim_close = _f(setup.get("sweep_close")) or _f(setup.get("entry"))
    if level_price is None or extreme is None or reclaim_close is None:
        return []
    max_distance_bps = float(block.get("max_distance_bps", 90.0))
    matches: list[dict[str, Any]] = []
    for timeframe in block.get("timeframes") or ["1h", "4h"]:
        frame = normalize_frame(htf._load_frame(str(symbol), str(timeframe)))  # noqa: SLF001
        if frame.empty:
            continue
        for level in htf.confirmed_pivot_levels(frame, as_of=decision_at, cfg=_htf_cfg(cfg, str(timeframe))):
            if level.get("kind") != wanted_kind:
                continue
            price = float(level["price"])
            distance_bps = abs(level_price - price) / max(level_price, 1e-12) * 10_000.0
            zone_bps = float(level.get("zone_width") or 0.0) / max(price, 1e-12) * 10_000.0
            allowed_bps = max(max_distance_bps, zone_bps)
            near_range_level = distance_bps <= allowed_bps
            if direction == "long":
                swept_zone = extreme <= price + float(level.get("zone_width") or 0.0)
                reclaimed_zone = reclaim_close >= price - float(level.get("zone_width") or 0.0)
            else:
                swept_zone = extreme >= price - float(level.get("zone_width") or 0.0)
                reclaimed_zone = reclaim_close <= price + float(level.get("zone_width") or 0.0)
            if near_range_level or (swept_zone and reclaimed_zone):
                matches.append({
                    "timeframe": str(timeframe),
                    "kind": wanted_kind,
                    "price": price,
                    "zone_width": float(level.get("zone_width") or 0.0),
                    "pivot_at": level.get("pivot_at").isoformat() if hasattr(level.get("pivot_at"), "isoformat") else None,
                    "known_at": level.get("known_at").isoformat() if hasattr(level.get("known_at"), "isoformat") else None,
                    "distance_bps": round(distance_bps, 4),
                })
    return sorted(matches, key=lambda item: item["distance_bps"])


def _europe_strict_reason(setup: dict[str, Any], context: dict[str, Any], matches: list[dict[str, Any]],
                          cfg: dict[str, Any], profile: dict[str, Any]) -> str | None:
    if not profile.get("strict_europe", True):
        return None
    session = _session(setup["decision_at"])
    if session not in set((cfg.get("sessions") or {}).get("strict") or []):
        return None
    strict = dict(cfg.get("europe_strict") or {})
    min_notional = float(cfg["min_liquidation_notional_usd"]) * float(
        strict.get("min_liquidation_notional_usd_multiplier", 1.0)
    )
    if float(setup.get("liquidation_notional_usd") or 0.0) < min_notional:
        return "EUROPE_STRICT_LIQUIDATION_TOO_SMALL"
    min_rvol = float(cfg["min_rvol"]) * float(strict.get("min_rvol_multiplier", 1.0))
    if (_f(setup.get("rvol")) or 0.0) < min_rvol:
        return "EUROPE_STRICT_RVOL_TOO_WEAK"
    min_oi = float(cfg["min_oi_drop_pct"]) * float(strict.get("min_oi_drop_pct_multiplier", 1.0))
    if (_f(context.get("oi_change_pct")) is None) or float(context.get("oi_change_pct")) > -min_oi:
        return "EUROPE_STRICT_OI_NOT_FLUSHING"
    if strict.get("require_two_htf_timeframes"):
        if len({match.get("timeframe") for match in matches}) < 2:
            return "EUROPE_STRICT_HTF_CONFLUENCE_MISSING"
    return None


def detect_reclaim_entry(frame: pd.DataFrame, setup: dict[str, Any], now: datetime,
                         profile: dict[str, Any]) -> dict[str, Any]:
    """Return a confirmed reclaim entry, pending state, or terminal skip."""
    timeframe = str(profile.get("confirmation_timeframe") or "5m")
    frame = normalize_frame(frame)
    last = _latest_closed_index(frame, now, timeframe)
    decision_at = setup.get("decision_at")
    if frame.empty or last is None or not isinstance(decision_at, datetime):
        return {"status": "pending"}
    window_bars = int(profile.get("confirmation_window_bars", 4))
    window_end = decision_at + _delta(timeframe) * window_bars
    level = float(setup["level"])
    direction = str(setup["direction"])
    candles = frame.iloc[:last + 1].copy()
    candles["_close_at"] = candles["timestamp"] + pd.Timedelta(_delta(timeframe))
    candles = candles[(candles["_close_at"] > pd.Timestamp(decision_at)) &
                      (candles["_close_at"] <= pd.Timestamp(window_end))]
    holds: list[int] = []
    failed = False
    for index, candle in candles.iterrows():
        close, low, high = (_f(candle.get(key)) for key in ("close", "low", "high"))
        atr = _atr(frame, int(index))
        if None in (close, low, high, atr):
            continue
        buffer = float(atr) * float(profile.get("level_hold_buffer_atr", 0.08))
        progress = max(
            float(atr) * float(profile.get("min_reclaim_close_distance_atr", 0.02)),
            float(atr) * float(profile.get("min_progress_atr", 0.03)),
        )
        if direction == "long":
            hard_break = close < level - buffer
            holds_level = low >= level - buffer and close >= level + progress
        else:
            hard_break = close > level + buffer
            holds_level = high <= level + buffer and close <= level - progress
        if hard_break:
            failed = True
        if not holds_level:
            holds = []
            continue
        holds.append(int(index))
        required = int(profile.get("hold_bars", 1))
        consecutive = len(holds) >= required and all(
            holds[-offset] == holds[-offset - 1] + 1 for offset in range(1, required)
        ) if required > 1 else len(holds) >= 1
        if consecutive:
            entry_index = holds[-1]
            entry_at = _dt(frame.iloc[entry_index].get("timestamp"))
            entry = _f(frame.iloc[entry_index].get("close"))
            if entry_at is None or entry is None:
                return {"status": "pending"}
            return {
                "status": "entry",
                "entry_at": entry_at + _delta(timeframe),
                "entry": entry,
                "confirmation_bars": required,
                "confirmation_index": entry_index,
            }
    if pd.Timestamp(now) >= pd.Timestamp(window_end):
        return {"status": "skipped", "reason": "RECLAIM_FAILED" if failed else "RECLAIM_WINDOW_EXPIRED"}
    return {"status": "pending"}


def _entry_geometry(setup_or_row: dict[str, Any], entry: float, cfg: dict[str, Any]) -> dict[str, Any]:
    direction = str(setup_or_row["direction"])
    stop = _f(setup_or_row.get("stop") if "stop" in setup_or_row else setup_or_row.get("stop_price"))
    if stop is None:
        return {"ok": False, "reason": "INVALID_STOP_GEOMETRY"}
    risk = abs(entry - stop)
    if risk <= 0 or (direction == "long" and stop >= entry) or (direction == "short" and stop <= entry):
        return {"ok": False, "reason": "INVALID_STOP_GEOMETRY"}
    if risk / entry > float(cfg["max_stop_distance_pct"]):
        return {"ok": False, "reason": "STOP_TOO_WIDE"}
    targets = [entry + risk * float(r) if direction == "long" else entry - risk * float(r)
               for r in cfg.get("target_r") or [1.0, 2.0, 3.0]]
    return {"ok": True, "stop": stop, "risk": risk, "tp1": targets[0], "tp2": targets[1], "tp3": targets[2]}


def _upsert(conn: sqlite3.Connection, row: dict[str, Any]) -> None:
    values = [_json_cell(row.get(col)) if col.endswith("_json") else row.get(col) for col in OUTCOME_COLUMNS]
    columns = ",".join(OUTCOME_COLUMNS)
    updates = ",".join(f"{col}=excluded.{col}" for col in OUTCOME_COLUMNS if col != "candidate_id")
    conn.execute(
        f"INSERT INTO {OUTCOME_TABLE}({columns}) VALUES({','.join('?' for _ in OUTCOME_COLUMNS)}) "
        f"ON CONFLICT(candidate_id) DO UPDATE SET {updates}",
        values,
    )


def _record_observation(conn: sqlite3.Connection, cfg: dict[str, Any], symbol: str, now: datetime,
                        setup: dict[str, Any], reason: str, source_status: dict[str, Any],
                        profile_name: str | None = None) -> None:
    decision_at = setup.get("decision_at")
    sweep_at = setup.get("sweep_at")
    direction = str(setup.get("direction") or "")
    if not isinstance(decision_at, datetime) or not isinstance(sweep_at, datetime) or direction not in {"long", "short"}:
        return
    row = {
        "observation_id": _observation_id(cfg, symbol, decision_at, direction, reason, profile_name),
        "raw_event_id": _raw_event_id(cfg, symbol, decision_at, direction),
        "strategy_id": cfg["strategy_id"],
        "paper_lane": cfg["paper_lane"],
        "evaluated_at": now.isoformat(),
        "decision_at": decision_at.isoformat(),
        "sweep_at": sweep_at.isoformat(),
        "symbol": _canon(symbol),
        "direction": direction,
        "entry_profile": profile_name,
        "session_bucket": _session(decision_at),
        "level_price": setup.get("level"),
        "liquidation_notional_usd": setup.get("liquidation_notional_usd"),
        "liquidation_event_ids_json": setup.get("event_ids") or [],
        "rejection_reason": reason,
        "features_json": {
            "rvol": setup.get("rvol"),
            "wick_share": setup.get("wick_share"),
            "close_location": setup.get("close_location"),
            "level_touch_count": setup.get("level_touch_count"),
            "htf_matches": setup.get("htf_matches") or [],
        },
        "notes_json": {
            "liquidation_source_status": source_status.get("status"),
            "feed_available": source_status.get("feed_available"),
            "paper_only": True,
        },
    }
    values = [_json_cell(row.get(col)) if col.endswith("_json") else row.get(col) for col in OBSERVATION_COLUMNS]
    columns = ",".join(OBSERVATION_COLUMNS)
    updates = ",".join(f"{col}=excluded.{col}" for col in OBSERVATION_COLUMNS if col != "observation_id")
    conn.execute(
        f"INSERT INTO {OBS_TABLE}({columns}) VALUES({','.join('?' for _ in OBSERVATION_COLUMNS)}) "
        f"ON CONFLICT(observation_id) DO UPDATE SET {updates}",
        values,
    )


def _activation(conn: sqlite3.Connection, now: datetime, persist: bool) -> datetime:
    row = conn.execute(f"SELECT v FROM {META_TABLE} WHERE k='activated_at'").fetchone()
    activated = _dt(row[0]) if row else None
    if activated:
        return activated
    if persist:
        conn.execute(f"INSERT OR REPLACE INTO {META_TABLE}(k,v) VALUES('activated_at',?)", (now.isoformat(),))
    return now


def _base_row(cfg: dict[str, Any], symbol: str, now: datetime, setup: dict[str, Any],
              context: dict[str, Any], matches: list[dict[str, Any]], profile_name: str,
              profile: dict[str, Any], status: str, reason: str | None) -> dict[str, Any]:
    decision_at = setup["decision_at"]
    profile_id = str(profile["profile_id"])
    first_match = matches[0] if matches else {}
    row = {column: None for column in OUTCOME_COLUMNS}
    row.update({
        "candidate_id": _candidate_id(cfg, symbol, decision_at, setup["direction"], profile_id),
        "raw_event_id": _raw_event_id(cfg, symbol, decision_at, setup["direction"]),
        "strategy_id": cfg["strategy_id"],
        "profile_id": profile_id,
        "paper_lane": cfg["paper_lane"],
        "window": "forward_post_activation",
        "generated_at": now.isoformat(),
        "decision_at": decision_at.isoformat(),
        "sweep_at": setup["sweep_at"].isoformat(),
        "symbol": _canon(symbol),
        "direction": setup["direction"],
        "entry_profile": profile_name,
        "confirmation_timeframe": str(profile.get("confirmation_timeframe") or "5m"),
        "session_bucket": _session(decision_at),
        "level_price": setup["level"],
        "sweep_extreme": setup.get("sweep_extreme"),
        "sweep_close": setup.get("sweep_close") or setup.get("entry"),
        "htf_timeframes_json": sorted({match.get("timeframe") for match in matches if match.get("timeframe")}),
        "htf_level_price": first_match.get("price"),
        "htf_level_kind": first_match.get("kind"),
        "htf_pivot_at": first_match.get("pivot_at"),
        "htf_distance_bps": first_match.get("distance_bps"),
        "liquidation_notional_usd": setup.get("liquidation_notional_usd"),
        "liquidation_event_ids_json": setup.get("event_ids") or [],
        "oi_change_pct": context.get("oi_change_pct"),
        "spread_bps": context.get("spread_bps"),
        "eligibility_status": status,
        "rejection_reason": reason,
        "data_status": "ok" if status == "eligible" else "pending" if status == "pending_confirmation" else "dirty",
        "is_clean_for_edge": 1 if status == "eligible" else 0,
        "outcome_status": "open" if status == "eligible" else "pending" if status == "pending_confirmation" else "skipped",
        "latency_seconds": max(0.0, (now - decision_at).total_seconds()),
        "features_json": {
            "rvol": setup.get("rvol"),
            "wick_share": setup.get("wick_share"),
            "close_location": setup.get("close_location"),
            "level_touch_count": setup.get("level_touch_count"),
            "would_pass_two_touch_level": setup.get("would_pass_two_touch_level"),
            "oi_venue_pairs": context.get("oi_venue_pairs"),
            "liquidation_sources": setup.get("liquidation_exchanges") or [],
            "htf_matches": matches,
        },
        "notes_json": {
            "paper_only": True,
            "live_locked": True,
            "v1_live_retired": True,
            "entry_logic": "5m liquidation sweep -> 1h/4h level -> closed reclaim/hold",
        },
        "last_checked_at": now.isoformat(),
    })
    return row


def _apply_entry(row: dict[str, Any], confirmation: dict[str, Any], geometry: dict[str, Any],
                 now: datetime) -> dict[str, Any]:
    row.update({
        "entry_ts": confirmation["entry_at"].isoformat(),
        "entry_price": float(confirmation["entry"]),
        "stop_price": geometry["stop"],
        "tp1": geometry["tp1"],
        "tp2": geometry["tp2"],
        "tp3": geometry["tp3"],
        "confirmation_bars": confirmation.get("confirmation_bars"),
        "eligibility_status": "eligible",
        "rejection_reason": None,
        "data_status": "ok",
        "is_clean_for_edge": 1,
        "outcome_status": "open",
        "latency_seconds": max(0.0, (now - confirmation["entry_at"]).total_seconds()),
        "features_json": {
            **_decode_json(row.get("features_json")),
            "confirmation": {k: v for k, v in confirmation.items() if k != "entry_at"} | {
                "entry_at": confirmation["entry_at"].isoformat()
            },
            "stop_distance_pct": abs(float(confirmation["entry"]) - float(geometry["stop"])) / float(confirmation["entry"]),
        },
        "last_checked_at": now.isoformat(),
    })
    return row


def _entry_is_stale(confirmation: dict[str, Any], now: datetime, cfg: dict[str, Any]) -> bool:
    entry_at = confirmation.get("entry_at")
    if not isinstance(entry_at, datetime):
        return True
    age = max(0.0, (now - entry_at).total_seconds())
    return age > float(cfg.get("max_entry_latency_seconds", 180.0))


def _decode_json(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    try:
        parsed = json.loads(str(value or "{}"))
        return parsed if isinstance(parsed, dict) else {}
    except (TypeError, ValueError):
        return {}


def _setup_from_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "decision_at": _dt(row.get("decision_at")),
        "sweep_at": _dt(row.get("sweep_at")),
        "direction": row.get("direction"),
        "level": row.get("level_price"),
        "sweep_extreme": row.get("sweep_extreme"),
        "sweep_close": row.get("sweep_close"),
        "entry": row.get("sweep_close"),
        "stop": row.get("stop_price"),
    }


def _mature_pending(conn: sqlite3.Connection, now: datetime, cfg: dict[str, Any]) -> tuple[int, int]:
    by_name = {name: profile for name, profile in _profile_items(cfg)}
    rows = conn.execute(f"SELECT * FROM {OUTCOME_TABLE} WHERE outcome_status='pending'").fetchall()
    entered = skipped = 0
    for raw in rows:
        row = dict(raw)
        profile = by_name.get(str(row.get("entry_profile")))
        if not profile:
            row.update({"outcome_status": "skipped", "eligibility_status": "rejected",
                        "rejection_reason": "PROFILE_NOT_CONFIGURED", "last_checked_at": now.isoformat()})
            _upsert(conn, row)
            skipped += 1
            continue
        frame = _load_confirmation_frame(str(row["symbol"]), str(row["confirmation_timeframe"]), cfg)
        confirmation = detect_reclaim_entry(frame, _setup_from_row(row), now, profile)
        if confirmation["status"] == "pending":
            continue
        if confirmation["status"] == "skipped":
            row.update({"outcome_status": "skipped", "eligibility_status": "rejected",
                        "rejection_reason": confirmation["reason"], "data_status": "dirty",
                        "is_clean_for_edge": 0, "last_checked_at": now.isoformat(),
                        "features_json": {**_decode_json(row.get("features_json")), "confirmation": confirmation}})
            _upsert(conn, row)
            skipped += 1
            continue
        if _entry_is_stale(confirmation, now, cfg):
            row.update({"outcome_status": "skipped", "eligibility_status": "rejected",
                        "rejection_reason": "STALE_RECLAIM_ENTRY", "data_status": "dirty",
                        "is_clean_for_edge": 0, "last_checked_at": now.isoformat(),
                        "features_json": {**_decode_json(row.get("features_json")), "confirmation": confirmation}})
            _upsert(conn, row)
            skipped += 1
            continue
        geometry = _entry_geometry(_setup_from_row(row), float(confirmation["entry"]), cfg)
        if not geometry.get("ok"):
            row.update({"outcome_status": "skipped", "eligibility_status": "rejected",
                        "rejection_reason": geometry["reason"], "data_status": "dirty",
                        "is_clean_for_edge": 0, "last_checked_at": now.isoformat(),
                        "features_json": {**_decode_json(row.get("features_json")), "confirmation": confirmation}})
            _upsert(conn, row)
            skipped += 1
            continue
        _upsert(conn, _apply_entry(row, confirmation, geometry, now))
        entered += 1
    return entered, skipped


def _invalidate_stale_open_rows(conn: sqlite3.Connection, now: datetime, cfg: dict[str, Any]) -> int:
    limit = float(cfg.get("max_entry_latency_seconds", 180.0))
    rows = conn.execute(
        f"SELECT candidate_id,features_json FROM {OUTCOME_TABLE} "
        "WHERE outcome_status='open' AND latency_seconds>? "
        "AND close_reason IS NULL AND net_pnl_usd IS NULL",
        (limit,),
    ).fetchall()
    for raw in rows:
        features = _decode_json(raw["features_json"])
        features["stale_repair"] = {
            "reason": "entry row was created after max_entry_latency_seconds",
            "max_entry_latency_seconds": limit,
        }
        conn.execute(
            f"UPDATE {OUTCOME_TABLE} SET outcome_status='skipped',eligibility_status='rejected',"
            "rejection_reason='STALE_RECLAIM_ENTRY',data_status='dirty',is_clean_for_edge=0,"
            "features_json=?,last_checked_at=? WHERE candidate_id=?",
            (json_text(features), now.isoformat(), raw["candidate_id"]),
        )
    return len(rows)


def _max_holding_bars(cfg: dict[str, Any], profile_name: str) -> int:
    block = dict(cfg.get("max_holding_bars_by_profile") or {})
    return int(block.get(profile_name, block.get("default", 72)))


def _mature_open(conn: sqlite3.Connection, intelligence: sqlite3.Connection, now: datetime,
                 cfg: dict[str, Any]) -> int:
    rows = conn.execute(f"SELECT * FROM {OUTCOME_TABLE} WHERE outcome_status='open'").fetchall()
    closed = 0
    for raw in rows:
        row = dict(raw)
        entry_at = _dt(row.get("entry_ts"))
        if entry_at is None:
            continue
        frame = _load_confirmation_frame(str(row["symbol"]), str(row["confirmation_timeframe"]), cfg)
        future = frame[frame["timestamp"] >= pd.Timestamp(entry_at)]
        if future.empty:
            continue
        max_bars = _max_holding_bars(cfg, str(row["entry_profile"]))
        force_close = len(future) >= max_bars
        sim = simulate_confirmed_close_entry(
            direction=str(row["direction"]),
            entry=float(row["entry_price"]),
            stop=float(row["stop_price"]),
            tp1=float(row["tp1"]),
            tp2=float(row["tp2"]),
            tp3=float(row["tp3"]),
            future_candles=future.iloc[:max_bars],
            symbol=str(row["symbol"]),
            fee_profile=str(cfg["fee_profile"]),
            entry_at=entry_at,
            bar_minutes=_minutes(str(row["confirmation_timeframe"])),
            funding_events=_funding_events(intelligence, str(row["symbol"]), entry_at, now),
            force_close=force_close,
        ).to_dict()
        row.update({"outcome_status": sim.get("status")})
        row.update({key: value for key, value in sim.items() if key in OUTCOME_COLUMNS})
        row["last_checked_at"] = now.isoformat()
        _upsert(conn, row)
        closed += int(row.get("outcome_status") == "closed")
    return closed


def _process_setup(conn: sqlite3.Connection, cfg: dict[str, Any], symbol: str, now: datetime,
                   setup: dict[str, Any], context: dict[str, Any], matches: list[dict[str, Any]],
                   source_status: dict[str, Any], persist: bool) -> list[dict[str, Any]]:
    inserted: list[dict[str, Any]] = []
    for profile_name, profile in _profile_items(cfg):
        profile_id = str(profile["profile_id"])
        cid = _candidate_id(cfg, symbol, setup["decision_at"], setup["direction"], profile_id)
        if conn.execute(f"SELECT 1 FROM {OUTCOME_TABLE} WHERE candidate_id=?", (cid,)).fetchone():
            continue
        reason = _europe_strict_reason(setup, context, matches, cfg, profile)
        frame = _load_confirmation_frame(symbol, str(profile.get("confirmation_timeframe") or "5m"), cfg)
        confirmation = {"status": "skipped", "reason": reason} if reason else detect_reclaim_entry(frame, setup, now, profile)
        if confirmation["status"] == "pending":
            row = _base_row(cfg, symbol, now, setup, context, matches, profile_name, profile,
                            "pending_confirmation", None)
        elif confirmation["status"] == "skipped":
            reason = str(confirmation.get("reason") or reason or "RECLAIM_FAILED")
            row = _base_row(cfg, symbol, now, setup, context, matches, profile_name, profile,
                            "rejected", reason)
            if persist:
                _record_observation(conn, cfg, symbol, now, setup, reason, source_status, profile_name)
        else:
            if _entry_is_stale(confirmation, now, cfg):
                row = _base_row(cfg, symbol, now, setup, context, matches, profile_name, profile,
                                "rejected", "STALE_RECLAIM_ENTRY")
                if persist:
                    _record_observation(conn, cfg, symbol, now, setup, "STALE_RECLAIM_ENTRY", source_status, profile_name)
                    _upsert(conn, row)
                inserted.append(row)
                continue
            geometry = _entry_geometry(setup, float(confirmation["entry"]), cfg)
            if geometry.get("ok"):
                row = _apply_entry(
                    _base_row(cfg, symbol, now, setup, context, matches, profile_name, profile,
                              "eligible", None),
                    confirmation,
                    geometry,
                    now,
                )
            else:
                reason = str(geometry.get("reason") or "INVALID_STOP_GEOMETRY")
                row = _base_row(cfg, symbol, now, setup, context, matches, profile_name, profile,
                                "rejected", reason)
                if persist:
                    _record_observation(conn, cfg, symbol, now, setup, reason, source_status, profile_name)
        if persist:
            _upsert(conn, row)
        inserted.append(row)
    return inserted


def tick(*, db: str | None = None, persist: bool = True, now: datetime | None = None,
         cfg: dict[str, Any] | None = None) -> dict[str, Any]:
    cfg = cfg or load_strategy_config()
    now = now or utc_now()
    if not cfg.get("feature_flag"):
        return {"enabled": False, "rows": [], "entered_from_pending": 0, "closed_matured": 0,
                "summary_by_profile": {}}
    from src.config import load_config
    from src.data_collectors import market_intelligence_store as mi

    path = Path(db) if db else load_config().db_path
    trading = sqlite3.connect(":memory:" if not persist and not path.exists() else path, timeout=30.0)
    trading.row_factory = sqlite3.Row
    trading.execute("PRAGMA busy_timeout=30000")
    if not persist and path.exists():
        trading.execute("BEGIN")
    intelligence = mi.connect(ensure=False)
    try:
        ensure_tables(trading)
        activated = _activation(trading, now, persist)
        stale_invalidated = _invalidate_stale_open_rows(trading, now, cfg)
        entered, confirmation_skipped = _mature_pending(trading, now, cfg)
        closed = _mature_open(trading, intelligence, now, cfg)
        source_status = _liquidation_source_status(intelligence, cfg, now)
        inserted: list[dict[str, Any]] = []
        observations = 0
        blocked_sessions = set((cfg.get("sessions") or {}).get("blocked") or [])
        symbols = _symbols(intelligence, now, cfg)
        for symbol in symbols:
            frame = _load_base_frame(symbol, cfg)
            last = _latest_closed_index(frame, now, str(cfg.get("base_sweep_timeframe") or "5m"))
            if last is None:
                continue
            start = max(int(cfg["level_lookback_bars"]) + 14, last - int(cfg.get("recent_sweep_scan_bars", 24)) + 1)
            for idx in range(start, last + 1):
                bar_at = _dt(frame.iloc[idx].get("timestamp"))
                if bar_at is None:
                    continue
                decision_at = bar_at + _delta(str(cfg.get("base_sweep_timeframe") or "5m"))
                events = _event_rows(intelligence, symbol, decision_at, cfg)
                setup = v1.detect_sweep(
                    frame, idx, events, cfg,
                    liquidation_feed_available=bool(source_status.get("feed_available")),
                )
                if not setup.get("ok"):
                    if persist and setup.get("decision_at") and setup.get("direction"):
                        setup = _decorate_setup(frame, idx, setup)
                        _record_observation(trading, cfg, symbol, now, setup, str(setup.get("reason")), source_status)
                        observations += 1
                    continue
                setup = _decorate_setup(frame, idx, setup)
                if _session(setup["decision_at"]) in blocked_sessions:
                    if persist:
                        _record_observation(trading, cfg, symbol, now, setup, "WEAK_SESSION_BLOCKED", source_status)
                        observations += 1
                    continue
                matches = _htf_matches(symbol, setup, cfg)
                setup["htf_matches"] = matches
                if not matches:
                    if persist:
                        _record_observation(trading, cfg, symbol, now, setup, "NO_HTF_LEVEL", source_status)
                        observations += 1
                    continue
                context = _contexts(intelligence, symbol, setup["decision_at"], cfg)
                if not context.get("ok"):
                    if persist:
                        _record_observation(trading, cfg, symbol, now, setup, str(context.get("reason")), source_status)
                        observations += 1
                    continue
                inserted.extend(_process_setup(trading, cfg, symbol, now, setup, context, matches, source_status, persist))
        all_rows = [dict(row) for row in trading.execute(f"SELECT * FROM {OUTCOME_TABLE}")]
        observation_reasons = [
            dict(row) for row in trading.execute(
                f"SELECT rejection_reason,COUNT(*) AS rows,MAX(decision_at) AS latest_decision_at "
                f"FROM {OBS_TABLE} GROUP BY rejection_reason ORDER BY rows DESC LIMIT 12"
            ).fetchall()
        ]
        summary_by_profile: dict[str, dict[str, Any]] = {}
        diagnostics_by_profile: dict[str, dict[str, Any]] = {}
        for profile_name, profile in _profile_items(cfg):
            profile_id = str(profile["profile_id"])
            rows = [row for row in all_rows if row.get("profile_id") == profile_id]
            summary_by_profile[profile_name] = clean_forward_summary(
                rows,
                activated_at=activated.isoformat(),
                now=now,
                min_closed=int(cfg["min_clean_closed"]),
                min_days=float(cfg["min_forward_days"]),
                min_pf=float(cfg["min_profit_factor"]),
                max_review_drawdown_usd=float(cfg["max_review_drawdown_usd"]),
            )
            diagnostics_by_profile[profile_name] = strategy_diagnostics(
                rows, group_keys=("direction", "session_bucket", "rejection_reason", "entry_profile")
            )
        if persist:
            cols = ("generated_at", "profile_id", "strategy_id", "activated_at", "forward_rows",
                    "clean_rows", "dirty_rows", "clean_closed", "net_pnl_usd", "net_r",
                    "fees_usd", "slippage_usd", "funding_usd", "profit_factor", "winrate",
                    "max_drawdown_usd", "forward_days", "verdict", "diagnostics_json",
                    "config_json")
            for profile_name, profile in _profile_items(cfg):
                summary = summary_by_profile[profile_name]
                diagnostics = diagnostics_by_profile[profile_name]
                trading.execute(
                    f"INSERT OR REPLACE INTO {EVAL_TABLE}({','.join(cols)}) "
                    f"VALUES({','.join('?' for _ in cols)})",
                    (
                        now.isoformat(), profile["profile_id"], cfg["strategy_id"], activated.isoformat(),
                        summary["forward_rows"], summary["clean_rows"], summary["dirty_rows"],
                        summary["clean_closed"], summary["net_pnl_usd"], summary["net_r"],
                        summary["fees_usd"], summary["slippage_usd"], summary["funding_usd"],
                        summary["profit_factor"], summary["winrate"], summary["max_drawdown_usd"],
                        summary["forward_days"], summary["verdict"], json_text(diagnostics), json_text(cfg),
                    ),
                )
            trading.commit()
        else:
            trading.rollback()
        return {
            "enabled": True,
            "rows": inserted,
            "entered_from_pending": entered,
            "confirmation_skipped": confirmation_skipped,
            "stale_invalidated": stale_invalidated,
            "closed_matured": closed,
            "observations": observations,
            "symbol_count": len(symbols),
            "summary_by_profile": summary_by_profile,
            "diagnostics_by_profile": diagnostics_by_profile,
            "liquidation_source": source_status,
            "observation_reasons": observation_reasons,
        }
    finally:
        intelligence.close()
        trading.close()


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# Crypto Liquidity Sweep/Reclaim v2 - Paper",
        "",
        "5m observed liquidation sweep -> confirmed 1h/4h level -> closed reclaim/hold -> Paper entry.",
        "v1 live is retired; this v2 lane never queues live decisions or exchange orders.",
        "",
        f"- enabled: `{result.get('enabled')}`",
        f"- liquidation source: `{(result.get('liquidation_source') or {}).get('status', 'unknown')}` "
        f"(transport `{(result.get('liquidation_source') or {}).get('transport_status', 'unknown')}`)",
        f"- new rows: `{len(result.get('rows') or [])}` · entered from pending: `{result.get('entered_from_pending', 0)}` · "
        f"confirmation skips: `{result.get('confirmation_skipped', 0)}` · stale invalidated: `{result.get('stale_invalidated', 0)}` · "
        f"matured: `{result.get('closed_matured', 0)}` · "
        f"observations: `{result.get('observations', 0)}` · symbols scanned: `{result.get('symbol_count', 0)}`",
    ]
    reasons = result.get("observation_reasons") or []
    if reasons:
        lines.extend([
            "",
            "## Observation Blocks",
            "",
            "| reason | rows | latest decision |",
            "|---|---:|---|",
        ])
        for row in reasons:
            lines.append(
                f"| `{row.get('rejection_reason')}` | {int(row.get('rows') or 0)} | "
                f"{row.get('latest_decision_at') or '-'} |"
            )
    for profile_name, summary in (result.get("summary_by_profile") or {}).items():
        lines.extend([
            "",
            f"## {profile_name}",
            "",
            f"- verdict: **{summary.get('verdict')}** · clean closed: `{summary.get('clean_closed', 0)}` · "
            f"net USD: `{summary.get('net_pnl_usd', 0.0):.2f}` · PF: `{summary.get('profit_factor')}`",
            "",
        ])
        lines.extend(diagnostics_markdown((result.get("diagnostics_by_profile") or {}).get(profile_name) or {}))
    return "\n".join(lines)


def write_report(result: dict[str, Any], path: str | None = None) -> str:
    target = ROOT / (path or load_strategy_config()["report_path"])
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_markdown(result) + "\n", encoding="utf-8")
    return str(target)


__all__ = [
    "OUTCOME_TABLE", "OBS_TABLE", "detect_reclaim_entry", "ensure_tables",
    "load_strategy_config", "render_markdown", "tick", "write_report",
]
