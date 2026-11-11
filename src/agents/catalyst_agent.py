from __future__ import annotations

import json
from datetime import date, datetime, timedelta
from typing import Any

from src.agents.base_agent import BaseAgent
from src.models import CatalystSummary
from src.utils.symbols import symbol_to_ticker
from src.utils.validation import model_to_dict


class CatalystAgent(BaseAgent):
    name = "catalyst_agent"

    def run(
        self,
        symbols: list[str],
        events: list[dict[str, Any]],
        news_output: dict[str, Any],
    ) -> dict[str, CatalystSummary]:
        today = date.today()
        ticker_to_symbol = {symbol_to_ticker(symbol): symbol for symbol in symbols}
        results = {
            symbol: CatalystSummary(symbol=symbol)
            for symbol in symbols
        }

        for event in events:
            ticker = str(event.get("ticker") or "").upper()
            symbol = ticker_to_symbol.get(ticker)
            if not symbol:
                continue
            event_date = self._parse_date(event.get("event_date") or event.get("date"))
            if event_date and not (today - timedelta(days=2) <= event_date <= today + timedelta(days=7)):
                continue
            event_type = str(event.get("event_type") or event.get("type") or "other").lower()
            text = f"{event_type}: {event.get('event') or ''}"
            importance = float(event.get("importance") or 1)
            summary = results[symbol]
            if event_type in {"unlock", "delisting", "migration"}:
                summary.risk_events.append(text)
                summary.warnings.append(f"Event risk detected: {text}")
            else:
                summary.catalysts.append(text)
            summary.importance_score += importance
            summary.verification_status = "manual_event"

        by_symbol = news_output.get("by_symbol", {})
        for ticker, items in by_symbol.items():
            symbol = ticker_to_symbol.get(str(ticker).upper())
            if not symbol:
                continue
            summary = results[symbol]
            for item in items[:3]:
                title = item.get("title", "")
                source = item.get("source", "")
                summary.catalysts.append(f"news: {title} ({source})")
                summary.importance_score += float(item.get("importance") or 1) * 0.5
            if summary.verification_status == "none":
                summary.verification_status = (
                    "canonical_news_event" if news_output.get("canonical_policy_active") else "news_mention")

        # Canonical risk events are never appended to the positive catalyst
        # list. They remain visible to critic/reporting as explicit risk.
        for ticker, items in (news_output.get("risk_by_symbol") or {}).items():
            symbol = ticker_to_symbol.get(str(ticker).upper())
            if not symbol:
                continue
            summary = results[symbol]
            for item in items[:3]:
                meta = item.get("canonical_event") or {}
                text = f"{meta.get('event_type') or 'news_risk'}: {item.get('title', '')}"
                if text not in summary.risk_events:
                    summary.risk_events.append(text)
                summary.warnings.append(f"Canonical news risk: {text}")
            if summary.verification_status == "none":
                summary.verification_status = "canonical_risk_event"

        for summary in results.values():
            if summary.risk_events:
                summary.interpretation = "fresh catalyst exists but risk events require caution"
            elif summary.catalysts:
                summary.interpretation = "fresh attention/catalyst detected"
            summary.importance_score = round(summary.importance_score, 2)

        self.save_output({symbol: model_to_dict(item) for symbol, item in results.items()})
        return results

    @staticmethod
    def _parse_date(value: Any) -> date | None:
        if not value:
            return None
        if isinstance(value, date) and not isinstance(value, datetime):
            return value
        try:
            return datetime.fromisoformat(str(value)[:10]).date()
        except Exception:
            return None
