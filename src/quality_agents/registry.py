from __future__ import annotations

from typing import Any

from .config import QualityAgentsConfig
from .event_risk_agent import EventRiskAgent
from .execution_sanity_agent import ExecutionSanityAgent
from .llm_cached_advisory_agent import LLMCachedAdvisoryAgent
from .market_regime_agent import MarketRegimeAgent
from .news_entity_agent import NewsEntityAgent


AGENT_TYPES: dict[str, type[Any]] = {
    "news_entity": NewsEntityAgent,
    "event_risk": EventRiskAgent,
    "market_regime": MarketRegimeAgent,
    "execution_sanity": ExecutionSanityAgent,
    "llm_cached_advisory": LLMCachedAdvisoryAgent,
}


def build_registry(
    cfg: QualityAgentsConfig, *, names: set[str] | None = None,
) -> list[Any]:
    selected = names or set(AGENT_TYPES)
    return [
        agent_type()
        for name, agent_type in AGENT_TYPES.items()
        if name in selected and cfg.agent_enabled(name)
    ]


__all__ = ["AGENT_TYPES", "build_registry"]
