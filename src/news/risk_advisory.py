"""Production news RISK warnings (2026-07-04) — risk-only, NEVER a trade signal.

Reads `events` (earnings) + `news_items` (SEC/legal/FDA/hack/delisting/unlock/maintenance/offering/
macro) for the stocks/crypto universe and emits ONLY the allowed production risk effects. It can set
a `block_requires_operator_review` on a symbol, but it NEVER boosts a score, upgrades a tier, or
generates a buy/sell — and it never touches live/paper routing. Strong events only.
"""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from typing import Any

from src.config import load_config

# The ONLY effects this layer may produce. (No score boost / tier upgrade / buy-sell / live.)
ALLOWED_EFFECTS = (
    "risk_warning", "block_requires_operator_review", "do_not_chase_warning",
    "freshness_warning", "source_quality_warning", "conflicting_news_warning",
)

# strong-event keyword → (event_type, effect). Only genuinely material events qualify.
_STRONG = [
    (("sec ", " sec,", "s.e.c", "doj", "department of justice", "indict", "subpoena", "fraud charges",
      "securities fraud", "class action", "investigation into", "sec charges", "sec sues"),
     "legal_risk", "block_requires_operator_review"),
    (("fda rejects", "complete response letter", "clinical hold", "phase 3 fail", "trial failed",
      "missed primary endpoint", "fda warning letter"), "fda_clinical", "block_requires_operator_review"),
    (("hack", "exploit", "breach", "drained", "funds stolen", "security incident"),
     "exploit_hack", "block_requires_operator_review"),
    (("delist", "delisting", "will be removed", "trading suspended permanently"),
     "delisting", "block_requires_operator_review"),
    (("public offering", "shelf registration", "at-the-market offering", "convertible notes offering",
      "secondary offering", "prices offering", "share dilution"), "offering_dilution", "risk_warning"),
    (("token unlock", "cliff unlock", "vesting unlock", "large unlock"), "token_unlock", "risk_warning"),
    (("system maintenance", "suspend deposits", "halt withdrawals", "wallet maintenance",
      "scheduled maintenance"), "exchange_maintenance", "risk_warning"),
]
_BULL = ("beats", "surges", "approval", "upgrade", "record high", "wins contract", "buyback", "soars")
_BEAR = ("misses", "downgrade", "probe", "lawsuit", "recall", "cuts guidance", "plunge", "halts", "delist")


def _conn(db):
    c = sqlite3.connect(db or str(load_config().db_path))
    c.row_factory = sqlite3.Row
    return c


def _universe() -> set[str]:
    try:
        from src.stocks import load_stocks_config
        return {str(s).upper() for s in (load_stocks_config().default_symbols or [])}
    except Exception:
        return set()


def _stocks_universe() -> set[str]:
    out = set(_universe())
    try:
        from src.catalysts.entity_aliases import get_stocks_matcher
        out |= {str(t).upper() for t in get_stocks_matcher(str(load_config().root)).by_ticker.keys()}
    except Exception:
        pass
    return out


def _crypto_universe() -> set[str]:
    try:
        from src.catalysts.entity_aliases import get_matcher
        return {str(t).upper() for t in get_matcher(str(load_config().root)).by_ticker.keys()}
    except Exception:
        return set()


def _asset_class_for_symbol(symbol: str, fallback: str | None,
                            stocks: set[str], crypto: set[str]) -> str:
    """Resolve asset class from the canonical universes, not from possibly-misclassified news rows."""
    base = str(symbol or "").split("/")[0].upper()
    fb = str(fallback or "").lower()
    if base in stocks and base not in crypto:
        return "stocks"
    if base in crypto and base not in stocks:
        return "crypto"
    if base in stocks and base in crypto:
        return "crypto" if "/" in str(symbol) or fb.startswith("crypto") else "stocks"
    return "stocks" if fb.startswith("stock") else "crypto" if fb.startswith("crypto") else "unknown"


def compute_risk_warnings(db: str | None = None, *, hours: int = 48,
                          now: datetime | None = None) -> dict[str, Any]:
    """Per-symbol production risk effects (allowed set only). Read-only; no score/tier/routing change."""
    ref = (now or datetime.now(timezone.utc)).date().isoformat()
    conn = _conn(db)
    warnings: list[dict[str, Any]] = []
    stocks_universe = _stocks_universe()
    crypto_universe = _crypto_universe()
    try:
        # 1) earnings today / tomorrow → do_not_chase + operator-review (earnings risk)
        try:
            erows = conn.execute(
                "SELECT ticker, event_date FROM events WHERE event_type='earnings' "
                "AND event_date >= date(?) AND event_date <= date(?, '+1 day')", (ref, ref)).fetchall()
        except sqlite3.OperationalError:
            erows = []
        for r in erows:
            when = "today" if str(r["event_date"])[:10] == ref else "tomorrow"
            warnings.append({"symbol": str(r["ticker"]).upper(), "asset_class": "stocks",
                             "event_type": "earnings", "effect": "do_not_chase_warning",
                             "reason": f"earnings {when} ({r['event_date']}) — avoid chasing into the print",
                             "source": "events", "published_at": r["event_date"]})
            warnings.append({"symbol": str(r["ticker"]).upper(), "asset_class": "stocks",
                             "event_type": "earnings", "effect": "block_requires_operator_review",
                             "reason": f"earnings {when}: new A/B here needs operator review",
                             "source": "events", "published_at": r["event_date"]})
        import json as _json
        has_canonical = conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name='news_canonical_events'"
        ).fetchone()
        if has_canonical:
            # Canonical rows use trusted_symbols only, collapse repeated reports
            # and carry the fixed risk action decided by the influence policy.
            from src.news.source_health import _parse_ts
            ref_dt = now or datetime.now(timezone.utc)
            cutoff = ref_dt.timestamp() - hours * 3600
            crows = conn.execute(
                "SELECT * FROM news_canonical_events WHERE is_cluster_primary=1 "
                "AND risk_action!='none' ORDER BY published_at DESC").fetchall()
            for r in crows:
                published = _parse_ts(r["published_at"])
                if published is None or published.timestamp() < cutoff:
                    continue
                try:
                    syms = _json.loads(r["trusted_symbols_json"] or "[]") or []
                except Exception:
                    syms = []
                effect = ("block_requires_operator_review" if r["risk_action"] == "operator_review"
                          else "risk_warning")
                for s in syms:
                    sym = str(s).split("/")[0].upper()
                    warnings.append({"symbol": sym,
                                     "asset_class": _asset_class_for_symbol(
                                         str(s), r["asset_class"], stocks_universe, crypto_universe),
                                     "event_type": r["event_type"], "effect": effect,
                                     "reason": (r["title"] or "")[:120], "source": r["source"],
                                     "published_at": r["published_at"]})
        else:
            # Old-schema fallback.
            from src.news.source_health import window_news_rows
            nrows = window_news_rows(
                conn, hours=hours, now=now, limit=600,
                where="detected_symbols_json IS NOT NULL AND detected_symbols_json NOT IN ('[]','')") or []
            for r in nrows:
                title = (r["title"] or "").lower()
                for kws, etype, effect in _STRONG:
                    if any(k in title for k in kws):
                        try:
                            syms = _json.loads(r["detected_symbols_json"]) or []
                        except Exception:
                            syms = []
                        for s in syms:
                            sym = str(s).split("/")[0].upper()
                            warnings.append({"symbol": sym,
                                             "asset_class": _asset_class_for_symbol(
                                                 str(s), r["asset_class"], stocks_universe, crypto_universe),
                                             "event_type": etype,
                                             "effect": effect, "reason": (r["title"] or "")[:120],
                                             "source": r["source"], "published_at": r["published_at"]})
                        break
    finally:
        conn.close()
    # de-dup (symbol, effect, event_type)
    seen, deduped = set(), []
    for w in warnings:
        k = (w["symbol"], w["effect"], w["event_type"])
        if k not in seen:
            seen.add(k)
            deduped.append(w)
    by_symbol: dict[str, list] = {}
    for w in deduped:
        by_symbol.setdefault(w["symbol"], []).append(w)
    blocks = sorted({w["symbol"] for w in deduped if w["effect"] == "block_requires_operator_review"})
    return {"as_of": ref, "window_hours": hours, "warnings": deduped, "by_symbol": by_symbol,
            "symbols_requiring_operator_review": blocks,
            "allowed_effects": list(ALLOWED_EFFECTS),
            "changes_score": False, "changes_tier": False, "changes_actionability": False,
            "generates_trade": False,
            "note": "RISK-ONLY production effects. Never a buy/sell, never a score/tier change, never "
                    "live. block_requires_operator_review SURFACES an operator-review warning for NEW "
                    "A/B consideration (display/advisory only) — it does not itself gate signal "
                    "routing or execution."}


def write_diagnostics(db: str | None = None, *, hours: int = 48,
                      now: datetime | None = None, write: bool = True) -> dict[str, Any]:
    """Compose the production catalyst/risk read-model artifact for the control-plane.

    Combines risk-only warnings (this module) with the normalized-event summary
    (src.news.events). Writes `data/diagnostics/news_catalysts.json` — a pure read-model
    the Mini App reads. NEVER a trade signal; risk-only, live locked. Fail-open.
    """
    rw = compute_risk_warnings(db, hours=hours, now=now)
    events_summary: dict[str, Any] = {"available": False}
    try:
        from src.news.events import normalized_events
        ev = normalized_events(db, hours=hours, now=now)
        if ev.get("available"):
            by_type: dict[str, int] = {}
            by_class: dict[str, int] = {}
            for e in ev.get("events", []):
                by_type[e.get("event_type", "other")] = by_type.get(e.get("event_type", "other"), 0) + 1
                by_class[e.get("asset_class", "other")] = by_class.get(e.get("asset_class", "other"), 0) + 1
            events_summary = {
                "available": True, "count": ev.get("count", 0),
                "deduped_from": ev.get("deduped_from", 0),
                "conflicting_symbols": ev.get("conflicting_symbols", []),
                "by_event_type": by_type, "by_asset_class": by_class,
                "recent": [
                    {k: e.get(k) for k in ("source_quality", "asset_class", "event_type",
                                           "symbols", "direction_hint", "title", "source")}
                    for e in ev.get("events", [])[:20]
                ],
            }
    except Exception as exc:  # noqa: BLE001 — advisory only
        events_summary = {"available": False, "reason": str(exc)}

    artifact = {
        "as_of": rw["as_of"], "window_hours": hours, "live_locked": True,
        "allowed_effects": list(ALLOWED_EFFECTS),
        "not_allowed": ["score_boost", "tier_upgrade", "buy_sell_signal_from_news",
                        "live_order", "auto_live_or_manual_live_unlock"],
        "symbols_requiring_operator_review": rw["symbols_requiring_operator_review"],
        "warnings": rw["warnings"], "by_symbol": rw["by_symbol"],
        "events_summary": events_summary,
        "changes_score": False, "changes_tier": False, "generates_trade": False,
        "note": rw["note"],
    }
    if write:
        try:
            import json as _json
            root = load_config().root
            (root / "data" / "diagnostics").mkdir(parents=True, exist_ok=True)
            (root / "data" / "diagnostics" / "news_catalysts.json").write_text(
                _json.dumps(artifact, indent=2, default=str), encoding="utf-8")
        except Exception:  # noqa: BLE001 — never fatal
            pass
    return artifact


def render_markdown(rw: dict) -> str:
    lines = ["## Production risk warnings (risk-only — never a buy/sell / score / tier change)"]
    if not rw["warnings"]:
        lines.append("- No strong risk events in the window.")
        return "\n".join(lines)
    if rw["symbols_requiring_operator_review"]:
        lines.append(f"- **Operator-review warning (advisory — does NOT gate routing/execution):** "
                     f"{', '.join(rw['symbols_requiring_operator_review'])}")
    for sym, ws in sorted(rw["by_symbol"].items()):
        effs = sorted({w["effect"] for w in ws})
        ex = ws[0]
        lines.append(f"- {sym} [{ex['event_type']}]: {', '.join(effs)} — {ex['reason']} "
                     f"({ex['source']})")
    lines.append(f"_{rw['note']}_")
    return "\n".join(lines)
