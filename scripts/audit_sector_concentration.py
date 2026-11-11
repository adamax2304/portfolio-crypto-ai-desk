"""Read-only sector/factor concentration audit (2026-06-16).

The `sector` column is empty in production, so sector membership is derived from a
static symbol map for the known stock universe. Quantifies how much R was made/lost
on *correlated same-sector clusters* (>=2 same-direction positions entered the same
day) vs singletons, and surfaces the worst "everyone stopped together" days.

NO writes to the DB. NO trading. NO strategy/scoring/TP/SL change.
"""

from __future__ import annotations

import sqlite3
import statistics
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "db" / "crypto_ai_desk.sqlite"

# Fine sector + coarse factor. Tech complex (semis+megacap+high-beta) all co-move.
SECTOR = {
    "AMD": "semis", "NVDA": "semis", "AVGO": "semis", "SMH": "semis", "SMCI": "semis",
    "AAPL": "megacap_tech", "MSFT": "megacap_tech", "AMZN": "megacap_tech",
    "META": "megacap_tech", "GOOGL": "megacap_tech", "NFLX": "megacap_tech",
    "QQQ": "megacap_tech", "XLK": "megacap_tech", "XLY": "megacap_tech",
    "TSLA": "high_beta_tech", "PLTR": "high_beta_tech", "COIN": "high_beta_tech",
    "MSTR": "high_beta_tech",
    "LLY": "healthcare", "UNH": "healthcare", "XLV": "healthcare",
    "JPM": "financials", "XLF": "financials",
    "XOM": "energy", "XLE": "energy",
    "SPY": "broad_index", "DIA": "broad_index", "IWM": "broad_index",
}
TECH_COMPLEX = {"semis", "megacap_tech", "high_beta_tech"}


def factor_of(sym):
    s = SECTOR.get(sym, "other")
    return "tech_complex" if s in TECH_COMPLEX else s


def load(db):
    q = """SELECT p.symbol, p.mode, p.tier, p.direction,
             o.entry_triggered, o.entry_triggered_at, o.final_outcome, o.final_r
           FROM proposed_signals p
           JOIN (SELECT *, ROW_NUMBER() OVER(PARTITION BY signal_id ORDER BY checked_at DESC) rn
                 FROM signal_outcomes) o
             ON o.signal_id=p.signal_id AND o.rn=1
           WHERE p.asset_class='stocks' AND o.entry_triggered=1
             AND o.final_outcome IN ('win','loss','expired','ambiguous')
             AND o.entry_triggered_at IS NOT NULL"""
    rows = []
    for r in db.execute(q):
        d = dict(r)
        d["sector"] = SECTOR.get(d["symbol"], "other")
        d["factor"] = factor_of(d["symbol"])
        d["day"] = str(d["entry_triggered_at"])[:10]
        d["r"] = float(d["final_r"]) if d["final_r"] is not None else 0.0
        rows.append(d)
    return rows


def cluster_audit(rows, group_key, label):
    # group entered trades by (day, group, direction)
    groups = defaultdict(list)
    for r in rows:
        groups[(r["day"], r[group_key], r["direction"])].append(r)
    clustered, singleton = [], []
    allloss_clusters = []
    for k, members in groups.items():
        if len(members) >= 2:
            clustered.extend(members)
            tot = sum(m["r"] for m in members)
            losses = sum(1 for m in members if m["r"] < 0)
            if losses == len(members):  # whole cluster lost together
                allloss_clusters.append((k, members, tot))
        else:
            singleton.extend(members)

    def stat(rs):
        if not rs:
            return (0, 0.0, 0.0, 0.0)
        rr = [x["r"] for x in rs]
        wr = 100.0 * sum(1 for x in rr if x > 0) / len(rr)
        return (len(rr), round(sum(rr), 1), round(statistics.mean(rr), 3), round(wr, 1))

    print(f"\n===== CLUSTER AUDIT by {label} =====")
    n, tot, avg, wr = stat(clustered)
    print(f"  CLUSTERED (>=2 same-day same-{label} same-dir): n={n} totR={tot} avgR={avg} WR={wr}%")
    n, tot, avg, wr = stat(singleton)
    print(f"  SINGLETON:                                      n={n} totR={tot} avgR={avg} WR={wr}%")
    # all-loss clusters
    allloss_clusters.sort(key=lambda x: x[2])
    tot_allloss = round(sum(c[2] for c in allloss_clusters), 1)
    print(f"  ALL-LOSS clusters: {len(allloss_clusters)} | total R bled = {tot_allloss}")
    print("  worst all-loss clusters:")
    for (day, grp, direc), members, tot in allloss_clusters[:8]:
        syms = ",".join(m["symbol"] for m in members)
        print(f"    {day} {grp:14s} {direc:5s} legs={len(members)} R={tot:.1f}  [{syms}]")
    return allloss_clusters


if __name__ == "__main__":
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    rows = load(db)
    print(f"entered+closed stocks trades: {len(rows)}; total R = {round(sum(r['r'] for r in rows),1)}")
    # exposure distribution: max concurrent same-day same-factor longs
    byday = defaultdict(lambda: defaultdict(int))
    for r in rows:
        if r["direction"] == "long":
            byday[r["day"]][r["factor"]] += 1
    maxc = defaultdict(int)
    for day, fac in byday.items():
        for f, c in fac.items():
            maxc[f] = max(maxc[f], c)
    print("\nmax same-day concurrent LONG entries per factor:")
    for f, c in sorted(maxc.items(), key=lambda x: -x[1]):
        print(f"  {f:14s} {c}")
    cluster_audit(rows, "sector", "sector")
    cluster_audit(rows, "factor", "factor")
