"""Compute performance metrics over recorded signals + their outcomes.

All metrics are R-based, so they're comparable across symbols and price levels.
Sample sizes are explicit on every metric block — small samples produce
"low_confidence" observations, not strong recommendations. This module never
edits configuration; it only reports.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any, Iterable

from src.signals.config import SignalTrackingConfig
from src.signals.models import (
    OPEN_STATUSES,
    OUTCOME_AMBIGUOUS,
    OUTCOME_EXPIRED,
    OUTCOME_LOSS,
    OUTCOME_NOT_TRIGGERED,
    OUTCOME_WIN,
    STATUS_AMBIGUOUS,
    STATUS_EXPIRED,
    STATUS_MISSED_NO_ENTRY,
    STATUS_STOPPED,
    STATUS_TP1,
    STATUS_TP2,
    STATUS_TP3,
    STATUS_TRIGGERED,
    STATUS_WAITING,
)
from src.storage.sqlite import SQLiteStore


# Period names → window length in hours. Used by signal-stats and reviews.
PERIOD_HOURS: dict[str, float | None] = {
    "today": 24,
    "week": 24 * 7,
    "month": 24 * 30,
    "all": None,
}


@dataclass
class MetricBucket:
    """One row of metrics for a slice of signals."""

    label: str
    total_signals: int = 0
    triggered: int = 0
    not_triggered: int = 0
    expired_in_position: int = 0
    wins: int = 0
    losses: int = 0
    ambiguous: int = 0
    tp1_hits: int = 0
    tp2_hits: int = 0
    tp3_hits: int = 0
    stop_hits: int = 0
    # R aggregates are built from the AUTHORITATIVE paper-execution R (Model F), NOT the legacy
    # touch `final_r`. `sum_legacy_touch_r` keeps the old touch total as a labelled diagnostic only.
    sum_r: float = 0.0
    sum_positive_r: float = 0.0
    sum_negative_r_abs: float = 0.0
    paper_resolved: int = 0
    sum_legacy_touch_r: float = 0.0
    mfe_r_total: float = 0.0
    mfe_r_count: int = 0
    mae_r_total: float = 0.0
    mae_r_count: int = 0
    time_to_entry_minutes_total: float = 0.0
    time_to_entry_count: int = 0

    def as_summary(self, *, min_sample: int) -> dict[str, Any]:
        triggered = max(self.triggered, 0)
        winrate = (self.wins / triggered) if triggered else None
        capture_rate = (self.triggered / self.total_signals) if self.total_signals else None
        tp1_rate = (self.tp1_hits / triggered) if triggered else None
        stop_rate = (self.stop_hits / triggered) if triggered else None
        # avg / total R are the honest paper-execution R (Model F), averaged over the trades that
        # actually resolved a paper R (paper_resolved), NOT the touch-based final_r.
        avg_r = (self.sum_r / self.paper_resolved) if self.paper_resolved else None
        pf = None
        if self.sum_negative_r_abs > 0:
            pf = self.sum_positive_r / self.sum_negative_r_abs
        elif self.sum_positive_r > 0:
            pf = float("inf")
        avg_mfe = (self.mfe_r_total / self.mfe_r_count) if self.mfe_r_count else None
        avg_mae = (self.mae_r_total / self.mae_r_count) if self.mae_r_count else None
        avg_ttf = (
            (self.time_to_entry_minutes_total / self.time_to_entry_count)
            if self.time_to_entry_count
            else None
        )
        return {
            "label": self.label,
            "sample_size": self.total_signals,
            "confidence_level": confidence_for_sample(self.total_signals, min_sample),
            "triggered": self.triggered,
            "not_triggered": self.not_triggered,
            "expired_in_position": self.expired_in_position,
            "ambiguous": self.ambiguous,
            "wins": self.wins,
            "losses": self.losses,
            "tp1_hits": self.tp1_hits,
            "tp2_hits": self.tp2_hits,
            "tp3_hits": self.tp3_hits,
            "stop_hits": self.stop_hits,
            "winrate_triggered": _round(winrate),
            "capture_rate": _round(capture_rate),
            "tp1_rate": _round(tp1_rate),
            "stop_rate": _round(stop_rate),
            # authoritative paper R (Model F). USD net (paper_portfolio_ledger) is the authoritative
            # profitability; these R fields are the auxiliary paper-R diagnostics.
            "average_r": _round(avg_r),
            "total_r": _round(self.sum_r),
            "profit_factor": _round(pf),
            "paper_resolved": self.paper_resolved,
            "risk_model": "early_mfe_protection_v1",
            # LEGACY touch metric (old final_r, highest-TP-touched) — optimistic, NOT PnL, never
            # summed as profit. Surfaced only for the touch-vs-paper diagnostic.
            "legacy_touch_total_r": _round(self.sum_legacy_touch_r),
            "average_mfe_r": _round(avg_mfe),
            "average_mae_r": _round(avg_mae),
            "average_time_to_entry_min": _round(avg_ttf),
        }


def _round(value: float | None) -> float | None:
    if value is None:
        return None
    try:
        if value == float("inf") or value == float("-inf"):
            return value
        return round(float(value), 4)
    except (TypeError, ValueError):
        return None


def confidence_for_sample(sample: int, min_for_rec: int) -> str:
    """Map sample size to a label. Aligned with the spec's sample-size rule."""

    if sample < 10:
        return "anecdotal"
    if sample < 30:
        return "weak"
    if sample < min_for_rec:
        return "moderate"
    if sample < 100:
        return "stronger"
    return "reliable"


def _iso_window_start(hours: float | None) -> str | None:
    if hours is None:
        return None
    return (datetime.now(timezone.utc) - timedelta(hours=hours)).strftime(
        "%Y-%m-%dT%H:%M:%S+00:00"
    )


def _final_outcome_from_status(status: str, outcome: dict[str, Any] | None) -> str:
    if outcome and outcome.get("final_outcome"):
        return str(outcome["final_outcome"])
    if status == STATUS_STOPPED:
        return OUTCOME_LOSS
    if status in (STATUS_TP1, STATUS_TP2, STATUS_TP3):
        return OUTCOME_WIN
    if status == STATUS_MISSED_NO_ENTRY:
        return OUTCOME_NOT_TRIGGERED
    if status == STATUS_EXPIRED:
        return OUTCOME_EXPIRED
    if status == STATUS_AMBIGUOUS:
        return OUTCOME_AMBIGUOUS
    return ""


def _time_to_entry_minutes(signal: dict[str, Any], outcome: dict[str, Any] | None) -> float | None:
    if not outcome or not outcome.get("entry_triggered_at"):
        return None
    try:
        from datetime import datetime as _dt
        created = _dt.fromisoformat(str(signal["created_at"]).replace("Z", "+00:00"))
        triggered = _dt.fromisoformat(str(outcome["entry_triggered_at"]).replace("Z", "+00:00"))
        delta = triggered - created
        return max(delta.total_seconds() / 60.0, 0.0)
    except Exception:
        return None


def collect(
    store: SQLiteStore,
    *,
    config: SignalTrackingConfig,
    period: str = "all",
    mode: str | None = None,
    tier: str | None = None,
    direction: str | None = None,
    weekend_mode: bool | None = None,
    asset_class: str | None = None,
    extra_filter=None,
) -> tuple[MetricBucket, list[dict[str, Any]]]:
    """Return (overall_bucket, raw_signal_rows) for the requested slice."""

    since = _iso_window_start(PERIOD_HOURS.get(period))
    rows = store.load_signals_for_period(
        since=since,
        mode=mode,
        tier=tier,
        direction=direction,
        asset_class=asset_class,
    )
    if weekend_mode is not None:
        rows = [r for r in rows if bool(r.get("weekend_mode_active")) == weekend_mode]
    if extra_filter is not None:
        rows = [r for r in rows if extra_filter(r)]

    bucket = MetricBucket(label=_describe_label(period, mode, tier, direction, weekend_mode))
    for row in rows:
        outcome = store.load_latest_outcome(row["signal_id"])
        _accumulate(bucket, row, outcome)
    return bucket, rows


def _describe_label(
    period: str,
    mode: str | None,
    tier: str | None,
    direction: str | None,
    weekend_mode: bool | None,
) -> str:
    parts = [period]
    if tier:
        parts.append(f"tier={tier}")
    if mode:
        parts.append(f"mode={mode}")
    if direction:
        parts.append(f"dir={direction}")
    if weekend_mode is True:
        parts.append("weekend")
    elif weekend_mode is False:
        parts.append("weekday")
    return " / ".join(parts)


def _ff(v: Any) -> float | None:
    try:
        return None if v in (None, "") else float(v)
    except (TypeError, ValueError):
        return None


def _paper_execution_r(signal: dict[str, Any], outcome: dict[str, Any] | None,
                       triggered: bool) -> float | None:
    """Honest paper-execution R (Model F) for ONE trade, reconstructed from its recorded path.
    Returns None when the trade never entered / is still open. NEVER uses `final_r` as the PnL —
    this is the authoritative paper-R the stats/report/PF headline is built from."""
    if not outcome or not triggered:
        return None
    try:
        from src.execution.paper_execution_accounting import compute_paper_execution
        entry = _ff(signal.get("entry_trigger")) or _ff(signal.get("suggested_entry")) \
            or _ff(signal.get("entry_low"))
        stop = _ff(signal.get("invalidation")) or _ff(signal.get("stop_loss"))
        fo = str(outcome.get("final_outcome") or "").lower()
        rec = compute_paper_execution(
            direction=str(signal.get("direction") or "long"), entry=entry, stop=stop,
            tp1=_ff(signal.get("tp1")), tp2=_ff(signal.get("tp2")), tp3=_ff(signal.get("tp3")),
            reached_tp1=bool(outcome.get("tp1_hit")), reached_tp2=bool(outcome.get("tp2_hit")),
            reached_tp3=bool(outcome.get("tp3_hit")), hit_stop=bool(outcome.get("stop_hit")),
            expired=(fo == "expired"), entered=True,
            mfe_r=_ff(outcome.get("max_favorable_excursion_r")))
        return rec.get("paper_execution_r")
    except Exception:
        return None


def _accumulate(bucket: MetricBucket, signal: dict[str, Any],
                outcome: dict[str, Any] | None) -> None:
    bucket.total_signals += 1
    status = str(signal.get("status") or "")
    triggered = False
    if outcome and outcome.get("entry_triggered"):
        triggered = True
    elif status not in (STATUS_WAITING, STATUS_MISSED_NO_ENTRY):
        triggered = status not in OPEN_STATUSES or status in (STATUS_TP1, STATUS_TP2, STATUS_TP3, STATUS_TRIGGERED)
    if triggered:
        bucket.triggered += 1
    elif status == STATUS_MISSED_NO_ENTRY:
        bucket.not_triggered += 1
    elif status == STATUS_EXPIRED:
        bucket.expired_in_position += 1

    if outcome:
        if outcome.get("tp1_hit"):
            bucket.tp1_hits += 1
        if outcome.get("tp2_hit"):
            bucket.tp2_hits += 1
        if outcome.get("tp3_hit"):
            bucket.tp3_hits += 1
        if outcome.get("stop_hit"):
            bucket.stop_hits += 1

        # LEGACY touch total (diagnostic only) — kept separate, NEVER the profitability R.
        final_r = outcome.get("final_r")
        if isinstance(final_r, (int, float)) and triggered:
            bucket.sum_legacy_touch_r += float(final_r)
        # AUTHORITATIVE R = paper-execution R (Model F), summed only over resolved paper trades.
        pe_r = _paper_execution_r(signal, outcome, triggered)
        if pe_r is not None:
            bucket.paper_resolved += 1
            bucket.sum_r += pe_r
            if pe_r > 0:
                bucket.sum_positive_r += pe_r
            elif pe_r < 0:
                bucket.sum_negative_r_abs += abs(pe_r)

        final_outcome = _final_outcome_from_status(status, outcome)
        if triggered:
            if final_outcome == OUTCOME_WIN:
                bucket.wins += 1
            elif final_outcome == OUTCOME_LOSS:
                bucket.losses += 1
            elif final_outcome == OUTCOME_AMBIGUOUS:
                bucket.ambiguous += 1

        mfe_r = outcome.get("max_favorable_excursion_r")
        mae_r = outcome.get("max_adverse_excursion_r")
        if isinstance(mfe_r, (int, float)):
            bucket.mfe_r_total += float(mfe_r)
            bucket.mfe_r_count += 1
        if isinstance(mae_r, (int, float)):
            bucket.mae_r_total += float(mae_r)
            bucket.mae_r_count += 1

        ttf = _time_to_entry_minutes(signal, outcome)
        if ttf is not None:
            bucket.time_to_entry_minutes_total += ttf
            bucket.time_to_entry_count += 1


@dataclass
class BreakdownReport:
    overall: dict[str, Any]
    by_tier: list[dict[str, Any]] = field(default_factory=list)
    by_mode: list[dict[str, Any]] = field(default_factory=list)
    by_direction: list[dict[str, Any]] = field(default_factory=list)
    by_exchange_confirmation: list[dict[str, Any]] = field(default_factory=list)
    by_weekend_mode: list[dict[str, Any]] = field(default_factory=list)
    by_sector: list[dict[str, Any]] = field(default_factory=list)
    by_narrative: list[dict[str, Any]] = field(default_factory=list)
    by_setup: list[dict[str, Any]] = field(default_factory=list)
    sample_size: int = 0


def compute_breakdowns(
    store: SQLiteStore,
    *,
    config: SignalTrackingConfig,
    period: str = "all",
    mode: str | None = None,
    tier: str | None = None,
    direction: str | None = None,
    weekend_mode: bool | None = None,
    asset_class: str | None = None,
) -> BreakdownReport:
    overall, rows = collect(
        store,
        config=config,
        period=period,
        mode=mode,
        tier=tier,
        direction=direction,
        weekend_mode=weekend_mode,
        asset_class=asset_class,
    )
    min_sample = config.minimum_sample_for_recommendations

    def _summary_for(extra: dict[str, Any]) -> list[dict[str, Any]]:
        groups: dict[str, MetricBucket] = {}
        for row in rows:
            key = str(extra["key_fn"](row) or "(unknown)")
            bucket = groups.setdefault(key, MetricBucket(label=f"{extra['label']}={key}"))
            outcome = store.load_latest_outcome(row["signal_id"])
            _accumulate(bucket, row, outcome)
        return [b.as_summary(min_sample=min_sample) for b in groups.values() if b.total_signals]

    report = BreakdownReport(
        overall=overall.as_summary(min_sample=min_sample),
        sample_size=overall.total_signals,
    )
    report.by_tier = _summary_for({"label": "tier", "key_fn": lambda r: r.get("tier")})
    report.by_mode = _summary_for({"label": "mode", "key_fn": lambda r: r.get("mode")})
    report.by_direction = _summary_for({"label": "direction", "key_fn": lambda r: r.get("direction")})
    report.by_exchange_confirmation = _summary_for(
        {"label": "exchange_confirmation", "key_fn": lambda r: r.get("exchange_confirmation_type")}
    )
    report.by_weekend_mode = _summary_for(
        {"label": "weekend", "key_fn": lambda r: "Y" if r.get("weekend_mode_active") else "N"}
    )
    report.by_sector = _summary_for({"label": "sector", "key_fn": lambda r: r.get("sector") or "(none)"})
    report.by_narrative = _summary_for(
        {"label": "narrative", "key_fn": lambda r: r.get("narrative") or "(none)"}
    )
    report.by_setup = _summary_for({"label": "setup", "key_fn": lambda r: r.get("setup_type") or "(none)"})
    return report


def _tier_of(row: dict[str, Any]) -> str:
    return str(row.get("tier") or "").strip().upper()


#: Tiers considered "actionable" — these are the only tiers the desk acts on
#: and the only ones that produce Telegram A/B alerts. C-tier is watchlist /
#: research quality and must NOT dilute the headline performance number.
ACTIONABLE_TIERS: frozenset[str] = frozenset({"A", "B"})
WATCHLIST_TIERS: frozenset[str] = frozenset({"C"})


def headline_split(
    store: SQLiteStore,
    *,
    config: SignalTrackingConfig,
    period: str = "week",
    mode: str | None = None,
    direction: str | None = None,
    weekend_mode: bool | None = None,
    asset_class: str | None = None,
) -> dict[str, Any]:
    """R1 reporting helper — split performance into actionable vs watchlist.

    Returns a pure-data dict (no rendering, no mutation):

        {
          "period", "asset_class", "mode",
          "actionable": <summary A+B>,     # headline metric
          "watchlist":  <summary C>,       # research/watchlist only
          "all_tier":   <summary A+B+C>,   # diagnostic, NOT the headline
          "by_tier":    {"A": <summary>, "B": <summary>, "C": <summary>},
        }

    PF / avg-R are recomputed from the **raw** R sums of each slice (not
    re-aggregated from rounded summaries), so the A/B headline PF is exact and
    a negative C-tier never bleeds into it. This is presentation only — it
    reads the same outcomes the rest of the desk reads and changes nothing.
    """

    min_sample = config.minimum_sample_for_recommendations

    def _bucket(pred, label: str) -> dict[str, Any]:
        bk, _ = collect(
            store,
            config=config,
            period=period,
            mode=mode,
            direction=direction,
            weekend_mode=weekend_mode,
            asset_class=asset_class,
            extra_filter=pred,
        )
        summary = bk.as_summary(min_sample=min_sample)
        summary["label"] = label
        return summary

    actionable = _bucket(lambda r: _tier_of(r) in ACTIONABLE_TIERS, "actionable (A/B)")
    watchlist = _bucket(lambda r: _tier_of(r) in WATCHLIST_TIERS, "watchlist (C)")
    all_tier = _bucket(lambda r: True, "all-tier diagnostic")
    by_tier = {t: _bucket(lambda r, t=t: _tier_of(r) == t, f"tier {t}") for t in ("A", "B", "C")}

    return {
        "period": period,
        "asset_class": asset_class,
        "mode": mode,
        "actionable": actionable,
        "watchlist": watchlist,
        "all_tier": all_tier,
        "by_tier": by_tier,
    }


def compact_packet_summary(
    store: SQLiteStore,
    *,
    config: SignalTrackingConfig,
    period: str = "week",
    asset_class: str | None = None,
) -> dict[str, Any]:
    """Compact dict for use in llm_analysis_packet.md."""

    report = compute_breakdowns(store, config=config, period=period, asset_class=asset_class)
    return {
        "period": period,
        "overall": report.overall,
        "by_tier": report.by_tier,
        "by_mode": report.by_mode,
        "by_direction": report.by_direction,
        "by_weekend_mode": report.by_weekend_mode,
        "by_exchange_confirmation": report.by_exchange_confirmation,
    }


def observations(
    breakdown: BreakdownReport,
    *,
    config: SignalTrackingConfig,
) -> list[dict[str, Any]]:
    """Generate observation strings with explicit sample-size warnings."""

    notes: list[dict[str, Any]] = []
    min_rec = config.minimum_sample_for_recommendations
    min_rule_change = config.minimum_sample_for_rule_change_suggestions

    def _note(level: str, text: str, sample: int) -> None:
        notes.append(
            {
                "level": level,
                "text": text,
                "sample": sample,
                "confidence": confidence_for_sample(sample, min_rec),
                "manual_approval_required": True,
            }
        )

    for tier_summary in breakdown.by_tier:
        sample = tier_summary.get("sample_size", 0) or 0
        wr = tier_summary.get("winrate_triggered")
        pf = tier_summary.get("profit_factor")
        if sample < 10:
            continue
        if wr is not None and wr < 0.35:
            _note(
                "observation",
                f"{tier_summary['label']}: triggered winrate {wr:.0%} is low. "
                "Consider reviewing entries.",
                sample,
            )
        if isinstance(pf, (int, float)) and pf != float("inf") and pf < 0.8:
            _note(
                "observation",
                f"{tier_summary['label']}: profit factor {pf:.2f} below 0.8.",
                sample,
            )

    for wkn in breakdown.by_weekend_mode:
        sample = wkn.get("sample_size", 0) or 0
        if sample < 10:
            continue
        wr = wkn.get("winrate_triggered")
        if wr is not None and "weekend=Y" in str(wkn.get("label", "")) and wr < 0.4:
            _note(
                "observation",
                f"{wkn['label']}: weekend signals underperform "
                f"(winrate {wr:.0%}, n={sample}).",
                sample,
            )

    for exch in breakdown.by_exchange_confirmation:
        sample = exch.get("sample_size", 0) or 0
        if sample < 10:
            continue
        label = str(exch.get("label", ""))
        if "MEXC-only" in label and (exch.get("capture_rate") or 1) < 0.3:
            _note(
                "observation",
                f"{label}: low capture rate ({exch.get('capture_rate')}, n={sample}). "
                "MEXC-only ideas may need cross-exchange confirmation.",
                sample,
            )

    has_strong_evidence = any(
        n["sample"] >= min_rule_change for n in notes if n["level"] == "observation"
    )
    if not has_strong_evidence and notes:
        notes.append(
            {
                "level": "meta",
                "text": (
                    "All observations above are below the "
                    f"{min_rule_change}-sample threshold required to even *suggest* a "
                    "rule change. Treat as anecdotal pattern detection."
                ),
                "sample": 0,
                "confidence": "anecdotal",
                "manual_approval_required": True,
            }
        )

    return notes
