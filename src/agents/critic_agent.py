from __future__ import annotations

from src.agents.base_agent import BaseAgent
from src.models import (
    CatalystSummary,
    Critique,
    DerivativesSummary,
    MarketRegime,
    MomentumCandidate,
    RiskAssessment,
    TechnicalSetup,
)
from src.utils.validation import model_to_dict


class CriticAgent(BaseAgent):
    name = "critic_agent"

    def run(
        self,
        setups: list[TechnicalSetup],
        candidates: list[MomentumCandidate],
        regime: MarketRegime,
        derivatives: dict[str, DerivativesSummary],
        catalysts: dict[str, CatalystSummary],
        risks: dict[str, RiskAssessment],
    ) -> dict[str, Critique]:
        candidate_map = {candidate.symbol: candidate for candidate in candidates}
        results: dict[str, Critique] = {}

        for setup in setups:
            candidate = candidate_map.get(setup.symbol)
            derivative = derivatives.get(setup.symbol)
            catalyst = catalysts.get(setup.symbol)
            risk = risks.get(setup.symbol)
            contradictions: list[str] = []
            late = False
            weak_signal = False

            if regime.label in {"transition", "range/chop"}:
                contradictions.append("The broad tape is not decisive; momentum can mean-revert.")
            if candidate and candidate.volume_ratio is not None and candidate.volume_ratio < 0.75:
                contradictions.append("Relative strength is not backed by strong current volume.")
                weak_signal = True
            if derivative is None or not derivative.data_available:
                contradictions.append("No usable derivatives read, so leverage confirmation is missing.")
                weak_signal = True
            elif setup.direction == "long" and derivative.alignment_score < -0.2:
                contradictions.append(f"Derivatives lean against the long: {derivative.interpretation}")
            elif setup.direction == "short" and derivative.alignment_score > 0.2:
                contradictions.append(f"Derivatives lean against the short: {derivative.interpretation}")
            if catalyst is None or catalyst.verification_status == "none":
                contradictions.append("No fresh catalyst is verified for this symbol.")
            if candidate and candidate.distance_from_ema20_atr is not None and abs(candidate.distance_from_ema20_atr) > 1.75:
                contradictions.append("The move may be late relative to EMA20/ATR.")
                late = True
            if risk and risk.risk_score >= 60:
                contradictions.append(f"Risk score is elevated at {risk.risk_score}/100.")

            if not contradictions:
                contradictions.append("No major contradiction found, but entry discipline still matters.")

            verdict = "reject" if risk and risk.risk_score >= 75 else "watch"
            if setup.direction in {"long", "short"} and not weak_signal and not late and risk and risk.risk_score < 45:
                verdict = "acceptable if entry triggers"

            results[setup.symbol] = Critique(
                symbol=setup.symbol,
                counter_thesis=self._counter_thesis(setup, regime),
                contradictions=contradictions,
                late_or_crowded=late,
                weak_signal_dependency=weak_signal,
                verdict=verdict,
            )

        self.save_output({symbol: model_to_dict(item) for symbol, item in results.items()})
        return results

    @staticmethod
    def _counter_thesis(setup: TechnicalSetup, regime: MarketRegime) -> str:
        if setup.direction == "long":
            return (
                f"The long fails if {setup.symbol} is just a beta bounce inside a {regime.label} "
                "market and buyers do not defend the planned pullback zone."
            )
        if setup.direction == "short":
            return (
                f"The short fails if {setup.symbol} is a late breakdown into exhausted sellers "
                "and BTC/ETH reclaim local levels."
            )
        return "There is no active trade; the counter-thesis is that attention is real but execution is not ready."
