"""Event-sequence Shadow experiment for Crypto Derivatives Reset Continuation.

A liquidation flush is observed at event time, then may mature into a
two-close reclaim while OI and funding reset during a bounded 60-minute window.
This module owns its price cache and only ``crypto_derivreset_v3_*`` tables.
It has no dependency on retired Derivatives Reset experiments.
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
    table_exists,
    utc_now,
)
from src.storage.file_store import FileStore


ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "config" / "shadow_crypto_derivreset_v3.yaml"
SHADOW_OHLCV_ROOT = ROOT / "data" / "shadow" / "derivreset_v3" / "ohlcv"
STRATEGY_KEY = "crypto_derivreset_v3"

DEFAULTS: dict[str, Any] = {
    "feature_flag": False,
    "strategy_id": "crypto_derivreset_v3",
    "profile_id": "crypto_derivreset_v3_event_sequence",
    "shadow_lane": "shadow_derivreset_v3",
    "timeframe": "5m",
    "primary_exchange": "bybit",
    "fallback_timeframes": ["15m"],
    "max_symbols": 40,
    "max_detection_latency_seconds": 420,
    "derivative_freshness_minutes": 10,
    "catalyst_freshness_hours": 24,
    "event_expiry_minutes": 60,
    "oi_peak_max_age_minutes": 120,
    "min_history_points": 3,
    "structure_lookback_bars": 24,
    "flush_window_bars": 12,
    "hold_bars": 2,
    "min_flush_wick_pct": 0.15,
    "min_post_reclaim_progress_pct": 0.15,
    "max_post_reclaim_progress_pct": 2.0,
    "max_stop_distance_pct": 3.0,
    "min_rvol": 1.2,
    "min_oi_drop_from_peak_pct": 0.5,
    "max_oi_drop_from_peak_pct": 20.0,
    "max_oi_rebuild_from_trough_pct": 0.5,
    "min_safe_oi_progress_pct": 0.3,
    "min_funding_extreme_abs": 0.0001,
    "funding_neutral_ratio": 0.70,
    "min_24h_quote_volume_usd": 10_000_000,
    "max_static_spread_bps_major": 8.0,
    "max_static_spread_bps_alt": 20.0,
    "spread_vs_1h_average_max": 2.0,
    "min_spread_history_samples": 3,
    "block_sessions": ["asia", "off"],
    "guard_mode": "intraday",
    "max_symbol_trades_per_12h": 1,
    "symbol_trade_cooldown_hours": 12,
    "original_stop_cooldown_hours": 24,
    "target_r": [1.0, 2.0, 3.0],
    "max_holding_bars": 288,
    "fee_profile": "bybit_non_vip_usdt_perp",
    "funding_exchange": "bybit",
    "funding_intervals": 1.0,
    "min_clean_closed": 30,
    "min_forward_days": 28,
    "min_profit_factor": 1.25,
    "max_review_drawdown_usd": 250.0,
    "report_path": "reports/CRYPTO_DERIVRESET_V3_SHADOW.md",
}

REJECTION_REASONS = {
    "CANDLES_MISSING", "DETECTION_LATENCY", "FLUSH_WICK_TOO_SMALL", "FLUSH_NOT_LOCAL_EXTREME",
    "RECLAIM_NOT_HELD_TWO_BARS", "STRUCTURE_NOT_RECLAIMED", "RECLAIM_TOO_EXTENDED",
    "INVALID_STOP_GEOMETRY", "STOP_TOO_WIDE", "RVOL_TOO_WEAK", "DERIVATIVES_MISSING",
    "DERIVATIVES_STALE", "OI_PEAK_NOT_EVENT_ALIGNED", "OI_DID_NOT_RESET", "OI_DROP_TOO_LARGE",
    "FUNDING_NOT_DIRECTIONAL", "FUNDING_NOT_EXTREME", "FUNDING_NOT_MEAN_REVERTED",
    "FAILED_RECLAIM_OI_BUILD", "LIQUIDITY_DATA_MISSING", "LIQUIDITY_TOO_LOW",
    "SPREAD_HISTORY_MISSING", "SPREAD_CASCADE_ACTIVE", "SPREAD_STATIC_TOO_WIDE",
    "BTC_ETH_REGIME_CONFLICT", "ONCHAIN_HARD_RISK", "PORTFOLIO_GUARD_BLOCKED",
    "WEAK_SESSION_BLOCKED", "SYMBOL_TRADE_COOLDOWN", "SYMBOL_STOP_COOLDOWN",
    "RECLAIM_WINDOW_EXPIRED", "DATA_DIRTY",
}

OUTCOME_COLUMNS = (
    "candidate_id", "event_id", "strategy_id", "profile_id", "shadow_lane", "window", "generated_at",
    "observed_at", "decision_at", "flush_at", "symbol", "direction", "session_bucket",
    "market_regime", "catalyst_state", "size_weight", "eligibility_status", "rejection_reason",
    "data_status", "is_clean_for_edge", "entry_ts", "entry_price", "stop_price", "tp1", "tp2", "tp3",
    "outcome_status", "close_reason", "exit_price", "exit_ts", "gross_pnl_usd", "net_pnl_usd",
    "net_r", "fees_usd", "slippage_usd", "funding_usd", "funding_source", "funding_estimated",
    "funding_event_count", "risk_usd", "mfe_r", "mae_r", "protection_armed", "lock_armed",
    "highest_tp_touched", "bars_held", "latency_seconds", "features_json", "notes_json", "last_checked_at",
)

OUTCOME_DDL = """
CREATE TABLE IF NOT EXISTS crypto_derivreset_v3_shadow_outcomes (
  candidate_id TEXT PRIMARY KEY, event_id TEXT NOT NULL, strategy_id TEXT NOT NULL, profile_id TEXT NOT NULL,
  shadow_lane TEXT NOT NULL, window TEXT NOT NULL, generated_at TEXT NOT NULL, observed_at TEXT NOT NULL,
  decision_at TEXT NOT NULL, flush_at TEXT, symbol TEXT NOT NULL, direction TEXT, session_bucket TEXT,
  market_regime TEXT, catalyst_state TEXT, size_weight REAL, eligibility_status TEXT NOT NULL,
  rejection_reason TEXT, data_status TEXT, is_clean_for_edge INTEGER NOT NULL DEFAULT 0, entry_ts TEXT,
  entry_price REAL, stop_price REAL, tp1 REAL, tp2 REAL, tp3 REAL, outcome_status TEXT, close_reason TEXT,
  exit_price REAL, exit_ts TEXT, gross_pnl_usd REAL, net_pnl_usd REAL, net_r REAL, fees_usd REAL,
  slippage_usd REAL, funding_usd REAL, funding_source TEXT, funding_estimated INTEGER,
  funding_event_count INTEGER, risk_usd REAL, mfe_r REAL, mae_r REAL, protection_armed INTEGER,
  lock_armed INTEGER, highest_tp_touched INTEGER, bars_held INTEGER, latency_seconds REAL,
  features_json TEXT, notes_json TEXT, last_checked_at TEXT
)
"""
EVENT_DDL = """
CREATE TABLE IF NOT EXISTS crypto_derivreset_v3_shadow_events (
  event_id TEXT PRIMARY KEY, strategy_id TEXT NOT NULL, profile_id TEXT NOT NULL, shadow_lane TEXT NOT NULL,
  symbol TEXT NOT NULL, direction TEXT NOT NULL, flush_at TEXT NOT NULL, observed_at TEXT NOT NULL,
  expires_at TEXT NOT NULL, level REAL NOT NULL, extreme REAL NOT NULL, wick_pct REAL NOT NULL,
  seed_oi_peak REAL, seed_funding_extreme REAL, status TEXT NOT NULL, last_reason TEXT,
  seed_features_json TEXT NOT NULL, last_features_json TEXT, last_checked_at TEXT NOT NULL
)
"""
EVAL_DDL = """
CREATE TABLE IF NOT EXISTS crypto_derivreset_v3_shadow_evaluations (
  generated_at TEXT PRIMARY KEY, strategy_id TEXT, profile_id TEXT, activated_at TEXT,
  forward_rows INTEGER, clean_rows INTEGER, dirty_rows INTEGER, clean_closed INTEGER,
  net_pnl_usd REAL, net_r REAL, fees_usd REAL, slippage_usd REAL, funding_usd REAL,
  profit_factor REAL, winrate REAL, max_drawdown_usd REAL, forward_days REAL, verdict TEXT,
  rejection_counts_json TEXT, diagnostics_json TEXT, config_json TEXT
)
"""
META_DDL = "CREATE TABLE IF NOT EXISTS crypto_derivreset_v3_shadow_meta (k TEXT PRIMARY KEY, v TEXT NOT NULL)"


def load_strategy_config() -> dict[str, Any]:
    return load_yaml_block(CONFIG_PATH, STRATEGY_KEY, DEFAULTS)


def ensure_tables(conn: sqlite3.Connection) -> None:
    conn.execute(OUTCOME_DDL)
    conn.execute(EVENT_DDL)
    conn.execute(EVAL_DDL)
    conn.execute(META_DDL)
    text_cols = {
        "event_id", "strategy_id", "profile_id", "shadow_lane", "window", "generated_at", "observed_at",
        "decision_at", "flush_at", "symbol", "direction", "session_bucket", "market_regime",
        "catalyst_state", "eligibility_status", "rejection_reason", "data_status", "entry_ts",
        "outcome_status", "close_reason", "exit_ts", "funding_source", "features_json", "notes_json",
        "last_checked_at",
    }
    int_cols = {"is_clean_for_edge", "funding_estimated", "funding_event_count", "protection_armed",
                "lock_armed", "highest_tp_touched", "bars_held"}
    ensure_columns(conn, "crypto_derivreset_v3_shadow_outcomes", {
        col: "TEXT" if col in text_cols else "INTEGER" if col in int_cols else "REAL"
        for col in OUTCOME_COLUMNS if col != "candidate_id"
    })
    conn.execute("CREATE INDEX IF NOT EXISTS idx_derivreset_v3_open ON "
                 "crypto_derivreset_v3_shadow_outcomes(outcome_status,entry_ts)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_derivreset_v3_events ON "
                 "crypto_derivreset_v3_shadow_events(status,symbol,flush_at)")


def _event_id(cfg: dict[str, Any], symbol: str, flush_at: datetime) -> str:
    raw = f"{cfg['strategy_id']}|{_canonical(symbol)}|{flush_at.isoformat()}"
    return "cdr3e_" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:20]


def _candidate_id(event_id: str, decision_at: datetime) -> str:
    return "cdr3o_" + hashlib.sha256(f"{event_id}|{decision_at.isoformat()}".encode("utf-8")).hexdigest()[:20]


def _bar_delta(cfg: dict[str, Any]) -> timedelta:
    value = str(cfg.get("timeframe") or "5m").lower()
    if value.endswith("m"):
        try:
            return timedelta(minutes=max(1, int(value[:-1])))
        except ValueError:
            pass
    return timedelta(minutes=5)


def _session(ts: datetime) -> str:
    hour = ts.astimezone(timezone.utc).hour
    if hour <= 6:
        return "asia"
    if hour <= 12:
        return "europe"
    if hour <= 20:
        return "us"
    return "off"


def _base(symbol: str) -> str:
    value = str(symbol or "").upper().split(":", 1)[0]
    return value.split("/", 1)[0].replace("USDT", "").replace("USD", "")


def _canonical(symbol: str) -> str:
    base = _base(symbol)
    return f"{base}/USDT" if base else str(symbol or "").upper()


def _normalized(symbol: str) -> str:
    return _canonical(symbol).replace("/", "")


def _f(value: Any) -> float | None:
    try:
        return None if value in (None, "") else float(value)
    except (TypeError, ValueError):
        return None


def _raw(row: dict[str, Any]) -> dict[str, Any]:
    try:
        value = json.loads(row.get("raw_json") or "{}")
        return value if isinstance(value, dict) else {}
    except (TypeError, ValueError):
        return {}


def _latest_closed_index(frame: pd.DataFrame, now: datetime, cfg: dict[str, Any]) -> int | None:
    if frame.empty:
        return None
    cutoff = pd.Timestamp(now) - pd.Timedelta(_bar_delta(cfg))
    closed = frame.index[frame["timestamp"] <= cutoff].tolist()
    return int(closed[-1]) if closed else None


class ShadowOhlcvStore:
    """V3-local price cache with a read-only desk-cache bootstrap fallback."""

    def __init__(self, fallback: FileStore):
        self.fallback = fallback

    @staticmethod
    def _path(exchange: str, symbol: str, timeframe: str) -> Path:
        from src.utils.symbols import symbol_to_filename
        return SHADOW_OHLCV_ROOT / exchange.lower() / timeframe / f"{symbol_to_filename(symbol)}.csv"

    def save_ohlcv(self, exchange: str, symbol: str, timeframe: str, frame: pd.DataFrame) -> Path:
        if frame.empty:
            raise ValueError("refusing to replace DerivReset v3 OHLCV cache with an empty frame")
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
                if "timestamp" in frame.columns:
                    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True, errors="coerce")
                    frame = frame.dropna(subset=["timestamp"])
                return frame if not frame.empty else None
        return self.fallback.load_ohlcv(exchange, symbol, timeframe)


def _shadow_ohlcv_store() -> ShadowOhlcvStore:
    return ShadowOhlcvStore(FileStore(load_config()))


def _load_frame_with_source(store: ShadowOhlcvStore, symbol: str, cfg: dict[str, Any]) -> tuple[pd.DataFrame, str | None]:
    exchanges = ["bybit_linear", str(cfg.get("primary_exchange") or "bybit"), "binance", "mexc"]
    for timeframe in [cfg["timeframe"], *cfg.get("fallback_timeframes", [])]:
        candidates: list[tuple[pd.DataFrame, str]] = []
        for exchange in dict.fromkeys(exchanges):
            normalized = normalize_frame(store.load_ohlcv(exchange, _canonical(symbol), timeframe))
            if not normalized.empty:
                candidates.append((normalized, exchange))
        if candidates:
            return max(candidates, key=lambda item: item[0]["timestamp"].iloc[-1])
    return pd.DataFrame(), None


def _load_frame(symbol: str, cfg: dict[str, Any]) -> tuple[pd.DataFrame, str | None]:
    return _load_frame_with_source(_shadow_ohlcv_store(), symbol, cfg)


def _symbols(intelligence_conn: sqlite3.Connection, now: datetime, cfg: dict[str, Any]) -> list[str]:
    """Return a bounded, liquid, fresh Bybit universe for the five-minute scan."""
    rows = intelligence_conn.execute(
        "SELECT normalized_symbol,raw_json,provider_ts FROM derivative_snapshots "
        "WHERE exchange=? AND provider_ts>=? AND provider_ts<=? "
        "ORDER BY normalized_symbol,provider_ts DESC,id DESC",
        (str(cfg["primary_exchange"]),
         (now - timedelta(minutes=float(cfg["derivative_freshness_minutes"]))).isoformat(), now.isoformat()),
    ).fetchall()
    latest: dict[str, tuple[float, str]] = {}
    for normalized_symbol, raw_json, _ in rows:
        symbol = _canonical(str(normalized_symbol or ""))
        if not symbol or symbol in latest:
            continue
        try:
            raw = json.loads(raw_json or "{}")
        except (TypeError, ValueError):
            raw = {}
        volume = _f((raw or {}).get("turnover24h") or (raw or {}).get("quoteVolume") or
                    (raw or {}).get("quote_volume") or (raw or {}).get("amount24")) or 0.0
        latest[symbol] = (volume, symbol)
    return [symbol for _, symbol in sorted(latest.values(), key=lambda item: (-item[0], item[1]))[:int(cfg["max_symbols"])]]


def _bybit_linear_symbol(exchange: Any, symbol: str) -> str | None:
    market_id = f"{_base(load_config().exchange_alias('bybit', _canonical(symbol)))}USDT"
    for market in exchange.markets_by_id.get(market_id, []):
        if market.get("linear") or market.get("swap"):
            return str(market["symbol"])
    return None


def _refresh_bybit_linear(symbols: list[str], timeframe: str, store: ShadowOhlcvStore) -> tuple[list[str], dict[str, str]]:
    try:
        import ccxt
    except ImportError as exc:  # pragma: no cover - deployment dependency
        return [], {symbol: f"ccxt unavailable: {exc}" for symbol in symbols}
    exchange = ccxt.bybit({"enableRateLimit": True, "options": {"defaultType": "linear"}})
    fetched: list[str] = []
    failed: dict[str, str] = {}
    try:
        exchange.load_markets()
        for symbol in symbols:
            native = _bybit_linear_symbol(exchange, symbol)
            if native is None:
                failed[symbol] = "Bybit linear contract not listed"
                continue
            try:
                rows = exchange.fetch_ohlcv(native, timeframe=timeframe, limit=load_config().candle_limit(timeframe))
                if not rows:
                    failed[symbol] = "empty response"
                    continue
                frame = pd.DataFrame(rows, columns=["timestamp", "open", "high", "low", "close", "volume"])
                frame["timestamp"] = pd.to_datetime(frame["timestamp"], unit="ms", utc=True)
                for column in ("open", "high", "low", "close", "volume"):
                    frame[column] = pd.to_numeric(frame[column], errors="coerce")
                frame = frame.dropna().sort_values("timestamp").reset_index(drop=True)
                if frame.empty:
                    failed[symbol] = "all rows invalid"
                    continue
                store.save_ohlcv("bybit_linear", symbol, timeframe, frame)
                fetched.append(symbol)
            except Exception as exc:  # network failure never becomes a fallback signal
                failed[symbol] = str(exc)[:240]
    finally:
        try:
            exchange.close()
        except Exception:
            pass
    return fetched, failed


def refresh_ohlcv(*, cfg: dict[str, Any] | None = None) -> dict[str, Any]:
    """Refresh only the isolated v3 Bybit Linear price cache."""
    cfg = cfg or load_strategy_config()
    now = utc_now()
    from src.data_collectors import market_intelligence_store as intelligence_store

    intelligence_conn = intelligence_store.connect(ensure=False)
    try:
        symbols = _symbols(intelligence_conn, now, cfg)
    finally:
        intelligence_conn.close()
    if not symbols:
        return {"symbols": 0, "fetched": 0, "failed": 0, "timeframe": cfg["timeframe"]}
    fetched, failed = _refresh_bybit_linear(symbols, str(cfg["timeframe"]), _shadow_ohlcv_store())
    return {"symbols": len(symbols), "fetched": len(fetched), "failed": len(failed),
            "timeframe": cfg["timeframe"], "price_exchange": "bybit_linear",
            "failed_symbols": sorted(failed)[:10]}


def _liquidity(rows: list[dict[str, Any]], cfg: dict[str, Any]) -> dict[str, Any]:
    latest = rows[-1] if rows else None
    if not latest:
        return {"ok": False, "reason": "LIQUIDITY_DATA_MISSING"}
    raw = _raw(latest)
    quote = _f(raw.get("turnover24h") or raw.get("quoteVolume") or raw.get("quote_volume") or
               raw.get("amount24") or raw.get("quoteVolume24h"))
    if quote is None:
        return {"ok": False, "reason": "LIQUIDITY_DATA_MISSING"}
    if quote < float(cfg["min_24h_quote_volume_usd"]):
        return {"ok": False, "reason": "LIQUIDITY_TOO_LOW", "quote_volume": quote}
    return {"ok": True, "quote_volume": quote}


def _spread(rows: list[dict[str, Any]], *, as_of: datetime, symbol: str, cfg: dict[str, Any]) -> dict[str, Any]:
    points: list[tuple[datetime, float]] = []
    for row in rows:
        at = parse_dt(row.get("provider_ts"))
        raw = _raw(row)
        bid = _f(raw.get("bid1Price") or raw.get("bid1") or raw.get("bidPrice") or raw.get("bid"))
        ask = _f(raw.get("ask1Price") or raw.get("ask1") or raw.get("askPrice") or raw.get("ask"))
        if at and as_of - timedelta(hours=1) <= at <= as_of and bid and ask and ask > bid:
            points.append((at, (ask - bid) / ((ask + bid) / 2.0) * 10000.0))
    points.sort()
    if len(points) < int(cfg["min_spread_history_samples"]) + 1:
        return {"ok": False, "reason": "SPREAD_HISTORY_MISSING", "samples": len(points)}
    history, current = points[:-1], points[-1][1]
    average = sum(value for _, value in history) / len(history)
    if average <= 0 or current > average * float(cfg["spread_vs_1h_average_max"]):
        return {"ok": False, "reason": "SPREAD_CASCADE_ACTIVE", "current": current, "average": average}
    cap = float(cfg["max_static_spread_bps_major"] if _base(symbol) in {"BTC", "ETH", "SOL", "BNB", "XRP"}
                else cfg["max_static_spread_bps_alt"])
    if current > cap:
        return {"ok": False, "reason": "SPREAD_STATIC_TOO_WIDE", "current": current, "cap": cap}
    return {"ok": True, "current": current, "average": average, "samples": len(points)}


def _market_alignment(store: ShadowOhlcvStore, direction: str, as_of: datetime) -> str:
    returns: list[float] = []
    for symbol in ("BTC/USDT", "ETH/USDT"):
        frame = None
        for exchange in ("bybit_linear", "bybit", "binance"):
            frame = store.load_ohlcv(exchange, symbol, "15m")
            if frame is not None and not frame.empty:
                break
        data = normalize_frame(frame)
        data = data[data["timestamp"] + pd.Timedelta(minutes=15) <= pd.Timestamp(as_of)].tail(5)
        if len(data) < 5:
            return "unknown"
        returns.append((float(data["close"].iloc[-1]) / float(data["close"].iloc[0]) - 1.0) * 100.0)
    if direction == "long" and all(value >= -0.10 for value in returns):
        return "aligned"
    if direction == "short" and all(value <= 0.10 for value in returns):
        return "aligned"
    return "conflict"


def _hard_onchain_risk(conn: sqlite3.Connection, symbol: str, as_of: datetime) -> bool:
    if not table_exists(conn, "token_security_snapshots"):
        return False
    row = conn.execute(
        "SELECT is_honeypot,is_blacklisted,sell_tax FROM token_security_snapshots "
        "WHERE upper(asset_symbol)=? AND provider_ts<=? AND (received_at IS NULL OR received_at<=?) "
        "ORDER BY provider_ts DESC,id DESC LIMIT 1",
        (_base(symbol), as_of.isoformat(), as_of.isoformat()),
    ).fetchone()
    return bool(row and (int(row[0] or 0) == 1 or int(row[1] or 0) == 1 or float(row[2] or 0) >= 25.0))


def _catalyst_state(conn: sqlite3.Connection, symbol: str, as_of: datetime, cfg: dict[str, Any]) -> str:
    """Read point-in-time catalyst context; absent data never widens eligibility."""
    if not table_exists(conn, "news_canonical_events"):
        return "unavailable"
    rows = conn.execute(
        "SELECT trusted_symbols_json,effective_at,published_at,available_at,event_latency_class,created_at "
        "FROM news_canonical_events WHERE lower(COALESCE(asset_class,''))='crypto' AND linkage_allowed=1 "
        "AND is_cluster_primary=1 AND effective_at>=? AND effective_at<=? "
        "AND (created_at IS NULL OR created_at<=?) ORDER BY effective_at DESC",
        ((as_of - timedelta(days=7)).isoformat(), as_of.isoformat(), as_of.isoformat()),
    ).fetchall()
    base = _base(symbol)
    for row in rows:
        try:
            symbols = json.loads(row[0] or "[]")
        except (TypeError, ValueError):
            symbols = []
        if base not in {_base(value) for value in symbols}:
            continue
        effective, materialized = parse_dt(row[3] or row[1] or row[2]), parse_dt(row[5])
        available = max(value for value in (effective, materialized) if value is not None) if (effective or materialized) else None
        if available is None or available > as_of:
            continue
        latency_class = str(row[4] or "")
        if latency_class in {"THESIS_EVENT", "EXPIRED_EVENT", "AVAILABILITY_UNKNOWN"}:
            return "thesis" if latency_class == "THESIS_EVENT" else "stale"
        return "fresh" if as_of - available <= timedelta(hours=float(cfg["catalyst_freshness_hours"])) else "stale"
    return "none"


def _portfolio_guard(*, symbol: str, direction: str, session_bucket: str, market_regime: str,
                     exposure: dict[str, Any], cooldowns: dict[Any, Any], overlay_cfg: dict[str, Any],
                     guard_mode: str) -> tuple[str, list[str]]:
    severity = {"FULL_SIZE": 0, "HALF_SIZE": 1, "SHADOW_ONLY": 2, "BLOCK": 3}
    action, reasons = "FULL_SIZE", []

    def bump(target: str, reason: str) -> None:
        nonlocal action
        target = target if target in severity else "HALF_SIZE"
        if severity[target] > severity[action]:
            action = target
        reasons.append(reason)

    session_cd = cooldowns.get(("session", guard_mode, session_bucket))
    if session_cd and overlay_cfg.get("session_cooldown_enabled", True):
        bump(str((overlay_cfg.get("session_cooldown") or {}).get("action", "HALF_SIZE")),
             f"session_cooldown[{session_cd.get('reason') or 'active'}]")
    canonical = _canonical(symbol)
    symbol_cd = cooldowns.get(("symbol", canonical, guard_mode))
    if symbol_cd and overlay_cfg.get("symbol_cooldown_enabled", True):
        symbol_cfg = overlay_cfg.get("symbol_cooldown") or {}
        try:
            stop_count = int(str(symbol_cd.get("reason") or "").split("_", 1)[0])
        except ValueError:
            stop_count = 0
        target = (str(symbol_cfg.get("action_severe", "SHADOW_ONLY"))
                  if stop_count >= int(symbol_cfg.get("severe_original_stops", 3))
                  else str(symbol_cfg.get("action_strong_confirmation", "HALF_SIZE")))
        bump(target, f"symbol_cooldown[{symbol_cd.get('reason') or 'active'}]")
    if overlay_cfg.get("exposure_guard_enabled", True):
        limits = overlay_cfg.get("exposure") or {}
        over_action = str(limits.get("over_limit_action", "HALF_SIZE"))
        if guard_mode == "intraday" and int(exposure.get("intraday_open", 0)) >= int(limits.get("max_open_crypto_intraday", 4)):
            bump(over_action, "exposure_max_open_intraday")
        if int((exposure.get("by_symbol_mode") or {}).get((canonical, guard_mode), 0)) >= int(limits.get("max_open_same_symbol_mode", 1)):
            bump("SHADOW_ONLY", "exposure_same_symbol_mode_conflict")
        if _base(symbol) not in {"BTC", "ETH"}:
            weak = market_regime in {"risk_off", "weak", "unknown", "conflict", "opposed"}
            cap = "max_open_alt_beta_same_direction_btc_weak" if weak else "max_open_alt_beta_same_direction"
            held = "alt_short" if direction == "short" else "alt_long"
            if int(exposure.get(held, 0)) >= int(limits.get(cap, 2 if weak else 3)):
                bump(over_action, "exposure_alt_beta_same_direction")
    return action, reasons


def _funding_events(intelligence_conn: sqlite3.Connection, symbol: str, entry_at: datetime,
                    now: datetime, cfg: dict[str, Any]) -> list[dict[str, Any]]:
    return [dict(row) for row in intelligence_conn.execute(
        "SELECT event_at,received_at,funding_rate,funding_rate_8h FROM funding_rate_events "
        "WHERE exchange=? AND normalized_symbol=? AND event_at>? AND event_at<=? "
        "AND (received_at IS NULL OR received_at<=?) ORDER BY event_at,id",
        (str(cfg["funding_exchange"]), _normalized(symbol), entry_at.isoformat(), now.isoformat(), now.isoformat()),
    ).fetchall()]


def _seed_structure(frame: pd.DataFrame, idx: int, cfg: dict[str, Any]) -> dict[str, Any]:
    lookback = int(cfg["structure_lookback_bars"])
    if idx < lookback:
        return {"ok": False, "reason": "CANDLES_MISSING"}
    pre = frame.iloc[idx - lookback:idx + 1].reset_index(drop=True)
    anchor = pre.iloc[-4:-1]
    if len(pre) < lookback + 1 or len(anchor) != 3:
        return {"ok": False, "reason": "CANDLES_MISSING"}
    trend_start = float(pre["close"].iloc[0])
    level = float(anchor["close"].median())
    direction = "long" if level >= trend_start else "short"
    flush = pre.iloc[-1]
    extreme = float(flush["low"] if direction == "long" else flush["high"])
    wick_pct = ((level - extreme) / level * 100.0 if direction == "long"
                else (extreme - level) / level * 100.0)
    if wick_pct < float(cfg["min_flush_wick_pct"]):
        return {"ok": False, "reason": "FLUSH_WICK_TOO_SMALL", "direction": direction,
                "level": level, "extreme": extreme, "wick_pct": wick_pct}
    local = pre.iloc[-int(cfg["flush_window_bars"]):]
    is_extreme = (extreme <= float(local["low"].min()) if direction == "long"
                  else extreme >= float(local["high"].max()))
    if not is_extreme:
        return {"ok": False, "reason": "FLUSH_NOT_LOCAL_EXTREME", "direction": direction,
                "level": level, "extreme": extreme, "wick_pct": wick_pct}
    flush_at = frame.loc[idx, "timestamp"].to_pydatetime() + _bar_delta(cfg)
    return {"ok": True, "direction": direction, "level": level, "extreme": extreme,
            "wick_pct": wick_pct, "flush_at": flush_at}


def _derivative_rows(intelligence_conn: sqlite3.Connection, symbol: str, as_of: datetime,
                     cfg: dict[str, Any]) -> list[dict[str, Any]]:
    return [dict(row) for row in intelligence_conn.execute(
        "SELECT * FROM derivative_snapshots WHERE normalized_symbol=? AND lower(exchange)=lower(?) "
        "AND provider_ts>=? AND provider_ts<=? AND (received_at IS NULL OR received_at<=?) "
        "ORDER BY provider_ts,id",
        (_normalized(symbol), str(cfg["primary_exchange"]), (as_of - timedelta(hours=24)).isoformat(),
         as_of.isoformat(), as_of.isoformat()),
    ).fetchall()]


def _derivative_context(rows: list[dict[str, Any]], *, as_of: datetime, flush_at: datetime,
                        direction: str, cfg: dict[str, Any], require_reset: bool) -> dict[str, Any]:
    usable: list[dict[str, Any]] = []
    for row in rows:
        at, received = parse_dt(row.get("provider_ts")), parse_dt(row.get("received_at"))
        oi, funding = _f(row.get("oi_usd")), _f(row.get("funding_rate_8h"))
        if at is None or at > as_of or (received is not None and received > as_of):
            continue
        if at < as_of - timedelta(hours=24) or oi is None or oi <= 0 or funding is None:
            continue
        usable.append({"at": at, "oi": oi, "funding": funding})
    if len(usable) < int(cfg["min_history_points"]):
        return {"ok": False, "reason": "DERIVATIVES_MISSING", "points": len(usable)}
    usable.sort(key=lambda item: item["at"])
    newest = usable[-1]["at"]
    if as_of - newest > timedelta(minutes=float(cfg["derivative_freshness_minutes"])):
        return {"ok": False, "reason": "DERIVATIVES_STALE", "newest": newest.isoformat()}
    before = [point for point in usable if flush_at - timedelta(minutes=float(cfg["oi_peak_max_age_minutes"]))
              <= point["at"] <= flush_at]
    if not before:
        return {"ok": False, "reason": "OI_PEAK_NOT_EVENT_ALIGNED"}
    oi_peak = max(before, key=lambda item: item["oi"])
    funding_extreme = max(before, key=lambda item: abs(item["funding"]))
    expected_sign = 1.0 if direction == "long" else -1.0
    if funding_extreme["funding"] * expected_sign < float(cfg["min_funding_extreme_abs"]):
        return {"ok": False, "reason": "FUNDING_NOT_DIRECTIONAL",
                "funding_extreme": funding_extreme["funding"], "expected_sign": expected_sign}
    base = {"ok": True, "newest": newest.isoformat(), "oi_peak": oi_peak["oi"],
            "oi_peak_at": oi_peak["at"].isoformat(), "funding_extreme": funding_extreme["funding"],
            "funding_extreme_at": funding_extreme["at"].isoformat()}
    if not require_reset:
        return base
    after = [point for point in usable if flush_at < point["at"] <= as_of]
    if not after:
        return {"ok": False, "reason": "OI_PEAK_NOT_EVENT_ALIGNED", **base}
    current = usable[-1]
    oi_drop_pct = (oi_peak["oi"] - current["oi"]) / oi_peak["oi"] * 100.0
    if oi_drop_pct < float(cfg["min_oi_drop_from_peak_pct"]):
        return {"ok": False, "reason": "OI_DID_NOT_RESET", **base, "oi_current": current["oi"],
                "oi_drop_pct": oi_drop_pct}
    if oi_drop_pct > float(cfg["max_oi_drop_from_peak_pct"]):
        return {"ok": False, "reason": "OI_DROP_TOO_LARGE", **base, "oi_current": current["oi"],
                "oi_drop_pct": oi_drop_pct}
    if abs(current["funding"]) > abs(funding_extreme["funding"]) * float(cfg["funding_neutral_ratio"]):
        return {"ok": False, "reason": "FUNDING_NOT_MEAN_REVERTED", **base,
                "oi_current": current["oi"], "oi_drop_pct": oi_drop_pct,
                "funding_current": current["funding"]}
    trough = min(after, key=lambda item: item["oi"])
    oi_rebuild_pct = ((current["oi"] - trough["oi"]) / trough["oi"] * 100.0) if trough["oi"] else 0.0
    return {**base, "oi_current": current["oi"], "oi_drop_pct": oi_drop_pct,
            "funding_current": current["funding"], "oi_trough": trough["oi"],
            "oi_rebuild_pct": oi_rebuild_pct}


def _reclaim_structure(frame: pd.DataFrame, idx: int, event: dict[str, Any], cfg: dict[str, Any]) -> dict[str, Any]:
    if idx < 1:
        return {"ok": False, "reason": "CANDLES_MISSING"}
    delta, flush_at = _bar_delta(cfg), parse_dt(event["flush_at"])
    if flush_at is None:
        return {"ok": False, "reason": "CANDLES_MISSING"}
    holds = frame.iloc[idx - 1:idx + 1].reset_index(drop=True)
    if len(holds) != int(cfg["hold_bars"]) or any(
        ts.to_pydatetime() + delta <= flush_at for ts in holds["timestamp"]
    ):
        return {"ok": False, "reason": "RECLAIM_NOT_HELD_TWO_BARS"}
    level, extreme, direction = float(event["level"]), float(event["extreme"]), str(event["direction"])
    closes = holds["close"].astype(float).tolist()
    held = all(close > level for close in closes) if direction == "long" else all(close < level for close in closes)
    if not held:
        return {"ok": False, "reason": "RECLAIM_NOT_HELD_TWO_BARS"}
    entry = closes[-1]
    if (direction == "long" and extreme >= entry) or (direction == "short" and extreme <= entry):
        return {"ok": False, "reason": "INVALID_STOP_GEOMETRY"}
    stop_pct = abs(entry - extreme) / entry * 100.0
    if stop_pct > float(cfg["max_stop_distance_pct"]):
        return {"ok": False, "reason": "STOP_TOO_WIDE", "stop_pct": stop_pct}
    progress_pct = ((entry - level) / level * 100.0 if direction == "long"
                    else (level - entry) / level * 100.0)
    if progress_pct < float(cfg["min_post_reclaim_progress_pct"]):
        return {"ok": False, "reason": "STRUCTURE_NOT_RECLAIMED", "progress_pct": progress_pct}
    if progress_pct > float(cfg["max_post_reclaim_progress_pct"]):
        return {"ok": False, "reason": "RECLAIM_TOO_EXTENDED", "progress_pct": progress_pct}
    prior = frame[(frame["timestamp"] + pd.Timedelta(delta) <= pd.Timestamp(flush_at))].tail(
        int(cfg["structure_lookback_bars"]))
    mean_volume = float(prior["volume"].astype(float).mean()) if not prior.empty else 0.0
    rvol = float(holds["volume"].iloc[-1]) / mean_volume if mean_volume else None
    if rvol is None or rvol < float(cfg["min_rvol"]):
        return {"ok": False, "reason": "RVOL_TOO_WEAK", "rvol": rvol}
    risk = abs(entry - extreme)
    targets = [entry + multiple * risk if direction == "long" else entry - multiple * risk
               for multiple in map(float, cfg["target_r"])]
    decision_at = holds["timestamp"].iloc[-1].to_pydatetime() + delta
    return {"ok": True, "entry": entry, "stop": extreme, "targets": targets, "rvol": rvol,
            "progress_pct": progress_pct, "stop_pct": stop_pct, "decision_at": decision_at}


def _event_row(cfg: dict[str, Any], symbol: str, seed: dict[str, Any], observed_at: datetime,
               derivatives: dict[str, Any]) -> dict[str, Any]:
    flush_at = seed["flush_at"]
    return {
        "event_id": _event_id(cfg, symbol, flush_at), "strategy_id": cfg["strategy_id"],
        "profile_id": cfg["profile_id"], "shadow_lane": cfg["shadow_lane"], "symbol": _canonical(symbol),
        "direction": seed["direction"], "flush_at": flush_at.isoformat(), "observed_at": observed_at.isoformat(),
        "expires_at": (flush_at + timedelta(minutes=float(cfg["event_expiry_minutes"]))).isoformat(),
        "level": seed["level"], "extreme": seed["extreme"], "wick_pct": seed["wick_pct"],
        "seed_oi_peak": derivatives.get("oi_peak"), "seed_funding_extreme": derivatives.get("funding_extreme"),
        "status": "pending", "last_reason": None,
        "seed_features_json": json_text({"structure": seed, "derivatives": derivatives}),
        "last_features_json": None, "last_checked_at": observed_at.isoformat(),
    }


def _base_outcome(cfg: dict[str, Any], event: dict[str, Any], observed_at: datetime,
                  decision_at: datetime, structure: dict[str, Any] | None = None) -> dict[str, Any]:
    structure = structure or {}
    return {
        "candidate_id": _candidate_id(str(event["event_id"]), decision_at), "event_id": event["event_id"],
        "strategy_id": cfg["strategy_id"], "profile_id": cfg["profile_id"], "shadow_lane": cfg["shadow_lane"],
        "window": "forward_post_activation", "generated_at": observed_at.isoformat(),
        "observed_at": observed_at.isoformat(), "decision_at": decision_at.isoformat(), "flush_at": event["flush_at"],
        "symbol": event["symbol"], "direction": event["direction"], "session_bucket": _session(decision_at),
        "market_regime": "unknown", "catalyst_state": "none", "size_weight": 1.0,
        "eligibility_status": "rejected", "rejection_reason": None, "data_status": "clean",
        "is_clean_for_edge": 1, "entry_ts": None, "entry_price": structure.get("entry"),
        "stop_price": structure.get("stop"), "tp1": None, "tp2": None, "tp3": None,
        "outcome_status": "skipped", "close_reason": None, "exit_price": None, "exit_ts": None,
        "gross_pnl_usd": None, "net_pnl_usd": None, "net_r": None, "fees_usd": 0.0,
        "slippage_usd": 0.0, "funding_usd": 0.0, "funding_source": "unavailable",
        "funding_estimated": 0, "funding_event_count": 0, "risk_usd": None, "mfe_r": None,
        "mae_r": None, "protection_armed": 0, "lock_armed": 0, "highest_tp_touched": 0,
        "bars_held": 0, "latency_seconds": max(0.0, (observed_at - decision_at).total_seconds()),
        "features_json": "{}", "notes_json": "{}", "last_checked_at": observed_at.isoformat(),
    }


def _reject(row: dict[str, Any], reason: str, features: dict[str, Any], *, dirty: bool = False) -> dict[str, Any]:
    if reason not in REJECTION_REASONS:
        raise ValueError(f"unregistered rejection reason: {reason}")
    row["rejection_reason"], row["features_json"] = reason, json_text(features)
    if dirty:
        row["data_status"], row["is_clean_for_edge"] = "dirty", 0
    return row


def _local_cooldown(conn: sqlite3.Connection, symbol: str, decision_at: datetime,
                    cfg: dict[str, Any]) -> str | None:
    since = decision_at - timedelta(hours=float(cfg["symbol_trade_cooldown_hours"]))
    entered = conn.execute(
        "SELECT COUNT(*) FROM crypto_derivreset_v3_shadow_outcomes WHERE symbol=? "
        "AND eligibility_status='eligible' AND entry_ts>=? AND entry_ts<?",
        (_canonical(symbol), since.isoformat(), decision_at.isoformat()),
    ).fetchone()[0]
    if int(entered) >= int(cfg["max_symbol_trades_per_12h"]):
        return "SYMBOL_TRADE_COOLDOWN"
    since_stop = decision_at - timedelta(hours=float(cfg["original_stop_cooldown_hours"]))
    stopped = conn.execute(
        "SELECT 1 FROM crypto_derivreset_v3_shadow_outcomes WHERE symbol=? AND close_reason='original_stop' "
        "AND exit_ts>=? AND exit_ts<? LIMIT 1",
        (_canonical(symbol), since_stop.isoformat(), decision_at.isoformat()),
    ).fetchone()
    return "SYMBOL_STOP_COOLDOWN" if stopped else None


def _upsert_event(conn: sqlite3.Connection, event: dict[str, Any]) -> None:
    cols = tuple(event)
    conn.execute("INSERT OR IGNORE INTO crypto_derivreset_v3_shadow_events (" + ",".join(cols) + ") VALUES (" +
                 ",".join("?" for _ in cols) + ")", tuple(event[col] for col in cols))


def _update_event(conn: sqlite3.Connection, event_id: str, *, status: str | None = None,
                  reason: str | None = None, features: dict[str, Any] | None = None,
                  now: datetime) -> None:
    fields: dict[str, Any] = {"last_checked_at": now.isoformat()}
    if status is not None:
        fields["status"] = status
    if reason is not None:
        fields["last_reason"] = reason
    if features is not None:
        fields["last_features_json"] = json_text(features)
    conn.execute("UPDATE crypto_derivreset_v3_shadow_events SET " + ",".join(f"{key}=?" for key in fields) +
                 " WHERE event_id=?", tuple(fields.values()) + (event_id,))


def _insert_outcome(conn: sqlite3.Connection, row: dict[str, Any]) -> bool:
    sql = "INSERT OR IGNORE INTO crypto_derivreset_v3_shadow_outcomes (" + ",".join(OUTCOME_COLUMNS) + ") VALUES (" + ",".join("?" for _ in OUTCOME_COLUMNS) + ")"
    before = conn.total_changes
    conn.execute(sql, tuple(row.get(col) for col in OUTCOME_COLUMNS))
    return conn.total_changes > before


def _activation(conn: sqlite3.Connection, now: datetime, cfg: dict[str, Any], persist: bool) -> datetime:
    row = conn.execute("SELECT v FROM crypto_derivreset_v3_shadow_meta WHERE k='activated_at'").fetchone()
    if row:
        return parse_dt(row[0]) or now
    if persist:
        conn.execute("INSERT INTO crypto_derivreset_v3_shadow_meta(k,v) VALUES ('activated_at',?)", (now.isoformat(),))
    return now


def _mature_open_outcomes(conn: sqlite3.Connection, intelligence_conn: sqlite3.Connection,
                          now: datetime, cfg: dict[str, Any]) -> int:
    rows = [dict(row) for row in conn.execute(
        "SELECT * FROM crypto_derivreset_v3_shadow_outcomes WHERE outcome_status='open'"
    ).fetchall()]
    closed = 0
    for row in rows:
        entry_at = parse_dt(row.get("entry_ts"))
        if entry_at is None:
            continue
        frame, _ = _load_frame(str(row["symbol"]), cfg)
        future = normalize_frame(frame)
        future = future[(future["timestamp"] >= pd.Timestamp(entry_at)) &
                        (future["timestamp"] + pd.Timedelta(_bar_delta(cfg)) <= pd.Timestamp(now))]
        features = json.loads(row.get("features_json") or "{}")
        funding = (features.get("derivatives") or {}).get("funding_current")
        sim = simulate_confirmed_close_entry(
            direction=str(row.get("direction") or "long"), entry=float(row["entry_price"]),
            stop=float(row["stop_price"]), tp1=float(row["tp1"]), tp2=float(row["tp2"]), tp3=float(row["tp3"]),
            future_candles=future, symbol=str(row["symbol"]), fee_profile=str(cfg["fee_profile"]),
            funding_rate_8h=_f(funding), funding_intervals=float(cfg["funding_intervals"]),
            funding_events=_funding_events(intelligence_conn, str(row["symbol"]), entry_at, now, cfg),
            entry_at=entry_at, bar_minutes=int(_bar_delta(cfg).total_seconds() // 60),
            force_close=len(future) >= int(cfg["max_holding_bars"]),
        ).to_dict()
        updates = {("outcome_status" if key == "status" else key): value for key, value in sim.items()}
        updates["last_checked_at"] = now.isoformat()
        if updates.get("net_pnl_usd") is not None:
            for key in ("gross_pnl_usd", "net_pnl_usd", "fees_usd", "slippage_usd", "funding_usd", "risk_usd"):
                if updates.get(key) is not None:
                    updates[key] = round(float(updates[key]) * float(row.get("size_weight") or 1.0), 4)
        allowed = [key for key in updates if key in OUTCOME_COLUMNS and key != "candidate_id"]
        conn.execute("UPDATE crypto_derivreset_v3_shadow_outcomes SET " +
                     ",".join(f"{key}=?" for key in allowed) + " WHERE candidate_id=? AND outcome_status='open'",
                     tuple(updates[key] for key in allowed) + (row["candidate_id"],))
        closed += int(updates.get("outcome_status") == "closed")
    return closed


def _finalize_expired(conn: sqlite3.Connection, event: dict[str, Any], now: datetime,
                      cfg: dict[str, Any]) -> dict[str, Any]:
    reason = str(event.get("last_reason") or "RECLAIM_WINDOW_EXPIRED")
    dirty = reason in {"CANDLES_MISSING", "DETECTION_LATENCY", "DERIVATIVES_MISSING", "DERIVATIVES_STALE",
                       "LIQUIDITY_DATA_MISSING", "SPREAD_HISTORY_MISSING", "DATA_DIRTY"}
    row = _base_outcome(cfg, event, now, parse_dt(event["expires_at"]) or now)
    return _reject(row, reason, {"seed": json.loads(event["seed_features_json"] or "{}"),
                                 "last": json.loads(event.get("last_features_json") or "{}")}, dirty=dirty)


def _process_pending_event(conn: sqlite3.Connection, intelligence_conn: sqlite3.Connection,
                           event: dict[str, Any], now: datetime, cfg: dict[str, Any], overlay_cfg: dict[str, Any],
                           exposure: dict[str, Any], cooldowns: dict[Any, Any]) -> dict[str, Any] | None:
    flush_at, expires_at = parse_dt(event["flush_at"]), parse_dt(event["expires_at"])
    if flush_at is None or expires_at is None:
        _update_event(conn, event["event_id"], status="rejected", reason="CANDLES_MISSING", now=now)
        return None
    if now >= expires_at:
        row = _finalize_expired(conn, event, now, cfg)
        _update_event(conn, event["event_id"], status="expired", reason=row["rejection_reason"], now=now)
        return row
    frame, source = _load_frame(str(event["symbol"]), cfg)
    idx = _latest_closed_index(frame, now, cfg)
    if idx is None:
        _update_event(conn, event["event_id"], reason="CANDLES_MISSING", now=now)
        return None
    decision_at = frame.loc[idx, "timestamp"].to_pydatetime() + _bar_delta(cfg)
    if decision_at <= flush_at:
        return None
    if (now - decision_at).total_seconds() > float(cfg["max_detection_latency_seconds"]):
        _update_event(conn, event["event_id"], reason="DETECTION_LATENCY", now=now)
        return None
    structure = _reclaim_structure(frame, idx, event, cfg)
    if not structure.get("ok"):
        _update_event(conn, event["event_id"], reason=str(structure["reason"]),
                      features={"structure": structure, "price_exchange": source}, now=now)
        return None
    row = _base_outcome(cfg, event, now, structure["decision_at"], structure)
    if row["session_bucket"] in {str(x) for x in cfg.get("block_sessions", [])}:
        _update_event(conn, event["event_id"], reason="WEAK_SESSION_BLOCKED", features={"structure": structure}, now=now)
        return None
    derivative_rows = _derivative_rows(intelligence_conn, str(event["symbol"]), structure["decision_at"], cfg)
    derivatives = _derivative_context(derivative_rows, as_of=structure["decision_at"], flush_at=flush_at,
                                      direction=str(event["direction"]), cfg=cfg, require_reset=True)
    if not derivatives.get("ok"):
        _update_event(conn, event["event_id"], reason=str(derivatives["reason"]),
                      features={"structure": structure, "derivatives": derivatives}, now=now)
        return None
    if (derivatives.get("oi_rebuild_pct", 0.0) > float(cfg["max_oi_rebuild_from_trough_pct"]) and
            structure["progress_pct"] < float(cfg["min_safe_oi_progress_pct"])):
        _update_event(conn, event["event_id"], reason="FAILED_RECLAIM_OI_BUILD",
                      features={"structure": structure, "derivatives": derivatives}, now=now)
        return None
    liquidity = _liquidity(derivative_rows, cfg)
    spread = _spread(derivative_rows, as_of=structure["decision_at"], symbol=str(event["symbol"]), cfg=cfg)
    for context in (liquidity, spread):
        if not context.get("ok"):
            _update_event(conn, event["event_id"], reason=str(context["reason"]),
                          features={"structure": structure, "derivatives": derivatives, "context": context}, now=now)
            return None
    market_regime = _market_alignment(_shadow_ohlcv_store(), str(event["direction"]), structure["decision_at"])
    row["market_regime"] = market_regime
    if market_regime != "aligned":
        _update_event(conn, event["event_id"], reason="BTC_ETH_REGIME_CONFLICT",
                      features={"structure": structure, "derivatives": derivatives, "market_regime": market_regime}, now=now)
        return None
    row["catalyst_state"] = _catalyst_state(conn, str(event["symbol"]), structure["decision_at"], cfg)
    if _hard_onchain_risk(intelligence_conn, str(event["symbol"]), structure["decision_at"]):
        result = _reject(row, "ONCHAIN_HARD_RISK", {"structure": structure, "derivatives": derivatives})
        _update_event(conn, event["event_id"], status="rejected", reason=result["rejection_reason"], now=now)
        return result
    cooldown = _local_cooldown(conn, str(event["symbol"]), structure["decision_at"], cfg)
    if cooldown:
        _update_event(conn, event["event_id"], reason=cooldown, now=now)
        return None
    action, reasons = _portfolio_guard(
        symbol=str(event["symbol"]), direction=str(event["direction"]), session_bucket=row["session_bucket"],
        market_regime=market_regime, exposure=exposure, cooldowns=cooldowns, overlay_cfg=overlay_cfg,
        guard_mode=str(cfg["guard_mode"]),
    )
    if action in {"SHADOW_ONLY", "BLOCK"}:
        _update_event(conn, event["event_id"], reason="PORTFOLIO_GUARD_BLOCKED",
                      features={"structure": structure, "derivatives": derivatives, "guard_reasons": reasons}, now=now)
        return None
    if action == "HALF_SIZE":
        row["size_weight"] = 0.5
    row.update({
        "eligibility_status": "eligible", "entry_ts": structure["decision_at"].isoformat(),
        "tp1": structure["targets"][0], "tp2": structure["targets"][1], "tp3": structure["targets"][2],
        "outcome_status": "open", "close_reason": "awaiting_future_bars",
        "features_json": json_text({"seed": json.loads(event["seed_features_json"] or "{}"),
                                     "structure": structure, "derivatives": derivatives, "liquidity": liquidity,
                                     "spread": spread, "price_exchange": source,
                                     "portfolio_guard_action": action, "portfolio_guard_reasons": reasons}),
    })
    _update_event(conn, event["event_id"], status="entered", now=now)
    return row


def _seed_events(conn: sqlite3.Connection, intelligence_conn: sqlite3.Connection, now: datetime,
                 cfg: dict[str, Any]) -> dict[str, int]:
    created = {"observed": 0, "pending": 0, "seed_rejected": 0, "late": 0, "missing": 0}
    for symbol in _symbols(intelligence_conn, now, cfg):
        frame, _ = _load_frame(symbol, cfg)
        idx = _latest_closed_index(frame, now, cfg)
        if idx is None:
            created["missing"] += 1
            continue
        seed = _seed_structure(frame, idx, cfg)
        if not seed.get("ok"):
            continue
        created["observed"] += 1
        flush_at = seed["flush_at"]
        event_id = _event_id(cfg, symbol, flush_at)
        if conn.execute("SELECT 1 FROM crypto_derivreset_v3_shadow_events WHERE event_id=?", (event_id,)).fetchone():
            continue
        if (now - flush_at).total_seconds() > float(cfg["max_detection_latency_seconds"]):
            created["late"] += 1
            continue
        active = conn.execute(
            "SELECT 1 FROM crypto_derivreset_v3_shadow_events WHERE symbol=? AND status='pending' LIMIT 1",
            (_canonical(symbol),),
        ).fetchone()
        if active:
            continue
        # A five-minute bar cannot be acted on until the monitor has observed
        # it. Use that bounded observation time, not the candle-close label,
        # for derivative freshness; ``received_at <= now`` still prevents any
        # information arriving after the actual decision from leaking in.
        derivatives = _derivative_context(_derivative_rows(intelligence_conn, symbol, now, cfg),
                                           as_of=now, flush_at=flush_at, direction=seed["direction"],
                                           cfg=cfg, require_reset=False)
        if not derivatives.get("ok"):
            event = _event_row(cfg, symbol, seed, now, {"oi_peak": None, "funding_extreme": None})
            event.update(status="rejected", last_reason=str(derivatives["reason"]),
                         last_features_json=json_text({"structure": seed, "derivatives": derivatives}))
            _upsert_event(conn, event)
            created["seed_rejected"] += 1
            continue
        _upsert_event(conn, _event_row(cfg, symbol, seed, now, derivatives))
        created["pending"] += 1
    return created


def tick(*, db: str | None = None, persist: bool = True, now: datetime | None = None,
         cfg: dict[str, Any] | None = None) -> dict[str, Any]:
    """Observe a fresh flush, then test only its bounded forward sequence."""
    cfg, now = cfg or load_strategy_config(), now or utc_now()
    if not bool(cfg.get("feature_flag")):
        return {"enabled": False, "generated_at": now.isoformat(), "summary": {}}
    path = Path(db) if db else Path(load_config().db_path)
    if not persist and not path.exists():
        # A first dry run has no prior Shadow state to read. Keep it entirely
        # in memory so no empty database or private table is created on disk.
        conn = sqlite3.connect(":memory:")
    else:
        # Copying a hot production SQLite database can block behind the monitor
        # writer. A normal read transaction gives dry-runs a coherent snapshot
        # without stalling the derivatives loop.
        conn = sqlite3.connect(path, timeout=10.0)
        if not persist:
            conn.execute("BEGIN")
    conn.row_factory = sqlite3.Row
    intelligence_conn: sqlite3.Connection | None = None
    try:
        ensure_tables(conn)
        from src.data_collectors import market_intelligence_store as intelligence_store
        intelligence_conn = intelligence_store.connect(ensure=False)
        activation = _activation(conn, now, cfg, persist)
        matured = _mature_open_outcomes(conn, intelligence_conn, now, cfg)
        try:
            from src.execution import crypto_quality_overlay as overlay
            overlay_cfg = overlay.load_cfg()
            exposure, cooldowns = overlay.open_exposure(conn), overlay.read_cooldowns(conn, now)
        except Exception:
            overlay_cfg, exposure, cooldowns = {}, {}, {}
        created = _seed_events(conn, intelligence_conn, now, cfg)
        new_rows: list[dict[str, Any]] = []
        pending = [dict(row) for row in conn.execute(
            "SELECT * FROM crypto_derivreset_v3_shadow_events WHERE status='pending' ORDER BY flush_at"
        ).fetchall()]
        for event in pending:
            row = _process_pending_event(conn, intelligence_conn, event, now, cfg, overlay_cfg, exposure, cooldowns)
            if row is not None:
                new_rows.append(row)
        if persist:
            for row in new_rows:
                _insert_outcome(conn, row)
        rows = [dict(row) for row in conn.execute("SELECT * FROM crypto_derivreset_v3_shadow_outcomes").fetchall()]
        summary = clean_forward_summary(rows, activated_at=activation.isoformat(), now=now,
                                        min_closed=int(cfg["min_clean_closed"]), min_days=float(cfg["min_forward_days"]),
                                        min_pf=float(cfg["min_profit_factor"]),
                                        max_review_drawdown_usd=float(cfg["max_review_drawdown_usd"]))
        rejections: dict[str, int] = {}
        for row in rows:
            reason = row.get("rejection_reason")
            if reason:
                rejections[str(reason)] = rejections.get(str(reason), 0) + 1
        event_counts = {str(row["status"]): int(row["n"]) for row in conn.execute(
            "SELECT status,COUNT(*) n FROM crypto_derivreset_v3_shadow_events GROUP BY status"
        ).fetchall()}
        seed_rejections = {str(row["last_reason"]): int(row["n"]) for row in conn.execute(
            "SELECT last_reason,COUNT(*) n FROM crypto_derivreset_v3_shadow_events "
            "WHERE status='rejected' GROUP BY last_reason"
        ).fetchall() if row["last_reason"]}
        diagnostics = strategy_diagnostics(rows, group_keys=("session_bucket", "market_regime", "direction", "catalyst_state"))
        diagnostics["event_funnel"] = {**created, **{f"status_{key}": value for key, value in event_counts.items()},
                                        "seed_rejections": seed_rejections}
        if persist:
            columns = ("generated_at", "strategy_id", "profile_id", "activated_at", "forward_rows", "clean_rows",
                       "dirty_rows", "clean_closed", "net_pnl_usd", "net_r", "fees_usd", "slippage_usd",
                       "funding_usd", "profit_factor", "winrate", "max_drawdown_usd", "forward_days", "verdict",
                       "rejection_counts_json", "diagnostics_json", "config_json")
            conn.execute("INSERT OR REPLACE INTO crypto_derivreset_v3_shadow_evaluations (" + ",".join(columns) +
                         ") VALUES (" + ",".join("?" for _ in columns) + ")",
                         (now.isoformat(), cfg["strategy_id"], cfg["profile_id"], activation.isoformat(),
                          *(summary[key] for key in ("forward_rows", "clean_rows", "dirty_rows", "clean_closed",
                            "net_pnl_usd", "net_r", "fees_usd", "slippage_usd", "funding_usd", "profit_factor",
                            "winrate", "max_drawdown_usd", "forward_days", "verdict")), json_text(rejections),
                          json_text(diagnostics), json_text(cfg)))
            conn.commit()
        else:
            conn.rollback()
        return {"enabled": True, "generated_at": now.isoformat(), "activated_at": activation.isoformat(),
                "strategy_id": cfg["strategy_id"], "profile_id": cfg["profile_id"], "shadow_lane": cfg["shadow_lane"],
                "rows": new_rows, "closed_matured": matured, "summary": summary, "rejection_counts": rejections,
                "diagnostics": diagnostics, "event_counts": event_counts, "config": cfg}
    finally:
        if intelligence_conn is not None:
            intelligence_conn.close()
        conn.close()


def render_markdown(result: dict[str, Any]) -> str:
    if not result.get("enabled"):
        return "# Crypto Derivatives Reset Continuation v3 (Shadow)\n\n- status: **DISABLED**\n"
    summary, funnel = result["summary"], (result.get("diagnostics") or {}).get("event_funnel") or {}
    lines = [
        "# Crypto Derivatives Reset Continuation v3 (Shadow)", "",
        f"- strategy: `{result['strategy_id']}`; lane: `{result['shadow_lane']}`",
        f"- activated: `{result['activated_at']}`; generated: `{result['generated_at']}`",
        "- Event sequence: fresh flush -> bounded OI/funding reset -> two-close reclaim.",
        "- Isolated Shadow only: no Paper/Live routing or ledger writes.", "",
        "| forward rows | clean closed | net USD | PF | win% | DD USD | fees | slippage | funding | verdict |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
        f"| {summary['forward_rows']} | {summary['clean_closed']} | {summary['net_pnl_usd']:.2f} | "
        f"{summary['profit_factor'] if summary['profit_factor'] is not None else 'n/a'} | "
        f"{summary['winrate'] if summary['winrate'] is not None else 'n/a'} | {summary['max_drawdown_usd']:.2f} | "
        f"{summary['fees_usd']:.2f} | {summary['slippage_usd']:.2f} | {summary['funding_usd']:.2f} | {summary['verdict']} |",
        "", "## Event Funnel", "",
    ]
    for key, value in sorted(funnel.items()):
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Outcome Rejections", ""])
    for reason, count in sorted(result.get("rejection_counts", {}).items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"- `{reason}`: {count}")
    lines.extend(["", "## Diagnostics", ""])
    lines.extend(diagnostics_markdown(result.get("diagnostics") or {}))
    return "\n".join(lines) + "\n"


def write_report(result: dict[str, Any], path: str | None = None) -> str:
    target = Path(path) if path else ROOT / str(result.get("config", DEFAULTS).get("report_path"))
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_markdown(result), encoding="utf-8")
    return str(target)


__all__ = ["ensure_tables", "load_strategy_config", "refresh_ohlcv", "render_markdown", "tick", "write_report"]
