from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

import pytest

from src.llm_router import (
    Complexity,
    FinancialReasoning,
    LLMRouter,
    LLMRouterError,
    LLMTaskContext,
    LLMTier,
    Stakes,
)
from src.llm_router.metrics import routing_metrics
from src.llm_router.config import load_llm_router_config
from src.llm_router.provider import (
    LLMProviderError,
    OpenRouterProvider,
    ProviderResult,
    StructuredOutputError,
    extract_json_object,
)


def _task(**overrides) -> LLMTaskContext:
    values = {
        "agent_name": "test_agent",
        "task_type": "parsing",
        "system_prompt": "Return JSON.",
        "user_payload": {"text": "AAPL guidance raised"},
        "requires_structured_output": True,
    }
    values.update(overrides)
    return LLMTaskContext(**values)


def _enabled_test_router(*, db_path: Path, provider) -> LLMRouter:
    cfg = load_llm_router_config()
    return LLMRouter(
        cfg=replace(cfg, raw={**cfg.raw, "enabled": True}),
        db_path=db_path,
        provider=provider,
    )


class RecordingProvider:
    def __init__(self, payloads: dict[LLMTier, dict] | None = None) -> None:
        self.calls = []
        self.payloads = payloads or {}

    def call(self, *, model, task, **kwargs) -> ProviderResult:
        self.calls.append((model.tier, task))
        payload = self.payloads.get(model.tier, {"verdict": "NEUTRAL", "confidence": 0.8})
        return ProviderResult(
            payload=payload,
            text="{}",
            model=model.model_id,
            latency_ms=11.0,
            input_tokens=100,
            output_tokens=20,
            cost_usd=0.001,
        )


@pytest.mark.parametrize("task_type", ["parsing", "classification", "news_categorization"])
def test_routine_tasks_route_to_deepseek_tier(tmp_path: Path, task_type: str) -> None:
    provider = RecordingProvider()
    router = _enabled_test_router(db_path=tmp_path / "router.sqlite", provider=provider)
    result = router.call(_task(task_type=task_type))
    assert result.primary.tier == LLMTier.ROUTINE
    assert provider.calls == [(LLMTier.ROUTINE, provider.calls[0][1])]


def test_simple_financial_extraction_stays_routine(tmp_path: Path) -> None:
    provider = RecordingProvider()
    router = _enabled_test_router(db_path=tmp_path / "router.sqlite", provider=provider)
    result = router.call(_task(
        task_type="simple_financial_extraction",
        financial_reasoning=FinancialReasoning.DATA_PROCESSING,
    ))
    assert result.primary.tier == LLMTier.ROUTINE


@pytest.mark.parametrize(
    "task_type",
    ["financial_news_interpretation", "trade_thesis_synthesis", "multi_source_financial_reasoning"],
)
def test_complex_financial_tasks_route_to_gemini_tier(tmp_path: Path, task_type: str) -> None:
    provider = RecordingProvider()
    router = _enabled_test_router(db_path=tmp_path / "router.sqlite", provider=provider)
    result = router.call(_task(
        task_type=task_type,
        financial_reasoning=FinancialReasoning.SYNTHESIS,
        complexity=Complexity.HIGH,
        stakes=Stakes.HIGH,
        source_count=4,
    ))
    assert result.primary.tier == LLMTier.ANALYST
    assert result.review is None


def test_conflicting_low_confidence_case_gets_independent_muse_review(tmp_path: Path) -> None:
    provider = RecordingProvider({
        LLMTier.ANALYST: {"verdict": "SUPPORT", "direction": "long", "confidence": 0.31},
        LLMTier.REVIEW: {"verdict": "BLOCK", "direction": "short", "confidence": 0.73},
    })
    router = _enabled_test_router(db_path=tmp_path / "router.sqlite", provider=provider)
    result = router.call(_task(
        task_type="trade_thesis_synthesis",
        financial_reasoning=FinancialReasoning.SYNTHESIS,
        complexity=Complexity.HIGH,
        stakes=Stakes.HIGH,
        ambiguity="high",
        evidence_conflict=True,
    ))
    assert [tier for tier, _ in provider.calls] == [LLMTier.ANALYST, LLMTier.REVIEW]
    assert result.review is not None
    assert result.model_disagreement is True
    assert set(result.disagreement_fields) == {"direction", "verdict"}
    assert provider.calls[1][1].user_payload == provider.calls[0][1].user_payload


def test_clear_gemini_case_does_not_invoke_muse(tmp_path: Path) -> None:
    provider = RecordingProvider({
        LLMTier.ANALYST: {"verdict": "SUPPORT", "confidence": 0.92},
    })
    router = _enabled_test_router(db_path=tmp_path / "router.sqlite", provider=provider)
    result = router.call(_task(
        task_type="trade_setup_analysis",
        financial_reasoning=FinancialReasoning.INTERPRETATION,
        stakes=Stakes.HIGH,
    ))
    assert result.review is None
    assert [tier for tier, _ in provider.calls] == [LLMTier.ANALYST]


def test_model_reported_unresolved_contradiction_triggers_review(tmp_path: Path) -> None:
    provider = RecordingProvider({
        LLMTier.ANALYST: {
            "verdict": "CAUTION",
            "confidence": 0.62,
            "unresolved_contradictions": ["price and catalyst disagree"],
        },
        LLMTier.REVIEW: {"verdict": "CAUTION", "confidence": 0.7},
    })
    router = _enabled_test_router(db_path=tmp_path / "router.sqlite", provider=provider)
    result = router.call(_task(
        task_type="trade_setup_analysis",
        financial_reasoning=FinancialReasoning.INTERPRETATION,
        stakes=Stakes.MATERIAL,
        ambiguity="high",
    ))
    assert result.review is not None
    assert result.escalation_reason == "model_reported_unresolved_contradictions"


@pytest.mark.parametrize("key", ["model", "requested_model", "provider_model"])
def test_prohibited_concrete_model_request_is_rejected(tmp_path: Path, key: str) -> None:
    provider = RecordingProvider()
    router = _enabled_test_router(db_path=tmp_path / "router.sqlite", provider=provider)
    with pytest.raises(LLMRouterError, match="may not request a concrete model"):
        router.call(_task(metadata={key: "anthropic/claude-sonnet"}))
    assert not provider.calls


def test_retryable_provider_failure_retries_same_tier(tmp_path: Path) -> None:
    class FlakyProvider(RecordingProvider):
        def call(self, *, model, task, **kwargs):
            self.calls.append((model.tier, task))
            if len(self.calls) < 3:
                raise LLMProviderError("timeout", retryable=True)
            return ProviderResult({}, "{}", model.model_id, 5.0)

    provider = FlakyProvider()
    router = _enabled_test_router(db_path=tmp_path / "router.sqlite", provider=provider)
    result = router.call(_task())
    assert result.primary.retry_count == 2
    assert [tier for tier, _ in provider.calls] == [LLMTier.ROUTINE] * 3


def test_malformed_structured_output_retries_without_tier_escalation(tmp_path: Path) -> None:
    class MalformedOnce(RecordingProvider):
        def call(self, *, model, task, **kwargs):
            self.calls.append((model.tier, task))
            if len(self.calls) == 1:
                raise StructuredOutputError("malformed", retryable=True)
            return ProviderResult({"ok": True}, "{}", model.model_id, 4.0)

    provider = MalformedOnce()
    router = _enabled_test_router(db_path=tmp_path / "router.sqlite", provider=provider)
    result = router.call(_task())
    assert result.primary.structured_output_valid is True
    assert [tier for tier, _ in provider.calls] == [LLMTier.ROUTINE, LLMTier.ROUTINE]


def test_malformed_analyst_output_gets_one_routine_repair_and_tracks_both_costs(tmp_path: Path) -> None:
    class MalformedAnalyst(RecordingProvider):
        def call(self, *, model, task, **kwargs):
            self.calls.append((model.tier, task))
            if model.tier == LLMTier.ANALYST:
                raise StructuredOutputError(
                    "response_did_not_contain_json",
                    input_tokens=1000,
                    output_tokens=200,
                    cost_usd=0.01,
                    latency_ms=20,
                    raw_text="verdict support confidence high",
                )
            return ProviderResult(
                {"verdict": "SUPPORT", "confidence": 0.8},
                "{}",
                model.model_id,
                5.0,
                input_tokens=100,
                output_tokens=20,
                cost_usd=0.001,
            )

    db = tmp_path / "router.sqlite"
    provider = MalformedAnalyst()
    router = _enabled_test_router(db_path=db, provider=provider)
    result = router.call(_task(
        task_type="trade_setup_analysis",
        financial_reasoning=FinancialReasoning.INTERPRETATION,
        metadata={"max_retries": 0, "json_schema": {"type": "object"}},
    ))
    metrics = routing_metrics(db_path=db)

    assert [tier for tier, _ in provider.calls] == [LLMTier.ANALYST, LLMTier.ROUTINE]
    repair_task = provider.calls[1][1]
    assert repair_task.metadata["disable_reasoning"] is True
    assert "json_schema" not in repair_task.metadata
    assert result.primary.model == router.cfg.model(LLMTier.ANALYST).model_id
    assert result.primary.cost_usd == pytest.approx(0.011)
    assert metrics["provider_attempts"] == 2
    assert metrics["total_cost_usd"] == pytest.approx(0.011)


def test_daily_tier_budget_blocks_additional_provider_call(tmp_path: Path) -> None:
    class ExpensiveAnalyst(RecordingProvider):
        def call(self, *, model, task, **kwargs):
            self.calls.append((model.tier, task))
            return ProviderResult(
                {"verdict": "NEUTRAL", "confidence": 0.8},
                "{}",
                model.model_id,
                1.0,
                input_tokens=100,
                output_tokens=20,
                cost_usd=0.51,
            )

    provider = ExpensiveAnalyst()
    router = _enabled_test_router(db_path=tmp_path / "router.sqlite", provider=provider)
    task = _task(
        task_type="trade_setup_analysis",
        financial_reasoning=FinancialReasoning.INTERPRETATION,
        metadata={"max_retries": 0},
    )
    router.call(task)
    with pytest.raises(LLMRouterError, match="llm_daily_budget_exhausted:analyst"):
        router.call(task)
    assert [tier for tier, _ in provider.calls] == [LLMTier.ANALYST]


def test_authoritative_provider_daily_usage_enforces_total_budget(tmp_path: Path) -> None:
    class Provider(RecordingProvider):
        @staticmethod
        def daily_usage_usd():
            return 0.81

    provider = Provider()
    db = tmp_path / "router.sqlite"
    router = _enabled_test_router(db_path=db, provider=provider)
    with pytest.raises(LLMRouterError, match="llm_daily_budget_exhausted:total"):
        router.call(_task())
    assert provider.calls == []
    assert routing_metrics(db_path=db)["provider_attempts"] == 0


def test_provider_sends_strict_json_schema_and_records_generation_id(monkeypatch) -> None:
    captured = {}

    class Response:
        status_code = 200

        @staticmethod
        def json():
            return {
                "id": "gen-test-1",
                "choices": [{"message": {"content": '{"ok":true}'}}],
                "usage": {"prompt_tokens": 12, "completion_tokens": 4, "cost": 0.001},
            }

    def fake_post(url, *, headers, data, timeout):
        captured.update(json.loads(data.decode("utf-8")))
        return Response()

    monkeypatch.setattr("src.llm_router.provider.requests.post", fake_post)
    cfg = load_llm_router_config()
    provider = OpenRouterProvider(cfg=cfg, api_key="test-key")
    schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": {"ok": {"type": "boolean"}},
        "required": ["ok"],
    }
    result = provider.call(
        model=cfg.model(LLMTier.ROUTINE),
        task=_task(metadata={"json_schema": schema, "json_schema_name": "strict_test"}),
        timeout_seconds=5,
        max_tokens=100,
        temperature=0,
    )

    assert captured["response_format"] == {
        "type": "json_schema",
        "json_schema": {"name": "strict_test", "strict": True, "schema": schema},
    }
    assert captured["provider"] == {"require_parameters": True}
    assert {"id": "response-healing"} in captured["plugins"]
    assert result.generation_id == "gen-test-1"


def test_provider_disables_reasoning_and_reads_reasoning_json(monkeypatch) -> None:
    captured = {}

    class Response:
        status_code = 200

        @staticmethod
        def json():
            return {
                "choices": [{"message": {"content": "", "reasoning": '{"ok": true}'}}],
                "usage": {},
            }

    def fake_post(url, *, headers, data, timeout):
        captured.update(json.loads(data.decode("utf-8")))
        return Response()

    monkeypatch.setattr("src.llm_router.provider.requests.post", fake_post)
    cfg = load_llm_router_config()
    result = OpenRouterProvider(cfg=cfg, api_key="test-key").call(
        model=cfg.model(LLMTier.ROUTINE),
        task=_task(metadata={"disable_reasoning": True}),
        timeout_seconds=5,
        max_tokens=100,
        temperature=0,
    )
    assert captured["reasoning"] == {"enabled": False}
    assert result.payload == {"ok": True}


def test_extract_json_object_uses_balanced_candidate() -> None:
    text = 'prefix {not json} then {"ok": true, "note": "brace } inside"} suffix'
    assert extract_json_object(text) == {"ok": True, "note": "brace } inside"}


def test_model_unavailability_fails_safe_without_muse_fallback(tmp_path: Path) -> None:
    class DownProvider(RecordingProvider):
        def call(self, *, model, task, **kwargs):
            self.calls.append((model.tier, task))
            raise LLMProviderError("model_unavailable", retryable=False)

    provider = DownProvider()
    router = _enabled_test_router(db_path=tmp_path / "router.sqlite", provider=provider)
    with pytest.raises(LLMRouterError, match="model_unavailable"):
        router.call(_task(
            task_type="trade_setup_analysis",
            financial_reasoning=FinancialReasoning.INTERPRETATION,
        ))
    assert [tier for tier, _ in provider.calls] == [LLMTier.ANALYST]


def test_request_logging_metrics_and_shadow_replay(tmp_path: Path) -> None:
    db = tmp_path / "router.sqlite"
    provider = RecordingProvider()
    router = _enabled_test_router(db_path=db, provider=provider)
    result = router.call(_task())
    router.mark_downstream_action(result.primary.request_id, "cache_written")
    replay = router.replay(result.primary.request_id, [LLMTier.ROUTINE, LLMTier.ANALYST])
    metrics = routing_metrics(db_path=db)
    assert [row["status"] for row in replay] == ["OK", "OK"]
    assert metrics["calls"] == 1
    assert metrics["calls_by_tier"]["routine"]["calls"] == 1
    assert metrics["total_cost_usd"] == pytest.approx(0.001)


def test_agents_have_no_direct_model_or_openrouter_transport_bypass() -> None:
    root = Path(__file__).resolve().parents[1]
    offenders = []
    for path in (root / "src").rglob("*.py"):
        if "llm_router" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        if (
            "openrouter.ai/api" in text
            or "OpenRouterClient" in text
            or "import OpenRouterProvider" in text
        ):
            offenders.append(str(path.relative_to(root)))
    assert offenders == []


def test_concrete_model_ids_exist_only_in_central_config() -> None:
    root = Path(__file__).resolve().parents[1]
    cfg = load_llm_router_config()
    assert len(cfg.allowed_models) == 3
    allowed_locations = {root / "config" / "llm_router.yaml"}
    offenders = []
    for base in (root / "src", root / "config"):
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in {".py", ".yaml", ".yml", ".toml"}:
                continue
            if path in allowed_locations:
                continue
            text = path.read_text(encoding="utf-8")
            if any(model_id in text for model_id in cfg.allowed_models):
                offenders.append(str(path.relative_to(root)))
    assert offenders == []


def test_production_router_is_disabled_without_constructing_provider(tmp_path: Path) -> None:
    cfg = load_llm_router_config()
    assert cfg.enabled is False
    router = LLMRouter(cfg=cfg, db_path=tmp_path / "router.sqlite")
    assert router.provider is None
    with pytest.raises(LLMRouterError, match="llm_router_disabled"):
        router.call(_task())


def test_disabled_router_metrics_do_not_contact_openrouter(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    cfg = load_llm_router_config()
    assert cfg.enabled is False
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")

    def unexpected_usage_request(*args, **kwargs):
        raise AssertionError("disabled router must not query OpenRouter usage")

    monkeypatch.setattr(
        "src.llm_router.provider.OpenRouterProvider.daily_usage_usd",
        unexpected_usage_request,
    )
    metrics = routing_metrics(
        db_path=tmp_path / "router.sqlite",
        cfg=cfg,
        include_provider_usage=True,
    )
    assert metrics["provider_utc_day_cost_usd"] is None
