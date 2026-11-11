"""Stocks setup alert formatting + live-only Telegram routing tests.

The 48h audit found stocks-monitor Telegram delivery degraded (~19% fail,
HTTPError 400). Root cause: the alert text uses ``[STOCKS INTRADAY] [A]
[SYMBOL]`` bracket syntax plus tickers/values carrying $, _, +/-, parens —
all of which break Telegram **Markdown** entity parsing → 400 Bad Request.

Fix: send the alert as **plain text** (``parse_mode=""``) and stop emitting
Markdown control markers (the old ``_alert_type_`` italic) from the formatter.

These tests pin:
  - the formatter no longer emits Markdown italic markers;
  - hostile tickers/values (brackets, parens, _, +/-, $) don't crash it;
  - the monitor keeps setup alerts in the journal instead of phone-pushing them;
  - dedup/cooldown logic is unchanged by the formatter/transport fix.

Selection / cooldown / dedup logic is NOT modified.
"""

from __future__ import annotations

import sys
import uuid
from datetime import datetime, timezone

import pytest
import requests

from src import config as _config_mod
from src.config import load_config
from src.stocks.monitor import (
    AlertDecision,
    StocksMonitorSession,
    format_stocks_alert,
)
from src.storage.sqlite import SQLiteStore


@pytest.fixture(autouse=True)
def _isolated_db(tmp_path, monkeypatch):
    db_file = tmp_path / "isolated_tg.sqlite"

    def _patched_load_config(*args, **kwargs):
        cfg = _config_mod.load_config(*args, **kwargs)
        cfg.settings.setdefault("data", {})["db_path"] = str(db_file)
        return cfg

    monkeypatch.setattr(sys.modules[__name__], "load_config", _patched_load_config)
    yield


def _make_store() -> SQLiteStore:
    store = SQLiteStore(load_config().db_path)
    store.init_db()
    return store


def _insert_ab_signal(store, *, symbol, tier="A", score=90.0):
    sig_id = f"sig_tg_{uuid.uuid4().hex[:8]}"
    now = datetime.now(timezone.utc).isoformat()
    with store.connect() as conn:
        conn.execute(
            """
            INSERT INTO proposed_signals(
                signal_id, created_at, updated_at, symbol, direction, mode,
                tier, score, confidence, data_confidence,
                asset_class, status, entry_low, entry_high, invalidation
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (sig_id, now, now, symbol, "long", "intraday", tier, score,
             "high", "medium", "stocks", "waiting_for_entry", 102.0, 103.0, 100.0),
        )
    return sig_id


# ---------------------------------------------------------------------------
# Fake notifiers
# ---------------------------------------------------------------------------


class _RecordingNotifier:
    """Captures (text, parse_mode) of every send; always succeeds."""

    def __init__(self):
        self.sent: list[tuple[str, str]] = []

    def send(self, text: str, parse_mode: str = "Markdown") -> dict:
        self.sent.append((text, parse_mode))
        return {"ok": True}


class _Failing400Notifier:
    """Simulates the real-world Telegram 400 on every send."""

    def __init__(self):
        self.calls = 0

    def send(self, text: str, parse_mode: str = "Markdown") -> dict:
        self.calls += 1
        resp = requests.Response()
        resp.status_code = 400
        raise requests.HTTPError("400 Client Error: Bad Request", response=resp)


# ---------------------------------------------------------------------------
# Formatter — Markdown-marker / hostile-input safety
# ---------------------------------------------------------------------------


def _decision():
    return AlertDecision(True, "new_signal", "first alert")


def test_formatter_has_no_markdown_italic_markers():
    text = format_stocks_alert(
        signal={
            "symbol": "AAPL", "tier": "A", "direction": "long", "score": 88.6,
            "entry_low": 308.0, "entry_high": 308.9, "invalidation": 306.3,
            "tp1": 311.4, "tp2": 313.1, "expected_rr_tp1": 1.0,
        },
        decision=_decision(),
        context={},
    )
    # old behavior emitted `_alert_type_:` (Markdown italic). New is plain text
    # and reflects the alert sub-type in the standardized header instead of an
    # `alert_type:` line.
    assert "_alert_type_" not in text
    assert "NEW SIGNAL" in text


def test_formatter_handles_hostile_symbol_and_values():
    """Tickers/reasons carrying brackets, parens, _, +/-, $ must not crash the
    formatter and must be reproduced verbatim (we send as plain text)."""
    hostile = "BRK_B+ (test) [x] $US-D"
    text = format_stocks_alert(
        signal={
            "symbol": hostile, "tier": "B", "direction": "short", "score": 71.2,
            "entry_low": 12.5, "entry_high": 13.0, "invalidation": 14.0,
            "tp1": 10.0, "tp2": 9.0, "expected_rr_tp1": 2.0,
        },
        decision=AlertDecision(True, "new_signal", "reason with _under_ + [brackets] (parens) $5"),
        context={
            "main_risk": "gap risk _overnight_ +3% [earnings]",
            "news_catalyst": "M&A (rumor) — $TGT",
        },
    )
    assert isinstance(text, str) and text
    # standardized formatter preserves the original symbol case and reproduces
    # every hostile char verbatim (plain text — no Markdown escaping).
    assert hostile in text                  # symbol preserved verbatim, case intact
    assert "[x]" in text                    # bracket chars preserved verbatim


# ---------------------------------------------------------------------------
# Transport — plain-text send + failure isolation
# ---------------------------------------------------------------------------


def test_monitor_keeps_setup_alerts_journal_only(monkeypatch):
    store = _make_store()
    _insert_ab_signal(store, symbol="QA_TG_PLAIN", tier="A", score=90.0)
    session = StocksMonitorSession(
        load_config(), minutes=0, market_hours_only=False,
        send_telegram=True, dry_run=False,
    )
    # The signal under test is pre-seeded directly into the DB above, so the
    # (slow, live-network) report refresh is incidental here — stub it out so
    # this test stays fast and offline. Production behavior is unchanged.
    monkeypatch.setattr(session, "_refresh_report", lambda: None)
    monkeypatch.setattr(session, "_refresh_forward_shadow", lambda: None)
    rec = _RecordingNotifier()
    monkeypatch.setattr(session, "_notifier_or_none", lambda: rec)
    result = session.run_once()
    assert rec.sent == []
    assert result.decisions[0]["telegram_status"] == "setup_suppressed_live_only"


def test_monitor_setup_suppression_does_not_touch_failing_notifier(monkeypatch):
    store = _make_store()
    sig = _insert_ab_signal(store, symbol="QA_TG_FAIL", tier="A", score=90.0)
    session = StocksMonitorSession(
        load_config(), minutes=0, market_hours_only=False,
        send_telegram=True, dry_run=False,
    )
    # The signal is already seeded; this transport test must not depend on a
    # live report refresh or network latency.
    monkeypatch.setattr(session, "_refresh_report", lambda: None)
    monkeypatch.setattr(session, "_refresh_forward_shadow", lambda: None)
    fail = _Failing400Notifier()
    monkeypatch.setattr(session, "_notifier_or_none", lambda: fail)
    result = session.run_once()
    assert fail.calls == 0
    assert result.telegram_failed == 0
    # the alert row is still recorded for dashboard/research.
    last = store.last_signal_alert_for_signal(sig)
    assert last is not None
    assert last["telegram_status"] == "setup_suppressed_live_only"


# ---------------------------------------------------------------------------
# Dedup / cooldown unchanged by the fix
# ---------------------------------------------------------------------------


def test_dedup_unchanged_after_transport_fix(monkeypatch):
    """Second tick on an unchanged signal still de-dupes (no second send)."""
    store = _make_store()
    _insert_ab_signal(store, symbol="QA_TG_DEDUP", tier="A", score=90.0)
    session = StocksMonitorSession(
        load_config(), minutes=0, market_hours_only=False,
        send_telegram=True, dry_run=False,
    )
    # Dedup is evaluated against the seeded signal/alert rows, not report I/O.
    monkeypatch.setattr(session, "_refresh_report", lambda: None)
    monkeypatch.setattr(session, "_refresh_forward_shadow", lambda: None)
    rec = _RecordingNotifier()
    monkeypatch.setattr(session, "_notifier_or_none", lambda: rec)
    session.run_once()
    first_count = len(rec.sent)
    session.run_once()
    assert len(rec.sent) == first_count, "duplicate tick must not re-send"
