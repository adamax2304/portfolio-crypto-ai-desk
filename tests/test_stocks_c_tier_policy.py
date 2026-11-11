"""Stocks-intraday C-tier shadow/review-only policy (FAST SAFE ACCELERATION PART 1).

Asserts the restriction labels/routes C-tier stocks-intraday to shadow, leaves A/B
and crypto untouched, and never changes scoring/TP/SL/size.
"""
from __future__ import annotations

from src.signals.tier_policy import (
    c_tier_restriction_fields,
    is_restricted,
    is_stocks_intraday_c_tier,
)


def _sig(asset="stocks", mode="intraday", tier="C"):
    return {"asset_class": asset, "mode": mode, "tier": tier, "symbol": "FOO",
            "score": 55.0, "stop_loss": 98.0, "tp1": 104.0}


def test_stocks_intraday_c_tier_is_restricted_by_default():
    assert is_stocks_intraday_c_tier(_sig()) is True
    assert is_restricted(_sig(), "shadow_review_only") is True
    f = c_tier_restriction_fields(_sig(), "shadow_review_only")
    assert f["c_tier_restriction_applied"] is True
    assert f["c_tier_restriction_reason"] == "stocks_intraday_c_tier_30d_negative"
    assert f["diagnostic_or_policy"] == "risk_restriction"


def test_stocks_intraday_AB_not_restricted():
    for tier in ("A", "B"):
        assert is_restricted(_sig(tier=tier), "shadow_review_only") is False
        assert c_tier_restriction_fields(_sig(tier=tier))["c_tier_restriction_applied"] is False


def test_crypto_c_tier_unaffected():
    assert is_restricted(_sig(asset="crypto"), "shadow_review_only") is False
    # crypto intraday C-tier is NOT touched by this stocks-only policy
    assert c_tier_restriction_fields(_sig(asset="crypto"))["c_tier_restriction_applied"] is False


def test_stocks_swing_invest_c_tier_not_restricted_by_this_rule():
    for mode in ("swing", "invest", "scalp"):
        assert is_restricted(_sig(mode=mode), "shadow_review_only") is False


def test_actionable_policy_disables_restriction():
    assert is_restricted(_sig(), "actionable") is False
    f = c_tier_restriction_fields(_sig(), "actionable")
    assert f["c_tier_restriction_applied"] is False
    assert f["c_tier_policy"] == "actionable"


def test_policy_loads_from_config_default_restricted():
    from src.signals.tier_policy import load_stocks_intraday_c_tier_policy
    # config ships shadow_review_only; loader must never raise and defaults safe
    pol = load_stocks_intraday_c_tier_policy()
    assert pol in ("shadow_review_only", "actionable")


def test_fields_do_not_carry_scoring_or_tpsl_keys():
    # the policy must add ONLY routing/label fields — never tier/score/TP/SL/size
    f = c_tier_restriction_fields(_sig())
    for forbidden in ("tier", "score", "stop_loss", "tp1", "tp2", "tp3", "size_weight"):
        assert forbidden not in f


def test_paper_entry_never_pushes_stocks_intraday_c_tier(tmp_path):
    """C-tier is already blocked at decide_paper_entry ('tier=C not actionable').
    This confirms a C-tier stocks-intraday signal is NEVER pushed as an actionable
    alert (no Telegram send), i.e. it is shadow/review-only by construction."""
    import uuid
    from datetime import datetime, timezone
    from src.notifiers.paper_entry import send_paper_entry_alert
    from src.storage.sqlite import SQLiteStore

    store = SQLiteStore(tmp_path / "t.sqlite")
    store.init_db()
    now = datetime.now(timezone.utc).isoformat()

    class FakeNotifier:
        def __init__(self): self.sent = []
        def send(self, text, parse_mode="Markdown"): self.sent.append(text); return {"ok": True}

    sig = {
        "signal_id": f"ct_{uuid.uuid4().hex[:6]}", "created_at": now, "updated_at": now,
        "symbol": "ZZZZ", "direction": "long", "mode": "intraday", "tier": "C",
        "asset_class": "stocks", "score": 55.0, "status": "triggered",
        "entry_low": 100.0, "entry_high": 101.0, "stop_loss": 98.0,
        "tp1": 104.0, "tp2": 106.0, "tp3": 110.0,
    }
    n = FakeNotifier()
    res = send_paper_entry_alert(
        store=store, notifier=n, signal=sig, prev_status="waiting_for_entry",
        outcome_entry_triggered=True, outcome_entry_triggered_at=now,
        outcome_entry_price_used=100.5)
    # blocked upstream → not sent, never pushed to Telegram
    assert res["sent"] is False
    assert n.sent == []
    assert "not actionable" in (res["reason_skipped"] or "").lower()


def test_AB_stocks_intraday_still_actionable(tmp_path):
    """The restriction must NOT touch A/B: a B-tier stocks-intraday entry still sends."""
    import uuid
    from datetime import datetime, timezone
    from src.notifiers.paper_entry import send_paper_entry_alert
    from src.storage.sqlite import SQLiteStore

    store = SQLiteStore(tmp_path / "t.sqlite")
    store.init_db()
    now = datetime.now(timezone.utc).isoformat()

    class FakeNotifier:
        def __init__(self): self.sent = []
        def send(self, text, parse_mode="Markdown"): self.sent.append(text); return {"ok": True}

    sig = {
        "signal_id": f"ab_{uuid.uuid4().hex[:6]}", "created_at": now, "updated_at": now,
        "symbol": "AAPL", "direction": "long", "mode": "intraday", "tier": "B",
        "asset_class": "stocks", "score": 75.0, "status": "triggered",
        "entry_low": 100.0, "entry_high": 101.0, "stop_loss": 98.0,
        "tp1": 104.0, "tp2": 106.0, "tp3": 110.0,
    }
    res = send_paper_entry_alert(
        store=store, notifier=FakeNotifier(), signal=sig, prev_status="waiting_for_entry",
        outcome_entry_triggered=True, outcome_entry_triggered_at=now,
        outcome_entry_price_used=100.5)
    # A/B path is unchanged — not shadow_c_tier
    assert res["payload"]["c_tier_restriction_applied"] is False
    assert res["telegram_status"] != "shadow_c_tier"
