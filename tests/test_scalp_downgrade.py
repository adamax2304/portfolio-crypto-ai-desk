"""Guardrails for scalp shadow-only + live-only trade Telegram routing.

Ensures scalp stays non-actionable and non-scalp Paper entries reach Telegram
only after live handoff accepted them.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _fresh_entry_ts() -> str:
    """A just-now entry-touch timestamp so the paper-entry classifies as fresh
    (the freshness/late-routing layer is exercised separately)."""
    return datetime.now(timezone.utc).isoformat()


def _sig(asset, mode, direction="long", tier="B"):
    return {
        "signal_id": f"sig_{asset}_{mode}_{direction}",
        "asset_class": asset, "symbol": "ZEC/USDT" if asset == "crypto" else "AAPL",
        "direction": direction, "mode": mode, "tier": tier, "score": 70.0,
        "primary_exchange": "binance", "entry_low": 42.0, "entry_high": 42.3,
        "entry_trigger": 42.15, "stop_loss": 40.8, "invalidation": 40.8,
        "tp1": 43.2, "tp2": 44.5, "tp3": 46.0, "setup_type": "breakout",
        "news_supported": 0, "funding_context": "funding=0.0001, crowding=normal",
        "oi_context": "price up + OI up", "raw_idea_json": json.dumps({}),
    }


def _fresh_store(tmp_path):
    from src.storage.sqlite import SQLiteStore
    st = SQLiteStore(tmp_path / "t.sqlite")
    st.init_db()
    return st


def _force_full_overlay(monkeypatch):
    """Keep routing tests independent of the shared machine's current session state."""
    from src.execution.crypto_quality_overlay import OverlayDecision

    def _full(signal, **kwargs):
        return OverlayDecision(signal_id=signal["signal_id"], symbol=signal["symbol"],
                               mode=signal["mode"], action="FULL_SIZE", reasons=["test"])

    monkeypatch.setattr("src.execution.crypto_quality_overlay.decide_for_signal", _full)


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


# 1. scalp sizing weight is 0x
def test_1_scalp_sizing_weight_is_zero():
    from src.signals.sizing import size_decision
    d = size_decision({**_sig("crypto", "scalp"), "final_r": 1.0})
    assert d.weight == 0.0
    # sized_r must be 0 regardless of raw
    assert d.sized_r == 0.0


# 2. scalp setup Telegram remains suppressed
def test_2_scalp_setup_telegram_suppressed():
    from src.agents.supervisor import should_suppress_setup_telegram
    assert should_suppress_setup_telegram("crypto", "scalp") is True


# 3. scalp paper-entry immediate Telegram is shadow-only (not pushed)
def test_3_scalp_paper_entry_shadow_only(tmp_path):
    from src.notifiers.paper_entry import send_paper_entry_alert
    st = _fresh_store(tmp_path)
    notifier = MagicMock()
    out = send_paper_entry_alert(
        store=st, notifier=notifier, signal=_sig("crypto", "scalp"),
        prev_status="waiting_for_entry", outcome_entry_triggered=True,
        outcome_entry_triggered_at="2026-06-15T12:00:00+00:00",
        outcome_entry_price_used=42.15,
    )
    assert out["telegram_status"] == "shadow_only"
    assert out["sent"] is False
    notifier.send.assert_not_called()          # never pushed to phone
    assert "SHADOW ONLY" in out["message"]
    # row still recorded (research/journal visibility)
    with st.connect() as c:
        row = c.execute("SELECT telegram_status, payload_json FROM signal_alerts "
                        "WHERE alert_type='paper_entry'").fetchone()
    assert row is not None
    assert row[0] == "shadow_only"
    assert json.loads(row[1])["telegram_channel"] == "shadow_only"


# 4. scalp still appears in research/journal (predicate-only check: it is a real signal)
def test_4_scalp_still_generated_and_recorded(tmp_path):
    from src.notifiers.paper_entry import send_paper_entry_alert
    st = _fresh_store(tmp_path)
    send_paper_entry_alert(
        store=st, notifier=MagicMock(), signal=_sig("crypto", "scalp"),
        prev_status="waiting_for_entry", outcome_entry_triggered=True,
        outcome_entry_triggered_at="2026-06-15T12:00:00+00:00",
        outcome_entry_price_used=42.15,
    )
    with st.connect() as c:
        n = c.execute("SELECT COUNT(*) FROM signal_alerts WHERE mode='scalp'").fetchone()[0]
    assert n == 1  # recorded for research, just not pushed


def _assert_pushed(tmp_path, sig, monkeypatch):
    from src.notifiers.paper_entry import send_paper_entry_alert
    _force_live_queued(monkeypatch)
    st = _fresh_store(tmp_path)
    notifier = MagicMock()
    out = send_paper_entry_alert(
        store=st, notifier=notifier, signal=sig,
        prev_status="waiting_for_entry", outcome_entry_triggered=True,
        outcome_entry_triggered_at=_fresh_entry_ts(),
        outcome_entry_price_used=42.15,
    )
    return out, notifier


# 5. crypto intraday paper-entry still sends
def test_5_crypto_intraday_still_sends(tmp_path, monkeypatch):
    _force_full_overlay(monkeypatch)
    out, notifier = _assert_pushed(tmp_path, _sig("crypto", "intraday"), monkeypatch)
    assert out["telegram_status"] == "sent"
    assert out["payload"]["telegram_channel"] == "live_handoff"
    assert "LIVE QUEUED" in out["message"]
    notifier.send.assert_called_once()


# 6. native crypto swing geometry remains production-paper control
def test_6_crypto_swing_legacy_geometry_still_sends(tmp_path, monkeypatch):
    _force_full_overlay(monkeypatch)
    out, notifier = _assert_pushed(tmp_path, _sig("crypto", "swing"), monkeypatch)
    assert out["telegram_status"] == "sent"
    assert out["sent"] is True
    notifier.send.assert_called_once()


# 7. crypto failed-bounce short still sends
def test_7_crypto_short_still_sends(tmp_path, monkeypatch):
    _force_full_overlay(monkeypatch)
    out, notifier = _assert_pushed(tmp_path, _sig("crypto", "intraday", direction="short"), monkeypatch)
    assert out["telegram_status"] == "sent"


# 8. stocks intraday paper-entry still sends
def test_8_stocks_intraday_still_sends(tmp_path, monkeypatch):
    out, notifier = _assert_pushed(tmp_path, _sig("stocks", "intraday"), monkeypatch)
    assert out["telegram_status"] == "sent"


# 9. no TP/SL/scoring/routing change — scalp geometry agent untouched
def test_9_no_tp_sl_scoring_change():
    text = (ROOT / "src" / "agents" / "technical_setup_agent.py").read_text(encoding="utf-8")
    # geometry constants intact
    assert "1.0 * atr" in text and "1.2 * atr" in text and "0.65 * atr" in text


# 10. no auto-trade path
def test_10_no_auto_trade_path():
    import re
    for f in ("src/notifiers/paper_entry.py", "src/notifiers/close_alert.py"):
        t = (ROOT / f).read_text(encoding="utf-8")
        assert "place_order" not in t and "create_order" not in t and "ccxt" not in t
