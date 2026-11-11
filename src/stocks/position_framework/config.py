"""Config loader for the Stocks Position Framework (shadow-only)."""
from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None

# repo root = crypto-ai-desk/ (config.py is at src/stocks/position_framework/config.py)
_ROOT = Path(__file__).resolve().parents[3]
CONFIG_PATH = _ROOT / "config" / "stocks" / "position_framework.yaml"
DEFAULT_DB_PATH = _ROOT / "db" / "crypto_ai_desk.sqlite"

_FALLBACK: dict[str, Any] = {
    "enabled": True,
    "scheduler_enabled": True,
    "shadow_only": True,
    "write_proposed_signals": False,
    "active_playbooks": ["stocks_swing_growth_breakout"],
    "disabled_playbooks": {},
    "paper_equity_usd": 5000,
    "universe": {"max_symbols": 75, "min_price": 10, "min_avg_dollar_volume_30d": 25_000_000},
    "market_filter": {"require_spy_above_50d": True, "reject_if_spy_below_200d": True,
                      "reject_if_vix_above": 30, "warn_if_vix_above": 22},
    "sector_filter": {"require_sector_above_50d": True, "require_sector_rs_positive_vs_spy": True},
    "stock_filter": {"require_above_50d": True, "require_above_200d": True,
                     "require_rs_positive_vs_spy": True, "require_rs_positive_vs_sector": False,
                     "near_high_lookbacks": [63, 126, 252], "near_high_max_pct_below": 12,
                     "min_volume_ratio": 1.1},
    "setups": {}, "risk": {}, "exits": {}, "evidence_gate": {},
}


def load_config(path: str | Path | None = None) -> dict[str, Any]:
    """Return the `position_framework` sub-dict from the YAML (or a safe fallback)."""
    p = Path(path) if path else CONFIG_PATH
    if yaml is not None and p.exists():
        try:
            with open(p, "r", encoding="utf-8") as fh:
                data = yaml.safe_load(fh) or {}
            pf = data.get("position_framework")
            if isinstance(pf, dict):
                return pf
        except Exception:
            pass
    return dict(_FALLBACK)


def active_playbooks(cfg: dict[str, Any] | None = None) -> list[str]:
    cfg = cfg or load_config()
    return list(cfg.get("active_playbooks") or [])


def is_shadow_only(cfg: dict[str, Any] | None = None) -> bool:
    cfg = cfg or load_config()
    # Fail SAFE: default True. Only an explicit False could ever flip it (and nothing does that).
    return bool(cfg.get("shadow_only", True))


# Fetchable sector ETFs (must match SectorETFCollector / StocksConfig.sector_etfs values).
FETCHABLE_SECTOR_ETFS = {"XLK", "SMH", "XLF", "XLE", "XLY", "XLV",
                         "XLC", "XLI", "XLU", "XLRE", "XLB", "XLP"}


def universe_symbols(cfg: dict[str, Any] | None = None) -> list[str]:
    cfg = cfg or load_config()
    return [s.upper() for s in ((cfg.get("universe") or {}).get("symbols") or [])]


def sector_map(cfg: dict[str, Any] | None = None) -> dict[str, str]:
    cfg = cfg or load_config()
    return {k.upper(): v for k, v in (cfg.get("sector_map") or {}).items()}


def validate_universe(cfg: dict[str, Any] | None = None) -> list[str]:
    """Return config-completeness issues (empty list = clean):
      * a universe symbol missing from sector_map;
      * a sector_map ETF that is not one the collectors fetch.
    Live-data availability (SPY/QQQ/VIX/sector bars) is enforced at scan time by the detector,
    which REJECTS on missing data rather than passing neutral — this only guards the static config.
    """
    cfg = cfg or load_config()
    syms = universe_symbols(cfg)
    smap = sector_map(cfg)
    issues: list[str] = []
    for s in syms:
        if s not in smap:
            issues.append(f"{s}: missing from sector_map")
    for sym, etf in smap.items():
        if etf not in FETCHABLE_SECTOR_ETFS:
            issues.append(f"{sym}: maps to non-fetchable ETF {etf!r}")
    return issues
