from __future__ import annotations

import json
import sqlite3
from typing import Any

from .config import QualityAgentsConfig
from .helpers import make_verdict
from .schemas import AgentVerdict, SignalContext, Verdict
from .store import latest_llm_assessments


class LLMCachedAdvisoryAgent:
    name = "llm_cached_advisory"
    version = "llm_cached_advisory_v1"

    _VERDICT_MAP = {
        "SUPPORT": Verdict.SUPPORT,
        "PASS": Verdict.PASS,
        "CAUTION": Verdict.CAUTION,
        "BLOCK_HARD": Verdict.BLOCK_HARD,
        "INSUFFICIENT_DATA": Verdict.INSUFFICIENT_DATA,
    }

    def evaluate(
        self, conn: sqlite3.Connection, context: SignalContext, cfg: QualityAgentsConfig,
    ) -> AgentVerdict:
        rows = latest_llm_assessments(
            conn,
            signal_id=context.signal_id,
            asset_class=context.asset_class,
            symbol=context.symbol,
            decision_at=context.decision_at,
            limit=5,
        )
        if not rows:
            return make_verdict(
                name=self.name,
                version=self.version,
                verdict=Verdict.INSUFFICIENT_DATA,
                confidence=0.45,
                reason_codes=["LLM_ADVISORY_NOT_READY"],
                evidence={"symbol": context.symbol, "cached_assessments": 0},
                context=context,
                cfg=cfg,
                model="openrouter-cache",
                prompt_version=None,
            )
        parsed: list[dict[str, Any]] = []
        for row in rows:
            try:
                assessment = json.loads(row.get("assessment_json") or "{}")
            except (TypeError, json.JSONDecodeError):
                assessment = {}
            parsed.append({
                "assessment_id": row.get("assessment_id"),
                "scope": row.get("scope"),
                "target_key": row.get("target_key"),
                "created_at": row.get("created_at"),
                "expires_at": row.get("expires_at"),
                "model": row.get("model"),
                "verdict": str(row.get("verdict") or assessment.get("verdict") or "").upper(),
                "confidence": row.get("confidence"),
                "reason_codes": assessment.get("reason_codes") or [],
                "risk_action": assessment.get("risk_action"),
                "short_rationale": assessment.get("short_rationale"),
            })
        precedence = {"BLOCK_HARD": 0, "CAUTION": 1, "SUPPORT": 2, "PASS": 3, "INSUFFICIENT_DATA": 4}
        chosen = sorted(
            parsed,
            key=lambda item: (
                precedence.get(str(item.get("verdict") or "INSUFFICIENT_DATA"), 4),
                -float(item.get("confidence") or 0.0),
            ),
        )[0]
        verdict_text = str(chosen.get("verdict") or "INSUFFICIENT_DATA").upper()
        verdict = self._VERDICT_MAP.get(verdict_text, Verdict.INSUFFICIENT_DATA)
        codes = [
            f"LLM_{code}" if not str(code).startswith("LLM_") else str(code)
            for code in (chosen.get("reason_codes") or [])
        ]
        if not codes:
            codes = [f"LLM_{verdict_text}"]
        return make_verdict(
            name=self.name,
            version=self.version,
            verdict=verdict,
            confidence=float(chosen.get("confidence") or 0.0),
            reason_codes=codes,
            evidence={
                "symbol": context.symbol,
                "cached_assessments": len(parsed),
                "chosen": chosen,
                "assessments": parsed,
            },
            context=context,
            cfg=cfg,
            model=str(chosen.get("model") or "openrouter-cache"),
            prompt_version="cached_openrouter_advisory",
        )


__all__ = ["LLMCachedAdvisoryAgent"]
