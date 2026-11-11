"""Operational status report for all optional context/risk filters."""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.config import load_config
from src.intelligence.context_config import ROOT, load_context_filters
from src.intelligence.context_store import connect
from src.intelligence.market_risk_context import cross_exchange_state, stablecoin_state
from src.intelligence.options_context import latest


REPORT = ROOT / "reports" / "CONTEXT_FILTERS_STATUS.md"


def _count(conn, table: str) -> int:
    exists = conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table,)).fetchone()
    return int(conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]) if exists else 0


def build(now: datetime | None = None) -> dict[str, Any]:
    now = now or datetime.now(timezone.utc)
    cfg = load_context_filters()
    with connect() as conn:
        counts = {table: _count(conn, table) for table in (
            "token_unlock_events", "stablecoin_peg_snapshots", "cross_exchange_quote_snapshots",
            "options_context_snapshots", "insider_transactions", "context_filter_decisions")}
        option_counts = {asset: int(conn.execute(
            "SELECT COUNT(*) FROM options_context_snapshots WHERE asset_class=?", (asset,)).fetchone()[0])
            for asset in ("crypto", "stocks")}
        sources = [dict(r) for r in conn.execute(
            "SELECT source,status,last_success_at,consecutive_failures,error "
            "FROM intelligence_source_health WHERE source LIKE 'context:%' ORDER BY source")]
    overnight = {"rows": 0, "eligible": 0, "resolved_close": 0}
    try:
        trading = sqlite3.connect(str(load_config().db_path))
        cols = {r[1] for r in trading.execute("PRAGMA table_info(stocks_catalyst_rs_shadow_outcomes)")}
        if "overnight_eligible" in cols:
            row = trading.execute(
                "SELECT COUNT(*),SUM(COALESCE(overnight_eligible,0)),"
                "SUM(CASE WHEN would_next_close_net_pnl_usd IS NOT NULL THEN 1 ELSE 0 END) "
                "FROM stocks_catalyst_rs_shadow_outcomes").fetchone()
            overnight = {"rows": int(row[0] or 0), "eligible": int(row[1] or 0),
                         "resolved_close": int(row[2] or 0)}
        trading.close()
    except sqlite3.Error:
        pass
    return {"as_of": now.isoformat(), "config_version": cfg.get("version"), "live_enabled": False,
            "stablecoin": stablecoin_state(as_of=now),
            "cross_exchange": {s: cross_exchange_state(s, as_of=now)
                               for s in ("BTC/USDT", "ETH/USDT")},
            "options": {f"crypto:{s}": latest("crypto", s, as_of=now) for s in ("BTC", "ETH")}
                       | {f"stocks:{s}": latest("stocks", s, as_of=now) for s in ("SPY", "QQQ")},
            "counts": counts, "option_counts": option_counts, "sources": sources, "overnight": overnight,
            "routing": {name: bool((cfg.get(name) or {}).get("paper_routing_enabled", False))
                        for name in ("token_unlock", "stablecoin_depeg", "cross_exchange",
                                     "options_context", "gex", "insider_confirmation", "catalyst_overnight")}}


def render(data: dict[str, Any]) -> str:
    lines = ["# Context Filters Status", "", f"- as of: `{data['as_of']}`",
             f"- config: `{data.get('config_version')}`; live: **LOCKED**", "",
             "| filter | Paper routing | current state | evidence rows |", "|---|---:|---|--:|"]
    peg = data["stablecoin"]
    lines.append(f"| stablecoin depeg | yes | {peg.get('state')} / {peg.get('reason')} | "
                 f"{data['counts']['stablecoin_peg_snapshots']} |")
    xstate = ", ".join(f"{s}:{v.get('status')}/{v.get('would_action')}"
                       for s, v in data["cross_exchange"].items())
    lines.append(f"| cross-exchange consistency | yes | {xstate} | "
                 f"{data['counts']['cross_exchange_quote_snapshots']} |")
    lines.append(f"| token unlock | no (shadow) | DefiLlama public calendar fallback | "
                 f"{data['counts']['token_unlock_events']} |")
    lines.append(f"| crypto IV-RV | no (advisory) | Deribit DVOL | {data['option_counts']['crypto']} |")
    lines.append(f"| stocks GEX | no (shadow) | provisional yfinance OI/IV gamma proxy | "
                 f"{data['option_counts']['stocks']} |")
    lines.append(f"| insider cluster | no (shadow confirmation) | Form 4 code P | "
                 f"{data['counts']['insider_transactions']} |")
    lines.append(f"| Catalyst RS overnight | no (counterfactual) | eligible "
                 f"{data['overnight']['eligible']}, resolved {data['overnight']['resolved_close']} | "
                 f"{data['overnight']['rows']} |")
    lines.extend(["", "## Source health", ""])
    lines.extend(f"- `{x['source']}`: {x['status']}; failures={x['consecutive_failures']}; "
                 f"last_success={x['last_success_at']}" for x in data["sources"])
    lines.extend(["", "Only stablecoin depeg and cross-exchange consistency may reduce new Paper entries. ",
                  "All other filters are point-in-time Shadow/advisory evidence and cannot promote a trade."])
    return "\n".join(lines) + "\n"


def write(path: str | Path | None = None) -> dict[str, Any]:
    data = build()
    target = Path(path) if path else REPORT
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render(data), encoding="utf-8")
    return {"path": str(target), "data": data}


__all__ = ["build", "render", "write"]
