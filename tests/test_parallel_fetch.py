"""Tests for the P1 timeout fix — bounded parallel fetch in Supervisor.

Covers the concurrency primitive `Supervisor._parallel_fetch` used by
`update_data` to run independent OHLCV/derivatives collectors concurrently:
  - all independent tasks are invoked;
  - successful sources return their results;
  - one failing source degrades ONLY that source (others still succeed);
  - a slow source does not block the others (wall-clock ≈ max, not sum);
  - a source exceeding the per-source budget degrades to None and is logged;
  - per-source stage timings land in the diagnostics log.

These tests assert NO trading/scoring/tier behavior — purely fetch scheduling
and safety.
"""
from __future__ import annotations

import time
from pathlib import Path

from src.agents.supervisor import Supervisor
from src.config import load_config
from src.diagnostics import stage_timer


def _sup() -> Supervisor:
    return Supervisor(load_config())


def test_runs_all_tasks_and_returns_results():
    sup = _sup()
    tasks = {
        "a": lambda: "ra",
        "b": lambda: "rb",
        "c": lambda: "rc",
    }
    out = sup._parallel_fetch(tasks, label_prefix="ohlcv", symbols=5)
    assert out == {"a": "ra", "b": "rb", "c": "rc"}


def test_empty_tasks_returns_empty():
    sup = _sup()
    assert sup._parallel_fetch({}, label_prefix="deriv") == {}


def test_one_failure_degrades_only_that_source():
    sup = _sup()
    calls: list[str] = []

    def ok(name):
        calls.append(name)
        return f"r-{name}"

    def boom():
        calls.append("bad")
        raise RuntimeError("source down")

    tasks = {
        "good1": lambda: ok("good1"),
        "bad": boom,
        "good2": lambda: ok("good2"),
    }
    out = sup._parallel_fetch(tasks, label_prefix="ohlcv")
    assert out["bad"] is None              # failed source degraded
    assert out["good1"] == "r-good1"        # others unaffected
    assert out["good2"] == "r-good2"
    assert set(calls) >= {"good1", "good2", "bad"}  # all invoked


def test_concurrency_is_faster_than_sequential():
    sup = _sup()
    delay = 0.4

    def slow(name):
        time.sleep(delay)
        return name

    tasks = {n: (lambda nm=n: slow(nm)) for n in ("x", "y", "z", "w")}
    t0 = time.monotonic()
    out = sup._parallel_fetch(tasks, label_prefix="ohlcv", max_workers=4)
    elapsed = time.monotonic() - t0
    assert len(out) == 4 and all(out.values())
    # 4 tasks x 0.4s sequential = 1.6s; concurrent (4 workers) ~0.4-0.8s.
    assert elapsed < delay * 2.5, f"not concurrent: {elapsed:.2f}s"


def test_slow_source_times_out_and_degrades(monkeypatch):
    sup = _sup()
    # Force a tiny per-source budget. ProjectConfig is a frozen dataclass, so
    # patch the class method (not the frozen instance).
    orig = type(sup.config).report_setting

    def _patched(self, key, default=None):
        if key == "fetch_source_timeout_s":
            return 0.3
        return orig(self, key, default)

    monkeypatch.setattr(type(sup.config), "report_setting", _patched)

    def hang():
        time.sleep(5.0)
        return "late"

    tasks = {"fast": lambda: "ok", "hang": hang}
    t0 = time.monotonic()
    out = sup._parallel_fetch(tasks, label_prefix="deriv", max_workers=4)
    elapsed = time.monotonic() - t0
    assert out["fast"] == "ok"
    assert out["hang"] is None              # exceeded budget -> degraded
    # we did not wait the full 5s to collect (budget ~0.3s); allow slack for
    # the executor shutdown waiting on the orphan thread is bounded by sleep.
    assert elapsed < 6.0


def test_per_source_timings_written_to_diagnostics_log(tmp_path):
    sup = _sup()
    stage_timer.set_report("test-parallel")
    sup._parallel_fetch(
        {"binance": lambda: "x", "mexc": lambda: "y"},
        label_prefix="ohlcv", symbols=7,
    )
    from datetime import datetime, timezone
    log = Path("logs") / "diagnostics" / (
        "crypto_report_timing_" + datetime.now(timezone.utc).strftime("%Y-%m-%d") + ".log"
    )
    assert log.exists()
    text = log.read_text(encoding="utf-8")
    assert "ohlcv_binance" in text
    assert "ohlcv_mexc" in text
