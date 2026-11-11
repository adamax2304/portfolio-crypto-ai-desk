"""Observed-liquidation sweep reversal, isolated to one Shadow lane.

This is deliberately distinct from Derivatives Reset: it fades a completed
sweep back *inside* a prior range after an observed force-order event.
It never generates a desk signal, writes Paper state, or calls live routing.
The derivatives monitor may independently hand only fresh clean rows to a
version-pinned bridge after this function returns.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from src.execution.shadow_strategy_common import (
    clean_forward_summary, diagnostics_markdown, ensure_columns, json_text,
    load_yaml_block, normalize_frame, parse_dt, simulate_confirmed_close_entry,
    strategy_diagnostics, utc_now,
)

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "config" / "shadow_crypto_liquidity_sweep.yaml"
STRATEGY_KEY = "crypto_liquidity_sweep_v1"

DEFAULTS: dict[str, Any] = {
    "feature_flag": True, "strategy_id": STRATEGY_KEY,
    "profile_id": "crypto_liquidity_sweep_reversal_5m_v1",
    "shadow_lane": "shadow_crypto_liquidity_sweep", "timeframe": "5m",
    "primary_exchange": "bybit", "max_symbols": 40, "level_lookback_bars": 36,
    "level_touch_tolerance_bps": 12.0,
    "min_sweep_bps": 8.0, "min_wick_share": 0.45, "min_close_location": 0.60,
    "min_rvol": 1.25, "liquidation_window_minutes": 10,
    "min_liquidation_notional_usd": 50_000, "liquidation_sources": ["binance", "bybit"],
    "liquidation_observation_sources": ["binance", "bybit", "okx"],
    "min_oi_drop_pct": 0.25,
    "derivatives_freshness_minutes": 10, "liquidity_freshness_minutes": 10,
    "max_spread_bps": 20.0, "block_sessions": ["asia", "off"],
    "stop_buffer_atr": 0.12, "max_stop_distance_pct": 0.035,
    "target_r": [1.0, 2.0, 3.0], "max_holding_bars": 72,
    "fee_profile": "bybit_non_vip_usdt_perp", "min_clean_closed": 30,
    "min_forward_days": 28, "min_profit_factor": 1.25,
    "max_review_drawdown_usd": 250.0,
    "report_path": "reports/CRYPTO_LIQUIDITY_SWEEP_V1_SHADOW.md",
}

OUTCOME_COLUMNS = (
    "candidate_id", "strategy_id", "profile_id", "shadow_lane", "window", "generated_at",
    "decision_at", "sweep_at", "symbol", "direction", "session_bucket", "level_price",
    "liquidation_notional_usd", "liquidation_event_ids_json", "oi_change_pct", "spread_bps",
    "eligibility_status", "rejection_reason", "data_status", "is_clean_for_edge", "entry_ts",
    "entry_price", "stop_price", "tp1", "tp2", "tp3", "outcome_status", "close_reason",
    "exit_price", "exit_ts", "gross_pnl_usd", "net_pnl_usd", "net_r", "fees_usd",
    "slippage_usd", "funding_usd", "risk_usd", "mfe_r", "mae_r", "protection_armed",
    "lock_armed", "highest_tp_touched", "bars_held", "latency_seconds", "features_json",
    "notes_json", "last_checked_at",
)

# Rejected structural sweeps are deliberately separate from outcomes.  This
# lets the lane explain whether it lacks events, has weak structure, or is
# being filtered, without contaminating its executed-only edge measurement.
OBSERVATION_COLUMNS = (
    "observation_id", "strategy_id", "profile_id", "shadow_lane", "evaluated_at",
    "decision_at", "sweep_at", "symbol", "direction", "session_bucket",
    "level_price", "liquidation_notional_usd", "liquidation_event_ids_json",
    "rejection_reason", "features_json", "notes_json",
)

OUTCOME_DDL = """
CREATE TABLE IF NOT EXISTS crypto_liquidity_sweep_v1_shadow_outcomes (
  candidate_id TEXT PRIMARY KEY, strategy_id TEXT NOT NULL, profile_id TEXT NOT NULL,
  shadow_lane TEXT NOT NULL, window TEXT NOT NULL, generated_at TEXT NOT NULL,
  decision_at TEXT NOT NULL, sweep_at TEXT NOT NULL, symbol TEXT NOT NULL, direction TEXT NOT NULL,
  session_bucket TEXT, level_price REAL, liquidation_notional_usd REAL, liquidation_event_ids_json TEXT,
  oi_change_pct REAL, spread_bps REAL, eligibility_status TEXT NOT NULL, rejection_reason TEXT,
  data_status TEXT, is_clean_for_edge INTEGER NOT NULL DEFAULT 0, entry_ts TEXT, entry_price REAL,
  stop_price REAL, tp1 REAL, tp2 REAL, tp3 REAL, outcome_status TEXT, close_reason TEXT,
  exit_price REAL, exit_ts TEXT, gross_pnl_usd REAL, net_pnl_usd REAL, net_r REAL, fees_usd REAL,
  slippage_usd REAL, funding_usd REAL, risk_usd REAL, mfe_r REAL, mae_r REAL,
  protection_armed INTEGER, lock_armed INTEGER, highest_tp_touched INTEGER, bars_held INTEGER,
  latency_seconds REAL, features_json TEXT, notes_json TEXT, last_checked_at TEXT
)
"""
EVAL_DDL = """
CREATE TABLE IF NOT EXISTS crypto_liquidity_sweep_v1_shadow_evaluations (
  generated_at TEXT PRIMARY KEY, strategy_id TEXT, profile_id TEXT, activated_at TEXT,
  forward_rows INTEGER, clean_rows INTEGER, dirty_rows INTEGER, clean_closed INTEGER,
  net_pnl_usd REAL, net_r REAL, fees_usd REAL, slippage_usd REAL, funding_usd REAL,
  profit_factor REAL, winrate REAL, max_drawdown_usd REAL, forward_days REAL, verdict TEXT,
  diagnostics_json TEXT, config_json TEXT
)
"""
OBSERVATION_DDL = """
CREATE TABLE IF NOT EXISTS crypto_liquidity_sweep_v1_shadow_observations (
  observation_id TEXT PRIMARY KEY, strategy_id TEXT NOT NULL, profile_id TEXT NOT NULL,
  shadow_lane TEXT NOT NULL, evaluated_at TEXT NOT NULL, decision_at TEXT NOT NULL,
  sweep_at TEXT NOT NULL, symbol TEXT NOT NULL, direction TEXT NOT NULL,
  session_bucket TEXT, level_price REAL, liquidation_notional_usd REAL,
  liquidation_event_ids_json TEXT, rejection_reason TEXT NOT NULL,
  features_json TEXT, notes_json TEXT
)
"""
META_DDL = "CREATE TABLE IF NOT EXISTS crypto_liquidity_sweep_v1_shadow_meta (k TEXT PRIMARY KEY, v TEXT NOT NULL)"

REJECTION_REASONS = {
    "CANDLES_MISSING", "NO_COMPLETED_SWEEP", "LIQUIDATION_DATA_MISSING", "LIQUIDATION_SIDE_MISMATCH",
    "LIQUIDATION_NOT_OBSERVED", "LIQUIDATION_NOTIONAL_TOO_SMALL", "OI_DATA_MISSING", "OI_NOT_FLUSHING", "LIQUIDITY_DATA_MISSING",
    "SPREAD_TOO_WIDE", "RVOL_TOO_WEAK", "WEAK_SESSION_BLOCKED", "INVALID_STOP_GEOMETRY",
    "STOP_TOO_WIDE", "AMBIGUOUS_RANGE_SWEEP", "DATA_DIRTY",
}


def load_strategy_config() -> dict[str, Any]:
    return load_yaml_block(CONFIG_PATH, STRATEGY_KEY, DEFAULTS)


def ensure_tables(conn: sqlite3.Connection) -> None:
    conn.execute(OUTCOME_DDL)
    conn.execute(EVAL_DDL)
    conn.execute(OBSERVATION_DDL)
    conn.execute(META_DDL)
    text = {"strategy_id", "profile_id", "shadow_lane", "window", "generated_at", "decision_at",
            "sweep_at", "symbol", "direction", "session_bucket", "liquidation_event_ids_json",
            "eligibility_status", "rejection_reason", "data_status", "entry_ts", "outcome_status",
            "close_reason", "exit_ts", "features_json", "notes_json", "last_checked_at"}
    integer = {"is_clean_for_edge", "protection_armed", "lock_armed", "highest_tp_touched", "bars_held"}
    ensure_columns(conn, "crypto_liquidity_sweep_v1_shadow_outcomes", {
        col: "TEXT" if col in text else "INTEGER" if col in integer else "REAL"
        for col in OUTCOME_COLUMNS if col != "candidate_id"
    })
    conn.execute("CREATE INDEX IF NOT EXISTS idx_liqsweep_open ON "
                 "crypto_liquidity_sweep_v1_shadow_outcomes(outcome_status, entry_ts)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_liqsweep_symbol ON "
                 "crypto_liquidity_sweep_v1_shadow_outcomes(symbol, decision_at)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_liqsweep_observation_reason ON "
                 "crypto_liquidity_sweep_v1_shadow_observations(rejection_reason, decision_at)")


def _canon(symbol: str) -> str:
    base = str(symbol or "").upper().split(":", 1)[0].replace("_", "/")
    if "/" not in base and base.endswith("USDT"):
        base = f"{base[:-4]}/USDT"
    return base


def _session(now: datetime) -> str:
    h = now.astimezone(timezone.utc).hour
    return "asia" if h <= 6 else "europe" if h <= 12 else "us" if h <= 20 else "off"


def _candidate_id(cfg: dict[str, Any], symbol: str, at: datetime, direction: str) -> str:
    raw = f"{cfg['strategy_id']}|{_canon(symbol)}|{at.isoformat()}|{direction}"
    return "clsv1_" + hashlib.sha256(raw.encode()).hexdigest()[:22]


def _observation_id(cfg: dict[str, Any], symbol: str, at: datetime, direction: str) -> str:
    raw = f"observation|{cfg['strategy_id']}|{_canon(symbol)}|{at.isoformat()}|{direction}"
    return "clsobs_" + hashlib.sha256(raw.encode()).hexdigest()[:22]


def _f(value: Any) -> float | None:
    try:
        return None if value in (None, "") else float(value)
    except (TypeError, ValueError):
        return None


def _dt(value: Any) -> datetime | None:
    parsed = parse_dt(value)
    return parsed.astimezone(timezone.utc) if parsed else None


def _atr(frame: pd.DataFrame, idx: int, periods: int = 14) -> float | None:
    if idx < periods:
        return None
    prior = frame.iloc[max(0, idx - periods): idx + 1].copy()
    prev = prior["close"].shift(1)
    tr = pd.concat([(prior["high"] - prior["low"]), (prior["high"] - prev).abs(),
                    (prior["low"] - prev).abs()], axis=1).max(axis=1)
    value = _f(tr.mean())
    return value if value and value > 0 else None


def _bar_minutes(cfg: dict[str, Any]) -> int:
    value = str(cfg.get("timeframe") or "5m").strip().lower()
    if value.endswith("m"):
        try:
            return max(1, int(value[:-1]))
        except ValueError:
            pass
    return 5


def _latest_closed_index(frame: pd.DataFrame, now: datetime, cfg: dict[str, Any]) -> int | None:
    """Locate the last candle whose close was known at ``now``."""
    if frame.empty:
        return None
    closed_at = frame["timestamp"] + pd.Timedelta(minutes=_bar_minutes(cfg))
    indices = frame.index[closed_at <= pd.Timestamp(now)].tolist()
    return int(indices[-1]) if indices else None


def _level_touch_count(prior: pd.DataFrame, level: float, direction: str, cfg: dict[str, Any]) -> int:
    """Count prior tests of the swept boundary within a small price tolerance."""
    if level <= 0:
        return 0
    tolerance = level * float(cfg.get("level_touch_tolerance_bps", 12.0)) / 10_000.0
    prices = prior["low"] if direction == "long" else prior["high"]
    return int(((prices.astype(float) - level).abs() <= tolerance).sum())


def detect_sweep(frame: pd.DataFrame, idx: int, events: list[dict[str, Any]], cfg: dict[str, Any],
                 *, liquidation_feed_available: bool = True) -> dict[str, Any]:
    """Return a deterministic reversal setup or an enumerable rejection."""
    frame = normalize_frame(frame)
    lookback = int(cfg["level_lookback_bars"])
    if frame.empty or idx < lookback + 14:
        return {"ok": False, "reason": "CANDLES_MISSING"}
    row = frame.iloc[idx]
    sweep_at = _dt(row.get("timestamp"))
    if sweep_at is None:
        return {"ok": False, "reason": "CANDLES_MISSING"}
    # Candle timestamps are bar opens in every supported archive. The actual
    # decision is possible only when this bar has closed.
    decision_at = sweep_at + timedelta(minutes=_bar_minutes(cfg))
    prior = frame.iloc[idx - lookback:idx]
    high, low, close, open_ = (_f(row.get(k)) for k in ("high", "low", "close", "open"))
    if None in (high, low, close, open_):
        return {"ok": False, "reason": "CANDLES_MISSING"}
    span = high - low
    if span <= 0:
        return {"ok": False, "reason": "NO_COMPLETED_SWEEP"}
    lower, upper = float(prior["low"].min()), float(prior["high"].max())
    bps = float(cfg["min_sweep_bps"]) / 10_000.0
    long_sweep = low < lower * (1 - bps) and close >= lower
    short_sweep = high > upper * (1 + bps) and close <= upper
    if long_sweep and short_sweep:
        # A bar that raids both sides of the range is a volatility expansion,
        # not a directional liquidation reversal.
        return {"ok": False, "reason": "AMBIGUOUS_RANGE_SWEEP"}
    if not long_sweep and not short_sweep:
        return {"ok": False, "reason": "NO_COMPLETED_SWEEP"}
    direction = "long" if long_sweep else "short"
    level = lower if long_sweep else upper
    level_touches = _level_touch_count(prior, level, direction, cfg)
    wick = (min(open_, close) - low) / span if long_sweep else (high - max(open_, close)) / span
    close_location = (close - low) / span if long_sweep else (high - close) / span
    volume = _f(row.get("volume")) or 0.0
    base_volume = _f(prior["volume"].tail(20).median()) or 0.0
    facts = {"sweep_at": sweep_at, "decision_at": decision_at, "direction": direction,
             "level": level, "wick_share": wick, "close_location": close_location,
             "rvol": volume / base_volume if base_volume else None,
             "level_touch_count": level_touches,
             "would_pass_two_touch_level": level_touches >= 2}
    if wick < float(cfg["min_wick_share"]) or close_location < float(cfg["min_close_location"]):
        return {**facts, "ok": False, "reason": "NO_COMPLETED_SWEEP"}
    if not base_volume or volume / base_volume < float(cfg["min_rvol"]):
        return {**facts, "ok": False, "reason": "RVOL_TOO_WEAK"}
    wanted_side = "SELL" if long_sweep else "BUY"
    window_start = decision_at - timedelta(minutes=float(cfg["liquidation_window_minutes"]))
    matched = [e for e in events if str(e.get("side") or "").upper() == wanted_side
               and (event_at := _dt(e.get("event_at"))) is not None and window_start <= event_at <= decision_at]
    if not events:
        return {**facts, "ok": False, "reason": "LIQUIDATION_NOT_OBSERVED" if liquidation_feed_available
                else "LIQUIDATION_DATA_MISSING"}
    if not matched:
        return {**facts, "ok": False, "reason": "LIQUIDATION_SIDE_MISMATCH"}
    notional = sum(float(e.get("notional_usd") or 0.0) for e in matched)
    if notional < float(cfg["min_liquidation_notional_usd"]):
        return {**facts, "ok": False, "reason": "LIQUIDATION_NOTIONAL_TOO_SMALL",
                "liquidation_notional_usd": notional,
                "event_ids": [str(e.get("event_id")) for e in matched]}
    atr = _atr(frame, idx)
    if atr is None:
        return {**facts, "ok": False, "reason": "CANDLES_MISSING"}
    stop = low - atr * float(cfg["stop_buffer_atr"]) if long_sweep else high + atr * float(cfg["stop_buffer_atr"])
    risk = abs(close - stop)
    if risk <= 0 or (long_sweep and stop >= close) or (short_sweep and stop <= close):
        return {**facts, "ok": False, "reason": "INVALID_STOP_GEOMETRY"}
    if risk / close > float(cfg["max_stop_distance_pct"]):
        return {**facts, "ok": False, "reason": "STOP_TOO_WIDE"}
    targets = [close + risk * float(r) if long_sweep else close - risk * float(r)
               for r in cfg["target_r"]]
    return {**facts, "ok": True, "entry": close,
            "stop": stop, "tp1": targets[0], "tp2": targets[1], "tp3": targets[2],
            "liquidation_notional_usd": notional, "event_ids": [str(e.get("event_id")) for e in matched],
            "liquidation_exchanges": sorted({str(e.get("exchange") or "unknown") for e in matched})}


def _event_rows(conn: sqlite3.Connection, symbol: str, at: datetime, cfg: dict[str, Any]) -> list[dict[str, Any]]:
    from src.data_collectors.market_intelligence_store import normalize_symbol
    start = (at - timedelta(minutes=float(cfg["liquidation_window_minutes"]))).isoformat()
    exchanges = [str(value).lower() for value in (cfg.get("liquidation_sources") or [])]
    if not exchanges:
        return []
    placeholders = ",".join("?" for _ in exchanges)
    rows = conn.execute("SELECT exchange,event_id,event_at,side,notional_usd FROM liquidation_events "
                        f"WHERE normalized_symbol=? AND exchange IN ({placeholders}) "
                        "AND event_at>=? AND event_at<=?",
                        (normalize_symbol(symbol), *exchanges, start, at.isoformat())).fetchall()
    return [dict(r) for r in rows]


def _contexts(conn: sqlite3.Connection, symbol: str, at: datetime, cfg: dict[str, Any]) -> dict[str, Any]:
    from src.data_collectors import market_intelligence_store as mi
    derivative = mi.latest_derivatives_context(conn, symbol, as_of=at,
                                                max_age_minutes=float(cfg["derivatives_freshness_minutes"]))
    liquidity = mi.latest_liquidity_context(conn, symbol, as_of=at,
                                              max_age_minutes=float(cfg["liquidity_freshness_minutes"]))
    if derivative.get("venue_count", 0) < 1:
        return {"ok": False, "reason": "OI_DATA_MISSING"}
    if liquidity.get("venue_count", 0) < 1:
        return {"ok": False, "reason": "LIQUIDITY_DATA_MISSING"}
    spread = _f(liquidity.get("spread_bps"))
    if spread is None or spread > float(cfg["max_spread_bps"]):
        return {"ok": False, "reason": "SPREAD_TOO_WIDE", "spread_bps": spread}
    # Compare the same exchange set at both timestamps.  Comparing an
    # all-venue latest aggregate to one arbitrary historical row can invent an
    # OI flush that never happened.
    normalized = mi.normalize_symbol(symbol)
    fresh_after = (at - timedelta(minutes=float(cfg["derivatives_freshness_minutes"]))).isoformat()
    latest_rows = conn.execute(
        "SELECT * FROM (SELECT d.exchange,d.oi_usd,d.provider_ts,"
        "ROW_NUMBER() OVER(PARTITION BY d.exchange ORDER BY d.provider_ts DESC,d.id DESC) rn "
        "FROM derivative_snapshots d WHERE d.normalized_symbol=? AND d.provider_ts>=? AND d.provider_ts<=? "
        "AND d.oi_usd IS NOT NULL) WHERE rn=1",
        (normalized, fresh_after, at.isoformat()),
    ).fetchall()
    current_oi = 0.0
    prior_oi = 0.0
    pairs = 0
    old_cutoff = at - timedelta(minutes=10)
    for latest in latest_rows:
        latest_value = _f(latest["oi_usd"])
        if latest_value is None or latest_value <= 0:
            continue
        old = conn.execute(
            "SELECT oi_usd,provider_ts FROM derivative_snapshots WHERE normalized_symbol=? AND exchange=? "
            "AND provider_ts<=? AND oi_usd IS NOT NULL ORDER BY provider_ts DESC,id DESC LIMIT 1",
            (normalized, latest["exchange"], old_cutoff.isoformat()),
        ).fetchone()
        old_value = _f(old["oi_usd"]) if old else None
        old_at = _dt(old["provider_ts"]) if old else None
        if old_value is None or old_value <= 0 or old_at is None or old_cutoff - old_at > timedelta(minutes=10):
            continue
        current_oi += latest_value
        prior_oi += old_value
        pairs += 1
    if not pairs or prior_oi <= 0:
        return {"ok": False, "reason": "OI_DATA_MISSING", "spread_bps": spread}
    oi_change = (current_oi - prior_oi) / prior_oi * 100.0
    if oi_change > -float(cfg["min_oi_drop_pct"]):
        return {"ok": False, "reason": "OI_NOT_FLUSHING", "oi_change_pct": oi_change, "spread_bps": spread}
    return {"ok": True, "oi_change_pct": oi_change, "spread_bps": spread, "oi_venue_pairs": pairs}


def _upsert(conn: sqlite3.Connection, row: dict[str, Any]) -> None:
    values = [_json_cell(row.get(c)) if c.endswith("_json") else row.get(c) for c in OUTCOME_COLUMNS]
    cols = ",".join(OUTCOME_COLUMNS)
    updates = ",".join(f"{c}=excluded.{c}" for c in OUTCOME_COLUMNS if c != "candidate_id")
    conn.execute(f"INSERT INTO crypto_liquidity_sweep_v1_shadow_outcomes({cols}) VALUES({','.join('?' for _ in OUTCOME_COLUMNS)}) "
                 f"ON CONFLICT(candidate_id) DO UPDATE SET {updates}", values)


def _json_cell(value: Any) -> Any:
    """Serialize new structures once while preserving SQLite JSON text."""
    return value if isinstance(value, str) else json_text(value)


def _record_observation(conn: sqlite3.Connection, cfg: dict[str, Any], symbol: str, now: datetime,
                        session: str, setup: dict[str, Any], reason: str,
                        source_status: dict[str, Any]) -> None:
    """Persist a non-trading funnel row for a structurally swept candle only."""
    decision_at = setup.get("decision_at")
    sweep_at = setup.get("sweep_at")
    direction = str(setup.get("direction") or "")
    if not isinstance(decision_at, datetime) or not isinstance(sweep_at, datetime) or direction not in {"long", "short"}:
        return
    row = {
        "observation_id": _observation_id(cfg, symbol, decision_at, direction),
        "strategy_id": cfg["strategy_id"], "profile_id": cfg["profile_id"],
        "shadow_lane": cfg["shadow_lane"], "evaluated_at": now.isoformat(),
        "decision_at": decision_at.isoformat(), "sweep_at": sweep_at.isoformat(),
        "symbol": _canon(symbol), "direction": direction, "session_bucket": session,
        "level_price": setup.get("level"), "liquidation_notional_usd": setup.get("liquidation_notional_usd"),
        "liquidation_event_ids_json": setup.get("event_ids") or [], "rejection_reason": reason,
        "features_json": {key: setup.get(key) for key in (
            "wick_share", "close_location", "rvol", "level_touch_count", "would_pass_two_touch_level",
        )},
        "notes_json": {"liquidation_source_status": source_status.get("status"),
                       "feed_available": source_status.get("feed_available")},
    }
    values = [_json_cell(row.get(c)) if c.endswith("_json") else row.get(c) for c in OBSERVATION_COLUMNS]
    cols = ",".join(OBSERVATION_COLUMNS)
    updates = ",".join(f"{c}=excluded.{c}" for c in OBSERVATION_COLUMNS if c != "observation_id")
    conn.execute(f"INSERT INTO crypto_liquidity_sweep_v1_shadow_observations({cols}) "
                 f"VALUES({','.join('?' for _ in OBSERVATION_COLUMNS)}) "
                 f"ON CONFLICT(observation_id) DO UPDATE SET {updates}", values)


def _activation(conn: sqlite3.Connection, now: datetime, persist: bool) -> datetime:
    row = conn.execute("SELECT v FROM crypto_liquidity_sweep_v1_shadow_meta WHERE k='activated_at'").fetchone()
    if row and _dt(row[0]):
        return _dt(row[0])  # type: ignore[return-value]
    if persist:
        conn.execute("INSERT OR REPLACE INTO crypto_liquidity_sweep_v1_shadow_meta(k,v) VALUES('activated_at',?)", (now.isoformat(),))
    return now


def _load_frame(symbol: str, cfg: dict[str, Any]) -> pd.DataFrame:
    # Reuse the monitor-maintained, read-only Bybit 5m cache. Results remain fully isolated.
    from src.execution.crypto_derivreset_v3_shadow import _load_frame as load_shared_frame
    frame, _ = load_shared_frame(symbol, {"timeframe": cfg["timeframe"], "fallback_timeframes": ["15m"],
                                           "primary_exchange": cfg["primary_exchange"]})
    return normalize_frame(frame)


def _symbols(conn: sqlite3.Connection, now: datetime, cfg: dict[str, Any]) -> list[str]:
    from src.execution.crypto_derivreset_v3_shadow import _symbols as shared_symbols
    return shared_symbols(conn, now, {"primary_exchange": cfg["primary_exchange"],
                                      "derivative_freshness_minutes": cfg["derivatives_freshness_minutes"],
                                      "max_symbols": cfg["max_symbols"]})


def _funding_events(conn: sqlite3.Connection | None, symbol: str, entry_at: datetime,
                    now: datetime) -> list[dict[str, Any]]:
    if conn is None:
        return []
    try:
        from src.data_collectors.market_intelligence_store import normalize_symbol
        rows = conn.execute(
            "SELECT event_at,received_at,funding_rate,funding_rate_8h FROM funding_rate_events "
            "WHERE normalized_symbol=? AND event_at>? AND event_at<=? ORDER BY event_at",
            (normalize_symbol(symbol), entry_at.isoformat(), now.isoformat()),
        ).fetchall()
    except sqlite3.Error:
        return []
    return [dict(row) for row in rows]


def _liquidation_source_status(conn: sqlite3.Connection, cfg: dict[str, Any],
                               now: datetime | None = None) -> dict[str, Any]:
    now = now or utc_now()
    venues = [str(value).lower() for value in (cfg.get("liquidation_sources") or [])]
    if not venues:
        return {"status": "DISABLED", "event_count": 0, "latest_event_at": None,
                "feed_available": False, "transport_status": "disabled", "sources": {}}
    health_sources = [f"liquidations:{venue}_ws" for venue in venues]
    health_placeholders = ",".join("?" for _ in health_sources)
    try:
        health_rows = conn.execute(
            "SELECT source,status,last_success_at,error FROM intelligence_source_health "
            f"WHERE source IN ({health_placeholders})", health_sources
        ).fetchall()
    except sqlite3.Error:
        health_rows = []
    health = {str(row["source"]): dict(row) for row in health_rows}
    recent_cutoff = now - timedelta(minutes=15)
    active_sources = [row for row in health.values()
                      if row.get("status") in {"ok", "degraded"}
                      and (_dt(row.get("last_success_at")) or now) >= recent_cutoff]

    # The append-only tape is large (millions of rows). COUNT/MAX filtered
    # only by exchange forced a full scan on every monitor pass and could hold
    # this Paper sidecar for minutes. We need presence and freshness here, not
    # an exact lifetime count, so inspect only the newest row per venue.
    def newest_events(selected: list[str]) -> tuple[int, str | None]:
        latest_values: list[str] = []
        for venue in selected:
            try:
                row = conn.execute(
                    "SELECT event_at FROM liquidation_events "
                    "WHERE exchange=? ORDER BY rowid DESC LIMIT 1",
                    (venue,),
                ).fetchone()
            except sqlite3.Error:
                row = None
            if row and row[0]:
                latest_values.append(str(row[0]))
        return len(latest_values), max(latest_values, default=None)

    count, latest = newest_events(venues)
    observation_venues = list(dict.fromkeys(
        [*venues, *(str(value).lower() for value in (cfg.get("liquidation_observation_sources") or []))]
    ))
    observation_count, observation_latest = newest_events(observation_venues)
    return {
        "status": "EVENTS_AVAILABLE" if count else "NO_EVENTS_YET",
        "event_count": count,
        "latest_event_at": latest,
        "feed_available": bool(active_sources),
        "transport_status": "ok" if active_sources else "unknown",
        "sources": health,
        "event_count_kind": "venues_with_events",
        # The wider tape is evidence for later comparison only. It never
        # affects the two-venue admission decision above.
        "observation": {"venues": observation_venues, "event_count": observation_count,
                        "latest_event_at": observation_latest,
                        "event_count_kind": "venues_with_events"},
    }


def _mature_open(conn: sqlite3.Connection, now: datetime, cfg: dict[str, Any],
                 intelligence: sqlite3.Connection | None = None) -> int:
    rows = conn.execute("SELECT * FROM crypto_liquidity_sweep_v1_shadow_outcomes WHERE outcome_status='open'").fetchall()
    closed = 0
    for raw in rows:
        row = dict(raw); entry_at = _dt(row.get("entry_ts"));
        if entry_at is None:
            continue
        frame = _load_frame(str(row["symbol"]), cfg)
        future = frame[frame["timestamp"] > pd.Timestamp(entry_at)]
        if future.empty:
            continue
        force = len(future) >= int(cfg["max_holding_bars"])
        sim = simulate_confirmed_close_entry(direction=row["direction"], entry=float(row["entry_price"]),
            stop=float(row["stop_price"]), tp1=float(row["tp1"]), tp2=float(row["tp2"]), tp3=float(row["tp3"]),
            future_candles=future.iloc[:int(cfg["max_holding_bars"])], symbol=row["symbol"],
            fee_profile=cfg["fee_profile"], entry_at=entry_at, bar_minutes=_bar_minutes(cfg),
            funding_events=_funding_events(intelligence, str(row["symbol"]), entry_at, now),
            force_close=force).to_dict()
        # The simulator calls this field ``status``.  Outcomes deliberately
        # call it ``outcome_status``; map it explicitly rather than silently
        # leaving every position open forever.
        mapped = {"outcome_status": sim.get("status")}
        mapped.update({key: value for key, value in sim.items() if key in OUTCOME_COLUMNS})
        row.update(mapped)
        row["last_checked_at"] = now.isoformat()
        _upsert(conn, row)
        closed += int(row.get("outcome_status") == "closed")
    return closed


def tick(*, db: str | None = None, persist: bool = True, now: datetime | None = None,
         cfg: dict[str, Any] | None = None) -> dict[str, Any]:
    cfg = cfg or load_strategy_config(); now = now or utc_now()
    if not cfg.get("feature_flag"):
        return {"enabled": False, "rows": [], "closed_matured": 0, "summary": {"verdict": "DISABLED"}}
    from src.data_collectors import market_intelligence_store as mi
    from src.config import load_config
    path = Path(db) if db else load_config().db_path
    conn = sqlite3.connect(":memory:" if not persist and not path.exists() else path, timeout=10.0)
    conn.row_factory = sqlite3.Row
    if not persist and path.exists():
        conn.execute("BEGIN")
    intelligence = mi.connect(ensure=False)
    try:
        ensure_tables(conn); activated = _activation(conn, now, persist)
        closed = _mature_open(conn, now, cfg, intelligence)
        inserted: list[dict[str, Any]] = []
        source_status = _liquidation_source_status(intelligence, cfg, now)
        observed_rejections = 0
        for symbol in _symbols(intelligence, now, cfg):
            frame = _load_frame(symbol, cfg)
            if frame.empty or len(frame) < int(cfg["level_lookback_bars"]) + 16:
                continue
            idx = _latest_closed_index(frame, now, cfg)
            if idx is None or idx < int(cfg["level_lookback_bars"]) + 14:
                continue
            bar_at = _dt(frame.iloc[idx].get("timestamp"))
            if bar_at is None:
                continue
            decision_at = bar_at + timedelta(minutes=_bar_minutes(cfg))
            events = _event_rows(intelligence, symbol, decision_at, cfg)
            setup = detect_sweep(frame, idx, events, cfg,
                                 liquidation_feed_available=bool(source_status.get("feed_available")))
            if not setup.get("ok"):
                if persist and setup.get("decision_at"):
                    _record_observation(conn, cfg, symbol, now, _session(decision_at), setup,
                                        str(setup.get("reason") or "NO_COMPLETED_SWEEP"), source_status)
                    observed_rejections += 1
                continue
            decision_at = setup["decision_at"]
            context = _contexts(intelligence, symbol, decision_at, cfg)
            session = _session(decision_at)
            reason = None if context.get("ok") else context.get("reason")
            if session in set(cfg.get("block_sessions") or []):
                reason = "WEAK_SESSION_BLOCKED"
            direction = str(setup["direction"])
            cid = _candidate_id(cfg, symbol, decision_at, direction)
            exists = conn.execute("SELECT 1 FROM crypto_liquidity_sweep_v1_shadow_outcomes WHERE candidate_id=?", (cid,)).fetchone()
            if exists:
                continue
            clean = int(reason is None)
            row = {"candidate_id": cid, "strategy_id": cfg["strategy_id"], "profile_id": cfg["profile_id"],
                   "shadow_lane": cfg["shadow_lane"], "window": "forward_post_activation",
                   "generated_at": now.isoformat(), "decision_at": decision_at.isoformat(), "sweep_at": setup["sweep_at"].isoformat(),
                   "symbol": _canon(symbol), "direction": direction, "session_bucket": session,
                   "level_price": setup["level"], "liquidation_notional_usd": setup["liquidation_notional_usd"],
                   "liquidation_event_ids_json": setup["event_ids"], "oi_change_pct": context.get("oi_change_pct"),
                   "spread_bps": context.get("spread_bps"), "eligibility_status": "eligible" if clean else "rejected",
                   "rejection_reason": reason, "data_status": "ok" if clean else "dirty", "is_clean_for_edge": clean,
                   "entry_ts": decision_at.isoformat() if clean else None, "entry_price": setup["entry"] if clean else None,
                   "stop_price": setup["stop"] if clean else None, "tp1": setup["tp1"] if clean else None,
                   "tp2": setup["tp2"] if clean else None, "tp3": setup["tp3"] if clean else None,
                   "outcome_status": "open" if clean else "skipped", "close_reason": None,
                   "latency_seconds": max(0.0, (now - decision_at).total_seconds()),
                   "features_json": {"rvol": setup["rvol"], "wick_share": setup["wick_share"],
                                     "close_location": setup["close_location"],
                                     "level_touch_count": setup.get("level_touch_count"),
                                     "would_pass_two_touch_level": setup.get("would_pass_two_touch_level"),
                                     "oi_venue_pairs": context.get("oi_venue_pairs"),
                                     "liquidation_sources": setup.get("liquidation_exchanges") or []},
                   "notes_json": {"paper_untouched": True, "live_locked": True}, "last_checked_at": now.isoformat()}
            if persist:
                _upsert(conn, row)
            inserted.append(row)
        rows = [dict(r) for r in conn.execute("SELECT * FROM crypto_liquidity_sweep_v1_shadow_outcomes")]
        summary = clean_forward_summary(rows, activated_at=activated.isoformat(), now=now,
            min_closed=int(cfg["min_clean_closed"]), min_days=float(cfg["min_forward_days"]),
            min_pf=float(cfg["min_profit_factor"]), max_review_drawdown_usd=float(cfg["max_review_drawdown_usd"]))
        diagnostics = strategy_diagnostics(rows, group_keys=("direction", "session_bucket", "rejection_reason"))
        if persist:
            columns = ("generated_at", "strategy_id", "profile_id", "activated_at", "forward_rows", "clean_rows",
                       "dirty_rows", "clean_closed", "net_pnl_usd", "net_r", "fees_usd", "slippage_usd",
                       "funding_usd", "profit_factor", "winrate", "max_drawdown_usd", "forward_days", "verdict",
                       "diagnostics_json", "config_json")
            conn.execute("INSERT OR REPLACE INTO crypto_liquidity_sweep_v1_shadow_evaluations (" + ",".join(columns) +
                         ") VALUES(" + ",".join("?" for _ in columns) + ")",
                         (now.isoformat(), cfg["strategy_id"], cfg["profile_id"], activated.isoformat(),
                          summary["forward_rows"], summary["clean_rows"], summary["dirty_rows"], summary["clean_closed"],
                          summary["net_pnl_usd"], summary["net_r"], summary["fees_usd"], summary["slippage_usd"],
                          summary["funding_usd"], summary["profit_factor"], summary["winrate"],
                          summary["max_drawdown_usd"], summary["forward_days"], summary["verdict"],
                          json_text(diagnostics), json_text(cfg)))
            conn.commit()
        else:
            conn.rollback()
        return {"enabled": True, "rows": inserted, "closed_matured": closed, "summary": summary,
                "diagnostics": diagnostics, "liquidation_events_available": bool(source_status["event_count"]),
                "liquidation_source": source_status, "observed_rejections": observed_rejections}
    finally:
        intelligence.close(); conn.close()


def render_markdown(result: dict[str, Any]) -> str:
    s = result.get("summary") or {}
    lines = ["# Crypto Liquidity Sweep v1 — Shadow", "", "Observed Binance/Bybit forced-liquidation events + range-sweep reversal; OKX is diagnostic coverage only.",
             "The detector itself creates no Paper signal or order. A separate live bridge may mirror only fresh clean outcomes to the common preflight outbox.", "",
             f"- enabled: `{result.get('enabled')}`", f"- liquidation source: `{(result.get('liquidation_source') or {}).get('status', 'unknown')}` "
             f"(transport `{(result.get('liquidation_source') or {}).get('transport_status', 'unknown')}`; "
             f"events `{(result.get('liquidation_source') or {}).get('event_count', 0)}`)",
             f"- diagnostic liquidation coverage: `{','.join(((result.get('liquidation_source') or {}).get('observation') or {}).get('venues') or [])}` "
             f"({((result.get('liquidation_source') or {}).get('observation') or {}).get('event_count', 0)} events; not an entry gate)",
             f"- new rows: `{len(result.get('rows') or [])}` · matured: `{result.get('closed_matured', 0)}` · observed rejected sweeps: `{result.get('observed_rejections', 0)}`",
             f"- verdict: **{s.get('verdict', 'DISABLED')}** · clean closed: `{s.get('clean_closed', 0)}` · net USD: `{s.get('net_pnl_usd', 0):.2f}` · PF: `{s.get('profit_factor')}`", ""]
    lines.extend(diagnostics_markdown(result.get("diagnostics") or {}))
    return "\n".join(lines)


def write_report(result: dict[str, Any], path: str | None = None) -> str:
    target = ROOT / (path or load_strategy_config()["report_path"])
    target.parent.mkdir(parents=True, exist_ok=True); target.write_text(render_markdown(result) + "\n", encoding="utf-8")
    return str(target)


__all__ = ["detect_sweep", "ensure_tables", "load_strategy_config", "render_markdown", "tick", "write_report"]
