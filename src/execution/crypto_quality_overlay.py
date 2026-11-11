"""Crypto quality / risk overlay — PAPER / READ-MODEL / ACTIONABILITY ONLY.

A soft circuit-breaker that runs AFTER signal generation and BEFORE the paper-actionability/entry
decision. It routes a crypto paper candidate to one of FULL_SIZE / HALF_SIZE / SHADOW_ONLY / BLOCK
based on BTC/ETH regime, session quality, rolling session + per-symbol cooldowns, open-exposure and
entry-mode quality. The goal is to thin out clusters of bad crypto trades / original_stops WITHOUT
killing tp3_runner / profit_lock winners — so the main mechanism is HALF_SIZE / SHADOW_ONLY, and BLOCK
is used only for explicitly-disabled policy modes (and only when hard_block_enabled).

Guardrails (all enforced here):
  * NEVER touches live / auto-live / manual-live (live_enabled is a hard-off config flag).
  * NEVER rewrites signal generation, tier, score, TP/SL, final_r, signal_outcomes.
  * Writes ONLY the additive read-model tables crypto_quality_overlay_decisions + crypto_quality_cooldowns.
  * Missing / stale data is NEVER treated as good — it lowers confidence and floors the action to
    `default_unknown_data_action` (HALF_SIZE). Unknown ≠ confirmed.
  * Every decision is reversible via config/crypto_quality_overlay.yaml.

Profitability inputs are path-complete Paper rows (paper_execution_r + active-fee-profile
net_pnl_usdt), never legacy final_r or aggregate touch reconstructions.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None

_ROOT = Path(__file__).resolve().parents[2]
VERSION = "cqo_v1"
ACTIVE_FEE_PROFILE = "bybit_non_vip_usdt_perp"   # matches config/paper_portfolio.yaml (UI/control-plane)

FULL_SIZE, HALF_SIZE, SHADOW_ONLY, BLOCK = "FULL_SIZE", "HALF_SIZE", "SHADOW_ONLY", "BLOCK"
_SEV = {FULL_SIZE: 0, HALF_SIZE: 1, SHADOW_ONLY: 2, BLOCK: 3}
LOSS_STOPS = ("original_stop", "breakeven_stop")

_DEFAULT_CFG: dict[str, Any] = {
    "enabled": True, "paper_actionability_enabled": True, "live_enabled": False,
    "hard_block_enabled": False, "default_unknown_data_action": HALF_SIZE,
    "session_cooldown_enabled": True, "symbol_cooldown_enabled": True,
    "exposure_guard_enabled": True, "counterfactual_enabled": True, "overlay_version": VERSION,
    "regime": {"btc_return_conflict_pct": 0.10, "btc_weak_states": ["risk_off", "chop", "weak"],
               "state_aliases": {"risk-off": "risk_off", "btc_risk_off": "risk_off",
                                 "bearish": "risk_off", "downtrend": "risk_off",
                                 "risk-on": "risk_on", "bullish": "risk_on", "uptrend": "risk_on",
                                 "transition_down": "weak", "range": "chop", "ranging": "chop"},
               "min_rvol_strong": 1.5, "max_spread_bps_major": 8.0, "max_spread_bps_alt": 20.0,
               "major_symbols": ["BTC", "ETH", "SOL", "BNB", "XRP"]},
    "session": {"buckets": {"asia": {"start": 0, "end": 6, "quality": "weak"},
                            "europe": {"start": 7, "end": 13, "quality": "strong"},
                            "us": {"start": 13, "end": 21, "quality": "ok"},
                            "off": {"start": 21, "end": 24, "quality": "weak"}},
                "monday_stricter": True},
    "modes": {"scalp": {"disabled": True}, "swing": {"full_score_min": 70, "half_score_min": 65,
              "chop_action": HALF_SIZE},
              "intraday": {"advisory_soft_low": 65, "advisory_soft_high": 74}},
    "entry_modes": {
        "intraday": {"LIMIT_THEN_TAKER_TIMEOUT": "shadow_only", "BREAKOUT_CONTINUATION": "strong_confirm",
                     "PULLBACK_LIMIT": "primary", "LEVEL_HOLD_V2": "primary", "MOMENTUM_TAKER_NOW": "cautious",
                     "STRUCTURAL_RETEST": "primary", "NO_CHASE_SKIP": "shadow_only"},
        "swing": {"LIMIT_THEN_TAKER_TIMEOUT": "cooldown_dependent", "BREAKOUT_CONTINUATION": "swing_confirm",
                  "PULLBACK_LIMIT": "primary", "PULLBACK_CONFIRMED_RETEST": "primary",
                  "FIB_IMPULSE_RETEST": "primary", "STRUCTURAL_RETEST": "primary"}},
    "exposure": {"max_open_crypto_intraday": 4, "max_open_same_symbol_mode": 1,
                 "max_open_alt_beta_same_direction": 3, "max_open_alt_beta_same_direction_btc_weak": 2,
                 "over_limit_action": HALF_SIZE},
    "session_cooldown": {"lookback_hours": 8.0, "min_sample": 5, "consecutive_original_stops": 3,
                         "streak_lookback_trades": 5, "streak_ttl_hours": 4.0,
                         "net_r_floor": -2.0, "profit_factor_floor": 0.7,
                         "original_stop_rate_ceiling": 0.60, "ttl_hours": 8.0, "action": HALF_SIZE,
                         "action_btc_weak_risky_entry": HALF_SIZE},
    "symbol_cooldown": {"lookback_hours": 36.0, "trigger_original_stops": 2, "ttl_hours": 12.0,
                        "action": HALF_SIZE, "action_weak_regime": HALF_SIZE,
                        "action_strong_confirmation": HALF_SIZE,
                        "severe_original_stops": 3, "action_severe": HALF_SIZE},
    "intraday_session_gate": {"enabled": True, "weak_buckets": ["asia", "off"],
                              "action": HALF_SIZE, "action_with_confirmation": FULL_SIZE},
    "intraday_risk_off_gate": {"enabled": True, "action": BLOCK,
                                "long_regime_states": ["risk_off", "btc_risk_off"]},
    "intraday_derivatives_gate": {"enabled": True, "no_squeeze_action": HALF_SIZE},
    "derivatives_quality_guard": {"enabled": True, "min_fresh_venues": 2,
                                  "conflicting_oi_price_action": HALF_SIZE,
                                  "max_cross_venue_funding_spread": 0.001},
    "onchain_guard": {"enabled": True, "hard_block_verified_honeypot": True,
                      "hard_block_verified_blacklist": True, "hard_block_sell_tax_pct": 25.0,
                      "soft_reduce_sell_tax_pct": 8.0, "soft_reduce_top10_holder_pct": 70.0,
                      "soft_reduce_mintable": True},
    "weak_session_profit_protection": {"enabled": True, "arm_after_r": 0.5, "protected_stop_r": 0.0,
                                       "scope": "weak_session_or_cooldown_only"},
}


def load_cfg() -> dict[str, Any]:
    path = _ROOT / "config" / "crypto_quality_overlay.yaml"
    cfg = dict(_DEFAULT_CFG)
    if yaml and path.exists():
        try:
            with open(path, "r", encoding="utf-8") as fh:
                cfg = {**_DEFAULT_CFG, **((yaml.safe_load(fh) or {}).get("crypto_quality_overlay") or {})}
        except Exception:
            pass
    # Separate file/sign-off (config/cohort_guard.yaml); nested here so evaluate() stays a pure
    # function reading everything from one cfg dict, same as every other sub-rule.
    cfg["cohort_guard"] = load_cohort_guard_cfg()
    return cfg


def config_hash(cfg: dict[str, Any] | None = None) -> str:
    """Stable fingerprint of the effective overlay + cohort configuration."""
    payload = json.dumps(cfg or load_cfg(), sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def load_cohort_guard_cfg() -> dict[str, Any]:
    """config/cohort_guard.yaml -- separate file, separate operator sign-off from the main
    overlay config. A read/parse problem returns {} (guard inactive) rather than raising or
    guessing -- consistent with this module's "absence of data is never treated as evidence
    of a bad setup" rule; it must never itself become a surprise demotion source."""
    path = _ROOT / "config" / "cohort_guard.yaml"
    if yaml and path.exists():
        try:
            with open(path, "r", encoding="utf-8") as fh:
                return (yaml.safe_load(fh) or {}).get("cohort_guard") or {}
        except Exception:
            pass
    return {}


# ---- tables ------------------------------------------------------------------------------------
_DDL_DECISIONS = """
CREATE TABLE IF NOT EXISTS crypto_quality_overlay_decisions (
  signal_id TEXT PRIMARY KEY, symbol TEXT, mode TEXT, entry_mode TEXT, side TEXT, score REAL,
  timestamp TEXT, btc_regime_state TEXT, btc_15m_return REAL, btc_1h_return REAL,
  btc_ema_slope_state TEXT, eth_confirm_state TEXT, volume_rvol REAL, oi_change REAL,
  funding_state TEXT, spread_bps REAL, estimated_slippage_bps REAL, session_bucket_utc TEXT,
  session_quality_state TEXT, symbol_cooldown_state TEXT, mode_session_cooldown_state TEXT,
  crypto_quality_score REAL, crypto_quality_verdict TEXT, quality_action TEXT,
  quality_reasons_json TEXT, would_have_been_action_without_overlay TEXT, overlay_version TEXT,
  overlay_config_hash TEXT, computed_at TEXT, decision_context_type TEXT
);
"""
_DDL_COOLDOWNS = """
CREATE TABLE IF NOT EXISTS crypto_quality_cooldowns (
  cooldown_type TEXT, affected_mode TEXT, affected_session_bucket TEXT, affected_symbol TEXT,
  cooldown_active INTEGER, cooldown_reason TEXT, cooldown_started_at TEXT, cooldown_expires_at TEXT,
  recent_closed_count INTEGER, recent_original_stop_count INTEGER, recent_net_pnl_usd REAL,
  recent_profit_factor REAL, recent_original_stop_rate REAL, computed_at TEXT, version TEXT,
  PRIMARY KEY (cooldown_type, affected_mode, affected_session_bucket, affected_symbol)
);
"""
_DDL_POINT_IN_TIME = """
CREATE TABLE IF NOT EXISTS crypto_quality_overlay_decision_snapshots (
  signal_id TEXT PRIMARY KEY, quality_action TEXT, entry_mode TEXT, entry_mode_source TEXT,
  preentry_data_quality TEXT, overlay_version TEXT, quality_reasons_json TEXT,
  overlay_config_hash TEXT, decision_json TEXT, decided_at TEXT, decision_context_type TEXT
);
"""


def _has(conn, t) -> bool:
    return bool(conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (t,)).fetchone())


# ordered column list for crypto_quality_overlay_decisions — used for the explicit-column INSERT so a
# future nullable column never breaks the write, and for the idempotent migration below.
_DECISION_COLS = (
    "signal_id", "symbol", "mode", "entry_mode", "side", "score", "timestamp", "btc_regime_state",
    "btc_15m_return", "btc_1h_return", "btc_ema_slope_state", "eth_confirm_state", "volume_rvol",
    "oi_change", "funding_state", "spread_bps", "estimated_slippage_bps", "session_bucket_utc",
    "session_quality_state", "symbol_cooldown_state", "mode_session_cooldown_state", "crypto_quality_score",
    "crypto_quality_verdict", "quality_action", "quality_reasons_json",
    "would_have_been_action_without_overlay", "overlay_version", "overlay_config_hash",
    "computed_at", "decision_context_type",
)


def ensure_tables(conn) -> None:
    """Create the overlay read-model tables + idempotently migrate an OLDER decisions schema (one that
    predates the decision_context_type column, created by a CREATE-IF-NOT-EXISTS before the column was
    added). Never drops, never deletes rows: pre-existing rows are labelled 'current_snapshot'. Never
    touches live / final_r / signal_outcomes / proposed_signals."""
    conn.execute(_DDL_DECISIONS)
    conn.execute(_DDL_COOLDOWNS)
    conn.execute(_DDL_POINT_IN_TIME)
    cols = {r[1] for r in conn.execute("PRAGMA table_info(crypto_quality_overlay_decisions)")}
    if "decision_context_type" not in cols:
        conn.execute("ALTER TABLE crypto_quality_overlay_decisions ADD COLUMN decision_context_type TEXT")
        conn.execute("UPDATE crypto_quality_overlay_decisions SET decision_context_type='current_snapshot' "
                     "WHERE decision_context_type IS NULL")
    if "overlay_config_hash" not in cols:
        conn.execute("ALTER TABLE crypto_quality_overlay_decisions ADD COLUMN overlay_config_hash TEXT")
    snap_cols = {r[1] for r in conn.execute(
        "PRAGMA table_info(crypto_quality_overlay_decision_snapshots)")}
    if "overlay_config_hash" not in snap_cols:
        conn.execute(
            "ALTER TABLE crypto_quality_overlay_decision_snapshots "
            "ADD COLUMN overlay_config_hash TEXT")


def _num(v):
    try:
        return None if v in (None, "") else float(v)
    except (TypeError, ValueError):
        return None


def _worse(a: str, b: str) -> str:
    return a if _SEV.get(a, 0) >= _SEV.get(b, 0) else b


# ---- context readers (cached, fail-conservative) -----------------------------------------------
_MKT_CACHE: dict = {}


def _fs():
    from src.config import load_config
    from src.storage.file_store import FileStore
    return FileStore(load_config())


def _load(fs, symbol, tf, as_of=None):
    """Load binance OHLCV; if as_of is set, slice to bars whose close-time ≤ as_of (lookahead-safe)."""
    try:
        df = fs.load_ohlcv("binance", symbol, tf)
    except Exception:
        return None
    if df is None or getattr(df, "empty", True) or "timestamp" not in getattr(df, "columns", []):
        return None
    if as_of is not None:
        import pandas as pd
        d = df.copy()
        d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
        d = d.dropna(subset=["timestamp"])
        d = d[d["timestamp"] <= pd.Timestamp(as_of)]
        return d if not d.empty else None
    return df


def _slope_state(frame) -> str:
    try:
        from src.indicators.technicals import enrich_ohlcv
        e = enrich_ohlcv(frame)
        if "ema20" not in e or len(e) < 6:
            return "unknown"
        cur = float(e["ema20"].iloc[-1]); prev = float(e["ema20"].iloc[-5])
        if prev == 0:
            return "unknown"
        chg = (cur / prev) - 1.0
        c = float(e["close"].iloc[-1])
        above = c >= cur
        if chg > 0.0005 and above:
            return "up"
        if chg < -0.0005 and not above:
            return "down"
        return "flat"
    except Exception:
        return "unknown"


def _normalized_regime_state(value: Any, cfg: dict | None = None) -> str:
    """Map producer-specific regime labels onto the overlay's policy vocabulary."""
    state = str(value or "unknown").strip().lower().replace(" ", "_")
    aliases = dict((_DEFAULT_CFG.get("regime") or {}).get("state_aliases") or {})
    aliases.update(((cfg or {}).get("regime") or {}).get("state_aliases") or {})
    return str(aliases.get(state, state) or "unknown").lower()


def market_context(now, cfg, fs=None, as_of=None) -> dict:
    """BTC 15m/1h returns + EMA-slope + regime + ETH confirm. Cached per (date,hour) for LIVE reads;
    as_of (counterfactual) reconstructs lookahead-safe from OHLCV and is never cached."""
    live = as_of is None
    key = (now.date().isoformat(), now.hour)
    if live and key in _MKT_CACHE:
        return _MKT_CACHE[key]
    fs = fs or _fs()
    out = {"btc_15m_return": None, "btc_1h_return": None, "btc_ema_slope_state": "unknown",
           "btc_regime_state": "unknown", "eth_confirm_state": "unknown", "status": "unknown"}
    try:
        from src.indicators.technicals import pct_return, trend_label
        b15 = _load(fs, "BTC/USDT", "15m", as_of)
        b1h = _load(fs, "BTC/USDT", "1h", as_of)
        if b15 is not None:
            out["btc_15m_return"] = pct_return(b15, 1)
        if b1h is not None:
            out["btc_1h_return"] = pct_return(b1h, 1)
            out["btc_ema_slope_state"] = _slope_state(b1h)
            out["btc_regime_state"] = _normalized_regime_state(trend_label(b1h), cfg)
        eth = _load(fs, "ETH/USDT", "1h", as_of)
        if eth is not None:
            out["eth_confirm_state"] = trend_label(eth) or "unknown"
        if out["btc_15m_return"] is not None and out["btc_1h_return"] is not None:
            out["status"] = "ok"
    except Exception:
        pass
    # LIVE: prefer the cached market-dashboard crypto regime label when available (advisory).
    if live:
        try:
            from src.config import load_config
            conn = sqlite3.connect(f"file:{load_config().db_path}?mode=ro", uri=True)
            try:
                r = conn.execute("SELECT crypto_market_mode FROM market_dashboard_snapshots "
                                 "ORDER BY id DESC LIMIT 1").fetchone()
                if r and r[0]:
                    out["btc_regime_state"] = _normalized_regime_state(r[0], cfg)
            finally:
                conn.close()
        except Exception:
            pass
        _MKT_CACHE[key] = out
    return out


def _read_json(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return {}


def _base_symbol(symbol: str) -> str:
    return str(symbol or "").split("/")[0].split(":")[0].upper()


def _observed_intraday_features(fs, symbol: str, as_of=None) -> dict[str, Any]:
    """Compute diagnostic-only features from *fully closed* 15m bars.

    These fields intentionally have an ``observed_`` prefix.  They are frozen
    into the point-in-time decision record but do not feed the current overlay
    action.  That gives the intraday Shadow tests an honest feature set before
    any new gate is considered for Paper.
    """
    out: dict[str, Any] = {
        "observed_price_feature_status": "unknown",
        "observed_price_bar_closed_at": None,
        "observed_atr14_pct": None,
        "observed_realized_vol_1h_pct": None,
        "observed_realized_vol_4h_pct": None,
        "observed_rvol20": None,
        "observed_dollar_volume_24h": None,
        "observed_vwap20_distance_pct": None,
    }
    try:
        import math
        import pandas as pd
        from src.indicators.technicals import atr

        frame = fs.load_ohlcv("binance", symbol, "15m")
        required = {"timestamp", "high", "low", "close", "volume"}
        if frame is None or getattr(frame, "empty", True) or not required.issubset(frame.columns):
            return out
        cutoff = pd.Timestamp(as_of or datetime.now(timezone.utc))
        cutoff = cutoff.tz_localize("UTC") if cutoff.tzinfo is None else cutoff.tz_convert("UTC")
        data = frame.copy()
        data["timestamp"] = pd.to_datetime(data["timestamp"], utc=True, errors="coerce")
        for column in ("high", "low", "close", "volume"):
            data[column] = pd.to_numeric(data[column], errors="coerce")
        data = data.dropna(subset=["timestamp", "high", "low", "close", "volume"])
        # A row timestamp is the start of a 15m candle.  Exclude the still
        # forming candle and any later row, even in a replay with cached data.
        data = data[data["timestamp"] + pd.Timedelta(minutes=15) <= cutoff]
        if data.empty:
            out["observed_price_feature_status"] = "no_closed_bar_before_as_of"
            return out
        out["observed_price_bar_closed_at"] = (data["timestamp"].iloc[-1] + pd.Timedelta(minutes=15)).isoformat()
        if len(data) < 21:
            out["observed_price_feature_status"] = "insufficient_closed_bars"
            return out
        last_close = float(data["close"].iloc[-1])
        atr14 = atr(data, 14).iloc[-1]
        if pd.notna(atr14) and last_close > 0:
            out["observed_atr14_pct"] = float(atr14) / last_close * 100.0
        prior_volume = float(data["volume"].iloc[-21:-1].mean())
        if prior_volume > 0:
            out["observed_rvol20"] = float(data["volume"].iloc[-1]) / prior_volume
        returns = data["close"].pct_change().dropna()
        for field, periods in (("observed_realized_vol_1h_pct", 4), ("observed_realized_vol_4h_pct", 16)):
            sample = returns.tail(periods)
            if len(sample) == periods:
                out[field] = float(sample.std(ddof=0) * math.sqrt(periods) * 100.0)
        if len(data) >= 96:
            out["observed_dollar_volume_24h"] = float((data["close"] * data["volume"]).tail(96).sum())
        window = data.tail(20)
        total_volume = float(window["volume"].sum())
        if total_volume > 0 and last_close > 0:
            vwap = float((((window["high"] + window["low"] + window["close"]) / 3.0) * window["volume"]).sum() / total_volume)
            out["observed_vwap20_distance_pct"] = ((last_close / vwap) - 1.0) * 100.0 if vwap else None
        out["observed_price_feature_status"] = "ok"
    except Exception:
        out["observed_price_feature_status"] = "unavailable"
    return out


def symbol_context(fs, symbol, mode, cfg, as_of=None, db=None) -> dict:
    """Per-symbol RVOL / OI-change / funding-state / spread / slippage. Missing → UNKNOWN (never good)."""
    out = {"volume_rvol": None, "oi_change": None, "funding_state": "unknown",
           "spread_bps": None, "estimated_slippage_bps": None,
           "oi_price_regime": "unknown", "derivatives_venue_count": 0,
           "derivatives_status": "unknown", "cross_venue_funding_spread": None,
           "observed_liquidity_status": "unknown", "observed_liquidity_venue_count": 0,
           "observed_liquidity_provider_ts": None, "observed_spread_bps": None,
           "observed_bid_depth_10bps_usd": None, "observed_ask_depth_10bps_usd": None,
           "observed_bid_depth_25bps_usd": None, "observed_ask_depth_25bps_usd": None}
    reg = cfg.get("regime") or {}
    majors = {str(s).upper() for s in (reg.get("major_symbols") or [])}
    base = _base_symbol(symbol)
    intelligence_db = None
    # RVOL from the symbol's own 15m OHLCV
    try:
        from src.indicators.volume_anomaly import volume_ratio
        df = _load(fs, symbol, "15m", as_of)
        if df is not None:
            out["volume_rvol"] = volume_ratio(df, 20)
    except Exception:
        pass
    # Canonical venue-aware point-in-time history.  ``as_of`` is passed to SQL,
    # so replay/counterfactual calls cannot see a later snapshot.
    out.update(_observed_intraday_features(fs, symbol, as_of=as_of))
    try:
        from src.config import load_config
        from src.data_collectors import market_intelligence_store as _mi
        # Production signal/actionability tables live in the trading DB, while
        # high-cadence provider snapshots use their own WAL sidecar. Preserve
        # an explicitly injected non-production DB for deterministic tests.
        requested = Path(db).resolve() if db else None
        trading = Path(load_config().db_path).resolve()
        intelligence_db = requested if requested and requested != trading else None
        with _mi.connect(intelligence_db) as conn:
            deriv = _mi.latest_derivatives_context(conn, symbol, as_of=as_of)
            liquidity = _mi.latest_liquidity_context(conn, symbol, as_of=as_of)
        out.update({
            "oi_change": deriv.get("oi_change_24h"), "funding_state": deriv.get("funding_state") or "unknown",
            "oi_price_regime": deriv.get("oi_price_regime") or "unknown",
            "derivatives_venue_count": int(deriv.get("venue_count") or 0),
            "derivatives_status": deriv.get("status") or "unknown",
            "cross_venue_funding_spread": deriv.get("cross_venue_funding_spread"),
            "funding_rate_8h": deriv.get("funding_rate_8h"),
            "derivatives_latest_provider_ts": deriv.get("latest_provider_ts"),
            "observed_liquidity_status": liquidity.get("status") or "unknown",
            "observed_liquidity_venue_count": int(liquidity.get("venue_count") or 0),
            "observed_liquidity_provider_ts": liquidity.get("latest_provider_ts"),
            "observed_spread_bps": liquidity.get("spread_bps"),
            "observed_bid_depth_10bps_usd": liquidity.get("bid_depth_10bps_usd"),
            "observed_ask_depth_10bps_usd": liquidity.get("ask_depth_10bps_usd"),
            "observed_bid_depth_25bps_usd": liquidity.get("bid_depth_25bps_usd"),
            "observed_ask_depth_25bps_usd": liquidity.get("ask_depth_25bps_usd"),
        })
    except Exception:
        pass
    try:
        from src.intelligence.onchain_risk import compute_onchain_risk
        out.update(compute_onchain_risk(symbol, now=as_of, db=intelligence_db))
    except Exception:
        pass
    try:
        from src.intelligence.token_unlock_context import context as unlock_context
        unlock = unlock_context(symbol, as_of=as_of, db_path=intelligence_db)
        out.update({f"token_unlock_{key}": value for key, value in unlock.items()})
        out["token_unlock_adv_days"] = unlock.get("unlock_adv_days")
    except Exception:
        out.update({"token_unlock_status": "unknown", "token_unlock_action": "FULL_SIZE",
                    "token_unlock_would_action": "FULL_SIZE"})
    try:
        from src.intelligence.market_risk_context import cross_exchange_state
        venue = cross_exchange_state(symbol, as_of=as_of, db_path=intelligence_db)
        out.update({f"cross_exchange_{key}": value for key, value in venue.items()})
    except Exception:
        out.update({"cross_exchange_status": "unknown", "cross_exchange_action": "FULL_SIZE",
                    "cross_exchange_would_action": "FULL_SIZE"})
    try:
        from src.intelligence.options_context import latest as latest_options_context
        options = latest_options_context("crypto", base, as_of=as_of, db_path=intelligence_db)
        out.update({f"options_{key}": value for key, value in options.items()})
    except Exception:
        out.update({"options_status": "unknown"})
    # spread from universe cache (percent → bps); slippage heuristic when unavailable
    try:
        for rel in ("data/processed/market_summary/universe_latest.json",
                    "data/processed/symbol_universe.json"):
            u = _read_json(_ROOT / rel)
            rows = u.get("symbols") or u.get("candidates") or (u if isinstance(u, list) else [])
            hit = next((r for r in rows if isinstance(r, dict) and r.get("symbol") == symbol), None)
            if hit and hit.get("spread_pct") is not None:
                out["spread_bps"] = round(float(hit["spread_pct"]) * 100.0, 2)
                break
    except Exception:
        pass
    out["estimated_slippage_bps"] = 2.0 if base in majors else (5.0 if out["spread_bps"] is not None else None)
    return out


# ---- session ------------------------------------------------------------------------------------
def session_bucket(now, cfg) -> str:
    h = now.astimezone(timezone.utc).hour
    for name, b in ((cfg.get("session") or {}).get("buckets") or {}).items():
        s, e = int(b.get("start", 0)), int(b.get("end", 24))
        if s <= h < e:
            return name
    return "off"


def session_quality(bucket, now, cfg) -> str:
    b = ((cfg.get("session") or {}).get("buckets") or {}).get(bucket) or {}
    q = str(b.get("quality") or "weak")
    if (cfg.get("session") or {}).get("monday_stricter", True) and now.astimezone(timezone.utc).weekday() == 0:
        q = {"strong": "ok", "ok": "weak"}.get(q, q)     # Monday one notch stricter
    return q


# ---- closed-outcome + USD helpers (read-only) --------------------------------------------------
def _usd_map(conn, before_iso=None):
    """signal_id → active-fee-profile terminal exit net_pnl_usdt (deterministic)."""
    if not _has(conn, "paper_portfolio_ledger"):
        return {}
    rows = conn.execute(
        "SELECT l.signal_id, l.net_pnl_usdt FROM paper_portfolio_ledger l "
        "JOIN (SELECT signal_id, MAX(rowid) AS rid FROM paper_portfolio_ledger "
        "      WHERE event_type='exit' AND fee_profile=? GROUP BY signal_id) t "
        "  ON t.signal_id=l.signal_id AND l.rowid=t.rid", (ACTIVE_FEE_PROFILE,)).fetchall()
    return {sid: _num(p) for sid, p in rows}


def _entry_mode_for(conn):
    """signal_id -> valid, lookahead-safe pre-entry mode only.

    ``signal_entry_mode`` is a post-entry diagnostic and must never be used for
    a current overlay decision or new-logic evidence.
    """
    m = {}
    tbl = "signal_entry_mode_preentry"
    if _has(conn, tbl):
        cols = {r[1] for r in conn.execute(f"PRAGMA table_info({tbl})")}
        if "data_quality" in cols:
            for sid, em in conn.execute(
                "SELECT signal_id, entry_mode FROM signal_entry_mode_preentry "
                "WHERE entry_mode IS NOT NULL AND data_quality='ok'"):
                m[sid] = em
    return m


# ---- cooldowns ---------------------------------------------------------------------------------
def compute_cooldowns(conn, cfg, now) -> list[dict]:
    """Rolling session (mode×bucket) + per-symbol(+mode) cooldown states from recent CLOSED crypto
    outcomes. Pure read of proposed_signals+paper_execution_outcomes(+ledger). Returns rows to persist."""
    if not (_has(conn, "proposed_signals") and _has(conn, "paper_execution_outcomes")):
        return []
    outcome_cols = {str(row[1]) for row in conn.execute("PRAGMA table_info(paper_execution_outcomes)")}
    required = {"exit_at", "evidence_class", "execution_validity", "economic_trade_key"}
    # A legacy schema cannot distinguish a real forward exit from a historical
    # recomputation.  Do not manufacture a cooldown from ambiguous evidence.
    if not required.issubset(outcome_cols):
        return []
    usd = _usd_map(conn)
    sc = cfg.get("session_cooldown") or {}
    yc = cfg.get("symbol_cooldown") or {}
    sess_lb = float(sc.get("lookback_hours", 8.0)); sym_lb = float(yc.get("lookback_hours", 36.0))
    horizon = max(sess_lb, sym_lb)
    version_clause = ""
    params: list[Any] = [
        (now - timedelta(hours=horizon)).isoformat(), now.isoformat()
    ]
    if "version" in outcome_cols:
        from src.execution.paper_live_exit_path import VERSION as live_exit_version
        version_clause = "AND o.version=? "
        params.append(live_exit_version)
    rows = conn.execute(
        "SELECT p.signal_id, p.symbol, p.mode, o.close_reason, o.paper_execution_r, o.exit_at, "
        "COALESCE(NULLIF(o.economic_trade_key,''), o.signal_id) "
        "FROM paper_execution_outcomes o JOIN proposed_signals p ON p.signal_id=o.signal_id "
        "WHERE p.asset_class='crypto' AND o.close_reason NOT IN ('open','no_entry') "
        "AND o.evidence_class='forward_postfreeze' AND o.execution_validity='valid' "
        "AND o.exit_at IS NOT NULL AND o.exit_at >= ? AND o.exit_at <= ? "
        + version_clause +
        "ORDER BY o.exit_at ASC, o.signal_id ASC",
        tuple(params)).fetchall()
    by_sess: dict[tuple, list] = {}
    by_sym: dict[tuple, list] = {}
    seen_trade_keys: set[str] = set()
    for sid, sym, mode, close, r, ts, trade_key in rows:
        key = str(trade_key or sid)
        if key in seen_trade_keys:
            continue
        seen_trade_keys.add(key)
        try:
            t = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
            if t.tzinfo is None:
                t = t.replace(tzinfo=timezone.utc)
        except Exception:
            continue
        bucket = session_bucket(t, cfg)
        rec = {"close": str(close or ""), "r": _num(r), "usd": usd.get(sid), "t": t}
        if (now - t).total_seconds() <= sess_lb * 3600:
            by_sess.setdefault((mode, bucket), []).append(rec)
        if (now - t).total_seconds() <= sym_lb * 3600:
            by_sym.setdefault((sym, mode), []).append(rec)

    out: list[dict] = []
    now_iso = now.isoformat()
    if cfg.get("session_cooldown_enabled", True):
        for (mode, bucket), recs in by_sess.items():
            out.append(_session_cooldown_row(mode, bucket, recs, sc, now_iso))
    if cfg.get("symbol_cooldown_enabled", True):
        for (sym, mode), recs in by_sym.items():
            out.append(_symbol_cooldown_row(sym, mode, recs, yc, now_iso))
    return [r for r in out if r]


def _pf(recs) -> float | None:
    gains = sum(x["r"] for x in recs if x["r"] and x["r"] > 0)
    losses = -sum(x["r"] for x in recs if x["r"] and x["r"] < 0)
    if losses <= 0:
        return float("inf") if gains > 0 else None
    return round(gains / losses, 3)


def _session_cooldown_row(mode, bucket, recs, sc, now_iso):
    n = len(recs)
    stops = [x for x in recs if x["close"] in LOSS_STOPS or x["close"] == "original_stop"]
    orig = [x for x in recs if x["close"] == "original_stop"]
    net_r = round(sum(x["r"] for x in recs if x["r"] is not None), 3)
    net_usd = round(sum(x["usd"] for x in recs if x["usd"] is not None), 2)
    pf = _pf(recs)
    stop_rate = round(len(orig) / n, 3) if n else 0.0
    min_s = int(sc.get("min_sample", 5))
    # A real loss streak gets a short size reduction. A broader cooldown needs
    # the full minimum sample; three rows alone are too little evidence to
    # suppress an entire Paper lane.
    streak_window = max(min_s, int(sc.get("streak_lookback_trades", min_s)))
    recent_recs = recs[-streak_window:]
    consec = 0
    for x in reversed(recent_recs):
        if x["close"] == "original_stop":
            consec += 1
        else:
            break
    reasons = []
    streak_active = n >= min_s and consec >= int(sc.get("consecutive_original_stops", 3))
    if streak_active:
        reasons.append(f"streak_{consec}_original_stops_last_{len(recent_recs)}")
    if n >= min_s and net_r <= float(sc.get("net_r_floor", -2.0)):
        reasons.append(f"net_r_{net_r}<=floor")
    if n >= min_s and pf is not None and pf < float(sc.get("profit_factor_floor", 0.7)):
        reasons.append(f"pf_{pf}<floor_n{n}")
    if n >= min_s and stop_rate > float(sc.get("original_stop_rate_ceiling", 0.60)):
        reasons.append(f"stop_rate_{stop_rate}>ceiling_n{n}")
    active = bool(reasons)
    started = min((x["t"] for x in recs), default=None)
    expires = None
    if active:
        broad_active = any(not reason.startswith("streak_") for reason in reasons)
        ttl = float(sc.get("ttl_hours", 8.0) if broad_active else sc.get("streak_ttl_hours", 4.0))
        expires = (max(x["t"] for x in recs) + timedelta(hours=ttl)).isoformat()
    return {"cooldown_type": "session", "affected_mode": mode, "affected_session_bucket": bucket,
            "affected_symbol": "*", "cooldown_active": int(active),
            "cooldown_reason": ",".join(reasons), "cooldown_started_at": started.isoformat() if started else None,
            "cooldown_expires_at": expires, "recent_closed_count": n,
            "recent_original_stop_count": len(orig), "recent_net_pnl_usd": net_usd,
            "recent_profit_factor": (None if pf == float("inf") else pf),
            "recent_original_stop_rate": stop_rate, "computed_at": now_iso, "version": VERSION}


def _symbol_cooldown_row(sym, mode, recs, yc, now_iso):
    n = len(recs)
    orig = [x for x in recs if x["close"] == "original_stop"]
    net_usd = round(sum(x["usd"] for x in recs if x["usd"] is not None), 2)
    pf = _pf(recs)
    min_s = int(yc.get("min_sample", 3))
    stop_trigger = len(orig) >= int(yc.get("trigger_original_stops", 2))
    # 2026-07-13 audit: the raw stop-count trigger had no minimum sample and no PnL check, so a
    # symbol that's still net profitable (winners outweighing the stops) got HALF_SIZE'd anyway.
    # Both gates mirror session_cooldown's existing min_sample/net_r_floor pattern.
    is_profitable = net_usd > float(yc.get("net_pnl_override_usd", 0.0))
    active = stop_trigger and n >= min_s and not is_profitable
    reasons = [f"{len(orig)}_original_stops_in_window"] if active else []
    started = min((x["t"] for x in recs), default=None)
    expires = ((max(x["t"] for x in recs) + timedelta(hours=float(yc.get("ttl_hours", 24.0)))).isoformat()
               if active else None)
    return {"cooldown_type": "symbol", "affected_mode": mode, "affected_session_bucket": "*",
            "affected_symbol": sym, "cooldown_active": int(active), "cooldown_reason": ",".join(reasons),
            "cooldown_started_at": started.isoformat() if started else None, "cooldown_expires_at": expires,
            "recent_closed_count": n, "recent_original_stop_count": len(orig),
            "recent_net_pnl_usd": net_usd, "recent_profit_factor": (None if pf == float("inf") else pf),
            "recent_original_stop_rate": round(len(orig) / n, 3) if n else 0.0,
            "computed_at": now_iso, "version": VERSION}


def refresh_cooldowns(*, db: str | None = None, now_iso: str | None = None) -> dict[str, Any]:
    from src.config import load_config
    cfg = load_cfg()
    path = db or str(load_config().db_path)
    now = datetime.fromisoformat(now_iso) if now_iso else datetime.now(timezone.utc)
    conn = sqlite3.connect(path)
    try:
        ensure_tables(conn)
        rows = compute_cooldowns(conn, cfg, now)
        conn.execute("DELETE FROM crypto_quality_cooldowns")
        for r in rows:
            conn.execute(
                "INSERT OR REPLACE INTO crypto_quality_cooldowns VALUES "
                "(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (r["cooldown_type"], r["affected_mode"], r["affected_session_bucket"], r["affected_symbol"],
                 r["cooldown_active"], r["cooldown_reason"], r["cooldown_started_at"], r["cooldown_expires_at"],
                 r["recent_closed_count"], r["recent_original_stop_count"], r["recent_net_pnl_usd"],
                 r["recent_profit_factor"], r["recent_original_stop_rate"], r["computed_at"], r["version"]))
        conn.commit()
        sess_active = sum(1 for r in rows if r["cooldown_type"] == "session" and r["cooldown_active"])
        sym_active = sum(1 for r in rows if r["cooldown_type"] == "symbol" and r["cooldown_active"])
        return {"session_cooldown": sess_active > 0, "symbols_on_cooldown": sym_active, "rows": len(rows)}
    finally:
        conn.close()


def read_cooldowns(conn, now):
    """Return {('session',mode,bucket): row, ('symbol',symbol,mode): row} of ACTIVE, non-expired cooldowns."""
    if not _has(conn, "crypto_quality_cooldowns"):
        return {}
    out = {}
    for row in conn.execute("SELECT cooldown_type, affected_mode, affected_session_bucket, affected_symbol, "
                            "cooldown_active, cooldown_reason, cooldown_expires_at FROM crypto_quality_cooldowns "
                            "WHERE cooldown_active=1"):
        ctype, mode, bucket, sym, active, reason, expires = row
        if expires:
            try:
                exp = datetime.fromisoformat(str(expires).replace("Z", "+00:00"))
                if exp.tzinfo is None:
                    exp = exp.replace(tzinfo=timezone.utc)
                if now > exp:
                    continue          # TTL elapsed → treat as inactive
            except Exception:
                pass
        key = ("session", mode, bucket) if ctype == "session" else ("symbol", sym, mode)
        out[key] = {"reason": reason, "expires": expires}
    return out


def _catalyst_labels_for(conn) -> dict[str, dict]:
    """signal_id -> catalyst/news labels. Read-only; missing table = no catalyst boost."""
    if not _has(conn, "signal_catalyst_labels"):
        return {}
    try:
        rows = conn.execute(
            "SELECT signal_id, catalyst_freshness, catalyst_strength, source_quality, "
            "symbol_mapping, derivatives_label FROM signal_catalyst_labels"
        ).fetchall()
    except sqlite3.OperationalError:
        return {}
    out: dict[str, dict] = {}
    for r in rows:
        out[r[0]] = {
            "catalyst_freshness": r[1],
            "catalyst_strength": r[2],
            "source_quality": r[3],
            "symbol_mapping": r[4],
            "derivatives_label": r[5],
        }
    return out


# ---- exposure ----------------------------------------------------------------------------------
_ALT_MAJORS = {"BTC", "ETH"}
_TERMINAL_LIFECYCLE_STATES = {"CLOSED", "INVALID", "NO_ENTRY"}
_TERMINAL_SIGNAL_STATUSES = {
    "stopped", "tp3_hit", "expired", "stale_before_entry", "entry_moved_away",
    "ambiguous", "invalidated_before_entry", "missed_no_entry", "expired_no_entry",
    "cancelled_by_regime_change", "cancelled_by_news", "cancelled", "canceled",
    "closed", "invalid", "no_entry",
}


def _accepted_paper_alerts(conn) -> dict[str, dict]:
    """Return actual point-in-time Paper acceptances keyed by signal_id.

    The overlay snapshot is a requested action.  The paper-entry alert is the
    authoritative routing result: late/risk/shadow statuses and size_weight=0
    mean that no Paper position was accepted, even if the requested action was
    HALF_SIZE.  Missing acceptance evidence is deliberately not promoted.
    """
    if not _has(conn, "signal_alerts"):
        return {}
    try:
        from src.execution.paper_actionability import NON_ACTIONABLE_ALERT_STATUSES
        rows = conn.execute(
            "SELECT signal_id,telegram_status,payload_json FROM signal_alerts "
            "WHERE alert_type='paper_entry' ORDER BY sent_at ASC,rowid ASC"
        ).fetchall()
    except sqlite3.OperationalError:
        return {}
    latest: dict[str, tuple[str, dict]] = {}
    for signal_id, status, payload_json in rows:
        try:
            payload = json.loads(payload_json or "{}")
            payload = payload if isinstance(payload, dict) else {}
        except (TypeError, ValueError):
            payload = {}
        latest[str(signal_id)] = (str(status or "").lower(), payload)

    accepted: dict[str, dict] = {}
    for signal_id, (status, payload) in latest.items():
        if status in NON_ACTIONABLE_ALERT_STATUSES:
            continue
        if status != "sent" and not status.startswith("error:"):
            continue
        action = str(payload.get("crypto_swing_main_paper_action")
                     or payload.get("cqo_effective_paper_action")
                     or payload.get("cqo_quality_action") or FULL_SIZE).upper()
        if action not in (FULL_SIZE, HALF_SIZE):
            continue
        default_weight = 0.5 if action == HALF_SIZE else 1.0
        try:
            weight = float(payload.get("size_weight", default_weight))
        except (TypeError, ValueError):
            weight = 0.0
        if weight <= 0.0:
            continue
        accepted[signal_id] = {"paper_action": action, "size_weight": min(1.0, weight),
                               "telegram_status": status}
    return accepted


def open_exposure(conn) -> dict:
    """Actually accepted, currently-open crypto Paper positions.

    ``_open_positions_by_signal`` is internal bookkeeping used to remove the
    candidate itself when its paper-execution row was written before the
    point-in-time overlay decision.  Tracker-only/Shadow rows never consume a
    Paper exposure slot.
    """
    if not (_has(conn, "proposed_signals") and _has(conn, "paper_execution_outcomes")):
        return {"intraday_open": 0, "by_symbol_mode": {}, "alt_long": 0, "alt_short": 0,
                "actionable_open": 0, "raw_open_outcomes": 0, "excluded_nonactionable": 0,
                "excluded_terminal": 0, "_open_positions_by_signal": {}}
    outcome_cols = {r[1] for r in conn.execute("PRAGMA table_info(paper_execution_outcomes)")}
    signal_cols = {r[1] for r in conn.execute("PRAGMA table_info(proposed_signals)")}
    lifecycle_sql = "o.lifecycle_state" if "lifecycle_state" in outcome_cols else "NULL"
    status_sql = "p.status" if "status" in signal_cols else "NULL"
    rows = conn.execute(
        f"SELECT o.signal_id,p.symbol,p.mode,p.direction,{lifecycle_sql},{status_sql} "
        "FROM paper_execution_outcomes o JOIN proposed_signals p ON p.signal_id=o.signal_id "
        "WHERE lower(COALESCE(p.asset_class,''))='crypto' AND o.close_reason='open'").fetchall()
    accepted = _accepted_paper_alerts(conn)
    by_sym_mode: dict[tuple, int] = {}
    by_signal: dict[str, list[tuple[str, str, str]]] = {}
    intraday_open = alt_long = alt_short = 0
    excluded_terminal = excluded_nonactionable = 0
    for signal_id, sym, mode, direction, lifecycle_state, signal_status in rows:
        if str(lifecycle_state or "").upper() in _TERMINAL_LIFECYCLE_STATES \
                or str(signal_status or "").lower() in _TERMINAL_SIGNAL_STATUSES:
            excluded_terminal += 1
            continue
        if str(signal_id) not in accepted:
            excluded_nonactionable += 1
            continue
        by_signal.setdefault(str(signal_id), []).append((sym, mode, direction))
        by_sym_mode[(sym, mode)] = by_sym_mode.get((sym, mode), 0) + 1
        if mode == "intraday":
            intraday_open += 1
        if _base_symbol(sym) not in _ALT_MAJORS:
            if str(direction).lower() == "short":
                alt_short += 1
            else:
                alt_long += 1
    return {"intraday_open": intraday_open, "by_symbol_mode": by_sym_mode,
            "alt_long": alt_long, "alt_short": alt_short, "actionable_open": len(by_signal),
            "raw_open_outcomes": len(rows), "excluded_nonactionable": excluded_nonactionable,
            "excluded_terminal": excluded_terminal,
            "_open_positions_by_signal": by_signal}


def _exposure_without_current_signal(exposure: dict, signal_id: str | None) -> dict:
    """Return exposure immediately before ``signal_id`` would be opened.

    The tracker records the additive paper-execution row before it asks this
    overlay whether the entry is actionable. Without this adjustment, a new
    candidate always appears to conflict with itself and can also consume one
    alt-beta slot. Existing positions remain fully counted.
    """
    own_positions = (exposure.get("_open_positions_by_signal") or {}).get(str(signal_id or "")) or []
    if not own_positions:
        return exposure

    out = dict(exposure)
    out["by_symbol_mode"] = dict(exposure.get("by_symbol_mode") or {})
    removed = 0
    for sym, mode, direction in own_positions:
        removed += 1
        key = (sym, mode)
        remaining = max(0, int(out["by_symbol_mode"].get(key, 0)) - 1)
        if remaining:
            out["by_symbol_mode"][key] = remaining
        else:
            out["by_symbol_mode"].pop(key, None)
        if mode == "intraday":
            out["intraday_open"] = max(0, int(out.get("intraday_open", 0)) - 1)
        if _base_symbol(sym) not in _ALT_MAJORS:
            side_key = "alt_short" if str(direction).lower() == "short" else "alt_long"
            out[side_key] = max(0, int(out.get(side_key, 0)) - 1)
    out["actionable_open"] = max(0, int(out.get("actionable_open", 0)) - removed)
    return out


# ---- decision ----------------------------------------------------------------------------------
@dataclass
class OverlayDecision:
    signal_id: str = ""
    symbol: str = ""
    mode: str = ""
    entry_mode: str | None = None
    side: str = ""
    score: float | None = None
    timestamp: str = ""
    action: str = FULL_SIZE
    baseline_action: str = FULL_SIZE
    quality_score: float = 100.0
    verdict: str = "STRONG"
    reasons: list[str] = field(default_factory=list)
    ctx: dict = field(default_factory=dict)

    def fields(self) -> dict:
        c = self.ctx
        return {
            "signal_id": self.signal_id, "symbol": self.symbol, "mode": self.mode,
            "entry_mode": self.entry_mode, "side": self.side, "score": self.score,
            "timestamp": self.timestamp, "btc_regime_state": c.get("btc_regime_state"),
            "btc_15m_return": c.get("btc_15m_return"), "btc_1h_return": c.get("btc_1h_return"),
            "btc_ema_slope_state": c.get("btc_ema_slope_state"), "eth_confirm_state": c.get("eth_confirm_state"),
            "volume_rvol": c.get("volume_rvol"), "oi_change": c.get("oi_change"),
            "funding_state": c.get("funding_state"), "spread_bps": c.get("spread_bps"),
            "estimated_slippage_bps": c.get("estimated_slippage_bps"),
            "session_bucket_utc": c.get("session_bucket_utc"), "session_quality_state": c.get("session_quality_state"),
            "symbol_cooldown_state": c.get("symbol_cooldown_state"),
            "mode_session_cooldown_state": c.get("mode_session_cooldown_state"),
            "crypto_quality_score": round(self.quality_score, 1), "crypto_quality_verdict": self.verdict,
            "quality_action": self.action, "quality_reasons_json": json.dumps(self.reasons),
            "would_have_been_action_without_overlay": self.baseline_action, "overlay_version": VERSION,
            "overlay_config_hash": c.get("overlay_config_hash"),
            "entry_mode_source": c.get("entry_mode_source"),
            "preentry_data_quality": c.get("preentry_data_quality"),
            "strong_confirmation": c.get("strong_confirmation"),
            "fresh_catalyst_confirmed": c.get("fresh_catalyst_confirmed"),
            "cohort_guard_policy_version": c.get("cohort_guard_policy_version"),
            "cohort_guard_mode": c.get("cohort_guard_mode"),
            "cohort_guard_routing_enabled": c.get("cohort_guard_routing_enabled"),
            "cohort_guard_in_scope": c.get("cohort_guard_in_scope"),
            "cohort_guard_would_demote": c.get("cohort_guard_would_demote"),
            "derivatives_status": c.get("derivatives_status"),
            "derivatives_venue_count": c.get("derivatives_venue_count"),
            "oi_price_regime": c.get("oi_price_regime"),
            "funding_rate_8h": c.get("funding_rate_8h"),
            "observed_price_feature_status": c.get("observed_price_feature_status"),
            "observed_price_bar_closed_at": c.get("observed_price_bar_closed_at"),
            "observed_atr14_pct": c.get("observed_atr14_pct"),
            "observed_realized_vol_1h_pct": c.get("observed_realized_vol_1h_pct"),
            "observed_realized_vol_4h_pct": c.get("observed_realized_vol_4h_pct"),
            "observed_rvol20": c.get("observed_rvol20"),
            "observed_dollar_volume_24h": c.get("observed_dollar_volume_24h"),
            "observed_vwap20_distance_pct": c.get("observed_vwap20_distance_pct"),
            "observed_liquidity_status": c.get("observed_liquidity_status"),
            "observed_liquidity_venue_count": c.get("observed_liquidity_venue_count"),
            "observed_liquidity_provider_ts": c.get("observed_liquidity_provider_ts"),
            "observed_spread_bps": c.get("observed_spread_bps"),
            "observed_bid_depth_10bps_usd": c.get("observed_bid_depth_10bps_usd"),
            "observed_ask_depth_10bps_usd": c.get("observed_ask_depth_10bps_usd"),
            "observed_bid_depth_25bps_usd": c.get("observed_bid_depth_25bps_usd"),
            "observed_ask_depth_25bps_usd": c.get("observed_ask_depth_25bps_usd"),
            "onchain_risk_status": c.get("onchain_risk_status"),
            "onchain_risk_score": c.get("onchain_risk_score"),
            "onchain_data_confidence": c.get("onchain_data_confidence"),
            "contract_verified": c.get("contract_verified"),
            "paper_guard_eligible": c.get("paper_guard_eligible"),
            "token_unlock_status": c.get("token_unlock_status"),
            "token_unlock_action": c.get("token_unlock_action"),
            "token_unlock_would_action": c.get("token_unlock_would_action"),
            "token_unlock_reason": c.get("token_unlock_reason"),
            "token_unlock_days_to_unlock": c.get("token_unlock_days_to_unlock"),
            "token_unlock_pct_circulating": c.get("token_unlock_pct_circulating"),
            "token_unlock_adv_days": c.get("token_unlock_adv_days"),
            "token_unlock_context_ts": c.get("token_unlock_context_ts"),
            "cross_exchange_status": c.get("cross_exchange_status"),
            "cross_exchange_action": c.get("cross_exchange_action"),
            "cross_exchange_would_action": c.get("cross_exchange_would_action"),
            "cross_exchange_reason": c.get("cross_exchange_reason"),
            "cross_exchange_divergence_bps": c.get("cross_exchange_divergence_bps"),
            "cross_exchange_fresh_venues": c.get("cross_exchange_fresh_venues"),
            "cross_exchange_persistent": c.get("cross_exchange_persistent"),
            "cross_exchange_context_ts": c.get("cross_exchange_context_ts"),
            "options_status": c.get("options_status"),
            "options_iv30": c.get("options_iv30"),
            "options_rv30": c.get("options_rv30"),
            "options_vrp": c.get("options_vrp"),
            "options_iv_rank": c.get("options_iv_rank"),
            "options_context_ts": c.get("options_provider_ts"),
            "paper_exposure_intraday_open": c.get("paper_exposure_intraday_open"),
            "paper_exposure_actionable_open": c.get("paper_exposure_actionable_open"),
            "paper_exposure_raw_open_outcomes": c.get("paper_exposure_raw_open_outcomes"),
            "paper_exposure_excluded_nonactionable": c.get("paper_exposure_excluded_nonactionable"),
            "paper_exposure_excluded_terminal": c.get("paper_exposure_excluded_terminal"),
        }


def _btc_weak_confirmed(mkt, cfg) -> bool:
    """True only when we KNOW the regime is weak (data present + a weak label). Unknown/missing data is
    NOT counted as weak for the purpose of DEMOTING size — that is the difference between a surgical
    guard (demote on evidence of a bad regime) and a strangler (demote on absence of good data)."""
    if mkt.get("status") != "ok":
        return False
    st = _normalized_regime_state(mkt.get("btc_regime_state"), cfg)
    weak = {str(x).lower() for x in ((cfg.get("regime") or {}).get("btc_weak_states") or [])}
    # ``unknown`` is an absence of a classified regime, not positive evidence of
    # a weak BTC tape. Keep this explicit even if an old config accidentally lists it.
    return st != "unknown" and st in weak


def _btc_unknown(mkt) -> bool:
    return mkt.get("status") != "ok"


def _btc_aligned(side, mkt, cfg) -> bool | None:
    r15, r1h = mkt.get("btc_15m_return"), mkt.get("btc_1h_return")
    if r15 is None or r1h is None:
        return None
    thr = float((cfg.get("regime") or {}).get("btc_return_conflict_pct", 0.10))
    if str(side).lower() == "short":
        return r15 <= thr and r1h <= thr
    return r15 >= -thr and r1h >= -thr


def _rvol_strong(sym, cfg) -> bool:
    rv = sym.get("volume_rvol")
    return rv is not None and rv >= float((cfg.get("regime") or {}).get("min_rvol_strong", 1.5))


def _spread_ok(symbol, sym, cfg) -> bool | None:
    sp = sym.get("spread_bps")
    if sp is None:
        return None
    reg = cfg.get("regime") or {}
    majors = {str(s).upper() for s in (reg.get("major_symbols") or [])}
    cap = float(reg.get("max_spread_bps_major", 8.0) if _base_symbol(symbol) in majors
                else reg.get("max_spread_bps_alt", 20.0))
    return sp <= cap


def _funding_against(side, sym) -> bool:
    st = str(sym.get("funding_state") or "unknown")
    if str(side).lower() == "short":
        return st == "short_crowded"          # shorting into a crowded-short = squeeze risk
    return st == "extreme_long"               # longing into extreme-long crowding


def _strong_confirmation(cand, mkt, sym, cfg) -> bool:
    """Full positive confirmation — requires DATA PRESENT (not unknown) + BTC aligned + strong RVOL +
    funding not against + spread ok + high score + regime not weak. Used for BREAKOUT full-size and
    the symbol-cooldown bypass."""
    aligned = _btc_aligned(cand["side"], mkt, cfg)
    spread = _spread_ok(cand["symbol"], sym, cfg)
    score = cand.get("score")
    score_ok = score is not None and float(score) >= 70
    return bool(not _btc_unknown(mkt) and aligned is True and _rvol_strong(sym, cfg)
                and not _funding_against(cand["side"], sym) and spread is not False and score_ok
                and not _btc_weak_confirmed(mkt, cfg))


def _fresh_catalyst(cand: dict) -> bool:
    """True only for a catalyst that is recent enough to justify intraday risk.

    Old labels like ``old(107.7h)`` are intentionally NOT a catalyst boost. Missing
    labels never block by themselves, but also never rescue weak-session / risky
    intraday trades.
    """
    if not cand.get("news_supported"):
        return False
    fresh = str(cand.get("catalyst_freshness") or "").lower()
    strength = str(cand.get("catalyst_strength") or "").lower()
    mapping = str(cand.get("symbol_mapping") or "").lower()
    source = str(cand.get("source_quality") or "").lower()
    freshness_ok = fresh.startswith("fresh") or fresh.startswith("recent")
    strength_ok = strength in ("medium", "strong")
    mapping_ok = mapping in ("exact", "trusted", "entity_exact", "symbol_exact")
    source_ok = source not in ("rumour", "rumor", "low_quality")
    return bool(freshness_ok and strength_ok and mapping_ok and source_ok)


def _cooldown_stop_count(row: dict | None) -> int:
    if not row:
        return 0
    reason = str(row.get("reason") or "")
    for part in reason.split(","):
        head = part.strip().split("_", 1)[0]
        try:
            return max(0, int(head))
        except ValueError:
            continue
    return 0


def evaluate(cand: dict, mkt: dict, sym: dict, session: dict, cooldowns: dict,
             exposure: dict, cfg: dict) -> OverlayDecision:
    """Pure decision. Composes every sub-rule and takes the WORST (most conservative) action, floored
    by default_unknown_data_action when critical market data is unknown. FULL never survives unknown BTC."""
    mode = str(cand.get("mode") or "").lower()
    side = str(cand.get("side") or "long").lower()
    em = str(cand.get("entry_mode") or "").upper()
    score = _num(cand.get("score"))
    reasons: list[str] = []
    action = FULL_SIZE
    unk_floor = str(cfg.get("default_unknown_data_action", HALF_SIZE))

    def bump(a, why):
        nonlocal action
        if _SEV.get(a, 0) > _SEV.get(action, 0):
            action = a
        if why and why not in reasons:
            reasons.append(why)

    quality = 100.0
    unknown = _btc_unknown(mkt)
    weak_conf = _btc_weak_confirmed(mkt, cfg)          # KNOWN-weak regime (data present)
    aligned = _btc_aligned(side, mkt, cfg)
    rvol_ok = _rvol_strong(sym, cfg)
    spread = _spread_ok(cand["symbol"], sym, cfg)
    funding_bad = _funding_against(side, sym)
    sess_q = str(session.get("session_quality_state") or "weak")
    sess_bucket = str(session.get("session_bucket_utc") or "")
    risky_em = em in ("LIMIT_THEN_TAKER_TIMEOUT", "BREAKOUT_CONTINUATION", "MOMENTUM_TAKER_NOW", "NO_CHASE_SKIP")
    fresh_cat = _fresh_catalyst(cand)
    market_regime = str(cand.get("market_regime") or "").strip().lower()

    # ---- confidence penalties (crypto_quality_score only — these NEVER demote size on their own,
    #      so a clean primary setup with merely-missing data stays FULL and winners are not killed) --
    if unknown:
        quality -= 26; reasons.append("market_data_unknown")   # unknown data alone drops out of STRONG
    if weak_conf:
        quality -= 15; reasons.append("btc_regime_weak")
    if aligned is False:
        quality -= 20; reasons.append("btc_direction_conflict")
    if not rvol_ok:
        quality -= 8
    if funding_bad:
        quality -= 8; reasons.append("funding_against")
    if sess_q == "weak":
        quality -= 8

    # ---- size demotions require POSITIVE evidence of a bad setup (not absence of good data) -----
    # Unknown data floors ONLY a risky entry mode (unknown must not let a risky mode be full size).
    if unknown and risky_em:
        bump(unk_floor, "risky_entry_unknown_data_floor")
    if spread is False:
        bump(HALF_SIZE, "spread_too_wide")
    if aligned is False and funding_bad:
        bump(HALF_SIZE, "direction_conflict_and_funding_against")

    # A broad high-volatility trend is neither a risk-off veto nor a reason to
    # deploy normal size.  The scoring pipeline has already required trend,
    # breadth, volume and entry geometry; this is the final execution-size
    # discipline for a candidate that reached Paper legitimately.
    if market_regime == "high-volatility trend":
        bump(HALF_SIZE, "high_volatility_trend_reduced_size")
        quality -= 6

    # ---- mode rules (NOT a global score threshold) --------------------------------------------
    modes = cfg.get("modes") or {}
    if mode == "scalp":
        if (modes.get("scalp") or {}).get("disabled", True):
            bump(SHADOW_ONLY, "scalp_disabled_shadow_only")
    elif mode == "swing":
        sw = modes.get("swing") or {}
        full_min = float(sw.get("full_score_min", 70)); half_min = float(sw.get("half_score_min", 65))
        if score is not None:
            if score < half_min and weak_conf:
                bump(SHADOW_ONLY, "swing_low_score_weak_regime")
            elif score < full_min and weak_conf:
                bump(HALF_SIZE, "swing_mid_score_weak_regime")
    # intraday: score is intentionally NOT a cutoff (65-66 not auto-cut, 70-74 not auto-trusted).

    # ---- entry-mode rules ----------------------------------------------------------------------
    em_cfg = ((cfg.get("entry_modes") or {}).get(mode) or {})
    policy = str(em_cfg.get(em) or "")
    if policy == "shadow_only":
        bump(SHADOW_ONLY, f"entry_mode_{em}_shadow_only")
    elif policy == "strong_confirm":
        if not _strong_confirmation(cand, mkt, sym, cfg):
            bump(SHADOW_ONLY if weak_conf else HALF_SIZE, f"entry_mode_{em}_requires_strong_confirmation")
        if mode == "intraday" and not fresh_cat and not _strong_confirmation(cand, mkt, sym, cfg):
            bump(HALF_SIZE, f"entry_mode_{em}_needs_fresh_catalyst_or_market_confirmation")
    elif policy == "cautious":
        bump(HALF_SIZE, f"entry_mode_{em}_cautious")
    elif policy == "swing_confirm":
        if weak_conf:
            bump(HALF_SIZE, f"entry_mode_{em}_needs_swing_regime_confirm")
    # primary / cooldown_dependent: no automatic demote — the regime guard + cooldowns handle risk.

    # ---- intraday regime guard (long into a CONFIRMED failing tape) ----------------------------
    if mode == "intraday" and side == "long" and not unknown:
        r15, r1h = mkt.get("btc_15m_return"), mkt.get("btc_1h_return")
        slope = str(mkt.get("btc_ema_slope_state") or "unknown")
        failing = (r15 is not None and r15 < 0 and r1h is not None and r1h <= 0 and slope in ("down", "flat")
                   and not rvol_ok and sess_q == "weak")
        if failing:
            if em in ("BREAKOUT_CONTINUATION", "LIMIT_THEN_TAKER_TIMEOUT"):
                bump(SHADOW_ONLY, "intraday_regime_guard_failing_tape")
            else:
                bump(HALF_SIZE, "intraday_regime_guard_failing_tape")

    # ---- intraday session gate -----------------------------------------------------------------
    # The latest USD ledger audit showed crypto intraday Asia/off entries were the largest and most
    # persistent drag. Keep weak-session intraday smaller unless the trade has
    # a fresh catalyst or full market confirmation, while preserving forward
    # Paper evidence for the current calibration.
    sg = cfg.get("intraday_session_gate") or {}
    weak_buckets = {str(x).lower() for x in (sg.get("weak_buckets") or ["asia", "off"])}
    if mode == "intraday" and sg.get("enabled", True) and sess_bucket.lower() in weak_buckets:
        if fresh_cat or _strong_confirmation(cand, mkt, sym, cfg):
            bump(str(sg.get("action_with_confirmation", HALF_SIZE)), f"intraday_weak_session_{sess_bucket}_confirmed")
        else:
            bump(str(sg.get("action", SHADOW_ONLY)), f"intraday_weak_session_{sess_bucket}")

    # The forward intraday audit identified a confirmed BTC risk-off state as a
    # distinctly bad long cohort. Keep this deliberately surgical: only a fresh,
    # explicit risk-off classification blocks a new intraday long. Other weak
    # states still use the existing soft session/cooldown rules; missing data is
    # never re-labelled as risk-off.
    rog = cfg.get("intraday_risk_off_gate") or {}
    risk_off_states = {_normalized_regime_state(value, cfg) for value in (
        rog.get("long_regime_states") or ("risk_off", "btc_risk_off"))}
    if (mode == "intraday" and side == "long" and rog.get("enabled", True)
            and mkt.get("status") == "ok"
            and _normalized_regime_state(mkt.get("btc_regime_state"), cfg) in risk_off_states):
        target = str(rog.get("action", BLOCK)).upper()
        # This rule is a genuine Paper veto. A malformed config must not quietly
        # turn it into a size reduction or permit a live/paper candidate.
        if target not in (SHADOW_ONLY, BLOCK):
            target = BLOCK
        bump(target, "intraday_btc_risk_off_long_block")
        quality -= 25

    # ---- derivatives quality gate --------------------------------------------------------------
    # "no-squeeze" was not a positive edge source in the intraday audit. It should not block a good
    # setup by itself, but it also should not carry FULL without fresh catalyst / full confirmation.
    dg = cfg.get("intraday_derivatives_gate") or {}
    deriv = str(cand.get("derivatives_label") or "").lower()
    if mode == "intraday" and dg.get("enabled", True) and deriv == "no-squeeze" \
            and not fresh_cat and not _strong_confirmation(cand, mkt, sym, cfg):
        bump(str(dg.get("no_squeeze_action", HALF_SIZE)), "derivatives_no_squeeze_no_full_without_confirmation")

    # Canonical derivatives guard: only confirmed adverse structure can reduce
    # paper size. Missing/stale data is visible but does not demote a primary
    # setup by itself. It can never increase score/action.
    dq = cfg.get("derivatives_quality_guard") or {}
    if dq.get("enabled", True) and sym.get("derivatives_status") == "ok":
        oi_regime = str(sym.get("oi_price_regime") or "unknown")
        conflict = ((side == "long" and oi_regime == "fresh_shorts") or
                    (side == "short" and oi_regime == "fresh_longs"))
        if conflict:
            bump(str(dq.get("conflicting_oi_price_action", HALF_SIZE)), f"derivatives_{oi_regime}_against_{side}")
            quality -= 8
        funding_spread = _num(sym.get("cross_venue_funding_spread"))
        if funding_spread is not None and funding_spread > float(dq.get("max_cross_venue_funding_spread", 0.001)):
            bump(HALF_SIZE, "derivatives_cross_venue_disagreement")
            quality -= 5

    # Verified on-chain security is a paper-only safety boundary. Hard BLOCK is
    # reserved for independently confirmed critical facts; concentration,
    # mintability and moderate tax can only reduce size. Unknown/stale data is
    # fail-open and never a positive confirmation.
    og = cfg.get("onchain_guard") or {}
    if og.get("enabled", True) and sym.get("paper_guard_eligible") and sym.get("contract_verified"):
        conf = str(sym.get("onchain_data_confidence") or "unknown")
        if og.get("hard_block_verified_honeypot", True) and int(sym.get("honeypot_confirmations") or 0) >= 2:
            bump(BLOCK, "onchain_verified_honeypot")
            quality -= 60
        elif og.get("hard_block_verified_blacklist", True) and int(sym.get("blacklist_confirmations") or 0) >= 2:
            bump(BLOCK, "onchain_verified_blacklist")
            quality -= 50
        sell_tax = _num(sym.get("sell_tax"))
        if sell_tax is not None and sell_tax >= float(og.get("hard_block_sell_tax_pct", 25.0)) \
                and int(sym.get("extreme_sell_tax_confirmations") or 0) >= 2:
            bump(BLOCK, "onchain_verified_extreme_sell_tax")
            quality -= 45
        elif sell_tax is not None and sell_tax >= float(og.get("soft_reduce_sell_tax_pct", 8.0)):
            bump(HALF_SIZE, "onchain_elevated_sell_tax")
            quality -= 12
        if og.get("soft_reduce_mintable", True) and sym.get("mint_risk"):
            bump(HALF_SIZE, "onchain_mintable_contract")
            quality -= 8
        top10 = _num(sym.get("top10_holder_pct"))
        if top10 is not None and top10 >= float(og.get("soft_reduce_top10_holder_pct", 70.0)):
            bump(HALF_SIZE, "onchain_high_holder_concentration")
            quality -= 10

    # Point-in-time event and execution-consistency contexts. Token unlocks are
    # observation-only by default; a confirmed persistent venue divergence is
    # an execution safety guard and may only reduce paper actionability.
    unlock_would = str(sym.get("token_unlock_would_action") or FULL_SIZE)
    unlock_action = str(sym.get("token_unlock_action") or FULL_SIZE)
    if side == "long" and sym.get("token_unlock_status") == "ok":
        if unlock_would != FULL_SIZE:
            reasons.append(f"token_unlock_watch[{sym.get('token_unlock_reason') or unlock_would}]")
        if unlock_action in (HALF_SIZE, SHADOW_ONLY, BLOCK):
            bump(unlock_action, f"token_unlock_guard[{sym.get('token_unlock_reason') or unlock_action}]")
            quality -= 8 if unlock_action == HALF_SIZE else 15

    venue_action = str(sym.get("cross_exchange_action") or FULL_SIZE)
    if sym.get("cross_exchange_status") == "ok" and venue_action in (HALF_SIZE, SHADOW_ONLY, BLOCK):
        bump(venue_action, f"cross_exchange_guard[{sym.get('cross_exchange_reason') or venue_action}]")
        quality -= 8 if venue_action == HALF_SIZE else 15

    # ---- narrow bad-cohort guard (config/cohort_guard.yaml, separate operator sign-off) ----------
    cg = cfg.get("cohort_guard") or {}
    cg_mode = str(cg.get("mode", "off"))
    cg_routing_enabled = bool(cg.get("routing_enabled", False))
    cg_policy = str(cg.get("policy_version") or "cohort_guard_unversioned")
    cg_in_scope = False
    cg_would_demote = False
    if cg.get("enabled") and cg_mode in ("warn", "paper_review_only"):
        cohort = (cg.get("guarded") or {}).get("crypto_intraday_catalyst_or_momentum") or {}
        guarded_modes = {str(x).upper() for x in (cohort.get("guarded_entry_modes") or [])}
        excluded_modes = {str(x).upper() for x in (cohort.get("excluded_entry_modes") or [])}
        cg_in_scope = bool(cohort and mode == "intraday" and side == "long"
                           and em in guarded_modes and em not in excluded_modes)
        if cg_in_scope:
            escape_if_any = {str(x) for x in (cohort.get("escape_if_any") or [])}
            escapes = (("catalyst_confirmed" in escape_if_any and fresh_cat)
                       or ("strong_confirmation" in escape_if_any
                           and _strong_confirmation(cand, mkt, sym, cfg)))
            cg_would_demote = not escapes
            if cg_would_demote:
                if cg_mode == "paper_review_only" and cg_routing_enabled:
                    bump(str(cohort.get("action_when_enabled", SHADOW_ONLY)),
                         "cohort_guard_review[crypto_intraday_unconfirmed_breakout]")
                else:
                    reasons.append("cohort_guard_warn[crypto_intraday_unconfirmed_breakout]")

    # ---- cooldowns -----------------------------------------------------------------------------
    sess_cd = cooldowns.get(("session", mode, session.get("session_bucket_utc")))
    sym_cd = cooldowns.get(("symbol", cand.get("symbol"), mode))
    strong = _strong_confirmation(cand, mkt, sym, cfg)
    if sess_cd and cfg.get("session_cooldown_enabled", True):
        sc = cfg.get("session_cooldown") or {}
        risky_cd = em in ("LIMIT_THEN_TAKER_TIMEOUT", "BREAKOUT_CONTINUATION")
        act = (str(sc.get("action_btc_weak_risky_entry", SHADOW_ONLY)) if (weak_conf and risky_cd)
               else str(sc.get("action", HALF_SIZE)))
        bump(act, f"session_cooldown[{sess_cd['reason']}]")
        quality -= 12
    if sym_cd and cfg.get("symbol_cooldown_enabled", True):
        yc = cfg.get("symbol_cooldown") or {}
        severe_n = int(yc.get("severe_original_stops", 3))
        if _cooldown_stop_count(sym_cd) >= severe_n:
            bump(str(yc.get("action_severe", SHADOW_ONLY)), f"symbol_cooldown_severe[{sym_cd['reason']}]")
        elif strong:
            bump(str(yc.get("action_strong_confirmation", HALF_SIZE)), "cooldown_bypassed_by_strong_confirmation")
        elif weak_conf:
            bump(str(yc.get("action_weak_regime", SHADOW_ONLY)), f"symbol_cooldown_weak_regime[{sym_cd['reason']}]")
        else:
            bump(str(yc.get("action", HALF_SIZE)), f"symbol_cooldown[{sym_cd['reason']}]")
        quality -= 12

    # ---- exposure guard (soft) -----------------------------------------------------------------
    if cfg.get("exposure_guard_enabled", True):
        ex = cfg.get("exposure") or {}
        over_act = str(ex.get("over_limit_action", HALF_SIZE))
        # An exposure cap alone is common and often fine; a weak/unknown/conflicting BTC regime
        # alone is already handled elsewhere. It's the two firing TOGETHER that the 2026-08-10
        # hour-19-UTC audit found toxic (8 of 9 losers), so only that combination gets the
        # stricter action -- a plain exposure hit in a healthy regime still stays at over_act.
        over_act_weak = str(ex.get("over_limit_action_btc_weak", over_act))
        if mode == "swing":
            # Swing is a higher-timeframe lane: a weak/choppy BTC tape should
            # normally reduce size, not erase an otherwise fresh and valid
            # setup. Keep the hard same-symbol conflict below, and keep true
            # BLOCK/SHADOW rules from stale data, invalid geometry, on-chain
            # and venue guards intact.
            over_act_weak = str(ex.get("swing_over_limit_action_btc_weak", HALF_SIZE))
        regime_hot = weak_conf or unknown
        if mode == "intraday" and exposure.get("intraday_open", 0) >= int(ex.get("max_open_crypto_intraday", 4)):
            bump(over_act_weak if regime_hot else over_act, "exposure_max_open_intraday")
            quality -= 8
        if exposure.get("by_symbol_mode", {}).get((cand.get("symbol"), mode), 0) >= int(ex.get("max_open_same_symbol_mode", 1)):
            bump(SHADOW_ONLY, "exposure_same_symbol_mode_conflict")     # hard-ish: already holding this
            quality -= 10
        if _base_symbol(cand.get("symbol")) not in _ALT_MAJORS:
            cap = int(ex.get("max_open_alt_beta_same_direction_btc_weak", 2) if regime_hot
                      else ex.get("max_open_alt_beta_same_direction", 3))
            held = exposure.get("alt_short", 0) if side == "short" else exposure.get("alt_long", 0)
            if held >= cap:
                bump(over_act_weak if regime_hot else over_act, "exposure_alt_beta_same_direction")
                quality -= 8

    # ---- BLOCK only for explicit policy + hard_block_enabled -----------------------------------
    if action == SHADOW_ONLY and cfg.get("hard_block_enabled", False) and policy == "shadow_only" \
            and em == "LIMIT_THEN_TAKER_TIMEOUT" and weak_conf:
        bump(BLOCK, "hard_block_disabled_entry_mode_weak_regime")

    quality = max(0.0, min(100.0, quality))
    verdict = ("STRONG" if quality >= 75 else "OK" if quality >= 55 else "WEAK" if quality >= 35 else "TOXIC")
    baseline = SHADOW_ONLY if (mode == "scalp" and (modes.get("scalp") or {}).get("disabled", True)) else FULL_SIZE
    return OverlayDecision(
        signal_id=str(cand.get("signal_id") or ""), symbol=str(cand.get("symbol") or ""), mode=mode,
        entry_mode=cand.get("entry_mode"), side=side, score=score, timestamp=str(cand.get("timestamp") or ""),
        action=action, baseline_action=baseline, quality_score=quality, verdict=verdict, reasons=reasons,
        ctx={**mkt, **sym, "session_bucket_utc": session.get("session_bucket_utc"),
             "session_quality_state": session.get("session_quality_state"),
             "paper_exposure_intraday_open": exposure.get("intraday_open", 0),
             "paper_exposure_actionable_open": exposure.get("actionable_open", 0),
             "paper_exposure_raw_open_outcomes": exposure.get("raw_open_outcomes", 0),
             "paper_exposure_excluded_nonactionable": exposure.get("excluded_nonactionable", 0),
             "paper_exposure_excluded_terminal": exposure.get("excluded_terminal", 0),
             "symbol_cooldown_state": ("on_cooldown" if sym_cd else "clear"),
             "mode_session_cooldown_state": ("on_cooldown" if sess_cd else "clear"),
             # Persist this point-in-time fact so a later experiment can require the
             # same strong-confirmation gate without reconstructing current market data.
             "strong_confirmation": bool(strong),
             "fresh_catalyst_confirmed": bool(fresh_cat),
             "cohort_guard_policy_version": cg_policy,
             "cohort_guard_mode": cg_mode,
             "cohort_guard_routing_enabled": cg_routing_enabled,
             "cohort_guard_in_scope": bool(cg_in_scope),
             "cohort_guard_would_demote": bool(cg_would_demote)})


# ---- live hook + batch refresh -----------------------------------------------------------------
def decide_for_signal(signal: dict, *, db: str | None = None, fs=None, now=None,
                      cfg: dict | None = None) -> OverlayDecision:
    """LIVE hook (called from the paper-entry path). Fail-conservative: any error → default unknown
    action (never FULL, never crash). Live is never affected regardless of this decision."""
    cfg = cfg or load_cfg()
    cfg_hash = config_hash(cfg)
    now = now or datetime.now(timezone.utc)
    unk = str(cfg.get("default_unknown_data_action", HALF_SIZE))
    if not cfg.get("enabled", True) or not cfg.get("paper_actionability_enabled", True):
        d = OverlayDecision(signal_id=str(signal.get("signal_id") or ""), action=FULL_SIZE,
                            reasons=["overlay_disabled"])
        d.ctx["overlay_config_hash"] = cfg_hash
        return d
    try:
        from src.config import load_config
        path = db or str(load_config().db_path)
        fs = fs or _fs()
        # The ordinary setup label is lookahead-safe and captured at signal
        # creation. A versioned Paper profile may intentionally execute a
        # stricter, causally confirmed mode later (for example LEVEL_HOLD_1BAR).
        # Trust that override only when the profile id and tracker-attached
        # execution mode agree; never trust the post-entry diagnostic label.
        from src.execution.paper_entry_provenance import execution_mode_for_signal
        execution_provenance = execution_mode_for_signal(signal)
        if execution_provenance is not None:
            pre_quality = execution_provenance.data_quality
            pre_mode = execution_provenance.entry_mode
            pre_source = execution_provenance.source
        else:
            from src.execution import preentry_classifier as _preentry
            pre = _preentry.ensure_for_signal(signal, db=path, fs=fs)
            pre_quality = str((pre or {}).get("data_quality") or "unavailable")
            pre_mode = (pre or {}).get("entry_mode") if pre_quality == "ok" else None
            pre_source = str((pre or {}).get("source") or "preentry_unavailable")
        mkt = market_context(now, cfg, fs=fs)
        symc = symbol_context(fs, signal.get("symbol"), signal.get("mode"), cfg, as_of=now, db=path)
        bucket = session_bucket(now, cfg)
        session = {"session_bucket_utc": bucket, "session_quality_state": session_quality(bucket, now, cfg)}
        conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
        try:
            cooldowns = read_cooldowns(conn, now)
            exposure = _exposure_without_current_signal(open_exposure(conn), signal.get("signal_id"))
            labels = _catalyst_labels_for(conn).get(signal.get("signal_id")) or {}
        finally:
            conn.close()
        cand = {"signal_id": signal.get("signal_id"), "symbol": signal.get("symbol"),
                "mode": signal.get("mode"), "side": signal.get("direction"), "score": signal.get("score"),
                "entry_mode": pre_mode,
                "market_regime": signal.get("market_regime"),
                "news_supported": signal.get("news_supported"), "timestamp": now.isoformat(),
                **labels}
        out = evaluate(cand, mkt, symc, session, cooldowns, exposure, cfg)
        out.ctx["entry_mode_source"] = pre_source
        out.ctx["preentry_data_quality"] = pre_quality
        out.ctx["overlay_config_hash"] = cfg_hash
        return out
    except Exception as exc:  # fail-conservative
        return OverlayDecision(signal_id=str(signal.get("signal_id") or ""), symbol=str(signal.get("symbol") or ""),
                               mode=str(signal.get("mode") or ""), action=unk, verdict="WEAK",
                               reasons=[f"overlay_error:{type(exc).__name__}"],
                               ctx={"status": "error", "overlay_config_hash": cfg_hash})


def persist_point_in_time_decision(decision: OverlayDecision, *, db: str | None = None) -> bool:
    """Persist the first actual paper-entry overlay decision without overwriting it.

    The regular decisions table is a mutable current-context dashboard.  This
    separate append-once snapshot is the audit record for the decision that was
    available at the paper alert itself.
    """
    from src.config import load_config
    path = db or str(load_config().db_path)
    f = decision.fields()
    sid = str(f.get("signal_id") or "")
    if not sid:
        return False
    row = (sid, f.get("quality_action"), f.get("entry_mode"), f.get("entry_mode_source"),
           f.get("preentry_data_quality"), f.get("overlay_version"), f.get("quality_reasons_json"),
           f.get("overlay_config_hash"), json.dumps(f, sort_keys=True),
           datetime.now(timezone.utc).isoformat(), "point_in_time")
    conn = sqlite3.connect(path)
    try:
        ensure_tables(conn)
        cur = conn.execute(
            "INSERT OR IGNORE INTO crypto_quality_overlay_decision_snapshots "
            "(signal_id,quality_action,entry_mode,entry_mode_source,preentry_data_quality,overlay_version,"
            "quality_reasons_json,overlay_config_hash,decision_json,decided_at,decision_context_type) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?)", row)
        conn.commit()
        return bool(cur.rowcount)
    finally:
        conn.close()


def persist_context_filter_decisions(decision: OverlayDecision, *, db_path=None,
                                     decided_at: datetime | None = None) -> int:
    """Persist isolated per-filter evidence in the intelligence sidecar."""
    from src.intelligence.context_store import connect, insert_named
    decided_at = decided_at or datetime.now(timezone.utc)
    fields = decision.fields()
    sid = str(fields.get("signal_id") or "")
    if not sid:
        return 0
    cols = ("signal_id", "filter_name", "filter_version", "decision_at", "context_ts",
            "action", "reason", "shadow_only", "features_json")
    blocks = (
        ("token_unlock", "token_unlock_v1", fields.get("token_unlock_context_ts"),
         fields.get("token_unlock_would_action") or FULL_SIZE,
         fields.get("token_unlock_reason"), 1,
         {k: v for k, v in fields.items() if k.startswith("token_unlock_")}),
        ("cross_exchange_consistency", "cross_exchange_v1", fields.get("cross_exchange_context_ts"),
         fields.get("cross_exchange_action") or FULL_SIZE,
         fields.get("cross_exchange_reason"), 0,
         {k: v for k, v in fields.items() if k.startswith("cross_exchange_")}),
        ("crypto_iv_rv", "crypto_iv_rv_v1", fields.get("options_context_ts"), FULL_SIZE,
         "advisory_only", 1,
         {k: v for k, v in fields.items() if k.startswith("options_")}),
    )
    written = 0
    with connect(db_path) as conn:
        for name, version, context_ts, action, reason, shadow_only, features in blocks:
            row = {"signal_id": sid, "filter_name": name, "filter_version": version,
                   "decision_at": decided_at.isoformat(), "context_ts": context_ts,
                   "action": action, "reason": reason, "shadow_only": shadow_only,
                   "features_json": features}
            written += int(insert_named(conn, "context_filter_decisions", row, cols))
        conn.commit()
    return written


def refresh(*, lookback_hours: float = 336.0, persist: bool = True, db: str | None = None,
            now_iso: str | None = None) -> dict[str, Any]:
    """Batch: (re)evaluate recent crypto signals with CURRENT context → persist read-model decisions.
    Refreshes cooldowns first. Writes ONLY crypto_quality_overlay_decisions / crypto_quality_cooldowns."""
    from src.config import load_config
    cfg = load_cfg()
    path = db or str(load_config().db_path)
    now = datetime.fromisoformat(now_iso) if now_iso else datetime.now(timezone.utc)
    refresh_cooldowns(db=path, now_iso=now.isoformat())
    fs = _fs()
    counts = {"evaluated": 0, "FULL_SIZE": 0, "HALF_SIZE": 0, "SHADOW_ONLY": 0, "BLOCK": 0, "blocked": 0}
    conn = sqlite3.connect(path)
    try:
        ensure_tables(conn)          # creates + idempotently migrates (adds decision_context_type)
        conn.commit()
        if not _has(conn, "proposed_signals"):
            return counts
        em_map = _entry_mode_for(conn)
        labels_map = _catalyst_labels_for(conn)
        cooldowns = read_cooldowns(conn, now)
        exposure = open_exposure(conn)
        mkt = market_context(now, cfg, fs=fs)
        symbol_context_cache: dict[str, dict] = {}
        rows = conn.execute(
            "SELECT signal_id, symbol, mode, direction, score, news_supported, created_at "
            "FROM proposed_signals WHERE asset_class='crypto' AND created_at >= ? "
            "ORDER BY created_at DESC LIMIT 500", ((now - timedelta(hours=lookback_hours)).isoformat(),)).fetchall()
        for row_index, (sid, sym, mode, direction, score, news, created) in enumerate(rows, start=1):
            # Current-snapshot batch rows sharing a symbol also share the same
            # derivatives/on-chain/RVOL context. Avoid hundreds of identical
            # SQLite + OHLCV reads; the live point-in-time hook remains uncached.
            if sym not in symbol_context_cache:
                symbol_context_cache[sym] = symbol_context(fs, sym, mode, cfg, db=path)
            symc = symbol_context_cache[sym]
            bucket = session_bucket(now, cfg)
            session = {"session_bucket_utc": bucket, "session_quality_state": session_quality(bucket, now, cfg)}
            cand = {"signal_id": sid, "symbol": sym, "mode": mode, "side": direction, "score": score,
                    "entry_mode": em_map.get(sid), "news_supported": news, "timestamp": created,
                    **(labels_map.get(sid) or {})}
            candidate_exposure = _exposure_without_current_signal(exposure, sid)
            d = evaluate(cand, mkt, symc, session, cooldowns, candidate_exposure, cfg)
            d.ctx["overlay_config_hash"] = config_hash(cfg)
            counts["evaluated"] += 1
            counts[d.action] = counts.get(d.action, 0) + 1
            if d.action == BLOCK:
                counts["blocked"] += 1
            if persist:
                f = d.fields()
                # decisions written by refresh() are a CURRENT routing snapshot (context = now), NOT
                # lookahead-safe historical evidence — the resolver never uses these to size a trade.
                f["computed_at"] = now.isoformat()
                f["decision_context_type"] = "current_snapshot"
                # explicit column list so a future nullable column never breaks the write.
                conn.execute(
                    "INSERT OR REPLACE INTO crypto_quality_overlay_decisions ("
                    + ",".join(_DECISION_COLS) + ") VALUES (" + ",".join("?" * len(_DECISION_COLS)) + ")",
                    tuple(f[k] for k in _DECISION_COLS))
                if row_index % 25 == 0:
                    conn.commit()
        if persist:
            conn.commit()
        counts["generated_at"] = now.isoformat()
        return counts
    finally:
        conn.close()


# ---- cohort-guard forward evidence --------------------------------------------------------------
def _cohort_slice_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    vals = [float(r["paper_execution_r"]) for r in rows if r.get("paper_execution_r") is not None]
    gross_profit = sum(v for v in vals if v > 0)
    gross_loss = -sum(v for v in vals if v < 0)
    return {
        "resolved": len(vals),
        "wins": sum(v > 0 for v in vals),
        "losses": sum(v < 0 for v in vals),
        "breakeven": sum(v == 0 for v in vals),
        "win_rate": round(100 * sum(v > 0 for v in vals) / len(vals), 1) if vals else None,
        "net_r": round(sum(vals), 4),
        "avg_r": round(sum(vals) / len(vals), 4) if vals else None,
        "profit_factor": (round(gross_profit / gross_loss, 4) if gross_loss else
                          ("inf" if gross_profit else None)),
    }


def _cohort_guard_evidence(conn: sqlite3.Connection, cfg: dict[str, Any]) -> dict[str, Any]:
    """Forward-only evidence from immutable point-in-time decisions created by this policy version.

    Mutable current snapshots and pre-v2/backfill rows are intentionally excluded. The result may
    recommend operator review, but it never flips the routing mode automatically.
    """
    cg = cfg.get("cohort_guard") or {}
    policy = str(cg.get("policy_version") or "cohort_guard_unversioned")
    gate = cg.get("evidence_gate") or {}
    out: dict[str, Any] = {
        "mode": str(cg.get("mode", "off")),
        "routing_enabled": bool(cg.get("routing_enabled", False)),
        "policy_version": policy,
        "evidence_source": str(gate.get("evidence_source") or "point_in_time_post_v2"),
        "min_resolved_forward": int(gate.get("min_resolved_forward", 30)),
        "profit_factor_max": float(gate.get("profit_factor_max", 0.8)),
        "require_negative_avg_r": bool(gate.get("require_negative_avg_r", True)),
        "eligible_rows": 0,
        "slices": [],
    }
    needed = ("crypto_quality_overlay_decision_snapshots", "proposed_signals",
              "paper_execution_outcomes")
    if not all(_has(conn, t) for t in needed):
        out.update({"activation_verdict": "NO_FORWARD_EVIDENCE", "target": _cohort_slice_metrics([])})
        return out
    try:
        raw = conn.execute(
            "SELECT s.signal_id,s.decision_json,p.created_at,o.paper_execution_r,"
            "o.paper_execution_outcome,o.evidence_class,"
            "COALESCE(NULLIF(o.economic_trade_key,''),s.signal_id) economic_trade_key "
            "FROM crypto_quality_overlay_decision_snapshots s "
            "JOIN proposed_signals p ON p.signal_id=s.signal_id "
            "JOIN paper_execution_outcomes o ON o.signal_id=s.signal_id "
            "WHERE s.decision_context_type='point_in_time' "
            "AND lower(COALESCE(p.asset_class,''))='crypto' "
            "AND lower(COALESCE(p.mode,''))='intraday' "
            "AND lower(COALESCE(p.direction,''))='long' "
            "AND o.evidence_class='forward_postfreeze' "
            "AND o.paper_execution_outcome IN ('win','loss','breakeven') "
            "ORDER BY p.created_at DESC,s.signal_id"
        ).fetchall()
    except sqlite3.OperationalError:
        out.update({"activation_verdict": "NO_FORWARD_EVIDENCE", "target": _cohort_slice_metrics([])})
        return out

    rows: list[dict[str, Any]] = []
    seen_keys: set[str] = set()
    for sid, decision_json, created_at, r_value, outcome, evidence_class, trade_key in raw:
        try:
            decision = json.loads(decision_json or "{}")
        except (TypeError, ValueError):
            continue
        if str(decision.get("cohort_guard_policy_version") or "") != policy:
            continue
        key = str(trade_key or sid)
        if key in seen_keys:
            continue
        seen_keys.add(key)
        rows.append({
            "signal_id": sid,
            "created_at": created_at,
            "entry_mode": str(decision.get("entry_mode") or "UNKNOWN").upper(),
            "fresh_catalyst": bool(decision.get("fresh_catalyst_confirmed")),
            "in_scope": bool(decision.get("cohort_guard_in_scope")),
            "would_demote": bool(decision.get("cohort_guard_would_demote")),
            "paper_execution_r": r_value,
            "outcome": outcome,
            "evidence_class": evidence_class,
        })

    out["eligible_rows"] = len(rows)
    for entry_mode in sorted({r["entry_mode"] for r in rows}):
        for catalyst in (False, True):
            part = [r for r in rows if r["entry_mode"] == entry_mode
                    and r["fresh_catalyst"] is catalyst]
            if part:
                out["slices"].append({
                    "entry_mode": entry_mode,
                    "catalyst": "fresh" if catalyst else "no_fresh",
                    **_cohort_slice_metrics(part),
                })

    target_rows = [r for r in rows if r["in_scope"] and r["would_demote"]]
    target = _cohort_slice_metrics(target_rows)
    out["target"] = target
    n = int(target.get("resolved") or 0)
    pf = target.get("profit_factor")
    avg_r = target.get("avg_r")
    if not rows:
        verdict = "NO_FORWARD_EVIDENCE"
    elif n < out["min_resolved_forward"]:
        verdict = "INSUFFICIENT_FORWARD_SAMPLE"
    else:
        pf_weak = isinstance(pf, (int, float)) and pf <= out["profit_factor_max"]
        avg_weak = (avg_r is not None and avg_r < 0) if out["require_negative_avg_r"] else True
        verdict = "ELIGIBLE_FOR_OPERATOR_REVIEW" if pf_weak and avg_weak else "NOT_ELIGIBLE"
    out["activation_verdict"] = verdict
    return out


# ---- report / API summary ----------------------------------------------------------------------
def report_data(*, db: str | None = None, now_iso: str | None = None) -> dict[str, Any]:
    """Read-only summary for the CLI report + the control-plane 'Crypto Quality Overlay' card:
    decision mix, active cooldowns, worst symbols, weak sessions, and 2d/7d/14d counterfactual."""
    from src.config import load_config
    path = db or str(load_config().db_path)
    now = datetime.fromisoformat(now_iso) if now_iso else datetime.now(timezone.utc)
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    cfg = load_cfg()
    out: dict[str, Any] = {"overlay_version": VERSION, "generated_at": now.isoformat()}
    try:
        if _has(conn, "crypto_quality_overlay_decisions"):
            out["action_mix"] = dict(conn.execute(
                "SELECT quality_action, COUNT(*) FROM crypto_quality_overlay_decisions "
                "GROUP BY quality_action").fetchall())
            out["top_reasons"] = conn.execute(
                "SELECT quality_reasons_json, COUNT(*) c FROM crypto_quality_overlay_decisions "
                "WHERE quality_action!='FULL_SIZE' GROUP BY quality_reasons_json ORDER BY c DESC LIMIT 8"
            ).fetchall()
        else:
            out["action_mix"] = {}
        out["cohort_guard"] = _cohort_guard_evidence(conn, cfg)
        if _has(conn, "crypto_quality_cooldowns"):
            cds = read_cooldowns(conn, now)
            out["active_session_cooldowns"] = [f"{m}/{b} ({d['reason']})" for (t, m, b), d in cds.items() if t == "session"]
            out["active_symbol_cooldowns"] = [f"{s}/{m} ({d['reason']})" for (t, s, m), d in cds.items() if t == "symbol"]
            out["worst_symbols"] = conn.execute(
                "SELECT affected_symbol, affected_mode, recent_original_stop_count, recent_net_pnl_usd "
                "FROM crypto_quality_cooldowns WHERE cooldown_type='symbol' AND cooldown_active=1 "
                "ORDER BY recent_net_pnl_usd ASC LIMIT 8").fetchall()
    finally:
        conn.close()
    try:
        from src.execution import crypto_overlay_counterfactual as _cf
        out["counterfactual"] = _cf.window_summaries(db=path, now_iso=now.isoformat())
    except Exception as exc:  # noqa: BLE001
        out["counterfactual"] = {"error": str(exc)}
    return out


def render_markdown(*, db: str | None = None, now_iso: str | None = None) -> str:
    d = report_data(db=db, now_iso=now_iso)
    L = [f"# Crypto Quality Overlay — {d['overlay_version']} ({d['generated_at']})", "",
         "> PAPER / READ-MODEL. Soft sizing/routing breaker for crypto paper candidates. Live LOCKED; "
         "signal generation / tier / final_r untouched. Only ever downgrades (never upgrades).", "",
         "## Decision mix (recent crypto signals)"]
    mix = d.get("action_mix") or {}
    L += [f"- {k}: {v}" for k, v in sorted(mix.items(), key=lambda kv: -kv[1])] or ["- _none_"]
    cg = d.get("cohort_guard") or {}
    L += ["", "## Crypto intraday cohort guard (forward-only)",
          f"- routing mode: **{cg.get('mode', 'off')}**; policy: `{cg.get('policy_version', '-')}`",
          f"- second routing key enabled: **{cg.get('routing_enabled', False)}**",
          f"- activation verdict: **{cg.get('activation_verdict', 'NO_FORWARD_EVIDENCE')}**",
          f"- narrow target resolved: **{(cg.get('target') or {}).get('resolved', 0)} / "
          f"{cg.get('min_resolved_forward', 30)}**",
          "- only append-once point-in-time post-v2 decisions count; current snapshots and backfill do not"]
    slices = cg.get("slices") or []
    if slices:
        L += ["", "| entry mode | catalyst | resolved | WR | PF | net R | avg R |",
              "|---|---|---:|---:|---:|---:|---:|"]
        for s in slices:
            L.append(f"| {s.get('entry_mode')} | {s.get('catalyst')} | {s.get('resolved', 0)} | "
                     f"{s.get('win_rate')} | {s.get('profit_factor')} | {s.get('net_r', 0):+.2f} | "
                     f"{s.get('avg_r')} |")
    cf = d.get("counterfactual") or {}
    if "error" not in cf:
        L += ["", "## Counterfactual (baseline full-size vs overlay) — avoided loss vs missed profit"]
        L.append("_net Δ USD conflates two different things: HALF_SIZE mechanically halving a winning "
                  "cohort's dollar total looks the same as a genuinely bad call. avoided-loss $ / "
                  "missed-profit $ split those apart so a guard that's net-negative because it protects "
                  "against real losses isn't judged the same as one that's just cutting winners._")
        L.append("| window | net Δ USD | avoided-loss $ | missed-profit $ | PF base→overlay | orig-stop red. | missed tp3 runners | missed winners | trade Δ |")
        L.append("|---|---|---|---|---|---|---|---|---|")
        for key, lab in (("d2", "48h"), ("d7", "7d"), ("d14", "14d"), ("all", "all")):
            s = cf.get(key) or {}
            L.append(f"| {lab} | {s.get('net_overlay_delta_usd', 0):+.0f} | "
                     f"{s.get('avoided_loss_usd', 0):+.0f} | {s.get('missed_profit_usd', 0):+.0f} | "
                     f"{s.get('baseline_pf')}→{s.get('overlay_pf')} | "
                     f"{s.get('original_stop_reduction', 0)}/{s.get('baseline_original_stops', 0)} | "
                     f"{s.get('missed_tp3_runners', 0)}/{s.get('total_tp3_runners', 0)} | "
                     f"{s.get('missed_winners', 0)} | {s.get('trade_count_delta', 0)} |")
        _all = cf.get("all") or {}
        _no_baseline = (_all.get("evaluated", 0) or 0) - (_all.get("with_usd", 0) or 0)
        if _no_baseline:
            L += ["", f"**⚠ SHADOW_ONLY blind spot:** {_no_baseline} of {_all.get('evaluated', 0)} all-time "
                  "evaluated trades have NO visible baseline (mostly SHADOW_ONLY routing, which writes no "
                  "paper_portfolio_ledger row) and are excluded from every number above. avoided-loss $ is "
                  "therefore a floor, not the true total prevented loss -- SHADOW_ONLY's real counterfactual "
                  "impact is currently unmeasured, not zero."]
        L += ["", "_Evidence-class split (Model F): only forward_postfreeze is proof the underlying trades are "
              "profitable — backfill_pretrained is the same in-sample data that chose Model F's own thresholds "
              "and must never be read as \"profitable\"; unclassified predates the evidence_class column._"]
        L.append("| window | forward_postfreeze n/resolved/netR | backfill_pretrained n/resolved/netR | unclassified n |")
        L.append("|---|---|---|---|")
        for key, lab in (("d2", "48h"), ("d7", "7d"), ("d14", "14d"), ("all", "all")):
            s = cf.get(key) or {}
            fwd = s.get("evidence_forward_postfreeze") or {}
            bfd = s.get("evidence_backfill_pretrained") or {}
            unc = s.get("evidence_unclassified") or {}
            fwd_r = fwd.get("net_r_sum"); bfd_r = bfd.get("net_r_sum")
            L.append(f"| {lab} | {fwd.get('n', 0)}/{fwd.get('resolved', 0)}/"
                     f"{'-' if fwd_r is None else f'{fwd_r:+.2f}'} | "
                     f"{bfd.get('n', 0)}/{bfd.get('resolved', 0)}/"
                     f"{'-' if bfd_r is None else f'{bfd_r:+.2f}'} | "
                     f"{unc.get('n', 0)} |")
    L += ["", f"## Active session cooldowns: {len(d.get('active_session_cooldowns') or [])}"]
    L += [f"- {x}" for x in (d.get("active_session_cooldowns") or [])[:12]] or ["- _none_"]
    L += ["", f"## Active symbol cooldowns: {len(d.get('active_symbol_cooldowns') or [])}"]
    L += [f"- {x}" for x in (d.get("active_symbol_cooldowns") or [])[:15]] or ["- _none_"]
    ws = d.get("worst_symbols") or []
    if ws:
        L += ["", "## Worst current symbols (on cooldown, by recent paper USD)"]
        L += [f"- {r[0]}/{r[1]}: {int(r[2] or 0)} stops, net {r[3]:+.0f} USD" for r in ws]
    return "\n".join(L)


def write_report(*, db: str | None = None, now_iso: str | None = None, md: str | None = None) -> str:
    """md: pass an already-computed render_markdown() result to avoid recomputing it (this report's
    render is expensive -- see load_config caching note in src/config.py). Only used by this
    module's one caller (src/cli.py's crypto-overlay-report command); omit for standalone use."""
    if md is None:
        md = render_markdown(db=db, now_iso=now_iso)
    out = _ROOT / "reports" / "CRYPTO_QUALITY_OVERLAY.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md, encoding="utf-8")
    return str(out)


__all__ = ["load_cfg", "decide_for_signal", "persist_point_in_time_decision", "evaluate", "refresh", "refresh_cooldowns", "read_cooldowns",
           "report_data", "render_markdown", "write_report",
           "compute_cooldowns", "open_exposure", "market_context", "symbol_context", "session_bucket",
           "session_quality", "OverlayDecision", "VERSION", "ACTIVE_FEE_PROFILE",
           "FULL_SIZE", "HALF_SIZE", "SHADOW_ONLY", "BLOCK"]
