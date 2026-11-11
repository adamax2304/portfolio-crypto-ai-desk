from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

import pandas as pd

from .common import PROJECT_ROOT, digest
from .features import add_indicators
from .simulator import simulate


@dataclass(frozen=True)
class Fold:
    fold_id: str
    start: pd.Timestamp
    end: pd.Timestamp

    def __post_init__(self) -> None:
        object.__setattr__(self, "start", pd.Timestamp(self.start).tz_convert("UTC") if pd.Timestamp(self.start).tzinfo else pd.Timestamp(self.start, tz="UTC"))
        object.__setattr__(self, "end", pd.Timestamp(self.end).tz_convert("UTC") if pd.Timestamp(self.end).tzinfo else pd.Timestamp(self.end, tz="UTC"))


@dataclass(frozen=True)
class Bundle:
    asset: str
    symbol: str
    trend: pd.DataFrame
    context: pd.DataFrame
    entry: pd.DataFrame
    entry_timeframe: str
    source: str
    derivatives: pd.DataFrame
    news: pd.DataFrame


RegimeGate = Callable[[Bundle, pd.Timestamp, str, dict[str, Any]], tuple[bool, str | None, dict[str, Any]]]


def _json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)


def _number(value: Any) -> float | None:
    try:
        out = float(value)
    except (TypeError, ValueError):
        return None
    return out if pd.notna(out) else None


def _prepare(frame: pd.DataFrame, strategy: dict[str, Any], *, timeframe: str) -> pd.DataFrame:
    if frame is None or frame.empty:
        return pd.DataFrame()
    out = frame.copy()
    if "timestamp" not in out.columns and "bar_open_at" in out.columns:
        out["timestamp"] = out["bar_open_at"]
    if "bar_open_at" not in out.columns and "timestamp" in out.columns:
        out["bar_open_at"] = out["timestamp"]
    out["bar_open_at"] = pd.to_datetime(out["bar_open_at"], utc=True, errors="coerce")
    out = out.dropna(subset=["bar_open_at"]).sort_values("bar_open_at").reset_index(drop=True)
    if "bar_close_at" not in out.columns:
        minutes = {"5m": 5, "15m": 15, "1h": 60, "4h": 240}.get(timeframe, 15)
        out["bar_close_at"] = out["bar_open_at"] + pd.Timedelta(minutes=minutes) - pd.Timedelta(milliseconds=1)
    return add_indicators(out, strategy, session_vwap=False)


def _file_symbol(symbol: str) -> str:
    return symbol.replace("/", "_").upper()


def _read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    frame = pd.read_csv(path)
    if "timestamp" in frame.columns:
        frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True, errors="coerce")
    return frame


def _resample_4h(h1: pd.DataFrame) -> pd.DataFrame:
    if h1.empty:
        return pd.DataFrame()
    frame = h1.copy()
    if "timestamp" not in frame.columns:
        frame["timestamp"] = frame["bar_open_at"]
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True, errors="coerce")
    frame = frame.dropna(subset=["timestamp"]).set_index("timestamp").sort_index()
    out = frame.resample("4h").agg({
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last",
        "volume": "sum",
    }).dropna().reset_index()
    return out


def load_bundle(asset: str, symbol: str, strategy: dict[str, Any]) -> Bundle | None:
    base = PROJECT_ROOT / "data" / "history" / "ohlcv" / "binance"
    name = _file_symbol(symbol)
    entry = _prepare(_read_csv(base / "15m" / f"{name}.csv"), strategy, timeframe="15m")
    h1 = _prepare(_read_csv(base / "1h" / f"{name}.csv"), strategy, timeframe="1h")
    context = _prepare(_resample_4h(h1), strategy, timeframe="4h")
    if entry.empty or h1.empty or context.empty:
        return None
    empty = pd.DataFrame()
    return Bundle(asset, symbol.upper(), h1, context, entry, "15m", "binance_history", empty, empty)


def _asof_index(frame: pd.DataFrame, at: pd.Timestamp) -> int | None:
    if frame.empty:
        return None
    times = pd.to_datetime(frame["bar_close_at"], utc=True, errors="coerce")
    index = int(times.searchsorted(at, side="right") - 1)
    return index if index >= 0 else None


def _trend_direction(bundle: Bundle, at: pd.Timestamp) -> list[str]:
    ctx_i = _asof_index(bundle.context, at)
    h1_i = _asof_index(bundle.trend, at)
    if ctx_i is None or h1_i is None:
        return []
    ctx = bundle.context.iloc[ctx_i]
    h1 = bundle.trend.iloc[h1_i]
    required = ("close", "ema_fast", "ema_slow", "ema_slope_atr")
    if any(pd.isna(ctx.get(key)) for key in required) or any(pd.isna(h1.get(key)) for key in required):
        return []
    directions: list[str] = []
    if (
        float(ctx["close"]) > float(ctx["ema_slow"])
        and float(ctx["ema_fast"]) > float(ctx["ema_slow"])
        and float(ctx["ema_slope_atr"]) > 0
        and float(h1["close"]) >= float(h1["ema_fast"])
    ):
        directions.append("long")
    if (
        float(ctx["close"]) < float(ctx["ema_slow"])
        and float(ctx["ema_fast"]) < float(ctx["ema_slow"])
        and float(ctx["ema_slope_atr"]) < 0
        and float(h1["close"]) <= float(h1["ema_fast"])
    ):
        directions.append("short")
    return directions


def _latest_impulse(h1: pd.DataFrame, at: pd.Timestamp, direction: str, variant: dict[str, Any],
                    strategy: dict[str, Any]) -> tuple[int | None, dict[str, Any]]:
    h1_i = _asof_index(h1, at)
    if h1_i is None:
        return None, {"reason": "TREND_TIMEFRAME_UNAVAILABLE"}
    expiry = int(variant.get("retest_expiry_h1_bars", 12))
    start = max(0, h1_i - expiry)
    min_atr = float(variant.get("fvg_min_atr", strategy.get("fvg_min_atr", 0.10)))
    candidates: list[tuple[int, float]] = []
    for idx in range(start, h1_i + 1):
        row = h1.iloc[idx]
        open_, close, high, low, atr = (_number(row.get(key)) for key in ("open", "close", "high", "low", "atr"))
        if None in (open_, close, high, low, atr) or atr <= 0:
            continue
        body = close - open_
        if direction == "long" and body <= 0:
            continue
        if direction == "short" and body >= 0:
            continue
        strength = abs(body) / atr
        range_strength = abs(high - low) / atr
        if max(strength, range_strength * 0.55) >= min_atr:
            candidates.append((idx, strength))
    if not candidates:
        return None, {"reason": "FVG_TOO_SMALL"}
    return candidates[-1][0], {}


def _zone(row: pd.Series, direction: str) -> dict[str, float]:
    open_ = float(row["open"])
    close = float(row["close"])
    low = min(open_, close)
    high = max(open_, close)
    if direction == "long":
        return {"low": low + (high - low) * 0.382, "high": low + (high - low) * 0.618}
    return {"low": low + (high - low) * 0.382, "high": low + (high - low) * 0.618}


def _rsi_reset_ok(h1: pd.DataFrame, impulse_idx: int, h1_idx: int, direction: str,
                  strategy: dict[str, Any]) -> tuple[bool, str | None, dict[str, Any]]:
    profile = (strategy.get("rsi_profiles") or {}).get("baseline") or {}
    window = h1.iloc[max(0, impulse_idx - 2):h1_idx + 1]
    values = pd.to_numeric(window.get("rsi"), errors="coerce").dropna()
    current = _number(h1.iloc[h1_idx].get("rsi"))
    if current is None or values.empty:
        return False, "RSI_RESET_NOT_CONFIRMED", {"rsi_current": current}
    if direction == "long":
        lo = float(profile.get("long_reset_min", 40))
        hi = float(profile.get("long_reset_max", 55))
        current_max = float(profile.get("long_current_max", 68))
        ok = bool(((values >= lo) & (values <= hi)).any() and current <= current_max)
    else:
        lo = float(profile.get("short_reset_min", 45))
        hi = float(profile.get("short_reset_max", 60))
        current_min = float(profile.get("short_current_min", 32))
        ok = bool(((values >= lo) & (values <= hi)).any() and current >= current_min)
    return ok, None if ok else "RSI_RESET_NOT_CONFIRMED", {"rsi_current": current, "rsi_min": float(values.min()), "rsi_max": float(values.max())}


def _entry_confirmation(entry: pd.DataFrame, at: pd.Timestamp, zone: dict[str, float], direction: str,
                        strategy: dict[str, Any]) -> tuple[bool, str | None, dict[str, Any]]:
    current_rows = pd.to_datetime(entry["bar_open_at"], utc=True, errors="coerce")
    idx = int(current_rows.searchsorted(at, side="left"))
    if idx <= 0 or idx >= len(entry):
        return False, "ENTRY_TIMEFRAME_UNAVAILABLE", {}
    prev = entry.iloc[idx - 1]
    current = entry.iloc[idx]
    atr = _number(prev.get("atr"))
    close = _number(prev.get("close"))
    low = _number(prev.get("low"))
    high = _number(prev.get("high"))
    current_open = _number(current.get("open")) or _number(prev.get("close"))
    if None in (atr, close, low, high, current_open) or atr <= 0:
        return False, "ENTRY_TIMEFRAME_UNAVAILABLE", {}
    if direction == "long":
        touched = low <= zone["high"]
        reclaimed = close >= zone["high"]
        extension = max(0.0, current_open - zone["high"]) / atr
    else:
        touched = high >= zone["low"]
        reclaimed = close <= zone["low"]
        extension = max(0.0, zone["low"] - current_open) / atr
    if not touched or not reclaimed:
        return False, "NO_CLOSED_RECLAIM_CONFIRMATION", {
            "last_close": close, "last_low": low, "last_high": high,
        }
    if extension > float(strategy.get("max_entry_extension_atr", 0.35)):
        return False, "ENTRY_CHASE_EXTENSION", {"entry_extension_atr": extension}
    return True, None, {
        "entry_at": pd.Timestamp(current["bar_open_at"]),
        "entry": float(current_open),
        "atr": atr,
        "entry_extension_atr": extension,
        "confirm_bar_close": close,
    }


def _stop(direction: str, entry_price: float, zone: dict[str, float], recent: pd.DataFrame,
          atr: float, strategy: dict[str, Any]) -> tuple[float | None, str | None, dict[str, Any]]:
    buffer = float(strategy.get("stop_buffer_atr", 0.20)) * atr
    min_pct = float(strategy.get("min_stop_pct", 0.005))
    max_pct = float(strategy.get("max_stop_pct_crypto", 0.07))
    max_atr = float(strategy.get("max_stop_atr", 1.50))
    if direction == "long":
        recent_low = float(pd.to_numeric(recent["low"], errors="coerce").min())
        stop = min(zone["low"], recent_low) - buffer
        max_allowed = entry_price * max_pct
        min_allowed = entry_price * min_pct
        risk = entry_price - stop
        if risk < min_allowed:
            stop = entry_price - min_allowed
            risk = min_allowed
    else:
        recent_high = float(pd.to_numeric(recent["high"], errors="coerce").max())
        stop = max(zone["high"], recent_high) + buffer
        max_allowed = entry_price * max_pct
        min_allowed = entry_price * min_pct
        risk = stop - entry_price
        if risk < min_allowed:
            stop = entry_price + min_allowed
            risk = min_allowed
    if risk <= 0 or risk > max_allowed or risk / atr > max_atr:
        return None, "STOP_GEOMETRY_OUT_OF_BOUNDS", {"risk": risk, "max_allowed": max_allowed, "atr": atr}
    return float(stop), None, {"risk": risk, "risk_pct": risk / entry_price}


def _candidate_id(run_id: str, bundle: Bundle, at: pd.Timestamp, direction: str, formed_at: Any) -> str:
    raw = f"{run_id}|{bundle.asset}|{bundle.symbol}|{at.isoformat()}|{direction}|{formed_at}"
    return "ttr_" + hashlib.sha256(raw.encode()).hexdigest()[:22]


def _row(run_id: str, bundle: Bundle, variant: dict[str, Any], fold: Fold, direction: str,
         at: pd.Timestamp, formed_at: Any, status: str, reason: str | None,
         features: dict[str, Any], geometry: dict[str, Any] | None = None,
         entry_at: pd.Timestamp | None = None) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "candidate_id": _candidate_id(run_id, bundle, at, direction, formed_at),
        "variant_id": str(variant.get("variant_id") or "forward"),
        "fold_id": fold.fold_id,
        "asset": bundle.asset,
        "symbol": bundle.symbol,
        "direction": direction,
        "fvg_formed_at": pd.Timestamp(formed_at).isoformat() if formed_at is not None else None,
        "decision_at": at.isoformat(),
        "entry_at": entry_at.isoformat() if entry_at is not None else None,
        "status": status,
        "rejection_reason": reason,
        "is_clean": int(status != "rejected"),
        "source_quality": "POINT_IN_TIME",
        "features_json": _json(features),
        "geometry_json": _json(geometry or {}),
    }


def evaluate_variant(*, run_id: str, bundle: Bundle, variant: dict[str, Any], fold: Fold,
                     cfg: dict[str, Any], regime_gate: RegimeGate | None = None,
                     apply_fold_embargo: bool = True, ignore_symbol_busy: bool = False) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    strategy = cfg.get("strategy") or {}
    entry = _prepare(bundle.entry, strategy, timeframe=bundle.entry_timeframe or "15m")
    h1 = _prepare(bundle.trend, strategy, timeframe="1h")
    context = _prepare(bundle.context, strategy, timeframe="4h")
    if entry.empty or h1.empty or context.empty:
        return [], []
    work = Bundle(bundle.asset, bundle.symbol, h1, context, entry, bundle.entry_timeframe, bundle.source, bundle.derivatives, bundle.news)
    times = pd.to_datetime(entry["bar_open_at"], utc=True, errors="coerce")
    indices = [i for i, at in enumerate(times) if pd.notna(at) and fold.start <= pd.Timestamp(at) <= fold.end]
    candidates: list[dict[str, Any]] = []
    fills: list[dict[str, Any]] = []
    busy_until: pd.Timestamp | None = None
    for entry_idx in indices:
        at = pd.Timestamp(times.iloc[entry_idx])
        if entry_idx < 60:
            continue
        directions = _trend_direction(work, at)
        if not directions:
            continue
        h1_idx = _asof_index(h1, at)
        if h1_idx is None:
            continue
        for direction in directions:
            impulse_idx, meta = _latest_impulse(h1, at, direction, variant, strategy)
            if impulse_idx is None:
                continue
            impulse = h1.iloc[impulse_idx]
            formed_at = impulse.get("bar_close_at")
            zone = _zone(impulse, direction)
            features: dict[str, Any] = {
                "zone": {
                    "low": zone["low"],
                    "high": zone["high"],
                    "atr": _number(impulse.get("atr")),
                    "formed_at": pd.Timestamp(formed_at).isoformat(),
                    "impulse_strength_atr": (
                        abs(float(impulse["close"]) - float(impulse["open"])) / max(float(impulse["atr"]), 1e-12)
                        if _number(impulse.get("atr")) else None
                    ),
                },
                "setup": "regime_conditioned_impulse_reclaim",
                "direction": direction,
            }
            reset_ok, reset_reason, reset_features = _rsi_reset_ok(h1, impulse_idx, h1_idx, direction, strategy)
            features["rsi_reset"] = reset_features
            if not reset_ok:
                candidates.append(_row(run_id, work, variant, fold, direction, at, formed_at, "rejected", reset_reason, features))
                continue
            ok, confirm_reason, confirm = _entry_confirmation(entry, at, zone, direction, strategy)
            features["confirmation"] = confirm
            if not ok:
                candidates.append(_row(run_id, work, variant, fold, direction, at, formed_at, "rejected", confirm_reason, features))
                continue
            if regime_gate is not None:
                allowed, gate_reason, gate_features = regime_gate(work, at, direction, variant)
                features["regime_conditioned"] = gate_features
                if not allowed:
                    candidates.append(_row(run_id, work, variant, fold, direction, at, formed_at, "rejected", gate_reason, features))
                    continue
            recent = entry.iloc[max(0, entry_idx - 8):entry_idx]
            stop, stop_reason, stop_features = _stop(direction, float(confirm["entry"]), zone, recent, float(confirm["atr"]), strategy)
            features["stop"] = stop_features
            if stop is None:
                candidates.append(_row(run_id, work, variant, fold, direction, at, formed_at, "rejected", stop_reason, features))
                continue
            risk = abs(float(confirm["entry"]) - stop)
            target_r = list(variant.get("targets_r") or strategy.get("crypto_targets_r") or [1.3, 2.3, 3.6])
            targets = [
                float(confirm["entry"]) + float(value) * risk
                if direction == "long" else float(confirm["entry"]) - float(value) * risk
                for value in target_r
            ]
            geometry = {
                "entry": float(confirm["entry"]),
                "stop": stop,
                "targets": targets,
                "entry_mode": "REGIME_RECLAIM",
            }
            entry_at = pd.Timestamp(confirm["entry_at"])
            if busy_until is not None and entry_at <= busy_until and not ignore_symbol_busy:
                candidates.append(_row(run_id, work, variant, fold, direction, at, formed_at, "rejected", "SYMBOL_POSITION_ALREADY_OPEN", features))
                continue
            candidate = _row(run_id, work, variant, fold, direction, at, formed_at, "accepted", None, features, geometry, entry_at)
            candidates.append(candidate)
            future = entry[pd.to_datetime(entry["bar_open_at"], utc=True, errors="coerce") >= entry_at].copy()
            sim = simulate(
                direction=direction,
                entry=float(confirm["entry"]),
                stop=stop,
                targets_r=target_r,
                bars=future,
                risk_usd=float((cfg.get("costs") or {}).get("crypto", {}).get("risk_usd", 25.0)),
                taker_fee_rate=float((cfg.get("costs") or {}).get("crypto", {}).get("taker_fee_rate", 0.0006)),
                maker_fee_rate=float((cfg.get("costs") or {}).get("crypto", {}).get("maker_fee_rate", 0.0004)),
                slippage_bps=float((cfg.get("costs") or {}).get("crypto", {}).get("slippage_bps_stress", 15.0)),
                model_f=strategy.get("model_f") or {},
                force_exit_at_end=False,
            ).to_dict()
            fill = {
                "run_id": run_id,
                "trade_id": digest({"candidate": candidate["candidate_id"], "entry_at": entry_at.isoformat()})[:24],
                "candidate_id": candidate["candidate_id"],
                "variant_id": candidate["variant_id"],
                "fold_id": fold.fold_id,
                "asset": bundle.asset,
                "symbol": bundle.symbol,
                "direction": direction,
                "entry_at": entry_at.isoformat(),
                "exit_at": sim.get("exit_at"),
                "entry_price": float(confirm["entry"]),
                "stop_price": stop,
                "exit_price": None,
                "close_reason": sim.get("close_reason"),
                "bars_held": int(sim.get("bars_held") or 0),
                "gross_r": sim.get("net_r"),
                "net_r": sim.get("net_r"),
                "gross_pnl_usd": sim.get("gross_pnl_usd"),
                "net_pnl_usd": sim.get("net_pnl_usd"),
                "fees_usd": float(sim.get("fees_usd") or 0.0),
                "slippage_usd": float(sim.get("slippage_usd") or 0.0),
                "funding_usd": float(sim.get("funding_usd") or 0.0),
                "mfe_r": sim.get("mfe_r"),
                "mae_r": sim.get("mae_r"),
                "highest_tp": int(sim.get("highest_tp") or 0),
                "execution_quality": "point_in_time_reclaim",
                "events_json": "{}",
            }
            fills.append(fill)
            if sim.get("exit_at"):
                busy_until = pd.Timestamp(sim["exit_at"])
    return candidates, fills

