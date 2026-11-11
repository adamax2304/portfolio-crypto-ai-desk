"""Paper-only confirmed crypto-swing pullback profiles.

The old swing ``PULLBACK_LIMIT`` entered when price traded into the planned
zone.  That gives good prices, but it also selects for bad fills: many limit
orders fill because the pullback is still failing.  These profiles keep the
same source signal, but require causal proof that the zone was defended before
the Paper book can enter.

No live routing lives here.  This module returns a versioned Paper entry plan
for the tracker only.
"""
from __future__ import annotations

import json
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

CONFIRMED_RETEST_MODE = "PULLBACK_CONFIRMED_RETEST"
FIB_IMPULSE_MODE = "FIB_IMPULSE_RETEST"

CONFIRMED_RETEST_PROFILE = "crypto_swing_pullback_confirmed_retest_paper_v1"
FIB_IMPULSE_PROFILE = "crypto_swing_fib_impulse_retest_paper_v1"

DEFAULT_CFG: dict[str, Any] = {
    "enabled": True,
    "live_enabled": False,
    "activated_at": "2026-09-02T00:00:00+00:00",
    "asset_class": "crypto",
    "mode": "swing",
    "source_entry_mode": "PULLBACK_LIMIT",
    "target_multipliers": [1.30, 2.30, 3.60],
    "profiles": {
        "fib_impulse_retest": {
            "enabled": True,
            "profile_id": FIB_IMPULSE_PROFILE,
            "entry_mode": FIB_IMPULSE_MODE,
            "lookback_bars": 8,
            "max_impulse_bars": 4,
            "min_directional_bars": 1,
            "min_impulse_atr": 1.60,
            "min_impulse_pct": 0.018,
            "max_extension_from_impulse_high_atr": 0.75,
            "fib_entry_shallow": 0.50,
            "fib_entry_deep": 0.618,
            "fib_cancel": 0.786,
            "stop_buffer_atr_fraction": 0.10,
            "max_stop_width_multiplier": 1.75,
            "max_retest_bars": 10,
            "min_confirmation_volume_ratio": 0.60,
        },
        "confirmed_retest": {
            "enabled": True,
            "profile_id": CONFIRMED_RETEST_PROFILE,
            "entry_mode": CONFIRMED_RETEST_MODE,
            "max_zone_penetration_fraction": 0.65,
            "reclaim_fraction": 0.50,
            "min_confirmation_volume_ratio": 0.60,
            "stop_buffer_atr_fraction": 0.10,
            "max_stop_width_multiplier": 1.60,
            "max_retest_bars": 8,
        },
    },
}


def load_cfg() -> dict[str, Any]:
    path = ROOT / "config" / "crypto_swing_pullback_paper.yaml"
    if yaml and path.exists():
        try:
            raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            user = raw.get("crypto_swing_pullback_paper") or {}
            cfg = deepcopy(DEFAULT_CFG)
            if isinstance(user, dict):
                for key, value in user.items():
                    if key == "profiles" and isinstance(value, dict):
                        for name, profile in value.items():
                            if isinstance(profile, dict):
                                base = cfg["profiles"].setdefault(name, {})
                                base.update(profile)
                            else:
                                cfg["profiles"][name] = profile
                    else:
                        cfg[key] = value
            return cfg
        except Exception:
            pass
    return deepcopy(DEFAULT_CFG)


def _number(value: Any) -> float | None:
    try:
        return None if value in (None, "") else float(value)
    except (TypeError, ValueError):
        return None


def _matches(signal: dict[str, Any], source_entry_mode: str, cfg: dict[str, Any]) -> bool:
    activated_at = pd.to_datetime(cfg.get("activated_at"), utc=True, errors="coerce")
    created_at = pd.to_datetime(signal.get("created_at"), utc=True, errors="coerce")
    return bool(
        cfg.get("enabled", True)
        and not cfg.get("live_enabled", False)
        and str(signal.get("asset_class") or "crypto").lower()
        == str(cfg.get("asset_class") or "crypto").lower()
        and str(signal.get("mode") or "").lower() == str(cfg.get("mode") or "swing").lower()
        and str(source_entry_mode or "").upper()
        == str(cfg.get("source_entry_mode") or "PULLBACK_LIMIT").upper()
        and not pd.isna(activated_at)
        and not pd.isna(created_at)
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


def _created_at(signal: dict[str, Any]) -> pd.Timestamp | None:
    created = pd.to_datetime(signal.get("created_at"), utc=True, errors="coerce")
    return None if pd.isna(created) else created


def _pre_signal_frame(all_candles: pd.DataFrame | None, signal: dict[str, Any]) -> pd.DataFrame:
    if all_candles is None or all_candles.empty or "timestamp" not in all_candles.columns:
        return pd.DataFrame(columns=getattr(all_candles, "columns", None))
    created = _created_at(signal)
    if created is None:
        return all_candles.iloc[:0].copy()
    stamps = pd.to_datetime(all_candles["timestamp"], utc=True, errors="coerce")
    return all_candles.loc[stamps <= created].reset_index(drop=True)


def _zone(signal: dict[str, Any]) -> tuple[float | None, float | None]:
    low = _number(signal.get("entry_low"))
    high = _number(signal.get("entry_high"))
    if low is None or high is None:
        return None, None
    return min(low, high), max(low, high)


def _direction(signal: dict[str, Any]) -> str:
    return "short" if str(signal.get("direction") or "").lower() == "short" else "long"


def _row_time(row: pd.Series) -> str | None:
    try:
        return pd.to_datetime(row.get("timestamp"), utc=True).isoformat()
    except Exception:
        return None


def _volume_ratio(candles: pd.DataFrame, index: int, lookback: int = 20) -> float | None:
    volume = _number(candles.iloc[index].get("volume"))
    if volume is None:
        return None
    prior = pd.to_numeric(candles.iloc[max(0, index - lookback):index].get("volume"), errors="coerce")
    base = float(prior.median()) if len(prior.dropna()) else None
    if base is None or base <= 0:
        return None
    return volume / base


def _rejection_confirmed(
    *,
    row: pd.Series,
    long: bool,
    zone_low: float,
    zone_high: float,
    reclaim_fraction: float,
) -> bool:
    open_ = _number(row.get("open"))
    high = _number(row.get("high"))
    low = _number(row.get("low"))
    close = _number(row.get("close"))
    if None in (open_, high, low, close) or high <= low:
        return False
    midpoint = zone_low + (zone_high - zone_low) * reclaim_fraction
    candle_range = high - low
    if long:
        lower_wick = min(open_, close) - low
        return bool(close >= midpoint and (close >= open_ or lower_wick >= candle_range * 0.35))
    upper_wick = high - max(open_, close)
    return bool(close <= midpoint and (close <= open_ or upper_wick >= candle_range * 0.35))


def _entry_expiry(*, start_at: Any, timeframe_seconds: int, max_retest_bars: int) -> str | None:
    start = pd.to_datetime(start_at, utc=True, errors="coerce")
    if pd.isna(start) or timeframe_seconds <= 0:
        return None
    expiry = start + pd.Timedelta(seconds=timeframe_seconds * max(1, int(max_retest_bars)))
    return expiry.isoformat()


def _targets(entry: float, stop: float, direction: str, cfg: dict[str, Any]) -> dict[str, float]:
    risk = abs(entry - stop)
    sign = -1.0 if direction == "short" else 1.0
    multipliers = [float(x) for x in (cfg.get("target_multipliers") or [1.3, 2.3, 3.6])]
    return {
        "tp1": round(entry + sign * multipliers[0] * risk, 8),
        "tp2": round(entry + sign * multipliers[1] * risk, 8),
        "tp3": round(entry + sign * multipliers[2] * risk, 8),
        "risk_per_unit": risk,
    }


def _stop_is_usable(
    *,
    signal: dict[str, Any],
    entry: float,
    stop: float,
    direction: str,
    profile: dict[str, Any],
) -> tuple[bool, str, dict[str, Any]]:
    old_stop = _number(signal.get("invalidation")) or _number(signal.get("stop_loss"))
    old_entry = _number(signal.get("suggested_entry")) or (
        _number(signal.get("entry_high")) if direction == "long" else _number(signal.get("entry_low"))
    )
    if old_stop is None or old_entry is None:
        return False, "original_stop_geometry_missing", {}
    new_risk = abs(entry - stop)
    old_risk = abs(old_entry - old_stop)
    if new_risk <= 0 or old_risk <= 0:
        return False, "stop_risk_invalid", {}
    if direction == "long" and not stop < entry:
        return False, "long_stop_not_below_entry", {"entry": entry, "stop": stop}
    if direction == "short" and not stop > entry:
        return False, "short_stop_not_above_entry", {"entry": entry, "stop": stop}
    max_mult = float(profile.get("max_stop_width_multiplier") or 1.6)
    ratio = new_risk / old_risk
    if ratio > max_mult:
        return False, "stop_width_exceeds_profile_limit", {
            "new_to_old_stop_width": round(ratio, 6),
            "max_stop_width_multiplier": max_mult,
        }
    return True, "stop_geometry_ok", {
        "new_to_old_stop_width": round(ratio, 6),
        "max_stop_width_multiplier": max_mult,
    }


def _pending(profile: dict[str, Any], reason: str, facts: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "applied": True,
        "ready": False,
        "profile_id": str(profile.get("profile_id") or ""),
        "entry_mode": str(profile.get("entry_mode") or ""),
        "reason": reason,
        "profile_gate": facts or {},
    }


def _plan_payload(
    *,
    profile: dict[str, Any],
    entry_mode: str,
    reason: str,
    entry_low: float,
    entry_high: float,
    stop: float,
    direction: str,
    candles: pd.DataFrame,
    start_index: int,
    confirmation_at: str,
    timeframe_seconds: int,
    cfg: dict[str, Any],
    facts: dict[str, Any],
) -> dict[str, Any]:
    entry = entry_high if direction == "long" else entry_low
    geometry = {
        "entry_low": entry_low,
        "entry_high": entry_high,
        "entry_trigger": None,
        "suggested_entry": entry,
        "stop_loss": stop,
        "invalidation": stop,
        **_targets(entry, stop, direction, cfg),
    }
    max_bars = max(1, int(profile.get("max_retest_bars") or 8))
    entry_expires_at = _entry_expiry(
        start_at=confirmation_at, timeframe_seconds=timeframe_seconds, max_retest_bars=max_bars,
    )
    profile_gate = {
        **facts,
        "entry_after_confirmation": True,
        "max_retest_bars": max_bars,
        "paper_profile_version": str(profile.get("profile_id") or ""),
    }
    return {
        "applied": True,
        "ready": True,
        "profile_id": str(profile.get("profile_id") or ""),
        "entry_mode": entry_mode,
        "source_entry_mode": "PULLBACK_LIMIT",
        "reason": reason,
        "confirmation_at": confirmation_at,
        "entry_expires_at": entry_expires_at,
        "candles": candles.iloc[start_index:].reset_index(drop=True),
        "profile_gate": profile_gate,
        "signal_updates": geometry,
    }


def _resolve_confirmed_retest(
    *,
    signal: dict[str, Any],
    candles: pd.DataFrame,
    timeframe_seconds: int,
    cfg: dict[str, Any],
    profile: dict[str, Any],
) -> dict[str, Any]:
    zone_low, zone_high = _zone(signal)
    if zone_low is None or zone_high is None or zone_high <= zone_low:
        return _pending(profile, "entry_zone_missing")
    direction = _direction(signal)
    long = direction == "long"
    atr = _atr(candles) or _number(signal.get("risk_per_unit")) or abs(zone_high - zone_low)
    if not atr or atr <= 0:
        return _pending(profile, "atr_missing")
    stop = _number(signal.get("invalidation")) or _number(signal.get("stop_loss"))
    if stop is None:
        return _pending(profile, "stop_missing")

    max_pen = float(profile.get("max_zone_penetration_fraction") or 0.65)
    reclaim = float(profile.get("reclaim_fraction") or 0.50)
    min_vol = float(profile.get("min_confirmation_volume_ratio") or 0.60)
    buffer = float(profile.get("stop_buffer_atr_fraction") or 0.10) * atr

    for index, row in candles.iterrows():
        high = _number(row.get("high"))
        low = _number(row.get("low"))
        if high is None or low is None:
            continue
        touched = low <= zone_high and high >= zone_low
        if not touched:
            if (long and low <= stop) or (not long and high >= stop):
                return _pending(profile, "invalidated_before_confirmed_pullback")
            continue
        boundary = zone_low if long else zone_high
        worst = low if long else high
        penetration = max(0.0, (boundary - worst) if long else (worst - boundary)) / (zone_high - zone_low)
        if penetration > max_pen:
            return _pending(profile, "zone_penetration_excessive", {
                "zone_penetration_fraction": round(penetration, 6),
                "max_zone_penetration_fraction": max_pen,
            })
        if not _rejection_confirmed(
            row=row, long=long, zone_low=zone_low, zone_high=zone_high, reclaim_fraction=reclaim,
        ):
            continue
        vol_ratio = _volume_ratio(candles, int(index))
        if vol_ratio is not None and vol_ratio < min_vol:
            continue
        confirmation_at = _row_time(row)
        if not confirmation_at:
            return _pending(profile, "confirmation_timestamp_missing")
        stop_candidate = min(stop, low - buffer) if long else max(stop, high + buffer)
        entry = zone_high if long else zone_low
        ok, reason, facts = _stop_is_usable(
            signal=signal, entry=entry, stop=stop_candidate, direction=direction, profile=profile,
        )
        if not ok:
            return _pending(profile, reason, facts)
        return _plan_payload(
            profile=profile,
            entry_mode=str(profile.get("entry_mode") or CONFIRMED_RETEST_MODE),
            reason="confirmed_pullback_zone_retest",
            entry_low=zone_low,
            entry_high=zone_high,
            stop=stop_candidate,
            direction=direction,
            candles=candles,
            start_index=int(index) + 1,
            confirmation_at=confirmation_at,
            timeframe_seconds=timeframe_seconds,
            cfg=cfg,
            facts={
                "confirmation_volume_ratio": round(vol_ratio, 6) if vol_ratio is not None else None,
                "zone_penetration_fraction": round(penetration, 6),
                **facts,
            },
        )
    return _pending(profile, "confirmed_retest_pending")


def _impulse_candidate(
    *,
    signal: dict[str, Any],
    all_candles: pd.DataFrame | None,
    cfg: dict[str, Any],
    profile: dict[str, Any],
) -> dict[str, Any] | None:
    pre = _pre_signal_frame(all_candles, signal)
    if pre.empty:
        return None
    lookback = max(2, int(profile.get("lookback_bars") or 8))
    max_bars = max(1, int(profile.get("max_impulse_bars") or 4))
    pre = pre.tail(max(lookback, max_bars + 14)).reset_index(drop=True)
    atr = _atr(pre) or _number(signal.get("risk_per_unit"))
    if atr is None or atr <= 0:
        return None
    direction = _direction(signal)
    long = direction == "long"
    min_impulse_atr = float(profile.get("min_impulse_atr") or 1.6)
    min_impulse_pct = float(profile.get("min_impulse_pct") or 0.018)
    min_directional = int(profile.get("min_directional_bars") or 1)

    best: dict[str, Any] | None = None
    for bars in range(1, max_bars + 1):
        if len(pre) < bars:
            continue
        window = pre.tail(bars)
        first = window.iloc[0]
        last = window.iloc[-1]
        open_ = _number(first.get("open"))
        close = _number(last.get("close"))
        if open_ is None or close is None or open_ <= 0:
            continue
        net = (close - open_) if long else (open_ - close)
        directional = 0
        for _, row in window.iterrows():
            ro = _number(row.get("open"))
            rc = _number(row.get("close"))
            if ro is not None and rc is not None and ((rc >= ro) if long else (rc <= ro)):
                directional += 1
        if directional < min_directional:
            continue
        high = float(pd.to_numeric(window.get("high"), errors="coerce").max())
        low = float(pd.to_numeric(window.get("low"), errors="coerce").min())
        span = high - low
        if span <= 0:
            continue
        impulse_atr = net / atr
        impulse_pct = net / open_
        if impulse_atr < min_impulse_atr or impulse_pct < min_impulse_pct:
            continue
        candidate = {
            "bars": bars,
            "atr": atr,
            "impulse_atr": impulse_atr,
            "impulse_pct": impulse_pct,
            "impulse_high": high,
            "impulse_low": low,
            "impulse_started_at": _row_time(first),
            "impulse_ended_at": _row_time(last),
        }
        if best is None or candidate["impulse_atr"] > best["impulse_atr"]:
            best = candidate
    return best


def _resolve_fib_impulse(
    *,
    signal: dict[str, Any],
    candles: pd.DataFrame,
    all_candles: pd.DataFrame | None,
    timeframe_seconds: int,
    cfg: dict[str, Any],
    profile: dict[str, Any],
) -> dict[str, Any]:
    impulse = _impulse_candidate(signal=signal, all_candles=all_candles, cfg=cfg, profile=profile)
    if not impulse:
        return {"applied": False}
    direction = _direction(signal)
    long = direction == "long"
    high = float(impulse["impulse_high"])
    low = float(impulse["impulse_low"])
    span = high - low
    shallow = float(profile.get("fib_entry_shallow") or 0.50)
    deep = float(profile.get("fib_entry_deep") or 0.618)
    cancel = float(profile.get("fib_cancel") or 0.786)
    if long:
        zone_high = high - shallow * span
        zone_low = high - deep * span
        cancel_level = high - cancel * span
    else:
        zone_low = low + shallow * span
        zone_high = low + deep * span
        cancel_level = low + cancel * span
    zone_low, zone_high = min(zone_low, zone_high), max(zone_low, zone_high)
    atr = float(impulse["atr"])
    buffer = float(profile.get("stop_buffer_atr_fraction") or 0.10) * atr
    stop = cancel_level - buffer if long else cancel_level + buffer
    max_ext = float(profile.get("max_extension_from_impulse_high_atr") or 0.75)
    min_vol = float(profile.get("min_confirmation_volume_ratio") or 0.60)

    for index, row in candles.iterrows():
        high_bar = _number(row.get("high"))
        low_bar = _number(row.get("low"))
        close = _number(row.get("close"))
        if high_bar is None or low_bar is None or close is None:
            continue
        if (long and low_bar <= stop) or (not long and high_bar >= stop):
            return _pending(profile, "fib_cancel_level_breached_before_confirmation", {
                **{k: round(v, 6) if isinstance(v, float) else v for k, v in impulse.items()},
                "fib_cancel_level": round(cancel_level, 8),
            })
        # If price extends too far after the impulse before pulling back, this
        # is no longer the same impulse-retest setup.
        if (long and high_bar > high + atr * max_ext) or (not long and low_bar < low - atr * max_ext):
            return {"applied": False}
        touched = low_bar <= zone_high and high_bar >= zone_low
        if not touched:
            continue
        if not _rejection_confirmed(
            row=row, long=long, zone_low=zone_low, zone_high=zone_high, reclaim_fraction=0.50,
        ):
            continue
        vol_ratio = _volume_ratio(candles, int(index))
        if vol_ratio is not None and vol_ratio < min_vol:
            continue
        entry = zone_high if long else zone_low
        ok, reason, facts = _stop_is_usable(
            signal=signal, entry=entry, stop=stop, direction=direction, profile=profile,
        )
        if not ok:
            return _pending(profile, reason, facts)
        confirmation_at = _row_time(row)
        if not confirmation_at:
            return _pending(profile, "fib_confirmation_timestamp_missing")
        return _plan_payload(
            profile=profile,
            entry_mode=str(profile.get("entry_mode") or FIB_IMPULSE_MODE),
            reason="fib_impulse_zone_confirmed_retest",
            entry_low=zone_low,
            entry_high=zone_high,
            stop=stop,
            direction=direction,
            candles=candles,
            start_index=int(index) + 1,
            confirmation_at=confirmation_at,
            timeframe_seconds=timeframe_seconds,
            cfg=cfg,
            facts={
                **{k: round(v, 6) if isinstance(v, float) else v for k, v in impulse.items()},
                "fib_entry_shallow": shallow,
                "fib_entry_deep": deep,
                "fib_cancel": cancel,
                "fib_cancel_level": round(cancel_level, 8),
                "confirmation_volume_ratio": round(vol_ratio, 6) if vol_ratio is not None else None,
                **facts,
            },
        )
    return _pending(profile, "fib_impulse_retest_pending", {
        **{k: round(v, 6) if isinstance(v, float) else v for k, v in impulse.items()},
    })


def resolve_entry(
    *,
    signal: dict[str, Any],
    source_entry_mode: str,
    candles: pd.DataFrame,
    all_candles: pd.DataFrame | None,
    now: datetime,
    timeframe_seconds: int,
    cfg: dict[str, Any] | None = None,
) -> dict[str, Any]:
    cfg = cfg or load_cfg()
    if not _matches(signal, source_entry_mode, cfg):
        return {"applied": False}
    closed = _closed_prefix(candles, now=now, timeframe_seconds=timeframe_seconds)
    profiles = cfg.get("profiles") if isinstance(cfg.get("profiles"), dict) else {}
    fib = profiles.get("fib_impulse_retest") if isinstance(profiles.get("fib_impulse_retest"), dict) else {}
    if fib.get("enabled", True):
        out = _resolve_fib_impulse(
            signal=signal,
            candles=closed,
            all_candles=all_candles,
            timeframe_seconds=timeframe_seconds,
            cfg=cfg,
            profile=fib,
        )
        if out.get("applied"):
            return out
    confirmed = profiles.get("confirmed_retest") if isinstance(profiles.get("confirmed_retest"), dict) else {}
    if confirmed.get("enabled", True):
        return _resolve_confirmed_retest(
            signal=signal,
            candles=closed,
            timeframe_seconds=timeframe_seconds,
            cfg=cfg,
            profile=confirmed,
        )
    return {"applied": False}


def signal_overrides(original: dict[str, Any], adjusted: dict[str, Any]) -> dict[str, Any]:
    keys = (
        "entry_low", "entry_high", "entry_trigger", "suggested_entry",
        "stop_loss", "invalidation", "tp1", "tp2", "tp3", "risk_per_unit",
        "raw_idea_json",
    )
    return {key: adjusted[key] for key in keys if adjusted.get(key) != original.get(key)}


def apply_signal_updates(signal: dict[str, Any], plan: dict[str, Any]) -> dict[str, Any]:
    updates = plan.get("signal_updates") if isinstance(plan.get("signal_updates"), dict) else {}
    if not updates:
        return dict(signal)
    out = dict(signal)
    out.update(updates)
    raw: dict[str, Any]
    try:
        raw = json.loads(out.get("raw_idea_json") or "{}")
        if not isinstance(raw, dict):
            raw = {}
    except Exception:
        raw = {}
    raw["paper_entry_profile"] = plan.get("profile_id")
    raw["paper_execution_entry_mode"] = plan.get("entry_mode")
    raw["crypto_swing_pullback_profile"] = {
        "version": plan.get("profile_id"),
        "entry_mode": plan.get("entry_mode"),
        "source_entry_mode": plan.get("source_entry_mode"),
        "reason": plan.get("reason"),
        "confirmation_at": plan.get("confirmation_at"),
        "entry_expires_at": plan.get("entry_expires_at"),
        "profile_gate": plan.get("profile_gate") or {},
        "fixed_usd_risk_requires_smaller_position": True,
    }
    out["raw_idea_json"] = json.dumps(raw, sort_keys=True)
    return out


__all__ = [
    "CONFIRMED_RETEST_MODE",
    "FIB_IMPULSE_MODE",
    "CONFIRMED_RETEST_PROFILE",
    "FIB_IMPULSE_PROFILE",
    "apply_signal_updates",
    "load_cfg",
    "resolve_entry",
    "signal_overrides",
]
