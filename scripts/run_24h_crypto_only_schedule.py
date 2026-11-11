"""24-hour CRYPTO-ONLY scheduler — 12 cycles, every 2 hours.

Weekend validation run after the PART 1–5 fix round. Runs ONLY:

* `track-signals --all` (before + after);
* `scalp-report`;
* `intraday-report`;
* a bounded `monitor-watchlist` window (default 90 min) per cycle;
* `active-signals --asset-class crypto`;
* `signal-stats --asset-class crypto`;
* the untracked-legacy detector;
* `review-day --write-obsidian` at end of each cycle (UTC date-stamped).

This scheduler **never invokes** any stocks command:
``stocks-intraday-report``, ``stocks-position-scan``,
``stocks-position-report``, ``stocks-monitor-session``,
``alert-status --asset-class stocks``, etc. — they're explicitly
out of scope for this weekend run. (Old stocks swing/invest are
DEPRECATED/REMOVED and are not scheduled anywhere.)

Safety
------
* Read-only with respect to scoring / agents / thresholds / strategy.
* No auto-trade; the project has no execution layer.
* Crypto monitor lock prevents duplicate background monitors.
* If a previous lock holds a stale PID, it is killed (consistent with
  the existing 12h scheduler) before starting a new one.
* Cycle failures are logged; the loop continues.

CLI
---
``--dry-run``                 validate the plan + CLI surface, no execution.
``--hours 24``                total session length (default 24).
``--interval-hours 2``        gap between cycles (default 2).
``--minutes N``               override total minutes (smoke test).
``--interval-minutes M``      override interval minutes (smoke test).
``--monitor-minutes 90``      crypto monitor window length per cycle.
``--skip-reports``            skip slow reports — fast loop/tracking smoke test.
``--send-telegram /
  --no-send-telegram``         enable Telegram summaries.

Examples
--------

Smoke (2 short cycles, no Telegram)::

    python -m scripts.run_24h_crypto_only_schedule \
        --minutes 6 --interval-minutes 3 --monitor-minutes 1 \
        --skip-reports --no-send-telegram

Production (24h, 12 cycles, Telegram on)::

    python -m scripts.run_24h_crypto_only_schedule \
        --hours 24 --interval-hours 2 --monitor-minutes 90 --send-telegram
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
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo


def _utc_today_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TZ = "Asia/Nicosia"


# (label, argv, kind, duration_min)
Step = tuple[str, list[str], str, int]


def _cli(*args: str) -> list[str]:
    return [sys.executable, "-m", "src.cli", *args]


def _script(*args: str) -> list[str]:
    return [sys.executable, "-m", *args]


# ---------------------------------------------------------------------------
# Steps — crypto only
# ---------------------------------------------------------------------------


def regular_reports() -> list[Step]:
    """Steps run at the start of every cycle."""

    return [
        ("track-signals (pre)", _cli("track-signals", "--all"), "command", 0),
        ("crypto scalp report", _cli("scalp-report"), "command", 0),
        ("crypto intraday report", _cli("intraday-report"), "command", 0),
    ]


def regular_tail() -> list[Step]:
    """Steps run at the end of every cycle."""

    return [
        ("active-signals (crypto)",
         _cli("active-signals", "--asset-class", "crypto", "--limit", "20"),
         "command", 0),
        ("signal-stats (crypto)",
         _cli("signal-stats", "--asset-class", "crypto"),
         "command", 0),
        ("untracked-legacy detector",
         _script("scripts.detect_untracked_legacy_alerts",
                 "--since", _utc_today_str()),
         "command", 0),
        ("track-signals (post)", _cli("track-signals", "--all"), "command", 0),
        ("daily review (obsidian)",
         _cli("review-day", "--no-print", "--write-obsidian"),
         "command", 0),
    ]


def crypto_monitor_step(monitor_minutes: int) -> Step:
    """Bounded crypto monitor — runs in the background; the launcher
    tracks the PID via a lockfile and stops it at the end of the cycle.

    The CLI supports ``--duration-hours``; we pass fractional hours.
    Interval is 5 minutes (300 s).
    """

    hours = max(monitor_minutes / 60.0, 1.0 / 60.0)
    return (
        f"crypto monitor ({monitor_minutes} min, background)",
        _cli(
            "monitor-watchlist",
            "--interval", "300",
            "--duration-hours", f"{hours:.3f}",
        ),
        "crypto_monitor",
        monitor_minutes,
    )


# ---------------------------------------------------------------------------
# Run context
# ---------------------------------------------------------------------------


@dataclass
class RunContext:
    send_telegram: bool
    dry_run: bool
    skip_reports: bool
    monitor_minutes: int
    started_at: datetime
    logger: logging.Logger = field(default=None)

    def __post_init__(self):
        date_str = self.started_at.astimezone(ZoneInfo(DEFAULT_TZ)).date().isoformat()
        self.day_dir = (
            PROJECT_ROOT / "data" / "scheduled_runs" / f"{date_str}_24h_crypto_only"
        )
        self.day_dir.mkdir(parents=True, exist_ok=True)
        self.crypto_lock = self.day_dir / "crypto_monitor.pid"
        self.log_path = self.day_dir / "scheduler.log"
        self.cycle_results: list[dict[str, Any]] = []

        log = logging.getLogger("crypto24h")
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
# Subprocess helpers — same pattern as the 12h scheduler.
# ---------------------------------------------------------------------------


def _truncate(text: str, n: int = 4000) -> str:
    if len(text) <= n:
        return text
    return text[: n // 2] + "\n…[truncated]…\n" + text[-n // 2:]


def run_command(
    ctx: RunContext,
    argv: list[str],
    *,
    label: str,
    timeout: int | None = None,
) -> dict[str, Any]:
    ctx.logger.info("CMD START: %s", label)
    if ctx.dry_run:
        return {
            "label": label,
            "ok": True,
            "exit_code": 0,
            "duration_s": 0,
            "stdout_tail": "(dry-run)",
        }
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env.setdefault("PYTHONPATH", str(PROJECT_ROOT))
    t0 = time.monotonic()
    try:
        p = subprocess.run(
            argv,
            cwd=PROJECT_ROOT,
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
        dur = time.monotonic() - t0
        out = (p.stdout or "") + (("\n--STDERR--\n" + p.stderr) if p.stderr else "")
        ctx.logger.info("CMD END: %s exit=%d %.1fs", label, p.returncode, dur)
        return {
            "label": label,
            "ok": p.returncode == 0,
            "exit_code": p.returncode,
            "duration_s": round(dur, 1),
            "stdout_tail": _truncate(out),
        }
    except subprocess.TimeoutExpired as exc:
        ctx.logger.error("CMD TIMEOUT: %s", label)
        return {
            "label": label,
            "ok": False,
            "exit_code": -1,
            "duration_s": round(time.monotonic() - t0, 1),
            "stdout_tail": f"(timeout)\n{exc}",
        }
    except Exception as exc:  # noqa: BLE001
        ctx.logger.error("CMD FAILED: %s :: %s", label, exc)
        return {
            "label": label,
            "ok": False,
            "exit_code": -2,
            "duration_s": round(time.monotonic() - t0, 1),
            "stdout_tail": f"(exception) {exc}\n{traceback.format_exc()}",
        }


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
                capture_output=True,
                text=True,
                timeout=10,
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
            capture_output=True,
            text=True,
            timeout=15,
        )
    else:
        try:
            os.kill(pid, signal.SIGTERM)
        except OSError:
            pass


def start_crypto_monitor(
    ctx: RunContext,
    argv: list[str],
    *,
    label: str,
) -> dict[str, Any]:
    if ctx.dry_run:
        return {
            "label": label,
            "ok": True,
            "exit_code": 0,
            "duration_s": 0,
            "stdout_tail": "(dry-run)",
        }
    prior = _read_lock_pid(ctx.crypto_lock)
    if prior is not None and _is_pid_alive(prior):
        ctx.logger.warning("stale crypto monitor PID=%d — killing", prior)
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
        flags = (
            getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
            if sys.platform == "win32"
            else 0
        )
        p = subprocess.Popen(
            argv,
            cwd=PROJECT_ROOT,
            env=env,
            stdout=open(logf, "w", encoding="utf-8"),
            stderr=subprocess.STDOUT,
            creationflags=flags,
        )
        ctx.crypto_lock.write_text(str(p.pid))
        ctx.logger.info("CRYPTO MONITOR pid=%d -> %s", p.pid, logf.name)
        return {
            "label": label,
            "ok": True,
            "exit_code": 0,
            "duration_s": 0,
            "stdout_tail": f"(background pid={p.pid})",
        }
    except Exception as exc:  # noqa: BLE001
        ctx.logger.error("CRYPTO MONITOR FAILED: %s", exc)
        return {
            "label": label,
            "ok": False,
            "exit_code": -3,
            "duration_s": 0,
            "stdout_tail": str(exc),
        }


def send_telegram(ctx: RunContext, text: str) -> str:
    if not ctx.send_telegram or ctx.dry_run:
        return "skipped"
    capped = text if len(text) <= 3800 else text[:3700] + "\n…[truncated]…"
    try:
        sys.path.insert(0, str(PROJECT_ROOT))
        from src.notifiers.telegram import TelegramNotifier  # type: ignore

        n = TelegramNotifier(PROJECT_ROOT / "config" / "notifications.yaml")
        if not n.enabled or not n.chat_id:
            return "skipped"
        n.send(capped, parse_mode="")  # plain text — avoids Markdown 400s
        return "sent"
    except Exception as exc:  # noqa: BLE001
        ctx.logger.warning("Telegram failed: %s", exc)
        return f"failed:{exc.__class__.__name__}"


# ---------------------------------------------------------------------------
# Cycle assembly + execution
# ---------------------------------------------------------------------------


def build_cycle_steps(ctx: RunContext, *, cycle_num: int) -> list[Step]:
    steps: list[Step] = []
    if ctx.skip_reports:
        steps.append(
            ("track-signals (pre)", _cli("track-signals", "--all"), "command", 0)
        )
    else:
        steps.extend(regular_reports())
        # Background crypto monitor — bounded per cycle.
        steps.append(crypto_monitor_step(ctx.monitor_minutes))
    steps.extend(regular_tail())
    return steps


def execute_cycle(ctx: RunContext, cycle_num: int, total_cycles: int) -> dict[str, Any]:
    start = datetime.now(ZoneInfo(DEFAULT_TZ))
    ctx.logger.info("=" * 60)
    ctx.logger.info("CYCLE %d/%d START (crypto-only, weekend)", cycle_num, total_cycles)
    ctx.logger.info("=" * 60)

    steps = build_cycle_steps(ctx, cycle_num=cycle_num)
    results: list[dict[str, Any]] = []
    for label, argv, kind, duration in steps:
        try:
            if kind == "crypto_monitor":
                results.append(start_crypto_monitor(ctx, argv, label=label))
            else:
                results.append(run_command(ctx, argv, label=label, timeout=900))
        except Exception as exc:  # noqa: BLE001
            ctx.logger.error("STEP EXCEPTION: %s", exc)
            results.append(
                {
                    "label": label,
                    "ok": False,
                    "exit_code": -4,
                    "duration_s": 0,
                    "stdout_tail": f"(exception) {exc}",
                }
            )

    end = datetime.now(ZoneInfo(DEFAULT_TZ))
    ok = sum(1 for r in results if r.get("ok"))
    bad = len(results) - ok

    summary_path = ctx.day_dir / f"cycle_{cycle_num:02d}_summary.md"
    lines = [
        f"# Cycle {cycle_num}/{total_cycles} — crypto-only (weekend)",
        "",
        f"- Started: {start.isoformat()}",
        f"- Finished: {end.isoformat()}",
        f"- Steps: ok={ok} failed={bad}",
        f"- Monitor window: {ctx.monitor_minutes} min",
        "",
        "## Steps",
        "",
    ]
    for i, r in enumerate(results, start=1):
        mark = "OK" if r.get("ok") else "FAIL"
        lines.append(
            f"### {i}. [{mark}] {r['label']} "
            f"(exit={r.get('exit_code')}, {r.get('duration_s')}s)"
        )
        lines.append("")
        lines.append("```text")
        lines.append((r.get("stdout_tail") or "")[:5000])
        lines.append("```")
        lines.append("")
    summary_path.write_text("\n".join(lines), encoding="utf-8")

    tg = (
        f"[24H CRYPTO-ONLY] cycle {cycle_num}/{total_cycles}\n"
        f"started: {start.strftime('%H:%M')} finished: {end.strftime('%H:%M')}\n"
        f"steps: ok={ok} failed={bad}\n"
    )
    if bad:
        for r in results:
            if not r.get("ok"):
                tg += f"FAIL: {r['label']} (exit={r.get('exit_code')})\n"
    tg_status = send_telegram(ctx, tg)
    ctx.logger.info(
        "CYCLE %d END ok=%d failed=%d telegram=%s",
        cycle_num,
        ok,
        bad,
        tg_status,
    )

    # Always stop the background crypto monitor at end of cycle so the
    # next one starts fresh and we never hold two monitors at once.
    prior = _read_lock_pid(ctx.crypto_lock)
    if prior is not None and _is_pid_alive(prior):
        ctx.logger.info("end-of-cycle: stopping crypto monitor pid=%d", prior)
        _kill_pid(prior)
    try:
        ctx.crypto_lock.unlink(missing_ok=True)
    except Exception:
        pass

    record = {
        "cycle": cycle_num,
        "started": start.isoformat(),
        "finished": end.isoformat(),
        "ok": ok,
        "failed": bad,
        "telegram": tg_status,
    }
    ctx.cycle_results.append(record)
    return record


# ---------------------------------------------------------------------------
# Final review
# ---------------------------------------------------------------------------


def write_final_review(ctx: RunContext) -> Path:
    def _capture(argv: list[str]) -> str:
        try:
            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"
            env.setdefault("PYTHONPATH", str(PROJECT_ROOT))
            p = subprocess.run(
                argv,
                cwd=PROJECT_ROOT,
                env=env,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=180,
            )
            return (p.stdout or "")[:2500]
        except Exception as exc:  # noqa: BLE001
            return f"(capture failed: {exc})"

    review = ctx.day_dir / "final_24h_crypto_only_review.md"
    root_review = PROJECT_ROOT / "FINAL_24H_CRYPTO_ONLY_REVIEW.md"

    lines = [
        "# Final 24H Crypto-Only Review — "
        f"{ctx.started_at.astimezone(ZoneInfo(DEFAULT_TZ)).date()}",
        "",
        f"_Session: {ctx.started_at.isoformat()} → "
        f"{datetime.now(ZoneInfo(DEFAULT_TZ)).isoformat()}_",
        "",
        "## 1. Cycles completed",
        "",
        "| Cycle | Started | Finished | ok | failed | TG |",
        "|-------|---------|----------|----|--------|----|",
    ]
    for r in ctx.cycle_results:
        lines.append(
            f"| {r['cycle']} | {r['started'][11:16]} | "
            f"{r['finished'][11:16]} | {r['ok']} | {r['failed']} | "
            f"{r['telegram']} |"
        )
    today = _utc_today_str()
    lines += [
        "",
        "## 2. Final track-signals snapshot",
        "",
        "```text",
        _capture(_cli("track-signals", "--all")),
        "```",
        "",
        "## 3. Final signal-stats (crypto only)",
        "",
        "```text",
        _capture(_cli("signal-stats", "--asset-class", "crypto")),
        "```",
        "",
        "## 4. Active crypto signals",
        "",
        "```text",
        _capture(_cli("active-signals", "--asset-class", "crypto", "--limit", "40")),
        "```",
        "",
        "## 5. Untracked legacy alert detector",
        "",
        "```text",
        _capture(_script("scripts.detect_untracked_legacy_alerts", "--since", today)),
        "```",
        "",
        "## 6. Daily review (obsidian)",
        "",
        "```text",
        _capture(_cli("review-day", "--no-print", "--write-obsidian")),
        "```",
        "",
        "## 7–14. Manual interpretation",
        "",
        "- **Best signals**: review per-cycle summaries + signal-stats above.",
        "- **Worst signals**: ditto.",
        "- **Shorts vs longs**: signal-stats breakdown by direction.",
        "- **Filter strictness**: if 0 A/B during a clean trend day, "
        "  investigate; if 0 A/B during chop/Extreme Fear, that's correct.",
        "- **Weekend mode effect**: compare A-tier counts vs the prior weekday "
        "  run; weekend penalty should reduce upgrades.",
        "- **Final verdict**: crypto scalp useful / watchlist / no trade; "
        "  crypto intraday useful / watchlist / no trade; overall crypto edge "
        "  unproven / promising / weak. THIS IS A HUMAN READ — the scheduler "
        "  does not auto-judge.",
        "",
        "## Safety",
        "",
        "- No auto-trade (no execution layer exists).",
        "- No scoring / threshold / agent / strategy changes.",
        "- Stocks pipeline NEVER invoked during this run.",
        "- Telegram alerts gated by PART 1 (registration-before-alert) and "
        "  the existing notifier cooldown.",
        "",
    ]
    content = "\n".join(lines)
    review.write_text(content, encoding="utf-8")
    root_review.write_text(content, encoding="utf-8")
    ctx.logger.info("Final review written: %s (and %s)", review, root_review)
    return review


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------


def run_loop(
    ctx: RunContext,
    *,
    total_seconds: float,
    interval_seconds: float,
) -> None:
    deadline = ctx.started_at + timedelta(seconds=total_seconds)
    total_cycles = max(1, int(total_seconds / interval_seconds))
    ctx.logger.info(
        "24h crypto-only boot — total=%.0fs interval=%.0fs cycles=%d "
        "deadline=%s telegram=%s skip_reports=%s monitor_min=%d",
        total_seconds,
        interval_seconds,
        total_cycles,
        deadline.isoformat(),
        ctx.send_telegram,
        ctx.skip_reports,
        ctx.monitor_minutes,
    )
    cycle_num = 0
    next_at = datetime.now(ZoneInfo(DEFAULT_TZ))
    while True:
        now = datetime.now(ZoneInfo(DEFAULT_TZ))
        if cycle_num > 0 and now >= deadline:
            break
        if now < next_at:
            time.sleep(min(30, (next_at - now).total_seconds()))
            continue
        cycle_num += 1
        execute_cycle(ctx, cycle_num, total_cycles)
        next_at = datetime.now(ZoneInfo(DEFAULT_TZ)) + timedelta(seconds=interval_seconds)
        if datetime.now(ZoneInfo(DEFAULT_TZ)) >= deadline:
            break
    write_final_review(ctx)
    ctx.logger.info("24h crypto-only session complete — %d cycle(s)", cycle_num)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--hours", type=float, default=24.0)
    ap.add_argument("--interval-hours", type=float, default=2.0)
    ap.add_argument(
        "--minutes",
        type=float,
        default=None,
        help="Override total length in minutes (smoke test).",
    )
    ap.add_argument(
        "--interval-minutes",
        type=float,
        default=None,
        help="Override interval in minutes (smoke test).",
    )
    ap.add_argument(
        "--monitor-minutes",
        type=int,
        default=90,
        help="Bounded crypto monitor window per cycle (default 90 min).",
    )
    ap.add_argument(
        "--skip-reports",
        action="store_true",
        help="Skip slow reports — fast loop/tracking smoke test.",
    )
    ap.add_argument("--dry-run", action="store_true")
    tg = ap.add_mutually_exclusive_group()
    tg.add_argument("--send-telegram", dest="send_tg", action="store_true")
    tg.add_argument("--no-send-telegram", dest="send_tg", action="store_false")
    ap.set_defaults(send_tg=True)
    args = ap.parse_args()

    total_seconds = (
        (args.minutes * 60) if args.minutes is not None else (args.hours * 3600)
    )
    interval_seconds = (
        (args.interval_minutes * 60)
        if args.interval_minutes is not None
        else (args.interval_hours * 3600)
    )

    ctx = RunContext(
        send_telegram=bool(args.send_tg) and not args.dry_run,
        dry_run=args.dry_run,
        skip_reports=args.skip_reports,
        monitor_minutes=int(args.monitor_minutes),
        started_at=datetime.now(ZoneInfo(DEFAULT_TZ)),
    )

    if args.dry_run:
        ctx.logger.info("=== DRY RUN ===")
        n_cycles = max(1, int(total_seconds / interval_seconds))
        now = datetime.now(ZoneInfo(DEFAULT_TZ))
        for i in range(n_cycles):
            when = now + timedelta(seconds=interval_seconds * i)
            steps = build_cycle_steps(ctx, cycle_num=i + 1)
            ctx.logger.info(
                "cycle %d @ %s (%d steps)",
                i + 1,
                when.strftime("%H:%M"),
                len(steps),
            )
        # Validate CLI surface — crypto only.
        ctx.logger.info("--- validating crypto CLI surface ---")
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        env.setdefault("PYTHONPATH", str(PROJECT_ROOT))
        for cmd in (
            "track-signals",
            "scalp-report",
            "intraday-report",
            "active-signals",
            "signal-stats",
            "monitor-watchlist",
            "review-day",
        ):
            try:
                p = subprocess.run(
                    [sys.executable, "-m", "src.cli", cmd, "--help"],
                    cwd=PROJECT_ROOT,
                    env=env,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    timeout=60,
                )
                ctx.logger.info(
                    "validate %-22s %s",
                    cmd,
                    "OK" if p.returncode == 0 else "FAIL",
                )
            except Exception as exc:  # noqa: BLE001
                ctx.logger.warning("validate %s raised %s", cmd, exc)
        # Confirm scheduler does NOT mention stocks commands.
        # Crypto-only weekend run: NO stocks commands in the plan. Old swing/invest are
        # deprecated/removed; the new shadow-only stocks-position commands are also out of scope.
        forbidden = {
            "stocks-intraday-report",
            "stocks-position-scan",
            "stocks-position-report",
            "stocks-monitor-session",
        }
        rendered = " ".join(
            " ".join(s[1]) for s in build_cycle_steps(ctx, cycle_num=1)
        )
        offenders = [c for c in forbidden if c in rendered]
        if offenders:
            ctx.logger.error("stocks command found in steps: %s", offenders)
            return 2
        ctx.logger.info("--- stocks-disabled check OK (no stocks commands in plan) ---")
        ctx.logger.info("=== dry run complete ===")
        return 0

    try:
        run_loop(ctx, total_seconds=total_seconds, interval_seconds=interval_seconds)
        return 0
    except KeyboardInterrupt:
        ctx.logger.warning("interrupted — cleaning up")
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
