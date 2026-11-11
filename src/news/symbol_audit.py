"""News symbol-mapping quality audit (2026-07-03) — READ-ONLY.

Rolling audit over `news_items`: volume, symbol_match_rate by source, top unmatched high-importance
headlines, and asset_class cross-tag candidates (crypto symbol in a stocks row or vice-versa). Pure
diagnostics — never re-tags a row, never changes ingestion/scoring/tiers.
"""
from __future__ import annotations

import json
import sqlite3
from typing import Any

from src.config import load_config

# crypto detected symbols carry a "/USDT" (or other quote) suffix; stocks are bare tickers.
_AMBIGUOUS = {"LINK", "NEAR", "OP", "SEI", "APT", "ONE", "FLOW"}


def _conn(db):
    c = sqlite3.connect(db or str(load_config().db_path))
    c.row_factory = sqlite3.Row
    return c


def _syms(raw) -> list[str]:
    try:
        v = json.loads(raw) if isinstance(raw, str) else (raw or [])
        return [str(s) for s in (v or [])]
    except Exception:
        return []


def _is_context_only(row: dict) -> bool:
    """Rows that intentionally have no tradable symbol should not pollute the symbol-match KPI."""
    if str(row.get("source") or "") != "DefiLlama":
        return False
    try:
        raw = json.loads(row.get("raw_json") or "{}") or {}
    except Exception:
        raw = {}
    return raw.get("provider") == "DefiLlama" and raw.get("symbol_tradable") is False


def audit(db: str | None = None, *, hours: int = 24, now=None) -> dict[str, Any]:
    from src.news.source_health import window_news_rows
    conn = _conn(db)
    try:
        # Robust rolling windows (parsed published_at; invalid/date_unavailable excluded from BOTH
        # the audit window and the 72h denominator — the old SQL string compare over-counted).
        rows = window_news_rows(conn, hours=hours, now=now)
        rows72 = window_news_rows(conn, hours=72, now=now)
        if rows is None or rows72 is None:
            return {"available": False}
        n72 = len(rows72)
    finally:
        conn.close()
    context_only = [r for r in rows if _is_context_only(r)]
    kpi_rows = [r for r in rows if not _is_context_only(r)]
    total = len(kpi_rows)
    matched = [r for r in kpi_rows if _syms(r["detected_symbols_json"])]
    by_source: dict[str, dict] = {}
    for r in kpi_rows:
        g = by_source.setdefault(str(r["source"] or "?"), {"n": 0, "matched": 0})
        g["n"] += 1
        if _syms(r["detected_symbols_json"]):
            g["matched"] += 1
    src_rates = sorted(
        ({"source": s, "rows": g["n"], "matched": g["matched"],
          "match_rate": round(g["matched"] / g["n"], 3) if g["n"] else 0.0}
         for s, g in by_source.items()), key=lambda x: (x["rows"], x["match_rate"]), reverse=True)
    # top unmatched HIGH-importance headlines (potential missed tickers)
    unmatched_hi = sorted(
        ({"source": r["source"], "title": (r["title"] or "")[:110], "importance": r["importance"]}
         for r in kpi_rows if not _syms(r["detected_symbols_json"]) and (r["importance"] or 0) >= 1.5),
        key=lambda x: (x["importance"] or 0), reverse=True)[:15]
    # ambiguous-suppression candidates: title mentions an ambiguous ticker but nothing was detected
    ambiguous = []
    for r in kpi_rows:
        if _syms(r["detected_symbols_json"]):
            continue
        toks = set((r["title"] or "").replace(",", " ").replace(".", " ").split())
        hit = _AMBIGUOUS & toks
        if hit:
            ambiguous.append({"source": r["source"], "title": (r["title"] or "")[:100],
                              "ambiguous": sorted(hit)})
    # asset_class cross-tag candidates: crypto-style (/quote) symbol in a stocks row, or a bare
    # ticker in a crypto row (heuristic — flagged for review, NEVER auto-corrected)
    mismatches = []
    for r in matched:
        ac = str(r["asset_class"] or "")
        syms = _syms(r["detected_symbols_json"])
        has_pair = any("/" in s for s in syms)
        all_bare = all("/" not in s for s in syms)
        if ac == "stocks" and has_pair:
            mismatches.append({"source": r["source"], "asset_class": ac, "symbols": syms,
                               "title": (r["title"] or "")[:90], "kind": "crypto_symbol_in_stocks_row"})
        elif ac == "crypto" and all_bare and syms:
            mismatches.append({"source": r["source"], "asset_class": ac, "symbols": syms,
                               "title": (r["title"] or "")[:90], "kind": "bare_ticker_in_crypto_row"})
    return {
        "available": True, "window_hours": hours,
        "rows_window": total, "rows_72h": n72, "rows_with_symbols": len(matched),
        "context_only_rows_excluded": len(context_only),
        "overall_match_rate": round(len(matched) / total, 3) if total else 0.0,
        "match_rate_by_source": src_rates[:25],
        "top_unmatched_high_importance": unmatched_hi,
        "ambiguous_suppression_candidates": ambiguous[:15],
        "asset_class_mismatch_candidates": mismatches[:20],
        "top_useful_sources": sorted(src_rates, key=lambda x: x["matched"], reverse=True)[:10],
        "note": "READ-ONLY audit — flags mapping issues for review; never re-tags rows or changes scoring.",
    }


def render_markdown(a: dict) -> str:
    if not a.get("available"):
        return "## News symbol-mapping audit\n- unavailable (news_items empty)"
    lines = [f"## News symbol-mapping audit (last {a['window_hours']}h)",
             f"- rows {a['rows_window']} (72h {a['rows_72h']}) · with symbols {a['rows_with_symbols']} "
             f"· overall match rate **{int(a['overall_match_rate']*100)}%**", "",
             "**Match rate by source (top):**"]
    if a.get("context_only_rows_excluded"):
        lines.insert(2, f"- context-only rows excluded from match KPI: {a['context_only_rows_excluded']}")
    for s in a["match_rate_by_source"][:12]:
        lines.append(f"- {s['source']}: {s['matched']}/{s['rows']} = {int(s['match_rate']*100)}%")
    if a["top_unmatched_high_importance"]:
        lines.append("")
        lines.append("**Top unmatched high-importance headlines (possible missed tickers):**")
        for u in a["top_unmatched_high_importance"][:8]:
            lines.append(f"- [{u['source']}] {u['title']}")
    if a["asset_class_mismatch_candidates"]:
        lines.append("")
        lines.append("**Asset-class cross-tag candidates (review only, never auto-corrected):**")
        for m in a["asset_class_mismatch_candidates"][:8]:
            lines.append(f"- {m['kind']} [{m['source']}]: {m['symbols']} — {m['title']}")
    return "\n".join(lines)
