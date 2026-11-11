from __future__ import annotations

from src.agents.base_agent import BaseAgent
from src.models import (
    CatalystSummary,
    Critique,
    DerivativesSummary,
    ExchangeConfirmation,
    MarketRegime,
    MomentumCandidate,
    NarrativeSummary,
    RejectedIdea,
    RiskAssessment,
    ScoreBreakdown,
    TechnicalSetup,
    TradeIdea,
)
from src.utils.formatting import fmt_float
from src.utils.validation import model_to_dict


class TradeIdeaAgent(BaseAgent):
    name = "trade_idea_agent"

    def run(
        self,
        setups: list[TechnicalSetup],
        candidates: list[MomentumCandidate],
        scores: dict[str, ScoreBreakdown],
        regime: MarketRegime,
        derivatives: dict[str, DerivativesSummary] | None = None,
        catalysts: dict[str, CatalystSummary] | None = None,
        risks: dict[str, RiskAssessment] | None = None,
        critiques: dict[str, Critique] | None = None,
        narratives: dict[str, NarrativeSummary] | None = None,
        exchange_confirmations: dict[str, ExchangeConfirmation] | None = None,
        mode: str = "intraday",
    ) -> list[TradeIdea]:
        candidate_map = {candidate.symbol: candidate for candidate in candidates}
        derivatives = derivatives or {}
        catalysts = catalysts or {}
        risks = risks or {}
        critiques = critiques or {}
        narratives = narratives or {}
        exchange_confirmations = exchange_confirmations or {}
        valid_threshold = float(self.config.scoring.get("thresholds", {}).get("valid_idea", 70))
        watch_threshold = float(
            self.config.scoring.get("thresholds", {}).get("watchlist_only", 55)
        )
        mode_normalised = mode if mode in {"scalp", "intraday", "swing"} else "intraday"
        ideas: list[TradeIdea] = []
        rejected: list[RejectedIdea] = []

        for setup in setups:
            score = scores.get(setup.symbol)
            candidate = candidate_map.get(setup.symbol)
            if score is None or candidate is None:
                continue

            tier = score.tier
            if tier in {"A", "B"} and setup.direction in {"long", "short"}:
                direction = setup.direction
                status = "open"
            elif tier == "C":
                direction = "watchlist only"
                status = "watchlist"
            else:
                direction = "no trade"
                status = "no_trade"
                rejected.append(
                    self._build_rejected(setup, candidate, score, exchange_confirmations)
                )
                # Still build the TradeIdea below so downstream code (SQLite,
                # charts) sees the symbol, but mark it tier=rejected.

            risk = risks.get(setup.symbol)
            derivative = derivatives.get(setup.symbol)
            catalyst = catalysts.get(setup.symbol)
            critique = critiques.get(setup.symbol)
            narrative = self._symbol_narrative(setup.symbol, narratives)

            risk_level = risk.risk_level if risk else "medium"
            if score.risk_penalty >= 20 or regime.label == "high-volatility danger":
                risk_level = "high"
            elif not risk and score.risk_penalty <= 8 and score.final_score >= 75:
                risk_level = "medium-low"

            thesis = self._build_thesis(setup, candidate, regime, direction, catalyst)
            evidence = self._build_evidence(
                setup, candidate, regime, score, derivative, catalyst, risk, narrative
            )
            counterarguments = self._build_counterarguments(setup, score, regime, critique, risk)
            entry_plan = self._entry_plan(setup, direction)
            if setup.invalidation is not None and direction in {"long", "short"}:
                invalidation = f"{setup.timeframe} close beyond {fmt_float(setup.invalidation)}"
            elif (
                setup.invalidation is not None
                and direction == "watchlist only"
                and setup.direction in {"long", "short"}
            ):
                invalidation = (
                    f"Potential invalidation if activated: {setup.timeframe} close beyond "
                    f"{fmt_float(setup.invalidation)}. Not active while score is below threshold."
                )
            else:
                invalidation = "No clean invalidation yet; no active trade."
            targets = self._targets(setup, direction)
            monitor = [
                "BTC and ETH structure around local support/resistance.",
                "Volume on pullback or breakout retest.",
                "Whether price accepts inside the entry zone instead of chasing.",
                "Funding, OI change, and long/short skew for crowding.",
            ]
            avoid = [
                "Do not enter if price is more than 2 ATR away from the planned entry.",
                "Do not enter if BTC breaks down against the regime thesis.",
                "Avoid if fresh news is unverified or contradicts the setup.",
            ]
            if setup.warnings:
                avoid.extend(setup.warnings[:3])
            if risk:
                avoid.extend(risk.reasons_to_avoid[:4])

            confirmation = exchange_confirmations.get(setup.symbol)
            exchange_focus = confirmation.suggested_exchange_focus if confirmation else self.config.anchor_exchange
            exchanges_confirmed = confirmation.exchanges_listed if confirmation else []
            data_confidence = self._data_confidence(
                derivative=derivative, catalyst=catalyst, confirmation=confirmation, score=score
            )

            ideas.append(
                TradeIdea(
                    symbol=setup.symbol,
                    direction=direction,
                    score=score.final_score,
                    confidence=score.confidence,
                    risk_level=risk_level,
                    timeframe=self._mode_timeframe(mode_normalised, setup.timeframe),
                    tier=tier,
                    mode=mode_normalised,
                    exchange_focus=exchange_focus,
                    exchanges_confirmed=exchanges_confirmed,
                    data_confidence=data_confidence,
                    thesis=thesis,
                    evidence=evidence,
                    counterarguments=counterarguments,
                    entry_plan=entry_plan,
                    invalidation=invalidation,
                    targets=targets,
                    what_to_monitor=monitor,
                    avoid_conditions=avoid,
                    data_sources_used=[
                        "local multi-exchange ccxt OHLCV cache (Binance/Bybit/MEXC)",
                        "Binance USD-M futures public endpoints",
                        "Bybit/OKX public derivatives endpoints",
                        "RSS/news cache",
                        "manual events + manual narrative/social notes",
                        "deterministic technical indicators",
                        "local scoring.yaml weights + tier caps",
                    ],
                    cap_reasons=list(score.cap_reasons),
                    status=status,
                    raw={
                        "setup": model_to_dict(setup),
                        "candidate": model_to_dict(candidate),
                        "score": model_to_dict(score),
                        "derivatives": model_to_dict(derivative) if derivative else {},
                        "catalyst": model_to_dict(catalyst) if catalyst else {},
                        "risk": model_to_dict(risk) if risk else {},
                        "critique": model_to_dict(critique) if critique else {},
                        "narrative": model_to_dict(narrative) if narrative else {},
                        "exchange_confirmation": model_to_dict(confirmation) if confirmation else {},
                    },
                )
            )

        ideas.sort(key=lambda idea: (idea.tier == "A", idea.tier == "B", idea.score), reverse=True)
        max_items = int(self.config.report_setting("max_trade_ideas", 5)) + int(
            self.config.report_setting("max_watchlist", 10)
        )
        ideas = ideas[:max_items]
        self.save_output(
            {
                "mode": mode_normalised,
                "ideas": [model_to_dict(idea) for idea in ideas],
                "rejected": [model_to_dict(item) for item in rejected],
            }
        )
        # Store rejected separately so the supervisor/report can render them.
        self._last_rejected = rejected
        return ideas

    @property
    def last_rejected(self) -> list[RejectedIdea]:
        return getattr(self, "_last_rejected", [])

    @staticmethod
    def _mode_timeframe(mode: str, setup_tf: str) -> str:
        if mode == "scalp":
            return f"{setup_tf} thesis / 5m execution (scalp 30m-2h)"
        if mode == "swing":
            return f"{setup_tf} thesis / 4h execution (swing several days)"
        return f"{setup_tf} thesis / 15m execution (intraday 4-24h)"

    @staticmethod
    def _data_confidence(
        derivative: DerivativesSummary | None,
        catalyst: CatalystSummary | None,
        confirmation: ExchangeConfirmation | None,
        score: ScoreBreakdown,
    ) -> str:
        score_value = 0
        if derivative and derivative.data_available:
            score_value += 1
        if catalyst and (catalyst.catalysts or catalyst.risk_events):
            score_value += 1
        if confirmation and confirmation.anchor_listed:
            score_value += 1
        if confirmation and confirmation.derivatives_listed:
            score_value += 1
        if score.data_quality == "strong":
            score_value += 1
        if score_value >= 4:
            return "high"
        if score_value >= 2:
            return "medium"
        return "low"

    @staticmethod
    def _build_rejected(
        setup: TechnicalSetup,
        candidate: MomentumCandidate,
        score: ScoreBreakdown,
        confirmations: dict[str, ExchangeConfirmation],
    ) -> RejectedIdea:
        confirmation = confirmations.get(setup.symbol)
        reasons: list[str] = list(score.cap_reasons)
        if score.warnings:
            reasons.extend(score.warnings[:3])
        if setup.invalidation is None:
            reasons.append("no clean invalidation")
        if confirmation and confirmation.high_risk_only:
            reasons.append("MEXC-only listing")
        if not reasons:
            reasons.append("score below tier-C threshold")
        primary = reasons[0]
        return RejectedIdea(
            symbol=setup.symbol,
            tier="rejected",
            score=score.final_score,
            direction_bias=candidate.direction_bias,
            primary_reason=primary,
            reasons=reasons[:6],
            exchanges=confirmation.exchanges_listed if confirmation else [],
            risk_flags=confirmation.risk_flags if confirmation else [],
        )

    def _build_thesis(
        self,
        setup: TechnicalSetup,
        candidate: MomentumCandidate,
        regime: MarketRegime,
        direction: str,
        catalyst: CatalystSummary | None = None,
    ) -> str:
        catalyst_note = ""
        if catalyst and catalyst.catalysts:
            catalyst_note = f" Fresh attention exists via {len(catalyst.catalysts)} catalyst/news item(s)."
        if direction in {"long", "short"}:
            side = "long continuation/pullback" if direction == "long" else "short breakdown/retest"
            return (
                f"{setup.symbol} has a {side} setup while the desk classifies the market as "
                f"{regime.label}. Momentum score is {candidate.score}/100 with tags: "
                f"{', '.join(candidate.reason_tags) or 'clean but not flashy'}.{catalyst_note}"
            )
        return (
            f"{setup.symbol} is interesting, but the evidence is not strong enough for an active "
            f"trade. Keep it on watch and demand a better entry or cleaner confirmation.{catalyst_note}"
        )

    def _build_evidence(
        self,
        setup: TechnicalSetup,
        candidate: MomentumCandidate,
        regime: MarketRegime,
        score: ScoreBreakdown,
        derivative: DerivativesSummary | None = None,
        catalyst: CatalystSummary | None = None,
        risk: RiskAssessment | None = None,
        narrative: NarrativeSummary | None = None,
    ) -> list[str]:
        evidence = [
            f"Market regime: {regime.label} ({regime.risk_mode}); style: {regime.recommended_style}.",
            f"24h return: {candidate.return_24h if candidate.return_24h is not None else 'n/a'}%; "
            f"7d return: {candidate.return_7d if candidate.return_7d is not None else 'n/a'}%.",
            f"Relative strength vs BTC: {candidate.relative_strength_btc if candidate.relative_strength_btc is not None else 'n/a'}%.",
            f"Volume ratio vs 20-period average: {candidate.volume_ratio if candidate.volume_ratio is not None else 'n/a'}x.",
            f"Trend: {setup.trend}; setup quality: {setup.setup_quality}/100; RR to TP1: {setup.rr_to_tp1 if setup.rr_to_tp1 is not None else 'n/a'}R.",
            f"Score breakdown: {score.components}; risk penalty: -{score.risk_penalty}.",
        ]
        if derivative and derivative.data_available:
            evidence.append(
                f"Derivatives: {derivative.interpretation}; funding {derivative.funding_rate if derivative.funding_rate is not None else 'n/a'}; "
                f"OI change {derivative.oi_change_pct if derivative.oi_change_pct is not None else 'n/a'}%; crowding {derivative.crowding_risk}."
            )
        else:
            evidence.append("Derivatives: unavailable for this symbol; confidence reduced.")
        if catalyst and (catalyst.catalysts or catalyst.risk_events):
            evidence.append(
                f"Catalyst/news: {catalyst.interpretation}; verification {catalyst.verification_status}; "
                f"importance {catalyst.importance_score}."
            )
        else:
            evidence.append("Catalyst/news: no fresh verified catalyst detected.")
        if risk:
            evidence.append(f"Risk gate: {risk.risk_level} risk, score {risk.risk_score}/100.")
        if narrative:
            evidence.append(
                f"Narrative: {narrative.narrative} is {narrative.status}, heat {narrative.heat_score}/100, risk {narrative.risk_score}/100."
            )
        return evidence

    def _build_counterarguments(
        self,
        setup: TechnicalSetup,
        score: ScoreBreakdown,
        regime: MarketRegime,
        critique: Critique | None = None,
        risk: RiskAssessment | None = None,
    ) -> list[str]:
        counters = []
        if critique:
            counters.append(critique.counter_thesis)
            counters.extend(critique.contradictions[:5])
        else:
            counters.append("Critic layer did not produce a symbol-specific critique.")
        if risk:
            counters.extend(risk.warnings[:4])
        if regime.label in {"range/chop", "transition"}:
            counters.append("Market regime is not clean; breakouts can fail quickly.")
        if setup.warnings:
            counters.extend(setup.warnings[:3])
        if score.final_score < 70:
            counters.append("Score is below active-trade threshold; this is watchlist/no-trade.")
        return counters

    def _entry_plan(self, setup: TechnicalSetup, direction: str) -> str:
        if direction not in {"long", "short"}:
            if (
                direction == "watchlist only"
                and setup.direction in {"long", "short"}
                and setup.entry_low is not None
                and setup.entry_high is not None
            ):
                side = "pullback" if setup.direction == "long" else "failed bounce/retest"
                return (
                    f"Watch only. Conditional {side} zone: {fmt_float(setup.entry_low)}-"
                    f"{fmt_float(setup.entry_high)}. Do not treat this as active until regime, "
                    "volume, or confirmation improves."
                )
            return "Watch only. Wait for a cleaner setup with entry, invalidation, and at least 1R to TP1."
        if direction == "long":
            return (
                f"Preferred entry: pullback into {fmt_float(setup.entry_low)}-"
                f"{fmt_float(setup.entry_high)}. No market buy if extended."
            )
        return (
            f"Preferred entry: failed bounce/retest into {fmt_float(setup.entry_low)}-"
            f"{fmt_float(setup.entry_high)}. No late short after a vertical flush."
        )

    def _targets(self, setup: TechnicalSetup, direction: str) -> list[str]:
        if direction not in {"long", "short"}:
            if direction == "watchlist only" and setup.direction in {"long", "short"}:
                return [
                    f"Conditional TP1: {fmt_float(setup.tp1)}",
                    f"Conditional TP2: {fmt_float(setup.tp2)}",
                    f"Conditional TP3: {fmt_float(setup.tp3)}",
                ]
            return ["No active targets until the setup becomes valid."]
        return [
            f"TP1: {fmt_float(setup.tp1)}",
            f"TP2: {fmt_float(setup.tp2)}",
            f"TP3: {fmt_float(setup.tp3)}",
        ]

    @staticmethod
    def _symbol_narrative(
        symbol: str, narratives: dict[str, NarrativeSummary]
    ) -> NarrativeSummary | None:
        matches = [
            narrative for narrative in narratives.values()
            if symbol in narrative.representative_symbols
        ]
        if not matches:
            return None
        return max(matches, key=lambda item: item.heat_score)
