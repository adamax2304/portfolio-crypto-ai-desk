"""Entry policy for confirmed crypto-intraday pullbacks.

V2 requires a controlled zone touch, a quality reclaim of the mid-zone and a
short, post-confirmation retest window.  It creates no signal and does not
alter score/geometry; live-routing eligibility remains owned by the canary
policy.
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

DEFAULT_CFG: dict[str, Any] = {
    "enabled": True,
    "live_enabled": False,
    "profile_id": "crypto_intraday_level_hold_v2_paper_v1",
    "activated_at": "2026-08-24T00:00:00+00:00",
    "asset_class": "crypto",
    "mode": "intraday",
    "source_entry_mode": "PULLBACK_LIMIT",
    "confirmation_kind": "level_hold_v2",
    "v2": {
        "max_zone_penetration_fraction": 0.25,
        "min_confirmation_volume_ratio": 0.75,
        "max_retest_bars": 3,
        "market": {
            "enabled": True,
            "max_countertrend_btc_15m_return_pct": 0.25,
            "max_countertrend_btc_1h_return_pct": 0.50,
        },
    },
}


def load_cfg() -> dict[str, Any]:
    path = ROOT / "config" / "crypto_intraday_level_hold_paper.yaml"
    if yaml and path.exists():
        try:
            raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            user = raw.get("crypto_intraday_level_hold_paper") or {}
            cfg = deepcopy(DEFAULT_CFG)
            if isinstance(user, dict):
                cfg.update(user)
            return cfg
        except Exception:
            pass
    return deepcopy(DEFAULT_CFG)


def _matches(signal: dict[str, Any], source_entry_mode: str, cfg: dict[str, Any]) -> bool:
    activated_at = pd.to_datetime(cfg.get("activated_at"), utc=True, errors="coerce")
    created_at = pd.to_datetime(signal.get("created_at"), utc=True, errors="coerce")
    return bool(
        cfg.get("enabled", True)
        and str(signal.get("asset_class") or "crypto").lower() == str(cfg.get("asset_class") or "crypto").lower()
        and str(signal.get("mode") or "").lower() == str(cfg.get("mode") or "intraday").lower()
        and str(source_entry_mode or "").upper() == str(cfg.get("source_entry_mode") or "PULLBACK_LIMIT").upper()
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


def _entry_mode(cfg: dict[str, Any]) -> str:
    return "LEVEL_HOLD_V2" if str(cfg.get("confirmation_kind") or "").lower() == "level_hold_v2" else "LEVEL_HOLD_1BAR"


def _pending(profile_id: str, entry_mode: str, reason: str, *, profile_gate: dict[str, Any] | None = None) -> dict[str, Any]:
    out: dict[str, Any] = {
        "applied": True, "ready": False, "profile_id": profile_id,
        "entry_mode": entry_mode, "reason": reason,
    }
    if profile_gate:
        out["profile_gate"] = profile_gate
    return out


def _number(value: Any) -> float | None:
    try:
        return None if value in (None, "") else float(value)
    except (TypeError, ValueError):
        return None


def _v2_structural_gate(
    *,
    signal: dict[str, Any],
    candles: pd.DataFrame,
    gate: dict[str, Any],
    cfg: dict[str, Any],
    now: datetime,
) -> tuple[bool, str, dict[str, Any]]:
    """Check only the V2 quality facts visible at confirmation.

    This intentionally does not add a second portfolio/risk guard.  The
    quality overlay remains responsible for Paper sizing and exposure.  Here
    we reject only a weak reclaim, excessive excursion through the zone, a
    stop touched before entry, or a confirmed BTC move directly against it.
    """
    v2 = cfg.get("v2") if isinstance(cfg.get("v2"), dict) else {}
    long = str(signal.get("direction") or "long").lower() != "short"
    low, high = _number(signal.get("entry_low")), _number(signal.get("entry_high"))
    stop = _number(signal.get("invalidation")) or _number(signal.get("stop_loss"))
    confirm_idx = int(gate.get("confirmation_index") or -1)
    touch_idx = confirm_idx - 1
    if low is None or high is None or high <= low or touch_idx < 0 or confirm_idx >= len(candles):
        return False, "v2_geometry_unavailable", {}

    touch = candles.iloc[touch_idx]
    confirmation = candles.iloc[confirm_idx]
    touch_low, touch_high = _number(touch.get("low")), _number(touch.get("high"))
    confirmation_low, confirmation_high = _number(confirmation.get("low")), _number(confirmation.get("high"))
    if None in (touch_low, touch_high, confirmation_low, confirmation_high):
        return False, "v2_candle_range_missing", {}

    relevant = candles.iloc[: confirm_idx + 1]
    if stop is not None:
        lowest = pd.to_numeric(relevant.get("low"), errors="coerce").min()
        highest = pd.to_numeric(relevant.get("high"), errors="coerce").max()
        if (long and pd.notna(lowest) and float(lowest) <= stop) or (
            not long and pd.notna(highest) and float(highest) >= stop
        ):
            return False, "v2_pre_confirmation_invalidation", {}

    boundary = low if long else high
    worst = min(touch_low, confirmation_low) if long else max(touch_high, confirmation_high)
    penetration = max(0.0, (boundary - worst) if long else (worst - boundary)) / (high - low)
    max_penetration = float(v2.get("max_zone_penetration_fraction") or 0.25)
    if penetration > max_penetration:
        return False, "v2_zone_penetration_excessive", {
            "zone_penetration_fraction": round(penetration, 6),
            "max_zone_penetration_fraction": max_penetration,
        }

    touch_volume = _number(touch.get("volume"))
    confirmation_volume = _number(confirmation.get("volume"))
    if touch_volume is None or confirmation_volume is None or touch_volume <= 0:
        return False, "v2_confirmation_volume_missing", {}
    volume_ratio = confirmation_volume / touch_volume
    min_volume_ratio = float(v2.get("min_confirmation_volume_ratio") or 0.75)
    if volume_ratio < min_volume_ratio:
        return False, "v2_confirmation_volume_too_low", {
            "confirmation_volume_ratio": round(volume_ratio, 6),
            "min_confirmation_volume_ratio": min_volume_ratio,
        }

    market_gate = v2.get("market") if isinstance(v2.get("market"), dict) else {}
    market_facts: dict[str, Any] = {}
    if bool(market_gate.get("enabled", True)):
        try:
            from src.execution.crypto_quality_overlay import load_cfg as load_overlay_cfg, market_context

            context = market_context(now, load_overlay_cfg())
            btc_15m = _number(context.get("btc_15m_return"))
            btc_1h = _number(context.get("btc_1h_return"))
            market_facts = {
                "btc_context_status": str(context.get("status") or "unknown"),
                "btc_15m_return_pct": btc_15m,
                "btc_1h_return_pct": btc_1h,
            }
            max_15m = float(market_gate.get("max_countertrend_btc_15m_return_pct") or 0.25)
            max_1h = float(market_gate.get("max_countertrend_btc_1h_return_pct") or 0.50)
            if (long and ((btc_15m is not None and btc_15m < -max_15m) or
                          (btc_1h is not None and btc_1h < -max_1h))) or (
                not long and ((btc_15m is not None and btc_15m > max_15m) or
                              (btc_1h is not None and btc_1h > max_1h))
            ):
                return False, "v2_btc_countertrend", market_facts
        except Exception:
            # A missing context is visible in the snapshot but is not a veto.
            # The existing overlay applies its normal unknown-data policy.
            market_facts = {"btc_context_status": "unavailable"}

    return True, "v2_quality_confirmed", {
        "zone_penetration_fraction": round(penetration, 6),
        "max_zone_penetration_fraction": max_penetration,
        "confirmation_volume_ratio": round(volume_ratio, 6),
        "min_confirmation_volume_ratio": min_volume_ratio,
        **market_facts,
    }


def _entry_expiry(*, confirmation_at: Any, timeframe_seconds: int, cfg: dict[str, Any], signal: dict[str, Any]) -> str | None:
    confirmed = pd.to_datetime(confirmation_at, utc=True, errors="coerce")
    if pd.isna(confirmed) or timeframe_seconds <= 0:
        return None
    v2 = cfg.get("v2") if isinstance(cfg.get("v2"), dict) else {}
    bars = max(1, int(v2.get("max_retest_bars") or 3))
    expiry = confirmed + pd.Timedelta(seconds=timeframe_seconds * bars)
    signal_expiry = pd.to_datetime(signal.get("expires_at"), utc=True, errors="coerce")
    if not pd.isna(signal_expiry):
        expiry = min(expiry, signal_expiry)
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
    """Return the Paper entry plan without mutating a signal or database.

    ``ready=False`` is intentional: the tracker keeps the original signal
    pending until the observed close and later retest both exist.
    """
    cfg = cfg or load_cfg()
    if not _matches(signal, source_entry_mode, cfg):
        return {"applied": False}
    entry_mode = _entry_mode(cfg)
    closed = _closed_prefix(candles, now=now, timeframe_seconds=timeframe_seconds)
    if closed.empty:
        return _pending(cfg["profile_id"], entry_mode, "no_closed_confirmation_bar")
    try:
        from src.execution.crypto_intraday_idea_sweep import pullback_confirmation_gate

        gate = pullback_confirmation_gate(
            {
                "direction": signal.get("direction"),
                "entry_low": _float(signal.get("entry_low")),
                "entry_high": _float(signal.get("entry_high")),
                "entry_trigger": _float(signal.get("entry_trigger")),
                "entry": _float(signal.get("suggested_entry")),
            },
            closed,
            str(cfg.get("confirmation_kind") or "level_hold_1bar"),
            entry_expires_at=signal.get("expires_at"),
        )
    except Exception:
        return _pending(cfg["profile_id"], entry_mode, "confirmation_gate_error")
    if not gate.get("eligible"):
        return _pending(cfg["profile_id"], entry_mode, gate.get("reason") or "confirmation_pending")
    profile_gate: dict[str, Any] = {}
    if entry_mode == "LEVEL_HOLD_V2":
        allowed, reason, profile_gate = _v2_structural_gate(
            signal=signal, candles=closed, gate=gate, cfg=cfg, now=now,
        )
        if not allowed:
            return _pending(cfg["profile_id"], entry_mode, reason, profile_gate=profile_gate)
    start = int(gate.get("start_index") or 0)
    out = {
        "applied": True, "ready": True, "profile_id": cfg["profile_id"],
        "entry_mode": entry_mode, "reason": "confirmed_level_hold_retest",
        "confirmation_at": gate.get("confirmation_at"),
        "candles": candles.iloc[start:].reset_index(drop=True),
    }
    if entry_mode == "LEVEL_HOLD_V2":
        out["profile_gate"] = profile_gate
        out["entry_expires_at"] = _entry_expiry(
            confirmation_at=gate.get("confirmation_at"), timeframe_seconds=timeframe_seconds,
            cfg=cfg, signal=signal,
        )
    return out


def _float(value: Any) -> float | None:
    try:
        return None if value in (None, "") else float(value)
    except (TypeError, ValueError):
        return None


__all__ = ["load_cfg", "resolve_entry"]
