"""Versioned provenance for raw crypto-intraday pullback entries.

This profile intentionally does not add a new entry rule. It labels the
existing point-in-time PULLBACK_LIMIT path so Paper reports and live policy no
longer have to treat profitable forward pullbacks as an unprofiled exception.
"""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import pandas as pd

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CFG: dict[str, Any] = {
    "enabled": True,
    "live_enabled": True,
    "profile_id": "crypto_intraday_pullback_paper_v1",
    "activated_at": "",
    "asset_class": "crypto",
    "mode": "intraday",
    "source_entry_mode": "PULLBACK_LIMIT",
}


def load_cfg() -> dict[str, Any]:
    path = ROOT / "config" / "crypto_intraday_pullback_paper.yaml"
    if yaml and path.exists():
        try:
            raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            user = raw.get("crypto_intraday_pullback_paper") or {}
            cfg = deepcopy(DEFAULT_CFG)
            if isinstance(user, dict):
                cfg.update(user)
            return cfg
        except Exception:
            pass
    return deepcopy(DEFAULT_CFG)


def resolve_profile(*, signal: dict[str, Any], source_entry_mode: str,
                    cfg: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return versioned provenance for a forward pullback, or no-op."""
    cfg = cfg or load_cfg()
    activated_at = pd.to_datetime(cfg.get("activated_at"), utc=True, errors="coerce")
    created_at = pd.to_datetime(signal.get("created_at"), utc=True, errors="coerce")
    applies = (
        bool(cfg.get("enabled", True))
        and str(signal.get("asset_class") or "crypto").lower()
        == str(cfg.get("asset_class") or "crypto").lower()
        and str(signal.get("mode") or "").lower()
        == str(cfg.get("mode") or "intraday").lower()
        and str(source_entry_mode or "").upper()
        == str(cfg.get("source_entry_mode") or "PULLBACK_LIMIT").upper()
        and not pd.isna(activated_at)
        and not pd.isna(created_at)
        and created_at >= activated_at
    )
    if not applies:
        return {"applied": False}
    return {
        "applied": True,
        "ready": True,
        "profile_id": str(cfg["profile_id"]),
        "entry_mode": "PULLBACK_LIMIT",
        "source_entry_mode": str(source_entry_mode).upper(),
        "reason": "versioned_intraday_pullback_point_in_time",
    }


__all__ = ["load_cfg", "resolve_profile"]
