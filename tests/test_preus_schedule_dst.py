"""Pre-US review schedule: every DST offset has an 08:50 ET worker start.

Windows Task Scheduler stores triggers in the account's local Europe/Nicosia
clock. The task deliberately carries 14:50, 15:50, and 16:50 local starts
(plus five-minute retries); the PowerShell wrapper accepts only the one that
is actually 08:50 ET. This avoids the two annual US/EU DST mismatch windows.
"""
from __future__ import annotations

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pytest

NY = ZoneInfo("America/New_York")
LOCAL = ZoneInfo("Europe/Nicosia")
LOCAL_TRIGGER_HOURS = (14, 15, 16)
TARGET_ET_HOUR = 8
TARGET_ET_MINUTE = 50


def _candidate_fire_times_in_et(date: datetime) -> list[datetime]:
    return [
        datetime(date.year, date.month, date.day, hour, TARGET_ET_MINUTE, tzinfo=LOCAL).astimezone(NY)
        for hour in LOCAL_TRIGGER_HOURS
    ]


@pytest.mark.parametrize("day_offset", list(range(0, 365, 5)))
def test_one_dst_safe_trigger_targets_0850_et(day_offset):
    date = datetime(2026, 1, 1) + timedelta(days=day_offset)
    fire_times = _candidate_fire_times_in_et(date)
    assert sum((item.hour, item.minute) == (TARGET_ET_HOUR, TARGET_ET_MINUTE) for item in fire_times) == 1


def test_preus_review_budget_finishes_before_stock_decision_window():
    """A 20-minute review plus two minutes of ingest completes before 09:15."""
    target = datetime(2026, 6, 15, TARGET_ET_HOUR, TARGET_ET_MINUTE, tzinfo=NY)
    decision_window_start = datetime(2026, 6, 15, 9, 15, tzinfo=NY)
    margin_minutes = (decision_window_start - target).total_seconds() / 60.0
    assert margin_minutes >= 22.0
