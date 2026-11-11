"""Paper-only reclaim gate for crypto swing breakouts.

The production ``BREAKOUT_CONTINUATION`` idea may be directionally right, but
the raw touch model is too optimistic for swing execution.  This resolver keeps
that source idea in Paper only after a causal closed-bar reclaim/hold and then
tests a bounded retest of the reclaimed level.
"""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None


ROOT = Path(__file__).resolve().parents[2]

ENTRY_MODE = "BREAKOUT_RECLAIM_V2"
PROFILE_ID = "crypto_swing_breakout_reclaim_paper_v2"

DEFAULT_CFG: dict[str, Any] = {
    "enabled": True,
    "live_enabled": False,
    "activated_at": "2026-09-16T00:00:00+00:00",
    "asset_class": "crypto",
    "mode": "swing",
    "source_entry_mode": "BREAKOUT_CONTINUATION",
    "profile_id": PROFILE_ID,
    "entry_mode": ENTRY_MODE,
    "min_reclaim_close_distance_atr": 0.04,
    "level_hold_buffer_atr": 0.12,
    "min_confirmation_volume_ratio": 0.70,
    "first_touch_rejection_wick_share": 0.40,
    "retest_zone_atr": 0.18,
    "min_retest_zone_bps": 8.0,
    "max_retest_bars": 8,
    "block_confirmed_btc_countertrend": True,
    "btc_conflict_return_pct": 0.35,
}


def load_cfg() -> dict[str, Any]:
    path = ROOT / "config" / "crypto_swing_breakout_reclaim_paper.yaml"
    if yaml and path.exists():
        try:
            raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            user = raw.get("crypto_swing_breakout_reclaim_paper") or {}
            cfg = deepcopy(DEFAULT_CFG)
            if isinstance(user, dict):
                cfg.update(user)
            return cfg
        except Exception:
            pass
    return deepcopy(DEFAULT_CFG)


def _number(value: Any) -> float | None:
    try:
        return None if value in (None, "") else float(value)
    except (TypeError, ValueError):
        return None


def _direction(signal: dict[str, Any]) -> str:
    return "short" if str(signal.get("direction") or "").lower() == "short" else "long"


def _created_at(signal: dict[str, Any]) -> pd.Timestamp | None:
    created = pd.to_datetime(signal.get("created_at"), utc=True, errors="coerce")
    return None if pd.isna(created) else created


def _matches(signal: dict[str, Any], source_entry_mode: str, cfg: dict[str, Any]) -> bool:
    activated_at = pd.to_datetime(cfg.get("activated_at"), utc=True, errors="coerce")
    created_at = _created_at(signal)
    return bool(
        cfg.get("enabled", True)
        and not cfg.get("live_enabled", False)
        and str(signal.get("asset_class") or "crypto").lower()
        == str(cfg.get("asset_class") or "crypto").lower()
        and str(signal.get("mode") or "").lower() == str(cfg.get("mode") or "swing").lower()
        and str(source_entry_mode or "").upper()
        == str(cfg.get("source_entry_mode") or "BREAKOUT_CONTINUATION").upper()
        and not pd.isna(activated_at)
        and created_at is not None
        and created_at >= activated_at
    )


def _closed_prefix(candles: pd.DataFrame, *, now: datetime, timeframe_seconds: int) -> pd.DataFrame:
    if candles is None or candles.empty or timeframe_seconds <= 0 or "timestamp" not in candles.columns:
        return pd.DataFrame(columns=getattr(candles, "columns", None))
    stamps = pd.to_datetime(candles["timestamp"], utc=True, errors="coerce")
    cutoff = pd.Timestamp(now.astimezone(timezone.utc)) - pd.Timedelta(seconds=timeframe_seconds)
    return candles.loc[stamps <= cutoff].reset_index(drop=True)


def _atr(candles: pd.DataFrame, n: int = 14) -> float | None:
    if candles is None or len(candles) < 2:
        return None
    trs: list[float] = []
    prev_close = _number(candles.iloc[0].get("close"))
    for _, row in candles.iloc[1:].iterrows():
        high = _number(row.get("high"))
        low = _number(row.get("low"))
        if high is None or low is None or prev_close is None:
            prev_close = _number(row.get("close"))
            continue
        trs.append(max(high - low, abs(high - prev_close), abs(low - prev_close)))
        prev_close = _number(row.get("close"))
    tail = trs[-n:]
    return sum(tail) / len(tail) if tail else None


def _volume_ratio(candles: pd.DataFrame, index: int, lookback: int = 20) -> float | None:
    volume = _number(candles.iloc[index].get("volume"))
    if volume is None:
        return None
    prior = pd.to_numeric(candles.iloc[max(0, index - lookback):index].get("volume"), errors="coerce")
    base = float(prior.median()) if len(prior.dropna()) else None
    if base is None or base <= 0:
        return None
    return volume / base


def _row_time(row: pd.Series) -> str | None:
    try:
        return pd.to_datetime(row.get("timestamp"), utc=True).isoformat()
    except Exception:
        return None


def _level(signal: dict[str, Any], direction: str) -> float | None:
    trigger = _number(signal.get("entry_trigger"))
    if trigger is not None:
        return trigger
    low = _number(signal.get("entry_low"))
    high = _number(signal.get("entry_high"))
    if low is not None and high is not None:
        return max(low, high) if direction == "long" else min(low, high)
    return _number(signal.get("suggested_entry"))


def _first_touch_rejected(
    row: pd.Series,
    *,
    direction: str,
    level: float,
    buffer: float,
    wick_share: float,
) -> bool:
    open_ = _number(row.get("open"))
    high = _number(row.get("high"))
    low = _number(row.get("low"))
    close = _number(row.get("close"))
    if None in (open_, high, low, close) or high <= low:
        return False
    candle_range = high - low
    if direction == "long":
        upper_wick = high - max(open_, close)
        return bool(high >= level and close < level - buffer and upper_wick >= candle_range * wick_share)
    lower_wick = min(open_, close) - low
    return bool(low <= level and close > level + buffer and lower_wick >= candle_range * wick_share)


def _btc_countertrend_block(signal: dict[str, Any], cfg: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
    if not cfg.get("block_confirmed_btc_countertrend", True):
        return False, {}
    try:
        from src.execution.crypto_quality_overlay import load_cfg as load_overlay_cfg
        from src.execution.crypto_quality_overlay import market_context

        ctx = market_context(load_overlay_cfg()) or {}
    except Exception:
        return False, {"btc_market_context": "unavailable"}
    direction = _direction(signal)
    threshold = abs(float(cfg.get("btc_conflict_return_pct") or 0.35))
    ret_candidates = [
        _number(ctx.get("btc_return_1h_pct")),
        _number(ctx.get("btc_return_15m_pct")),
        _number(ctx.get("btc_pct_1h")),
        _number(ctx.get("btc_1h_return_pct")),
    ]
    btc_ret = next((value for value in ret_candidates if value is not None), None)
    state = str(ctx.get("state") or ctx.get("regime") or ctx.get("market_regime") or "").lower()
    block = (
        (direction == "long" and (
            (btc_ret is not None and btc_ret <= -threshold)
            or state in {"risk_off", "bearish", "downtrend"}
        ))
        or (direction == "short" and (
            (btc_ret is not None and btc_ret >= threshold)
            or state in {"risk_on", "bullish", "uptrend"}
        ))
    )
    return block, {"btc_return_pct": btc_ret, "btc_state": state or None}


def _pending(cfg: dict[str, Any], reason: str, facts: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "applied": True,
        "ready": False,
        "profile_id": str(cfg.get("profile_id") or PROFILE_ID),
        "entry_mode": str(cfg.get("entry_mode") or ENTRY_MODE),
        "reason": reason,
        "source_entry_mode": str(cfg.get("source_entry_mode") or "BREAKOUT_CONTINUATION"),
        "profile_gate": facts or {},
        "candles": pd.DataFrame(),
    }


def _entry_expiry(*, start_at: Any, timeframe_seconds: int, max_retest_bars: int) -> str | None:
    start = pd.to_datetime(start_at, utc=True, errors="coerce")
    if pd.isna(start) or timeframe_seconds <= 0:
        return None
    expiry = start + pd.Timedelta(seconds=timeframe_seconds * max(1, int(max_retest_bars)))
    return expiry.isoformat()


def resolve_entry(
    *,
    signal: dict[str, Any],
    source_entry_mode: str,
    candles: pd.DataFrame,
    now: datetime,
    timeframe_seconds: int,
    cfg: dict[str, Any] | None = None,
) -> dict[str, Any]:
    cfg = deepcopy(cfg or load_cfg())
    if not _matches(signal, source_entry_mode, cfg):
        return {"applied": False}

    direction = _direction(signal)
    level = _level(signal, direction)
    if level is None or level <= 0:
        return _pending(cfg, "breakout_reclaim_missing_level")

    closed = _closed_prefix(candles, now=now, timeframe_seconds=timeframe_seconds)
    if closed.empty:
        return _pending(cfg, "breakout_reclaim_waiting_for_closed_bar", {"level": level})
    if "timestamp" in closed.columns:
        created = _created_at(signal)
        if created is not None:
            stamps = pd.to_datetime(closed["timestamp"], utc=True, errors="coerce")
            closed = closed.loc[stamps >= created].reset_index(drop=True)
    if closed.empty:
        return _pending(cfg, "breakout_reclaim_waiting_for_post_signal_bar", {"level": level})

    atr = _atr(closed)
    if atr is None or atr <= 0:
        atr = level * 0.01
    hold_buffer = atr * float(cfg.get("level_hold_buffer_atr") or 0.12)
    close_distance = atr * float(cfg.get("min_reclaim_close_distance_atr") or 0.04)
    min_volume_ratio = float(cfg.get("min_confirmation_volume_ratio") or 0.0)
    first_touch_checked = False

    for index, row in closed.iterrows():
        high = _number(row.get("high"))
        low = _number(row.get("low"))
        close = _number(row.get("close"))
        if high is None or low is None or close is None:
            continue
        touches_level = (high >= level >= low)
        if touches_level and not first_touch_checked:
            first_touch_checked = True
            if _first_touch_rejected(
                row,
                direction=direction,
                level=level,
                buffer=hold_buffer,
                wick_share=float(cfg.get("first_touch_rejection_wick_share") or 0.40),
            ):
                return _pending(cfg, "breakout_reclaim_first_touch_rejected", {
                    "level": level,
                    "bar_at": _row_time(row),
                    "atr": round(atr, 8),
                })
        if direction == "long":
            confirmed = close >= level + close_distance and low >= level - hold_buffer
        else:
            confirmed = close <= level - close_distance and high <= level + hold_buffer
        if not confirmed:
            continue
        volume_ratio = _volume_ratio(closed, int(index))
        if volume_ratio is not None and volume_ratio < min_volume_ratio:
            continue
        btc_block, btc_facts = _btc_countertrend_block(signal, cfg)
        facts = {
            "level": level,
            "atr": round(atr, 8),
            "hold_buffer": round(hold_buffer, 8),
            "min_close_distance": round(close_distance, 8),
            "confirmation_volume_ratio": round(volume_ratio, 6) if volume_ratio is not None else None,
            "entry_after_confirmation": True,
            **btc_facts,
        }
        if btc_block:
            return _pending(cfg, "breakout_reclaim_btc_countertrend_block", facts)

        zone_width = max(
            atr * float(cfg.get("retest_zone_atr") or 0.18),
            level * (float(cfg.get("min_retest_zone_bps") or 8.0) / 10_000.0),
        )
        confirmation_at = _row_time(row)
        entry_expires_at = _entry_expiry(
            start_at=confirmation_at,
            timeframe_seconds=timeframe_seconds,
            max_retest_bars=int(cfg.get("max_retest_bars") or 8),
        )
        return {
            "applied": True,
            "ready": True,
            "profile_id": str(cfg.get("profile_id") or PROFILE_ID),
            "entry_mode": str(cfg.get("entry_mode") or ENTRY_MODE),
            "reason": "crypto_swing_breakout_reclaim_v2",
            "source_entry_mode": str(cfg.get("source_entry_mode") or "BREAKOUT_CONTINUATION"),
            "confirmation_at": confirmation_at,
            "entry_expires_at": entry_expires_at,
            "entry_low": round(level - zone_width, 8),
            "entry_high": round(level + zone_width, 8),
            "entry_trigger": None,
            "candles": closed.iloc[int(index) + 1:].reset_index(drop=True),
            "profile_gate": facts,
        }

    return _pending(cfg, "breakout_reclaim_confirmation_pending", {
        "level": level,
        "atr": round(atr, 8),
        "closed_bars_seen": int(len(closed)),
    })


__all__ = ["ENTRY_MODE", "PROFILE_ID", "load_cfg", "resolve_entry"]
