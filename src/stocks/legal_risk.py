"""Stocks legal/headline risk gate (PART 3 + PART 17 fix).

PART 17 (2026-06-03) — persistent legal-flag carry.

The original PART 3 gate relied on whatever rows ``CompanyNewsAgent``
surfaced via ``load_recent_news(limit=200)``. Once the news feed flow
exceeded ~200 fresh rows / cycle (Telegram collector + RSS), older
legal facts — SMCI's March-2026 SDNY indictment, the April-2026 IR
update, the May-2026 class-action filings — were silently dropped
beyond the 200-row LIMIT, and the gate stopped firing for SMCI even
though the news was right there in the DB. PART 17 adds an
explicit ``load_active_legal_news()`` loader that queries the
news_items table directly for symbol+legal-keyword matches across a
**90-day rolling window**, regardless of recency-rank.

In ``trade_idea_agent.py`` the legal-risk path now:

* fetches the recent CompanyNewsAgent hits (unchanged),
* merges with the persistent legal-keyword window via the new loader,
* runs ``detect_legal_risk`` on the union,
* if the result is blocking AND the tier is A/B → **demotes tier to C**
  (still visible in reports for human review; no longer falsely-clean
  actionable; Telegram dispatch remains blocked by the existing
  monitor-side gate).


The deterministic stocks pipeline rated SMCI A-tier on 2026-05-29 cycle 2
purely on price/momentum despite an **active federal indictment**, multiple
securities class-action filings, and a prior E&Y auditor resignation. The
system was structurally blind to that category of risk because no agent
read news titles for legal red flags.

This module is read-only and intentionally minimal:

* Pattern-match (case-insensitive) over recent CompanyNewsAgent hits.
* Categorise into ``indictment / sec_doj / securities_fraud /
  auditor / class_action / going_concern / restatement / delisting``.
* Return a structured assessment; the caller decides what to do.

Integration:

* :class:`src.stocks.agents.trade_idea_agent.StockTradeIdeaAgent` calls
  :func:`detect_legal_risk` per symbol and, when the verdict is high
  severity, appends ``ACTIVE_LEGAL_HEADLINE_RISK: <categories>`` to
  ``idea.avoid_conditions`` and a ``legal_headline_risk: ...`` entry to
  ``idea.cap_reasons``. The signal-tracking registry persists
  ``avoid_conditions`` as ``no_entry_conditions_json``.
* :class:`src.stocks.monitor.MaterialImprovementChecker` reads
  ``no_entry_conditions_json`` from the live ``proposed_signals`` row
  and blocks Telegram dispatch with ``alert_type="legal_block"``.

The gate **does not change scoring or thresholds.** It blocks Telegram
dispatch and records a no-entry condition; the score/tier remain visible
in reports for human review.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any, Iterable


# ---------------------------------------------------------------------------
# Pattern definitions
# ---------------------------------------------------------------------------

# Each category maps to a list of regexes (case-insensitive). Keep these
# narrow — we want few false positives. A single high-confidence hit is
# enough to block; vague signals (e.g. "investigation" alone) are NOT
# included because they trigger on every routine SEC filing review.

LEGAL_RISK_PATTERNS: dict[str, list[str]] = {
    "indictment": [
        r"\bindict(ed|ment|ing)\b",
        r"\bfederal (indictment|charges?)\b",
        r"\bcriminal (charge|charges|indictment)\b",
        r"\barrest(ed)?\b.{0,40}\b(ceo|cfo|executive|founder|chair)\b",
    ],
    "sec_doj": [
        r"\bSEC\b.{0,40}\b(charges?|charged|sues|complaint|enforcement action|investigation|probe)\b",
        r"\bDOJ\b.{0,40}\b(charges?|charged|sues|investigation|probe)\b",
        r"\bdepartment of justice\b.{0,40}\b(charges?|sues|investigation|probe)\b",
        r"\bsecurities and exchange commission\b.{0,40}\b(charges?|sues|complaint|investigation)\b",
    ],
    "securities_fraud": [
        r"\bsecurities fraud\b",
        r"\baccounting fraud\b",
        r"\bfinancial fraud\b",
        r"\bmisstatement[s]? of (financials|earnings|revenue)\b",
    ],
    "auditor": [
        r"\bauditor (resign[a-z]*|stepped? down|withdrew|dismissed)\b",
        r"\b(E&Y|Ernst & Young|PwC|PricewaterhouseCoopers|Deloitte|KPMG|BDO) "
        r"(resign[a-z]*|withdraw[a-z]*|step[a-z]* down)\b",
        # PART 17 — handle "<Auditor> resigns/withdraws as <company> auditor".
        r"\b(E&Y|Ernst & Young|PwC|PricewaterhouseCoopers|Deloitte|KPMG|BDO) "
        r"resign[a-z]*\b",
        r"\bgoing concern (doubt|warning|qualification)\b",
        r"\badverse audit opinion\b",
    ],
    "class_action": [
        r"\b(securities? )?class[- ]action (lawsuit|complaint|filed|filing|deadline)\b",
        # PART 17 — handle "Files New Securities Class Action Against" and
        # "Securities Class Action Against <company>" headline patterns
        # that the law-firm PR wire uses.
        r"\bsecurities? class[- ]action\b",
        r"\b(files?|announces?|reminds?)\b.{0,60}\bclass[- ]action\b",
        r"\bshareholder lawsuit\b",
        r"\binvestors? sue[ds]?\b",
    ],
    "going_concern": [
        r"\bgoing concern\b",
        r"\bbankruptcy (filing|petition|chapter 11|chapter 7)\b",
        r"\bchapter (7|11)\b.{0,30}\bbankrupt",
    ],
    "restatement": [
        r"\b(financial )?restatement\b",
        r"\brestate(d|s)? (its )?(earnings|financials|results)\b",
        r"\bmaterial weakness\b.{0,30}\b(internal controls?|reporting)\b",
    ],
    "delisting": [
        r"\bdelist(ed|ing|ment)\b",
        r"\bnoncompliance with (NASDAQ|NYSE) (listing )?(rules|standards)\b",
        r"\btrading halt(ed)?\b",
    ],
}

# Categories that always block A/B Telegram dispatch when matched with any
# hit. Lower-severity categories (restatement, delisting alone) still get
# surfaced in the counter-thesis but do not auto-block; they are an
# advisory note.
BLOCKING_CATEGORIES = frozenset({
    "indictment",
    "sec_doj",
    "securities_fraud",
    "auditor",
    "class_action",
    "going_concern",
})

# Marker string used on ``idea.avoid_conditions`` (and persisted as
# ``no_entry_conditions_json``) — the monitor scans for this prefix to
# decide whether to block Telegram. Stable across schema migrations.
AVOID_CONDITION_MARKER = "ACTIVE_LEGAL_HEADLINE_RISK"


# ---------------------------------------------------------------------------
# Assessment dataclass
# ---------------------------------------------------------------------------


@dataclass
class LegalRiskAssessment:
    categories: list[str] = field(default_factory=list)
    severity: str = "none"  # "high" / "medium" / "none"
    evidence: list[dict[str, str]] = field(default_factory=list)
    blocking: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "categories": list(self.categories),
            "severity": self.severity,
            "evidence": list(self.evidence),
            "blocking": self.blocking,
        }

    @property
    def avoid_condition(self) -> str | None:
        if not self.blocking:
            return None
        cats = ",".join(sorted(self.categories))
        return f"{AVOID_CONDITION_MARKER}: {cats}"

    @property
    def cap_reason(self) -> str | None:
        if not self.blocking:
            return None
        return f"legal_headline_risk: {','.join(sorted(self.categories))}"

    @property
    def counter_thesis(self) -> str | None:
        if not self.categories:
            return None
        cats = ", ".join(sorted(self.categories))
        if self.blocking:
            return (
                f"ACTIVE LEGAL HEADLINE RISK ({cats}) — score reflects "
                "price/momentum but does NOT see legal/governance issues. "
                "Telegram dispatch suppressed; verify headlines before any action."
            )
        return f"Headline note: {cats} mentioned in recent news; review before acting."


# ---------------------------------------------------------------------------
# Detection
# ---------------------------------------------------------------------------


def _haystack(hit: dict[str, Any]) -> str:
    """Flatten a news hit into a single searchable string."""

    parts: list[str] = []
    for key in ("title", "headline", "summary", "description"):
        v = hit.get(key)
        if v:
            parts.append(str(v))
    return " ".join(parts)


def _compile_patterns() -> dict[str, list[re.Pattern[str]]]:
    return {
        cat: [re.compile(p, re.IGNORECASE) for p in patterns]
        for cat, patterns in LEGAL_RISK_PATTERNS.items()
    }


_COMPILED = _compile_patterns()


def detect_legal_risk(news_hits: Iterable[dict[str, Any]]) -> LegalRiskAssessment:
    """Scan news titles for legal/headline risk categories.

    ``news_hits`` is an iterable of dicts with at least a ``title`` (or
    ``headline``) field. Other fields (``source``, ``url``, ``published_at``)
    are preserved into the evidence list when present.
    """

    matched: dict[str, list[dict[str, str]]] = {}
    for hit in news_hits or []:
        text = _haystack(hit)
        if not text:
            continue
        for category, patterns in _COMPILED.items():
            if any(p.search(text) for p in patterns):
                matched.setdefault(category, []).append(
                    {
                        "category": category,
                        "title": str(hit.get("title") or hit.get("headline") or "")[:240],
                        "source": str(hit.get("source") or ""),
                        "url": str(hit.get("url") or ""),
                        "published_at": str(hit.get("published_at") or ""),
                    }
                )

    if not matched:
        return LegalRiskAssessment()

    categories = sorted(matched.keys())
    evidence: list[dict[str, str]] = []
    for cat in categories:
        evidence.extend(matched[cat][:3])  # keep first 3 hits per category

    blocking = any(c in BLOCKING_CATEGORIES for c in categories)
    severity = "high" if blocking else "medium"
    return LegalRiskAssessment(
        categories=categories,
        severity=severity,
        evidence=evidence,
        blocking=blocking,
    )


# ---------------------------------------------------------------------------
# Monitor-side helper
# ---------------------------------------------------------------------------


def _is_within_legal_window(value: str | None, *, start: datetime, end: datetime) -> bool:
    """Validate a timestamp after the indexed coarse SQL window.

    A date-only legacy value is interpreted as midnight UTC. Invalid strings
    such as ``date_unavailable`` are never allowed to become active risk
    evidence merely because of lexical ordering.
    """
    raw = str(value or "").strip()
    if not raw:
        return False
    try:
        parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        try:
            parsed = datetime.strptime(raw, "%Y-%m-%d")
        except ValueError:
            return False
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return start < parsed.astimezone(timezone.utc) <= end


def load_active_legal_news(
    db: Any,
    symbols: Iterable[str],
    *,
    lookback_days: int = 90,
    now: datetime | None = None,
) -> dict[str, list[dict[str, Any]]]:
    """PART 17 — load persistent legal-flag news per symbol.

    Queries ``news_items`` for rows whose ``detected_symbols_json``
    contains any of ``symbols`` AND whose title hits at least one of
    the LEGAL_RISK_PATTERNS regexes. The query is bounded by
    ``lookback_days`` (default **90 days**) — long enough to catch
    a March-2026 SDNY indictment in a June-2026 review, short enough
    to expire stale flags after the typical legal resolution window.

    Returns ``{symbol_upper: [news_dict, ...]}``. Each news_dict has the
    same shape as the ``StockNewsHit`` dicts surfaced by
    ``CompanyNewsAgent`` so callers can drop them straight into
    ``detect_legal_risk``.

    No DB write. Read-only. Safe to call multiple times per cycle.
    """
    sym_set = {str(s).split("/")[0].upper() for s in (symbols or []) if s}
    if not sym_set:
        return {}

    # 1) Pull a wider window than the regular news pipeline so we don't
    #    drop legal flags behind the 200-row freshness ceiling. We
    #    intentionally use a generous limit and time-filter — the regex
    #    pre-filter happens server-side via LIKE for performance.
    legal_like = (
        "%indict%",
        "%SEC%",
        "%DOJ%",
        "%class action%",
        "%securities fraud%",
        "%accounting fraud%",
        # PART 17 — auditor / resignation patterns (LIKE is permissive;
        # the LEGAL_RISK_PATTERNS regex below is the source of truth).
        "%auditor resign%",
        "%auditor withdrew%",
        "%resigns as%",  # "X resigns as <company> auditor"
        "%resignation as%",
        # Auditor-firm names — only flagged when paired with a regex hit.
        "%ernst & young%",
        "%pricewaterhousecoopers%",
        "%pwc%",
        "%deloitte%",
        "%kpmg%",
        "%bdo%",
        "%going concern%",
        "%restatement%",
        "%material weakness%",
        "%delist%",
        "%export-control%",
        "%export control%",
        "%bankruptcy%",
        "%chapter 11%",
    )
    where_like = " OR ".join("LOWER(title) LIKE ?" for _ in legal_like)
    timestamped_sql = (
        "SELECT title, source, url, published_at, "
        "       detected_symbols_json, importance, asset_class "
        "FROM news_items "
        f"WHERE ({where_like}) "
        "  AND ("
        "    asset_class = 'stocks' OR detected_symbols_json IS NOT NULL"
        "  ) "
        "  AND published_at IS NOT NULL AND TRIM(published_at) <> '' "
        "  AND published_at > ? AND published_at < ? "
        "ORDER BY published_at DESC "
        "LIMIT 2000"
    )
    undated_sql = (
        "SELECT title, source, url, published_at, "
        "       detected_symbols_json, importance, asset_class "
        "FROM news_items "
        f"WHERE ({where_like}) "
        "  AND (asset_class = 'stocks' OR detected_symbols_json IS NOT NULL) "
        "  AND (published_at IS NULL OR TRIM(published_at) = '') "
        "ORDER BY id DESC LIMIT 2000"
    )
    like_params = [f"%{kw.strip('%').lower()}%" for kw in legal_like]
    reference = now or datetime.now(timezone.utc)
    if reference.tzinfo is None:
        reference = reference.replace(tzinfo=timezone.utc)
    reference = reference.astimezone(timezone.utc)
    cutoff = reference - timedelta(days=int(lookback_days))
    coarse_start = cutoff.date().isoformat()
    coarse_end = (reference.date() + timedelta(days=1)).isoformat()

    with db.connect() as conn:
        rows = list(conn.execute(timestamped_sql, [*like_params, coarse_start, coarse_end]))
        # Keep undated legacy legal reports fail-closed. There are very few in
        # production and they cannot turn a signal into an entry by themselves.
        rows.extend(conn.execute(undated_sql, like_params))

    # 2) Per row, intersect detected_symbols with the caller's symbol
    #    set, then verify the title actually matches a LEGAL_RISK pattern
    #    (the LIKE pre-filter is loose; the regexes are the source of
    #    truth used by detect_legal_risk).
    out: dict[str, list[dict[str, Any]]] = {s: [] for s in sym_set}
    for row in rows:
        # sqlite3.Row supports indexing by column name even after fetchall.
        try:
            title = (row["title"] or "")
            symbols_json = row["detected_symbols_json"] or "[]"
            source = row["source"] or ""
            url = row["url"] or ""
            published_at = row["published_at"] or ""
            importance = row["importance"]
        except Exception:
            # Plain-tuple fallback (older SQLite Row mode).
            title, source, url, published_at, symbols_json, importance = (
                row[0], row[1], row[2], row[3], row[4], row[5]
            )
        if published_at and not _is_within_legal_window(
            published_at, start=cutoff, end=reference
        ):
            continue
        try:
            detected = json.loads(symbols_json)
        except Exception:
            detected = []
        matched = {str(s).split("/")[0].upper() for s in detected} & sym_set
        if not matched:
            continue
        # Fail-closed regex check.
        has_legal_pattern = any(
            any(p.search(title) for p in _COMPILED[cat])
            for cat in LEGAL_RISK_PATTERNS
        )
        if not has_legal_pattern:
            continue
        hit = {
            "title": title,
            "source": source,
            "url": url,
            "published_at": published_at,
            "importance": importance,
        }
        for sym in matched:
            out[sym].append(hit)
    return out


def signal_has_legal_block(signal_row: dict[str, Any]) -> bool:
    """Return True iff the ``proposed_signals`` row carries an active
    legal-risk avoid_condition. Used by the stocks monitor to suppress
    Telegram dispatch for blocked A/B tiers.
    """

    raw = signal_row.get("no_entry_conditions_json")
    if not raw:
        return False
    try:
        items = json.loads(raw)
    except Exception:
        return False
    if not isinstance(items, list):
        return False
    return any(
        isinstance(it, str) and it.startswith(AVOID_CONDITION_MARKER) for it in items
    )
