"""Per-ticker news / catalyst / analyst / earnings / legal context — LOCAL cache ONLY.

Reuses the existing stocks readers (no network, no paid providers). Returns concise lines for the
shadow review packet. NEVER fabricates: when nothing reliable exists for a symbol it returns an
empty `lines` list and the caller prints an explicit "no reliable ticker-specific news" note.
Read-only: opens the desk SQLite for reads, never writes.
"""
from __future__ import annotations

import json
from datetime import date, datetime
from typing import Any

_ANALYST_KEYWORDS = ("upgrade", "downgrade", "initiate", "initiated", "price target",
                     "overweight", "underweight", "reiterat", "buy rating", "sell rating",
                     "outperform", "raised to", "cut to", "lowered to")


def _symbols_of(row: dict) -> list[str]:
    try:
        return [str(s).upper() for s in json.loads(row.get("detected_symbols_json") or "[]")]
    except Exception:
        return []


def _dt(s: str | None) -> str:
    return str(s)[:10] if s else "—"


def ticker_context(symbol: str | None, *, config=None, db=None, news_limit: int = 200,
                   lookback_days: int = 90, max_news: int = 4) -> dict[str, Any]:
    """Return {"symbol", "lines": [...], "legal_blocking": bool}. All sources are best-effort and
    fail-open to nothing (honest emptiness beats a fabricated line)."""
    out: dict[str, Any] = {"symbol": symbol, "lines": [], "legal_blocking": False}
    if not symbol:
        return out
    sym = str(symbol).upper()
    lines: list[str] = []

    # Build a read-only SQLiteStore handle (from an injected db, a config.db_path, or the default).
    if db is None:
        try:
            from src.storage.sqlite import SQLiteStore
            dbp = getattr(config, "db_path", None)
            if dbp is None:
                from src.config import load_config as _load_pc
                dbp = _load_pc().db_path
            db = SQLiteStore(dbp)
            db.init_db()
        except Exception:
            return out

    # --- recent company news for this ticker ---
    news_rows: list[dict] = []
    try:
        # Position framework is longer-horizon → a 90d symbol-specific window, not a latest-N tail. The
        # per-symbol filter + [:max_news] slice keep the packet bounded.
        try:
            rows = db.load_news_window(hours=90 * 24, limit=6000, asset_class="stocks")
        except Exception:
            rows = db.load_recent_news(limit=news_limit, asset_class="stocks")
        news_rows = [r for r in rows if sym in _symbols_of(r)]
    except Exception:
        news_rows = []
    for r in news_rows[:max_news]:
        lines.append(f"news: {r.get('title', '?')} ({r.get('source', '?')}, {_dt(r.get('published_at'))})")

    # --- analyst actions (keyword scan over this ticker's local news; no fabrication) ---
    analyst = [r for r in news_rows
               if any(k in (r.get("title") or "").lower() for k in _ANALYST_KEYWORDS)]
    for r in analyst[:2]:
        lines.append(f"analyst: {r.get('title')} ({r.get('source', '?')}, {_dt(r.get('published_at'))})")

    # --- legal / regulatory / headline risk ---
    try:
        from src.stocks.legal_risk import load_active_legal_news, detect_legal_risk
        legal_hits = load_active_legal_news(db, [sym], lookback_days=lookback_days).get(sym, [])
        assess = detect_legal_risk(legal_hits)
        if getattr(assess, "severity", "none") != "none":
            cats = ", ".join(getattr(assess, "categories", []) or [])
            lines.append(f"LEGAL/HEADLINE RISK ({assess.severity}): {cats or 'flagged'}")
            out["legal_blocking"] = bool(getattr(assess, "blocking", False))
    except Exception:
        pass

    # --- recent earnings print (local news) ---
    try:
        from src.stocks.earnings_freshness import load_recent_earnings_news
        er = load_recent_earnings_news(db, [sym], lookback_hours=48).get(sym)
        if er:
            lines.append(f"recent earnings print: {er.get('title', 'earnings')} ({_dt(er.get('published_at'))})")
    except Exception:
        pass

    # --- upcoming earnings from the local events table (no network) ---
    try:
        events = db.load_events(limit=500)
        today = date.today()
        for ev in events:
            if (ev.get("ticker") or "").upper() != sym:
                continue
            if "earnings" not in (str(ev.get("event_type") or ev.get("event") or "").lower()):
                continue
            try:
                d = datetime.strptime(str(ev.get("event_date"))[:10], "%Y-%m-%d").date()
            except Exception:
                continue
            days = (d - today).days
            if 0 <= days <= 21:
                lines.append(f"upcoming earnings: {d.isoformat()} (in {days}d) — hold-window risk")
                break
    except Exception:
        pass

    out["lines"] = lines
    return out
