"""Isolated stock-intraday entry refinements for Shadow research only.

The active Paper stock intraday lane is intentionally not imported or changed
here.  This module scouts a separate, liquid universe and evaluates four
confirmed-close profiles against the same stock costs and Model-F protection
used by Paper.  It never writes ``proposed_signals``, ``signal_outcomes``,
``final_r`` or a Paper ledger table.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import pandas as pd

from src.config import load_config
from src.execution.paper_shadow_engine import _trim_stock_intraday_to_rth
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
from src.stocks.market_calendar import is_us_cash_session_open, us_cash_session_close


ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "config" / "shadow_stocks_intraday_variants.yaml"
STRATEGY_KEY = "stocks_intraday_variants"

DEFAULTS: dict[str, Any] = {
    "feature_flag": False,
    "strategy_id": "stocks_intraday_variants_v1",
    "shadow_lane": "shadow_stocks_intraday_variants",
    "fee_profile": "stock_etf_default",
    "timeframe": "15m",
    "refresh_min_interval_minutes": 15,
    "min_clean_closed": 30,
    "min_forward_days": 28,
    "min_profit_factor": 1.25,
    "max_review_drawdown_usd": 250.0,
    "shadow_symbols": [],
    "profiles": [],
    "report_path": "reports/STOCKS_INTRADAY_VARIANTS_SHADOW.md",
}

REJECTION_REASONS = {
    "OUTSIDE_RTH",
    "PRE_GATE_NOT_AB",
    "SETUP_MISSING",
    "GEOMETRY_INVALID",
    "STOCK_BARS_MISSING",
    "DATA_COVERAGE_DIRTY",
    "VWAP_HOLD_NOT_CONFIRMED",
    "BREAKOUT_CONFIRM_NOT_REACHED",
    "BREAKOUT_RETEST_NOT_CONFIRMED",
    "NO_FUTURE_BARS",
    "MARKET_CONTEXT_UNAVAILABLE",
    "SECTOR_CONTEXT_UNAVAILABLE",
    "MARKET_CONTEXT_NOT_CONFIRMED",
    "SECTOR_CONTEXT_NOT_CONFIRMED",
    "CONFIRMATION_ATR_UNAVAILABLE",
    "CONFIRMATION_BODY_TOO_WEAK",
    "CONFIRMATION_CLOSE_TOO_WEAK",
    "CONFIRMATION_RVOL_UNAVAILABLE",
    "CONFIRMATION_RVOL_TOO_LOW",
    "ENTRY_TOO_EXTENDED",
    "STOP_TOO_WIDE",
}

OUTCOME_COLUMNS = (
    "candidate_id", "strategy_id", "profile_id", "shadow_lane", "window", "generated_at",
    "decision_at", "source_candidate_at", "symbol", "direction", "entry_mode", "rule_name",
    "source_tier", "market_context_status", "sector_confirmation_status", "context_group",
    "session_phase", "liquidity_status", "catalyst_quality", "sector", "sector_etf",
    "eligibility_status", "rejection_reason", "data_status", "is_clean_for_edge", "entry_ts",
    "entry_price", "stop_price", "tp1", "tp2", "tp3", "outcome_status", "close_reason",
    "exit_price", "exit_ts", "gross_pnl_usd", "net_pnl_usd", "net_r", "fees_usd",
    "slippage_usd", "funding_usd", "funding_source", "funding_estimated", "funding_event_count",
    "risk_usd", "mfe_r", "mae_r", "protection_armed", "lock_armed", "highest_tp_touched",
    "bars_held", "latency_seconds", "features_json", "notes_json",
)

OUTCOME_DDL = """
CREATE TABLE IF NOT EXISTS stocks_intraday_variant_shadow_outcomes (
  candidate_id TEXT PRIMARY KEY, strategy_id TEXT NOT NULL, profile_id TEXT NOT NULL,
  shadow_lane TEXT NOT NULL, window TEXT NOT NULL, generated_at TEXT NOT NULL,
  decision_at TEXT NOT NULL, source_candidate_at TEXT, symbol TEXT NOT NULL, direction TEXT NOT NULL,
  entry_mode TEXT NOT NULL, rule_name TEXT NOT NULL, source_tier TEXT, market_context_status TEXT,
  sector_confirmation_status TEXT, context_group TEXT, session_phase TEXT, liquidity_status TEXT,
  catalyst_quality TEXT, sector TEXT, sector_etf TEXT, eligibility_status TEXT NOT NULL,
  rejection_reason TEXT, data_status TEXT NOT NULL, is_clean_for_edge INTEGER NOT NULL DEFAULT 0,
  entry_ts TEXT, entry_price REAL, stop_price REAL, tp1 REAL, tp2 REAL, tp3 REAL,
  outcome_status TEXT, close_reason TEXT, exit_price REAL, exit_ts TEXT, gross_pnl_usd REAL,
  net_pnl_usd REAL, net_r REAL, fees_usd REAL, slippage_usd REAL, funding_usd REAL,
  funding_source TEXT, funding_estimated INTEGER, funding_event_count INTEGER, risk_usd REAL,
  mfe_r REAL, mae_r REAL, protection_armed INTEGER, lock_armed INTEGER, highest_tp_touched INTEGER,
  bars_held INTEGER, latency_seconds REAL, features_json TEXT NOT NULL, notes_json TEXT NOT NULL
)
"""
EVAL_DDL = """
CREATE TABLE IF NOT EXISTS stocks_intraday_variant_shadow_evaluations (
  generated_at TEXT NOT NULL, profile_id TEXT NOT NULL, strategy_id TEXT NOT NULL,
  shadow_lane TEXT NOT NULL, activated_at TEXT, forward_rows INTEGER, clean_rows INTEGER,
  dirty_rows INTEGER, clean_closed INTEGER, net_pnl_usd REAL, net_r REAL, fees_usd REAL,
  slippage_usd REAL, funding_usd REAL, profit_factor REAL, winrate REAL,
  max_drawdown_usd REAL, forward_days REAL, verdict TEXT, rejection_counts_json TEXT NOT NULL,
  diagnostics_json TEXT NOT NULL, config_json TEXT NOT NULL,
  PRIMARY KEY (generated_at, profile_id)
)
"""
META_DDL = """CREATE TABLE IF NOT EXISTS stocks_intraday_variant_shadow_meta (
  k TEXT PRIMARY KEY, v TEXT NOT NULL
)"""


def load_strategy_config() -> dict[str, Any]:
    cfg = load_yaml_block(CONFIG_PATH, STRATEGY_KEY, DEFAULTS)
    cfg["profiles"] = [dict(x) for x in cfg.get("profiles") or [] if isinstance(x, dict)]
    cfg["shadow_symbols"] = [str(x).upper() for x in cfg.get("shadow_symbols") or []]
    return cfg


def ensure_tables(conn: sqlite3.Connection) -> None:
    conn.execute(OUTCOME_DDL)
    conn.execute(EVAL_DDL)
    conn.execute(META_DDL)
    text_columns = {
        "strategy_id", "profile_id", "shadow_lane", "window", "generated_at", "decision_at",
        "source_candidate_at", "symbol", "direction", "entry_mode", "rule_name", "source_tier",
        "market_context_status", "sector_confirmation_status", "context_group", "session_phase",
        "liquidity_status", "catalyst_quality", "sector", "sector_etf", "eligibility_status",
        "rejection_reason", "data_status", "entry_ts", "outcome_status", "close_reason", "exit_ts",
        "funding_source", "features_json", "notes_json",
    }
    int_columns = {"is_clean_for_edge", "funding_estimated", "funding_event_count", "protection_armed",
                   "lock_armed", "highest_tp_touched", "bars_held"}
    ensure_columns(conn, "stocks_intraday_variant_shadow_outcomes", {
        col: ("TEXT" if col in text_columns else "INTEGER" if col in int_columns else "REAL")
        for col in OUTCOME_COLUMNS if col != "candidate_id"
    })
    conn.execute("CREATE INDEX IF NOT EXISTS idx_sivso_profile_window ON "
                 "stocks_intraday_variant_shadow_outcomes(profile_id,window,is_clean_for_edge,outcome_status)")


def _float(value: Any) -> float | None:
    try:
        return None if value in (None, "") else float(value)
    except (TypeError, ValueError):
        return None


def _candidate_id(strategy: str, profile: str, symbol: str, source_at: str, setup: dict[str, Any]) -> str:
    observed = parse_dt(source_at)
    session = (observed.astimezone(ZoneInfo("America/New_York")).date().isoformat()
               if observed else str(source_at)[:10])
    # One profile/symbol is one candidate per NY cash session.  The first
    # captured setup is retained below and later passes merely mature its
    # outcome. This prevents a moving technical level from becoming several
    # pseudo-independent trades in the same session.
    raw = f"{strategy}|{profile}|{symbol}|{session}"
    return "siv_" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]


def _context_group(raw: dict[str, Any]) -> str:
    gate = raw.get("intraday_actionability") or {}
    market = str(gate.get("market_context_status") or "unknown").lower() in {"ok", "confirmed"}
    sector = str(gate.get("sector_confirmation_status") or "unknown").lower() == "confirmed"
    if market and sector:
        return "market_and_sector_confirmed"
    if market:
        return "market_only"
    if sector:
        return "sector_only"
    return "neither_or_unknown"


def _rth(frame: pd.DataFrame) -> pd.DataFrame:
    out = normalize_frame(frame)
    if out.empty:
        return out
    ny = out["timestamp"].dt.tz_convert("America/New_York")
    mask = ((ny.dt.weekday < 5)
            & ((ny.dt.hour > 9) | ((ny.dt.hour == 9) & (ny.dt.minute >= 30)))
            & (ny.dt.hour < 16))
    return out.loc[mask].reset_index(drop=True)


def _coverage_clean(frame: pd.DataFrame, minutes: int) -> bool:
    if len(frame) < 2:
        return False
    gaps = frame["timestamp"].sort_values().diff().dropna().dt.total_seconds() / 60.0
    return bool(gaps.empty or float(gaps.max()) <= minutes * 2.1)


def _vwap(frame: pd.DataFrame, through_idx: int) -> float | None:
    part = frame.iloc[:through_idx + 1]
    if part.empty or "volume" not in part or float(part["volume"].fillna(0).sum()) <= 0:
        return None
    typical = (part["high"].astype(float) + part["low"].astype(float) + part["close"].astype(float)) / 3.0
    return float((typical * part["volume"].astype(float)).sum() / part["volume"].astype(float).sum())


def _same_side(direction: str, price: float, level: float) -> bool:
    return price >= level if direction == "long" else price <= level


def _inside_or_touches(direction: str, row: pd.Series, low: float, high: float) -> bool:
    return float(row["low"]) <= high if direction == "long" else float(row["high"]) >= low


def _atr(frame: pd.DataFrame, idx: int, lookback: int = 14) -> float | None:
    """Point-in-time ATR from bars available at the confirmation close."""
    start = max(0, int(idx) - max(1, int(lookback)) + 1)
    part = frame.iloc[start:int(idx) + 1]
    if part.empty:
        return None
    highs = pd.to_numeric(part["high"], errors="coerce")
    lows = pd.to_numeric(part["low"], errors="coerce")
    closes = pd.to_numeric(part["close"], errors="coerce")
    prev = closes.shift(1)
    tr = pd.concat([(highs - lows).abs(), (highs - prev).abs(), (lows - prev).abs()], axis=1).max(axis=1)
    value = float(tr.dropna().mean()) if not tr.dropna().empty else 0.0
    return value if value > 0 else None


def _confirmation_quality(
    *, profile: dict[str, Any], frame: pd.DataFrame, idx: int, direction: str,
    trigger: float, stop: float,
) -> tuple[dict[str, float] | None, str | None]:
    """Validate optional point-in-time candle quality for strict research profiles.

    The baseline profiles deliberately do not call this helper.  This makes the
    quality profiles a clean paired experiment rather than a silent rewrite of
    the existing Paper-compatible Shadow control.
    """
    quality_keys = {
        "min_body_atr", "min_close_location", "min_rvol", "rvol_lookback",
        "max_trigger_extension_atr", "max_stop_atr",
    }
    if not any(key in profile for key in quality_keys):
        return {}, None
    row = frame.iloc[int(idx)]
    open_px, high, low, close = (_float(row.get(key)) for key in ("open", "high", "low", "close"))
    if None in {open_px, high, low, close} or high <= low:
        return None, "CONFIRMATION_BODY_TOO_WEAK"
    atr = _atr(frame, idx, int(profile.get("atr_lookback") or 14))
    if atr is None:
        return None, "CONFIRMATION_ATR_UNAVAILABLE"
    long = direction == "long"
    body = abs(close - open_px)
    close_location = ((close - low) / (high - low)) if long else ((high - close) / (high - low))
    if (long and close < open_px) or ((not long) and close > open_px):
        return None, "CONFIRMATION_BODY_TOO_WEAK"
    if body / atr < float(profile.get("min_body_atr") or 0.0):
        return None, "CONFIRMATION_BODY_TOO_WEAK"
    if close_location < float(profile.get("min_close_location") or 0.0):
        return None, "CONFIRMATION_CLOSE_TOO_WEAK"
    lookback = max(1, int(profile.get("rvol_lookback") or 8))
    prior = pd.to_numeric(frame.iloc[max(0, int(idx) - lookback):int(idx)]["volume"], errors="coerce").dropna()
    volume = _float(row.get("volume"))
    if "min_rvol" in profile:
        if prior.empty or float(prior.median()) <= 0 or volume is None:
            return None, "CONFIRMATION_RVOL_UNAVAILABLE"
        if volume / float(prior.median()) < float(profile["min_rvol"]):
            return None, "CONFIRMATION_RVOL_TOO_LOW"
    extension = abs(close - trigger) / atr
    if extension > float(profile.get("max_trigger_extension_atr", float("inf"))):
        return None, "ENTRY_TOO_EXTENDED"
    if abs(close - stop) / atr > float(profile.get("max_stop_atr", float("inf"))):
        return None, "STOP_TOO_WIDE"
    return {
        "atr": round(atr, 8), "body_atr": round(body / atr, 8),
        "close_location": round(close_location, 8), "trigger_extension_atr": round(extension, 8),
        "stop_distance_atr": round(abs(close - stop) / atr, 8),
        "rvol": (round(volume / float(prior.median()), 8) if not prior.empty and volume is not None else None),
    }, None


def _requires_confirmed_context(profile: dict[str, Any]) -> bool:
    return bool(profile.get("require_market_sector_confirmed", False))


def _context_rejection(row: dict[str, Any], profile: dict[str, Any]) -> str | None:
    if not _requires_confirmed_context(profile):
        return None
    market = str(row.get("market_context_status") or "unknown").lower()
    sector = str(row.get("sector_confirmation_status") or "unknown").lower()
    if market in {"unknown", "stale", "no_data", "error", ""}:
        return "MARKET_CONTEXT_UNAVAILABLE"
    if market not in {"ok", "confirmed"}:
        return "MARKET_CONTEXT_NOT_CONFIRMED"
    if sector in {"unknown", "stale", "no_data", "error", ""}:
        return "SECTOR_CONTEXT_UNAVAILABLE"
    if sector != "confirmed":
        return "SECTOR_CONTEXT_NOT_CONFIRMED"
    return None


def _profile_entry(
    *, profile: dict[str, Any], direction: str, setup: dict[str, Any], bars: Any,
    decision_at: datetime, bar_minutes: int,
) -> tuple[dict[str, Any] | None, str | None]:
    """Return confirmed close entry or registered rejection reason.

    Only bars that close after the point-in-time candidate timestamp are used.
    The returned index is the confirmation bar; the simulator sees later bars only.
    """
    frame = _rth(normalize_frame(bars))
    if frame.empty:
        return None, "STOCK_BARS_MISSING"
    # VWAP is a session statistic.  Keep the whole originating RTH session so
    # the confirmation candle sees the real session VWAP, while entering only
    # on a bar that closed after the point-in-time candidate observation.
    ny_dates = frame["timestamp"].dt.tz_convert("America/New_York").dt.date
    source_session = decision_at.astimezone(ZoneInfo("America/New_York")).date()
    frame = frame.loc[ny_dates == source_session].reset_index(drop=True)
    closes = frame["timestamp"] + pd.Timedelta(minutes=bar_minutes)
    eligible_indices = [int(i) for i in frame.index[closes > pd.Timestamp(decision_at)]]
    if not eligible_indices:
        return None, "NO_FUTURE_BARS"
    low, high = _float(setup.get("entry_low")), _float(setup.get("entry_high"))
    stop, tp1, tp2, tp3 = (_float(setup.get(k)) for k in ("invalidation", "tp1", "tp2", "tp3"))
    if None in {low, high, stop, tp1, tp2, tp3}:
        return None, "SETUP_MISSING"
    low, high = min(low, high), max(low, high)
    trigger = high if direction == "long" else low
    rule = str(profile.get("rule") or "").lower()

    if rule == "pullback_vwap_hold":
        touched = False
        for idx in eligible_indices:
            row = frame.iloc[idx]
            if not touched and _inside_or_touches(direction, row, low, high):
                touched = True
                continue
            if not touched:
                continue
            vwap = _vwap(frame, idx)
            close = _float(row.get("close"))
            open_price = _float(row.get("open"))
            # A hold needs to close back through the *far edge* of the zone as
            # well as the session VWAP.  A wick/touch alone remains a pullback,
            # never a confirmed entry.
            beyond_zone = close >= high if direction == "long" else close <= low
            directional_body = bool(
                close is not None and open_price is not None
                and (close >= open_price if direction == "long" else close <= open_price)
            )
            if (vwap is not None and close is not None and beyond_zone
                    and _same_side(direction, close, vwap)):
                if profile.get("require_directional_body") and not directional_body:
                    continue
                lookback = max(1, int(profile.get("rvol_lookback") or 8))
                prior = pd.to_numeric(
                    frame.iloc[max(0, idx - lookback):idx]["volume"], errors="coerce"
                ).dropna()
                volume = _float(row.get("volume"))
                confirmation_rvol = (
                    volume / float(prior.median())
                    if volume is not None and not prior.empty and float(prior.median()) > 0
                    else None
                )
                return {"idx": idx, "entry": close, "stop": stop, "tp1": tp1, "tp2": tp2, "tp3": tp3,
                        "entry_ts": (row["timestamp"] + pd.Timedelta(minutes=bar_minutes)).isoformat(),
                        "vwap": vwap, "quality": {
                            "directional_body": directional_body,
                            "confirmation_rvol": confirmation_rvol,
                        }}, None
        return None, "VWAP_HOLD_NOT_CONFIRMED"

    if rule == "breakout_confirm":
        need = max(1, int(profile.get("confirmation_bars") or 1))
        run = 0
        for idx in eligible_indices:
            row = frame.iloc[idx]
            close, vwap = _float(row.get("close")), _vwap(frame, idx)
            confirmed = close is not None and vwap is not None and _same_side(direction, close, trigger) and _same_side(direction, close, vwap)
            run = run + 1 if confirmed else 0
            if run >= need:
                quality, reason = _confirmation_quality(
                    profile=profile, frame=frame, idx=idx, direction=direction, trigger=trigger, stop=stop,
                )
                if reason:
                    return None, reason
                return {"idx": idx, "entry": close, "stop": stop, "tp1": tp1, "tp2": tp2, "tp3": tp3,
                        "entry_ts": (row["timestamp"] + pd.Timedelta(minutes=bar_minutes)).isoformat(),
                        "vwap": vwap, "quality": quality}, None
        return None, "BREAKOUT_CONFIRM_NOT_REACHED"

    if rule == "breakout_retest":
        broke = False
        for idx in eligible_indices:
            row = frame.iloc[idx]
            close, vwap = _float(row.get("close")), _vwap(frame, idx)
            above = close is not None and vwap is not None and _same_side(direction, close, trigger) and _same_side(direction, close, vwap)
            if above and not broke:
                broke = True
                continue
            retest = (float(row["low"]) <= trigger if direction == "long" else float(row["high"]) >= trigger)
            if broke and retest and above:
                quality, reason = _confirmation_quality(
                    profile=profile, frame=frame, idx=idx, direction=direction, trigger=trigger, stop=stop,
                )
                if reason:
                    return None, reason
                return {"idx": idx, "entry": close, "stop": stop, "tp1": tp1, "tp2": tp2, "tp3": tp3,
                        "entry_ts": (row["timestamp"] + pd.Timedelta(minutes=bar_minutes)).isoformat(),
                        "vwap": vwap, "quality": quality}, None
        return None, "BREAKOUT_RETEST_NOT_CONFIRMED"
    raise ValueError(f"unsupported shadow profile rule: {rule}")


def _base_row(*, cfg: dict[str, Any], profile: dict[str, Any], idea: Any,
              generated_at: datetime, window: str) -> dict[str, Any]:
    raw = dict(getattr(idea, "raw", None) or {})
    setup = dict(raw.get("setup") or {})
    gate = dict(raw.get("intraday_actionability") or {})
    candidate = dict(raw.get("candidate") or {})
    source_at = str(getattr(idea, "generated_at", None) or generated_at.isoformat())
    symbol = str(getattr(idea, "symbol", "")).upper()
    direction = str(getattr(idea, "direction", "long")).lower()
    return {
        "candidate_id": _candidate_id(str(cfg["strategy_id"]), str(profile["profile_id"]), symbol, source_at, setup),
        "strategy_id": cfg["strategy_id"], "profile_id": profile["profile_id"],
        "shadow_lane": cfg["shadow_lane"], "window": window, "generated_at": generated_at.isoformat(),
        "decision_at": source_at, "source_candidate_at": source_at, "symbol": symbol, "direction": direction,
        "entry_mode": str(profile.get("entry_mode") or "").upper(), "rule_name": str(profile.get("rule") or ""),
        "source_tier": str(raw.get("pre_gate_tier") or getattr(idea, "tier", "C")),
        "market_context_status": str(gate.get("market_context_status") or "unknown"),
        "sector_confirmation_status": str(gate.get("sector_confirmation_status") or "unknown"),
        "context_group": _context_group(raw), "session_phase": str(gate.get("session_phase") or "unknown"),
        "liquidity_status": str(gate.get("liquidity_status") or "unknown"),
        "catalyst_quality": str(gate.get("catalyst_quality") or "none"),
        "sector": candidate.get("sector"), "sector_etf": candidate.get("sector_etf"),
        "eligibility_status": "rejected", "rejection_reason": None, "data_status": "clean",
        "is_clean_for_edge": 1, "entry_ts": None, "entry_price": None, "stop_price": None,
        "tp1": None, "tp2": None, "tp3": None, "outcome_status": "skipped", "close_reason": None,
        "exit_price": None, "exit_ts": None, "gross_pnl_usd": None, "net_pnl_usd": None, "net_r": None,
        "fees_usd": 0.0, "slippage_usd": 0.0, "funding_usd": 0.0, "funding_source": "not_applicable",
        "funding_estimated": 0, "funding_event_count": 0, "risk_usd": None, "mfe_r": None,
        "mae_r": None, "protection_armed": 0, "lock_armed": 0, "highest_tp_touched": 0,
        "bars_held": 0, "latency_seconds": None,
        "features_json": json_text({"setup": setup, "gate": gate, "source_tier": raw.get("pre_gate_tier")}),
        "notes_json": json_text({"research_only": True, "paper_unchanged": True}),
    }


def evaluate_idea(*, cfg: dict[str, Any], profile: dict[str, Any], idea: Any,
                  stock_bars: Any, generated_at: datetime, window: str) -> dict[str, Any]:
    row = _base_row(cfg=cfg, profile=profile, idea=idea, generated_at=generated_at, window=window)
    raw = dict(getattr(idea, "raw", None) or {})
    setup = dict(raw.get("setup") or {})
    source_at = parse_dt(row["source_candidate_at"]) or generated_at
    if not is_us_cash_session_open(source_at):
        row["rejection_reason"] = "OUTSIDE_RTH"
        return row
    if str(raw.get("pre_gate_tier") or getattr(idea, "tier", "C")).upper() not in {"A", "B"}:
        row["rejection_reason"] = "PRE_GATE_NOT_AB"
        return row
    context_reason = _context_rejection(row, profile)
    if context_reason:
        # Missing point-in-time context is not a market loss, but it must not
        # become "clean" evidence for a context-dependent refinement.
        row.update(rejection_reason=context_reason, data_status="context_unavailable", is_clean_for_edge=0)
        return row
    frame = _rth(normalize_frame(stock_bars))
    if frame.empty:
        row.update(rejection_reason="STOCK_BARS_MISSING", data_status="dirty", is_clean_for_edge=0)
        return row
    source_day = source_at.astimezone(ZoneInfo("America/New_York")).date()
    day = frame.loc[frame["timestamp"].dt.tz_convert("America/New_York").dt.date == source_day].reset_index(drop=True)
    if not _coverage_clean(day, int(str(cfg["timeframe"]).rstrip("m"))):
        row.update(rejection_reason="DATA_COVERAGE_DIRTY", data_status="dirty", is_clean_for_edge=0)
        return row
    entry_info, reason = _profile_entry(
        profile=profile, direction=row["direction"], setup=setup, bars=day,
        decision_at=source_at, bar_minutes=int(str(cfg["timeframe"]).rstrip("m")),
    )
    if reason:
        row["rejection_reason"] = reason
        return row
    assert entry_info is not None
    entry = float(entry_info["entry"])
    stop = float(entry_info["stop"])
    long = row["direction"] == "long"
    if (long and stop >= entry) or ((not long) and stop <= entry):
        row["rejection_reason"] = "GEOMETRY_INVALID"
        return row
    confirmation_idx = int(entry_info["idx"])
    future = day.iloc[confirmation_idx + 1:].reset_index(drop=True)
    pseudo_signal = {"asset_class": "stocks", "mode": "intraday", "created_at": row["source_candidate_at"]}
    future = _trim_stock_intraday_to_rth(future, pseudo_signal)
    if future.empty:
        row["rejection_reason"] = "NO_FUTURE_BARS"
        return row
    bar_minutes = int(str(cfg["timeframe"]).rstrip("m"))
    last_close = future.iloc[-1]["timestamp"] + pd.Timedelta(minutes=bar_minutes)
    session_close = us_cash_session_close(source_at)
    # A partial local cache is not proof that the session ended.  This is
    # deliberately stricter than comparing against refresh wall-clock time:
    # force an intraday time exit only once the final RTH bar is present.
    session_complete = bool(session_close and last_close >= pd.Timestamp(session_close))
    sim = simulate_confirmed_close_entry(
        direction=row["direction"], entry=entry, stop=stop, tp1=float(entry_info["tp1"]),
        tp2=float(entry_info["tp2"]), tp3=float(entry_info["tp3"]), future_candles=future,
        symbol=row["symbol"], fee_profile=cfg["fee_profile"], entry_at=parse_dt(entry_info["entry_ts"]),
        bar_minutes=bar_minutes, force_close=session_complete,
    )
    row.update(eligibility_status="eligible", entry_ts=entry_info["entry_ts"], entry_price=entry,
               stop_price=stop, tp1=float(entry_info["tp1"]), tp2=float(entry_info["tp2"]),
               tp3=float(entry_info["tp3"]), latency_seconds=max(0.0, (parse_dt(entry_info["entry_ts"]) - source_at).total_seconds()))
    for key, value in sim.to_dict().items():
        target = "outcome_status" if key == "status" else key
        if target in row:
            row[target] = value
    feature = json.loads(row["features_json"])
    feature.update({"confirmation": entry_info, "coverage_clean": True})
    row["features_json"] = json_text(feature)
    row["protection_armed"] = int(bool(row["protection_armed"]))
    row["lock_armed"] = int(bool(row["lock_armed"]))
    return row


def _activation(conn: sqlite3.Connection, now: datetime, persist: bool) -> str:
    existing = conn.execute("SELECT v FROM stocks_intraday_variant_shadow_meta WHERE k='activated_at'").fetchone()
    if existing:
        return str(existing[0])
    activated_at = now.isoformat()
    if persist:
        conn.execute("INSERT INTO stocks_intraday_variant_shadow_meta(k,v) VALUES ('activated_at',?)", (activated_at,))
    return activated_at


def _recently_refreshed(conn: sqlite3.Connection, now: datetime, cfg: dict[str, Any]) -> bool:
    row = conn.execute("SELECT v FROM stocks_intraday_variant_shadow_meta WHERE k='last_refresh_at'").fetchone()
    previous = parse_dt(row[0]) if row else None
    return bool(previous and now - previous < timedelta(minutes=float(cfg["refresh_min_interval_minutes"])))


def _primary_catalyst_readiness(conn: sqlite3.Connection, now: datetime) -> dict[str, Any]:
    if not table_exists(conn, "news_canonical_events"):
        return {"status": "unavailable", "reason": "news_canonical_events_missing"}
    start = (now - timedelta(hours=24)).isoformat()
    raw_rows = conn.execute(
        "SELECT source_quality, COUNT(*) AS n FROM news_canonical_events "
        "WHERE lower(COALESCE(asset_class,''))='stocks' AND effective_at>=? GROUP BY source_quality", (start,)
    ).fetchall()
    linked_rows = conn.execute(
        "SELECT source_quality, COUNT(*) AS n FROM news_canonical_events "
        "WHERE lower(COALESCE(asset_class,''))='stocks' AND effective_at>=? "
        "AND is_cluster_primary=1 AND linkage_allowed=1 GROUP BY source_quality", (start,)
    ).fetchall()
    raw_counts = {str(r[0] or "unknown"): int(r[1]) for r in raw_rows}
    linked_counts = {str(r[0] or "unknown"): int(r[1]) for r in linked_rows}
    trusted = {"company_pr", "regulator", "reputable", "primary"}
    primary = sum(linked_counts.get(key, 0) for key in trusted)
    return {
        "status": "ok", "lookback_hours": 24,
        "canonical_rows": sum(raw_counts.values()), "linked_primary_events": sum(linked_counts.values()),
        "primary_or_reputable_events": primary,
        "secondary_events": linked_counts.get("secondary", 0),
        "by_source_quality": linked_counts, "raw_by_source_quality": raw_counts,
        "note": "readiness counts only cluster-primary, linkage-allowed events; generic SEC filings remain excluded.",
    }


def _all_rows(conn: sqlite3.Connection, profile_id: str | None = None) -> list[dict[str, Any]]:
    conn.row_factory = sqlite3.Row
    sql = "SELECT * FROM stocks_intraday_variant_shadow_outcomes"
    args: tuple[Any, ...] = ()
    if profile_id:
        sql += " WHERE profile_id=?"
        args = (profile_id,)
    return [dict(row) for row in conn.execute(sql, args)]


def _snapshot_idea(row: dict[str, Any]) -> Any:
    """Reconstruct the original point-in-time candidate for a later outcome pass."""
    try:
        features = json.loads(row.get("features_json") or "{}")
    except (TypeError, ValueError):
        features = {}
    setup = dict(features.get("setup") or {})
    return type("ShadowIdea", (), {
        "symbol": row["symbol"], "direction": row["direction"], "tier": row.get("source_tier") or "C",
        "generated_at": row.get("source_candidate_at") or row.get("decision_at"),
        "raw": {
            "pre_gate_tier": row.get("source_tier") or "C", "setup": setup,
            "candidate": {"sector": row.get("sector"), "sector_etf": row.get("sector_etf")},
            "intraday_actionability": {
                "market_context_status": row.get("market_context_status"),
                "sector_confirmation_status": row.get("sector_confirmation_status"),
                "session_phase": row.get("session_phase"), "liquidity_status": row.get("liquidity_status"),
                "catalyst_quality": row.get("catalyst_quality"),
            },
        },
    })()


def _same_ny_session(ts: Any, now: datetime) -> bool:
    observed = parse_dt(ts)
    return bool(observed and observed.astimezone(ZoneInfo("America/New_York")).date()
                == now.astimezone(ZoneInfo("America/New_York")).date())


def _needs_lifecycle_replay(row: dict[str, Any], now: datetime) -> bool:
    """Keep intraday candidates moving until their same-day result is final."""
    if _same_ny_session(row.get("source_candidate_at"), now):
        return True
    if str(row.get("outcome_status") or "").lower() == "open":
        return True
    return str(row.get("rejection_reason") or "").upper() == "NO_FUTURE_BARS"


def _upsert_outcomes(conn: sqlite3.Connection, rows: list[dict[str, Any]]) -> None:
    """Update a maturing outcome without rewriting its first observation.

    The initial decision timestamp/window are evidence fields, not mutable
    display fields.  Later monitor passes can resolve an open entry/exit, but
    cannot turn a historical row into forward evidence or vice versa.
    """
    if not rows:
        return
    first_observation = {
        "candidate_id", "strategy_id", "profile_id", "shadow_lane", "window", "generated_at",
        "decision_at", "source_candidate_at", "symbol", "direction", "entry_mode", "rule_name",
        "source_tier", "market_context_status", "sector_confirmation_status", "context_group",
        "session_phase", "liquidity_status", "catalyst_quality", "sector", "sector_etf",
    }
    updates = [col for col in OUTCOME_COLUMNS if col not in first_observation]
    sql = (
        "INSERT INTO stocks_intraday_variant_shadow_outcomes (" + ",".join(OUTCOME_COLUMNS) + ") VALUES ("
        + ",".join("?" for _ in OUTCOME_COLUMNS) + ") ON CONFLICT(candidate_id) DO UPDATE SET "
        + ",".join(f"{col}=excluded.{col}" for col in updates)
    )
    conn.executemany(sql, [tuple(row.get(col) for col in OUTCOME_COLUMNS) for row in rows])


def _scout_ideas(cfg: dict[str, Any]) -> list[Any]:
    """Run the existing stock chain against a research-only universe.

    ``shadow_only=True`` prevents report, trade-idea and proposed-signal
    persistence.  The analysis agents remain the one source of stock context,
    so no second scoring or routing path is introduced.
    """
    from src.stocks.pipelines.stocks_pipeline import StocksPipeline

    app_cfg = load_config()
    pipeline = StocksPipeline(app_cfg)
    symbols = list(dict.fromkeys([*cfg["shadow_symbols"], "SPY", "QQQ"]))
    result = pipeline.run_report(mode="intraday", symbols=symbols, shadow_only=True)
    return result.ideas


def refresh(*, db: str | None = None, persist: bool = True, force: bool = False,
            now: datetime | None = None, cfg: dict[str, Any] | None = None,
            ideas: list[Any] | None = None, bars_by_symbol: dict[str, Any] | None = None) -> dict[str, Any]:
    cfg = cfg or load_strategy_config()
    now = now or utc_now()
    path = Path(db) if db else Path(load_config().db_path)
    if not bool(cfg.get("feature_flag")):
        return {"enabled": False, "generated_at": now.isoformat(), "config": cfg, "rows": [], "profiles": []}
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    try:
        ensure_tables(conn)
        conn.commit()
        if not force and _recently_refreshed(conn, now, cfg):
            return {"enabled": True, "skipped_recent_refresh": True, "generated_at": now.isoformat(),
                    "config": cfg, "rows": [], "profiles": []}
        activated_at = _activation(conn, now, persist)
        if persist:
            conn.commit()
        observations = ideas if ideas is not None else (_scout_ideas(cfg) if is_us_cash_session_open(now) else [])
        fs = FileStore(load_config())
        rows: list[dict[str, Any]] = []
        activation = parse_dt(activated_at)
        existing_rows = _all_rows(conn)
        existing_by_id = {str(row["candidate_id"]): row for row in existing_rows}
        bars_cache: dict[str, Any] = dict(bars_by_symbol or {})
        processed: set[str] = set()

        def bars_for(symbol: str) -> Any:
            if symbol not in bars_cache:
                bars_cache[symbol] = fs.load_stocks_ohlcv(symbol, cfg["timeframe"])
            return bars_cache[symbol]

        for idea in observations:
            symbol = str(getattr(idea, "symbol", "")).upper()
            if symbol not in set(cfg["shadow_symbols"]):
                continue
            source_at = parse_dt(getattr(idea, "generated_at", None)) or now
            window = "historical_backfill" if activation and source_at < activation else "forward_post_activation"
            for profile in cfg["profiles"]:
                raw = dict(getattr(idea, "raw", None) or {})
                candidate_id = _candidate_id(str(cfg["strategy_id"]), str(profile["profile_id"]), symbol,
                                             str(getattr(idea, "generated_at", None) or now.isoformat()),
                                             dict(raw.get("setup") or {}))
                existing = existing_by_id.get(candidate_id)
                source_idea = _snapshot_idea(existing) if existing else idea
                source_window = str(existing.get("window")) if existing else window
                rows.append(evaluate_idea(cfg=cfg, profile=profile, idea=source_idea, stock_bars=bars_for(symbol),
                                          generated_at=now, window=source_window))
                processed.add(candidate_id)

        # A candidate can disappear from the current scanner after its first
        # observation. Continue walking that original setup through the rest
        # of the same RTH session. Also replay an older unresolved candidate:
        # the final RTH bar may only reach the local cache after that session's
        # last scheduler cycle, but an intraday trade must never stay open for
        # multiple calendar days.
        for existing in existing_rows:
            candidate_id = str(existing["candidate_id"])
            if candidate_id in processed or not _needs_lifecycle_replay(existing, now):
                continue
            profile = next((p for p in cfg["profiles"] if p["profile_id"] == existing.get("profile_id")), None)
            if profile is None:
                continue
            source_idea = _snapshot_idea(existing)
            rows.append(evaluate_idea(cfg=cfg, profile=profile, idea=source_idea,
                                      stock_bars=bars_for(str(existing["symbol"]).upper()), generated_at=now,
                                      window=str(existing.get("window") or "historical_backfill")))
            processed.add(candidate_id)
        if persist and rows:
            _upsert_outcomes(conn, rows)
            # Summaries can scan the complete evidence table. Do not hold the
            # outcome write lease while they are being calculated.
            conn.commit()
        all_rows = _all_rows(conn)
        profiles: list[dict[str, Any]] = []
        for profile in cfg["profiles"]:
            profile_rows = [r for r in all_rows if r.get("profile_id") == profile["profile_id"]]
            summary = clean_forward_summary(profile_rows, activated_at=activated_at, now=now,
                                            min_closed=int(cfg["min_clean_closed"]),
                                            min_days=float(cfg["min_forward_days"]),
                                            min_pf=float(cfg["min_profit_factor"]),
                                            max_review_drawdown_usd=float(cfg["max_review_drawdown_usd"]))
            diagnostics = strategy_diagnostics(profile_rows, group_keys=("context_group", "session_phase", "sector", "catalyst_quality"))
            reasons = Counter(str(r.get("rejection_reason")) for r in profile_rows if r.get("rejection_reason"))
            profiles.append({"profile": profile, "summary": summary, "diagnostics": diagnostics,
                             "rejection_counts": dict(sorted(reasons.items()))})
            if persist:
                cols = ("generated_at", "profile_id", "strategy_id", "shadow_lane", "activated_at", "forward_rows",
                        "clean_rows", "dirty_rows", "clean_closed", "net_pnl_usd", "net_r", "fees_usd",
                        "slippage_usd", "funding_usd", "profit_factor", "winrate", "max_drawdown_usd",
                        "forward_days", "verdict", "rejection_counts_json", "diagnostics_json", "config_json")
                values = (now.isoformat(), profile["profile_id"], cfg["strategy_id"], cfg["shadow_lane"], activated_at,
                          *(summary[k] for k in ("forward_rows", "clean_rows", "dirty_rows", "clean_closed", "net_pnl_usd",
                                                  "net_r", "fees_usd", "slippage_usd", "funding_usd", "profit_factor",
                                                  "winrate", "max_drawdown_usd", "forward_days", "verdict")),
                          json_text(dict(reasons)), json_text(diagnostics), json_text(cfg))
                conn.execute("INSERT OR REPLACE INTO stocks_intraday_variant_shadow_evaluations (" + ",".join(cols)
                             + ") VALUES (" + ",".join("?" for _ in cols) + ")", values)
                conn.commit()
        readiness = _primary_catalyst_readiness(conn, now)
        if persist:
            conn.execute("INSERT OR REPLACE INTO stocks_intraday_variant_shadow_meta(k,v) VALUES ('last_refresh_at',?)",
                         (now.isoformat(),))
            conn.commit()
        return {"enabled": True, "generated_at": now.isoformat(), "activated_at": activated_at,
                "strategy_id": cfg["strategy_id"], "shadow_lane": cfg["shadow_lane"], "rows": rows,
                "profiles": profiles, "primary_catalyst_readiness": readiness, "config": cfg,
                "paper_unchanged": True, "live_locked": True}
    finally:
        conn.close()


def render_markdown(result: dict[str, Any]) -> str:
    if not result.get("enabled"):
        return "# Stocks Intraday Variants (Shadow)\n\n- status: **DISABLED** (`feature_flag=false`)\n"
    lines = [
        "# Stocks Intraday Entry Variants (Shadow)", "",
        f"- strategy: `{result['strategy_id']}`; lane: `{result['shadow_lane']}`",
        f"- activated: `{result['activated_at']}`; Paper rules and live routing are unchanged.",
        "- Only clean, closed, forward rows count toward evidence. Any positive result remains `REVIEW_ONLY`.", "",
        "## Profile summaries", "",
        "| profile | forward | clean closed | net USD | PF | win% | fees | slippage | verdict |",
        "|---|--:|--:|--:|--:|--:|--:|--:|---|",
    ]
    for item in result["profiles"]:
        s = item["summary"]
        lines.append(f"| `{item['profile']['profile_id']}` | {s['forward_rows']} | {s['clean_closed']} | "
                     f"{s['net_pnl_usd']:.2f} | {s['profit_factor'] if s['profit_factor'] is not None else '-'} | "
                     f"{(s['winrate'] * 100) if s['winrate'] is not None else '-'} | {s['fees_usd']:.2f} | "
                     f"{s['slippage_usd']:.2f} | {s['verdict']} |")
    readiness = result.get("primary_catalyst_readiness") or {}
    lines.extend(["", "## Primary catalyst readiness", "",
                  f"- status: `{readiness.get('status', 'unknown')}`; canonical rows last 24h: "
                  f"`{readiness.get('canonical_rows', 0)}`; linked primary events: "
                  f"`{readiness.get('linked_primary_events', 0)}`.",
                  f"- linked trusted/reputable: `{readiness.get('primary_or_reputable_events', 0)}`; "
                  f"linked secondary: `{readiness.get('secondary_events', 0)}`.",
                  f"- {readiness.get('note', '')}"])
    for item in result["profiles"]:
        lines.extend(["", f"## `{item['profile']['profile_id']}` rejections", ""])
        lines.extend(f"- `{reason}`: {count}" for reason, count in item["rejection_counts"].items())
        if not item["rejection_counts"]:
            lines.append("- _none_")
        lines.extend([""] + diagnostics_markdown(item["diagnostics"]))
    lines.extend(["", "No auto-promotion: minimum 30 clean closed forward trades, 28 forward days, positive USD PnL, PF >= 1.25, acceptable drawdown and manual review."])
    return "\n".join(lines) + "\n"


def write_report(result: dict[str, Any], path: str | None = None) -> str:
    target = Path(path) if path else ROOT / result.get("config", DEFAULTS).get("report_path", DEFAULTS["report_path"])
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_markdown(result), encoding="utf-8")
    return str(target)


__all__ = [
    "OUTCOME_COLUMNS", "REJECTION_REASONS", "ensure_tables", "evaluate_idea", "load_strategy_config",
    "refresh", "render_markdown", "write_report", "_profile_entry",
]
