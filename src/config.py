from __future__ import annotations

import functools
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data or {}


@dataclass(frozen=True)
class ProjectConfig:
    root: Path
    settings: dict[str, Any]
    watchlist: dict[str, Any]
    sources: dict[str, Any]
    scoring: dict[str, Any]
    universe: dict[str, Any]
    exchanges: dict[str, Any]

    @property
    def exchange_id(self) -> str:
        return str(
            self.watchlist.get("exchange")
            or self.settings.get("exchange", {}).get("default", "binance")
        )

    @property
    def enabled_exchanges(self) -> list[str]:
        configured = self.universe.get("enabled_exchanges")
        if configured:
            return [str(item).lower() for item in configured]
        return [self.exchange_id.lower()]

    @property
    def anchor_exchange(self) -> str:
        return str(self.universe.get("anchor_exchange") or self.exchange_id).lower()

    @property
    def high_risk_exchanges(self) -> set[str]:
        return {str(item).lower() for item in self.universe.get("high_risk_exchanges", []) or []}

    def exchange_setting(self, exchange: str, key: str, default: Any = None) -> Any:
        block = self.exchanges.get(exchange.lower(), {})
        return block.get(key, default)

    def exchange_enabled(self, exchange: str) -> bool:
        return bool(self.exchange_setting(exchange, "enabled", True))

    def exchange_role(self, exchange: str) -> str:
        return str(self.exchange_setting(exchange, "role", "discovery"))

    def exchange_ccxt_id(self, exchange: str) -> str:
        return str(self.exchange_setting(exchange, "ccxt_id", exchange))

    def exchange_trust(self, exchange: str) -> float:
        return float(self.exchange_setting(exchange, "trust", 0.5))

    def exchange_weight(self, exchange: str) -> float:
        return float(self.exchange_setting(exchange, "weight", 0.5))

    def exchange_alias(self, exchange: str, symbol: str) -> str:
        aliases = (self.exchanges.get("symbol_aliases", {}) or {}).get(exchange.lower(), {}) or {}
        return str(aliases.get(symbol, symbol))

    def min_24h_volume_for_exchange(self, exchange: str, discovery: bool = False) -> float:
        if discovery:
            per = (self.universe.get("discovery_overrides") or {}).get(
                "min_24h_quote_volume_per_exchange"
            ) or {}
            if isinstance(per, dict) and exchange.lower() in per:
                return float(per[exchange.lower()])
        per = self.universe.get("min_24h_quote_volume_per_exchange") or {}
        if isinstance(per, dict) and exchange.lower() in per:
            return float(per[exchange.lower()])
        return float(self.universe.get("min_24h_quote_volume", 2_000_000))

    def universe_setting_for_discovery(self, key: str, default: Any = None) -> Any:
        overrides = self.universe.get("discovery_overrides") or {}
        if key in overrides:
            return overrides[key]
        return self.universe_setting(key, default)

    @property
    def symbols(self) -> list[str]:
        return [str(symbol).upper() for symbol in self.watchlist.get("symbols", [])]

    @property
    def timeframes(self) -> list[str]:
        return [str(tf) for tf in self.watchlist.get("timeframes", ["1h", "4h", "1d"])]

    @property
    def raw_dir(self) -> Path:
        return self.root / self.settings.get("data", {}).get("raw_dir", "data/raw")

    @property
    def processed_dir(self) -> Path:
        return self.root / self.settings.get("data", {}).get(
            "processed_dir", "data/processed"
        )

    @property
    def reports_dir(self) -> Path:
        return self.root / self.settings.get("data", {}).get("reports_dir", "data/reports")

    @property
    def db_path(self) -> Path:
        return self.root / self.settings.get("data", {}).get(
            "db_path", "db/crypto_ai_desk.sqlite"
        )

    def candle_limit(self, timeframe: str) -> int:
        limits = self.settings.get("data", {}).get("ohlcv_limit", {})
        return int(limits.get(timeframe, 220))

    def report_setting(self, key: str, default: Any = None) -> Any:
        return self.settings.get("reports", {}).get(key, default)

    def scoring_weight(self, key: str, default: float = 0.0) -> float:
        return float(self.scoring.get("weights", {}).get(key, default))

    def universe_setting(self, key: str, default: Any = None) -> Any:
        if key in self.universe:
            return self.universe.get(key, default)
        return self.watchlist.get("dynamic_universe", {}).get(key, default)


@functools.lru_cache(maxsize=8)
def _load_config_cached(project_root: Path) -> ProjectConfig:
    config_dir = project_root / "config"
    return ProjectConfig(
        root=project_root,
        settings=load_yaml(config_dir / "settings.yaml"),
        watchlist=load_yaml(config_dir / "watchlist.yaml"),
        sources=load_yaml(config_dir / "sources.yaml"),
        scoring=load_yaml(config_dir / "scoring.yaml"),
        universe=load_yaml(config_dir / "universe.yaml"),
        exchanges=load_yaml(config_dir / "exchanges.yaml"),
    )


def load_config(root: Path | None = None) -> ProjectConfig:
    """2026-07-16 watchdog investigation: load_config() re-read and re-parsed 6 YAML files from
    disk on EVERY call with zero caching. Hot paths like crypto_quality_overlay.symbol_context()
    and market_intelligence_store.default_db_path() call it once per historical trade during
    report replay -- with 823+ trades that's 2000+ calls/~15,000 YAML parses per report run,
    which is what pushed `crypto-overlay-report` past its 300s scheduler timeout (measured
    ~365s just in yaml.safe_load) and tripped the heartbeat watchdog. Each scheduler step already
    runs as its own fresh subprocess (see scripts/run_default_market_schedule.py's _cli() helper),
    so a process-lifetime cache never serves stale config across steps/cycles -- an operator's
    config edit takes effect on the next step exactly as before. ProjectConfig is frozen/immutable,
    so sharing the cached instance across callers within one process is safe."""
    project_root = (root or PROJECT_ROOT).resolve()
    return _load_config_cached(project_root)


def clear_config_cache() -> None:
    """Drop the load_config() cache. For long-lived processes (monitors, the scheduler loop
    itself) that want to pick up a config edit without a full restart, or for tests that need a
    fresh read after writing new config files under the same root path."""
    _load_config_cached.cache_clear()
