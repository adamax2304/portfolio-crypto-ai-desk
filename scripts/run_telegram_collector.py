"""Long-running entrypoint for the Telegram realtime news collector.

Run as a background process — independent of the trading scheduler::

    py -3 scripts/run_telegram_collector.py

Exits cleanly on Ctrl+C (SIGINT). On Telethon disconnection or session
expiry the loop returns; supervise externally if you want auto-restart
(e.g. PowerShell ``while ($true) { ...; Start-Sleep 5 }``).

Safety contract:
    - reads-only relative to the trading scheduler (no scoring/strategy)
    - never sends Telegram alerts (notifier path untouched)
    - persists straight to news_items SQLite via SQLiteStore.save_news_items
"""
from __future__ import annotations

import asyncio
import logging
import signal
import sys
from pathlib import Path

# .env loader is optional.
try:  # pragma: no cover
    from dotenv import load_dotenv
except Exception:  # noqa: BLE001
    def load_dotenv(*_a, **_kw):  # type: ignore
        return False


PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def _setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


async def _amain() -> int:
    load_dotenv(PROJECT_ROOT / ".env")
    _setup_logging()

    from src.config import load_config
    from src.storage.file_store import FileStore
    from src.storage.sqlite import SQLiteStore
    from src.data_collectors.telegram_collector import TelegramCollector

    cfg = load_config(PROJECT_ROOT)
    store = FileStore(cfg)
    db = SQLiteStore(cfg.db_path)

    collector = TelegramCollector(cfg, store, db)

    loop = asyncio.get_running_loop()

    def _signal_stop(*_a):
        logging.getLogger("run_telegram_collector").info("signal received — stopping")
        collector.stop()

    # SIGINT/SIGTERM only work cleanly on Unix; on Windows we still hook
    # SIGINT for Ctrl+C. SIGTERM is best-effort.
    try:
        loop.add_signal_handler(signal.SIGINT, _signal_stop)
        loop.add_signal_handler(signal.SIGTERM, _signal_stop)
    except NotImplementedError:
        # Windows asyncio doesn't support add_signal_handler — Ctrl+C still
        # raises KeyboardInterrupt at the await boundary.
        pass

    try:
        processed = await collector.run()
        if (collector.public_fallback_required
                and collector.settings.public_html_fallback_enabled):
            processed += await collector.run_public_html_fallback()
        return processed
    except KeyboardInterrupt:
        collector.stop()
        return 0


def main() -> int:
    try:
        return asyncio.run(_amain())
    except KeyboardInterrupt:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
