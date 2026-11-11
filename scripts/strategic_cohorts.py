"""Recompute strategic cohorts after the asset-aware B-book fix (READ-ONLY analytics).

Three separate books:
  * A  — active mechanical/taker paper ledger (fee_profile = active)
  * B  — structural/maker-first paper ledger (fee_profile = bybit_structural_maker_first)
  * S  — paper-shadow FORWARD, clean cohort only (DATA_GAP_LATE excluded, new_logic_shadow, filled)

For A/B: full cost split (gross / exchange_fees / slippage / funding / net) from the ledger.
For S: shadow rows carry only a combined fee, so gross/slippage/funding are reported as n/a.

Writes per-book CSVs (fine granularity by asset_class/mode/tier/direction/setup_type) and prints
a coarse asset_class×mode×direction×setup_family summary with the cohort-allocator weight/status.
NEVER writes to signal_outcomes; never touches live.
"""
from __future__ import annotations
import csv, os, sqlite3
from datetime import datetime, timezone

from src.execution.cohort_allocator import allocate, setup_family

DB = "db/crypto_ai_desk.sqlite"
ACTIVE = "bybit_non_vip_usdt_perp"
BSTRUCT = "bybit_structural_maker_first"


def _dd(nets: list[float]) -> float:
    """Max peak-to-trough drawdown ($) over the cohort's net-pnl sequence."""
    peak = run = mdd = 0.0
    for v in nets:
        run += (v or 0.0)
        peak = max(peak, run)
        mdd = min(mdd, run - peak)
    return round(mdd, 2)


def _ledger_rows(con, fee_profile):
    q = """
    SELECT l.timestamp, COALESCE(p.asset_class,'?') ac, COALESCE(p.mode,'?') mode,
           COALESCE(p.tier,'?') tier, COALESCE(p.direction,'?') dir,
           COALESCE(p.setup_type,'?') setup,
           l.gross_pnl_usdt g, l.fees_usdt ex, l.slippage_usdt sl, l.funding_usdt fu,
           l.net_pnl_usdt net, l.paper_execution_r r
    FROM paper_portfolio_ledger l LEFT JOIN proposed_signals p ON l.signal_id=p.signal_id
    WHERE l.event_type='exit' AND l.fee_profile=?
    """
    return [dict(r) for r in con.execute(q, (fee_profile,))]


def _shadow_rows(con):
    dgl = {r[0] for r in con.execute(
        "SELECT signal_id FROM entry_latency_audit WHERE cause='DATA_GAP_LATE'")} \
        if con.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='entry_latency_audit'").fetchone() else set()
    q = """
    SELECT o.entry_fill_time timestamp, COALESCE(p.asset_class,'?') ac, COALESCE(p.mode,'?') mode,
           COALESCE(p.tier,'?') tier, COALESCE(p.direction,'?') dir, COALESCE(p.setup_type,'?') setup,
           o.net_r r, o.net_pnl_usdt net, o.fees_usdt ex, o.signal_id sid
    FROM paper_shadow_execution_outcomes o LEFT JOIN proposed_signals p ON o.signal_id=p.signal_id
    WHERE o.window='forward_since_activation' AND o.branch='new_logic_shadow'
      AND o.entry_fill_status='filled'
    """
    rows = [dict(r) for r in con.execute(q)]
    return [r for r in rows if r["sid"] not in dgl]


def _key(r):
    return (r["ac"], r["mode"], r["tier"], r["dir"], r["setup"])


def _aggregate(rows, has_split: bool):
    groups: dict[tuple, list] = {}
    for r in rows:
        groups.setdefault(_key(r), []).append(r)
    out = []
    for k, rs in sorted(groups.items()):
        rs.sort(key=lambda x: x.get("timestamp") or "")
        n = len(rs)
        net = round(sum(x["net"] or 0 for x in rs), 2)
        wins = sum(1 for x in rs if (x["net"] or 0) > 0)
        rvals = [x["r"] for x in rs if x.get("r") is not None]
        row = {"asset_class": k[0], "mode": k[1], "tier": k[2], "direction": k[3], "setup_type": k[4],
               "trades": n,
               "gross": round(sum(x.get("g") or 0 for x in rs), 2) if has_split else None,
               "exchange_fees": round(sum(x.get("ex") or 0 for x in rs), 2),
               "slippage": round(sum(x.get("sl") or 0 for x in rs), 2) if has_split else None,
               "funding": round(sum(x.get("fu") or 0 for x in rs), 2) if has_split else None,
               "net": net, "avg_r": round(sum(rvals) / len(rvals), 3) if rvals else None,
               "win_rate": round(100 * wins / n, 1) if n else 0.0,
               "max_dd_usd": _dd([x["net"] for x in rs])}
        al = allocate(k[0], k[1], k[3], setup_type=k[4])
        row["alloc_weight"] = al.weight
        row["alloc_status"] = al.status
        out.append(row)
    return out


def _coarse(rows):
    """asset_class × mode × direction × setup_family roll-up with allocator weight/status."""
    g: dict[tuple, dict] = {}
    for r in rows:
        fam = setup_family(r["setup_type"])
        k = (r["asset_class"], r["mode"], r["direction"], fam)
        d = g.setdefault(k, {"trades": 0, "net": 0.0})
        d["trades"] += r["trades"]; d["net"] += r["net"]
    out = []
    for k, d in sorted(g.items()):
        al = allocate(k[0], k[1], k[2], playbook=k[3])
        out.append({"asset_class": k[0], "mode": k[1], "direction": k[2], "setup_family": k[3],
                    "trades": d["trades"], "net_usd": round(d["net"], 2),
                    "alloc_weight": al.weight, "alloc_status": al.status})
    return out


def _write_csv(path, rows):
    if not rows:
        return
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)


def main():
    date = datetime.now(timezone.utc).date().isoformat()
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    A = _aggregate(_ledger_rows(con, ACTIVE), has_split=True)
    B = _aggregate(_ledger_rows(con, BSTRUCT), has_split=True)
    S = _aggregate(_shadow_rows(con), has_split=False)
    con.close()
    os.makedirs("data/research", exist_ok=True)
    _write_csv(f"data/research/strategic_cohorts_A_{date}.csv", A)
    _write_csv(f"data/research/strategic_cohorts_B_{date}.csv", B)
    _write_csv(f"data/research/strategic_cohorts_shadow_forward_clean_{date}.csv", S)

    def book_tot(rows):
        return (sum(r["trades"] for r in rows), round(sum(r["net"] for r in rows), 2))

    for name, rows in (("A (mechanical/taker)", A), ("B (structural/maker)", B),
                       ("S (shadow fwd clean)", S)):
        t, net = book_tot(rows)
        print(f"\n=== {name}: {t} trades, net ${net} ===")
        print(f"{'asset':7}{'mode':9}{'dir':6}{'family':13}{'trades':>7}{'net$':>10}{'w':>6}{'status':>18}")
        for c in _coarse(rows):
            print(f"{c['asset_class']:7}{c['mode']:9}{c['direction']:6}{c['setup_family']:13}"
                  f"{c['trades']:>7}{c['net_usd']:>10}{c['alloc_weight']:>6}{c['alloc_status']:>18}")
    print(f"\nwrote 3 CSVs to data/research/ (date {date})")


if __name__ == "__main__":
    main()
