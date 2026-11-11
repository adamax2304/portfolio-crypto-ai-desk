"""Catalyst integrity monitoring (after the ASTER label fix).

Guards against regression of the bug where a high-importance, symbol-tagged
news_items row was NOT reflected as a catalyst (momentum basket called a
catalyst-backed mover "no catalyst"). Pure reporting — never promotes a trade,
never changes scoring.

Two entry points:
  * `catalyst_integrity_for_signal` — per-candidate payload fields.
  * `scan_catalyst_integrity` — daily summary + warnings.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.catalysts.collector import CATALYST_MIN_IMPORTANCE, news_catalyst_symbols


def _base_ticker(symbol: str | None) -> str:
    return str(symbol or "").split("/")[0].strip().upper()


def catalyst_integrity_for_signal(
    conn: Any,
    signal: dict[str, Any],
    *,
    lookback_hours: int = 24,
    min_importance: float = CATALYST_MIN_IMPORTANCE,
) -> dict[str, Any]:
    """Per-candidate catalyst-integrity fields for the alert payload.

    Confirms whether THIS symbol has a direct high-importance news_items hit and
    labels accordingly. Fails open to 'unknown' (never fabricates a catalyst)."""
    try:
        # Honest unknown: if news_items is unavailable we cannot claim "no catalyst".
        if conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='news_items'"
        ).fetchone() is None:
            raise RuntimeError("news_items table unavailable")
        cats = news_catalyst_symbols(
            conn, lookback_hours=lookback_hours, min_importance=min_importance)
        base = _base_ticker(signal.get("symbol"))
        backed = base in cats
        return {
            "catalyst_integrity_status": (
                "catalyst_backed_confirmed" if backed else "no_direct_news_catalyst"),
            "direct_news_items_checked": True,
            "catalyst_mapping_confidence": "high",
        }
    except Exception:
        return {
            "catalyst_integrity_status": "unknown",
            "direct_news_items_checked": False,
            "catalyst_mapping_confidence": "low",
        }


def _catalyst_dir(now: datetime) -> Path:
    from src.config import load_config
    root = load_config().root
    day = now.astimezone(timezone.utc).strftime("%Y-%m-%d")
    return root / "data" / "catalysts" / day


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    try:
        if not path.exists():
            return out
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                out.append(json.loads(line))
    except Exception:
        return out
    return out


def scan_catalyst_integrity(
    conn: Any,
    *,
    now: datetime | None = None,
    lookback_hours: int = 24,
    min_importance: float = CATALYST_MIN_IMPORTANCE,
    unmapped_warn_threshold: int = 5,
) -> dict[str, Any]:
    """Daily integrity summary. Combines DB-derived catalyst symbols with the
    day's catalyst artifacts (if present) to flag:
      * high-importance symbol-tagged news that did NOT map into catalyst_events;
      * any no-catalyst/momentum-basket symbol that DOES have a direct news hit
        (the exact bug signature).
    Artifact-derived numbers are null (not faked) when artifacts are absent.

    The artifact collector is intentionally narrower than the raw-news
    classifier: it excludes diffuse and non-actionable headlines.  Therefore a
    raw direct-news symbol that is absent from ``catalyst_events.jsonl`` is an
    observability gap, not by itself a trading regression.  The actionable
    regression signature remains a momentum/no-catalyst basket carrying a
    direct news hit.
    """
    now = now or datetime.now(timezone.utc)
    warnings: list[str] = []
    result: dict[str, Any] = {
        "as_of": now.isoformat(),
        "high_importance_symbol_tagged": None,
        "catalyst_symbols": [],
        "mapped_event_symbols": None,
        "unmapped_high_importance_symbols": None,
        "unmapped_high_importance_count": None,
        "artifact_scope_gap_symbols": None,
        "no_catalyst_basket_news_hits": [],
        "warning": False,
        "warnings": warnings,
        "catalyst_integrity_status": "unknown",
        "catalyst_mapping_confidence": "low",
        "direct_news_items_checked": False,
    }

    # 1) DB-derived catalyst symbols (the source of truth the fix relies on).
    try:
        cats = news_catalyst_symbols(
            conn, lookback_hours=lookback_hours, min_importance=min_importance)
        result["catalyst_symbols"] = sorted(cats)
        result["direct_news_items_checked"] = True
        row = conn.execute(
            "SELECT COUNT(*) FROM news_items "
            "WHERE COALESCE(importance,0) >= ? "
            "AND COALESCE(detected_symbols_json,'') NOT IN ('','[]','null')",
            (min_importance,),
        ).fetchone()
        result["high_importance_symbol_tagged"] = int(row[0]) if row else None
    except Exception:
        warnings.append("could not read news_items catalyst symbols")
        result["warning"] = True
        return result

    # 2) Artifact cross-check (best-effort).
    cat_dir = _catalyst_dir(now)
    events = _load_jsonl(cat_dir / "catalyst_events.jsonl")
    baskets = _load_jsonl(cat_dir / "narrative_baskets.jsonl")

    if events:
        mapped: set[str] = set()
        for ev in events:
            mapped.add(_base_ticker(ev.get("symbol")))
            for rs in (ev.get("related_symbols") or []):
                mapped.add(_base_ticker(rs))
        mapped.discard("")
        result["mapped_event_symbols"] = sorted(mapped)
        unmapped = sorted(s for s in result["catalyst_symbols"] if s not in mapped)
        result["unmapped_high_importance_symbols"] = unmapped
        result["unmapped_high_importance_count"] = len(unmapped)
        result["artifact_scope_gap_symbols"] = unmapped

    if baskets:
        cats = set(result["catalyst_symbols"])
        hits: list[str] = []
        for b in baskets:
            summary = str(b.get("catalyst_summary") or "").lower()
            is_no_catalyst = (
                b.get("basket_name") == "momentum_breakout"
                and "without confirmed news catalyst" in summary
                and "catalyst-backed" not in summary
            )
            if not is_no_catalyst:
                continue
            for sym in (list(b.get("primary_symbols") or [])
                        + list(b.get("related_symbols") or [])):
                if _base_ticker(sym) in cats:
                    hits.append(_base_ticker(sym))
        if hits:
            result["no_catalyst_basket_news_hits"] = sorted(set(hits))
            warnings.append(
                "no-catalyst basket contains symbols with direct news hits "
                f"(regression signature): {', '.join(sorted(set(hits)))}")

    result["warning"] = bool(warnings)
    result["catalyst_integrity_status"] = "warning" if warnings else "ok"
    result["catalyst_mapping_confidence"] = (
        "high" if (events and not warnings) else
        "medium" if events else "low")
    return result
