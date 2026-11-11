"""Tests for the realistic-execution accounting models (read-only research).

Locks the model formulas the PnL audit relies on. No production logic involved.
"""
from __future__ import annotations

from scripts.realistic_pnl_sim import compute_models, model_f_mfe

R1, R2, R3 = 1.0, 2.0, 3.0


def test_tp1_then_stop():
    # TP1 touched, then stop (no TP3). The whole point of the audit.
    m = compute_models(c1=True, c2=False, c3=False, st=True, exp=False, R1=R1, R2=R2, R3=R3)
    assert m["m0_legacy_touch"] == 1.0      # current: counts as +TP1 WIN (optimistic)
    assert m["m1_first_tp_close"] == 1.0    # exited at TP1 before reversal
    assert m["m2_hold_tp3"] == -1.0         # held for TP3 -> gave back to stop = LOSS
    assert m["m3_tp1_be"] == 0.0            # BE after TP1 -> breakeven
    assert m["m4_tp1_lock02"] == 0.2        # +0.2R locked
    assert m["m5_partial_be"] == 0.5        # 50% at TP1 (+0.5R), runner BE'd to 0
    assert m["dC_lock05"] == 0.5


def test_tp2_then_stop():
    m = compute_models(c1=True, c2=True, c3=False, st=True, exp=False, R1=R1, R2=R2, R3=R3)
    assert m["m0_legacy_touch"] == 2.0      # current: +TP2 WIN
    assert m["m2_hold_tp3"] == -1.0         # held for TP3 -> stop = LOSS
    assert m["dD_tp1_after_tp2"] == 1.0     # stop moved to TP1 after TP2 -> +1R locked
    assert m["m6_partial_tp1_tp2"] == (1.0 + 2.0 + 0.0) / 3.0  # 1/3 TP1 + 1/3 TP2 + runner BE


def test_tp3_hit_all_capture():
    m = compute_models(c1=True, c2=True, c3=True, st=False, exp=False, R1=R1, R2=R2, R3=R3)
    assert m["m0_legacy_touch"] == 3.0
    assert m["m2_hold_tp3"] == 3.0
    assert m["m3_tp1_be"] == 3.0
    assert m["m5_partial_be"] == 0.5 * 1.0 + 0.5 * 3.0   # partial + full-R runner
    assert m["m6_partial_tp1_tp2"] == (1.0 + 2.0 + 3.0) / 3.0


def test_stop_first_all_minus1():
    m = compute_models(c1=False, c2=False, c3=False, st=True, exp=False, R1=R1, R2=R2, R3=R3)
    assert all(m[k] == -1.0 for k in ("m0_legacy_touch", "m1_first_tp_close", "m2_hold_tp3", "m3_tp1_be", "m5_partial_be"))


def test_expired_no_tp_zero():
    m = compute_models(c1=False, c2=False, c3=False, st=False, exp=True, R1=R1, R2=R2, R3=R3)
    assert all(m[k] == 0.0 for k in m)


def test_partial_be_beats_hold_on_giveback():
    # On a TP1-then-stop give-back, partial/BE must be >= hold-to-TP3 (the saved give-back)
    give = compute_models(True, False, False, True, False, R1, R2, R3)
    assert give["m5_partial_be"] > give["m2_hold_tp3"]
    assert give["m3_tp1_be"] > give["m2_hold_tp3"]


def test_model_f_mfe_protection():
    m0_win = 1.0
    # Stopped but reached +0.7R favorable first -> MFE-armed BE rescues to 0R (not -1R)
    assert model_f_mfe(c3=False, st=True, exp=False, mfe=0.7, m0=m0_win) == 0.0
    # Stopped but reached +1.3R favorable -> +0.5R locked
    assert model_f_mfe(c3=False, st=True, exp=False, mfe=1.3, m0=m0_win) == 0.5
    # Stopped, never got +0.6R favorable -> full -1R (signal genuinely failed)
    assert model_f_mfe(c3=False, st=True, exp=False, mfe=0.3, m0=m0_win) == -1.0
    # Reached TP3 -> keep best-TP result (protection never triggered against it)
    assert model_f_mfe(c3=True, st=False, exp=False, mfe=3.1, m0=3.0) == 3.0
    # Clean TP win (not stopped) with high MFE -> keeps its booked R
    assert model_f_mfe(c3=False, st=False, exp=False, mfe=1.2, m0=2.0) == 2.0
