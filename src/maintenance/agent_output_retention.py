"""Retention for disposable on-disk agent output snapshots.

Agents persist a timestamped JSON output on every run. Consumers read the
newest matching output, so retaining an unlimited history only consumes disk
and can eventually prevent SQLite from recording health heartbeats. This
module deliberately touches only regular ``*.json`` files beneath the given
agent-output directory; it never changes SQLite, trading records, configs, or
the latest retained snapshots.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


DEFAULT_DAYS = 7


def _now(now: datetime | None = None) -> datetime:
    return now or datetime.now(timezone.utc)


def _cutoff(days: int, now: datetime | None = None) -> datetime:
    if days < 1:
        raise ValueError("days must be at least 1")
    return _now(now) - timedelta(days=days)


def _candidate_files(output_dir: Path, cutoff: datetime) -> list[Path]:
    if not output_dir.exists():
        return []
    cutoff_ts = cutoff.timestamp()
    return [
        path for path in output_dir.glob("*.json")
        if path.is_file() and not path.is_symlink() and path.stat().st_mtime < cutoff_ts
    ]


def plan(
    output_dir: str | Path = "data/processed/agent_outputs",
    *,
    days: int = DEFAULT_DAYS,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Return the exact disposable snapshot set without changing files."""
    root = Path(output_dir).resolve()
    cutoff = _cutoff(days, now)
    candidates = _candidate_files(root, cutoff)
    retained = [path for path in root.glob("*.json") if path.is_file()] if root.exists() else []
    bytes_to_remove = sum(path.stat().st_size for path in candidates)
    return {
        "output_dir": str(root),
        "days": days,
        "cutoff": cutoff.isoformat(),
        "candidate_files": len(candidates),
        "candidate_bytes": bytes_to_remove,
        "candidate_mb": round(bytes_to_remove / 1_000_000, 1),
        "retained_files": len(retained) - len(candidates),
    }


def run(
    output_dir: str | Path = "data/processed/agent_outputs",
    *,
    days: int = DEFAULT_DAYS,
    dry_run: bool = True,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Remove only old disposable JSON snapshots. Dry-run by default."""
    result = plan(output_dir, days=days, now=now)
    result["dry_run"] = dry_run
    result["removed_files"] = 0
    result["removed_bytes"] = 0
    if dry_run:
        return result

    root = Path(result["output_dir"])
    cutoff = _cutoff(days, now)
    for path in _candidate_files(root, cutoff):
        try:
            size = path.stat().st_size
            path.unlink()
        except FileNotFoundError:
            continue
        result["removed_files"] += 1
        result["removed_bytes"] += size
    result["removed_mb"] = round(result["removed_bytes"] / 1_000_000, 1)
    return result
