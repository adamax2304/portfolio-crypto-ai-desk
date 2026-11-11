from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.data_collectors.crypto_invest_universe import refresh_universe


def main() -> None:
    parser = argparse.ArgumentParser(description="Review the liquid Crypto Invest universe")
    parser.add_argument("--apply", action="store_true", help="replace the reviewed YAML list")
    args = parser.parse_args()
    print(json.dumps(refresh_universe(apply=args.apply), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
