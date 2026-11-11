from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "config" / "live_routes.yaml"


def load_registry(path: str | Path | None = None) -> dict[str, Any]:
    selected = Path(path) if path is not None else CONFIG_PATH
    payload = yaml.safe_load(selected.read_text(encoding="utf-8")) or {}
    block = payload.get("live_routes") or {}
    routes = block.get("routes") or {}
    if not isinstance(routes, dict):
        raise ValueError("LIVE_ROUTE_REGISTRY_INVALID")
    return {"version": str(block.get("version") or ""), "routes": routes}


def route_key(*, mode: str, entry_mode: str, asset_class: str = "crypto") -> str | None:
    normalized_mode = str(mode or "").lower()
    normalized_entry = str(entry_mode or "").upper()
    if str(asset_class or "crypto").lower().startswith("stock"):
        return "stocks_intraday_breakout" if normalized_entry == "BREAKOUT_CONTINUATION" else None
    mapping = {
        ("swing", "BREAKOUT_CONTINUATION"): "crypto_swing_breakout",
        ("swing", "LIMIT_THEN_TAKER_TIMEOUT"): "crypto_swing_limit_then_taker",
        ("swing", "PULLBACK_LIMIT"): "crypto_swing_pullback",
        ("intraday", "LEVEL_HOLD_V2"): "crypto_intraday_level_hold_v2",
        ("intraday", "BREAKOUT_CONTINUATION"): "crypto_intraday_breakout",
        ("intraday", "PULLBACK_LIMIT"): "crypto_intraday_pullback",
        ("liquidity_sweep", "LIQUIDITY_SWEEP"): "crypto_liquidity_sweep",
        ("invest", "REGIME_RECLAIM"): "crypto_invest",
    }
    return mapping.get((normalized_mode, normalized_entry))


def route(*, mode: str, entry_mode: str, asset_class: str = "crypto",
          path: str | Path | None = None) -> dict[str, Any] | None:
    key = route_key(mode=mode, entry_mode=entry_mode, asset_class=asset_class)
    if key is None:
        return None
    item = (load_registry(path).get("routes") or {}).get(key)
    if not isinstance(item, dict):
        return None
    return {"route_key": key, **item}


def route_enabled(*, mode: str, entry_mode: str, asset_class: str = "crypto",
                  path: str | Path | None = None) -> bool:
    item = route(mode=mode, entry_mode=entry_mode, asset_class=asset_class, path=path)
    return bool(item and item.get("enabled") is True)


__all__ = ["CONFIG_PATH", "load_registry", "route", "route_enabled", "route_key"]
