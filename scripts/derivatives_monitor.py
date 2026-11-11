"""Forward derivatives current-state and liquidation monitor."""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sqlite3
import subprocess
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

from src.data_collectors import market_intelligence_store as mi
from src.data_collectors.derivatives_pipeline import DerivativesPipeline, active_symbols, liquidation_event_id
from src.data_collectors.liquidity_collector import LiquidityCollector


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MONITOR_LOCK = PROJECT_ROOT / ".locks" / "derivatives_monitor.pid"
HEARTBEAT_PATH = PROJECT_ROOT / "data" / "runtime_locks" / "derivatives_monitor.heartbeat.json"
FAST_FLUSH_HEARTBEAT_PATH = (
    PROJECT_ROOT / "data" / "runtime_locks" / "fast_flush_paper.heartbeat.json"
)
COOLDOWN_REFRESH_SECONDS = 300
SOURCE_TIMEOUT_SECONDS = 180
PROGRESS_HEARTBEAT_SECONDS = 30
FAST_FLUSH_CADENCE_SECONDS = 15
# Fifteen-minute snapshots retain replay evidence without copying the one-minute
# universe every five minutes while the forward Paper profiles are running.
FAST_FLUSH_ARCHIVE_SECONDS = 900
FAST_FLUSH_REPORT_SECONDS = 60
FAST_FLUSH_SETTLE_SECONDS = 1.5


def _retry_sqlite_locked(func, *args, attempts: int = 3, delay_seconds: float = 0.5, **kwargs):
    """Retry only transient SQLite writer contention; propagate every other error."""
    for attempt in range(attempts):
        try:
            return func(*args, **kwargs)
        except sqlite3.OperationalError as exc:
            if "locked" not in str(exc).lower() or attempt + 1 >= attempts:
                raise
            time.sleep(delay_seconds * (attempt + 1))
    raise RuntimeError("unreachable sqlite retry state")


def _aligned_delay(cadence_seconds: float, settle_seconds: float = 0.0) -> float:
    """Seconds until the next wall-clock cadence boundary plus settle time."""
    cadence = max(1.0, float(cadence_seconds))
    now = time.time()
    shifted = now - float(settle_seconds)
    next_tick = (int(shifted // cadence) + 1) * cadence + float(settle_seconds)
    return max(0.05, next_tick - now)


async def _constant_result(value):
    """Return a precomputed disabled-lane result without starting a thread."""
    return value


def _write_heartbeat(stage: str, *, status: str = "OK", detail: dict | None = None) -> None:
    """Publish worker progress even when the liquidation tape is quiet."""
    payload = {
        "at": datetime.now(timezone.utc).isoformat(),
        "pid": os.getpid(),
        "stage": str(stage),
        "status": str(status),
        "detail": detail or {},
    }
    HEARTBEAT_PATH.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(payload, sort_keys=True)
    for attempt in range(3):
        temporary = HEARTBEAT_PATH.with_name(
            f"{HEARTBEAT_PATH.name}.{os.getpid()}.{time.monotonic_ns()}.tmp"
        )
        try:
            temporary.write_text(encoded, encoding="utf-8")
            temporary.replace(HEARTBEAT_PATH)
            return
        except PermissionError:
            try:
                temporary.unlink()
            except FileNotFoundError:
                pass
            time.sleep(0.05 * (attempt + 1))
        except OSError:
            try:
                temporary.unlink()
            except FileNotFoundError:
                pass
            time.sleep(0.05 * (attempt + 1))


def _write_fast_flush_heartbeat(*, status: str, detail: dict | None = None) -> None:
    """Expose the latency-critical Paper lane independently of the main worker."""
    payload = {
        "at": datetime.now(timezone.utc).isoformat(),
        "pid": os.getpid(),
        "status": str(status),
        "cadence_seconds": FAST_FLUSH_CADENCE_SECONDS,
        "detail": detail or {},
    }
    FAST_FLUSH_HEARTBEAT_PATH.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(payload, sort_keys=True, default=str)
    temporary = FAST_FLUSH_HEARTBEAT_PATH.with_name(
        f"{FAST_FLUSH_HEARTBEAT_PATH.name}.{os.getpid()}.{time.monotonic_ns()}.tmp"
    )
    try:
        temporary.write_text(encoded, encoding="utf-8")
        temporary.replace(FAST_FLUSH_HEARTBEAT_PATH)
    except OSError:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass


def _pid_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    if pid == os.getpid():
        return True
    if os.name == "nt":
        try:
            result = subprocess.run(
                ["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            return str(pid) in (result.stdout or "")
        except OSError:
            return False
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def _acquire_monitor_lock() -> bool:
    """Allow exactly one derivatives writer, including manual launches."""
    MONITOR_LOCK.parent.mkdir(parents=True, exist_ok=True)
    for _ in range(2):
        try:
            fd = os.open(MONITOR_LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            try:
                owner = int(MONITOR_LOCK.read_text(encoding="utf-8").strip())
            except (OSError, ValueError):
                owner = 0
            if owner and _pid_alive(owner):
                return False
            try:
                MONITOR_LOCK.unlink()
            except FileNotFoundError:
                pass
            continue
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(str(os.getpid()))
        return True
    return False


def _release_monitor_lock() -> None:
    try:
        if MONITOR_LOCK.read_text(encoding="utf-8").strip() == str(os.getpid()):
            MONITOR_LOCK.unlink()
    except FileNotFoundError:
        pass


async def _nonfatal_thread(label: str, func, *args, **kwargs):
    """Keep one sidecar write failure from skipping the rest of a poll."""
    timeout_seconds = float(kwargs.pop("_timeout_seconds", SOURCE_TIMEOUT_SECONDS))
    started = time.monotonic()
    task = asyncio.create_task(asyncio.to_thread(func, *args, **kwargs))
    try:
        while True:
            elapsed = time.monotonic() - started
            remaining = timeout_seconds - elapsed
            if remaining <= 0:
                task.cancel()
                _write_heartbeat(
                    "source_refresh_timed_out",
                    status="DEGRADED",
                    detail={"source": label, "elapsed_seconds": round(elapsed, 1)},
                )
                return {"error": f"{label}:TimeoutError:>{timeout_seconds:.0f}s"}
            try:
                result = await asyncio.wait_for(
                    asyncio.shield(task),
                    timeout=min(PROGRESS_HEARTBEAT_SECONDS, remaining),
                )
                _write_heartbeat(
                    "source_refresh_completed",
                    detail={"source": label, "elapsed_seconds": round(time.monotonic() - started, 1)},
                )
                return result
            except asyncio.TimeoutError:
                elapsed = time.monotonic() - started
                if elapsed >= timeout_seconds:
                    task.cancel()
                    _write_heartbeat(
                        "source_refresh_timed_out",
                        status="DEGRADED",
                        detail={"source": label, "elapsed_seconds": round(elapsed, 1)},
                    )
                    return {"error": f"{label}:TimeoutError:>{timeout_seconds:.0f}s"}
                _write_heartbeat(
                    "source_refresh_in_progress",
                    detail={"source": label, "elapsed_seconds": round(elapsed, 1)},
                )
    except Exception as exc:  # noqa: BLE001 - background observability boundary
        _write_heartbeat(
            "source_refresh_failed",
            status="DEGRADED",
            detail={
                "source": label,
                "elapsed_seconds": round(time.monotonic() - started, 1),
                "error": type(exc).__name__,
            },
        )
        return {"error": f"{label}:{type(exc).__name__}:{str(exc)[:300]}"}


async def _serial_local_thread(label: str, func, *args, **kwargs):
    """Wait for a bounded local job without spawning overlapping retries.

    ``asyncio.to_thread`` cannot kill its worker after a timeout. Returning on a
    timeout would therefore let the next cadence launch a second SQLite writer
    while the first one is still running. Fast-flush Paper evaluation is local
    and finite, so keep one in-flight call and publish progress until it exits.
    """
    started = time.monotonic()
    task = asyncio.create_task(asyncio.to_thread(func, *args, **kwargs))
    try:
        while not task.done():
            done, _ = await asyncio.wait({task}, timeout=PROGRESS_HEARTBEAT_SECONDS)
            if done:
                break
            _write_heartbeat(
                "source_refresh_in_progress",
                detail={"source": label, "elapsed_seconds": round(time.monotonic() - started, 1)},
            )
        result = await task
        _write_heartbeat(
            "source_refresh_completed",
            detail={"source": label, "elapsed_seconds": round(time.monotonic() - started, 1)},
        )
        return result
    except Exception as exc:  # noqa: BLE001 - background observability boundary
        _write_heartbeat(
            "source_refresh_failed",
            status="DEGRADED",
            detail={
                "source": label,
                "elapsed_seconds": round(time.monotonic() - started, 1),
                "error": type(exc).__name__,
            },
        )
        return {"error": f"{label}:{type(exc).__name__}:{str(exc)[:300]}"}


async def _gather_with_progress(*awaitables):
    """Keep the worker heartbeat fresh while bounded providers are running."""
    group = asyncio.gather(*awaitables)
    started = time.monotonic()
    while not group.done():
        try:
            return await asyncio.wait_for(
                asyncio.shield(group), timeout=PROGRESS_HEARTBEAT_SECONDS,
            )
        except asyncio.TimeoutError:
            _write_heartbeat(
                "current_refresh_in_progress",
                detail={"elapsed_seconds": round(time.monotonic() - started, 1)},
            )
    return await group


async def current_loop(pipeline: DerivativesPipeline, stop_at: float, cadence: int) -> None:
    liquidity = LiquidityCollector(db_path=pipeline.db_path, trading_db_path=pipeline.trading_db_path)
    next_cooldown_refresh = 0.0
    while time.monotonic() < stop_at:
        _write_heartbeat("current_refresh_started")
        try:
            from src.intelligence.market_risk_context import refresh as refresh_market_risk
            # Independent collection calls used to run serially.  The shadow
            # tick still waits for all completed snapshots, but one slow
            # provider no longer adds its full duration to every other feed.
            from src.execution import crypto_derivreset_v3_shadow as derivreset_v3
            from src.execution import crypto_htf_liquidity_reclaim_shadow as htf_reclaim
            derivreset_enabled = bool(derivreset_v3.load_strategy_config().get("feature_flag"))
            htf_reclaim_enabled = bool(htf_reclaim.load_strategy_config().get("feature_flag"))
            result, liquidity_result, risk, shadow_ohlcv, htf_reclaim_ohlcv = await _gather_with_progress(
                _nonfatal_thread("derivatives_current", pipeline.refresh_current),
                _nonfatal_thread("liquidity", liquidity.refresh),
                _nonfatal_thread("market_risk", refresh_market_risk, db_path=pipeline.db_path),
                _nonfatal_thread("derivreset_v3_ohlcv", derivreset_v3.refresh_ohlcv)
                if derivreset_enabled else _constant_result({"status": "archived"}),
                _nonfatal_thread("htf_liquidity_reclaim_ohlcv", htf_reclaim.refresh_ohlcv)
                if htf_reclaim_enabled else _constant_result({"status": "archived"}),
            )
            cooldown_result = {"skipped": "not_due"}
            if time.monotonic() >= next_cooldown_refresh:
                from src.execution import crypto_quality_overlay as quality_overlay
                cooldown_result = await _nonfatal_thread(
                    "crypto_quality_cooldowns",
                    quality_overlay.refresh_cooldowns,
                    db=str(pipeline.trading_db_path),
                )
                next_cooldown_refresh = time.monotonic() + COOLDOWN_REFRESH_SECONDS
            # The event-sequence experiment evaluates only the freshly observed,
            # closed-bar state and persists exclusively to its own Shadow tables.
            shadow_v3 = (
                await _serial_local_thread("derivreset_v3_tick", derivreset_v3.tick)
                if derivreset_enabled else {"enabled": False, "rows": [], "event_counts": {}}
            )
            shadow_v3_report = None if shadow_v3.get("error") else await _nonfatal_thread(
                "derivreset_v3_report", derivreset_v3.write_report, shadow_v3)
            # The short-retest experiment reuses the same freshly collected
            # OHLCV/derivatives snapshots, but owns separate state and outcomes.
            from src.execution import crypto_short_retest_shadow as short_retest
            short_retest_enabled = bool(short_retest.load_strategy_config().get("feature_flag"))
            short_retest_result = (
                await _serial_local_thread("short_retest_tick", short_retest.tick)
                if short_retest_enabled else {"enabled": False, "rows": [], "event_counts": {}}
            )
            short_retest_report = (
                None if short_retest_result.get("error")
                else await _nonfatal_thread(
                    "short_retest_report", short_retest.write_report,
                    short_retest_result,
                )
            )
            # Liquidity Sweep v1 is an operator-approved long-only canary
            # bridge. v2 below remains the Paper-only reclaim lane.
            from src.execution import crypto_liquidity_sweep_shadow as liquidity_sweep
            from src.execution import crypto_liquidity_sweep_reclaim_paper as liquidity_sweep_v2
            from src.live_execution.crypto_liquidity_sweep_bridge import capture_forward_sweeps
            liquidity_sweep_enabled = bool(liquidity_sweep.load_strategy_config().get("feature_flag"))
            liquidity_sweep_v2_enabled = bool(
                liquidity_sweep_v2.load_strategy_config().get("feature_flag")
            )
            liquidity_sweep_result = (
                await _serial_local_thread(
                    "liquidity_sweep_tick", _retry_sqlite_locked, liquidity_sweep.tick,
                )
                if liquidity_sweep_enabled else {"enabled": False, "rows": []}
            )
            liquidity_sweep_live = (
                {"status": "SKIPPED_SOURCE_ERROR", "queued": 0}
                if liquidity_sweep_result.get("error")
                else await _serial_local_thread(
                    "liquidity_sweep_live_bridge",
                    capture_forward_sweeps,
                    liquidity_sweep_result.get("rows") or [],
                )
            )
            liquidity_sweep_report = (
                None if liquidity_sweep_result.get("error")
                else await _nonfatal_thread(
                    "liquidity_sweep_report", liquidity_sweep.write_report,
                    liquidity_sweep_result,
                )
            )
            liquidity_sweep_v2_result = (
                await _serial_local_thread(
                    "liquidity_sweep_v2_paper_tick", _retry_sqlite_locked,
                    liquidity_sweep_v2.tick,
                )
                if liquidity_sweep_v2_enabled
                else {"enabled": False, "rows": [], "summary_by_profile": {}}
            )
            liquidity_sweep_v2_report = (
                None if liquidity_sweep_v2_result.get("error")
                else await _nonfatal_thread(
                    "liquidity_sweep_v2_paper_report", liquidity_sweep_v2.write_report,
                    liquidity_sweep_v2_result,
                )
            )
            # This slower continuation experiment shares only freshly
            # collected public inputs. Its cache, rows and evidence remain
            # completely independent from the 5m reversal lane.
            htf_reclaim_result = (
                await _serial_local_thread("htf_liquidity_reclaim_tick", htf_reclaim.tick)
                if htf_reclaim_enabled
                else {"enabled": False, "rows": [], "summary_by_profile": {}}
            )
            htf_reclaim_report = (
                None if htf_reclaim_result.get("error")
                else await _nonfatal_thread(
                    "htf_liquidity_reclaim_report", htf_reclaim.write_report,
                    htf_reclaim_result,
                )
            )
            print(json.dumps({"at": mi.utc_now_iso(), "current": result, "liquidity": liquidity_result,
                              "market_risk_context": risk,
                              "crypto_quality_cooldowns": cooldown_result,
                              "derivreset_v3": {
                                  "enabled": shadow_v3.get("enabled"),
                                  "ohlcv": shadow_ohlcv,
                                  "new": len(shadow_v3.get("rows") or []),
                                  "matured": shadow_v3.get("closed_matured", 0),
                                  "pending": (shadow_v3.get("event_counts") or {}).get("pending", 0),
                                  "verdict": (shadow_v3.get("summary") or {}).get("verdict"),
                                  "report": shadow_v3_report,
                              },
                              "short_retest": {
                                  "enabled": short_retest_result.get("enabled"),
                                  "new": len(short_retest_result.get("rows") or []),
                                  "matured": short_retest_result.get("closed_matured", 0),
                                  "pending": (short_retest_result.get("event_counts") or {}).get("pending", 0),
                                  "verdict": (short_retest_result.get("strict_summary") or {}).get("verdict"),
                                  "report": short_retest_report,
                              },
                              "liquidity_sweep": {
                                  "enabled": liquidity_sweep_result.get("enabled"),
                                  "source_error": liquidity_sweep_result.get("error"),
                                  "new": len(liquidity_sweep_result.get("rows") or []),
                                  "matured": liquidity_sweep_result.get("closed_matured", 0),
                                   "verdict": (liquidity_sweep_result.get("summary") or {}).get("verdict"),
                                   "liquidation_events_available": liquidity_sweep_result.get("liquidation_events_available"),
                                   "live_bridge": liquidity_sweep_live,
                                   "report": liquidity_sweep_report,
                              },
                              "liquidity_sweep_v2_paper": {
                                  "enabled": liquidity_sweep_v2_result.get("enabled"),
                                  "source_error": liquidity_sweep_v2_result.get("error"),
                                  "new": len(liquidity_sweep_v2_result.get("rows") or []),
                                  "entered": liquidity_sweep_v2_result.get("entered_from_pending", 0),
                                  "matured": liquidity_sweep_v2_result.get("closed_matured", 0),
                                  "verdicts": {name: value.get("verdict") for name, value in
                                               (liquidity_sweep_v2_result.get("summary_by_profile") or {}).items()},
                                  "report": liquidity_sweep_v2_report,
                              },
                              "fast_flush_v3_paper": {
                                  "enabled": True,
                                  "source_error": None,
                                  "delegated": "independent_15s_paper_loop",
                              },
                              "htf_liquidity_reclaim": {
                                  "ohlcv": htf_reclaim_ohlcv,
                                  "enabled": htf_reclaim_result.get("enabled"),
                                  "new_pending": len(htf_reclaim_result.get("rows") or []),
                                  "entered": htf_reclaim_result.get("entered_from_pending", 0),
                                  "matured": htf_reclaim_result.get("closed_matured", 0),
                                  "verdicts": {name: value.get("verdict") for name, value in
                                               (htf_reclaim_result.get("summary_by_profile") or {}).items()},
                                  "report": htf_reclaim_report,
                              }}, default=str), flush=True)
            _write_heartbeat(
                "current_refresh_completed",
                detail={
                    "liquidity_sweep_new": len(liquidity_sweep_result.get("rows") or []),
                    "liquidity_sweep_v2_paper_new": len(liquidity_sweep_v2_result.get("rows") or []),
                    "fast_flush_v3_paper": "independent_15s_loop",
                    "htf_reclaim_new": len(htf_reclaim_result.get("rows") or []),
                },
            )
        except Exception as exc:
            # The monitor is a long-running fail-open collector. One transient
            # network/SQLite failure is a missed poll, not a reason to exit.
            print(json.dumps({"at": mi.utc_now_iso(), "current_error": str(exc)}, default=str), flush=True)
            _write_heartbeat(
                "current_refresh_failed", status="ERROR", detail={"error": type(exc).__name__}
            )
        remaining = max(0.0, stop_at - time.monotonic())
        if remaining:
            await asyncio.sleep(min(max(10, cadence), remaining))


async def fast_flush_paper_loop(pipeline: DerivativesPipeline, stop_at: float,
                                cadence: int = FAST_FLUSH_CADENCE_SECONDS) -> None:
    """Run the 1m Paper comparison independently of slower research lanes."""
    from src.execution import crypto_fast_flush_reclaim_paper as fast_flush_v3

    next_report = 0.0
    while time.monotonic() < stop_at:
        started = time.monotonic()
        result = await _serial_local_thread(
            "fast_flush_v3_paper_tick",
            fast_flush_v3.tick,
        )
        report: dict | str | None = None
        if not result.get("error") and started >= next_report:
            report = await _nonfatal_thread(
                "fast_flush_v3_paper_report",
                fast_flush_v3.write_report,
                result,
                _timeout_seconds=20,
            )
            next_report = started + FAST_FLUSH_REPORT_SECONDS
        elapsed = round(time.monotonic() - started, 3)
        heartbeat_detail = {
            "elapsed_seconds": elapsed,
            "new": len(result.get("rows") or []),
            "matured": result.get("closed_matured", 0),
            "expired_pending": result.get("expired_pending", 0),
            "funnel": result.get("funnel"),
            "timings_ms": result.get("timings_ms"),
            "liquidation_source": result.get("liquidation_source"),
            "candidate_refresh": result.get("candidate_refresh"),
            "error": result.get("error"),
        }
        heartbeat_status = (
            "ERROR" if result.get("error") else
            "DEGRADED" if elapsed > float(cadence) else
            "OK"
        )
        _write_fast_flush_heartbeat(status=heartbeat_status, detail=heartbeat_detail)
        print(json.dumps({
            "at": mi.utc_now_iso(),
            "fast_flush_v3_fast_loop": {
                "enabled": result.get("enabled"),
                "source_error": result.get("error"),
                "candidate_refresh": result.get("candidate_refresh"),
                "funnel": result.get("funnel"),
                "timings_ms": result.get("timings_ms"),
                "expired_pending": result.get("expired_pending", 0),
                "new": len(result.get("rows") or []),
                "matured": result.get("closed_matured", 0),
                "verdicts": {
                    name: value.get("verdict")
                    for name, value in (result.get("summary_by_profile") or {}).items()
                },
                "report": report,
                "elapsed_seconds": elapsed,
            },
        }, default=str), flush=True)
        remaining = max(0.0, stop_at - time.monotonic())
        sleep_for = _aligned_delay(cadence, FAST_FLUSH_SETTLE_SECONDS)
        if remaining:
            await asyncio.sleep(min(sleep_for, remaining))


async def fast_flush_archive_loop(pipeline: DerivativesPipeline, stop_at: float,
                                  cadence: int = FAST_FLUSH_ARCHIVE_SECONDS) -> None:
    """Archive research bars without delaying the entry-decision loop."""
    from src.data_collectors.fast_flush_research_store import archive_runtime_frames

    while time.monotonic() < stop_at:
        started = time.monotonic()
        result = await _nonfatal_thread(
            "fast_flush_v3_1m_archive",
            archive_runtime_frames,
            active_symbols(limit=60, db_path=pipeline.trading_db_path),
            _timeout_seconds=45,
        )
        print(json.dumps({
            "at": mi.utc_now_iso(),
            "fast_flush_v3_archive": result,
        }, default=str), flush=True)
        remaining = max(0.0, stop_at - time.monotonic())
        sleep_for = max(1.0, float(cadence) - (time.monotonic() - started))
        if remaining:
            await asyncio.sleep(min(sleep_for, remaining))


def _record_liquidation_health(pipeline: DerivativesPipeline, source: str, **kwargs) -> None:
    try:
        with mi.connect(pipeline.db_path) as conn:
            mi.record_source_health(conn, source, **kwargs)
            conn.commit()
    except sqlite3.Error:
        # Preserve the websocket loop when another bounded writer owns SQLite.
        pass


async def liquidation_loop(pipeline: DerivativesPipeline, stop_at: float) -> None:
    try:
        import websockets
    except ImportError:
        print("liquidations disabled: websockets package missing", flush=True)
        return
    # Current documented Binance raw-stream endpoint. The old /ws path can
    # connect but is not the supported market-stream route.
    url = "wss://fstream.binance.com/market/ws/!forceOrder@arr"
    while time.monotonic() < stop_at:
        try:
            async with websockets.connect(url, ping_interval=20, ping_timeout=20, close_timeout=5) as ws:
                _record_liquidation_health(pipeline, "liquidations:binance_ws", status="ok", success=True)
                last_heartbeat = time.monotonic()
                while time.monotonic() < stop_at:
                    try:
                        raw = await asyncio.wait_for(
                            ws.recv(), timeout=min(60.0, max(1.0, stop_at - time.monotonic())))
                    except asyncio.TimeoutError:
                        # A quiet market can legitimately have no forced-order
                        # events for hours. Keep transport health independent
                        # from writes so a connected websocket is not stale.
                        if time.monotonic() - last_heartbeat >= 300:
                            _record_liquidation_health(pipeline, "liquidations:binance_ws", status="ok", success=True)
                            last_heartbeat = time.monotonic()
                        continue
                    payload = json.loads(raw)
                    events = payload if isinstance(payload, list) else [payload]
                    with mi.connect(pipeline.db_path) as conn:
                        written = 0
                        for event in events:
                            order = event.get("o") if isinstance(event, dict) else None
                            if not isinstance(order, dict):
                                continue
                            symbol = str(order.get("s") or "")
                            written += int(mi.insert_liquidation_event(
                                conn, exchange="binance", event_id=liquidation_event_id("binance", order),
                                event_at=datetime.fromtimestamp(float(order.get("T") or event.get("E")) / 1000,
                                                                tz=timezone.utc).isoformat(),
                                symbol=symbol, side=order.get("S"), price=float(order.get("ap") or order.get("p") or 0),
                                quantity=float(order.get("z") or order.get("q") or 0), raw_json=event))
                        if written:
                            mi.record_source_health(conn, "liquidations:binance_ws", status="ok", success=True,
                                                    records_written=written)
                            last_heartbeat = time.monotonic()
                        conn.commit()
        except Exception as exc:
            if time.monotonic() >= stop_at:
                break
            _record_liquidation_health(
                pipeline, "liquidations:binance_ws", status="error", success=False, error=str(exc)[:500]
            )
            await asyncio.sleep(5)


def _bybit_liquidation_symbols(pipeline: DerivativesPipeline) -> list[str]:
    """Return actual Bybit native IDs for the sweep lane's fresh universe."""
    from src.execution import crypto_liquidity_sweep_shadow as liquidity_sweep

    with mi.connect(pipeline.db_path, ensure=False) as conn:
        cfg = liquidity_sweep.load_strategy_config()
        canonical = liquidity_sweep._symbols(conn, datetime.now(timezone.utc), cfg)
        if not canonical:
            return []
        normalized = [mi.normalize_symbol(symbol) for symbol in canonical]
        placeholders = ",".join("?" for _ in normalized)
        cutoff = (datetime.now(timezone.utc) - timedelta(
            minutes=float(cfg["derivatives_freshness_minutes"])
        )).isoformat()
        rows = conn.execute(
            "SELECT instrument_id FROM ("
            " SELECT normalized_symbol,instrument_id,"
            " ROW_NUMBER() OVER(PARTITION BY normalized_symbol ORDER BY provider_ts DESC,id DESC) rn"
            " FROM derivative_snapshots WHERE lower(exchange)='bybit'"
            f" AND normalized_symbol IN ({placeholders}) AND provider_ts>=?"
            ") WHERE rn=1 AND instrument_id IS NOT NULL AND instrument_id<>''",
            (*normalized, cutoff),
        ).fetchall()
    return list(dict.fromkeys(str(row["instrument_id"]).upper() for row in rows))


async def _bybit_subscribe_liquidations(ws, topics: list[str]) -> tuple[list[str], dict[str, str]]:
    """Subscribe one native topic at a time so one invalid listing is isolated."""
    accepted: list[str] = []
    rejected: dict[str, str] = {}
    for topic in topics:
        await ws.send(json.dumps({"op": "subscribe", "args": [topic]}))
        response = json.loads(await asyncio.wait_for(ws.recv(), timeout=10.0))
        if isinstance(response, dict) and response.get("op") == "subscribe" and response.get("success"):
            accepted.append(topic)
        else:
            rejected[topic] = str((response or {}).get("ret_msg") or response)[:240]
    return accepted, rejected


def _bybit_force_order(event: dict) -> tuple[str, str, str, float, float, str] | None:
    """Normalise Bybit's liquidated-position side to forced order side."""
    symbol = str(event.get("s") or "").upper()
    position_side = str(event.get("S") or "").upper()
    try:
        happened = int(float(event.get("T")))
        price = float(event.get("p"))
        quantity = float(event.get("v"))
    except (TypeError, ValueError):
        return None
    if not symbol or price <= 0 or quantity <= 0 or position_side not in {"BUY", "SELL"}:
        return None
    # Bybit defines S as the liquidated position side: Buy means a long was
    # liquidated, which creates a forced sell; Sell means the inverse.
    forced_side = "SELL" if position_side == "BUY" else "BUY"
    payload = {"s": symbol, "T": happened, "S": forced_side, "p": price, "q": quantity}
    return symbol, forced_side, datetime.fromtimestamp(happened / 1000, tz=timezone.utc).isoformat(), price, quantity, liquidation_event_id("bybit", payload)


async def bybit_liquidation_loop(pipeline: DerivativesPipeline, stop_at: float) -> None:
    try:
        import websockets
    except ImportError:
        print("bybit liquidations disabled: websockets package missing", flush=True)
        return
    url = "wss://stream.bybit.com/v5/public/linear"
    while time.monotonic() < stop_at:
        try:
            symbols = await asyncio.to_thread(_bybit_liquidation_symbols, pipeline)
            topics = [f"allLiquidation.{symbol}" for symbol in symbols]
            if not topics:
                await asyncio.sleep(5)
                continue
            async with websockets.connect(url, ping_interval=None, ping_timeout=None, close_timeout=5) as ws:
                accepted, rejected = await _bybit_subscribe_liquidations(ws, topics)
                if not accepted:
                    raise RuntimeError(f"Bybit liquidation subscription rejected: {rejected!r}")
                _record_liquidation_health(
                    pipeline, "liquidations:bybit_ws",
                    status="degraded" if rejected else "ok", success=True,
                    error="; ".join(f"{topic}:{reason}" for topic, reason in rejected.items())[:500] or None,
                    details={"requested_symbols": len(topics), "accepted_symbols": len(accepted),
                             "rejected_topics": sorted(rejected)},
                )
                last_heartbeat = time.monotonic()
                while time.monotonic() < stop_at:
                    try:
                        raw = await asyncio.wait_for(
                            ws.recv(), timeout=min(20.0, max(1.0, stop_at - time.monotonic())))
                    except asyncio.TimeoutError:
                        await ws.send(json.dumps({"op": "ping"}))
                        _record_liquidation_health(pipeline, "liquidations:bybit_ws", status="ok", success=True,
                                                   details={"symbols": len(accepted), "heartbeat": True,
                                                            "rejected_topics": sorted(rejected)})
                        last_heartbeat = time.monotonic()
                        continue
                    payload = json.loads(raw)
                    data = payload.get("data") if isinstance(payload, dict) else None
                    events = data if isinstance(data, list) else [data]
                    with mi.connect(pipeline.db_path) as conn:
                        written = 0
                        for event in events:
                            if not isinstance(event, dict):
                                continue
                            normalized = _bybit_force_order(event)
                            if normalized is None:
                                continue
                            symbol, side, event_at, price, quantity, event_id = normalized
                            written += int(mi.insert_liquidation_event(
                                conn, exchange="bybit", event_id=event_id, event_at=event_at,
                                symbol=symbol, side=side, price=price, quantity=quantity,
                                raw_json={"topic": payload.get("topic"), "event": event,
                                          "liquidated_position_side": event.get("S")}))
                        if written:
                            mi.record_source_health(conn, "liquidations:bybit_ws", status="ok", success=True,
                                                    records_written=written, details={"symbols": len(accepted),
                                                                                      "rejected_topics": sorted(rejected)})
                            last_heartbeat = time.monotonic()
                        conn.commit()
        except Exception as exc:
            if time.monotonic() >= stop_at:
                break
            _record_liquidation_health(pipeline, "liquidations:bybit_ws", status="error", success=False,
                                       error=str(exc)[:500])
            await asyncio.sleep(5)


def _okx_liquidation_symbols(pipeline: DerivativesPipeline) -> dict[str, str]:
    """Map the bounded research universe to OKX USDT-SWAP IDs.

    The OKX liquidation channel is subscribed at the instrument-type level,
    then filtered locally. This avoids a subscription failure for one unlisted
    alt while retaining an explicit, bounded set of symbols that can affect
    the Shadow experiments.
    """
    from src.data_collectors.derivatives_pipeline import active_symbols

    symbols = active_symbols(limit=80, db_path=pipeline.trading_db_path)
    return {f"{mi.base_symbol(symbol)}-USDT-SWAP": symbol for symbol in symbols}


def _okx_contract_multipliers(pipeline: DerivativesPipeline) -> dict[str, tuple[float, str]]:
    """Fetch OKX contract values so forced-contract counts are never called USD.

    A missing multiplier is deliberately represented by ``None`` notional at
    insert time; it remains observable but cannot inflate the strategy's
    liquidation threshold.
    """
    base = str((pipeline.cfg.sources.get("public_endpoints") or {}).get("okx") or "https://www.okx.com").rstrip("/")
    response = requests.get(f"{base}/api/v5/public/instruments", params={"instType": "SWAP"}, timeout=12)
    response.raise_for_status()
    payload = response.json()
    values: dict[str, tuple[float, str]] = {}
    for item in payload.get("data") or []:
        if not isinstance(item, dict):
            continue
        inst_id = str(item.get("instId") or "").upper()
        try:
            contract_value = float(item.get("ctVal"))
        except (TypeError, ValueError):
            continue
        if inst_id and contract_value > 0:
            values[inst_id] = (contract_value, str(item.get("ctValCcy") or "").upper())
    return values


def _okx_force_order(
    event: dict[str, object], *, multipliers: dict[str, tuple[float, str]]
) -> list[tuple[str, str, str, float, float, float | None, str]]:
    """Normalise every liquidation nested in one OKX liquidation-orders push.

    The channel's top-level ``data[i]`` element carries only ``instId`` /
    ``instType`` / ``uly``; the actual per-liquidation fields (``side``,
    ``posSide``, ``sz``, ``bkPx``, ``ts``) live inside a nested ``details``
    list, and one push can batch several liquidations for the same
    instrument (confirmed against OKX's v5 schema: ccxt's ``okx.ts``
    ``parseWsLiquidation`` reads ``safeList(liquidation, 'details', [])``).
    Reading these fields off the top-level ``event`` — the previous
    implementation — silently matched nothing on every real message, so this
    also falls back to treating ``event`` itself as one detail entry for any
    payload shape that is genuinely flat.

    ``posSide`` identifies the position that was liquidated: a liquidated
    long produces a forced sell and vice versa. ``side`` is retained only as
    a fallback for net-mode payloads. Contract size is converted with OKX's
    public ``ctVal`` metadata before it is treated as a USD notional.
    """
    instrument = str(event.get("instId") or "").upper()
    details = event.get("details")
    entries = details if isinstance(details, list) and details else [event]
    multiplier = multipliers.get(instrument)
    out: list[tuple[str, str, str, float, float, float | None, str]] = []
    for detail in entries:
        if not isinstance(detail, dict):
            continue
        position_side = str(detail.get("posSide") or "").lower()
        fallback_side = str(detail.get("side") or "").upper()
        if position_side == "long":
            forced_side = "SELL"
        elif position_side == "short":
            forced_side = "BUY"
        elif fallback_side in {"BUY", "SELL"}:
            forced_side = fallback_side
        else:
            continue
        try:
            happened = int(float(detail.get("ts")))
            price = float(detail.get("bkPx") or detail.get("fillPx") or detail.get("px"))
            contracts = float(detail.get("sz"))
        except (TypeError, ValueError):
            continue
        if not instrument or happened <= 0 or price <= 0 or contracts <= 0:
            continue
        notional_usd = None
        if multiplier:
            contract_value, contract_ccy = multiplier
            notional_usd = contracts * contract_value
            if contract_ccy not in {"USDT", "USD"}:
                notional_usd *= price
        identity = {
            "s": instrument, "T": happened, "S": forced_side, "p": price,
            "q": f"{contracts}|{detail.get('ordId') or detail.get('tradeId') or detail.get('id') or ''}",
        }
        out.append((
            instrument, forced_side, datetime.fromtimestamp(happened / 1000, tz=timezone.utc).isoformat(),
            price, contracts, notional_usd, liquidation_event_id("okx", identity),
        ))
    return out


async def _okx_subscribe_liquidations(ws) -> None:
    await ws.send(json.dumps({"op": "subscribe", "args": [{"channel": "liquidation-orders", "instType": "SWAP"}]}))
    response = json.loads(await asyncio.wait_for(ws.recv(), timeout=10.0))
    if not (isinstance(response, dict) and response.get("event") == "subscribe"
            and (response.get("arg") or {}).get("channel") == "liquidation-orders"):
        raise RuntimeError(f"OKX liquidation subscription rejected: {response!r}")


async def okx_liquidation_loop(pipeline: DerivativesPipeline, stop_at: float) -> None:
    """Record an independent OKX liquidation tape for observation only.

    This transport adds coverage diagnostics but is not an eligibility gate.
    The two strategies retain their Binance/Bybit admission sources until a
    clean forward comparison can establish that third-venue confirmation adds
    edge instead of merely reducing sample size.
    """
    try:
        import websockets
    except ImportError:
        print("OKX liquidations disabled: websockets package missing", flush=True)
        return
    url = "wss://ws.okx.com:8443/ws/v5/public"
    while time.monotonic() < stop_at:
        try:
            wanted = await asyncio.to_thread(_okx_liquidation_symbols, pipeline)
            multipliers = await asyncio.to_thread(_okx_contract_multipliers, pipeline)
            if not wanted:
                await asyncio.sleep(5)
                continue
            async with websockets.connect(url, ping_interval=None, ping_timeout=None, close_timeout=5) as ws:
                await _okx_subscribe_liquidations(ws)
                _record_liquidation_health(
                    pipeline, "liquidations:okx_ws", status="ok", success=True,
                    details={"eligible_symbols": len(wanted), "contract_multipliers": len(multipliers)},
                )
                last_heartbeat = last_symbols_refresh = time.monotonic()
                while time.monotonic() < stop_at:
                    try:
                        raw = await asyncio.wait_for(
                            ws.recv(), timeout=min(30.0, max(1.0, stop_at - time.monotonic()))
                        )
                    except asyncio.TimeoutError:
                        await ws.send("ping")
                        _record_liquidation_health(
                            pipeline, "liquidations:okx_ws", status="ok", success=True,
                            details={"eligible_symbols": len(wanted), "heartbeat": True},
                        )
                        if time.monotonic() - last_symbols_refresh >= 300:
                            wanted = await asyncio.to_thread(_okx_liquidation_symbols, pipeline)
                            last_symbols_refresh = time.monotonic()
                        last_heartbeat = time.monotonic()
                        continue
                    payload = json.loads(raw)
                    if payload == "pong" or not isinstance(payload, dict):
                        continue
                    data = payload.get("data")
                    events = data if isinstance(data, list) else [data]
                    with mi.connect(pipeline.db_path) as conn:
                        written = 0
                        observed = 0
                        for event in events:
                            if not isinstance(event, dict):
                                continue
                            for normalized in _okx_force_order(event, multipliers=multipliers):
                                instrument, side, event_at, price, quantity, notional, event_id = normalized
                                if instrument not in wanted:
                                    continue
                                observed += 1
                                written += int(mi.insert_liquidation_event(
                                    conn, exchange="okx", event_id=event_id, event_at=event_at,
                                    symbol=wanted[instrument], side=side, price=price, quantity=quantity,
                                    notional_usd=notional, raw_json={"channel": payload.get("arg"), "event": event,
                                                                      "contract_multiplier": multipliers.get(instrument)},
                                ))
                        if observed:
                            mi.record_source_health(
                                conn, "liquidations:okx_ws", status="ok", success=True,
                                records_written=written,
                                details={"eligible_symbols": len(wanted), "observed": observed,
                                         "contract_multipliers": len(multipliers)},
                            )
                            last_heartbeat = time.monotonic()
                        conn.commit()
        except Exception as exc:
            if time.monotonic() >= stop_at:
                break
            _record_liquidation_health(pipeline, "liquidations:okx_ws", status="error", success=False,
                                       error=str(exc)[:500])
            await asyncio.sleep(5)


async def run(minutes: int, cadence: int) -> None:
    if not _acquire_monitor_lock():
        print(json.dumps({"at": mi.utc_now_iso(), "status": "already_running"}), flush=True)
        return
    pipeline = DerivativesPipeline()
    stop_at = time.monotonic() + max(1, minutes) * 60
    _write_heartbeat("started", detail={"minutes": minutes, "cadence_seconds": cadence})
    try:
        await asyncio.gather(
            current_loop(pipeline, stop_at, cadence),
            fast_flush_paper_loop(pipeline, stop_at),
            fast_flush_archive_loop(pipeline, stop_at),
            liquidation_loop(pipeline, stop_at),
            bybit_liquidation_loop(pipeline, stop_at),
            okx_liquidation_loop(pipeline, stop_at),
        )
    finally:
        _write_heartbeat("stopped", status="STOPPED")
        _release_monitor_lock()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--minutes", type=int, default=130)
    parser.add_argument("--cadence-seconds", type=int, default=120)
    args = parser.parse_args()
    asyncio.run(run(args.minutes, args.cadence_seconds))


if __name__ == "__main__":
    main()
