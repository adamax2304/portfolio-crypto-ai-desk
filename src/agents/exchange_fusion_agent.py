"""Cross-exchange fusion: turn per-venue candidate data into a confirmation score.

For each fused candidate the agent decides:

* which exchanges actually list the symbol (anchor / derivatives / discovery),
* whether the move is consistent across venues (price + volume agreement),
* what data confidence the desk should claim,
* the best exchange to read structure from, and
* whether MEXC-only / poor-anchor flags should downgrade the idea.

Outputs feed into ScoringAgent (caps + bonuses), TradeIdeaAgent (evidence
block, exchange focus, data confidence), and the report (multi-exchange
confirmation table + rejected reasons).
"""

from __future__ import annotations

from typing import Any

from src.agents.base_agent import BaseAgent
from src.models import ExchangeConfirmation
from src.utils.validation import clamp, model_to_dict


class ExchangeFusionAgent(BaseAgent):
    name = "exchange_fusion_agent"

    def run(
        self,
        fused_candidates: list[dict[str, Any]],
        exchange_symbol_map: dict[str, list[str]] | None = None,
    ) -> dict[str, ExchangeConfirmation]:
        exchange_symbol_map = exchange_symbol_map or {}
        anchor = self.config.anchor_exchange
        high_risk = self.config.high_risk_exchanges
        # Derivative-role exchanges (Bybit etc.) — anything not anchor and not high_risk.
        derivative_exchanges = {
            exchange
            for exchange in self.config.enabled_exchanges
            if exchange != anchor and exchange not in high_risk
        }
        results: dict[str, ExchangeConfirmation] = {}

        for row in fused_candidates:
            symbol = str(row.get("symbol"))
            per_exchange: dict[str, dict[str, Any]] = row.get("per_exchange") or {}
            listed = sorted(per_exchange.keys() or exchange_symbol_map.get(symbol, []))
            anchor_listed = anchor in per_exchange
            derivatives_listed = any(exchange in derivative_exchanges for exchange in per_exchange)
            discovery_listed = any(exchange in high_risk for exchange in per_exchange)
            high_risk_only = bool(listed) and all(exchange in high_risk for exchange in listed)

            changes = [
                float(item.get("change_24h"))
                for item in per_exchange.values()
                if item.get("change_24h") is not None
            ]
            volumes = [
                float(item.get("volume_anomaly") or 0)
                for item in per_exchange.values()
            ]
            price_consistency = self._consistency(changes)
            volume_consistency = self._consistency(volumes, tolerance=0.6)

            confirmation_score = self._confirmation_score(
                anchor_listed=anchor_listed,
                derivatives_listed=derivatives_listed,
                discovery_listed=discovery_listed,
                price_consistency=price_consistency,
                volume_consistency=volume_consistency,
                listed_count=len(listed),
                high_risk_only=high_risk_only,
            )

            best_exchange = self._pick_best_exchange(per_exchange, anchor)
            focus = self._pick_focus_exchange(
                per_exchange, anchor, derivative_exchanges, high_risk
            )

            risk_flags: list[str] = []
            if high_risk_only:
                risk_flags.append("mexc_only")
            if not anchor_listed and not high_risk_only:
                risk_flags.append("not_on_anchor")
            if listed and not derivatives_listed and not high_risk_only:
                risk_flags.append("no_derivatives_confirmation")
            if changes and price_consistency < 0.5:
                risk_flags.append("price_divergence_across_exchanges")

            interpretation = self._interpret(
                anchor_listed=anchor_listed,
                derivatives_listed=derivatives_listed,
                high_risk_only=high_risk_only,
                price_consistency=price_consistency,
            )

            results[symbol] = ExchangeConfirmation(
                symbol=symbol,
                exchanges_listed=listed,
                anchor_listed=anchor_listed,
                derivatives_listed=derivatives_listed,
                discovery_listed=discovery_listed,
                high_risk_only=high_risk_only,
                price_consistency=round(price_consistency, 2),
                volume_consistency=round(volume_consistency, 2),
                confirmation_score=round(confirmation_score, 1),
                best_exchange_for_data=best_exchange,
                suggested_exchange_focus=focus,
                risk_flags=risk_flags,
                interpretation=interpretation,
            )

        self.save_output({symbol: model_to_dict(item) for symbol, item in results.items()})
        return results

    @staticmethod
    def _consistency(values: list[float], tolerance: float = 0.4) -> float:
        if len(values) <= 1:
            return 0.5
        avg = sum(values) / len(values)
        if avg == 0:
            return 0.5
        spread = max(values) - min(values)
        rel = abs(spread) / max(abs(avg), tolerance)
        return clamp(1.0 - min(rel, 1.5), 0.0, 1.0)

    def _confirmation_score(
        self,
        anchor_listed: bool,
        derivatives_listed: bool,
        discovery_listed: bool,
        price_consistency: float,
        volume_consistency: float,
        listed_count: int,
        high_risk_only: bool,
    ) -> float:
        score = 30.0
        if anchor_listed:
            score += 30
        if derivatives_listed:
            score += 20
        if discovery_listed and not high_risk_only:
            score += 8
        if listed_count >= 3:
            score += 10
        elif listed_count >= 2:
            score += 5
        score += price_consistency * 10
        score += volume_consistency * 6
        if high_risk_only:
            score = min(score, 55)
        return clamp(score)

    @staticmethod
    def _pick_best_exchange(per_exchange: dict[str, dict[str, Any]], anchor: str) -> str:
        if not per_exchange:
            return ""
        if anchor in per_exchange:
            return anchor
        return max(
            per_exchange.items(),
            key=lambda pair: float(pair[1].get("liquidity_score") or 0),
        )[0]

    @staticmethod
    def _pick_focus_exchange(
        per_exchange: dict[str, dict[str, Any]],
        anchor: str,
        derivative_exchanges: set[str],
        high_risk: set[str],
    ) -> str:
        # Prefer anchor (best structure), fall back to a derivatives venue, then any.
        if anchor in per_exchange:
            return anchor
        for exchange in per_exchange:
            if exchange in derivative_exchanges:
                return exchange
        for exchange in per_exchange:
            if exchange not in high_risk:
                return exchange
        return next(iter(per_exchange.keys()), "")

    @staticmethod
    def _interpret(
        anchor_listed: bool,
        derivatives_listed: bool,
        high_risk_only: bool,
        price_consistency: float,
    ) -> str:
        if high_risk_only:
            return "MEXC-only; treat as speculative discovery, demand confirmation from anchor or Bybit."
        if anchor_listed and derivatives_listed and price_consistency >= 0.7:
            return "Anchor + derivatives confirm; move is consistent across venues."
        if anchor_listed and not derivatives_listed:
            return "Anchor listed but no derivatives confirmation; healthier than MEXC-only but no positioning data."
        if not anchor_listed:
            return "Not listed on anchor exchange; reduce confidence and prefer focus venue."
        if price_consistency < 0.5:
            return "Price divergence across exchanges; one venue may be lagging or fake."
        return "Mixed cross-exchange picture; rely on best_exchange_for_data."
