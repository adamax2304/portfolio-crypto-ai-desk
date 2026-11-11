from __future__ import annotations

from datetime import datetime, timezone
from zoneinfo import ZoneInfo


def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def utc_now_iso() -> str:
    return utc_now().isoformat()


def local_now_iso(timezone_name: str) -> str:
    return utc_now().astimezone(ZoneInfo(timezone_name)).isoformat()


def report_timestamp(timezone_name: str) -> str:
    return utc_now().astimezone(ZoneInfo(timezone_name)).strftime("%Y-%m-%d %H:%M:%S %Z")
