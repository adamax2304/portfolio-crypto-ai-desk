"""Convert generated TradeIdea objects into ProposedSignal rows and store them.

The registry is the one-and-only entry point for inserting new signals. Both
the supervisor auto-hook and the `register-signals` CLI go through here, so
the dedupe logic / field extraction / safety filters live in a single place.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable

from src.execution.stop_contract import (
    build_initial_stop_contract,
    entry_anchor as stop_entry_anchor,
    stop_contract_label,
    upsert_signal_initial_stop_plan,
)
from src.models import TradeIdea
from src.signals.config import SignalTrackingConfig
from src.signals.models import (
    STATUS_GENERATED,
    STATUS_WAITING,
    ProposedSignal,
    signal_id_for,
)
from src.storage.sqlite import SQLiteStore


@dataclass
class RegistrationResult:
    inserted: int = 0
    skipped_existing: int = 0
    skipped_tier: int = 0
    skipped_no_setup: int = 0
    skipped_no_trigger: int = 0
    skipped_portfolio_guard: int = 0
    portfolio_guard_reason: str = ""
    signal_ids: list[str] = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        if self.signal_ids is None:
            self.signal_ids = []


def _iso_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")


def _coerce_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _extract_setup_type(idea: TradeIdea) -> str:
    """Best-effort label from candidate tags + thesis."""

    tags = []
    cand = (idea.raw or {}).get("candidate") or {}
    raw_tags = cand.get("reason_tags") or []
    if isinstance(raw_tags, list):
        tags = [str(t).lower() for t in raw_tags]
    haystack = (idea.thesis or "").lower() + " " + " ".join(tags)
    # Order matters — pick the most specific match first.
    for label, needles in (
        ("breakdown", ["breakdown"]),
        ("breakout", ["breakout"]),
        ("reclaim", ["reclaim"]),
        ("squeeze", ["squeeze"]),
        ("reversal", ["reversal", "exhaustion", "capitulation"]),
        ("mean_reversion", ["mean reversion", "mean-reversion", "fade"]),
        ("pullback", ["pullback", "retest", "failed bounce"]),
        ("continuation", ["continuation", "trend"]),
    ):
        if any(needle in haystack for needle in needles):
            return label
    return "other"


def _exchange_confirmation_type(idea: TradeIdea) -> str:
    exchanges = {str(e).lower() for e in (idea.exchanges_confirmed or [])}
    if not exchanges:
        return "unknown"
    if exchanges == {"mexc"}:
        return "MEXC-only"
    if "binance" in exchanges and "bybit" in exchanges:
        return "Binance+Bybit"
    if "binance" in exchanges and len(exchanges) > 1:
        return "cross-exchange"
    if "binance" in exchanges:
        return "Binance"
    if "bybit" in exchanges:
        return "Bybit"
    if "mexc" in exchanges:
        return "MEXC-only"
    return "unknown"


def _sector_and_narrative(idea: TradeIdea) -> tuple[str, str]:
    narrative_raw = (idea.raw or {}).get("narrative") or {}
    if isinstance(narrative_raw, dict):
        # narrative_raw may be either {"label": ...} or a richer payload.
        narrative = (
            str(narrative_raw.get("primary") or narrative_raw.get("label") or "")
        )
    else:
        narrative = ""
    cand = (idea.raw or {}).get("candidate") or {}
    sector = str(cand.get("sector") or cand.get("ticker_family") or "")
    return sector, narrative


def _risk_per_unit(direction: str, entry_low: float | None,
                   entry_high: float | None, invalidation: float | None) -> float | None:
    """Distance from preferred entry to invalidation in price units."""

    if invalidation is None:
        return None
    if direction == "long":
        anchor = entry_high if entry_high is not None else entry_low
        if anchor is None:
            return None
        diff = anchor - invalidation
    elif direction == "short":
        anchor = entry_low if entry_low is not None else entry_high
        if anchor is None:
            return None
        diff = invalidation - anchor
    else:
        return None
    return float(diff) if diff > 0 else None


def _expected_rr(direction: str, entry_anchor: float | None,
                 invalidation: float | None, target: float | None) -> float | None:
    if entry_anchor is None or invalidation is None or target is None:
        return None
    if direction == "long":
        reward = target - entry_anchor
        risk = entry_anchor - invalidation
    elif direction == "short":
        reward = entry_anchor - target
        risk = invalidation - entry_anchor
    else:
        return None
    if risk is None or risk <= 0:
        return None
    return float(reward / risk)


def _qualifies_for_tracking(
    idea: TradeIdea, config: SignalTrackingConfig
) -> tuple[bool, str]:
    """Return (track, reason_if_skipped) for the Armed Watch lifecycle.

    Registration means the candidate can later be monitored and potentially
    activated.  Every registered idea therefore needs directional, internally
    consistent entry/stop geometry; a high tier alone is never enough.
    """

    if idea.direction not in ("long", "short"):
        return False, "tier"

    tier_is_tracked = idea.tier in config.track_tiers
    c_watch_enabled = config.track_watchlist_with_trigger and idea.tier == "C"
    if not (tier_is_tracked or c_watch_enabled):
        return False, "tier"

    setup = (idea.raw or {}).get("setup") or {}
    entry_low = _coerce_float(setup.get("entry_low"))
    entry_high = _coerce_float(setup.get("entry_high"))
    invalidation = _coerce_float(setup.get("invalidation"))
    if invalidation is None or (entry_low is None and entry_high is None):
        return False, "no_trigger"

    # A one-sided zone is supported for legacy/imported signals, but the stop
    # still has to invalidate the stated direction rather than sit inside it.
    entry_anchor = entry_high if idea.direction == "long" else entry_low
    if entry_anchor is None:
        entry_anchor = entry_low if idea.direction == "long" else entry_high
    if entry_anchor is None:
        return False, "no_trigger"
    if idea.direction == "long" and invalidation >= entry_anchor:
        return False, "no_trigger"
    if idea.direction == "short" and invalidation <= entry_anchor:
        return False, "no_trigger"
    return True, ""


def _apply_news_influence_contract(store: SQLiteStore, signal: ProposedSignal,
                                   idea: TradeIdea) -> None:
    """Make canonical news policy authoritative at signal registration.

    This closes the scan-time gap where a broad ``news_count`` could set
    ``news_supported`` before the stricter post-scan refresh ran. Manual events
    remain valid. Old DBs without the canonical table preserve legacy behavior.
    The helper is fail-open for registration availability, but never fabricates
    a canonical hit.
    """
    catalyst = (idea.raw or {}).get("catalyst") or {}
    manual_event = isinstance(catalyst, dict) and catalyst.get("verification_status") == "manual_event"
    try:
        with store.connect() as conn:
            has_table = conn.execute(
                "SELECT 1 FROM sqlite_master WHERE type='table' AND name='news_canonical_events'"
            ).fetchone()
            if not has_table:
                return
            from src.signals.catalyst_label_refresh import direct_news_for_signal
            hit = direct_news_for_signal(
                conn, signal.symbol, signal.created_at, asset_class=signal.asset_class,
                direction=signal.direction, mode=signal.mode,
            )
        signal.news_supported = bool(manual_event or hit)
        signal.telegram_supported = bool(hit and hit.get("has_telegram"))
        try:
            raw = json.loads(signal.raw_idea_json or "{}")
            if not isinstance(raw, dict):
                raw = {}
            raw["news_influence_contract"] = {
                "policy_version": "news_influence_v1", "authoritative": True,
                "supported": bool(signal.news_supported),
                "source": "manual_event" if manual_event else (
                    "canonical_event" if hit else "no_eligible_canonical_event"),
                "event_type": hit.get("event_type") if hit else None,
                "direction_hint": hit.get("direction_hint") if hit else None,
                "content_level": hit.get("content_level") if hit else None,
                "confidence": hit.get("confidence") if hit else None,
            }
            signal.raw_idea_json = json.dumps(raw, ensure_ascii=False)
        except Exception:
            pass
    except Exception:
        # Registration must remain available during a read-model DB hiccup.
        return


def build_signal_from_idea(
    idea: TradeIdea,
    *,
    config: SignalTrackingConfig,
    report_id: str,
    market_regime: str = "",
    weekend_mode_active: bool = False,
    source_report_path: str = "",
    source_context_path: str = "",
    created_at: str | None = None,
    asset_class: str = "crypto",
) -> ProposedSignal | None:
    """Returns None if the idea doesn't qualify for tracking."""

    qualifies, _ = _qualifies_for_tracking(idea, config)
    if not qualifies:
        return None

    setup = dict((idea.raw or {}).get("setup") or {})
    direction = idea.direction
    # The active crypto-swing Paper target profile is versioned in config. Its
    # application is limited to new Paper signals; Shadow profiles stay separate.
    resolved_asset_class = getattr(idea, "asset_class", None) or asset_class
    swing_target_profile: dict[str, Any] | None = None
    if str(resolved_asset_class or "").lower() == "crypto" and str(idea.mode or "").lower() == "swing":
        try:
            from src.execution.crypto_swing_paper_policy import apply_target_profile_to_setup
            setup, swing_target_profile = apply_target_profile_to_setup(setup, direction=direction)
        except Exception:
            pass
    entry_low = _coerce_float(setup.get("entry_low"))
    entry_high = _coerce_float(setup.get("entry_high"))
    invalidation = _coerce_float(setup.get("invalidation"))
    tp1 = _coerce_float(setup.get("tp1"))
    tp2 = _coerce_float(setup.get("tp2"))
    tp3 = _coerce_float(setup.get("tp3"))
    entry_anchor = entry_high if direction == "long" else entry_low

    derivatives = (idea.raw or {}).get("derivatives") or {}
    catalysts = (idea.raw or {}).get("catalyst") or {}
    # 2026-06-15 label fix: news_supported was only set from the crypto
    # catalyst-agent path (idea.raw["catalyst"]["catalysts"]). The stocks
    # pipeline attaches per-ticker news as idea.raw["news_count"] (count of
    # CompanyNewsAgent hits_by_symbol[symbol]) — which IS ticker-specific, not
    # generic market/sector. Recognise that path too so stocks signals carry
    # the catalyst label. Display/measurement only — score/tier/routing are
    # NOT changed by this flag. See reports/STOCKS_NEWS_SUPPORTED_LABEL_FIX_REPORT.md.
    news_supported = bool(catalysts.get("catalysts")) if isinstance(catalysts, dict) else False
    if not news_supported:
        try:
            news_count = int((idea.raw or {}).get("news_count") or 0)
        except (TypeError, ValueError):
            news_count = 0
        if news_count > 0:
            news_supported = True
    derivatives_supported = bool(derivatives.get("data_available")) if isinstance(derivatives, dict) else False

    sector, narrative = _sector_and_narrative(idea)
    created = created_at or _iso_now()
    raw_validity_h = _coerce_float((idea.raw or {}).get("validity_window_hours"))
    validity_h = raw_validity_h if raw_validity_h and raw_validity_h > 0 else config.validity_hours_for(idea.mode)
    try:
        created_dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
        if created_dt.tzinfo is None:
            created_dt = created_dt.replace(tzinfo=timezone.utc)
        else:
            created_dt = created_dt.astimezone(timezone.utc)
    except (TypeError, ValueError):
        created_dt = datetime.now(timezone.utc)
    expires_dt = created_dt + timedelta(hours=validity_h)
    expires_iso = expires_dt.strftime("%Y-%m-%dT%H:%M:%S+00:00")

    signal_id = signal_id_for(
        symbol=idea.symbol,
        mode=idea.mode,
        direction=direction,
        tier=idea.tier,
        entry_low=entry_low,
        entry_high=entry_high,
        invalidation=invalidation,
        created_at=created,
        report_id=report_id,
        strategy_identity=str((idea.raw or {}).get("paper_entry_profile") or ""),
    )

    raw_payload = _safe_idea_payload(idea)
    initial_stop_contract = build_initial_stop_contract(
        symbol=idea.symbol,
        asset_class=resolved_asset_class,
        mode=idea.mode,
        direction=direction,
        entry_price=stop_entry_anchor(direction, entry_low, entry_high, entry_anchor),
        stop_price=invalidation,
        setup=setup,
        payload=raw_payload,
    )
    raw_payload["initial_stop_contract"] = initial_stop_contract
    raw_payload["stop_contract"] = initial_stop_contract
    raw_payload["stop_label"] = stop_contract_label(initial_stop_contract)
    raw_derivatives = (idea.raw or {}).get("derivatives") or {}
    if isinstance(raw_derivatives, dict):
        # Preserve compact proposal-time values as an alert fallback. Fresh
        # Telegram values still come from the canonical read-only archive.
        raw_payload["derivatives_at_proposal"] = {
            key: raw_derivatives.get(key)
            for key in (
                "data_available", "funding_rate", "crowding_risk", "funding_state",
                "open_interest_usd", "open_interest_value", "oi_change_24h",
                "oi_change_pct", "venue_count", "interpretation",
            )
            if raw_derivatives.get(key) is not None
        }
    if swing_target_profile and swing_target_profile.get("available"):
        raw_payload["paper_target_profile"] = {
            "name": swing_target_profile.get("profile"),
            "version": swing_target_profile.get("version"),
            "target_multipliers": swing_target_profile.get("target_multipliers"),
            "source": swing_target_profile.get("source"),
        }

    return ProposedSignal(
        signal_id=signal_id,
        created_at=created,
        symbol=idea.symbol,
        direction=direction,
        mode=idea.mode,
        tier=idea.tier,
        score=float(idea.score),
        confidence=idea.confidence,
        data_confidence=idea.data_confidence,
        exchange_focus=idea.exchange_focus or "",
        asset_class=resolved_asset_class,
        listed_exchanges=list(idea.exchanges_confirmed or []),
        primary_exchange=idea.exchange_focus or "",
        exchange_confirmation_type=_exchange_confirmation_type(idea),
        market_regime=market_regime,
        weekend_mode_active=bool(weekend_mode_active),
        sector=sector,
        narrative=narrative,
        setup_type=_extract_setup_type(idea),
        news_supported=news_supported,
        telegram_supported=False,  # populated later when bridge cross-check is wired
        derivatives_supported=derivatives_supported,
        oi_context=str(derivatives.get("interpretation", "")) if isinstance(derivatives, dict) else "",
        funding_context=(
            f"funding={derivatives.get('funding_rate')}, "
            f"crowding={derivatives.get('crowding_risk')}"
            if isinstance(derivatives, dict) and derivatives.get("data_available")
            else ""
        ),
        entry_type="zone" if (entry_low is not None and entry_high is not None) else "trigger",
        entry_low=entry_low,
        entry_high=entry_high,
        entry_trigger=entry_anchor,
        suggested_entry=entry_anchor,
        stop_loss=invalidation,
        invalidation=invalidation,
        tp1=tp1,
        tp2=tp2,
        tp3=tp3,
        risk_per_unit=_risk_per_unit(direction, entry_low, entry_high, invalidation),
        expected_rr_tp1=_expected_rr(direction, entry_anchor, invalidation, tp1),
        expected_rr_tp2=_expected_rr(direction, entry_anchor, invalidation, tp2),
        expected_rr_tp3=_expected_rr(direction, entry_anchor, invalidation, tp3),
        validity_window_hours=validity_h,
        expires_at=expires_iso,
        thesis=idea.thesis or "",
        counter_thesis=" | ".join(idea.counterarguments or []),
        no_entry_conditions=list(idea.avoid_conditions or []),
        source_report_path=source_report_path,
        source_context_path=source_context_path,
        report_id=report_id,
        raw_idea_json=json.dumps(raw_payload, default=str),
        status=STATUS_WAITING,
    )


def _safe_idea_payload(idea: TradeIdea) -> dict[str, Any]:
    """Trim the idea payload before persisting — we don't need megabytes."""

    return {
        "symbol": idea.symbol,
        "direction": idea.direction,
        "tier": idea.tier,
        "mode": idea.mode,
        "score": idea.score,
        "confidence": idea.confidence,
        "data_confidence": idea.data_confidence,
        "exchange_focus": idea.exchange_focus,
        "exchanges_confirmed": list(idea.exchanges_confirmed or []),
        "thesis": idea.thesis,
        "evidence": list(idea.evidence or []),
        "counterarguments": list(idea.counterarguments or []),
        "entry_plan": idea.entry_plan,
        "invalidation": idea.invalidation,
        "targets": list(idea.targets or []),
        "cap_reasons": list(idea.cap_reasons or []),
        "raw_setup": (idea.raw or {}).get("setup") or {},
        "raw_score": (idea.raw or {}).get("score") or {},
        "stop_contract": (idea.raw or {}).get("stop_contract")
        or ((idea.raw or {}).get("setup") or {}).get("stop_contract")
        or {},
        "initial_stop_contract": (idea.raw or {}).get("initial_stop_contract")
        or ((idea.raw or {}).get("setup") or {}).get("initial_stop_contract")
        or {},
        "candidate_structural_stop_contract": (idea.raw or {}).get("candidate_structural_stop_contract")
        or ((idea.raw or {}).get("setup") or {}).get("candidate_structural_stop_contract")
        or {},
        # stocks-intraday diagnostics persisted into raw_idea_json (crypto ideas simply omit these):
        # `structured`/`candidate` power the sector read-time fallback (intraday_guards._sector_from)
        # and the report/packet metric lines; pre_gate_tier/final_tier/demoted_by_gate power
        # recovery_stats and the "would-have-been-A/B" demoted-candidate sections.
        "structured": (idea.raw or {}).get("structured") or {},
        "candidate": (idea.raw or {}).get("candidate") or {},
        "pre_gate_tier": (idea.raw or {}).get("pre_gate_tier"),
        "final_tier": (idea.raw or {}).get("final_tier"),
        "demoted_by_gate": (idea.raw or {}).get("demoted_by_gate"),
        # The stocks pipeline stamps the exact final decision time once and
        # uses it for its session gate and the persisted signal timestamp.
        # Keep it in the snapshot so an audit can prove those clocks agree.
        "decision_at": (idea.raw or {}).get("decision_at"),
        # SI-1..SI-5 actionability-gate diagnostics (market/sector/session/liquidity/catalyst statuses,
        # demote reasons, or gate_error fields). Persisted so the SI-7 post-trade classifier, the SI-6
        # LLM packet, and the report/UI can read exactly why a stocks-intraday A/B was demoted to C.
        # Crypto / non-intraday ideas simply carry {}.
        "intraday_actionability": (idea.raw or {}).get("intraday_actionability") or {},
        # Versioned Paper-profile provenance.  Kept compact so a profile can
        # opt into a different deterministic entry confirmation without
        # silently changing ordinary stock Paper routing.
        "paper_entry_profile": (idea.raw or {}).get("paper_entry_profile"),
        "paper_lane": (idea.raw or {}).get("paper_lane"),
        "paper_entry_policy_version": (idea.raw or {}).get("paper_entry_policy_version"),
        "paper_execution_entry_mode": (idea.raw or {}).get("paper_execution_entry_mode"),
        "paper_entry_confirmation": (idea.raw or {}).get("paper_entry_confirmation"),
        "paper_size_weight": (idea.raw or {}).get("paper_size_weight"),
        "paper_size_reason": (idea.raw or {}).get("paper_size_reason"),
        "validity_window_hours": (idea.raw or {}).get("validity_window_hours"),
        "source_shadow_profile": (idea.raw or {}).get("source_shadow_profile"),
        "paper_max_chase_r": (idea.raw or {}).get("paper_max_chase_r"),
        "paper_size_label": (idea.raw or {}).get("paper_size_label"),
        "source_shadow_candidate_id": (idea.raw or {}).get("source_shadow_candidate_id"),
        "source_news_event_id": (idea.raw or {}).get("source_news_event_id"),
        "catalyst_type": (idea.raw or {}).get("catalyst_type"),
        "catalyst_source_quality": (idea.raw or {}).get("catalyst_source_quality"),
        "evidence_cohort": (idea.raw or {}).get("evidence_cohort"),
        "confirmation_at": (idea.raw or {}).get("confirmation_at"),
        "confirmation_price": (idea.raw or {}).get("confirmation_price"),
        "catalyst_rs_features": (idea.raw or {}).get("catalyst_rs_features") or {},
        "stock_swing_event_rs_pullback": (idea.raw or {}).get("stock_swing_event_rs_pullback") or {},
        "news_context": (idea.raw or {}).get("news_context") or {},
    }


def register_ideas(
    store: SQLiteStore,
    ideas: Iterable[TradeIdea],
    *,
    config: SignalTrackingConfig,
    report_id: str,
    market_regime: str = "",
    weekend_mode_active: bool = False,
    source_report_path: str = "",
    source_context_path: str = "",
    asset_class: str = "crypto",
    created_at: str | None = None,
) -> RegistrationResult:
    """Persist all qualifying signals. Safe to call multiple times — dedupes
    by signal_id."""

    result = RegistrationResult()
    if not config.enabled:
        return result
    # A batch may be a generator. Materialize it once so the guard audit count, blocked count and
    # subsequent registration loop all refer to the exact same candidate set.
    ideas = list(ideas)
    # 2026-07-13 audit: the one REAL (non-diagnostic) portfolio-wide kill-switch -- a severe
    # recent combined crypto+stocks drawdown pauses new signal registration for BOTH asset
    # classes until the rolling window recovers. This is the single entry point both funnel
    # through (see module docstring), so this is the correct and only place to enforce it.
    # Fails open (never blocks) on any read/config problem -- see src/risk/portfolio_guard.py.
    # 2026-07-13 review: portfolio_guard.py's OWN internal fail-open only covers runtime errors
    # reached after a successful import -- an import-time failure (e.g. a future syntax error in
    # that module) would otherwise propagate straight out of this function uncaught, breaking
    # ALL signal registration (both asset classes) until fixed. That is a far worse outage than
    # the one this guard exists to prevent, so the import itself is wrapped here too.
    try:
        from src.risk.portfolio_guard import blocks_new_signals
        should_block, reason = blocks_new_signals(
            db=str(store.db_path),
            audit_context={
                "source": "signals.registry.register_ideas",
                "report_id": report_id,
                "candidate_count": len(ideas),
                "asset_classes": sorted({
                    str(getattr(idea, "asset_class", None) or asset_class).lower()
                    for idea in ideas
                }),
            },
        )
    except Exception:
        should_block, reason = False, "portfolio_guard unavailable"
    if should_block:
        result.skipped_portfolio_guard = len(ideas)
        result.portfolio_guard_reason = reason
        return result
    for idea in ideas:
        qualifies, reason = _qualifies_for_tracking(idea, config)
        if not qualifies:
            if reason == "tier":
                result.skipped_tier += 1
            elif reason == "no_trigger":
                result.skipped_no_trigger += 1
            continue
        signal = build_signal_from_idea(
            idea,
            config=config,
            report_id=report_id,
            market_regime=market_regime,
            weekend_mode_active=weekend_mode_active,
            source_report_path=source_report_path,
            source_context_path=source_context_path,
            asset_class=asset_class,
            created_at=created_at,
        )
        if signal is None:
            result.skipped_no_setup += 1
            continue
        _apply_news_influence_contract(store, signal, idea)
        inserted = store.upsert_proposed_signal(signal.to_row())
        try:
            raw = json.loads(signal.raw_idea_json or "{}")
            contract = raw.get("initial_stop_contract") or raw.get("stop_contract") or {}
            if isinstance(contract, dict) and contract:
                with store.connect() as conn:
                    upsert_signal_initial_stop_plan(
                        conn,
                        signal_id=signal.signal_id,
                        contract=contract,
                        source="signals.registry",
                    )
        except Exception:
            pass
        if inserted:
            result.inserted += 1
            result.signal_ids.append(signal.signal_id)
        else:
            result.skipped_existing += 1
    return result


def register_from_agent_output(
    store: SQLiteStore,
    *,
    config: SignalTrackingConfig,
    agent_output_path: Path,
    report_id: str = "",
    market_regime: str = "",
    weekend_mode_active: bool = False,
    source_report_path: str = "",
    source_context_path: str = "",
    asset_class: str = "crypto",
) -> RegistrationResult:
    """Read a trade_idea_agent.json file and register everything in it."""

    if not agent_output_path.exists():
        return RegistrationResult()
    try:
        with agent_output_path.open("r", encoding="utf-8") as fh:
            payload = json.load(fh)
    except Exception:
        return RegistrationResult()
    ideas_payload = payload.get("ideas") if isinstance(payload, dict) else None
    if not ideas_payload:
        return RegistrationResult()
    rid = report_id or payload.get("report_id") or agent_output_path.stem
    ideas: list[TradeIdea] = []
    for entry in ideas_payload:
        try:
            ideas.append(TradeIdea(**entry))
        except Exception:
            # Skip malformed legacy records rather than blocking registration.
            continue
    return register_ideas(
        store,
        ideas,
        config=config,
        report_id=str(rid),
        market_regime=market_regime,
        weekend_mode_active=weekend_mode_active,
        source_report_path=source_report_path,
        source_context_path=source_context_path,
        asset_class=asset_class,
    )
