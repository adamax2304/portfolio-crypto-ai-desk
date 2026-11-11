"""Research-only Stock Swing Event RS Pullback V1 backtest.

This script is deliberately isolated under research_labs. It reads local OHLCV
CSV files and the production SQLite news read-model, but writes only local
research artifacts and a local research.sqlite database.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sqlite3
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable

import pandas as pd
import requests
import yaml


ROOT = Path(__file__).resolve().parents[2]
NY_TZ = "America/New_York"

RUNS_DDL = """
CREATE TABLE IF NOT EXISTS runs (
  run_id TEXT PRIMARY KEY,
  generated_at TEXT NOT NULL,
  study_start TEXT NOT NULL,
  study_end TEXT NOT NULL,
  config_json TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS variant_metrics (
  run_id TEXT NOT NULL,
  phase TEXT NOT NULL,
  variant_id TEXT NOT NULL,
  scope TEXT NOT NULL,
  metrics_json TEXT NOT NULL,
  PRIMARY KEY (run_id, phase, variant_id, scope)
);
CREATE TABLE IF NOT EXISTS trades (
  run_id TEXT NOT NULL,
  phase TEXT NOT NULL,
  variant_id TEXT NOT NULL,
  trade_id TEXT NOT NULL,
  symbol TEXT NOT NULL,
  entry_date TEXT,
  exit_date TEXT,
  status TEXT,
  net_pnl_usd REAL,
  net_r REAL,
  payload_json TEXT NOT NULL,
  PRIMARY KEY (run_id, phase, variant_id, trade_id)
);
"""


@dataclass(frozen=True)
class Variant:
    variant_id: str
    impulse_return_min: float
    impulse_atr_min: float
    volume_ratio_min: float
    rs20_min: float
    rs63_min: float
    rs_sector_min: float
    pullback_level: str
    touch_tolerance_atr: float
    require_green_reclaim: bool
    min_stop_atr: float
    max_stop_atr: float
    tp1_r: float
    tp1_pct: float
    tp2_r: float
    tp2_pct: float
    max_hold_days: int
    max_chase_atr: float
    allow_neutral: bool = True
    allow_risk_off: bool = False


def _utc(value: str | datetime | pd.Timestamp) -> pd.Timestamp:
    ts = pd.Timestamp(value)
    if ts.tzinfo is None:
        return ts.tz_localize("UTC")
    return ts.tz_convert("UTC")


def _date(value: str | datetime | pd.Timestamp) -> pd.Timestamp:
    return pd.Timestamp(value).tz_localize(None).normalize()


def load_config(path: Path) -> dict[str, Any]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return raw["stock_swing_event_rs_pullback_research"]


def _resolve(path: str | Path) -> Path:
    p = Path(path)
    return p if p.is_absolute() else ROOT / p


def load_universe(cfg: dict[str, Any]) -> tuple[list[str], dict[str, str], set[str]]:
    path = _resolve(cfg["data"]["universe_config"])
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    symbols = [str(item).upper() for item in raw.get("default_symbols", [])]
    indices = {str(item).upper() for item in raw.get("indices", [])}
    sector_etfs = {str(item).upper() for item in (raw.get("sector_etfs", {}) or {}).values()}
    benchmarks = indices | sector_etfs | {"^VIX"}
    sector_map = {str(k).upper(): str(v) for k, v in (raw.get("symbol_sector_map", {}) or {}).items()}
    trade_symbols = [s for s in symbols if s not in benchmarks and not s.startswith("^")]
    return sorted(dict.fromkeys(trade_symbols)), sector_map, benchmarks


def load_ohlcv(price_root: Path, symbol: str, timeframe: str) -> pd.DataFrame:
    path = price_root / timeframe / f"{symbol.upper()}.csv"
    if not path.exists():
        return pd.DataFrame()
    try:
        frame = pd.read_csv(path)
    except Exception:
        return pd.DataFrame()
    if frame.empty:
        return pd.DataFrame()
    columns = {str(c).lower(): c for c in frame.columns}
    time_col = columns.get("date") or columns.get("datetime") or frame.columns[0]
    rename = {columns.get(k, k): k for k in ("open", "high", "low", "close", "volume") if columns.get(k)}
    out = frame.rename(columns=rename)
    if not all(c in out.columns for c in ("open", "high", "low", "close", "volume")):
        return pd.DataFrame()
    out["timestamp"] = pd.to_datetime(out[time_col], utc=True, errors="coerce")
    out = out.dropna(subset=["timestamp", "close"]).copy()
    out["date"] = out["timestamp"].dt.tz_convert(NY_TZ).dt.tz_localize(None).dt.normalize()
    out = out.drop_duplicates("date").sort_values("date")
    out = out.set_index("date")
    for col in ("open", "high", "low", "close", "volume"):
        out[col] = pd.to_numeric(out[col], errors="coerce")
    return out[["timestamp", "open", "high", "low", "close", "volume"]].dropna()


def add_features(df: pd.DataFrame, spy: pd.DataFrame, sector: pd.DataFrame | None = None) -> pd.DataFrame:
    if df.empty:
        return df
    out = df.copy()
    prev_close = out["close"].shift(1)
    tr = pd.concat([
        out["high"] - out["low"],
        (out["high"] - prev_close).abs(),
        (out["low"] - prev_close).abs(),
    ], axis=1).max(axis=1)
    out["prev_close"] = prev_close
    out["true_range"] = tr
    out["atr14"] = tr.rolling(14).mean()
    out["atr14_prev"] = out["atr14"].shift(1)
    out["sma20"] = out["close"].rolling(20).mean()
    out["sma50"] = out["close"].rolling(50).mean()
    out["sma200"] = out["close"].rolling(200).mean()
    out["ema10"] = out["close"].ewm(span=10, adjust=False).mean()
    out["ema21"] = out["close"].ewm(span=21, adjust=False).mean()
    out["vol_avg20"] = out["volume"].rolling(20).mean().shift(1)
    out["volume_ratio"] = out["volume"] / out["vol_avg20"]
    out["dollar_volume_30d"] = (out["close"] * out["volume"]).rolling(30).mean()
    out["ret1"] = out["close"] / prev_close - 1.0
    out["ret20"] = out["close"].pct_change(20)
    out["ret63"] = out["close"].pct_change(63)
    spy_close = spy["close"].reindex(out.index).ffill()
    out["spy_ret20"] = spy_close.pct_change(20)
    out["spy_ret63"] = spy_close.pct_change(63)
    out["rs20_spy"] = out["ret20"] - out["spy_ret20"]
    out["rs63_spy"] = out["ret63"] - out["spy_ret63"]
    if sector is not None and not sector.empty:
        sector_close = sector["close"].reindex(out.index).ffill()
        out["sector_ret20"] = sector_close.pct_change(20)
        out["sector_ret63"] = sector_close.pct_change(63)
        out["rs20_sector"] = out["ret20"] - out["sector_ret20"]
        out["rs63_sector"] = out["ret63"] - out["sector_ret63"]
    else:
        out["rs20_sector"] = math.nan
        out["rs63_sector"] = math.nan
    return out


def market_regime(spy: pd.DataFrame, vix: pd.DataFrame) -> pd.Series:
    s = spy.copy()
    s["sma50"] = s["close"].rolling(50).mean()
    s["sma200"] = s["close"].rolling(200).mean()
    vix_close = vix["close"].reindex(s.index).ffill() if not vix.empty else pd.Series(index=s.index, dtype=float)
    labels = []
    for idx, row in s.iterrows():
        v = vix_close.get(idx)
        if row["close"] < row["sma200"] or (pd.notna(v) and float(v) >= 30):
            labels.append("risk_off")
        elif row["close"] > row["sma50"] and row["close"] > row["sma200"] and (pd.isna(v) or float(v) < 22):
            labels.append("risk_on")
        else:
            labels.append("neutral")
    return pd.Series(labels, index=s.index)


def variants() -> list[Variant]:
    result: list[Variant] = []
    for impulse in (0.025, 0.035, 0.05):
        for level in ("fib50", "fib618", "ema21", "hybrid"):
            for stop_min in (1.2, 1.5):
                for tp1, tp2 in ((1.5, 2.5), (2.0, 3.0)):
                    strict = impulse >= 0.05
                    vid = (
                        f"imp{int(impulse*1000):03d}_{level}_"
                        f"stop{str(stop_min).replace('.', '')}_tp{str(tp1).replace('.', '')}"
                    )
                    result.append(Variant(
                        variant_id=vid,
                        impulse_return_min=impulse,
                        impulse_atr_min=1.0 if not strict else 1.25,
                        volume_ratio_min=1.0 if not strict else 1.2,
                        rs20_min=0.00 if not strict else 0.02,
                        rs63_min=0.00,
                        rs_sector_min=-0.03 if not strict else 0.00,
                        pullback_level=level,
                        touch_tolerance_atr=0.20,
                        require_green_reclaim=False,
                        min_stop_atr=stop_min,
                        max_stop_atr=2.8,
                        tp1_r=tp1,
                        tp1_pct=0.40,
                        tp2_r=tp2,
                        tp2_pct=0.30,
                        max_hold_days=25,
                        max_chase_atr=0.75,
                    ))
    return result


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default


def _reclaim(row: pd.Series, level: float, require_green: bool) -> bool:
    if not math.isfinite(level) or level <= 0:
        return False
    span = float(row["high"] - row["low"])
    closes_well = span <= 0 or float(row["close"]) >= float(row["low"]) + 0.50 * span
    green_ok = (float(row["close"]) >= float(row["open"])) if require_green else True
    return float(row["low"]) <= level and float(row["close"]) >= level and closes_well and green_ok


def _level_for(row: pd.Series, impulse_low: float, impulse_high: float, variant: Variant) -> tuple[float, str]:
    fib50 = impulse_high - 0.50 * (impulse_high - impulse_low)
    fib618 = impulse_high - 0.618 * (impulse_high - impulse_low)
    ema21 = _safe_float(row.get("ema21"), math.nan)
    if variant.pullback_level == "fib50":
        return fib50, "fib50"
    if variant.pullback_level == "fib618":
        return fib618, "fib618"
    if variant.pullback_level == "ema21":
        return ema21, "ema21"
    candidates = [("fib50", fib50), ("ema21", ema21), ("fib618", fib618)]
    candidates = [(name, val) for name, val in candidates if math.isfinite(val) and val > 0]
    if not candidates:
        return math.nan, "none"
    close = float(row["close"])
    return min(candidates, key=lambda item: abs(item[1] - close))[1], "hybrid"


def _trade_id(symbol: str, variant_id: str, entry_date: Any, seed: str = "") -> str:
    raw = f"{symbol}|{variant_id}|{entry_date}|{seed}"
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]


def simulate_trade(
    *,
    symbol: str,
    variant: Variant,
    df: pd.DataFrame,
    entry_idx: int,
    entry_price: float,
    stop_price: float,
    risk_usd: float,
    tp1: float,
    tp2: float,
    slippage_bps: float,
    commission_bps: float,
    phase: str,
    evidence: dict[str, Any],
) -> dict[str, Any]:
    risk_per_share = entry_price - stop_price
    if entry_idx >= len(df) or risk_per_share <= 0 or risk_usd <= 0:
        return {"status": "invalid", "reason": "INVALID_SIM_GEOMETRY"}
    qty_total = risk_usd / risk_per_share
    remaining = 1.0
    pnl = 0.0
    fees = qty_total * entry_price * ((slippage_bps + commission_bps) / 10000.0)
    stop = stop_price
    tp1_done = False
    tp2_done = False
    mfe_r = 0.0
    mae_r = 0.0
    exits: list[dict[str, Any]] = []
    end_idx = min(len(df) - 1, entry_idx + variant.max_hold_days)
    exit_idx = end_idx
    exit_reason = "max_hold"
    for k in range(entry_idx, end_idx + 1):
        row = df.iloc[k]
        high = float(row["high"])
        low = float(row["low"])
        close = float(row["close"])
        open_px = float(row["open"])
        mfe_r = max(mfe_r, (high - entry_price) / risk_per_share)
        mae_r = min(mae_r, (low - entry_price) / risk_per_share)
        if low <= stop:
            px = min(open_px, stop) if open_px < stop else stop
            part_qty = qty_total * remaining
            pnl += part_qty * (px - entry_price)
            fees += part_qty * px * ((slippage_bps + commission_bps) / 10000.0)
            exits.append({"date": str(df.index[k].date()), "reason": "stop", "price": px, "pct": remaining})
            exit_idx = k
            exit_reason = "stop" if stop <= stop_price + 1e-12 else "trail_stop"
            remaining = 0.0
            break
        if not tp1_done and high >= tp1:
            part = min(remaining, variant.tp1_pct)
            part_qty = qty_total * part
            pnl += part_qty * (tp1 - entry_price)
            fees += part_qty * tp1 * ((slippage_bps + commission_bps) / 10000.0)
            exits.append({"date": str(df.index[k].date()), "reason": "tp1", "price": tp1, "pct": part})
            remaining -= part
            tp1_done = True
            stop = max(stop, entry_price)
        if tp1_done and not tp2_done and high >= tp2:
            part = min(remaining, variant.tp2_pct)
            part_qty = qty_total * part
            pnl += part_qty * (tp2 - entry_price)
            fees += part_qty * tp2 * ((slippage_bps + commission_bps) / 10000.0)
            exits.append({"date": str(df.index[k].date()), "reason": "tp2", "price": tp2, "pct": part})
            remaining -= part
            tp2_done = True
        if tp1_done:
            ema21 = _safe_float(row.get("ema21"), math.nan)
            atr = _safe_float(row.get("atr14"), 0.0)
            if math.isfinite(ema21) and atr > 0:
                stop = max(stop, ema21 - 0.10 * atr)
        if k == end_idx and remaining > 0:
            part_qty = qty_total * remaining
            pnl += part_qty * (close - entry_price)
            fees += part_qty * close * ((slippage_bps + commission_bps) / 10000.0)
            exits.append({"date": str(df.index[k].date()), "reason": "max_hold", "price": close, "pct": remaining})
            exit_idx = k
            remaining = 0.0
            break
    net = pnl - fees
    return {
        "trade_id": _trade_id(symbol, variant.variant_id, df.index[entry_idx], evidence.get("seed", "")),
        "phase": phase,
        "variant_id": variant.variant_id,
        "symbol": symbol,
        "entry_date": str(df.index[entry_idx].date()),
        "exit_date": str(df.index[exit_idx].date()) if exit_idx < len(df) else None,
        "status": "closed",
        "exit_reason": exit_reason,
        "entry_price": round(entry_price, 6),
        "stop_price": round(stop_price, 6),
        "tp1": round(tp1, 6),
        "tp2": round(tp2, 6),
        "risk_usd": round(risk_usd, 4),
        "qty": round(qty_total, 8),
        "gross_pnl_usd": round(pnl, 4),
        "fees_slippage_usd": round(fees, 4),
        "net_pnl_usd": round(net, 4),
        "net_r": round(net / risk_usd, 4) if risk_usd else None,
        "mfe_r": round(mfe_r, 4),
        "mae_r": round(mae_r, 4),
        "bars_held": int(exit_idx - entry_idx + 1),
        "exits": exits,
        "evidence": evidence,
    }


def _passes_common_filters(row: pd.Series, variant: Variant, min_price: float, min_dv: float) -> tuple[bool, str | None]:
    if float(row["close"]) < min_price:
        return False, "PRICE_TOO_LOW"
    if _safe_float(row.get("dollar_volume_30d")) < min_dv:
        return False, "DOLLAR_VOLUME_TOO_LOW"
    if _safe_float(row.get("atr14_prev")) <= 0:
        return False, "ATR_MISSING"
    if _safe_float(row.get("volume_ratio")) < variant.volume_ratio_min:
        return False, "VOLUME_RATIO_LOW"
    if _safe_float(row.get("rs20_spy"), -999) < variant.rs20_min:
        return False, "RS20_SPY_LOW"
    if _safe_float(row.get("rs63_spy"), -999) < variant.rs63_min:
        return False, "RS63_SPY_LOW"
    rs_sector = _safe_float(row.get("rs20_sector"), 0.0)
    if rs_sector < variant.rs_sector_min:
        return False, "RS_SECTOR_LOW"
    return True, None


def _is_impulse(row: pd.Series, variant: Variant) -> bool:
    atr = _safe_float(row.get("atr14_prev"))
    if atr <= 0:
        return False
    move = _safe_float(row.get("ret1"))
    tr_atr = _safe_float(row.get("true_range")) / atr
    close_strong = float(row["close"]) > float(row["open"]) or move >= variant.impulse_return_min * 1.25
    return move >= variant.impulse_return_min and tr_atr >= variant.impulse_atr_min and close_strong


def _size_weight(regime: str, variant: Variant, cfg: dict[str, Any]) -> float:
    if regime == "risk_on":
        return 1.0
    if regime == "neutral":
        return float(cfg["risk"]["neutral_size_weight"]) if variant.allow_neutral else 0.0
    if regime == "risk_off":
        return float(cfg["risk"]["risk_off_size_weight"]) if variant.allow_risk_off else 0.0
    return 0.0


def find_pullback_after_impulse(
    *,
    symbol: str,
    df: pd.DataFrame,
    variant: Variant,
    impulse_idx: int,
    regimes: pd.Series,
    cfg: dict[str, Any],
    phase: str,
    evidence: dict[str, Any],
) -> dict[str, Any] | None:
    cluster_days = int(cfg["execution"]["impulse_cluster_days"])
    max_pullback_days = int(cfg["execution"]["max_pullback_days"])
    stop_buffer_atr = float(cfg["risk"]["stop_buffer_atr"])
    max_stop_pct = float(cfg["risk"]["max_stop_pct"])
    slippage_bps = float(cfg["risk"]["slippage_bps_per_side"])
    commission_bps = float(cfg["risk"].get("commission_bps_per_side", 0.0))
    end_cluster = impulse_idx
    for k in range(impulse_idx + 1, min(len(df), impulse_idx + cluster_days)):
        if float(df.iloc[k]["close"]) >= float(df.iloc[k - 1]["close"]):
            end_cluster = k
        else:
            break
    impulse = df.iloc[impulse_idx:end_cluster + 1]
    impulse_low = float(impulse["low"].min())
    impulse_high = float(impulse["high"].max())
    if impulse_high <= impulse_low:
        return None
    for j in range(end_cluster + 1, min(len(df) - 1, end_cluster + 1 + max_pullback_days)):
        row = df.iloc[j]
        atr = _safe_float(row.get("atr14"), _safe_float(row.get("atr14_prev")))
        if atr <= 0:
            continue
        raw_level, level_name = _level_for(row, impulse_low, impulse_high, variant)
        level = raw_level + variant.touch_tolerance_atr * atr
        if not _reclaim(row, level, variant.require_green_reclaim):
            continue
        regime = str(row.get("market_regime") or "neutral")
        weight = _size_weight(regime, variant, cfg)
        if weight <= 0:
            return None
        next_row = df.iloc[j + 1]
        entry = float(next_row["open"])
        chase_limit = float(row["close"]) + variant.max_chase_atr * atr
        if entry > chase_limit:
            return None
        structural_low = min(float(df.iloc[end_cluster + 1:j + 1]["low"].min()), raw_level)
        structural_stop = structural_low - stop_buffer_atr * atr
        min_stop = entry - variant.min_stop_atr * atr
        stop = min(structural_stop, min_stop)
        risk_per_share = entry - stop
        if risk_per_share <= 0:
            continue
        risk_atr = risk_per_share / atr
        stop_pct = risk_per_share / entry * 100.0
        if risk_atr > variant.max_stop_atr or stop_pct > max_stop_pct:
            continue
        risk_usd = float(cfg["risk"]["risk_usd_full"]) * weight
        tp1 = entry + variant.tp1_r * risk_per_share
        tp2 = entry + variant.tp2_r * risk_per_share
        enriched = dict(evidence)
        enriched.update({
            "seed": evidence.get("seed") or str(df.index[impulse_idx].date()),
            "impulse_date": str(df.index[impulse_idx].date()),
            "confirmation_date": str(df.index[j].date()),
            "market_regime": regime,
            "size_weight": weight,
            "pullback_level": level_name,
            "impulse_return": round(_safe_float(df.iloc[impulse_idx].get("ret1")), 5),
            "impulse_tr_atr": round(_safe_float(df.iloc[impulse_idx].get("true_range")) / _safe_float(df.iloc[impulse_idx].get("atr14_prev"), 1), 4),
            "volume_ratio": round(_safe_float(df.iloc[impulse_idx].get("volume_ratio")), 4),
            "rs20_spy": round(_safe_float(df.iloc[impulse_idx].get("rs20_spy")), 5),
            "rs63_spy": round(_safe_float(df.iloc[impulse_idx].get("rs63_spy")), 5),
            "rs20_sector": round(_safe_float(df.iloc[impulse_idx].get("rs20_sector")), 5),
        })
        return simulate_trade(
            symbol=symbol,
            variant=variant,
            df=df,
            entry_idx=j + 1,
            entry_price=entry,
            stop_price=stop,
            risk_usd=risk_usd,
            tp1=tp1,
            tp2=tp2,
            slippage_bps=slippage_bps,
            commission_bps=commission_bps,
            phase=phase,
            evidence=enriched,
        )
    return None


def backtest_technical(
    data: dict[str, pd.DataFrame],
    sectors: dict[str, str],
    regimes: pd.Series,
    variant: Variant,
    cfg: dict[str, Any],
    start: pd.Timestamp,
    end: pd.Timestamp,
) -> list[dict[str, Any]]:
    min_price = float(cfg["universe"]["min_price"])
    min_dv = float(cfg["universe"]["min_avg_dollar_volume_30d"])
    trades: list[dict[str, Any]] = []
    for symbol, df in data.items():
        if df.empty:
            continue
        active_until = -1
        for i in range(220, len(df) - 2):
            day = df.index[i]
            if day < start or day > end or i <= active_until:
                continue
            row = df.iloc[i]
            regime = str(row.get("market_regime") or "neutral")
            if _size_weight(regime, variant, cfg) <= 0:
                continue
            passed, _ = _passes_common_filters(row, variant, min_price, min_dv)
            if not passed or not _is_impulse(row, variant):
                continue
            trade = find_pullback_after_impulse(
                symbol=symbol,
                df=df,
                variant=variant,
                impulse_idx=i,
                regimes=regimes,
                cfg=cfg,
                phase="technical_skeleton",
                evidence={
                    "cohort": "technical_skeleton",
                    "sector": sectors.get(symbol),
                    "news_state": "NO_NEWS_REQUIRED",
                },
            )
            if trade:
                trades.append(trade)
                try:
                    active_until = df.index.get_loc(pd.Timestamp(trade["exit_date"]))
                except Exception:
                    active_until = i + 5
    return trades


def _json_list(value: Any) -> list[str]:
    try:
        parsed = json.loads(value or "[]")
    except Exception:
        return []
    return [str(item).upper() for item in parsed] if isinstance(parsed, list) else []


def _parse_dt(value: Any) -> pd.Timestamp | None:
    if value in (None, ""):
        return None
    try:
        return _utc(value)
    except Exception:
        return None


def _event_score(event: dict[str, Any], cfg: dict[str, Any]) -> tuple[float, str]:
    event_type = str(event.get("event_type") or "unknown").lower()
    hint = str(event.get("direction_hint") or "").lower()
    quality = str(event.get("source_quality") or "").lower()
    confidence = _safe_float(event.get("confidence"), 0.5)
    if event_type in set(cfg["news"]["blocking_event_types"]):
        return -100.0, "blocking_event"
    if hint == "bearish":
        return -30.0, "bearish_event"
    if event_type not in set(cfg["news"]["bullish_event_types"]):
        return 0.0, "unsupported_event_type"
    if quality not in set(cfg["news"]["trusted_source_qualities"]):
        return 5.0, "weak_source"
    base = {
        "earnings": 26,
        "guidance": 24,
        "analyst_action": 16,
        "partnership": 18,
        "mna": 20,
        "product_launch": 16,
        "contract_award": 20,
        "strategic_investment": 18,
        "fda_clinical": 14,
        "buyback": 16,
    }.get(event_type, 8)
    quality_boost = {"regulator": 8, "primary": 8, "company_pr": 6, "reputable": 4, "secondary": 1}.get(quality, 0)
    return base + quality_boost + 10 * max(0.0, min(1.0, confidence)), "bullish_supported"


def load_local_events(cfg: dict[str, Any], start: pd.Timestamp, end: pd.Timestamp) -> list[dict[str, Any]]:
    db_path = _resolve(cfg["data"]["db_path"])
    if not db_path.exists():
        return []
    sql = """
        SELECT event_id,news_item_id,title,source,published_at,available_at,event_latency_class,
               trusted_symbols_json,event_type,direction_hint,source_quality,confidence,
               linkage_allowed,risk_action,is_cluster_primary
        FROM news_canonical_events
        WHERE lower(COALESCE(asset_class,''))='stocks'
          AND COALESCE(linkage_allowed,0)=1
          AND available_at IS NOT NULL
          AND datetime(available_at)>=datetime(?)
          AND datetime(available_at)<=datetime(?)
        ORDER BY available_at,event_id
    """
    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        rows = [dict(row) for row in conn.execute(sql, (start.isoformat(), end.isoformat())).fetchall()]
    finally:
        conn.close()
    events: list[dict[str, Any]] = []
    for row in rows:
        score, reason = _event_score(row, cfg)
        row["event_score"] = score
        row["event_score_reason"] = reason
        row["symbols"] = _json_list(row.get("trusted_symbols_json"))
        row["available_ts"] = _parse_dt(row.get("available_at"))
        if row["available_ts"] is not None:
            events.append(row)
    return events


def backtest_events(
    *,
    events: list[dict[str, Any]],
    data: dict[str, pd.DataFrame],
    sectors: dict[str, str],
    regimes: pd.Series,
    variant: Variant,
    cfg: dict[str, Any],
    phase: str,
    start: pd.Timestamp,
    end: pd.Timestamp,
) -> list[dict[str, Any]]:
    min_price = float(cfg["universe"]["min_price"])
    min_dv = float(cfg["universe"]["min_avg_dollar_volume_30d"])
    by_symbol: dict[str, list[dict[str, Any]]] = {}
    for event in events:
        if "event_score" not in event:
            score, reason = _event_score(event, cfg)
            event["event_score"] = score
            event["event_score_reason"] = reason
        if _safe_float(event.get("event_score")) <= 0:
            continue
        at = event.get("available_ts")
        if at is None or at < start.tz_localize("UTC") or at > end.tz_localize("UTC"):
            continue
        for symbol in event.get("symbols") or []:
            if symbol in data:
                by_symbol.setdefault(symbol, []).append(event)
    trades: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for symbol, items in by_symbol.items():
        df = data.get(symbol)
        if df is None or df.empty:
            continue
        active_until = -1
        for event in sorted(items, key=lambda item: item["available_ts"]):
            event_day = _date(event["available_ts"].tz_convert(NY_TZ))
            if event_day not in df.index:
                later = df.index[df.index >= event_day]
                if len(later) == 0:
                    continue
                event_day = later[0]
            i0 = int(df.index.get_loc(event_day))
            if i0 <= active_until:
                continue
            chosen_idx = None
            for i in range(i0, min(len(df) - 2, i0 + 3)):
                row = df.iloc[i]
                passed, _ = _passes_common_filters(row, variant, min_price, min_dv)
                if not passed:
                    continue
                event_min_move = max(0.0125, variant.impulse_return_min * 0.55)
                event_min_atr = max(0.65, variant.impulse_atr_min * 0.65)
                if _safe_float(row.get("ret1")) >= event_min_move and (
                    _safe_float(row.get("true_range")) / max(_safe_float(row.get("atr14_prev")), 1e-9)
                ) >= event_min_atr:
                    chosen_idx = i
                    break
            if chosen_idx is None:
                continue
            seed = str(event.get("event_id") or event.get("url") or event.get("title") or "")
            key = (symbol, str(event_day.date()))
            if key in seen:
                continue
            trade = find_pullback_after_impulse(
                symbol=symbol,
                df=df,
                variant=variant,
                impulse_idx=chosen_idx,
                regimes=regimes,
                cfg=cfg,
                phase=phase,
                evidence={
                    "cohort": phase,
                    "sector": sectors.get(symbol),
                    "news_state": "NEWS_REQUIRED",
                    "event_id": event.get("event_id"),
                    "news_item_id": event.get("news_item_id"),
                    "event_type": event.get("event_type"),
                    "direction_hint": event.get("direction_hint"),
                    "source": event.get("source"),
                    "source_quality": event.get("source_quality"),
                    "confidence": event.get("confidence"),
                    "event_latency_class": event.get("event_latency_class"),
                    "published_at": event.get("published_at"),
                    "available_at": event.get("available_at"),
                    "event_score": event.get("event_score"),
                    "seed": seed,
                },
            )
            if trade:
                trades.append(trade)
                seen.add(key)
                try:
                    active_until = df.index.get_loc(pd.Timestamp(trade["exit_date"]))
                except Exception:
                    active_until = chosen_idx + 5
    return trades


def _load_dotenv() -> None:
    path = ROOT / ".env"
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        text = line.strip()
        if not text or text.startswith("#") or "=" not in text:
            continue
        key, value = text.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def _classify_reconstructed(item: dict[str, Any]) -> tuple[str, str, float]:
    text = f"{item.get('headline') or ''} {item.get('summary') or ''}".lower()
    bearish = (
        "downgrade", "cuts guidance", "cut guidance", "misses", "missed estimates",
        "investigation", "probe", "lawsuit", "offering", "public offering",
        "sec charges", "recall", "rejects", "halts trial",
    )
    bullish_map = [
        ("earnings", ("beats", "beat estimates", "raises guidance", "record revenue")),
        ("guidance", ("raises guidance", "guidance raised", "boosts outlook")),
        ("analyst_action", ("upgraded", "upgrade", "price target raised", "raises target")),
        ("partnership", ("partnership", "partners with", "collaboration", "collaborates")),
        ("contract_award", ("wins contract", "awarded contract", "selected by")),
        ("product_launch", ("launches", "unveils", "introduces", "rolls out")),
        ("buyback", ("buyback", "share repurchase", "repurchase authorization")),
        ("mna", ("to acquire", "acquires", "merger", "takeover")),
        ("fda_clinical", ("fda approves", "approval", "positive trial")),
    ]
    if any(term in text for term in bearish):
        return "legal_risk", "bearish", 0.65
    for event_type, terms in bullish_map:
        if any(term in text for term in terms):
            return event_type, "bullish", 0.62
    return "other_news", "unknown", 0.35


def fetch_reconstructed_news(cfg: dict[str, Any], symbols: list[str], start: pd.Timestamp, end: pd.Timestamp) -> list[dict[str, Any]]:
    cache_path = _resolve(cfg["news"]["reconstructed_cache"])
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    if cache_path.exists():
        rows = []
        for line in cache_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                try:
                    item = json.loads(line)
                    item["available_ts"] = _parse_dt(item.get("available_at"))
                    item["symbols"] = _json_list(item.get("trusted_symbols_json"))
                    rows.append(item)
                except json.JSONDecodeError:
                    pass
        if rows:
            return rows
    _load_dotenv()
    token = os.getenv("FINNHUB_API_KEY", "").strip()
    if not token:
        return []
    start_s = start.date().isoformat()
    end_s = end.date().isoformat()
    rows: list[dict[str, Any]] = []
    for idx, symbol in enumerate(symbols):
        try:
            response = requests.get(
                "https://finnhub.io/api/v1/company-news",
                params={"symbol": symbol, "from": start_s, "to": end_s, "token": token},
                timeout=15,
            )
            if response.status_code == 429:
                time.sleep(2.0)
                continue
            response.raise_for_status()
            payload = response.json() or []
            for item in payload[:250]:
                published = pd.to_datetime(item.get("datetime"), unit="s", utc=True, errors="coerce")
                if pd.isna(published):
                    continue
                event_type, hint, confidence = _classify_reconstructed(item)
                available = published + timedelta(minutes=int(cfg["news"]["reconstructed_delay_minutes"]))
                rows.append({
                    "event_id": f"recon_{symbol}_{item.get('id') or hashlib.sha1(str(item).encode()).hexdigest()[:12]}",
                    "news_item_id": None,
                    "title": item.get("headline"),
                    "source": item.get("source") or "Finnhub historical",
                    "published_at": published.isoformat(),
                    "available_at": available.isoformat(),
                    "event_latency_class": "RECONSTRUCTED_30M",
                    "trusted_symbols_json": json.dumps([symbol]),
                    "symbols": [symbol],
                    "event_type": event_type,
                    "direction_hint": hint,
                    "source_quality": "secondary",
                    "confidence": confidence,
                    "available_ts": available,
                })
            if idx and idx % 20 == 0:
                time.sleep(1.0)
        except Exception:
            continue
    if rows:
        with cache_path.open("w", encoding="utf-8") as fh:
            for row in rows:
                safe = dict(row)
                safe["available_ts"] = str(safe["available_ts"])
                fh.write(json.dumps(safe, sort_keys=True) + "\n")
    return rows


def metrics(trades: Iterable[dict[str, Any]]) -> dict[str, Any]:
    rows = [t for t in trades if t.get("status") == "closed"]
    values = [float(t.get("net_pnl_usd") or 0.0) for t in rows]
    wins = [v for v in values if v > 0]
    losses = [v for v in values if v < 0]
    gross_loss = abs(sum(losses))
    equity = 0.0
    peak = 0.0
    max_dd = 0.0
    by_symbol: dict[str, float] = {}
    for t, v in zip(rows, values):
        equity += v
        peak = max(peak, equity)
        max_dd = max(max_dd, peak - equity)
        by_symbol[str(t.get("symbol"))] = by_symbol.get(str(t.get("symbol")), 0.0) + max(0.0, v)
    positive_total = sum(max(0.0, v) for v in values)
    top_symbol_share = max(by_symbol.values()) / positive_total if by_symbol and positive_total else None
    avg_hold = sum(float(t.get("bars_held") or 0) for t in rows) / len(rows) if rows else None
    return {
        "closed": len(rows),
        "net_pnl_usd": round(sum(values), 4),
        "profit_factor": round(sum(wins) / gross_loss, 4) if gross_loss else None,
        "winrate": round(len(wins) / len(rows), 4) if rows else None,
        "max_drawdown_usd": round(max_dd, 4),
        "avg_net_r": round(sum(float(t.get("net_r") or 0.0) for t in rows) / len(rows), 4) if rows else None,
        "avg_hold_days": round(avg_hold, 2) if avg_hold is not None else None,
        "top_symbol_profit_share": round(top_symbol_share, 4) if top_symbol_share is not None else None,
    }


def split_metrics(trades: list[dict[str, Any]], split_date: pd.Timestamp) -> dict[str, Any]:
    train = [t for t in trades if pd.Timestamp(t["entry_date"]) < split_date]
    test = [t for t in trades if pd.Timestamp(t["entry_date"]) >= split_date]
    return {"train": metrics(train), "test": metrics(test), "all": metrics(trades)}


def select_variants(results: dict[str, list[dict[str, Any]]], split_date: pd.Timestamp, cfg: dict[str, Any]) -> list[str]:
    rows = []
    for vid, trades in results.items():
        stat = split_metrics(trades, split_date)
        test = stat["test"]
        train = stat["train"]
        if train["closed"] < 20 or test["closed"] < int(cfg["selection"]["min_test_closed"]):
            continue
        if test["net_pnl_usd"] <= float(cfg["selection"]["min_test_net_usd"]):
            continue
        pf = test["profit_factor"] or 0.0
        if pf < float(cfg["selection"]["min_test_pf"]):
            continue
        if (test["top_symbol_profit_share"] or 1.0) > float(cfg["selection"]["max_top_symbol_profit_share"]):
            continue
        rows.append((vid, pf, test["net_pnl_usd"], test["closed"], train["profit_factor"] or 0.0))
    rows.sort(key=lambda item: (item[1], item[2], item[3], item[4]), reverse=True)
    if rows:
        return [row[0] for row in rows[:8]]
    fallback = []
    for vid, trades in results.items():
        test = split_metrics(trades, split_date)["test"]
        fallback.append((vid, test["profit_factor"] or 0.0, test["net_pnl_usd"], test["closed"]))
    fallback.sort(key=lambda item: (item[1], item[2], item[3]), reverse=True)
    return [row[0] for row in fallback[:8]]


def annotate_news_presence(trades: list[dict[str, Any]], events: list[dict[str, Any]], lookback_days: int) -> dict[str, list[dict[str, Any]]]:
    by_symbol: dict[str, list[pd.Timestamp]] = {}
    for event in events:
        if _safe_float(event.get("event_score")) <= 0:
            continue
        at = event.get("available_ts")
        if at is None:
            continue
        day = _date(at.tz_convert(NY_TZ))
        for symbol in event.get("symbols") or []:
            by_symbol.setdefault(symbol, []).append(day)
    grouped = {"positive_news_recent": [], "no_recent_positive_news": []}
    for trade in trades:
        entry_day = pd.Timestamp(trade["entry_date"])
        recent = any(0 <= (entry_day - day).days <= lookback_days for day in by_symbol.get(str(trade["symbol"]), []))
        grouped["positive_news_recent" if recent else "no_recent_positive_news"].append(trade)
    return grouped


def persist(run_id: str, cfg: dict[str, Any], start: pd.Timestamp, end: pd.Timestamp,
            phase_results: dict[str, dict[str, list[dict[str, Any]]]], metrics_by_scope: dict[str, Any]) -> None:
    db = _resolve(cfg["data"]["research_db"])
    db.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db)
    try:
        conn.executescript(RUNS_DDL)
        conn.execute(
            "INSERT OR REPLACE INTO runs(run_id,generated_at,study_start,study_end,config_json) VALUES(?,?,?,?,?)",
            (run_id, datetime.now(timezone.utc).isoformat(), start.isoformat(), end.isoformat(), json.dumps(cfg, sort_keys=True)),
        )
        conn.execute("DELETE FROM variant_metrics WHERE run_id=?", (run_id,))
        conn.execute("DELETE FROM trades WHERE run_id=?", (run_id,))
        for key, stat in metrics_by_scope.items():
            phase, variant_id, scope = key.split("|", 2)
            conn.execute(
                "INSERT INTO variant_metrics(run_id,phase,variant_id,scope,metrics_json) VALUES(?,?,?,?,?)",
                (run_id, phase, variant_id, scope, json.dumps(stat, sort_keys=True)),
            )
        for phase, by_variant in phase_results.items():
            for variant_id, rows in by_variant.items():
                for t in rows:
                    conn.execute(
                        "INSERT OR REPLACE INTO trades(run_id,phase,variant_id,trade_id,symbol,entry_date,exit_date,status,net_pnl_usd,net_r,payload_json) "
                        "VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                        (
                            run_id, phase, variant_id, str(t.get("trade_id")), str(t.get("symbol")),
                            t.get("entry_date"), t.get("exit_date"), t.get("status"),
                            t.get("net_pnl_usd"), t.get("net_r"), json.dumps(t, default=str, sort_keys=True),
                        ),
                    )
        conn.commit()
    finally:
        conn.close()


def write_artifacts(
    *,
    cfg: dict[str, Any],
    run_id: str,
    phase_results: dict[str, dict[str, list[dict[str, Any]]]],
    metrics_by_scope: dict[str, Any],
    selected: list[str],
    split_date: pd.Timestamp,
    data_coverage: dict[str, Any],
    local_events: list[dict[str, Any]],
    reconstructed_events: list[dict[str, Any]],
) -> Path:
    out = _resolve(cfg["data"]["artifacts_dir"])
    out.mkdir(parents=True, exist_ok=True)
    summary = {
        "run_id": run_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "selected_variants": selected,
        "split_date": str(split_date.date()),
        "data_coverage": data_coverage,
        "metrics": metrics_by_scope,
        "local_events": len(local_events),
        "reconstructed_events": len(reconstructed_events),
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    rows = []
    for phase, by_variant in phase_results.items():
        for variant_id, trades in by_variant.items():
            for t in trades:
                flat = {
                    "phase": phase,
                    "variant_id": variant_id,
                    "trade_id": t.get("trade_id"),
                    "symbol": t.get("symbol"),
                    "entry_date": t.get("entry_date"),
                    "exit_date": t.get("exit_date"),
                    "exit_reason": t.get("exit_reason"),
                    "net_pnl_usd": t.get("net_pnl_usd"),
                    "net_r": t.get("net_r"),
                    "mfe_r": t.get("mfe_r"),
                    "mae_r": t.get("mae_r"),
                    "bars_held": t.get("bars_held"),
                    "evidence": json.dumps(t.get("evidence") or {}, sort_keys=True),
                }
                rows.append(flat)
    if rows:
        pd.DataFrame(rows).to_csv(out / "trades.csv", index=False)
    report = render_report(cfg, summary, phase_results, metrics_by_scope, selected)
    path = out / "STOCKS_SWING_EVENT_RS_PULLBACK_RESEARCH.md"
    path.write_text(report, encoding="utf-8")
    return path


def _fmt(value: Any) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, float):
        return f"{value:.4f}" if abs(value) < 10 else f"{value:.2f}"
    return str(value)


def _variant_settings_text(variant: Variant | None) -> str:
    if variant is None:
        return "n/a"
    return (
        f"`{variant.variant_id}`: impulse >= {variant.impulse_return_min * 100:.1f}%, "
        f"impulse >= {variant.impulse_atr_min:.2f} ATR, volume ratio >= {variant.volume_ratio_min:.1f}, "
        f"RS20 vs SPY >= {variant.rs20_min:.2f}, sector RS >= {variant.rs_sector_min:.2f}, "
        f"pullback `{variant.pullback_level}`, min stop {variant.min_stop_atr:.1f} ATR, "
        f"max stop {variant.max_stop_atr:.1f} ATR / 15%, TP {variant.tp1_r:.1f}R/{variant.tp2_r:.1f}R/runner, "
        f"max hold {variant.max_hold_days}d"
    )


def render_report(
    cfg: dict[str, Any],
    summary: dict[str, Any],
    phase_results: dict[str, dict[str, list[dict[str, Any]]]],
    metrics_by_scope: dict[str, Any],
    selected: list[str],
) -> str:
    variant_by_id = {variant.variant_id: variant for variant in variants()}
    lines = [
        "# Stock Swing Event RS Pullback V1 Research",
        "",
        "> Research-only. No Paper/live/proposed_signals tables were changed.",
        "",
        f"- Run: `{summary['run_id']}`",
        f"- Split date: `{summary['split_date']}`",
        f"- Local canonical stock events: `{summary['local_events']}`",
        f"- Reconstructed events: `{summary['reconstructed_events']}`",
        "",
        "## Data coverage",
        "",
    ]
    cov = summary["data_coverage"]
    lines += [
        f"- Trade symbols loaded: `{cov.get('symbols_loaded')}` / `{cov.get('symbols_requested')}`.",
        f"- Daily date range: `{cov.get('first_daily')}` to `{cov.get('last_daily')}`.",
        f"- SPY rows: `{cov.get('spy_rows')}`; VIX rows: `{cov.get('vix_rows')}`.",
        "",
        "## Top technical variants",
        "",
        "| Variant | Train closed | Train net | Train PF | Test closed | Test net | Test PF | Test WR | Top-symbol share |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    tech = phase_results.get("technical_skeleton", {})
    ranked = []
    for vid in tech:
        test = metrics_by_scope.get(f"technical_skeleton|{vid}|test", {})
        train = metrics_by_scope.get(f"technical_skeleton|{vid}|train", {})
        ranked.append((vid, test.get("profit_factor") or 0.0, test.get("net_pnl_usd") or -1e9, test.get("closed") or 0))
    ranked.sort(key=lambda item: (item[1], item[2], item[3]), reverse=True)
    for vid, *_ in ranked[:12]:
        train = metrics_by_scope.get(f"technical_skeleton|{vid}|train", {})
        test = metrics_by_scope.get(f"technical_skeleton|{vid}|test", {})
        lines.append(
            f"| `{vid}` | {_fmt(train.get('closed'))} | {_fmt(train.get('net_pnl_usd'))} | {_fmt(train.get('profit_factor'))} | "
            f"{_fmt(test.get('closed'))} | {_fmt(test.get('net_pnl_usd'))} | {_fmt(test.get('profit_factor'))} | "
            f"{_fmt(test.get('winrate'))} | {_fmt(test.get('top_symbol_profit_share'))} |"
        )
    lines += ["", "## News and ablation", "",
              "| Phase / scope | Variant | Closed | Net USD | PF | WR | Max DD | Avg hold |",
              "|---|---|---:|---:|---:|---:|---:|---:|"]
    for key, stat in sorted(metrics_by_scope.items()):
        phase, vid, scope = key.split("|", 2)
        if phase == "technical_skeleton" and scope in {"train", "test"}:
            continue
        if phase == "technical_skeleton" and vid not in selected:
            continue
        if phase != "technical_skeleton" and vid not in selected:
            continue
        label = f"{phase}/{scope}"
        lines.append(
            f"| `{label}` | `{vid}` | {_fmt(stat.get('closed'))} | {_fmt(stat.get('net_pnl_usd'))} | "
            f"{_fmt(stat.get('profit_factor'))} | {_fmt(stat.get('winrate'))} | "
            f"{_fmt(stat.get('max_drawdown_usd'))} | {_fmt(stat.get('avg_hold_days'))} |"
        )
    best = selected[0] if selected else None
    quality_variant = "imp050_ema21_stop15_tp20" if "imp050_ema21_stop15_tp20" in selected else best
    flow_variant = "imp025_ema21_stop15_tp20" if "imp025_ema21_stop15_tp20" in selected else None
    recommendation = "NO_PAPER_YET"
    reason = "No variant passed the minimum test robustness gates."
    if best:
        test = metrics_by_scope.get(f"technical_skeleton|{best}|test", {})
        local = metrics_by_scope.get(f"local_real_news|{best}|all", {})
        if (test.get("closed") or 0) >= int(cfg["selection"]["min_test_closed"]) and (test.get("net_pnl_usd") or 0) > 0:
            recommendation = "PAPER_CANARY"
            reason = (
                "Use technical skeleton as the entry engine; use news as score boost/blocker until "
                "the real-news sample reaches the configured minimum."
            )
            if (local.get("closed") or 0) >= int(cfg["selection"]["min_local_news_closed_for_news_claim"]) and (local.get("net_pnl_usd") or 0) > 0:
                reason = "Local causal-news sample is positive enough to require a catalyst in Paper V1."
    lines += [
        "",
        "## Recommendation",
        "",
        f"- Verdict: **{recommendation}**.",
        f"- Candidate variant: `{best or 'none'}`.",
        f"- Reason: {reason}",
        "",
        "Paper V1 settings if enabled:",
        "",
        "- Long-only.",
        "- Entry mode: `EVENT_RS_PULLBACK`.",
        "- Risk: `$10` full size, `$5` neutral/risk-reduced.",
        "- Stop: structural pullback low/Fib invalidation plus ATR buffer; no artificial tight stop.",
        "- News: canonical events are used point-in-time by `available_at`; reconstructed news is research-only.",
        "- Live: disabled until at least 30 clean Paper closes.",
        "",
        "Recommended Paper layout:",
        "",
        f"- Quality sleeve, 1x: {_variant_settings_text(variant_by_id.get(quality_variant or ''))}.",
        f"- Flow sleeve, 0.5x: {_variant_settings_text(variant_by_id.get(flow_variant or ''))}.",
        "- Do not require a catalyst yet. Positive causal news may boost tier; negative legal/dilution/delisting/calendar-risk news blocks or downgrades.",
        "- Record every candidate, rejected setup, news item `published_at/ingested_at/available_at`, impulse anchor, entry level, stop basis, MFE/MAE, and exit reason.",
    ]
    return "\n".join(lines)


def prepare_data(cfg: dict[str, Any]) -> tuple[dict[str, pd.DataFrame], dict[str, str], pd.Series, dict[str, Any]]:
    price_root = _resolve(cfg["data"]["price_root"])
    symbols, sector_map, benchmarks = load_universe(cfg)
    spy = load_ohlcv(price_root, "SPY", "1d")
    vix = load_ohlcv(price_root, "^VIX", "1d")
    regimes = market_regime(spy, vix)
    sector_etf_by_sector = (yaml.safe_load(_resolve(cfg["data"]["universe_config"]).read_text(encoding="utf-8")) or {}).get("sector_etfs", {}) or {}
    raw_frames: dict[str, pd.DataFrame] = {}
    for bench in sorted(benchmarks | set(sector_etf_by_sector.values())):
        raw_frames[bench] = load_ohlcv(price_root, bench, "1d")
    data: dict[str, pd.DataFrame] = {}
    for symbol in symbols:
        frame = load_ohlcv(price_root, symbol, "1d")
        if frame.empty:
            continue
        sector = sector_map.get(symbol)
        sector_df = raw_frames.get(str(sector_etf_by_sector.get(sector, ""))) if sector else None
        enriched = add_features(frame, spy, sector_df)
        enriched["market_regime"] = regimes.reindex(enriched.index).ffill()
        data[symbol] = enriched
    first_daily = min((df.index.min() for df in data.values() if not df.empty), default=None)
    last_daily = max((df.index.max() for df in data.values() if not df.empty), default=None)
    coverage = {
        "symbols_requested": len(symbols),
        "symbols_loaded": len(data),
        "first_daily": str(first_daily.date()) if first_daily is not None else None,
        "last_daily": str(last_daily.date()) if last_daily is not None else None,
        "spy_rows": len(spy),
        "vix_rows": len(vix),
    }
    return data, sector_map, regimes, coverage


def run(cfg: dict[str, Any], *, phase: str, fetch_reconstructed: bool) -> tuple[dict[str, Any], Path]:
    start = _date(cfg["data"]["study_start"])
    end = _date(cfg["data"]["study_end"])
    split_date = end - pd.Timedelta(days=180)
    data, sectors, regimes, coverage = prepare_data(cfg)
    all_variants = variants()
    fingerprint = json.dumps({"cfg": cfg, "variants": [asdict(v) for v in all_variants], "phase": phase}, sort_keys=True)
    run_id = hashlib.sha1(fingerprint.encode("utf-8")).hexdigest()[:16]

    phase_results: dict[str, dict[str, list[dict[str, Any]]]] = {}
    metrics_by_scope: dict[str, Any] = {}

    if phase in {"all", "technical"}:
        phase_results["technical_skeleton"] = {}
        for idx, variant in enumerate(all_variants, start=1):
            rows = backtest_technical(data, sectors, regimes, variant, cfg, start, end)
            phase_results["technical_skeleton"][variant.variant_id] = rows
            split = split_metrics(rows, split_date)
            for scope, stat in split.items():
                metrics_by_scope[f"technical_skeleton|{variant.variant_id}|{scope}"] = stat
            if idx % 8 == 0 or idx == len(all_variants):
                print(f"technical_skeleton: {idx}/{len(all_variants)} variants", flush=True)

    selected = select_variants(phase_results.get("technical_skeleton", {}), split_date, cfg)
    variant_by_id = {v.variant_id: v for v in all_variants}
    selected_variants = [variant_by_id[vid] for vid in selected if vid in variant_by_id]

    local_events: list[dict[str, Any]] = []
    if phase in {"all", "local-news", "ablation"}:
        local_events = load_local_events(cfg, start, end)
        phase_results["local_real_news"] = {}
        for variant in selected_variants:
            rows = backtest_events(
                events=local_events, data=data, sectors=sectors, regimes=regimes, variant=variant,
                cfg=cfg, phase="local_real_news", start=start, end=end,
            )
            phase_results["local_real_news"][variant.variant_id] = rows
            metrics_by_scope[f"local_real_news|{variant.variant_id}|all"] = metrics(rows)

    reconstructed_events: list[dict[str, Any]] = []
    if phase in {"all", "reconstructed-news", "ablation"}:
        if fetch_reconstructed:
            reconstructed_events = fetch_reconstructed_news(cfg, list(data.keys()), start, end)
        else:
            cache_path = _resolve(cfg["news"]["reconstructed_cache"])
            if cache_path.exists():
                reconstructed_events = []
                for line in cache_path.read_text(encoding="utf-8").splitlines():
                    if not line.strip():
                        continue
                    item = json.loads(line)
                    item["available_ts"] = _parse_dt(item.get("available_at"))
                    item["symbols"] = _json_list(item.get("trusted_symbols_json"))
                    reconstructed_events.append(item)
        phase_results["reconstructed_news"] = {}
        for variant in selected_variants:
            rows = backtest_events(
                events=reconstructed_events, data=data, sectors=sectors, regimes=regimes, variant=variant,
                cfg=cfg, phase="reconstructed_news", start=start, end=end,
            )
            phase_results["reconstructed_news"][variant.variant_id] = rows
            metrics_by_scope[f"reconstructed_news|{variant.variant_id}|all"] = metrics(rows)

    if phase in {"all", "ablation"}:
        if not local_events:
            local_events = load_local_events(cfg, start, end)
        for vid in selected:
            base = phase_results.get("technical_skeleton", {}).get(vid, [])
            grouped = annotate_news_presence(base, local_events, int(cfg["news"]["local_lookback_days"]))
            for scope, rows in grouped.items():
                metrics_by_scope[f"ablation|{vid}|{scope}"] = metrics(rows)

    persist(run_id, cfg, start, end, phase_results, metrics_by_scope)
    report = write_artifacts(
        cfg=cfg, run_id=run_id, phase_results=phase_results, metrics_by_scope=metrics_by_scope,
        selected=selected, split_date=split_date, data_coverage=coverage,
        local_events=local_events, reconstructed_events=reconstructed_events,
    )
    return {
        "run_id": run_id,
        "selected": selected,
        "coverage": coverage,
        "metrics": metrics_by_scope,
        "report": str(report),
    }, report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=str(Path(__file__).with_name("config.yaml")))
    parser.add_argument("--phase", choices=["all", "technical", "local-news", "reconstructed-news", "ablation"], default="all")
    parser.add_argument("--fetch-reconstructed-news", action="store_true")
    args = parser.parse_args(argv)
    cfg = load_config(Path(args.config))
    result, report = run(cfg, phase=args.phase, fetch_reconstructed=args.fetch_reconstructed_news)
    print(json.dumps({
        "run_id": result["run_id"],
        "selected": result["selected"][:5],
        "coverage": result["coverage"],
        "report": str(report),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
