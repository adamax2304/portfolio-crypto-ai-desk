"""Two-minute fail-open fast-news monitor."""
from __future__ import annotations

import argparse
import json
import time

from src.news.fast_news import refresh, write_diagnostics


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--minutes", type=int, default=24 * 60)
    parser.add_argument("--interval-seconds", type=int, default=120)
    args = parser.parse_args()
    stop_at = time.monotonic() + max(1, args.minutes) * 60
    while time.monotonic() < stop_at:
        try:
            result = refresh()
            path = write_diagnostics(result)
            print(json.dumps({"fast_news": result, "diagnostics": str(path)}, default=str), flush=True)
        except Exception as exc:  # fail-open monitor boundary
            print(json.dumps({"fast_news_error": type(exc).__name__}), flush=True)
        remaining = max(0.0, stop_at - time.monotonic())
        if remaining:
            time.sleep(min(max(10, args.interval_seconds), remaining))


if __name__ == "__main__":
    main()
