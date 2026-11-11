"""PART 4 — Historical paper-execution recalculation (derived, read-only).

Recomputes touch_r / first_tp_close_r / hold_tp3_r / model_f (paper_execution_r)
for every entered economic trade (deduped), WITHOUT touching signal_outcomes /
final_r. Writes data/research/paper_execution_recalc_<date>.csv and prints
window x book aggregates (all / 60d / 30d / 7d / 48h / today).
"""
from __future__ import annotations
import csv, os
from datetime import timedelta

from scripts.strategy_viability import build, S


def main():
    now, recs = build()
    date = now.date().isoformat()
    rename = {
        "m0_legacy_touch": "touch_r",
        "m1_first_tp_close": "first_tp_close_r",
        "m2_hold_tp3": "hold_tp3_r",
        "mF_mfe_protect": "paper_execution_r",  # Model F = authoritative paper PnL
    }
    out_cols = ["key", "book", "symbol", "asset_class", "mode", "tier", "direction",
                "playbook", "regime", "catalyst", "entry_at", "reached_tp1", "reached_tp2",
                "reached_tp3", "hit_stop", "expired", "mfe_r", "mae_r", "recorded_final_r",
                "touch_r", "first_tp_close_r", "hold_tp3_r", "paper_execution_r"]
    os.makedirs("data/research", exist_ok=True)
    out = f"data/research/paper_execution_recalc_{date}.csv"
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(out_cols)
        for r in recs:
            row = dict(r)
            for src, dst in rename.items():
                row[dst] = r[src]
            w.writerow([row.get(c) for c in out_cols])
    print(f"=== {len(recs)} deduped economic trades -> {out} (now={date})")

    windows = {"all": None, "60d": 60, "30d": 30, "7d": 7, "48h": 2, "today": 0}
    books = ("actionable", "shadow")
    print(f"\n{'window':8}{'book':12}{'n':>5}{'touch_r':>10}{'first_tp':>10}{'hold_tp3':>10}{'paper_exec(F)':>15}{'overstmt':>10}")
    for wname, days in windows.items():
        if days is None:
            since = None
        elif days == 0:
            since = now.date().isoformat()
        else:
            since = (now - timedelta(days=days)).isoformat()
        for book in books:
            g = [x for x in recs if x["book"] == book and (since is None or (x["entry_at"] or "") >= since)]
            if not g:
                print(f"{wname:8}{book:12}{0:>5}"); continue
            t = S(g, "m0_legacy_touch"); pe = S(g, "mF_mfe_protect")
            print(f"{wname:8}{book:12}{len(g):>5}{t:>10}{S(g,'m1_first_tp_close'):>10}"
                  f"{S(g,'m2_hold_tp3'):>10}{pe:>15}{round(t-pe,1):>10}")


if __name__ == "__main__":
    main()
