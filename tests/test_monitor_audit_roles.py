"""Role-aware monitor-audit diagnostics."""
from __future__ import annotations

from src.signals import monitor_audit


def test_process_enumerator_ignores_shell_command_text(monkeypatch):
    class _Proc:
        def __init__(self, pid, name, cmdline):
            self.info = {"pid": pid, "name": name, "cmdline": cmdline, "create_time": 0}

    fake = type("Psutil", (), {"process_iter": staticmethod(lambda _attrs: [
        _Proc(1, "powershell.exe", ["powershell", "Get processes containing pending-monitor"]),
        _Proc(2, "python.exe", ["python", "-m", "src.cli", "pending-monitor"]),
    ])})()
    monkeypatch.setitem(__import__("sys").modules, "psutil", fake)

    rows, note = monitor_audit._running_processes()

    assert note is None
    assert [(row["pid"], row["label"]) for row in rows] == [(2, "pending-monitor")]


def test_watchlist_and_pending_are_complementary_not_duplicate(monkeypatch):
    monkeypatch.setattr(monitor_audit, "_running_processes", lambda: ([
        {"pid": 1, "label": "monitor-watchlist", "cmd": "watch", "started": 0},
        {"pid": 2, "label": "pending-monitor", "cmd": "pending", "started": 0},
    ], None))
    monkeypatch.setattr(monitor_audit, "_leader_locks", lambda root: [])
    assert not any("mexc-canary-monitor" in warning for warning in monitor_audit.audit()["warnings"])


def test_same_role_duplicate_is_still_reported(monkeypatch):
    monkeypatch.setattr(monitor_audit, "_running_processes", lambda: ([
        {"pid": 1, "label": "pending-monitor", "cmd": "pending-1", "started": 0},
        {"pid": 2, "label": "pending-monitor", "cmd": "pending-2", "started": 0},
    ], None))
    monkeypatch.setattr(monitor_audit, "_leader_locks", lambda root: [])
    assert any("2 pending-monitor" in warning for warning in monitor_audit.audit()["warnings"])


def test_mexc_canary_leader_and_standby_are_not_reported_as_duplicate(monkeypatch):
    monkeypatch.setattr(monitor_audit, "_running_processes", lambda: ([
        {"pid": 1, "label": "mexc-canary-monitor", "cmd": "mexc-1", "started": 0},
        {"pid": 2, "label": "mexc-canary-monitor", "cmd": "mexc-2", "started": 0},
    ], None))
    monkeypatch.setattr(monitor_audit, "_leader_locks", lambda root: [])
    assert not any("mexc-canary-monitor" in warning for warning in monitor_audit.audit()["warnings"])
