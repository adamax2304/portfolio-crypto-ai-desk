"""Session Risk Guard (Asia dead-zone 00–06 UTC) — unit + guardrail tests.

Covers the shared decision (guard_decision), the production tier overlay
(apply_to_scores), and the invariant that the module never touches live execution.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from src.analysis import session_guard as sg

UTC = timezone.utc


def _cfg(**over) -> sg.SessionGuardConfig:
    base = dict(
        enabled=True, dz_enabled=True, utc_start_hour=0, utc_end_hour=6,
        asset_classes=("crypto",), blocked_modes=("scalp", "intraday"),
        demote_to_tier="C", allowed_mode_risk_multiplier=1.0,
        monday=sg.MondayStricter(enabled=True, extra_blocked_modes=(),
                                 allowed_mode_risk_multiplier=0.5),
        disabled_modes_enabled=False, disabled_modes={},
    )
    base.update(over)
    return sg.SessionGuardConfig(**base)


# ---- guard_decision -------------------------------------------------------

def test_scalp_intraday_blocked_inside_window_swing_allowed():
    # Tuesday 03:00 UTC — inside 00–06, not Monday.
    t = datetime(2026, 7, 7, 3, 0, tzinfo=UTC)
    cfg = _cfg()
    assert sg.guard_decision(t, "scalp", "crypto", cfg).blocked is True
    assert sg.guard_decision(t, "intraday", "crypto", cfg).blocked is True
    dec_sw = sg.guard_decision(t, "swing", "crypto", cfg)
    assert dec_sw.blocked is False and dec_sw.in_window is True and dec_sw.active is True


def test_no_block_outside_window():
    t = datetime(2026, 7, 7, 10, 0, tzinfo=UTC)  # Tue 10:00 = EU session
    cfg = _cfg()
    for m in ("scalp", "intraday", "swing"):
        dec = sg.guard_decision(t, m, "crypto", cfg)
        assert dec.blocked is False and dec.in_window is False and dec.active is False


def test_non_crypto_never_blocked():
    t = datetime(2026, 7, 7, 3, 0, tzinfo=UTC)
    cfg = _cfg()
    assert sg.guard_decision(t, "scalp", "stocks", cfg).blocked is False
    assert sg.guard_decision(t, "intraday", "stock_etf", cfg).active is False


def test_monday_flag_and_risk_multiplier():
    t = datetime(2026, 7, 6, 2, 0, tzinfo=UTC)  # Monday 02:00 UTC
    cfg = _cfg()
    dec = sg.guard_decision(t, "swing", "crypto", cfg)
    assert dec.is_monday is True
    assert dec.risk_multiplier == 0.5  # Monday-stricter multiplier for allowed modes


def test_monday_extra_blocked_modes():
    t = datetime(2026, 7, 6, 2, 0, tzinfo=UTC)  # Monday 02:00
    cfg = _cfg(monday=sg.MondayStricter(enabled=True, extra_blocked_modes=("swing",),
                                        allowed_mode_risk_multiplier=0.5))
    assert sg.guard_decision(t, "swing", "crypto", cfg).blocked is True  # swing cut on Mon
    # non-Monday: swing stays allowed
    t2 = datetime(2026, 7, 7, 2, 0, tzinfo=UTC)
    assert sg.guard_decision(t2, "swing", "crypto", cfg).blocked is False


def test_disabled_config_is_noop():
    t = datetime(2026, 7, 7, 3, 0, tzinfo=UTC)
    assert sg.guard_decision(t, "scalp", "crypto", _cfg(enabled=False)).active is False
    assert sg.guard_decision(t, "scalp", "crypto", _cfg(dz_enabled=False)).active is False


def test_naive_datetime_treated_as_utc():
    t = datetime(2026, 7, 7, 3, 0)  # naive
    assert sg.guard_decision(t, "scalp", "crypto", _cfg()).blocked is True


def test_window_boundaries_half_open():
    cfg = _cfg()
    assert sg.guard_decision(datetime(2026, 7, 7, 0, 0, tzinfo=UTC), "scalp", "crypto", cfg).blocked is True   # 00:00 in
    assert sg.guard_decision(datetime(2026, 7, 7, 5, 59, tzinfo=UTC), "scalp", "crypto", cfg).blocked is True  # 05:59 in
    assert sg.guard_decision(datetime(2026, 7, 7, 6, 0, tzinfo=UTC), "scalp", "crypto", cfg).blocked is False  # 06:00 out


def test_wraparound_window():
    cfg = _cfg(utc_start_hour=22, utc_end_hour=2)  # 22:00–01:59
    assert sg.guard_decision(datetime(2026, 7, 7, 23, 0, tzinfo=UTC), "scalp", "crypto", cfg).blocked is True
    assert sg.guard_decision(datetime(2026, 7, 7, 1, 0, tzinfo=UTC), "scalp", "crypto", cfg).blocked is True
    assert sg.guard_decision(datetime(2026, 7, 7, 12, 0, tzinfo=UTC), "scalp", "crypto", cfg).blocked is False


# ---- hard mode kill-switch (crypto scalp disabled) ------------------------

def _cfg_scalp_off(**over):
    return _cfg(disabled_modes_enabled=True, disabled_modes={"crypto": ("scalp",)}, **over)


def test_crypto_scalp_disabled_any_hour_any_day():
    cfg = _cfg_scalp_off()
    # inside window
    d1 = sg.guard_decision(datetime(2026, 7, 7, 3, 0, tzinfo=UTC), "scalp", "crypto", cfg)
    # OUTSIDE the dead-zone window (US session) — still killed
    d2 = sg.guard_decision(datetime(2026, 7, 7, 15, 0, tzinfo=UTC), "scalp", "crypto", cfg)
    for d in (d1, d2):
        assert d.blocked is True and d.kind == "mode_disabled"
        assert d.demote_to_tier == "rejected"


def test_disabled_kill_is_time_independent():
    cfg = _cfg_scalp_off()
    d = sg.guard_decision(None, "scalp", "crypto", cfg)  # no timestamp
    assert d.blocked is True and d.kind == "mode_disabled"


def test_kill_only_targets_listed_mode_and_asset():
    cfg = _cfg_scalp_off()
    t = datetime(2026, 7, 7, 15, 0, tzinfo=UTC)  # US session (not dead-zone)
    assert sg.guard_decision(t, "intraday", "crypto", cfg).blocked is False  # intraday still runs
    assert sg.guard_decision(t, "swing", "crypto", cfg).blocked is False
    assert sg.guard_decision(t, "scalp", "stocks", cfg).blocked is False     # only crypto scalp killed


def test_apply_to_scores_rejects_disabled_crypto_scalp():
    cfg = _cfg_scalp_off()
    t = datetime(2026, 7, 7, 15, 0, tzinfo=UTC)  # any hour
    scores = {"BTC/USDT": _Score("A"), "ETH/USDT": _Score("B")}
    recs = sg.apply_to_scores(scores, "scalp", "crypto", t, cfg)
    assert scores["BTC/USDT"].tier == "rejected" and scores["ETH/USDT"].tier == "rejected"
    assert recs["BTC/USDT"].new_tier == "rejected"


def test_real_config_disables_crypto_scalp():
    root = Path(__file__).resolve().parents[1]
    cfg = sg.load_config(root)
    assert cfg.disabled_modes_enabled is True
    assert "scalp" in cfg.disabled_modes.get("crypto", ())
    # actual decision from real config: crypto scalp is off, crypto intraday is not killed
    assert sg.guard_decision(datetime(2026, 7, 7, 15, 0, tzinfo=UTC), "scalp", "crypto", cfg).blocked is True
    assert sg.guard_decision(datetime(2026, 7, 7, 15, 0, tzinfo=UTC), "intraday", "crypto", cfg).blocked is False


# ---- Monday Asia coverage (verification requested) ------------------------

def test_monday_asia_open_is_covered():
    """Monday 00–06 UTC (Asia open) must demote crypto intraday and flag Monday."""
    cfg = _cfg()  # dead-zone on, no kill
    d = sg.guard_decision(datetime(2026, 7, 6, 2, 0, tzinfo=UTC), "intraday", "crypto", cfg)
    assert d.blocked is True and d.kind == "asia_dead_zone" and d.is_monday is True
    # swing on Monday morning stays actionable but risk-reduced
    ds = sg.guard_decision(datetime(2026, 7, 6, 2, 0, tzinfo=UTC), "swing", "crypto", cfg)
    assert ds.blocked is False and ds.is_monday is True and ds.risk_multiplier == 0.5


# ---- apply_to_scores (production tier overlay) ----------------------------

class _Score:
    def __init__(self, tier):
        self.tier = tier
        self.cap_reasons: list = []
        self.reasons: list = []


def test_apply_to_scores_demotes_ab_to_c_for_blocked_mode():
    t = datetime(2026, 7, 7, 3, 0, tzinfo=UTC)
    scores = {"BTC/USDT": _Score("A"), "ETH/USDT": _Score("B"), "SOL/USDT": _Score("C")}
    recs = sg.apply_to_scores(scores, "scalp", "crypto", t, _cfg())
    assert scores["BTC/USDT"].tier == "C"        # A -> C
    assert scores["ETH/USDT"].tier == "C"        # B -> C
    assert scores["SOL/USDT"].tier == "C"        # C stays C (never raised)
    assert recs["BTC/USDT"].to_dict()["demoted"] is True
    assert recs["BTC/USDT"].new_tier == "C" and recs["BTC/USDT"].original_tier == "A"
    assert any("asia_dead_zone_guard" in r for r in scores["BTC/USDT"].cap_reasons)


def test_apply_to_scores_noop_for_swing_and_out_of_window():
    t = datetime(2026, 7, 7, 3, 0, tzinfo=UTC)
    scores = {"BTC/USDT": _Score("A")}
    assert sg.apply_to_scores(scores, "swing", "crypto", t, _cfg()) == {}
    assert scores["BTC/USDT"].tier == "A"        # swing untouched
    t_out = datetime(2026, 7, 7, 10, 0, tzinfo=UTC)
    assert sg.apply_to_scores(scores, "scalp", "crypto", t_out, _cfg()) == {}
    assert scores["BTC/USDT"].tier == "A"        # out of window untouched


def test_apply_never_raises_tier():
    t = datetime(2026, 7, 7, 3, 0, tzinfo=UTC)
    scores = {"X": _Score("rejected")}
    sg.apply_to_scores(scores, "intraday", "crypto", t, _cfg())
    assert scores["X"].tier == "rejected"        # demote_to_tier=C must not raise rejected->C


# ---- config load ----------------------------------------------------------

def test_real_config_loads_and_is_enabled():
    root = Path(__file__).resolve().parents[1]
    cfg = sg.load_config(root)
    assert cfg.enabled and cfg.dz_enabled
    assert cfg.utc_start_hour == 0 and cfg.utc_end_hour == 6
    assert cfg.blocked_modes == ()
    assert "swing" not in cfg.blocked_modes
    dec = sg.guard_decision(datetime(2026, 7, 7, 3, 0, tzinfo=UTC), "intraday", "crypto", cfg)
    assert dec.active is True and dec.blocked is False


def test_missing_config_is_safe_noop(tmp_path):
    cfg = sg.load_config(tmp_path)  # no config/session_risk.yaml here
    assert cfg.enabled is False and cfg.dz_enabled is False


# ---- guardrail: no live-execution surface ---------------------------------

def test_module_has_no_live_order_calls():
    src = Path(sg.__file__).read_text(encoding="utf-8").lower()
    for bad in ("create_order", "place_order", "submit_order", "auto_live",
                "manual_live", "final_r =", "update proposed_signals"):
        assert bad not in src, f"session_guard must be paper/overlay only: {bad!r}"
