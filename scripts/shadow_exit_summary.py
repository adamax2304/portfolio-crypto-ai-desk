"""Shadow exit ledger summary (FAST SAFE ACCELERATION PART 3).

Reads data/reports/shadow_exit_ledger.csv and writes reports/SHADOW_EXIT_LEDGER_SUMMARY.md:
net R / PF / winrate / winners-clipped / losers-saved per variant (+ per mode/tier),
with a do_not_enable / shadow_candidate / candidate_for_paper_rule recommendation.
Read-only; never enables anything.
"""
from __future__ import annotations

import csv
import statistics
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

LEDGER = ROOT / "data" / "reports" / "shadow_exit_ledger.csv"
OUT = ROOT / "reports" / "SHADOW_EXIT_LEDGER_SUMMARY.md"


def _f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def stats(rs):
    rs = [r for r in rs if r is not None]
    if not rs:
        return {"n": 0, "net_R": 0.0, "PF": None, "winrate": None}
    wins = [x for x in rs if x > 0]
    losses = [x for x in rs if x < 0]
    gl = -sum(losses)
    return {"n": len(rs), "net_R": round(sum(rs), 1),
            "PF": round(sum(wins) / gl, 2) if gl else None,
            "winrate": round(len(wins) / len(rs) * 100, 1)}


def main():
    if not LEDGER.exists():
        OUT.write_text("# Shadow Exit Ledger — Summary\n\n_No ledger yet. Run "
                       "`scripts.shadow_exit_ledger_update` first._\n", encoding="utf-8")
        print("no ledger")
        return
    rows = list(csv.DictReader(LEDGER.open(encoding="utf-8")))
    covered = [r for r in rows if r.get("data_coverage_status") == "covered"]
    by_variant = defaultdict(list)
    clipped = defaultdict(int)
    saved = defaultdict(int)
    for r in covered:
        v = r["variant"]
        by_variant[v].append(_f(r.get("shadow_R")))
        if str(r.get("winner_clipped")).lower() == "true":
            clipped[v] += 1
        if str(r.get("loser_saved")).lower() == "true":
            saved[v] += 1

    actual = stats([_f(r.get("actual_R")) for r in covered if r["variant"] == "A_current"])
    n_trades = len({r["signal_id"] for r in rows})
    n_covered = len({r["signal_id"] for r in covered})
    coverage_pct = round(n_covered / n_trades * 100, 1) if n_trades else 0

    lines = [
        "# Shadow Exit Ledger — Summary (PART 3)", "",
        f"**Trades in ledger:** {n_trades} · **covered:** {n_covered} ({coverage_pct}%) · "
        f"**missing_data:** {n_trades - n_covered}",
        "**Shadow measurement only — real exits unchanged, `partial_exit_model.enabled` stays false.**",
        "",
        "## Net R / PF / winrate by variant (covered trades)",
        "| variant | n | net_R | PF | winrate | winners_clipped | losers_saved |",
        "|---|---|---|---|---|---|---|",
    ]
    order = ["A_current", "B_BE_0.5R", "C_BE_1R", "D_partial50_1R", "E_partial50_1R_BE",
             "F_trail_1R", "G_candle_close_stop", "H_no_reentry", "I_one_reentry"]
    cur = stats(by_variant.get("A_current", []))
    best = None
    for v in order:
        if v not in by_variant:
            continue
        s = stats(by_variant[v])
        lines.append(f"| {v} | {s['n']} | {s['net_R']} | {s['PF']} | {s['winrate']} | "
                     f"{clipped.get(v, 0)} | {saved.get(v, 0)} |")
        if v != "A_current" and (best is None or s["net_R"] > best[1]):
            best = (v, s["net_R"], s["PF"])

    # recommendation
    actual_net = actual["net_R"]
    if coverage_pct < 70:
        rec = ("DATA_COVERAGE_STILL_INSUFFICIENT — do not interpret as decision-grade; "
               "let the OHLCV archive/backfill grow.")
    elif best and best[1] > cur["net_R"] + 1.0:
        # a variant reduces drawdown vs the (shadow) current path
        enable_ok = best[1] > 0 and (best[2] or 0) >= 1.0
        rec = (f"shadow_candidate: {best[0]} reduces drawdown (net {best[1]}R, PF {best[2]}) "
               f"vs shadow-current ({cur['net_R']}R) on {coverage_pct}% coverage. "
               + ("Net-positive + PF>1 → strong candidate, but " if enable_ok
                  else f"still net-negative / PF<1 on this window, so ")
               + "measure FORWARD as a SHADOW rule across up+down regimes; DO NOT enable in "
                 "trade logic yet. NOTE: shadow A_current (5m + conservative same-candle) is "
                 f"PESSIMISTIC vs the real recorded book (actual net {actual_net}R) — only the "
                 "RELATIVE variant deltas are meaningful, not absolute levels.")
    else:
        rec = "do_not_enable — no variant clearly beats current on covered data."

    lines += ["", "## Recommendation", f"- {rec}", "",
              f"Actual (A_current) baseline: net {actual['net_R']}R, PF {actual['PF']}, "
              f"winrate {actual['winrate']}% over {actual['n']} covered trades.", "",
              "_Per-mode/tier/regime cuts are available in the ledger CSV; this summary "
              "headlines the variant comparison. No production change._"]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT} · trades={n_trades} covered={n_covered} ({coverage_pct}%)")


if __name__ == "__main__":
    main()
