"""Telegram delivery retry (PART 7) — one safe retry on transient timeout.

Pure delivery reliability: never writes a second alert row (caller dedups by
signal_id+alert_type), never touches trade logic.
"""
from __future__ import annotations

from pathlib import Path

import pytest
import requests

from src.notifiers.telegram import TelegramNotifier


def _notifier(tmp_path: Path) -> TelegramNotifier:
    cfg = tmp_path / "notifications.yaml"
    cfg.write_text("telegram:\n  bot_token: 'x:y'\n  chat_id: '123'\n  enabled: true\n", encoding="utf-8")
    return TelegramNotifier(cfg)


class _Resp:
    def raise_for_status(self):
        return None

    def json(self):
        return {"ok": True, "result": {"message_id": 1}}


def test_readtimeout_once_then_retry_succeeds(tmp_path, monkeypatch):
    calls = {"n": 0}

    def fake_post(*a, **k):
        calls["n"] += 1
        if calls["n"] == 1:
            raise requests.exceptions.ReadTimeout("boom")
        return _Resp()

    monkeypatch.setattr("src.notifiers.telegram.requests.post", fake_post)
    monkeypatch.setattr("src.notifiers.telegram.time.sleep", lambda *_: None)
    out = _notifier(tmp_path).send("hi")
    assert out["ok"] is True
    assert calls["n"] == 2  # retried exactly once


def test_readtimeout_twice_raises(tmp_path, monkeypatch):
    calls = {"n": 0}

    def fake_post(*a, **k):
        calls["n"] += 1
        raise requests.exceptions.ReadTimeout("boom")

    monkeypatch.setattr("src.notifiers.telegram.requests.post", fake_post)
    monkeypatch.setattr("src.notifiers.telegram.time.sleep", lambda *_: None)
    with pytest.raises(requests.exceptions.ReadTimeout):
        _notifier(tmp_path).send("hi")
    assert calls["n"] == 2  # one retry only, then give up (status stays error:ReadTimeout)


def test_http_error_not_retried(tmp_path, monkeypatch):
    calls = {"n": 0}

    class _ErrResp:
        def raise_for_status(self):
            raise requests.exceptions.HTTPError("429")

        def json(self):
            return {}

    def fake_post(*a, **k):
        calls["n"] += 1
        return _ErrResp()

    monkeypatch.setattr("src.notifiers.telegram.requests.post", fake_post)
    with pytest.raises(requests.exceptions.HTTPError):
        _notifier(tmp_path).send("hi")
    assert calls["n"] == 1  # non-timeout errors are NOT retried


def test_fast_send_is_single_bounded_attempt(tmp_path, monkeypatch):
    calls = []

    def fake_post(*a, **k):
        calls.append(k)
        raise requests.exceptions.ReadTimeout("boom")

    monkeypatch.setattr("src.notifiers.telegram.requests.post", fake_post)
    with pytest.raises(requests.exceptions.ReadTimeout):
        _notifier(tmp_path).send_fast("entry")
    assert len(calls) == 1
    assert calls[0]["timeout"] == (3.05, 4.0)
