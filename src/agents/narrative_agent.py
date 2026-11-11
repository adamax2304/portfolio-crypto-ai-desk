from __future__ import annotations

from src.agents.base_agent import BaseAgent
from src.models import CatalystSummary, MomentumCandidate, NarrativeSummary
from src.utils.symbols import symbol_to_ticker
from src.utils.validation import clamp, model_to_dict


class NarrativeAgent(BaseAgent):
    name = "narrative_agent"

    def run(
        self,
        candidates: list[MomentumCandidate],
        news_output: dict,
        catalysts: dict[str, CatalystSummary],
    ) -> dict[str, NarrativeSummary]:
        narrative_config = self.config.watchlist.get("narratives", {})
        candidate_by_ticker = {symbol_to_ticker(item.symbol): item for item in candidates}
        by_narrative = news_output.get("by_narrative", {})
        by_symbol = news_output.get("by_symbol", {})
        results: dict[str, NarrativeSummary] = {}

        for name, payload in narrative_config.items():
            configured_tickers = [str(item).upper() for item in payload.get("symbols", [])]
            representative = [
                candidate_by_ticker[ticker].symbol
                for ticker in configured_tickers
                if ticker in candidate_by_ticker
            ]
            candidate_items = [
                candidate_by_ticker[ticker]
                for ticker in configured_tickers
                if ticker in candidate_by_ticker
            ]

            symbol_news_count = sum(
                len(by_symbol.get(ticker, [])) for ticker in configured_tickers
            )
            raw_narrative_news_count = len(by_narrative.get(str(name), []))
            # A broad theme mention cannot heat every configured narrative in
            # the absence of a representative market candidate. When a
            # representative exists but no symbol-specific story does, retain
            # one contextual mention at most.
            narrative_news_count = (
                0 if not representative else
                min(raw_narrative_news_count, 1) if symbol_news_count == 0 else
                raw_narrative_news_count
            )
            catalyst_score = sum(
                catalysts.get(symbol, CatalystSummary(symbol=symbol)).importance_score
                for symbol in representative
            )

            attention_score = clamp(
                narrative_news_count * 18 + symbol_news_count * 12 + catalyst_score * 8
            )
            if symbol_news_count == 0 and catalyst_score == 0:
                attention_score = min(attention_score, 35.0)
            if candidate_items:
                momentum_score = clamp(
                    sum(item.score for item in candidate_items) / len(candidate_items)
                )
                volume_score = clamp(
                    sum(min((item.volume_ratio or 0) / 2, 1.5) * 100 for item in candidate_items)
                    / len(candidate_items)
                )
                risk_score = clamp(
                    sum(self._candidate_risk(item) for item in candidate_items)
                    / len(candidate_items)
                )
            else:
                momentum_score = 0.0
                volume_score = 0.0
                risk_score = 20.0 if attention_score > 0 else 0.0

            heat_score = clamp(
                attention_score * 0.35
                + momentum_score * 0.35
                + volume_score * 0.15
                - risk_score * 0.15
            )
            status = self._status(heat_score, risk_score, attention_score)
            evidence = []
            if narrative_news_count:
                evidence.append(f"{narrative_news_count} narrative-level news mention(s).")
            if symbol_news_count:
                evidence.append(f"{symbol_news_count} representative-symbol news mention(s).")
            if candidate_items:
                leaders = sorted(candidate_items, key=lambda item: item.score, reverse=True)[:3]
                evidence.append(
                    "Momentum leaders: "
                    + ", ".join(f"{item.symbol} {item.score}/100" for item in leaders)
                )
            warnings = []
            if raw_narrative_news_count and not representative:
                warnings.append(
                    "Broad narrative mentions ignored without a representative market candidate."
                )
            if risk_score >= 55:
                warnings.append("Narrative may be crowded or extended.")
            if attention_score >= 60 and momentum_score < 45:
                warnings.append("Attention is not supported by price momentum.")

            results[str(name)] = NarrativeSummary(
                narrative=str(name),
                attention_score=round(attention_score, 1),
                momentum_score=round(momentum_score, 1),
                volume_score=round(volume_score, 1),
                risk_score=round(risk_score, 1),
                heat_score=round(heat_score, 1),
                representative_symbols=representative,
                status=status,
                evidence=evidence or ["No meaningful fresh narrative evidence."],
                warnings=warnings,
            )

        results = dict(
            sorted(results.items(), key=lambda item: item[1].heat_score, reverse=True)
        )
        self.save_output({name: model_to_dict(item) for name, item in results.items()})
        return results

    @staticmethod
    def _candidate_risk(candidate: MomentumCandidate) -> float:
        risk = 20.0
        if candidate.distance_from_ema20_atr is not None and abs(candidate.distance_from_ema20_atr) > 2:
            risk += 35
        if candidate.volume_ratio is not None and candidate.volume_ratio < 0.5:
            risk += 15
        if candidate.return_24h is not None and candidate.return_24h > 8:
            risk += 20
        return clamp(risk)

    @staticmethod
    def _status(heat_score: float, risk_score: float, attention_score: float) -> str:
        if heat_score >= 70 and risk_score < 55:
            return "hot"
        if heat_score >= 50:
            return "rising"
        if attention_score >= 60 and risk_score >= 55:
            return "crowded/watch carefully"
        if heat_score <= 20:
            return "quiet"
        return "mixed"
