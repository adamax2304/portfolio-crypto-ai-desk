from __future__ import annotations

import json
import os
import time
import uuid
from pathlib import Path
from typing import Any

from src.config import load_config

from .config import LLMRouterConfig, load_llm_router_config
from .policy import RoutingPolicyError, select_independent_review, select_primary_tier
from .provider import (
    LLMProviderError,
    OpenRouterProvider,
    ProviderResult,
    StructuredOutputError,
)
from .schemas import LLMCallResult, LLMRouterResult, LLMTaskContext, LLMTier
from .store import LLMRouterStore, stable_hash, utc_now_iso


class LLMRouterError(RuntimeError):
    pass


class _ProviderCallFailed(RuntimeError):
    def __init__(self, error: LLMProviderError, retry_count: int) -> None:
        super().__init__(str(error))
        self.error = error
        self.retry_count = retry_count


def _confidence(payload: dict[str, Any]) -> float | None:
    try:
        value = payload.get("confidence")
        return max(0.0, min(1.0, float(value))) if value is not None else None
    except (TypeError, ValueError):
        return None


def _normalized_signal(payload: dict[str, Any], field: str) -> str:
    value = str(payload.get(field) or "").strip().lower()
    aliases = {
        "long": "bullish", "buy": "bullish", "support": "support",
        "short": "bearish", "sell": "bearish", "block_hard": "block",
    }
    return aliases.get(value, value)


def compare_independent_analyses(
    primary: dict[str, Any], review: dict[str, Any],
) -> tuple[bool, tuple[str, ...]]:
    fields: list[str] = []
    p_direction = _normalized_signal(primary, "direction") or _normalized_signal(primary, "direction_hint")
    r_direction = _normalized_signal(review, "direction") or _normalized_signal(review, "direction_hint")
    if {p_direction, r_direction} == {"bullish", "bearish"}:
        fields.append("direction")
    p_verdict = _normalized_signal(primary, "verdict")
    r_verdict = _normalized_signal(review, "verdict")
    if (
        {p_verdict, r_verdict} & {"support", "approve", "proceed"}
        and {p_verdict, r_verdict} & {"block", "reject", "avoid"}
    ):
        fields.append("verdict")
    return bool(fields), tuple(fields)


class LLMRouter:
    def __init__(
        self,
        *,
        cfg: LLMRouterConfig | None = None,
        db_path: str | Path | None = None,
        provider: Any | None = None,
        store: LLMRouterStore | None = None,
    ) -> None:
        self.cfg = cfg or load_llm_router_config()
        path = Path(db_path or load_config().db_path)
        self.store = store or LLMRouterStore(path)
        if provider is None and self.cfg.enabled:
            env_name = str(self.cfg.raw.get("api_key_env") or "OPENROUTER_API_KEY")
            provider = OpenRouterProvider(cfg=self.cfg, api_key=os.getenv(env_name, "").strip())
        self.provider = provider

    def _enforce_budget(self, tier: LLMTier) -> None:
        budget = self.cfg.block("budget")
        if not bool(budget.get("enabled", False)):
            return
        spend = self.store.daily_spend()
        hard_total = float(budget.get("total_hard_daily_usd") or 0.0)
        tier_cap = float(budget.get(f"{tier.value}_daily_usd") or 0.0)
        provider_daily = None
        usage_reader = getattr(self.provider, "daily_usage_usd", None)
        if callable(usage_reader):
            try:
                provider_daily = usage_reader()
            except Exception:
                provider_daily = None
        effective_total = max(
            spend["total"],
            float(provider_daily) if provider_daily is not None else 0.0,
        )
        if hard_total > 0 and effective_total >= hard_total:
            raise LLMProviderError(
                f"llm_daily_budget_exhausted:total:{effective_total:.6f}>={hard_total:.6f}"
            )
        if tier_cap > 0 and spend[tier.value] >= tier_cap:
            raise LLMProviderError(
                f"llm_daily_budget_exhausted:{tier.value}:"
                f"{spend[tier.value]:.6f}>={tier_cap:.6f}"
            )

    def _record_attempt(
        self,
        *,
        request_id: str,
        task: LLMTaskContext,
        tier: LLMTier,
        purpose: str,
        attempt_number: int,
        result: ProviderResult | None = None,
        error: LLMProviderError | None = None,
    ) -> None:
        self.store.record_attempt({
            "attempt_id": str(uuid.uuid4()),
            "request_id": request_id,
            "timestamp": utc_now_iso(),
            "agent": task.agent_name,
            "task_type": task.task_type,
            "selected_tier": tier.value,
            "selected_model": self.cfg.model(tier).model_id,
            "purpose": purpose,
            "attempt_number": attempt_number,
            "status": "OK" if result is not None else "ERROR",
            "input_tokens": result.input_tokens if result else int(getattr(error, "input_tokens", 0)),
            "output_tokens": result.output_tokens if result else int(getattr(error, "output_tokens", 0)),
            "latency_ms": result.latency_ms if result else float(getattr(error, "latency_ms", 0.0)),
            "cost_usd": result.cost_usd if result else float(getattr(error, "cost_usd", 0.0)),
            "generation_id": result.generation_id if result else getattr(error, "generation_id", None),
            "error_type": None if result is not None else str(error),
        })

    def _repair_structured_output(
        self,
        *,
        request_id: str,
        task: LLMTaskContext,
        original_tier: LLMTier,
        original_error: StructuredOutputError,
        attempt_number: int,
    ) -> ProviderResult:
        """Repair formatting once on the routine tier without redoing analysis."""
        repair_tier = LLMTier.ROUTINE
        self._enforce_budget(repair_tier)
        repair_task = LLMTaskContext(
            agent_name=task.agent_name,
            task_type="structured_json",
            system_prompt=(
                "Convert the supplied model response into the requested JSON schema. "
                "Preserve its meaning, add no new financial claims, and return JSON only."
            ),
            user_payload={
                "original_response": original_error.raw_text[:12000],
                "required_schema": task.metadata.get("json_schema") or task.user_payload.get("output_schema"),
            },
            financial_reasoning=task.financial_reasoning,
            complexity=task.complexity,
            stakes=task.stakes,
            requires_structured_output=True,
            signal_id=task.signal_id,
            asset_class=task.asset_class,
            symbol=task.symbol,
            mode=task.mode,
            metadata={
                "max_tokens": min(400, int(task.metadata.get("max_tokens") or 400)),
                "temperature": 0,
                # Repair only the envelope. Repeating the original strict
                # schema can reproduce an empty completion on the same route.
                "disable_reasoning": True,
                "max_retries": 0,
            },
        )
        try:
            repaired = self.provider.call(
                model=self.cfg.model(repair_tier),
                task=repair_task,
                timeout_seconds=float(self.cfg.block("request").get("timeout_seconds") or 30),
                max_tokens=int(repair_task.metadata["max_tokens"]),
                temperature=0.0,
            )
        except LLMProviderError as exc:
            self._record_attempt(
                request_id=request_id,
                task=task,
                tier=repair_tier,
                purpose="structured_output_repair",
                attempt_number=attempt_number,
                error=exc,
            )
            raise
        self._record_attempt(
            request_id=request_id,
            task=task,
            tier=repair_tier,
            purpose="structured_output_repair",
            attempt_number=attempt_number,
            result=repaired,
        )
        # The analyst still owns the reasoning. DeepSeek only repaired the
        # envelope, while the attempt ledger preserves both model charges.
        return ProviderResult(
            payload=repaired.payload,
            text=repaired.text,
            model=self.cfg.model(original_tier).model_id,
            latency_ms=original_error.latency_ms + repaired.latency_ms,
            input_tokens=original_error.input_tokens + repaired.input_tokens,
            output_tokens=original_error.output_tokens + repaired.output_tokens,
            cost_usd=original_error.cost_usd + repaired.cost_usd,
            tool_calls=repaired.tool_calls,
            structured_output_valid=True,
            generation_id=repaired.generation_id,
        )

    def _provider_call(
        self, task: LLMTaskContext, tier: LLMTier, *, request_id: str,
    ) -> tuple[ProviderResult, int]:
        request_cfg = self.cfg.block("request")
        retries = max(
            0,
            int(task.metadata.get("max_retries", request_cfg.get("max_retries") or 0)),
        )
        backoff = max(0.0, float(request_cfg.get("retry_backoff_seconds") or 0.0))
        last_error: LLMProviderError | None = None
        for attempt in range(retries + 1):
            try:
                self._enforce_budget(tier)
            except LLMProviderError as exc:
                # This is an application-side refusal, not a provider attempt.
                # Keep it in the logical request ledger without inflating the
                # paid-attempt counter.
                raise _ProviderCallFailed(exc, attempt) from exc
            try:
                result = self.provider.call(
                    model=self.cfg.model(tier),
                    task=task,
                    timeout_seconds=float(request_cfg.get("timeout_seconds") or 30),
                    max_tokens=int(task.metadata.get("max_tokens") or request_cfg.get("max_tokens") or 900),
                    temperature=float(task.metadata.get("temperature") or request_cfg.get("temperature") or 0),
                )
                if result.model not in self.cfg.allowed_models:
                    raise LLMProviderError("provider_returned_non_whitelisted_model")
                self._record_attempt(
                    request_id=request_id,
                    task=task,
                    tier=tier,
                    purpose="primary",
                    attempt_number=attempt + 1,
                    result=result,
                )
                return result, attempt
            except StructuredOutputError as exc:
                self._record_attempt(
                    request_id=request_id,
                    task=task,
                    tier=tier,
                    purpose="primary",
                    attempt_number=attempt + 1,
                    error=exc,
                )
                try:
                    repaired = self._repair_structured_output(
                        request_id=request_id,
                        task=task,
                        original_tier=tier,
                        original_error=exc,
                        attempt_number=attempt + 2,
                    )
                except LLMProviderError as repair_error:
                    raise _ProviderCallFailed(repair_error, attempt + 1) from repair_error
                return repaired, attempt + 1
            except LLMProviderError as exc:
                last_error = exc
                self._record_attempt(
                    request_id=request_id,
                    task=task,
                    tier=tier,
                    purpose="primary",
                    attempt_number=attempt + 1,
                    error=exc,
                )
                if not exc.retryable or attempt >= retries:
                    raise _ProviderCallFailed(exc, attempt) from exc
                time.sleep(backoff * (2 ** attempt))
        failure = last_error or LLMProviderError("provider_call_failed")
        raise _ProviderCallFailed(failure, retries) from failure

    def _record(
        self,
        *,
        request_id: str,
        parent_request_id: str | None,
        task: LLMTaskContext,
        tier: LLMTier,
        routing_reason: str,
        escalation_reason: str | None,
        provider_result: ProviderResult | None,
        retry_count: int,
        error: Exception | None,
        evaluation_only: bool,
    ) -> None:
        payload = provider_result.payload if provider_result else {}
        store_replay = bool(self.cfg.block("retention").get("store_replay_payloads", True))
        self.store.record_request(
            {
                "request_id": request_id,
                "parent_request_id": parent_request_id,
                "timestamp": utc_now_iso(),
                "agent": task.agent_name,
                "task_type": task.task_type,
                "selected_tier": tier.value,
                "selected_model": self.cfg.model(tier).model_id,
                "routing_reason": routing_reason,
                "escalation_reason": escalation_reason,
                "status": "ERROR" if error else "OK",
                "input_tokens": provider_result.input_tokens if provider_result else 0,
                "output_tokens": provider_result.output_tokens if provider_result else 0,
                "latency_ms": provider_result.latency_ms if provider_result else 0.0,
                "cost_usd": provider_result.cost_usd if provider_result else 0.0,
                "tool_calls_json": json.dumps(provider_result.tool_calls if provider_result else []),
                "structured_output_valid": int(bool(provider_result and provider_result.structured_output_valid)),
                "retry_count": retry_count,
                "confidence": _confidence(payload),
                "review_status": None,
                "model_disagreement": 0,
                "disagreement_fields_json": "[]",
                "final_downstream_action": None,
                "signal_id": task.signal_id,
                "asset_class": task.asset_class,
                "symbol": task.symbol,
                "mode": task.mode,
                "input_hash": stable_hash(task.replay_payload()),
                "output_hash": stable_hash(payload) if provider_result else None,
                "error_type": str(error) if error else None,
                "evaluation_only": int(evaluation_only),
            },
            task.replay_payload() if store_replay else None,
        )

    def _execute(
        self,
        task: LLMTaskContext,
        *,
        tier: LLMTier,
        routing_reason: str,
        escalation_reason: str | None = None,
        parent_request_id: str | None = None,
        evaluation_only: bool = False,
    ) -> LLMCallResult:
        request_id = str(uuid.uuid4())
        try:
            result, retry_count = self._provider_call(task, tier, request_id=request_id)
        except _ProviderCallFailed as failure:
            exc = failure.error
            self._record(
                request_id=request_id, parent_request_id=parent_request_id, task=task,
                tier=tier, routing_reason=routing_reason,
                escalation_reason=escalation_reason, provider_result=None,
                retry_count=failure.retry_count, error=exc, evaluation_only=evaluation_only,
            )
            raise LLMRouterError(str(exc)) from exc
        self._record(
            request_id=request_id, parent_request_id=parent_request_id, task=task,
            tier=tier, routing_reason=routing_reason,
            escalation_reason=escalation_reason, provider_result=result,
            retry_count=retry_count, error=None, evaluation_only=evaluation_only,
        )
        return LLMCallResult(
            request_id=request_id,
            payload=result.payload,
            text=result.text,
            tier=tier,
            model=result.model,
            routing_reason=routing_reason,
            latency_ms=result.latency_ms,
            input_tokens=result.input_tokens,
            output_tokens=result.output_tokens,
            cost_usd=result.cost_usd,
            tool_calls=result.tool_calls,
            structured_output_valid=result.structured_output_valid,
            retry_count=retry_count,
            confidence=_confidence(result.payload),
        )

    def call(self, task: LLMTaskContext) -> LLMRouterResult:
        if not self.cfg.enabled:
            raise LLMRouterError("llm_router_disabled")
        try:
            decision = select_primary_tier(task, self.cfg)
        except RoutingPolicyError as exc:
            raise LLMRouterError(str(exc)) from exc
        primary = self._execute(
            task, tier=decision.tier, routing_reason=decision.reason,
        )
        escalation = select_independent_review(task, primary.payload, primary.tier, self.cfg)
        if not escalation:
            self.store.update_review(
                primary.request_id, review_status="NOT_REQUIRED",
                model_disagreement=False, disagreement_fields=(), escalation_reason=None,
            )
            return LLMRouterResult(primary=primary)

        review_task = LLMTaskContext(
            **{
                **task.__dict__,
                "system_prompt": (
                    task.system_prompt
                    + "\nPerform an independent review from the original evidence. "
                    "Do not assume another model's conclusion is correct. Return the same JSON schema."
                ),
                "independent_review_requested": False,
                "metadata": {**task.metadata, "independent_review": True},
            }
        )
        try:
            review = self._execute(
                review_task,
                tier=LLMTier.REVIEW,
                routing_reason="independent_review_only",
                escalation_reason=escalation,
                parent_request_id=primary.request_id,
            )
        except LLMRouterError:
            self.store.update_review(
                primary.request_id,
                review_status="ERROR",
                model_disagreement=False,
                disagreement_fields=(),
                escalation_reason=escalation,
            )
            raise
        disagreement, fields = compare_independent_analyses(primary.payload, review.payload)
        self.store.mark_downstream_action(
            review.request_id,
            "independent_review_disagreement" if disagreement else "independent_review_completed",
        )
        self.store.update_review(
            primary.request_id,
            review_status="COMPLETED",
            model_disagreement=disagreement,
            disagreement_fields=fields,
            escalation_reason=escalation,
        )
        return LLMRouterResult(
            primary=primary,
            review=review,
            model_disagreement=disagreement,
            disagreement_fields=fields,
            escalation_reason=escalation,
        )

    def mark_downstream_action(self, request_id: str, action: str) -> None:
        self.store.mark_downstream_action(request_id, action)

    def replay(self, request_id: str, tiers: list[LLMTier]) -> list[dict[str, Any]]:
        original = LLMTaskContext.from_replay_payload(self.store.load_replay_task(request_id))
        results: list[dict[str, Any]] = []
        for tier in tiers:
            replay_id = str(uuid.uuid4())
            try:
                call = self._execute(
                    original,
                    tier=tier,
                    routing_reason="evaluation_replay_forced_tier",
                    parent_request_id=request_id,
                    evaluation_only=True,
                )
                item = {
                    "replay_id": replay_id,
                    "source_request_id": request_id,
                    "request_id": call.request_id,
                    "tier": tier.value,
                    "model": call.model,
                    "status": "OK",
                    "payload_json": json.dumps(call.payload, ensure_ascii=False, sort_keys=True),
                    "latency_ms": call.latency_ms,
                    "cost_usd": call.cost_usd,
                    "created_at": utc_now_iso(),
                    "error_type": None,
                }
            except LLMRouterError as exc:
                item = {
                    "replay_id": replay_id,
                    "source_request_id": request_id,
                    "request_id": "",
                    "tier": tier.value,
                    "model": self.cfg.model(tier).model_id,
                    "status": "ERROR",
                    "payload_json": None,
                    "latency_ms": 0.0,
                    "cost_usd": 0.0,
                    "created_at": utc_now_iso(),
                    "error_type": str(exc),
                }
            self.store.record_replay_result(item)
            results.append(item)
        return results


def get_llm_router(*, db_path: str | Path | None = None) -> LLMRouter:
    return LLMRouter(db_path=db_path)


__all__ = [
    "LLMRouter",
    "LLMRouterError",
    "compare_independent_analyses",
    "get_llm_router",
]
