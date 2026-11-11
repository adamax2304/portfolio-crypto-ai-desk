"""Unified normalized event layer over `news_items` (2026-07-04) — READ-MODEL.

Projects raw news rows into a normalized event shape (source_quality / asset_class / event_type+
subtype / direction_hint / confidence / latency / dedupe_key), de-dupes across source families, and
flags conflicting (bullish+bearish) coverage per symbol. Read-only; never changes score/tier/routing.
"""
from __future__ import annotations

import hashlib
import json
import re
import sqlite3
from datetime import datetime, timezone
from typing import Any

from src.config import load_config
from src.news.source_health import _parse_ts, window_news_rows

# source name → quality bucket
_QUALITY = {
    "SEC EDGAR": "regulator",
    "Binance Announcements": "exchange",
    "GlobeNewswire (Stocks)": "company_pr", "PR Newswire (Stocks)": "company_pr",
    "Business Wire (Stocks)": "company_pr", "DefiLlama": "primary",
}
_QUALITY_PREFIX = {"t.me/": "social"}

# keyword → (event_type, subtype). First match wins; per asset_class.
_STOCK_TAXO = [
    (("8-k", "10-q", "10-k", "424b", "s-1", "s-3", "form 4"), "sec_filing", None),
    (("earnings", "eps", "quarterly results", "reports q"), "earnings", None),
    (("guidance", "outlook", "forecast"), "guidance", None),
    (("upgrade", "downgrade", "price target", "initiates coverage", "reiterates"), "analyst_action", None),
    (("lawsuit", "sec ", "doj", "investigation", "fraud", "subpoena", "settlement", "probe"), "legal_risk", None),
    (("offering", "dilution", "shelf registration", "convertible notes"), "offering_dilution", None),
    (("acquire", "acquisition", "merger", "buyout", "takeover"), "mna", None),
    (("fda", "phase 3", "clinical", "trial results"), "fda_clinical", None),
    (("ceo", "cfo", "resign", "steps down", "appoints"), "management_change", None),
    (("launches", "unveils", "new product", "release"), "product_launch", None),
    (("partnership", "partners with", "collaborat"), "partnership", None),
]
_CRYPTO_TAXO = [
    (("will list", "lists ", "listing", "adds ", "spot trading"), "listing", None),
    (("delist", "removal of", "will be removed"), "delisting", None),
    (("perpetual", "futures listing", "usdt-margined"), "futures_listing", None),
    (("unlock", "vesting", "cliff"), "token_unlock", None),
    (("hack", "exploit", "breach", "drained", "stolen"), "exploit_hack", None),
    (("whale", "transferred", "moved", "deposited to"), "whale_transfer", None),
    (("tvl", "total value locked"), "tvl_change", None),
    (("stablecoin", "usdt supply", "usdc supply"), "stablecoin_flow", None),
    (("governance", "proposal", "vote"), "governance", None),
    (("airdrop",), "airdrop", None),
    (("launchpool", "launchpad"), "launchpad", None),
    (("maintenance", "suspend deposits", "halt withdrawals"), "maintenance", None),
]
_MACRO_TAXO = [
    (("fomc", "fed ", "powell", "rate cut", "rate hike"), "fed", None),
    (("cpi", "inflation"), "cpi", None), (("pce",), "pce", None),
    (("jobs report", "nonfarm", "payroll", "unemployment"), "jobs", None),
    (("yields", "treasury"), "yields", None), (("dollar", "dxy"), "dollar", None),
    (("war", "attack", "sanctions", "geopolit"), "geopolitical_risk", None),
    (("oil", "opec", "crude"), "oil", None),
]
_BULL = ("beats", "surges", "approval", "upgrade", "record", "wins", "buyback", "soars", "jumps", "rally")
_BEAR = ("misses", "downgrade", "probe", "lawsuit", "recall", "cuts", "plunge", "halts", "delist", "warns", "falls")


def _quality(source: str) -> str:
    if source in _QUALITY:
        return _QUALITY[source]
    for pref, q in _QUALITY_PREFIX.items():
        if str(source).startswith(pref):
            return q
    return "secondary"


def _classify(title: str, asset_class: str) -> tuple[str, str | None]:
    t = (title or "").lower()
    taxo = _STOCK_TAXO if str(asset_class).startswith("stock") else _CRYPTO_TAXO
    for kws, et, sub in taxo:
        if any(k in t for k in kws):
            return et, sub
    for kws, et, sub in _MACRO_TAXO:
        if any(k in t for k in kws):
            return et, sub
    return ("macro_headline" if str(asset_class).startswith("stock") else "other_news"), None


def _direction(title: str) -> str:
    t = (title or "").lower()
    b, r = any(k in t for k in _BULL), any(k in t for k in _BEAR)
    return "mixed" if b and r else "bullish" if b else "bearish" if r else "neutral"


def _dedupe_key(source: str, symbols: list, event_type: str, published_at: str, title: str) -> str:
    norm = re.sub(r"[^a-z0-9 ]", "", (title or "").lower())[:60]
    fam = str(source).split()[0].lower()
    day = str(published_at)[:13]
    sym = (sorted(symbols)[0] if symbols else "-")
    return hashlib.sha1(f"{fam}|{sym}|{event_type}|{day}|{norm}".encode()).hexdigest()[:16]


def normalized_events(db: str | None = None, *, hours: int = 48, limit: int = 800,
                      now: datetime | None = None) -> dict[str, Any]:
    ref = now or datetime.now(timezone.utc)
    conn = sqlite3.connect(db or str(load_config().db_path))
    conn.row_factory = sqlite3.Row
    try:
        # Prefer the materialized trust/policy layer when available. It has
        # source-independent clusters, content confidence and a fixed linkage
        # contract; the legacy projection below remains an old-DB fallback.
        has_canonical = conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name='news_canonical_events'"
        ).fetchone()
        if has_canonical:
            all_rows = [dict(r) for r in conn.execute(
                "SELECT * FROM news_canonical_events ORDER BY published_at DESC").fetchall()]
            cutoff = ref.timestamp() - hours * 3600
            window = [r for r in all_rows if _parse_ts(r.get("published_at")) is not None
                      and _parse_ts(r.get("published_at")).timestamp() >= cutoff]
            primaries = [r for r in window if int(r.get("is_cluster_primary") or 0) == 1][:limit]
            events = []
            for r in primaries:
                try:
                    symbols = json.loads(r.get("trusted_symbols_json") or "[]")
                except Exception:
                    symbols = []
                pub = _parse_ts(r.get("published_at"))
                events.append({
                    "event_id": r.get("event_id"), "source": r.get("source"),
                    "source_quality": r.get("source_quality"), "asset_class": r.get("asset_class"),
                    "symbols": symbols, "event_type": r.get("event_type"),
                    "event_subtype": r.get("event_subtype"), "title": (r.get("title") or "")[:160],
                    "url": r.get("url"), "published_at_utc": r.get("published_at"),
                    "latency_seconds": round((ref - pub).total_seconds()) if pub else None,
                    "importance": None, "direction_hint": r.get("direction_hint"),
                    "dedupe_key": r.get("cluster_key"), "content_level": r.get("content_level"),
                    "confidence": r.get("confidence"), "linkage_allowed": bool(r.get("linkage_allowed")),
                    "linkage_reason": r.get("linkage_reason"), "risk_action": r.get("risk_action"),
                    "corroboration_count": r.get("corroboration_count"),
                    "policy_version": r.get("policy_version"),
                })
            dir_by_sym: dict[str, set] = {}
            for e in events:
                for sym in e["symbols"]:
                    dir_by_sym.setdefault(str(sym).split("/")[0].upper(), set()).add(e["direction_hint"])
            conflicting = sorted(s for s, dirs in dir_by_sym.items()
                                 if {"bullish", "bearish"} <= dirs)
            for e in events:
                e["conflicting"] = any(str(s).split("/")[0].upper() in conflicting
                                       for s in e["symbols"])
            return {"available": True, "window_hours": hours, "count": len(events),
                    "deduped_from": len(window), "conflicting_symbols": conflicting,
                    "events": events, "canonical": True,
                    "note": "canonical materialized events; title/social confidence policy enforced."}
        # Robust rolling window: parse published_at Python-side, drop invalid/date_unavailable, sort
        # by parsed ts desc, then LIMIT — so 24h vs 48h are genuinely different slices (the old
        # `published_at >= datetime('now', ?)` SQL over-counted mixed formats).
        rows = window_news_rows(conn, hours=hours, now=ref, limit=limit)
    finally:
        conn.close()
    if rows is None:
        return {"available": False, "events": []}
    events, seen = [], set()
    for r in rows:
        try:
            syms = [str(s) for s in (json.loads(r["detected_symbols_json"]) if r["detected_symbols_json"] else [])]
        except Exception:
            syms = []
        ac = str(r["asset_class"] or "crypto")
        et, sub = _classify(r["title"], ac)
        pub = _parse_ts(r["published_at"])
        latency = round((ref - pub).total_seconds()) if pub else None
        key = _dedupe_key(r["source"], syms, et, r["published_at"], r["title"])
        if key in seen:
            continue
        seen.add(key)
        events.append({
            "event_id": f"nev_{r['id']}", "source": r["source"], "source_quality": _quality(r["source"]),
            "asset_class": ("macro" if et in {"fed", "cpi", "pce", "jobs", "yields", "dollar",
                            "geopolitical_risk", "oil"} else ac),
            "symbols": [s.split("/")[0].upper() for s in syms], "event_type": et, "event_subtype": sub,
            "title": (r["title"] or "")[:160], "url": r["url"], "published_at_utc": r["published_at"],
            "latency_seconds": latency, "importance": r["importance"],
            "direction_hint": _direction(r["title"]), "dedupe_key": key,
        })
    # conflict: a symbol with both bullish and bearish events in the window
    dir_by_sym: dict[str, set] = {}
    for e in events:
        for s in e["symbols"]:
            dir_by_sym.setdefault(s, set()).add(e["direction_hint"])
    conflicting = sorted({s for s, ds in dir_by_sym.items() if {"bullish", "bearish"} <= ds})
    for e in events:
        e["conflicting"] = any(s in conflicting for s in e["symbols"])
    return {"available": True, "window_hours": hours, "count": len(events),
            "deduped_from": len(rows), "conflicting_symbols": conflicting, "events": events,
            "note": "read-model over news_items; never changes score/tier/actionability."}
