"""Read-only counterfactual: what would the stocks concentration cap have done?

Replays historical entered+closed stocks-intraday A/B trades day-by-day through
apply_stock_concentration_caps and compares baseline raw/sized R vs capped sized R.
Shows BOTH benefits (loss R removed) and costs (winner R removed). No DB writes.
"""

from __future__ import annotations

import sqlite3
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

from src.signals.portfolio_caps import apply_stock_concentration_caps
from src.signals.sizing import size_decision

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "db" / "crypto_ai_desk.sqlite"


def load(db):
    q = """SELECT p.signal_id, p.symbol, p.mode, p.tier, p.direction, p.score,
             p.news_supported, p.created_at, p.asset_class,
             o.entry_triggered_at, o.final_r
           FROM proposed_signals p
           JOIN (SELECT *, ROW_NUMBER() OVER(PARTITION BY signal_id ORDER BY checked_at DESC) rn
                 FROM signal_outcomes) o ON o.signal_id=p.signal_id AND o.rn=1
           WHERE p.asset_class='stocks' AND p.mode='intraday'
             AND UPPER(COALESCE(p.tier,'')) IN ('A','B')
             AND o.entry_triggered=1 AND o.final_r IS NOT NULL
             AND o.entry_triggered_at IS NOT NULL"""
    rows = []
    for r in db.execute(q):
        d = dict(r)
        d["final_r"] = float(d["final_r"])
        d["day"] = str(d["entry_triggered_at"])[:10]
        # use the entry day as created_at for same-day Rule A grouping
        d["created_at"] = str(d["entry_triggered_at"])
        rows.append(d)
    return rows


def run(db, since=None, label="all"):
    rows = load(db)
    if since:
        rows = [r for r in rows if r["day"] >= since]
    bydays = defaultdict(list)
    for r in rows:
        bydays[r["day"]].append(r)

    base_raw = base_sized = capped = proxy_only = 0.0
    n_half = n_shadow = 0
    winner_r_cut = loser_r_cut = 0.0
    day_base = defaultdict(float)
    day_capped = defaultdict(float)

    for day, sigs in bydays.items():
        capped_sigs = apply_stock_concentration_caps(sigs, existing_positions=[])
        for s in capped_sigs:
            r = s["final_r"]
            pw = size_decision(s).weight or 0.0          # playbook sized weight
            ew = s["concentration_effective_weight"]      # capped effective weight
            base_raw += r
            base_sized += r * pw
            capped += r * ew
            # proxy-only variant: apply Rule A (proxy dedup) but NOT Rule B sector cap
            proxy_w = 0.0 if s["concentration_status"] == "shadow_proxy_duplicate" else pw
            proxy_only += r * proxy_w
            day_base[day] += r * pw
            day_capped[day] += r * ew
            st = s["concentration_status"]
            if st == "half_size":
                n_half += 1
            elif st in ("shadow_proxy_duplicate", "shadow_sector_cap"):
                n_shadow += 1
            # cost/benefit attribution: R the cap removed vs playbook sizing
            removed = r * pw - r * ew
            if removed != 0:
                if r > 0:
                    winner_r_cut += removed     # cutting a winner = cost (removed>0 means we kept less upside)
                elif r < 0:
                    loser_r_cut += removed      # cutting a loser = benefit (removed<0 → we avoided loss)

    # all-loss cluster R before/after (same-day same-bucket same-dir, all losers)
    from src.stocks.risk_clusters import get_stock_risk_bucket
    cl_base = cl_capped = 0.0
    clusters = defaultdict(list)
    for r in rows:
        clusters[(r["day"], get_stock_risk_bucket(r["symbol"]), r["direction"])].append(r)
    for k, mem in clusters.items():
        if len(mem) >= 2 and all(m["final_r"] < 0 for m in mem):
            capped_sigs = {s["signal_id"]: s for s in apply_stock_concentration_caps(mem, [])}
            for m in mem:
                pw = size_decision(m).weight or 0.0
                cl_base += m["final_r"] * pw
                cl_capped += m["final_r"] * capped_sigs[m["signal_id"]]["concentration_effective_weight"]

    worst_base = min(day_base.values()) if day_base else 0.0
    worst_capped = min(day_capped.values()) if day_capped else 0.0
    # days where cap HURT (capped < base, i.e. cut net-positive day)
    hurt = sum(1 for d in day_base if day_capped[d] < day_base[d] - 1e-9 and day_base[d] > 0)
    helped = sum(1 for d in day_base if day_capped[d] > day_base[d] + 1e-9)

    print(f"\n===== COUNTERFACTUAL ({label}) — n={len(rows)} entered stock-intraday A/B =====")
    print(f"  baseline raw R         : {base_raw:+.1f}")
    print(f"  baseline sized R (pb)  : {base_sized:+.1f}")
    print(f"  proxy-only capped R    : {proxy_only:+.1f}   (delta {proxy_only-base_sized:+.1f})  [Rule A only]")
    print(f"  full-cap (A+B) R       : {capped:+.1f}   (delta {capped-base_sized:+.1f})  [Rule A+B]")
    print(f"  signals → half_size    : {n_half}")
    print(f"  signals → shadow       : {n_shadow}")
    print(f"  R cut from WINNERS (cost)   : {winner_r_cut:+.1f}")
    print(f"  R cut from LOSERS  (benefit): {loser_r_cut:+.1f}")
    print(f"  all-loss cluster R: baseline {cl_base:+.1f} → capped {cl_capped:+.1f} (saved {cl_base-cl_capped:+.1f})")
    print(f"  worst single day: baseline {worst_base:+.1f} → capped {worst_capped:+.1f}")
    print(f"  days cap HELPED: {helped} | days cap HURT (cut a green day): {hurt}")


if __name__ == "__main__":
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    now = datetime.now(timezone.utc)
    run(db, (now - timedelta(hours=24)).strftime("%Y-%m-%d"), "24h")
    run(db, (now - timedelta(days=7)).strftime("%Y-%m-%d"), "7d")
    run(db, (now - timedelta(days=14)).strftime("%Y-%m-%d"), "14d")
    run(db, None, "all")
