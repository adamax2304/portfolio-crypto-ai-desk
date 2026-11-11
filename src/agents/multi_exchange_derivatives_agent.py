from __future__ import annotations

from typing import Any

from src.agents.base_agent import BaseAgent
from src.models import MultiExchangeDerivativesSummary
from src.utils.validation import model_to_dict


class MultiExchangeDerivativesAgent(BaseAgent):
    name = "multi_exchange_derivatives_agent"

    def run(
        self,
        records: dict[str, dict[str, Any]],
        bybit_history: dict[str, dict[str, Any]] | None = None,
    ) -> dict[str, MultiExchangeDerivativesSummary]:
        bybit_history = bybit_history or {}
        results: dict[str, MultiExchangeDerivativesSummary] = {}
        for symbol, record in records.items():
            exchanges = dict(record.get("exchanges", {}) or {})
            history = bybit_history.get(symbol) or {}
            if history.get("data_available"):
                # Enrich the cheap ticker snapshot with derived history metrics.
                bybit_block = exchanges.get("bybit") or {}
                for key in (
                    "oi_change_pct_24h",
                    "funding_percentile",
                    "funding_recent_mean",
                    "interpretation",
                ):
                    if history.get(key) is not None:
                        bybit_block[key] = history[key]
                if "funding_rate" not in bybit_block and history.get("funding_rate") is not None:
                    bybit_block["funding_rate"] = history["funding_rate"]
                exchanges["bybit"] = bybit_block
            funding_rates: dict[str, float] = {}
            oi_values: dict[str, float] = {}
            warnings = []

            for exchange, payload in exchanges.items():
                funding = payload.get("funding_rate")
                if isinstance(funding, (int, float)):
                    funding_rates[str(exchange)] = float(funding)
                oi_value = (
                    payload.get("open_interest_value")
                    or payload.get("open_interest_usd")
                    or payload.get("open_interest")
                )
                if isinstance(oi_value, (int, float)):
                    oi_values[str(exchange)] = float(oi_value)

            if not exchanges:
                consensus = "no Bybit/OKX derivatives data"
                warnings.append("External derivatives venues unavailable for this symbol.")
            elif funding_rates:
                avg_funding = sum(funding_rates.values()) / len(funding_rates)
                if avg_funding > 0.0005:
                    consensus = "positive funding across external venues"
                elif avg_funding < -0.0003:
                    consensus = "negative funding across external venues"
                else:
                    consensus = "external funding is neutral"
            else:
                consensus = "external OI/funding partial; treat as context only"
                warnings.append("Funding missing from external venues.")

            crowding_risk = "unknown"
            if funding_rates:
                max_abs = max(abs(item) for item in funding_rates.values())
                if max_abs >= 0.001:
                    crowding_risk = "elevated"
                    warnings.append("One external venue shows elevated funding.")
                elif max_abs >= 0.0005:
                    crowding_risk = "moderate"
                else:
                    crowding_risk = "low"

            # Bybit history adds OI delta + funding percentile context.
            bybit_block = exchanges.get("bybit") or {}
            funding_percentile = bybit_block.get("funding_percentile")
            if isinstance(funding_percentile, (int, float)):
                if funding_percentile >= 90:
                    warnings.append(
                        f"Bybit funding in {funding_percentile}th percentile vs 7d — crowded extreme."
                    )
                    crowding_risk = "elevated"
                elif funding_percentile <= 10:
                    warnings.append(
                        f"Bybit funding in {funding_percentile}th percentile vs 7d — possible squeeze fuel."
                    )
            oi_delta = bybit_block.get("oi_change_pct_24h")
            if isinstance(oi_delta, (int, float)) and abs(oi_delta) >= 10:
                direction_word = "expanding" if oi_delta > 0 else "unwinding"
                warnings.append(
                    f"Bybit OI {direction_word} {oi_delta}% over 24h — fresh positioning."
                )

            results[symbol] = MultiExchangeDerivativesSummary(
                symbol=symbol,
                exchanges_available=sorted(exchanges.keys()),
                funding_rates=funding_rates,
                open_interest_values=oi_values,
                consensus=consensus,
                crowding_risk=crowding_risk,
                warnings=warnings,
            )

        self.save_output({symbol: model_to_dict(item) for symbol, item in results.items()})
        return results
