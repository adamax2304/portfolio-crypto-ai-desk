"""Loader for config/signal_tracking.yaml."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from src.config import load_yaml


DEFAULT_VALIDITY_HOURS: dict[str, float] = {
    "scalp": 2,
    "intraday": 24,
    "swing": 168,
    "invest": 720,
}


@dataclass(frozen=True)
class SignalTrackingConfig:
    enabled: bool = True
    track_tiers: tuple[str, ...] = ("A", "B")
    track_watchlist_with_trigger: bool = True
    track_rejected_by_default: bool = False
    default_validity_hours: dict[str, float] = field(default_factory=lambda: dict(DEFAULT_VALIDITY_HOURS))
    check_intervals: dict[str, list[str]] = field(default_factory=dict)
    outcome_default: str = "conservative"
    outcome_ambiguous_same_candle: str = "conservative"
    stop_loss_r: float = -1.0
    tp1_r: float = 1.0
    tp2_r: float = 2.0
    tp3_r: float = 3.0
    partial_exit_enabled: bool = False
    partial_tp1_size: float = 0.4
    partial_tp2_size: float = 0.4
    partial_tp3_size: float = 0.2
    minimum_sample_for_recommendations: int = 30
    minimum_sample_for_rule_change_suggestions: int = 50
    automatic_rule_changes: bool = False
    automatic_scoring_weight_changes: bool = False
    raw: dict[str, Any] = field(default_factory=dict)

    def validity_hours_for(self, mode: str) -> float:
        return float(self.default_validity_hours.get(mode, self.default_validity_hours.get("intraday", 24)))

    def tracks(self, tier: str) -> bool:
        return tier in self.track_tiers


def load_signal_tracking_config(project_root: Path) -> SignalTrackingConfig:
    raw = load_yaml(Path(project_root) / "config" / "signal_tracking.yaml") or {}
    if not raw:
        return SignalTrackingConfig()
    tiers = raw.get("track_tiers") or ["A", "B"]
    default_validity = dict(DEFAULT_VALIDITY_HOURS)
    default_validity.update(raw.get("default_validity_hours") or {})
    outcome = raw.get("outcome_model") or {}
    r_model = raw.get("r_model") or {}
    partial = raw.get("partial_exit_model") or {}
    return SignalTrackingConfig(
        enabled=bool(raw.get("enabled", True)),
        track_tiers=tuple(str(t).upper() for t in tiers),
        track_watchlist_with_trigger=bool(raw.get("track_watchlist_with_trigger", True)),
        track_rejected_by_default=bool(raw.get("track_rejected_by_default", False)),
        default_validity_hours=default_validity,
        check_intervals=raw.get("check_intervals") or {},
        outcome_default=str(outcome.get("default", "conservative")),
        outcome_ambiguous_same_candle=str(outcome.get("ambiguous_same_candle", "conservative")),
        stop_loss_r=float(r_model.get("stop_loss_r", -1.0)),
        tp1_r=float(r_model.get("tp1_r", 1.0)),
        tp2_r=float(r_model.get("tp2_r", 2.0)),
        tp3_r=float(r_model.get("tp3_r", 3.0)),
        partial_exit_enabled=bool(partial.get("enabled", False)),
        partial_tp1_size=float(partial.get("tp1_size", 0.4)),
        partial_tp2_size=float(partial.get("tp2_size", 0.4)),
        partial_tp3_size=float(partial.get("tp3_size", 0.2)),
        minimum_sample_for_recommendations=int(raw.get("minimum_sample_size_for_recommendations", 30)),
        minimum_sample_for_rule_change_suggestions=int(raw.get("minimum_sample_size_for_rule_change_suggestions", 50)),
        automatic_rule_changes=bool(raw.get("automatic_rule_changes", False)),
        automatic_scoring_weight_changes=bool(raw.get("automatic_scoring_weight_changes", False)),
        raw=raw,
    )
