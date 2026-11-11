from __future__ import annotations

import argparse
import json

from src.quality_agents.llm_advisory import refresh_openrouter_advisory


def main() -> None:
    parser = argparse.ArgumentParser(description="Refresh OpenRouter-backed quality-agent advisory cache")
    parser.add_argument("--db", default=None)
    parser.add_argument("--lookback-hours", type=float, default=None)
    parser.add_argument("--max-events", type=int, default=None)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    result = refresh_openrouter_advisory(
        db=args.db,
        lookback_hours=args.lookback_hours,
        max_events=args.max_events,
        force=args.force,
    )
    print(json.dumps(result, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
