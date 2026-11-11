"""Catalyst / narrative enrichment layer.

This package adds **structured** catalyst classification + narrative
basket clustering on top of the existing `news_items` + `events` tables.
It does NOT fetch new data — it reads what the RSS / news_trader bridge
pipeline already collected, classifies it, clusters related events into
baskets, and persists JSONL for the scheduler / enriched-review skill /
report builder to consume.

Public API:
* :class:`CatalystEvent`, :class:`NarrativeBasket` — dataclasses
* :func:`collect_catalysts` — top-level entry point used by the
  ``catalyst-scan`` CLI command and the default scheduler.
* :func:`classify_catalyst_type` — pure classifier (regex-based).
* :func:`build_narrative_baskets` — clustering.

Safety:
* No auto-trade.
* No scoring changes.
* No LLM auto-invocation.
* Read-only with respect to `news_items` / `events`; writes only to
  `data/catalysts/<YYYY-MM-DD>/`.
"""

from src.catalysts.models import (
    CATALYST_TYPES,
    PLAYBOOKS,
    CatalystEvent,
    NarrativeBasket,
)
from src.catalysts.classifier import (
    classify_catalyst_type,
    classify_source_quality,
    detect_low_liquidity_risk,
    detect_rumour_marker,
    detect_geopolitical_severity,
    score_importance,
)
from src.catalysts.baskets import build_narrative_baskets, build_momentum_breakout_basket
from src.catalysts.collector import collect_catalysts, CatalystScanResult
from src.catalysts.entity_aliases import EntityAliasMatcher, get_matcher

__all__ = [
    "CATALYST_TYPES",
    "PLAYBOOKS",
    "CatalystEvent",
    "NarrativeBasket",
    "CatalystScanResult",
    "EntityAliasMatcher",
    "get_matcher",
    "classify_catalyst_type",
    "classify_source_quality",
    "detect_low_liquidity_risk",
    "detect_rumour_marker",
    "detect_geopolitical_severity",
    "score_importance",
    "build_narrative_baskets",
    "build_momentum_breakout_basket",
    "collect_catalysts",
]
