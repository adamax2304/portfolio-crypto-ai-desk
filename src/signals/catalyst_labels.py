"""Display-only catalyst quality labels (catalyst safe-fix PART 3).

Computes diagnostic labels (freshness / strength / source / mapping /
derivatives) from a signal-shaped dict + its raw_idea_json + funding/OI
context strings. PURE / READ-ONLY — never mutates scoring, tier, or signal
rows. Used by the dashboard, journal, Telegram block, and packet.

All functions tolerate missing fields and never raise.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any


REPUTABLE = {
    "coindesk", "cointelegraph", "reuters", "bloomberg", "cnbc", "theblock",
    "the block", "marketwatch", "seeking alpha", "yahoo finance", "motley fool",
    "wsj", "financial times",
}
SOCIAL = {"t.me", "telegram", "twitter", "x.com", "reddit"}
OFFICIAL_HINTS = {"announcement", "binance", "bybit", "coinbase", "sec.gov", "official"}


@dataclass
class CatalystLabels:
    catalyst_freshness: str   # fresh / recent / old / none
    catalyst_strength: str    # strong / medium / weak / none
    source_quality: str       # official / reputable / social / unknown / none
    symbol_mapping: str       # exact / inferred / ambiguous / missing
    derivatives_label: str    # OI-up / funding-supportive / no-squeeze / squeeze-risk / missing / not-available
    headline_short: str       # short headline if available

    def as_dict(self) -> dict[str, str]:
        return asdict(self)

    def one_line(self) -> str:
        """Compact dashboard/journal stamp."""
        return (
            f"catalyst: {self.catalyst_freshness} · strength: {self.catalyst_strength} · "
            f"source: {self.source_quality} · map: {self.symbol_mapping} · "
            f"deriv: {self.derivatives_label}"
        )


def _age_hours(ts: Any, ref: datetime | None = None) -> float | None:
    if not ts:
        return None
    try:
        d = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
        if d.tzinfo is None:
            d = d.replace(tzinfo=timezone.utc)
    except Exception:
        return None
    now = ref or datetime.now(timezone.utc)
    return max(0.0, (now - d).total_seconds() / 3600.0)


def _freshness_label(age_h: float | None) -> str:
    if age_h is None:
        return "none"
    if age_h <= 1:
        return f"fresh({age_h:.1f}h)"
    if age_h <= 6:
        return f"recent({age_h:.1f}h)"
    return f"old({age_h:.1f}h)"


def _source_quality(source: str) -> str:
    s = (source or "").lower()
    if not s:
        return "unknown"
    if any(h in s for h in OFFICIAL_HINTS):
        return "official"
    if any(h in s for h in REPUTABLE):
        return "reputable"
    if any(h in s for h in SOCIAL):
        return "social"
    return "unknown"


def _derivatives_label(signal: dict[str, Any]) -> str:
    asset = (signal.get("asset_class") or "crypto").lower()
    if asset == "stocks":
        return "not-available"
    funding = (signal.get("funding_context") or "").lower()
    oi = (signal.get("oi_context") or "").lower()
    if not funding and not oi:
        return "missing"
    blob = funding + " " + oi
    # Treat explicit "no squeeze" / "crowding=normal" as benign, not risk.
    has_squeeze = ("squeeze" in blob or "crowded" in blob) and \
        "no squeeze" not in blob and "crowding=normal" not in blob
    if has_squeeze:
        return "squeeze-risk"
    if "oi up" in oi or "fresh positioning" in oi:
        return "OI-up"
    if "deleveraging" in oi or "short covering" in oi:
        return "funding-supportive"
    return "no-squeeze"


def compute_labels(signal: dict[str, Any], *, now: datetime | None = None) -> CatalystLabels:
    """Compute display labels from a proposed_signals-shaped dict.

    Reads (all optional): asset_class, news_supported, created_at,
    funding_context, oi_context, raw_idea_json (which may carry
    catalyst meta / news hits / importance).
    """
    asset = (signal.get("asset_class") or "crypto").lower()
    news_supported = bool(signal.get("news_supported"))

    # Parse raw_idea_json for catalyst meta / news hit details if present.
    raw = signal.get("raw_idea_json") or signal.get("raw") or {}
    if isinstance(raw, str):
        try:
            raw = json.loads(raw)
        except Exception:
            raw = {}
    if not isinstance(raw, dict):
        raw = {}

    catalyst_meta = raw.get("catalyst_meta") or {}
    cat_block = raw.get("catalyst") or {}
    cat_list = cat_block.get("catalysts") if isinstance(cat_block, dict) else None

    # Headline + source + published_at — prefer explicit meta, else first catalyst.
    headline = catalyst_meta.get("headline_short") or ""
    source = catalyst_meta.get("source") or ""
    published_at = catalyst_meta.get("published_at")
    available_at = catalyst_meta.get("available_at")
    latency_class = catalyst_meta.get("event_latency_class")
    importance = catalyst_meta.get("importance")

    if (not headline or not source) and isinstance(cat_list, list) and cat_list:
        first = cat_list[0] if isinstance(cat_list[0], dict) else {}
        headline = headline or str(first.get("headline") or first.get("title") or "")
        source = source or str(first.get("source") or "")
        published_at = published_at or first.get("published_at")
        available_at = available_at or first.get("available_at")
        latency_class = latency_class or first.get("event_latency_class")
        if importance is None:
            importance = first.get("importance")

    # Freshness
    if not news_supported:
        freshness = "none"
    elif latency_class:
        # The class is fixed when this desk first saw the news. A delayed RSS
        # row therefore cannot label itself as an intraday fresh catalyst.
        freshness = str(latency_class)
    else:
        age = _age_hours(published_at, now) if published_at else None
        # Fallback: if no published_at but news_supported, mark recent (unknown age).
        freshness = _freshness_label(age) if age is not None else "recent(?)"

    # Strength from importance score, else from presence.
    if not news_supported:
        strength = "none"
    else:
        try:
            imp = float(importance) if importance is not None else None
        except (TypeError, ValueError):
            imp = None
        if imp is None:
            strength = "medium"
        elif imp >= 7:
            strength = "strong"
        elif imp >= 4:
            strength = "medium"
        else:
            strength = "weak"

    # Source quality
    src_q = _source_quality(source) if news_supported else "none"

    # Symbol mapping confidence
    if not news_supported:
        mapping = "missing"
    else:
        mode = catalyst_meta.get("mapping")
        mapping = mode or "exact"  # default: detected_symbols_json is exact

    deriv = _derivatives_label(signal)

    return CatalystLabels(
        catalyst_freshness=freshness,
        catalyst_strength=strength,
        source_quality=src_q,
        symbol_mapping=mapping,
        derivatives_label=deriv,
        headline_short=(headline or "")[:80],
    )


def move_type(signal: dict[str, Any], labels: CatalystLabels | None = None) -> str:
    """Telegram 'Move type' line: catalyst-backed / technical momentum / chase risk."""
    labels = labels or compute_labels(signal)
    if bool(signal.get("news_supported")) and labels.catalyst_freshness != "none":
        return "catalyst-backed"
    # chase risk if flagged in the signal's cap reasons / notes
    raw = signal.get("raw_idea_json") or ""
    if isinstance(raw, str) and ("2 ATR" in raw or "chase" in raw.lower()):
        return "chase risk"
    return "technical momentum"


def telegram_block(
    signal: dict[str, Any], *, now: datetime | None = None,
    derivatives_snapshot: dict[str, Any] | None = None,
) -> list[str]:
    """Compact catalyst plus explicit funding/OI block for Telegram."""
    labels = compute_labels(signal, now=now)
    asset = (signal.get("asset_class") or "crypto").lower()
    # Line 1 — Catalyst
    if not bool(signal.get("news_supported")):
        cat_line = "Catalyst: none"
    else:
        src = labels.source_quality if labels.source_quality not in ("none", "unknown") else "news"
        hl = f" — {labels.headline_short}" if labels.headline_short else ""
        cat_line = f"Catalyst: {labels.catalyst_freshness} {src}{hl}".rstrip()
    # Line 2 — Funding/OI
    if asset == "stocks":
        fo_line = "Funding/OI: not available for stocks"
    elif labels.derivatives_label == "missing":
        fo_line = "Funding/OI: missing"
    elif labels.derivatives_label == "squeeze-risk":
        fo_line = "Funding/OI: conflicting (squeeze risk)"
    else:
        fo_line = f"Funding/OI: confirmed ({labels.derivatives_label})"

    # Values come from the read-only multi-venue archive at send time. This
    # keeps Telegram useful even if a signal predates its first refresh.
    try:
        from src.notifiers.derivatives_context import telegram_lines
        deriv_lines, _ = telegram_lines(
            signal, now=now, snapshot=derivatives_snapshot,
        )
    except Exception:
        deriv_lines = [fo_line]
    # Line 3 — Move type
    mv_line = f"Move type: {move_type(signal, labels)}"
    return [cat_line, *deriv_lines, mv_line]
