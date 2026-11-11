from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


class AgentEnvelope(BaseModel):
    agent_name: str
    generated_at: str = Field(default_factory=utc_now_iso)
    data: dict[str, Any] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)


class MarketRegime(BaseModel):
    label: str
    confidence: float
    risk_mode: str
    recommended_style: str
    btc_trend: str
    eth_trend: str
    alt_breadth: dict[str, float]
    volatility: dict[str, float | str]
    key_levels: dict[str, dict[str, float]]
    explanation: str
    warnings: list[str] = Field(default_factory=list)


class MomentumCandidate(BaseModel):
    symbol: str
    direction_bias: Literal["long", "short", "watch"]
    score: float
    rank: int = 0
    return_24h: float | None = None
    return_7d: float | None = None
    relative_strength_btc: float | None = None
    relative_strength_eth: float | None = None
    volume_ratio: float | None = None
    atr_percentile: float | None = None
    distance_from_ema20_atr: float | None = None
    reason_tags: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    # PART 22 — short squeeze-risk diagnostics (populated by MomentumScannerAgent
    # when OHLCV is available; consumed by the short squeeze guard).
    return_1h: float | None = None
    quote_volume_24h_usd: float | None = None
    upper_wick_atr_max: float | None = None
    upper_wick_atr_avg: float | None = None


class TechnicalSetup(BaseModel):
    symbol: str
    direction: Literal["long", "short", "watchlist_only", "no_trade"]
    timeframe: str
    current_price: float
    entry_low: float | None = None
    entry_high: float | None = None
    invalidation: float | None = None
    tp1: float | None = None
    tp2: float | None = None
    tp3: float | None = None
    atr: float | None = None
    rr_to_tp1: float | None = None
    setup_quality: float = 0.0
    trend: str = "unknown"
    support: float | None = None
    resistance: float | None = None
    stop_source: str = ""
    stop_model: str = ""
    stop_contract: dict[str, Any] = Field(default_factory=dict)
    candidate_structural_stop_contract: dict[str, Any] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)


class ScoreBreakdown(BaseModel):
    final_score: float
    confidence: str
    data_quality: str
    tier: Literal["A", "B", "C", "rejected"] = "C"
    components: dict[str, float]
    risk_penalty: float
    score_cap: float | None = None
    cap_reasons: list[str] = Field(default_factory=list)
    reasons: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class ExchangeConfirmation(BaseModel):
    symbol: str
    exchanges_listed: list[str] = Field(default_factory=list)
    anchor_listed: bool = False
    derivatives_listed: bool = False
    discovery_listed: bool = False
    high_risk_only: bool = False
    price_consistency: float = 0.0
    volume_consistency: float = 0.0
    confirmation_score: float = 0.0
    best_exchange_for_data: str = ""
    suggested_exchange_focus: str = ""
    risk_flags: list[str] = Field(default_factory=list)
    interpretation: str = "no cross-exchange context"


class RejectedIdea(BaseModel):
    symbol: str
    tier: str = "rejected"
    score: float = 0.0
    direction_bias: str = "watch"
    primary_reason: str = "no setup"
    reasons: list[str] = Field(default_factory=list)
    exchanges: list[str] = Field(default_factory=list)
    risk_flags: list[str] = Field(default_factory=list)


class DerivativesSummary(BaseModel):
    symbol: str
    data_available: bool
    funding_rate: float | None = None
    open_interest: float | None = None
    open_interest_value: float | None = None
    oi_change_pct: float | None = None
    price_change_pct: float | None = None
    long_short_ratio: float | None = None
    interpretation: str = "data unavailable"
    crowding_risk: str = "unknown"
    squeeze_potential: str = "unknown"
    alignment_score: float = 0.0
    warnings: list[str] = Field(default_factory=list)


class NewsItem(BaseModel):
    title: str
    source: str
    url: str
    published_at: str | None = None
    # Preserve the text that was actually available at ingest time.  The
    # resolver can then recover entities that are mentioned only in an RSS
    # description or Telegram message body.
    content: str | None = None
    summary: str | None = None
    ingested_at: str | None = None
    first_seen_at: str | None = None
    # Time at which this desk first observed the item. This is distinct from
    # the publisher timestamp: delayed editorial news is context, not a new
    # intraday catalyst.
    available_at: str | None = None
    event_latency_class: str | None = None
    source_observation_delay_seconds: float | None = None
    content_hash: str | None = None
    source_message_id: str | None = None
    source_channel_id: str | None = None
    source_category: str | None = None
    # Structured request context from symbol-scoped provider endpoints.
    # This is provenance, not a score or a trading recommendation.
    provider_symbols: list[str] = Field(default_factory=list)
    provider_symbol_provenance: str | None = None
    detected_symbols: list[str] = Field(default_factory=list)
    detected_narratives: list[str] = Field(default_factory=list)
    importance: float = 1.0
    verification_status: str = "single_source"


class CatalystSummary(BaseModel):
    symbol: str
    catalysts: list[str] = Field(default_factory=list)
    risk_events: list[str] = Field(default_factory=list)
    importance_score: float = 0.0
    interpretation: str = "no fresh catalyst detected"
    verification_status: str = "none"
    warnings: list[str] = Field(default_factory=list)


class RiskAssessment(BaseModel):
    symbol: str
    risk_score: float
    risk_level: str
    warnings: list[str] = Field(default_factory=list)
    reasons_to_avoid: list[str] = Field(default_factory=list)
    valid_if: list[str] = Field(default_factory=list)


class NarrativeSummary(BaseModel):
    narrative: str
    attention_score: float = 0.0
    momentum_score: float = 0.0
    volume_score: float = 0.0
    risk_score: float = 0.0
    heat_score: float = 0.0
    representative_symbols: list[str] = Field(default_factory=list)
    status: str = "quiet"
    evidence: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class MacroGeopoliticsSummary(BaseModel):
    risk_score: float = 0.0
    btc_bias: str = "neutral"
    themes: list[str] = Field(default_factory=list)
    headlines: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    explanation: str = "No macro/geopolitical signal detected."


class SocialAttentionSummary(BaseModel):
    symbol: str
    mention_count: int = 0
    attention_score: float = 0.0
    sources: list[str] = Field(default_factory=list)
    top_mentions: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class CrowdWatchSummary(BaseModel):
    signal_count: int = 0
    configured_sources: list[str] = Field(default_factory=list)
    active_signals: list[str] = Field(default_factory=list)
    symbols: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class MultiExchangeDerivativesSummary(BaseModel):
    symbol: str
    exchanges_available: list[str] = Field(default_factory=list)
    funding_rates: dict[str, float] = Field(default_factory=dict)
    open_interest_values: dict[str, float] = Field(default_factory=dict)
    consensus: str = "no external derivatives confirmation"
    crowding_risk: str = "unknown"
    warnings: list[str] = Field(default_factory=list)


class CoverageAudit(BaseModel):
    source_health: dict[str, str] = Field(default_factory=dict)
    missing_sources: list[str] = Field(default_factory=list)
    stale_or_partial_sources: list[str] = Field(default_factory=list)
    important_blindspots: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class Critique(BaseModel):
    symbol: str
    counter_thesis: str
    contradictions: list[str] = Field(default_factory=list)
    late_or_crowded: bool = False
    weak_signal_dependency: bool = False
    verdict: str = "needs confirmation"


class TradeIdea(BaseModel):
    symbol: str
    direction: Literal["long", "short", "watchlist only", "no trade"]
    score: float
    confidence: str
    risk_level: str
    timeframe: str
    tier: Literal["A", "B", "C", "rejected"] = "C"
    mode: Literal["scalp", "intraday", "swing", "invest"] = "intraday"
    asset_class: Literal["crypto", "stocks"] = "crypto"
    exchange_focus: str = ""
    exchanges_confirmed: list[str] = Field(default_factory=list)
    data_confidence: str = "medium"
    thesis: str
    evidence: list[str]
    counterarguments: list[str]
    entry_plan: str
    invalidation: str
    targets: list[str]
    what_to_monitor: list[str]
    avoid_conditions: list[str]
    data_sources_used: list[str]
    cap_reasons: list[str] = Field(default_factory=list)
    status: str = "open"
    raw: dict[str, Any] = Field(default_factory=dict)


class CrowdAttention(BaseModel):
    symbol: str
    stage: Literal[
        "silent",
        "early_attention",
        "growing_hype",
        "euphoria",
        "exhaustion",
        "fear_capitulation",
        "rumor_driven",
        "unknown",
    ] = "unknown"
    attention_score: float = 0.0
    momentum_score: float = 0.0
    crowding_risk: float = 0.0
    confidence: str = "low"
    evidence: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
