from __future__ import annotations

from src.agents.base_agent import BaseAgent
from src.analysis.relative_strength_gate import (
    gate_params,
    is_relative_strength_leader,
    is_trend_aligned_short,
)
from src.models import (
    CatalystSummary,
    DerivativesSummary,
    MarketRegime,
    MomentumCandidate,
    RiskAssessment,
    TechnicalSetup,
)
from src.utils.validation import clamp, model_to_dict


class RiskAgent(BaseAgent):
    name = "risk_agent"

    def run(
        self,
        setups: list[TechnicalSetup],
        candidates: list[MomentumCandidate],
        regime: MarketRegime,
        derivatives: dict[str, DerivativesSummary],
        catalysts: dict[str, CatalystSummary],
    ) -> dict[str, RiskAssessment]:
        candidate_map = {candidate.symbol: candidate for candidate in candidates}
        results: dict[str, RiskAssessment] = {}

        for setup in setups:
            candidate = candidate_map.get(setup.symbol)
            derivative = derivatives.get(setup.symbol)
            catalyst = catalysts.get(setup.symbol)
            risk_score = 25.0
            warnings = list(setup.warnings)
            avoid: list[str] = []
            valid_if: list[str] = []

            # PART 20 (2026-06): relative-strength leaders (rising vs a weak
            # BTC) get a REDUCED — but never zero — adverse-regime penalty.
            # They are still counter-tape and must size down, but they should
            # not be auto-buried like a coin drifting with the falling market.
            rs_leader_long = (
                setup.direction == "long"
                and is_relative_strength_leader(candidate, **gate_params(self.config))
            )
            # PART 21: a short pressing a weak coin WITH a falling tape is
            # trend-aligned — it earns the same reduced (not flat-+25) danger
            # penalty as a long leader, instead of being suppressed like a
            # blind counter-trend entry.
            trend_aligned_short = (
                setup.direction == "short"
                and is_trend_aligned_short(candidate, regime)
            )

            if regime.label in {"transition", "range/chop"}:
                risk_score += 10
                warnings.append("Market regime is mixed; breakout failure risk is elevated.")
                valid_if.append("BTC/ETH confirm local direction instead of chopping.")
            if regime.label == "high-volatility trend":
                trend_aligned = (
                    (setup.direction == "long" and regime.btc_trend in {"uptrend", "transition_up"})
                    or (setup.direction == "short" and regime.btc_trend in {"downtrend", "transition_down"})
                )
                if trend_aligned:
                    risk_score += 8
                    warnings.append(
                        "Broad trend is intact but volatility is elevated; use reduced size and enter only on a pullback or retest."
                    )
                    valid_if.append("Do not chase: require the planned pullback/retest entry to trigger.")
                else:
                    risk_score += 20
                    avoid.append("Trade direction conflicts with a high-volatility trend.")
            if regime.label == "high-volatility danger":
                if rs_leader_long:
                    risk_score += 12
                    avoid.append(
                        "Counter-tape long in high-volatility danger — half size, tight invalidation."
                    )
                elif trend_aligned_short:
                    risk_score += 14
                    warnings.append(
                        "Short aligned with a volatile-bear tape — manageable, but size down: squeeze risk in extreme volatility."
                    )
                else:
                    risk_score += 25
                    avoid.append("No fresh entries during high-volatility danger unless size is reduced.")
            if setup.direction == "long" and regime.label == "bearish trend":
                if rs_leader_long:
                    risk_score += 12
                    warnings.append(
                        "Relative-strength leader long against a bearish tape — reduce size and demand confirmation."
                    )
                else:
                    risk_score += 25
                    avoid.append("Long setup conflicts with bearish market regime.")
            if setup.direction == "short" and regime.label == "bullish trend":
                risk_score += 20
                avoid.append("Short setup fights bullish market regime.")

            if candidate and candidate.volume_ratio is not None and candidate.volume_ratio < 0.5:
                risk_score += 8
                warnings.append("Volume is below average; breakout confirmation is weak.")
                valid_if.append("Volume expands above the 20-period average on retest.")
            if candidate and candidate.distance_from_ema20_atr is not None and abs(candidate.distance_from_ema20_atr) > 2:
                risk_score += 12
                avoid.append("Move is extended more than 2 ATR from EMA20.")
            if setup.rr_to_tp1 is not None and setup.rr_to_tp1 < 1:
                risk_score += 14
                avoid.append("Risk/reward to TP1 is below 1R.")
            if setup.invalidation is None and setup.direction in {"long", "short"}:
                risk_score += 25
                avoid.append("No clear invalidation.")

            if derivative is None or not derivative.data_available:
                risk_score += 6
                warnings.append("Derivatives data unavailable; leverage crowding is unknown.")
            else:
                if "extreme" in derivative.crowding_risk:
                    risk_score += 18
                    avoid.append("Funding is extreme; avoid late crowded long exposure.")
                elif "elevated" in derivative.crowding_risk:
                    risk_score += 8
                    warnings.append("Funding is elevated; entry must be clean.")
                warnings.extend(derivative.warnings[:2])

            if catalyst and catalyst.risk_events:
                risk_score += 15
                warnings.extend(catalyst.warnings)
                avoid.append("Catalyst risk event is near the trading window.")
            if catalyst is None or catalyst.verification_status == "none":
                warnings.append("No fresh verified catalyst detected.")

            risk_score = clamp(risk_score)
            if risk_score >= 70:
                risk_level = "high"
            elif risk_score >= 45:
                risk_level = "medium"
            else:
                risk_level = "low"
            if not valid_if:
                valid_if.append("Setup remains valid only if entry, invalidation, and market regime stay aligned.")

            results[setup.symbol] = RiskAssessment(
                symbol=setup.symbol,
                risk_score=round(risk_score, 1),
                risk_level=risk_level,
                warnings=list(dict.fromkeys(warnings)),
                reasons_to_avoid=list(dict.fromkeys(avoid)),
                valid_if=list(dict.fromkeys(valid_if)),
            )

        self.save_output({symbol: model_to_dict(item) for symbol, item in results.items()})
        return results
