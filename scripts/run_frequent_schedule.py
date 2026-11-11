"""Frequent monitoring schedule — runs every 2 hours from "now" until shutoff.

Compared to ``run_tomorrow_schedule.py`` (5 fixed cycles), this scheduler:

* runs an immediate **first cycle** as soon as it boots;
* then fires a **regular scan** every 2 hours;
* upgrades the scan to a **long-monitor cycle** when it overlaps the
  configured US-open / mid-US / final-review windows.

Failure-safe, read-only with respect to scoring / agents / thresholds.
Uses only existing CLI commands; never auto-trades.

Usage::

    python -m scripts.run_frequent_schedule --hours 23 --send-telegram
    python -m scripts.run_frequent_schedule --hours 6 --no-send-telegram
    python -m scripts.run_frequent_schedule --dry-run

``--hours`` controls how long the loop runs from boot (default 23 hours,
covers a full day minus 1 hour of buffer).

The scheduler picks today's date (Asia/Nicosia) for the daily folder. If you
need to run past midnight, the folder rotates automatically — each cycle is
written under ``data/scheduled_runs/<current-date>/``.

Special-window definitions (Asia/Nicosia):
* **US open window:** 16:00–17:30 → cycle gets a 90-min stocks monitor +
  crypto monitor, Telegram on.
* **Mid-US window:** 18:30–20:00 → 60-min stocks + crypto monitors.
* **US close / final review:** 22:00–23:00 → no monitors, but dedup +
  alert-status are included.

If a regular tick falls inside one of those windows, the long-monitor
version runs in its place (the cycle is not duplicated).
"""

from __future__ import annotations

import argparse
import logging
import os
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

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TZ = "Asia/Nicosia"
INTERVAL_HOURS = 2.0

# Special-window detection (Nicosia hours, inclusive ranges).
US_OPEN_WINDOW = ("16:00", "17:30")
MID_US_WINDOW = ("18:30", "20:00")
FINAL_REVIEW_WINDOW = ("22:00", "23:00")


def _cli(*args: str) -> list[str]:
    return [sys.executable, "-m", "src.cli", *args]


# Regular 2-hour scan — fast, no monitors.
REGULAR_STEPS: list[tuple[str, list[str], str, int]] = [
    ("track-signals (pre)", _cli("track-signals", "--all"), "command", 0),
    ("crypto scalp report", _cli("scalp-report"), "command", 0),
    ("crypto intraday report", _cli("intraday-report"), "command", 0),
    ("stocks intraday report", _cli("stocks-intraday-report"), "command", 0),
    ("active-signals (crypto)",
     _cli("active-signals", "--asset-class", "crypto", "--limit", "20"), "command", 0),
    ("active-signals (stocks)",
     _cli("active-signals", "--asset-class", "stocks", "--limit", "20"), "command", 0),
    ("signal-stats (crypto)",
     _cli("signal-stats", "--asset-class", "crypto"), "command", 0),
    ("signal-stats (stocks)",
     _cli("signal-stats", "--asset-class", "stocks"), "command", 0),
    ("track-signals (post)", _cli("track-signals", "--all"), "command", 0),
]

# US-open special — adds 90-min crypto + 90-min stocks monitors.
US_OPEN_STEPS: list[tuple[str, list[str], str, int]] = [
    ("track-signals (pre)", _cli("track-signals", "--all"), "command", 0),
    ("crypto scalp report", _cli("scalp-report"), "command", 0),
    ("crypto intraday report", _cli("intraday-report"), "command", 0),
    ("stocks intraday report", _cli("stocks-intraday-report"), "command", 0),
    ("crypto monitor (90 min, background)",
     _cli("monitor-watchlist", "--interval", "600", "--iterations", "9"),
     "crypto_monitor", 90),
    ("stocks monitor session (90 min)",
     _cli("stocks-monitor-session", "--minutes", "90", "--interval-minutes", "10",
          "--market-hours-only", "--send-telegram"),
     "stocks_monitor", 90),
    ("track-signals (post-monitors)", _cli("track-signals", "--all"), "command", 0),
    ("signal-stats (crypto)",
     _cli("signal-stats", "--asset-class", "crypto"), "command", 0),
    ("signal-stats (stocks)",
     _cli("signal-stats", "--asset-class", "stocks"), "command", 0),
]

# Mid-US — 60-min monitors.
MID_US_STEPS: list[tuple[str, list[str], str, int]] = [
    ("track-signals (pre)", _cli("track-signals", "--all"), "command", 0),
    ("crypto scalp report", _cli("scalp-report"), "command", 0),
    ("crypto intraday report", _cli("intraday-report"), "command", 0),
    ("stocks intraday report", _cli("stocks-intraday-report"), "command", 0),
    ("crypto monitor (60 min, background)",
     _cli("monitor-watchlist", "--interval", "600", "--iterations", "6"),
     "crypto_monitor", 60),
    ("stocks monitor session (60 min)",
     _cli("stocks-monitor-session", "--minutes", "60", "--interval-minutes", "10",
          "--market-hours-only", "--send-telegram"),
     "stocks_monitor", 60),
    ("track-signals (post-monitors)", _cli("track-signals", "--all"), "command", 0),
    ("active-signals (crypto)",
     _cli("active-signals", "--asset-class", "crypto", "--limit", "20"), "command", 0),
    ("active-signals (stocks)",
     _cli("active-signals", "--asset-class", "stocks", "--limit", "20"), "command", 0),
    ("signal-stats (crypto)",
     _cli("signal-stats", "--asset-class", "crypto"), "command", 0),
    ("signal-stats (stocks)",
     _cli("signal-stats", "--asset-class", "stocks"), "command", 0),
]

# Final review — no new monitors.
FINAL_REVIEW_STEPS: list[tuple[str, list[str], str, int]] = [
    ("track-signals (final)", _cli("track-signals", "--all"), "command", 0),
    ("active-signals (crypto)",
     _cli("active-signals", "--asset-class", "crypto", "--limit", "50"), "command", 0),
    ("active-signals (stocks)",
     _cli("active-signals", "--asset-class", "stocks", "--limit", "50"), "command", 0),
    ("signal-stats (crypto)",
     _cli("signal-stats", "--asset-class", "crypto"), "command", 0),
    ("signal-stats (stocks)",
     _cli("signal-stats", "--asset-class", "stocks"), "command", 0),
    ("alert-status (stocks)",
     _cli("alert-status", "--asset-class", "stocks"), "command", 0),
    ("alert-status (crypto)",
     _cli("alert-status", "--asset-class", "crypto"), "command", 0),
    ("dedup signal stats", [sys.executable, "-m", "scripts.dedup_signal_stats"],
     "command", 0),
]


@dataclass
class RunContext:
    send_telegram: bool
    dry_run: bool
    hours: float
    started_at: datetime
    cycles_done: list[str] = field(default_factory=list)
    logger: logging.Logger = field(default=None)  # set in __post_init__

    def __post_init__(self):
        # Determine daily folder for today (Nicosia date at boot).
        target_date = self.started_at.astimezone(ZoneInfo(DEFAULT_TZ)).date().isoformat()
        self.day_dir = PROJECT_ROOT / "data" / "scheduled_runs" / target_date
        self.day_dir.mkdir(parents=True, exist_ok=True)
        self.crypto_lock = self.day_dir / "crypto_monitor.pid"
        self.log_path = self.day_dir / "frequent_scheduler.log"

        log = logging.getLogger("frequent_scheduler")
        log.setLevel(logging.INFO)
        if not log.handlers:
            fh = logging.FileHandler(self.log_path, encoding="utf-8")
            fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
            log.addHandler(fh)
            sh = logging.StreamHandler(sys.stdout)
            sh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
            log.addHandler(sh)
        self.logger = log


# ---------------------------------------------------------------------------
# Time window helpers
# ---------------------------------------------------------------------------


def _hm_to_minutes(hm: str) -> int:
    h, m = (int(p) for p in hm.split(":"))
    return h * 60 + m


def _window_label(now: datetime) -> str:
    """Return 'us_open', 'mid_us', 'final_review', or 'regular'."""
    tz = now.astimezone(ZoneInfo(DEFAULT_TZ))
    minutes = tz.hour * 60 + tz.minute
    if _hm_to_minutes(US_OPEN_WINDOW[0]) <= minutes <= _hm_to_minutes(US_OPEN_WINDOW[1]):
        return "us_open"
    if _hm_to_minutes(MID_US_WINDOW[0]) <= minutes <= _hm_to_minutes(MID_US_WINDOW[1]):
        return "mid_us"
    if _hm_to_minutes(FINAL_REVIEW_WINDOW[0]) <= minutes <= _hm_to_minutes(FINAL_REVIEW_WINDOW[1]):
        return "final_review"
    return "regular"


def _steps_for(label: str) -> list[tuple[str, list[str], str, int]]:
    return {
        "us_open": US_OPEN_STEPS,
        "mid_us": MID_US_STEPS,
        "final_review": FINAL_REVIEW_STEPS,
    }.get(label, REGULAR_STEPS)


# ---------------------------------------------------------------------------
# Subprocess helpers (mirror run_tomorrow_schedule)
# ---------------------------------------------------------------------------


def _truncate(text: str, max_chars: int = 4000) -> str:
    if len(text) <= max_chars:
        return text
    return text[: max_chars // 2] + "\n…[truncated]…\n" + text[-max_chars // 2 :]


def run_command(ctx: RunContext, argv: list[str], *, label: str,
                timeout: int | None = None) -> dict[str, Any]:
    ctx.logger.info("CMD START: %s", label)
    if ctx.dry_run:
        return {"label": label, "argv": argv, "ok": True, "exit_code": 0,
                "duration_s": 0, "stdout_tail": "(dry-run)"}
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env.setdefault("PYTHONPATH", str(PROJECT_ROOT))
    started = time.monotonic()
    try:
        proc = subprocess.run(
            argv, cwd=PROJECT_ROOT, env=env,
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=timeout,
        )
        duration = time.monotonic() - started
        out = (proc.stdout or "") + (("\n--STDERR--\n" + proc.stderr) if proc.stderr else "")
        ctx.logger.info("CMD END: %s exit=%d duration=%.1fs", label,
                        proc.returncode, duration)
        return {"label": label, "argv": argv, "ok": proc.returncode == 0,
                "exit_code": proc.returncode, "duration_s": round(duration, 1),
                "stdout_tail": _truncate(out)}
    except subprocess.TimeoutExpired as exc:
        duration = time.monotonic() - started
        ctx.logger.error("CMD TIMEOUT: %s after %.1fs", label, duration)
        return {"label": label, "argv": argv, "ok": False, "exit_code": -1,
                "duration_s": round(duration, 1),
                "stdout_tail": f"(timeout)\n{exc}"}
    except Exception as exc:  # noqa: BLE001
        duration = time.monotonic() - started
        ctx.logger.error("CMD FAILED: %s :: %s", label, exc)
        return {"label": label, "argv": argv, "ok": False, "exit_code": -2,
                "duration_s": round(duration, 1),
                "stdout_tail": f"(exception) {exc}\n{traceback.format_exc()}"}


def _read_lock_pid(lock: Path) -> int | None:
    if not lock.exists():
        return None
    try:
        return int(lock.read_text().strip())
    except Exception:
        return None


def _is_pid_alive(pid: int) -> bool:
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
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(pid)],
                       capture_output=True, text=True, timeout=15)
    else:
        try:
            os.kill(pid, signal.SIGTERM)
        except OSError:
            pass


def start_crypto_monitor(ctx: RunContext, argv: list[str], *, label: str) -> dict[str, Any]:
    if ctx.dry_run:
        return {"label": label, "argv": argv, "ok": True, "exit_code": 0,
                "duration_s": 0, "stdout_tail": "(dry-run, background skipped)"}
    prior = _read_lock_pid(ctx.crypto_lock)
    if prior is not None and _is_pid_alive(prior):
        ctx.logger.warning("stale crypto monitor PID=%d detected — killing", prior)
        _kill_pid(prior)
        time.sleep(2)
    try:
        ctx.crypto_lock.unlink(missing_ok=True)
    except Exception:
        pass
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env.setdefault("PYTHONPATH", str(PROJECT_ROOT))
    logf = ctx.day_dir / f"crypto_monitor_{int(time.time())}.log"
    try:
        creation_flags = 0
        if sys.platform == "win32":
            creation_flags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
        proc = subprocess.Popen(
            argv, cwd=PROJECT_ROOT, env=env,
            stdout=open(logf, "w", encoding="utf-8"),
            stderr=subprocess.STDOUT, creationflags=creation_flags,
        )
        ctx.crypto_lock.write_text(str(proc.pid))
        ctx.logger.info("CRYPTO MONITOR pid=%d logfile=%s", proc.pid, logf)
        return {"label": label, "argv": argv, "ok": True, "exit_code": 0,
                "duration_s": 0,
                "stdout_tail": f"(background pid={proc.pid} -> {logf.name})"}
    except Exception as exc:  # noqa: BLE001
        ctx.logger.error("CRYPTO MONITOR START FAILED: %s", exc)
        return {"label": label, "argv": argv, "ok": False, "exit_code": -3,
                "duration_s": 0, "stdout_tail": str(exc)}


# ---------------------------------------------------------------------------
# Telegram (Telegram bug: cap text to 3800 chars before send)
# ---------------------------------------------------------------------------


def send_telegram(ctx: RunContext, text: str) -> str:
    if not ctx.send_telegram or ctx.dry_run:
        return "skipped"
    capped = text if len(text) <= 3800 else text[:3700] + "\n…[truncated]…"
    try:
        sys.path.insert(0, str(PROJECT_ROOT))
        from src.notifiers.telegram import TelegramNotifier  # type: ignore
        notifier = TelegramNotifier(PROJECT_ROOT / "config" / "notifications.yaml")
        if not notifier.enabled or not notifier.chat_id:
            return "skipped"
        # Send as plain text to avoid Markdown parse errors (today's 400s).
        notifier.send(capped, parse_mode="")
        return "sent"
    except Exception as exc:  # noqa: BLE001
        ctx.logger.warning("Telegram send failed: %s", exc)
        return f"failed:{exc.__class__.__name__}"


# ---------------------------------------------------------------------------
# Cycle execution
# ---------------------------------------------------------------------------


def execute_cycle(ctx: RunContext, window_label: str) -> None:
    cycle_ts = datetime.now(ZoneInfo(DEFAULT_TZ))
    cycle_id = f"cycle_{cycle_ts.strftime('%H%M')}_{window_label}"
    ctx.logger.info("=" * 60)
    ctx.logger.info("CYCLE START %s (window=%s)", cycle_id, window_label)
    ctx.logger.info("=" * 60)

    steps = _steps_for(window_label)
    step_results: list[dict[str, Any]] = []
    for label, argv, kind, duration in steps:
        try:
            if kind == "crypto_monitor":
                step_results.append(start_crypto_monitor(ctx, argv, label=label))
            elif kind == "stocks_monitor":
                timeout = (duration + 10) * 60
                step_results.append(run_command(ctx, argv, label=label, timeout=timeout))
            else:
                step_results.append(run_command(ctx, argv, label=label, timeout=900))
        except Exception as exc:  # noqa: BLE001
            ctx.logger.error("STEP EXCEPTION: %s", exc)
            step_results.append({"label": label, "argv": argv, "ok": False,
                                 "exit_code": -4, "duration_s": 0,
                                 "stdout_tail": f"(exception) {exc}"})

    # Write per-cycle Markdown.
    md = ctx.day_dir / f"{cycle_id}.md"
    finished_at = datetime.now(ZoneInfo(DEFAULT_TZ))
    lines = [
        f"# {cycle_id}",
        "",
        f"- Window: {window_label}",
        f"- Started: {cycle_ts.isoformat()}",
        f"- Finished: {finished_at.isoformat()}",
        "",
        "## Steps",
        "",
    ]
    for i, r in enumerate(step_results, start=1):
        ok = "✅" if r.get("ok") else "❌"
        lines.append(
            f"### {i}. {ok} {r['label']} (exit={r.get('exit_code')}, "
            f"{r.get('duration_s')}s)"
        )
        lines.append("")
        lines.append("```text")
        lines.append((r.get("stdout_tail") or "")[:5000])
        lines.append("```")
        lines.append("")
    md.write_text("\n".join(lines), encoding="utf-8")

    # Telegram summary.
    ok = sum(1 for r in step_results if r.get("ok"))
    bad = len(step_results) - ok
    tg_text = (
        f"[FREQUENT] {cycle_id}\n"
        f"window: {window_label}\n"
        f"started: {cycle_ts.isoformat()}\n"
        f"finished: {finished_at.isoformat()}\n"
        f"steps: ok={ok} failed={bad}\n"
    )
    if bad:
        for r in step_results:
            if not r.get("ok"):
                tg_text += f"FAIL: {r['label']} (exit={r.get('exit_code')})\n"
    status = send_telegram(ctx, tg_text)
    ctx.logger.info("CYCLE END %s telegram=%s", cycle_id, status)
    ctx.cycles_done.append(cycle_id)

    # End-of-monitor cleanup (kill background crypto monitor if still running
    # past the cycle — the next regular tick will start a fresh one when needed).
    if window_label in {"us_open", "mid_us"}:
        prior = _read_lock_pid(ctx.crypto_lock)
        if prior is not None and _is_pid_alive(prior):
            ctx.logger.info("end-of-cycle: stopping background crypto monitor pid=%d", prior)
            _kill_pid(prior)
        try:
            ctx.crypto_lock.unlink(missing_ok=True)
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------


def run_loop(ctx: RunContext) -> None:
    deadline = ctx.started_at + timedelta(hours=ctx.hours)
    ctx.logger.info(
        "frequent scheduler boot — hours=%.1f deadline=%s dry_run=%s telegram=%s",
        ctx.hours, deadline.isoformat(), ctx.dry_run, ctx.send_telegram,
    )

    # Cycle 1 = immediately.
    execute_cycle(ctx, _window_label(datetime.now(ZoneInfo(DEFAULT_TZ))))

    next_at = datetime.now(ZoneInfo(DEFAULT_TZ)) + timedelta(hours=INTERVAL_HOURS)
    while True:
        now = datetime.now(ZoneInfo(DEFAULT_TZ))
        if now >= deadline:
            ctx.logger.info("deadline reached — exiting")
            break
        if now < next_at:
            sleep_s = min(60, (next_at - now).total_seconds())
            if sleep_s > 0:
                time.sleep(sleep_s)
            continue
        execute_cycle(ctx, _window_label(datetime.now(ZoneInfo(DEFAULT_TZ))))
        next_at += timedelta(hours=INTERVAL_HOURS)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--hours", type=float, default=23.0,
                        help="How long the loop runs from boot. Default 23.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Validate plan only, do not execute.")
    tg = parser.add_mutually_exclusive_group()
    tg.add_argument("--send-telegram", dest="send_tg", action="store_true")
    tg.add_argument("--no-send-telegram", dest="send_tg", action="store_false")
    parser.set_defaults(send_tg=True)
    args = parser.parse_args()

    send_tg = bool(args.send_tg) and not args.dry_run
    ctx = RunContext(
        send_telegram=send_tg, dry_run=args.dry_run, hours=args.hours,
        started_at=datetime.now(ZoneInfo(DEFAULT_TZ)),
    )

    if args.dry_run:
        # Print plan for next ~12 hours.
        now = datetime.now(ZoneInfo(DEFAULT_TZ))
        ctx.logger.info("=== dry run — plan preview ===")
        for i in range(int(args.hours / INTERVAL_HOURS) + 1):
            when = now + timedelta(hours=INTERVAL_HOURS * i)
            label = _window_label(when)
            n_steps = len(_steps_for(label))
            ctx.logger.info("cycle %d @ %s (window=%s, %d steps)",
                            i + 1, when.strftime("%H:%M"), label, n_steps)
        ctx.logger.info("=== dry run complete ===")
        return 0

    try:
        run_loop(ctx)
        return 0
    except KeyboardInterrupt:
        ctx.logger.warning("interrupted — cleaning up monitors")
        prior = _read_lock_pid(ctx.crypto_lock)
        if prior is not None:
            _kill_pid(prior)
        try:
            ctx.crypto_lock.unlink(missing_ok=True)
        except Exception:
            pass
        return 130
    except Exception as exc:  # noqa: BLE001
        ctx.logger.exception("fatal: %s", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
