from __future__ import annotations

from typing import Any

from src.agents.base_agent import BaseAgent
from src.models import MomentumCandidate, SocialAttentionSummary
from src.utils.symbols import symbol_to_ticker
from src.utils.validation import clamp, model_to_dict


class SocialAttentionAgent(BaseAgent):
    name = "social_attention_agent"

    def run(
        self,
        mentions: list[dict[str, Any]],
        candidates: list[MomentumCandidate],
    ) -> dict[str, SocialAttentionSummary]:
        candidate_by_ticker = {symbol_to_ticker(item.symbol): item for item in candidates}
        grouped: dict[str, list[dict[str, Any]]] = {}
        for mention in mentions:
            for ticker in mention.get("symbols", []) or []:
                ticker = str(ticker).upper()
                if ticker in candidate_by_ticker:
                    grouped.setdefault(candidate_by_ticker[ticker].symbol, []).append(mention)

        results: dict[str, SocialAttentionSummary] = {}
        for symbol, rows in grouped.items():
            sources = sorted({str(row.get("source") or "unknown") for row in rows})
            raw_score = 0.0
            titles: list[str] = []
            for row in rows:
                raw_score += 8
                raw_score += min(float(row.get("score") or 0) / 20, 12)
                raw_score += min(float(row.get("comments") or 0) / 10, 10)
                title = str(row.get("title") or "")
                if title:
                    titles.append(title)
            candidate = next((item for item in candidates if item.symbol == symbol), None)
            warnings = []
            if candidate and candidate.volume_ratio is not None and candidate.volume_ratio < 0.8 and raw_score > 25:
                warnings.append("Social attention is not backed by above-average spot volume.")
            if candidate and candidate.distance_from_ema20_atr is not None and abs(candidate.distance_from_ema20_atr) > 2:
                warnings.append("Crowd attention may be arriving after an extended move.")

            results[symbol] = SocialAttentionSummary(
                symbol=symbol,
                mention_count=len(rows),
                attention_score=round(clamp(raw_score), 1),
                sources=sources,
                top_mentions=titles[:5],
                warnings=warnings,
            )

        results = dict(sorted(results.items(), key=lambda item: item[1].attention_score, reverse=True))
        self.save_output({symbol: model_to_dict(item) for symbol, item in results.items()})
        return results
