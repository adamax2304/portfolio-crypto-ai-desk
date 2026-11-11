"""Passive signal tracking & performance analytics.

This module is intentionally observation-only. It records proposed signals,
reconciles their outcomes against later OHLCV, and exposes statistics. It
never auto-edits scoring weights, stops, or strategies.
"""

from src.signals.config import SignalTrackingConfig, load_signal_tracking_config
from src.signals.models import ProposedSignal, SignalOutcome, signal_id_for

__all__ = [
    "SignalTrackingConfig",
    "load_signal_tracking_config",
    "ProposedSignal",
    "SignalOutcome",
    "signal_id_for",
]
