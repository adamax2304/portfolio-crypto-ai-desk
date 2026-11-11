from __future__ import annotations

import functools
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "config" / "quality_agents.yaml"


DEFAULTS: dict[str, Any] = {
    "enabled": True,
    "operation_mode": "shadow",
    "hard_block_allowlist": [
        "INVALID_SYMBOL",
        "MISSING_GEOMETRY",
        "INVALID_DIRECTIONAL_GEOMETRY",
        "CURRENT_PRICE_NOT_REVALIDATED",
        "VENUE_UNAVAILABLE",
        "PROTECTIVE_STOP_MISSING",
        "EVENT_HALT_ACTIVE",
        "WRONG_ENTITY_CONFIRMED",
    ],
    "agents": {
        "news_entity": {"enabled": True, "mode": "shadow", "ttl_minutes": 30},
        "event_risk": {"enabled": True, "mode": "shadow", "ttl_minutes": 30},
        "market_regime": {"enabled": True, "mode": "shadow", "ttl_minutes": 20},
        "execution_sanity": {"enabled": True, "mode": "shadow", "ttl_minutes": 10},
        "post_trade_forensics": {"enabled": True, "mode": "diagnostic", "ttl_minutes": 1440},
        "llm_cached_advisory": {"enabled": True, "mode": "shadow", "ttl_minutes": 45},
    },
    "market_snapshot_max_age_minutes": 90,
    "llm_advisory_refresh": {
        "enabled": False,
        "lookback_hours": 8,
        "candidate_scope": "active_ab",
        "candidate_lookback_hours": 48,
        "candidate_statuses": [
            "generated", "waiting_for_entry", "triggered", "tp1_hit", "tp2_hit",
        ],
        "candidate_tiers": ["A", "B"],
        "excluded_modes": ["scalp"],
        "max_active_symbols": 80,
        "max_events": 16,
        "max_symbols_per_event": 2,
        "max_assessments_per_run": 4,
        "ttl_minutes": 360,
        "min_confidence": 0.50,
        "max_tokens": 400,
        "max_retries": 1,
    },
    "retention": {
        "runs_days": 180,
        "signal_verdict_days": 180,
        "market_verdict_days": 90,
        "resolved_incident_days": 90,
        "reducer_days": 180,
        "post_trade_days": 730,
        "llm_assessment_days": 180,
        "experiment_assignment_days": 365,
    },
}


def _merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    result = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _merge(result[key], value)
        else:
            result[key] = value
    return result


@dataclass(frozen=True)
class QualityAgentsConfig:
    raw: dict[str, Any]

    @property
    def enabled(self) -> bool:
        return bool(self.raw.get("enabled", True))

    @property
    def operation_mode(self) -> str:
        value = str(self.raw.get("operation_mode") or "shadow").lower()
        return value if value in {"shadow", "advisory", "enforced"} else "shadow"

    @property
    def hard_block_allowlist(self) -> set[str]:
        return {str(item).upper() for item in (self.raw.get("hard_block_allowlist") or [])}

    def agent(self, name: str) -> dict[str, Any]:
        value = (self.raw.get("agents") or {}).get(name, {}) or {}
        return value if isinstance(value, dict) else {}

    def agent_enabled(self, name: str) -> bool:
        return self.enabled and bool(self.agent(name).get("enabled", True))

    def agent_mode(self, name: str) -> str:
        return str(self.agent(name).get("mode") or "shadow").lower()

    def ttl_minutes(self, name: str, default: float = 30.0) -> float:
        try:
            return max(1.0, float(self.agent(name).get("ttl_minutes", default)))
        except (TypeError, ValueError):
            return default

    def get(self, key: str, default: Any = None) -> Any:
        return self.raw.get(key, default)

    @property
    def llm_advisory_refresh(self) -> dict[str, Any]:
        value = self.raw.get("llm_advisory_refresh") or {}
        return value if isinstance(value, dict) else {}


@functools.lru_cache(maxsize=4)
def load_quality_agents_config(path: str | Path | None = None) -> QualityAgentsConfig:
    cfg_path = Path(path) if path else CONFIG_PATH
    payload: dict[str, Any] = {}
    if cfg_path.exists():
        with cfg_path.open("r", encoding="utf-8") as handle:
            payload = (yaml.safe_load(handle) or {}).get("quality_agents") or {}
    return QualityAgentsConfig(_merge(DEFAULTS, payload))


def clear_quality_agents_config_cache() -> None:
    load_quality_agents_config.cache_clear()
