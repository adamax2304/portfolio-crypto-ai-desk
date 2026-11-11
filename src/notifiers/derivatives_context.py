"""Read-only funding and open-interest context for Telegram trade messages.

Telegram is an operator surface, not a market-data collector. This module
reads only the already-ingested market-intelligence archive and never waits on
an exchange HTTP request. Missing or stale data is shown honestly and never
changes scoring, Paper execution, or live routing.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.data_collectors import market_intelligence_store as mi


MAX_AGE_MINUTES = 45


def _as_utc(value: datetime | None) -> datetime:
    now = value or datetime.now(timezone.utc)
    return now.replace(tzinfo=timezone.utc) if now.tzinfo is None else now.astimezone(timezone.utc)


def _parse_ts(value: Any) -> datetime | None:
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None
    return parsed.replace(tzinfo=timezone.utc) if parsed.tzinfo is None else parsed.astimezone(timezone.utc)


def current_snapshot(
    symbol: str,
    *,
    now: datetime | None = None,
    max_age_minutes: int = MAX_AGE_MINUTES,
) -> dict[str, Any]:
    """Return a fresh multi-venue point-in-time snapshot without any writes."""
    as_of = _as_utc(now)
    try:
        db_path = Path(mi.default_db_path())
        if not db_path.exists():
            return {}
        conn = sqlite3.connect(
            f"file:{db_path.as_posix()}?mode=ro", uri=True, timeout=2.0,
        )
        conn.row_factory = sqlite3.Row
        try:
            context = mi.latest_derivatives_context(
                conn, symbol, as_of=as_of, max_age_minutes=max_age_minutes,
            )
        finally:
            conn.close()
    except (OSError, sqlite3.Error, ValueError):
        return {}

    if context.get("status") != "ok":
        return {}
    latest = _parse_ts(context.get("latest_provider_ts"))
    if latest is None:
        return {}
    age_seconds = max(0, int((as_of - latest).total_seconds()))
    return {
        "source": "fresh_multi_venue_snapshot",
        "symbol": str(symbol),
        "as_of": as_of.isoformat(),
        "latest_provider_ts": latest.isoformat(),
        "age_seconds": age_seconds,
        "venue_count": int(context.get("venue_count") or 0),
        "venues": list(context.get("venues") or []),
        "funding_rate_8h": context.get("funding_rate_8h"),
        "funding_state": context.get("funding_state"),
        "oi_usd": context.get("oi_usd"),
        # The market-intelligence store returns a ratio (0.05 = 5%). The
        # Telegram contract uses explicitly named percentage units.
        "oi_change_24h_pct": (
            float(context["oi_change_24h"]) * 100
            if context.get("oi_change_24h") is not None else None
        ),
        "oi_change_venue_count": int(context.get("oi_change_venue_count") or 0),
    }


def _embedded_snapshot(signal: dict[str, Any]) -> dict[str, Any]:
    """Use proposal-time data only when a fresh archive row is unavailable."""
    raw: Any = signal.get("derivatives_at_proposal") or signal.get("derivatives") or {}
    if not raw:
        payload = signal.get("raw_idea_json") or {}
        if isinstance(payload, str):
            try:
                payload = json.loads(payload)
            except (TypeError, ValueError, json.JSONDecodeError):
                payload = {}
        if isinstance(payload, dict):
            raw = payload.get("derivatives_at_proposal") or {}
    if not isinstance(raw, dict):
        return {}

    funding = raw.get("funding_rate")
    oi_usd = raw.get("open_interest_usd")
    if oi_usd is None:
        oi_usd = raw.get("open_interest_value")
    if funding is None and oi_usd is None:
        return {}
    return {
        "source": "proposal_snapshot",
        "funding_rate_8h": funding,
        "funding_state": raw.get("crowding_risk") or raw.get("funding_state"),
        "oi_usd": oi_usd,
        "oi_change_24h_pct": raw.get("oi_change_24h_pct") or raw.get("oi_change_pct"),
        "venue_count": int(raw.get("venue_count") or 0),
        "age_seconds": None,
    }


def resolve_for_telegram(
    signal: dict[str, Any], *, now: datetime | None = None,
    snapshot: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Resolve current context, then a labelled proposal-time fallback."""
    if (signal.get("asset_class") or "crypto").lower() != "crypto":
        return {"source": "not_applicable"}
    if snapshot is not None:
        return dict(snapshot)
    current = current_snapshot(str(signal.get("symbol") or ""), now=now)
    return current or _embedded_snapshot(signal)


def _number(value: Any) -> float | None:
    try:
        return None if value in (None, "") else float(value)
    except (TypeError, ValueError):
        return None


def _usd(value: Any) -> str | None:
    amount = _number(value)
    if amount is None:
        return None
    absolute = abs(amount)
    if absolute >= 1_000_000_000:
        return f"${amount / 1_000_000_000:.2f}B"
    if absolute >= 1_000_000:
        return f"${amount / 1_000_000:.2f}M"
    if absolute >= 1_000:
        return f"${amount / 1_000:.1f}K"
    return f"${amount:.0f}"


def _pct(value: Any, *, decimals: int = 1) -> str | None:
    number = _number(value)
    return None if number is None else f"{number:+.{decimals}f}%"


def telegram_lines(
    signal: dict[str, Any], *, now: datetime | None = None,
    snapshot: dict[str, Any] | None = None,
) -> tuple[list[str], dict[str, Any]]:
    """Format explicit funding and OI lines for every crypto trade message."""
    if (signal.get("asset_class") or "crypto").lower() == "stocks":
        return (["Funding/OI: not available for stocks"], {"source": "not_applicable"})

    resolved = resolve_for_telegram(signal, now=now, snapshot=snapshot)
    if not resolved:
        return (
            [
                "Funding (8h): unavailable - no fresh derivatives snapshot",
                "Open interest: unavailable - no fresh derivatives snapshot",
            ],
            {"source": "unavailable"},
        )

    funding = _number(resolved.get("funding_rate_8h"))
    oi_usd = _usd(resolved.get("oi_usd"))
    venues = int(resolved.get("venue_count") or 0)
    state = str(resolved.get("funding_state") or "unknown").replace("_", " ")
    suffix = f" · {venues} venue{'s' if venues != 1 else ''}" if venues else ""
    age = _number(resolved.get("age_seconds"))
    if age is not None:
        suffix += f" · {max(0, round(age / 60))}m old"
    elif resolved.get("source") == "proposal_snapshot":
        suffix += " · at proposal"

    if funding is None:
        funding_line = "Funding (8h): unavailable" + suffix
    else:
        funding_line = f"Funding (8h): {funding * 100:+.4f}% · {state}" + suffix

    oi_change = _pct(resolved.get("oi_change_24h_pct"))
    oi_change_venues = int(resolved.get("oi_change_venue_count") or 0)
    if oi_usd is None:
        oi_line = "Open interest: unavailable (no USD-normalized fresh OI)" + suffix
    else:
        change_label = "24h median" if oi_change_venues > 1 else "24h"
        change = f" · {change_label} {oi_change}" if oi_change else ""
        oi_line = f"Open interest: {oi_usd}{change}" + suffix
    return [funding_line, oi_line], resolved
