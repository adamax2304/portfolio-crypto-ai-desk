"""12-hour monitoring scheduler — 6 cycles, every 2 hours.

Runs market analysis + signal tracking + Telegram alerts across crypto and
stocks for a bounded 12-hour session. Designed to run unattended (PC awake)
or via Windows Task Scheduler.

Behaviour
---------
* **6 regular cycles**, one every 2 hours (configurable).
* **Long-horizon context runs ONCE** at the first cycle only (crypto swing report; and, only
  when ``position_framework.scheduler_enabled: true``, the shadow-only stocks-position scan). Old
  stocks swing/invest are DEPRECATED/REMOVED and are not scheduled anywhere.
* **US-window cycles are high-priority**: if a cycle starts inside the US
  pre-market / open / mid / close windows, it appends a 60-minute stocks
  monitor + a background crypto monitor.
* Failure-safe: a failing command is logged, the cycle continues.
* Read-only w.r.t. scoring / agents / thresholds. Never auto-trades.

CLI
---
``--dry-run``                 validate plan + CLI surface, no execution.
``--hours 12``                total session length (default 12).
``--interval-hours 2``        gap between cycles (default 2).
``--minutes N``               override: minute-based total (smoke test).
``--interval-minutes M``      override: minute-based gap (smoke test).
``--skip-reports``            skip the slow scalp/intraday/stocks reports
                              (fast smoke test of the loop + tracking).
``--send-telegram / --no-send-telegram``

Smoke example::

    python -m scripts.run_12h_monitor_schedule --minutes 10 --interval-minutes 5 \\
        --skip-reports --no-send-telegram

Production example::

    python -m scripts.run_12h_monitor_schedule --hours 12 --interval-hours 2 --send-telegram
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

# US equity windows (Nicosia hours, inclusive). US regular session
# 13:30–20:00 UTC = 16:30–23:00 Nicosia (UTC+3).
US_PREMARKET = ("15:30", "16:30")   # ~1h before open
US_OPEN = ("16:30", "17:30")
US_MID = ("18:30", "20:00")
US_CLOSE = ("22:00", "23:00")


def _cli(*args: str) -> list[str]:
    return [sys.executable, "-m", "src.cli", *args]


# (label, argv, kind, duration_min)
Step = tuple[str, list[str], str, int]

REGULAR_REPORTS: list[Step] = [
    ("track-signals (pre)", _cli("track-signals", "--all"), "command", 0),
    ("crypto scalp report", _cli("scalp-report"), "command", 0),
    ("crypto intraday report", _cli("intraday-report"), "command", 0),
    ("stocks intraday report", _cli("stocks-intraday-report"), "command", 0),
]

REGULAR_TAIL: list[Step] = [
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

def _pf_scheduler_enabled() -> bool:
    """config/stocks/position_framework.yaml:scheduler_enabled. Fail-safe → False."""
    try:
        from src.stocks.position_framework.config import load_config as _pf_cfg
        return bool(_pf_cfg().get("scheduler_enabled", False))
    except Exception:
        return False


def _pf_v2_scheduler_enabled() -> bool:
    """config/stocks/position_swing_v2.yaml:scheduler_enabled. Fail-safe to False."""
    try:
        from src.stocks.position_framework.v2_config import load_config as _v2_cfg
        return bool(_v2_cfg().get("scheduler_enabled", False))
    except Exception:
        return False


# Long-horizon context — run ONCE at the first cycle.
# Old stocks swing/invest are DEPRECATED/REMOVED and are NOT scheduled here (never, not even as a
# no-op). The new stocks position framework is SHADOW-ONLY and only scheduled when
# `scheduler_enabled: true`; steps here are fail-open (a failing command is logged, cycle continues).
SWING_INVEST_STEPS: list[Step] = [
    ("crypto swing report (once)", _cli("swing-report"), "command", 0),
]
if _pf_scheduler_enabled():
    SWING_INVEST_STEPS.append(
        ("stocks position framework scan (shadow, once)", _cli("stocks-position-scan"), "command", 0))
if _pf_v2_scheduler_enabled():
    SWING_INVEST_STEPS.extend([
        ("stocks position swing v2 outcome refresh (shadow, once)",
         _cli("stocks-position-v2-outcome-refresh", "--no-update"), "command", 0),
        ("stocks position swing v2 scan (shadow, once)",
         _cli("stocks-position-v2-scan", "--no-update"), "command", 0),
        ("stocks position swing v2 enriched packet (shadow, once)",
         _cli("prepare-stocks-position-v2-analysis"), "command", 0),
    ])

# High-priority US-window monitors (appended before the tail).
US_MONITOR_STEPS: list[Step] = [
    ("crypto monitor (60 min, background)",
     _cli("monitor-watchlist", "--interval", "600", "--iterations", "6"),
     "crypto_monitor", 60),
    ("stocks monitor session (60 min)",
     _cli("stocks-monitor-session", "--minutes", "60", "--interval-minutes", "10",
          "--market-hours-only", "--send-telegram"),
     "stocks_monitor", 60),
]


@dataclass
class RunContext:
    send_telegram: bool
    dry_run: bool
    skip_reports: bool
    started_at: datetime
    logger: logging.Logger = field(default=None)

    def __post_init__(self):
        date_str = self.started_at.astimezone(ZoneInfo(DEFAULT_TZ)).date().isoformat()
        self.day_dir = PROJECT_ROOT / "data" / "scheduled_runs" / f"{date_str}_12h_monitor"
        self.day_dir.mkdir(parents=True, exist_ok=True)
        self.crypto_lock = self.day_dir / "crypto_monitor.pid"
        self.log_path = self.day_dir / "scheduler.log"
        self.cycle_results: list[dict[str, Any]] = []

        log = logging.getLogger("monitor12h")
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
# Window detection
# ---------------------------------------------------------------------------


def _hm(hm: str) -> int:
    h, m = (int(x) for x in hm.split(":"))
    return h * 60 + m


def _is_us_window(now: datetime) -> str | None:
    tz = now.astimezone(ZoneInfo(DEFAULT_TZ))
    minutes = tz.hour * 60 + tz.minute
    for name, (a, b) in (
        ("pre-market", US_PREMARKET), ("open", US_OPEN),
        ("mid", US_MID), ("close", US_CLOSE),
    ):
        if _hm(a) <= minutes <= _hm(b):
            return name
    return None


# ---------------------------------------------------------------------------
# Subprocess + monitor helpers (same pattern as the other schedulers)
# ---------------------------------------------------------------------------


def _truncate(text: str, n: int = 4000) -> str:
    return text if len(text) <= n else text[: n // 2] + "\n…[truncated]…\n" + text[-n // 2:]


def run_command(ctx: RunContext, argv: list[str], *, label: str,
                timeout: int | None = None) -> dict[str, Any]:
    ctx.logger.info("CMD START: %s", label)
    if ctx.dry_run:
        return {"label": label, "ok": True, "exit_code": 0, "duration_s": 0,
                "stdout_tail": "(dry-run)"}
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env.setdefault("PYTHONPATH", str(PROJECT_ROOT))
    t0 = time.monotonic()
    try:
        p = subprocess.run(argv, cwd=PROJECT_ROOT, env=env, capture_output=True,
                           text=True, encoding="utf-8", errors="replace", timeout=timeout)
        dur = time.monotonic() - t0
        out = (p.stdout or "") + (("\n--STDERR--\n" + p.stderr) if p.stderr else "")
        ctx.logger.info("CMD END: %s exit=%d %.1fs", label, p.returncode, dur)
        return {"label": label, "ok": p.returncode == 0, "exit_code": p.returncode,
                "duration_s": round(dur, 1), "stdout_tail": _truncate(out)}
    except subprocess.TimeoutExpired as exc:
        ctx.logger.error("CMD TIMEOUT: %s", label)
        return {"label": label, "ok": False, "exit_code": -1,
                "duration_s": round(time.monotonic() - t0, 1),
                "stdout_tail": f"(timeout)\n{exc}"}
    except Exception as exc:  # noqa: BLE001
        ctx.logger.error("CMD FAILED: %s :: %s", label, exc)
        return {"label": label, "ok": False, "exit_code": -2,
                "duration_s": round(time.monotonic() - t0, 1),
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
            out = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"],
                                 capture_output=True, text=True, timeout=10)
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
        return {"label": label, "ok": True, "exit_code": 0, "duration_s": 0,
                "stdout_tail": "(dry-run)"}
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
        flags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0) if sys.platform == "win32" else 0
        p = subprocess.Popen(argv, cwd=PROJECT_ROOT, env=env,
                             stdout=open(logf, "w", encoding="utf-8"),
                             stderr=subprocess.STDOUT, creationflags=flags)
        ctx.crypto_lock.write_text(str(p.pid))
        ctx.logger.info("CRYPTO MONITOR pid=%d -> %s", p.pid, logf.name)
        return {"label": label, "ok": True, "exit_code": 0, "duration_s": 0,
                "stdout_tail": f"(background pid={p.pid})"}
    except Exception as exc:  # noqa: BLE001
        ctx.logger.error("CRYPTO MONITOR FAILED: %s", exc)
        return {"label": label, "ok": False, "exit_code": -3, "duration_s": 0,
                "stdout_tail": str(exc)}


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


def build_cycle_steps(ctx: RunContext, *, cycle_num: int, us_window: str | None) -> list[Step]:
    steps: list[Step] = []
    # 1. Reports (unless skipped).
    if ctx.skip_reports:
        steps.append(("track-signals (pre)", _cli("track-signals", "--all"), "command", 0))
    else:
        steps.extend(REGULAR_REPORTS)
        # Swing/invest only at cycle 1.
        if cycle_num == 1:
            steps.extend(SWING_INVEST_STEPS)
    # 2. US-window monitors (high-priority), unless skip-reports.
    if us_window and not ctx.skip_reports:
        steps.extend(US_MONITOR_STEPS)
    # 3. Tail (active + stats + post-track).
    steps.extend(REGULAR_TAIL)
    return steps


def execute_cycle(ctx: RunContext, cycle_num: int) -> dict[str, Any]:
    start = datetime.now(ZoneInfo(DEFAULT_TZ))
    us_window = _is_us_window(start)
    priority = "HIGH" if us_window else "regular"
    ctx.logger.info("=" * 60)
    ctx.logger.info("CYCLE %d START (%s, us_window=%s)", cycle_num, priority, us_window)
    ctx.logger.info("=" * 60)

    steps = build_cycle_steps(ctx, cycle_num=cycle_num, us_window=us_window)
    results: list[dict[str, Any]] = []
    for label, argv, kind, duration in steps:
        try:
            if kind == "crypto_monitor":
                results.append(start_crypto_monitor(ctx, argv, label=label))
            elif kind == "stocks_monitor":
                results.append(run_command(ctx, argv, label=label,
                                           timeout=(duration + 10) * 60))
            else:
                results.append(run_command(ctx, argv, label=label, timeout=900))
        except Exception as exc:  # noqa: BLE001
            ctx.logger.error("STEP EXCEPTION: %s", exc)
            results.append({"label": label, "ok": False, "exit_code": -4,
                            "duration_s": 0, "stdout_tail": f"(exception) {exc}"})

    end = datetime.now(ZoneInfo(DEFAULT_TZ))
    ok = sum(1 for r in results if r.get("ok"))
    bad = len(results) - ok

    # Write cycle summary.
    summary_path = ctx.day_dir / f"cycle_{cycle_num}_summary.md"
    lines = [
        f"# Cycle {cycle_num} — {priority}",
        "",
        f"- Started: {start.isoformat()}",
        f"- Finished: {end.isoformat()}",
        f"- US window: {us_window or 'none'}",
        f"- Steps: ok={ok} failed={bad}",
        f"- Swing/invest included: {'yes' if cycle_num == 1 and not ctx.skip_reports else 'no'}",
        "",
        "## Steps",
        "",
    ]
    for i, r in enumerate(results, start=1):
        mark = "✅" if r.get("ok") else "❌"
        lines.append(f"### {i}. {mark} {r['label']} (exit={r.get('exit_code')}, {r.get('duration_s')}s)")
        lines.append("")
        lines.append("```text")
        lines.append((r.get("stdout_tail") or "")[:5000])
        lines.append("```")
        lines.append("")
    summary_path.write_text("\n".join(lines), encoding="utf-8")

    # Telegram summary.
    tg = (f"[12H MONITOR] cycle {cycle_num}/{6} ({priority})\n"
          f"started: {start.strftime('%H:%M')} finished: {end.strftime('%H:%M')}\n"
          f"us_window: {us_window or 'none'}\n"
          f"steps: ok={ok} failed={bad}\n")
    if bad:
        for r in results:
            if not r.get("ok"):
                tg += f"FAIL: {r['label']} (exit={r.get('exit_code')})\n"
    tg_status = send_telegram(ctx, tg)
    ctx.logger.info("CYCLE %d END ok=%d failed=%d telegram=%s", cycle_num, ok, bad, tg_status)

    # Clean background crypto monitor at end of a high-priority cycle.
    if us_window:
        prior = _read_lock_pid(ctx.crypto_lock)
        if prior is not None and _is_pid_alive(prior):
            ctx.logger.info("end-of-cycle: stopping crypto monitor pid=%d", prior)
            _kill_pid(prior)
        try:
            ctx.crypto_lock.unlink(missing_ok=True)
        except Exception:
            pass

    record = {"cycle": cycle_num, "priority": priority, "us_window": us_window,
              "started": start.isoformat(), "finished": end.isoformat(),
              "ok": ok, "failed": bad, "telegram": tg_status}
    ctx.cycle_results.append(record)
    return record


# ---------------------------------------------------------------------------
# Final review
# ---------------------------------------------------------------------------


def write_final_review(ctx: RunContext) -> Path:
    # Pull final stats snapshots (best-effort).
    def _capture(argv: list[str]) -> str:
        try:
            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"
            env.setdefault("PYTHONPATH", str(PROJECT_ROOT))
            p = subprocess.run(argv, cwd=PROJECT_ROOT, env=env, capture_output=True,
                               text=True, encoding="utf-8", errors="replace", timeout=120)
            return (p.stdout or "")[:2000]
        except Exception as exc:  # noqa: BLE001
            return f"(capture failed: {exc})"

    review = ctx.day_dir / "final_12h_review.md"
    root_review = PROJECT_ROOT / "FINAL_12H_MONITOR_REVIEW.md"

    lines = [
        f"# Final 12H Monitor Review — {ctx.started_at.astimezone(ZoneInfo(DEFAULT_TZ)).date()}",
        "",
        f"_Session: {ctx.started_at.isoformat()} → "
        f"{datetime.now(ZoneInfo(DEFAULT_TZ)).isoformat()}_",
        "",
        "## 1. Cycles completed",
        "",
        "| Cycle | Priority | US window | Started | Finished | ok | failed | TG |",
        "|-------|----------|-----------|---------|----------|----|--------|----|",
    ]
    for r in ctx.cycle_results:
        lines.append(
            f"| {r['cycle']} | {r['priority']} | {r['us_window'] or '-'} | "
            f"{r['started'][11:16]} | {r['finished'][11:16]} | {r['ok']} | "
            f"{r['failed']} | {r['telegram']} |"
        )
    lines += [
        "",
        "## 2-8. Final snapshots",
        "",
        "### track-signals --all",
        "```text", _capture(_cli("track-signals", "--all")), "```",
        "",
        "### signal-stats crypto",
        "```text", _capture(_cli("signal-stats", "--asset-class", "crypto")), "```",
        "",
        "### signal-stats stocks",
        "```text", _capture(_cli("signal-stats", "--asset-class", "stocks")), "```",
        "",
        "### dedup (raw vs deduped)",
        "```text", _capture([sys.executable, "-m", "scripts.dedup_signal_stats"])[:1500], "```",
        "",
        "### alert-status",
        "```text",
        _capture(_cli("alert-status", "--asset-class", "stocks")),
        _capture(_cli("alert-status", "--asset-class", "crypto")),
        "```",
        "",
        "## 9-13. Interpretation (manual)",
        "- Best/worst setups, filter strictness, A/B meaningfulness: review the "
        "per-cycle summaries + signal-stats above. The scheduler does NOT "
        "auto-judge tradeability — that is a human read.",
        "- Crypto filters: if crypto produced 0 A/B during a CLEAN uptrend for "
        "the whole session, investigate. During downtrend, 0 A/B is correct.",
        "- Stocks raw stats are inflated by repeat registrations; trust the "
        "deduped view above.",
        "",
        "## 14. Safety confirmation",
        "- No auto-trades. No scoring/threshold/agent/architecture changes. "
        "Only existing CLI commands invoked. Telegram A/B-only via CLI gates.",
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


def run_loop(ctx: RunContext, *, total_seconds: float, interval_seconds: float) -> None:
    deadline = ctx.started_at + timedelta(seconds=total_seconds)
    ctx.logger.info("12h monitor boot — total=%.0fs interval=%.0fs deadline=%s telegram=%s skip_reports=%s",
                    total_seconds, interval_seconds, deadline.isoformat(),
                    ctx.send_telegram, ctx.skip_reports)
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
        execute_cycle(ctx, cycle_num)
        next_at = datetime.now(ZoneInfo(DEFAULT_TZ)) + timedelta(seconds=interval_seconds)
        if datetime.now(ZoneInfo(DEFAULT_TZ)) >= deadline:
            break
    write_final_review(ctx)
    ctx.logger.info("12h monitor session complete — %d cycle(s)", cycle_num)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--hours", type=float, default=12.0)
    ap.add_argument("--interval-hours", type=float, default=2.0)
    ap.add_argument("--minutes", type=float, default=None,
                    help="Override total length in minutes (smoke test).")
    ap.add_argument("--interval-minutes", type=float, default=None,
                    help="Override interval in minutes (smoke test).")
    ap.add_argument("--skip-reports", action="store_true",
                    help="Skip slow reports — fast loop/tracking smoke test.")
    ap.add_argument("--dry-run", action="store_true")
    tg = ap.add_mutually_exclusive_group()
    tg.add_argument("--send-telegram", dest="send_tg", action="store_true")
    tg.add_argument("--no-send-telegram", dest="send_tg", action="store_false")
    ap.set_defaults(send_tg=True)
    args = ap.parse_args()

    total_seconds = (args.minutes * 60) if args.minutes is not None else (args.hours * 3600)
    interval_seconds = (args.interval_minutes * 60) if args.interval_minutes is not None \
        else (args.interval_hours * 3600)

    ctx = RunContext(
        send_telegram=bool(args.send_tg) and not args.dry_run,
        dry_run=args.dry_run, skip_reports=args.skip_reports,
        started_at=datetime.now(ZoneInfo(DEFAULT_TZ)),
    )

    if args.dry_run:
        ctx.logger.info("=== DRY RUN ===")
        n_cycles = max(1, int(total_seconds / interval_seconds) + 1)
        now = datetime.now(ZoneInfo(DEFAULT_TZ))
        for i in range(n_cycles):
            when = now + timedelta(seconds=interval_seconds * i)
            usw = _is_us_window(when)
            steps = build_cycle_steps(ctx, cycle_num=i + 1, us_window=usw)
            ctx.logger.info("cycle %d @ %s (us=%s, %d steps%s)",
                            i + 1, when.strftime("%H:%M"), usw or "none", len(steps),
                            ", +long-horizon" if i == 0 and not ctx.skip_reports else "")
        # Validate CLI surface.
        ctx.logger.info("--- validating CLI ---")
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        env.setdefault("PYTHONPATH", str(PROJECT_ROOT))
        # Old stocks-swing-report / stocks-invest-report are DEPRECATED/REMOVED and no longer
        # scheduled; validate the NEW shadow-only stocks-position commands instead.
        for cmd in ("track-signals", "scalp-report", "intraday-report",
                    "stocks-intraday-report", "swing-report", "stocks-position-scan",
                    "stocks-position-report", "stocks-position-v2-scan",
                    "stocks-position-v2-outcome-refresh", "stocks-position-v2-report",
                    "prepare-stocks-position-v2-analysis", "active-signals", "signal-stats",
                    "monitor-watchlist", "stocks-monitor-session", "alert-status"):
            try:
                p = subprocess.run([sys.executable, "-m", "src.cli", cmd, "--help"],
                                   cwd=PROJECT_ROOT, env=env, capture_output=True,
                                   text=True, encoding="utf-8", errors="replace",
                                   timeout=60)
                ctx.logger.info("validate %-24s %s", cmd, "OK" if p.returncode == 0 else "FAIL")
            except Exception as exc:  # noqa: BLE001
                ctx.logger.warning("validate %s raised %s", cmd, exc)
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
