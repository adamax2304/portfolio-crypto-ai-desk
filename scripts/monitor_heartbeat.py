"""Monitor / scheduler heartbeat watchdog (operational).

Independent of the scheduler so it can warn when the scheduler dies. Checks last
cycle time, process liveness, last Telegram/alert, DB + intelligence/archive/catalyst
freshness, and circuit-breaker dry-run availability; sends a COMPACT Telegram status
(start / cycle) or a deduped WARNING (no-cycle / process-stopped / stale). With
--auto-restart it relaunches the scheduler via start_monitor_scheduler.ps1 (idempotent,
so it never starts a duplicate). Read-only on trading data; NEVER touches trade logic.

Usage:
  python -m scripts.monitor_heartbeat --event start
  python -m scripts.monitor_heartbeat --event check --auto-restart
  python -m scripts.monitor_heartbeat --event cycle
"""
from __future__ import annotations

import argparse
import gzip
import json
import re
import shutil
import sqlite3
import subprocess
import sys
import os
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

TRADING_DB = ROOT / "db" / "crypto_ai_desk.sqlite"
INTEL_DB = ROOT / "data" / "intelligence" / "intelligence.sqlite"
MARKET_INTEL_DB = ROOT / "data" / "intelligence" / "market_intelligence.sqlite"
DERIVATIVES_HEARTBEAT = ROOT / "data" / "runtime_locks" / "derivatives_monitor.heartbeat.json"
SCHED_LOG = ROOT / "data" / "autostart" / "scheduler.log"
STATE = ROOT / "data" / "autostart" / "heartbeat_state.json"
LAUNCHER = ROOT / "scripts" / "start_monitor_scheduler.ps1"
PROCESS_LOG_ROTATE_BYTES = 8 * 1024 * 1024


def _rotate_process_log(
    path: Path, *, max_bytes: int = PROCESS_LOG_ROTATE_BYTES, keep: int = 4
) -> Path | None:
    """Compress a stopped worker's oversized append log before restart."""
    try:
        if not path.exists() or path.stat().st_size <= max(0, int(max_bytes)):
            return None
        archive_dir = path.parent / "archive"
        archive_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        target = archive_dir / f"{path.name}.{stamp}.{os.getpid()}.gz"
        with path.open("rb") as source, gzip.open(target, "wb", compresslevel=6) as output:
            shutil.copyfileobj(source, output, length=1024 * 1024)
        path.unlink()
        archives = sorted(
            archive_dir.glob(f"{path.name}.*.gz"),
            key=lambda item: item.stat().st_mtime,
            reverse=True,
        )
        for old in archives[max(1, int(keep)):]:
            old.unlink(missing_ok=True)
        return target
    except OSError:
        # Log rotation must never prevent a monitor restart.
        return None


@contextmanager
def _restart_lease(name: str, *, stale_seconds: float = 120.0):
    """Serialize watchdog restarts so concurrent health checks cannot spawn peers."""
    path = ROOT / "data" / "runtime_locks" / f"{name}.restart.lock"
    path.parent.mkdir(parents=True, exist_ok=True)
    acquired = False
    descriptor = None
    for _ in range(2):
        try:
            descriptor = os.open(str(path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(descriptor, f"{os.getpid()} {time.time()}".encode("ascii"))
            acquired = True
            break
        except FileExistsError:
            try:
                if time.time() - path.stat().st_mtime > stale_seconds:
                    path.unlink(missing_ok=True)
                    continue
            except OSError:
                pass
            break
    try:
        yield acquired
    finally:
        if descriptor is not None:
            os.close(descriptor)
        if acquired:
            path.unlink(missing_ok=True)

INTERVAL_MIN = 120      # expected cycle interval
GRACE_MIN = 50          # + monitor window; warn only after interval+grace with no cycle
DERIVED_GRACE_MIN = 90  # derived steps run late; warn after a missed cycle, not mid-cycle
WARN_COOLDOWN_MIN = 60  # don't repeat the same warning more often than this
NY = ZoneInfo("America/New_York")
STOCK_WORKER_START_MINUTE_ET = 8 * 60 + 50
STOCK_WORKER_PREOPEN_CONTROL_END_MINUTE_ET = 9 * 60 + 25
STOCK_WORKER_END_MINUTE_ET = 16 * 60 + 5
MEXC_CANARY_HEARTBEAT_GRACE_SEC = 120
# A full fast-entry tick can take a few minutes when many pending symbols need
# cross-exchange candle refresh. The worker publishes a tick heartbeat before
# the I/O starts, so this detects a true stall without starting duplicate
# monitors during a legitimate heavy cycle.
PENDING_MONITOR_LEASE_GRACE_SEC = 300
# A public Telegram HTML cycle can take several minutes because every configured
# channel is fetched independently.  Treat it as stalled only after a full cycle
# plus its next poll interval, rather than mistaking an in-progress cycle for a
# dead listener.
TELEGRAM_PUBLIC_FALLBACK_GRACE_SEC = 12 * 60
DERIVATIVES_HEARTBEAT_GRACE_SEC = 6 * 60
DERIVATIVES_DATA_GRACE_MIN = 15
PREUS_BASELINE_START_MINUTE_ET = 8 * 60 + 50
PREUS_BASELINE_END_MINUTE_ET = 9 * 60 + 12
LLM_QUALITY_TASK_NAME = "CryptoAIDesk_LLMQuality"
# Under memory pressure Windows can spend several minutes paging in a new
# Python worker.  Do not stack another replacement on top of a process that is
# visibly alive but has not had a fair chance to publish its first heartbeat.
MONITOR_STARTUP_GRACE_SEC = 5 * 60


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _age_min(iso: str | None) -> float | None:
    if not iso:
        return None
    try:
        dt = datetime.fromisoformat(str(iso).replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return (_now() - dt).total_seconds() / 60.0
    except Exception:
        return None


def _monitor_startup_age_seconds(status: dict | None) -> float | None:
    """Return the youngest matching worker age, if process metadata is readable."""
    try:
        import psutil  # type: ignore

        ages = []
        for pid in (status or {}).get("pids", []):
            try:
                ages.append(max(0.0, time.time() - psutil.Process(int(pid)).create_time()))
            except Exception:
                continue
        return min(ages) if ages else None
    except Exception:
        return None


def _monitor_is_starting(status: dict | None) -> bool:
    age = _monitor_startup_age_seconds(status)
    return age is not None and age <= MONITOR_STARTUP_GRACE_SEC


def scheduler_status() -> tuple[bool | None, float | None]:
    """Return (alive, uptime_minutes). uptime is the oldest matching process's age
    (None if not alive/unknown). Used to avoid false 'stale' alarms right after start."""
    try:
        out = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | "
             "Where-Object { $_.CommandLine -like '*run_default_market_schedule*' } | "
             "ForEach-Object { $_.CreationDate.ToUniversalTime().ToString('o') }"],
            capture_output=True, text=True, timeout=20)
        lines = [ln.strip() for ln in (out.stdout or "").splitlines() if ln.strip()]
        if not lines:
            return False, None
        ages = [_age_min(ln) for ln in lines]
        ages = [a for a in ages if a is not None]
        return True, (max(ages) if ages else None)
    except Exception:
        return None, None  # unknown


def stock_monitor_status() -> dict:
    """Report the dedicated stocks monitor independently of the long scheduler.

    The scheduler can be alive while its stock child is absent. This matters
    because the pre-US candidate review has a short, time-sensitive window.
    """
    try:
        out = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | "
             "Where-Object { $_.CommandLine -like '*stocks-monitor-session*' } | "
             "ForEach-Object { \"$($_.ProcessId)|$($_.CreationDate.ToUniversalTime().ToString('o'))\" }"],
            capture_output=True, text=True, timeout=20,
        )
        processes = []
        for line in (out.stdout or "").splitlines():
            pid_raw, _, created_at = line.strip().partition("|")
            if pid_raw.isdigit():
                processes.append({"pid": int(pid_raw), "created_at": created_at or None})
        return {"alive": bool(processes), "pids": [p["pid"] for p in processes], "processes": processes}
    except Exception:
        return {"alive": None, "pids": [], "processes": []}


def pending_monitor_status() -> dict:
    """Report the crypto fast-entry worker independently of the scheduler."""
    try:
        out = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | "
             "Where-Object { $_.CommandLine -like '*-m src.cli pending-monitor*' } | "
             "ForEach-Object { $_.ProcessId }"],
            capture_output=True, text=True, timeout=20,
        )
        pids = [int(line.strip()) for line in (out.stdout or "").splitlines()
                if line.strip().isdigit()]
        status = {"alive": bool(pids), "pids": pids, "required": True}
        heartbeat_path = ROOT / "data" / "runtime_locks" / "pending_monitor.heartbeat.json"
        try:
            payload = json.loads(heartbeat_path.read_text(encoding="utf-8"))
            heartbeat_pid = int(payload.get("pid") or 0)
            heartbeat_at = str(payload.get("at") or "") or None
            age_min = _age_min(heartbeat_at)
            status.update({
                "heartbeat_at": heartbeat_at,
                "heartbeat_pid": heartbeat_pid or None,
                "heartbeat_stage": payload.get("stage"),
                "heartbeat_tick": payload.get("tick"),
                "heartbeat_age_seconds": None if age_min is None else round(age_min * 60.0, 3),
            })
            # Ignore a heartbeat from a replaced process. The runtime PID file
            # is intentionally not used: it records startup only, not progress.
            if heartbeat_pid in pids and age_min is not None:
                status["lease_age_seconds"] = round(age_min * 60.0, 3)
                status["lease_fresh"] = age_min * 60.0 <= PENDING_MONITOR_LEASE_GRACE_SEC
                return status
        except (FileNotFoundError, ValueError, TypeError, json.JSONDecodeError):
            pass
        lock = ROOT / ".locks" / "pending_monitor_leader_crypto.lock"
        try:
            age = max(0.0, time.time() - lock.stat().st_mtime)
            status["lease_age_seconds"] = round(age, 3)
            status["lease_fresh"] = age <= PENDING_MONITOR_LEASE_GRACE_SEC
        except FileNotFoundError:
            status["lease_age_seconds"] = None
            status["lease_fresh"] = False
        return status
    except Exception:
        return {"alive": None, "pids": [], "required": True}


def _reclaim_dead_pending_monitor_lock() -> None:
    """Remove only a crypto leader lease whose recorded process is dead."""
    lock = ROOT / ".locks" / "pending_monitor_leader_crypto.lock"
    try:
        holder = lock.read_text(encoding="utf-8").strip().split(maxsplit=1)
        if not holder or not holder[0].isdigit():
            return
        pid = int(holder[0])
        alive = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             f"if (Get-Process -Id {pid} -ErrorAction SilentlyContinue) {{ exit 0 }} else {{ exit 1 }}"],
            capture_output=True, text=True, timeout=15,
        ).returncode == 0
        if not alive:
            lock.unlink(missing_ok=True)
    except FileNotFoundError:
        return
    except Exception:
        return


def start_pending_monitor() -> tuple[bool, str]:
    """Start the fast crypto tracker under the normal leader lock."""
    try:
        current = pending_monitor_status()
        if current.get("alive"):
            pids = ",".join(str(pid) for pid in current.get("pids", [])) or "unknown"
            return False, f"pending monitor already running pid={pids}"
        _reclaim_dead_pending_monitor_lock()
        log_path = ROOT / "data" / "autostart" / "pending_monitor_watchdog.log"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        _rotate_process_log(log_path)
        flags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
        with log_path.open("a", encoding="utf-8") as log:
            proc = subprocess.Popen(
                [sys.executable, "-m", "src.cli", "pending-monitor",
                 "--duration-hours", "0"],
                cwd=ROOT, env={**_live_canary_child_environment(), "PYTHONIOENCODING": "utf-8"},
                stdout=log, stderr=subprocess.STDOUT, creationflags=flags,
            )
        return True, f"started pending monitor pid={proc.pid}"
    except Exception as exc:
        return False, f"pending monitor start failed: {type(exc).__name__}: {exc}"


def _stop_exact_monitor_processes(pids: list[int], marker: str) -> list[int]:
    """Stop only the supplied Python PIDs whose command line still matches marker."""
    stopped: list[int] = []
    for pid in pids:
        if not isinstance(pid, int) or pid <= 0:
            continue
        escaped = marker.replace("'", "''")
        script = (
            f"$p=Get-CimInstance Win32_Process -Filter \"ProcessId={pid}\"; "
            f"if ($p -and $p.CommandLine -like '*{escaped}*') {{ "
            f"Stop-Process -Id {pid} -Force; exit 0 }}; exit 1"
        )
        try:
            result = subprocess.run(
                ["powershell", "-NoProfile", "-Command", script],
                capture_output=True, text=True, timeout=20,
            )
            if result.returncode == 0:
                stopped.append(pid)
        except Exception:
            continue
    return stopped


def _wait_for_processes_stopped(pids: list[int], *, timeout_seconds: float = 5.0) -> bool:
    """Wait for process teardown before checking whether a replacement exists."""
    pending = {int(pid) for pid in pids if isinstance(pid, int) and pid > 0}
    deadline = time.monotonic() + max(0.0, timeout_seconds)
    while pending and time.monotonic() < deadline:
        try:
            import psutil  # type: ignore

            pending = {pid for pid in pending if psutil.pid_exists(pid)}
        except Exception:
            break
        if pending:
            time.sleep(0.05)
    return not pending


def _orphan_monitor_lock(lock: Path, stopped_pids: list[int]) -> None:
    """Preserve a stopped monitor's lease for audit while freeing the leader slot."""
    try:
        holder = lock.read_text(encoding="utf-8").strip().split(maxsplit=1)
        if not holder or not holder[0].isdigit() or int(holder[0]) not in stopped_pids:
            return
        stamp = _now().strftime("%Y%m%d_%H%M%S")
        lock.replace(lock.with_name(f"{lock.name}.orphaned_watchdog_{stamp}"))
    except FileNotFoundError:
        return
    except Exception:
        return


def _lock_owner_pid(path: Path) -> int | None:
    """Read the first PID token from a monitor lease without modifying it."""
    try:
        token = path.read_text(encoding="utf-8").strip().split(maxsplit=1)[0]
        return int(token) if token.isdigit() else None
    except (FileNotFoundError, OSError, IndexError):
        return None


def restart_pending_monitor(status: dict | None = None) -> tuple[bool, str]:
    """Replace a live-but-stalled fast tracker without touching unrelated workers."""
    with _restart_lease("pending_monitor") as acquired:
        if not acquired:
            return False, "pending monitor restart already in progress"
        current = status or pending_monitor_status()
        pids = [int(pid) for pid in current.get("pids", []) if str(pid).isdigit()]
        stopped = _stop_exact_monitor_processes(pids, "-m src.cli pending-monitor")
        if pids and not stopped:
            return False, "pending monitor restart refused: process identity changed"
        _orphan_monitor_lock(ROOT / ".locks" / "pending_monitor_leader_crypto.lock", stopped)
        return start_pending_monitor()


def ensure_pending_monitor(*, auto_start: bool = False) -> dict:
    status = pending_monitor_status()
    stalled = status.get("alive") is True and status.get("lease_fresh") is False
    status["action"] = "stalled" if stalled else ("healthy" if status.get("alive") else "missing")
    if stalled and auto_start:
        ok, message = restart_pending_monitor(status)
        status["action"] = "restarted" if ok else "restart_failed"
        status["message"] = message
        if ok:
            status["alive"] = True
            status["lease_fresh"] = True
    elif status.get("alive") is False and auto_start:
        ok, message = start_pending_monitor()
        status["action"] = "started" if ok else "start_failed"
        status["message"] = message
        if ok:
            status["alive"] = True
    return status


def telegram_collector_status() -> dict:
    """Report the long-running event-driven Telegram news listener."""
    try:
        out = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | "
             "Where-Object { $_.CommandLine -like '*run_telegram_collector.py*' } | "
             "ForEach-Object { $_.ProcessId }"],
            capture_output=True, text=True, timeout=20,
        )
        pids = [int(line.strip()) for line in (out.stdout or "").splitlines()
                if line.strip().isdigit()]
        return {"alive": bool(pids), "pids": pids}
    except Exception:
        return {"alive": None, "pids": []}


def telegram_public_fallback_status(
    *,
    db: Path = TRADING_DB,
    now: datetime | None = None,
) -> dict:
    """Read the durable completion marker for the public Telegram fallback.

    A collector PID only proves that Windows has not reaped it.  When Telethon
    authentication is revoked, the public HTML fallback is the data path that
    matters, so use its completed-cycle record as the heartbeat.
    """
    current = now or _now()
    result = {
        "available": False,
        "last_completed_at": None,
        "last_status": None,
        "last_item_count": None,
        "age_seconds": None,
        "fresh": False,
        "grace_seconds": TELEGRAM_PUBLIC_FALLBACK_GRACE_SEC,
    }
    try:
        conn = sqlite3.connect(f"file:{db.as_posix()}?mode=ro", uri=True, timeout=5)
        row = conn.execute(
            "SELECT finished_at,status,item_count FROM news_source_runs "
            "WHERE source_name='collector_public_html' ORDER BY id DESC LIMIT 1"
        ).fetchone()
        conn.close()
        result["available"] = True
        if not row:
            return result
        completed_at = str(row[0] or "") or None
        result.update({
            "last_completed_at": completed_at,
            "last_status": str(row[1] or "") or None,
            "last_item_count": int(row[2] or 0),
        })
        if not completed_at:
            return result
        completed = datetime.fromisoformat(completed_at.replace("Z", "+00:00"))
        if completed.tzinfo is None:
            completed = completed.replace(tzinfo=timezone.utc)
        age_seconds = max(0.0, (current - completed.astimezone(timezone.utc)).total_seconds())
        result["age_seconds"] = round(age_seconds, 3)
        result["fresh"] = (
            str(result["last_status"] or "").lower() in {"ok", "ok_empty"}
            and age_seconds <= TELEGRAM_PUBLIC_FALLBACK_GRACE_SEC
        )
    except Exception as exc:
        result["error"] = type(exc).__name__
    return result


def _telegram_collector_enabled() -> bool:
    try:
        import yaml

        with (ROOT / "config" / "sources.yaml").open("r", encoding="utf-8") as fh:
            cfg = yaml.safe_load(fh) or {}
        return bool((cfg.get("telegram_channels") or {}).get("enabled", False))
    except Exception:
        return False


def _telegram_public_fallback_enabled() -> bool:
    try:
        import yaml

        with (ROOT / "config" / "sources.yaml").open("r", encoding="utf-8") as fh:
            cfg = yaml.safe_load(fh) or {}
        block = cfg.get("telegram_channels") or {}
        return bool(block.get("public_html_fallback_enabled", True))
    except Exception:
        return False


def _telegram_reauth_required() -> bool:
    """Avoid restart loops when Telegram revoked the project session.

    A new login code is the only recovery for this condition, so restarting a
    process every heartbeat merely creates noisy failures.
    """
    try:
        # The old telemetry key intentionally grouped the primary listener and
        # public HTML fallback. A successful fallback row could therefore hide
        # the primary listener's revoked Telethon session. Read the primary
        # process record by name first; retain the keyed lookup for older DBs.
        conn = sqlite3.connect(
            f"file:{TRADING_DB.as_posix()}?mode=ro", uri=True, timeout=5
        )
        row = conn.execute(
            "SELECT error_code,error_message FROM news_source_runs "
            "WHERE source_name='collector' AND source_type='telegram_collector' "
            "ORDER BY id DESC LIMIT 1"
        ).fetchone()
        conn.close()
        if row is None:
            from src.news.source_telemetry import latest_runs

            latest = latest_runs().get("telegram:collector") or {}
            code = str(latest.get("error_code") or "").lower()
            message = str(latest.get("error_message") or "").lower()
        else:
            code = str(row[0] or "").lower()
            message = str(row[1] or "").lower()
        return code == "session_reauth_required" or (
            "authorization key" in message and "session" in message
        )
    except Exception:
        return False


def _latest_catalyst_label_refresh(db: Path = TRADING_DB) -> str | None:
    """Return the real completion time, including a successful no-op pass."""
    try:
        conn = sqlite3.connect(f"file:{db.as_posix()}?mode=ro", uri=True, timeout=5)
        has_runs = conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' "
            "AND name='catalyst_label_refresh_runs'"
        ).fetchone()
        if has_runs:
            row = conn.execute(
                "SELECT completed_at FROM catalyst_label_refresh_runs "
                "ORDER BY id DESC LIMIT 1"
            ).fetchone()
            if row and row[0]:
                conn.close()
                return str(row[0])
        conn.close()
    except Exception:
        pass
    # Backward-compatible fallback until the first upgraded refresh completes.
    return _db_max(db, "SELECT MAX(computed_at) FROM signal_catalyst_labels")


def start_telegram_collector() -> tuple[bool, str]:
    """Start the realtime listener; the process itself records transport health."""
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "$task=Get-ScheduledTask -TaskName CryptoAIDesk_TelegramCollector "
             "-ErrorAction Stop; if ($task.State -eq 'Running') { "
             "Stop-ScheduledTask -TaskName CryptoAIDesk_TelegramCollector; "
             "Start-Sleep -Milliseconds 500 }; "
             "Start-ScheduledTask -TaskName CryptoAIDesk_TelegramCollector"],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode == 0:
            return True, "started Telegram collector via scheduled task"
    except Exception:
        pass
    try:
        log_path = ROOT / "data" / "autostart" / "telegram_collector_watchdog.log"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        flags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
        with log_path.open("a", encoding="utf-8") as log:
            proc = subprocess.Popen(
                [sys.executable, str(ROOT / "scripts" / "run_telegram_collector.py")],
                cwd=ROOT, env=os.environ.copy(), stdout=log,
                stderr=subprocess.STDOUT, creationflags=flags,
            )
        return True, f"started Telegram collector pid={proc.pid}"
    except Exception as exc:
        return False, f"Telegram collector start failed: {type(exc).__name__}: {exc}"


def restart_telegram_collector(status: dict | None = None) -> tuple[bool, str]:
    """Replace only a verified stalled collector, never an unrelated Python job."""
    current = status or telegram_collector_status()
    pids = [int(pid) for pid in current.get("pids", []) if str(pid).isdigit()]
    stopped = _stop_exact_monitor_processes(pids, "run_telegram_collector.py")
    if pids and not stopped:
        return False, "Telegram collector restart refused: process identity changed"
    if stopped:
        time.sleep(0.25)
    return start_telegram_collector()


def ensure_telegram_collector(*, auto_start: bool = False) -> dict:
    status = telegram_collector_status()
    status["required"] = _telegram_collector_enabled()
    status["action"] = "not_required"
    if not status["required"]:
        return status

    reauth_required = _telegram_reauth_required()
    status["reauth_required"] = reauth_required
    fallback_enabled = _telegram_public_fallback_enabled()
    if status["alive"] is False:
        if reauth_required and not fallback_enabled:
            status["action"] = "auth_required"
            status["message"] = "Telegram session revoked; re-run setup_telegram_auth.py once"
            return status
        status["action"] = "fallback_missing" if reauth_required else "missing"
        if auto_start:
            ok, message = start_telegram_collector()
            status["action"] = "fallback_started" if ok and reauth_required else (
                "started" if ok else "start_failed"
            )
            status["message"] = message
        return status

    if status["alive"] is True:
        # ``news_source_runs`` historically grouped the primary listener and
        # public fallback under one telemetry key.  A fresh fallback completion
        # is therefore the most reliable runtime evidence of fallback mode,
        # even if the older reauthorization row has already rolled out of the
        # retention window.
        fallback = telegram_public_fallback_status()
        # A previous public-HTML cycle is durable evidence that this process
        # has entered fallback mode even when a later telemetry row no longer
        # retains the original Telethon reauthorization error. Without this
        # check a frozen fallback PID was incorrectly reported as healthy.
        fallback_expected = bool(
            fallback_enabled and (reauth_required or fallback.get("last_completed_at"))
        )
        fallback_active = bool(fallback.get("fresh")) or fallback_expected
        if not fallback_active:
            status["action"] = "healthy"
            return status
        status["public_fallback"] = fallback
        if not fallback_enabled:
            status["action"] = "auth_required"
            status["message"] = "Telegram session revoked and public HTML fallback is disabled"
        elif fallback.get("fresh"):
            status["action"] = "fallback_healthy"
        else:
            status["action"] = "fallback_stale"
            age = fallback.get("age_seconds")
            detail = "no completed fallback cycle" if age is None else f"last cycle {age:.0f}s ago"
            status["message"] = f"Telegram public fallback stale: {detail}"
            if auto_start:
                ok, message = restart_telegram_collector(status)
                status["action"] = "fallback_restarted" if ok else "fallback_restart_failed"
                status["message"] = message
        return status
    return status


def mexc_canary_monitor_status() -> dict:
    """Read the dedicated live monitor's process and durable heartbeat state."""
    try:
        out = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | "
             "Where-Object { $_.CommandLine -like '*mexc-canary-monitor*' } | "
             "ForEach-Object { $_.ProcessId }"],
            capture_output=True, text=True, timeout=20,
        )
        pids = [int(line.strip()) for line in (out.stdout or "").splitlines() if line.strip().isdigit()]
    except Exception:
        pids = []
    leader_pid = _lock_owner_pid(
        ROOT / ".locks" / "pending_monitor_leader_mexc-canary.lock"
    )
    health: dict = {"alive": bool(pids), "pids": pids, "leader_pid": leader_pid,
                    "standby_pids": [pid for pid in pids if pid != leader_pid],
                    "heartbeat_at": None,
                    "heartbeat_age_seconds": None, "heartbeat_status": None, "required": False}
    try:
        from src.live_execution.config import load_live_canary_config

        cfg = load_live_canary_config()
        health["required"] = bool(cfg.execution_mode == "live" and cfg.submission_enabled)
    except Exception:
        pass
    try:
        conn = sqlite3.connect(f"file:{TRADING_DB.as_posix()}?mode=ro", uri=True, timeout=5)
        row = conn.execute(
            "SELECT control_value,updated_at FROM mexc_canary_control "
            "WHERE control_key='monitor_heartbeat'"
        ).fetchone()
        conn.close()
        if row:
            payload = json.loads(str(row[0]) or "{}")
            at = str(payload.get("at") or row[1] or "") or None
            age_min = _age_min(at)
            health.update({
                "heartbeat_at": at,
                "heartbeat_age_seconds": None if age_min is None else round(age_min * 60.0, 3),
                "heartbeat_status": payload.get("status"),
                "live_armed": payload.get("live_armed"),
            })
    except Exception:
        pass
    return health


def prune_mexc_canary_duplicates(status: dict | None = None) -> dict:
    """Stop verified non-leaders while preserving the authoritative live worker."""
    current = status or mexc_canary_monitor_status()
    leader_pid = current.get("leader_pid")
    pids = [int(pid) for pid in current.get("pids", []) if str(pid).isdigit()]
    if not isinstance(leader_pid, int) or leader_pid not in pids:
        return {"status": "SKIPPED_NO_VERIFIED_LEADER", "stopped": [], "remaining": pids}
    duplicates = [pid for pid in pids if pid != leader_pid]
    stopped = _stop_exact_monitor_processes(duplicates, "mexc-canary-monitor")
    return {
        "status": "OK" if len(stopped) == len(duplicates) else "PARTIAL",
        "leader_pid": leader_pid,
        "stopped": stopped,
        "remaining": [pid for pid in pids if pid not in stopped],
    }


def _read_user_environment(name: str) -> str:
    """Fetch a credential only for the child environment; never log its value."""
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             f"[Environment]::GetEnvironmentVariable('{name}','User')"],
            capture_output=True, text=True, timeout=15,
        )
        return (result.stdout or "").strip()
    except Exception:
        return ""


def _live_canary_child_environment() -> dict[str, str]:
    """Restore every armed venue's user-scoped credentials for the child."""
    env = os.environ.copy()
    try:
        from src.live_execution.config import load_live_canary_config

        cfg = load_live_canary_config()
        names = (
            cfg.credential_names()[:3]
            + cfg.bybit_credential_names()[:3]
        )
        for name in names:
            value = env.get(name) or _read_user_environment(name)
            if value:
                env[name] = value
    except Exception:
        pass
    return env


def _stocks_market_data_child_environment() -> dict[str, str]:
    """Pass current user-scoped Alpaca credentials to stock workers.

    The desktop scheduler may have inherited an older process environment before
    credentials were added or rotated. Prefer the current user values for this
    read-only market-data worker so its next launch does not reuse stale keys.
    """
    env = os.environ.copy()
    for name in (
        "ALPACA_API_KEY", "ALPACA_API_SECRET", "ALPACA_DATA_BASE_URL",
        "ALPACA_TRADING_BASE_URL",
    ):
        value = _read_user_environment(name)
        if value:
            env[name] = value
    return env


def start_mexc_canary_monitor() -> tuple[bool, str]:
    """Start a standby MEXC monitor with the same user-scoped arm environment."""
    try:
        from src.live_execution.config import load_live_canary_config

        cfg = load_live_canary_config()
        if not (cfg.execution_mode == "live" and cfg.submission_enabled):
            return False, "MEXC monitor not started: live submission is disabled"
        current = mexc_canary_monitor_status()
        if current.get("alive"):
            pids = ",".join(str(pid) for pid in current.get("pids", [])) or "unknown"
            return False, f"MEXC monitor already running pid={pids}"
        env = _live_canary_child_environment()
        log_path = ROOT / "data" / "autostart" / "mexc_canary_watchdog.log"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        _rotate_process_log(log_path)
        flags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
        with log_path.open("a", encoding="utf-8") as log:
            proc = subprocess.Popen(
                [sys.executable, "-m", "src.cli", "mexc-canary-monitor", "--interval", "3", "--duration-hours", "0"],
                cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT,
                creationflags=flags,
            )
        return True, f"started MEXC canary standby pid={proc.pid}"
    except Exception as exc:
        return False, f"MEXC canary monitor start failed: {type(exc).__name__}: {exc}"


def restart_mexc_canary_monitor(status: dict | None = None) -> tuple[bool, str]:
    """Replace a stale MEXC monitor after exact command-line verification."""
    with _restart_lease("mexc_canary_monitor") as acquired:
        if not acquired:
            return False, "MEXC monitor restart already in progress"
        current = status or mexc_canary_monitor_status()
        pids = [int(pid) for pid in current.get("pids", []) if str(pid).isdigit()]
        stopped = _stop_exact_monitor_processes(pids, "mexc-canary-monitor")
        if pids and not stopped:
            return False, "MEXC monitor restart refused: process identity changed"
        if stopped and not _wait_for_processes_stopped(stopped):
            return False, "MEXC monitor restart delayed: prior process is still terminating"
        _orphan_monitor_lock(ROOT / ".locks" / "pending_monitor_leader_mexc-canary.lock", stopped)
        return start_mexc_canary_monitor()


def derivatives_monitor_status() -> dict:
    try:
        out = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | "
             "Where-Object { $_.CommandLine -like '*scripts.derivatives_monitor*' } | "
             "ForEach-Object { $_.ProcessId }"],
            capture_output=True, text=True, timeout=20,
        )
        pids = [int(line.strip()) for line in (out.stdout or "").splitlines()
                if line.strip().isdigit()]
    except Exception:
        pids = []
    heartbeat = None
    try:
        heartbeat = json.loads(DERIVATIVES_HEARTBEAT.read_text(encoding="utf-8"))
    except (FileNotFoundError, ValueError, json.JSONDecodeError):
        pass
    leader_pid = _lock_owner_pid(ROOT / ".locks" / "derivatives_monitor.pid")
    return {
        "alive": bool(pids),
        "pids": pids,
        "leader_pid": leader_pid,
        "duplicate_pids": [pid for pid in pids if pid != leader_pid],
        "heartbeat": heartbeat,
    }


def prune_derivatives_monitor_duplicates(status: dict | None = None) -> dict:
    """Stop legacy derivatives writers that do not own the singleton lock."""
    current = status or derivatives_monitor_status()
    leader_pid = current.get("leader_pid")
    pids = [int(pid) for pid in current.get("pids", []) if str(pid).isdigit()]
    if not isinstance(leader_pid, int) or leader_pid not in pids:
        return {"status": "SKIPPED_NO_VERIFIED_LEADER", "stopped": [], "remaining": pids}
    duplicates = [pid for pid in pids if pid != leader_pid]
    stopped = _stop_exact_monitor_processes(duplicates, "scripts.derivatives_monitor")
    return {
        "status": "OK" if len(stopped) == len(duplicates) else "PARTIAL",
        "leader_pid": leader_pid,
        "stopped": stopped,
        "remaining": [pid for pid in pids if pid not in stopped],
    }


def restart_derivatives_monitor(status: dict | None = None) -> tuple[bool, str]:
    with _restart_lease("derivatives_monitor") as acquired:
        if not acquired:
            return False, "derivatives monitor restart already in progress"
        current = status or derivatives_monitor_status()
        pids = [int(pid) for pid in current.get("pids", []) if str(pid).isdigit()]
        stopped = _stop_exact_monitor_processes(pids, "scripts.derivatives_monitor")
        if pids and not stopped:
            return False, "derivatives monitor restart refused: process identity changed"
        lock = ROOT / ".locks" / "derivatives_monitor.pid"
        try:
            lock.unlink(missing_ok=True)
        except OSError:
            pass
        try:
            log_path = ROOT / "data" / "autostart" / "derivatives_monitor_watchdog.log"
            log_path.parent.mkdir(parents=True, exist_ok=True)
            _rotate_process_log(log_path)
            flags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
            with log_path.open("a", encoding="utf-8") as log:
                proc = subprocess.Popen(
                    [sys.executable, "-m", "scripts.derivatives_monitor", "--minutes", "1440",
                     "--cadence-seconds", "120"],
                    cwd=ROOT, env={**os.environ, "PYTHONIOENCODING": "utf-8"},
                    stdout=log, stderr=subprocess.STDOUT, creationflags=flags,
                )
            runtime = ROOT / "data" / "runtime_locks" / "derivatives_monitor.pid"
            runtime.parent.mkdir(parents=True, exist_ok=True)
            runtime.write_text(str(proc.pid), encoding="utf-8")
            return True, f"derivatives monitor restarted pid={proc.pid}"
        except Exception as exc:
            return False, f"derivatives monitor restart failed: {type(exc).__name__}: {exc}"


def stock_worker_window(now: datetime | None = None) -> dict:
    """Return the NYSE-day control window for the stock monitor."""
    moment = now or _now()
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)
    local = moment.astimezone(NY)
    try:
        from src.stocks.market_calendar import is_us_holiday
        holiday = is_us_holiday(moment)
    except Exception:
        holiday = False
    minute = local.hour * 60 + local.minute
    trading_day = local.weekday() < 5 and not holiday
    return {
        "session_date": local.date().isoformat(),
        "minute_et": minute,
        "trading_day": trading_day,
        "coverage_expected": bool(trading_day and STOCK_WORKER_START_MINUTE_ET <= minute < STOCK_WORKER_END_MINUTE_ET),
        "preopen_control": bool(trading_day and STOCK_WORKER_START_MINUTE_ET <= minute < STOCK_WORKER_PREOPEN_CONTROL_END_MINUTE_ET),
    }


def _start_stock_monitor() -> tuple[bool, str]:
    """Launch one stock observer; its leader lease prevents duplicate writes."""
    argv = [
        sys.executable, "-m", "src.cli", "stocks-monitor-session",
        "--minutes", "540", "--interval-minutes", "1",
        "--report-refresh-minutes", "5", "--market-hours-only", "--send-telegram",
    ]
    try:
        import os

        log_path = ROOT / "data" / "autostart" / "stock_monitor_watchdog.log"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        _rotate_process_log(log_path)
        flags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
        with log_path.open("a", encoding="utf-8") as log:
            proc = subprocess.Popen(
                argv, cwd=ROOT,
                env={**_stocks_market_data_child_environment(), "PYTHONIOENCODING": "utf-8"},
                stdout=log, stderr=subprocess.STDOUT, creationflags=flags,
            )
        return True, f"started stocks monitor pid={proc.pid}"
    except Exception as exc:
        return False, f"stocks monitor start failed: {type(exc).__name__}: {exc}"


def _stock_monitor_started_before_session(status: dict, window: dict) -> bool:
    """A 26-hour worker started yesterday expires before today's 16:05 ET close."""
    expected = str(window.get("session_date") or "")
    starts = []
    for process in status.get("processes") or []:
        try:
            created = datetime.fromisoformat(str(process.get("created_at") or "").replace("Z", "+00:00"))
            if created.tzinfo is None:
                created = created.replace(tzinfo=timezone.utc)
            starts.append(created.astimezone(NY).date().isoformat())
        except Exception:
            continue
    return bool(starts) and all(start < expected for start in starts)


def _stop_stock_monitor(pids: list[int]) -> None:
    """Stop only the stale stock observer, then reclaim its dead leader lease."""
    for pid in pids:
        try:
            subprocess.run(
                ["taskkill", "/F", "/PID", str(pid)],
                capture_output=True, text=True, timeout=15,
            )
        except Exception:
            pass
    lock = ROOT / ".locks" / "pending_monitor_leader_stocks.lock"
    try:
        holder = lock.read_text(encoding="utf-8").strip().split(maxsplit=1)
        if holder and holder[0].isdigit() and int(holder[0]) in set(pids):
            lock.unlink(missing_ok=True)
    except Exception:
        pass


def ensure_stock_monitor(*, now: datetime | None = None, auto_start: bool = False) -> dict:
    """Ensure a pre-US/RTH stock observer exists without touching strategy logic."""
    window = stock_worker_window(now)
    status = stock_monitor_status()
    result = {**window, **status, "action": "not_required"}
    if not window["coverage_expected"]:
        return result
    if status["alive"] is True:
        if window["preopen_control"] and _stock_monitor_started_before_session(status, window):
            result["action"] = "rollover_required"
            if auto_start:
                _stop_stock_monitor(status["pids"])
                ok, message = _start_stock_monitor()
                result.update({"alive": ok, "pids": [], "processes": [],
                               "action": "rolled_over" if ok else "rollover_failed", "message": message})
            return result
        return result
    if status["alive"] is None:
        return result
    result["action"] = "missing"
    if auto_start:
        ok, message = _start_stock_monitor()
        result["action"] = "started" if ok else "start_failed"
        result["message"] = message
    return result


def _stock_preopen_health() -> dict | None:
    """Read the durable pre-US hand-off record if this lane has run before."""
    try:
        uri = f"file:{TRADING_DB.as_posix()}?mode=ro"
        conn = sqlite3.connect(uri, uri=True, timeout=5)
        exists = conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' "
            "AND name='mexc_stock_futures_preopen_health'"
        ).fetchone()
        if not exists:
            conn.close()
            return None
        row = conn.execute(
            "SELECT session_date,checked_at,status,reason,actionable_count,processed_count "
            "FROM mexc_stock_futures_preopen_health ORDER BY checked_at DESC LIMIT 1"
        ).fetchone()
        conn.close()
        if row is None:
            return None
        return dict(zip(("session_date", "checked_at", "status", "reason", "actionable_count", "processed_count"), row))
    except Exception:
        return None


def last_cycle_iso() -> str | None:
    try:
        if not SCHED_LOG.exists():
            return None
        txt = SCHED_LOG.read_text(encoding="utf-8", errors="ignore").splitlines()
        for line in reversed(txt):
            if "CYCLE" in line and "END" in line:
                m = re.match(r"(\d{4}-\d{2}-\d{2})[ ](\d{2}:\d{2}:\d{2})", line)
                if m:
                    # scheduler.log timestamps are local; treat naive→assume local tz offset unknown,
                    # so compare loosely by also checking DB outcome recency below.
                    return f"{m.group(1)}T{m.group(2)}"
        return None
    except Exception:
        return None


def _db_max(db: Path, sql: str, ro: bool = True):
    try:
        uri = f"file:{db.as_posix()}?mode=ro" if ro else str(db)
        c = sqlite3.connect(uri, uri=ro, timeout=5)
        v = c.execute(sql).fetchone()[0]
        c.close()
        return v
    except Exception:
        return None


def _db_latest(db: Path, table: str, value_column: str, id_column: str = "id"):
    """Read the newest append-only row without scanning the full table."""
    identifiers = (table, value_column, id_column)
    if not all(re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", value) for value in identifiers):
        raise ValueError("unsafe SQLite identifier")
    return _db_max(
        db,
        f"SELECT {value_column} FROM {table} ORDER BY {id_column} DESC LIMIT 1",
    )


def _preus_review_deadline_minute() -> int:
    """Read the pre-US LLM deadline from the same config as the gate."""
    try:
        from src.execution.stocks_preus_review import load_cfg

        value = str(load_cfg().get("review_deadline_et") or "09:12")
        hour, minute = value.split(":", 1)
        return int(hour) * 60 + int(minute)
    except Exception:
        return 9 * 60 + 12


def _preus_llm_review_enabled() -> bool:
    try:
        from src.execution.stocks_preus_review import load_cfg

        return bool((load_cfg().get("llm_agent") or {}).get("enabled", True))
    except Exception:
        return True


def preus_review_health(*, db: Path = TRADING_DB, now: datetime | None = None) -> dict:
    """Read the durable configured-deadline structured-review hand-off health.

    The stock monitor writes this record from the routine's saved candidate
    snapshot.  It distinguishes a deliberate ``NO_ELIGIBLE`` morning from a
    missing bundle/verdict, rather than treating any old pre-US review row as
    proof that today's hand-off ran.
    """
    moment = (now or _now()).astimezone(NY)
    minute = moment.hour * 60 + moment.minute
    deadline_minute = _preus_review_deadline_minute()
    expected = (
        _preus_llm_review_enabled()
        and moment.weekday() < 5
        and deadline_minute <= minute <= 16 * 60 + 30
    )
    result = {
        "expected": expected,
        "deadline_et": f"{deadline_minute // 60:02d}:{deadline_minute % 60:02d}",
        "session_date": moment.date().isoformat(),
        "latest_reviewed_at": None,
        "latest_review_session": None,
        "overnight_plan_count": 0,
        "status": "NOT_DUE" if not expected else "UNKNOWN",
    }
    if not db.exists():
        result["status"] = "DB_MISSING"
        return result
    try:
        uri = f"file:{db.as_posix()}?mode=ro"
        conn = sqlite3.connect(uri, uri=True, timeout=5)
        conn.row_factory = sqlite3.Row
        has_health = conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' "
            "AND name='stocks_preus_review_health'"
        ).fetchone()
        row = None
        if has_health:
            row = conn.execute(
                "SELECT checked_at,eligible_count,reviewed_count,missing_count,status,reason "
                "FROM stocks_preus_review_health WHERE session_date=?",
                (result["session_date"],),
            ).fetchone()
        conn.close()
        if not expected:
            result["status"] = "NOT_DUE"
        elif row is None:
            result["status"] = "MISSING_HANDOFF_HEALTH"
        else:
            result.update({
                "latest_reviewed_at": row["checked_at"],
                "latest_review_session": result["session_date"],
                "overnight_plan_count": int(row["eligible_count"] or 0),
                "reviewed_count": int(row["reviewed_count"] or 0),
                "missing_count": int(row["missing_count"] or 0),
                "reason": row["reason"],
                "status": str(row["status"] or "UNKNOWN"),
            })
    except Exception as exc:
        result["status"] = "ERROR"
        result["error"] = type(exc).__name__
    return result


def ensure_preus_baseline(*, now: datetime | None = None, auto_start: bool = False) -> dict:
    """Guarantee the autonomous structured pre-US review has run.

    The wrapper records a deterministic baseline before its bounded OpenRouter
    calls, so recovery cannot strand an otherwise valid plan. The heartbeat
    reuses that wrapper only when Task Scheduler missed its trigger.
    """
    moment = (now or _now()).astimezone(NY)
    minute = moment.hour * 60 + moment.minute
    session_date = moment.date().isoformat()
    in_window = (
        moment.weekday() < 5
        and PREUS_BASELINE_START_MINUTE_ET <= minute <= PREUS_BASELINE_END_MINUTE_ET
    )
    marker = ROOT / "data" / "scheduled_runs" / "preus_review" / f"{session_date}.openrouter.done"
    result = {
        "session_date": session_date,
        "in_window": in_window,
        "ready": marker.exists(),
        "action": "ready" if marker.exists() else ("pending_window" if in_window else "not_due"),
    }
    if not in_window or marker.exists() or not auto_start:
        return result
    try:
        proc = subprocess.run(
            [
                "powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
                "-File", str(ROOT / "scripts" / "run_preus_llm_review.ps1"), "-Force",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=180,
        )
        result["ready"] = marker.exists()
        result["action"] = "recovered" if proc.returncode == 0 and result["ready"] else "recovery_failed"
        if result["action"] == "recovery_failed":
            result["message"] = (proc.stderr or proc.stdout or "pre-US baseline did not create marker")[-600:]
    except Exception as exc:
        result["action"] = "recovery_failed"
        result["message"] = f"{type(exc).__name__}: {exc}"
    return result


def collect() -> dict:
    alive, uptime = scheduler_status()
    derivatives_heartbeat = None
    try:
        derivatives_heartbeat = json.loads(DERIVATIVES_HEARTBEAT.read_text(encoding="utf-8"))
    except (FileNotFoundError, ValueError, json.JSONDecodeError):
        pass
    try:
        from scripts.run_llm_quality_schedule import health_snapshot

        llm_quality_refresh = health_snapshot(root=ROOT, now=_now())
    except Exception as exc:
        llm_quality_refresh = {
            "required": True,
            "status": "HEALTH_ERROR",
            "stale": True,
            "error": f"{type(exc).__name__}: {exc}",
        }
    return {
        "now": _now().isoformat(),
        "scheduler_alive": alive,
        "scheduler_uptime_min": uptime,
        "last_cycle": last_cycle_iso(),
        "last_alert": _db_max(TRADING_DB, "SELECT MAX(sent_at) FROM signal_alerts"),
        "last_outcome": _db_latest(TRADING_DB, "signal_outcomes", "checked_at"),
        "last_signal": _db_max(TRADING_DB, "SELECT MAX(created_at) FROM proposed_signals"),
        "last_intel": _db_max(INTEL_DB, "SELECT MAX(computed_at) FROM deriv_cache"),
        "last_derivative_snapshot": _db_latest(
            MARKET_INTEL_DB, "derivative_snapshots", "received_at"
        ),
        "last_liquidity_snapshot": _db_latest(
            MARKET_INTEL_DB, "liquidity_snapshots", "received_at"
        ),
        "derivatives_heartbeat": derivatives_heartbeat,
        "derivatives_monitor": derivatives_monitor_status(),
        # 2026-07-13 audit: these 3 steps could silently stop updating every cycle while every
        # other check above stays green -- heartbeat must notice, not just track_active_signals.
        "last_cooldowns": _db_max(TRADING_DB, "SELECT MAX(computed_at) FROM crypto_quality_cooldowns"),
        "last_paper_exec": _db_max(TRADING_DB, "SELECT MAX(computed_at) FROM paper_execution_outcomes"),
        "last_catalyst_labels": _latest_catalyst_label_refresh(TRADING_DB),
        "stock_preopen_health": _stock_preopen_health(),
        "preus_review_health": preus_review_health(),
        "llm_quality_refresh": llm_quality_refresh,
        "pending_monitor": pending_monitor_status(),
        "mexc_canary_monitor": mexc_canary_monitor_status(),
    }


def _load_state() -> dict:
    try:
        return json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    except Exception:
        return {}


def _save_state(s: dict) -> None:
    try:
        STATE.parent.mkdir(parents=True, exist_ok=True)
        STATE.write_text(json.dumps(s), encoding="utf-8")
    except Exception:
        pass


def _send(text: str) -> bool:
    try:
        from src.notifiers.telegram import TelegramNotifier
        n = TelegramNotifier(ROOT / "config" / "notifications.yaml")
        if not getattr(n, "enabled", False) or not getattr(n, "chat_id", None):
            print("[heartbeat] telegram not configured; message:", text)
            return False
        n.send(text, parse_mode="")
        return True
    except Exception as exc:
        print(f"[heartbeat] telegram send failed ({type(exc).__name__}); message:", text)
        return False


def _restart() -> str:
    """Restart the scheduler cleanly. Prefer the task-owned path (Start-ScheduledTask
    CryptoAIDeskMonitor) so the new process lives under the Task Scheduler service and is
    not killed when this watchdog process exits; fall back to the detached launcher."""
    try:
        r = subprocess.run(["powershell", "-NoProfile", "-Command",
                            "if ((Get-ScheduledTask -TaskName CryptoAIDeskMonitor).State -eq 'Running') { "
                            "Stop-ScheduledTask -TaskName CryptoAIDeskMonitor; Start-Sleep -Milliseconds 500 }; "
                            "Start-ScheduledTask -TaskName CryptoAIDeskMonitor"],
                           capture_output=True, text=True, timeout=30)
        if r.returncode == 0:
            return " · auto-restart via CryptoAIDeskMonitor task"
    except Exception:
        pass
    try:
        subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
                        "-File", str(LAUNCHER), "-Quiet"], timeout=60)
        return " · auto-restart via launcher"
    except Exception:
        return " · auto-restart FAILED"


def _start_llm_quality_refresh() -> str:
    """Kick the independent cache refresh task without touching the market scheduler."""
    try:
        result = subprocess.run(
            [
                "powershell", "-NoProfile", "-Command",
                f"Start-ScheduledTask -TaskName '{LLM_QUALITY_TASK_NAME}'",
            ],
            capture_output=True,
            text=True,
            timeout=20,
        )
        if result.returncode == 0:
            return "LLM advisory refresh task started"
        detail = (result.stderr or result.stdout or "unknown task error").strip()[-300:]
        return f"LLM advisory refresh task start failed ({detail})"
    except Exception as exc:
        return f"LLM advisory refresh task start failed ({type(exc).__name__})"


def _send_deduped(key: str, text: str, state: dict) -> None:
    last = _age_min(state.get(key))
    if last is not None and last < WARN_COOLDOWN_MIN:
        print(f"[heartbeat] suppressed (cooldown {last:.0f}<{WARN_COOLDOWN_MIN}m): {key}")
        return
    if _send(text):
        state[key] = _now().isoformat()


def _run(args: argparse.Namespace) -> None:
    s = collect()
    state = _load_state()
    stock_worker = ensure_stock_monitor(now=_now(), auto_start=args.auto_restart)
    s["stock_monitor"] = stock_worker
    s["preus_baseline"] = ensure_preus_baseline(now=_now(), auto_start=args.auto_restart)
    pending_worker = ensure_pending_monitor(auto_start=args.auto_restart)
    s["pending_monitor"] = pending_worker
    telegram_worker = ensure_telegram_collector(auto_start=args.auto_restart)
    s["telegram_collector"] = telegram_worker
    mexc_worker = s["mexc_canary_monitor"]

    # Scheduler restarts used to leave permanent standby processes behind.
    # Clean only PIDs proven not to own the corresponding internal lease.
    duplicate_repair_errors: list[str] = []
    if args.auto_restart:
        mexc_cleanup = prune_mexc_canary_duplicates(mexc_worker)
        if mexc_cleanup.get("stopped"):
            mexc_worker = mexc_canary_monitor_status()
            s["mexc_canary_monitor"] = mexc_worker
            s["mexc_canary_duplicate_cleanup"] = mexc_cleanup
        if mexc_cleanup.get("status") == "PARTIAL":
            duplicate_repair_errors.append("MEXC live monitor duplicate cleanup incomplete")

        derivatives_cleanup = prune_derivatives_monitor_duplicates(s.get("derivatives_monitor"))
        if derivatives_cleanup.get("stopped"):
            s["derivatives_monitor"] = derivatives_monitor_status()
            s["derivatives_duplicate_cleanup"] = derivatives_cleanup
        if derivatives_cleanup.get("status") == "PARTIAL":
            duplicate_repair_errors.append("derivatives monitor duplicate cleanup incomplete")

    out_age = _age_min(s["last_outcome"])
    intel_age = _age_min(s["last_intel"])
    fresh = lambda a: ("?" if a is None else (f"{a/60:.1f}h" if a >= 60 else f"{a:.0f}m"))

    if args.event == "start":
        _send("🟢 Monitor started — default scheduler launching (diagnostic heartbeat).")
        print(json.dumps(s, indent=1, default=str)); return

    if args.event == "cycle":
        _send(f"🟢 Monitor cycle OK — last alert {fresh(_age_min(s['last_alert']))} ago, "
              f"intel cache {fresh(intel_age)} ago. Diagnostic only.")
        print(json.dumps(s, indent=1, default=str)); return

    # --- check (watchdog) ---
    alive = s["scheduler_alive"]
    uptime = s["scheduler_uptime_min"]
    # "stuck" = alive long enough to have completed a cycle but tracking still old.
    # A freshly-started scheduler legitimately has old outcomes until its first cycle
    # completes, so only flag staleness once uptime exceeds one full interval+grace.
    cycle_window = INTERVAL_MIN + GRACE_MIN
    stale = (out_age is not None and out_age > cycle_window)
    stuck = bool(alive) and stale and (uptime is None or uptime > cycle_window)
    problems = []
    problems.extend(duplicate_repair_errors)
    if alive is False:
        problems.append("scheduler process not running")
    if stuck:
        problems.append(f"scheduler alive (up {fresh(uptime)}) but no tracking update for {fresh(out_age)}")

    # A healthy long scheduler is not enough proof that the narrow 09:15--09:30
    # ET stock hand-off ran. Watch the dedicated worker and its durable record.
    if stock_worker["coverage_expected"] and stock_worker["alive"] is False:
        detail = stock_worker.get("message") or "stocks monitor process absent"
        problems.append(f"stocks pre-US/RTH monitor unavailable ({detail})")
    if stock_worker["preopen_control"] and stock_worker["alive"] is True:
        control_key = f"stock_preopen_control_{stock_worker['session_date']}"
        if not state.get(control_key):
            pid_text = ",".join(str(pid) for pid in stock_worker.get("pids", [])) or "unknown"
            if _send(
                "[STOCK PRE-US] control OK: monitor active "
                f"(pid {pid_text}); 09:15-09:30 ET decision window covered."
            ):
                state[control_key] = _now().isoformat()
    if stock_worker["coverage_expected"] and stock_worker["minute_et"] >= 9 * 60 + 35:
        health = s.get("stock_preopen_health")
        if not health or health.get("session_date") != stock_worker["session_date"]:
            problems.append("stocks pre-US hand-off record missing after decision window")
        elif str(health.get("status") or "") == "ACTIONABLE_UNPROCESSED":
            problems.append("stocks pre-US actionable candidates were not processed")

    preus_llm = s.get("preus_review_health") or {}
    preus_problem_statuses = {
        "MISSING_HANDOFF_HEALTH", "BUNDLE_MISSING", "BUNDLE_FAILED",
        "BUNDLE_LATE", "REVIEW_LATE", "REVIEW_MISSING", "PARTIAL_REVIEW_MISSING",
        "HEALTH_UNAVAILABLE", "ERROR",
    }
    if preus_llm.get("expected") and preus_llm.get("status") in preus_problem_statuses:
        problems.append(
            "stocks Pre-US structured review hand-off incomplete for current session "
            f"(status={preus_llm.get('status')}, eligible={preus_llm.get('overnight_plan_count', 0)}, "
            f"missing={preus_llm.get('missing_count', 0)})"
        )
    preus_baseline = s.get("preus_baseline") or {}
    if preus_baseline.get("in_window") and not preus_baseline.get("ready"):
        problems.append(
            "stocks Pre-US baseline packet missing during hand-off window "
            f"(action={preus_baseline.get('action')})"
        )

    llm_quality = s.get("llm_quality_refresh") or {}
    if llm_quality.get("required"):
        llm_status = str(llm_quality.get("status") or "MISSING")
        llm_age = llm_quality.get("age_minutes")
        advisory = llm_quality.get("advisory") or {}
        error_detail = (
            llm_quality.get("error")
            or advisory.get("error")
            or ", ".join(
                f"{key} x{count}"
                for key, count in sorted((advisory.get("error_types") or {}).items())
            )
        )
        if llm_quality.get("stale"):
            problems.append(
                "LLM advisory cache refresh stale "
                f"({fresh(llm_age)} old, status={llm_status})"
            )
            if args.auto_restart:
                problems.append(_start_llm_quality_refresh())
        elif llm_status in {"ERROR", "DEGRADED", "INVALID_HEARTBEAT", "HEALTH_ERROR"}:
            problems.append(
                "LLM advisory cache refresh unhealthy "
                f"(status={llm_status}, error={error_detail or 'unknown'})"
            )

    if pending_worker.get("action") in {"stalled", "restart_failed"}:
        detail = pending_worker.get("message") or (
            f"heartbeat {pending_worker.get('heartbeat_age_seconds')}s old"
        )
        problems.append(f"crypto fast-entry monitor stalled ({detail})")
    elif pending_worker.get("alive") is False:
        detail = pending_worker.get("message") or "pending monitor process absent"
        problems.append(f"crypto fast-entry monitor unavailable ({detail})")

    derivative_heartbeat = s.get("derivatives_heartbeat") or {}
    derivative_heartbeat_age = _age_min(derivative_heartbeat.get("at"))
    derivative_stale = (
        derivative_heartbeat_age is None
        or derivative_heartbeat_age * 60.0 > DERIVATIVES_HEARTBEAT_GRACE_SEC
        or str(derivative_heartbeat.get("status") or "") == "ERROR"
    )
    derivative_starting = _monitor_is_starting(s.get("derivatives_monitor"))
    if derivative_stale and not derivative_starting:
        problems.append(
            "derivatives monitor heartbeat stale "
            f"({fresh(derivative_heartbeat_age)} old, stage={derivative_heartbeat.get('stage')})"
        )
        if args.auto_restart:
            ok, message = restart_derivatives_monitor(s.get("derivatives_monitor"))
            problems.append(message)
    for key, label in (
        ("last_derivative_snapshot", "derivative snapshots"),
        ("last_liquidity_snapshot", "liquidity snapshots"),
    ):
        age = _age_min(s.get(key))
        if age is None or age > DERIVATIVES_DATA_GRACE_MIN:
            problems.append(f"{label} stale ({fresh(age)} old)")

    if telegram_worker.get("required") and telegram_worker.get("action") in {
        "missing", "start_failed", "fallback_missing", "fallback_stale",
        "fallback_restart_failed", "auth_required",
    }:
        detail = telegram_worker.get("message") or "Telegram collector process absent"
        problems.append(f"Telegram news collector unhealthy ({detail})")

    if mexc_worker.get("required"):
        mexc_heartbeat_age = mexc_worker.get("heartbeat_age_seconds")
        mexc_stale = (
            mexc_heartbeat_age is None
            or float(mexc_heartbeat_age) > MEXC_CANARY_HEARTBEAT_GRACE_SEC
            or str(mexc_worker.get("heartbeat_status") or "") != "OK"
        )
        mexc_starting = _monitor_is_starting(mexc_worker)
        if mexc_worker.get("alive") is False:
            problems.append("MEXC live monitor process unavailable")
        elif mexc_stale and not mexc_starting:
            detail = "missing" if mexc_heartbeat_age is None else f"{mexc_heartbeat_age:.0f}s old"
            problems.append(f"MEXC live monitor heartbeat stale ({detail})")
        if args.auto_restart and mexc_worker.get("alive") is False:
            started, message = start_mexc_canary_monitor()
            problems.append(message)
        elif args.auto_restart and mexc_stale and not mexc_starting:
            started, message = restart_mexc_canary_monitor(mexc_worker)
            problems.append(message)

    # 2026-07-13 audit: previously only tracking/intel freshness was checked, so cooldowns/
    # Model F/catalyst labels could silently stop updating every cycle and heartbeat would
    # still report OK. Same "alive long enough that this should have refreshed by now" gate.
    long_enough_alive = bool(alive) and (uptime is None or uptime > cycle_window)
    derived_window = INTERVAL_MIN + DERIVED_GRACE_MIN
    for key, label in (("last_cooldowns", "crypto_quality_cooldowns"),
                       ("last_paper_exec", "paper_execution_outcomes"),
                       ("last_catalyst_labels", "signal_catalyst_labels")):
        age = _age_min(s[key])
        if long_enough_alive and age is not None and age > derived_window:
            problems.append(f"{label} stale (no update for {fresh(age)})")

    if problems:
        restarted = ""
        # Only relaunch when the process is actually gone/unknown — never kill a live
        # (possibly slow) scheduler mid-cycle.
        if args.auto_restart and alive is not True:
            restarted = _restart()
        _send_deduped("warn", f"⚠ Monitor watchdog: {'; '.join(problems)}.{restarted} (diagnostic)", state)
    else:
        # healthy: send an OK ping at most once per cooldown (low noise)
        _send_deduped("ok", f"🟢 Monitor OK — tracking {fresh(out_age)} ago, intel {fresh(intel_age)} ago, "
                            f"up {fresh(uptime)}. Diagnostic only.", state)
    _save_state(state)
    print(json.dumps({**s, "problems": problems}, indent=1, default=str))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--event", choices=["start", "cycle", "check"], default="check")
    ap.add_argument("--auto-restart", action="store_true")
    args = ap.parse_args()
    if args.event == "check":
        with _restart_lease("monitor_heartbeat_check", stale_seconds=300) as acquired:
            if not acquired:
                print(json.dumps({
                    "status": "SKIPPED",
                    "reason": "monitor_heartbeat_check_already_running",
                }))
                return
            _run(args)
            return
    _run(args)


if __name__ == "__main__":
    main()
