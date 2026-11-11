"""Top-level catalyst-scan entry point.

Reads recent rows from ``news_items`` (the RSS / news_trader bridge
already populates this), classifies each into a structured
:class:`CatalystEvent`, clusters into :class:`NarrativeBasket`s, and
writes JSONL to ``data/catalysts/<YYYY-MM-DD>/``.

Pure read of ``news_items`` + ``events``. No new HTTP fetching here.
LLM is NOT invoked. No auto-trade. No scoring side effects.

The scheduler runs this as a thin step
(``python -m src.cli catalyst-scan``); failures inside it must never
propagate up — the caller wraps the subprocess timeout and logs a
warning. See PART 7 of the spec.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable

from src.catalysts.baskets import build_narrative_baskets, NARRATIVE_TAGS, _basket_for_event
from src.catalysts.classifier import (
    classify_catalyst_type,
    classify_source_quality,
    detect_low_liquidity_risk,
    detect_rumour_marker,
    is_test_source,
    score_importance,
)
from src.catalysts.models import CatalystEvent, NarrativeBasket
from src.storage.sqlite import SQLiteStore


CATALYST_DIR = Path("data") / "catalysts"
DEFAULT_LOOKBACK_HOURS = 12


@dataclass
class CatalystScanResult:
    cycle_label: str
    events: list[CatalystEvent] = field(default_factory=list)
    baskets: list[NarrativeBasket] = field(default_factory=list)
    events_path: Path | None = None
    baskets_path: Path | None = None
    summary_path: Path | None = None
    rejected_test_sources: int = 0
    rejected_missing_fields: int = 0
    scanned_rows: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "cycle_label": self.cycle_label,
            "events": [e.to_dict() for e in self.events],
            "baskets": [b.to_dict() for b in self.baskets],
            "events_path": str(self.events_path) if self.events_path else None,
            "baskets_path": str(self.baskets_path) if self.baskets_path else None,
            "summary_path": str(self.summary_path) if self.summary_path else None,
            "rejected_test_sources": self.rejected_test_sources,
            "rejected_missing_fields": self.rejected_missing_fields,
            "scanned_rows": self.scanned_rows,
        }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _hash_id(*parts: str) -> str:
    raw = "||".join(p or "" for p in parts).encode("utf-8")
    return "cat_" + hashlib.sha1(raw).hexdigest()[:16]


def _parse_published(value: str | None) -> datetime | None:
    if not value:
        return None
    for fmt in (
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S+00:00",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
    ):
        try:
            d = datetime.strptime(value.replace("Z", "+00:00"), fmt)
            if d.tzinfo is None:
                d = d.replace(tzinfo=timezone.utc)
            return d
        except Exception:
            continue
    try:
        d = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if d.tzinfo is None:
            d = d.replace(tzinfo=timezone.utc)
        return d
    except Exception:
        return None


def _freshness_hours(published_at: str | None) -> float | None:
    dt = _parse_published(published_at)
    if dt is None:
        return None
    now = datetime.now(timezone.utc)
    return max(0.0, (now - dt).total_seconds() / 3600.0)


def _normalize_symbol(s: str) -> str:
    s = (s or "").strip().upper()
    if not s:
        return s
    if "/" not in s:
        s = f"{s}/USDT"
    return s


def _url_slug(url: str | None) -> str:
    """Human-readable text from a URL slug (adds matchable words for the fallback matcher)."""
    if not url:
        return ""
    try:
        import re as _re
        tail = _re.sub(r"[?#].*$", "", str(url)).rstrip("/").rsplit("/", 1)[-1]
        return _re.sub(r"[-_]+", " ", _re.sub(r"\.(html?|php|aspx?)$", "", tail))
    except Exception:
        return ""


def _row_to_event(
    row: dict[str, Any],
    *,
    rejected_test: list[None],
    rejected_missing: list[None],
    alias_matcher: "EntityAliasMatcher | None" = None,
    crypto_matcher: "EntityAliasMatcher | None" = None,
    stocks_matcher: "EntityAliasMatcher | None" = None,
) -> list[CatalystEvent]:
    """Build CatalystEvent(s) from one news_items row.

    A row may mention multiple symbols → we emit one event per detected
    symbol so basket-clustering can see each. If no symbols detected we
    emit a single basket-level event with symbol="".
    """

    source = str(row.get("source") or "").strip()
    title = str(row.get("title") or "").strip()
    url = str(row.get("url") or "").strip()
    if not title or not source or not url:
        rejected_missing.append(None)
        return []
    if is_test_source(source):
        rejected_test.append(None)
        return []

    try:
        symbols_raw = json.loads(row.get("detected_symbols_json") or "[]")
    except Exception:
        symbols_raw = []
    symbols = [_normalize_symbol(str(s)) for s in symbols_raw if str(s).strip()]

    asset_class = str(row.get("asset_class") or "crypto").lower()
    # PART 2 fallback (asset-aware, 2026-07-08): when upstream didn't detect a symbol, run the curated
    # matcher for THIS row's asset class (stocks matcher → bare tickers; crypto matcher → SYM/USDT) over
    # combined text (title + url slug), not the crypto matcher for everything. Case-sensitive ticker guard
    # still prevents common-word collisions ("near"/"one"/"link"/"flow"). Macro/geopolitics rows that name
    # no tradable entity stay symbol-less (no forced ticker).
    if not symbols:
        _m = ((stocks_matcher if asset_class.startswith("stock") else crypto_matcher)
              or alias_matcher)     # alias_matcher = legacy crypto fallback for old callers
        if _m is not None:
            _slug = _url_slug(url)
            hits = _m.detect(f"{title} {_slug}".strip())
            if hits:
                # stocks matcher returns bare tickers; keep them bare. crypto returns SYM/USDT already.
                symbols = list(hits)
    catalyst_type = classify_catalyst_type(title)
    source_quality = classify_source_quality(source)
    low_liq = detect_low_liquidity_risk(title)
    rumour = detect_rumour_marker(title)

    if rumour and catalyst_type == "other_news":
        catalyst_type = "rumour_only"
    elif rumour:
        # keep the more specific type, just tag confidence down via flag
        pass

    if low_liq and catalyst_type == "other_news":
        catalyst_type = "low_liquidity_event"

    published_at = row.get("published_at")
    fresh = _freshness_hours(published_at)

    confidence = "high" if source_quality == "primary_source" else (
        "medium" if source_quality == "single_source" else "low"
    )
    if rumour:
        confidence = "low"

    # Sell-the-news heuristic: pump rumour + already-rallied related
    # symbols would be a real check; on classification alone we just set
    # the flag when the title talks about leaks / pre-reveals.
    sell_news = bool(
        catalyst_type in {"official_product_teaser", "rumour_only"}
    )

    primary_symbol = symbols[0] if symbols else ""
    related = symbols[1:] if len(symbols) > 1 else []

    importance = score_importance(
        catalyst_type=catalyst_type,
        source_quality=source_quality,
        freshness_hours=fresh,
        symbol=primary_symbol,
        related_symbols=related,
        title=title,
        is_rumour=rumour,
    )

    base_event = CatalystEvent(
        catalyst_id=_hash_id(url, primary_symbol or "basket"),
        asset_class=asset_class,
        symbol=primary_symbol,
        related_symbols=related,
        catalyst_type=catalyst_type,
        source=source,
        source_quality=source_quality,
        title=title[:480],
        url=url,
        timestamp=str(published_at) if published_at else None,
        freshness_hours=fresh,
        confidence=confidence,
        importance=importance,
        low_liquidity_risk=low_liq,
        sell_the_news_risk=sell_news,
        narrative=NARRATIVE_TAGS.get(_basket_for_event_skeleton(catalyst_type, [primary_symbol, *related])) or "",
    )

    return [base_event]


def _basket_for_event_skeleton(catalyst_type: str, symbols: list[str]) -> str | None:
    """Pre-classify basket without constructing a full event (avoid recursion)."""

    syms = {_normalize_symbol(s) for s in symbols if s}
    if catalyst_type in {"exchange_delisting", "margin_delisting", "low_liquidity_event"}:
        return "delisting_thin_liquidity"
    from src.catalysts.baskets import STATIC_BASKETS

    for basket_name, members in STATIC_BASKETS.items():
        if basket_name == "delisting_thin_liquidity":
            continue
        all_members = {*members["primary"], *members["related"]}
        if syms & set(all_members):
            return basket_name
    return None


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def collect_catalysts(
    db: SQLiteStore,
    *,
    project_root: Path,
    lookback_hours: int = DEFAULT_LOOKBACK_HOURS,
    cycle_label: str | None = None,
    write_files: bool = True,
) -> CatalystScanResult:
    """Run one catalyst scan: read recent news_items → classify → cluster → persist."""

    now = datetime.now(timezone.utc)
    cycle_label = cycle_label or now.strftime("cycle_%H-%M")
    cutoff_dt = now - timedelta(hours=lookback_hours)
    cutoff_iso = cutoff_dt.strftime("%Y-%m-%dT%H:%M:%S+00:00")

    result = CatalystScanResult(cycle_label=cycle_label)

    rejected_test: list[None] = []
    rejected_missing: list[None] = []
    events: list[CatalystEvent] = []

    # PART 2 — load BOTH curated entity-alias matchers (asset-aware, 2026-07-08) so a stocks row uses the
    # stocks matcher and a crypto row uses the crypto matcher when upstream RSS detection was empty.
    from src.catalysts.entity_aliases import get_matcher, get_stocks_matcher

    crypto_matcher = get_matcher(str(project_root))
    stocks_matcher = get_stocks_matcher(str(project_root))
    alias_matcher = crypto_matcher   # legacy name kept for the _row_to_event fallback signature

    # Pull recent rows from news_items. Defensive: if the table or
    # columns are missing on an older DB, we degrade gracefully.
    try:
        with db.connect() as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                """
                SELECT id, title, source, url, published_at,
                       detected_symbols_json, asset_class, raw_json
                  FROM news_items
                 WHERE COALESCE(published_at, '') >= ?
                    OR published_at IS NULL
                 ORDER BY id DESC
                 LIMIT 500
                """,
                (cutoff_iso,),
            ).fetchall()
    except sqlite3.OperationalError:
        rows = []

    for row in rows:
        result.scanned_rows += 1
        events.extend(_row_to_event(
            dict(row),
            rejected_test=rejected_test,
            rejected_missing=rejected_missing,
            alias_matcher=alias_matcher,
            crypto_matcher=crypto_matcher,
            stocks_matcher=stocks_matcher,
        ))

    result.rejected_test_sources = len(rejected_test)
    result.rejected_missing_fields = len(rejected_missing)
    result.events = events
    result.baskets = build_narrative_baskets(events)

    # PART 5 fix — add a momentum_breakout basket from latest report top
    # movers if any qualify (>=10% 24h, >=0.5x volume). Surfaces "new
    # gainers" even when no fresh news catalyst exists. Read-only.
    try:
        from src.catalysts.baskets import build_momentum_breakout_basket
        movers = _load_latest_top_movers(project_root)
        # PART 1 catalyst-integrity fix: do a DIRECT news_items lookup so a mover with a
        # recent high-importance symbol-tagged catalyst is NOT mislabeled "no catalyst".
        cat_syms: set[str] = set()
        try:
            with db.connect() as _cc:
                cat_syms = news_catalyst_symbols(
                    _cc, lookback_hours=max(lookback_hours, 24),
                    min_importance=CATALYST_MIN_IMPORTANCE,
                )
        except Exception:
            cat_syms = set()
        breakout = build_momentum_breakout_basket(movers, catalyst_symbols=cat_syms)
        if breakout is not None:
            result.baskets.append(breakout)
    except Exception:
        # Non-fatal: catalyst scan must never fail because of report parsing.
        pass

    if write_files:
        date_str = now.astimezone(timezone.utc).strftime("%Y-%m-%d")
        out_dir = project_root / CATALYST_DIR / date_str
        out_dir.mkdir(parents=True, exist_ok=True)
        events_path = out_dir / "catalyst_events.jsonl"
        baskets_path = out_dir / "narrative_baskets.jsonl"
        summary_path = out_dir / f"catalyst_{cycle_label}.md"
        # APPEND to events.jsonl so each cycle adds to the day's log.
        with events_path.open("a", encoding="utf-8") as fh:
            for ev in events:
                fh.write(json.dumps(ev.to_dict(), ensure_ascii=False) + "\n")
        # OVERWRITE baskets — they're a snapshot of the latest state.
        with baskets_path.open("w", encoding="utf-8") as fh:
            for basket in result.baskets:
                fh.write(json.dumps(basket.to_dict(), ensure_ascii=False) + "\n")
        summary_path.write_text(render_summary_markdown(result), encoding="utf-8")
        result.events_path = events_path
        result.baskets_path = baskets_path
        result.summary_path = summary_path

    return result


# ---------------------------------------------------------------------------
# Direct per-symbol news_items lookup (PART 1 catalyst-integrity fix)
# ---------------------------------------------------------------------------

# Importance floor for "this mover is catalyst-backed" (matches news collectors'
# base importance of 1.0 for a symbol-tagged row). Configurable; do not lower
# blindly — it only affects the *label*, never scoring/entries.
CATALYST_MIN_IMPORTANCE = 1.0


def news_catalyst_symbols(
    conn,
    *,
    lookback_hours: int = 24,
    min_importance: float = CATALYST_MIN_IMPORTANCE,
    now: datetime | None = None,
) -> set[str]:
    """Return the set of base tickers (e.g. ``{"ASTER"}``) that have a recent,
    symbol-tagged news_items row at/above ``min_importance``.

    DIRECT, schema-aware lookup — never trusts a basket's "no catalyst" claim.
    Defensive: discovers the symbol column (``detected_symbols_json`` preferred,
    falls back to a legacy ``detected_symbols`` column) and degrades to an empty
    set on any error. Read-only.
    """

    out: set[str] = set()
    try:
        cols = {r[1] for r in conn.execute("PRAGMA table_info(news_items)")}
    except sqlite3.OperationalError:
        return out
    sym_col = ("detected_symbols_json" if "detected_symbols_json" in cols
               else ("detected_symbols" if "detected_symbols" in cols else None))
    if not sym_col:
        return out
    has_imp = "importance" in cols
    reference = now or datetime.now(timezone.utc)
    if reference.tzinfo is None:
        reference = reference.replace(tzinfo=timezone.utc)
    cutoff = (reference.astimezone(timezone.utc) - timedelta(hours=lookback_hours)).strftime(
        "%Y-%m-%dT%H:%M:%S+00:00"
    )
    sel = f"{sym_col}" + (", importance" if has_imp else "")
    try:
        rows = conn.execute(
            f"SELECT {sel} FROM news_items WHERE published_at >= ? "
            f"ORDER BY id DESC LIMIT 1000",
            (cutoff,),
        ).fetchall()
    except sqlite3.OperationalError:
        return out
    for row in rows:
        raw = row[0]
        imp = row[1] if (has_imp and len(row) > 1) else None
        if has_imp and imp is not None:
            try:
                if float(imp) < min_importance:
                    continue
            except (TypeError, ValueError):
                pass
        try:
            syms = json.loads(raw) if isinstance(raw, str) else (raw or [])
        except (TypeError, ValueError, json.JSONDecodeError):
            syms = []
        for s in (syms or []):
            base = str(s).split("/")[0].strip().upper()
            if base:
                out.add(base)
    return out


# ---------------------------------------------------------------------------
# Latest report top-movers parser (for momentum_breakout basket)
# ---------------------------------------------------------------------------


def _load_latest_top_movers(project_root: Path) -> list[dict]:
    """Parse the latest scalp + intraday reports for the "Strongest Symbols"
    block and return a list of mover dicts.

    Each dict: ``{symbol, score, return_24h_pct, volume_ratio,
    overextension_risk}``.

    Read-only. Returns ``[]`` on any error.
    """

    import re

    movers: list[dict] = []
    for mode in ("scalp", "intraday"):
        report_dir = project_root / "data" / "reports" / mode
        if not report_dir.exists():
            continue
        # Pick the most recent file.
        candidates = sorted(report_dir.glob("*.md"))
        if not candidates:
            continue
        latest = candidates[-1]
        try:
            text = latest.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        # Find the "Strongest Symbols" block and parse its lines.
        # Format: "- SYMBOL/USDT: score X, 24h Y%, RS vs BTC Z%, volume Wx"
        start = text.find("### Strongest Symbols")
        if start < 0:
            continue
        end = text.find("###", start + 5)
        block = text[start:end] if end > 0 else text[start:]
        pattern = re.compile(
            r"^-\s+(?P<symbol>[A-Z0-9_]+/USDT)\s*:\s*"
            r"score\s+(?P<score>[\d.]+)\s*,\s*"
            r"24h\s+(?P<r24>-?[\d.]+)%\s*,\s*"
            r"RS\s+vs\s+BTC\s+(?P<rs>-?[\d.]+)%\s*,\s*"
            r"volume\s+(?P<vol>[\d.]+)x",
            re.MULTILINE,
        )
        for m in pattern.finditer(block):
            try:
                r24 = float(m.group("r24"))
                vol = float(m.group("vol"))
                score = float(m.group("score"))
            except ValueError:
                continue
            movers.append({
                "symbol": m.group("symbol"),
                "score": score,
                "return_24h_pct": r24,
                "volume_ratio": vol,
                # Overextension heuristic — score high but vol low signals
                # late-cycle chase. Mirrors the system's own "do not chase"
                # gate without re-running it.
                "overextension_risk": (score >= 85 and vol < 0.5) or r24 > 50,
            })
    # Dedup by symbol — keep the row with the highest 24h pct.
    by_sym: dict[str, dict] = {}
    for m in movers:
        s = m["symbol"]
        if s not in by_sym or m["return_24h_pct"] > by_sym[s]["return_24h_pct"]:
            by_sym[s] = m
    return list(by_sym.values())


# ---------------------------------------------------------------------------
# Markdown summary (used by report builder + scheduler cycle summary)
# ---------------------------------------------------------------------------


def render_summary_markdown(result: CatalystScanResult) -> str:
    lines: list[str] = [
        f"# Catalyst / narrative scan — {result.cycle_label}",
        "",
        f"Scanned `news_items` rows: **{result.scanned_rows}** "
        f"(rejected test_source: {result.rejected_test_sources}, "
        f"rejected missing fields: {result.rejected_missing_fields})",
        "",
        f"Catalyst events: **{len(result.events)}**",
        f"Narrative baskets: **{len(result.baskets)}**",
        "",
    ]

    by_type: dict[str, int] = {}
    for ev in result.events:
        by_type[ev.catalyst_type] = by_type.get(ev.catalyst_type, 0) + 1
    if by_type:
        lines.append("## By catalyst type")
        lines.append("")
        for k, v in sorted(by_type.items(), key=lambda kv: -kv[1]):
            lines.append(f"- {k}: {v}")
        lines.append("")

    if result.baskets:
        lines.append("## Narrative baskets")
        lines.append("")
        for b in result.baskets:
            primary = ", ".join(b.primary_symbols) or "—"
            related = ", ".join(b.related_symbols) or "—"
            lines.append(
                f"- **{b.basket_name}** (playbook: `{b.suggested_playbook}`, "
                f"source: {b.source_quality}, fresh: {b.freshness})"
            )
            lines.append(f"  - primary: {primary}")
            lines.append(f"  - related: {related}")
            lines.append(f"  - summary: {b.catalyst_summary[:240]}")
            lines.append("")

    # Top catalysts by importance — surfaces the most consequential events
    # first (including unmapped/basket-level ones), instead of insertion
    # order. Ranking aid only; no scoring side effects.
    ranked = sorted(
        (ev for ev in result.events if ev.catalyst_type != "other_news"),
        key=lambda e: e.importance,
        reverse=True,
    )
    if ranked:
        lines.append("## Top catalysts by importance")
        lines.append("")
        for ev in ranked[:10]:
            sym = ev.symbol or "(basket)"
            lines.append(
                f"- `{ev.importance:.2f}` **{sym}** [{ev.catalyst_type}] "
                f"{ev.title[:130]} ({ev.source}, {ev.source_quality})"
            )
        lines.append("")

    high_conf = [
        ev for ev in result.events
        if ev.confidence == "high" and ev.catalyst_type != "other_news"
    ]
    if high_conf:
        high_conf.sort(key=lambda e: e.importance, reverse=True)
        lines.append("## High-confidence catalysts (primary source)")
        lines.append("")
        for ev in high_conf[:15]:
            sym = ev.symbol or "(basket)"
            lines.append(
                f"- `{ev.importance:.2f}` **{sym}** [{ev.catalyst_type}] — {ev.title[:140]} "
                f"({ev.source}, {ev.timestamp or 'date unavailable'})"
            )
        lines.append("")

    rumours = [ev for ev in result.events if ev.catalyst_type == "rumour_only"]
    if rumours:
        lines.append("## Rumours (treat as low confidence)")
        lines.append("")
        for ev in rumours[:10]:
            sym = ev.symbol or "(basket)"
            lines.append(f"- {sym}: {ev.title[:140]} ({ev.source})")
        lines.append("")

    legal = [ev for ev in result.events if ev.catalyst_type == "legal_risk"]
    if legal:
        lines.append("## Legal / regulatory risk")
        lines.append("")
        for ev in legal[:10]:
            sym = ev.symbol or "(basket)"
            lines.append(f"- **{sym}**: {ev.title[:140]} ({ev.source})")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(
        "_Read-only enrichment. No auto-trade, no scoring changes. "
        "Manual Opus review reads this file via the `enriched-review` skill._"
    )
    return "\n".join(lines) + "\n"
