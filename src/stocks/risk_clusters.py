"""Stock risk-cluster / proxy lookup for the concentration cap overlay (2026-06-16).

Pure, read-only helpers over ``config/stock_risk_clusters.yaml``. NO scoring, NO TP/SL,
NO generation, NO DB writes — just symbol → (risk_bucket, proxy_group) classification used
by ``src/signals/portfolio_caps.py`` and the dashboards.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

_DEFAULT_CONFIG = Path(__file__).resolve().parents[2] / "config" / "stock_risk_clusters.yaml"


def normalize_symbol(symbol: str | None) -> str:
    """Upper-case, strip whitespace and a trailing exchange/quote suffix.

    Stocks are bare tickers ("AAPL"); be defensive about "AAPL.US" / "AAPL/USD" /
    lower-case input so the map lookup is robust.
    """
    if not symbol:
        return ""
    s = str(symbol).strip().upper()
    for sep in (".", "/", ":", " "):
        if sep in s:
            s = s.split(sep, 1)[0]
    return s


@lru_cache(maxsize=8)
def load_stock_risk_clusters(config_path: str | None = None) -> dict[str, Any]:
    """Load and normalize the cluster map. Cached by path. Never raises on a missing
    file — falls back to an empty map with safe defaults."""
    path = Path(config_path) if config_path else _DEFAULT_CONFIG
    defaults = {"risk_bucket": "unknown", "proxy_group": "symbol_itself"}
    symbols: dict[str, dict[str, str]] = {}
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        defaults = {**defaults, **(raw.get("defaults") or {})}
        for sym, meta in (raw.get("symbols") or {}).items():
            meta = meta or {}
            symbols[normalize_symbol(sym)] = {
                "risk_bucket": str(meta.get("risk_bucket", defaults["risk_bucket"])),
                "proxy_group": str(meta.get("proxy_group", defaults["proxy_group"])),
            }
    except FileNotFoundError:
        pass
    except Exception:
        # Malformed config must never break the pipeline; fall back to defaults.
        symbols = {}
    return {"defaults": defaults, "symbols": symbols}


def _meta_for(symbol: str | None, config_path: str | None = None) -> dict[str, str]:
    cfg = load_stock_risk_clusters(config_path)
    norm = normalize_symbol(symbol)
    if norm in cfg["symbols"]:
        return cfg["symbols"][norm]
    # Unknown symbol: its own proxy group is keyed by the symbol so it only ever
    # collapses against itself, never against an unrelated unknown name.
    return {
        "risk_bucket": cfg["defaults"]["risk_bucket"],
        "proxy_group": f'{cfg["defaults"]["proxy_group"]}:{norm}' if norm else cfg["defaults"]["proxy_group"],
    }


def get_stock_risk_bucket(symbol: str | None, config_path: str | None = None) -> str:
    return _meta_for(symbol, config_path)["risk_bucket"]


def get_stock_proxy_group(symbol: str | None, config_path: str | None = None) -> str:
    return _meta_for(symbol, config_path)["proxy_group"]
