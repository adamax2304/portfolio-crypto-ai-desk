"""One-shot Telegram news catch-up for configured channels.

This is a production ingest helper for `news_items` only. It reads configured public Telegram
channels through their public `t.me/s` pages and the same TelegramCollector normalization path used
by the live listener. It never opens the Telethon session, sends Telegram alerts, or touches
signals, scores, routing, or live state.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv
except Exception:  # pragma: no cover
    def load_dotenv(*_a, **_kw):  # type: ignore
        return False


PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def _main(args: argparse.Namespace) -> int:
    load_dotenv(PROJECT_ROOT / ".env")
    from src.config import load_config
    from src.data_collectors.telegram_collector import TelegramCollector
    from src.data_collectors.telegram_collector import TelegramCollectorSettings
    from src.storage.file_store import FileStore
    from src.storage.sqlite import SQLiteStore

    cfg = load_config(PROJECT_ROOT)
    db = SQLiteStore(cfg.db_path)
    db.init_db()
    settings = TelegramCollectorSettings.from_sources_yaml(getattr(cfg, "sources", {}) or {})
    collector = TelegramCollector(cfg, FileStore(cfg), db, settings=settings)
    handles = {h.strip().lstrip("@") for h in (args.handles or "").split(",") if h.strip()}
    result = collector.collect_public_html_once(
        hours=args.hours,
        limit_per_channel=args.limit_per_channel,
        handles=handles or None,
    )
    print(json.dumps(result, indent=2, ensure_ascii=True, default=str))
    return 0 if result.get("ok") else 2


def main() -> int:
    ap = argparse.ArgumentParser(description="Catch up recent Telegram news into news_items.")
    ap.add_argument("--hours", type=int, default=72)
    ap.add_argument("--limit-per-channel", type=int, default=30)
    ap.add_argument(
        "--handles",
        default="",
        help="Comma-separated configured handles to catch up. Empty = all configured channels.",
    )
    return _main(ap.parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
