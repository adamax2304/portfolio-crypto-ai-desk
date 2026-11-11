"""Production symbol re-tagging for news_items (2026-07-04).

Re-runs the entity-alias matcher over recent news_items and UNIONs newly-matched tickers into
``detected_symbols_json`` — production ENRICHMENT to lift the news→symbol match rate (the KPI). It
only ever ADDS symbols (never removes), and it NEVER touches score, tier, actionability, routing, or
final_r. Fail-open. Use `dry_run=True` to measure the lift without writing.
"""
from __future__ import annotations

import json
import sqlite3
from typing import Any

from src.config import load_config


def _matched(raw) -> set[str]:
    try:
        return set(json.loads(raw) if isinstance(raw, str) else (raw or []))
    except Exception:
        return set()


def _text_of(row) -> str:
    text = str(row["title"] or "")
    try:
        rj = json.loads(row["raw_json"]) if row["raw_json"] else {}
        extra = str(rj.get("summary") or rj.get("description") or rj.get("body") or "")
        if extra:
            text = f"{text} {extra}"
    except Exception:
        pass
    return text[:2000]


def retag(db: str | None = None, *, hours: int = 72, limit: int = 5000,
          dry_run: bool = False, now=None) -> dict[str, Any]:
    """Re-detect symbols over the last ``hours`` of news_items and add any new matches. Returns
    before/after match-rate stats. Read-only when ``dry_run``. ``now`` is injectable for tests."""
    from src.news.source_health import window_news_rows
    cfg = load_config()
    conn = sqlite3.connect(db or str(cfg.db_path))
    conn.row_factory = sqlite3.Row
    from src.catalysts.entity_aliases import get_stocks_matcher, get_matcher
    sm = get_stocks_matcher(str(cfg.root))
    cm = get_matcher(str(cfg.root))
    try:
        # Robust rolling window (parsed published_at; invalid/date_unavailable excluded).
        rows = window_news_rows(conn, hours=hours, now=now, limit=limit) or []
        total = len(rows)
        before = sum(1 for r in rows if _matched(r["detected_symbols_json"]))
        updated = newly = 0
        for r in rows:
            ac = str(r["asset_class"] or "crypto")
            det = (sm.detect(_text_of(r)) if ac.startswith("stock") else cm.detect(_text_of(r)))
            cur = _matched(r["detected_symbols_json"])
            union = cur | set(det)
            if union != cur and union:
                if not dry_run:
                    conn.execute("UPDATE news_items SET detected_symbols_json=? WHERE id=?",
                                 (json.dumps(sorted(union)), r["id"]))
                updated += 1
                if not cur:
                    newly += 1
        if not dry_run:
            conn.commit()
        after = before + newly     # newly = rows that went from 0 → ≥1 symbol
    finally:
        conn.close()
    return {
        "rows": total, "hours": hours, "dry_run": dry_run,
        "before_matched": before, "after_matched": after,
        "before_rate": round(before / total, 3) if total else 0.0,
        "after_rate": round(after / total, 3) if total else 0.0,
        "rows_updated": updated, "newly_tagged": newly,
        "note": "production symbol ENRICHMENT (union-only) — never changes score/tier/actionability.",
    }
