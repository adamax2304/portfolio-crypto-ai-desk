"""Tests for the structural TP validator (display-only)."""
from __future__ import annotations

from src.execution.tp_structure_validator import validate_tps


def test_mechanical_atr_ladder_flagged():
    # entry 100, stop 99, ATR 1 → TPs at +1/+2/+3 ATR, no structural levels.
    v = validate_tps(entry=100, stop=99, tp1=101, tp2=102, tp3=103, direction="long",
                     atr=1.0, swing_levels=[], market_regime="chop", playbook="x")
    assert v.tp_quality_label in ("MECHANICAL_R_ONLY", "MIXED")  # ATR-extension recognized but no structure
    assert v.volume_profile_supported == "unknown"
    assert v.tp1_source.startswith("atr_extension") or v.tp1_source == "mechanical_r_ladder"


def test_structural_tps_accepted():
    # TPs placed right on swing levels.
    v = validate_tps(entry=100, stop=99, tp1=101, tp2=102, tp3=103, direction="long",
                     atr=1.0, swing_levels=[101.0, 102.0, 103.0],
                     market_regime="bullish trend", playbook="crypto_swing_narrative_rs_momentum")
    assert v.tp_quality_label == "STRUCTURAL"
    assert v.tp_near_chart_level is True
    assert v.tp_is_mechanical_r_ladder is False


def test_tp3_needs_stronger_evidence_in_chop():
    # Far mechanical TP3, chop regime, non-runner playbook → TP3 warning.
    v = validate_tps(entry=100, stop=99, tp1=101, tp2=102, tp3=103, direction="long",
                     atr=1.0, swing_levels=[], market_regime="chop",
                     playbook="stocks_intraday_rth_momentum")
    assert v.tp3_warning is not None
    assert v.tp3_allowed_reason is None


def test_tp3_runner_playbook_allowed():
    v = validate_tps(entry=100, stop=99, tp1=101, tp2=102, tp3=103, direction="long",
                     atr=1.0, swing_levels=[], market_regime="bullish trend",
                     playbook="crypto_failed_bounce_short")
    assert v.tp3_allowed_reason is not None
