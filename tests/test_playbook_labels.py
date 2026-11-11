"""Tests for the playbook labeling utility.

Annotation-only utility; tests cover the routing decisions for every
mode × asset_class × direction × news combination called out in the
STRATEGY_PLAYBOOK_AUDIT document.
"""
from __future__ import annotations

from src.signals.playbooks import (
    OVERLAY_CATALYST_BACKED,
    OVERLAY_LOW_CONFIDENCE_SCALP,
    OVERLAY_RS_LEADER,
    OVERLAY_SHORT_PLAYBOOK,
    OVERLAY_WATCHLIST_ONLY_MODE,
    PLAYBOOK_CRYPTO_FAILED_BOUNCE_SHORT,
    PLAYBOOK_CRYPTO_INTRADAY,
    PLAYBOOK_CRYPTO_SCALP,
    PLAYBOOK_CRYPTO_SWING,
    PLAYBOOK_STOCKS_INTRADAY,
    PLAYBOOK_STOCKS_INVEST_WATCH,
    PLAYBOOK_STOCKS_SWING_EVENT_RS_PULLBACK,
    PLAYBOOK_STOCKS_SWING_WATCH,
    STATUS_ACTIONABLE,
    STATUS_LOW_CONFIDENCE,
    STATUS_WATCHLIST_ONLY,
    label_for,
)


def _sig(**kw):
    base = dict(asset_class="crypto", mode="intraday", direction="long",
                tier="B", score=70, news_supported=0)
    base.update(kw)
    return base


# ---------------------------------------------------------------------------
# Primary playbook routing
# ---------------------------------------------------------------------------

def test_crypto_scalp_is_low_confidence():
    lbl = label_for(_sig(mode="scalp"))
    assert lbl.playbook == PLAYBOOK_CRYPTO_SCALP
    assert lbl.status == STATUS_LOW_CONFIDENCE
    assert OVERLAY_LOW_CONFIDENCE_SCALP in lbl.overlays
    assert "TP1/2h horizon" in lbl.why


def test_crypto_intraday_with_catalyst_is_actionable():
    lbl = label_for(_sig(mode="intraday", news_supported=1))
    assert lbl.playbook == PLAYBOOK_CRYPTO_INTRADAY
    assert lbl.status == STATUS_ACTIONABLE
    assert OVERLAY_CATALYST_BACKED in lbl.overlays
    assert "catalyst" in lbl.why.lower()


def test_crypto_intraday_no_catalyst_is_actionable_but_weaker():
    lbl = label_for(_sig(mode="intraday", news_supported=0))
    assert lbl.playbook == PLAYBOOK_CRYPTO_INTRADAY
    assert lbl.status == STATUS_ACTIONABLE
    assert OVERLAY_CATALYST_BACKED not in lbl.overlays
    assert "no-catalyst" in lbl.why.lower() or "no catalyst" in lbl.why.lower()


def test_crypto_swing_long_is_primary_playbook():
    lbl = label_for(_sig(mode="swing", score=75))
    assert lbl.playbook == PLAYBOOK_CRYPTO_SWING
    assert lbl.status == STATUS_ACTIONABLE
    assert "primary" in lbl.why.lower() or "WR 72" in lbl.why


def test_crypto_intraday_short_routes_to_failed_bounce():
    lbl = label_for(_sig(mode="intraday", direction="short"))
    assert lbl.playbook == PLAYBOOK_CRYPTO_FAILED_BOUNCE_SHORT
    assert lbl.status == STATUS_ACTIONABLE
    assert OVERLAY_SHORT_PLAYBOOK in lbl.overlays


def test_crypto_swing_short_routes_to_failed_bounce():
    lbl = label_for(_sig(mode="swing", direction="short"))
    assert lbl.playbook == PLAYBOOK_CRYPTO_FAILED_BOUNCE_SHORT


# ---------------------------------------------------------------------------
# Stocks playbooks
# ---------------------------------------------------------------------------

def test_stocks_intraday_is_actionable():
    lbl = label_for(_sig(asset_class="stocks", mode="intraday"))
    assert lbl.playbook == PLAYBOOK_STOCKS_INTRADAY
    assert lbl.status == STATUS_ACTIONABLE


def test_stocks_swing_is_watchlist_only():
    lbl = label_for(_sig(asset_class="stocks", mode="swing"))
    assert lbl.playbook == PLAYBOOK_STOCKS_SWING_WATCH
    assert lbl.status == STATUS_WATCHLIST_ONLY
    assert OVERLAY_WATCHLIST_ONLY_MODE in lbl.overlays


def test_stock_swing_event_rs_profile_is_actionable_paper_playbook():
    lbl = label_for(_sig(
        asset_class="stocks",
        mode="swing",
        raw_idea_json='{"paper_entry_profile":"stocks_swing_event_rs_pullback_quality_paper_v1"}',
    ))
    assert lbl.playbook == PLAYBOOK_STOCKS_SWING_EVENT_RS_PULLBACK
    assert lbl.status == STATUS_ACTIONABLE
    assert OVERLAY_WATCHLIST_ONLY_MODE not in lbl.overlays


def test_stocks_invest_is_watchlist_only():
    lbl = label_for(_sig(asset_class="stocks", mode="invest"))
    assert lbl.playbook == PLAYBOOK_STOCKS_INVEST_WATCH
    assert lbl.status == STATUS_WATCHLIST_ONLY
    assert OVERLAY_WATCHLIST_ONLY_MODE in lbl.overlays


# ---------------------------------------------------------------------------
# Overlays
# ---------------------------------------------------------------------------

def test_rs_leader_overlay_only_on_high_score_crypto_intraday_swing_long():
    high = label_for(_sig(mode="swing", score=85))
    low = label_for(_sig(mode="swing", score=70))
    short = label_for(_sig(mode="swing", direction="short", score=85))
    scalp = label_for(_sig(mode="scalp", score=85))
    assert OVERLAY_RS_LEADER in high.overlays
    assert OVERLAY_RS_LEADER not in low.overlays
    assert OVERLAY_RS_LEADER not in short.overlays
    assert OVERLAY_RS_LEADER not in scalp.overlays


def test_catalyst_overlay_present_on_news_supported():
    lbl = label_for(_sig(news_supported=1))
    assert OVERLAY_CATALYST_BACKED in lbl.overlays


def test_short_overlay_present_on_short_direction():
    lbl = label_for(_sig(direction="short"))
    assert OVERLAY_SHORT_PLAYBOOK in lbl.overlays


# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------

def test_markdown_block_contains_required_fields():
    lbl = label_for(_sig(mode="swing", news_supported=1, score=85))
    md = lbl.to_markdown_block(heading_level=4)
    assert "#### Playbook" in md
    assert lbl.playbook in md
    assert "actionable" in md
    assert "rs_leader" in md
    assert "catalyst_backed" in md
    assert "Why this playbook:" in md
    assert "Known failure mode:" in md


def test_to_dict_round_trip():
    lbl = label_for(_sig(mode="scalp"))
    d = lbl.to_dict()
    assert d["playbook"] == PLAYBOOK_CRYPTO_SCALP
    assert d["status"] == STATUS_LOW_CONFIDENCE
    assert OVERLAY_LOW_CONFIDENCE_SCALP in d["overlays"]


# ---------------------------------------------------------------------------
# Robustness
# ---------------------------------------------------------------------------

def test_unknown_mode_falls_through_safely():
    lbl = label_for({"asset_class": "crypto", "mode": "exotic", "direction": "long"})
    assert lbl.playbook in ("unknown", PLAYBOOK_CRYPTO_INTRADAY,
                            PLAYBOOK_CRYPTO_SCALP, PLAYBOOK_CRYPTO_SWING)


def test_missing_fields_does_not_raise():
    label_for({})  # should not raise
