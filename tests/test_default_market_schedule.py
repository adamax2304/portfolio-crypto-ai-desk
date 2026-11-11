"""Tests for `scripts/run_default_market_schedule.py` — the desk's
permanent operating loop.

Pins the contract:

* weekday → crypto + stocks; weekend → crypto-only.
* `--crypto-only` / `--no-stocks` override weekday-stocks ON.
* long-horizon (crypto swing daily + optional shadow-only stocks position scan) only on the
  first cycle of the UTC day. Old stocks swing/invest are DEPRECATED/REMOVED and never scheduled;
  the stocks position scan is gated by position_framework.scheduler_enabled.
* Windows DLL init failure (exit 3221225794) is retried; non-DLL
  failures pass through.
* Stocks scalp is a 'note' step — does not invoke any CLI, does not fail.
* No Opus / Claude / Anthropic tokens appear in the rendered command
  plan (auto-LLM blocked).
"""

from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from scripts.run_default_market_schedule import (
    DEFAULT_TZ,
    LONG_HORIZON_WINDOW_HOURS,
    NONFATAL_TIMEOUT_OVERRIDES,
    NONFATAL_TIMEOUT_SECONDS,
    RunContext,
    _reclaim_orphaned_monitor_leader_lock,
    _start_background_monitor,
    WINDOWS_DLL_INIT_FAILED_EXIT,
    bootstrap_execution_monitors,
    build_cycle_steps,
    current_long_horizon_window,
    due_long_horizon_window,
    is_weekend,
    stocks_enabled,
)


TZ = ZoneInfo(DEFAULT_TZ)


def test_heavy_shadow_counterfactuals_have_longer_nonfatal_timeout():
    assert NONFATAL_TIMEOUT_SECONDS == 300
    assert NONFATAL_TIMEOUT_OVERRIDES[
        "crypto swing versioned shadow sweep (counterfactual)"
    ] >= 900
    assert NONFATAL_TIMEOUT_OVERRIDES[
        "crypto quality overlay report (counterfactual)"
    ] >= 900
    assert NONFATAL_TIMEOUT_OVERRIDES["intelligence layer update"] >= 600


def test_dashboard_refreshes_have_short_nonfatal_timeouts():
    assert NONFATAL_TIMEOUT_OVERRIDES["refresh obsidian dashboard"] == 60
    assert NONFATAL_TIMEOUT_OVERRIDES["telegram dashboard refresh (read-only)"] == 60


def test_monitor_locks_are_global_across_scheduler_days(tmp_path, monkeypatch):
    """A scheduler restart/date rollover must reuse, not duplicate, monitors."""
    import scripts.run_default_market_schedule as schedule

    monkeypatch.setattr(schedule, "PROJECT_ROOT", tmp_path)
    first = RunContext(
        send_telegram=False, dry_run=True, skip_reports=False,
        monitor_minutes=90, crypto_only=False,
        started_at=datetime(2026, 7, 29, 23, 59, tzinfo=TZ),
    )
    second = RunContext(
        send_telegram=False, dry_run=True, skip_reports=False,
        monitor_minutes=90, crypto_only=False,
        started_at=datetime(2026, 7, 30, 0, 1, tzinfo=TZ),
    )

    assert first.crypto_lock == second.crypto_lock
    assert first.pending_lock == second.pending_lock
    assert "runtime_locks" in str(first.crypto_lock)


def test_orphaned_internal_leader_lock_is_reclaimed_but_live_owner_is_preserved(tmp_path, monkeypatch):
    """Restart recovery must never displace a still-running monitor."""
    import logging
    import scripts.run_default_market_schedule as schedule

    monkeypatch.setattr(schedule, "PROJECT_ROOT", tmp_path)
    lease = tmp_path / ".locks" / "pending_monitor_leader_crypto.lock"
    lease.parent.mkdir(parents=True)
    lease.write_text("12345 pending-12345", encoding="utf-8")
    monkeypatch.setattr(schedule, "_is_pid_alive", lambda pid: False)
    assert _reclaim_orphaned_monitor_leader_lock("crypto", logger=logging.getLogger("test")) is True
    assert not lease.exists()

    lease.write_text("98765 pending-98765", encoding="utf-8")
    monkeypatch.setattr(schedule, "_is_pid_alive", lambda pid: True)
    assert _reclaim_orphaned_monitor_leader_lock("crypto", logger=logging.getLogger("test")) is False
    assert lease.exists()


def test_background_launcher_adopts_existing_monitor_without_spawning(tmp_path, monkeypatch):
    """A manual leader with no runtime PID file must not get a standby peer."""
    import scripts.run_default_market_schedule as schedule

    monkeypatch.setattr(schedule, "PROJECT_ROOT", tmp_path)
    ctx = RunContext(
        send_telegram=False, dry_run=False, skip_reports=False,
        monitor_minutes=1, crypto_only=False,
        started_at=datetime(2026, 7, 30, 10, 0, tzinfo=TZ),
    )
    monkeypatch.setattr(schedule, "_read_lock_pid", lambda _path: None)
    monkeypatch.setattr(schedule, "_find_running_monitor", lambda marker: 4242)

    class _NeverSpawn:
        def __init__(self, *_args, **_kwargs):
            raise AssertionError("existing monitor must be adopted, not duplicated")

    monkeypatch.setattr(schedule.subprocess, "Popen", _NeverSpawn)
    result = _start_background_monitor(
        ctx, ["python", "-m", "src.cli", "pending-monitor"], label="pending",
        lock_path=ctx.pending_lock, log_prefix="pending", pretty_name="pending",
        process_marker="pending-monitor",
    )
    assert result["stdout_tail"] == "(adopted existing pid=4242)"
    assert ctx.pending_lock.read_text(encoding="utf-8") == "4242"


def test_dashboard_launcher_reclaims_a_reused_global_poll_pid(tmp_path, monkeypatch):
    """A PID collision cannot make the scheduler skip callback polling."""
    import scripts.run_default_market_schedule as schedule

    monkeypatch.setattr(schedule, "PROJECT_ROOT", tmp_path)
    ctx = RunContext(
        send_telegram=False, dry_run=False, skip_reports=False,
        monitor_minutes=1, crypto_only=False,
        started_at=datetime(2026, 7, 30, 10, 0, tzinfo=TZ),
    )
    poll_lock = tmp_path / "data" / "telegram" / "dashboard_state.json.poll.lock"
    poll_lock.parent.mkdir(parents=True)
    poll_lock.write_text("4242", encoding="ascii")
    monkeypatch.setattr(schedule, "_is_pid_alive", lambda _pid: True)
    monkeypatch.setattr(
        schedule, "_process_has_marker", lambda _pid, _marker: False
    )
    captured = {}

    def _start(*args, **kwargs):
        captured.update(kwargs)
        return {"ok": True, "stdout_tail": "started"}

    monkeypatch.setattr(schedule, "_start_background_monitor", _start)
    result = schedule.start_telegram_dashboard_monitor(
        ctx, ["python", "-m", "src.cli", "telegram-dashboard"], label="dashboard"
    )
    assert result["ok"] is True
    assert captured["process_marker"] == "telegram-dashboard"
    assert not poll_lock.exists()


def test_derivatives_launcher_matches_the_real_module_command(monkeypatch, tmp_path):
    import scripts.run_default_market_schedule as schedule

    captured = {}

    def _start(*args, **kwargs):
        captured.update(kwargs)
        return {"ok": True}

    monkeypatch.setattr(schedule, "_start_background_monitor", _start)
    ctx = type("Ctx", (), {"derivatives_lock": tmp_path / "derivatives.pid"})()
    schedule.start_derivatives_monitor(
        ctx,
        ["python", "-m", "scripts.derivatives_monitor"],
        label="derivatives",
    )
    assert captured["process_marker"] == "scripts.derivatives_monitor"


# ---------------------------------------------------------------------------
# Calendar gates
# ---------------------------------------------------------------------------


def test_saturday_is_weekend():
    sat = datetime(2026, 5, 30, 12, 0, tzinfo=TZ)  # Saturday
    assert is_weekend(sat) is True


def test_sunday_is_weekend():
    sun = datetime(2026, 5, 31, 12, 0, tzinfo=TZ)
    assert is_weekend(sun) is True


def test_monday_is_weekday():
    mon = datetime(2026, 6, 1, 12, 0, tzinfo=TZ)
    assert is_weekend(mon) is False


def test_friday_is_weekday():
    fri = datetime(2026, 6, 5, 18, 0, tzinfo=TZ)
    assert is_weekend(fri) is False


def test_stocks_off_on_weekend():
    sat = datetime(2026, 5, 30, 12, 0, tzinfo=TZ)
    assert stocks_enabled(sat) is False


def test_stocks_on_on_weekday():
    mon = datetime(2026, 6, 1, 12, 0, tzinfo=TZ)
    assert stocks_enabled(mon) is True


def test_force_crypto_only_overrides_weekday():
    mon = datetime(2026, 6, 1, 12, 0, tzinfo=TZ)
    assert stocks_enabled(mon, force_crypto_only=True) is False


# ---------------------------------------------------------------------------
# Cycle composition
# ---------------------------------------------------------------------------


def _labels(now: datetime, **kw) -> list[str]:
    defaults = dict(
        crypto_only=False,
        include_long_horizon=False,
        monitor_minutes=90,
        skip_reports=False,
    )
    defaults.update(kw)
    return [s[0] for s in build_cycle_steps(now=now, **defaults)]


def test_archived_crypto_invest_forward_monitor_is_not_scheduled():
    mon = datetime(2026, 6, 1, 12, 0, tzinfo=TZ)
    steps = build_cycle_steps(
        now=mon, crypto_only=False, include_long_horizon=False,
        monitor_minutes=90, skip_reports=True,
    )
    selected = [step for step in steps if step[2] == "crypto_invest_forward_monitor"]
    assert selected == []


def test_crypto_live_mode_audit_runs_in_support_tail():
    mon = datetime(2026, 6, 1, 12, 0, tzinfo=TZ)
    steps = build_cycle_steps(
        now=mon, crypto_only=False, include_long_horizon=False,
        monitor_minutes=90, skip_reports=True,
    )
    selected = [step for step in steps if step[0] == "crypto live mode audit"]
    assert len(selected) == 1
    assert "crypto-live-mode-audit" in selected[0][1]
    assert selected[0][2] == "command_nonfatal"
    fallback = [step for step in steps if step[0] == "crypto live fallback capture"]
    assert len(fallback) == 1
    assert "crypto-live-fallback-capture" in fallback[0][1]
    assert fallback[0][2] == "command_nonfatal"
    labels = [step[0] for step in steps]
    assert labels.index("crypto live fallback capture") < labels.index("crypto live mode audit")


def test_weekend_cycle_excludes_all_stocks_commands():
    sat = datetime(2026, 5, 30, 12, 0, tzinfo=TZ)
    labels = _labels(sat)
    assert all("stocks" not in label.lower() for label in labels), labels


def test_weekday_cycle_includes_stocks_intraday():
    mon = datetime(2026, 6, 1, 12, 0, tzinfo=TZ)
    labels = _labels(mon)
    assert "stocks intraday report" in labels
    # Stocks scalp is a 'note' step, not a real command — it should appear
    # in the plan (as a marker) so the cycle summary records the gap.
    assert "stocks scalp report" in labels
    assert "news source health monitor (alert-only)" in labels


def test_default_cycle_does_not_schedule_preus_bundle_and_keeps_bounded_tp_refresh():
    mon = datetime(2026, 6, 1, 12, 0, tzinfo=TZ)
    steps = build_cycle_steps(now=mon, crypto_only=False, include_long_horizon=False,
                              monitor_minutes=1, skip_reports=False)
    by_label = {step[0]: step for step in steps}
    assert "stocks pre-US review candidate bundle (advisory)" not in by_label
    assert "paper structural TP refresh" in by_label
    assert "--limit" in by_label["paper structural TP refresh"][1]
    assert "200" in by_label["paper structural TP refresh"][1]


def test_paper_maintenance_is_bounded_and_does_not_repeat_execution_in_ledger():
    mon = datetime(2026, 6, 1, 12, 0, tzinfo=TZ)
    steps = build_cycle_steps(now=mon, crypto_only=False, include_long_horizon=False,
                              monitor_minutes=1, skip_reports=False)
    by_label = {step[0]: step for step in steps}
    expected_limits = {
        "paper execution accounting refresh": "120",
        "paper structural stop plan": "200",
        "paper entry-mode classify": "200",
        "paper stock direction (multi-factor)": "240",
        "entry latency audit (root cause)": "120",
        "paper-shadow A/B execution": "240",
    }
    for label, value in expected_limits.items():
        assert "--limit" in by_label[label][1] or "--max-signals" in by_label[label][1]
        assert value in by_label[label][1]
    assert "--skip-execution-refresh" in by_label["paper portfolio ledger refresh"][1]


def test_intraday_report_reuses_cache_and_cannot_block_live_loop():
    mon = datetime(2026, 6, 1, 12, 0, tzinfo=TZ)
    steps = build_cycle_steps(now=mon, crypto_only=False, include_long_horizon=False,
                              monitor_minutes=1, skip_reports=False)
    report = next(step for step in steps if step[0] == "crypto intraday report")

    assert report[2] == "command_nonfatal"
    assert "--no-update" in report[1]
    assert "--skip-packet" in report[1]
    assert NONFATAL_TIMEOUT_OVERRIDES[report[0]] == 180


def test_long_cycle_does_not_put_llm_cache_refresh_behind_research_steps():
    mon = datetime(2026, 6, 1, 12, 0, tzinfo=TZ)
    labels = _labels(mon, include_long_horizon=True)
    assert "quality agents openrouter advisory cache refresh" not in labels
    assert "central LLM router cost and distribution monitor" not in labels


def test_sequential_promotion_gate_follows_paper_shadow_refresh():
    mon = datetime(2026, 6, 1, 12, 0, tzinfo=TZ)
    steps = build_cycle_steps(now=mon, crypto_only=False, include_long_horizon=False,
                              monitor_minutes=1, skip_reports=False)
    labels = [step[0] for step in steps]
    shadow = labels.index("paper-shadow A/B execution")
    gate = labels.index("sequential promotion gate (forward A/B, read-model)")
    assert shadow < gate
    assert "sequential-gate-report" in steps[gate][1]
    assert steps[gate][2] == "command_nonfatal"


def test_fast_news_monitor_is_started_independently_of_report_cycle():
    mon = datetime(2026, 6, 1, 12, 0, tzinfo=TZ)
    step = next(s for s in build_cycle_steps(now=mon, crypto_only=False,
                                             include_long_horizon=False, monitor_minutes=1,
                                             skip_reports=False)
                if "fast Finnhub news monitor" in s[0])
    assert "scripts.fast_news_monitor" in step[1]
    assert "--interval-seconds" in step[1] and "120" in step[1]
    assert step[2] == "fast_news_monitor"


def test_cold_boot_starts_background_monitors_before_cycle(monkeypatch):
    import scripts.run_default_market_schedule as schedule

    launched: list[str] = []

    def fake_launcher(_ctx, _argv, *, label):
        launched.append(label)
        return {"label": label, "ok": True}

    for name in (
        "start_crypto_monitor", "start_pending_monitor", "start_mexc_canary_monitor",
        "start_crypto_invest_forward_monitor", "start_derivatives_monitor",
        "start_fast_news_monitor", "start_stocks_monitor",
        "start_telegram_dashboard_monitor",
    ):
        monkeypatch.setattr(schedule, name, fake_launcher)

    class Ctx:
        crypto_only = False
        monitor_minutes = 90
        logger = schedule.logging.getLogger("bootstrap-test")

    results = bootstrap_execution_monitors(
        Ctx(), now=datetime(2026, 6, 1, 12, 0, tzinfo=TZ)
    )
    assert len(results) == len(launched)
    assert any("MEXC canary monitor" in label for label in launched)
    assert any("fast Finnhub news" in label for label in launched)
    assert any("derivatives" in label for label in launched)
    assert any("stocks monitor" in label for label in launched)


def test_news_health_monitor_is_alert_only_and_nonfatal():
    mon = datetime(2026, 6, 1, 12, 0, tzinfo=TZ)
    step = next(s for s in build_cycle_steps(now=mon, crypto_only=False,
                                             include_long_horizon=False, monitor_minutes=1,
                                             skip_reports=False)
                if s[0] == "news source health monitor (alert-only)")
    assert "news-health-monitor" in step[1]
    assert "--send-telegram" in step[1]
    assert step[2] == "command_nonfatal"

    steps = build_cycle_steps(now=mon, crypto_only=False,
                              include_long_horizon=False, monitor_minutes=1,
                              skip_reports=False)
    labels = [item[0] for item in steps]
    refresh = labels.index("news source health snapshot refresh")
    monitor = labels.index("news source health monitor (alert-only)")
    assert refresh < monitor
    assert "news-source-health" in steps[refresh][1]
    assert steps[refresh][2] == "command_nonfatal"


def test_catalyst_label_repair_runs_before_heavy_tracking_once():
    mon = datetime(2026, 6, 1, 12, 0, tzinfo=TZ)
    steps = build_cycle_steps(
        now=mon, crypto_only=False, include_long_horizon=False,
        monitor_minutes=1, skip_reports=False,
    )
    labels = [step[0] for step in steps]
    assert labels.count("catalyst label refresh") == 1
    assert labels.index("catalyst label refresh") < labels.index("track-signals (pre)")


def test_paper_operational_audit_consumes_fresh_news_quality_verdict():
    mon = datetime(2026, 6, 1, 12, 0, tzinfo=TZ)
    labels = _labels(mon)
    assert labels.index("news quality gold/replay gate") < labels.index(
        "paper operational audit (USD/evidence/funnel)"
    )


def test_crypto_only_flag_strips_stocks_on_weekday():
    mon = datetime(2026, 6, 1, 12, 0, tzinfo=TZ)
    labels = _labels(mon, crypto_only=True)
    assert all("stocks" not in label.lower() for label in labels), labels


def test_news_entity_health_monitor_is_alert_only_and_nonfatal():
    """2026-07-13 audit: this diagnostic previously only ran via manual CLI and could go stale for
    days unnoticed. Now a scheduled step, same alert-only/fail-open shape as source health."""
    mon = datetime(2026, 6, 1, 12, 0, tzinfo=TZ)
    step = next(s for s in build_cycle_steps(now=mon, crypto_only=False,
                                             include_long_horizon=False, monitor_minutes=1,
                                             skip_reports=False)
                if s[0] == "news entity resolver health monitor (alert-only)")
    assert "news-entity-health" in step[1]
    assert "--send-telegram" in step[1]
    assert step[2] == "command_nonfatal"


def test_news_content_and_gap_diagnostics_and_targeted_telegram_recovery_are_scheduled():
    mon = datetime(2026, 6, 1, 12, 0, tzinfo=TZ)
    steps = build_cycle_steps(now=mon, crypto_only=False, include_long_horizon=False,
                              monitor_minutes=1, skip_reports=False)
    by_label = {step[0]: step for step in steps}
    assert "telegram stale-source targeted recovery" in by_label
    assert "scripts.telegram_stale_recovery" in by_label["telegram stale-source targeted recovery"][1]
    for label, command in (
        ("news content coverage diagnostic (read-only)", "news-content-coverage"),
        ("news coverage gaps diagnostic (read-only)", "news-coverage-gaps"),
    ):
        assert label in by_label and command in by_label[label][1]
        assert by_label[label][2] == "command_nonfatal"


def test_entry_mode_calibration_refresh_is_scheduled_and_nonfatal():
    """2026-07-13 audit: the per-slice calibration read-model previously only refreshed on manual
    CLI. Cheap pure-SQL aggregation (no OHLCV cost of its own) -> safe every cycle."""
    mon = datetime(2026, 6, 1, 12, 0, tzinfo=TZ)
    step = next(s for s in build_cycle_steps(now=mon, crypto_only=False,
                                             include_long_horizon=False, monitor_minutes=1,
                                             skip_reports=False)
                if s[0] == "entry-mode calibration refresh (read-model)")
    assert "entry-mode-calibration-refresh" in step[1]
    assert step[2] == "command_nonfatal"


def test_stocks_intraday_forward_evaluator_runs_after_coverage_flags():
    mon = datetime(2026, 6, 1, 12, 0, tzinfo=TZ)
    steps = build_cycle_steps(now=mon, crypto_only=False, include_long_horizon=False,
                              monitor_minutes=1, skip_reports=False)
    labels = [step[0] for step in steps]
    coverage = labels.index("stock coverage gate (cache-only re-classify + mark outcomes)")
    evaluation = labels.index("stocks intraday forward shadow evaluation (clean-only)")
    assert coverage < evaluation
    command = steps[evaluation][1]
    assert "stocks-intraday-forward-shadow-evaluate" in command
    assert steps[evaluation][2] == "command_nonfatal"


def test_weekend_cycle_still_marks_new_stock_shadow_rows():
    sat = datetime(2026, 5, 30, 12, 0, tzinfo=TZ)
    labels = _labels(sat)
    assert "stock coverage gate (cache-only re-classify + mark outcomes)" in labels


def test_long_horizon_block_new_contract(monkeypatch):
    """Archived crypto swing and old stocks swing/invest are GONE. The stocks
    position framework is shadow-only and gated by scheduler_enabled — a 'disabled' note when
    off, the shadow scan when on."""
    import scripts.run_default_market_schedule as sched
    mon = datetime(2026, 6, 1, 12, 0, tzinfo=TZ)

    # Scheduler disabled (default): archived crypto swing is absent and the
    # position framework remains a disabled note.
    monkeypatch.setattr(sched, "_position_framework_scheduler_enabled", lambda: False)
    dis = _labels(mon, include_long_horizon=True)
    assert "agent run summary retention (daily)" in dis
    assert "crypto swing report (daily)" not in dis
    assert "market-regime policy calibration (daily, read-only)" in dis
    assert "stocks swing report (daily)" not in dis
    assert "stocks invest report (daily)" not in dis
    assert "stocks position framework scan (disabled)" in dis
    assert "stocks position framework scan (shadow, daily)" not in dis

    # scheduler enabled → shadow-only position scan present, no disabled note
    monkeypatch.setattr(sched, "_position_framework_scheduler_enabled", lambda: True)
    en = _labels(mon, include_long_horizon=True)
    assert "stocks position framework scan (shadow, daily)" in en
    assert en.count("stocks position framework outcome refresh (shadow, daily)") == 2
    assert "stocks position framework scan (disabled)" not in en

    # without the long-horizon flag: none of the daily-once steps appear
    without = _labels(mon, include_long_horizon=False)
    assert "agent run summary retention (daily)" not in without
    assert "crypto swing report (daily)" not in without
    assert "market-regime policy calibration (daily, read-only)" not in without
    assert not any("stocks position framework" in lbl for lbl in without)


def test_stock_news_fast_resolver_refreshes_labels_same_cycle():
    mon = datetime(2026, 6, 1, 12, 0, tzinfo=TZ)
    labels = _labels(mon)
    stock_report = labels.index("stocks intraday report")
    fast_resolve = labels.index("news entity resolve (fast 24h post-ingest)")
    post_label = labels.index("catalyst label refresh (post-stock news)")
    assert stock_report < fast_resolve < post_label


def test_long_horizon_weekend_excludes_stocks(monkeypatch):
    """On weekend the daily block must NOT include ANY stocks step — old swing/invest OR the new
    shadow position scan (crypto-only weekend)."""
    import scripts.run_default_market_schedule as sched
    monkeypatch.setattr(sched, "_position_framework_scheduler_enabled", lambda: True)
    sat = datetime(2026, 5, 30, 12, 0, tzinfo=TZ)
    labels = _labels(sat, include_long_horizon=True)
    assert "crypto swing report (daily)" not in labels
    assert "stocks swing report (daily)" not in labels
    assert "stocks invest report (daily)" not in labels
    assert not any("stocks position framework" in lbl for lbl in labels)


def test_no_old_stocks_swing_invest_commands_anywhere(monkeypatch):
    """Belt-and-suspenders: no rendered label OR argv may contain the deprecated commands, across
    weekend / weekday / long-horizon and both scheduler_enabled states."""
    import scripts.run_default_market_schedule as sched
    scenarios = [
        (datetime(2026, 5, 30, 12, 0, tzinfo=TZ), dict(include_long_horizon=True)),          # weekend
        (datetime(2026, 6, 1, 12, 0, tzinfo=TZ), dict(include_long_horizon=True)),           # weekday
        (datetime(2026, 6, 1, 12, 0, tzinfo=TZ), dict(include_long_horizon=True, crypto_only=True)),
    ]
    for enabled in (False, True):
        monkeypatch.setattr(sched, "_position_framework_scheduler_enabled", lambda e=enabled: e)
        for now, kw in scenarios:
            steps = build_cycle_steps(now=now, crypto_only=kw.get("crypto_only", False),
                                      include_long_horizon=True, monitor_minutes=90, skip_reports=False)
            for label, argv, *_ in steps:
                blob = (label + " " + (" ".join(argv) if isinstance(argv, list) else "")).lower()
                assert "stocks-swing-report" not in blob and "stocks-invest-report" not in blob, blob


# ---------------------------------------------------------------------------
# PART 9 — twice-daily long-horizon windows
# ---------------------------------------------------------------------------


def test_long_horizon_windows_constant_shape():
    """Exactly two windows, both inside 24h, non-overlapping."""
    assert set(LONG_HORIZON_WINDOW_HOURS) == {1, 2}
    for lo, hi in LONG_HORIZON_WINDOW_HOURS.values():
        assert 0 <= lo < hi <= 24
    # Windows must not overlap
    w1 = LONG_HORIZON_WINDOW_HOURS[1]
    w2 = LONG_HORIZON_WINDOW_HOURS[2]
    assert w1[1] <= w2[0] or w2[1] <= w1[0]


def test_window1_fires_around_04_eest():
    """A cycle at 04:04 EEST must be classified as window 1."""
    now = datetime(2026, 6, 2, 4, 4, tzinfo=TZ)
    assert current_long_horizon_window(now) == 1


def test_window2_fires_around_16_eest():
    """A cycle at 16:04 EEST must be classified as window 2."""
    now = datetime(2026, 6, 2, 16, 4, tzinfo=TZ)
    assert current_long_horizon_window(now) == 2


def test_outside_windows_returns_none():
    """Cycles at 10:04 / 22:04 / 00:04 EEST are outside both windows."""
    for hour in (0, 6, 8, 10, 12, 14, 18, 20, 22, 23):
        now = datetime(2026, 6, 2, hour, 4, tzinfo=TZ)
        assert current_long_horizon_window(now) is None, hour


def test_window1_lower_bound_inclusive():
    """03:00 EEST is the first minute of window 1 (inclusive lower bound)."""
    assert current_long_horizon_window(datetime(2026, 6, 2, 3, 0, tzinfo=TZ)) == 1


def test_window1_upper_bound_exclusive():
    """05:00 EEST is past window 1 (exclusive upper bound)."""
    assert current_long_horizon_window(datetime(2026, 6, 2, 5, 0, tzinfo=TZ)) is None


def test_windows_evaluate_in_project_tz_even_for_utc_now():
    """A datetime in UTC must be projected into Asia/Nicosia for the gate."""
    # 01:04 UTC == 04:04 EEST in summer (UTC+3) — should be window 1.
    now = datetime(2026, 6, 2, 1, 4, tzinfo=ZoneInfo("UTC"))
    assert current_long_horizon_window(now) == 1


def test_overdue_afternoon_swing_window_is_recovered_once_after_restart():
    now = datetime(2026, 6, 2, 18, 15, tzinfo=TZ)
    window, recovery = due_long_horizon_window(now, is_done=lambda window_id: window_id == 1)
    assert (window, recovery) == (2, True)


def test_on_time_swing_window_is_not_labeled_as_recovery():
    now = datetime(2026, 6, 2, 16, 15, tzinfo=TZ)
    window, recovery = due_long_horizon_window(now, is_done=lambda _window_id: False)
    assert (window, recovery) == (2, False)


def test_all_completed_swing_windows_do_not_run_again_after_restart():
    now = datetime(2026, 6, 2, 18, 15, tzinfo=TZ)
    window, recovery = due_long_horizon_window(now, is_done=lambda _window_id: True)
    assert (window, recovery) == (None, False)


def test_cycle_always_includes_track_signals_and_detector():
    sat = datetime(2026, 5, 30, 12, 0, tzinfo=TZ)
    labels = _labels(sat)
    assert "track-signals (pre)" in labels
    assert "track-signals (post)" in labels
    assert "untracked-legacy detector" in labels
    assert "daily review (obsidian)" in labels
    assert "telegram dashboard refresh (read-only)" in labels


def test_cycle_includes_crypto_monitor_when_reports_run():
    sat = datetime(2026, 5, 30, 12, 0, tzinfo=TZ)
    labels = _labels(sat)
    crypto_monitor_index = next(i for i, label in enumerate(labels) if "crypto watchlist monitor" in label)
    scalp_index = labels.index("crypto scalp report")
    intraday_index = labels.index("crypto intraday report")
    assert crypto_monitor_index < scalp_index < intraday_index


def test_cycle_includes_fast_pending_monitor_with_independent_kind():
    sat = datetime(2026, 5, 30, 12, 0, tzinfo=TZ)
    step = next(
        s for s in build_cycle_steps(
            now=sat, crypto_only=False, include_long_horizon=False,
            monitor_minutes=90, skip_reports=False,
        )
        if s[2] == "pending_monitor"
    )
    assert "pending-monitor" in step[1]
    assert step[1][step[1].index("--interval") + 1] == "30"
    assert step[3] == 0


def test_cycle_includes_read_only_dashboard_callback_monitor():
    sat = datetime(2026, 5, 30, 12, 0, tzinfo=TZ)
    step = next(
        s for s in build_cycle_steps(
            now=sat, crypto_only=False, include_long_horizon=False,
            monitor_minutes=90, skip_reports=False,
        )
        if s[2] == "telegram_dashboard_monitor"
    )
    assert step[0] == "telegram dashboard callbacks (read-only, background)"
    assert "telegram-dashboard" in step[1]
    assert "--no-create" in step[1]
    assert step[1][step[1].index("--duration-hours") + 1] == "0"


def test_pending_is_continuous_and_stocks_monitor_spans_a_full_day():
    """Latency monitors overlap scheduler cycles without stop/start gaps."""
    import scripts.run_default_market_schedule as sched

    crypto = sched.crypto_monitor_step(90)
    pending = sched.pending_monitor_step(90)
    stocks = sched.stocks_monitor_step(90)
    assert crypto[3] == 0 and "continuous" in crypto[0]
    assert crypto[1][crypto[1].index("--duration-hours") + 1] == "0"
    assert pending[3] == 0 and "continuous" in pending[0]
    assert pending[1][pending[1].index("--duration-hours") + 1] == "0"
    assert stocks[3] == 1560 and "--minutes" in stocks[1]
    assert stocks[1][stocks[1].index("--minutes") + 1] == "1560"


def test_weekday_cycle_includes_stocks_monitor():
    """PART 7: stocks A/B alert monitor must run between cycles on weekdays."""
    mon = datetime(2026, 6, 1, 14, 0, tzinfo=TZ)
    labels = _labels(mon)
    assert any("stocks monitor" in label for label in labels), labels


def test_weekend_cycle_omits_stocks_monitor():
    """Stocks monitor is gated on stocks_enabled(), so weekends skip it."""
    sat = datetime(2026, 5, 30, 12, 0, tzinfo=TZ)
    labels = _labels(sat)
    assert not any("stocks monitor" in label for label in labels), labels


def test_crypto_only_flag_skips_stocks_monitor():
    """Force-crypto-only on a weekday must NOT spin up the stocks monitor."""
    mon = datetime(2026, 6, 1, 14, 0, tzinfo=TZ)
    labels = _labels(mon, crypto_only=True)
    assert not any("stocks monitor" in label for label in labels), labels


# ---------------------------------------------------------------------------
# PART 13 — monitors must NOT be killed at end of cycle
# ---------------------------------------------------------------------------


def test_execute_cycle_does_not_kill_monitors_at_end_of_cycle():
    """Source-level guard. The end-of-cycle cleanup must NOT call
    `_kill_pid` on the just-spawned crypto/stocks monitor — that was the
    PART 13 bug that silenced Telegram alerts for a whole day.

    The end-of-cycle block is allowed to LOG (e.g. heartbeat) but must
    not contain `_kill_pid(...)` near "end-of-cycle".
    """
    import re
    from pathlib import Path

    src_path = (
        Path(__file__).resolve().parent.parent
        / "scripts" / "run_default_market_schedule.py"
    )
    src = src_path.read_text(encoding="utf-8")

    # Isolate `execute_cycle` body.
    match = re.search(
        r"def execute_cycle\(\s*ctx: RunContext.*?(?=\ndef\s)",
        src,
        flags=re.DOTALL,
    )
    assert match is not None, "could not locate execute_cycle body"
    body = match.group(0)

    # Locate the post-tail cleanup block (after the steps loop, before return).
    # Must not contain "_kill_pid" in proximity to "end-of-cycle".
    cleanup = re.search(
        r"# PART 13 .*?return record",
        body,
        flags=re.DOTALL,
    )
    assert cleanup is not None, (
        "PART 13 cleanup block markers missing — refactor preserved?"
    )
    block = cleanup.group(0)
    assert "_kill_pid(" not in block, (
        "PART 13 regression: end-of-cycle cleanup must NOT kill monitors. "
        "They are meant to run between cycles with their own --duration-hours "
        "lifetime."
    )


def test_skip_reports_drops_heavy_steps_but_keeps_tail():
    sat = datetime(2026, 5, 30, 12, 0, tzinfo=TZ)
    labels = _labels(sat, skip_reports=True)
    assert "crypto scalp report" not in labels
    assert "crypto intraday report" not in labels
    assert "untracked-legacy detector" in labels
    assert "daily review (obsidian)" in labels


def test_stock_cycle_includes_mexc_paper_tick_and_monitor_watchdog():
    mon = datetime(2026, 6, 1, 14, 0, tzinfo=TZ)
    labels = _labels(mon, crypto_only=False)
    assert "stocks MEXC futures paper tick" in labels
    assert "monitor heartbeat watchdog" in labels
    assert "live funnel report" in labels


def test_long_horizon_cycle_includes_isolated_swing_breakout_refinement_report():
    """The reclaim/refailure experiment stays an explicit Shadow-only report step."""
    mon = datetime(2026, 6, 1, 12, 0, tzinfo=TZ)
    steps = build_cycle_steps(
        now=mon, crypto_only=False, include_long_horizon=True,
        monitor_minutes=90, skip_reports=False,
    )
    step = next(s for s in steps if "breakout reclaim/refailure refinements" in s[0])
    assert "scripts.crypto_swing_entry_sweep" in step[1]
    assert "--breakout-refinements" in step[1]
    assert step[2] == "command_nonfatal"
    assert step[3] == 0


# ---------------------------------------------------------------------------
# No-Opus / no-LLM auto-invocation guarantee
# ---------------------------------------------------------------------------


def test_no_llm_tokens_in_any_cycle_plan():
    forbidden = ("opus", "anthropic", "claude api", "enriched-review")
    for now in (
        datetime(2026, 5, 30, 12, 0, tzinfo=TZ),  # weekend
        datetime(2026, 6, 1, 12, 0, tzinfo=TZ),   # weekday
        datetime(2026, 6, 1, 12, 0, tzinfo=TZ),   # weekday again with long-horizon
    ):
        steps = build_cycle_steps(
            now=now, crypto_only=False, include_long_horizon=True,
            monitor_minutes=90, skip_reports=False,
        )
        rendered = " ".join(
            " ".join(s[1]) if isinstance(s[1], list) else "" for s in steps
        ).lower()
        for word in forbidden:
            assert word not in rendered, f"{word} should not appear in {rendered[:200]}"


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


def test_windows_dll_init_failed_constant_is_correct():
    assert WINDOWS_DLL_INIT_FAILED_EXIT == 0xC0000142
