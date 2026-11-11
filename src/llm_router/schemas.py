from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class LLMTier(str, Enum):
    ROUTINE = "routine"
    ANALYST = "analyst"
    REVIEW = "review"


class FinancialReasoning(str, Enum):
    NONE = "none"
    DATA_PROCESSING = "data_processing"
    INTERPRETATION = "interpretation"
    SYNTHESIS = "synthesis"


class Complexity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Stakes(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    MATERIAL = "material"


@dataclass(frozen=True)
class LLMTaskContext:
    agent_name: str
    task_type: str
    system_prompt: str
    user_payload: dict[str, Any]
    financial_reasoning: FinancialReasoning = FinancialReasoning.NONE
    complexity: Complexity = Complexity.LOW
    stakes: Stakes = Stakes.LOW
    ambiguity: str = "low"
    evidence_conflict: bool = False
    requires_tools: bool = False
    requires_vision: bool = False
    requires_structured_output: bool = True
    source_count: int = 1
    context_length: int | None = None
    previous_attempt_failed: bool = False
    previous_confidence: float | None = None
    independent_review_requested: bool = False
    tools: list[dict[str, Any]] = field(default_factory=list)
    image_urls: list[str] = field(default_factory=list)
    web_search: bool = False
    signal_id: str | None = None
    asset_class: str | None = None
    symbol: str | None = None
    mode: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def replay_payload(self) -> dict[str, Any]:
        return {
            "agent_name": self.agent_name,
            "task_type": self.task_type,
            "system_prompt": self.system_prompt,
            "user_payload": self.user_payload,
            "financial_reasoning": self.financial_reasoning.value,
            "complexity": self.complexity.value,
            "stakes": self.stakes.value,
            "ambiguity": self.ambiguity,
            "evidence_conflict": self.evidence_conflict,
            "requires_tools": self.requires_tools,
            "requires_vision": self.requires_vision,
            "requires_structured_output": self.requires_structured_output,
            "source_count": self.source_count,
            "context_length": self.context_length,
            "previous_attempt_failed": self.previous_attempt_failed,
            "previous_confidence": self.previous_confidence,
            "independent_review_requested": self.independent_review_requested,
            "tools": self.tools,
            "image_urls": self.image_urls,
            "web_search": self.web_search,
            "signal_id": self.signal_id,
            "asset_class": self.asset_class,
            "symbol": self.symbol,
            "mode": self.mode,
            "metadata": self.metadata,
        }

    @classmethod
    def from_replay_payload(cls, raw: dict[str, Any]) -> "LLMTaskContext":
        return cls(
            agent_name=str(raw["agent_name"]),
            task_type=str(raw["task_type"]),
            system_prompt=str(raw["system_prompt"]),
            user_payload=dict(raw.get("user_payload") or {}),
            financial_reasoning=FinancialReasoning(raw.get("financial_reasoning", "none")),
            complexity=Complexity(raw.get("complexity", "low")),
            stakes=Stakes(raw.get("stakes", "low")),
            ambiguity=str(raw.get("ambiguity") or "low"),
            evidence_conflict=bool(raw.get("evidence_conflict", False)),
            requires_tools=bool(raw.get("requires_tools", False)),
            requires_vision=bool(raw.get("requires_vision", False)),
            requires_structured_output=bool(raw.get("requires_structured_output", True)),
            source_count=max(0, int(raw.get("source_count") or 0)),
            context_length=raw.get("context_length"),
            previous_attempt_failed=bool(raw.get("previous_attempt_failed", False)),
            previous_confidence=raw.get("previous_confidence"),
            independent_review_requested=bool(raw.get("independent_review_requested", False)),
            tools=list(raw.get("tools") or []),
            image_urls=list(raw.get("image_urls") or []),
            web_search=bool(raw.get("web_search", False)),
            signal_id=raw.get("signal_id"),
            asset_class=raw.get("asset_class"),
            symbol=raw.get("symbol"),
            mode=raw.get("mode"),
            metadata=dict(raw.get("metadata") or {}),
        )


@dataclass(frozen=True)
class LLMCallResult:
    request_id: str
    payload: dict[str, Any]
    text: str
    tier: LLMTier
    model: str
    routing_reason: str
    latency_ms: float
    input_tokens: int
    output_tokens: int
    cost_usd: float
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    structured_output_valid: bool = True
    retry_count: int = 0
    confidence: float | None = None


@dataclass(frozen=True)
class LLMRouterResult:
    primary: LLMCallResult
    review: LLMCallResult | None = None
    model_disagreement: bool = False
    disagreement_fields: tuple[str, ...] = ()
    escalation_reason: str | None = None

    @property
    def payload(self) -> dict[str, Any]:
        return self.primary.payload

    @property
    def model(self) -> str:
        return self.primary.model

    @property
    def latency_ms(self) -> float:
        return self.primary.latency_ms

