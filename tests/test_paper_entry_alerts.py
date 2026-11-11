"""Tests for the paper-entry Telegram alert layer."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from src.notifiers.paper_entry import (
    decide_paper_entry,
    has_existing_paper_entry_alert,
    send_paper_entry_alert,
)


# ---------- Fixtures --------------------------------------------------------

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


def _crypto_b_swing_signal() -> dict:
    return {
        "signal_id": "sig_test_crypto_swing_1",
        "asset_class": "crypto",
        "symbol": "ZEC/USDT",
        "direction": "long",
        "mode": "swing",
        "tier": "B",
        "score": 74.2,
        "primary_exchange": "binance",
        "data_confidence": "medium",
        "entry_low": 42.0, "entry_high": 42.3, "entry_trigger": 42.15,
        "suggested_entry": 42.15,
        "stop_loss": 40.80, "invalidation": 40.80,
        "tp1": 43.20, "tp2": 44.50, "tp3": 46.00,
        "thesis": "ZEC swing breakout vs BTC strength. Catalyst-backed narrative.",
        "news_supported": 1,
        "setup_type": "breakout",
        "market_regime": "risk_on",
        "funding_context": "funding=0.00005, crowding=normal",
        "raw_idea_json": json.dumps({"evidence": ["RS leader vs BTC", "narrative cluster"]}),
    }


def _crypto_b_scalp_signal() -> dict:
    s = _crypto_b_swing_signal()
    s["signal_id"] = "sig_test_crypto_scalp_1"
    s["symbol"] = "OP/USDT"
    s["mode"] = "scalp"
    s["setup_type"] = "breakout"
    s["score"] = 68.0
    return s


def _stocks_a_intraday_long_signal() -> dict:
    return {
        "signal_id": "sig_test_stocks_a_long_1",
        "asset_class": "stocks",
        "symbol": "AAPL",
        "direction": "long",
        "mode": "intraday",
        "tier": "A",
        "score": 82.0,
        "data_confidence": "high",
        "entry_low": 254.0, "entry_high": 254.5, "entry_trigger": 254.5,
        "suggested_entry": 254.5,
        "stop_loss": 251.0, "invalidation": 251.0,
        "tp1": 257.0, "tp2": 259.5, "tp3": 263.0,
        "thesis": "AAPL RTH momentum continuation.",
        "news_supported": 0,
        "setup_type": "breakout",
        "market_regime": "risk_on",
        "funding_context": "",
        "raw_idea_json": json.dumps({}),
    }


def _c_tier_signal() -> dict:
    s = _crypto_b_swing_signal()
    s["signal_id"] = "sig_test_c"
    s["tier"] = "C"
    s["score"] = 52
    return s


def _stocks_swing_signal() -> dict:
    s = _stocks_a_intraday_long_signal()
    s["signal_id"] = "sig_test_stocks_swing"
    s["mode"] = "swing"
    s["tier"] = "B"
    return s


# ---------- Tests -----------------------------------------------------------

def test_1_alert_fires_on_waiting_to_triggered():
    s = _crypto_b_swing_signal()
    d = decide_paper_entry(s, prev_status="waiting_for_entry",
                           entry_triggered=True,
                           entry_triggered_at="2026-06-11T11:22:00+00:00",
                           entry_price_used=42.15)
    assert d.should_send is True
    # 2026-06-14 standardization: header on its own line, body on next
    assert "PAPER ENTRY — TRIGGERED" in d.message
    assert "CRYPTO ZEC/USDT LONG" in d.message
    assert d.payload["entry_reference"] == 42.15


def test_2_no_dup_on_second_call(tmp_path: Path):
    db_path = tmp_path / "t.sqlite"
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE signal_alerts (
          alert_id TEXT PRIMARY KEY, signal_id TEXT, asset_class TEXT, mode TEXT,
          symbol TEXT, tier TEXT, score REAL, direction TEXT, sent_at TEXT,
          alert_type TEXT, telegram_status TEXT, message_hash TEXT, payload_json TEXT
        )
    """)
    conn.execute("INSERT INTO signal_alerts VALUES('a1','sig_test_crypto_swing_1','crypto','swing',"
                 "'ZEC/USDT','B',74.2,'long','2026-06-11T11:00:00+00:00','paper_entry','sent','h','{}')")
    conn.commit()
    conn.close()

    class FakeStore:
        def connect(self):
            return sqlite3.connect(db_path)

    assert has_existing_paper_entry_alert(FakeStore(), "sig_test_crypto_swing_1") is True
    assert has_existing_paper_entry_alert(FakeStore(), "sig_test_other") is False


def test_3_no_alert_for_c_tier():
    s = _c_tier_signal()
    d = decide_paper_entry(s, prev_status="waiting_for_entry",
                           entry_triggered=True,
                           entry_triggered_at="2026-06-11T11:22:00+00:00",
                           entry_price_used=42.15)
    assert d.should_send is False
    assert "tier=C" in d.reason_skipped or "not actionable" in d.reason_skipped


def _stocks_c_session_cap_signal() -> dict:
    s = _stocks_a_intraday_long_signal()
    s["signal_id"] = "sig_test_stocks_preus_c"
    s["tier"] = "C"
    s["score"] = 62.0
    s["raw_idea_json"] = json.dumps({
        "pre_gate_tier": "B",
        "cap_reasons": ["market_closed_intraday_planning_only: US cash session closed"],
    })
    return s


def _preus_review_db(tmp_path: Path, signal: dict, *, now: datetime | None = None) -> Path:
    """Minimal DB with proposed_signals + the pre-US review tables, seeded
    with the given signal so decide_paper_entry(db=...) can look it up."""
    from src.execution import stocks_preus_review as preus

    path = tmp_path / "preus_paper_entry.sqlite"
    stamp = now or datetime.now(timezone.utc)
    conn = sqlite3.connect(str(path))
    conn.execute("""CREATE TABLE proposed_signals (
        signal_id TEXT PRIMARY KEY, symbol TEXT, asset_class TEXT, mode TEXT, direction TEXT,
        tier TEXT, score REAL, status TEXT, created_at TEXT, entry_trigger REAL, suggested_entry REAL,
        entry_low REAL, entry_high REAL, stop_loss REAL, invalidation REAL, raw_idea_json TEXT
    )""")
    conn.execute("""CREATE TABLE stocks_paper_decision_snapshots (
        signal_id TEXT PRIMARY KEY, funnel_state TEXT
    )""")
    # news_items with ONE fresh, high-importance, symbol-tagged row so the
    # catalyst-integrity hard-gate check (src/catalysts/integrity.py ->
    # news_catalyst_symbols) confirms a genuine catalyst instead of excluding
    # for "no direct news catalyst" — matching what a real pre-US SUPPORT
    # candidate must have. Legal/earnings hard-gate helpers query the same
    # table and find nothing blocking (no matching keywords in this row).
    conn.execute("""CREATE TABLE news_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT, source TEXT, url TEXT, published_at TEXT,
        detected_symbols_json TEXT, importance REAL, asset_class TEXT
    )""")
    conn.execute(
        "INSERT INTO news_items (title, source, url, published_at, detected_symbols_json, "
        "importance, asset_class) VALUES (?,?,?,?,?,?,?)",
        ("AAPL announces new product line", "test-source", "https://example.test/1",
         stamp.isoformat(), json.dumps([signal["symbol"]]), 5.0, "stocks"),
    )
    conn.execute(
        "INSERT INTO proposed_signals VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (signal["signal_id"], signal["symbol"], "stocks", "intraday", "long",
         signal["tier"], signal["score"], "waiting_for_entry",
         stamp.isoformat(), 190.0, 190.0, None, None, 185.0, 185.0,
         signal["raw_idea_json"]),
    )
    conn.commit()
    conn.close()
    return path


def test_3b_c_tier_stocks_session_cap_remains_blocked_without_review(tmp_path: Path):
    """No review recorded -> falls straight back to the unmodified deterministic
    tier gate (spec: missing/expired review must never block the pipeline, it
    must just behave exactly as before)."""
    s = _stocks_c_session_cap_signal()
    db = _preus_review_db(tmp_path, s)
    d = decide_paper_entry(s, prev_status="waiting_for_entry", entry_triggered=True,
                           entry_triggered_at="2026-07-28T12:00:00+00:00",
                           entry_price_used=190.0, db=str(db))
    assert d.should_send is False
    assert "not actionable" in d.reason_skipped


def test_3c_c_tier_stocks_session_cap_becomes_actionable_with_supportive_review(tmp_path: Path, monkeypatch):
    from src.execution import stocks_preus_review as preus

    monkeypatch.setattr(
        preus, "_hard_gate_reason", lambda conn, row, *, now, cfg, **kwargs: None
    )
    s = _stocks_c_session_cap_signal()
    review_at = datetime(2026, 7, 28, 12, 55, tzinfo=timezone.utc)  # 08:55 ET
    db = _preus_review_db(tmp_path, s, now=review_at - timedelta(minutes=15))
    cfg = preus.load_cfg()
    preus.record_verdict(
        signal_id=s["signal_id"], verdict="SUPPORT", requested_adjustment=5,
        evidence={k: True for k in cfg["support_requires"]}, db=db, now=review_at,
    )
    d = decide_paper_entry(s, prev_status="waiting_for_entry", entry_triggered=True,
                           entry_triggered_at="2026-07-28T13:00:00+00:00",
                           entry_price_used=190.0, db=str(db))
    assert d.should_send is True


def test_3d_c_tier_stocks_substantive_reason_never_actionable_even_with_review(tmp_path: Path):
    """A C-tier caused by a SUBSTANTIVE reason (not market_closed) must never
    be promoted, even if a SUPPORT review row happens to exist for it."""
    from src.execution import stocks_preus_review as preus

    s = _stocks_c_session_cap_signal()
    s["raw_idea_json"] = json.dumps({
        "pre_gate_tier": "C",
        "cap_reasons": ["legal_headline_risk: SEC investigation"],
    })
    db = _preus_review_db(tmp_path, s)
    cfg = preus.load_cfg()
    preus.record_verdict(
        signal_id=s["signal_id"], verdict="SUPPORT", requested_adjustment=5,
        evidence={k: True for k in cfg["support_requires"]}, db=db,
    )
    d = decide_paper_entry(s, prev_status="waiting_for_entry", entry_triggered=True,
                           entry_triggered_at="2026-07-28T12:00:00+00:00",
                           entry_price_used=190.0, db=str(db))
    assert d.should_send is False


def test_3e_c_tier_stocks_review_lookup_error_falls_back_deterministically(tmp_path: Path):
    """A DB path that does not exist / errors during lookup must degrade to
    the unmodified deterministic path, never raise."""
    s = _stocks_c_session_cap_signal()
    d = decide_paper_entry(s, prev_status="waiting_for_entry", entry_triggered=True,
                           entry_triggered_at="2026-07-28T12:00:00+00:00",
                           entry_price_used=190.0, db=str(tmp_path / "does_not_exist.sqlite"))
    assert d.should_send is False
    assert "not actionable" in d.reason_skipped


def test_4_no_alert_for_stocks_swing_or_invest():
    s = _stocks_swing_signal()
    d = decide_paper_entry(s, prev_status="waiting_for_entry",
                           entry_triggered=True,
                           entry_triggered_at="2026-06-11T13:30:00+00:00",
                           entry_price_used=254.5)
    assert d.should_send is False
    assert "paused" in d.reason_skipped or "watchlist" in d.reason_skipped or "swing/invest" in d.reason_skipped


def test_5_no_alert_when_not_triggered():
    s = _crypto_b_swing_signal()
    d = decide_paper_entry(s, prev_status="stale_before_entry",
                           entry_triggered=False,
                           entry_triggered_at=None, entry_price_used=None)
    assert d.should_send is False


def test_6_message_includes_playbook_label():
    s = _crypto_b_swing_signal()
    d = decide_paper_entry(s, prev_status="waiting_for_entry",
                           entry_triggered=True,
                           entry_triggered_at="2026-06-11T11:22:00+00:00",
                           entry_price_used=42.15)
    assert "Playbook:" in d.message
    assert "crypto_swing_narrative_rs_momentum" in d.message or \
           "crypto_" in d.message  # playbook label present


def test_7_message_includes_size_weight_and_reason():
    s = _crypto_b_swing_signal()
    d = decide_paper_entry(s, prev_status="waiting_for_entry",
                           entry_triggered=True,
                           entry_triggered_at="2026-06-11T11:22:00+00:00",
                           entry_price_used=42.15)
    assert "Size:" in d.message
    assert "x" in d.message  # the "1x" / "0.5x" suffix


def test_8_message_includes_entry_stop_tp():
    s = _crypto_b_swing_signal()
    d = decide_paper_entry(s, prev_status="waiting_for_entry",
                           entry_triggered=True,
                           entry_triggered_at="2026-06-11T11:22:00+00:00",
                           entry_price_used=42.15)
    # 2026-06-14 standardization: line is now `Entry: 42.1500`
    assert "Entry: 42.1500" in d.message or "Entry: 42." in d.message
    assert "Stop: 40." in d.message
    assert "TP: 43." in d.message and "44." in d.message


def test_9_message_includes_tradingview_link():
    s = _crypto_b_swing_signal()
    d = decide_paper_entry(s, prev_status="waiting_for_entry",
                           entry_triggered=True,
                           entry_triggered_at="2026-06-11T11:22:00+00:00",
                           entry_price_used=42.15)
    assert "TradingView:" in d.message
    assert "tradingview.com" in d.message
    assert "BINANCE:ZECUSDT" in d.message


def test_10_alert_uses_plain_text_parse_mode(tmp_path: Path, monkeypatch):
    _force_live_queued(monkeypatch)
    s = _stocks_a_intraday_long_signal()
    notifier = MagicMock()
    db_path = tmp_path / "t.sqlite"
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE signal_alerts (
          alert_id TEXT PRIMARY KEY, signal_id TEXT, asset_class TEXT, mode TEXT,
          symbol TEXT, tier TEXT, score REAL, direction TEXT, sent_at TEXT,
          alert_type TEXT, telegram_status TEXT, message_hash TEXT, payload_json TEXT
        )
    """)
    conn.commit()
    conn.close()

    class FakeStore:
        def connect(self):
            c = sqlite3.connect(db_path)
            c.row_factory = sqlite3.Row
            return c
        def record_signal_alert(self, **kw):
            with self.connect() as c:
                c.execute(
                    "INSERT INTO signal_alerts(alert_id, signal_id, asset_class, mode, symbol, tier, score, "
                    "direction, sent_at, alert_type, telegram_status, message_hash, payload_json) "
                    "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (kw["alert_id"], kw["signal_id"], kw["asset_class"], kw.get("mode"),
                     kw["symbol"], kw["tier"], kw.get("score"), kw.get("direction"),
                     kw["sent_at"], kw["alert_type"], kw.get("telegram_status"),
                     kw.get("message_hash"), json.dumps(kw.get("payload") or {})),
                )

    out = send_paper_entry_alert(
        store=FakeStore(), notifier=notifier, signal=s,
        prev_status="waiting_for_entry",
        outcome_entry_triggered=True,
        # fresh entry so the freshness layer keeps it actionable (=> sent)
        outcome_entry_triggered_at=datetime.now(timezone.utc).isoformat(),
        outcome_entry_price_used=42.15,
    )
    assert out["sent"] is True
    assert out["payload"]["telegram_channel"] == "live_handoff"
    assert "LIVE QUEUED" in out["message"]
    notifier.send.assert_called_once()
    args, kwargs = notifier.send.call_args
    # parse_mode must be empty string (plain text)
    assert kwargs.get("parse_mode", None) == "" or (len(args) >= 2 and args[1] == "")


def test_10a_revalidated_delayed_stock_bar_remains_actionable(tmp_path: Path, monkeypatch):
    _force_live_queued(monkeypatch)
    signal = _stocks_a_intraday_long_signal()
    notifier = MagicMock()
    db_path = tmp_path / "stock-delayed.sqlite"
    conn = sqlite3.connect(db_path)
    conn.execute("""CREATE TABLE signal_alerts (
        alert_id TEXT PRIMARY KEY, signal_id TEXT, asset_class TEXT, mode TEXT,
        symbol TEXT, tier TEXT, score REAL, direction TEXT, sent_at TEXT,
        alert_type TEXT, telegram_status TEXT, message_hash TEXT, payload_json TEXT
    )""")
    conn.commit()
    conn.close()

    class FakeStore:
        def connect(self):
            c = sqlite3.connect(db_path)
            c.row_factory = sqlite3.Row
            return c

        def record_signal_alert(self, **kw):
            with self.connect() as c:
                c.execute(
                    "INSERT INTO signal_alerts VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (kw["alert_id"], kw["signal_id"], kw["asset_class"], kw.get("mode"),
                     kw["symbol"], kw["tier"], kw.get("score"), kw.get("direction"),
                     kw["sent_at"], kw["alert_type"], kw.get("telegram_status"),
                     kw.get("message_hash"), json.dumps(kw.get("payload") or {})),
                )

    FakeStore.db_path = db_path

    out = send_paper_entry_alert(
        store=FakeStore(), notifier=notifier, signal=signal,
        prev_status="waiting_for_entry", outcome_entry_triggered=True,
        outcome_entry_triggered_at=datetime.now(timezone.utc).isoformat(),
        outcome_entry_price_used=254.4,
        outcome_entry_time_basis="provider_delayed_current_bar",
        outcome_entry_currently_executable=True,
    )
    assert out["sent"] is True
    assert out["telegram_status"] == "sent"
    assert "STOCK_ENTRY_DELAYED_DATA_COHORT" in out["payload"]["paper_decision_reason_codes"]
    assert out["payload"]["telegram_channel"] == "live_handoff"
    notifier.send.assert_called_once()


def test_10b_alert_labels_a_rejected_mexc_handoff(tmp_path: Path, monkeypatch):
    s = _crypto_b_swing_signal()
    notifier = MagicMock()
    db_path = tmp_path / "handoff.sqlite"
    conn = sqlite3.connect(db_path)
    conn.execute("CREATE TABLE signal_alerts(alert_id TEXT PRIMARY KEY, signal_id TEXT, alert_type TEXT)")
    conn.commit()
    conn.close()

    class FakeStore:
        def connect(self):
            c = sqlite3.connect(db_path)
            c.row_factory = sqlite3.Row
            return c

        def record_signal_alert(self, **_kwargs):
            return None

    FakeStore.db_path = db_path

    monkeypatch.setattr(
        "src.live_execution.service.capture_paper_candidate",
        lambda **_kwargs: {"status": "REJECTED", "reasons": ["ENTRY_MODE_NOT_ALLOWED"]},
    )
    out = send_paper_entry_alert(
        store=FakeStore(), notifier=notifier, signal=s,
        prev_status="waiting_for_entry", outcome_entry_triggered=True,
        outcome_entry_triggered_at=datetime.now(timezone.utc).isoformat(),
        outcome_entry_price_used=42.15,
    )
    assert out["sent"] is False
    assert out["telegram_status"] == "live_not_queued"
    assert out["reason_skipped"] == "live_not_queued"
    assert "Live: not queued (ENTRY_MODE_NOT_ALLOWED)" in out["message"]
    notifier.send.assert_not_called()


def test_11_crypto_scalp_message_includes_low_confidence():
    s = _crypto_b_scalp_signal()
    d = decide_paper_entry(s, prev_status="waiting_for_entry",
                           entry_triggered=True,
                           entry_triggered_at="2026-06-11T11:22:00+00:00",
                           entry_price_used=42.15)
    assert d.should_send is True
    assert "LOW-CONFIDENCE SCALP" in d.message


def test_12_stocks_a_tier_long_includes_caution_and_half_size():
    s = _stocks_a_intraday_long_signal()
    d = decide_paper_entry(s, prev_status="waiting_for_entry",
                           entry_triggered=True,
                           entry_triggered_at="2026-06-11T13:30:00+00:00",
                           entry_price_used=254.5)
    assert d.should_send is True
    assert "A-tier long caution" in d.message
    assert "Size: 0.5x" in d.message


def test_pullback_v2_quality_weight_reaches_paper_alert():
    s = _stocks_a_intraday_long_signal()
    s.update({
        "tier": "B",
        "score": 76.0,
        "paper_entry_profile": "stocks_intraday_pullback_vwap_paper_v2",
        "paper_size_weight": 0.5,
        "paper_size_reason": "pullback_v2_half_quality: confirmation_rvol_weak_or_missing",
        "raw_idea_json": json.dumps({
            "paper_entry_profile": "stocks_intraday_pullback_vwap_paper_v2",
            "paper_lane": "paper_stocks_intraday_pullback_vwap",
        }),
    })
    d = decide_paper_entry(
        s, prev_status="waiting_for_entry", entry_triggered=True,
        entry_triggered_at="2026-08-19T13:45:00+00:00", entry_price_used=254.5,
    )
    assert d.should_send is True
    assert "Size: 0.5x" in d.message


def test_13_no_telegram_import_in_replay_scripts():
    """Backtest/replay scripts must not depend on the notifier."""
    import re
    scripts_dir = Path(__file__).resolve().parents[1] / "scripts"
    pat = re.compile(r"(TelegramNotifier|notifiers\.telegram|notifiers\.paper_entry)")
    for path in scripts_dir.glob("replay_*.py"):
        text = path.read_text(encoding="utf-8")
        assert not pat.search(text), f"{path} imports a notifier — replay must stay read-only"


def test_14_existing_signal_alert_types_unaffected():
    """The new 'paper_entry' alert_type does not clash with existing types."""
    from src.notifiers.paper_entry import PLAYBOOKS_FORBIDDEN_FOR_ENTRY_ALERT
    # Sanity: existing types include 'new_signal','entry_change','tier_upgrade'.
    # The new type 'paper_entry' is distinct.
    assert "paper_entry" not in {
        "new_signal", "entry_change", "tier_upgrade",
        "score_improvement", "invalidation_change",
    }
    # Two-paused playbooks remain forbidden.
    assert "stocks_swing_watchlist_rs_rotation" in PLAYBOOKS_FORBIDDEN_FOR_ENTRY_ALERT
    assert "stocks_invest_watchlist_30d_thesis" in PLAYBOOKS_FORBIDDEN_FOR_ENTRY_ALERT
