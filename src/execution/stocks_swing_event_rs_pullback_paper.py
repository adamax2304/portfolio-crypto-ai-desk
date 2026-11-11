"""Paper lane for Stock Swing Event RS Pullback V1.

The lane is daily/swing, long-only, and Paper-only. It scans completed stock
daily bars for a strong impulse, waits for a pullback/reclaim near EMA21, then
registers a forward Paper signal with a 25-day validity window. Canonical news
can boost or block a candidate, but positive news is not mandatory.
"""
from __future__ import annotations

import json
import math
import sqlite3
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from src.models import TradeIdea
from src.storage.file_store import FileStore


ROOT = Path(__file__).resolve().parents[2]
TRACKER_TIMEFRAME = "1d"
ENTRY_MODE = "EVENT_RS_PULLBACK"

DEFAULT_CFG: dict[str, Any] = {
    "enabled": True,
    "live_enabled": False,
    "strategy_id": "stocks_swing_event_rs_pullback_paper_v1",
    "paper_lane": "paper_stocks_swing_event_rs_pullback",
    "timeframe": "1d",
    "tracker_timeframe": TRACKER_TIMEFRAME,
    "entry_mode": ENTRY_MODE,
    "use_default_universe": True,
    "symbols": [],
    "scan_recent_confirmations_days": 3,
    "max_signals_per_profile_run": 12,
    "validity_window_hours": 600,
    "universe": {"min_price": 5.0, "min_avg_dollar_volume_30d": 25_000_000},
    "risk": {
        "neutral_size_weight": 0.5,
        "risk_off_size_weight": 0.5,
        "stop_buffer_atr": 0.25,
        "max_stop_pct": 15.0,
    },
    "execution": {
        "max_pullback_days": 10,
        "impulse_cluster_days": 3,
        "max_hold_days": 25,
        "entry_timeout_days": 1,
        "same_bar_policy": "stop_first",
    },
    "news": {
        "lookback_days": 7,
        "score_boost_max": 8,
        "bullish_event_types": [
            "earnings", "guidance", "analyst_action", "partnership", "mna",
            "product_launch", "contract_award", "strategic_investment",
            "fda_clinical", "buyback",
        ],
        "blocking_event_types": [
            "legal_risk", "offering_dilution", "exchange_delisting",
            "margin_delisting", "sec_filing", "calendar_risk",
        ],
        "trusted_source_qualities": [
            "regulator", "primary", "company_pr", "reputable", "secondary",
        ],
    },
    "profiles": [],
}


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    out = deepcopy(base)
    for key, value in (override or {}).items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = _deep_merge(out[key], value)
        else:
            out[key] = value
    return out


def load_cfg() -> dict[str, Any]:
    path = ROOT / "config" / "paper" / "stocks" / "event_rs_pullback.yaml"
    cfg = deepcopy(DEFAULT_CFG)
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        supplied = raw.get("stocks_swing_event_rs_pullback_paper") or {}
        if isinstance(supplied, dict):
            cfg = _deep_merge(cfg, supplied)
    except Exception:
        pass
    return cfg


def _utc(value: datetime | None = None) -> datetime:
    moment = value or datetime.now(timezone.utc)
    return moment.replace(tzinfo=timezone.utc) if moment.tzinfo is None else moment.astimezone(timezone.utc)


def _float(value: Any, default: float | None = None) -> float | None:
    try:
        if value in (None, "") or pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default


def _raw(signal: dict[str, Any]) -> dict[str, Any]:
    value = signal.get("raw_idea_json") if isinstance(signal, dict) else None
    if isinstance(value, dict):
        return dict(value)
    try:
        parsed = json.loads(value or "{}")
        return parsed if isinstance(parsed, dict) else {}
    except (TypeError, ValueError, json.JSONDecodeError):
        return {}


def _profile_ids(cfg: dict[str, Any]) -> set[str]:
    return {str(p.get("profile_id") or "") for p in (cfg.get("profiles") or []) if p.get("profile_id")}


def matches_signal(signal: dict[str, Any], cfg: dict[str, Any] | None = None) -> bool:
    cfg = cfg or load_cfg()
    raw = _raw(signal)
    return bool(
        cfg.get("enabled", True)
        and str(signal.get("asset_class") or "").lower() == "stocks"
        and str(signal.get("mode") or "").lower() == "swing"
        and str(raw.get("paper_entry_profile") or "") in _profile_ids(cfg)
        and raw.get("paper_lane") == cfg.get("paper_lane")
    )


def configured_symbols(cfg: dict[str, Any] | None = None) -> list[str]:
    cfg = cfg or load_cfg()
    explicit = [str(item).upper() for item in (cfg.get("symbols") or []) if str(item).strip()]
    if explicit:
        return sorted(dict.fromkeys(explicit))
    if not cfg.get("use_default_universe", True):
        return []
    try:
        raw = yaml.safe_load((ROOT / "config" / "stocks" / "universe.yaml").read_text(encoding="utf-8")) or {}
    except Exception:
        return []
    indices = {str(item).upper() for item in (raw.get("indices") or [])}
    sector_etfs = {str(item).upper() for item in (raw.get("sector_etfs", {}) or {}).values()}
    benchmarks = indices | sector_etfs | {str(raw.get("volatility_index") or "").upper()}
    symbols = [
        str(item).upper()
        for item in (raw.get("default_symbols") or [])
        if str(item).upper() not in benchmarks and not str(item).startswith("^")
    ]
    return sorted(dict.fromkeys(symbols))


def _sector_map() -> tuple[dict[str, str], dict[str, str]]:
    try:
        raw = yaml.safe_load((ROOT / "config" / "stocks" / "universe.yaml").read_text(encoding="utf-8")) or {}
    except Exception:
        return {}, {}
    return (
        {str(k).upper(): str(v) for k, v in (raw.get("symbol_sector_map") or {}).items()},
        {str(k): str(v).upper() for k, v in (raw.get("sector_etfs") or {}).items()},
    )


def _normalize_daily(frame: pd.DataFrame | None) -> pd.DataFrame:
    if frame is None or frame.empty:
        return pd.DataFrame()
    out = frame.copy()
    out = out.rename(columns={str(c): str(c).lower() for c in out.columns})
    if "timestamp" not in out.columns:
        return pd.DataFrame()
    out["timestamp"] = pd.to_datetime(out["timestamp"], utc=True, errors="coerce")
    for col in ("open", "high", "low", "close", "volume"):
        if col not in out.columns:
            return pd.DataFrame()
        out[col] = pd.to_numeric(out[col], errors="coerce")
    out = out.dropna(subset=["timestamp", "open", "high", "low", "close", "volume"]).copy()
    if out.empty:
        return pd.DataFrame()
    out["date"] = out["timestamp"].dt.tz_convert("America/New_York").dt.tz_localize(None).dt.normalize()
    out = out.drop_duplicates("date").sort_values("date").set_index("date")
    return out[["timestamp", "open", "high", "low", "close", "volume"]]


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
    out["sma50"] = out["close"].rolling(50).mean()
    out["sma200"] = out["close"].rolling(200).mean()
    out["ema21"] = out["close"].ewm(span=21, adjust=False).mean()
    out["vol_avg20"] = out["volume"].rolling(20).mean().shift(1)
    out["volume_ratio"] = out["volume"] / out["vol_avg20"]
    out["dollar_volume_30d"] = (out["close"] * out["volume"]).rolling(30).mean()
    out["ret1"] = out["close"] / prev_close - 1.0
    out["ret20"] = out["close"].pct_change(20)
    out["ret63"] = out["close"].pct_change(63)
    spy_close = spy["close"].reindex(out.index).ffill() if not spy.empty else pd.Series(index=out.index, dtype=float)
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


def _market_regime(spy: pd.DataFrame, vix: pd.DataFrame | None = None) -> pd.Series:
    if spy.empty:
        return pd.Series(dtype=str)
    s = spy.copy()
    s["sma50"] = s["close"].rolling(50).mean()
    s["sma200"] = s["close"].rolling(200).mean()
    vix_close = vix["close"].reindex(s.index).ffill() if vix is not None and not vix.empty else pd.Series(index=s.index, dtype=float)
    labels: list[str] = []
    for _, row in s.iterrows():
        v = vix_close.get(row.name)
        if row["close"] < row["sma200"] or (pd.notna(v) and float(v) >= 30):
            labels.append("risk_off")
        elif row["close"] > row["sma50"] and row["close"] > row["sma200"] and (pd.isna(v) or float(v) < 22):
            labels.append("risk_on")
        else:
            labels.append("neutral")
    return pd.Series(labels, index=s.index)


def _reclaim(row: pd.Series, level: float, require_green: bool) -> bool:
    if not math.isfinite(level) or level <= 0:
        return False
    span = float(row["high"] - row["low"])
    closes_well = span <= 0 or float(row["close"]) >= float(row["low"]) + 0.50 * span
    green_ok = float(row["close"]) >= float(row["open"]) if require_green else True
    return float(row["low"]) <= level and float(row["close"]) >= level and closes_well and green_ok


def _level_for(row: pd.Series, impulse_low: float, impulse_high: float, profile: dict[str, Any]) -> tuple[float, str]:
    fib50 = impulse_high - 0.50 * (impulse_high - impulse_low)
    fib618 = impulse_high - 0.618 * (impulse_high - impulse_low)
    ema21 = _float(row.get("ema21"), math.nan)
    level_type = str(profile.get("pullback_level") or "ema21")
    if level_type == "fib50":
        return fib50, "fib50"
    if level_type == "fib618":
        return fib618, "fib618"
    if level_type == "ema21":
        return float(ema21), "ema21"
    candidates = [("fib50", fib50), ("ema21", float(ema21)), ("fib618", fib618)]
    candidates = [(name, val) for name, val in candidates if math.isfinite(val) and val > 0]
    if not candidates:
        return math.nan, "none"
    close = float(row["close"])
    return min(candidates, key=lambda item: abs(item[1] - close))[1], "hybrid"


def _passes_common_filters(row: pd.Series, profile: dict[str, Any], cfg: dict[str, Any]) -> tuple[bool, str | None]:
    universe = cfg.get("universe") or {}
    if float(row["close"]) < float(universe.get("min_price") or 5.0):
        return False, "PRICE_TOO_LOW"
    if _float(row.get("dollar_volume_30d"), 0.0) < float(universe.get("min_avg_dollar_volume_30d") or 25_000_000):
        return False, "DOLLAR_VOLUME_TOO_LOW"
    if _float(row.get("atr14_prev"), 0.0) <= 0:
        return False, "ATR_MISSING"
    if _float(row.get("volume_ratio"), 0.0) < float(profile.get("volume_ratio_min") or 0.0):
        return False, "VOLUME_RATIO_LOW"
    if _float(row.get("rs20_spy"), -999.0) < float(profile.get("rs20_min") or 0.0):
        return False, "RS20_SPY_LOW"
    if _float(row.get("rs63_spy"), -999.0) < float(profile.get("rs63_min") or 0.0):
        return False, "RS63_SPY_LOW"
    if _float(row.get("rs20_sector"), 0.0) < float(profile.get("rs_sector_min") or 0.0):
        return False, "RS_SECTOR_LOW"
    return True, None


def _is_impulse(row: pd.Series, profile: dict[str, Any]) -> bool:
    atr = _float(row.get("atr14_prev"), 0.0)
    if not atr or atr <= 0:
        return False
    move = _float(row.get("ret1"), 0.0) or 0.0
    tr_atr = (_float(row.get("true_range"), 0.0) or 0.0) / atr
    impulse_return_min = float(profile.get("impulse_return_min") or 0.0)
    close_strong = float(row["close"]) > float(row["open"]) or move >= impulse_return_min * 1.25
    return move >= impulse_return_min and tr_atr >= float(profile.get("impulse_atr_min") or 0.0) and close_strong


def _size_weight(regime: str, profile: dict[str, Any], cfg: dict[str, Any]) -> float:
    sleeve = max(0.0, min(1.0, float(profile.get("sleeve_size_weight") or 1.0)))
    if regime == "risk_on":
        return sleeve
    risk = cfg.get("risk") or {}
    if regime == "neutral":
        return sleeve * float(risk.get("neutral_size_weight") or 0.5) if profile.get("allow_neutral", True) else 0.0
    if regime == "risk_off":
        return sleeve * float(risk.get("risk_off_size_weight") or 0.5) if profile.get("allow_risk_off", False) else 0.0
    return 0.0


def _json_symbols(value: Any) -> set[str]:
    try:
        parsed = json.loads(value or "[]")
    except Exception:
        parsed = []
    return {str(item).upper().replace("$", "") for item in parsed} if isinstance(parsed, list) else set()


def _event_time(row: sqlite3.Row | dict[str, Any]) -> str | None:
    for key in ("available_at", "effective_at", "published_at", "created_at"):
        value = row[key] if isinstance(row, sqlite3.Row) and key in row.keys() else row.get(key) if isinstance(row, dict) else None
        if value:
            return str(value)
    return None


def _news_context(conn: sqlite3.Connection, symbol: str, as_of: datetime, cfg: dict[str, Any]) -> dict[str, Any]:
    news_cfg = cfg.get("news") or {}
    cutoff = as_of - timedelta(days=float(news_cfg.get("lookback_days") or 7))
    bullish_types = {str(x).lower() for x in (news_cfg.get("bullish_event_types") or [])}
    blocking_types = {str(x).lower() for x in (news_cfg.get("blocking_event_types") or [])}
    trusted_qualities = {str(x).lower() for x in (news_cfg.get("trusted_source_qualities") or [])}
    try:
        exists = conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name='news_canonical_events'"
        ).fetchone()
        if not exists:
            return {"state": "NO_CANONICAL_NEWS_TABLE", "boost": 0.0, "events": [], "blocked": False}
        cols = {str(r[1]) for r in conn.execute("PRAGMA table_info(news_canonical_events)")}
        time_col = (
            "available_at" if "available_at" in cols
            else "effective_at" if "effective_at" in cols
            else "published_at" if "published_at" in cols
            else ""
        )
        if not time_col:
            return {"state": "NEWS_TIME_COLUMN_MISSING", "boost": 0.0, "events": [], "blocked": False}
        symbol_col = "trusted_symbols_json" if "trusted_symbols_json" in cols else (
            "mentioned_symbols_json" if "mentioned_symbols_json" in cols else ""
        )
        if not symbol_col:
            return {"state": "NEWS_SYMBOL_COLUMN_MISSING", "boost": 0.0, "events": [], "blocked": False}
        fields = {
            "title": "title" if "title" in cols else "NULL",
            "source": "source" if "source" in cols else "NULL",
            "available_at": time_col,
            "effective_at": "effective_at" if "effective_at" in cols else "published_at" if "published_at" in cols else "NULL",
            "published_at": "published_at" if "published_at" in cols else "NULL",
            "event_type": "event_type" if "event_type" in cols else "NULL",
            "direction_hint": "direction_hint" if "direction_hint" in cols else "NULL",
            "source_quality": "source_quality" if "source_quality" in cols else "NULL",
            "confidence": "confidence" if "confidence" in cols else "NULL",
            "trusted_symbols_json": symbol_col,
            "linkage_allowed": "linkage_allowed" if "linkage_allowed" in cols else "1",
        }
        asset_clause = "AND lower(COALESCE(asset_class,''))='stocks'" if "asset_class" in cols else ""
        rows = conn.execute(
            "SELECT "
            f"{fields['title']} AS title,{fields['source']} AS source,"
            f"{fields['available_at']} AS available_at,{fields['effective_at']} AS effective_at,"
            f"{fields['published_at']} AS published_at,{fields['event_type']} AS event_type,"
            f"{fields['direction_hint']} AS direction_hint,{fields['source_quality']} AS source_quality,"
            f"{fields['confidence']} AS confidence,{fields['trusted_symbols_json']} AS trusted_symbols_json,"
            f"{fields['linkage_allowed']} AS linkage_allowed "
            "FROM news_canonical_events WHERE "
            f"datetime({time_col}) >= datetime(?) "
            f"AND datetime({time_col}) <= datetime(?) "
            f"{asset_clause} "
            f"ORDER BY datetime({time_col}) DESC LIMIT 300",
            (cutoff.isoformat(), as_of.isoformat()),
        ).fetchall()
    except Exception:
        return {"state": "NEWS_QUERY_ERROR", "boost": 0.0, "events": [], "blocked": False}

    events: list[dict[str, Any]] = []
    blocked: list[dict[str, Any]] = []
    boost = 0.0
    for row in rows:
        if symbol.upper() not in _json_symbols(row["trusted_symbols_json"]):
            continue
        if int(row["linkage_allowed"] or 0) != 1:
            continue
        etype = str(row["event_type"] or "").lower()
        hint = str(row["direction_hint"] or "").lower()
        quality = str(row["source_quality"] or "").lower()
        event = {
            "title": str(row["title"] or "")[:180],
            "source": str(row["source"] or ""),
            "event_type": etype,
            "direction_hint": hint,
            "source_quality": quality,
            "confidence": _float(row["confidence"], 0.0),
            "available_at": _event_time(row),
        }
        if etype in blocking_types or hint == "bearish":
            blocked.append(event)
            continue
        if etype in bullish_types and (not trusted_qualities or quality in trusted_qualities) and hint != "bearish":
            conf = _float(row["confidence"], 0.5) or 0.5
            boost = max(boost, min(float(news_cfg.get("score_boost_max") or 8), 3.0 + 5.0 * conf))
            events.append(event)
    if blocked:
        return {
            "state": "BLOCKED_BY_RECENT_NEWS",
            "boost": 0.0,
            "events": events[:3],
            "blocked": True,
            "block_reason": blocked[0],
        }
    return {
        "state": "POSITIVE_RECENT_NEWS" if events else "NO_NEWS_REQUIRED",
        "boost": round(boost, 3),
        "events": events[:3],
        "blocked": False,
    }


def _candidate_for_confirmation(
    *,
    symbol: str,
    df: pd.DataFrame,
    profile: dict[str, Any],
    cfg: dict[str, Any],
    confirmation_idx: int,
    sector: str | None = None,
) -> dict[str, Any] | None:
    if df.empty or confirmation_idx <= 0 or confirmation_idx >= len(df):
        return None
    max_pullback = int((cfg.get("execution") or {}).get("max_pullback_days") or 10)
    cluster_days = int((cfg.get("execution") or {}).get("impulse_cluster_days") or 3)
    stop_buffer = float((cfg.get("risk") or {}).get("stop_buffer_atr") or 0.25)
    max_stop_pct = float((cfg.get("risk") or {}).get("max_stop_pct") or 15.0)
    best: dict[str, Any] | None = None
    start = max(220, confirmation_idx - max_pullback - cluster_days - 1)
    for impulse_idx in range(start, confirmation_idx):
        impulse_row = df.iloc[impulse_idx]
        ok, reason = _passes_common_filters(impulse_row, profile, cfg)
        if not ok or not _is_impulse(impulse_row, profile):
            continue
        end_cluster = impulse_idx
        for k in range(impulse_idx + 1, min(len(df), impulse_idx + cluster_days)):
            if float(df.iloc[k]["close"]) >= float(df.iloc[k - 1]["close"]):
                end_cluster = k
            else:
                break
        if confirmation_idx <= end_cluster or confirmation_idx > end_cluster + max_pullback:
            continue
        impulse = df.iloc[impulse_idx:end_cluster + 1]
        impulse_low = float(impulse["low"].min())
        impulse_high = float(impulse["high"].max())
        if impulse_high <= impulse_low:
            continue
        row = df.iloc[confirmation_idx]
        atr = _float(row.get("atr14"), _float(row.get("atr14_prev"), 0.0)) or 0.0
        if atr <= 0:
            continue
        raw_level, level_name = _level_for(row, impulse_low, impulse_high, profile)
        level = raw_level + float(profile.get("touch_tolerance_atr") or 0.20) * atr
        if not _reclaim(row, level, bool(profile.get("require_green_reclaim", False))):
            continue
        regime = str(row.get("market_regime") or "neutral")
        size_weight = _size_weight(regime, profile, cfg)
        if size_weight <= 0:
            continue
        entry_low = float(row["close"])
        entry_high = entry_low + float(profile.get("max_chase_atr") or 0.75) * atr
        structural_low = min(float(df.iloc[end_cluster + 1:confirmation_idx + 1]["low"].min()), raw_level)
        structural_stop = structural_low - stop_buffer * atr
        min_stop = entry_high - float(profile.get("min_stop_atr") or 1.5) * atr
        stop = min(structural_stop, min_stop)
        risk = entry_high - stop
        if risk <= 0:
            continue
        risk_atr = risk / atr
        stop_pct = risk / entry_high * 100.0
        if risk_atr > float(profile.get("max_stop_atr") or 2.8) or stop_pct > max_stop_pct:
            continue
        score = float(profile.get("base_score") or 70)
        score += min(6.0, max(0.0, (_float(impulse_row.get("ret1"), 0.0) or 0.0) - float(profile.get("impulse_return_min") or 0.0)) * 100.0)
        score += min(4.0, max(0.0, (_float(impulse_row.get("volume_ratio"), 0.0) or 0.0) - float(profile.get("volume_ratio_min") or 0.0)) * 2.0)
        score += min(4.0, max(0.0, (_float(impulse_row.get("rs20_spy"), 0.0) or 0.0) - float(profile.get("rs20_min") or 0.0)) * 100.0)
        candidate = {
            "symbol": symbol.upper(),
            "profile": dict(profile),
            "profile_id": str(profile["profile_id"]),
            "variant_id": str(profile.get("variant_id") or ""),
            "entry_mode": ENTRY_MODE,
            "confirmation_idx": confirmation_idx,
            "confirmation_at": pd.to_datetime(row["timestamp"], utc=True).to_pydatetime().isoformat(),
            "confirmation_date": str(df.index[confirmation_idx].date()),
            "impulse_date": str(df.index[impulse_idx].date()),
            "entry_low": round(entry_low, 6),
            "entry_high": round(entry_high, 6),
            "entry_trigger": round(entry_high, 6),
            "invalidation": round(stop, 6),
            "tp1": round(entry_high + float(profile.get("tp1_r") or 2.0) * risk, 6),
            "tp2": round(entry_high + float(profile.get("tp2_r") or 3.0) * risk, 6),
            "tp3": round(entry_high + float(profile.get("tp3_r") or 4.0) * risk, 6),
            "risk_per_unit": round(risk, 6),
            "score": round(min(100.0, score), 3),
            "tier": "A" if score >= 82 else "B",
            "market_regime": regime,
            "size_weight": round(size_weight, 4),
            "sector": sector or "",
            "pullback_level": level_name,
            "impulse_return": round(_float(impulse_row.get("ret1"), 0.0) or 0.0, 5),
            "impulse_tr_atr": round((_float(impulse_row.get("true_range"), 0.0) or 0.0) / max(_float(impulse_row.get("atr14_prev"), 1.0) or 1.0, 1e-9), 4),
            "volume_ratio": round(_float(impulse_row.get("volume_ratio"), 0.0) or 0.0, 4),
            "rs20_spy": round(_float(impulse_row.get("rs20_spy"), 0.0) or 0.0, 5),
            "rs63_spy": round(_float(impulse_row.get("rs63_spy"), 0.0) or 0.0, 5),
            "rs20_sector": round(_float(impulse_row.get("rs20_sector"), 0.0) or 0.0, 5),
            "stop_distance_pct": round(stop_pct, 4),
            "stop_distance_atr": round(risk_atr, 4),
        }
        if best is None or float(candidate["score"]) > float(best["score"]):
            best = candidate
    return best


def scan_candidates(*, project_config: Any, cfg: dict[str, Any] | None = None,
                    now: datetime | None = None, db_path: Path | None = None) -> list[dict[str, Any]]:
    cfg = cfg or load_cfg()
    moment = _utc(now)
    file_store = FileStore(project_config)
    spy = _normalize_daily(file_store.load_stocks_ohlcv("SPY", "1d"))
    vix = _normalize_daily(file_store.load_stocks_ohlcv("^VIX", "1d"))
    if spy.empty:
        return []
    regimes = _market_regime(spy, vix)
    sectors, sector_etfs = _sector_map()
    sector_frames: dict[str, pd.DataFrame] = {}
    for sector, etf in sector_etfs.items():
        sector_frames[sector] = _normalize_daily(file_store.load_stocks_ohlcv(etf, "1d"))

    selected: list[dict[str, Any]] = []
    symbols = configured_symbols(cfg)
    recent_days = max(1, int(cfg.get("scan_recent_confirmations_days") or 3))
    max_age = pd.Timestamp(moment) - pd.Timedelta(days=recent_days + 2)
    for symbol in symbols:
        raw = _normalize_daily(file_store.load_stocks_ohlcv(symbol, "1d"))
        if raw.empty or len(raw) < 240:
            continue
        sector = sectors.get(symbol, "")
        frame = add_features(raw, spy, sector_frames.get(sector))
        if not regimes.empty:
            frame["market_regime"] = regimes.reindex(frame.index).ffill().fillna("neutral")
        else:
            frame["market_regime"] = "neutral"
        if frame.empty:
            continue
        recent_indices = []
        for idx in range(max(220, len(frame) - recent_days), len(frame)):
            ts = pd.to_datetime(frame.iloc[idx]["timestamp"], utc=True, errors="coerce")
            if pd.isna(ts) or ts < max_age:
                continue
            recent_indices.append(idx)
        for profile in (cfg.get("profiles") or []):
            if not profile.get("profile_id"):
                continue
            best_for_symbol: dict[str, Any] | None = None
            for idx in recent_indices:
                candidate = _candidate_for_confirmation(
                    symbol=symbol, df=frame, profile=profile, cfg=cfg,
                    confirmation_idx=idx, sector=sector,
                )
                if candidate and (best_for_symbol is None or candidate["score"] > best_for_symbol["score"]):
                    best_for_symbol = candidate
            if best_for_symbol is not None:
                selected.append(best_for_symbol)

    path = db_path or Path(project_config.db_path)
    try:
        conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True, timeout=30.0)
        conn.row_factory = sqlite3.Row
    except Exception:
        conn = None
    try:
        for candidate in selected:
            news = (
                _news_context(conn, candidate["symbol"], moment, cfg)
                if conn is not None else
                {"state": "NEWS_DB_UNAVAILABLE", "boost": 0.0, "events": [], "blocked": False}
            )
            candidate["news_context"] = news
            if news.get("blocked"):
                candidate["blocked"] = True
                candidate["block_reason"] = "recent_negative_or_blocking_news"
                continue
            candidate["score"] = round(min(100.0, float(candidate["score"]) + float(news.get("boost") or 0.0)), 3)
            candidate["tier"] = "A" if float(candidate["score"]) >= 82 else "B"
    finally:
        if conn is not None:
            conn.close()
    selected = [c for c in selected if not c.get("blocked")]
    selected.sort(key=lambda item: (item["profile_id"], -float(item["score"]), item["symbol"]))
    capped: list[dict[str, Any]] = []
    per_profile_cap = max(1, int(cfg.get("max_signals_per_profile_run") or 12))
    counts: dict[str, int] = {}
    for item in selected:
        pid = str(item["profile_id"])
        counts[pid] = counts.get(pid, 0)
        if counts[pid] >= per_profile_cap:
            continue
        counts[pid] += 1
        capped.append(item)
    return capped


def _already_registered(conn: sqlite3.Connection, candidate: dict[str, Any], cfg: dict[str, Any]) -> bool:
    try:
        rows = conn.execute(
            "SELECT raw_idea_json FROM proposed_signals "
            "WHERE asset_class='stocks' AND mode='swing' AND symbol=?",
            (str(candidate["symbol"]).upper(),),
        ).fetchall()
    except sqlite3.OperationalError:
        return False
    for (raw_json,) in rows:
        try:
            raw = json.loads(raw_json or "{}")
        except Exception:
            raw = {}
        if not isinstance(raw, dict):
            continue
        detail = raw.get("stock_swing_event_rs_pullback") or {}
        if (
            raw.get("paper_lane") == cfg.get("paper_lane")
            and raw.get("paper_entry_profile") == candidate.get("profile_id")
            and str(detail.get("confirmation_date") or "") == str(candidate.get("confirmation_date") or "")
        ):
            return True
    return False


def _idea(candidate: dict[str, Any], cfg: dict[str, Any], now: datetime) -> TradeIdea:
    entry = float(candidate["entry_high"])
    stop = float(candidate["invalidation"])
    profile = candidate.get("profile") or {}
    news = candidate.get("news_context") or {}
    setup = {
        "entry_low": float(candidate["entry_low"]),
        "entry_high": entry,
        "invalidation": stop,
        "tp1": float(candidate["tp1"]),
        "tp2": float(candidate["tp2"]),
        "tp3": float(candidate["tp3"]),
        "atr": None,
        "entry_timeout_days": (cfg.get("execution") or {}).get("entry_timeout_days"),
        "max_hold_days": (cfg.get("execution") or {}).get("max_hold_days"),
    }
    detail = {
        key: candidate.get(key)
        for key in (
            "variant_id", "confirmation_at", "confirmation_date", "impulse_date",
            "market_regime", "size_weight", "pullback_level", "impulse_return",
            "impulse_tr_atr", "volume_ratio", "rs20_spy", "rs63_spy",
            "rs20_sector", "stop_distance_pct", "stop_distance_atr", "sector",
        )
    }
    raw = {
        "pre_gate_tier": candidate["tier"],
        "final_tier": candidate["tier"],
        "demoted_by_gate": False,
        "paper_entry_profile": candidate["profile_id"],
        "paper_lane": cfg["paper_lane"],
        "paper_entry_policy_version": "stocks_swing_event_rs_pullback_v1",
        "paper_entry_confirmation": "daily_impulse_rs_pullback_reclaim",
        "paper_execution_entry_mode": ENTRY_MODE,
        "paper_size_weight": float(candidate["size_weight"]),
        "paper_size_reason": f"{profile.get('name', 'profile')}_sleeve_{candidate['market_regime']}",
        "validity_window_hours": float(cfg.get("validity_window_hours") or 600),
        "source_research": cfg.get("source_research"),
        "stock_swing_event_rs_pullback": detail,
        "news_context": news,
        "setup": setup,
        "structured": {
            "sector": candidate.get("sector"),
            "market_regime": candidate.get("market_regime"),
            "rs_vs_spy": candidate.get("rs20_spy"),
            "rs20_sector": candidate.get("rs20_sector"),
            "volume_ratio": candidate.get("volume_ratio"),
            "stop_distance_pct": candidate.get("stop_distance_pct"),
            "stop_distance_atr": candidate.get("stop_distance_atr"),
        },
        "candidate": {
            "sector": candidate.get("sector"),
            "reason_tags": [
                "event_rs_pullback", "daily_impulse", "ema21_reclaim",
                str(profile.get("name") or "profile"),
            ],
        },
        "catalyst": {
            "catalysts": [event.get("title") for event in (news.get("events") or []) if event.get("title")],
            "verification_status": news.get("state"),
        },
    }
    symbol = str(candidate["symbol"]).upper()
    evidence = [
        f"profile={profile.get('name') or candidate['profile_id']}",
        f"impulse={candidate['impulse_return']:.2%}, tr_atr={candidate['impulse_tr_atr']}",
        f"RS20_SPY={candidate['rs20_spy']:.2%}, sector_RS20={candidate['rs20_sector']:.2%}",
        f"pullback_level={candidate['pullback_level']}, regime={candidate['market_regime']}",
        f"news_state={news.get('state')}",
    ]
    return TradeIdea(
        symbol=symbol,
        direction="long",
        score=float(candidate["score"]),
        confidence="high" if candidate["tier"] == "A" else "medium",
        risk_level="medium",
        timeframe=str(cfg.get("timeframe") or "1d"),
        tier=str(candidate["tier"]),
        mode="swing",
        asset_class="stocks",
        exchange_focus="US",
        exchanges_confirmed=["US"],
        data_confidence="high",
        thesis=(
            f"{symbol} has a daily event/RS pullback reclaim after a strong impulse; "
            f"enter only if price trades back into the forward entry zone."
        ),
        evidence=evidence,
        counterarguments=[
            "Broad-market risk-off can invalidate the swing before the thesis has time to work.",
            "News is supportive/blocking context, not mandatory proof of continuation.",
        ],
        entry_plan=f"Forward Paper entry zone {setup['entry_low']:.4g}-{setup['entry_high']:.4g}",
        invalidation=f"{stop:.4g}",
        targets=[f"{setup['tp1']:.4g}", f"{setup['tp2']:.4g}", f"{setup['tp3']:.4g}"],
        what_to_monitor=["SPY trend", "sector RS", "event/news invalidation", "daily close below reclaim level"],
        avoid_conditions=["negative/blocking company news", "risk_off regime", "gap far above no-chase zone"],
        data_sources_used=["local_stock_ohlcv_1d", "canonical_news_available_at"],
        raw=raw,
    )


def refresh(*, db: str | None = None, project_config: Any | None = None,
            now: datetime | None = None, skip_data_update: bool = False,
            cfg: dict[str, Any] | None = None) -> dict[str, Any]:
    del skip_data_update
    cfg = cfg or load_cfg()
    moment = _utc(now)
    if not cfg.get("enabled", True):
        return {"enabled": False, "selected": 0, "registered": 0, "signal_ids": []}
    from src.config import load_config
    from src.signals.config import load_signal_tracking_config
    from src.signals.registry import register_ideas
    from src.stocks.paper_funnel import snapshot_signals
    from src.storage.sqlite import SQLiteStore

    project = project_config or load_config()
    path = Path(db) if db else Path(project.db_path)
    candidates = scan_candidates(project_config=project, cfg=cfg, now=moment, db_path=path)
    try:
        conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True, timeout=30.0)
        candidates = [c for c in candidates if not _already_registered(conn, c, cfg)]
    except Exception:
        pass
    finally:
        try:
            conn.close()  # type: ignore[name-defined]
        except Exception:
            pass
    ideas = [_idea(candidate, cfg, moment) for candidate in candidates]
    store = SQLiteStore(path)
    registration = register_ideas(
        store,
        ideas,
        config=load_signal_tracking_config(project.root),
        report_id=f"{cfg['strategy_id']}_{moment.date().isoformat()}",
        market_regime="stocks_swing_event_rs_pullback",
        asset_class="stocks",
        created_at=moment.isoformat(),
    )
    if registration.signal_ids:
        snapshot_signals(path, registration.signal_ids, now=moment)
    by_profile: dict[str, int] = {}
    for candidate in candidates:
        pid = str(candidate.get("profile_id") or "")
        by_profile[pid] = by_profile.get(pid, 0) + 1
    return {
        "enabled": True,
        "selected": len(ideas),
        "registered": registration.inserted,
        "existing": registration.skipped_existing,
        "signal_ids": list(registration.signal_ids),
        "profile_ids": sorted(_profile_ids(cfg)),
        "paper_lane": cfg["paper_lane"],
        "live_enabled": False,
        "decision_at": moment.isoformat(),
        "by_profile": by_profile,
    }


def resolve_entry(*, signal: dict[str, Any], candles: pd.DataFrame, now: datetime,
                  timeframe_seconds: int, cfg: dict[str, Any] | None = None) -> dict[str, Any]:
    del now
    cfg = cfg or load_cfg()
    if not matches_signal(signal, cfg):
        return {"applied": False}
    if int(timeframe_seconds) != 86400:
        return {"applied": True, "ready": False, "profile_id": _raw(signal).get("paper_entry_profile"),
                "entry_mode": ENTRY_MODE, "reason": "1d_tracking_frame_required"}
    raw = _raw(signal)
    size_weight = _float(raw.get("paper_size_weight"), 1.0)
    return {
        "applied": True,
        "ready": True,
        "profile_id": raw.get("paper_entry_profile"),
        "entry_mode": ENTRY_MODE,
        "reason": "daily_event_rs_pullback_forward_zone",
        "confirmation_at": (raw.get("stock_swing_event_rs_pullback") or {}).get("confirmation_at"),
        "entry_price": _float(signal.get("entry_trigger")) or _float(signal.get("entry_high")),
        "entry_trigger": _float(signal.get("entry_trigger")) or _float(signal.get("entry_high")),
        "max_chase_r": None,
        "paper_size_weight": size_weight,
        "paper_size_reason": str(raw.get("paper_size_reason") or "stocks_swing_event_rs_pullback"),
        "candles": candles,
    }


__all__ = [
    "TRACKER_TIMEFRAME", "ENTRY_MODE", "load_cfg", "configured_symbols",
    "matches_signal", "add_features", "scan_candidates",
    "_candidate_for_confirmation", "refresh", "resolve_entry",
]
