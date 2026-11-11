"""Recent-earnings-print detector (PART P1-fix, 2026-06-04).

The 12h audit found AVGO re-issued as an A-tier LONG with a stale pre-earnings
entry zone and ``earnings: UNKNOWN`` — because yfinance's calendar missed the
event. This module provides a news/catalyst-based fallback: scan ``news_items``
for a recent **earnings PRINT** (past-tense: "reported Q2 results", "beats
estimates", "post-earnings", etc.) so the trade-idea agent can invalidate a
stale setup even when the calendar is blind ("news wins over calendar UNKNOWN").

Read-only. No DB writes. Pure regex + one SELECT.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timedelta, timezone
from typing import Any

from src.storage.sqlite import SQLiteStore

# Past-tense / event-occurred earnings phrasing. Future/ahead-of-print phrasing
# is excluded by _FUTURE below so "X to report Q2 next week" does NOT match.
_EARNINGS_PATTERNS = [
    re.compile(r"\breported\b.{0,30}\b(q[1-4]|quarter|earnings|results)\b", re.I),
    re.compile(r"\b(q[1-4]|quarterly|fiscal)\b.{0,20}\b(results|earnings|revenue|eps)\b", re.I),
    re.compile(r"\b(beats?|misse[sd]|tops?|posts?|smash(?:es|ed)?)\b.{0,30}\b(estimates|expectations|eps|revenue|earnings|forecast)\b", re.I),
    re.compile(r"\bearnings call\b", re.I),
    re.compile(r"\bpost-?earnings\b", re.I),
    re.compile(r"\bafter the bell\b.{0,40}\b(report|earnings|results|revenue)\b", re.I),
    re.compile(r"\b(record|raises?|cuts?|lowers?)\b.{0,20}\b(revenue|guidance|outlook)\b", re.I),
]
_FUTURE = re.compile(
    r"\b(will report|to report|ahead of|previews?|expected to report|"
    r"before (the )?earnings|set to report|due to report|earnings preview|"
    r"upcoming earnings|when it reports)\b",
    re.I,
)

_LIKE = (
    "%earnings%", "%q1 results%", "%q2 results%", "%q3 results%", "%q4 results%",
    "%quarterly results%", "%fiscal%results%", "%beats estimates%",
    "%misses estimates%", "%post-earnings%", "%revenue%", "%eps%", "%guidance%",
)


def _is_earnings_print(title: str) -> bool:
    if not title:
        return False
    if _FUTURE.search(title):
        return False
    return any(p.search(title) for p in _EARNINGS_PATTERNS)


def _is_within_window(value: str | None, *, start: datetime, end: datetime) -> bool:
    """Validate timestamped news after the indexed coarse SQL range.

    Some legacy rows use date-only strings, while malformed values such as
    ``date_unavailable`` must never become a fresh earnings print.
    """
    raw = str(value or "").strip()
    if not raw:
        return False
    try:
        parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        try:
            parsed = datetime.strptime(raw, "%Y-%m-%d")
        except ValueError:
            return False
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return start < parsed.astimezone(timezone.utc) <= end


def load_recent_earnings_news(
    db: SQLiteStore,
    symbols: list[str],
    lookback_hours: int = 36,
    *,
    now: datetime | None = None,
) -> dict[str, dict[str, Any]]:
    """Return ``{SYMBOL: {"published_at", "title", "source", "url"}}`` for the
    most-recent confirmed earnings PRINT per symbol within ``lookback_hours``.

    A "print" = a past-tense earnings/results headline mapped to the symbol.
    Symbols with no recent earnings news are absent from the dict.
    """
    sym_set = {str(s).split("/")[0].upper() for s in (symbols or []) if s}
    if not sym_set:
        return {}
    where_like = " OR ".join("LOWER(title) LIKE ?" for _ in _LIKE)
    timestamped_sql = (
        "SELECT title, source, url, published_at, detected_symbols_json "
        "FROM news_items "
        f"WHERE ({where_like}) "
        "  AND published_at IS NOT NULL AND TRIM(published_at) <> '' "
        "  AND published_at > ? AND published_at < ? "
        "ORDER BY published_at DESC LIMIT 3000"
    )
    undated_sql = (
        "SELECT title, source, url, published_at, detected_symbols_json "
        "FROM news_items "
        f"WHERE ({where_like}) "
        "  AND (published_at IS NULL OR TRIM(published_at) = '') "
        "ORDER BY id DESC LIMIT 3000"
    )
    like_params = [f"%{kw.strip('%').lower()}%" for kw in _LIKE]
    reference = now or datetime.now(timezone.utc)
    if reference.tzinfo is None:
        reference = reference.replace(tzinfo=timezone.utc)
    reference = reference.astimezone(timezone.utc)
    start = reference - timedelta(hours=int(lookback_hours))
    # Use a date-aligned range so date-only legacy values enter the small
    # candidate set, then apply the exact timestamp check in Python.
    coarse_start = start.date().isoformat()
    coarse_end = (reference.date() + timedelta(days=1)).isoformat()

    out: dict[str, dict[str, Any]] = {}
    try:
        with db.connect() as conn:
            rows = list(conn.execute(timestamped_sql, [*like_params, coarse_start, coarse_end]))
            rows.extend(conn.execute(undated_sql, like_params))
    except Exception:
        return {}
    for row in rows:
        try:
            title = row["title"] or ""
            source = row["source"] or ""
            url = row["url"] or ""
            published_at = row["published_at"] or ""
            symbols_json = row["detected_symbols_json"] or "[]"
        except Exception:
            title, source, url, published_at, symbols_json = (
                row[0], row[1], row[2], row[3], row[4]
            )
        if not _is_earnings_print(title):
            continue
        # Undated rows retain the historical conservative behavior: they can
        # still block a stale setup. Timestamped rows must be point-in-time
        # valid; future or malformed values are excluded.
        if published_at and not _is_within_window(published_at, start=start, end=reference):
            continue
        try:
            detected = json.loads(symbols_json)
        except Exception:
            detected = []
        matched = {str(s).split("/")[0].upper() for s in detected} & sym_set
        for sym in matched:
            # rows are DESC by published_at → first seen is the latest.
            if sym not in out:
                out[sym] = {
                    "published_at": published_at,
                    "title": title,
                    "source": source,
                    "url": url,
                }
    return out
