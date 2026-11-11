from __future__ import annotations

import argparse
import json

from src.maintenance.market_intelligence_retention import run


def main() -> int:
    parser = argparse.ArgumentParser(description="Archive bounded old market-intelligence rows.")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--max-rows-per-table", type=int, default=250_000)
    parser.add_argument("--archive-dir")
    args = parser.parse_args()
    result = run(
        dry_run=not args.apply,
        max_rows_per_table=args.max_rows_per_table,
        archive_dir=args.archive_dir,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
