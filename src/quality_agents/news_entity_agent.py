from __future__ import annotations

import sqlite3
from typing import Any

from .config import QualityAgentsConfig
from .helpers import compact_event, make_verdict, matching_news_events
from .schemas import AgentVerdict, SignalContext, Verdict


class NewsEntityAgent:
    name = "news_entity"
    version = "news_entity_quality_v1"

    def evaluate(
        self, conn: sqlite3.Connection, context: SignalContext, cfg: QualityAgentsConfig,
    ) -> AgentVerdict:
        events = matching_news_events(conn, context)
        news_claimed = bool(
            context.signal.get("news_supported")
            or context.payload.get("news_supported")
            or context.payload.get("catalyst_supported")
        )
        evidence: dict[str, Any] = {
            "symbol": context.symbol,
            "news_claimed": news_claimed,
            "matched_event_count": len(events),
            "events": [compact_event(row) for row in events[:5]],
        }
        if not events:
            verdict = Verdict.CAUTION if news_claimed else Verdict.INSUFFICIENT_DATA
            reason = "CATALYST_ENTITY_UNVERIFIED" if news_claimed else "NO_MATCHED_NEWS_EVENT"
            return make_verdict(
                name=self.name, version=self.version, verdict=verdict,
                confidence=0.82 if news_claimed else 0.55, reason_codes=[reason],
                evidence=evidence, context=context, cfg=cfg,
            )

        usable = [row for row in events if row.get("supports_mode")]
        linked = [row for row in usable if bool(row.get("linkage_allowed"))]
        directions = {str(row.get("direction_hint") or "neutral").lower() for row in linked}
        aligned_hint = "bullish" if context.direction == "long" else "bearish"
        aligned = aligned_hint in directions
        opposed = (
            context.direction == "long" and "bearish" in directions
        ) or (
            context.direction == "short" and "bullish" in directions
        )
        evidence.update({
            "mode_usable_count": len(usable),
            "linkage_allowed_count": len(linked),
            "direction_hints": sorted(directions),
        })
        if opposed:
            return make_verdict(
                name=self.name, version=self.version, verdict=Verdict.CAUTION,
                confidence=0.8, reason_codes=["NEWS_DIRECTION_CONFLICT"],
                evidence=evidence, context=context, cfg=cfg,
            )
        if not usable:
            return make_verdict(
                name=self.name, version=self.version, verdict=Verdict.CAUTION,
                confidence=0.78, reason_codes=["NEWS_NOT_USABLE_FOR_HORIZON"],
                evidence=evidence, context=context, cfg=cfg,
            )
        if not linked:
            return make_verdict(
                name=self.name, version=self.version, verdict=Verdict.CAUTION,
                confidence=0.76, reason_codes=["NEWS_LINKAGE_NOT_TRUSTED"],
                evidence=evidence, context=context, cfg=cfg,
            )
        if aligned:
            return make_verdict(
                name=self.name, version=self.version, verdict=Verdict.SUPPORT,
                confidence=max(float(row.get("confidence") or 0.0) for row in linked),
                reason_codes=["TRUSTED_DIRECTIONAL_NEWS"], evidence=evidence,
                context=context, cfg=cfg,
            )
        return make_verdict(
            name=self.name, version=self.version, verdict=Verdict.PASS,
            confidence=0.7, reason_codes=["TRUSTED_NEWS_NEUTRAL"], evidence=evidence,
            context=context, cfg=cfg,
        )
