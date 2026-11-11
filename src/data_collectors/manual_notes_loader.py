"""Load manual narrative + social notes from data/manual/*.yaml.

The desk intentionally keeps a manual surface so the user can inject signals
that no free API exposes (Telegram alpha, niche X accounts, rumor flags).
Manual notes never auto-trade — they only adjust attention/narrative scores.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def load_manual_social_notes(root: Path) -> list[dict[str, Any]]:
    data = _load_yaml(root / "data" / "manual" / "social_notes.yaml")
    notes = data.get("notes") or []
    cleaned: list[dict[str, Any]] = []
    for raw in notes:
        if not isinstance(raw, dict):
            continue
        ticker = str(raw.get("ticker") or raw.get("symbol") or "").upper().split("/")[0]
        if not ticker:
            continue
        cleaned.append(
            {
                "ticker": ticker,
                "narrative": str(raw.get("narrative") or ""),
                "source": str(raw.get("source") or ""),
                "note": str(raw.get("note") or ""),
                "timestamp": str(raw.get("timestamp") or ""),
                "sentiment": str(raw.get("sentiment") or "neutral").lower(),
                "confidence": str(raw.get("confidence") or "low").lower(),
                "verification": str(raw.get("verification") or "single_source").lower(),
            }
        )
    return cleaned


def load_manual_narrative_notes(root: Path) -> list[dict[str, Any]]:
    data = _load_yaml(root / "data" / "manual" / "narrative_notes.yaml")
    notes = data.get("notes") or []
    cleaned: list[dict[str, Any]] = []
    for raw in notes:
        if not isinstance(raw, dict):
            continue
        narrative = str(raw.get("narrative") or "").strip()
        if not narrative:
            continue
        cleaned.append(
            {
                "narrative": narrative,
                "stage": str(raw.get("stage") or "unknown").lower(),
                "note": str(raw.get("note") or ""),
                "confidence": str(raw.get("confidence") or "low").lower(),
                "timestamp": str(raw.get("timestamp") or ""),
                "representative_symbols": [
                    str(item).upper() for item in (raw.get("representative_symbols") or [])
                ],
            }
        )
    return cleaned
