"""Refresh verified free on-chain data and its paper-safe intelligence cache.

The collector is timeout-bounded, rate-limited and fail-open. Only canonical
native assets or contracts confirmed by the registry may influence the paper
guard; unresolved ticker matches remain visibility-only.
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.intelligence import store as istore  # noqa: E402
from src.intelligence import onchain_risk as oc  # noqa: E402

TRADING_DB = ROOT / "db" / "crypto_ai_desk.sqlite"


def active_symbols(limit: int) -> list[str]:
    from src.data_collectors.derivatives_pipeline import active_symbols as shared_active_symbols
    return shared_active_symbols(limit, TRADING_DB)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=40)
    args = ap.parse_args()
    now = datetime.now(timezone.utc)
    cfg = oc.config_status()
    if not cfg.get("configured"):
        print(f"onchain_risk_update: disabled ({cfg.get('reason')})")
        return
    syms = active_symbols(args.limit)
    from src.data_collectors.onchain_pipeline import OnchainPipeline
    refresh = OnchainPipeline().refresh(syms)
    conn = istore.connect()
    try:
        n = 0
        for s in syms:
            oc.update_and_cache(s, now=now, conn=conn)
            n += 1
        conn.commit()
        print(f"onchain_risk_update: updated {n} symbols; refresh={refresh}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
