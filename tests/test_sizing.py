"""Tests for the playbook-aware sizing reporting layer.

These tests pin the routing matrix specified in
`reports/PROFITABILITY_LEVERS_AUDIT.md` (Lever 1) and verify:
  - the helper produces the correct weight per cohort,
  - raw_r is echoed back unchanged,
  - sized_r is `raw_r * weight`,
  - the helper does not raise on missing fields.
"""
from __future__ import annotations

from src.signals.sizing import (
    SizingDecision,
    portfolio_totals,
    size_decision,
    size_signals,
)


def _sig(**kw):
    base = dict(
        asset_class="crypto",
        mode="intraday",
        direction="long",
        tier="B",
        score=70,
        news_supported=0,
        final_r=1.0,
    )
    base.update(kw)
    return base


# ---------------------------------------------------------------------------
# Cohort routing matrix
# ---------------------------------------------------------------------------


def test_crypto_scalp_gets_zero_shadow_only():
    # 2026-06-15 downgrade: crypto scalp is SHADOW ONLY → 0× (was 0.5×).
    d = size_decision(_sig(mode="scalp"))
    assert d.weight == 0.0
    assert d.playbook == "crypto_scalp_momentum_continuation"


def test_stocks_a_tier_intraday_long_gets_half():
    d = size_decision(_sig(asset_class="stocks", mode="intraday",
                           tier="A", direction="long", score=82))
    assert d.weight == 0.5
    assert d.playbook == "stocks_intraday_rth_momentum"
    assert "A-tier" in d.reason or "overpromotion" in d.reason


def test_stocks_b_tier_intraday_gets_full():
    d = size_decision(_sig(asset_class="stocks", mode="intraday",
                           tier="B", direction="long", score=70))
    assert d.weight == 1.0
    assert d.playbook == "stocks_intraday_rth_momentum"


def test_stocks_intraday_short_gets_full():
    d = size_decision(_sig(asset_class="stocks", mode="intraday",
                           tier="B", direction="short", score=70))
    assert d.weight == 1.0


def test_stocks_swing_gets_zero():
    d = size_decision(_sig(asset_class="stocks", mode="swing",
                           tier="B", direction="long"))
    assert d.weight == 0.0
    assert d.playbook == "stocks_swing_watchlist_rs_rotation"


def test_stock_swing_event_rs_gets_full_weight():
    d = size_decision(_sig(
        asset_class="stocks",
        mode="swing",
        tier="B",
        direction="long",
        raw_idea_json='{"paper_entry_profile":"stocks_swing_event_rs_pullback_quality_paper_v1"}',
        final_r=1.25,
    ))
    assert d.weight == 1.0
    assert d.playbook == "stocks_swing_event_rs_pullback"
    assert d.sized_r == 1.25


def test_stocks_invest_gets_zero():
    d = size_decision(_sig(asset_class="stocks", mode="invest",
                           tier="B", direction="long"))
    assert d.weight == 0.0
    assert d.playbook == "stocks_invest_watchlist_30d_thesis"


def test_c_tier_gets_zero():
    d = size_decision(_sig(asset_class="crypto", mode="swing",
                           tier="C", direction="long"))
    assert d.weight == 0.0
    assert "tier" in d.reason.lower() or "watchlist" in d.reason.lower()


def test_crypto_swing_long_gets_full():
    d = size_decision(_sig(mode="swing", tier="B", direction="long"))
    assert d.weight == 1.0
    assert d.playbook == "crypto_swing_narrative_rs_momentum"


def test_crypto_intraday_catalyst_gets_full():
    d = size_decision(_sig(mode="intraday", tier="B", news_supported=1))
    assert d.weight == 1.0
    assert d.playbook == "crypto_intraday_catalyst_or_momentum"


def test_crypto_short_gets_full():
    d = size_decision(_sig(mode="intraday", tier="B", direction="short"))
    assert d.weight == 1.0
    assert d.playbook == "crypto_failed_bounce_short"


# ---------------------------------------------------------------------------
# Raw R / sized R math
# ---------------------------------------------------------------------------


def test_raw_r_echoed_back_unchanged():
    d = size_decision(_sig(final_r=-1.0))
    assert d.raw_r == -1.0  # echoed verbatim


def test_sized_r_is_product_of_raw_and_weight():
    # Use a 1.0× cohort to verify the raw×weight product (scalp is now 0×).
    d = size_decision(_sig(mode="swing", final_r=-1.0))
    assert d.weight == 1.0
    assert d.sized_r == -1.0
    # scalp (0×) → sized 0 regardless of raw
    ds = size_decision(_sig(mode="scalp", final_r=-1.0))
    assert ds.weight == 0.0
    assert ds.sized_r == 0.0


def test_sized_r_zero_when_paused_mode():
    d = size_decision(_sig(asset_class="stocks", mode="swing", final_r=-1.0))
    assert d.weight == 0.0
    assert d.sized_r == 0.0


def test_sized_r_none_when_raw_r_missing():
    d = size_decision(_sig(final_r=None))
    assert d.raw_r is None
    assert d.sized_r is None


def test_explicit_raw_r_key_supported():
    """The helper accepts `raw_r` as well as `final_r`."""
    sig = _sig()
    sig.pop("final_r", None)
    sig["raw_r"] = 2.0
    d = size_decision(sig)
    assert d.raw_r == 2.0


# ---------------------------------------------------------------------------
# Robustness
# ---------------------------------------------------------------------------


def test_helper_does_not_raise_on_missing_fields():
    size_decision({})  # should not raise
    size_signals([{}])


def test_size_signals_does_not_mutate_input():
    sig = _sig(mode="swing", final_r=1.0)
    snapshot = dict(sig)
    out = size_signals([sig])
    assert sig == snapshot  # unchanged
    assert out[0]["sizing_weight"] == 1.0
    assert out[0]["sized_r"] == 1.0


# ---------------------------------------------------------------------------
# Portfolio aggregation
# ---------------------------------------------------------------------------


def test_portfolio_totals_skip_zero_weight_from_sized_metrics():
    """Watchlist / paused signals should not appear in WR or PF math."""
    decisions = [
        size_decision(_sig(mode="swing", final_r=1.0)),                 # +1 (1.0×)
        size_decision(_sig(mode="swing", final_r=-1.0)),                # -1 (1.0×)
        size_decision(_sig(asset_class="stocks", mode="swing",
                           final_r=-1.0)),                              # 0  (0× paused)
        size_decision(_sig(mode="scalp", final_r=-1.0)),                # 0  (0× shadow-only)
        size_decision(_sig(tier="C", final_r=-1.0)),                    # 0  (0× C-tier)
    ]
    totals = portfolio_totals(decisions)
    # n_sized counts weight>0 with raw_r — 2 of 5 (scalp now 0×).
    assert totals["n_sized"] == 2
    # sum_sized_r = +1 -1 = 0.0
    assert totals["sum_sized_r"] == 0.0
    # sum_raw_r echoes ALL raw_r (sizing doesn't change raw). 5 signals: +1,-1,-1,-1,-1 = -3.
    assert totals["sum_raw_r"] == -3.0
    # wins/losses are sized-only — 1 win (+1) and 1 loss (-1)
    assert totals["wins"] == 1
    assert totals["losses"] == 1


# ---------------------------------------------------------------------------
# Invariant: no DB / signal generation imports
# ---------------------------------------------------------------------------


def test_sizing_module_does_not_import_writer_paths():
    """Spec invariant: the sizing module must not import writer paths."""
    import inspect
    from src.signals import sizing as mod
    src = inspect.getsource(mod)
    assert "TelegramNotifier" not in src
    assert "SQLiteStore" not in src
    assert "register_ideas" not in src
    assert "upsert_proposed_signal" not in src
    assert "scoring_agent" not in src
