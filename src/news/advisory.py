"""News/catalyst ADVISORY aggregator (2026-07-03) — DISPLAY-ONLY.

Bundles the read-only news signals into one advisory block for the stocks report / enriched packet /
control app: earnings risk (from `events`), fresh SEC/legal filings (from `news_items`), source-health
warnings (dead PRIMARY sources), and a "no fresh primary source" note. This NEVER changes score, tier,
A/B/C, paper/live routing, or actionability — it is a warning/context surface only.
"""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from typing import Any

from src.config import load_config


def _conn(db):
    c = sqlite3.connect(db or str(load_config().db_path))
    c.row_factory = sqlite3.Row
    return c


def earnings_advisory(db: str | None = None, *, now: datetime | None = None) -> dict[str, Any]:
    """Earnings-risk advisory from the `events` table (event_type='earnings'). Read-only."""
    ref = (now or datetime.now(timezone.utc)).date().isoformat()
    conn = _conn(db)
    try:
        try:
            rows = [dict(r) for r in conn.execute(
                "SELECT ticker, event_date FROM events WHERE event_type='earnings' "
                "AND event_date >= date(?, '-1 day') AND event_date <= date(?, '+2 day')",
                (ref, ref)).fetchall()]
        except sqlite3.OperationalError:
            rows = []
    finally:
        conn.close()
    today = sorted({r["ticker"] for r in rows if str(r["event_date"])[:10] == ref})
    tomorrow = sorted({r["ticker"] for r in rows if str(r["event_date"])[:10] > ref})
    recent = sorted({r["ticker"] for r in rows if str(r["event_date"])[:10] < ref})
    at_risk = sorted(set(today) | set(tomorrow))
    return {"as_of": ref, "earnings_today": today, "earnings_tomorrow": tomorrow,
            "earnings_last_24h": recent, "symbols_under_earnings_risk": at_risk,
            "advisory": ("AVOID holding through / chasing into earnings for: "
                         + ", ".join(at_risk) if at_risk else "no earnings within the window"),
            "changes_score": False, "changes_actionability": False}


def sec_legal_advisory(db: str | None = None, *, hours: int = 48, limit: int = 8,
                       now: datetime | None = None) -> dict[str, Any]:
    """Fresh SEC filings / legal-risk headlines for stocks (advisory context). Read-only."""
    from src.news.source_health import window_news_rows
    conn = _conn(db)
    try:
        # Robust rolling window (parsed published_at; invalid/date_unavailable excluded).
        rows = window_news_rows(
            conn, hours=hours, now=now, limit=limit,
            where="asset_class='stocks' "
            "AND (source='SEC EDGAR' OR lower(title) LIKE '%lawsuit%' OR lower(title) LIKE '%sec %' "
            "OR lower(title) LIKE '%settlement%' OR lower(title) LIKE '%investigation%')") or []
    finally:
        conn.close()
    return {"count": len(rows),
            "items": [{"source": r["source"], "title": (r["title"] or "")[:110],
                       "published_at": r["published_at"]} for r in rows]}


def news_advisory(db: str | None = None) -> dict[str, Any]:
    """Combined DISPLAY-ONLY advisory: earnings + SEC/legal + source-health warnings. No score change."""
    earn = earnings_advisory(db)
    legal = sec_legal_advisory(db)
    health_warn: list[str] = []
    try:
        from src.news.source_health import compute_source_health
        h = compute_source_health(db)
        s = h["summary"]
        if s["dead_primary"]:
            health_warn.append(f"DEAD primary news sources: {', '.join(s['dead_primary'])}")
        if s["dead"]:
            health_warn.append(f"{s['dead']} configured sources are DEAD (enabled but not writing)")
        # no fresh primary stock source at all?
        prim_ok = any(r["primary_source"] and r["asset_class"] == "stocks" and r["stale_status"] == "OK"
                      for r in h["sources"])
        if not prim_ok:
            health_warn.append("NO fresh primary STOCK source is healthy — treat single-source "
                               "headlines with caution")
    except Exception:
        pass
    canonical: list[dict[str, Any]] = []
    try:
        from src.news.events import normalized_events
        events = normalized_events(db, hours=48, limit=400)
        canonical = [e for e in events.get("events", [])
                     if str(e.get("asset_class") or "").startswith("stock")
                     and (e.get("linkage_allowed") or e.get("risk_action") not in (None, "none"))][:12]
    except Exception:
        canonical = []
    return {"earnings": earn, "sec_legal": legal, "source_health_warnings": health_warn,
            "canonical_material_events": canonical,
            "advisory_only": True, "changes_score": False, "changes_tier": False,
            "changes_actionability": False}


def render_advisory_block(adv: dict) -> str:
    """Compact Markdown; display-only. Never implies a score/tier change."""
    e = adv["earnings"]
    lines = ["## News/catalyst advisory (display-only — does NOT change score / tier / actionability)"]
    lines.append(f"- Earnings risk (as of {e['as_of']}): today [{', '.join(e['earnings_today']) or '—'}] "
                 f"· tomorrow [{', '.join(e['earnings_tomorrow']) or '—'}] "
                 f"· last 24h [{', '.join(e['earnings_last_24h']) or '—'}]")
    if e["symbols_under_earnings_risk"]:
        lines.append(f"  - ⚠ {e['advisory']}".replace("⚠", "WARNING:"))
    sl = adv["sec_legal"]
    if sl["count"]:
        lines.append(f"- Fresh SEC/legal (48h): {sl['count']} item(s)")
        for it in sl["items"][:4]:
            lines.append(f"  - [{it['source']}] {it['title']}")
    else:
        lines.append("- Fresh SEC/legal (48h): none")
    for w in adv["source_health_warnings"]:
        lines.append(f"- SOURCE HEALTH: {w}")
    material = adv.get("canonical_material_events") or []
    if material:
        lines.append("- Canonical material events for Opus review:")
        for event in material[:8]:
            symbols = ",".join(event.get("symbols") or []) or "market"
            lines.append(
                f"  - {symbols} · {event.get('event_type')} · {event.get('direction_hint')} · "
                f"confidence={event.get('confidence')} · {event.get('source_quality')}/"
                f"{event.get('content_level')} · {str(event.get('title') or '')[:120]}"
            )
    return "\n".join(lines)
