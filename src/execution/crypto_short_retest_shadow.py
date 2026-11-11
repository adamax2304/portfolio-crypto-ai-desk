"""Isolated Shadow strategy for short continuation after a failed support retest.

The strategy observes a fresh downside break, waits for a bounded retest of the
broken level, then enters only after a rejection candle is confirmed by the
next closed candle. It owns its SQLite tables and never writes Paper, signal,
Telegram-entry, MEXC, or live-routing state.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import median
from typing import Any

import pandas as pd

from src.config import load_config
from src.execution import crypto_derivreset_v3_shadow as market_data
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


ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "config" / "shadow_crypto_short_retest.yaml"
CONFIG_KEY = "crypto_short_retest"

DEFAULTS: dict[str, Any] = {
    "feature_flag": False,
    "strategy_id": "crypto_short_retest_v1",
    "shadow_lane": "shadow_crypto_short_retest",
    "source_timeframe": "5m",
    "primary_exchange": "bybit",
    "max_symbols": 40,
    "max_source_bar_age_seconds": 480,
    "max_source_bar_age_seconds_by_mode": {},
    "profiles": {},
    "context": {
        "derivative_freshness_minutes": 15,
        "min_strict_derivative_venues": 2,
        "crowded_short_funding_8h": -0.001,
        "crowded_short_oi_growth_pct": 8.0,
        "max_spread_bps": 35.0,
        "min_quote_volume_usd": 2_000_000,
        "btc_violent_rebound_pct_1h": 1.0,
        "eth_violent_rebound_pct_1h": 0.8,
        "positive_fast_catalyst_hours": 6,
        "weak_session_size_weight": 0.5,
        "weak_sessions": ["asia", "off"],
    },
    "fee_profile": "bybit_non_vip_usdt_perp",
    "funding_exchange": "bybit",
    "funding_intervals": 1.0,
    "min_clean_closed": 30,
    "min_forward_days": 28,
    "min_profit_factor": 1.25,
    "max_review_drawdown_usd": 250.0,
    "report_path": "reports/CRYPTO_SHORT_RETEST_SHADOW.md",
}

EVENT_COLUMNS = (
    "event_id", "strategy_id", "profile_id", "shadow_lane", "symbol", "trade_mode",
    "timeframe_minutes", "breakdown_at", "observed_at", "expires_at", "level",
    "breakdown_low", "atr", "break_rvol", "status", "last_reason",
    "seed_features_json", "last_features_json", "last_checked_at",
)
OUTCOME_COLUMNS = (
    "candidate_id", "event_id", "strategy_id", "profile_id", "shadow_lane", "window",
    "generated_at", "decision_at", "symbol", "direction", "trade_mode",
    "timeframe_minutes", "session_bucket", "market_regime", "catalyst_state",
    "derivatives_state", "evidence_cohort", "size_weight", "eligibility_status",
    "rejection_reason", "data_status", "is_clean_for_edge", "breakdown_at",
    "retest_at", "rejection_at", "entry_ts", "entry_price", "stop_price",
    "tp1", "tp2", "tp3", "outcome_status", "close_reason", "exit_price",
    "exit_ts", "gross_pnl_usd", "net_pnl_usd", "net_r", "fees_usd",
    "slippage_usd", "funding_usd", "funding_source", "funding_estimated",
    "funding_event_count", "risk_usd", "mfe_r", "mae_r", "protection_armed",
    "lock_armed", "highest_tp_touched", "bars_held", "latency_seconds",
    "features_json", "notes_json", "last_checked_at",
)

EVENT_DDL = """
CREATE TABLE IF NOT EXISTS crypto_short_retest_shadow_events (
  event_id TEXT PRIMARY KEY, strategy_id TEXT NOT NULL, profile_id TEXT NOT NULL,
  shadow_lane TEXT NOT NULL, symbol TEXT NOT NULL, trade_mode TEXT NOT NULL,
  timeframe_minutes INTEGER NOT NULL, breakdown_at TEXT NOT NULL, observed_at TEXT NOT NULL,
  expires_at TEXT NOT NULL, level REAL NOT NULL, breakdown_low REAL NOT NULL, atr REAL NOT NULL,
  break_rvol REAL, status TEXT NOT NULL, last_reason TEXT, seed_features_json TEXT NOT NULL,
  last_features_json TEXT, last_checked_at TEXT NOT NULL
)
"""
OUTCOME_DDL = """
CREATE TABLE IF NOT EXISTS crypto_short_retest_shadow_outcomes (
  candidate_id TEXT PRIMARY KEY, event_id TEXT NOT NULL, strategy_id TEXT NOT NULL,
  profile_id TEXT NOT NULL, shadow_lane TEXT NOT NULL, window TEXT NOT NULL,
  generated_at TEXT NOT NULL, decision_at TEXT NOT NULL, symbol TEXT NOT NULL,
  direction TEXT NOT NULL, trade_mode TEXT NOT NULL, timeframe_minutes INTEGER NOT NULL,
  session_bucket TEXT, market_regime TEXT, catalyst_state TEXT, derivatives_state TEXT,
  evidence_cohort TEXT NOT NULL, size_weight REAL NOT NULL, eligibility_status TEXT NOT NULL,
  rejection_reason TEXT, data_status TEXT NOT NULL, is_clean_for_edge INTEGER NOT NULL DEFAULT 0,
  breakdown_at TEXT, retest_at TEXT, rejection_at TEXT, entry_ts TEXT, entry_price REAL,
  stop_price REAL, tp1 REAL, tp2 REAL, tp3 REAL, outcome_status TEXT, close_reason TEXT,
  exit_price REAL, exit_ts TEXT, gross_pnl_usd REAL, net_pnl_usd REAL, net_r REAL,
  fees_usd REAL, slippage_usd REAL, funding_usd REAL, funding_source TEXT,
  funding_estimated INTEGER, funding_event_count INTEGER, risk_usd REAL, mfe_r REAL,
  mae_r REAL, protection_armed INTEGER, lock_armed INTEGER, highest_tp_touched INTEGER,
  bars_held INTEGER, latency_seconds REAL, features_json TEXT, notes_json TEXT,
  last_checked_at TEXT
)
"""
EVAL_DDL = """
CREATE TABLE IF NOT EXISTS crypto_short_retest_shadow_evaluations (
  generated_at TEXT PRIMARY KEY, strategy_id TEXT NOT NULL, activated_at TEXT NOT NULL,
  forward_rows INTEGER, clean_rows INTEGER, dirty_rows INTEGER, clean_closed INTEGER,
  net_pnl_usd REAL, net_r REAL, fees_usd REAL, slippage_usd REAL, funding_usd REAL,
  profit_factor REAL, winrate REAL, max_drawdown_usd REAL, forward_days REAL,
  verdict TEXT, rejection_counts_json TEXT, diagnostics_json TEXT, config_json TEXT
)
"""
META_DDL = """
CREATE TABLE IF NOT EXISTS crypto_short_retest_shadow_meta (
  k TEXT PRIMARY KEY, v TEXT NOT NULL
)
"""

REJECTION_REASONS = {
    "SOURCE_BARS_MISSING", "SOURCE_BARS_STALE", "BREAK_NOT_CONFIRMED",
    "BREAK_TOO_EXTENDED", "BREAK_VOLUME_TOO_WEAK", "RETEST_WINDOW_EXPIRED",
    "RETEST_NOT_REACHED", "LEVEL_RECLAIMED", "REJECTION_NOT_CONFIRMED",
    "RETEST_BUY_VOLUME_TOO_STRONG", "CONFIRM_VOLUME_TOO_WEAK", "ENTRY_TOO_EXTENDED",
    "STOP_TOO_WIDE", "INVALID_GEOMETRY", "NO_ROOM_TO_SUPPORT",
    "CROWDED_SHORT", "BTC_ETH_VIOLENT_REBOUND", "POSITIVE_FAST_CATALYST",
    "ONCHAIN_HARD_RISK", "SPREAD_TOO_WIDE", "LIQUIDITY_TOO_LOW",
}


def load_strategy_config() -> dict[str, Any]:
    return load_yaml_block(CONFIG_PATH, CONFIG_KEY, DEFAULTS)


def _source_bar_age_limit(cfg: dict[str, Any], trade_mode: str) -> float:
    """Return the configured source freshness allowance for this trade horizon."""
    by_mode = cfg.get("max_source_bar_age_seconds_by_mode") or {}
    return float(by_mode.get(str(trade_mode).lower(), cfg["max_source_bar_age_seconds"]))


def ensure_tables(conn: sqlite3.Connection) -> None:
    conn.execute(EVENT_DDL)
    conn.execute(OUTCOME_DDL)
    conn.execute(EVAL_DDL)
    conn.execute(META_DDL)
    event_integer = {"timeframe_minutes"}
    event_real = {"level", "breakdown_low", "atr", "break_rvol"}
    ensure_columns(conn, "crypto_short_retest_shadow_events", {
        col: ("INTEGER" if col in event_integer else "REAL" if col in event_real else "TEXT")
        for col in EVENT_COLUMNS if col != "event_id"
    })
    ensure_columns(conn, "crypto_short_retest_shadow_outcomes", {
        col: ("INTEGER" if col in {
            "timeframe_minutes", "is_clean_for_edge", "funding_estimated",
            "funding_event_count", "protection_armed", "lock_armed",
            "highest_tp_touched", "bars_held",
        } else "TEXT" if col in {
            "event_id", "strategy_id", "profile_id", "shadow_lane", "window",
            "generated_at", "decision_at", "symbol", "direction", "trade_mode",
            "session_bucket", "market_regime", "catalyst_state", "derivatives_state",
            "evidence_cohort", "eligibility_status", "rejection_reason", "data_status",
            "breakdown_at", "retest_at", "rejection_at", "entry_ts", "outcome_status",
            "close_reason", "exit_ts", "funding_source", "features_json", "notes_json",
            "last_checked_at",
        } else "REAL")
        for col in OUTCOME_COLUMNS if col != "candidate_id"
    })
    conn.execute("CREATE INDEX IF NOT EXISTS idx_short_retest_pending ON "
                 "crypto_short_retest_shadow_events(status,profile_id,breakdown_at)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_short_retest_open ON "
                 "crypto_short_retest_shadow_outcomes(outcome_status,entry_ts)")


def _f(value: Any) -> float | None:
    try:
        return None if value in (None, "") else float(value)
    except (TypeError, ValueError):
        return None


def _canonical(symbol: str) -> str:
    value = str(symbol or "").upper().split(":", 1)[0]
    base = value.split("/", 1)[0].replace("USDT", "").replace("USD", "")
    return f"{base}/USDT" if base else value


def _normalized(symbol: str) -> str:
    return _canonical(symbol).replace("/", "")


def _base(symbol: str) -> str:
    return _canonical(symbol).split("/", 1)[0]


def _session(ts: datetime) -> str:
    hour = ts.astimezone(timezone.utc).hour
    if hour <= 6:
        return "asia"
    if hour <= 12:
        return "europe"
    if hour <= 20:
        return "us"
    return "off"


def _event_id(cfg: dict[str, Any], profile_id: str, symbol: str, breakdown_at: datetime) -> str:
    raw = f"{cfg['strategy_id']}|{profile_id}|{_canonical(symbol)}|{breakdown_at.isoformat()}"
    return "csr_e_" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:20]


def _candidate_id(event_id: str) -> str:
    return "csr_o_" + hashlib.sha256(event_id.encode("utf-8")).hexdigest()[:20]


def _atr(frame: pd.DataFrame, idx: int, periods: int = 14) -> float | None:
    start = max(1, idx - periods + 1)
    values: list[float] = []
    for pos in range(start, idx + 1):
        row, prev = frame.iloc[pos], frame.iloc[pos - 1]
        high, low, previous = float(row["high"]), float(row["low"]), float(prev["close"])
        values.append(max(high - low, abs(high - previous), abs(low - previous)))
    return sum(values) / len(values) if values else None


def _resample_source(frame: pd.DataFrame, minutes: int, *, now: datetime) -> pd.DataFrame:
    source = normalize_frame(frame)
    if source.empty:
        return source
    source = source[source["timestamp"] + pd.Timedelta(minutes=5) <= pd.Timestamp(now)].copy()
    if source.empty:
        return source
    expected = max(1, int(minutes) // 5)
    indexed = source.set_index("timestamp")
    grouped = indexed.resample(f"{int(minutes)}min", origin="epoch", label="left", closed="left")
    out = grouped.agg({
        "open": "first", "high": "max", "low": "min", "close": "last",
        "volume": "sum",
    })
    counts = grouped["close"].count()
    out = out[counts >= expected].dropna().reset_index()
    return normalize_frame(out)


def _source_frame(symbol: str, cfg: dict[str, Any]) -> tuple[pd.DataFrame, str | None]:
    source_cfg = market_data.load_strategy_config()
    source_cfg["timeframe"] = str(cfg.get("source_timeframe") or "5m")
    source_cfg["max_symbols"] = int(cfg.get("max_symbols") or 40)
    return market_data._load_frame(symbol, source_cfg)


def _profile_frame(symbol: str, source_frame: pd.DataFrame,
                   profile: dict[str, Any], cfg: dict[str, Any],
                   *, now: datetime) -> pd.DataFrame:
    """Prefer the existing native 1h cache for swing; otherwise resample 5m."""
    minutes = int(profile["timeframe_minutes"])
    if minutes >= 60 and minutes % 60 == 0:
        native_cfg = market_data.load_strategy_config()
        native_cfg["timeframe"] = f"{minutes // 60}h"
        native_cfg["fallback_timeframes"] = []
        native, _ = market_data._load_frame(symbol, native_cfg)
        native = normalize_frame(native)
        native = native[
            native["timestamp"] + pd.Timedelta(minutes=minutes) <= pd.Timestamp(now)
        ]
        if len(native) >= int(profile["structure_lookback_bars"]) + 1:
            return native.reset_index(drop=True)
    return _resample_source(source_frame, minutes, now=now)


def _symbols(intelligence_conn: sqlite3.Connection, now: datetime, cfg: dict[str, Any]) -> list[str]:
    source_cfg = market_data.load_strategy_config()
    source_cfg["max_symbols"] = int(cfg.get("max_symbols") or 40)
    source_cfg["derivative_freshness_minutes"] = float(
        (cfg.get("context") or {}).get("derivative_freshness_minutes", 15)
    )
    return market_data._symbols(intelligence_conn, now, source_cfg)


def detect_breakdown(frame: pd.DataFrame, idx: int, profile: dict[str, Any]) -> dict[str, Any]:
    lookback = int(profile["structure_lookback_bars"])
    if idx < lookback:
        return {"ok": False, "reason": "SOURCE_BARS_MISSING"}
    atr = _atr(frame, idx - 1)
    if atr is None or atr <= 0:
        return {"ok": False, "reason": "SOURCE_BARS_MISSING"}
    history = frame.iloc[idx - lookback:idx]
    bar = frame.iloc[idx]
    level = float(history["low"].min())
    close = float(bar["close"])
    distance = (level - close) / atr
    if distance < float(profile["min_break_distance_atr"]):
        return {"ok": False, "reason": "BREAK_NOT_CONFIRMED", "distance_atr": distance}
    if distance > float(profile["max_break_extension_atr"]):
        return {"ok": False, "reason": "BREAK_TOO_EXTENDED", "distance_atr": distance}
    mean_volume = float(history["volume"].tail(20).mean()) if "volume" in history else 0.0
    rvol = float(bar.get("volume") or 0.0) / mean_volume if mean_volume > 0 else None
    if rvol is not None and rvol < float(profile["min_break_rvol"]):
        return {"ok": False, "reason": "BREAK_VOLUME_TOO_WEAK", "break_rvol": rvol}
    minutes = int(profile["timeframe_minutes"])
    breakdown_at = pd.Timestamp(bar["timestamp"]).to_pydatetime() + timedelta(minutes=minutes)
    return {
        "ok": True, "level": level, "breakdown_low": float(bar["low"]), "atr": atr,
        "break_rvol": rvol, "breakdown_at": breakdown_at, "distance_atr": distance,
    }


def confirm_retest(frame: pd.DataFrame, event: dict[str, Any],
                   profile: dict[str, Any], *, now: datetime) -> dict[str, Any]:
    minutes = int(profile["timeframe_minutes"])
    breakdown_at = parse_dt(event.get("breakdown_at"))
    if breakdown_at is None:
        return {"ok": False, "reason": "SOURCE_BARS_MISSING"}
    bars = normalize_frame(frame)
    bars = bars[
        (bars["timestamp"] + pd.Timedelta(minutes=minutes) > pd.Timestamp(breakdown_at))
        & (bars["timestamp"] + pd.Timedelta(minutes=minutes) <= pd.Timestamp(now))
    ].head(int(profile["retest_window_bars"]) + 1).reset_index(drop=True)
    if len(bars) < 2:
        return {"ok": False, "reason": "RETEST_NOT_REACHED"}
    level, atr = float(event["level"]), float(event["atr"])
    retest_limit = level - float(profile["retest_proximity_atr"]) * atr
    max_acceptance = level + float(profile["max_retest_acceptance_atr"]) * atr
    hard_reclaim = level + float(
        profile.get("hard_reclaim_atr", profile["max_retest_acceptance_atr"])
    ) * atr
    rejection_close = level - float(profile["rejection_close_below_atr"]) * atr
    for idx in range(len(bars) - 1):
        retest = bars.iloc[idx]
        if float(retest["high"]) < retest_limit:
            continue
        if float(retest["close"]) > hard_reclaim:
            return {"ok": False, "reason": "LEVEL_RECLAIMED",
                    "retest_at": (pd.Timestamp(retest["timestamp"]).to_pydatetime()
                                  + timedelta(minutes=minutes)).isoformat()}
        if (
            float(retest["close"]) > max_acceptance
            and float(bars.iloc[idx + 1]["close"]) > max_acceptance
        ):
            return {"ok": False, "reason": "LEVEL_RECLAIMED",
                    "retest_at": (pd.Timestamp(retest["timestamp"]).to_pydatetime()
                                  + timedelta(minutes=minutes)).isoformat()}
        candle_range = max(float(retest["high"]) - float(retest["low"]), 1e-12)
        upper_wick_share = (float(retest["high"]) - max(float(retest["open"]), float(retest["close"]))) / candle_range
        bearish_rejection = float(retest["close"]) < float(retest["open"]) or upper_wick_share >= 0.20
        if float(retest["close"]) > rejection_close or not bearish_rejection:
            continue
        confirm = bars.iloc[idx + 1]
        reference = (
            float(retest["close"])
            if str(profile.get("confirmation_reference") or "low").lower() == "close"
            else float(retest["low"])
        )
        required_close = reference - float(profile["confirmation_below_rejection_atr"]) * atr
        if float(confirm["close"]) >= required_close:
            continue
        extension = (level - float(confirm["close"])) / atr
        if extension > float(profile["max_entry_extension_atr"]):
            return {"ok": False, "reason": "ENTRY_TOO_EXTENDED", "entry_extension_atr": extension}
        pre = frame[
            frame["timestamp"] + pd.Timedelta(minutes=minutes)
            < pd.Timestamp(event["breakdown_at"])
        ].tail(20)
        mean_volume = float(pre["volume"].mean()) if not pre.empty else 0.0
        confirm_rvol = float(confirm.get("volume") or 0.0) / mean_volume if mean_volume > 0 else None
        if confirm_rvol is not None and confirm_rvol < float(profile["min_confirm_rvol"]):
            return {"ok": False, "reason": "CONFIRM_VOLUME_TOO_WEAK", "confirm_rvol": confirm_rvol}
        break_volume = _f((json.loads(event.get("seed_features_json") or "{}")).get("break_volume"))
        if break_volume and float(retest.get("volume") or 0.0) > break_volume * float(
            profile["max_retest_vs_break_volume"]
        ):
            return {"ok": False, "reason": "RETEST_BUY_VOLUME_TOO_STRONG"}
        entry = float(confirm["close"])
        stop = max(float(retest["high"]), level + float(profile["max_retest_acceptance_atr"]) * atr)
        stop += float(profile["stop_buffer_atr"]) * atr
        risk = stop - entry
        if risk <= 0:
            return {"ok": False, "reason": "INVALID_GEOMETRY"}
        if risk / atr > float(profile["max_stop_atr"]) or risk / entry * 100 > float(profile["max_stop_pct"]):
            return {"ok": False, "reason": "STOP_TOO_WIDE", "stop_atr": risk / atr}
        prior_supports = [
            float(value) for value in pre["low"].tolist()
            if float(value) < entry - 0.10 * atr
        ]
        nearest_support = max(prior_supports) if prior_supports else None
        room_r = (entry - nearest_support) / risk if nearest_support is not None else float("inf")
        if room_r < float(profile["min_room_to_support_r"]):
            return {"ok": False, "reason": "NO_ROOM_TO_SUPPORT", "room_r": room_r}
        targets = [entry - risk * float(value) for value in profile["target_r"]]
        retest_at = pd.Timestamp(retest["timestamp"]).to_pydatetime() + timedelta(minutes=minutes)
        decision_at = pd.Timestamp(confirm["timestamp"]).to_pydatetime() + timedelta(minutes=minutes)
        return {
            "ok": True, "entry": entry, "stop": stop, "targets": targets,
            "retest_at": retest_at, "rejection_at": retest_at, "decision_at": decision_at,
            "entry_extension_atr": extension, "stop_atr": risk / atr,
            "room_r": room_r, "nearest_support": nearest_support,
            "confirm_rvol": confirm_rvol, "upper_wick_share": upper_wick_share,
        }
    return {"ok": False, "reason": "REJECTION_NOT_CONFIRMED"}


def _raw(row: dict[str, Any]) -> dict[str, Any]:
    try:
        value = json.loads(row.get("raw_json") or "{}")
        return value if isinstance(value, dict) else {}
    except (TypeError, ValueError):
        return {}


def _derivatives_context(conn: sqlite3.Connection, symbol: str, as_of: datetime,
                         cfg: dict[str, Any], structure: dict[str, Any]) -> dict[str, Any]:
    context = cfg["context"]
    rows = [dict(row) for row in conn.execute(
        "SELECT * FROM derivative_snapshots WHERE normalized_symbol=? AND provider_ts>=? "
        "AND provider_ts<=? AND (received_at IS NULL OR received_at<=?) ORDER BY provider_ts,id",
        (_normalized(symbol), (as_of - timedelta(hours=2)).isoformat(),
         as_of.isoformat(), as_of.isoformat()),
    ).fetchall()]
    fresh_after = as_of - timedelta(minutes=float(context["derivative_freshness_minutes"]))
    latest: dict[str, dict[str, Any]] = {}
    history: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        at = parse_dt(row.get("provider_ts"))
        if at is None:
            continue
        exchange = str(row.get("exchange") or "unknown").lower()
        history.setdefault(exchange, []).append(row)
        if at >= fresh_after:
            latest[exchange] = row
    funding = [_f(row.get("funding_rate_8h")) for row in latest.values()]
    funding = [value for value in funding if value is not None]
    oi_changes: list[float] = []
    for exchange, last in latest.items():
        series = history.get(exchange) or []
        current_oi = _f(last.get("oi_usd"))
        first_oi = next((_f(item.get("oi_usd")) for item in series if _f(item.get("oi_usd"))), None)
        if current_oi and first_oi:
            oi_changes.append((current_oi - first_oi) / first_oi * 100.0)
    funding_median = median(funding) if funding else None
    oi_growth = median(oi_changes) if oi_changes else None
    crowded = bool(
        funding_median is not None
        and funding_median <= float(context["crowded_short_funding_8h"])
    ) or bool(
        oi_growth is not None
        and oi_growth >= float(context["crowded_short_oi_growth_pct"])
        and float(structure.get("entry_extension_atr") or 0.0) < 0.20
    )
    spreads, quote_volumes = [], []
    for row in latest.values():
        raw = _raw(row)
        bid = _f(raw.get("bid1Price") or raw.get("bidPrice") or raw.get("bid"))
        ask = _f(raw.get("ask1Price") or raw.get("askPrice") or raw.get("ask"))
        if bid and ask and ask > bid:
            spreads.append((ask - bid) / ((ask + bid) / 2.0) * 10_000)
        quote = _f(raw.get("turnover24h") or raw.get("quoteVolume") or raw.get("amount24"))
        if quote is not None:
            quote_volumes.append(quote)
    spread = median(spreads) if spreads else None
    quote_volume = max(quote_volumes) if quote_volumes else None
    strict = (
        len(latest) >= int(context["min_strict_derivative_venues"])
        and funding_median is not None and spread is not None and quote_volume is not None
    )
    state = "crowded_short" if crowded else "supportive" if strict else "unknown"
    return {
        "state": state, "strict": strict, "venues": len(latest),
        "funding_median_8h": funding_median, "oi_growth_pct": oi_growth,
        "spread_bps": spread, "quote_volume_usd": quote_volume,
    }


def _market_state(symbol_frames: dict[str, pd.DataFrame], as_of: datetime,
                  cfg: dict[str, Any]) -> dict[str, Any]:
    returns: dict[str, float | None] = {}
    for symbol in ("BTC/USDT", "ETH/USDT"):
        frame = normalize_frame(symbol_frames.get(symbol))
        frame = frame[
            frame["timestamp"] + pd.Timedelta(minutes=5) <= pd.Timestamp(as_of)
        ].tail(13)
        returns[symbol] = (
            (float(frame["close"].iloc[-1]) / float(frame["close"].iloc[0]) - 1.0) * 100.0
            if len(frame) >= 13 else None
        )
    context = cfg["context"]
    violent = (
        returns["BTC/USDT"] is not None and returns["ETH/USDT"] is not None
        and returns["BTC/USDT"] >= float(context["btc_violent_rebound_pct_1h"])
        and returns["ETH/USDT"] >= float(context["eth_violent_rebound_pct_1h"])
    )
    return {"state": "violent_rebound" if violent else "compatible",
            "btc_return_1h": returns["BTC/USDT"], "eth_return_1h": returns["ETH/USDT"]}


def _positive_fast_catalyst(conn: sqlite3.Connection, symbol: str, as_of: datetime,
                            cfg: dict[str, Any]) -> bool:
    if not table_exists(conn, "news_canonical_events"):
        return False
    cols = {row[1] for row in conn.execute("PRAGMA table_info(news_canonical_events)")}
    required = {"direction_hint", "asset_class", "linkage_allowed", "trusted_symbols_json"}
    if not required.issubset(cols):
        return False
    time_col = "effective_at" if "effective_at" in cols else (
        "published_at" if "published_at" in cols else None
    )
    if time_col is None:
        return False
    rows = conn.execute(
        f"SELECT trusted_symbols_json,direction_hint,{time_col} FROM news_canonical_events "
        "WHERE lower(COALESCE(asset_class,''))='crypto' AND linkage_allowed=1 "
        f"AND {time_col}>=? AND {time_col}<=?",
        ((as_of - timedelta(hours=float(cfg["context"]["positive_fast_catalyst_hours"]))).isoformat(),
         as_of.isoformat()),
    ).fetchall()
    base = _base(symbol)
    for symbols_json, direction, _ in rows:
        try:
            symbols = {_base(value) for value in json.loads(symbols_json or "[]")}
        except (TypeError, ValueError):
            symbols = set()
        if base in symbols and str(direction or "").lower() in {"positive", "bullish", "long"}:
            return True
    return False


def context_rejection(*, derivatives: dict[str, Any], market: dict[str, Any],
                      positive_fast_catalyst: bool, onchain_hard_risk: bool,
                      cfg: dict[str, Any]) -> str | None:
    """Reject only explicit hazards; missing auxiliary context stays exploratory."""
    if derivatives.get("state") == "crowded_short":
        return "CROWDED_SHORT"
    spread = _f(derivatives.get("spread_bps"))
    if spread is not None and spread > float(cfg["context"]["max_spread_bps"]):
        return "SPREAD_TOO_WIDE"
    quote = _f(derivatives.get("quote_volume_usd"))
    if quote is not None and quote < float(cfg["context"]["min_quote_volume_usd"]):
        return "LIQUIDITY_TOO_LOW"
    if market.get("state") == "violent_rebound":
        return "BTC_ETH_VIOLENT_REBOUND"
    if positive_fast_catalyst:
        return "POSITIVE_FAST_CATALYST"
    if onchain_hard_risk:
        return "ONCHAIN_HARD_RISK"
    return None


def _insert(conn: sqlite3.Connection, table: str, columns: tuple[str, ...],
            row: dict[str, Any], *, replace: bool = False) -> None:
    verb = "INSERT OR REPLACE" if replace else "INSERT OR IGNORE"
    conn.execute(
        f"{verb} INTO {table} ({','.join(columns)}) VALUES "
        f"({','.join('?' for _ in columns)})",
        tuple(row.get(column) for column in columns),
    )


def _activation(conn: sqlite3.Connection, now: datetime, persist: bool) -> datetime:
    row = conn.execute(
        "SELECT v FROM crypto_short_retest_shadow_meta WHERE k='activated_at'"
    ).fetchone()
    if row:
        return parse_dt(row[0]) or now
    if persist:
        conn.execute(
            "INSERT INTO crypto_short_retest_shadow_meta(k,v) VALUES('activated_at',?)",
            (now.isoformat(),),
        )
    return now


def _event_row(cfg: dict[str, Any], profile_id: str, profile: dict[str, Any],
               symbol: str, seed: dict[str, Any], observed_at: datetime) -> dict[str, Any]:
    expires = seed["breakdown_at"] + timedelta(
        minutes=int(profile["timeframe_minutes"]) * int(profile["retest_window_bars"])
    )
    return {
        "event_id": _event_id(cfg, profile_id, symbol, seed["breakdown_at"]),
        "strategy_id": cfg["strategy_id"], "profile_id": profile_id,
        "shadow_lane": cfg["shadow_lane"], "symbol": _canonical(symbol),
        "trade_mode": profile["trade_mode"],
        "timeframe_minutes": int(profile["timeframe_minutes"]),
        "breakdown_at": seed["breakdown_at"].isoformat(),
        "observed_at": observed_at.isoformat(), "expires_at": expires.isoformat(),
        "level": seed["level"], "breakdown_low": seed["breakdown_low"],
        "atr": seed["atr"], "break_rvol": seed.get("break_rvol"),
        "status": "pending", "last_reason": None,
        "seed_features_json": json_text({
            **seed, "break_volume": seed.get("break_volume"),
        }),
        "last_features_json": None, "last_checked_at": observed_at.isoformat(),
    }


def _seed_events(conn: sqlite3.Connection, intelligence_conn: sqlite3.Connection,
                 now: datetime, cfg: dict[str, Any],
                 source_frames: dict[str, pd.DataFrame]) -> dict[str, int]:
    counts = {"symbols": 0, "breakdowns": 0, "new_events": 0, "stale_source": 0}
    for symbol in _symbols(intelligence_conn, now, cfg):
        counts["symbols"] += 1
        source = source_frames.get(symbol)
        if source is None or source.empty:
            continue
        latest_close = pd.Timestamp(source["timestamp"].iloc[-1]).to_pydatetime() + timedelta(minutes=5)
        source_age_seconds = (now - latest_close).total_seconds()
        eligible_profile_found = False
        for profile_id, profile in cfg["profiles"].items():
            if not bool(profile.get("enabled", True)):
                continue
            if source_age_seconds > _source_bar_age_limit(cfg, str(profile.get("trade_mode") or "")):
                continue
            eligible_profile_found = True
            frame = _profile_frame(symbol, source, profile, cfg, now=now)
            if frame.empty:
                continue
            seed = detect_breakdown(frame, len(frame) - 1, profile)
            if not seed.get("ok"):
                continue
            counts["breakdowns"] += 1
            seed["break_volume"] = float(frame.iloc[-1].get("volume") or 0.0)
            event = _event_row(cfg, profile_id, profile, symbol, seed, now)
            if conn.execute(
                "SELECT 1 FROM crypto_short_retest_shadow_events WHERE event_id=?",
                (event["event_id"],),
            ).fetchone():
                continue
            active = conn.execute(
                "SELECT 1 FROM crypto_short_retest_shadow_events "
                "WHERE profile_id=? AND symbol=? AND status IN ('pending','entered')",
                (profile_id, _canonical(symbol)),
            ).fetchone()
            if active:
                continue
            _insert(conn, "crypto_short_retest_shadow_events", EVENT_COLUMNS, event)
            counts["new_events"] += 1
        if not eligible_profile_found:
            counts["stale_source"] += 1
    return counts


def _reject_outcome(cfg: dict[str, Any], event: dict[str, Any], now: datetime,
                    reason: str, features: dict[str, Any]) -> dict[str, Any]:
    if reason not in REJECTION_REASONS:
        raise ValueError(f"unregistered short-retest rejection: {reason}")
    dirty = reason in {"SOURCE_BARS_MISSING", "SOURCE_BARS_STALE"}
    return {
        "candidate_id": _candidate_id(event["event_id"]), "event_id": event["event_id"],
        "strategy_id": cfg["strategy_id"], "profile_id": event["profile_id"],
        "shadow_lane": cfg["shadow_lane"], "window": "forward_post_activation",
        "generated_at": event["observed_at"], "decision_at": now.isoformat(),
        "symbol": event["symbol"], "direction": "short", "trade_mode": event["trade_mode"],
        "timeframe_minutes": event["timeframe_minutes"], "session_bucket": _session(now),
        "market_regime": "unknown", "catalyst_state": "unknown",
        "derivatives_state": "unknown", "evidence_cohort": "exploratory_v1",
        "size_weight": 0.5, "eligibility_status": "rejected", "rejection_reason": reason,
        "data_status": "dirty" if dirty else "clean_rejection", "is_clean_for_edge": 0,
        "breakdown_at": event["breakdown_at"], "outcome_status": "skipped",
        "close_reason": reason.lower(), "latency_seconds": None,
        "features_json": json_text(features), "notes_json": json_text({
            "shadow_only": True, "paper_untouched": True, "live_locked": True,
        }),
        "last_checked_at": now.isoformat(),
    }


def _update_event(conn: sqlite3.Connection, event_id: str, *, status: str,
                  reason: str | None, features: dict[str, Any], now: datetime) -> None:
    conn.execute(
        "UPDATE crypto_short_retest_shadow_events SET status=?,last_reason=?,"
        "last_features_json=?,last_checked_at=? WHERE event_id=?",
        (status, reason, json_text(features), now.isoformat(), event_id),
    )


def _process_events(conn: sqlite3.Connection, intelligence_conn: sqlite3.Connection,
                    now: datetime, cfg: dict[str, Any],
                    source_frames: dict[str, pd.DataFrame]) -> list[dict[str, Any]]:
    outcomes: list[dict[str, Any]] = []
    market_frames: dict[str, pd.DataFrame] = {}
    for market_symbol in ("BTC/USDT", "ETH/USDT"):
        market_frame = source_frames.get(market_symbol)
        if market_frame is None or market_frame.empty:
            market_frame = _source_frame(market_symbol, cfg)[0]
        market_frames[market_symbol] = market_frame
    for event in [
        dict(row) for row in conn.execute(
            "SELECT * FROM crypto_short_retest_shadow_events "
            "WHERE status='pending' ORDER BY breakdown_at"
        ).fetchall()
    ]:
        profile = cfg["profiles"].get(event["profile_id"])
        if not profile:
            continue
        source = source_frames.get(event["symbol"])
        if source is None or source.empty:
            expires_at = parse_dt(event["expires_at"]) or now
            if now >= expires_at:
                row = _reject_outcome(
                    cfg, event, now, "SOURCE_BARS_MISSING", {"source": "missing"}
                )
                outcomes.append(row)
                _update_event(
                    conn, event["event_id"], status="expired",
                    reason="SOURCE_BARS_MISSING", features={}, now=now,
                )
            else:
                _update_event(conn, event["event_id"], status="pending",
                              reason="SOURCE_BARS_MISSING", features={}, now=now)
            continue
        source_close = (
            pd.Timestamp(source["timestamp"].iloc[-1]).to_pydatetime()
            + timedelta(minutes=5)
        )
        source_age_seconds = (now - source_close).total_seconds()
        source_age_limit = _source_bar_age_limit(cfg, str(event.get("trade_mode") or ""))
        if source_age_seconds > source_age_limit:
            freshness = {
                "source_close": source_close.isoformat(),
                "source_age_seconds": source_age_seconds,
                "source_age_limit_seconds": source_age_limit,
            }
            expires_at = parse_dt(event["expires_at"]) or now
            if now >= expires_at:
                row = _reject_outcome(
                    cfg, event, now, "SOURCE_BARS_STALE",
                    freshness,
                )
                outcomes.append(row)
                _update_event(
                    conn, event["event_id"], status="expired",
                    reason="SOURCE_BARS_STALE",
                    features=freshness, now=now,
                )
            else:
                _update_event(
                    conn, event["event_id"], status="pending",
                    reason="SOURCE_BARS_STALE",
                    features=freshness, now=now,
                )
            continue
        frame = _profile_frame(event["symbol"], source, profile, cfg, now=now)
        structure = confirm_retest(frame, event, profile, now=now)
        expires_at = parse_dt(event["expires_at"]) or now
        if not structure.get("ok"):
            reason = str(structure["reason"])
            terminal = reason in {
                "LEVEL_RECLAIMED", "ENTRY_TOO_EXTENDED", "RETEST_BUY_VOLUME_TOO_STRONG",
                "CONFIRM_VOLUME_TOO_WEAK", "STOP_TOO_WIDE", "INVALID_GEOMETRY",
                "NO_ROOM_TO_SUPPORT",
            } or now >= expires_at
            if terminal:
                if now >= expires_at and reason in {"RETEST_NOT_REACHED", "REJECTION_NOT_CONFIRMED"}:
                    reason = "RETEST_WINDOW_EXPIRED"
                row = _reject_outcome(cfg, event, now, reason, {"structure": structure})
                outcomes.append(row)
                _update_event(conn, event["event_id"], status="expired", reason=reason,
                              features={"structure": structure}, now=now)
            else:
                _update_event(conn, event["event_id"], status="pending", reason=reason,
                              features={"structure": structure}, now=now)
            continue
        decision_at = structure["decision_at"]
        derivatives = _derivatives_context(
            intelligence_conn, event["symbol"], decision_at, cfg, structure
        )
        market = _market_state(market_frames, decision_at, cfg)
        catalyst = market_data._catalyst_state(
            conn, event["symbol"], decision_at,
            {**market_data.load_strategy_config(),
             "catalyst_freshness_hours": cfg["context"]["positive_fast_catalyst_hours"]},
        )
        hard_reason = context_rejection(
            derivatives=derivatives, market=market,
            positive_fast_catalyst=_positive_fast_catalyst(
                conn, event["symbol"], decision_at, cfg
            ),
            onchain_hard_risk=market_data._hard_onchain_risk(
                intelligence_conn, event["symbol"], decision_at
            ),
            cfg=cfg,
        )
        features = {
            "structure": structure, "derivatives": derivatives,
            "market": market, "catalyst_state": catalyst,
        }
        if hard_reason:
            row = _reject_outcome(cfg, event, now, hard_reason, features)
            outcomes.append(row)
            _update_event(conn, event["event_id"], status="rejected", reason=hard_reason,
                          features=features, now=now)
            continue
        strict = bool(derivatives["strict"])
        cohort = "strict_v1" if strict else "exploratory_v1"
        session = _session(decision_at)
        size = (
            float(cfg["context"]["weak_session_size_weight"])
            if session in set(cfg["context"]["weak_sessions"]) else 1.0
        )
        entry, stop = float(structure["entry"]), float(structure["stop"])
        targets = structure["targets"]
        row = {
            "candidate_id": _candidate_id(event["event_id"]), "event_id": event["event_id"],
            "strategy_id": cfg["strategy_id"], "profile_id": event["profile_id"],
            "shadow_lane": cfg["shadow_lane"], "window": "forward_post_activation",
            "generated_at": event["observed_at"], "decision_at": decision_at.isoformat(),
            "symbol": event["symbol"], "direction": "short", "trade_mode": event["trade_mode"],
            "timeframe_minutes": event["timeframe_minutes"], "session_bucket": session,
            "market_regime": market["state"], "catalyst_state": catalyst,
            "derivatives_state": derivatives["state"], "evidence_cohort": cohort,
            "size_weight": size, "eligibility_status": "eligible", "rejection_reason": None,
            "data_status": "clean" if strict else "aux_context_incomplete",
            "is_clean_for_edge": int(strict), "breakdown_at": event["breakdown_at"],
            "retest_at": structure["retest_at"].isoformat(),
            "rejection_at": structure["rejection_at"].isoformat(),
            "entry_ts": decision_at.isoformat(), "entry_price": entry, "stop_price": stop,
            "tp1": targets[0], "tp2": targets[1], "tp3": targets[2],
            "outcome_status": "open", "close_reason": "awaiting_future_bars",
            "latency_seconds": max(0.0, (now - decision_at).total_seconds()),
            "features_json": json_text(features), "notes_json": json_text({
                "shadow_only": True, "paper_untouched": True, "live_locked": True,
                "missing_aux_context_never_counts_as_clean": True,
            }), "last_checked_at": now.isoformat(),
        }
        outcomes.append(row)
        _update_event(conn, event["event_id"], status="entered", reason=None,
                      features=features, now=now)
    return outcomes


def _funding_events(intelligence_conn: sqlite3.Connection, symbol: str,
                    entry_at: datetime, now: datetime, cfg: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        dict(row) for row in intelligence_conn.execute(
            "SELECT event_at,received_at,funding_rate,funding_rate_8h FROM funding_rate_events "
            "WHERE lower(exchange)=lower(?) AND normalized_symbol=? AND event_at>? AND event_at<=? "
            "AND (received_at IS NULL OR received_at<=?) ORDER BY event_at,id",
            (cfg["funding_exchange"], _normalized(symbol), entry_at.isoformat(),
             now.isoformat(), now.isoformat()),
        ).fetchall()
    ]


def _mature(conn: sqlite3.Connection, intelligence_conn: sqlite3.Connection,
            now: datetime, cfg: dict[str, Any],
            source_frames: dict[str, pd.DataFrame]) -> int:
    closed = 0
    rows = [
        dict(row) for row in conn.execute(
            "SELECT * FROM crypto_short_retest_shadow_outcomes WHERE outcome_status='open'"
        ).fetchall()
    ]
    for row in rows:
        profile = cfg["profiles"].get(row["profile_id"])
        entry_at = parse_dt(row.get("entry_ts"))
        source = source_frames.get(row["symbol"])
        if not profile or entry_at is None or source is None or source.empty:
            continue
        frame = _profile_frame(row["symbol"], source, profile, cfg, now=now)
        future = frame[
            (frame["timestamp"] + pd.Timedelta(minutes=int(profile["timeframe_minutes"]))
             > pd.Timestamp(entry_at))
            & (frame["timestamp"] + pd.Timedelta(minutes=int(profile["timeframe_minutes"]))
               <= pd.Timestamp(now))
        ]
        max_holding_bars = int(profile["max_holding_bars"])
        reached_time_stop = len(future) >= max_holding_bars
        future = future.head(max_holding_bars)
        features = json.loads(row.get("features_json") or "{}")
        funding_rate = ((features.get("derivatives") or {}).get("funding_median_8h"))
        sim = simulate_confirmed_close_entry(
            direction="short", entry=float(row["entry_price"]), stop=float(row["stop_price"]),
            tp1=float(row["tp1"]), tp2=float(row["tp2"]), tp3=float(row["tp3"]),
            future_candles=future, symbol=row["symbol"], fee_profile=cfg["fee_profile"],
            funding_rate_8h=_f(funding_rate), funding_intervals=float(cfg["funding_intervals"]),
            funding_events=_funding_events(intelligence_conn, row["symbol"], entry_at, now, cfg),
            entry_at=entry_at, bar_minutes=int(profile["timeframe_minutes"]),
            force_close=reached_time_stop,
        ).to_dict()
        updates = {
            ("outcome_status" if key == "status" else key): value
            for key, value in sim.items()
        }
        updates["last_checked_at"] = now.isoformat()
        if updates.get("net_pnl_usd") is not None:
            for key in (
                "gross_pnl_usd", "net_pnl_usd", "fees_usd", "slippage_usd",
                "funding_usd", "risk_usd",
            ):
                if updates.get(key) is not None:
                    updates[key] = round(
                        float(updates[key]) * float(row.get("size_weight") or 1.0), 4
                    )
        allowed = [
            key for key in updates if key in OUTCOME_COLUMNS and key != "candidate_id"
        ]
        conn.execute(
            "UPDATE crypto_short_retest_shadow_outcomes SET "
            + ",".join(f"{key}=?" for key in allowed)
            + " WHERE candidate_id=? AND outcome_status='open'",
            tuple(updates[key] for key in allowed) + (row["candidate_id"],),
        )
        if updates.get("outcome_status") == "closed":
            conn.execute(
                "UPDATE crypto_short_retest_shadow_events SET status='closed',"
                "last_checked_at=? WHERE event_id=? AND status='entered'",
                (now.isoformat(), row["event_id"]),
            )
            closed += 1
    return closed


def _summary_rows(rows: list[dict[str, Any]], activated_at: str,
                  now: datetime, cfg: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    strict_rows = [row for row in rows if row.get("evidence_cohort") == "strict_v1"]
    strict = clean_forward_summary(
        strict_rows, activated_at=activated_at, now=now,
        min_closed=int(cfg["min_clean_closed"]), min_days=float(cfg["min_forward_days"]),
        min_pf=float(cfg["min_profit_factor"]),
        max_review_drawdown_usd=float(cfg["max_review_drawdown_usd"]),
    )
    all_rows = clean_forward_summary(
        rows, activated_at=activated_at, now=now,
        min_closed=int(cfg["min_clean_closed"]), min_days=float(cfg["min_forward_days"]),
        min_pf=float(cfg["min_profit_factor"]),
        max_review_drawdown_usd=float(cfg["max_review_drawdown_usd"]),
    )
    all_rows["verdict"] = strict["verdict"]
    all_rows["official_evidence_cohort"] = "strict_v1"
    return all_rows, strict


def tick(*, db: str | None = None, persist: bool = True,
         now: datetime | None = None, cfg: dict[str, Any] | None = None,
         source_frames: dict[str, pd.DataFrame] | None = None) -> dict[str, Any]:
    cfg, now = cfg or load_strategy_config(), now or utc_now()
    if not bool(cfg.get("feature_flag")):
        return {"enabled": False, "generated_at": now.isoformat(), "summary": {}}
    path = Path(db) if db else Path(load_config().db_path)
    conn = sqlite3.connect(path if persist or path.exists() else ":memory:", timeout=10.0)
    conn.row_factory = sqlite3.Row
    intelligence_conn = None
    try:
        ensure_tables(conn)
        from src.data_collectors import market_intelligence_store as intelligence_store
        intelligence_conn = intelligence_store.connect(ensure=False)
        activation = _activation(conn, now, persist)
        frames = dict(source_frames or {})
        symbols = _symbols(intelligence_conn, now, cfg)
        for symbol in {*symbols, "BTC/USDT", "ETH/USDT"}:
            if symbol not in frames:
                frames[symbol] = _source_frame(symbol, cfg)[0]
        matured = _mature(conn, intelligence_conn, now, cfg, frames)
        seeded = _seed_events(conn, intelligence_conn, now, cfg, frames)
        new_rows = _process_events(conn, intelligence_conn, now, cfg, frames)
        if persist:
            for row in new_rows:
                _insert(
                    conn, "crypto_short_retest_shadow_outcomes",
                    OUTCOME_COLUMNS, row,
                )
        rows = [
            dict(row) for row in conn.execute(
                "SELECT * FROM crypto_short_retest_shadow_outcomes"
            ).fetchall()
        ]
        summary, strict_summary = _summary_rows(
            rows, activation.isoformat(), now, cfg
        )
        rejections: dict[str, int] = {}
        for row in rows:
            reason = row.get("rejection_reason")
            if reason:
                rejections[str(reason)] = rejections.get(str(reason), 0) + 1
        event_states = {
            str(row["status"]): int(row["n"])
            for row in conn.execute(
                "SELECT status,COUNT(*) n FROM crypto_short_retest_shadow_events GROUP BY status"
            ).fetchall()
        }
        diagnostics = strategy_diagnostics(
            rows, group_keys=(
                "profile_id", "session_bucket", "market_regime",
                "derivatives_state", "evidence_cohort",
            ),
        )
        diagnostics["event_funnel"] = {**seeded, **event_states}
        diagnostics["strict_summary"] = strict_summary
        if persist:
            columns = (
                "generated_at", "strategy_id", "activated_at", "forward_rows",
                "clean_rows", "dirty_rows", "clean_closed", "net_pnl_usd",
                "net_r", "fees_usd", "slippage_usd", "funding_usd",
                "profit_factor", "winrate", "max_drawdown_usd", "forward_days",
                "verdict", "rejection_counts_json", "diagnostics_json", "config_json",
            )
            eval_row = {
                "generated_at": now.isoformat(), "strategy_id": cfg["strategy_id"],
                "activated_at": activation.isoformat(), **{
                    key: summary[key] for key in (
                        "forward_rows", "clean_rows", "dirty_rows", "clean_closed",
                        "net_pnl_usd", "net_r", "fees_usd", "slippage_usd",
                        "funding_usd", "profit_factor", "winrate",
                        "max_drawdown_usd", "forward_days", "verdict",
                    )
                },
                "rejection_counts_json": json_text(rejections),
                "diagnostics_json": json_text(diagnostics),
                "config_json": json_text(cfg),
            }
            _insert(
                conn, "crypto_short_retest_shadow_evaluations",
                columns, eval_row, replace=True,
            )
            conn.commit()
        else:
            conn.rollback()
        return {
            "enabled": True, "generated_at": now.isoformat(),
            "activated_at": activation.isoformat(), "strategy_id": cfg["strategy_id"],
            "shadow_lane": cfg["shadow_lane"], "rows": new_rows,
            "closed_matured": matured, "summary": summary,
            "strict_summary": strict_summary, "rejection_counts": rejections,
            "event_counts": event_states, "diagnostics": diagnostics, "config": cfg,
        }
    finally:
        if intelligence_conn is not None:
            intelligence_conn.close()
        conn.close()


def render_markdown(result: dict[str, Any]) -> str:
    if not result.get("enabled"):
        return "# Crypto Short Continuation Retest (Shadow)\n\n- status: **DISABLED**\n"
    summary, strict = result["summary"], result["strict_summary"]
    lines = [
        "# Crypto Short Continuation Retest (Shadow)", "",
        f"- strategy: `{result['strategy_id']}`; lane: `{result['shadow_lane']}`",
        f"- activated: `{result['activated_at']}`; generated: `{result['generated_at']}`",
        "- Sequence: confirmed support break -> bounded retest -> bearish rejection -> next-close confirmation.",
        "- Exploratory entries remain visible when auxiliary context is missing, but only strict_v1 can prove edge.",
        "- Isolated Shadow only: no Paper, Telegram-entry, MEXC, or live writes.", "",
        "| all forward | strict clean closed | net USD | PF | win% | DD USD | fees | slippage | funding | verdict |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
        f"| {summary['forward_rows']} | {strict['clean_closed']} | {strict['net_pnl_usd']:.2f} | "
        f"{strict['profit_factor'] if strict['profit_factor'] is not None else 'n/a'} | "
        f"{strict['winrate'] if strict['winrate'] is not None else 'n/a'} | "
        f"{strict['max_drawdown_usd']:.2f} | {strict['fees_usd']:.2f} | "
        f"{strict['slippage_usd']:.2f} | {strict['funding_usd']:.2f} | {strict['verdict']} |",
        "", "## Event funnel", "",
    ]
    for key, value in sorted((result.get("diagnostics") or {}).get("event_funnel", {}).items()):
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Rejections", ""])
    for reason, count in sorted(
        (result.get("rejection_counts") or {}).items(),
        key=lambda item: (-item[1], item[0]),
    ):
        lines.append(f"- `{reason}`: {count}")
    lines.extend(["", *diagnostics_markdown(result.get("diagnostics") or {})])
    return "\n".join(lines) + "\n"


def write_report(result: dict[str, Any], path: str | None = None) -> str:
    target = Path(path) if path else ROOT / str(
        result.get("config", DEFAULTS).get("report_path")
    )
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_markdown(result), encoding="utf-8")
    return str(target)


__all__ = [
    "confirm_retest", "context_rejection", "detect_breakdown", "ensure_tables",
    "load_strategy_config", "render_markdown", "tick", "write_report",
]
