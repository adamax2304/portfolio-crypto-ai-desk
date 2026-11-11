"""The dedicated dashboard bot receives trade traffic; health/news stay separate."""

from __future__ import annotations

from pathlib import Path

import pytest

from src.notifiers.telegram import TelegramNotConfigured
from src.notifiers.trade_telegram import notifier_for


def _write_configs(root: Path, *, dashboard_enabled: bool = True) -> None:
    config = root / "config"
    config.mkdir(parents=True)
    config.joinpath("notifications.yaml").write_text(
        "telegram:\n  enabled: true\n  bot_token: old:token\n  chat_id: '11'\n",
        encoding="utf-8",
    )
    config.joinpath("telegram_dashboard.yaml").write_text(
        "telegram_dashboard:\n"
        f"  enabled: {'true' if dashboard_enabled else 'false'}\n"
        "  bot_token: new:token\n  chat_id: '22'\n"
        "  state_path: data/telegram/state.json\n",
        encoding="utf-8",
    )


def test_trade_notifier_uses_dedicated_dashboard_bot_and_not_old_notifier(tmp_path):
    _write_configs(tmp_path)
    notifier = notifier_for(tmp_path)
    assert notifier.token == "new:token"
    assert notifier.chat_id == "22"
    assert notifier.cooldown_minutes == 30


def test_trade_notifier_fails_closed_without_enabled_dashboard_bot(tmp_path):
    _write_configs(tmp_path, dashboard_enabled=False)
    with pytest.raises(TelegramNotConfigured):
        notifier_for(tmp_path)
