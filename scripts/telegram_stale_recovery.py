"""Bounded self-healing catch-up for Telegram channels with actual health failures.

This script is scheduler-safe: it evaluates source health first, does nothing
for normally quiet channels, and reads only public `t.me/s` pages for selected
broken/no-row channels. It never opens the Telethon session, scores, routes,
alerts trades, or modifies live state.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv
except Exception:  # pragma: no cover
    def load_dotenv(*_args, **_kwargs):  # type: ignore
        return False

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def _main(args: argparse.Namespace) -> int:
    load_dotenv(PROJECT_ROOT / ".env")
    from src.config import load_config
    from src.data_collectors.telegram_collector import TelegramCollector, TelegramCollectorSettings
    from src.news.source_health import compute_source_health
    from src.news.source_telemetry import record_source_run
    from src.news.telegram_recovery import record_attempts, select_recovery_targets
    from src.storage.file_store import FileStore
    from src.storage.sqlite import SQLiteStore

    cfg = load_config(PROJECT_ROOT)
    health = compute_source_health(str(cfg.db_path))
    targets = select_recovery_targets(health, db=str(cfg.db_path), max_targets=args.max_targets)
    output: dict = {"targets": targets, "attempts": [], "processed": 0, "available": True}
    if not targets:
        print(json.dumps(output, indent=2, ensure_ascii=True))
        return 0

    db = SQLiteStore(cfg.db_path)
    db.init_db()
    settings = TelegramCollectorSettings.from_sources_yaml(getattr(cfg, "sources", {}) or {})
    try:
        collector = TelegramCollector(cfg, FileStore(cfg), db, settings=settings)
        result = collector.collect_public_html_once(
            hours=args.hours, limit_per_channel=args.limit_per_channel,
            handles={item["handle"] for item in targets},
        )
        output["processed"] = int(result.get("processed") or 0)
        output["public_html"] = result
        channel_counts = {
            str(handle).lower().lstrip("@"): int(count or 0)
            for handle, count in (result.get("channels") or {}).items()
        }
        failed_handles = {
            str(handle).lower().lstrip("@") for handle in result.get("failed_channels") or []
        }
        for target in targets:
            handle = target["handle"].lower().lstrip("@")
            if handle not in failed_handles:
                count = channel_counts.get(handle, 0)
                state, detail = (
                    ("recovered", "public HTML reachable") if count else ("reachable_empty", "public HTML reachable")
                )
                transport_status = "ok" if count else "ok_empty"
            else:
                state = "failed"
                detail = "public HTML unavailable"
                count, transport_status = 0, "error"
            output["attempts"].append({"source": target["source"], "status": state, "detail": detail})
            record_source_run(source_name=target["source"], source_type="telegram", status=transport_status,
                              item_count=count, error_code=(detail if transport_status == "error" else None),
                              error_message=(detail if transport_status == "error" else None),
                              metadata={"event": "targeted_stale_recovery", "prior_status": target["status"]},
                              db=str(cfg.db_path))
    except Exception as exc:  # non-fatal scheduler path; telemetry makes the failure visible
        output["available"] = False
        output["reason"] = f"{type(exc).__name__}: {exc}"
        for target in targets:
            output["attempts"].append({"source": target["source"], "status": "failed", "detail": output["reason"]})
            record_source_run(source_name=target["source"], source_type="telegram", status="error",
                              error_code=type(exc).__name__, error_message=str(exc),
                              metadata={"event": "targeted_stale_recovery"}, db=str(cfg.db_path))
    finally:
        record_attempts(output["attempts"], db=str(cfg.db_path))
    print(json.dumps(output, indent=2, ensure_ascii=True, default=str))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Recover only unhealthy Telegram news sources.")
    parser.add_argument("--hours", type=int, default=72)
    parser.add_argument("--limit-per-channel", type=int, default=20)
    parser.add_argument("--max-targets", type=int, default=6)
    return _main(parser.parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
