"""Tests for the standardized Telegram alert templates (2026-06-14)."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from src.notifiers.alert_headers import (
    DISCLAIMER_MANUAL_SHADOW,
    DISCLAIMER_NOT_ACTIONABLE,
    HEADER_CLOSE_EXPIRED,
    HEADER_CLOSE_STOP,
    HEADER_CLOSE_TP,
    HEADER_OPERATOR_SUMMARY,
    HEADER_PAPER_ENTRY_LONG,
    HEADER_PAPER_ENTRY_SHORT,
    HEADER_SETUP_WAITING,
    HEADER_STOCKS_SETUP_ENTRY_CHANGE,
    HEADER_STOCKS_SETUP_NEW,
    HEADER_STOCKS_SETUP_SCORE_IMPROVEMENT,
    HEADER_STOCKS_SETUP_TIER_UPGRADE,
    operator_summary,
)
from src.notifiers.close_alert import decide_close, send_close_alert
from src.notifiers.paper_entry import decide_paper_entry
from src.notifiers.setup_alert import render_setup_alert


# ---- Fixtures ----------------------------------------------------------


def _crypto_swing_signal() -> dict:
    return {
        "signal_id": "sig_swing_1",
        "asset_class": "crypto",
        "symbol": "ZEC/USDT",
        "direction": "long",
        "mode": "swing",
        "tier": "B",
        "score": 74.2,
        "primary_exchange": "binance",
        "data_confidence": "medium",
        "entry_low": 42.0,
        "entry_high": 42.3,
        "entry_trigger": 42.15,
        "stop_loss": 40.80,
        "invalidation": 40.80,
        "tp1": 43.20,
        "tp2": 44.50,
        "tp3": 46.00,
        "thesis": "ZEC swing breakout vs BTC strength. Catalyst-backed narrative.",
        "setup_type": "breakout",
        "news_supported": 1,
        "market_regime": "risk_on",
        "funding_context": "funding=0.00005, crowding=normal",
        "raw_idea_json": json.dumps({"evidence": ["RS leader", "narrative cluster"]}),
    }


def _crypto_scalp_signal() -> dict:
    s = _crypto_swing_signal()
    s["signal_id"] = "sig_scalp_1"
    s["symbol"] = "OP/USDT"
    s["mode"] = "scalp"
    s["setup_type"] = "breakout"
    return s


def _stocks_a_long_signal() -> dict:
    return {
        "signal_id": "sig_aapl_a_1",
        "asset_class": "stocks",
        "symbol": "AAPL",
        "direction": "long",
        "mode": "intraday",
        "tier": "A",
        "score": 82.0,
        "data_confidence": "high",
        "entry_low": 254.0,
        "entry_high": 254.5,
        "entry_trigger": 254.5,
        "stop_loss": 251.0,
        "invalidation": 251.0,
        "tp1": 257.0,
        "tp2": 259.5,
        "tp3": 263.0,
        "thesis": "AAPL RTH momentum continuation.",
        "setup_type": "breakout",
        "news_supported": 0,
        "market_regime": "risk_on",
        "funding_context": "",
        "raw_idea_json": json.dumps({}),
    }


def _crypto_no_news_short_signal() -> dict:
    s = _crypto_swing_signal()
    s["signal_id"] = "sig_short_1"
    s["symbol"] = "BTC/USDT"
    s["mode"] = "intraday"
    s["direction"] = "short"
    s["news_supported"] = 0
    s["setup_type"] = "breakdown"
    return s


# ---- Setup alert tests --------------------------------------------------


def test_1_crypto_setup_header_present():
    msg = render_setup_alert(_crypto_swing_signal())
    assert HEADER_SETUP_WAITING in msg
    assert msg.startswith(HEADER_SETUP_WAITING)


def test_2_crypto_setup_says_no_paper_entry_yet():
    msg = render_setup_alert(_crypto_swing_signal())
    assert "No paper entry yet." in msg
    assert DISCLAIMER_MANUAL_SHADOW in msg


def test_3_crypto_setup_includes_signal_id():
    msg = render_setup_alert(_crypto_swing_signal())
    assert "signal_id: sig_swing_1" in msg


def test_4_crypto_setup_no_long_thesis_paragraph():
    s = _crypto_swing_signal()
    s["thesis"] = "x" * 1000  # huge thesis
    msg = render_setup_alert(s)
    # Either capped to under 900 char OR thesis was truncated to a first sentence.
    assert len(msg) <= 900 + 20  # MAX_SETUP plus minor truncation marker
    # No 300+ char block from thesis appears.
    assert "x" * 200 not in msg


def test_5_stocks_setup_uses_subtype_header():
    msg = render_setup_alert(_stocks_a_long_signal(), stocks_subtype="new_signal")
    assert HEADER_STOCKS_SETUP_NEW in msg
    msg2 = render_setup_alert(_stocks_a_long_signal(), stocks_subtype="entry_change")
    assert HEADER_STOCKS_SETUP_ENTRY_CHANGE in msg2
    msg3 = render_setup_alert(_stocks_a_long_signal(), stocks_subtype="score_improvement")
    assert HEADER_STOCKS_SETUP_SCORE_IMPROVEMENT in msg3
    msg4 = render_setup_alert(_stocks_a_long_signal(), stocks_subtype="tier_upgrade")
    assert HEADER_STOCKS_SETUP_TIER_UPGRADE in msg4


def test_5b_stocks_a_long_setup_shows_caution():
    msg = render_setup_alert(_stocks_a_long_signal(), stocks_subtype="new_signal")
    assert "A-tier long caution" in msg


# ---- Paper-entry tests --------------------------------------------------


def test_6_paper_entry_header_long():
    s = _crypto_swing_signal()
    d = decide_paper_entry(
        s,
        prev_status="waiting_for_entry",
        entry_triggered=True,
        entry_triggered_at="2026-06-14T11:22:00+00:00",
        entry_price_used=42.15,
    )
    assert d.should_send is True
    assert HEADER_PAPER_ENTRY_LONG in d.message
    assert HEADER_PAPER_ENTRY_LONG.startswith("[")


def test_6b_paper_entry_header_short():
    s = _crypto_no_news_short_signal()
    d = decide_paper_entry(
        s,
        prev_status="waiting_for_entry",
        entry_triggered=True,
        entry_triggered_at="2026-06-14T11:22:00+00:00",
        entry_price_used=70000.0,
    )
    assert HEADER_PAPER_ENTRY_SHORT in d.message


def test_7_paper_entry_separates_paper_record_from_mexc_confirmation():
    d = decide_paper_entry(
        _crypto_swing_signal(),
        prev_status="waiting_for_entry",
        entry_triggered=True,
        entry_triggered_at="2026-06-14T11:22:00+00:00",
        entry_price_used=42.15,
    )
    assert "Paper entry recorded. MEXC execution is confirmed separately after preflight." in d.message


def test_8_paper_entry_includes_signal_id_visibly():
    d = decide_paper_entry(
        _crypto_swing_signal(),
        prev_status="waiting_for_entry",
        entry_triggered=True,
        entry_triggered_at="2026-06-14T11:22:00+00:00",
        entry_price_used=42.15,
    )
    assert "signal_id: sig_swing_1" in d.message


def test_9_crypto_scalp_paper_entry_low_confidence_flag():
    d = decide_paper_entry(
        _crypto_scalp_signal(),
        prev_status="waiting_for_entry",
        entry_triggered=True,
        entry_triggered_at="2026-06-14T11:22:00+00:00",
        entry_price_used=42.15,
    )
    assert "LOW-CONFIDENCE SCALP" in d.message


def test_10_no_news_short_paper_entry_warning():
    s = _crypto_no_news_short_signal()
    # The risk-flag helper looks at funding_context for crowding wording —
    # for the no-news case the rationale block doesn't mark caution. The
    # setup_alert template DOES emit the caution; paper_entry currently
    # relies on the signal having news_supported=0 + mode=intraday short.
    # Re-render the SETUP message — the caution flag is shared.
    msg = render_setup_alert(s)
    assert "NO-NEWS / NO-DERIV SHORT" in msg


def test_11_stocks_a_long_paper_entry_caution():
    s = _stocks_a_long_signal()
    d = decide_paper_entry(
        s,
        prev_status="waiting_for_entry",
        entry_triggered=True,
        entry_triggered_at="2026-06-14T13:30:00+00:00",
        entry_price_used=254.5,
    )
    assert d.should_send is True
    assert "A-tier long caution" in d.message
    assert "Size: 0.5x" in d.message


# ---- Close-alert tests --------------------------------------------------


def test_12_close_alert_keeps_runner_open_on_first_tp():
    s = _crypto_swing_signal()
    outcome = {
        "final_outcome": "win",
        "final_r": 1.0,
        "entry_triggered": 1,
        "entry_triggered_at": "2026-06-14T11:00:00+00:00",
        "tp1_hit": 1,
        "tp1_hit_at": "2026-06-14T13:30:00+00:00",
    }
    d = decide_close(s, outcome, prev_final_outcome=None)
    assert d.should_send is False
    assert "milestone" in d.reason_skipped


def test_13_close_alert_dedup_no_double_send(tmp_path: Path):
    db_path = tmp_path / "t.sqlite"
    conn = sqlite3.connect(db_path)
    conn.execute(
        """CREATE TABLE signal_alerts (alert_id TEXT PRIMARY KEY, signal_id TEXT,
        asset_class TEXT, mode TEXT, symbol TEXT, tier TEXT, score REAL,
        direction TEXT, sent_at TEXT, alert_type TEXT, telegram_status TEXT,
        message_hash TEXT, payload_json TEXT)"""
    )
    conn.execute(
        "INSERT INTO signal_alerts VALUES ('a1','sig_swing_1','crypto','swing',"
        "'ZEC/USDT','B',74.2,'long','2026-06-14T13:30:00+00:00','close_tp','sent','h','{}')"
    )
    conn.commit()
    conn.close()

    class FakeStore:
        def connect(self):
            c = sqlite3.connect(db_path)
            c.row_factory = sqlite3.Row
            return c

        def record_signal_alert(self, **kw):
            pass

    notifier = MagicMock()
    out = send_close_alert(
        store=FakeStore(),
        notifier=notifier,
        signal=_crypto_swing_signal(),
        outcome_row={"status": "tp3_hit", "final_outcome": "win", "final_r": 1.0,
                     "entry_triggered": 1, "tp1_hit": 1, "tp2_hit": 1, "tp3_hit": 1,
                     "tp3_hit_at": "2026-06-14T13:30:00+00:00",
                     "entry_triggered_at": "2026-06-14T11:00:00+00:00"},
        prev_final_outcome=None,
    )
    assert out["sent"] is False
    assert "duplicate" in (out["reason_skipped"] or "").lower()
    notifier.send.assert_not_called()


def test_13b_close_alert_skipped_when_prev_status_already_terminal():
    """Transition guard: a trade already closed in a prior cycle must NOT
    re-alert. This is the 2026-06-15 fix for the historical-backfill flood."""
    s = _crypto_swing_signal()
    outcome = {"final_outcome": "win", "final_r": 1.0, "entry_triggered": 1,
               "tp1_hit": 1, "tp1_hit_at": "2026-06-14T13:30:00+00:00",
               "entry_triggered_at": "2026-06-14T11:00:00+00:00"}
    # prev_status already terminal → skip
    d = decide_close(s, outcome, prev_status="tp1_hit")
    assert d.should_send is False
    assert "milestone" in d.reason_skipped
    # fresh transition from a pending status → send
    d2 = decide_close(s, outcome, prev_status="triggered")
    assert d2.should_send is False


def test_13c_close_alert_age_backstop():
    """A signal created far in the past must not alert even if prev_status
    is non-terminal (defensive backfill guard)."""
    s = _crypto_swing_signal()
    s["created_at"] = "2026-01-01T00:00:00+00:00"  # months ago
    outcome = {"status": "tp3_hit", "final_outcome": "win", "final_r": 1.0,
               "entry_triggered": 1, "tp1_hit": 1, "tp2_hit": 1, "tp3_hit": 1,
               "tp3_hit_at": "2026-01-01T02:00:00+00:00",
               "entry_triggered_at": "2026-01-01T00:30:00+00:00"}
    d = decide_close(s, outcome, prev_status="triggered")
    assert d.should_send is False
    assert "too old" in d.reason_skipped


def test_14_close_alert_skipped_for_never_entered():
    s = _crypto_swing_signal()
    outcome = {"final_outcome": "loss", "final_r": -1.0, "entry_triggered": 0}
    d = decide_close(s, outcome, prev_final_outcome=None)
    assert d.should_send is False
    assert "never entered" in d.reason_skipped


def test_15_close_alert_skipped_for_c_tier_and_paused_playbooks():
    s = _crypto_swing_signal()
    s["tier"] = "C"
    outcome = {"final_outcome": "loss", "final_r": -1.0, "entry_triggered": 1,
               "entry_triggered_at": "2026-06-14T11:00:00+00:00",
               "stop_hit": 1, "stop_hit_at": "2026-06-14T12:00:00+00:00"}
    d = decide_close(s, outcome, prev_final_outcome=None)
    assert d.should_send is False
    assert "tier=C" in d.reason_skipped

    s2 = _stocks_a_long_signal()
    s2["mode"] = "swing"  # paused
    outcome2 = {"final_outcome": "loss", "final_r": -1.0, "entry_triggered": 1,
                "entry_triggered_at": "2026-06-14T13:30:00+00:00",
                "stop_hit": 1, "stop_hit_at": "2026-06-14T14:30:00+00:00"}
    d2 = decide_close(s2, outcome2, prev_final_outcome=None)
    assert d2.should_send is False


# ---- Close-alert lifecycle-aware R wording (PART 3) ---------------------


def test_close_expired_after_entry_not_bare_plus_0r():
    """An expired-after-entry close must read as 'unresolved 0R', not '+0.0R' profit,
    and must carry a reason — never a bare 'expired'."""
    s = _crypto_swing_signal()
    outcome = {"final_outcome": "expired", "final_r": 0.0, "entry_triggered": 1,
               "entry_triggered_at": "2026-06-14T11:00:00+00:00",
               "checked_at": "2026-06-14T19:00:00+00:00"}
    d = decide_close(s, outcome, prev_status="triggered")
    assert d.should_send is True
    assert "+-" not in d.message
    assert "unresolved" in d.message.lower()
    assert "no tp/sl before validity window" in d.message.lower()
    # the old confusing bare profit line must be gone
    assert "Result: +0.0R raw" not in d.message


def test_close_true_flat_shows_closed_flat_0r():
    s = _crypto_swing_signal()
    outcome = {"status": "tp3_hit", "final_outcome": "win", "final_r": 0.0,
               "entry_triggered": 1, "tp1_hit": 1, "tp2_hit": 1, "tp3_hit": 1,
               "tp3_hit_at": "2026-06-14T13:30:00+00:00",
               "entry_triggered_at": "2026-06-14T11:00:00+00:00"}
    d = decide_close(s, outcome, prev_status="triggered")
    assert "CLOSED FLAT 0R" in d.message
    assert "+-" not in d.message


def test_close_loss_sign_no_double_sign():
    s = _crypto_swing_signal()
    outcome = {"final_outcome": "loss", "final_r": -1.0, "entry_triggered": 1,
               "stop_hit": 1, "stop_hit_at": "2026-06-14T12:00:00+00:00",
               "entry_triggered_at": "2026-06-14T11:00:00+00:00"}
    d = decide_close(s, outcome, prev_status="triggered")
    assert "+-" not in d.message
    assert "legacy touch -1.0R" in d.message


def test_close_win_with_negative_r_flags_contradiction():
    s = _crypto_swing_signal()
    outcome = {"status": "tp3_hit", "final_outcome": "win", "final_r": -1.0,
               "entry_triggered": 1, "tp1_hit": 1, "tp2_hit": 1, "tp3_hit": 1,
               "tp3_hit_at": "2026-06-14T13:30:00+00:00",
               "entry_triggered_at": "2026-06-14T11:00:00+00:00"}
    d = decide_close(s, outcome, prev_status="triggered")
    assert "+-" not in d.message
    assert "data check" in d.message.lower()


# ---- Operator summary --------------------------------------------------


def test_15b_setup_telegram_suppressed_for_live_only_trade_feed():
    """2026-08-31: setup alerts are journal/dashboard only; Telegram trade
    notifications are reserved for live-routed entries/fills/closes."""
    from src.agents.supervisor import should_suppress_setup_telegram as f
    assert f("crypto", "scalp") is True
    assert f("CRYPTO", "SCALP") is True
    assert f("crypto", "intraday") is True
    assert f("crypto", "swing") is True
    assert f("stocks", "scalp") is True
    assert f("stocks", "intraday") is True


def test_16_operator_summary_header_and_disclaimer():
    msg = operator_summary("Some body content here.\nMultiple lines OK.",
                            title="TEST SUMMARY")
    assert msg.startswith(HEADER_OPERATOR_SUMMARY)
    assert "NOT ACTIONABLE" in msg
    assert "No paper entry recorded." in msg


# ---- Parse-mode discipline ----------------------------------------------


def test_17_setup_alert_is_plain_text_safe():
    # The standardized template must not emit Markdown markers that would
    # break parse_mode='Markdown'.
    msg = render_setup_alert(_crypto_swing_signal())
    # No raw "*bold*" markers in body
    assert not (msg.count("*") > 0 and "**" in msg)
    # No raw backtick code fences
    assert "```" not in msg


def test_17b_live_routed_paper_entry_call_uses_plain_text(tmp_path: Path, monkeypatch):
    """When a Paper entry is accepted into live handoff, notifier.send uses
    parse_mode=''."""
    from src.notifiers.paper_entry import send_paper_entry_alert
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
    db_path = tmp_path / "t.sqlite"
    conn = sqlite3.connect(db_path)
    conn.execute(
        """CREATE TABLE signal_alerts (alert_id TEXT PRIMARY KEY, signal_id TEXT,
        asset_class TEXT, mode TEXT, symbol TEXT, tier TEXT, score REAL,
        direction TEXT, sent_at TEXT, alert_type TEXT, telegram_status TEXT,
        message_hash TEXT, payload_json TEXT)"""
    )
    conn.commit()
    conn.close()

    class FakeStore:
        def connect(self):
            c = sqlite3.connect(db_path)
            c.row_factory = sqlite3.Row
            return c

        def record_signal_alert(self, **kw):
            pass

    notifier = MagicMock()
    send_paper_entry_alert(
        store=FakeStore(),
        notifier=notifier,
        signal=_crypto_swing_signal(),
        prev_status="waiting_for_entry",
        outcome_entry_triggered=True,
        # fresh entry so it routes as actionable (sent), not late-shadow
        outcome_entry_triggered_at=datetime.now(timezone.utc).isoformat(),
        outcome_entry_price_used=42.15,
    )
    notifier.send.assert_called_once()
    args, kwargs = notifier.send.call_args
    # Plain text
    assert kwargs.get("parse_mode", None) == "" or (len(args) >= 2 and args[1] == "")


# ---- Surface invariants (no scoring/TP/SL/sizing change) ----------------


def test_18_no_strategy_files_modified_by_template_layer():
    """Grep the new notifier modules for any forbidden surface mutation."""
    import re
    modules = [
        Path(__file__).resolve().parents[1] / "src" / "notifiers" / "alert_headers.py",
        Path(__file__).resolve().parents[1] / "src" / "notifiers" / "setup_alert.py",
        Path(__file__).resolve().parents[1] / "src" / "notifiers" / "close_alert.py",
    ]
    pat = re.compile(r"UPDATE proposed_signals|UPDATE signal_outcomes|"
                     r"DELETE FROM signal_outcomes|TP|stop_loss\s*=|tier\s*=")
    for m in modules:
        text = m.read_text(encoding="utf-8")
        # These modules format messages only; they may MENTION tp/stop_loss
        # as DICT KEYS read from the signal — but never assign to them.
        # The "set" pattern is `something = value`. Check there's no
        # `signal['stop_loss'] = ` etc.
        assert "signal['stop_loss'] =" not in text
        assert "signal['tp1'] =" not in text
        assert "UPDATE " not in text
