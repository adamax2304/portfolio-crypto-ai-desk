"""Position / leverage advisor — label-only (operational deploy PART 7).

Asserts notional math, the wide/tight-stop behavior, the unsafe-liquidation case,
the unknown path, and that the function is pure (no routing/size/execution effect).
"""
from __future__ import annotations

from src.risk.position_advisor import position_leverage_advice, advisor_line


def test_normal_case_computes_notional():
    a = position_leverage_advice(entry=100.0, stop=98.0, equity=10_000)
    # 2% stop, 0.5% risk → risk 50 / 0.02 = 2500 notional
    assert a["position_advisor_status"] == "ok"
    assert a["stop_distance_pct"] == 2.0
    assert a["suggested_notional"] == 2500.0
    assert a["max_safe_leverage_estimate"] >= 1
    assert a["diagnostic_only"] is True


def test_wide_stop_reduces_notional():
    tight = position_leverage_advice(entry=100.0, stop=98.0, equity=10_000)["suggested_notional"]
    wide = position_leverage_advice(entry=100.0, stop=90.0, equity=10_000)["suggested_notional"]
    assert wide < tight  # 10% stop → smaller notional than 2% stop


def test_tight_stop_increases_notional_but_warns_on_leverage():
    a = position_leverage_advice(entry=100.0, stop=99.96, equity=10_000)  # 0.04% stop
    assert a["suggested_notional"] > 50_000  # very large notional
    assert a["position_advisor_status"] == "warning"
    assert a["leverage_warning"] and "max safe" in a["leverage_warning"]


def test_missing_stop_is_unknown():
    a = position_leverage_advice(entry=100.0, stop=None)
    assert a["position_advisor_status"] == "unknown"
    assert a["suggested_notional"] is None


def test_unsafe_liquidation_buffer_when_stop_too_wide():
    a = position_leverage_advice(entry=100.0, stop=20.0, equity=10_000)  # 80% stop
    assert a["position_advisor_status"] == "unsafe"
    assert "UNSAFE" in (a["leverage_warning"] or "")


def test_invalid_entry_stop_unknown():
    assert position_leverage_advice(entry=0, stop=0)["position_advisor_status"] == "unknown"
    assert position_leverage_advice(entry=100, stop=100)["position_advisor_status"] == "unknown"


def test_advisor_line_renders_and_unknown_is_none():
    ok = position_leverage_advice(entry=100.0, stop=98.0)
    assert advisor_line(ok) and "Position advisor" in advisor_line(ok)
    assert advisor_line(position_leverage_advice(entry=None, stop=None)) is None


def test_pure_no_side_effects():
    sig_like = {"entry": 100.0, "stop": 98.0}
    before = dict(sig_like)
    position_leverage_advice(entry=sig_like["entry"], stop=sig_like["stop"])
    assert sig_like == before  # inputs untouched; no order/size mutation
