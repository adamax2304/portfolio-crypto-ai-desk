"""Short, independent OpenRouter quality-agent maintenance cycle.

This runner is intentionally separate from the long market/research scheduler.
It refreshes the advisory cache, records router metrics and publishes an atomic
heartbeat even when there are no new news events to classify.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterator

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

HEARTBEAT_PATH = ROOT / "data" / "runtime" / "llm_quality_refresh.heartbeat.json"
LOCK_PATH = ROOT / "data" / "runtime_locks" / "llm_quality_refresh.lock"
DEFAULT_STALE_AFTER_MINUTES = 45.0


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _pid_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        import psutil  # type: ignore

        return psutil.pid_exists(pid) and psutil.Process(pid).is_running()
    except Exception:
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False


@contextmanager
def _lease(path: Path = LOCK_PATH) -> Iterator[bool]:
    """Prevent overlapping scheduled runs without displacing a live owner."""
    path.parent.mkdir(parents=True, exist_ok=True)
    acquired = False
    descriptor: int | None = None
    for _ in range(2):
        try:
            descriptor = os.open(str(path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            payload = json.dumps({"pid": os.getpid(), "started_at": _utc_now().isoformat()})
            os.write(descriptor, payload.encode("utf-8"))
            acquired = True
            break
        except FileExistsError:
            try:
                owner = json.loads(path.read_text(encoding="utf-8"))
                owner_pid = int(owner.get("pid") or 0)
            except Exception:
                owner_pid = 0
            if _pid_alive(owner_pid):
                break
            try:
                path.unlink(missing_ok=True)
            except OSError:
                break
    try:
        yield acquired
    finally:
        if descriptor is not None:
            os.close(descriptor)
        if acquired:
            path.unlink(missing_ok=True)


def _atomic_write(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + f".{os.getpid()}.tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    os.replace(tmp, path)


def _load_schedule_config(root: Path = ROOT) -> dict[str, Any]:
    try:
        import yaml

        raw = yaml.safe_load((root / "config" / "quality_agents.yaml").read_text(encoding="utf-8")) or {}
        quality = raw.get("quality_agents") or {}
        refresh = quality.get("llm_advisory_refresh") or {}
        return {
            "required": bool(quality.get("enabled", False) and refresh.get("enabled", False)),
            "interval_minutes": float(refresh.get("interval_minutes") or 15),
            "stale_after_minutes": float(
                refresh.get("stale_after_minutes") or DEFAULT_STALE_AFTER_MINUTES
            ),
        }
    except Exception:
        return {
            "required": True,
            "interval_minutes": 15.0,
            "stale_after_minutes": DEFAULT_STALE_AFTER_MINUTES,
        }


def health_snapshot(
    *,
    root: Path = ROOT,
    now: datetime | None = None,
) -> dict[str, Any]:
    config = _load_schedule_config(root)
    heartbeat = root / "data" / "runtime" / "llm_quality_refresh.heartbeat.json"
    try:
        payload = json.loads(heartbeat.read_text(encoding="utf-8"))
    except FileNotFoundError:
        payload = {}
    except (OSError, ValueError, json.JSONDecodeError):
        payload = {"status": "INVALID_HEARTBEAT"}
    completed_at = payload.get("completed_at") or payload.get("started_at")
    age_minutes: float | None = None
    if completed_at:
        try:
            stamp = datetime.fromisoformat(str(completed_at).replace("Z", "+00:00"))
            if stamp.tzinfo is None:
                stamp = stamp.replace(tzinfo=timezone.utc)
            age_minutes = max(
                0.0,
                ((now or _utc_now()).astimezone(timezone.utc) - stamp).total_seconds() / 60.0,
            )
        except (TypeError, ValueError):
            pass
    stale_after = float(config["stale_after_minutes"])
    return {
        **payload,
        **config,
        "age_minutes": age_minutes,
        "stale": bool(config["required"] and (age_minutes is None or age_minutes > stale_after)),
        "heartbeat_path": str(heartbeat),
    }


def run_once(
    *,
    force: bool = False,
    lookback_hours: float | None = None,
    max_events: int | None = None,
    refresh_fn: Callable[..., dict[str, Any]] | None = None,
    metrics_fn: Callable[..., dict[str, Any]] | None = None,
    db_path: str | Path | None = None,
    now_fn: Callable[[], datetime] = _utc_now,
    heartbeat_path: Path = HEARTBEAT_PATH,
) -> dict[str, Any]:
    from src.config import load_config
    from src.llm_router.metrics import routing_metrics
    from src.quality_agents.llm_advisory import refresh_openrouter_advisory

    refresh = refresh_fn or refresh_openrouter_advisory
    metrics = metrics_fn or routing_metrics
    started = now_fn()
    running = {
        "status": "RUNNING",
        "pid": os.getpid(),
        "started_at": started.isoformat(),
        "completed_at": None,
    }
    _atomic_write(heartbeat_path, running)
    result: dict[str, Any] = dict(running)
    try:
        advisory = refresh(
            lookback_hours=lookback_hours,
            max_events=max_events,
            force=force,
        )
        configured_db = db_path if db_path is not None else load_config().db_path
        try:
            router_metrics = metrics(
                db_path=configured_db, hours=24.0, include_provider_usage=True,
            )
        except Exception as exc:
            # Cost telemetry is observability, not part of the advisory result.
            # A temporary metrics read lock must not invalidate fresh agent
            # assessments or trigger a false trading-system outage alert.
            router_metrics = {
                "status": "DEGRADED",
                "error": f"{type(exc).__name__}: {exc}",
            }
        advisory_status = str(advisory.get("status") or "ERROR").upper()
        disabled_by_config = (
            advisory_status == "DISABLED"
            and advisory.get("reason") == "LLM_ADVISORY_DISABLED"
        )
        if advisory_status == "OK":
            status = "OK"
        elif disabled_by_config:
            status = "DISABLED"
        elif advisory_status == "BUDGET_PAUSED":
            status = "BUDGET_PAUSED"
        elif advisory_status == "DEGRADED":
            status = "DEGRADED"
        else:
            status = "ERROR"
        result.update(
            status=status,
            advisory=advisory,
            metrics=router_metrics,
            error=advisory.get("error") if status != "OK" else None,
        )
    except Exception as exc:
        result.update(
            status="ERROR",
            advisory=None,
            metrics=None,
            error=f"{type(exc).__name__}: {exc}",
        )
    completed = now_fn()
    result.update(
        completed_at=completed.isoformat(),
        duration_seconds=round(max(0.0, (completed - started).total_seconds()), 3),
    )
    _atomic_write(heartbeat_path, result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--once", action="store_true", help="run one bounded refresh (default)")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--lookback-hours", type=float, default=None)
    parser.add_argument("--max-events", type=int, default=None)
    args = parser.parse_args()
    with _lease() as acquired:
        if not acquired:
            print(json.dumps({"status": "SKIPPED", "reason": "refresh_already_running"}))
            return 0
        result = run_once(
            force=args.force,
            lookback_hours=args.lookback_hours,
            max_events=args.max_events,
        )
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, default=str))
    return 0 if result.get("status") in {"OK", "DISABLED", "BUDGET_PAUSED"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
