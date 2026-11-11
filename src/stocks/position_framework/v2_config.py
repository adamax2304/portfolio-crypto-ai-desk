"""Configuration for the isolated Stocks Position Swing V2 shadow lane."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None

ROOT = Path(__file__).resolve().parents[3]
CONFIG_PATH = ROOT / "config" / "stocks" / "position_swing_v2.yaml"

DEFAULT: dict[str, Any] = {
    "enabled": True,
    "scheduler_enabled": True,
    "shadow_only": True,
    "write_proposed_signals": False,
    "strategy_id": "stocks_position_swing_v2",
    "shadow_lane": "shadow_stocks_position_swing_v2",
    "profile_version": "stocks_position_swing_v2@2026-07-30",
    "universe": {
        "use_position_framework_universe": True,
        "max_symbols": 75,
        "min_price": 10,
        "min_avg_dollar_volume_30d": 25_000_000,
    },
    "market": {
        "risk_on": {
            "allow_breakout_retest": True,
            "allow_trend_pullback_reclaim": True,
            "size_weight": 1.0,
        },
        "neutral": {
            "allow_breakout_retest": False,
            "allow_trend_pullback_reclaim": True,
            "size_weight": 0.5,
        },
        "risk_off": {
            "allow_breakout_retest": False,
            "allow_trend_pullback_reclaim": False,
            "size_weight": 0.0,
        },
        "warn_vix_above": 22,
        "risk_off_vix_above": 30,
    },
    "stock_filter": {
        "require_above_50d": True,
        "require_above_200d": True,
        "require_weekly_above_30w": True,
        "require_rs_positive_vs_spy": True,
        "require_rs_positive_vs_sector": True,
        "max_pct_below_52w_high": 15,
    },
    "setups": {},
    "event_risk": {},
    "risk": {},
    "exits": {},
    "execution": {},
    "evidence_gate": {},
}


def _merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    result = deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _merge(result[key], value)
        else:
            result[key] = value
    return result


def load_config(path: str | Path | None = None) -> dict[str, Any]:
    cfg_path = Path(path) if path else CONFIG_PATH
    if yaml is None or not cfg_path.exists():
        return deepcopy(DEFAULT)
    try:
        data = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
        user = data.get("stocks_position_swing_v2") or {}
        return _merge(DEFAULT, user) if isinstance(user, dict) else deepcopy(DEFAULT)
    except Exception:
        return deepcopy(DEFAULT)


def safety_invariants(cfg: dict[str, Any] | None = None) -> list[str]:
    current = cfg or load_config()
    issues: list[str] = []
    if not current.get("shadow_only", True):
        issues.append("shadow_only must remain true")
    if current.get("write_proposed_signals", False):
        issues.append("write_proposed_signals must remain false")
    if current.get("strategy_id") != "stocks_position_swing_v2":
        issues.append("unexpected strategy_id")
    if current.get("shadow_lane") != "shadow_stocks_position_swing_v2":
        issues.append("unexpected shadow_lane")
    return issues
