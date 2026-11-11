"""Configuration for the read-only Telegram dashboard."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class DashboardConfig:
    enabled: bool
    bot_token: str
    chat_id: str
    state_path: Path
    poll_timeout_seconds: int
    refresh_seconds: int
    page_size: int
    pin_message: bool


def load_dashboard_config(root: Path) -> DashboardConfig:
    """Load dashboard settings without ever reading Telegram credentials."""
    path = root / "config" / "telegram_dashboard.yaml"
    payload: dict[str, Any] = {}
    if path.exists():
        with path.open("r", encoding="utf-8") as handle:
            payload = yaml.safe_load(handle) or {}
    block = payload.get("telegram_dashboard") or {}
    state_value = str(block.get("state_path") or "data/telegram/dashboard_state.json")
    return DashboardConfig(
        enabled=bool(block.get("enabled", False)),
        # Dashboard credentials are intentionally separate from the alert bot:
        # the dashboard needs inbound callback transport while alerts may use a
        # different webhook-connected bot.
        bot_token=str(block.get("bot_token") or "").strip(),
        chat_id=str(block.get("chat_id") or "").strip(),
        state_path=root / state_value,
        poll_timeout_seconds=max(1, int(block.get("poll_timeout_seconds", 20))),
        refresh_seconds=max(30, int(block.get("refresh_seconds", 300))),
        page_size=max(3, min(10, int(block.get("page_size", 5)))),
        pin_message=bool(block.get("pin_message", True)),
    )
