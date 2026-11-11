"""Tests for the Stocks Intraday Monitor + signal_alerts ledger.

Covers the contract laid out in the spec:
  - registered signal with alert_sent=false sends alert;
  - already alerted same signal does not resend;
  - B→A tier upgrade sends update alert;
  - score improvement threshold sends update alert;
  - C-tier does not alert;
  - signal missing invalidation does not alert;
  - crypto alert behavior is unchanged (no rows written to the legacy
    watchlist_alerts table by the stocks monitor).
"""

from __future__ import annotations

import sqlite3
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

import pytest

from src import config as _config_mod
from src.config import load_config
from src.stocks.monitor import (
    DEFAULT_SCORE_IMPROVEMENT,
    AlertDecision,
    MaterialImprovementChecker,
    StocksMonitorSession,
    format_stocks_alert,
)
from src.storage.sqlite import SQLiteStore


@pytest.fixture(autouse=True)
def _isolated_db(tmp_path, monkeypatch):
    """Test-isolation fix (2026-06-03): route every ``load_config()`` in this
    module to a fresh per-test temp SQLite DB.

    Both the helper store (``_make_store``) and the ``StocksMonitorSession``
    (which opens ``SQLiteStore(config.db_path)`` internally) then share one
    EMPTY database, so cooldown / dedup state is deterministic and the live
    production DB (``db/crypto_ai_desk.sqlite``) is never read or written.

    Pure fixture-level dependency injection — no production code is changed and
    no production data is touched. ``cfg.db_path`` resolves
    ``self.root / settings['data']['db_path']``; an absolute temp path on the
    right-hand side wins, so this cleanly redirects the store location.
    """
    db_file = tmp_path / "isolated_monitor.sqlite"

    def _patched_load_config(*args, **kwargs):
        cfg = _config_mod.load_config(*args, **kwargs)
        cfg.settings.setdefault("data", {})["db_path"] = str(db_file)
        return cfg

    monkeypatch.setattr(sys.modules[__name__], "load_config", _patched_load_config)
    yield


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_store() -> SQLiteStore:
    config = load_config()
    store = SQLiteStore(config.db_path)
    store.init_db()
    return store


def _insert_ab_signal(
    store: SQLiteStore,
    *,
    symbol: str,
    tier: str = "B",
    score: float = 72.0,
    direction: str = "long",
    asset_class: str = "stocks",
    mode: str = "intraday",
    status: str = "waiting_for_entry",
    invalidation: float | None = 100.0,
    entry_low: float = 102.0,
    entry_high: float = 103.0,
) -> str:
    sig_id = f"sig_test_{asset_class}_{uuid.uuid4().hex[:8]}"
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
            (
                sig_id, now, now, symbol, direction, mode, tier, score,
                "high", "medium", asset_class, status,
                entry_low, entry_high, invalidation,
            ),
        )
    return sig_id


def _cleanup(store: SQLiteStore, signal_ids: list[str]) -> None:
    if not signal_ids:
        return
    qmarks = ",".join("?" for _ in signal_ids)
    with store.connect() as conn:
        conn.execute(
            f"DELETE FROM signal_alerts WHERE signal_id IN ({qmarks})",
            tuple(signal_ids),
        )
        conn.execute(
            f"DELETE FROM proposed_signals WHERE signal_id IN ({qmarks})",
            tuple(signal_ids),
        )


# ---------------------------------------------------------------------------
# MaterialImprovementChecker — pure logic, no I/O
# ---------------------------------------------------------------------------


def test_decide_sends_new_signal_when_no_prior_alert():
    checker = MaterialImprovementChecker()
    decision = checker.decide(
        current={"tier": "B", "invalidation": 100.0, "score": 75.0},
        last_alert=None,
    )
    assert decision.should_send is True
    assert decision.alert_type == "new_signal"


def test_decide_skips_when_already_alerted_no_change():
    checker = MaterialImprovementChecker()
    current = {
        "tier": "B", "invalidation": 100.0, "score": 75.0,
        "entry_low": 102.0, "entry_high": 103.0,
    }
    last_alert = {
        "tier": "B", "score": 75.0,
        "payload_json": '{"entry_low": 102.0, "entry_high": 103.0, "invalidation": 100.0}',
    }
    decision = checker.decide(current=current, last_alert=last_alert)
    assert decision.should_send is False
    assert decision.alert_type == "duplicate"


def test_decide_tier_upgrade_B_to_A_sends_update():
    checker = MaterialImprovementChecker()
    decision = checker.decide(
        current={"tier": "A", "invalidation": 100.0, "score": 82.0},
        last_alert={
            "tier": "B", "score": 75.0,
            "payload_json": '{"invalidation": 100.0}',
        },
    )
    assert decision.should_send is True
    assert decision.alert_type == "tier_upgrade"


def test_decide_score_improvement_threshold_sends_update():
    checker = MaterialImprovementChecker(score_threshold=5.0)
    decision = checker.decide(
        current={"tier": "B", "invalidation": 100.0, "score": 81.0},
        last_alert={
            "tier": "B", "score": 75.0,
            "payload_json": '{"invalidation": 100.0}',
        },
    )
    assert decision.should_send is True
    assert decision.alert_type == "score_improvement"


def test_decide_below_score_threshold_no_alert():
    checker = MaterialImprovementChecker(score_threshold=5.0)
    decision = checker.decide(
        current={"tier": "B", "invalidation": 100.0, "score": 77.0},
        last_alert={
            "tier": "B", "score": 75.0,
            "payload_json": '{"invalidation": 100.0}',
        },
    )
    assert decision.should_send is False
    assert decision.alert_type == "duplicate"


def test_decide_C_tier_never_alerts():
    checker = MaterialImprovementChecker()
    decision = checker.decide(
        current={"tier": "C", "invalidation": 100.0, "score": 60.0},
        last_alert=None,
    )
    assert decision.should_send is False


def test_decide_missing_invalidation_rejects_alert():
    checker = MaterialImprovementChecker()
    decision = checker.decide(
        current={"tier": "A", "invalidation": None, "score": 90.0},
        last_alert=None,
    )
    assert decision.should_send is False
    assert "invalidation" in decision.reason


def test_decide_entry_zone_change_sends_update():
    checker = MaterialImprovementChecker(entry_change_pct=0.5)
    decision = checker.decide(
        current={
            "tier": "B", "invalidation": 100.0, "score": 75.0,
            "entry_low": 102.0, "entry_high": 103.0,
        },
        last_alert={
            "tier": "B", "score": 75.0,
            "payload_json": '{"entry_low": 110.0, "entry_high": 111.0, "invalidation": 100.0}',
        },
    )
    assert decision.should_send is True
    assert decision.alert_type == "entry_change"


def test_decide_invalidation_change_sends_update():
    checker = MaterialImprovementChecker(invalidation_change_pct=0.5)
    decision = checker.decide(
        current={"tier": "B", "invalidation": 95.0, "score": 75.0},
        last_alert={
            "tier": "B", "score": 75.0,
            "payload_json": '{"invalidation": 100.0}',
        },
    )
    assert decision.should_send is True
    assert decision.alert_type == "invalidation_change"


# ---------------------------------------------------------------------------
# Alert formatter
# ---------------------------------------------------------------------------


def test_format_stocks_alert_contains_required_sections():
    text = format_stocks_alert(
        signal={
            "symbol": "AAPL", "tier": "A", "direction": "long",
            "score": 88.64, "confidence": "high", "data_confidence": "medium",
            "entry_low": 308.04, "entry_high": 308.88, "invalidation": 306.35,
            "tp1": 311.41, "tp2": 313.10, "expected_rr_tp1": 1.0,
        },
        decision=AlertDecision(True, "new_signal", "first alert"),
        context={"regime": "bullish", "sector_confirmation": "tech leading"},
    )
    # 2026-06-14 standardized SETUP — WAITING FOR ENTRY template
    # (src/notifiers/setup_alert.py). The header carries the asset/sub-type,
    # the second line carries asset/symbol/direction, and tier+score, entry,
    # stop (invalidation), TP, why and status are dedicated sections.
    for line in (
        "STOCKS SETUP",          # standardized header prefix
        "NEW SIGNAL",            # alert sub-type reflected in the header
        "STOCKS AAPL LONG",      # asset / symbol / direction
        "Tier/Score: A / 88.64",
        "Entry:",
        "Stop:",                 # invalidation / stop level
        "TP:",
        "Why:",
        "Status:",
    ):
        assert line in text, f"missing '{line}' in alert text"


# ---------------------------------------------------------------------------
# Monitor session — integration with live SQLite
# ---------------------------------------------------------------------------


def test_session_sends_alert_for_new_ab_signal_then_skips_duplicate():
    """Insert one A-tier signal. First tick must record exactly one
    'new_signal' alert. Second tick on unchanged signal must record no
    new alert (duplicate)."""
    store = _make_store()
    inserted: list[str] = []
    try:
        sig = _insert_ab_signal(
            store, symbol="QA_MON_NEW", tier="A", score=90.0
        )
        inserted.append(sig)
        config = load_config()
        session = StocksMonitorSession(
            config,
            minutes=0,
            market_hours_only=False,
            send_telegram=False,
            dry_run=True,
        )
        tick1 = session.run_once()
        new1 = [d for d in tick1.decisions if d.get("action") == "alert"]
        assert any(d.get("symbol") == "QA_MON_NEW" for d in new1), (
            f"first tick should alert; decisions={tick1.decisions}"
        )
        last = store.last_signal_alert_for_signal(sig)
        assert last is not None
        assert last["alert_type"] == "new_signal"
        assert last["telegram_status"] == "dry_run"

        tick2 = session.run_once()
        alerts2 = [d for d in tick2.decisions if d.get("action") == "alert"
                   and d.get("symbol") == "QA_MON_NEW"]
        assert not alerts2, "second tick must not re-alert the same signal"
    finally:
        _cleanup(store, inserted)


def test_session_c_tier_does_not_alert():
    store = _make_store()
    inserted: list[str] = []
    try:
        sig = _insert_ab_signal(
            store, symbol="QA_MON_C", tier="C", score=60.0
        )
        inserted.append(sig)
        config = load_config()
        session = StocksMonitorSession(
            config,
            minutes=0,
            market_hours_only=False,
            send_telegram=False,
            dry_run=True,
        )
        tick = session.run_once()
        alerts = [d for d in tick.decisions
                  if d.get("action") == "alert" and d.get("symbol") == "QA_MON_C"]
        assert not alerts
        # Also: nothing should land in signal_alerts.
        last = store.last_signal_alert_for_signal(sig)
        assert last is None
    finally:
        _cleanup(store, inserted)


def test_session_b_to_a_upgrade_sends_update_alert():
    store = _make_store()
    inserted: list[str] = []
    try:
        sig = _insert_ab_signal(
            store, symbol="QA_MON_UP", tier="B", score=75.0
        )
        inserted.append(sig)
        config = load_config()
        session = StocksMonitorSession(
            config,
            minutes=0,
            market_hours_only=False,
            send_telegram=False,
            dry_run=True,
        )
        session.run_once()
        # Promote to A-tier.
        with store.connect() as conn:
            conn.execute(
                "UPDATE proposed_signals SET tier = 'A', score = 85.0 "
                "WHERE signal_id = ?",
                (sig,),
            )
        tick2 = session.run_once()
        upgrade = [
            d for d in tick2.decisions
            if d.get("symbol") == "QA_MON_UP" and d.get("action") == "alert"
        ]
        assert upgrade, f"expected upgrade alert; decisions={tick2.decisions}"
        assert upgrade[0]["alert_type"] == "tier_upgrade"
    finally:
        _cleanup(store, inserted)


def test_session_score_improvement_sends_update_alert():
    store = _make_store()
    inserted: list[str] = []
    try:
        sig = _insert_ab_signal(
            store, symbol="QA_MON_SCORE", tier="B", score=70.0
        )
        inserted.append(sig)
        config = load_config()
        session = StocksMonitorSession(
            config,
            minutes=0,
            market_hours_only=False,
            send_telegram=False,
            dry_run=True,
            score_improvement=DEFAULT_SCORE_IMPROVEMENT,
            # PART 2 fix: this test pins the score_improvement classification.
            # The new 45-min cooldown is exercised in
            # tests/test_stocks_monitor_cooldown.py — disable it here so the
            # two run_once() calls (a few ms apart) can both reach the
            # checker.
            cooldown_minutes=0.0,
        )
        session.run_once()
        # +6 score is above the default 5-point threshold.
        with store.connect() as conn:
            conn.execute(
                "UPDATE proposed_signals SET score = 76.0 WHERE signal_id = ?",
                (sig,),
            )
        tick2 = session.run_once()
        upgrades = [
            d for d in tick2.decisions
            if d.get("symbol") == "QA_MON_SCORE" and d.get("action") == "alert"
        ]
        assert upgrades
        assert upgrades[0]["alert_type"] == "score_improvement"
    finally:
        _cleanup(store, inserted)


def test_session_missing_invalidation_blocks_alert():
    store = _make_store()
    inserted: list[str] = []
    try:
        sig = _insert_ab_signal(
            store, symbol="QA_MON_NOINV", tier="A", score=90.0,
            invalidation=None,
        )
        inserted.append(sig)
        config = load_config()
        session = StocksMonitorSession(
            config,
            minutes=0,
            market_hours_only=False,
            send_telegram=False,
            dry_run=True,
        )
        tick = session.run_once()
        assert tick.skipped_no_invalidation >= 1
        last = store.last_signal_alert_for_signal(sig)
        assert last is None
    finally:
        _cleanup(store, inserted)


def test_session_does_not_touch_watchlist_alerts_table():
    """Crypto's legacy alert log must remain untouched by the stocks
    monitor. Otherwise the crypto cooldown logic could mis-fire."""
    store = _make_store()
    inserted: list[str] = []
    with store.connect() as conn:
        before_row = conn.execute(
            "SELECT COUNT(*) AS n FROM watchlist_alerts"
        ).fetchone()
    before = int(before_row["n"]) if before_row else 0
    try:
        sig = _insert_ab_signal(store, symbol="QA_MON_ISOL", tier="A", score=90.0)
        inserted.append(sig)
        config = load_config()
        session = StocksMonitorSession(
            config,
            minutes=0,
            market_hours_only=False,
            send_telegram=False,
            dry_run=True,
        )
        session.run_once()
    finally:
        _cleanup(store, inserted)
    with store.connect() as conn:
        after_row = conn.execute(
            "SELECT COUNT(*) AS n FROM watchlist_alerts"
        ).fetchone()
    after = int(after_row["n"]) if after_row else 0
    assert before == after, (
        "stocks monitor must not write to watchlist_alerts (crypto-only table)"
    )


def test_session_records_dry_run_status_when_telegram_disabled():
    store = _make_store()
    inserted: list[str] = []
    try:
        sig = _insert_ab_signal(
            store, symbol="QA_MON_DRY", tier="A", score=91.0
        )
        inserted.append(sig)
        config = load_config()
        session = StocksMonitorSession(
            config,
            minutes=0,
            market_hours_only=False,
            send_telegram=False,
            dry_run=True,
        )
        session.run_once()
        last = store.last_signal_alert_for_signal(sig)
        assert last is not None
        assert last["telegram_status"] == "dry_run"
    finally:
        _cleanup(store, inserted)


# ---------------------------------------------------------------------------
# alert-status helper
# ---------------------------------------------------------------------------


def test_alert_status_summary_counts_stocks_ab_and_alerts():
    store = _make_store()
    inserted: list[str] = []
    try:
        # Insert one A-tier and one B-tier stocks signal.
        sig_a = _insert_ab_signal(store, symbol="QA_STATUS_A", tier="A", score=88.0)
        sig_b = _insert_ab_signal(store, symbol="QA_STATUS_B", tier="B", score=72.0)
        inserted.extend([sig_a, sig_b])

        config = load_config()
        session = StocksMonitorSession(
            config,
            minutes=0,
            market_hours_only=False,
            send_telegram=False,
            dry_run=True,
        )
        session.run_once()

        summary = store.alert_status_summary(asset_class="stocks")
        assert summary["ab_signals_total"] >= 2
        assert summary["alerts_sent_total"] >= 2
        # Both signals should have at least one alert row.
        assert summary["ab_alerted"] >= 2
    finally:
        _cleanup(store, inserted)


# ---------------------------------------------------------------------------
# Smoke: CLI command exposes correct options
# ---------------------------------------------------------------------------


def test_cli_stocks_monitor_session_command_exposes_options():
    import inspect

    from src.cli import app

    cmd = next(
        (c for c in app.registered_commands if c.name == "stocks-monitor-session"),
        None,
    )
    assert cmd is not None, "stocks-monitor-session command not registered"
    sig = inspect.signature(cmd.callback)
    expected = {
        "minutes",
        "interval_minutes",
        "market_hours_only",
        "send_telegram",
        "dry_run",
    }
    assert expected.issubset(set(sig.parameters)), (
        f"missing options: {expected - set(sig.parameters)}"
    )


def test_session_runs_fast_pending_lane_every_tick_but_full_report_on_slow_cadence(monkeypatch):
    from types import SimpleNamespace

    session = StocksMonitorSession(
        load_config(), minutes=0, interval_minutes=1, report_refresh_minutes=10,
        market_hours_only=False, send_telegram=False, dry_run=False,
        background_report_refresh=False,
    )
    calls = {"report": 0, "shadow": 0, "refresh": 0, "track": 0}
    order = []

    def _report():
        calls["report"] += 1
        order.append("report")

    def _shadow():
        calls["shadow"] += 1
        order.append("shadow")

    monkeypatch.setattr(session, "_refresh_report", _report)
    monkeypatch.setattr(session, "_refresh_forward_shadow", _shadow)

    def _refresh(_signal_ids=None):
        calls["refresh"] += 1
        order.append("refresh")
        return {"attempted": 2, "fetched": 2, "failed": 0}

    def _track(notifier, _signal_ids=None):
        calls["track"] += 1
        order.append("track")
        return SimpleNamespace(checked=3, tp_hits=1, stopped=0)

    monkeypatch.setattr(session, "_refresh_pending_ohlcv", _refresh)
    monkeypatch.setattr(session, "_track_pending_entries", _track)
    monkeypatch.setattr(session, "_load_active_ab", lambda: [])

    first = session.run_once()
    second = session.run_once()

    assert calls == {"report": 1, "shadow": 1, "refresh": 2, "track": 2}
    assert order == ["refresh", "track", "report", "shadow", "refresh", "track"]
    assert first.report_refreshed is True and second.report_refreshed is False
    assert first.pending_checked == 3 and second.pending_checked == 3
    assert first.pending_symbols_refreshed == 2 and second.pending_symbols_refreshed == 2


def test_slow_report_runs_in_background_without_blocking_pending_lane(monkeypatch):
    from threading import Event
    from types import SimpleNamespace

    session = StocksMonitorSession(
        load_config(), minutes=0, interval_minutes=1, report_refresh_minutes=10,
        market_hours_only=False, send_telegram=False, dry_run=False,
        background_report_refresh=True,
    )
    started = Event()
    release = Event()

    def _slow_report():
        started.set()
        assert release.wait(5)

    monkeypatch.setattr(session, "_refresh_report", _slow_report)
    monkeypatch.setattr(
        session, "_refresh_pending_ohlcv",
        lambda _signal_ids=None: {"attempted": 1, "fetched": 1, "failed": 0})
    monkeypatch.setattr(
        session, "_track_pending_entries",
        lambda notifier, _signal_ids=None: SimpleNamespace(
            checked=2, tp_hits=0, stopped=0))
    monkeypatch.setattr(session, "_load_active_ab", lambda: [])
    monkeypatch.setattr(session, "_refresh_forward_shadow", lambda: None)

    first = session.run_once()
    assert started.wait(2)
    assert first.pending_checked == 2
    assert first.report_refreshed is False
    release.set()
    session._report_future.result(timeout=5)
    second = session.run_once()
    assert second.pending_checked == 2
    assert second.report_refreshed is True


def test_forward_shadow_refresh_runs_off_the_paper_execution_thread(monkeypatch):
    """A slow research pass must not hold up the next one-minute Paper tick."""
    from threading import Event
    from types import SimpleNamespace

    session = StocksMonitorSession(
        load_config(), minutes=0, interval_minutes=1, report_refresh_minutes=10,
        market_hours_only=False, send_telegram=False, dry_run=False,
        background_report_refresh=True,
    )
    started = Event()
    release = Event()

    def _slow_shadow():
        started.set()
        assert release.wait(5)

    monkeypatch.setattr(session, "_refresh_forward_shadow", _slow_shadow)
    first = SimpleNamespace(decisions=[])
    session._start_forward_shadow_refresh(first)
    assert started.wait(2)
    assert first.decisions == [
        {"action": "forward_shadow_refresh", "status": "started"}
    ]

    while_running = SimpleNamespace(decisions=[])
    session._start_forward_shadow_refresh(while_running)
    assert while_running.decisions == [
        {"action": "forward_shadow_refresh", "status": "running"}
    ]

    release.set()
    session._shadow_future.result(timeout=5)
    completed = SimpleNamespace(decisions=[])
    session._collect_forward_shadow_refresh(completed)
    assert completed.decisions == [
        {"action": "forward_shadow_refresh", "status": "completed"}
    ]


def test_fast_pending_tracker_is_strictly_stocks_intraday(monkeypatch):
    from types import SimpleNamespace
    import src.signals.config as config_module
    import src.signals.tracker as tracker_module

    session = StocksMonitorSession(
        load_config(), minutes=0, market_hours_only=False,
        send_telegram=False, dry_run=False,
    )
    captured = {}
    monkeypatch.setattr(config_module, "load_signal_tracking_config",
                        lambda root: SimpleNamespace(enabled=True))

    def _track(**kwargs):
        captured.update(kwargs)
        return SimpleNamespace(checked=0, tp_hits=0, stopped=0)

    monkeypatch.setattr(tracker_module, "track_pending_entries", _track)
    session._track_pending_entries(None)

    assert captured["asset_class"] == "stocks"
    assert captured["modes"] == {"intraday"}
    assert captured["telemetry_source"] == "stocks-monitor-session"
    assert captured["paper_entry_dry_run"] is True


def test_fast_report_refresh_registers_versioned_profiles_from_same_result(monkeypatch):
    from types import SimpleNamespace
    from src.execution import stocks_intraday_breakout_1bar_paper as breakout
    from src.execution import stocks_catalyst_rs_paper as catalyst_rs
    from src.execution import stocks_intraday_pullback_paper as pullback
    from src.stocks.pipelines import stocks_pipeline

    shared_result = SimpleNamespace(ideas=[], decision_at="2026-08-10T14:00:00+00:00")
    calls = []

    class _Pipeline:
        def __init__(self, config):
            self.config = config

        def run_report(self, **kwargs):
            calls.append(("report", kwargs))
            hook = kwargs.get("on_decision")
            if hook is not None:
                hook(self, shared_result)
            return shared_result

    monkeypatch.setattr(stocks_pipeline, "StocksPipeline", _Pipeline)
    monkeypatch.setattr(
        breakout, "register_result",
        lambda **kwargs: calls.append(("breakout", kwargs)) or {"registered": 2},
    )
    monkeypatch.setattr(
        pullback, "register_result",
        lambda **kwargs: calls.append(("pullback", kwargs)) or {"registered": 1},
    )
    monkeypatch.setattr(
        catalyst_rs, "refresh",
        lambda **kwargs: calls.append(("catalyst_rs", kwargs)) or {"registered": 3},
    )
    session = StocksMonitorSession(
        load_config(), minutes=0, market_hours_only=False,
        send_telegram=False, dry_run=False,
    )

    summary = session._refresh_report()

    assert [name for name, _payload in calls] == [
        "report", "breakout", "pullback", "catalyst_rs"
    ]
    assert calls[0][1]["fast_data_update"] is True
    assert calls[1][1]["result"] is shared_result
    assert calls[2][1]["result"] is shared_result
    assert summary["breakout_1bar"]["registered"] == 2
    assert summary["pullback_vwap"]["registered"] == 1
    assert calls[3][1]["refresh_shadow"] is True
    assert summary["catalyst_rs"]["registered"] == 3


def test_schedule_uses_fast_crypto_and_stocks_pending_cadences():
    from scripts.run_default_market_schedule import pending_monitor_step, stocks_monitor_step

    crypto_argv = pending_monitor_step(90)[1]
    stocks_argv = stocks_monitor_step(90)[1]
    assert crypto_argv[crypto_argv.index("--interval") + 1] == "30"
    assert crypto_argv[crypto_argv.index("--duration-hours") + 1] == "0"
    assert stocks_argv[stocks_argv.index("--interval-minutes") + 1] == "1"
    # Pre-open uses its explicit forced decision pass. During RTH the slower
    # cadence leaves write headroom for the one-minute execution tracker.
    assert stocks_argv[stocks_argv.index("--report-refresh-minutes") + 1] == "15"
    # 26h overlaps the scheduler's two-hour hand-off, so an expiring worker
    # cannot leave the next pre-market without a monitor.
    assert stocks_argv[stocks_argv.index("--minutes") + 1] == "1560"


def test_cli_alert_status_command_exists():
    import inspect

    from src.cli import app

    cmd = next(
        (c for c in app.registered_commands if c.name == "alert-status"),
        None,
    )
    assert cmd is not None
    sig = inspect.signature(cmd.callback)
    assert "asset_class" in sig.parameters
