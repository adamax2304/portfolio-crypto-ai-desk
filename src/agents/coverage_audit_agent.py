from __future__ import annotations

from typing import Any

from src.agents.base_agent import BaseAgent
from src.models import CoverageAudit, DerivativesSummary, SocialAttentionSummary
from src.utils.validation import model_to_dict


class CoverageAuditAgent(BaseAgent):
    name = "coverage_audit_agent"

    def run(
        self,
        latest_update: dict[str, Any],
        market_data: dict[str, Any],
        derivatives: dict[str, DerivativesSummary],
        social: dict[str, SocialAttentionSummary],
        multi_exchange_records: dict[str, dict[str, Any]],
    ) -> CoverageAudit:
        source_health: dict[str, str] = {}
        missing: list[str] = []
        partial: list[str] = []

        if market_data:
            source_health["ohlcv"] = f"ok: {len(market_data)} cached symbols"
        else:
            source_health["ohlcv"] = "missing"
            missing.append("OHLCV candles")

        failed_ohlcv = latest_update.get("failed", {})
        if failed_ohlcv:
            partial.append(f"OHLCV failures: {len(failed_ohlcv)} symbol/timeframe items")

        derivative_available = [item for item in derivatives.values() if item.data_available]
        if derivative_available:
            source_health["binance_futures"] = f"ok: {len(derivative_available)} symbols"
        else:
            source_health["binance_futures"] = "missing"
            missing.append("Binance futures funding/OI")
        if latest_update.get("derivatives_failed"):
            partial.append(f"Binance futures failures: {len(latest_update.get('derivatives_failed', {}))} symbols")

        if multi_exchange_records:
            venue_count = sum(len((record.get("exchanges") or {})) for record in multi_exchange_records.values())
            source_health["bybit_okx_derivatives"] = f"partial/ok: {venue_count} venue-symbol records"
        else:
            source_health["bybit_okx_derivatives"] = "missing"
            missing.append("Bybit/OKX funding/OI")
        if latest_update.get("multi_exchange_derivatives_failed"):
            partial.append("Some Bybit/OKX futures endpoints failed; check last_update.json.")

        news_sources = latest_update.get("news_sources", [])
        if news_sources:
            source_health["rss_news"] = f"ok: {len(news_sources)} sources"
        else:
            source_health["rss_news"] = "missing"
            missing.append("RSS news")
        if latest_update.get("news_failures"):
            partial.append(f"RSS failures: {', '.join(latest_update.get('news_failures', {}).keys())}")

        social_sources = latest_update.get("social_sources", [])
        if social_sources or social:
            source_health["social_attention"] = f"partial/ok: {len(social_sources)} live sources, {len(social)} symbols"
        else:
            source_health["social_attention"] = "missing"
            partial.append("No live social attention hits; crowd context may be thin.")
        if latest_update.get("social_failures"):
            partial.append(f"Social source failures: {', '.join(latest_update.get('social_failures', {}).keys())}")

        blindspots = [
            "Liquidation heatmaps and leverage clusters are not connected yet.",
            "Order book depth, spreads, and CVD are not connected yet.",
            "ETF flows, stablecoin liquidity, DXY/yields, and macro calendar are not connected yet.",
            "On-chain whale flows and exchange inflow/outflow are not connected yet.",
            "Token unlock calendar is manual until TokenUnlocks/CryptoRank integration is added.",
            "Live X/Telegram/Discord/KOL feeds are manual until API/connectors are added.",
        ]
        warnings = []
        if missing:
            warnings.append("Some evidence streams are missing; avoid high-confidence conclusions from incomplete data.")
        if partial:
            warnings.append("Some evidence streams are partial; inspect source health before trading.")

        audit = CoverageAudit(
            source_health=source_health,
            missing_sources=missing,
            stale_or_partial_sources=partial,
            important_blindspots=blindspots,
            warnings=warnings,
        )
        self.save_output(model_to_dict(audit))
        return audit
