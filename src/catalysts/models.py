"""Dataclasses for the catalyst / narrative layer.

CatalystEvent
    A single structured catalyst record derived from a news_items row
    (or, in tests, a fixture dict).
NarrativeBasket
    A cluster of related symbols sharing a catalyst theme (e.g. BNB +
    ASTER on the GENIUS HODLer airdrop, HEI + PSG + NFP on
    delisting / thin liquidity, HYPE on Hyperliquid / perps).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


# Structured catalyst categories per Sprint spec PART 3.
CATALYST_TYPES: tuple[str, ...] = (
    "official_product_teaser",
    "product_launch",
    "exchange_listing",
    "exchange_delisting",
    "margin_delisting",
    "airdrop",
    "hodler_airdrop",
    "buyback_burn",
    "token_unlock",
    "roadmap_event",
    "mainnet_launch",
    "regulatory_sector_headline",
    "platform_growth",
    "social_narrative",
    "partnership",
    "legal_risk",
    "exploit_hack",
    "rumour_only",
    "low_liquidity_event",
    "sell_the_news_risk",
    # PART 5 fix — additional categories for richer narrative coverage.
    "governance_event",     # DAO vote outcome, foundation actions, treasury vote
    "infrastructure_failure",  # mainnet halt, outage, congestion (severe form of low_liquidity)
    "momentum_breakout",    # auto-tagged by basket builder for top movers without news
    # PART 6 fix — stocks-specific catalyst categories.
    "earnings_event",       # Q1/Q2 earnings reports, beats/misses, guidance updates
    "analyst_action",       # upgrades/downgrades, price target changes, initiations
    "clinical_milestone",   # FDA approval, Phase 3, biotech catalysts
    "insider_activity",     # insider buying / selling, 10b5-1 plans
    # Fallback when no specific category matches.
    "other_news",
)


# Suggested playbooks per Sprint spec PART 4.
PLAYBOOKS: tuple[str, ...] = (
    "early_breakout",
    "breakout_retest",
    "related_beta_rotation",
    "wait_pullback",
    "sell_the_news_watch",
    "avoid_chase",
    "avoid_low_liquidity",
    "no_trade",
)


def _iso_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")


@dataclass
class CatalystEvent:
    """A single classified catalyst record.

    Mirrors the field list in Sprint spec PART 3.
    """

    catalyst_id: str
    asset_class: str  # "crypto" | "stocks"
    symbol: str  # primary symbol; empty string when basket-level only
    related_symbols: list[str] = field(default_factory=list)
    catalyst_type: str = "other_news"
    source: str = ""
    source_quality: str = "single_source"  # primary_source / single_source / social_only / unverifiable
    title: str = ""
    url: str = ""
    timestamp: str | None = None  # original news publish time, ISO-8601
    collected_at: str = field(default_factory=_iso_now)
    freshness_hours: float | None = None
    narrative: str = ""  # short keyword tag
    confidence: str = "low"  # high / medium / low
    importance: float = 0.0  # normalized [0,1] prioritization score (see classifier.score_importance)
    expected_time_window: str = "unknown"  # "intraday" / "24-72h" / "weeks" / "unknown"
    price_reaction_so_far: str = "unknown"  # "priced_in" / "early" / "extended" / "unknown"
    volume_confirmation: str = "unknown"  # "confirmed" / "weak" / "unknown"
    overextension_risk: bool = False
    low_liquidity_risk: bool = False
    sell_the_news_risk: bool = False
    confirms_internal_signal: str = "unclear"  # "yes" / "no" / "unclear"
    contradicts_internal_signal: str = "unclear"
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "catalyst_id": self.catalyst_id,
            "asset_class": self.asset_class,
            "symbol": self.symbol,
            "related_symbols": list(self.related_symbols),
            "catalyst_type": self.catalyst_type,
            "source": self.source,
            "source_quality": self.source_quality,
            "title": self.title,
            "url": self.url,
            "timestamp": self.timestamp,
            "collected_at": self.collected_at,
            "freshness_hours": self.freshness_hours,
            "narrative": self.narrative,
            "confidence": self.confidence,
            "importance": self.importance,
            "expected_time_window": self.expected_time_window,
            "price_reaction_so_far": self.price_reaction_so_far,
            "volume_confirmation": self.volume_confirmation,
            "overextension_risk": self.overextension_risk,
            "low_liquidity_risk": self.low_liquidity_risk,
            "sell_the_news_risk": self.sell_the_news_risk,
            "confirms_internal_signal": self.confirms_internal_signal,
            "contradicts_internal_signal": self.contradicts_internal_signal,
            "notes": self.notes,
        }


@dataclass
class NarrativeBasket:
    """A cluster of related symbols sharing a catalyst theme."""

    basket_name: str
    primary_symbols: list[str] = field(default_factory=list)
    related_symbols: list[str] = field(default_factory=list)
    catalyst_summary: str = ""
    source_quality: str = "single_source"
    freshness: str = "unknown"  # short string: "<1h" / "<6h" / "stale"
    symbols_moved: list[str] = field(default_factory=list)
    symbols_lagging: list[str] = field(default_factory=list)
    symbols_overextended: list[str] = field(default_factory=list)
    symbols_blocked: list[str] = field(default_factory=list)
    suggested_playbook: str = "wait_pullback"
    event_ids: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=_iso_now)

    def to_dict(self) -> dict[str, Any]:
        return {
            "basket_name": self.basket_name,
            "primary_symbols": list(self.primary_symbols),
            "related_symbols": list(self.related_symbols),
            "catalyst_summary": self.catalyst_summary,
            "source_quality": self.source_quality,
            "freshness": self.freshness,
            "symbols_moved": list(self.symbols_moved),
            "symbols_lagging": list(self.symbols_lagging),
            "symbols_overextended": list(self.symbols_overextended),
            "symbols_blocked": list(self.symbols_blocked),
            "suggested_playbook": self.suggested_playbook,
            "event_ids": list(self.event_ids),
            "created_at": self.created_at,
        }
