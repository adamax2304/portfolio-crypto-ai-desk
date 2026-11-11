"""Telegram realtime news collector (PART 7).

Subscribes to a curated list of public Telegram channels via Telethon and
persists every received message into the ``news_items`` SQLite table using
the same schema/contract as :class:`RSSNewsCollector`. The collector is a
long-running async loop intended to be spawned as a separate process
(``scripts/run_telegram_collector.py``); it does NOT touch the trading
scheduler, the scoring/agents pipeline, or the Telegram *notifier* path —
purely an ingest layer.

Isolation contract
------------------
- Reads :data:`config/sources.yaml` -> ``telegram_channels``.
- Uses its own session file ``data/telegram/<session_name>.session``.
- Reuses ``TG_API_ID`` / ``TG_API_HASH`` (one Telegram account can have
  multiple parallel sessions — they do NOT share state with each other).
- Never reads or writes anything under the ``news_trader`` project.

Persistence contract
--------------------
For each non-empty message we build a :class:`src.models.NewsItem` and
call :meth:`SQLiteStore.save_news_items` with the channel's configured
``asset_class``. The synthetic URL is ``https://t.me/<handle>/<msg_id>``
which doubles as the SQLite ``UNIQUE`` dedup key. Re-ingesting the same
message becomes a no-op via ``ON CONFLICT(url) DO UPDATE`` (already in the
RSS code path).

The collector never sends a Telegram alert, never spawns LLM calls and
never modifies any scoring/strategy state.
"""
from __future__ import annotations

import asyncio
import logging
import os
import re
import socket
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from src.config import ProjectConfig
from src.logger import get_logger
from src.models import NewsItem
from src.news.content import clean_text, content_hash
from src.news.source_telemetry import now_iso, record_source_run
from src.storage.file_store import FileStore
from src.storage.sqlite import SQLiteStore
from src.utils.symbols import symbol_to_ticker

# Tickers whose word-boundary form is too generic to match against raw
# headlines without false positives (e.g. "near" the verb, "OP" the
# abbreviation). Mirror :data:`rss_news_collector.AMBIGUOUS_TICKERS`.
AMBIGUOUS_TICKERS = {"LINK", "NEAR", "OP", "SEI", "APT"}
_LOW_SIGNAL_EXACT = {
    "thanks for sharing",
    "wow big moves",
    "active ranking",
}
_LOW_SIGNAL_PREFIXES = (
    "/",
    "today total:",
    "active user:",
    "try to discuss daily topics",
    "users with ai generated replies",
    "i'm trading tradfi assets",
    "that's solid execution",
    "that\u2019s solid execution",
    "that's huge",
    "that\u2019s huge",
    "yeah exactly",
    "yeah that setup",
    "24h vol:",
    "btc exchange balance",
    "eth exchange balance",
    "liquidation rank",
    "oi gainers",
    "oi losers",
    "total crypto market cap update",
)
_LOW_SIGNAL_CONTAINS = (
    "gameday bonuses",
    "champion hunt",
    "referral program",
    "invite friends",
    "event runs across the community",
    "ai generated replies",
    "decrease rate & dominance:",
    "increase rate & dominance:",
    "i am gonna do big ponzi scam",
    "welcome to the group",
    "join my private group",
)
_LOOKONCHAIN_MARKET_TERMS = (
    "wallet", "address", "bought", "sold", "buying", "selling", "transferred", "transfer",
    "withdrew", "withdraw", "deposited", "deposit", "inflow", "outflow", "accumulated",
    "accumulate", "liquidat", "whale", "token", "exchange", "eth", "btc", "usdt", "$",
)
_CHAT_TERMS = ("ponzi", "dm me", "giveaway", "referral", "invite friends", "free airdrop")
_SESSION_REAUTH_MARKERS = (
    "authorization key",
    "session file",
    "session id",
    "auth key",
)


def session_reauth_required(exc: BaseException | str) -> bool:
    """Return whether Telegram has revoked the local authorization session.

    This is not a transient network error.  Retrying it in a watchdog loop only
    spams diagnostics and cannot restore access; an operator must authorize a
    fresh, project-local session once.
    """
    text = str(exc).lower()
    return any(marker in text for marker in _SESSION_REAUTH_MARKERS)


def resolve_session_name(
    base_name: str,
    *,
    per_host: bool = False,
    hostname: str | None = None,
) -> str:
    """Return a stable project session name that is safe across deployments."""
    override = os.getenv("TG_SESSION_NAME", "").strip()
    if override:
        raw = override
    elif per_host:
        raw = f"{base_name}_{hostname or socket.gethostname()}"
    else:
        raw = base_name
    clean = re.sub(r"[^A-Za-z0-9_-]+", "_", str(raw)).strip("_")
    return (clean or "crypto_ai_desk_tg")[:96]


@dataclass
class TelegramChannelConfig:
    """Single channel entry from ``config/sources.yaml``."""

    handle: str
    asset_class: str = "crypto"
    weight: float = 0.5
    primary_source: bool = False
    category: str = ""

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "TelegramChannelConfig":
        ac = str(raw.get("asset_class") or "crypto").lower()
        if ac not in ("crypto", "stocks"):
            ac = "crypto"
        return cls(
            handle=str(raw.get("handle") or "").lstrip("@"),
            asset_class=ac,
            weight=float(raw.get("weight") or 0.5),
            primary_source=bool(raw.get("primary_source")),
            category=str(raw.get("category") or ""),
        )


@dataclass
class TelegramCollectorSettings:
    enabled: bool = False
    session_name: str = "crypto_ai_desk_tg"
    session_path: str = "data/telegram"
    per_host_session: bool = False
    poll_keepalive_seconds: float = 30.0
    public_html_fallback_enabled: bool = True
    public_html_poll_seconds: float = 120.0
    channels: list[TelegramChannelConfig] = field(default_factory=list)

    @classmethod
    def from_sources_yaml(cls, sources: dict[str, Any]) -> "TelegramCollectorSettings":
        block = (sources or {}).get("telegram_channels") or {}
        ch_raw = block.get("channels") or []
        channels = [TelegramChannelConfig.from_dict(c) for c in ch_raw if c.get("handle")]
        base_session_name = str(block.get("session_name") or "crypto_ai_desk_tg")
        per_host_session = bool(block.get("per_host_session", False))
        return cls(
            enabled=bool(block.get("enabled", False)),
            session_name=resolve_session_name(
                base_session_name, per_host=per_host_session,
            ),
            session_path=str(block.get("session_path") or "data/telegram"),
            per_host_session=per_host_session,
            poll_keepalive_seconds=float(block.get("poll_keepalive_seconds") or 30.0),
            public_html_fallback_enabled=bool(block.get("public_html_fallback_enabled", True)),
            public_html_poll_seconds=float(block.get("public_html_poll_seconds") or 120.0),
            channels=channels,
        )


class TelegramCollector:
    """Async Telethon-driven news ingest.

    Use ``await TelegramCollector(config, db, store).run()`` from a runner.
    The collector idles cleanly when ``telegram_channels.enabled`` is false
    or when Telethon credentials are missing — designed so a misconfigured
    setup never crashes the parent process.
    """

    def __init__(
        self,
        config: ProjectConfig,
        store: FileStore,
        db: SQLiteStore,
        *,
        settings: TelegramCollectorSettings | None = None,
        api_id: int | None = None,
        api_hash: str | None = None,
    ) -> None:
        self.config = config
        self.store = store
        self.db = db
        self.logger = get_logger(self.__class__.__name__)
        self.settings = settings or TelegramCollectorSettings.from_sources_yaml(
            getattr(config, "sources", {}) or {}
        )
        # Credentials default to env vars (loaded via .env at runner entry).
        env_id = os.getenv("TG_API_ID", "").strip()
        self._api_id = api_id if api_id is not None else (int(env_id) if env_id.isdigit() else 0)
        self._api_hash = api_hash if api_hash is not None else os.getenv("TG_API_HASH", "").strip()
        # Ticker universes — same logic as RSSNewsCollector for parity.
        self.tickers = sorted(
            {symbol_to_ticker(symbol) for symbol in config.symbols},
            key=len,
            reverse=True,
        )
        self.narratives = config.watchlist.get("narratives", {})
        self._stocks_tickers = self._load_stocks_tickers()
        self._stop = asyncio.Event()
        self._recent_content: dict[str, dict[str, float]] = {}
        self.public_fallback_required = False

    # ── public ──────────────────────────────────────────────────────────

    def stop(self) -> None:
        """Request a graceful shutdown — safe to call from signal handlers."""
        self._stop.set()

    async def run(self) -> int:
        """Main entrypoint — returns when the stop event fires or the
        Telethon session can't be established. Returns the number of
        messages processed for visibility in tests / runner logs."""

        def _collector_status(status: str, *, error_code: str | None = None,
                              error_message: str | None = None,
                              metadata: dict[str, Any] | None = None) -> None:
            record_source_run(
                source_name="collector", source_type="telegram_collector", asset_class="all", status=status,
                error_code=error_code, error_message=error_message,
                metadata={"event": "collector_process", "channels": len(self.settings.channels), **(metadata or {})},
            )

        if not self.settings.enabled:
            _collector_status("disabled", error_code="telegram_disabled", error_message="telegram_channels.enabled=false")
            self.logger.info("telegram_channels.enabled=false — collector idle")
            return 0
        if not self.settings.channels:
            _collector_status("error", error_code="no_channels", error_message="no Telegram channels configured")
            self.logger.warning("no telegram channels configured — idle")
            return 0
        if not self._api_id or not self._api_hash:
            self.public_fallback_required = True
            _collector_status("unauthorized", error_code="missing_credentials", error_message="TG_API_ID/TG_API_HASH missing")
            self.logger.warning(
                "TG_API_ID/TG_API_HASH missing — collector idle. "
                "Set them in .env (see https://my.telegram.org)."
            )
            return 0
        try:
            from telethon import TelegramClient, events  # type: ignore
        except ImportError:
            _collector_status("error", error_code="telethon_missing", error_message="telethon not installed")
            self.logger.error("telethon not installed; collector idle. `pip install telethon`.")
            return 0

        session_dir = (Path(self.config.root) / self.settings.session_path).resolve()
        session_dir.mkdir(parents=True, exist_ok=True)
        session_path = session_dir / self.settings.session_name
        if not (session_dir / f"{self.settings.session_name}.session").exists():
            self.public_fallback_required = True
            _collector_status("unauthorized", error_code="session_missing", error_message="Telegram session file missing")
            self.logger.warning(
                "session file %s.session missing — run "
                "`py -3 scripts/setup_telegram_auth.py` once to authorize. Idle.",
                session_path,
            )
            return 0

        client = TelegramClient(str(session_path), self._api_id, self._api_hash)
        try:
            await client.connect()
            authorized = await client.is_user_authorized()
        except Exception as exc:  # noqa: BLE001
            reauth = session_reauth_required(exc)
            self.public_fallback_required = reauth
            _collector_status(
                "unauthorized" if reauth else "error",
                error_code="session_reauth_required" if reauth else type(exc).__name__,
                error_message=str(exc),
            )
            self.logger.error(
                "Telethon %s: %s — %s",
                "session requires reauthorization" if reauth else "connect failed",
                exc,
                "run setup_telegram_auth.py once" if reauth else "idling",
            )
            try:
                await client.disconnect()
            except Exception:  # noqa: BLE001
                pass
            return 0
        if not authorized:
            self.public_fallback_required = True
            _collector_status("unauthorized", error_code="session_unauthorized", error_message="Telegram session not authorized")
            self.logger.warning(
                "Telethon session not authorized — re-run setup_telegram_auth.py. Idling."
            )
            await client.disconnect()
            return 0

        try:
            me = await client.get_me()
        except Exception as exc:  # noqa: BLE001
            reauth = session_reauth_required(exc)
            self.public_fallback_required = reauth
            _collector_status(
                "unauthorized" if reauth else "error",
                error_code="session_reauth_required" if reauth else type(exc).__name__,
                error_message=str(exc),
            )
            self.logger.error("Telethon identity lookup failed: %s — idling", exc)
            await client.disconnect()
            return 0
        self.logger.info(
            "Telegram collector connected as @%s (id=%s) — listening on %d channels",
            getattr(me, "username", "?") or "?",
            getattr(me, "id", "?"),
            len(self.settings.channels),
        )
        _collector_status("ok", metadata={"event": "collector_connected", "resolved_target_count": len(self.settings.channels)})

        # Pre-resolve entities to avoid a ResolveUsernameRequest storm at
        # first message dispatch (FloodWait risk for >50 channels).
        resolved: list[tuple[TelegramChannelConfig, Any]] = []
        for ch in self.settings.channels:
            if self._stop.is_set():
                break
            try:
                entity = await asyncio.wait_for(client.get_entity(ch.handle), timeout=20.0)
                resolved.append((ch, entity))
                record_source_run(
                    source_name=f"t.me/{ch.handle}", source_type="telegram", asset_class=ch.asset_class,
                    status="ok", item_count=0,
                    metadata={"event": "entity_resolved", "category": ch.category, "collector": "telethon"},
                )
                # Soft pacing to stay under Telegram's resolve rate.
                await asyncio.sleep(0.8)
            except Exception as exc:  # noqa: BLE001
                record_source_run(
                    source_name=f"t.me/{ch.handle}", source_type="telegram", asset_class=ch.asset_class,
                    status="error", error_code=type(exc).__name__, error_message=str(exc),
                    metadata={"event": "entity_resolve", "category": ch.category},
                )
                self.logger.info("skip channel '%s' (%s)", ch.handle, type(exc).__name__)

        if not resolved:
            _collector_status("error", error_code="no_channels_resolved", error_message="no Telegram channels resolved")
            self.logger.warning("no telegram channels resolved — idle")
            await client.disconnect()
            return 0

        entities = [e for _, e in resolved]
        channels_by_id = {getattr(e, "id", None): cfg for cfg, e in resolved}

        processed = 0
        last_heartbeat = 0.0

        @client.on(events.NewMessage(chats=entities))
        async def _handler(event):  # noqa: ANN001
            nonlocal processed
            try:
                ok = await self._on_message(event, channels_by_id)
                if ok:
                    processed += 1
            except Exception:
                self.logger.exception("Telegram message handler failed")

        # Keep-alive loop — exits cleanly when stop() is called or the
        # TCP socket drops (the runner re-launches us on next cycle).
        keepalive = max(5.0, float(self.settings.poll_keepalive_seconds))
        try:
            while not self._stop.is_set():
                try:
                    await asyncio.wait_for(self._stop.wait(), timeout=keepalive)
                except asyncio.TimeoutError:
                    pass
                if self._stop.is_set():
                    break
                if not client.is_connected():
                    self.logger.warning("Telethon disconnected — exiting collector loop")
                    _collector_status("disconnected", error_code="telethon_disconnected", error_message="Telethon client disconnected")
                    for ch, _entity in resolved:
                        record_source_run(
                            source_name=f"t.me/{ch.handle}", source_type="telegram", asset_class=ch.asset_class,
                            status="disconnected", error_code="telethon_disconnected",
                            error_message="Telethon client disconnected",
                            metadata={"category": ch.category},
                        )
                    break
                if time.monotonic() - last_heartbeat >= max(300.0, keepalive * 6):
                    for ch, _entity in resolved:
                        record_source_run(
                            source_name=f"t.me/{ch.handle}", source_type="telegram", asset_class=ch.asset_class,
                            status="heartbeat", item_count=0,
                            metadata={"event": "collector_heartbeat", "category": ch.category},
                        )
                    last_heartbeat = time.monotonic()
        finally:
            try:
                await client.disconnect()
            except Exception:  # noqa: BLE001
                pass
            self.logger.info("Telegram collector stopped — processed %d messages", processed)
        return processed

    def collect_public_html_once(
        self,
        *,
        hours: int = 24,
        handles: set[str] | None = None,
        limit_per_channel: int | None = None,
    ) -> dict[str, Any]:
        """Poll public ``t.me/s`` pages without opening the Telethon session.

        This is a continuity path, not a replacement for event-driven Telethon.
        It uses the same NewsItem builder, URL dedupe and entity resolver input,
        while preserving publisher time separately from the desk's observation
        time. Private/restricted channels simply surface as source errors.
        """
        import requests
        from bs4 import BeautifulSoup

        cutoff = datetime.now(timezone.utc) - timedelta(hours=max(1, int(hours)))
        wanted_handles = (
            {str(handle).strip().lower().lstrip("@") for handle in handles if str(handle).strip()}
            if handles
            else None
        )
        bounded_limit = max(1, int(limit_per_channel)) if limit_per_channel is not None else None
        result: dict[str, Any] = {
            "processed": 0,
            "ok": 0,
            "failed": 0,
            "channels": {},
            "failed_channels": [],
        }
        headers = {"User-Agent": "Mozilla/5.0 (compatible; CryptoAIDeskNews/1.0)"}
        for cfg in self.settings.channels:
            handle = cfg.handle.lstrip("@")
            if wanted_handles is not None and handle.lower() not in wanted_handles:
                continue
            source = f"t.me/{handle}"
            saved = 0
            considered = 0
            try:
                response = requests.get(
                    f"https://t.me/s/{handle}", headers=headers, timeout=(5.0, 15.0),
                )
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
                for node in soup.select("div.tgme_widget_message_wrap"):
                    message = node.select_one("div.tgme_widget_message")
                    body_node = node.select_one("div.tgme_widget_message_text")
                    time_node = node.select_one("time[datetime]")
                    if message is None or body_node is None or time_node is None:
                        continue
                    post = str(message.get("data-post") or "")
                    if "/" not in post:
                        continue
                    post_handle, post_id = post.rsplit("/", 1)
                    try:
                        published = datetime.fromisoformat(
                            str(time_node.get("datetime") or "").replace("Z", "+00:00")
                        ).astimezone(timezone.utc)
                    except (TypeError, ValueError):
                        continue
                    if published < cutoff:
                        continue
                    body = body_node.get_text(" ", strip=True)
                    if not body or self._is_low_signal_message(body, cfg=cfg):
                        continue
                    if bounded_limit is not None and considered >= bounded_limit:
                        break
                    considered += 1
                    title = " ".join(body.split())
                    if len(title) > 280:
                        title = title[:277] + "..."
                    item = self._build_item(
                        title=title,
                        body=body,
                        url=f"https://t.me/{post_handle}/{post_id}",
                        published_iso=published.replace(microsecond=0).isoformat(),
                        source_name=source,
                        cfg=cfg,
                        source_message_id=post_id,
                        source_channel_id=post_handle,
                    )
                    if self._is_runtime_duplicate(item):
                        continue
                    self.db.save_news_items([item], asset_class=cfg.asset_class)
                    saved += 1
                record_source_run(
                    source_name=source, source_type="telegram", asset_class=cfg.asset_class,
                    status="ok" if saved else "ok_empty", item_count=saved,
                    metadata={"event": "public_html_fallback", "category": cfg.category},
                )
                result["ok"] += 1
            except Exception as exc:  # noqa: BLE001
                result["failed"] += 1
                result["failed_channels"].append(handle)
                record_source_run(
                    source_name=source, source_type="telegram", asset_class=cfg.asset_class,
                    status="error", error_code=type(exc).__name__, error_message=str(exc),
                    metadata={"event": "public_html_fallback", "category": cfg.category},
                )
            result["channels"][handle] = saved
            result["processed"] += saved
        record_source_run(
            source_name="collector_public_html", source_type="telegram_collector",
            asset_class="all", status="ok" if result["ok"] else "error",
            item_count=result["processed"], metadata={"event": "public_html_fallback_cycle", **result},
        )
        return result

    async def run_public_html_fallback(self) -> int:
        """Continuously poll public channels until the process is stopped."""
        total = 0
        interval = max(60.0, float(self.settings.public_html_poll_seconds))
        self.logger.warning(
            "Telethon unavailable; public Telegram HTML fallback active every %.0fs", interval,
        )
        while not self._stop.is_set():
            cycle = await asyncio.to_thread(self.collect_public_html_once)
            processed = int(cycle.get("processed") or 0)
            total += processed
            self.logger.info(
                "public Telegram HTML fallback cycle complete: processed=%d ok=%s failed=%s",
                processed,
                cycle.get("ok", 0),
                cycle.get("failed", 0),
            )
            try:
                await asyncio.wait_for(self._stop.wait(), timeout=interval)
            except asyncio.TimeoutError:
                pass
        return total

    async def catch_up_recent(
        self,
        *,
        hours: int = 72,
        limit_per_channel: int = 30,
        handles: set[str] | None = None,
    ) -> dict[str, Any]:
        """One-shot historical catch-up for configured channels.

        The long-running collector only receives future ``NewMessage`` events. After adding new
        sources we need a safe way to prove they are reachable and populate recent context without
        waiting for the next message. This method fetches recent messages from Telegram, persists
        them to ``news_items`` through the same ``_build_item`` path, and exits. It never sends
        Telegram alerts and never touches scoring/signals/routing/live state.
        """
        out: dict[str, Any] = {
            "available": False,
            "hours": int(hours),
            "limit_per_channel": int(limit_per_channel),
            "resolved": [],
            "failed": [],
            "processed": 0,
        }
        if not self.settings.enabled or not self.settings.channels:
            out["reason"] = "telegram disabled or no channels configured"
            return out
        if not self._api_id or not self._api_hash:
            out["reason"] = "TG_API_ID/TG_API_HASH missing"
            return out
        try:
            from telethon import TelegramClient  # type: ignore
        except ImportError:
            out["reason"] = "telethon not installed"
            return out

        session_dir = (Path(self.config.root) / self.settings.session_path).resolve()
        session_path = session_dir / self.settings.session_name
        if not (session_dir / f"{self.settings.session_name}.session").exists():
            out["reason"] = f"session file missing: {session_path}.session"
            return out

        wanted = {h.lower().lstrip("@") for h in handles} if handles else None
        channels = [
            ch for ch in self.settings.channels
            if wanted is None or ch.handle.lower().lstrip("@") in wanted
        ]
        cutoff = datetime.now(timezone.utc) - timedelta(hours=int(hours))
        client = TelegramClient(str(session_path), self._api_id, self._api_hash)
        try:
            await client.connect()
            if not await client.is_user_authorized():
                out["reason"] = "Telethon session not authorized"
                return out
            out["available"] = True
            for ch in channels:
                try:
                    entity = await asyncio.wait_for(client.get_entity(ch.handle), timeout=20.0)
                except Exception as exc:  # noqa: BLE001
                    out["failed"].append({"handle": ch.handle, "error": type(exc).__name__})
                    await asyncio.sleep(0.8)
                    continue
                username = (getattr(entity, "username", "") or ch.handle).lstrip("@")
                seen = saved = 0
                try:
                    async for msg in client.iter_messages(entity, limit=int(limit_per_channel)):
                        text = (getattr(msg, "message", None) or "").strip()
                        if not text:
                            continue
                        if self._is_low_signal_message(text, cfg=ch):
                            continue
                        msg_dt = (
                            msg.date.astimezone(timezone.utc).replace(microsecond=0)
                            if msg.date else datetime.now(timezone.utc).replace(microsecond=0)
                        )
                        if msg_dt < cutoff:
                            continue
                        title = " ".join(text.splitlines()).strip()
                        if len(title) > 280:
                            title = title[:277] + "..."
                        item = self._build_item(
                            title=title,
                            body=text,
                            url=f"https://t.me/{username}/{msg.id}",
                            published_iso=msg_dt.isoformat(),
                            source_name=f"t.me/{username}",
                            cfg=ch,
                            source_message_id=str(msg.id),
                            source_channel_id=str(getattr(entity, "id", "") or ""),
                        )
                        if self._is_runtime_duplicate(item):
                            continue
                        self.db.save_news_items([item], asset_class=ch.asset_class)
                        seen += 1
                        saved += 1
                except Exception as exc:  # noqa: BLE001
                    out["failed"].append({"handle": ch.handle, "error": type(exc).__name__})
                    record_source_run(
                        source_name=f"t.me/{ch.handle}", source_type="telegram", asset_class=ch.asset_class,
                        status="error", error_code=type(exc).__name__, error_message=str(exc),
                        metadata={"event": "catch_up", "category": ch.category},
                    )
                else:
                    record_source_run(
                        source_name=f"t.me/{username}", source_type="telegram", asset_class=ch.asset_class,
                        status="ok" if saved else "ok_empty", item_count=saved,
                        metadata={"event": "catch_up", "category": ch.category, "seen": seen},
                    )
                out["resolved"].append({"handle": ch.handle, "source": f"t.me/{username}",
                                        "seen": seen, "saved": saved})
                out["processed"] += saved
                await asyncio.sleep(0.8)
        finally:
            try:
                await client.disconnect()
            except Exception:
                pass
        return out

    # ── message handling ───────────────────────────────────────────────

    async def _on_message(
        self,
        event: Any,
        channels_by_id: dict[int, TelegramChannelConfig],
    ) -> bool:
        msg = event.message
        text = (getattr(msg, "message", None) or "").strip()
        if not text:
            return False
        chat = event.chat or await event.get_chat()
        username = (getattr(chat, "username", "") or "").lstrip("@")
        cfg = channels_by_id.get(getattr(chat, "id", None))
        if cfg is None:
            # Defensive: should never happen because we passed pre-resolved entities.
            return False
        if self._is_low_signal_message(text, cfg=cfg):
            return False

        published_iso = (
            msg.date.astimezone(timezone.utc).replace(microsecond=0).isoformat()
            if msg.date
            else datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        )
        url = f"https://t.me/{username or cfg.handle}/{msg.id}"
        title_one_line = " ".join(text.splitlines()).strip()
        if len(title_one_line) > 280:
            title_one_line = title_one_line[:277] + "..."

        item = self._build_item(
            title=title_one_line,
            body=text,
            url=url,
            published_iso=published_iso,
            source_name=f"t.me/{username or cfg.handle}",
            cfg=cfg,
            source_message_id=str(getattr(msg, "id", "") or ""),
            source_channel_id=str(getattr(chat, "id", "") or ""),
        )
        if self._is_runtime_duplicate(item):
            return False
        # Save with the channel's asset_class so news_items gets the right tag.
        self.db.save_news_items([item], asset_class=cfg.asset_class)
        self.logger.debug("[tg] %s: %s", item.source, title_one_line[:120])
        return True

    def _build_item(
        self,
        *,
        title: str,
        body: str,
        url: str,
        published_iso: str,
        source_name: str,
        cfg: TelegramChannelConfig,
        source_message_id: str | None = None,
        source_channel_id: str | None = None,
    ) -> NewsItem:
        clean_body = clean_text(body)
        text = f"{title} {clean_body}"
        if cfg.asset_class == "stocks":
            ticker_universe = self._stocks_tickers + self.tickers
        else:
            ticker_universe = self.tickers
        detected_symbols = [t for t in ticker_universe if self._mentions_ticker(text, t)]

        # Curated entity-alias matcher — only for crypto channels, mirrors
        # RSSNewsCollector behaviour. Read-only; never breaks ingest.
        if cfg.asset_class != "stocks":
            try:
                from src.catalysts.entity_aliases import get_matcher

                alias_hits = get_matcher(str(self.config.root)).detect(text)
                for sym in alias_hits:
                    base = sym.split("/")[0]
                    if base and base not in detected_symbols:
                        detected_symbols.append(base)
            except Exception:
                pass

        detected_narratives = self._detect_narratives(text)
        # Importance heuristic: base + symbol hits + narrative hits +
        # primary-source bonus + channel-weight nudge.
        importance = 1.0 + min(len(detected_symbols), 4) * 0.5 + min(len(detected_narratives), 3) * 0.4
        if cfg.primary_source:
            importance += 0.8
        # Map channel weight (0.5..0.95) to a small +0..+0.6 nudge so a
        # high-weight Bloomberg/DeItaone headline ranks above a low-weight
        # CoinTelegraph blurb even without ticker hits.
        importance += max(0.0, (cfg.weight - 0.5) * 1.2)

        verification = (
            "primary_source"
            if cfg.primary_source
            else ("single_source" if cfg.weight >= 0.8 else "single_source")
        )
        observed_at = now_iso()
        return NewsItem(
            title=title,
            source=source_name,
            url=url,
            published_at=published_iso,
            detected_symbols=detected_symbols,
            detected_narratives=detected_narratives,
            importance=round(importance, 2),
            verification_status=verification,
            content=clean_body or None,
            ingested_at=observed_at,
            first_seen_at=observed_at,
            available_at=observed_at,
            content_hash=content_hash(title, clean_body),
            source_message_id=source_message_id,
            source_channel_id=source_channel_id,
            source_category=cfg.category or None,
        )

    def _is_runtime_duplicate(self, item: NewsItem, *, window_seconds: float = 900.0) -> bool:
        """Suppress repeated identical payloads from the same channel in one process.

        Different channels are intentionally independent so corroboration is
        preserved; URL-level SQLite dedup remains the durable guard.
        """
        if not item.content_hash:
            return False
        now = time.monotonic()
        bucket = self._recent_content.setdefault(item.source, {})
        for key, seen_at in list(bucket.items()):
            if now - seen_at > window_seconds:
                bucket.pop(key, None)
        if item.content_hash in bucket:
            return True
        bucket[item.content_hash] = now
        return False

    def _load_stocks_tickers(self) -> list[str]:
        try:
            from src.stocks import load_stocks_config

            scfg = load_stocks_config(self.config.root)
            return sorted({s.upper() for s in scfg.default_symbols}, key=len, reverse=True)
        except Exception as exc:  # noqa: BLE001
            self.logger.debug("stocks tickers unavailable: %s", exc)
            return []

    def _detect_narratives(self, text: str) -> list[str]:
        upper_text = text.upper()
        detected: list[str] = []
        for name, payload in self.narratives.items():
            keywords = [str(item).upper() for item in payload.get("keywords", [])]
            symbols = [str(item).upper() for item in payload.get("symbols", [])]
            if any(keyword in upper_text for keyword in keywords) or any(
                self._mentions_ticker(text, symbol) for symbol in symbols
            ):
                detected.append(str(name))
        return detected

    @staticmethod
    def _mentions_ticker(text: str, ticker: str) -> bool:
        token = ticker.upper()
        patterns = [rf"\${re.escape(token)}(?![A-Za-z0-9])", rf"#{re.escape(token)}(?![A-Za-z0-9])"]
        if token not in AMBIGUOUS_TICKERS:
            patterns.append(rf"(?<![A-Za-z0-9]){re.escape(token)}(?![A-Za-z0-9])")
        patterns.append(rf"(?<![A-Za-z0-9]){re.escape(token)}/USDT(?![A-Za-z0-9])")
        return any(re.search(pattern, text) for pattern in patterns)

    @staticmethod
    def _is_low_signal_message(text: str, cfg: TelegramChannelConfig | None = None) -> bool:
        """Drop obvious Telegram bot/community chatter before it reaches news_items."""
        one = " ".join(str(text or "").split()).strip()
        if len(one) < 8:
            return True
        lower = one.lower()
        if lower in _LOW_SIGNAL_EXACT:
            return True
        if any(lower.startswith(prefix) for prefix in _LOW_SIGNAL_PREFIXES):
            return True
        if any(fragment in lower for fragment in _LOW_SIGNAL_CONTAINS):
            return True
        if "active user:" in lower and "person" in lower:
            return True
        # lookonchain has recently carried repeated conversational/scam chatter
        # alongside its wallet alerts.  Keep market observations, but quarantine
        # obvious non-market messages from this source only.
        handle = (cfg.handle if cfg else "").lower().lstrip("@")
        if handle == "lookonchain" and any(term in lower for term in _CHAT_TERMS):
            if not any(term in lower for term in _LOOKONCHAIN_MARKET_TERMS):
                return True
        return False
