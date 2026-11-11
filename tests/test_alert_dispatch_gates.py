"""Guards for the 2026-06-16 simultaneous open+close Telegram fix.

The tracker must never emit a paper-entry (open) and a close alert for the same
signal in the same evaluation. Root cause was `_classify` returning the
OUTCOME_EXPIRED *placeholder* as `final_outcome` for still-open trades, so the
close hook (keyed on `final_outcome`) fired a bogus close_expired in the same
tick the trade entered. The dispatch now keys on `status`.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock

# Recent timestamps so the close-alert >4d backfill age-guard never trips on
# stale hardcoded fixture dates (the test asserts a fresh close DOES send).
_NOW = datetime.now(timezone.utc)
_CREATED_AT = (_NOW - timedelta(hours=2)).isoformat()
_ENTRY_AT = (_NOW - timedelta(hours=1, minutes=30)).isoformat()
_TP_AT = (_NOW - timedelta(hours=1)).isoformat()

from src.signals.models import (
    STATUS_AMBIGUOUS,
    STATUS_EXPIRED,
    STATUS_MISSED_NO_ENTRY,
    STATUS_STOPPED,
    STATUS_TP1,
    STATUS_TP2,
    STATUS_TP3,
    STATUS_TRIGGERED,
    STATUS_WAITING,
)
from src.signals.tracker import should_alert_close, should_alert_paper_entry


def _sig(asset, mode, direction="long", tier="B"):
    return {
        "signal_id": f"sig_{asset}_{mode}_{direction}",
        "asset_class": asset, "symbol": "ZEC/USDT" if asset == "crypto" else "AAPL",
        "direction": direction, "mode": mode, "tier": tier, "score": 70.0,
        "primary_exchange": "binance", "entry_low": 42.0, "entry_high": 42.3,
        "entry_trigger": 42.15, "stop_loss": 40.8, "invalidation": 40.8,
        "tp1": 43.2, "tp2": 44.5, "tp3": 46.0, "setup_type": "breakout",
        "news_supported": 0, "created_at": _CREATED_AT,
        "raw_idea_json": json.dumps({}),
    }


def _store(tmp_path):
    from src.storage.sqlite import SQLiteStore
    st = SQLiteStore(tmp_path / "t.sqlite"); st.init_db(); return st


def _force_live_queued(monkeypatch):
    monkeypatch.setattr(
        "src.live_execution.service.capture_paper_candidate",
        lambda **_kwargs: {
            "status": "QUEUED",
            "queued": True,
            "decision_id": "live-test-decision",
            "reasons": [],
            "execution_mode": "live",
        },
    )


# ---- paper-entry: only while OPEN -----------------------------------------

def test_paper_entry_fires_when_entered_and_open():
    assert should_alert_paper_entry(True, STATUS_TRIGGERED) is True


def test_paper_entry_suppressed_when_not_entered():
    assert should_alert_paper_entry(False, STATUS_WAITING) is False
    assert should_alert_paper_entry(False, STATUS_TRIGGERED) is False


def test_paper_entry_suppressed_when_already_closed_same_tick():
    # Entered AND a terminal status in one evaluation → no entry alert.
    for st in (STATUS_TP1, STATUS_TP2, STATUS_TP3, STATUS_STOPPED,
               STATUS_EXPIRED, STATUS_AMBIGUOUS):
        assert should_alert_paper_entry(True, st) is False, st


# ---- close: only a genuine terminal transition out of OPEN ----------------

def test_close_fires_on_terminal_transition_from_triggered():
    for st in (STATUS_TP3, STATUS_STOPPED, STATUS_EXPIRED, STATUS_AMBIGUOUS):
        assert should_alert_close(st, STATUS_TRIGGERED) is True, st
    assert should_alert_close(STATUS_TP1, STATUS_TRIGGERED) is False
    assert should_alert_close(STATUS_TP2, STATUS_TRIGGERED) is False


def test_close_suppressed_for_open_trade_with_placeholder_outcome():
    # The bug: an open trade has status='triggered' but final_outcome='expired'
    # placeholder. Keyed on status, the close must NOT fire while open.
    assert should_alert_close(STATUS_TRIGGERED, STATUS_TRIGGERED) is False
    assert should_alert_close(STATUS_TRIGGERED, STATUS_WAITING) is False


def test_close_suppressed_for_same_tick_round_trip():
    # Enter+close within one evaluation: prev_status is pre-entry, so the close
    # has no paired entry alert and must be suppressed (operator had no window).
    assert should_alert_close(STATUS_EXPIRED, STATUS_WAITING) is False
    assert should_alert_close(STATUS_STOPPED, STATUS_MISSED_NO_ENTRY) is False
    assert should_alert_close(STATUS_TP1, STATUS_WAITING) is False


def test_close_suppressed_for_non_entry_statuses():
    assert should_alert_close(STATUS_MISSED_NO_ENTRY, STATUS_WAITING) is False
    assert should_alert_close(STATUS_WAITING, STATUS_WAITING) is False


# ---- the exact production bug never recurs --------------------------------

def test_no_simultaneous_open_and_close_in_one_evaluation():
    """For every (status, prev_status), entry and close are mutually exclusive."""
    statuses = [STATUS_WAITING, STATUS_TRIGGERED, STATUS_TP1, STATUS_TP2,
                STATUS_TP3, STATUS_STOPPED, STATUS_EXPIRED, STATUS_AMBIGUOUS,
                STATUS_MISSED_NO_ENTRY]
    for status in statuses:
        for prev in statuses:
            pe = should_alert_paper_entry(True, status)
            cl = should_alert_close(status, prev)
            assert not (pe and cl), f"both fired for status={status} prev={prev}"


# ---- integration: gate + routing -----------------------------------------

def test_scalp_legit_open_routes_shadow_only(tmp_path):
    """A scalp trade that DID open (gate fires) still routes shadow_only, not sent."""
    assert should_alert_paper_entry(True, STATUS_TRIGGERED) is True
    from src.notifiers.paper_entry import send_paper_entry_alert
    notifier = MagicMock()
    out = send_paper_entry_alert(
        store=_store(tmp_path), notifier=notifier, signal=_sig("crypto", "scalp"),
        prev_status="waiting_for_entry", outcome_entry_triggered=True,
        outcome_entry_triggered_at="2026-06-16T12:00:00+00:00",
        outcome_entry_price_used=42.15,
    )
    assert out["telegram_status"] == "shadow_only"
    assert out["sent"] is False
    notifier.send.assert_not_called()


# ---- entry freshness label + late-entry shadow routing (PART 5) -----------

def test_entry_freshness_classification():
    from datetime import datetime, timedelta, timezone
    from src.notifiers.paper_entry import entry_freshness
    now = datetime(2026, 6, 16, 12, 0, 0, tzinfo=timezone.utc)
    def at(mins):
        return (now - timedelta(minutes=mins)).isoformat()
    assert entry_freshness(at(0.5), now)[2] is True   # fresh, actionable
    assert "fresh" in entry_freshness(at(0.5), now)[0]
    assert entry_freshness(at(4), now)[2] is True      # acceptable
    assert entry_freshness(at(10), now)[2] is True     # late but actionable
    assert "late" in entry_freshness(at(10), now)[0]
    assert entry_freshness(at(40), now)[2] is False    # very late, not actionable
    assert "very late" in entry_freshness(at(40), now)[0]
    assert entry_freshness(None, now)[2] is False      # unknown → not actionable


def test_very_late_nonscalp_entry_routes_late_shadow(tmp_path):
    """A >15min-old non-scalp entry is recorded but NOT pushed (late shadow)."""
    from datetime import datetime, timedelta, timezone
    from src.notifiers.paper_entry import send_paper_entry_alert
    notifier = MagicMock()
    stale = (datetime.now(timezone.utc) - timedelta(minutes=40)).isoformat()
    out = send_paper_entry_alert(
        store=_store(tmp_path), notifier=notifier, signal=_sig("crypto", "intraday"),
        prev_status="waiting_for_entry", outcome_entry_triggered=True,
        outcome_entry_triggered_at=stale, outcome_entry_price_used=42.15,
    )
    assert out["telegram_status"] == "late_shadow"
    assert out["sent"] is False
    assert out["reason_skipped"] == "late_entry"
    assert "[LATE ENTRY DETECTED — DO NOT CHASE]" in out["message"]
    notifier.send.assert_not_called()


def test_fresh_nonscalp_entry_sends_with_label(tmp_path, monkeypatch):
    from datetime import datetime, timezone
    from src.notifiers.paper_entry import send_paper_entry_alert
    from src.execution import crypto_quality_overlay as cqo
    _force_live_queued(monkeypatch)
    monkeypatch.setattr(
        cqo, "decide_for_signal",
        lambda *args, **kwargs: cqo.OverlayDecision(action="FULL_SIZE", reasons=["test_fixture"]),
    )
    notifier = MagicMock()
    out = send_paper_entry_alert(
        store=_store(tmp_path), notifier=notifier, signal=_sig("crypto", "intraday"),
        prev_status="waiting_for_entry", outcome_entry_triggered=True,
        outcome_entry_triggered_at=datetime.now(timezone.utc).isoformat(),
        outcome_entry_price_used=42.15,
    )
    assert out["telegram_status"] == "sent"
    assert out["payload"]["telegram_channel"] == "live_handoff"
    assert "LIVE QUEUED" in out["message"]
    notifier.send.assert_called_once()


def test_nonscalp_close_after_open_sends(tmp_path):
    """Legit non-scalp close is pushed only when its entry was live-routed."""
    assert should_alert_close(STATUS_EXPIRED, STATUS_TRIGGERED) is True
    from src.notifiers.close_alert import send_close_alert
    store = _store(tmp_path)
    signal = _sig("crypto", "intraday")
    store.record_signal_alert(
        alert_id="entry-live",
        signal_id=signal["signal_id"],
        asset_class="crypto",
        symbol=signal["symbol"],
        tier="B",
        sent_at=_ENTRY_AT,
        alert_type="paper_entry",
        mode="intraday",
        score=70.0,
        direction="long",
        telegram_status="sent",
        message_hash="entry",
        payload={"telegram_channel": "live_handoff", "mexc_canary_capture_status": "QUEUED"},
    )
    notifier = MagicMock()
    outcome_row = {
        "status": "tp3_hit", "final_outcome": "win", "final_r": 1.0,
        "entry_triggered": 1, "entry_triggered_at": _ENTRY_AT,
        "tp1_hit": 1, "tp2_hit": 1, "tp3_hit": 1, "tp3_hit_at": _TP_AT,
    }
    out = send_close_alert(
        store=store, notifier=notifier, signal=signal,
        outcome_row=outcome_row, prev_status="triggered", dry_run=False,
    )
    assert out["telegram_status"] == "sent"
    notifier.send.assert_called_once()


def test_close_inherits_shadow_lineage_from_its_entry(tmp_path):
    """A non-actionable entry must never produce an actionable close."""
    from src.notifiers.close_alert import send_close_alert

    store = _store(tmp_path)
    signal = _sig("crypto", "intraday")
    store.record_signal_alert(
        alert_id="entry-shadow",
        signal_id=signal["signal_id"],
        asset_class="crypto",
        symbol=signal["symbol"],
        tier="B",
        sent_at=_ENTRY_AT,
        alert_type="paper_entry",
        mode="intraday",
        score=70.0,
        direction="long",
        telegram_status="shadow_only",
        message_hash="entry",
        payload={"telegram_channel": "shadow_only_risk_guard"},
    )
    notifier = MagicMock()
    out = send_close_alert(
        store=store,
        notifier=notifier,
        signal=signal,
        outcome_row={
            "status": "tp3_hit", "final_outcome": "win", "final_r": 1.0,
            "entry_triggered": 1, "entry_triggered_at": _ENTRY_AT,
            "tp1_hit": 1, "tp2_hit": 1, "tp3_hit": 1, "tp3_hit_at": _TP_AT,
        },
        prev_status="triggered",
        dry_run=False,
    )
    assert out["telegram_status"] == "shadow_only"
    assert out["payload"]["entry_alert_lineage"]["operator_visible"] is False
    notifier.send.assert_not_called()
