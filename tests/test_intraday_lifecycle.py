"""Intraday lifecycle labels / revalidation flags (profitability guardrails PART 5).

Asserts labels are assigned, carryover requires next-day review, and NOTHING is
force-closed (the function only returns labels — never an action/flatten field).
"""
from __future__ import annotations

from datetime import datetime, timezone, timedelta

from src.signals.lifecycle import compute_lifecycle_label

NOW = datetime(2026, 6, 17, 15, 0, tzinfo=timezone.utc)


def _sig(*, asset="crypto", mode="intraday", created_h=1, status="triggered",
         news=0):
    return {"asset_class": asset, "mode": mode, "status": status,
            "news_supported": news,
            "created_at": (NOW - timedelta(hours=created_h)).isoformat()}


def _entry(h):
    return (NOW - timedelta(hours=h)).isoformat()


def test_crypto_fresh_then_aging_then_stale():
    fresh = compute_lifecycle_label(_sig(), now=NOW, entry_triggered_at=_entry(2))
    assert fresh["lifecycle_label"] == "fresh_intraday"
    aging = compute_lifecycle_label(_sig(created_h=8), now=NOW, entry_triggered_at=_entry(8))
    assert aging["lifecycle_label"] == "aging_intraday"
    stale = compute_lifecycle_label(_sig(created_h=13), now=NOW, entry_triggered_at=_entry(13))
    assert stale["lifecycle_label"] == "stale_intraday"
    assert stale["next_day_revalidation_required"] is True


def test_crypto_carryover_requires_review_and_no_force_close():
    # created yesterday (UTC) → carryover
    sig = _sig(created_h=20)
    out = compute_lifecycle_label(sig, now=NOW, entry_triggered_at=_entry(20))
    assert out["carryover_warning"] is True
    assert out["next_day_revalidation_required"] is True
    assert "carryover" in out["lifecycle_label"]
    # diagnostic only — there is NO force-close / flatten / size field
    assert out["diagnostic_only"] is True
    assert "action" not in out and "force_close" not in out and "flatten" not in out


def test_crypto_expired_at_0r_candidate_past_validity():
    out = compute_lifecycle_label(_sig(created_h=26), now=NOW, entry_triggered_at=_entry(26))
    assert out["lifecycle_label"] == "expired_at_0R_candidate"
    assert out["next_day_revalidation_required"] is True


def test_stocks_overnight_hold_flagged():
    # stocks created yesterday → overnight + revalidation
    out = compute_lifecycle_label(_sig(asset="stocks", created_h=22), now=NOW,
                                  entry_triggered_at=_entry(22))
    assert out["rth_overnight_hold"] is True
    assert out["next_day_revalidation_required"] is True
    assert "carryover" in out["lifecycle_label"]


def test_stocks_fresh_intraday_during_rth():
    # 15:00 UTC is inside RTH (13-20), created 1h ago → fresh
    out = compute_lifecycle_label(_sig(asset="stocks", created_h=1), now=NOW,
                                  entry_triggered_at=_entry(1))
    assert out["lifecycle_label"] == "fresh_intraday"
    assert out["rth_overnight_hold"] is False


def test_terminal_or_non_intraday_not_labeled():
    closed = compute_lifecycle_label(_sig(status="stopped"), now=NOW)
    assert closed["lifecycle_label"] == "closed"
    swing = compute_lifecycle_label(_sig(mode="swing"), now=NOW)
    assert swing["lifecycle_label"] == "n/a"


def test_held_hours_and_regime_change_flag():
    out = compute_lifecycle_label(_sig(created_h=3), now=NOW, entry_triggered_at=_entry(3),
                                  regime_at_entry="bullish trend", regime_now="btc_risk_off")
    assert out["held_hours"] == 3.0
    assert out["regime_changed_since_entry"] is True
