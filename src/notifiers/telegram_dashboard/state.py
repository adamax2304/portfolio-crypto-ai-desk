"""Atomic local state for dashboard message and Telegram update cursor."""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any


def _pid_is_running(pid: int) -> bool:
    """Return whether a PID is live on Windows and POSIX without psutil."""
    if pid <= 0:
        return False
    if os.name == "nt":
        import ctypes

        process_query_limited_information = 0x1000
        handle = ctypes.windll.kernel32.OpenProcess(
            process_query_limited_information, False, pid
        )
        if not handle:
            return False
        ctypes.windll.kernel32.CloseHandle(handle)
        return True
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def _pid_is_dashboard_poller(pid: int) -> bool:
    """Return whether a PID is the dashboard poller, not merely a live PID.

    Windows can reuse a PID after the poller dies. Treating any live process
    with that number as the dashboard would leave callback buttons without a
    consumer until the next manual intervention.
    """
    if pid <= 0:
        return False
    # A second acquire attempt in this same poller remains a hard conflict.
    if pid == os.getpid():
        return True
    if not _pid_is_running(pid):
        return False
    try:
        if os.name == "nt":
            query = (
                f'$p=Get-CimInstance Win32_Process -Filter "ProcessId={pid}"; '
                'if ($p -and $p.CommandLine -match "telegram-dashboard") '
                '{ exit 0 }; exit 1'
            )
            return subprocess.run(
                ["powershell", "-NoProfile", "-Command", query],
                capture_output=True,
                text=True,
                timeout=8,
            ).returncode == 0
        return b"telegram-dashboard" in Path(f"/proc/{pid}/cmdline").read_bytes()
    except (OSError, subprocess.SubprocessError):
        return False


class DashboardStateStore:
    """Persist only UI state outside the trading SQLite database."""

    def __init__(self, path: Path):
        self.path = path

    def load(self) -> dict[str, Any]:
        if not self.path.exists():
            return {}
        try:
            with self.path.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
        except (OSError, json.JSONDecodeError):
            return {}
        return data if isinstance(data, dict) else {}

    def save(self, payload: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_name = tempfile.mkstemp(prefix=self.path.name, suffix=".tmp", dir=self.path.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
                handle.write("\n")
            os.replace(tmp_name, self.path)
        finally:
            if os.path.exists(tmp_name):
                os.unlink(tmp_name)

    def update(self, **values: Any) -> dict[str, Any]:
        state = self.load()
        state.update(values)
        self.save(state)
        return state

    def acquire_poll_lock(self) -> int:
        """Acquire a process lock so only one Bot API long-poller runs.

        A stale lock left behind by a crash is reclaimed when its recorded PID
        is no longer the dashboard process. This matters on Windows, where an
        unrelated process can inherit a dead poller's PID. The lock protects
        dashboard callbacks only; it has no relationship to SQLite or any
        execution worker lock.
        """
        lock_path = self.path.with_suffix(self.path.suffix + ".poll.lock")
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        for _attempt in range(2):
            try:
                fd = os.open(lock_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL)
            except FileExistsError:
                try:
                    pid = int(lock_path.read_text(encoding="ascii").strip())
                except (OSError, ValueError):
                    pid = -1
                if not _pid_is_dashboard_poller(pid):
                    try:
                        lock_path.unlink()
                    except FileNotFoundError:
                        pass
                    continue
                raise RuntimeError(f"telegram dashboard poller already running (pid={pid})")
            os.write(fd, str(os.getpid()).encode("ascii"))
            return fd
        raise RuntimeError("failed to acquire telegram dashboard poller lock")

    def release_poll_lock(self, fd: int) -> None:
        lock_path = self.path.with_suffix(self.path.suffix + ".poll.lock")
        try:
            os.close(fd)
        finally:
            try:
                lock_path.unlink()
            except FileNotFoundError:
                pass
