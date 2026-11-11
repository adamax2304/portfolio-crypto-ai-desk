from __future__ import annotations

import sqlite3

from .config import QualityAgentsConfig
from .helpers import compact_event, make_verdict, matching_news_events
from .schemas import AgentVerdict, SignalContext, Verdict


class EventRiskAgent:
    name = "event_risk"
    version = "event_risk_quality_v1"

    _HALT_TYPES = {"delisting", "maintenance"}
    _HIGH_RISK_TYPES = {"exploit_hack", "legal_risk", "fda_clinical"}
    _CAUTION_TYPES = {
        "offering_dilution", "earnings", "guidance", "management_change",
        "token_unlock", "geopolitical_risk", "fed", "cpi", "pce", "jobs",
    }

    def evaluate(
        self, conn: sqlite3.Connection, context: SignalContext, cfg: QualityAgentsConfig,
    ) -> AgentVerdict:
        events = matching_news_events(conn, context)
        risky = [
            row for row in events
            if str(row.get("risk_action") or "none") != "none"
            or str(row.get("event_type") or "") in self._HALT_TYPES | self._HIGH_RISK_TYPES | self._CAUTION_TYPES
        ]
        evidence = {
            "symbol": context.symbol,
            "risk_event_count": len(risky),
            "events": [compact_event(row) for row in risky[:5]],
        }
        if not risky:
            return make_verdict(
                name=self.name, version=self.version, verdict=Verdict.PASS,
                confidence=0.72, reason_codes=["NO_ACTIVE_EVENT_RISK"],
                evidence=evidence, context=context, cfg=cfg,
            )

        types = {str(row.get("event_type") or "") for row in risky}
        active_halt = any(
            str(row.get("event_type") or "") in self._HALT_TYPES
            and str(row.get("risk_action") or "") == "operator_review"
            for row in risky
        )
        if active_halt:
            return make_verdict(
                name=self.name, version=self.version, verdict=Verdict.BLOCK_HARD,
                confidence=0.94, reason_codes=["EVENT_HALT_ACTIVE"],
                evidence={**evidence, "event_types": sorted(types)},
                context=context, cfg=cfg,
            )
        reason_codes: list[str] = []
        if types & self._HIGH_RISK_TYPES:
            reason_codes.append("MATERIAL_EVENT_RISK")
        if "offering_dilution" in types and context.direction == "long":
            reason_codes.append("DILUTION_RISK_LONG")
        if "earnings" in types:
            reason_codes.append("EARNINGS_EVENT_RISK")
        if types & {"fed", "cpi", "pce", "jobs", "geopolitical_risk"}:
            reason_codes.append("MACRO_EVENT_RISK")
        if not reason_codes:
            reason_codes.append("EVENT_RISK_REVIEW")
        return make_verdict(
            name=self.name, version=self.version, verdict=Verdict.CAUTION,
            confidence=0.82, reason_codes=reason_codes,
            evidence={**evidence, "event_types": sorted(types)},
            context=context, cfg=cfg,
        )
