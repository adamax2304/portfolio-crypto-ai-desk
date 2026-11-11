from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class Verdict(str, Enum):
    PASS = "PASS"
    SUPPORT = "SUPPORT"
    CAUTION = "CAUTION"
    BLOCK_HARD = "BLOCK_HARD"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"
    ERROR = "ERROR"


class ReducerAction(str, Enum):
    ALLOW = "ALLOW"
    ALLOW_HALF_SIZE = "ALLOW_HALF_SIZE"
    ALLOW_NO_CATALYST_BOOST = "ALLOW_NO_CATALYST_BOOST"
    BLOCK_HARD = "BLOCK_HARD"
    REVIEW_ONLY = "REVIEW_ONLY"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def parse_utc(value: Any) -> datetime | None:
    if value in (None, ""):
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"), default=str)


def content_hash(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def normalize_symbol(value: Any) -> str:
    text = str(value or "").strip().upper().replace("-", "/").replace("_", "/")
    if text.endswith("/USDT") or text.endswith("/USD") or text.endswith("/USDC"):
        return text
    return text


def base_symbol(value: Any) -> str:
    return normalize_symbol(value).split("/", 1)[0]


@dataclass(frozen=True)
class SignalContext:
    signal_id: str
    symbol: str
    asset_class: str
    mode: str
    direction: str
    entry_mode: str
    decision_at: datetime
    signal: dict[str, Any] = field(repr=False)
    payload: dict[str, Any] = field(repr=False)
    stage: str = "live_capture"
    runtime_cache: dict[str, Any] = field(default_factory=dict, repr=False, compare=False)

    @classmethod
    def from_records(
        cls,
        signal: dict[str, Any],
        payload: dict[str, Any] | None = None,
        *,
        decision_at: datetime | None = None,
        stage: str = "live_capture",
    ) -> "SignalContext":
        body = dict(payload or {})
        signal_id = str(body.get("signal_id") or signal.get("signal_id") or "").strip()
        event_time = decision_at
        if event_time is None:
            for key in (
                "decision_at",
                "captured_at",
                "entry_triggered_at",
                "entry_detected_at",
                "generated_at",
                "created_at",
            ):
                event_time = parse_utc(body.get(key)) or parse_utc(signal.get(key))
                if event_time is not None:
                    break
        event_time = event_time or utc_now()
        return cls(
            signal_id=signal_id,
            symbol=normalize_symbol(signal.get("symbol") or body.get("symbol")),
            asset_class=str(signal.get("asset_class") or body.get("asset_class") or "crypto").lower(),
            mode=str(signal.get("mode") or body.get("mode") or "").lower(),
            direction=str(signal.get("direction") or body.get("direction") or "").lower(),
            entry_mode=str(
                body.get("paper_execution_entry_mode")
                or body.get("entry_mode")
                or signal.get("paper_execution_entry_mode")
                or signal.get("entry_mode")
                or ""
            ).upper(),
            decision_at=event_time.astimezone(timezone.utc),
            signal=dict(signal),
            payload=body,
            stage=str(stage or "live_capture"),
        )

    def input_payload(self) -> dict[str, Any]:
        return {
            "signal_id": self.signal_id,
            "symbol": self.symbol,
            "asset_class": self.asset_class,
            "mode": self.mode,
            "direction": self.direction,
            "entry_mode": self.entry_mode,
            "decision_at": self.decision_at.isoformat(),
            "stage": self.stage,
            "signal": self.signal,
            "payload": self.payload,
        }

    @property
    def input_hash(self) -> str:
        return content_hash(self.input_payload())


@dataclass(frozen=True)
class AgentVerdict:
    agent_name: str
    agent_version: str
    verdict: Verdict
    confidence: float
    reason_codes: tuple[str, ...]
    evidence: dict[str, Any]
    created_at: datetime
    expires_at: datetime
    model: str = "deterministic"
    prompt_version: str | None = None

    def __post_init__(self) -> None:
        if not self.agent_name or not self.agent_version:
            raise ValueError("agent identity is required")
        if not 0.0 <= float(self.confidence) <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        if self.expires_at <= self.created_at:
            raise ValueError("expires_at must be after created_at")

    def output_payload(self) -> dict[str, Any]:
        return {
            "agent_name": self.agent_name,
            "agent_version": self.agent_version,
            "verdict": self.verdict.value,
            "confidence": round(float(self.confidence), 6),
            "reason_codes": list(self.reason_codes),
            "evidence": self.evidence,
            "created_at": self.created_at.isoformat(),
            "expires_at": self.expires_at.isoformat(),
            "model": self.model,
            "prompt_version": self.prompt_version,
        }

    @property
    def output_hash(self) -> str:
        return content_hash(self.output_payload())


@dataclass(frozen=True)
class ReducedDecision:
    recommended_action: ReducerAction
    applied_action: ReducerAction
    reason_codes: tuple[str, ...]
    verdict_ids: tuple[str, ...]
    operation_mode: str
    created_at: datetime

    def as_dict(self) -> dict[str, Any]:
        return {
            "recommended_action": self.recommended_action.value,
            "applied_action": self.applied_action.value,
            "reason_codes": list(self.reason_codes),
            "verdict_ids": list(self.verdict_ids),
            "operation_mode": self.operation_mode,
            "created_at": self.created_at.isoformat(),
        }
