"""Report potentially important news that still lacks a trusted tradeable entity.

This is an audit queue, not a trading input.  It separates meaningful mapping
gaps (for example an exchange listing for an untracked token) from normal macro
context, so a high raw match rate cannot hide missed trade-relevant stories.
"""
from __future__ import annotations

import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.config import load_config
from src.news import entity_resolver as resolver
from src.news.content_coverage import content_level
from src.news.source_health import window_news_rows


_CRYPTO_RULES = {
    "listing": ("to list", "will list", "has listed", "opens trading", "perpetual", "delist"),
    "security": ("exploit", "hack", "drained", "breach", "stolen", "vulnerability"),
    "exchange_or_stablecoin": ("withdrawal", "depeg", "insolvency", "suspends", "halted"),
    "regulation": ("sec charges", "sec sues", "settlement", "indictment", "sanction"),
}
_STOCK_RULES = {
    "earnings": ("earnings", "guidance", "revenue", "eps", "forecast"),
    "filing_or_offering": ("8-k", "10-q", "10-k", "s-1", "offering", "dilution", "prospectus"),
    "legal": ("lawsuit", "investigation", "sec probe", "antitrust", "settlement"),
    "corporate_action": ("acquisition", "merger", "buyback", "bankruptcy", "trading halt"),
}
_STOCK_TICKER = re.compile(
    r"(?:\((?:NASDAQ|NYSE|NYSE\s+AMERICAN)\s*:\s*|\((?=[A-Z]{1,5}\)))"
    r"([A-Z]{1,5})\)?|\b(?:NASDAQ|NYSE|NYSE\s+AMERICAN)\s*:\s*([A-Z]{1,5})\b"
)
_CRYPTO_TICKER = re.compile(r"[$#]([A-Z][A-Z0-9]{1,19})\b")
_EDITORIAL_MARKERS = (
    "better buy", "should investors", "should you buy", "is it time to buy",
    "reasons to buy", "reasons investors", "buy the dip", "stock to buy",
    "here's why", "here’s why",
)
_EDITORIAL_TITLE_PATTERNS = (
    re.compile(r"\bcould be (?:a |the )?(?:massive |major |big |huge )?winner\b", re.I),
    re.compile(r"\b(?:top|best) \d+ stocks?\b", re.I),
)


def _root() -> Path:
    return Path(__file__).resolve().parents[2]


def _labels(text: str, asset_class: str) -> list[str]:
    rules = _STOCK_RULES if asset_class == "stocks" else _CRYPTO_RULES
    low = text.lower()
    return sorted(label for label, phrases in rules.items() if any(p in low for p in phrases))


def _has_trusted(value: Any) -> bool:
    try:
        return bool(json.loads(value)) if isinstance(value, str) else bool(value)
    except (TypeError, ValueError):
        return False


def _explicit_candidates(text: str, asset_class: str) -> list[str]:
    pattern = _STOCK_TICKER if asset_class == "stocks" else _CRYPTO_TICKER
    values: set[str] = set()
    for match in pattern.finditer(text):
        values.update(value for value in match.groups() if value)
    return sorted(values)


def _is_editorial_stock_title(title: str) -> bool:
    """Return true for opinion/idea headlines rather than issuer events."""
    normalized = str(title or "").lower()
    return (any(marker in normalized for marker in _EDITORIAL_MARKERS)
            or any(pattern.search(normalized) for pattern in _EDITORIAL_TITLE_PATTERNS))


def compute_coverage_gaps(db: str | None = None, *, hours: int = 72,
                          now: datetime | None = None, examples: int = 50) -> dict[str, Any]:
    """Find high-impact rows that have no trusted symbol after resolution.

    Rows are recomputed through the pure resolver for diagnosis only.  This lets
    the report reveal an alias/listing gap even if a scheduler pass has not yet
    persisted the resolver's latest version.
    """
    path = db or str(load_config().db_path)
    now = now or datetime.now(timezone.utc)
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        rows = window_news_rows(
            conn, hours=int(hours), now=now,
            columns=("title, source, url, published_at, asset_class, raw_json, content_text, importance, "
                     "trusted_symbols_json, resolution_status"),
        ) or []
    except sqlite3.OperationalError:
        rows = []
    finally:
        conn.close()

    items: list[dict[str, Any]] = []
    macro_context_only = 0
    non_symbol_impact_rows = 0
    scanned_important = 0
    crypto_matcher, stocks_matcher = resolver._matchers()
    for row in rows:
        asset = str(row.get("asset_class") or "crypto").lower()
        fields = resolver.extract_text_fields(row)
        labels = _labels(fields["combined"], asset)
        if not labels:
            continue
        scanned_important += 1
        if _has_trusted(row.get("trusted_symbols_json")):
            continue
        resolved = resolver.resolve_row(row, crypto_matcher=crypto_matcher, stocks_matcher=stocks_matcher)
        if resolved["trusted_symbols"]:
            state = "resolver_pending_persist"
        elif resolved["tradability_status"] == "macro_only":
            macro_context_only += 1
            continue
        elif any(e.get("kind") == "untracked_entity" for e in resolved["detected_entities"]):
            state = "untracked_entity"
        else:
            state = "unmapped_impact"
        untracked = [e.get("ticker") for e in resolved["detected_entities"]
                     if e.get("kind") == "untracked_entity" and e.get("ticker")]
        explicit = _explicit_candidates(fields["combined"], asset)
        # A generic lawsuit/earnings article with no issuer/project/ticker is
        # market context, not evidence that the resolver missed a tradable name.
        if not untracked and not explicit:
            non_symbol_impact_rows += 1
            continue
        matcher = stocks_matcher if asset == "stocks" else crypto_matcher
        if state == "unmapped_impact" and explicit and all(
            ticker not in matcher.by_ticker for ticker in explicit
        ):
            state = "outside_trade_universe"
        # Editorial comparison/opinion headlines are useful context but must
        # not make the resolver trust gate fail as if a factual issuer event
        # had been lost. Explicit mapped entities still remain visible through
        # resolver_pending_persist above.
        if (state == "unmapped_impact" and asset == "stocks" and not untracked
                and _is_editorial_stock_title(fields["title"])):
            non_symbol_impact_rows += 1
            continue
        items.append({
            "state": state, "impact_labels": labels, "asset_class": asset,
            "source": row.get("source"), "published_at": row["_ts"].isoformat(),
            "importance": row.get("importance"), "title": str(row.get("title") or "")[:240],
            "url": row.get("url"), "untracked_entities": sorted(set(untracked)),
            "explicit_candidates": explicit,
            "resolution_status": row.get("resolution_status"),
            "content_level": content_level(row),
        })
    priority = {"untracked_entity": 0, "unmapped_impact": 1, "outside_trade_universe": 2,
                "resolver_pending_persist": 3}
    items.sort(key=lambda item: item["published_at"], reverse=True)
    items.sort(key=lambda item: priority[item["state"]])
    by_state = {state: sum(1 for item in items if item["state"] == state)
                for state in ("untracked_entity", "unmapped_impact", "outside_trade_universe",
                              "resolver_pending_persist")}
    return {
        "generated_at": now.isoformat(), "hours": int(hours), "important_rows_scanned": scanned_important,
        "potential_gaps": len(items), "by_state": by_state, "macro_context_only": macro_context_only,
        "non_symbol_impact_rows": non_symbol_impact_rows,
        "items": items[: int(examples)],
        "note": "READ-ONLY audit queue. A gap is not a trading recommendation; it requires an issuer/project "
                "mapping or a resolver-persistence check before it can be trusted for catalyst linkage.",
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# News Coverage Gaps", "",
        f"_Generated: {report['generated_at'][:19]}Z · last {report['hours']}h · read-only._", "",
        f"High-impact rows scanned: **{report['important_rows_scanned']}** · potential mapping gaps: "
        f"**{report['potential_gaps']}** · macro-context-only: {report['macro_context_only']}", "",
        "| state | count |", "|---|---:|",
    ]
    for state, count in report["by_state"].items():
        lines.append(f"| {state} | {count} |")
    lines.append(f"\n_Non-symbol impact context excluded from this queue: {report['non_symbol_impact_rows']}._")
    items = report.get("items") or []
    if items:
        lines += ["", "## Needs review", ""]
        for item in items:
            entities = ", ".join(item["untracked_entities"]) or "none"
            lines.append(f"- **{item['state']}** · [{item['asset_class']}] {item['source']} · "
                         f"{', '.join(item['impact_labels'])} · entities: {entities} · "
                         f"{item['title']}")
    else:
        lines += ["", "_No high-impact rows currently lack a trusted entity mapping._"]
    lines += ["", f"_{report['note']}_"]
    return "\n".join(lines)


def refresh(db: str | None = None, *, hours: int = 72, now: datetime | None = None,
            write: bool = True) -> dict[str, Any]:
    report = compute_coverage_gaps(db, hours=hours, now=now)
    if write:
        root = _root()
        (root / "reports").mkdir(parents=True, exist_ok=True)
        (root / "data" / "diagnostics").mkdir(parents=True, exist_ok=True)
        (root / "reports" / "NEWS_COVERAGE_GAPS.md").write_text(render_markdown(report), encoding="utf-8")
        (root / "data" / "diagnostics" / "news_coverage_gaps.json").write_text(
            json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report


__all__ = ["compute_coverage_gaps", "render_markdown", "refresh"]
