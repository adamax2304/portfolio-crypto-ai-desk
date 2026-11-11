"""Dedicated notifier for trade-related Telegram traffic.

The dashboard bot is intentionally also the trade-alert bot.  System/news
watchdogs continue to use ``config/notifications.yaml`` and therefore cannot
silently interfere with dashboard callback transport.
"""

from __future__ import annotations

from pathlib import Path

from src.notifiers.telegram import TelegramNotConfigured, TelegramNotifier
from src.notifiers.telegram_dashboard.config import load_dashboard_config


def notifier_for(root: Path) -> TelegramNotifier:
    """Return the dedicated trade bot; fail closed instead of falling back."""
    cfg = load_dashboard_config(root)
    if not cfg.enabled or not cfg.bot_token or not cfg.chat_id:
        raise TelegramNotConfigured(
            "Trade Telegram bot is not configured in config/telegram_dashboard.yaml."
        )
    return TelegramNotifier(
        root / "config" / "notifications.yaml",
        token_override=cfg.bot_token,
        chat_id_override=cfg.chat_id,
        enabled_override=True,
    )


__all__ = ["notifier_for"]
