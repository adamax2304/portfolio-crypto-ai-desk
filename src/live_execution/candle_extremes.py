from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def _epoch_seconds(value: datetime | int | float) -> int:
    if isinstance(value, datetime):
        moment = value if value.tzinfo is not None else value.replace(tzinfo=timezone.utc)
        return int(moment.timestamp())
    return int(value)


def completed_post_entry_extreme(
    client: Any,
    symbol: str,
    *,
    direction: str,
    entry_at: datetime | int | float,
    observed_at: datetime | int | float,
) -> float | None:
    """Return an extreme only from fully closed one-minute candles after fill.

    An OHLC candle's high/low has no intrabar ordering. Its high can therefore
    precede a fill that happened later in the same candle. The current ticker
    covers post-fill movement immediately; completed candles add wick coverage
    only after their full minute is safely known to be after the entry.
    """
    entry_seconds = _epoch_seconds(entry_at)
    observed_seconds = _epoch_seconds(observed_at)
    first_post_entry_open = (entry_seconds // 60 + 1) * 60
    current_candle_open = (observed_seconds // 60) * 60
    if first_post_entry_open >= current_candle_open:
        return None

    try:
        rows = client.klines(
            symbol,
            start_seconds=first_post_entry_open,
            end_seconds=current_candle_open - 1,
        )
    except TypeError:
        # Bybit's normalized client exposes the same bars in milliseconds.
        rows = client.klines(
            symbol,
            start_ms=first_post_entry_open * 1000,
            end_ms=current_candle_open * 1000 - 1,
        )
    except (AttributeError, ValueError):
        return None

    key = "high" if str(direction).lower() == "long" else "low"
    values: list[float] = []
    for row in rows or []:
        try:
            candle_at = int(row["candle_at"])
            if candle_at > 10_000_000_000:
                candle_at //= 1000
            if not first_post_entry_open <= candle_at < current_candle_open:
                continue
            values.append(float(row[key]))
        except (KeyError, TypeError, ValueError):
            continue
    if not values:
        return None
    return max(values) if key == "high" else min(values)
