from __future__ import annotations

import argparse
import json

from src.quality_agents.report import write_effectiveness_report
from src.quality_agents.runner import refresh_post_trade_diagnostics


def main() -> None:
    parser = argparse.ArgumentParser(description="Refresh quality-agent diagnostics and evidence report")
    parser.add_argument("--db", default=None)
    parser.add_argument("--lookback-days", type=int, default=30)
    args = parser.parse_args()
    result = {
        "post_trade": refresh_post_trade_diagnostics(db=args.db),
        "report": write_effectiveness_report(db=args.db, lookback_days=args.lookback_days),
    }
    print(json.dumps(result, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
