"""Telegram bot notifier.

Reads token + chat_id from ``config/notifications.yaml``. ``detect_chat_id``
hits ``getUpdates`` to find the chat that most recently /start'd the bot —
this is the no-paste setup flow used by ``telegram-setup`` CLI command.

All network calls go through ``requests`` with short timeouts so the
monitor loop never hangs.
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

import requests
import yaml


TELEGRAM_API = "https://api.telegram.org/bot{token}/{method}"


class TelegramNotConfigured(Exception):
    pass


class TelegramNotifier:
    def __init__(self, config_path: Path, *, token_override: str | None = None,
                 chat_id_override: str | None = None,
                 enabled_override: bool | None = None):
        self.config_path = config_path
        self._cfg = self._load()
        self._token_override = token_override
        self._chat_id_override = chat_id_override
        self._enabled_override = enabled_override

    def _load(self) -> dict[str, Any]:
        if not self.config_path.exists():
            return {}
        with self.config_path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
        return data.get("telegram") or {}

    def reload(self) -> None:
        self._cfg = self._load()

    @property
    def token(self) -> str:
        return str(self._token_override if self._token_override is not None
                   else self._cfg.get("bot_token") or "").strip()

    @property
    def chat_id(self) -> str:
        return str(self._chat_id_override if self._chat_id_override is not None
                   else self._cfg.get("chat_id") or "").strip()

    @property
    def enabled(self) -> bool:
        enabled = (self._enabled_override if self._enabled_override is not None
                   else bool(self._cfg.get("enabled", True)))
        return bool(enabled) and bool(self.token)

    @property
    def cooldown_minutes(self) -> int:
        return int(self._cfg.get("cooldown_minutes", 30))

    def send(self, text: str, parse_mode: str = "Markdown") -> dict[str, Any]:
        if not self.enabled:
            raise TelegramNotConfigured("Telegram notifier disabled or missing token.")
        if not self.chat_id:
            raise TelegramNotConfigured(
                "chat_id is empty. Run `python -m src.cli telegram-setup` after sending /start to the bot."
            )
        url = TELEGRAM_API.format(token=self.token, method="sendMessage")
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": parse_mode,
            "disable_web_page_preview": True,
        }
        # One safe retry on a TRANSIENT timeout only (the common cause of
        # `error:ReadTimeout` delivery gaps). Idempotency of the alert ROW is
        # preserved by the caller's (signal_id, alert_type) dedup — this retry
        # only re-attempts the network send, never writes a second alert row and
        # never touches trade logic. Non-timeout errors (HTTP 4xx/5xx) are NOT
        # retried (raise immediately) so we don't hammer a real failure.
        last_exc: Exception | None = None
        for attempt in range(2):
            try:
                response = requests.post(url, json=payload, timeout=15)
                response.raise_for_status()
                return response.json()
            except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout) as exc:
                last_exc = exc
                if attempt == 0:
                    time.sleep(1.5)
                    continue
                raise
        raise last_exc  # pragma: no cover - loop always returns or raises above

    def send_fast(self, text: str, parse_mode: str = "Markdown") -> dict[str, Any]:
        """Send from a latency-critical trading path with a bounded wait.

        A paper-entry decision is already frozen into the MEXC handoff before
        this method is called.  Waiting through two 15-second Telegram timeouts
        would still stall the pending tracker and delay every later candidate.
        Use one short attempt here; the durable Telegram outbox owns retries.
        """
        if not self.enabled:
            raise TelegramNotConfigured("Telegram notifier disabled or missing token.")
        if not self.chat_id:
            raise TelegramNotConfigured(
                "chat_id is empty. Run `python -m src.cli telegram-setup` after sending /start to the bot."
            )
        url = TELEGRAM_API.format(token=self.token, method="sendMessage")
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": parse_mode,
            "disable_web_page_preview": True,
        }
        # Separate connect/read limits keep DNS/TLS trouble from consuming a
        # whole 30-second pending-monitor cadence.
        response = requests.post(url, json=payload, timeout=(3.05, 4.0))
        response.raise_for_status()
        return response.json()

    def detect_chat_id(self) -> str | None:
        """Read recent updates and pick the most-recent chat that sent /start.

        Returns the chat_id string if found, ``None`` otherwise.
        """
        if not self.token:
            raise TelegramNotConfigured("No bot_token configured.")
        url = TELEGRAM_API.format(token=self.token, method="getUpdates")
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        if not data.get("ok"):
            return None
        candidate: str | None = None
        for update in data.get("result") or []:
            message = update.get("message") or update.get("edited_message") or {}
            chat = message.get("chat") or {}
            chat_id = chat.get("id")
            if chat_id is None:
                continue
            candidate = str(chat_id)
        return candidate

    def save_chat_id(self, chat_id: str) -> None:
        """Persist chat_id back into the YAML config."""
        if not self.config_path.exists():
            payload: dict[str, Any] = {}
        else:
            with self.config_path.open("r", encoding="utf-8") as handle:
                payload = yaml.safe_load(handle) or {}
        block = payload.setdefault("telegram", {})
        block["chat_id"] = str(chat_id)
        with self.config_path.open("w", encoding="utf-8") as handle:
            yaml.safe_dump(payload, handle, sort_keys=False, allow_unicode=True)
        self.reload()
