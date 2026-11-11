"""Playbook-aware sizing — reporting / paper-PnL layer only.

This module computes a `sized_r` for each signal alongside the existing
`raw_r` recorded by the tracker. It does NOT influence:
  - signal generation (scoring/setups/agents)
  - tier thresholds or TP/SL geometry
  - Telegram alert eligibility
  - the proposed_signals or signal_outcomes tables

Weights come from `config/sizing_weights.yaml`. Routing per signal:
  1. Resolve the signal's playbook via `src/signals/playbooks.label_for`.
  2. Look up the playbook base weight.
  3. Apply tier override (C/rejected → 0).
  4. Apply fine override (e.g. stocks A-tier long intraday → 0.5).
  5. Compute `sized_r = raw_r * weight`.

Reference audit: reports/PROFITABILITY_LEVERS_AUDIT.md (Lever 1).
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from src.signals.playbooks import label_for


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_CONFIG_PATH = REPO_ROOT / "config" / "sizing_weights.yaml"


@dataclass(frozen=True)
class SizingDecision:
    """Result of routing a signal through the sizing layer."""
    weight: float
    playbook: str
    reason: str
    raw_r: float | None
    sized_r: float | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "weight": self.weight,
            "playbook": self.playbook,
            "reason": self.reason,
            "raw_r": self.raw_r,
            "sized_r": self.sized_r,
        }


def _normalize_tier(tier: Any) -> str:
    if tier is None:
        return ""
    return str(tier).strip().upper()


def _normalize_direction(direction: Any) -> str:
    if direction is None:
        return ""
    return str(direction).strip().lower()


@lru_cache(maxsize=4)
def _load_config(path_str: str) -> dict[str, Any]:
    """Read + cache the YAML. Cache key = the path string."""
    p = Path(path_str)
    if not p.exists():
        # Fall back to a sane default so the helper never raises in
        # production. Returning {} is interpreted as "all 1.0×".
        return {
            "playbooks": {},
            "tier_overrides": {"C": 0.0, "rejected": 0.0},
            "fine_overrides": [],
            "default_weight": 1.0,
        }
    with p.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    # Defensive defaults if any key is missing.
    data.setdefault("playbooks", {})
    data.setdefault("tier_overrides", {"C": 0.0, "rejected": 0.0})
    data.setdefault("fine_overrides", [])
    data.setdefault("default_weight", 1.0)
    return data


def _fine_match(signal_playbook: str, tier: str, direction: str,
                rule: dict[str, Any]) -> bool:
    """A fine_override rule matches when every field it specifies matches."""
    if rule.get("playbook") and rule["playbook"] != signal_playbook:
        return False
    if rule.get("tier") and rule["tier"].upper() != tier:
        return False
    if rule.get("direction") and rule["direction"].lower() != direction:
        return False
    return True


def size_decision(signal: dict[str, Any],
                  *, config_path: Path | None = None) -> SizingDecision:
    """Route a signal through the sizing layer.

    `signal` is a dict carrying at least:
      - asset_class, mode, tier, direction, news_supported, score
      - raw_r OR final_r (the tracker's recorded R)

    Returns a `SizingDecision` with weight, playbook label, reason,
    raw_r echoed back, and sized_r = raw_r * weight (or None when no R).
    """
    cfg_path = str(config_path or DEFAULT_CONFIG_PATH)
    cfg = _load_config(cfg_path)

    # Resolve playbook via the existing labeling utility.
    label = label_for(signal)
    playbook = label.playbook

    # Pick raw_r — accept either explicit `raw_r` or the tracker field `final_r`.
    raw_r = signal.get("raw_r")
    if raw_r is None:
        raw_r = signal.get("final_r")
    try:
        raw_r_val = float(raw_r) if raw_r is not None else None
    except (TypeError, ValueError):
        raw_r_val = None

    tier = _normalize_tier(signal.get("tier"))
    direction = _normalize_direction(signal.get("direction"))

    # Resolution order:
    # 1. Fine override (most specific).
    # 2. Tier override (C / rejected → 0).
    # 3. Playbook base weight.
    # 4. default_weight.
    weight: float | None = None
    reason = ""

    for rule in cfg.get("fine_overrides", []) or []:
        if isinstance(rule, dict) and _fine_match(playbook, tier, direction, rule):
            weight = float(rule.get("weight", 1.0))
            reason = str(rule.get("reason") or
                          f"fine override (playbook={playbook}, tier={tier}, direction={direction})")
            break

    if weight is None:
        tier_map = cfg.get("tier_overrides") or {}
        if tier in {str(k).upper() for k in tier_map.keys()}:
            # Normalize the key lookup (YAML loads keys as their literal form).
            for k, v in tier_map.items():
                if str(k).upper() == tier:
                    weight = float(v)
                    reason = f"tier override: {tier} → {weight}× (watchlist/shadow)"
                    break

    if weight is None:
        playbook_map = cfg.get("playbooks") or {}
        if playbook in playbook_map:
            weight = float(playbook_map[playbook])
            reason = f"playbook base: {playbook} → {weight}×"

    if weight is None:
        weight = float(cfg.get("default_weight", 1.0))
        reason = f"default weight: {weight}× (no rule matched)"

    sized_r = (raw_r_val * weight) if raw_r_val is not None else None
    return SizingDecision(
        weight=weight,
        playbook=playbook,
        reason=reason,
        raw_r=raw_r_val,
        sized_r=sized_r,
    )


def size_signals(signals: list[dict[str, Any]],
                 *, config_path: Path | None = None) -> list[dict[str, Any]]:
    """Convenience: annotate a list of signal dicts in-place with sizing fields.

    Each returned dict carries the original keys plus:
      - sizing_weight
      - sizing_playbook
      - sizing_reason
      - raw_r (echoed)
      - sized_r
    The input list is NOT mutated; new dicts are returned.
    """
    out: list[dict[str, Any]] = []
    for s in signals:
        d = dict(s)
        decision = size_decision(d, config_path=config_path)
        d["sizing_weight"] = decision.weight
        d["sizing_playbook"] = decision.playbook
        d["sizing_reason"] = decision.reason
        d["raw_r"] = decision.raw_r
        d["sized_r"] = decision.sized_r
        out.append(d)
    return out


def portfolio_totals(decisions: list[SizingDecision]) -> dict[str, Any]:
    """Compute aggregate stats for a set of sizing decisions.

    Returns:
      - n: total decisions
      - n_sized: with weight > 0
      - sum_raw_r, sum_sized_r
      - wins / losses / closed (by sized_r sign)
      - WR_closed (sized_r > 0 over closed)
      - PF: sum(positive sized) / |sum(negative sized)|
    """
    n = len(decisions)
    n_sized = sum(1 for d in decisions if d.weight > 0 and d.raw_r is not None)
    sum_raw = sum((d.raw_r or 0) for d in decisions)
    sum_sized = sum((d.sized_r or 0) for d in decisions)
    sized_only = [d for d in decisions if d.weight > 0 and d.sized_r is not None]
    wins = sum(1 for d in sized_only if d.sized_r > 0)
    losses = sum(1 for d in sized_only if d.sized_r < 0)
    pos = sum(d.sized_r for d in sized_only if d.sized_r > 0)
    neg = abs(sum(d.sized_r for d in sized_only if d.sized_r < 0)) or 1e-9
    return {
        "n": n,
        "n_sized": n_sized,
        "sum_raw_r": round(sum_raw, 2),
        "sum_sized_r": round(sum_sized, 2),
        "wins": wins,
        "losses": losses,
        "closed": wins + losses,
        "WR_closed": round((wins / max(wins + losses, 1)) * 100, 0),
        "PF": round((pos / neg), 2) if losses else (float("inf") if wins else 0.0),
    }
