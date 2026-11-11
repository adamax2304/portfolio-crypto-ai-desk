from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pandas as pd

from src.notifiers import trade_telegram
from src.notifiers.manual_paper_signal import (
    latest_closed_minute,
    render_manual_paper_close,
    render_manual_paper_entry,
    send_manual_paper_close,
    send_manual_paper_entry,
)
from src.notifiers.telegram_outbox import retry_pending
from src.storage.sqlite import SQLiteStore


UTC = timezone.utc


class _Notifier:
    def __init__(self, response=None):
        self.messages = []
        self.response = response or {"ok": True}

    def send_fast(self, text, parse_mode=""):
        self.messages.append((text, parse_mode))
        return self.response


def _args(tmp_path, *, now=None, entry_age=20, quote_age=10):
    now = now or datetime(2026, 10, 11, 12, 0, tzinfo=UTC)
    return {
        "root": tmp_path,
        "db_path": tmp_path / "alerts.sqlite",
        "signal_id": "manual-paper:test:event-1",
        "asset_class": "crypto",
        "symbol": "BTC/USDT",
        "direction": "long",
        "title": "Fast 1m Liquidity Reclaim · Paper",
        "entry_at": now - timedelta(seconds=entry_age),
        "reference_price": 101.25,
        "reference_at": now - timedelta(seconds=quote_age),
        "variants": [{"label": "FAST 1m", "entry": 101.0, "stop": 99.0,
                      "tp1": 102.6, "tp2": 103.7}],
        "now": now,
        "max_age_seconds": 90,
    }


def test_manual_paper_signal_sends_once_and_is_plain_manual_only(tmp_path, monkeypatch):
    store = SQLiteStore(tmp_path / "alerts.sqlite")
    store.init_db()
    notifier = _Notifier()
    monkeypatch.setattr(trade_telegram, "notifier_for", lambda _root: notifier)

    first = send_manual_paper_entry(**_args(tmp_path))
    duplicate = send_manual_paper_entry(**_args(tmp_path))

    assert first["sent"] is True
    assert duplicate["status"] == "duplicate"
    assert len(notifier.messages) == 1
    message, parse_mode = notifier.messages[0]
    assert parse_mode == ""
    assert "🟢 КРИПТА · PAPER СИГНАЛ" in message
    assert "Рынок ≈ $101.25 · 1m close 10с" in message
    assert "FAST 1m: вход $101" in message
    assert "стоп $99" in message
    assert "цели $102.6 / $103.7" in message
    assert "автоордер не отправлялся" in message
    with store.connect() as conn:
        assert conn.execute("SELECT COUNT(*) FROM signal_alerts").fetchone()[0] == 1
        assert conn.execute(
            "SELECT status FROM telegram_alert_outbox"
        ).fetchone()[0] == "sent"


def test_manual_paper_close_sends_once_with_outcome_and_is_plain_text(tmp_path, monkeypatch):
    store = SQLiteStore(tmp_path / "alerts.sqlite")
    store.init_db()
    notifier = _Notifier()
    monkeypatch.setattr(trade_telegram, "notifier_for", lambda _root: notifier)
    args = {
        "root": tmp_path,
        "db_path": tmp_path / "alerts.sqlite",
        "signal_id": "manual-paper:stocks:event-1",
        "asset_class": "stocks",
        "symbol": "PANW",
        "direction": "long",
        "title": "Liquidity Shock Reclaim · Paper",
        "variants": [{
            "label": "Стандарт", "outcome_status": "closed",
            "close_reason": "original_stop", "net_pnl_usd": -10.9,
            "net_r": -1.09, "exit_price": 403.33,
        }, {
            "label": "Структурные цели", "outcome_status": "closed",
            "close_reason": "tp2", "net_pnl_usd": 6.75,
            "net_r": 0.67, "exit_price": 413.20,
        }, {
            "label": "Защита", "outcome_status": "closed",
            "close_reason": "breakeven_stop", "highest_tp_touched": 1,
            "net_pnl_usd": 4.53, "net_r": 0.45, "exit_price": 10.49,
        }],
        "now": datetime(2026, 10, 12, 15, 30, tzinfo=UTC),
    }

    first = send_manual_paper_close(**args)
    duplicate = send_manual_paper_close(**args)

    assert first["sent"] is True
    assert duplicate["status"] == "duplicate"
    assert len(notifier.messages) == 1
    message, parse_mode = notifier.messages[0]
    assert parse_mode == ""
    assert "📊 PAPER · ИТОГ СДЕЛКИ · АКЦИИ" in message
    assert "Стандарт: СТОП · -1.09R · -10.90 USD · выход $403.33" in message
    assert "Структурные цели: TP2 · +0.67R · +6.75 USD" in message
    assert "Защита: TP1 · ЗАЩИТА · BE · +0.45R" in message
    assert "не реальные ордера" in message
    with store.connect() as conn:
        assert conn.execute(
            "SELECT alert_type,telegram_status FROM signal_alerts"
        ).fetchone()[:] == ("manual_paper_close", "sent")
        assert conn.execute(
            "SELECT status FROM telegram_alert_outbox"
        ).fetchone()[0] == "sent"


def test_manual_paper_close_rejects_unclosed_or_invalid_outcome(tmp_path, monkeypatch):
    notifier = _Notifier()
    monkeypatch.setattr(trade_telegram, "notifier_for", lambda _root: notifier)
    args = {
        "root": tmp_path,
        "db_path": tmp_path / "alerts.sqlite",
        "signal_id": "manual-paper:crypto:candidate-1",
        "asset_class": "crypto", "symbol": "BTC/USDT", "direction": "long",
        "title": "Fast 1m Liquidity Reclaim · Paper",
        "variants": [{"label": "FAST", "outcome_status": "open",
                      "net_pnl_usd": 0, "net_r": 0}],
        "now": datetime(2026, 10, 12, 15, 30, tzinfo=UTC),
    }

    result = send_manual_paper_close(**args)

    assert result["status"] == "outcome_not_closed"
    assert notifier.messages == []


def test_stale_entry_or_quote_is_suppressed_without_outbox_row(tmp_path, monkeypatch):
    store = SQLiteStore(tmp_path / "alerts.sqlite")
    store.init_db()
    notifier = _Notifier()
    monkeypatch.setattr(trade_telegram, "notifier_for", lambda _root: notifier)

    result = send_manual_paper_entry(**_args(tmp_path, quote_age=91))

    assert result["status"] == "stale"
    assert notifier.messages == []
    with store.connect() as conn:
        assert conn.execute("SELECT COUNT(*) FROM signal_alerts").fetchone()[0] == 0


def test_telegram_rejection_is_queued_for_outbox_retry(tmp_path, monkeypatch):
    store = SQLiteStore(tmp_path / "alerts.sqlite")
    store.init_db()
    notifier = _Notifier({"ok": False})
    monkeypatch.setattr(trade_telegram, "notifier_for", lambda _root: notifier)

    result = send_manual_paper_entry(**_args(tmp_path))

    assert result["status"] == "queued:RuntimeError"
    with store.connect() as conn:
        row = conn.execute(
            "SELECT status,attempts,last_error FROM telegram_alert_outbox"
        ).fetchone()
        assert row["status"] == "pending"
        assert row["attempts"] == 1
        assert row["last_error"] == "RuntimeError"


def test_manual_signal_retry_expires_instead_of_sending_stale_entry(tmp_path, monkeypatch):
    store = SQLiteStore(tmp_path / "alerts.sqlite")
    store.init_db()
    first_notifier = _Notifier({"ok": False})
    monkeypatch.setattr(trade_telegram, "notifier_for", lambda _root: first_notifier)
    now = datetime.now(UTC)
    result = send_manual_paper_entry(**_args(
        tmp_path, now=now, entry_age=0, quote_age=0,
    ))
    assert result["status"] == "queued:RuntimeError"

    retry_notifier = _Notifier()
    retry = retry_pending(store, retry_notifier, now=now + timedelta(seconds=91))

    assert retry == {"due": 1, "sent": 0, "failed": 0, "dead": 1}
    assert retry_notifier.messages == []
    with store.connect() as conn:
        assert conn.execute(
            "SELECT status,last_error FROM telegram_alert_outbox"
        ).fetchone()[:] == ("dead", "manual_signal_expired")
        assert conn.execute(
            "SELECT telegram_status FROM signal_alerts"
        ).fetchone()[0] == "expired"


def test_reference_price_uses_latest_closed_one_minute_bar_only():
    now = datetime(2026, 10, 11, 12, 2, 30, tzinfo=UTC)
    frame = pd.DataFrame([
        {"timestamp": now - timedelta(minutes=2), "close": 100.0},
        {"timestamp": now, "close": 999.0},
        {"timestamp": now - timedelta(minutes=1), "close": 101.0},
    ])

    quote = latest_closed_minute(frame, now=now)

    assert quote == (101.0, now)


def test_compact_stock_message_can_carry_three_distinct_risk_plans():
    now = datetime(2026, 10, 11, 12, 0, tzinfo=UTC)
    message = render_manual_paper_entry(
        asset_class="stocks", symbol="LRCX", direction="long",
        title="Liquidity Shock Reclaim · Paper", reference_price=100.5,
        reference_at=now - timedelta(seconds=15), now=now,
        variants=[
            {"label": "Стандарт", "entry": 100.0, "stop": 99.0, "tp1": 101.0, "tp2": 102.0},
            {"label": "Структура", "entry": 100.0, "stop": 98.8, "tp1": 101.2, "tp2": 102.5},
            {"label": "Стоп шире", "entry": 100.0, "stop": 98.5, "tp1": 101.5, "tp2": 103.0},
        ],
    )

    assert "LRCX · LONG" in message
    assert message.count("вход") == 3
    assert "1m close 15с" in message
    assert len(message) < 600


def test_only_requested_stock_and_crypto_profiles_are_telegram_enabled():
    from src.execution import (
        crypto_fast_flush_reclaim_paper as crypto_strategy,
        stocks_liquidity_shock_reclaim_paper as stock_strategy,
    )

    stock_alerts = stock_strategy.load_strategy_config()["manual_telegram_signals"]
    crypto_alerts = crypto_strategy.load_strategy_config()["manual_telegram_signals"]

    assert stock_alerts["enabled"] is True
    assert set(stock_alerts["profile_ids"]) == {
        "stocks_liquidity_shock_held_1m_structure_targets_paper_v1",
    }
    assert crypto_alerts == {
        "enabled": True,
        "max_age_seconds": 90,
        "profile_ids": [
            "crypto_fast_flush_reclaim_fast_1m_paper_v3",
            "crypto_fast_flush_reclaim_asia_1m_paper_v1",
            "crypto_fast_flush_reclaim_europe_1m_paper_v1",
        ],
        "profile_labels": {
            "crypto_fast_flush_reclaim_fast_1m_paper_v3": "FAST 1m - America (US)",
            "crypto_fast_flush_reclaim_asia_1m_paper_v1": "FAST 1m - Asia",
            "crypto_fast_flush_reclaim_europe_1m_paper_v1": "FAST 1m - Europe",
        },
    }
