"""Structured / paid-API news provider adapters (2026-07-03) — interface + clean-disabled.

A uniform provider interface for future paid feeds (Benzinga, Finnhub, Polygon, IEX/Tiingo). When
the API key env var is absent the provider is DISABLED with a clear reason and `fetch()` returns []
— NEVER a hard failure. When a key is present the provider can fetch and normalize into the shared
`news_items` schema. No keys are shipped; this only prepares the plumbing + diagnostics.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class ProviderStatus:
    name: str
    enabled: bool
    reason: str
    asset_class: str
    env_var: str
    source_type: str = "api"

    def to_dict(self) -> dict[str, Any]:
        return {"source": self.name, "source_type": self.source_type, "enabled": self.enabled,
                "asset_class": self.asset_class, "reason": self.reason, "env_var": self.env_var}


@dataclass
class NewsProvider:
    name: str
    env_var: str
    asset_class: str
    docs: str
    _fetch_impl: Callable[[str, int], list[dict]] | None = None

    def api_key(self) -> str | None:
        v = os.environ.get(self.env_var)
        return v.strip() if v and v.strip() else None

    def status(self) -> ProviderStatus:
        key = self.api_key()
        return ProviderStatus(
            name=self.name, enabled=bool(key), asset_class=self.asset_class, env_var=self.env_var,
            reason=("api key present" if key else f"disabled — set {self.env_var} to enable ({self.docs})"))

    def fetch(self, *, limit: int = 50) -> list[dict[str, Any]]:
        """Normalized rows (title/source/url/published_at/asset_class/detected_symbols/importance) or
        [] when disabled. Fail-open: never raises for a missing key or network error."""
        if not self.api_key():
            return []
        if self._fetch_impl is None:
            return []            # key present but no live impl wired yet (interface stub)
        try:
            return self._fetch_impl(self.api_key(), limit) or []
        except Exception:
            return []


# Registry — all disabled until the operator sets the corresponding env var. Normalized schema is the
# same as RSS/telegram ingest so source-health + symbol-audit cover these providers uniformly.
PROVIDERS: list[NewsProvider] = [
    NewsProvider("Benzinga News API", "BENZINGA_API_KEY", "stocks", "benzinga.com/apis"),
    NewsProvider("Polygon news", "POLYGON_API_KEY", "stocks", "polygon.io/docs"),
    NewsProvider("Tiingo/IEX news", "TIINGO_API_KEY", "stocks", "tiingo.com/documentation"),
    # macro / calendar / fundamentals data providers (key-gated; disabled until a key is set)
    NewsProvider("FRED (macro rates/yields/DXY)", "FRED_API_KEY", "macro", "fred.stlouisfed.org/docs/api"),
    NewsProvider("Alpha Vantage (fallback)", "ALPHAVANTAGE_API_KEY", "stocks", "alphavantage.co/documentation"),
    NewsProvider("FMP (earnings/calendar)", "FMP_API_KEY", "stocks", "site.financialmodelingprep.com/developer/docs"),
]

# Keyless FREE data providers that ARE production-enabled now (no API key required).
KEYLESS_PROVIDERS = [
    {"source": "DefiLlama", "source_type": "api", "asset_class": "crypto", "enabled": True,
     "reason": "free public API (TVL/fees/stablecoins) — no key", "production_enabled": True},
    {"source": "Stooq (stocks/index fallback)", "source_type": "api", "asset_class": "stocks",
     "enabled": True, "reason": "free CSV endpoint (historical/index fallback) — no key",
     "production_enabled": True},
]


def all_provider_statuses() -> list[dict[str, Any]]:
    """Key-gated providers + keyless free providers, for the source-health dashboard."""
    return provider_statuses() + [dict(p) for p in KEYLESS_PROVIDERS]


def provider_statuses() -> list[dict[str, Any]]:
    """Status of every structured provider for the source-health dashboard. Read-only."""
    return [p.status().to_dict() for p in PROVIDERS]
