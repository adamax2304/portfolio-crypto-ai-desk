"""US equity cash-session calendar (PART P1-fix, 2026-06-04).

Canonical, DST-aware check for whether the US regular cash session
(09:30–16:00 America/New_York, Mon–Fri, excluding NYSE holidays) is open.

Replaces the two crude UTC-only heuristics (`monitor._is_us_market_hours`,
`stocks_report_builder._market_session_label`) for *gating* purposes — those
remain for display but new signal-validity logic uses this module.

Pure / side-effect free. Falls back to a weekend-only check if `zoneinfo`
is somehow unavailable (never crashes the pipeline).
"""

from __future__ import annotations

from datetime import date, datetime, time, timedelta, timezone

try:
    from zoneinfo import ZoneInfo
    _NY = ZoneInfo("America/New_York")
except Exception:  # pragma: no cover - zoneinfo always present on 3.9+
    _NY = None

# NYSE full-day holidays (date-only, observed). Minimal rolling set — extend as
# needed. Used as a bonus over the weekend floor; a missing year just means
# those weekdays are treated as open (weekend floor still applies).
_NYSE_HOLIDAYS: frozenset[str] = frozenset({
    # 2025
    "2025-01-01", "2025-01-20", "2025-02-17", "2025-04-18", "2025-05-26",
    "2025-06-19", "2025-07-04", "2025-09-01", "2025-11-27", "2025-12-25",
    # 2026
    "2026-01-01", "2026-01-19", "2026-02-16", "2026-04-03", "2026-05-25",
    "2026-06-19", "2026-07-03", "2026-09-07", "2026-11-26", "2026-12-25",
})

_RTH_OPEN = time(9, 30)
_RTH_CLOSE = time(16, 0)
# NYSE equity-market early closes published for the years covered by this
# project calendar. Keep this explicit rather than guessing from a federal
# holiday rule: a future calendar update must be deliberate and auditable.
_NYSE_EARLY_CLOSES: dict[str, time] = {
    "2025-07-03": time(13, 0), "2025-11-28": time(13, 0), "2025-12-24": time(13, 0),
    "2026-11-27": time(13, 0), "2026-12-24": time(13, 0),
}


def _to_ny(now: datetime | None) -> datetime:
    if now is None:
        now = datetime.now(timezone.utc)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    if _NY is not None:
        return now.astimezone(_NY)
    # Fallback: approximate ET as UTC-4 (DST). Only used if zoneinfo missing.
    from datetime import timedelta
    return (now.astimezone(timezone.utc) - timedelta(hours=4))


def is_us_holiday(now: datetime | None = None) -> bool:
    ny = _to_ny(now)
    return ny.strftime("%Y-%m-%d") in _NYSE_HOLIDAYS


def is_us_cash_session_open(now: datetime | None = None) -> bool:
    """True iff the US regular cash session is open at *now* (UTC or aware).

    Rules: Mon–Fri, 09:30–16:00 America/New_York, not an NYSE holiday.
    Weekend / holiday / outside-RTH → False.
    """
    ny = _to_ny(now)
    if ny.weekday() >= 5:        # Sat/Sun
        return False
    if ny.strftime("%Y-%m-%d") in _NYSE_HOLIDAYS:
        return False
    close = _NYSE_EARLY_CLOSES.get(ny.strftime("%Y-%m-%d"), _RTH_CLOSE)
    return _RTH_OPEN <= ny.timetz().replace(tzinfo=None) < close


def us_cash_session_close(now: datetime | None = None) -> datetime | None:
    """Return the regular-session close for ``now``'s NY trading day in UTC.

    ``None`` means that the supplied calendar day is not an NYSE trading day.
    This is deliberately a calendar primitive, rather than a configurable
    strategy setting: a stock *intraday* trade may not become an overnight
    trade merely because its generic tracker validity is longer than RTH.
    Early-close handling is not modelled by this lightweight calendar yet, so
    callers still fail closed on holidays and weekends.
    """
    ny = _to_ny(now)
    if ny.weekday() >= 5 or ny.strftime("%Y-%m-%d") in _NYSE_HOLIDAYS:
        return None
    fallback_tz = timezone(timedelta(hours=-4))
    session_tz = _NY if _NY is not None else fallback_tz
    close = _NYSE_EARLY_CLOSES.get(ny.strftime("%Y-%m-%d"), _RTH_CLOSE)
    return datetime.combine(ny.date(), close, tzinfo=session_tz).astimezone(timezone.utc)


def stock_intraday_target_session(now: datetime) -> tuple[datetime, datetime]:
    """Return the RTH session an intraday plan created at ``now`` belongs to.

    Premarket and RTH plans belong to the current NY trading day. Plans
    created after that day's close, on a weekend, or on a holiday belong to
    the next NYSE session. This is intentionally separate from
    ``us_cash_session_close``: the latter is a calendar primitive for the
    supplied date, while this helper models a plan's executable session.
    """
    ny = _to_ny(now)
    target = ny.date()
    trading_day = target.weekday() < 5 and target.isoformat() not in _NYSE_HOLIDAYS
    close_time = _NYSE_EARLY_CLOSES.get(target.isoformat(), _RTH_CLOSE)
    if not trading_day or ny.timetz().replace(tzinfo=None) >= close_time:
        target += timedelta(days=1)
        while target.weekday() >= 5 or target.isoformat() in _NYSE_HOLIDAYS:
            target += timedelta(days=1)

    fallback_tz = timezone(timedelta(hours=-4))
    session_tz = _NY if _NY is not None else fallback_tz
    target_close = _NYSE_EARLY_CLOSES.get(target.isoformat(), _RTH_CLOSE)
    opened = datetime.combine(target, _RTH_OPEN, tzinfo=session_tz)
    closed = datetime.combine(target, target_close, tzinfo=session_tz)
    return opened.astimezone(timezone.utc), closed.astimezone(timezone.utc)


def stock_intraday_target_session_close(now: datetime) -> datetime:
    """Return the economic expiry for a stock-intraday plan."""
    return stock_intraday_target_session(now)[1]


def latest_us_cash_session(now: datetime | None = None) -> tuple[datetime, datetime, bool]:
    """Return the latest relevant NYSE RTH window in UTC.

    During RTH this is today's still-open session. Premarket, weekends and holidays use the latest
    completed trading day. The boolean is true only when the returned session is complete.
    """
    ny = _to_ny(now)
    target: date = ny.date()
    is_trading_day = ny.weekday() < 5 and target.isoformat() not in _NYSE_HOLIDAYS
    if not is_trading_day or ny.timetz().replace(tzinfo=None) < _RTH_OPEN:
        target -= timedelta(days=1)
        while target.weekday() >= 5 or target.isoformat() in _NYSE_HOLIDAYS:
            target -= timedelta(days=1)
    fallback_tz = timezone(timedelta(hours=-4))
    session_tz = _NY if _NY is not None else fallback_tz
    close_time = _NYSE_EARLY_CLOSES.get(target.isoformat(), _RTH_CLOSE)
    open_ny = datetime.combine(target, _RTH_OPEN, tzinfo=session_tz)
    close_ny = datetime.combine(target, close_time, tzinfo=session_tz)
    complete = target != ny.date() or ny.timetz().replace(tzinfo=None) >= close_time
    return open_ny.astimezone(timezone.utc), close_ny.astimezone(timezone.utc), complete


def us_session_label(now: datetime | None = None) -> str:
    """Human label: weekend / holiday / premarket / regular session / after-hours."""
    ny = _to_ny(now)
    if ny.weekday() >= 5:
        return "weekend"
    if ny.strftime("%Y-%m-%d") in _NYSE_HOLIDAYS:
        return "holiday"
    t = ny.timetz().replace(tzinfo=None)
    if t < _RTH_OPEN:
        return "premarket"
    if t <= _NYSE_EARLY_CLOSES.get(ny.strftime("%Y-%m-%d"), _RTH_CLOSE):
        return "regular session"
    return "after-hours"


def us_trading_days_until(target: date, *, today: date | None = None) -> int:
    """Count NYSE trading sessions after ``today`` through ``target``.

    A target on the next open session returns 1. Past targets return a negative
    calendar-day distance so callers can discard them explicitly.
    """
    current = today or _to_ny(None).date()
    if target < current:
        return (target - current).days
    count = 0
    probe = current + timedelta(days=1)
    while probe <= target:
        if probe.weekday() < 5 and probe.isoformat() not in _NYSE_HOLIDAYS:
            count += 1
        probe += timedelta(days=1)
    return count
