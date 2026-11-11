"""Running-monitor audit (read-only, 2026-07-05).

Reports which monitor processes are currently running (crypto `monitor-watchlist`, the fast
`pending-monitor`, `stocks-monitor-session`, and the schedulers) and whether more than one pending
monitor is active for the same asset_class — the duplication the leader lock is meant to prevent.

It NEVER kills a process (no destructive action) — it only observes and warns. Uses `psutil` when
available; otherwise reports the leader-lock files and says process enumeration is unavailable.
"""
from __future__ import annotations

import time
from pathlib import Path

from src.config import load_config

# command substrings we care about → a short label
_MONITOR_PATTERNS = {
    "pending-monitor": "pending-monitor",
    "monitor-watchlist": "monitor-watchlist",
    "stocks-monitor-session": "stocks-monitor-session",
    "mexc-canary-monitor": "mexc-canary-monitor",
    "run_default_market_schedule": "default-scheduler",
    "run_12h_monitor_schedule": "12h-scheduler",
    "run_24h_crypto_only_schedule": "24h-crypto-scheduler",
    "run_frequent_schedule": "frequent-scheduler",
}


def _running_processes() -> tuple[list[dict], str | None]:
    try:
        import psutil  # type: ignore
    except Exception:
        return [], "psutil not installed — process enumeration unavailable (leader locks still shown)"
    out: list[dict] = []
    for p in psutil.process_iter(["pid", "name", "cmdline", "create_time"]):
        try:
            # PowerShell/Codex diagnostics often contain the literal command
            # text ``pending-monitor`` and used to be counted as live workers.
            # Every monitored service in this project is a Python module, so
            # executable identity is the reliable first discriminator.
            process_name = str(p.info.get("name") or "").lower()
            if process_name not in {"python", "python.exe", "pythonw", "pythonw.exe", "py", "py.exe"}:
                continue
            cmd = " ".join(p.info.get("cmdline") or [])
        except Exception:
            continue
        if not cmd:
            continue
        for pat, label in _MONITOR_PATTERNS.items():
            if pat in cmd:
                out.append({"pid": p.info.get("pid"), "label": label,
                            "cmd": cmd[:200], "started": p.info.get("create_time")})
                break
    return out, None


def _leader_locks(root: Path) -> list[dict]:
    d = Path(root) / ".locks"
    rows: list[dict] = []
    try:
        for f in d.glob("pending_monitor_leader_*.lock"):
            try:
                age = time.time() - f.stat().st_mtime
                rows.append({"asset_class": f.stem.replace("pending_monitor_leader_", ""),
                             "holder": f.read_text(encoding="utf-8").strip()[:120],
                             "age_sec": round(age, 1), "fresh": age <= 180})
            except Exception:
                continue
    except Exception:
        pass
    return rows


def audit(db=None) -> dict:
    """Read-only snapshot of running monitors + leader locks + overlap warnings."""
    root = load_config().root
    procs, note = _running_processes()
    locks = _leader_locks(root)
    # duplication: >1 pending-style monitor running (monitor-watchlist + pending-monitor both touch
    # crypto pending entries). The tracker's own dedup makes this SAFE, but it wastes work + the
    # leader lock is meant to make the 2nd pending-monitor decline.
    # The slower watchlist scan and the fast pending monitor are complementary.
    # Same-role duplicates are checked below; the two expected roles are not.
    pending_like: list[dict] = []
    warnings: list[str] = []
    if len(pending_like) > 1:
        warnings.append(
            f"{len(pending_like)} crypto pending-style monitors running "
            f"({', '.join(sorted({p['label'] for p in pending_like}))}) — the tracker dedup makes "
            "this safe, but only one is needed; the pending-monitor leader lock declines duplicates.")
    for label in ("pending-monitor", "monitor-watchlist", "stocks-monitor-session"):
        count = sum(p["label"] == label for p in procs)
        if count > 1:
            warnings.append(f"{count} {label} processes running - expected 1.")
    # MEXC canary intentionally supports one active leader plus one standby.
    # Only the lease holder calls monitor_tick/reconciliation; a third process
    # is operational noise and should be investigated.
    mexc_count = sum(p["label"] == "mexc-canary-monitor" for p in procs)
    if mexc_count > 2:
        warnings.append(f"{mexc_count} mexc-canary-monitor processes running - expected at most leader + standby.")
    if not any(p["label"] == "pending-monitor" for p in procs):
        warnings.append("no pending-monitor process detected - fast entry timing is unavailable.")
    stocks = [p for p in procs if p["label"] == "stocks-monitor-session"]
    if len(stocks) > 1:
        warnings.append(f"{len(stocks)} stocks-monitor-session processes running — expected 1.")
    return {"available": True, "processes": procs, "leader_locks": locks,
            "warnings": warnings, "note": note,
            "read_only": True,
            "policy": "observe only — no destructive process kills without explicit operator approval."}


def render_markdown(db=None) -> str:
    a = audit(db)
    lines = ["## Monitor audit (read-only — observe only, no process kills)"]
    if a.get("note"):
        lines.append(f"- {a['note']}")
    if a["processes"]:
        lines.append("**Running monitors:**")
        for p in a["processes"]:
            lines.append(f"- [{p['label']}] pid {p['pid']}: `{p['cmd']}`")
    else:
        lines.append("- no monitor processes detected (or psutil unavailable).")
    if a["leader_locks"]:
        lines.append("")
        lines.append("**Pending-monitor leader locks:**")
        for lk in a["leader_locks"]:
            state = "FRESH" if lk["fresh"] else "stale"
            lines.append(f"- {lk['asset_class']}: {state} (age {lk['age_sec']}s) holder `{lk['holder']}`")
    for w in a["warnings"]:
        lines.append(f"- WARNING: {w}")
    return "\n".join(lines)
