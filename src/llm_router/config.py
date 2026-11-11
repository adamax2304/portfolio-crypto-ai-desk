from __future__ import annotations

import functools
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .schemas import LLMTier


ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "config" / "llm_router.yaml"
_EXPECTED_TIERS = {tier.value for tier in LLMTier}


class LLMRouterConfigError(RuntimeError):
    pass


@dataclass(frozen=True)
class ModelConfig:
    tier: LLMTier
    model_id: str
    input_cost_per_million: float
    output_cost_per_million: float
    supports_tools: bool
    supports_vision: bool
    supports_structured_output: bool


@dataclass(frozen=True)
class LLMRouterConfig:
    raw: dict[str, Any]
    models: dict[LLMTier, ModelConfig]

    @property
    def enabled(self) -> bool:
        return bool(self.raw.get("enabled", True))

    @property
    def allowed_models(self) -> frozenset[str]:
        return frozenset(model.model_id for model in self.models.values())

    def model(self, tier: LLMTier) -> ModelConfig:
        return self.models[tier]

    def block(self, name: str) -> dict[str, Any]:
        value = self.raw.get(name) or {}
        return value if isinstance(value, dict) else {}


def _load(path: Path) -> LLMRouterConfig:
    if not path.exists():
        raise LLMRouterConfigError(f"router config missing: {path}")
    with path.open("r", encoding="utf-8") as handle:
        raw = (yaml.safe_load(handle) or {}).get("llm_router") or {}
    model_rows = raw.get("models") or {}
    if set(model_rows) != _EXPECTED_TIERS:
        raise LLMRouterConfigError("model whitelist must define exactly routine, analyst, review")
    models: dict[LLMTier, ModelConfig] = {}
    seen: set[str] = set()
    for tier in LLMTier:
        row = model_rows.get(tier.value) or {}
        model_id = str(row.get("id") or "").strip()
        if not model_id or model_id in seen:
            raise LLMRouterConfigError(f"invalid or duplicate model id for {tier.value}")
        seen.add(model_id)
        models[tier] = ModelConfig(
            tier=tier,
            model_id=model_id,
            input_cost_per_million=float(row.get("input_cost_per_million") or 0.0),
            output_cost_per_million=float(row.get("output_cost_per_million") or 0.0),
            supports_tools=bool(row.get("supports_tools", False)),
            supports_vision=bool(row.get("supports_vision", False)),
            supports_structured_output=bool(row.get("supports_structured_output", False)),
        )
    return LLMRouterConfig(raw=dict(raw), models=models)


@functools.lru_cache(maxsize=4)
def load_llm_router_config(path: str | Path | None = None) -> LLMRouterConfig:
    return _load(Path(path) if path else CONFIG_PATH)


def clear_llm_router_config_cache() -> None:
    load_llm_router_config.cache_clear()


__all__ = [
    "CONFIG_PATH",
    "LLMRouterConfig",
    "LLMRouterConfigError",
    "ModelConfig",
    "clear_llm_router_config_cache",
    "load_llm_router_config",
]

