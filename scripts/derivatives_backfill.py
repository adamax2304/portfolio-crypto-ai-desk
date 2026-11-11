from __future__ import annotations

import argparse
import json

from src.data_collectors.derivatives_pipeline import DerivativesPipeline, active_symbols


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=30)
    parser.add_argument("--limit", type=int, default=40)
    args = parser.parse_args()
    pipeline = DerivativesPipeline()
    result = pipeline.backfill(active_symbols(args.limit), days=args.days)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
