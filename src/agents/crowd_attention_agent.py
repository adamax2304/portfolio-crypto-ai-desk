"""Crowd-attention staging per symbol.

Classifies each symbol into one of:
  silent | early_attention | growing_hype | euphoria |
  exhaustion | fear_capitulation | rumor_driven | unknown

Inputs:
  - candidates: price + volume + RS
  - social_attention: Reddit/manual mentions
  - manual_social_notes: list[dict] from data/manual/social_notes.yaml
  - derivatives: funding/OI per symbol (crowding signal)

The agent is intentionally conservative. It does NOT manufacture sentiment;
it surfaces "where is attention right now" so the trade-idea layer can either
demand confirmation (early attention, rumor) or cool down (euphoria,
crowding risk).
"""

from __future__ import annotations

from typing import Any

from src.agents.base_agent import BaseAgent
from src.models import (
    CrowdAttention,
    DerivativesSummary,
    MomentumCandidate,
    SocialAttentionSummary,
)
from src.utils.symbols import symbol_to_ticker
from src.utils.validation import clamp, model_to_dict


class CrowdAttentionAgent(BaseAgent):
    name = "crowd_attention_agent"

    def run(
        self,
        candidates: list[MomentumCandidate],
        social_attention: dict[str, SocialAttentionSummary] | None = None,
        manual_social_notes: list[dict[str, Any]] | None = None,
        derivatives: dict[str, DerivativesSummary] | None = None,
    ) -> dict[str, CrowdAttention]:
        social_attention = social_attention or {}
        manual_social_notes = manual_social_notes or []
        derivatives = derivatives or {}
        manual_by_ticker: dict[str, list[dict[str, Any]]] = {}
        for note in manual_social_notes:
            manual_by_ticker.setdefault(note["ticker"], []).append(note)

        results: dict[str, CrowdAttention] = {}
        for candidate in candidates:
            symbol = candidate.symbol
            ticker = symbol_to_ticker(symbol)
            social = social_attention.get(symbol)
            manual = manual_by_ticker.get(ticker, [])
            derivative = derivatives.get(symbol)

            attention_score = self._attention_score(social, manual)
            momentum_score = clamp(candidate.score)
            crowding_risk = self._crowding_risk(candidate, derivative)
            stage = self._stage(attention_score, momentum_score, crowding_risk, candidate, manual)
            evidence = self._evidence(social, manual, candidate, derivative)
            warnings = self._warnings(stage, attention_score, momentum_score, manual)
            confidence = self._confidence(social, manual, derivative)
            results[symbol] = CrowdAttention(
                symbol=symbol,
                stage=stage,
                attention_score=round(attention_score, 1),
                momentum_score=round(momentum_score, 1),
                crowding_risk=round(crowding_risk, 1),
                confidence=confidence,
                evidence=evidence,
                warnings=warnings,
            )

        self.save_output({symbol: model_to_dict(item) for symbol, item in results.items()})
        return results

    @staticmethod
    def _attention_score(
        social: SocialAttentionSummary | None,
        manual: list[dict[str, Any]],
    ) -> float:
        score = social.attention_score if social else 0.0
        for note in manual:
            weight = {"high": 18, "medium": 10, "low": 4}.get(note.get("confidence", "low"), 4)
            if note.get("verification") == "confirmed":
                weight += 4
            score += weight
        return clamp(score)

    @staticmethod
    def _crowding_risk(
        candidate: MomentumCandidate, derivative: DerivativesSummary | None
    ) -> float:
        risk = 0.0
        if candidate.return_24h is not None and candidate.return_24h > 15:
            risk += 35
        elif candidate.return_24h is not None and candidate.return_24h > 8:
            risk += 18
        if candidate.distance_from_ema20_atr is not None and abs(candidate.distance_from_ema20_atr) > 2:
            risk += 25
        if derivative and derivative.data_available and derivative.funding_rate is not None:
            if derivative.funding_rate > 0.001:
                risk += 30
            elif derivative.funding_rate > 0.0005:
                risk += 15
        return clamp(risk)

    @staticmethod
    def _stage(
        attention: float,
        momentum: float,
        crowding: float,
        candidate: MomentumCandidate,
        manual: list[dict[str, Any]],
    ) -> str:
        rumor_flag = any(note.get("verification") == "rumor" or note.get("sentiment") == "rumor" for note in manual)
        if rumor_flag and attention >= 15:
            return "rumor_driven"
        if attention >= 70 and crowding >= 55:
            return "euphoria"
        if attention >= 60 and momentum < 45:
            return "exhaustion"
        if attention >= 55 and momentum >= 60:
            return "growing_hype"
        if attention >= 30 and momentum >= 55 and crowding < 40:
            return "early_attention"
        if (candidate.return_24h or 0) < -10 and attention >= 30:
            return "fear_capitulation"
        if attention < 20 and momentum < 50:
            return "silent"
        return "unknown"

    @staticmethod
    def _evidence(
        social: SocialAttentionSummary | None,
        manual: list[dict[str, Any]],
        candidate: MomentumCandidate,
        derivative: DerivativesSummary | None,
    ) -> list[str]:
        ev: list[str] = []
        if social and social.mention_count:
            ev.append(f"Social: {social.mention_count} mentions, attention {social.attention_score}/100")
        if manual:
            ev.append(f"Manual: {len(manual)} note(s); latest: {manual[-1].get('note') or 'no text'}")
        if candidate.volume_ratio is not None:
            ev.append(f"Volume vs 20-avg: {candidate.volume_ratio}x")
        if derivative and derivative.data_available and derivative.funding_rate is not None:
            ev.append(f"Funding: {derivative.funding_rate}; crowding: {derivative.crowding_risk}")
        return ev

    @staticmethod
    def _warnings(
        stage: str,
        attention: float,
        momentum: float,
        manual: list[dict[str, Any]],
    ) -> list[str]:
        warnings: list[str] = []
        if stage == "euphoria":
            warnings.append("Euphoria stage: crowded long risk, demand pullback.")
        if stage == "rumor_driven":
            warnings.append("Rumor-driven attention; do not size up without verified catalyst.")
        if stage == "exhaustion":
            warnings.append("Attention high but momentum stalling; chase risk.")
        if stage == "fear_capitulation":
            warnings.append("Fear/capitulation: bottoming possible but no clean entry yet.")
        if attention >= 60 and momentum < 40:
            warnings.append("Attention not supported by price action.")
        return warnings

    @staticmethod
    def _confidence(
        social: SocialAttentionSummary | None,
        manual: list[dict[str, Any]],
        derivative: DerivativesSummary | None,
    ) -> str:
        points = 0
        if social and social.mention_count >= 3:
            points += 1
        if manual:
            points += 1
            if any(note.get("confidence") == "high" for note in manual):
                points += 1
        if derivative and derivative.data_available:
            points += 1
        if points >= 3:
            return "medium"
        if points >= 1:
            return "low"
        return "very low"
