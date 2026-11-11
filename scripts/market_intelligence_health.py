from __future__ import annotations

import argparse
import json

from src.intelligence.market_intelligence_health import refresh


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--send-telegram", action="store_true")
    args = parser.parse_args()
    print(json.dumps(refresh(send_telegram=args.send_telegram), indent=2, default=str))


if __name__ == "__main__":
    main()
