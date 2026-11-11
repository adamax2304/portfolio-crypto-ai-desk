"""Higher-timeframe liquidity sweep and reclaim, isolated to Shadow.

The lane finds *confirmed* 4h pivot zones, observes a one-hour sweep through a
zone alongside an actual Binance/Bybit forced-order/OI deleveraging event, then
waits for a 15m reclaim.  It deliberately creates two independent profiles:
the first confirmed reclaim and a two-close hold.  Neither profile creates a
desk signal, touches Paper state, or calls a Live executor.
"""
from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from src.config import load_config
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
from src.storage.file_store import FileStore


ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "config" / "shadow_crypto_htf_liquidity_reclaim.yaml"
SHADOW_OHLCV_ROOT = ROOT / "data" / "shadow" / "htf_liquidity_reclaim_v1" / "ohlcv"
STRATEGY_KEY = "crypto_htf_liquidity_reclaim_v1"

DEFAULTS: dict[str, Any] = {
    "feature_flag": False,
    "strategy_id": STRATEGY_KEY,
    "shadow_lane": "shadow_crypto_htf_liquidity_reclaim",
    "primary_exchange": "bybit",
    "max_symbols": 40,
    "structure_timeframe": "4h",
    "sweep_timeframe": "1h",
    "confirmation_timeframe": "15m",
    "structure_lookback_bars": 90,
    "pivot_left_bars": 3,
    "pivot_right_bars": 3,
    "zone_width_atr": 0.25,
    "min_sweep_atr": 0.15,
    "min_wick_share": 0.35,
    "min_close_location": 0.55,
    "min_rvol": 1.10,
    "liquidation_window_minutes": 60,
    "min_liquidation_notional_usd": 50_000.0,
    "liquidation_sources": ["binance", "bybit"],
    "liquidation_observation_sources": ["binance", "bybit", "okx"],
    "min_oi_drop_pct": 0.50,
    "max_adverse_funding_8h": 0.0010,
    "max_spread_bps": 25.0,
    "derivatives_freshness_minutes": 10,
    "liquidity_freshness_minutes": 10,
    "confirmation_window_bars": 4,
    "confirmation_progress_atr": 0.05,
    "max_oi_rebuild_pct": 1.50,
    "min_price_progress_atr": 0.05,
    "profiles": {
        "EARLY_RECLAIM": "crypto_htf_liquidity_reclaim_early_v1",
        "HELD_RECLAIM": "crypto_htf_liquidity_reclaim_held_v1",
    },
    "require_btc_alignment": True,
    "btc_ema_bars": 20,
    "block_sessions": [],
    "stop_buffer_atr": 0.25,
    "max_stop_distance_pct": 0.08,
    "min_opposing_level_r": 2.50,
    "tp1_r": 1.0,
    "tp2_r": 1.75,
    "opposing_target_fraction": 0.95,
    "max_holding_bars": 192,
    "fee_profile": "bybit_non_vip_usdt_perp",
    "min_clean_closed": 30,
    "min_forward_days": 28,
    "min_profit_factor": 1.25,
    "max_review_drawdown_usd": 250.0,
    "report_path": "reports/CRYPTO_HTF_LIQUIDITY_RECLAIM_V1_SHADOW.md",
}

OUTCOME_COLUMNS = (
    "candidate_id", "event_id", "strategy_id", "profile_id", "shadow_lane", "window", "generated_at",
    "decision_at", "sweep_at", "symbol", "direction", "entry_profile", "session_bucket",
    "structure_level", "structure_zone_width", "structure_pivot_at", "opposing_level_price",
    "sweep_close", "liquidation_notional_usd", "liquidation_event_ids_json", "oi_change_pct",
    "funding_rate_8h", "spread_bps", "eligibility_status", "rejection_reason", "data_status",
    "is_clean_for_edge", "entry_ts", "entry_price", "stop_price", "tp1", "tp2", "tp3",
    "outcome_status", "close_reason", "exit_price", "exit_ts", "gross_pnl_usd", "net_pnl_usd",
    "net_r", "fees_usd", "slippage_usd", "funding_usd", "funding_source", "funding_estimated",
    "funding_event_count", "risk_usd", "mfe_r", "mae_r", "protection_armed", "lock_armed",
    "highest_tp_touched", "bars_held", "latency_seconds", "features_json", "notes_json", "last_checked_at",
)
OBSERVATION_COLUMNS = (
    "observation_id", "strategy_id", "shadow_lane", "evaluated_at", "decision_at", "sweep_at",
    "symbol", "direction", "structure_level", "rejection_reason", "features_json", "notes_json",
)

OUTCOME_DDL = """
CREATE TABLE IF NOT EXISTS crypto_htf_liquidity_reclaim_v1_shadow_outcomes (
  candidate_id TEXT PRIMARY KEY, event_id TEXT NOT NULL, strategy_id TEXT NOT NULL, profile_id TEXT NOT NULL,
  shadow_lane TEXT NOT NULL, window TEXT NOT NULL, generated_at TEXT NOT NULL, decision_at TEXT NOT NULL,
  sweep_at TEXT NOT NULL, symbol TEXT NOT NULL, direction TEXT NOT NULL, entry_profile TEXT NOT NULL,
  session_bucket TEXT, structure_level REAL, structure_zone_width REAL, structure_pivot_at TEXT,
  opposing_level_price REAL, sweep_close REAL, liquidation_notional_usd REAL,
  liquidation_event_ids_json TEXT, oi_change_pct REAL, funding_rate_8h REAL, spread_bps REAL,
  eligibility_status TEXT NOT NULL, rejection_reason TEXT, data_status TEXT,
  is_clean_for_edge INTEGER NOT NULL DEFAULT 0, entry_ts TEXT, entry_price REAL, stop_price REAL,
  tp1 REAL, tp2 REAL, tp3 REAL, outcome_status TEXT, close_reason TEXT, exit_price REAL, exit_ts TEXT,
  gross_pnl_usd REAL, net_pnl_usd REAL, net_r REAL, fees_usd REAL, slippage_usd REAL, funding_usd REAL,
  funding_source TEXT, funding_estimated INTEGER, funding_event_count INTEGER, risk_usd REAL, mfe_r REAL,
  mae_r REAL, protection_armed INTEGER, lock_armed INTEGER, highest_tp_touched INTEGER, bars_held INTEGER,
  latency_seconds REAL, features_json TEXT, notes_json TEXT, last_checked_at TEXT
)
"""
EVAL_DDL = """
CREATE TABLE IF NOT EXISTS crypto_htf_liquidity_reclaim_v1_shadow_evaluations (
  generated_at TEXT NOT NULL, profile_id TEXT NOT NULL, strategy_id TEXT NOT NULL, activated_at TEXT,
  forward_rows INTEGER, clean_rows INTEGER, dirty_rows INTEGER, clean_closed INTEGER,
  net_pnl_usd REAL, net_r REAL, fees_usd REAL, slippage_usd REAL, funding_usd REAL,
  profit_factor REAL, winrate REAL, max_drawdown_usd REAL, forward_days REAL, verdict TEXT,
  diagnostics_json TEXT, config_json TEXT, PRIMARY KEY(generated_at, profile_id)
)
"""
OBSERVATION_DDL = """
CREATE TABLE IF NOT EXISTS crypto_htf_liquidity_reclaim_v1_shadow_observations (
  observation_id TEXT PRIMARY KEY, strategy_id TEXT NOT NULL, shadow_lane TEXT NOT NULL,
  evaluated_at TEXT NOT NULL, decision_at TEXT NOT NULL, sweep_at TEXT NOT NULL, symbol TEXT NOT NULL,
  direction TEXT NOT NULL, structure_level REAL, rejection_reason TEXT NOT NULL,
  features_json TEXT, notes_json TEXT
)
"""
META_DDL = "CREATE TABLE IF NOT EXISTS crypto_htf_liquidity_reclaim_v1_shadow_meta (k TEXT PRIMARY KEY, v TEXT NOT NULL)"

REJECTION_REASONS = {
    "CANDLES_MISSING", "NO_CONFIRMED_HTF_LEVEL", "NO_STRUCTURAL_SWEEP", "SWEEP_WICK_TOO_SMALL",
    "SWEEP_RVOL_TOO_WEAK", "LIQUIDATION_DATA_MISSING", "LIQUIDATION_NOT_OBSERVED",
    "LIQUIDATION_SIDE_MISMATCH", "LIQUIDATION_NOTIONAL_TOO_SMALL", "OI_DATA_MISSING",
    "OI_NOT_FLUSHING", "FUNDING_AGAINST_DIRECTION", "LIQUIDITY_DATA_MISSING", "SPREAD_TOO_WIDE",
    "BTC_ALIGNMENT_MISSING", "BTC_ALIGNMENT_CONFLICT", "WEAK_SESSION_BLOCKED", "STOP_TOO_WIDE",
    "INVALID_STOP_GEOMETRY", "OPPOSING_LEVEL_TOO_CLOSE", "RECLAIM_WINDOW_EXPIRED", "RECLAIM_FAILED",
    "RECLAIM_OI_STALLED", "DATA_DIRTY",
}


def load_strategy_config() -> dict[str, Any]:
    return load_yaml_block(CONFIG_PATH, STRATEGY_KEY, DEFAULTS)


def ensure_tables(conn: sqlite3.Connection) -> None:
    conn.execute(OUTCOME_DDL)
    conn.execute(EVAL_DDL)
    conn.execute(OBSERVATION_DDL)
    conn.execute(META_DDL)
    text = {
        "event_id", "strategy_id", "profile_id", "shadow_lane", "window", "generated_at", "decision_at",
        "sweep_at", "symbol", "direction", "entry_profile", "session_bucket", "structure_pivot_at",
        "liquidation_event_ids_json", "eligibility_status", "rejection_reason", "data_status", "entry_ts",
        "outcome_status", "close_reason", "exit_ts", "funding_source", "features_json", "notes_json",
        "last_checked_at",
    }
    integer = {"is_clean_for_edge", "funding_estimated", "funding_event_count", "protection_armed",
               "lock_armed", "highest_tp_touched", "bars_held"}
    ensure_columns(conn, "crypto_htf_liquidity_reclaim_v1_shadow_outcomes", {
        col: "TEXT" if col in text else "INTEGER" if col in integer else "REAL"
        for col in OUTCOME_COLUMNS if col != "candidate_id"
    })
    conn.execute("CREATE INDEX IF NOT EXISTS idx_htf_reclaim_state ON "
                 "crypto_htf_liquidity_reclaim_v1_shadow_outcomes(outcome_status,decision_at)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_htf_reclaim_symbol ON "
                 "crypto_htf_liquidity_reclaim_v1_shadow_outcomes(symbol,entry_profile,decision_at)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_htf_reclaim_observation_reason ON "
                 "crypto_htf_liquidity_reclaim_v1_shadow_observations(rejection_reason,decision_at)")


def _f(value: Any) -> float | None:
    try:
        return None if value in (None, "") else float(value)
    except (TypeError, ValueError):
        return None


def _dt(value: Any) -> datetime | None:
    parsed = parse_dt(value)
    return parsed.astimezone(timezone.utc) if parsed else None


def _canonical(symbol: str) -> str:
    value = str(symbol or "").upper().split(":", 1)[0].replace("_", "/")
    if "/" not in value and value.endswith("USDT"):
        value = f"{value[:-4]}/USDT"
    return value


def _minutes(timeframe: str) -> int:
    value = str(timeframe or "").strip().lower()
    try:
        if value.endswith("m"):
            return max(1, int(value[:-1]))
        if value.endswith("h"):
            return max(1, int(value[:-1])) * 60
    except ValueError:
        pass
    return 1


def _delta(timeframe: str) -> timedelta:
    return timedelta(minutes=_minutes(timeframe))


def _session(at: datetime) -> str:
    hour = at.astimezone(timezone.utc).hour
    return "asia" if hour <= 6 else "europe" if hour <= 12 else "us" if hour <= 20 else "off"


def _atr(frame: pd.DataFrame, idx: int, periods: int = 14) -> float | None:
    if idx < periods:
        return None
    part = frame.iloc[max(0, idx - periods):idx + 1]
    prev = part["close"].shift(1)
    tr = pd.concat(((part["high"] - part["low"]), (part["high"] - prev).abs(),
                    (part["low"] - prev).abs()), axis=1).max(axis=1)
    value = _f(tr.mean())
    return value if value and value > 0 else None


def _latest_closed_index(frame: pd.DataFrame, now: datetime, timeframe: str) -> int | None:
    frame = normalize_frame(frame)
    if frame.empty:
        return None
    closed = frame.index[frame["timestamp"] + pd.Timedelta(_delta(timeframe)) <= pd.Timestamp(now)].tolist()
    return int(closed[-1]) if closed else None


class HtfOhlcvStore:
    """Private cache; it may read the desk cache but never writes into it."""

    def __init__(self, fallback: FileStore):
        self.fallback = fallback

    @staticmethod
    def _path(exchange: str, symbol: str, timeframe: str) -> Path:
        from src.utils.symbols import symbol_to_filename
        return SHADOW_OHLCV_ROOT / exchange.lower() / timeframe / f"{symbol_to_filename(symbol)}.csv"

    def save_ohlcv(self, exchange: str, symbol: str, timeframe: str, frame: pd.DataFrame) -> Path:
        if frame.empty:
            raise ValueError("refusing to replace HTF reclaim cache with an empty frame")
        path = self._path(exchange, symbol, timeframe)
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_name(f".{path.name}.{os.getpid()}.{uuid.uuid4().hex}.tmp")
        try:
            with tmp.open("w", encoding="utf-8", newline="") as handle:
                frame.to_csv(handle, index=False)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(tmp, path)
        finally:
            try:
                tmp.unlink(missing_ok=True)
            except OSError:
                pass
        return path

    def load_ohlcv(self, exchange: str, symbol: str, timeframe: str) -> pd.DataFrame | None:
        path = self._path(exchange, symbol, timeframe)
        if path.exists():
            try:
                frame = pd.read_csv(path)
            except (OSError, UnicodeDecodeError, pd.errors.EmptyDataError, pd.errors.ParserError):
                return None
            if not frame.empty:
                frame["timestamp"] = pd.to_datetime(frame.get("timestamp"), utc=True, errors="coerce")
                return frame.dropna(subset=["timestamp"]).reset_index(drop=True)
        return self.fallback.load_ohlcv(exchange, symbol, timeframe)


def _ohlcv_store() -> HtfOhlcvStore:
    return HtfOhlcvStore(FileStore(load_config()))


def _load_frame(symbol: str, timeframe: str) -> pd.DataFrame:
    store = _ohlcv_store()
    for exchange in ("bybit_linear", "bybit", "binance", "mexc"):
        frame = normalize_frame(store.load_ohlcv(exchange, _canonical(symbol), timeframe))
        if not frame.empty:
            return frame
    return pd.DataFrame()


def _symbols(intelligence_conn: sqlite3.Connection, now: datetime, cfg: dict[str, Any]) -> list[str]:
    from src.execution.crypto_derivreset_v3_shadow import _symbols as latest_symbols
    return latest_symbols(intelligence_conn, now, {
        "primary_exchange": cfg["primary_exchange"],
        "derivative_freshness_minutes": cfg["derivatives_freshness_minutes"],
        "max_symbols": cfg["max_symbols"],
    })


def refresh_ohlcv(*, cfg: dict[str, Any] | None = None) -> dict[str, Any]:
    """Refresh a horizon only when a new candle has started.

    A full 40-symbol download of all three horizons every two minutes would
    compete with the execution-adjacent collector for both network time and
    SQLite attention.  The current open candle is sufficient to know the last
    closed candle; we fetch again when the exchange should have begun a new
    one. This yields 15m updates on 15m boundaries, 1h hourly and 4h every
    four hours, plus immediate recovery for a missing cache.
    """
    cfg = cfg or load_strategy_config()
    if not cfg.get("feature_flag"):
        return {"enabled": False, "symbols": 0, "timeframes": {}}
    from src.data_collectors import market_intelligence_store as mi
    from src.execution.crypto_derivreset_v3_shadow import _refresh_bybit_linear

    now = utc_now()
    intelligence = mi.connect(ensure=False)
    try:
        symbols = _symbols(intelligence, now, cfg)
    finally:
        intelligence.close()
    # BTC is required for a real alignment verdict but is not counted against
    # the liquid-alt universe cap.
    symbols = list(dict.fromkeys([*symbols, "BTC/USDT"]))
    store = _ohlcv_store()
    details: dict[str, dict[str, Any]] = {}
    for timeframe in (cfg["structure_timeframe"], cfg["sweep_timeframe"], cfg["confirmation_timeframe"]):
        minutes = _minutes(str(timeframe))
        expected_open = pd.Timestamp(now).floor(f"{minutes}min")
        due = []
        for symbol in symbols:
            frame = normalize_frame(store.load_ohlcv("bybit_linear", symbol, str(timeframe)))
            latest = frame["timestamp"].iloc[-1] if not frame.empty else None
            if latest is None or pd.Timestamp(latest) < expected_open:
                due.append(symbol)
        fetched, failed = _refresh_bybit_linear(due, str(timeframe), store) if due else ([], {})
        details[str(timeframe)] = {"due": len(due), "cached": len(symbols) - len(due),
                                  "fetched": len(fetched), "failed": len(failed),
                                  "failed_symbols": sorted(failed)[:10]}
    return {"symbols": len(symbols), "timeframes": details, "price_exchange": "bybit_linear"}


def confirmed_pivot_levels(frame: pd.DataFrame, *, as_of: datetime, cfg: dict[str, Any]) -> list[dict[str, Any]]:
    """Return only pivots whose right-hand confirmation bars had already closed.

    A 4h high/low is not usable at the pivot bar itself: it becomes available
    only after ``pivot_right_bars`` subsequent *closed* 4h candles.  This is
    the key guard against look-ahead bias in this lane.
    """
    frame = normalize_frame(frame)
    left, right = int(cfg["pivot_left_bars"]), int(cfg["pivot_right_bars"])
    last = _latest_closed_index(frame, as_of, str(cfg["structure_timeframe"]))
    if last is None or last < left + right:
        return []
    start = max(left, last - int(cfg["structure_lookback_bars"]))
    levels: list[dict[str, Any]] = []
    for idx in range(start, last - right + 1):
        chunk = frame.iloc[idx - left:idx + right + 1]
        high, low = _f(frame.iloc[idx].get("high")), _f(frame.iloc[idx].get("low"))
        atr = _atr(frame, idx)
        pivot_at = _dt(frame.iloc[idx].get("timestamp"))
        if high is None or low is None or atr is None or pivot_at is None:
            continue
        known_at = _dt(frame.iloc[idx + right].get("timestamp"))
        if known_at is None:
            continue
        known_at += _delta(str(cfg["structure_timeframe"]))
        if known_at > as_of:
            continue
        width = atr * float(cfg["zone_width_atr"])
        # Deterministic first-occurrence tie handling prevents duplicate zones
        # when two equal highs/lows appear in a small pivot window.
        if high == float(chunk["high"].max()) and int(chunk["high"].idxmax()) == idx:
            levels.append({"kind": "resistance", "price": high, "zone_width": width,
                           "pivot_at": pivot_at, "known_at": known_at})
        if low == float(chunk["low"].min()) and int(chunk["low"].idxmin()) == idx:
            levels.append({"kind": "support", "price": low, "zone_width": width,
                           "pivot_at": pivot_at, "known_at": known_at})
    return levels


def _matching_liquidations(events: list[dict[str, Any]], *, direction: str, decision_at: datetime,
                           cfg: dict[str, Any]) -> tuple[list[dict[str, Any]], str | None]:
    if not events:
        return [], "LIQUIDATION_NOT_OBSERVED"
    wanted = "SELL" if direction == "long" else "BUY"
    start = decision_at - timedelta(minutes=float(cfg["liquidation_window_minutes"]))
    matched = [event for event in events if str(event.get("side") or "").upper() == wanted
               and (at := _dt(event.get("event_at"))) is not None and start <= at <= decision_at]
    if not matched:
        return [], "LIQUIDATION_SIDE_MISMATCH"
    if sum(float(event.get("notional_usd") or 0.0) for event in matched) < float(cfg["min_liquidation_notional_usd"]):
        return matched, "LIQUIDATION_NOTIONAL_TOO_SMALL"
    return matched, None


def detect_structural_sweep(structure_frame: pd.DataFrame, sweep_frame: pd.DataFrame, sweep_idx: int,
                            events: list[dict[str, Any]], cfg: dict[str, Any],
                            *, liquidation_feed_available: bool = True) -> dict[str, Any]:
    """Detect a completed 1h raid of a previously confirmed 4h zone."""
    sweep_frame = normalize_frame(sweep_frame)
    if sweep_frame.empty or sweep_idx < 20:
        return {"ok": False, "reason": "CANDLES_MISSING"}
    row = sweep_frame.iloc[sweep_idx]
    sweep_at = _dt(row.get("timestamp"))
    if sweep_at is None:
        return {"ok": False, "reason": "CANDLES_MISSING"}
    decision_at = sweep_at + _delta(str(cfg["sweep_timeframe"]))
    levels = confirmed_pivot_levels(structure_frame, as_of=decision_at, cfg=cfg)
    if not levels:
        return {"ok": False, "reason": "NO_CONFIRMED_HTF_LEVEL", "decision_at": decision_at, "sweep_at": sweep_at}
    high, low, close, open_ = (_f(row.get(key)) for key in ("high", "low", "close", "open"))
    atr = _atr(sweep_frame, sweep_idx)
    if None in (high, low, close, open_, atr):
        return {"ok": False, "reason": "CANDLES_MISSING", "decision_at": decision_at, "sweep_at": sweep_at}
    span = high - low
    if span <= 0:
        return {"ok": False, "reason": "NO_STRUCTURAL_SWEEP", "decision_at": decision_at, "sweep_at": sweep_at}
    pierce = float(atr) * float(cfg["min_sweep_atr"])
    long_levels = [level for level in levels if level["kind"] == "support"
                   and low <= float(level["price"]) - pierce and close >= float(level["price"])]
    short_levels = [level for level in levels if level["kind"] == "resistance"
                    and high >= float(level["price"]) + pierce and close <= float(level["price"])]
    if not long_levels and not short_levels:
        return {"ok": False, "reason": "NO_STRUCTURAL_SWEEP", "decision_at": decision_at, "sweep_at": sweep_at}
    # A large bar through both unrelated zones is not a directional reclaim.
    if long_levels and short_levels:
        return {"ok": False, "reason": "NO_STRUCTURAL_SWEEP", "decision_at": decision_at, "sweep_at": sweep_at}
    direction = "long" if long_levels else "short"
    level = (max(long_levels, key=lambda item: item["price"]) if long_levels
             else min(short_levels, key=lambda item: item["price"]))
    wick = ((min(open_, close) - low) / span if direction == "long"
            else (high - max(open_, close)) / span)
    close_location = ((close - low) / span if direction == "long" else (high - close) / span)
    prior_volume = _f(sweep_frame.iloc[max(0, sweep_idx - 20):sweep_idx]["volume"].median()) or 0.0
    volume = _f(row.get("volume")) or 0.0
    facts = {
        "decision_at": decision_at, "sweep_at": sweep_at, "direction": direction,
        "level": level, "sweep_close": close, "sweep_extreme": low if direction == "long" else high,
        "sweep_atr": atr, "wick_share": wick, "close_location": close_location,
        "rvol": volume / prior_volume if prior_volume else None,
    }
    if wick < float(cfg["min_wick_share"]) or close_location < float(cfg["min_close_location"]):
        return {**facts, "ok": False, "reason": "SWEEP_WICK_TOO_SMALL"}
    if not prior_volume or volume / prior_volume < float(cfg["min_rvol"]):
        return {**facts, "ok": False, "reason": "SWEEP_RVOL_TOO_WEAK"}
    if not liquidation_feed_available:
        return {**facts, "ok": False, "reason": "LIQUIDATION_DATA_MISSING"}
    matched, reason = _matching_liquidations(events, direction=direction, decision_at=decision_at, cfg=cfg)
    if reason:
        return {**facts, "ok": False, "reason": reason,
                "liquidation_notional_usd": sum(float(item.get("notional_usd") or 0.0) for item in matched),
                "event_ids": [str(item.get("event_id")) for item in matched]}
    opposing_kind = "resistance" if direction == "long" else "support"
    opposing = sorted((item for item in levels if item["kind"] == opposing_kind
                       and ((item["price"] > close) if direction == "long" else (item["price"] < close))),
                      key=lambda item: item["price"], reverse=direction == "short")
    if not opposing:
        return {**facts, "ok": False, "reason": "OPPOSING_LEVEL_TOO_CLOSE"}
    opposing_level = opposing[0]
    stop = (low - float(atr) * float(cfg["stop_buffer_atr"]) if direction == "long"
            else high + float(atr) * float(cfg["stop_buffer_atr"]))
    risk = abs(close - stop)
    if risk <= 0 or (direction == "long" and stop >= close) or (direction == "short" and stop <= close):
        return {**facts, "ok": False, "reason": "INVALID_STOP_GEOMETRY"}
    if risk / close > float(cfg["max_stop_distance_pct"]):
        return {**facts, "ok": False, "reason": "STOP_TOO_WIDE"}
    opposing_r = ((float(opposing_level["price"]) - close) / risk if direction == "long"
                  else (close - float(opposing_level["price"])) / risk)
    if opposing_r < float(cfg["min_opposing_level_r"]):
        return {**facts, "ok": False, "reason": "OPPOSING_LEVEL_TOO_CLOSE", "opposing_level": opposing_level,
                "opposing_level_r": opposing_r}
    return {**facts, "ok": True, "stop": stop, "risk": risk, "opposing_level": opposing_level,
            "opposing_level_r": opposing_r,
            "liquidation_notional_usd": sum(float(item.get("notional_usd") or 0.0) for item in matched),
            "event_ids": [str(item.get("event_id")) for item in matched],
            "liquidation_exchanges": sorted({str(item.get("exchange") or "unknown") for item in matched})}


def _event_rows(conn: sqlite3.Connection, symbol: str, at: datetime, cfg: dict[str, Any]) -> list[dict[str, Any]]:
    from src.data_collectors.market_intelligence_store import normalize_symbol
    exchanges = [str(value).lower() for value in (cfg.get("liquidation_sources") or [])]
    if not exchanges:
        return []
    start = (at - timedelta(minutes=float(cfg["liquidation_window_minutes"]))).isoformat()
    placeholders = ",".join("?" for _ in exchanges)
    rows = conn.execute("SELECT exchange,event_id,event_at,side,notional_usd FROM liquidation_events "
                        f"WHERE normalized_symbol=? AND exchange IN ({placeholders}) AND event_at>=? AND event_at<=?",
                        (normalize_symbol(symbol), *exchanges, start, at.isoformat())).fetchall()
    return [dict(row) for row in rows]


def _liquidation_feed_status(conn: sqlite3.Connection, cfg: dict[str, Any], now: datetime) -> dict[str, Any]:
    venues = [str(value).lower() for value in (cfg.get("liquidation_sources") or [])]
    if not venues:
        return {"feed_available": False, "status": "DISABLED"}
    sources = [f"liquidations:{venue}_ws" for venue in venues]
    placeholders = ",".join("?" for _ in sources)
    try:
        health = conn.execute("SELECT status,last_success_at FROM intelligence_source_health "
                              f"WHERE source IN ({placeholders})", sources).fetchall()
    except sqlite3.Error:
        health = []
    fresh_cutoff = now - timedelta(minutes=15)
    active = [row for row in health if str(row["status"]) in {"ok", "degraded"}
              and (_dt(row["last_success_at"]) or datetime.min.replace(tzinfo=timezone.utc)) >= fresh_cutoff]
    observation_venues = list(dict.fromkeys(
        [*venues, *(str(value).lower() for value in (cfg.get("liquidation_observation_sources") or []))]
    ))
    observation_placeholders = ",".join("?" for _ in observation_venues)
    try:
        observation_count = int(conn.execute(
            f"SELECT COUNT(*) FROM liquidation_events WHERE exchange IN ({observation_placeholders})",
            observation_venues,
        ).fetchone()[0])
        observation_latest = conn.execute(
            f"SELECT MAX(event_at) FROM liquidation_events WHERE exchange IN ({observation_placeholders})",
            observation_venues,
        ).fetchone()[0]
    except sqlite3.Error:
        observation_count, observation_latest = 0, None
    return {
        "feed_available": bool(active), "status": "OK" if active else "UNAVAILABLE",
        # Deliberately diagnostic: a quiet/stale third venue cannot suppress a
        # Binance/Bybit-confirmed candidate.
        "observation": {"venues": observation_venues, "event_count": observation_count,
                        "latest_event_at": observation_latest},
    }


def _oi_change_between(conn: sqlite3.Connection, symbol: str, *, older_at: datetime, newer_at: datetime,
                       freshness_minutes: float) -> tuple[float | None, int]:
    """Same-venue point-in-time OI change; never compare mixed venue sets."""
    from src.data_collectors.market_intelligence_store import normalize_symbol
    norm = normalize_symbol(symbol)
    current = conn.execute(
        "SELECT * FROM (SELECT exchange,oi_usd,provider_ts,ROW_NUMBER() OVER "
        "(PARTITION BY exchange ORDER BY provider_ts DESC,id DESC) rn FROM derivative_snapshots "
        "WHERE normalized_symbol=? AND provider_ts>=? AND provider_ts<=? AND oi_usd IS NOT NULL) WHERE rn=1",
        (norm, (newer_at - timedelta(minutes=freshness_minutes)).isoformat(), newer_at.isoformat()),
    ).fetchall()
    prior_sum = current_sum = 0.0
    pairs = 0
    for item in current:
        now_oi = _f(item["oi_usd"])
        if not now_oi or now_oi <= 0:
            continue
        previous = conn.execute(
            "SELECT oi_usd,provider_ts FROM derivative_snapshots WHERE normalized_symbol=? AND exchange=? "
            "AND provider_ts<=? AND provider_ts>=? AND oi_usd IS NOT NULL ORDER BY provider_ts DESC,id DESC LIMIT 1",
            (norm, item["exchange"], older_at.isoformat(),
             (older_at - timedelta(minutes=freshness_minutes)).isoformat()),
        ).fetchone()
        old_oi = _f(previous["oi_usd"]) if previous else None
        if old_oi and old_oi > 0:
            prior_sum += old_oi
            current_sum += now_oi
            pairs += 1
    return ((current_sum - prior_sum) / prior_sum * 100.0 if pairs and prior_sum > 0 else None), pairs


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
    prior_at = at - _delta(str(cfg["sweep_timeframe"]))
    oi_change, pairs = _oi_change_between(conn, symbol, older_at=prior_at, newer_at=at,
                                           freshness_minutes=float(cfg["derivatives_freshness_minutes"]))
    if oi_change is None:
        return {"ok": False, "reason": "OI_DATA_MISSING", "spread_bps": spread}
    if oi_change > -float(cfg["min_oi_drop_pct"]):
        return {"ok": False, "reason": "OI_NOT_FLUSHING", "oi_change_pct": oi_change, "spread_bps": spread}
    return {"ok": True, "oi_change_pct": oi_change, "oi_venue_pairs": pairs, "spread_bps": spread,
            "funding_rate_8h": _f(derivative.get("funding_rate_8h"))}


def _funding_is_adverse(direction: str, funding: float | None, cfg: dict[str, Any]) -> bool:
    if funding is None:
        return False
    limit = float(cfg["max_adverse_funding_8h"])
    return funding > limit if direction == "long" else funding < -limit


def _btc_alignment(direction: str, at: datetime, cfg: dict[str, Any]) -> str:
    frame = _load_frame("BTC/USDT", str(cfg["structure_timeframe"]))
    last = _latest_closed_index(frame, at, str(cfg["structure_timeframe"]))
    lookback = int(cfg["btc_ema_bars"])
    if last is None or last + 1 < lookback:
        return "missing"
    closes = pd.to_numeric(frame.iloc[last - lookback + 1:last + 1]["close"], errors="coerce").dropna()
    if len(closes) < lookback:
        return "missing"
    ema = float(closes.ewm(span=lookback, adjust=False).mean().iloc[-1])
    close = float(closes.iloc[-1])
    desired = close >= ema if direction == "long" else close <= ema
    return "aligned" if desired else "conflict"


def _candidate_id(event_id: str, profile: str) -> str:
    return "chtflr_" + hashlib.sha256(f"{event_id}|{profile}".encode()).hexdigest()[:22]


def _event_id(cfg: dict[str, Any], symbol: str, at: datetime, direction: str) -> str:
    raw = f"{cfg['strategy_id']}|{_canonical(symbol)}|{at.isoformat()}|{direction}"
    return "chtfle_" + hashlib.sha256(raw.encode()).hexdigest()[:22]


def _observation_id(cfg: dict[str, Any], symbol: str, at: datetime, direction: str) -> str:
    raw = f"observation|{cfg['strategy_id']}|{_canonical(symbol)}|{at.isoformat()}|{direction}"
    return "chtflo_" + hashlib.sha256(raw.encode()).hexdigest()[:22]


def _upsert(conn: sqlite3.Connection, row: dict[str, Any]) -> None:
    values = [json_text(row.get(column)) if column.endswith("_json") else row.get(column) for column in OUTCOME_COLUMNS]
    columns = ",".join(OUTCOME_COLUMNS)
    updates = ",".join(f"{column}=excluded.{column}" for column in OUTCOME_COLUMNS if column != "candidate_id")
    conn.execute(f"INSERT INTO crypto_htf_liquidity_reclaim_v1_shadow_outcomes({columns}) "
                 f"VALUES({','.join('?' for _ in OUTCOME_COLUMNS)}) ON CONFLICT(candidate_id) DO UPDATE SET {updates}", values)


def _record_observation(conn: sqlite3.Connection, cfg: dict[str, Any], symbol: str, now: datetime,
                        setup: dict[str, Any], reason: str, source: dict[str, Any]) -> None:
    at, sweep_at, direction = setup.get("decision_at"), setup.get("sweep_at"), setup.get("direction")
    if not isinstance(at, datetime) or not isinstance(sweep_at, datetime) or direction not in {"long", "short"}:
        return
    row = {
        "observation_id": _observation_id(cfg, symbol, at, direction), "strategy_id": cfg["strategy_id"],
        "shadow_lane": cfg["shadow_lane"], "evaluated_at": now.isoformat(), "decision_at": at.isoformat(),
        "sweep_at": sweep_at.isoformat(), "symbol": _canonical(symbol), "direction": direction,
        "structure_level": (setup.get("level") or {}).get("price") if isinstance(setup.get("level"), dict) else None,
        "rejection_reason": reason,
        "features_json": {key: setup.get(key) for key in ("wick_share", "close_location", "rvol", "oi_change_pct", "opposing_level_r")},
        "notes_json": {"liquidation_source": source.get("status"), "feed_available": source.get("feed_available")},
    }
    values = [json_text(row.get(column)) if column.endswith("_json") else row.get(column) for column in OBSERVATION_COLUMNS]
    columns = ",".join(OBSERVATION_COLUMNS)
    updates = ",".join(f"{column}=excluded.{column}" for column in OBSERVATION_COLUMNS if column != "observation_id")
    conn.execute(f"INSERT INTO crypto_htf_liquidity_reclaim_v1_shadow_observations({columns}) "
                 f"VALUES({','.join('?' for _ in OBSERVATION_COLUMNS)}) ON CONFLICT(observation_id) DO UPDATE SET {updates}", values)


def _activation(conn: sqlite3.Connection, now: datetime, persist: bool) -> datetime:
    value = conn.execute("SELECT v FROM crypto_htf_liquidity_reclaim_v1_shadow_meta WHERE k='activated_at'").fetchone()
    activated = _dt(value[0]) if value else None
    if activated:
        return activated
    if persist:
        conn.execute("INSERT OR REPLACE INTO crypto_htf_liquidity_reclaim_v1_shadow_meta(k,v) VALUES('activated_at',?)", (now.isoformat(),))
    return now


def _confirmation_holds(frame: pd.DataFrame, idx: int, row: dict[str, Any], cfg: dict[str, Any]) -> bool:
    candle = frame.iloc[idx]
    level = float(row["structure_level"])
    width = float(row["structure_zone_width"] or 0.0)
    close, low, high = (_f(candle.get(key)) for key in ("close", "low", "high"))
    atr = _atr(frame, idx)
    if None in (close, low, high, atr):
        return False
    progress = float(atr) * float(cfg["confirmation_progress_atr"])
    if row["direction"] == "long":
        return close >= level + progress and low >= level - width
    return close <= level - progress and high <= level + width


def _confirmation_entry(frame: pd.DataFrame, row: dict[str, Any], now: datetime, cfg: dict[str, Any]) -> dict[str, Any]:
    """Choose a profile's closed 15m confirmation candle, or a terminal reject."""
    decision_at = _dt(row.get("decision_at"))
    if decision_at is None:
        return {"status": "skipped", "reason": "CANDLES_MISSING"}
    frame = normalize_frame(frame)
    last = _latest_closed_index(frame, now, str(cfg["confirmation_timeframe"]))
    if last is None:
        return {"status": "pending"}
    window_end = decision_at + _delta(str(cfg["confirmation_timeframe"])) * int(cfg["confirmation_window_bars"])
    candidates = frame.iloc[:last + 1]
    candidates = candidates[(candidates["timestamp"] >= pd.Timestamp(decision_at)) &
                            (candidates["timestamp"] < pd.Timestamp(window_end))]
    holds: list[int] = []
    failed = False
    level, width = float(row["structure_level"]), float(row["structure_zone_width"] or 0.0)
    for index, candle in candidates.iterrows():
        close = _f(candle.get("close"))
        if close is None:
            continue
        broken = close < level - width if row["direction"] == "long" else close > level + width
        if broken:
            failed = True
        if _confirmation_holds(frame, int(index), row, cfg):
            holds.append(int(index))
            required = 1 if row["entry_profile"] == "EARLY_RECLAIM" else 2
            confirmed = len(holds) >= 1 if required == 1 else (
                len(holds) >= 2 and holds[-1] == holds[-2] + 1
            )
            if confirmed:
                entry_index = holds[-1]
                entry_at = _dt(frame.iloc[entry_index].get("timestamp"))
                entry = _f(frame.iloc[entry_index].get("close"))
                if entry_at is not None and entry is not None:
                    return {"status": "entry", "entry_at": entry_at + _delta(str(cfg["confirmation_timeframe"])),
                            "entry": entry, "confirmation_bars": len(holds), "confirmation_index": entry_index}
        else:
            holds = []
    if last >= 0 and _dt(frame.iloc[last].get("timestamp")) and _dt(frame.iloc[last].get("timestamp")) + _delta(str(cfg["confirmation_timeframe"])) >= window_end:
        return {"status": "skipped", "reason": "RECLAIM_FAILED" if failed else "RECLAIM_WINDOW_EXPIRED"}
    return {"status": "pending"}


def _entry_geometry(row: dict[str, Any], entry: float, cfg: dict[str, Any]) -> dict[str, Any]:
    direction = str(row["direction"])
    stop = float(row["stop_price"])
    risk = abs(entry - stop)
    if risk <= 0 or (direction == "long" and stop >= entry) or (direction == "short" and stop <= entry):
        return {"ok": False, "reason": "INVALID_STOP_GEOMETRY"}
    if risk / entry > float(cfg["max_stop_distance_pct"]):
        return {"ok": False, "reason": "STOP_TOO_WIDE"}
    opposing = float(row["opposing_level_price"])
    opposing_r = ((opposing - entry) / risk if direction == "long" else (entry - opposing) / risk)
    if opposing_r < float(cfg["min_opposing_level_r"]):
        return {"ok": False, "reason": "OPPOSING_LEVEL_TOO_CLOSE"}
    target3 = (entry + (opposing - entry) * float(cfg["opposing_target_fraction"]) if direction == "long"
               else entry - (entry - opposing) * float(cfg["opposing_target_fraction"]))
    tp1 = entry + risk * float(cfg["tp1_r"]) if direction == "long" else entry - risk * float(cfg["tp1_r"])
    tp2 = entry + risk * float(cfg["tp2_r"]) if direction == "long" else entry - risk * float(cfg["tp2_r"])
    monotonic = tp1 < tp2 < target3 if direction == "long" else tp1 > tp2 > target3
    if not monotonic:
        return {"ok": False, "reason": "OPPOSING_LEVEL_TOO_CLOSE"}
    return {"ok": True, "stop": stop, "tp1": tp1, "tp2": tp2, "tp3": target3, "opposing_r": opposing_r}


def _entry_context(conn: sqlite3.Connection, row: dict[str, Any], *, entry_at: datetime, entry: float,
                   cfg: dict[str, Any]) -> dict[str, Any]:
    context = _contexts(conn, str(row["symbol"]), entry_at, cfg)
    if not context.get("ok"):
        return context
    funding = _f(context.get("funding_rate_8h"))
    if _funding_is_adverse(str(row["direction"]), funding, cfg):
        return {"ok": False, "reason": "FUNDING_AGAINST_DIRECTION", **context}
    sweep_at = _dt(row.get("decision_at"))
    if sweep_at is None:
        return {"ok": False, "reason": "DATA_DIRTY", **context}
    oi_rebuild, pairs = _oi_change_between(conn, str(row["symbol"]), older_at=sweep_at, newer_at=entry_at,
                                            freshness_minutes=float(cfg["derivatives_freshness_minutes"]))
    if oi_rebuild is None:
        return {"ok": False, "reason": "OI_DATA_MISSING", **context}
    features = _decode_json(row.get("features_json"))
    sweep_atr = _f(features.get("sweep_atr")) or 0.0
    progress = abs(entry - float(row["sweep_close"])) / max(sweep_atr, 1e-12)
    if oi_rebuild > float(cfg["max_oi_rebuild_pct"]) and progress < float(cfg["min_price_progress_atr"]):
        return {"ok": False, "reason": "RECLAIM_OI_STALLED", **context,
                "oi_rebuild_pct": oi_rebuild, "oi_rebuild_venue_pairs": pairs}
    return {"ok": True, **context, "oi_rebuild_pct": oi_rebuild, "oi_rebuild_venue_pairs": pairs}


def _mature_pending(conn: sqlite3.Connection, intelligence: sqlite3.Connection, now: datetime,
                    cfg: dict[str, Any]) -> tuple[int, int]:
    entered = skipped = 0
    rows = conn.execute("SELECT * FROM crypto_htf_liquidity_reclaim_v1_shadow_outcomes WHERE outcome_status='pending'").fetchall()
    for raw in rows:
        row = dict(raw)
        frame = _load_frame(str(row["symbol"]), str(cfg["confirmation_timeframe"]))
        confirmation = _confirmation_entry(frame, row, now, cfg)
        if confirmation["status"] == "pending":
            continue
        if confirmation["status"] == "skipped":
            row.update({"eligibility_status": "rejected", "rejection_reason": confirmation["reason"],
                        "data_status": "dirty", "is_clean_for_edge": 0, "outcome_status": "skipped",
                        "last_checked_at": now.isoformat()})
            _upsert(conn, row); skipped += 1
            continue
        entry_at, entry = confirmation["entry_at"], float(confirmation["entry"])
        geometry = _entry_geometry(row, entry, cfg)
        context = _entry_context(intelligence, row, entry_at=entry_at, entry=entry, cfg=cfg)
        reason = None if geometry.get("ok") and context.get("ok") else str(geometry.get("reason") or context.get("reason"))
        if reason:
            row.update({"eligibility_status": "rejected", "rejection_reason": reason, "data_status": "dirty",
                        "is_clean_for_edge": 0, "outcome_status": "skipped", "last_checked_at": now.isoformat(),
                        "features_json": {**_decode_json(row.get("features_json")), "confirmation": confirmation, "entry_context": context}})
            _upsert(conn, row); skipped += 1
            continue
        row.update({
            "entry_ts": entry_at.isoformat(), "entry_price": entry, "stop_price": geometry["stop"],
            "tp1": geometry["tp1"], "tp2": geometry["tp2"], "tp3": geometry["tp3"],
            "eligibility_status": "eligible", "rejection_reason": None, "data_status": "ok",
            "is_clean_for_edge": 1, "outcome_status": "open", "latency_seconds": max(0.0, (now - entry_at).total_seconds()),
            "features_json": {**_decode_json(row.get("features_json")), "confirmation": confirmation,
                              "entry_context": context, "opposing_level_r_at_entry": geometry["opposing_r"]},
            "last_checked_at": now.isoformat(),
        })
        _upsert(conn, row); entered += 1
    return entered, skipped


def _decode_json(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    try:
        parsed = json.loads(str(value or "{}"))
        return parsed if isinstance(parsed, dict) else {}
    except (TypeError, ValueError):
        return {}


def _funding_events(conn: sqlite3.Connection, symbol: str, entry_at: datetime, now: datetime) -> list[dict[str, Any]]:
    from src.data_collectors.market_intelligence_store import normalize_symbol
    rows = conn.execute("SELECT event_at,received_at,funding_rate,funding_rate_8h FROM funding_rate_events "
                        "WHERE normalized_symbol=? AND event_at>? AND event_at<=? ORDER BY event_at",
                        (normalize_symbol(symbol), entry_at.isoformat(), now.isoformat())).fetchall()
    return [dict(row) for row in rows]


def _mature_open(conn: sqlite3.Connection, intelligence: sqlite3.Connection, now: datetime, cfg: dict[str, Any]) -> int:
    closed = 0
    rows = conn.execute("SELECT * FROM crypto_htf_liquidity_reclaim_v1_shadow_outcomes WHERE outcome_status='open'").fetchall()
    for raw in rows:
        row = dict(raw)
        entry_at = _dt(row.get("entry_ts"))
        if entry_at is None:
            continue
        frame = _load_frame(str(row["symbol"]), str(cfg["confirmation_timeframe"]))
        future = frame[frame["timestamp"] > pd.Timestamp(entry_at)]
        if future.empty:
            continue
        force_close = len(future) >= int(cfg["max_holding_bars"])
        simulated = simulate_confirmed_close_entry(
            direction=str(row["direction"]), entry=float(row["entry_price"]), stop=float(row["stop_price"]),
            tp1=float(row["tp1"]), tp2=float(row["tp2"]), tp3=float(row["tp3"]),
            future_candles=future.iloc[:int(cfg["max_holding_bars"])], symbol=str(row["symbol"]),
            fee_profile=str(cfg["fee_profile"]), entry_at=entry_at,
            bar_minutes=_minutes(str(cfg["confirmation_timeframe"])),
            funding_events=_funding_events(intelligence, str(row["symbol"]), entry_at, now), force_close=force_close,
        ).to_dict()
        row.update({"outcome_status": simulated.get("status")})
        row.update({key: value for key, value in simulated.items() if key in OUTCOME_COLUMNS})
        row["last_checked_at"] = now.isoformat()
        _upsert(conn, row)
        closed += int(row.get("outcome_status") == "closed")
    return closed


def _create_pending_rows(conn: sqlite3.Connection, cfg: dict[str, Any], symbol: str, now: datetime,
                         setup: dict[str, Any], context: dict[str, Any]) -> list[dict[str, Any]]:
    event_id = _event_id(cfg, symbol, setup["decision_at"], setup["direction"])
    rows: list[dict[str, Any]] = []
    for profile, profile_id in dict(cfg["profiles"]).items():
        cid = _candidate_id(event_id, str(profile))
        if conn.execute("SELECT 1 FROM crypto_htf_liquidity_reclaim_v1_shadow_outcomes WHERE candidate_id=?", (cid,)).fetchone():
            continue
        level, opposing = setup["level"], setup["opposing_level"]
        row = {column: None for column in OUTCOME_COLUMNS}
        row.update({
            "candidate_id": cid, "event_id": event_id, "strategy_id": cfg["strategy_id"], "profile_id": profile_id,
            "shadow_lane": cfg["shadow_lane"], "window": "forward_post_activation", "generated_at": now.isoformat(),
            "decision_at": setup["decision_at"].isoformat(), "sweep_at": setup["sweep_at"].isoformat(),
            "symbol": _canonical(symbol), "direction": setup["direction"], "entry_profile": profile,
            "session_bucket": _session(setup["decision_at"]), "structure_level": level["price"],
            "structure_zone_width": level["zone_width"], "structure_pivot_at": level["pivot_at"].isoformat(),
            "opposing_level_price": opposing["price"], "sweep_close": setup["sweep_close"],
            # The sweep-time ATR-buffered stop from detect_structural_sweep() must survive onto the
            # pending row: _entry_geometry() reads row["stop_price"] to validate geometry at the
            # confirmation stage, before entry_price/tp1-3 exist. Without this, every candidate that
            # ever reaches confirmation crashes _mature_pending() with TypeError(float(None)).
            "stop_price": setup["stop"],
            "liquidation_notional_usd": setup["liquidation_notional_usd"], "liquidation_event_ids_json": setup["event_ids"],
            "oi_change_pct": context.get("oi_change_pct"), "funding_rate_8h": context.get("funding_rate_8h"),
            "spread_bps": context.get("spread_bps"), "eligibility_status": "pending_confirmation",
            "data_status": "pending", "is_clean_for_edge": 0, "outcome_status": "pending",
            "features_json": {
                "wick_share": setup["wick_share"], "close_location": setup["close_location"], "rvol": setup["rvol"],
                "sweep_atr": setup["sweep_atr"], "sweep_extreme": setup["sweep_extreme"],
                "opposing_level_r_at_sweep": setup["opposing_level_r"], "liquidation_sources": setup["liquidation_exchanges"],
                "structure_level_kind": level["kind"], "opposing_level_kind": opposing["kind"],
            },
            "notes_json": {"paper_untouched": True, "live_locked": True, "model_f": "authoritative_shared"},
            "last_checked_at": now.isoformat(),
        })
        _upsert(conn, row)
        rows.append(row)
    return rows


def tick(*, db: str | None = None, persist: bool = True, now: datetime | None = None,
         cfg: dict[str, Any] | None = None) -> dict[str, Any]:
    cfg = cfg or load_strategy_config()
    now = now or utc_now()
    if not cfg.get("feature_flag"):
        return {"enabled": False, "rows": [], "closed_matured": 0, "summary_by_profile": {}}
    from src.config import load_config as project_config
    from src.data_collectors import market_intelligence_store as mi

    path = Path(db) if db else project_config().db_path
    trading = sqlite3.connect(":memory:" if not persist and not path.exists() else path, timeout=10.0)
    trading.row_factory = sqlite3.Row
    if not persist and path.exists():
        trading.execute("BEGIN")
    intelligence = mi.connect(ensure=False)
    try:
        ensure_tables(trading)
        activated = _activation(trading, now, persist)
        entered, confirmation_skipped = _mature_pending(trading, intelligence, now, cfg)
        closed = _mature_open(trading, intelligence, now, cfg)
        source = _liquidation_feed_status(intelligence, cfg, now)
        inserted: list[dict[str, Any]] = []
        observations = 0
        for symbol in _symbols(intelligence, now, cfg):
            structure = _load_frame(symbol, str(cfg["structure_timeframe"]))
            hourly = _load_frame(symbol, str(cfg["sweep_timeframe"]))
            index = _latest_closed_index(hourly, now, str(cfg["sweep_timeframe"]))
            if index is None:
                continue
            decision_at = _dt(hourly.iloc[index].get("timestamp"))
            if decision_at is None:
                continue
            decision_at += _delta(str(cfg["sweep_timeframe"]))
            events = _event_rows(intelligence, symbol, decision_at, cfg)
            setup = detect_structural_sweep(structure, hourly, index, events, cfg,
                                            liquidation_feed_available=bool(source.get("feed_available")))
            if not setup.get("ok"):
                if persist and setup.get("decision_at"):
                    _record_observation(trading, cfg, symbol, now, setup, str(setup.get("reason")), source)
                    observations += 1
                continue
            context = _contexts(intelligence, symbol, setup["decision_at"], cfg)
            reason = None if context.get("ok") else str(context.get("reason"))
            if reason is None and _funding_is_adverse(str(setup["direction"]), _f(context.get("funding_rate_8h")), cfg):
                reason = "FUNDING_AGAINST_DIRECTION"
            alignment = _btc_alignment(str(setup["direction"]), setup["decision_at"], cfg)
            if reason is None and bool(cfg.get("require_btc_alignment")):
                reason = "BTC_ALIGNMENT_MISSING" if alignment == "missing" else "BTC_ALIGNMENT_CONFLICT" if alignment == "conflict" else None
            if reason is None and _session(setup["decision_at"]) in set(cfg.get("block_sessions") or []):
                reason = "WEAK_SESSION_BLOCKED"
            if reason:
                if persist:
                    setup["btc_alignment"] = alignment
                    _record_observation(trading, cfg, symbol, now, setup, reason, source)
                    observations += 1
                continue
            rows = _create_pending_rows(trading, cfg, symbol, now, setup, context)
            inserted.extend(rows)
        all_rows = [dict(row) for row in trading.execute("SELECT * FROM crypto_htf_liquidity_reclaim_v1_shadow_outcomes")]
        summary_by_profile: dict[str, dict[str, Any]] = {}
        diagnostics_by_profile: dict[str, dict[str, Any]] = {}
        for profile, profile_id in dict(cfg["profiles"]).items():
            rows = [row for row in all_rows if row.get("profile_id") == profile_id]
            summary_by_profile[profile] = clean_forward_summary(
                rows, activated_at=activated.isoformat(), now=now, min_closed=int(cfg["min_clean_closed"]),
                min_days=float(cfg["min_forward_days"]), min_pf=float(cfg["min_profit_factor"]),
                max_review_drawdown_usd=float(cfg["max_review_drawdown_usd"]),
            )
            diagnostics_by_profile[profile] = strategy_diagnostics(
                rows, group_keys=("direction", "session_bucket", "rejection_reason", "entry_profile")
            )
        if persist:
            cols = ("generated_at", "profile_id", "strategy_id", "activated_at", "forward_rows", "clean_rows",
                    "dirty_rows", "clean_closed", "net_pnl_usd", "net_r", "fees_usd", "slippage_usd", "funding_usd",
                    "profit_factor", "winrate", "max_drawdown_usd", "forward_days", "verdict", "diagnostics_json", "config_json")
            for profile, summary in summary_by_profile.items():
                trading.execute("INSERT OR REPLACE INTO crypto_htf_liquidity_reclaim_v1_shadow_evaluations(" + ",".join(cols) + ") "
                               "VALUES(" + ",".join("?" for _ in cols) + ")", (
                                   now.isoformat(), cfg["profiles"][profile], cfg["strategy_id"], activated.isoformat(),
                                   summary["forward_rows"], summary["clean_rows"], summary["dirty_rows"], summary["clean_closed"],
                                   summary["net_pnl_usd"], summary["net_r"], summary["fees_usd"], summary["slippage_usd"],
                                   summary["funding_usd"], summary["profit_factor"], summary["winrate"], summary["max_drawdown_usd"],
                                   summary["forward_days"], summary["verdict"], json_text(diagnostics_by_profile[profile]), json_text(cfg),
                               ))
            trading.commit()
        else:
            trading.rollback()
        return {"enabled": True, "rows": inserted, "entered_from_pending": entered,
                "confirmation_skipped": confirmation_skipped, "closed_matured": closed, "observations": observations,
                "summary_by_profile": summary_by_profile, "diagnostics_by_profile": diagnostics_by_profile,
                "liquidation_source": source}
    finally:
        intelligence.close()
        trading.close()


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# Crypto HTF Liquidity Reclaim v1 - Shadow", "",
        "4h confirmed pivots -> 1h observed liquidation sweep -> 15m reclaim.",
        "`EARLY_RECLAIM` (one closed confirmation) and `HELD_RECLAIM` (two) are independent profiles.",
        "No Paper signals, Telegram trade alerts, orders, or Live routing.", "",
        f"- enabled: `{result.get('enabled')}`",
        f"- liquidation transport: `{(result.get('liquidation_source') or {}).get('status', 'unknown')}`",
        f"- diagnostic liquidation coverage: `{','.join(((result.get('liquidation_source') or {}).get('observation') or {}).get('venues') or [])}` "
        f"({((result.get('liquidation_source') or {}).get('observation') or {}).get('event_count', 0)} events; not an entry gate)",
        f"- new pending rows: `{len(result.get('rows') or [])}` · confirmed entries: `{result.get('entered_from_pending', 0)}` · "
        f"confirmation skips: `{result.get('confirmation_skipped', 0)}` · matured: `{result.get('closed_matured', 0)}` · "
        f"observations: `{result.get('observations', 0)}`",
    ]
    for profile, summary in (result.get("summary_by_profile") or {}).items():
        lines.extend(["", f"## {profile}", "",
                      f"- verdict: **{summary.get('verdict')}** · clean closed: `{summary.get('clean_closed', 0)}` · "
                      f"net USD: `{summary.get('net_pnl_usd', 0.0):.2f}` · PF: `{summary.get('profit_factor')}`", ""])
        lines.extend(diagnostics_markdown((result.get("diagnostics_by_profile") or {}).get(profile) or {}))
    return "\n".join(lines)


def write_report(result: dict[str, Any], path: str | None = None) -> str:
    target = ROOT / (path or load_strategy_config()["report_path"])
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_markdown(result) + "\n", encoding="utf-8")
    return str(target)


__all__ = [
    "confirmed_pivot_levels", "detect_structural_sweep", "ensure_tables", "load_strategy_config",
    "refresh_ohlcv", "render_markdown", "tick", "write_report",
]
