"""One-day automated schedule for the crypto-ai-desk.

Runs 5 production cycles tomorrow (or the date passed via ``--date``) according
to the times defined in :data:`CYCLES`. Each cycle:

* runs a fixed list of CLI commands (track-signals, *-report, signal-stats,
  active-signals, …);
* optionally runs a stocks-monitor-session and/or crypto monitor-watchlist
  block for a configured duration;
* writes a Markdown summary per cycle into ``data/scheduled_runs/<date>/``;
* sends an optional Telegram summary;
* never touches scoring, agents, thresholds, or trading logic.

The script is **failure-safe**: any command that errors out is logged but does
not crash the day. Stale background monitors are detected via a per-day PID
file; the scheduler kills them before starting a new one.

CLI examples
------------
``python scripts/run_tomorrow_schedule.py --dry-run``
    Validate the plan; print commands; do not execute anything.

``python scripts/run_tomorrow_schedule.py --run-now cycle_1 --no-send-telegram``
    Run only ``cycle_1`` immediately, ignoring schedule times and Telegram.

``python scripts/run_tomorrow_schedule.py``
    Default: schedule all 5 cycles for tomorrow in Asia/Nicosia time.

Designed to run on Windows (PowerShell / cmd) and via ``run_tomorrow_schedule.bat``.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import shutil
import signal
import subprocess
import sys
import time
import traceback
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

# ---------------------------------------------------------------------------
# Project config
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TZ = "Asia/Nicosia"


@dataclass
class CycleStep:
    """A single command inside a cycle."""

    label: str
    argv: list[str]
    kind: str = "command"            # "command" | "stocks_monitor" | "crypto_monitor"
    duration_minutes: int = 0        # only meaningful for monitor kinds
    optional_skip_outside_market: bool = False


@dataclass
class Cycle:
    """One scheduled cycle (e.g. 'Morning Crypto Check')."""

    cycle_id: str
    name: str
    hour: int
    minute: int
    purpose: str
    steps: list[CycleStep]


# ---------------------------------------------------------------------------
# Cycle definitions — declarative; do not edit at runtime.
# ---------------------------------------------------------------------------

def _cli(*args: str) -> list[str]:
    """Build a ``python -m src.cli …`` argv list."""
    return [sys.executable, "-m", "src.cli", *args]


CYCLES: list[Cycle] = [
    Cycle(
        cycle_id="cycle_1",
        name="Morning Crypto Check",
        hour=9, minute=0,
        purpose=(
            "Track overnight outcomes, refresh crypto scalp + intraday, "
            "review active/stats. Stocks skipped (US market closed)."
        ),
        steps=[
            CycleStep("track-signals (pre)", _cli("track-signals", "--all")),
            CycleStep("crypto scalp report", _cli("scalp-report")),
            CycleStep("crypto intraday report", _cli("intraday-report")),
            CycleStep("active-signals (crypto)",
                      _cli("active-signals", "--asset-class", "crypto", "--limit", "20")),
            CycleStep("signal-stats (crypto)",
                      _cli("signal-stats", "--asset-class", "crypto")),
            CycleStep("track-signals (post)", _cli("track-signals", "--all")),
        ],
    ),
    Cycle(
        cycle_id="cycle_2",
        name="Pre-US Market Check",
        hour=14, minute=30,
        purpose=(
            "Update crypto + prepare stocks before US open. Surface any new "
            "A/B that emerged overnight."
        ),
        steps=[
            CycleStep("track-signals (pre)", _cli("track-signals", "--all")),
            CycleStep("crypto scalp report", _cli("scalp-report")),
            CycleStep("crypto intraday report", _cli("intraday-report")),
            CycleStep("stocks intraday report", _cli("stocks-intraday-report")),
            CycleStep("active-signals (crypto)",
                      _cli("active-signals", "--asset-class", "crypto", "--limit", "20")),
            CycleStep("active-signals (stocks)",
                      _cli("active-signals", "--asset-class", "stocks", "--limit", "20")),
            CycleStep("signal-stats (crypto)",
                      _cli("signal-stats", "--asset-class", "crypto")),
            CycleStep("signal-stats (stocks)",
                      _cli("signal-stats", "--asset-class", "stocks")),
            CycleStep("track-signals (post)", _cli("track-signals", "--all")),
        ],
    ),
    Cycle(
        cycle_id="cycle_3",
        name="US Open Full Monitor",
        hour=16, minute=20,
        purpose=(
            "Most important cycle. Starts 10 min before US open. Refresh "
            "everything, then run 90-minute stocks + crypto monitors in "
            "parallel with Telegram alerts."
        ),
        steps=[
            CycleStep("track-signals (pre)", _cli("track-signals", "--all")),
            CycleStep("crypto scalp report", _cli("scalp-report")),
            CycleStep("crypto intraday report", _cli("intraday-report")),
            CycleStep("stocks intraday report", _cli("stocks-intraday-report")),
            # Crypto monitor in background, stocks monitor blocks the cycle.
            CycleStep(
                "crypto monitor (90 min, background)",
                _cli("monitor-watchlist", "--interval", "600", "--iterations", "9"),
                kind="crypto_monitor",
                duration_minutes=90,
            ),
            CycleStep(
                "stocks monitor session (90 min)",
                _cli(
                    "stocks-monitor-session",
                    "--minutes", "90",
                    "--interval-minutes", "10",
                    "--market-hours-only",
                    "--send-telegram",
                ),
                kind="stocks_monitor",
                duration_minutes=90,
            ),
            CycleStep("track-signals (post-monitors)", _cli("track-signals", "--all")),
            CycleStep("signal-stats (crypto)",
                      _cli("signal-stats", "--asset-class", "crypto")),
            CycleStep("signal-stats (stocks)",
                      _cli("signal-stats", "--asset-class", "stocks")),
        ],
    ),
    Cycle(
        cycle_id="cycle_4",
        name="Mid-US Session Refresh",
        hour=19, minute=0,
        purpose=(
            "Check open-session continuation. Refresh reports + run 60-min "
            "stocks monitor. Crypto monitor restarted if not already running."
        ),
        steps=[
            CycleStep("track-signals (pre)", _cli("track-signals", "--all")),
            CycleStep("crypto scalp report", _cli("scalp-report")),
            CycleStep("crypto intraday report", _cli("intraday-report")),
            CycleStep("stocks intraday report", _cli("stocks-intraday-report")),
            CycleStep(
                "crypto monitor (60 min, background)",
                _cli("monitor-watchlist", "--interval", "600", "--iterations", "6"),
                kind="crypto_monitor",
                duration_minutes=60,
            ),
            CycleStep(
                "stocks monitor session (60 min)",
                _cli(
                    "stocks-monitor-session",
                    "--minutes", "60",
                    "--interval-minutes", "10",
                    "--market-hours-only",
                    "--send-telegram",
                ),
                kind="stocks_monitor",
                duration_minutes=60,
            ),
            CycleStep("track-signals (post-monitors)", _cli("track-signals", "--all")),
            CycleStep("active-signals (crypto)",
                      _cli("active-signals", "--asset-class", "crypto", "--limit", "20")),
            CycleStep("active-signals (stocks)",
                      _cli("active-signals", "--asset-class", "stocks", "--limit", "20")),
            CycleStep("signal-stats (crypto)",
                      _cli("signal-stats", "--asset-class", "crypto")),
            CycleStep("signal-stats (stocks)",
                      _cli("signal-stats", "--asset-class", "stocks")),
        ],
    ),
    Cycle(
        cycle_id="cycle_5",
        name="Final Daily Review",
        hour=22, minute=30,
        purpose=(
            "End-of-day. Final tracking pass + raw and deduped stats. Build "
            "DAILY_AUTO_MONITOR_REVIEW Markdown. No new trades."
        ),
        steps=[
            CycleStep("track-signals (final)", _cli("track-signals", "--all")),
            CycleStep("active-signals (crypto)",
                      _cli("active-signals", "--asset-class", "crypto", "--limit", "50")),
            CycleStep("active-signals (stocks)",
                      _cli("active-signals", "--asset-class", "stocks", "--limit", "50")),
            CycleStep("signal-stats (crypto)",
                      _cli("signal-stats", "--asset-class", "crypto")),
            CycleStep("signal-stats (stocks)",
                      _cli("signal-stats", "--asset-class", "stocks")),
            CycleStep("alert-status (stocks)",
                      _cli("alert-status", "--asset-class", "stocks")),
            CycleStep("alert-status (crypto)",
                      _cli("alert-status", "--asset-class", "crypto")),
            CycleStep(
                "dedup signal stats",
                [sys.executable, "-m", "scripts.dedup_signal_stats"],
            ),
        ],
    ),
]


# ---------------------------------------------------------------------------
# Run-context: per-day state and helpers
# ---------------------------------------------------------------------------


@dataclass
class CycleResult:
    cycle_id: str
    name: str
    started_at: str
    finished_at: str = ""
    step_results: list[dict[str, Any]] = field(default_factory=list)
    telegram_status: str = "skipped"
    fatal_error: str = ""


class RunContext:
    """Holds per-day directories, lockfiles, and the live logger."""

    def __init__(self, *, target_date: str, send_telegram: bool, dry_run: bool):
        self.target_date = target_date
        self.send_telegram = send_telegram
        self.dry_run = dry_run
        self.day_dir = PROJECT_ROOT / "data" / "scheduled_runs" / target_date
        self.day_dir.mkdir(parents=True, exist_ok=True)
        self.log_path = self.day_dir / "scheduler.log"
        self.crypto_lock = self.day_dir / "crypto_monitor.pid"
        self.cycle_results: list[CycleResult] = []

        # Configure logger.
        self.logger = logging.getLogger("tomorrow_scheduler")
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            fh = logging.FileHandler(self.log_path, encoding="utf-8")
            fh.setFormatter(
                logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
            )
            self.logger.addHandler(fh)
            sh = logging.StreamHandler(sys.stdout)
            sh.setFormatter(
                logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
            )
            self.logger.addHandler(sh)

    def cycle_summary_path(self, cycle_id: str, name: str) -> Path:
        safe = name.lower().replace(" ", "_").replace("/", "_")
        return self.day_dir / f"{cycle_id}_{safe}.md"


# ---------------------------------------------------------------------------
# Command execution
# ---------------------------------------------------------------------------


def _truncate_output(text: str, max_chars: int = 4000) -> str:
    if len(text) <= max_chars:
        return text
    return text[: max_chars // 2] + "\n…[truncated]…\n" + text[-max_chars // 2 :]


def run_command(
    ctx: RunContext,
    argv: list[str],
    *,
    label: str,
    timeout: int | None = None,
) -> dict[str, Any]:
    """Run a CLI command, capture output, log + return a result dict.

    Never raises — failures are recorded in the result and logged.
    """
    ctx.logger.info("CMD START: %s :: %s", label, " ".join(argv[2:]))
    if ctx.dry_run:
        ctx.logger.info("CMD DRY-RUN — not executed")
        return {
            "label": label, "argv": argv, "exit_code": 0, "duration_s": 0,
            "stdout_tail": "(dry-run)", "ok": True,
        }

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env.setdefault("PYTHONPATH", str(PROJECT_ROOT))
    started = time.monotonic()
    try:
        proc = subprocess.run(
            argv,
            cwd=PROJECT_ROOT,
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
        duration = time.monotonic() - started
        out = (proc.stdout or "") + ("\n--STDERR--\n" + (proc.stderr or "") if proc.stderr else "")
        out_tail = _truncate_output(out)
        ok = proc.returncode == 0
        ctx.logger.info(
            "CMD END: %s :: exit=%d duration=%.1fs", label, proc.returncode, duration
        )
        return {
            "label": label, "argv": argv, "exit_code": proc.returncode,
            "duration_s": round(duration, 1), "stdout_tail": out_tail, "ok": ok,
        }
    except subprocess.TimeoutExpired as exc:
        duration = time.monotonic() - started
        ctx.logger.error("CMD TIMEOUT: %s after %.1fs", label, duration)
        return {
            "label": label, "argv": argv, "exit_code": -1,
            "duration_s": round(duration, 1),
            "stdout_tail": f"(timeout after {duration:.0f}s)\n{exc}",
            "ok": False,
        }
    except Exception as exc:  # noqa: BLE001
        duration = time.monotonic() - started
        tb = traceback.format_exc()
        ctx.logger.error("CMD FAILED: %s :: %s", label, exc)
        return {
            "label": label, "argv": argv, "exit_code": -2,
            "duration_s": round(duration, 1),
            "stdout_tail": f"(exception) {exc}\n{tb}",
            "ok": False,
        }


# ---------------------------------------------------------------------------
# Crypto monitor lifecycle (background process with PID file)
# ---------------------------------------------------------------------------


def _read_lock_pid(lock: Path) -> int | None:
    if not lock.exists():
        return None
    try:
        return int(lock.read_text().strip())
    except Exception:
        return None


def _is_pid_alive(pid: int) -> bool:
    """Cross-platform check whether a PID is alive."""
    if pid <= 0:
        return False
    if sys.platform == "win32":
        try:
            out = subprocess.run(
                ["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"],
                capture_output=True, text=True, timeout=10,
            )
            return str(pid) in (out.stdout or "")
        except Exception:
            return False
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def _kill_pid(pid: int) -> None:
    if not _is_pid_alive(pid):
        return
    if sys.platform == "win32":
        subprocess.run(
            ["taskkill", "/F", "/T", "/PID", str(pid)],
            capture_output=True, text=True, timeout=15,
        )
    else:
        try:
            os.kill(pid, signal.SIGTERM)
        except OSError:
            pass


def start_crypto_monitor(ctx: RunContext, argv: list[str], *, label: str) -> dict[str, Any]:
    """Start a crypto monitor in background. Detect & kill stale prior PID.

    Returns a dict logging what was done; the monitor keeps running.
    """
    ctx.logger.info("CRYPTO MONITOR START: %s", label)
    if ctx.dry_run:
        ctx.logger.info("CRYPTO MONITOR DRY-RUN — not executed")
        return {"label": label, "argv": argv, "ok": True, "pid": None, "stdout_tail": "(dry-run)"}

    prior = _read_lock_pid(ctx.crypto_lock)
    if prior is not None and _is_pid_alive(prior):
        ctx.logger.warning("stale crypto monitor PID=%d detected — killing it", prior)
        _kill_pid(prior)
        time.sleep(2)
    elif prior is not None:
        ctx.logger.info("prior crypto monitor PID=%d already dead; clearing lock", prior)
    try:
        ctx.crypto_lock.unlink(missing_ok=True)
    except Exception:
        pass

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env.setdefault("PYTHONPATH", str(PROJECT_ROOT))
    log_path = ctx.day_dir / f"crypto_monitor_{int(time.time())}.log"
    try:
        creation_flags = 0
        if sys.platform == "win32":
            creation_flags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
        proc = subprocess.Popen(
            argv,
            cwd=PROJECT_ROOT,
            env=env,
            stdout=open(log_path, "w", encoding="utf-8"),
            stderr=subprocess.STDOUT,
            creationflags=creation_flags,
        )
        ctx.crypto_lock.write_text(str(proc.pid))
        ctx.logger.info("CRYPTO MONITOR pid=%d logfile=%s", proc.pid, log_path)
        return {
            "label": label, "argv": argv, "ok": True, "pid": proc.pid,
            "logfile": str(log_path),
            "stdout_tail": f"(background pid={proc.pid})",
        }
    except Exception as exc:  # noqa: BLE001
        ctx.logger.error("CRYPTO MONITOR START FAILED: %s", exc)
        return {"label": label, "argv": argv, "ok": False, "pid": None, "stdout_tail": str(exc)}


# ---------------------------------------------------------------------------
# Telegram summaries
# ---------------------------------------------------------------------------


def send_telegram_summary(ctx: RunContext, text: str) -> str:
    """Return 'sent' / 'skipped' / 'failed:<class>'."""
    if not ctx.send_telegram or ctx.dry_run:
        return "skipped"
    try:
        # Lazy import so the script also runs in dry mode without project deps.
        sys.path.insert(0, str(PROJECT_ROOT))
        from src.notifiers.telegram import TelegramNotifier  # type: ignore

        notifier = TelegramNotifier(PROJECT_ROOT / "config" / "notifications.yaml")
        if not notifier.enabled or not notifier.chat_id:
            ctx.logger.info("Telegram disabled or chat_id missing — summary skipped")
            return "skipped"
        notifier.send(text)
        return "sent"
    except Exception as exc:  # noqa: BLE001
        ctx.logger.warning("Telegram send failed: %s", exc)
        return f"failed:{exc.__class__.__name__}"


def build_cycle_telegram(cycle: Cycle, result: CycleResult) -> str:
    ok = sum(1 for s in result.step_results if s.get("ok"))
    failed = len(result.step_results) - ok
    head = f"[SCHEDULER] {cycle.cycle_id.upper()} — {cycle.name}"
    body = [
        head,
        f"started: {result.started_at}",
        f"finished: {result.finished_at}",
        f"steps: ok={ok} failed={failed}",
    ]
    for s in result.step_results:
        if not s.get("ok"):
            body.append(f"FAIL: {s['label']} (exit={s.get('exit_code')})")
    body.append("see daily folder for full log.")
    return "\n".join(body)


# ---------------------------------------------------------------------------
# Cycle execution
# ---------------------------------------------------------------------------


def execute_cycle(ctx: RunContext, cycle: Cycle) -> CycleResult:
    """Run every step of a cycle. Never raise — log + record."""
    ctx.logger.info("=" * 60)
    ctx.logger.info("CYCLE START: %s — %s", cycle.cycle_id, cycle.name)
    ctx.logger.info("=" * 60)
    now_iso = datetime.now(ZoneInfo(DEFAULT_TZ)).isoformat()
    result = CycleResult(cycle_id=cycle.cycle_id, name=cycle.name, started_at=now_iso)

    for step in cycle.steps:
        try:
            if step.kind == "crypto_monitor":
                step_result = start_crypto_monitor(ctx, step.argv, label=step.label)
            elif step.kind == "stocks_monitor":
                # Foreground blocking call. Timeout = duration + 10 min buffer.
                timeout = (step.duration_minutes + 10) * 60
                step_result = run_command(ctx, step.argv, label=step.label, timeout=timeout)
            else:
                step_result = run_command(ctx, step.argv, label=step.label, timeout=900)
            result.step_results.append(step_result)
        except Exception as exc:  # noqa: BLE001
            ctx.logger.error("STEP EXCEPTION (continuing): %s", exc)
            result.step_results.append({
                "label": step.label, "argv": step.argv, "exit_code": -3,
                "duration_s": 0,
                "stdout_tail": f"(exception) {exc}\n{traceback.format_exc()}",
                "ok": False,
            })

    finished_iso = datetime.now(ZoneInfo(DEFAULT_TZ)).isoformat()
    result.finished_at = finished_iso

    # Write per-cycle Markdown.
    md_path = ctx.cycle_summary_path(cycle.cycle_id, cycle.name)
    write_cycle_markdown(ctx, cycle, result, md_path)

    # Telegram summary.
    tg_text = build_cycle_telegram(cycle, result)
    result.telegram_status = send_telegram_summary(ctx, tg_text)
    ctx.logger.info("CYCLE END: %s (telegram=%s)", cycle.cycle_id, result.telegram_status)

    ctx.cycle_results.append(result)

    # Kill crypto monitor at the end of cycles 3 and 4 so the next cycle can
    # start clean. (Cycle 3 starts a 90-min monitor; by the time cycle 4
    # runs, it should be already finished or in its last minutes.)
    if cycle.cycle_id in {"cycle_3", "cycle_4"}:
        prior = _read_lock_pid(ctx.crypto_lock)
        if prior is not None and _is_pid_alive(prior):
            ctx.logger.info("end-of-cycle: stopping background crypto monitor pid=%d", prior)
            _kill_pid(prior)
        try:
            ctx.crypto_lock.unlink(missing_ok=True)
        except Exception:
            pass

    return result


def write_cycle_markdown(ctx: RunContext, cycle: Cycle, result: CycleResult, path: Path) -> None:
    lines = [
        f"# {cycle.name} — {cycle.cycle_id}",
        "",
        f"- Purpose: {cycle.purpose}",
        f"- Scheduled: {cycle.hour:02d}:{cycle.minute:02d} {DEFAULT_TZ}",
        f"- Started: {result.started_at}",
        f"- Finished: {result.finished_at}",
        f"- Telegram: {result.telegram_status}",
        "",
        "## Steps",
        "",
    ]
    for i, s in enumerate(result.step_results, start=1):
        ok = "✅" if s.get("ok") else "❌"
        lines.append(
            f"### {i}. {ok} {s['label']} "
            f"(exit={s.get('exit_code')}, {s.get('duration_s')}s)"
        )
        lines.append("")
        lines.append("```")
        lines.append(str(s.get("argv", "")))
        lines.append("```")
        lines.append("")
        lines.append("```text")
        lines.append((s.get("stdout_tail") or "")[:6000])
        lines.append("```")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Final daily review (cycle 5 helper)
# ---------------------------------------------------------------------------


def write_daily_review(ctx: RunContext) -> Path:
    target = ctx.day_dir / f"DAILY_AUTO_MONITOR_REVIEW_{ctx.target_date}.md"
    lines = [
        f"# Daily Auto-Monitor Review — {ctx.target_date}",
        "",
        f"_Generated by scripts/run_tomorrow_schedule.py at "
        f"{datetime.now(ZoneInfo(DEFAULT_TZ)).isoformat()}_",
        "",
        "## Cycles executed",
        "",
        "| Cycle | Started | Finished | Steps ok | Steps failed | Telegram |",
        "|-------|---------|----------|----------|--------------|----------|",
    ]
    for r in ctx.cycle_results:
        ok = sum(1 for s in r.step_results if s.get("ok"))
        bad = len(r.step_results) - ok
        lines.append(
            f"| {r.cycle_id} {r.name} | {r.started_at} | {r.finished_at} | "
            f"{ok} | {bad} | {r.telegram_status} |"
        )
    lines.extend([
        "",
        "## Reports generated today",
        "",
        "_See each cycle's Markdown for full report paths and command output._",
        "",
        "## Active signals / stats / dedup",
        "",
        "_The final cycle ran:_",
        "- `active-signals --asset-class crypto`",
        "- `active-signals --asset-class stocks`",
        "- `signal-stats --asset-class crypto`",
        "- `signal-stats --asset-class stocks`",
        "- `alert-status --asset-class crypto`",
        "- `alert-status --asset-class stocks`",
        "- `scripts.dedup_signal_stats`",
        "",
        "_See `cycle_5_*.md` for the raw outputs of each._",
        "",
        "## Verdict (auto-template)",
        "",
        "- Crypto scalp: see latest scalp report under "
        "`data/reports/scalp/`",
        "- Crypto intraday: see latest intraday report under "
        "`data/reports/intraday/`",
        "- Stocks intraday: see latest stocks intraday report under "
        "`data/reports/stocks/intraday/`",
        "",
        "_The scheduler intentionally does NOT auto-classify "
        "tradeable / watchlist / no-trade — that decision requires a human "
        "read of the reports + signal performance._",
        "",
        "## Safety check",
        "",
        "- ✅ No auto-trade actions taken",
        "- ✅ No scoring / threshold / agent changes",
        "- ✅ No architecture refactor",
        "- ✅ Only existing CLI commands invoked",
        "- ✅ Telegram alerts honour de-dup + invalidation rules in the CLI",
        "",
    ])
    target.write_text("\n".join(lines), encoding="utf-8")
    ctx.logger.info("Final daily review written: %s", target)
    return target


# ---------------------------------------------------------------------------
# Scheduling loop
# ---------------------------------------------------------------------------


def _seconds_until(target: datetime) -> float:
    return max(0.0, (target - datetime.now(target.tzinfo)).total_seconds())


def _cycle_datetime(cycle: Cycle, target_date: str) -> datetime:
    tz = ZoneInfo(DEFAULT_TZ)
    y, m, d = (int(p) for p in target_date.split("-"))
    return datetime(y, m, d, cycle.hour, cycle.minute, tzinfo=tz)


def run_full_schedule(ctx: RunContext) -> None:
    tz = ZoneInfo(DEFAULT_TZ)
    for cycle in CYCLES:
        when = _cycle_datetime(cycle, ctx.target_date)
        wait_s = _seconds_until(when)
        if wait_s > 0:
            ctx.logger.info(
                "sleeping %.0fs until %s (%s)", wait_s, when.isoformat(), cycle.cycle_id
            )
            # Sleep in chunks so a CTRL-C / KeyboardInterrupt is responsive.
            step = 30
            end = time.monotonic() + wait_s
            while time.monotonic() < end:
                time.sleep(min(step, end - time.monotonic()))
        else:
            ctx.logger.warning(
                "cycle %s was scheduled in the past (%s) — running immediately",
                cycle.cycle_id, when.isoformat(),
            )
        execute_cycle(ctx, cycle)
        if cycle.cycle_id == "cycle_5":
            write_daily_review(ctx)


def run_single_cycle(ctx: RunContext, cycle_id: str) -> None:
    cycle = next((c for c in CYCLES if c.cycle_id == cycle_id), None)
    if cycle is None:
        ctx.logger.error("unknown cycle id %r", cycle_id)
        raise SystemExit(2)
    execute_cycle(ctx, cycle)
    if cycle.cycle_id == "cycle_5":
        write_daily_review(ctx)


# ---------------------------------------------------------------------------
# Dry-run validation
# ---------------------------------------------------------------------------


def dry_run_plan(ctx: RunContext) -> None:
    ctx.logger.info("=== DRY RUN — no commands will be executed ===")
    for cycle in CYCLES:
        when = _cycle_datetime(cycle, ctx.target_date)
        ctx.logger.info(
            "%s (%s) @ %s — %d step(s)",
            cycle.cycle_id, cycle.name, when.isoformat(), len(cycle.steps),
        )
        for step in cycle.steps:
            kind = f"[{step.kind}]" if step.kind != "command" else ""
            ctx.logger.info("    %s %s :: %s", kind, step.label, " ".join(step.argv[2:]))

    # Validate that the CLI commands actually exist by running --help once.
    # We deliberately bypass the dry-run gate here so the validation does
    # something useful; --help is read-only and side-effect-free.
    ctx.logger.info("--- validating CLI surface ---")
    seen: set[str] = set()
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env.setdefault("PYTHONPATH", str(PROJECT_ROOT))
    for cycle in CYCLES:
        for step in cycle.steps:
            if len(step.argv) > 2 and step.argv[1] == "-m" and step.argv[2] == "src.cli":
                cli_cmd = step.argv[3] if len(step.argv) > 3 else None
                if cli_cmd and cli_cmd not in seen:
                    seen.add(cli_cmd)
                    try:
                        proc = subprocess.run(
                            [sys.executable, "-m", "src.cli", cli_cmd, "--help"],
                            cwd=PROJECT_ROOT, env=env,
                            capture_output=True, text=True,
                            encoding="utf-8", errors="replace", timeout=60,
                        )
                        if proc.returncode == 0:
                            ctx.logger.info("validate %-26s OK", cli_cmd)
                        else:
                            ctx.logger.warning(
                                "validate %-26s FAILED exit=%d", cli_cmd, proc.returncode
                            )
                    except Exception as exc:  # noqa: BLE001
                        ctx.logger.warning("validate %s raised %s", cli_cmd, exc)
    ctx.logger.info("=== dry run complete ===")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def _default_tomorrow() -> str:
    today = datetime.now(ZoneInfo(DEFAULT_TZ)).date()
    return (today + timedelta(days=1)).isoformat()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--date", default=_default_tomorrow(),
        help="YYYY-MM-DD target date in Asia/Nicosia. Default: tomorrow.",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print the plan and validate CLI commands; do not execute.",
    )
    parser.add_argument(
        "--run-now",
        choices=[c.cycle_id for c in CYCLES],
        help="Run a single cycle immediately, ignoring its scheduled time.",
    )
    tg = parser.add_mutually_exclusive_group()
    tg.add_argument(
        "--send-telegram", dest="send_tg", action="store_true",
        help="Force Telegram summaries on (default).",
    )
    tg.add_argument(
        "--no-send-telegram", dest="send_tg", action="store_false",
        help="Disable Telegram summaries.",
    )
    parser.set_defaults(send_tg=True)
    args = parser.parse_args()

    # Force dry-run mode to imply no Telegram.
    send_telegram = bool(args.send_tg) and not args.dry_run

    ctx = RunContext(
        target_date=args.date,
        send_telegram=send_telegram,
        dry_run=args.dry_run,
    )
    ctx.logger.info(
        "scheduler boot — date=%s dry_run=%s send_telegram=%s",
        args.date, args.dry_run, send_telegram,
    )

    try:
        if args.dry_run:
            dry_run_plan(ctx)
            return 0
        if args.run_now:
            run_single_cycle(ctx, args.run_now)
            return 0
        run_full_schedule(ctx)
        return 0
    except KeyboardInterrupt:
        ctx.logger.warning("interrupted by user — cleaning up monitors")
        prior = _read_lock_pid(ctx.crypto_lock)
        if prior is not None:
            _kill_pid(prior)
        try:
            ctx.crypto_lock.unlink(missing_ok=True)
        except Exception:
            pass
        return 130
    except Exception as exc:  # noqa: BLE001
        ctx.logger.exception("fatal scheduler error: %s", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
