from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .config import LLMRouterConfig
from .schemas import FinancialReasoning, LLMTaskContext, LLMTier, Stakes


class RoutingPolicyError(RuntimeError):
    pass


@dataclass(frozen=True)
class RoutingDecision:
    tier: LLMTier
    reason: str


_ROUTINE_TASKS = {
    "classification", "entity_identification", "extraction", "news_categorization",
    "news_event_classification", "normalization", "parsing", "simple_comparison",
    "simple_financial_extraction", "structured_json", "summarization", "validation",
}
_ANALYST_TASKS = {
    "catalyst_analysis", "earnings_analysis", "financial_news_interpretation",
    "fundamental_analysis", "macro_analysis", "market_regime_interpretation",
    "multi_source_financial_reasoning", "portfolio_analysis",
    "preus_trade_setup_analysis", "trade_setup_analysis", "trade_thesis_synthesis",
}
_FORBIDDEN_MODEL_KEYS = {"model", "model_id", "requested_model", "provider_model"}


def _reject_concrete_model_request(task: LLMTaskContext, cfg: LLMRouterConfig) -> None:
    requested = {
        str(value).strip()
        for key, value in task.metadata.items()
        if str(key).lower() in _FORBIDDEN_MODEL_KEYS and value is not None
    }
    if requested:
        raise RoutingPolicyError(
            "agents may not request a concrete model; supply task metadata to the router"
        )
    if len(cfg.allowed_models) != 3:
        raise RoutingPolicyError("production model whitelist must contain exactly three models")


def select_primary_tier(task: LLMTaskContext, cfg: LLMRouterConfig) -> RoutingDecision:
    _reject_concrete_model_request(task, cfg)
    task_type = task.task_type.strip().lower()
    if task_type in _ROUTINE_TASKS:
        return RoutingDecision(LLMTier.ROUTINE, f"known_routine_task:{task_type}")
    if task.financial_reasoning == FinancialReasoning.DATA_PROCESSING:
        return RoutingDecision(LLMTier.ROUTINE, "finance_data_processing_not_interpretation")
    if task_type in _ANALYST_TASKS:
        return RoutingDecision(LLMTier.ANALYST, f"known_financial_reasoning_task:{task_type}")
    if task.financial_reasoning in {
        FinancialReasoning.INTERPRETATION, FinancialReasoning.SYNTHESIS,
    }:
        return RoutingDecision(
            LLMTier.ANALYST,
            f"financial_{task.financial_reasoning.value}",
        )
    if task.source_count >= 3 and task.financial_reasoning != FinancialReasoning.NONE:
        return RoutingDecision(LLMTier.ANALYST, "multi_source_financial_context")
    return RoutingDecision(LLMTier.ROUTINE, "default_routine")


def _confidence(payload: dict[str, Any], task: LLMTaskContext) -> float | None:
    value = payload.get("confidence", task.previous_confidence)
    try:
        return max(0.0, min(1.0, float(value))) if value is not None else None
    except (TypeError, ValueError):
        return None


def select_independent_review(
    task: LLMTaskContext,
    primary_payload: dict[str, Any],
    primary_tier: LLMTier,
    cfg: LLMRouterConfig,
) -> str | None:
    if primary_tier != LLMTier.ANALYST:
        return None
    if task.independent_review_requested:
        return "explicit_independent_review"
    confidence = _confidence(primary_payload, task)
    low_threshold = float(cfg.block("policy").get("low_confidence_threshold") or 0.45)
    high_stakes = task.stakes in {Stakes.HIGH, Stakes.MATERIAL}
    ambiguity = task.ambiguity.strip().lower() in {"high", "unresolved", "material"}
    unresolved = bool(
        primary_payload.get("unresolved_contradictions")
        or primary_payload.get("unsupported_claims")
        or primary_payload.get("validation_failed")
    )
    if task.evidence_conflict and high_stakes and (ambiguity or unresolved):
        return "high_stakes_conflicting_evidence"
    if high_stakes and ambiguity and unresolved:
        return "model_reported_unresolved_contradictions"
    if task.evidence_conflict and confidence is not None and confidence < low_threshold:
        return "conflicting_evidence_low_confidence"
    if task.previous_attempt_failed and task.evidence_conflict and ambiguity:
        return "repeated_reasoning_failure_with_conflict"
    if task.task_type == "post_trade_forensic_analysis" and task.evidence_conflict and ambiguity:
        return "complex_post_trade_forensics"
    return None


__all__ = [
    "RoutingDecision",
    "RoutingPolicyError",
    "select_independent_review",
    "select_primary_tier",
]
