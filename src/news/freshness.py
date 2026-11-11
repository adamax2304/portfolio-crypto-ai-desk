"""Point-in-time news freshness classification.

The source timestamp tells us when an event happened; ``available_at`` tells
us when this desk could first act on it. Keeping those facts separate stops a
slow RSS poll from turning an old article into a fabricated intraday catalyst.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any

FAST_EVENT = "FAST_EVENT"
CONTINUATION_EVENT = "CONTINUATION_EVENT"
THESIS_EVENT = "THESIS_EVENT"
AVAILABILITY_UNKNOWN = "AVAILABILITY_UNKNOWN"
EXPIRED_EVENT = "EXPIRED_EVENT"

FAST_MAX = timedelta(minutes=10)
CONTINUATION_MAX = timedelta(hours=6)
THESIS_MAX = timedelta(days=7)


def parse_time(value: Any) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None
    return (parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)).astimezone(timezone.utc)


@dataclass(frozen=True)
class ObservationTiming:
    event_latency_class: str
    source_observation_delay_seconds: float | None


def classify_observation(published_at: Any, available_at: Any) -> ObservationTiming:
    """Classify an item at the instant it became usable by this system.

    ``FAST_EVENT`` is deliberately strict: both timestamps are required and
    the item must arrive within ten minutes. Unknown historical timing can
    never receive a fast catalyst boost.
    """
    published = parse_time(published_at)
    available = parse_time(available_at)
    if published is None or available is None:
        return ObservationTiming(AVAILABILITY_UNKNOWN, None)
    delay = max(0.0, (available - published).total_seconds())
    if delay <= FAST_MAX.total_seconds():
        label = FAST_EVENT
    elif delay <= CONTINUATION_MAX.total_seconds():
        label = CONTINUATION_EVENT
    elif delay <= THESIS_MAX.total_seconds():
        label = THESIS_EVENT
    else:
        label = EXPIRED_EVENT
    return ObservationTiming(label, round(delay, 3))


def usable_at(event_latency_class: str | None, available_at: Any, decision_at: Any) -> bool:
    """Return true only after the desk had actually observed the item."""
    available = parse_time(available_at)
    decision = parse_time(decision_at)
    return (
        str(event_latency_class or "") != AVAILABILITY_UNKNOWN
        and available is not None
        and decision is not None
        and available <= decision
    )


def supports_mode(event_latency_class: str | None, mode: str | None) -> bool:
    """Whether an observed event may support the named trading horizon.

    This does not grant an entry by itself. It merely prevents a slow item from
    posing as a fast catalyst; the strategy's existing price/structure/risk
    gates still decide actionability.
    """
    if not mode:
        return True  # compatibility for read-only callers without a strategy.
    value = str(mode).lower()
    event = str(event_latency_class or "")
    if "scalp" in value:
        return event == FAST_EVENT
    if any(token in value for token in ("swing", "position", "invest")):
        return event in {FAST_EVENT, CONTINUATION_EVENT, THESIS_EVENT}
    # Intraday continuation patterns may use a 10m-6h event only alongside
    # their separate reclaim/VWAP/retest confirmation. They cannot use thesis.
    return event in {FAST_EVENT, CONTINUATION_EVENT}


__all__ = [
    "FAST_EVENT", "CONTINUATION_EVENT", "THESIS_EVENT", "AVAILABILITY_UNKNOWN", "EXPIRED_EVENT",
    "ObservationTiming", "classify_observation", "parse_time", "usable_at", "supports_mode",
]
