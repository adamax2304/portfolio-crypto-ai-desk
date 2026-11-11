from __future__ import annotations

import re
import sqlite3
from typing import Any

from .config import QualityAgentsConfig
from .helpers import make_verdict
from .schemas import AgentVerdict, SignalContext, Verdict


def _number(value: Any) -> float | None:
    try:
        return None if value in (None, "") else float(value)
    except (TypeError, ValueError):
        return None


class ExecutionSanityAgent:
    name = "execution_sanity"
    version = "execution_sanity_quality_v1"

    def evaluate(
        self, conn: sqlite3.Connection, context: SignalContext, cfg: QualityAgentsConfig,
    ) -> AgentVerdict:
        del conn
        hard: list[str] = []
        caution: list[str] = []
        symbol = context.symbol
        if not symbol or not re.fullmatch(r"[A-Z0-9.]{1,24}(?:/[A-Z0-9]{2,8})?", symbol):
            hard.append("INVALID_SYMBOL")
        if context.direction not in {"long", "short"}:
            hard.append("INVALID_DIRECTION")

        payload = context.payload
        entry = _number(payload.get("entry_used") or payload.get("entry_price") or context.signal.get("suggested_entry"))
        stop = _number(payload.get("stop") or payload.get("original_stop") or context.signal.get("stop_loss"))
        targets = [
            _number(payload.get(key) if payload.get(key) not in (None, "") else context.signal.get(key))
            for key in ("tp1", "tp2", "tp3")
        ]
        if context.stage.startswith("live_"):
            if any(value is None for value in [entry, stop, *targets]):
                hard.append("MISSING_GEOMETRY")
            elif not (
                stop < entry < targets[0] < targets[1] < targets[2]
                if context.direction == "long"
                else targets[2] < targets[1] < targets[0] < entry < stop
            ):
                hard.append("INVALID_DIRECTIONAL_GEOMETRY")
            if payload.get("current_price_revalidated") is not True:
                hard.append("CURRENT_PRICE_NOT_REVALIDATED")
            if str(payload.get("entry_time_basis") or "") != "point_in_time_current_bar":
                caution.append("ENTRY_NOT_POINT_IN_TIME")
            age = _number(payload.get("entry_age_seconds"))
            if age is None or age < 0:
                caution.append("ENTRY_AGE_UNAVAILABLE")
            size = _number(payload.get("size_weight"))
            if size is None or size <= 0:
                hard.append("INVALID_RISK_SIZE")

        evidence = {
            "stage": context.stage,
            "symbol": symbol,
            "direction": context.direction,
            "entry_mode": context.entry_mode,
            "entry": entry,
            "stop": stop,
            "targets": targets,
            "entry_age_seconds": _number(payload.get("entry_age_seconds")),
            "entry_time_basis": payload.get("entry_time_basis"),
            "current_price_revalidated": payload.get("current_price_revalidated"),
            "size_weight": _number(payload.get("size_weight")),
        }
        if hard:
            return make_verdict(
                name=self.name, version=self.version, verdict=Verdict.BLOCK_HARD,
                confidence=0.99, reason_codes=hard + caution, evidence=evidence,
                context=context, cfg=cfg,
            )
        if caution:
            return make_verdict(
                name=self.name, version=self.version, verdict=Verdict.CAUTION,
                confidence=0.88, reason_codes=caution, evidence=evidence,
                context=context, cfg=cfg,
            )
        return make_verdict(
            name=self.name, version=self.version, verdict=Verdict.PASS,
            confidence=0.98, reason_codes=["EXECUTION_INPUTS_VALID"], evidence=evidence,
            context=context, cfg=cfg,
        )
