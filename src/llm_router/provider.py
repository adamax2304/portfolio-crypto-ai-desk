from __future__ import annotations

import json
import re
import threading
import time
from dataclasses import dataclass, field
from typing import Any

import requests

from .config import LLMRouterConfig, ModelConfig
from .schemas import LLMTaskContext


class LLMProviderError(RuntimeError):
    def __init__(
        self,
        message: str,
        *,
        retryable: bool = False,
        input_tokens: int = 0,
        output_tokens: int = 0,
        latency_ms: float = 0.0,
        cost_usd: float = 0.0,
        generation_id: str | None = None,
        raw_text: str = "",
    ) -> None:
        super().__init__(message)
        self.retryable = retryable
        self.input_tokens = max(0, int(input_tokens))
        self.output_tokens = max(0, int(output_tokens))
        self.latency_ms = max(0.0, float(latency_ms))
        self.cost_usd = max(0.0, float(cost_usd))
        self.generation_id = generation_id
        self.raw_text = str(raw_text or "")


class StructuredOutputError(LLMProviderError):
    pass


@dataclass(frozen=True)
class ProviderResult:
    payload: dict[str, Any]
    text: str
    model: str
    latency_ms: float
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0.0
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    structured_output_valid: bool = True
    generation_id: str | None = None


def extract_json_object(text: str) -> dict[str, Any]:
    body = str(text or "").strip()
    if body.startswith("```"):
        body = re.sub(r"^```(?:json)?\s*", "", body, flags=re.IGNORECASE)
        body = re.sub(r"\s*```$", "", body)

    def _as_object(candidate: str) -> dict[str, Any] | None:
        try:
            parsed: Any = json.loads(candidate)
            if isinstance(parsed, str):
                parsed = json.loads(parsed)
        except (json.JSONDecodeError, TypeError):
            return None
        return parsed if isinstance(parsed, dict) else None

    direct = _as_object(body)
    if direct is not None:
        return direct

    in_string = False
    escaped = False
    depth = 0
    start: int | None = None
    saw_brace = False
    for index, char in enumerate(body):
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "{":
            saw_brace = True
            if depth == 0:
                start = index
            depth += 1
        elif char == "}" and depth:
            depth -= 1
            if depth == 0 and start is not None:
                parsed = _as_object(body[start:index + 1])
                if parsed is not None:
                    return parsed
                start = None
    error = "malformed_structured_output" if saw_brace else "response_did_not_contain_json"
    raise StructuredOutputError(error, retryable=True)


def _content_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        parts: list[str] = []
        for part in value:
            if isinstance(part, dict):
                candidate = part.get("text") or part.get("content")
                if candidate:
                    parts.append(str(candidate))
            elif part is not None:
                parts.append(str(part))
        return "\n".join(parts)
    return "" if value is None else str(value)


class OpenRouterProvider:
    def __init__(self, *, cfg: LLMRouterConfig, api_key: str) -> None:
        if not api_key:
            raise LLMProviderError("missing_openrouter_api_key")
        self.cfg = cfg
        self.api_key = api_key
        self._usage_lock = threading.Lock()
        self._usage_cache_at = 0.0
        self._usage_daily_usd: float | None = None

    def daily_usage_usd(self, *, cache_seconds: float = 300.0) -> float | None:
        """Read authoritative UTC-day key spend, cached to avoid API chatter."""
        now = time.monotonic()
        with self._usage_lock:
            if (
                self._usage_daily_usd is not None
                and now - self._usage_cache_at <= max(1.0, float(cache_seconds))
            ):
                return self._usage_daily_usd
            try:
                response = requests.get(
                    str(
                        self.cfg.raw.get("key_status_url")
                        or "https://openrouter.ai/api/v1/key"
                    ),
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=10,
                )
                response.raise_for_status()
                value = float(((response.json() or {}).get("data") or {}).get("usage_daily"))
            except (requests.RequestException, TypeError, ValueError, AttributeError):
                return None
            self._usage_daily_usd = max(0.0, value)
            self._usage_cache_at = now
            return self._usage_daily_usd

    def call(
        self,
        *,
        model: ModelConfig,
        task: LLMTaskContext,
        timeout_seconds: float,
        max_tokens: int,
        temperature: float,
    ) -> ProviderResult:
        if model.model_id not in self.cfg.allowed_models:
            raise LLMProviderError("model_not_in_application_whitelist")
        if task.requires_tools and not model.supports_tools:
            raise LLMProviderError("selected_model_does_not_support_tools")
        if task.requires_vision and not model.supports_vision:
            raise LLMProviderError("selected_model_does_not_support_vision")
        if task.requires_structured_output and not model.supports_structured_output:
            raise LLMProviderError("selected_model_does_not_support_structured_output")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        if self.cfg.raw.get("http_referer"):
            headers["HTTP-Referer"] = str(self.cfg.raw["http_referer"])
        if self.cfg.raw.get("app_title"):
            headers["X-OpenRouter-Title"] = str(self.cfg.raw["app_title"])

        content: Any = json.dumps(task.user_payload, ensure_ascii=False, sort_keys=True)
        if task.image_urls:
            content = [{"type": "text", "text": content}] + [
                {"type": "image_url", "image_url": {"url": url}}
                for url in task.image_urls
            ]
        request: dict[str, Any] = {
            "model": model.model_id,
            "temperature": float(temperature),
            "max_tokens": max(64, int(max_tokens)),
            "messages": [
                {"role": "system", "content": task.system_prompt},
                {"role": "user", "content": content},
            ],
        }
        reasoning = task.metadata.get("reasoning")
        if isinstance(reasoning, dict):
            request["reasoning"] = dict(reasoning)
        elif bool(task.metadata.get("disable_reasoning", False)):
            request["reasoning"] = {"enabled": False}
        if task.requires_structured_output:
            schema = task.metadata.get("json_schema")
            if isinstance(schema, dict) and schema:
                raw_name = str(task.metadata.get("json_schema_name") or task.task_type or "task_output")
                name = re.sub(r"[^A-Za-z0-9_-]", "_", raw_name)[:64] or "task_output"
                request["response_format"] = {
                    "type": "json_schema",
                    "json_schema": {"name": name, "strict": True, "schema": schema},
                }
            else:
                request["response_format"] = {"type": "json_object"}
            request["provider"] = {"require_parameters": True}
            request.setdefault("plugins", []).append({"id": "response-healing"})
        if task.tools:
            request["tools"] = task.tools
        if task.web_search:
            request.setdefault("plugins", []).append({"id": "web", "max_results": 5})

        started = time.perf_counter()
        try:
            response = requests.post(
                str(self.cfg.raw.get("base_url")),
                headers=headers,
                data=json.dumps(request, ensure_ascii=False).encode("utf-8"),
                timeout=max(1.0, float(timeout_seconds)),
            )
        except requests.RequestException as exc:
            raise LLMProviderError(type(exc).__name__, retryable=True) from exc
        latency_ms = (time.perf_counter() - started) * 1000.0
        if response.status_code >= 400:
            retryable = response.status_code in {408, 409, 429} or response.status_code >= 500
            raise LLMProviderError(f"openrouter_http_{response.status_code}", retryable=retryable)
        try:
            body = response.json()
        except ValueError as exc:
            raise LLMProviderError("invalid_provider_json", retryable=True) from exc
        choices = body.get("choices") if isinstance(body, dict) else None
        if not choices:
            raise LLMProviderError("empty_provider_choices", retryable=True)
        message = choices[0].get("message") or {}
        raw_content = message.get("content")
        text = _content_text(raw_content)
        usage = body.get("usage") or {}
        input_tokens = int(usage.get("prompt_tokens") or 0)
        output_tokens = int(usage.get("completion_tokens") or 0)
        explicit_cost = usage.get("cost")
        if explicit_cost is None:
            cost = (
                input_tokens * model.input_cost_per_million
                + output_tokens * model.output_cost_per_million
            ) / 1_000_000.0
        else:
            try:
                cost = float(explicit_cost)
            except (TypeError, ValueError):
                cost = 0.0
        generation_id = str(body.get("id") or "").strip() or None
        try:
            if task.requires_structured_output:
                parsed = message.get("parsed")
                if isinstance(parsed, dict):
                    payload = parsed
                    if not text:
                        text = json.dumps(parsed, ensure_ascii=False)
                else:
                    candidates = [text, _content_text(choices[0].get("text"))]
                    for tool_call in message.get("tool_calls") or []:
                        if isinstance(tool_call, dict):
                            function = tool_call.get("function") or {}
                            candidates.append(_content_text(function.get("arguments")))
                    candidates.append(_content_text(message.get("reasoning")))
                    candidates = [candidate for candidate in candidates if candidate.strip()]
                    payload = None
                    last_error: StructuredOutputError | None = None
                    for candidate in candidates:
                        try:
                            payload = extract_json_object(candidate)
                            text = candidate
                            break
                        except StructuredOutputError as candidate_error:
                            last_error = candidate_error
                    if payload is None:
                        raise last_error or StructuredOutputError(
                            "response_did_not_contain_json", retryable=True,
                        )
            else:
                payload = {"text": text}
        except StructuredOutputError as exc:
            # The provider already completed and may have billed this call.
            # Preserve its exact usage so malformed output is not invisible
            # to budgets and cost reports.
            raise StructuredOutputError(
                str(exc),
                retryable=False,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                latency_ms=latency_ms,
                cost_usd=cost,
                generation_id=generation_id,
                raw_text=text or _content_text(message.get("reasoning")),
            ) from exc
        return ProviderResult(
            payload=payload,
            text=text,
            # Record the whitelisted logical selection. Providers may return a
            # dated deployment alias in ``body.model``; that is telemetry, not
            # permission to introduce a fourth application model.
            model=model.model_id,
            latency_ms=latency_ms,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_usd=max(0.0, cost),
            tool_calls=list(message.get("tool_calls") or []),
            structured_output_valid=True,
            generation_id=generation_id,
        )


__all__ = [
    "LLMProviderError",
    "OpenRouterProvider",
    "ProviderResult",
    "StructuredOutputError",
    "extract_json_object",
]
