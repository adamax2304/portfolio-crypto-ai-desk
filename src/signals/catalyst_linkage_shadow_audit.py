"""PART 4 — catalyst-linkage SHADOW audit (diagnostic only, never feeds scoring).

The production catalyst/news enrichment under-fires: scan-time ``CatalystAgent`` reads only
``load_recent_news(limit=100)`` (~5 h of crypto news), so symbol-tagged catalysts published earlier
the same day are missed and ``news_supported`` stays 0 (~26% of signals end up linked).

This module MEASURES how much wider time windows WOULD link, WITHOUT changing anything live:

* re-runs the SAME exact, word-boundary ``detected_symbols_json`` match the collector trusts, at
  the **current** (~5 h), **24 h** and **48 h** windows around each signal's creation time;
* records candidate shadow labels into a NEW additive table ``catalyst_shadow_audit``;
* estimates coverage at each window + a false-positive note.

It does NOT touch ``proposed_signals.news_supported``, ``signal_catalyst_labels``, scoring, tier,
routing, actionability, or final_r. Pure observability.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta, timezone
from typing import Any

from src.catalysts.collector import CATALYST_MIN_IMPORTANCE
from src.config import load_config
from src.signals.catalyst_label_refresh import _base_ticker, _is_telegram_source, _iso, _parse_iso

CURRENT_HOURS = 5      # production scan-time window proxy (limit=100 ≈ ~5h of crypto news)
WINDOWS = (24, 48)
FORWARD_HOURS = 2

_DDL = """
CREATE TABLE IF NOT EXISTS catalyst_shadow_audit (
    signal_id           TEXT PRIMARY KEY,
    asset_class         TEXT,
    symbol              TEXT,
    created_at          TEXT,
    current_supported   INTEGER,   -- production news_supported flag (~5h scan-time)
    catalyst_shadow_24h INTEGER,
    catalyst_shadow_48h INTEGER,
    match_confidence    REAL,      -- importance of best 48h hit (0..1), exact-mapping so high-precision
    source              TEXT,
    title               TEXT,
    news_timestamp      TEXT,
    why_matched         TEXT,
    computed_at         TEXT
)
"""


def _conn(db: str | None = None) -> sqlite3.Connection:
    cfg = load_config()
    c = sqlite3.connect(db or cfg.db_path)
    c.row_factory = sqlite3.Row
    return c


def _match(conn: sqlite3.Connection, symbol: str, created_at: str, asset_class: str,
           lookback_hours: int) -> dict[str, Any] | None:
    """Asset-aware exact ``detected_symbols_json`` match in a window bracketing ``created_at``.
    Read-only; mirrors the production matcher but parameterizes asset_class (crypto vs stocks)."""
    ticker = _base_ticker(symbol)
    if not ticker:
        return None
    ref = _parse_iso(created_at) or datetime.now(timezone.utc)
    lo = _iso(ref - timedelta(hours=lookback_hours))
    hi = _iso(ref + timedelta(hours=FORWARD_HOURS))
    try:
        cols = {r[1] for r in conn.execute("PRAGMA table_info(news_items)")}
    except sqlite3.OperationalError:
        return None
    if "detected_symbols_json" not in cols:
        return None
    has_imp = "importance" in cols
    ac = (asset_class or "crypto").lower()
    asset_clause = ("(asset_class='crypto' OR asset_class IS NULL)" if ac == "crypto"
                    else "asset_class='stocks'")
    sel = "title, source, published_at, detected_symbols_json" + (", importance" if has_imp else "")
    try:
        rows = conn.execute(
            f"SELECT {sel} FROM news_items WHERE {asset_clause} "
            "AND published_at >= ? AND published_at <= ? AND detected_symbols_json LIKE ? "
            "ORDER BY published_at DESC",
            (lo, hi, f'%"{ticker}"%'),
        ).fetchall()
    except sqlite3.OperationalError:
        return None
    best = None
    for row in rows:
        raw = row["detected_symbols_json"]
        try:
            syms = json.loads(raw) if isinstance(raw, str) else (raw or [])
        except (TypeError, ValueError, json.JSONDecodeError):
            syms = []
        if ticker not in {str(s).split("/")[0].strip().upper() for s in (syms or [])}:
            continue  # exact membership — never a title substring (no ORDI-from-"Ordinals")
        imp = row["importance"] if has_imp else None
        if has_imp and imp is not None:
            try:
                if float(imp) < CATALYST_MIN_IMPORTANCE:
                    continue
            except (TypeError, ValueError):
                pass
        hit = {"headline": str(row["title"] or ""), "source": str(row["source"] or ""),
               "published_at": row["published_at"],
               "importance": float(imp) if (has_imp and imp is not None) else None,
               "telegram": _is_telegram_source(row["source"])}
        if best is None or (hit["importance"] or 0) > (best.get("importance") or 0):
            best = hit
    return best


def audit(days: int = 7, db: str | None = None, now: datetime | None = None,
          persist: bool = True, asset_class: str | None = None) -> dict[str, Any]:
    """Run the shadow audit over recent signals. Read-only w.r.t. production tables; only writes the
    additive ``catalyst_shadow_audit`` table when ``persist``. Returns coverage estimates.

    ``asset_class`` optionally scopes the audit to one class (e.g. "stocks") — additive, advisory."""
    now = now or datetime.now(timezone.utc)
    computed_at = _iso(now)
    cutoff = _iso(now - timedelta(days=days))
    conn = _conn(db)
    try:
        if persist:
            conn.execute(_DDL)
        _ac_where = " AND asset_class = ?" if asset_class else ""
        _ac_params = ([cutoff, asset_class] if asset_class else [cutoff])
        rows = conn.execute(
            "SELECT signal_id, symbol, created_at, asset_class, "
            "COALESCE(news_supported,0) AS news_supported "
            f"FROM proposed_signals WHERE created_at >= ?{_ac_where} ORDER BY created_at DESC",
            _ac_params,
        ).fetchall()
        total = len(rows)
        cur_cov = h24 = h48 = newly24 = newly48 = 0
        for r in rows:
            cur = int(r["news_supported"] or 0)
            cur_cov += cur
            m24 = _match(conn, r["symbol"] or "", r["created_at"] or "", r["asset_class"] or "crypto", 24)
            m48 = _match(conn, r["symbol"] or "", r["created_at"] or "", r["asset_class"] or "crypto", 48)
            has24, has48 = bool(m24), bool(m48)
            h24 += has24
            h48 += has48
            if has24 and not cur:
                newly24 += 1
            if has48 and not cur:
                newly48 += 1
            if persist:
                best = m48 or m24
                conn.execute(
                    "INSERT INTO catalyst_shadow_audit (signal_id, asset_class, symbol, created_at, "
                    "current_supported, catalyst_shadow_24h, catalyst_shadow_48h, match_confidence, "
                    "source, title, news_timestamp, why_matched, computed_at) "
                    "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?) "
                    "ON CONFLICT(signal_id) DO UPDATE SET current_supported=excluded.current_supported, "
                    "catalyst_shadow_24h=excluded.catalyst_shadow_24h, "
                    "catalyst_shadow_48h=excluded.catalyst_shadow_48h, "
                    "match_confidence=excluded.match_confidence, source=excluded.source, "
                    "title=excluded.title, news_timestamp=excluded.news_timestamp, "
                    "why_matched=excluded.why_matched, computed_at=excluded.computed_at",
                    (r["signal_id"], r["asset_class"], r["symbol"], r["created_at"], cur,
                     int(has24), int(has48), (best.get("importance") if best else None),
                     (best.get("source") if best else None), (best.get("headline") if best else None),
                     (best.get("published_at") if best else None),
                     ("exact detected_symbols_json membership within window" if best else None),
                     computed_at),
                )
        if persist:
            conn.commit()
    finally:
        conn.close()
    pct = lambda n: round(100 * n / total, 1) if total else 0.0
    return {
        "days": days, "signals": total,
        "current_coverage_pct": pct(cur_cov), "current_window_hours": CURRENT_HOURS,
        "coverage_24h_pct": pct(h24), "coverage_48h_pct": pct(h48),
        "newly_linked_24h": newly24, "newly_linked_48h": newly48,
        "uplift_24h_pp": round(pct(h24) - pct(cur_cov), 1),
        "uplift_48h_pp": round(pct(h48) - pct(cur_cov), 1),
        "false_positive_note": ("matching is EXACT detected_symbols_json membership (word-boundary, "
                                "the same source-of-truth the integrity monitor trusts) — fabricated-"
                                "ticker FP risk is negligible; the residual risk is a real catalyst "
                                "being temporally coincidental, not symbol-misattributed."),
        "scoring_changed": False, "actionability_changed": False,
    }


TEMPORAL_COINCIDENCE_WARNING = (
    "temporal coincidence risk; exact symbol match is NOT trading proof — a headline within the "
    "window that names the ticker is not evidence the setup was catalyst-driven.")


def stocks_catalyst_advisory(db: str | None = None, *, days: int = 7,
                             examples: int = 3, now: datetime | None = None) -> dict[str, Any]:
    """DISPLAY/ADVISORY-ONLY stocks catalyst-linkage shadow summary for the report / LLM packet.

    Returns current news_supported %, 24h/48h EXACT-match shadow %, newly-linked counts, a few
    examples, and a temporal-coincidence warning. This NEVER changes scoring, tiers, actionability,
    or news_supported — it is a read-only advisory surface. ``examples`` are pulled from the persisted
    ``catalyst_shadow_audit`` table when present (best-effort)."""
    a = audit(days=days, db=db, now=now, persist=False, asset_class="stocks")
    ex: list[dict[str, Any]] = []
    try:
        conn = _conn(db)
        try:
            rows = conn.execute(
                "SELECT symbol, title, source, news_timestamp FROM catalyst_shadow_audit "
                "WHERE lower(COALESCE(asset_class,'')) LIKE 'stock%' AND catalyst_shadow_48h=1 "
                "AND COALESCE(current_supported,0)=0 AND title IS NOT NULL "
                "ORDER BY computed_at DESC LIMIT ?", (int(examples),)).fetchall()
            ex = [{"symbol": r["symbol"], "title": (r["title"] or "")[:90],
                   "source": r["source"], "news_timestamp": r["news_timestamp"]} for r in rows]
        finally:
            conn.close()
    except Exception:
        ex = []
    return {
        "asset_class": "stocks", "days": days, "signals": a["signals"],
        "news_supported_pct": a["current_coverage_pct"], "current_window_hours": a["current_window_hours"],
        "shadow_24h_pct": a["coverage_24h_pct"], "shadow_48h_pct": a["coverage_48h_pct"],
        "newly_linked_24h": a["newly_linked_24h"], "newly_linked_48h": a["newly_linked_48h"],
        "uplift_24h_pp": a["uplift_24h_pp"], "uplift_48h_pp": a["uplift_48h_pp"],
        "examples": ex, "warning": TEMPORAL_COINCIDENCE_WARNING,
        "advisory_only": True, "scoring_changed": False, "actionability_changed": False,
    }


def render_advisory_block(adv: dict[str, Any]) -> str:
    """Render the advisory dict as a compact Markdown block. Display-only; changes nothing."""
    lines = ["## Catalyst linkage — advisory (display-only, NOT a scoring/tier input)"]
    if not adv or not adv.get("signals"):
        lines.append("- No recent stocks signals to assess.")
        return "\n".join(lines)
    lines.append(
        f"- Coverage over last {adv['days']}d ({adv['signals']} stocks signals): "
        f"production news_supported **{adv['news_supported_pct']}%** "
        f"(~{adv['current_window_hours']}h scan window) · 24h exact-match shadow "
        f"**{adv['shadow_24h_pct']}%** (+{adv['uplift_24h_pp']}pp) · 48h exact-match shadow "
        f"**{adv['shadow_48h_pct']}%** (+{adv['uplift_48h_pp']}pp)")
    lines.append(f"- Newly-linked by wider window: 24h={adv['newly_linked_24h']} · "
                 f"48h={adv['newly_linked_48h']} (had no production catalyst, exact ticker match found)")
    for e in (adv.get("examples") or [])[:3]:
        lines.append(f"  - {e.get('symbol')}: {e.get('title')} ({e.get('source') or '?'})")
    lines.append(f"- **Caveat:** {adv['warning']} This block does not change tier or actionability.")
    return "\n".join(lines)
