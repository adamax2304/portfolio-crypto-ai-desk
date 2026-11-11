"""Shadow-intelligence background update (PART 7).

Heavy/compute work OUTSIDE the alert path. For active/recent symbols: bootstrap the
symbol timeline from recent signals/alerts/outcomes, compute + cache derivatives
trajectory and squeeze phase, compact/cleanup old timeline events, and write health
reports. Read-only on the trading DB; writes only to data/intelligence/. Non-fatal.

Usage:
  python -m scripts.intelligence_update            # full update
  python -m scripts.intelligence_update --limit 60
  python -m scripts.intelligence_update --health-only
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.intelligence import store as istore  # noqa: E402
from src.intelligence import symbol_timeline as tl  # noqa: E402
from src.intelligence import derivatives_trajectory as dv  # noqa: E402
from src.intelligence import squeeze_phase as sp  # noqa: E402
from src.data_collectors.market_intelligence_store import default_db_path  # noqa: E402

TRADING_DB = ROOT / "db" / "crypto_ai_desk.sqlite"
REPORTS = ROOT / "reports"


def _ro():
    return sqlite3.connect(f"file:{TRADING_DB.as_posix()}?mode=ro", uri=True)


def active_symbols(limit: int) -> list[str]:
    syms: list[str] = []
    try:
        c = _ro(); c.row_factory = sqlite3.Row
        since = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
        for r in c.execute(
            "SELECT symbol, COUNT(*) n FROM proposed_signals "
            "WHERE (asset_class='crypto' OR asset_class IS NULL) AND created_at>=? "
            "GROUP BY symbol ORDER BY n DESC", (since,)):
            if r["symbol"]:
                syms.append(r["symbol"])
        c.close()
    except Exception:
        pass
    return syms[:limit] if limit else syms


def bootstrap_timeline(conn, now):
    """Record recent signals/alerts/outcomes into the timeline (idempotent)."""
    n = 0
    try:
        c = _ro(); c.row_factory = sqlite3.Row
        since = (now - timedelta(days=7)).isoformat()
        for r in c.execute(
            "SELECT symbol,asset_class,mode,tier,direction,created_at,news_supported "
            "FROM proposed_signals WHERE created_at>=?", (since,)):
            tl.record_symbol_event(r["symbol"], "signal_generated", {
                "tier": r["tier"], "mode": r["mode"], "direction": r["direction"],
                "asset_class": r["asset_class"]},
                now=datetime.fromisoformat(str(r["created_at"]).replace("Z", "+00:00")), conn=conn)
            if r["news_supported"]:
                tl.record_symbol_event(r["symbol"], "catalyst_seen", {},
                                       now=datetime.fromisoformat(str(r["created_at"]).replace("Z", "+00:00")), conn=conn)
            n += 1
        c.close()
        conn.commit()
    except Exception:
        pass
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=80)
    ap.add_argument("--health-only", action="store_true")
    args = ap.parse_args()
    now = datetime.now(timezone.utc)

    if not args.health_only:
        conn = istore.connect()
        market_db = default_db_path()
        source_conn = None
        try:
            booted = bootstrap_timeline(conn, now)
            syms = active_symbols(args.limit)
            if market_db.exists():
                source_conn = sqlite3.connect(
                    f"file:{market_db.as_posix()}?mode=ro", uri=True, timeout=5.0
                )
                source_conn.row_factory = sqlite3.Row
            for s in syms:
                d = dv.update_and_cache(
                    s, now=now, conn=conn, source_conn=source_conn
                )
                sp.update_and_cache(s, now=now, deriv=d, conn=conn)
            conn.commit()
        finally:
            if source_conn is not None:
                source_conn.close()
            conn.close()
        removed = tl.cleanup_old_events(retention_days=90, now=now)
        print(f"intelligence_update: timeline_bootstrap={booted} symbols={len(syms)} cleaned={removed}")

    # health reports
    REPORTS.mkdir(parents=True, exist_ok=True)
    import json
    health = {
        "as_of": now.isoformat(),
        "timeline": tl.timeline_health_report(),
        "derivatives": dv.derivatives_trajectory_health_report(),
        "squeeze_phase": sp.squeeze_phase_health_report(),
    }
    from src.intelligence import onchain_risk as oc
    health["onchain"] = oc.onchain_risk_health_report()
    (REPORTS / "INTELLIGENCE_LAYER_HEALTH.md").write_text(
        "# Intelligence Layer — Health\n\n```json\n" + json.dumps(health, indent=1, default=str) + "\n```\n",
        encoding="utf-8")
    print(json.dumps(health, indent=1, default=str))


if __name__ == "__main__":
    main()
