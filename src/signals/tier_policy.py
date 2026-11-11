"""Tier routing policy (FAST SAFE ACCELERATION 2026-06-17).

Centralizes the stocks-intraday C-tier restriction as an explicit, configurable,
labeled policy. This is ROUTING / ACTIONABILITY only — it NEVER changes a signal's
tier, score, TP/SL, or size. A restricted signal is still registered and tracked;
it is simply never pushed as an actionable alert (shadow/review-only).

Background: the live stocks monitor already filters alerts to tier A/B, and the
Control Plane already classifies C-tier as non-actionable — so this does not change
behavior; it makes the rule a single source of truth + emits visibility labels.
A 30d diagnostic motivated it (stocks-intraday C-tier = −34R drag vs B +132R).
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

DEFAULT_POLICY = "shadow_review_only"
C_TIER_RESTRICTION_REASON = "stocks_intraday_c_tier_30d_negative"

_CACHE: dict[str, str] = {}


def load_stocks_intraday_c_tier_policy(project_root: Path | None = None) -> str:
    """Read `tier_policy.stocks_intraday_c_tier` from config/signal_tracking.yaml.
    Defaults to 'shadow_review_only'. Fails safe to the default (restricted)."""
    key = str(project_root or "_default")
    if key in _CACHE:
        return _CACHE[key]
    policy = DEFAULT_POLICY
    try:
        from src.config import load_config, load_yaml
        root = project_root
        if root is None:
            root = load_config().root
        raw = load_yaml(Path(root) / "config" / "signal_tracking.yaml") or {}
        val = (raw.get("tier_policy") or {}).get("stocks_intraday_c_tier")
        if isinstance(val, str) and val.strip():
            policy = val.strip().lower()
    except Exception:
        # Any failure → stay restricted (the safe default).
        policy = DEFAULT_POLICY
    _CACHE[key] = policy
    return policy


def is_stocks_intraday_c_tier(signal: dict[str, Any]) -> bool:
    return (
        str(signal.get("asset_class") or "").lower() == "stocks"
        and str(signal.get("mode") or "").lower() == "intraday"
        and str(signal.get("tier") or "").upper() == "C"
    )


def is_restricted(signal: dict[str, Any], policy: str | None = None) -> bool:
    """True iff this signal is a stocks-intraday C-tier under a restricting policy.
    Crypto (any tier) and A/B stocks are never restricted by this rule."""
    pol = (policy or DEFAULT_POLICY)
    return is_stocks_intraday_c_tier(signal) and pol != "actionable"


def c_tier_restriction_fields(
    signal: dict[str, Any], policy: str | None = None
) -> dict[str, Any]:
    """Add-only visibility fields for the payload / report / Control Plane.
    Always returns the keys; `c_tier_restriction_applied` is False for anything
    that is not a restricted stocks-intraday C-tier signal."""
    pol = policy or DEFAULT_POLICY
    applied = is_restricted(signal, pol)
    return {
        "c_tier_restriction_applied": applied,
        "c_tier_restriction_reason": C_TIER_RESTRICTION_REASON if applied else "",
        "diagnostic_or_policy": "risk_restriction" if applied else "none",
        "c_tier_policy": pol,
    }


def tier_from_score(score: float, *, a: float = 80.0, b: float = 65.0, c: float = 50.0) -> str:
    """Canonical score -> tier mapping, shared by StockScoringAgent._tier() and any
    downstream overlay that needs to recompute a tier from an adjusted score
    (e.g. the pre-US review overlay's `review_adjusted_score`). Pure threshold
    comparison only — callers apply hard blocks ('rejected') separately."""
    if score >= a:
        return "A"
    if score >= b:
        return "B"
    if score >= c:
        return "C"
    return "rejected"
