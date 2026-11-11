from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_manual_events(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        events = yaml.safe_load(f) or []
    if not isinstance(events, list):
        return []
    return [event for event in events if isinstance(event, dict)]
