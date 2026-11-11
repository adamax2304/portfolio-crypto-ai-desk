"""Stocks Position Framework — SHADOW-ONLY research lane (Phase 1).

A NEW, separate stocks position/swing framework that replaces the deprecated
`stocks_swing_watchlist_rs_rotation` / `stocks_invest_watchlist_30d_thesis` playbooks (removed
from active analysis/sizing/reports/prompt context due to poor forward performance).

HARD SCOPE:
  * SHADOW / RESEARCH ONLY — never writes proposed_signals, never actionable, never Telegram,
    never live / auto-live / manual-live.
  * Does NOT mix with stocks intraday (a different, still-active pipeline).
  * Authoritative profitability = USD net PnL; legacy final_r is diagnostic only.
  * Phase 1 activates ONLY `stocks_swing_growth_breakout` (long-only). Earnings-drift and
    invest-stage2 are disabled placeholders (see config.disabled_playbooks).
"""
from __future__ import annotations

PLAYBOOK = "stocks_swing_growth_breakout"
ASSET_CLASS = "stocks"
MODE = "swing"                       # reuse the existing swing mode label (NOT a new mode)
SHADOW_STATUS = "shadow_open"
SOURCE_VERSION = "position_framework_v1@2026-07-02"

SETUP_VARIANTS = (
    "breakout",
    "pullback_21d_50d",
    "reclaim_after_shakeout",
    "consolidation_continuation",
)
