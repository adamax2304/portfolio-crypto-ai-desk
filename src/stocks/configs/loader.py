"""Loader for config/stocks/*.yaml.

Kept deliberately separate from src/config.py so the crypto loader stays
unchanged. Both loaders share the load_yaml helper.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from src.config import PROJECT_ROOT, load_yaml


@dataclass(frozen=True)
class StocksConfig:
    """Frozen view over the three config/stocks/*.yaml files."""

    root: Path
    universe: dict[str, Any] = field(default_factory=dict)
    scoring: dict[str, Any] = field(default_factory=dict)
    risk: dict[str, Any] = field(default_factory=dict)

    # ------------------------------------------------------------------
    # Universe accessors
    # ------------------------------------------------------------------
    @property
    def enabled(self) -> bool:
        return bool(self.universe.get("enabled", True))

    @property
    def default_symbols(self) -> list[str]:
        return [str(s).upper() for s in (self.universe.get("default_symbols") or [])]

    @property
    def indices(self) -> list[str]:
        return [str(s).upper() for s in (self.universe.get("indices") or [])]

    @property
    def volatility_index(self) -> str:
        return str(self.universe.get("volatility_index") or "^VIX")

    @property
    def sector_etfs(self) -> dict[str, str]:
        return {
            str(k): str(v).upper()
            for k, v in (self.universe.get("sector_etfs") or {}).items()
        }

    @property
    def symbol_sector_map(self) -> dict[str, str]:
        return {
            str(k).upper(): str(v)
            for k, v in (self.universe.get("symbol_sector_map") or {}).items()
        }

    def sector_for(self, symbol: str) -> str:
        return self.symbol_sector_map.get(symbol.upper(), "")

    def sector_etf_for(self, symbol: str) -> str:
        sector = self.sector_for(symbol)
        if not sector:
            return ""
        return self.sector_etfs.get(sector, "")

    # ------------------------------------------------------------------
    # PART 18 — ETF / index recognition
    # ------------------------------------------------------------------
    @property
    def etf_universe(self) -> set[str]:
        """Union of broad-market indices + every sector ETF in the config.

        Used by the earnings-risk path to skip the "earnings UNKNOWN"
        false-positive for SPY/QQQ/IWM/DIA/SMH/XLK/etc. ETFs do not
        report earnings, so the "calendar lookup missing" warning is
        nonsense for them.
        """
        return set(self.indices) | {v for v in self.sector_etfs.values()}

    def is_etf(self, symbol: str) -> bool:
        """True iff ``symbol`` is one of the configured indices or
        sector ETFs. Case-insensitive."""
        return (symbol or "").upper() in self.etf_universe

    def timeframes_for(self, mode: str) -> list[str]:
        mode_map = self.universe.get("mode_timeframes") or {}
        return [str(tf) for tf in (mode_map.get(mode) or [])] or ["1d"]

    # ------------------------------------------------------------------
    # Scoring accessors
    # ------------------------------------------------------------------
    def weight(self, key: str, default: float = 0.0) -> float:
        return float((self.scoring.get("weights") or {}).get(key, default))

    def risk_penalty(self, key: str, default: float = 0.0) -> float:
        return float((self.scoring.get("risk_penalties") or {}).get(key, default))

    def mode_multiplier(self, mode: str, component: str, default: float = 1.0) -> float:
        block = (self.scoring.get("mode_weights") or {}).get(mode) or {}
        return float(block.get(component, default))

    def regime_multiplier(self, regime: str, component: str, default: float = 1.0) -> float:
        block = (self.scoring.get("regime_weights") or {}).get(regime) or {}
        return float(block.get(component, default))

    def cap(self, key: str, default: float | None = None) -> float | None:
        value = (self.scoring.get("caps") or {}).get(key, default)
        return None if value is None else float(value)

    def tier_threshold(self, tier: str, default: float) -> float:
        block = self.scoring.get("tiering") or {}
        key = f"{tier.lower()}_tier"
        return float(block.get(key, default))

    # ------------------------------------------------------------------
    # Risk-rule accessors
    # ------------------------------------------------------------------
    def earnings_rule(self, mode: str) -> dict[str, Any]:
        block = (self.risk.get("earnings") or {}).get(mode) or {}
        return dict(block)

    def regime_rule(self, regime: str) -> dict[str, Any]:
        block = (self.risk.get("regime") or {}).get(regime) or {}
        return dict(block)

    def confirmation_rule(self, key: str) -> dict[str, Any]:
        block = (self.risk.get("confirmation") or {}).get(key) or {}
        return dict(block)

    @property
    def liquidity_rules(self) -> dict[str, Any]:
        return dict(self.risk.get("liquidity") or {})

    @property
    def structure_rules(self) -> dict[str, Any]:
        return dict(self.risk.get("structure") or {})


def load_stocks_config(root: Path | None = None) -> StocksConfig:
    project_root = (root or PROJECT_ROOT).resolve()
    config_dir = project_root / "config" / "stocks"
    return StocksConfig(
        root=project_root,
        universe=load_yaml(config_dir / "universe.yaml"),
        scoring=load_yaml(config_dir / "scoring.yaml"),
        risk=load_yaml(config_dir / "risk.yaml"),
    )
