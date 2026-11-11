import asyncio
import sqlite3
import time

from scripts import derivatives_monitor


def test_nonfatal_provider_timeout_is_bounded(monkeypatch):
    pulses = []
    monkeypatch.setattr(
        derivatives_monitor, "_write_heartbeat",
        lambda stage, **kwargs: pulses.append((stage, kwargs)),
    )

    def slow_provider():
        time.sleep(0.1)
        return {"ok": True}

    result = asyncio.run(
        derivatives_monitor._nonfatal_thread(
            "slow", slow_provider, _timeout_seconds=0.01,
        )
    )
    assert result == {"error": "slow:TimeoutError:>0s"}
    assert pulses[-1][0] == "source_refresh_timed_out"
    assert pulses[-1][1]["status"] == "DEGRADED"


def test_nonfatal_provider_clears_progress_with_completed_heartbeat(monkeypatch):
    monkeypatch.setattr(derivatives_monitor, "PROGRESS_HEARTBEAT_SECONDS", 0.01)
    pulses = []
    monkeypatch.setattr(
        derivatives_monitor, "_write_heartbeat",
        lambda stage, **kwargs: pulses.append((stage, kwargs)),
    )

    def slow_provider():
        time.sleep(0.03)
        return {"ok": True}

    result = asyncio.run(derivatives_monitor._nonfatal_thread("slow", slow_provider))

    assert result == {"ok": True}
    assert any(stage == "source_refresh_in_progress" for stage, _ in pulses)
    assert pulses[-1][0] == "source_refresh_completed"


def test_progress_gather_returns_results_in_order(monkeypatch):
    monkeypatch.setattr(derivatives_monitor, "PROGRESS_HEARTBEAT_SECONDS", 0.01)
    pulses = []
    monkeypatch.setattr(
        derivatives_monitor, "_write_heartbeat",
        lambda stage, **kwargs: pulses.append((stage, kwargs)),
    )

    async def value(delay, result):
        await asyncio.sleep(delay)
        return result

    result = asyncio.run(
        derivatives_monitor._gather_with_progress(
            value(0.03, "first"), value(0.01, "second")
        )
    )
    assert result == ["first", "second"]
    assert any(stage == "current_refresh_in_progress" for stage, _ in pulses)


def test_sqlite_lock_retry_is_bounded_and_selective(monkeypatch):
    calls = []
    monkeypatch.setattr(derivatives_monitor.time, "sleep", lambda delay: None)

    def transient():
        calls.append(1)
        if len(calls) < 3:
            raise sqlite3.OperationalError("database is locked")
        return {"status": "OK"}

    assert derivatives_monitor._retry_sqlite_locked(transient) == {"status": "OK"}
    assert len(calls) == 3


def test_sqlite_retry_does_not_hide_non_lock_errors():
    def broken():
        raise sqlite3.OperationalError("no such table: missing")

    try:
        derivatives_monitor._retry_sqlite_locked(broken)
    except sqlite3.OperationalError as exc:
        assert "no such table" in str(exc)
    else:
        raise AssertionError("non-lock SQLite error was swallowed")


def test_fast_flush_loop_keeps_fixed_start_to_start_cadence(monkeypatch):
    assert derivatives_monitor.FAST_FLUSH_CADENCE_SECONDS == 15
    source = __import__("inspect").getsource(derivatives_monitor.fast_flush_paper_loop)
    assert "_aligned_delay(cadence, FAST_FLUSH_SETTLE_SECONDS)" in source
    assert "archive_runtime_frames" not in source


def test_fast_flush_wall_clock_alignment(monkeypatch):
    monkeypatch.setattr(derivatives_monitor.time, "time", lambda: 100.2)
    assert round(derivatives_monitor._aligned_delay(15, 1.5), 3) == 6.3
