from __future__ import annotations

import json
from copy import deepcopy
from typing import Any

from src.execution.stop_contract import entry_anchor, normalize_stop_contract


ENTRY_MODE = "BREAKOUT_CONTINUATION"
PROFILE_VERSION = "crypto_breakout_wider_stop_125_v1"
DEFAULT_WIDEN_FACTOR = 1.25


def _f(value: Any, default: float | None = None) -> float | None:
    try:
        return default if value in (None, "") else float(value)
    except (TypeError, ValueError):
        return default


def _loads(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return deepcopy(value)
    try:
        parsed = json.loads(value or "{}")
        return parsed if isinstance(parsed, dict) else {}
    except Exception:
        return {}


def _dump(raw: dict[str, Any]) -> str:
    return json.dumps(raw, ensure_ascii=False, default=str)


def _is_directional(direction: str, entry: float, stop: float,
                    targets: tuple[float, float, float]) -> bool:
    if direction == "long":
        return stop < entry < targets[0] < targets[1] < targets[2]
    if direction == "short":
        return targets[2] < targets[1] < targets[0] < entry < stop
    return False


def _target_multipliers(direction: str, entry: float, stop: float,
                        targets: tuple[float, float, float]) -> tuple[float, float, float] | None:
    risk = abs(entry - stop)
    if risk <= 0:
        return None
    if direction == "long":
        values = tuple((target - entry) / risk for target in targets)
    else:
        values = tuple((entry - target) / risk for target in targets)
    if any(value <= 0 for value in values):
        return None
    return values  # type: ignore[return-value]


def _reprice(direction: str, entry: float, risk: float,
             multipliers: tuple[float, float, float]) -> tuple[float, float, float]:
    if direction == "long":
        return tuple(round(entry + risk * value, 10) for value in multipliers)  # type: ignore[return-value]
    return tuple(round(entry - risk * value, 10) for value in multipliers)  # type: ignore[return-value]


def _with_wider_contract(
    *,
    signal: dict[str, Any],
    raw: dict[str, Any],
    entry: float,
    old_stop: float,
    new_stop: float,
    factor: float,
) -> dict[str, Any]:
    direction = str(signal.get("direction") or "").lower()
    asset_class = str(signal.get("asset_class") or "crypto").lower()
    mode = str(signal.get("mode") or "").lower()
    symbol = str(signal.get("symbol") or "")
    base = raw.get("initial_stop_contract") or raw.get("stop_contract") or {}
    contract = dict(base) if isinstance(base, dict) else {}
    contract.update(
        {
            "version": PROFILE_VERSION,
            "symbol": symbol,
            "asset_class": asset_class,
            "mode": mode,
            "direction": direction,
            "entry_price": entry,
            "stop_price": new_stop,
            "pre_widen_stop_price": old_stop,
            "widen_factor": factor,
            "stop_variant": "wider_125",
            "stop_model": "wider_125_breakout_v1",
            "label": "1.25x breakout stop",
            "fallback_used": bool(contract.get("fallback_used", False)),
        }
    )
    warnings = contract.get("warnings")
    if not isinstance(warnings, list):
        warnings = []
    if "breakout stop widened 1.25x; fixed USD risk must resize position down" not in warnings:
        warnings.append("breakout stop widened 1.25x; fixed USD risk must resize position down")
    contract["warnings"] = warnings
    return normalize_stop_contract(
        contract,
        symbol=symbol,
        asset_class=asset_class,
        mode=mode,
        direction=direction,
        entry_price=entry,
        stop_price=new_stop,
        source=str(contract.get("stop_source") or "wider_125_breakout"),
    )


def apply_wider_125_if_crypto_breakout(
    signal: dict[str, Any],
    *,
    entry_mode: str | None,
    widen_factor: float = DEFAULT_WIDEN_FACTOR,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return a signal copy with a wider breakout stop and repriced R ladder.

    This is execution geometry only. It preserves the original entry anchor and
    target R multipliers, then moves the stop to 1.25x current risk. Fixed-USD
    sizing remains owned by the paper/live sizing layer.
    """
    if str(signal.get("asset_class") or "crypto").lower() != "crypto":
        return dict(signal), {"applied": False, "reason": "asset_class_not_crypto"}
    if str(entry_mode or "").upper() != ENTRY_MODE:
        return dict(signal), {"applied": False, "reason": "entry_mode_not_breakout"}
    direction = str(signal.get("direction") or "").lower()
    if direction not in {"long", "short"}:
        return dict(signal), {"applied": False, "reason": "invalid_direction"}

    entry = entry_anchor(
        direction,
        signal.get("entry_low"),
        signal.get("entry_high"),
        signal.get("entry_trigger") or signal.get("suggested_entry"),
    )
    old_stop = _f(signal.get("invalidation") or signal.get("stop_loss"))
    targets_raw = (_f(signal.get("tp1")), _f(signal.get("tp2")), _f(signal.get("tp3")))
    if entry is None or old_stop is None or any(value is None for value in targets_raw):
        return dict(signal), {"applied": False, "reason": "missing_geometry"}
    targets = (float(targets_raw[0]), float(targets_raw[1]), float(targets_raw[2]))  # type: ignore[arg-type]
    if not _is_directional(direction, entry, old_stop, targets):
        return dict(signal), {"applied": False, "reason": "invalid_original_geometry"}

    multipliers = _target_multipliers(direction, entry, old_stop, targets)
    if multipliers is None:
        return dict(signal), {"applied": False, "reason": "invalid_r_ladder"}
    factor = max(1.0, float(widen_factor or DEFAULT_WIDEN_FACTOR))
    old_risk = abs(entry - old_stop)
    new_risk = old_risk * factor
    new_stop = round(entry - new_risk if direction == "long" else entry + new_risk, 10)
    new_targets = _reprice(direction, entry, new_risk, multipliers)
    if not _is_directional(direction, entry, new_stop, new_targets):
        return dict(signal), {"applied": False, "reason": "invalid_widened_geometry"}

    out = dict(signal)
    out["stop_loss"] = new_stop
    out["invalidation"] = new_stop
    out["tp1"], out["tp2"], out["tp3"] = new_targets
    out["risk_per_unit"] = new_risk
    out["expected_rr_tp1"] = multipliers[0]
    out["expected_rr_tp2"] = multipliers[1]
    out["expected_rr_tp3"] = multipliers[2]

    raw = _loads(signal.get("raw_idea_json"))
    setup = raw.get("raw_setup") or raw.get("setup")
    if isinstance(setup, dict):
        setup["invalidation"] = new_stop
        setup["tp1"], setup["tp2"], setup["tp3"] = new_targets
        setup["crypto_breakout_stop_profile_version"] = PROFILE_VERSION
        setup["crypto_breakout_stop_widen_factor"] = factor
    contract = _with_wider_contract(
        signal=out,
        raw=raw,
        entry=entry,
        old_stop=old_stop,
        new_stop=new_stop,
        factor=factor,
    )
    raw["initial_stop_contract"] = contract
    raw["stop_contract"] = contract
    raw["stop_label"] = contract.get("label")
    raw["crypto_breakout_stop_profile"] = {
        "version": PROFILE_VERSION,
        "entry_mode": ENTRY_MODE,
        "widen_factor": factor,
        "entry_anchor": entry,
        "old_stop": old_stop,
        "new_stop": new_stop,
        "old_risk": old_risk,
        "new_risk": new_risk,
        "target_r_multipliers": list(multipliers),
        "old_targets": list(targets),
        "new_targets": list(new_targets),
        "fixed_usd_risk_requires_smaller_position": True,
    }
    out["raw_idea_json"] = _dump(raw)
    return out, {
        "applied": True,
        "profile_version": PROFILE_VERSION,
        "widen_factor": factor,
        "entry": entry,
        "old_stop": old_stop,
        "new_stop": new_stop,
        "old_risk": old_risk,
        "new_risk": new_risk,
        "target_r_multipliers": multipliers,
        "new_targets": new_targets,
    }


def signal_overrides(original: dict[str, Any], adjusted: dict[str, Any]) -> dict[str, Any]:
    keys = (
        "stop_loss", "invalidation", "tp1", "tp2", "tp3", "risk_per_unit",
        "expected_rr_tp1", "expected_rr_tp2", "expected_rr_tp3", "raw_idea_json",
    )
    return {key: adjusted.get(key) for key in keys if adjusted.get(key) != original.get(key)}


__all__ = [
    "ENTRY_MODE",
    "PROFILE_VERSION",
    "DEFAULT_WIDEN_FACTOR",
    "apply_wider_125_if_crypto_breakout",
    "signal_overrides",
]
