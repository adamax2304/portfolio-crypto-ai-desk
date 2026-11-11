"""Stocks-intraday loss diagnostic + safe-filter counterfactual (operational deploy PART 8).

Read-only. Breaks down closed stocks-intraday signals by tier / catalyst / session /
regime / legal-flag / risk_bucket / ticker, and simulates safe FILTERS (no production
change) to see which would remove losers without killing winners. Writes:
  reports/STOCKS_INTRADAY_REWORK_DIAGNOSTIC.md
  reports/STOCKS_INTRADAY_FILTER_COUNTERFACTUAL.csv
"""
from __future__ import annotations

import csv
import json
import sqlite3
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.stocks.market_calendar import us_session_label  # noqa: E402
from src.stocks.risk_clusters import get_stock_risk_bucket  # noqa: E402

DB = ROOT / "db" / "crypto_ai_desk.sqlite"
MD = ROOT / "reports" / "STOCKS_INTRADAY_REWORK_DIAGNOSTIC.md"
CSV_OUT = ROOT / "reports" / "STOCKS_INTRADAY_FILTER_COUNTERFACTUAL.csv"
LOOKBACK_DAYS = 30


def _parse(ts):
    try:
        return datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
    except Exception:
        return None


def _legal(row) -> bool:
    j = row.get("no_entry_conditions_json") or ""
    return "LEGAL" in j.upper()


def main():
    now = datetime.now(timezone.utc)
    since = (now.timestamp() - LOOKBACK_DAYS * 86400)
    conn = sqlite3.connect(f"file:{DB.as_posix()}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        """
        SELECT s.signal_id, s.symbol, s.tier, s.direction, s.created_at,
               s.market_regime, s.sector, s.news_supported, s.no_entry_conditions_json,
               o.final_r, o.final_outcome
        FROM proposed_signals s
        JOIN signal_outcomes o ON o.signal_id = s.signal_id
        WHERE o.id IN (SELECT MAX(id) FROM signal_outcomes GROUP BY signal_id)
          AND s.asset_class='stocks' AND s.mode='intraday'
          AND o.final_outcome IN ('win','loss','partial_win')
        """).fetchall()
    conn.close()

    trades = []
    for r in rows:
        d = dict(r)
        ct = _parse(d["created_at"])
        if not ct or ct.timestamp() < since:
            continue
        d["_r"] = float(d["final_r"] or 0.0)
        d["_session"] = us_session_label(ct) if ct else "unknown"
        d["_bucket"] = get_stock_risk_bucket(d["symbol"])
        d["_catalyst"] = (d["news_supported"] or 0) > 0
        d["_legal"] = _legal(d)
        d["_hour"] = ct.astimezone(timezone.utc).hour if ct else None
        d["_tier"] = (d["tier"] or "?").upper()
        trades.append(d)

    def agg(key_fn):
        g = defaultdict(lambda: [0, 0.0])
        for t in trades:
            k = key_fn(t)
            g[k][0] += 1
            g[k][1] += t["_r"]
        return {k: {"n": v[0], "net_R": round(v[1], 1)} for k, v in g.items()}

    by_tier = agg(lambda t: t["_tier"])
    by_cat = agg(lambda t: "catalyst" if t["_catalyst"] else "no_catalyst")
    by_session = agg(lambda t: t["_session"])
    by_regime = agg(lambda t: t["market_regime"] or "unknown")
    by_legal = agg(lambda t: "legal_flag" if t["_legal"] else "clean")
    by_bucket = agg(lambda t: t["_bucket"])
    by_ticker = agg(lambda t: t["symbol"].split("/")[0].upper())

    total_n = len(trades)
    total_r = round(sum(t["_r"] for t in trades), 1)

    # ---- safe-filter counterfactuals (subset net R) ----
    def subset(pred):
        ts = [t for t in trades if pred(t)]
        return {"kept": len(ts), "dropped": total_n - len(ts),
                "net_R": round(sum(t["_r"] for t in ts), 1)}

    filters = {
        "current_all": subset(lambda t: True),
        "drop_C_tier": subset(lambda t: t["_tier"] != "C"),
        "only_catalyst_backed": subset(lambda t: t["_catalyst"]),
        "only_RTH_session": subset(lambda t: t["_session"] == "regular session"),
        "exclude_legal": subset(lambda t: not t["_legal"]),
        "AB_and_catalyst_and_RTH": subset(
            lambda t: t["_tier"] in ("A", "B") and t["_catalyst"] and t["_session"] == "regular session"),
        "AB_and_RTH_no_legal": subset(
            lambda t: t["_tier"] in ("A", "B") and t["_session"] == "regular session" and not t["_legal"]),
    }

    # per-trade CSV with filter flags
    CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
    with CSV_OUT.open("w", newline="", encoding="utf-8") as fo:
        w = csv.writer(fo)
        w.writerow(["signal_id", "symbol", "tier", "direction", "created_at", "session",
                    "regime", "risk_bucket", "catalyst", "legal_flag", "final_r", "final_outcome"])
        for t in sorted(trades, key=lambda x: x["_r"]):
            w.writerow([t["signal_id"], t["symbol"], t["_tier"], t["direction"], t["created_at"],
                        t["_session"], t["market_regime"], t["_bucket"], t["_catalyst"],
                        t["_legal"], t["_r"], t["final_outcome"]])

    def tbl(title, d, label="key"):
        out = [f"### {title}", f"| {label} | n | net_R |", "|---|---|---|"]
        for k, v in sorted(d.items(), key=lambda kv: kv[1]["net_R"]):
            out.append(f"| {k} | {v['n']} | {v['net_R']} |")
        return "\n".join(out)

    worst_tickers = sorted(by_ticker.items(), key=lambda kv: kv[1]["net_R"])[:10]

    lines = [
        "# Stocks-Intraday Rework Diagnostic (PART 8)", "",
        f"**Window:** last {LOOKBACK_DAYS}d · closed stocks-intraday trades: **{total_n}** · net **{total_r}R**",
        "**Read-only. No production change — filters are simulated only.**", "",
        tbl("By tier", by_tier, "tier"), "",
        tbl("By catalyst", by_cat, "catalyst"), "",
        tbl("By session (at creation)", by_session, "session"), "",
        tbl("By regime", by_regime, "regime"), "",
        tbl("By legal flag", by_legal, "legal"), "",
        tbl("By risk bucket", by_bucket, "bucket"), "",
        "### Worst 10 tickers by net R",
        "| ticker | n | net_R |", "|---|---|---|",
        *[f"| {k} | {v['n']} | {v['net_R']} |" for k, v in worst_tickers],
        "",
        "## Safe-filter counterfactuals (simulated, not applied)",
        "| filter | kept | dropped | net_R |", "|---|---|---|---|",
        *[f"| {k} | {v['kept']} | {v['dropped']} | {v['net_R']} |" for k, v in filters.items()],
        "",
        "See `STOCKS_INTRADAY_FILTER_COUNTERFACTUAL.csv` (per-trade) and "
        "`STOCKS_INTRADAY_SAFE_RESTRICTION_PLAN.md` for the recommendation.",
    ]
    MD.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"total_n": total_n, "total_r": total_r,
                      "by_tier": by_tier, "filters": filters}, indent=1, default=str))


if __name__ == "__main__":
    main()
