"""Stage-timing diagnostics for the crypto report pipeline.

Read-only/observational: this module ONLY measures wall-clock time and writes
append-only log lines under ``logs/diagnostics/crypto_report_timing_<UTC-date>.log``.
It never changes control flow — ``stage()`` re-raises any exception unchanged and
all file I/O is wrapped so a logging failure can never break a report.

Toggle off with env ``CRYPTO_REPORT_TIMING=0``.
"""
from __future__ import annotations

import os
import threading
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

_LOCK = threading.Lock()
_LOG_DIR = Path("logs") / "diagnostics"
_report_label = "report"


def _enabled() -> bool:
    return os.environ.get("CRYPTO_REPORT_TIMING", "1") != "0"


def set_report(label: str) -> None:
    """Tag subsequent log lines with the report kind (scalp/intraday/swing)."""
    global _report_label
    _report_label = str(label or "report")


def _logfile() -> Path:
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return _LOG_DIR / f"crypto_report_timing_{day}.log"


def _write(line: str) -> None:
    if not _enabled():
        return
    try:
        _LOG_DIR.mkdir(parents=True, exist_ok=True)
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
        with _LOCK, _logfile().open("a", encoding="utf-8") as fh:
            fh.write(f"{ts} [{_report_label}] {line}\n")
    except Exception:
        # Diagnostics must never break the pipeline.
        pass


def mark(message: str) -> None:
    """Write a free-form diagnostic line."""
    _write(message)


@contextmanager
def stage(name: str, **fields):
    """Time a pipeline stage. Logs START then END with duration; re-raises
    exceptions unchanged (status ERR:<type>). ``fields`` add k=v context
    (e.g. symbols=48)."""
    start = time.monotonic()
    _write(f"START {name}")
    err: BaseException | None = None
    try:
        yield
    except BaseException as exc:  # noqa: BLE001 - log then re-raise, never swallow
        err = exc
        raise
    finally:
        dur = time.monotonic() - start
        extra = " ".join(f"{k}={v}" for k, v in fields.items() if v is not None)
        status = "OK" if err is None else f"ERR:{type(err).__name__}"
        _write(f"END   {name} dur={dur:.1f}s {status}{(' ' + extra) if extra else ''}")
