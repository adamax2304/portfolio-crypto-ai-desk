"""Authoritative Paper entry-mode provenance.

The signal-creation classifier describes the setup that existed before entry.
Some versioned Paper profiles deliberately replace that setup with a stricter
execution rule after a causal confirmation.  This module is the single mapping
between those profiles and the mode that was actually executed.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


PROFILE_ENTRY_MODES: dict[str, str] = {
    "crypto_intraday_level_hold_1bar_paper_v1": "LEVEL_HOLD_1BAR",
    "crypto_intraday_level_hold_v2_paper_v1": "LEVEL_HOLD_V2",
    "crypto_intraday_breakout_paper_v1": "BREAKOUT_CONTINUATION",
    "crypto_intraday_pullback_paper_v1": "PULLBACK_LIMIT",
    "crypto_swing_breakout_reclaim_paper_v2": "BREAKOUT_RECLAIM_V2",
    "crypto_swing_pullback_confirmed_retest_paper_v1": "PULLBACK_CONFIRMED_RETEST",
    "crypto_swing_fib_impulse_retest_paper_v1": "FIB_IMPULSE_RETEST",
    "stocks_intraday_breakout_1bar_paper_v1": "BREAKOUT_CONTINUATION",
    "stocks_intraday_pullback_vwap_paper_v1": "PULLBACK_LIMIT",
    "stocks_intraday_pullback_vwap_paper_v2": "PULLBACK_LIMIT",
    "stocks_swing_event_rs_pullback_quality_paper_v1": "EVENT_RS_PULLBACK",
    "stocks_swing_event_rs_pullback_flow_paper_v1": "EVENT_RS_PULLBACK",
}


@dataclass(frozen=True)
class EntryModeProvenance:
    entry_mode: str
    source: str
    data_quality: str = "ok"
    profile_id: str | None = None


def execution_mode_for_signal(signal: dict[str, Any]) -> EntryModeProvenance | None:
    """Return a trusted profile execution mode, or ``None``.

    A profile is trusted only when both the versioned profile id and the mode
    attached by the tracker agree.  An unknown profile or mismatch falls back
    to the ordinary lookahead-safe pre-entry classifier; it is never guessed.
    """
    profile = str(signal.get("paper_entry_profile") or "").strip()
    expected = PROFILE_ENTRY_MODES.get(profile)
    if not expected:
        return None
    observed = str(signal.get("paper_execution_entry_mode") or "").strip().upper()
    if observed != expected:
        return None
    return EntryModeProvenance(
        entry_mode=expected,
        source="paper_execution_profile",
        profile_id=profile,
    )


__all__ = ["EntryModeProvenance", "PROFILE_ENTRY_MODES", "execution_mode_for_signal"]
