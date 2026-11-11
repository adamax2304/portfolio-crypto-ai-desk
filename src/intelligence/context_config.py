"""Config loader shared by the optional context filters."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]


def load_context_filters() -> dict[str, Any]:
    try:
        raw = yaml.safe_load((ROOT / "config" / "context_filters.yaml").read_text(encoding="utf-8")) or {}
        cfg = raw.get("context_filters") or {}
        return cfg if isinstance(cfg, dict) else {}
    except Exception:
        return {"version": "context_filters_unavailable", "live_enabled": False}


def section(name: str) -> dict[str, Any]:
    value = load_context_filters().get(name) or {}
    return value if isinstance(value, dict) else {}


__all__ = ["load_context_filters", "section", "ROOT"]
