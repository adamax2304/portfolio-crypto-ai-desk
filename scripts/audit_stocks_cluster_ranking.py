"""PART 4 — Stocks intraday cluster ranking (additive).

For each day, group same-cluster stocks intraday A/B signals and produce a
read-only ranking by score + B/A weight + catalyst + sector + liquidity proxy.
Output cluster-rank labels — do NOT suppress any alerts.
"""

from __future__ import annotations

import sqlite3
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

DB = ROOT / "db" / "crypto_ai_desk.sqlite"

CLUSTERS = {
    "mega_tech": {"MSFT", "AAPL", "NVDA", "GOOGL", "AMZN", "META", "AVGO", "TSLA", "PLTR"},
    "semis": {"NVDA", "AMD", "SMCI", "SMH", "XLK", "AVGO"},
    "index_etfs": {"QQQ", "SPY", "IWM"},
    "ai_infra": {"NVDA", "AVGO", "SMCI", "MU", "DELL"},
}


def cluster_for(sym: str) -> list[str]:
    return [c for c, syms in CLUSTERS.items() if sym in syms]


def rank_score(row: sqlite3.Row) -> float:
    """Higher = better candidate for the day."""
    score = float(row["score"] or 0)
    tier_boost = 0 if row["tier"] == "A" and row["direction"] == "long" else 5  # B-tier preferred per audit
    news = 5 if int(row["news_supported"] or 0) == 1 else 0
    # liquidity proxy: bigger symbol = bigger volume (rough heuristic)
    LIQUID = {"AAPL", "MSFT", "NVDA", "AMD", "TSLA", "AMZN", "GOOGL", "META", "SPY", "QQQ"}
    liq = 3 if row["symbol"] in LIQUID else 0
    return score + tier_boost + news + liq


def main() -> None:
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    rows = con.execute("""
        SELECT ps.signal_id, ps.symbol, ps.direction, ps.mode, ps.tier, ps.score,
               ps.news_supported, ps.sector, ps.created_at,
               o.final_r, o.final_outcome
        FROM proposed_signals ps
        LEFT JOIN (SELECT signal_id, MAX(id) AS mid FROM signal_outcomes GROUP BY signal_id) m
          ON m.signal_id = ps.signal_id
        LEFT JOIN signal_outcomes o ON o.id = m.mid
        WHERE ps.asset_class='stocks' AND ps.mode='intraday' AND ps.tier IN ('A','B')
          AND ps.created_at >= '2026-05-28'
        ORDER BY ps.created_at
    """).fetchall()

    # Group by (day, cluster, direction)
    by_key: dict[tuple[str, str, str], list[sqlite3.Row]] = defaultdict(list)
    for r in rows:
        day = r["created_at"][:10]
        for c in cluster_for(r["symbol"]):
            by_key[(day, c, r["direction"])].append(r)

    out = []
    out.append("# Stocks Intraday Cluster Ranking (PART 4 — additive only)")
    out.append("")
    out.append(f"**Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    out.append(f"**Scope:** stocks intraday A/B last 14d (n={len(rows)}).")
    out.append("**Behavior:** ranking only — no signal is suppressed.")
    out.append("")
    out.append("## Cluster-day summary (last 14d, ≥ 3 same-direction signals only)")
    out.append("")
    out.append("| Day | Cluster | Dir | n | best 1 (rank score) | best 3 (top syms) | cluster R | cluster risk |")
    out.append("|---|---|---|---:|---|---|---:|---|")
    cluster_drawdown_5d: dict[str, list[float]] = defaultdict(list)
    for (day, cl, d), items in sorted(by_key.items()):
        if len(items) < 3:
            continue
        ranked = sorted(items, key=rank_score, reverse=True)
        best1 = ranked[0]
        best3_syms = [r["symbol"] for r in ranked[:3]]
        cluster_r = sum(float(r["final_r"] or 0) for r in items)
        # cluster risk based on count + recent drawdown
        recent_dd = sum(cluster_drawdown_5d[cl][-5:]) if cluster_drawdown_5d[cl] else 0
        if len(items) >= 10 and recent_dd < -5:
            risk = "HIGH"
        elif len(items) >= 6 or recent_dd < -3:
            risk = "MEDIUM"
        else:
            risk = "LOW"
        out.append(f"| {day} | {cl} | {d} | {len(items)} | "
                   f"{best1['symbol']} ({rank_score(best1):.1f}) | "
                   f"{', '.join(best3_syms)} | {cluster_r:+.1f} | {risk} |")
        cluster_drawdown_5d[cl].append(cluster_r)
    out.append("")

    # Top cluster right now (today)
    today = max(r["created_at"][:10] for r in rows) if rows else ""
    out.append(f"## Current top cluster (most recent day: {today})")
    out.append("")
    todays = [(k, v) for k, v in by_key.items() if k[0] == today]
    if todays:
        for (day, cl, d), items in todays:
            if len(items) < 2:
                continue
            ranked = sorted(items, key=rank_score, reverse=True)
            out.append(f"- **{cl} / {d}** — top 3: {', '.join(r['symbol'] for r in ranked[:3])}")
    else:
        out.append("_no clusters in today's data_")
    out.append("")
    out.append("## Behavior")
    out.append("")
    out.append("- This audit is **additive only**. No alert is suppressed.")
    out.append("- Dashboards may display `cluster rank #N/M` and `cluster risk: high/medium/low` per signal.")
    out.append("- Operator can use the rank as a manual sizing hint; the system never enforces it.")

    out_md = ROOT / "reports" / "STOCKS_INTRADAY_CLUSTER_RANKING_AUDIT.md"
    out_md.write_text("\n".join(out), encoding="utf-8")
    print(f"wrote {out_md}")


if __name__ == "__main__":
    main()
