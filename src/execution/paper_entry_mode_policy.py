"""Paper entry-mode promotion policy.

This module is deliberately small and conservative: it only answers whether a
classified entry mode is disabled for the shadow promotion lane, or promoted
into the authoritative paper tracker. It never places orders and never changes
live routing.
"""
from __future__ import annotations

from functools import lru_cache
from typing import Any

from src.config import load_config, load_yaml


def _norm(value: Any, default: str = "") -> str:
    return str(value if value is not None else default).strip().lower()


def _mode(value: Any) -> str:
    return str(value or "").strip().upper()


@lru_cache(maxsize=1)
def load_policy() -> dict[str, Any]:
    cfg = load_config()
    return load_yaml(cfg.root / "config" / "paper_entry_mode_policy.yaml")


def _matches(rule: dict[str, Any], *, asset_class: str, trade_mode: str, entry_mode: str) -> bool:
    want_asset = _norm(rule.get("asset_class"), "*")
    want_trade_mode = _norm(rule.get("mode"), "*")
    modes = {_mode(m) for m in (rule.get("entry_modes") or [])}
    return (
        (want_asset == "*" or want_asset == _norm(asset_class, "crypto"))
        and (want_trade_mode == "*" or want_trade_mode == _norm(trade_mode))
        and ("*" in modes or _mode(entry_mode) in modes)
    )


def disabled_shadow_reason(*, asset_class: str, trade_mode: str, entry_mode: str) -> str | None:
    policy = load_policy()
    if not bool(policy.get("enabled", True)):
        return None
    for rule in policy.get("disabled_shadow") or []:
        if isinstance(rule, dict) and _matches(
            rule, asset_class=asset_class, trade_mode=trade_mode, entry_mode=entry_mode
        ):
            return str(rule.get("reason") or "entry_mode_disabled_by_policy")
    return None


def paper_promotion_reason(*, asset_class: str, trade_mode: str, entry_mode: str) -> str | None:
    policy = load_policy()
    if not bool(policy.get("enabled", True)):
        return None
    prod = policy.get("paper_production") or {}
    if not bool(prod.get("enabled", False)):
        return None
    for rule in prod.get("promoted") or []:
        if isinstance(rule, dict) and _matches(
            rule, asset_class=asset_class, trade_mode=trade_mode, entry_mode=entry_mode
        ):
            return str(rule.get("reason") or "entry_mode_promoted_to_paper")
    return None
