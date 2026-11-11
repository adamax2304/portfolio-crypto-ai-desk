"""Isolated multi-venue live execution package.

The package routes each immutable point-in-time Paper decision to one venue. It never creates
signals and never writes to proposed_signals, signal_outcomes, final_r, or the
Paper portfolio ledger.
"""

from .config import LiveCanaryConfig, load_live_canary_config

__all__ = ["LiveCanaryConfig", "load_live_canary_config"]
