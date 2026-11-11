"""Data models for proposed signals and their outcomes.

These dataclasses describe what we persist; the SQLite layer stores the same
fields in flat columns plus a JSON blob for the raw idea so we never lose
context. The signal_id is a deterministic hash, which lets us idempotently
re-register the same idea (and dedupe identical re-runs of a report).
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Iterable


# Lifecycle statuses (string constants; sqlite columns store as TEXT).
STATUS_GENERATED = "generated"
STATUS_WAITING = "waiting_for_entry"
STATUS_TRIGGERED = "triggered"
STATUS_TP1 = "tp1_hit"
STATUS_TP2 = "tp2_hit"
STATUS_TP3 = "tp3_hit"
STATUS_STOPPED = "stopped"
STATUS_INVALIDATED_BEFORE_ENTRY = "invalidated_before_entry"
STATUS_EXPIRED = "expired"
STATUS_MISSED_NO_ENTRY = "missed_no_entry"
STATUS_CANCELLED_REGIME = "cancelled_by_regime_change"
STATUS_CANCELLED_NEWS = "cancelled_by_news"
STATUS_AMBIGUOUS = "ambiguous"
STATUS_REVIEWED = "reviewed"

OPEN_STATUSES = frozenset(
    {
        STATUS_GENERATED,
        STATUS_WAITING,
        STATUS_TRIGGERED,
        STATUS_TP1,
        STATUS_TP2,
    }
)

# Final outcomes for the outcomes table.
OUTCOME_WIN = "win"
OUTCOME_LOSS = "loss"
OUTCOME_PARTIAL_WIN = "partial_win"
OUTCOME_EXPIRED = "expired"
OUTCOME_NOT_TRIGGERED = "not_triggered"
OUTCOME_MISSED = "missed"
OUTCOME_AMBIGUOUS = "ambiguous"


@dataclass
class ProposedSignal:
    """A snapshot of an A/B (optionally watchlist+trigger) idea we want to track."""

    signal_id: str
    created_at: str  # ISO UTC
    symbol: str
    direction: str  # long / short / watchlist
    mode: str  # scalp / intraday / swing / invest
    tier: str  # A / B / C
    score: float
    confidence: str
    data_confidence: str
    exchange_focus: str
    asset_class: str = "crypto"  # crypto / stocks
    listed_exchanges: list[str] = field(default_factory=list)
    primary_exchange: str = ""
    exchange_confirmation_type: str = "unknown"
    market_regime: str = ""
    weekend_mode_active: bool = False
    sector: str = ""
    narrative: str = ""
    setup_type: str = ""
    news_supported: bool = False
    telegram_supported: bool = False
    derivatives_supported: bool = False
    oi_context: str = ""
    funding_context: str = ""
    entry_type: str = "zone"  # zone / trigger / market / watchlist_trigger
    entry_low: float | None = None
    entry_high: float | None = None
    entry_trigger: float | None = None
    suggested_entry: float | None = None
    stop_loss: float | None = None
    invalidation: float | None = None
    tp1: float | None = None
    tp2: float | None = None
    tp3: float | None = None
    risk_per_unit: float | None = None
    expected_rr_tp1: float | None = None
    expected_rr_tp2: float | None = None
    expected_rr_tp3: float | None = None
    validity_window_hours: float = 24.0
    expires_at: str = ""  # ISO UTC
    thesis: str = ""
    counter_thesis: str = ""
    no_entry_conditions: list[str] = field(default_factory=list)
    source_report_path: str = ""
    source_context_path: str = ""
    report_id: str = ""
    raw_idea_json: str = "{}"
    status: str = STATUS_WAITING

    def to_row(self) -> dict[str, Any]:
        return {
            "signal_id": self.signal_id,
            "created_at": self.created_at,
            "updated_at": self.created_at,
            "symbol": self.symbol,
            "direction": self.direction,
            "mode": self.mode,
            "tier": self.tier,
            "score": float(self.score),
            "confidence": self.confidence,
            "data_confidence": self.data_confidence,
            "exchange_focus": self.exchange_focus,
            "asset_class": self.asset_class,
            "listed_exchanges_json": json.dumps(self.listed_exchanges),
            "primary_exchange": self.primary_exchange,
            "exchange_confirmation_type": self.exchange_confirmation_type,
            "market_regime": self.market_regime,
            "weekend_mode_active": 1 if self.weekend_mode_active else 0,
            "sector": self.sector,
            "narrative": self.narrative,
            "setup_type": self.setup_type,
            "news_supported": 1 if self.news_supported else 0,
            "telegram_supported": 1 if self.telegram_supported else 0,
            "derivatives_supported": 1 if self.derivatives_supported else 0,
            "oi_context": self.oi_context,
            "funding_context": self.funding_context,
            "entry_type": self.entry_type,
            "entry_low": self.entry_low,
            "entry_high": self.entry_high,
            "entry_trigger": self.entry_trigger,
            "suggested_entry": self.suggested_entry,
            "stop_loss": self.stop_loss,
            "invalidation": self.invalidation,
            "tp1": self.tp1,
            "tp2": self.tp2,
            "tp3": self.tp3,
            "risk_per_unit": self.risk_per_unit,
            "expected_rr_tp1": self.expected_rr_tp1,
            "expected_rr_tp2": self.expected_rr_tp2,
            "expected_rr_tp3": self.expected_rr_tp3,
            "validity_window_hours": float(self.validity_window_hours),
            "expires_at": self.expires_at,
            "thesis": self.thesis,
            "counter_thesis": self.counter_thesis,
            "no_entry_conditions_json": json.dumps(self.no_entry_conditions),
            "source_report_path": self.source_report_path,
            "source_context_path": self.source_context_path,
            "report_id": self.report_id,
            "raw_idea_json": self.raw_idea_json,
            "status": self.status,
        }


@dataclass
class SignalOutcome:
    signal_id: str
    checked_at: str
    status: str
    entry_triggered: bool = False
    entry_triggered_at: str | None = None
    entry_price_used: float | None = None
    stop_hit: bool = False
    stop_hit_at: str | None = None
    tp1_hit: bool = False
    tp1_hit_at: str | None = None
    tp2_hit: bool = False
    tp2_hit_at: str | None = None
    tp3_hit: bool = False
    tp3_hit_at: str | None = None
    max_favorable_excursion_pct: float | None = None
    max_adverse_excursion_pct: float | None = None
    max_favorable_excursion_r: float | None = None
    max_adverse_excursion_r: float | None = None
    final_r: float | None = None
    final_outcome: str | None = None
    notes: str = ""

    def to_row(self) -> dict[str, Any]:
        return {
            "signal_id": self.signal_id,
            "checked_at": self.checked_at,
            "status": self.status,
            "entry_triggered": 1 if self.entry_triggered else 0,
            "entry_triggered_at": self.entry_triggered_at,
            "entry_price_used": self.entry_price_used,
            "stop_hit": 1 if self.stop_hit else 0,
            "stop_hit_at": self.stop_hit_at,
            "tp1_hit": 1 if self.tp1_hit else 0,
            "tp1_hit_at": self.tp1_hit_at,
            "tp2_hit": 1 if self.tp2_hit else 0,
            "tp2_hit_at": self.tp2_hit_at,
            "tp3_hit": 1 if self.tp3_hit else 0,
            "tp3_hit_at": self.tp3_hit_at,
            "max_favorable_excursion_pct": self.max_favorable_excursion_pct,
            "max_adverse_excursion_pct": self.max_adverse_excursion_pct,
            "max_favorable_excursion_r": self.max_favorable_excursion_r,
            "max_adverse_excursion_r": self.max_adverse_excursion_r,
            "final_r": self.final_r,
            "final_outcome": self.final_outcome,
            "notes": self.notes,
        }


def signal_id_for(*, symbol: str, mode: str, direction: str, tier: str,
                  entry_low: float | None, entry_high: float | None,
                  invalidation: float | None, created_at: str,
                  report_id: str, strategy_identity: str = "") -> str:
    """Deterministic id — STABLE across cycles for the same setup on the same day.

    PART 10 (2026-06) fix. Pre-fix the hash included ``report_id`` (which
    rotated every cycle) and 10-digit-precision entry / SL floats (which
    micro-wobbled every cycle as fresh OHLCV recomputed ATR). The
    combination made every 2 h cycle mint a new ``signal_id`` for the
    same logical setup, inflating row counts ~5–15× for stocks intraday.

    Identity model (post-fix). A trade idea is identified by:

        symbol + mode + direction + tier + calendar_day

    Entry zone, invalidation, TPs, report_id, and HH:MM are all
    **trading metadata** that mutate as the system re-evaluates; they
    are not part of the trade's identity. The SQLite ``ON CONFLICT(
    signal_id) DO UPDATE`` path in ``upsert_proposed_signal`` then
    refreshes the latest entry/SL/TP onto the same row instead of
    creating a duplicate.

    Why include ``tier``? A C→B promotion materially changes alerting
    discipline (B is Telegram-eligible, C is watchlist-only) so we
    track them as distinct rows for honest performance attribution.
    Same setup demoted B→C on the next cycle similarly forks.

    Why include ``calendar_day``? So per-day outcome tracking still
    works — the same setup recurring on consecutive days is genuinely
    a different trade.

    The fix is forward-only. Historic duplicates in ``proposed_signals``
    stay as they are. The Obsidian dashboards already collapse by
    (symbol, mode, direction, day) so user-facing stats are honest now,
    and going forward the underlying table also stops duplicating.

    Function signature kept stable so existing callers compile without
    edits — the entry / SL / report_id / time-of-day parameters are
    simply ignored by the hash.
    """
    day_bucket = (created_at or "")[:10]
    parts = [
        symbol.upper(),
        mode.lower(),
        direction.lower(),
        tier.upper(),
        day_bucket,
    ]
    # Versioned Paper lanes need independent evidence. An empty identity keeps
    # every legacy signal id byte-for-byte stable.
    if strategy_identity:
        parts.append(str(strategy_identity).strip().lower())
    raw = "|".join(parts)
    digest = hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]
    return f"sig_{digest}"


def hash_iter(values: Iterable[Any]) -> str:
    return hashlib.sha1("|".join(str(v) for v in values).encode("utf-8")).hexdigest()[:12]
