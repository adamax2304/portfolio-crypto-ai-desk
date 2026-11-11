"""CRITICAL STRATEGY VIABILITY AUDIT — signal quality vs risk management (read-only).

Builds the full-history economic-trade dataset with MFE/MAE quality fields + every
execution-model R (via scripts.realistic_pnl_sim.compute_models), then prints:
  - signal-quality distributions (MFE reach rates, stop-first, giveback) by book,
  - per-cohort realistic expectancy ranking,
  - cohort-filter x risk-model portfolio search.

Does NOT mutate signal_outcomes or any production logic. MFE/MAE are the tracker's
recorded R-multiples (peak favorable / adverse excursion). Absolute R for non-touch
models is RELATIVE-ONLY (granularity + optimistic baseline).
"""
from __future__ import annotations
import csv, json, os, sqlite3
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone

from scripts.realistic_pnl_sim import parse, ff, rmult, actionable, compute_models, model_f_mfe

DB = "db/crypto_ai_desk.sqlite"
RESTART = "2026-06-18T00:00:00+00:00"  # persistent monitor restart (DECISION_LOG)


def build():
    con = sqlite3.connect(DB); con.row_factory = sqlite3.Row; cur = con.cursor()
    now = parse(cur.execute("SELECT max(checked_at) FROM signal_outcomes").fetchone()[0]) or datetime.now(timezone.utc)
    cur.execute("""
    WITH latest AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY signal_id ORDER BY checked_at DESC, id DESC) rn FROM signal_outcomes)
    SELECT o.*, p.symbol,p.direction,p.mode,p.tier,p.asset_class,p.market_regime,p.news_supported,p.telegram_supported,
           p.setup_type,p.created_at,p.suggested_entry,p.entry_trigger,p.entry_low,p.stop_loss,p.invalidation,
           p.tp1,p.tp2,p.tp3,p.raw_idea_json
    FROM latest o JOIN proposed_signals p ON p.signal_id=o.signal_id
    WHERE o.rn=1 AND o.entry_triggered=1""")
    rows = [dict(r) for r in cur.fetchall()]
    try:
        from src.signals.playbooks import label_for
    except Exception:
        label_for = None
    prio = {"win": 5, "loss": 5, "ambiguous": 4, "expired": 3, "not_triggered": 1, None: 0}
    trades = {}
    for r in rows:
        entry = ff(r["suggested_entry"]) or ff(r["entry_trigger"]) or ff(r["entry_low"])
        stop = ff(r["invalidation"]) or ff(r["stop_loss"])
        d = (r["direction"] or "long").lower()
        eat = parse(r["entry_triggered_at"]) or parse(r["created_at"]) or now
        key = (r["symbol"], d, (r["mode"] or "").lower(), (r["tier"] or "").upper(), round(entry or 0, 8), eat.date().isoformat())
        if key in trades and prio.get(r["final_outcome"], 0) <= prio.get(trades[key]["final_outcome"], 0):
            continue
        pb = r["setup_type"] or ""
        if label_for:
            try:
                sig = dict(r)
                if r["raw_idea_json"]: sig.update(json.loads(r["raw_idea_json"]))
                sig.update({"tier": r["tier"], "mode": r["mode"], "asset_class": r["asset_class"], "symbol": r["symbol"]})
                pb = label_for(sig).playbook
            except Exception:
                pass
        r["_e"], r["_s"], r["_pb"], r["_eat"], r["_key"] = entry, stop, pb, eat, "|".join(str(x) for x in key)
        trades[key] = r

    recs = []
    for r in trades.values():
        d = (r["direction"] or "long").lower()
        R1 = rmult(r["_e"], r["_s"], ff(r["tp1"]), d) or 0.0
        R2 = rmult(r["_e"], r["_s"], ff(r["tp2"]), d) or 0.0
        R3 = rmult(r["_e"], r["_s"], ff(r["tp3"]), d) or 0.0
        c1, c2, c3 = bool(r["tp1_hit"]), bool(r["tp2_hit"]), bool(r["tp3_hit"])
        st = bool(r["stop_hit"]); fo = (r["final_outcome"] or "").lower()
        exp = fo == "expired" or (not c1 and not st and fo != "win")
        mfe = ff(r["max_favorable_excursion_r"]) or 0.0
        mae = ff(r["max_adverse_excursion_r"]) or 0.0
        mm = compute_models(c1, c2, c3, st, exp, R1, R2, R3)
        eat = r["_eat"]
        recs.append({
            "key": r["_key"], "book": "actionable" if actionable(r["asset_class"], (r["mode"] or "").lower(), r["tier"]) else "shadow",
            "symbol": r["symbol"], "asset_class": r["asset_class"], "mode": (r["mode"] or "").lower(), "tier": (r["tier"] or "").upper(),
            "direction": d, "playbook": r["_pb"], "regime": (r["market_regime"] or "").strip() or "unknown",
            "catalyst": "yes" if (r["news_supported"] or r["telegram_supported"]) else "no",
            "entry_at": (eat.isoformat() if eat else ""), "reached_tp1": int(c1), "reached_tp2": int(c2), "reached_tp3": int(c3),
            "hit_stop": int(st), "expired": int(exp), "mfe_r": round(mfe, 3), "mae_r": round(mae, 3),
            "mfe_ge_05": int(mfe >= 0.5), "mfe_ge_1": int(mfe >= 1.0), "mfe_ge_2": int(mfe >= 2.0), "mfe_ge_3": int(mfe >= 3.0),
            "never_positive": int(mfe <= 0.05), "stop_first": int(st and mfe < 0.2),
            "giveback_mfe1": int(mfe >= 1.0 and st and not c3), "recorded_final_r": ff(r["final_r"]) or 0.0,
            "m0_legacy_touch": round(mm["m0_legacy_touch"], 3), "m1_first_tp_close": round(mm["m1_first_tp_close"], 3),
            "m2_hold_tp3": round(mm["m2_hold_tp3"], 3), "m3_tp1_be": round(mm["m3_tp1_be"], 3),
            "m4_tp1_lock02": round(mm["m4_tp1_lock02"], 3), "m5_partial_be": round(mm["m5_partial_be"], 3),
            "m6_partial_tp1_tp2": round(mm["m6_partial_tp1_tp2"], 3), "dC_lock05": round(mm["dC_lock05"], 3),
            "dD_tp1_after_tp2": round(mm["dD_tp1_after_tp2"], 3),
            "mF_mfe_protect": round(model_f_mfe(c3, st, exp, mfe, mm["m0_legacy_touch"]), 3),
        })
    return now, recs


MODELS = ["recorded_final_r", "m0_legacy_touch", "m1_first_tp_close", "m2_hold_tp3", "m3_tp1_be", "m4_tp1_lock02", "m5_partial_be", "m6_partial_tp1_tp2", "dC_lock05", "dD_tp1_after_tp2", "mF_mfe_protect"]
REALISTIC = ["m1_first_tp_close", "m2_hold_tp3", "m3_tp1_be", "m4_tp1_lock02", "m5_partial_be", "m6_partial_tp1_tp2", "dC_lock05", "dD_tp1_after_tp2", "mF_mfe_protect"]


def S(rs, k): return round(sum(x[k] for x in rs), 1)
def pct(rs, k): return f"{round(100*sum(x[k] for x in rs)/max(1,len(rs)),1)}%"


def quality(rs, name):
    if not rs: return
    mfes = sorted(x["mfe_r"] for x in rs)
    med = mfes[len(mfes)//2]
    best_real = max(REALISTIC, key=lambda m: S(rs, m))
    print(f"\n--- SIGNAL QUALITY: {name} (n={len(rs)}) ---")
    print(f"  MFE>=0.5R {pct(rs,'mfe_ge_05')} | >=1R {pct(rs,'mfe_ge_1')} | >=2R {pct(rs,'mfe_ge_2')} | >=3R {pct(rs,'mfe_ge_3')}")
    print(f"  never_positive {pct(rs,'never_positive')} | stop_first {pct(rs,'stop_first')} | giveback(MFE>=1 then stop) {pct(rs,'giveback_mfe1')}")
    print(f"  mean MFE {round(sum(x['mfe_r'] for x in rs)/len(rs),2)}R | median {round(med,2)}R | mean MAE {round(sum(x['mae_r'] for x in rs)/len(rs),2)}R")
    print(f"  reach: TP1 {pct(rs,'reached_tp1')} TP2 {pct(rs,'reached_tp2')} TP3 {pct(rs,'reached_tp3')} stop {pct(rs,'hit_stop')} exp {pct(rs,'expired')}")
    saved = sum(1 for x in rs if x["hit_stop"] and x["mfe_r"] >= 0.6 and not x["reached_tp3"])
    print(f"  R: recorded {S(rs,'recorded_final_r')} | legacy {S(rs,'m0_legacy_touch')} | first_tp {S(rs,'m1_first_tp_close')} | hold_tp3 {S(rs,'m2_hold_tp3')} | +0.5lock {S(rs,'dC_lock05')} | partial {S(rs,'m5_partial_be')} | MODEL_F(MFE) {S(rs,'mF_mfe_protect')} | BEST_real={best_real} {S(rs,best_real)}")
    print(f"  stopped trades that reached >=0.6R favorable first (MFE-BE would rescue): {saved} ({round(100*saved/max(1,len(rs)),1)}%)")


def main():
    now, recs = build()
    date = now.date().isoformat()
    os.makedirs("data/research", exist_ok=True)
    out = f"data/research/strategy_viability_dataset_{date}.csv"
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(recs[0].keys())); w.writeheader(); w.writerows(recs)
    print(f"=== {len(recs)} economic trades (all history {min(x['entry_at'] for x in recs)[:10]}..{date}) -> {out}")

    A = [x for x in recs if x["book"] == "actionable"]
    SH = [x for x in recs if x["book"] == "shadow"]
    quality(recs, "ALL"); quality(A, "ACTIONABLE"); quality(SH, "SHADOW")

    # per-cohort realistic expectancy (actionable), ranked by best realistic R/trade
    print("\n===== PER-COHORT (actionable) — playbook x best-realistic =====")
    by = defaultdict(list)
    for x in A: by[x["playbook"]].append(x)
    rankrows = []
    for pb, rs in by.items():
        best_real = max(REALISTIC, key=lambda m: S(rs, m))
        rankrows.append((pb, len(rs), S(rs, "recorded_final_r"), S(rs, "m1_first_tp_close"), S(rs, "dC_lock05"), best_real, S(rs, best_real), round(S(rs, best_real)/max(1, len(rs)), 3), pct(rs, "mfe_ge_1")))
    for row in sorted(rankrows, key=lambda r: -r[6]):
        print(f"  {row[0]:38} n={row[1]:3} rec={row[2]:6} first_tp={row[3]:7} +0.5lock={row[4]:7} BEST={row[5]}({row[6]}) R/t={row[7]:6} MFE>=1R={row[8]}")

    for dim in ("regime", "direction", "catalyst"):
        print(f"\n===== ACTIONABLE by {dim} (best realistic) =====")
        bb = defaultdict(list)
        for x in A: bb[x[dim]].append(x)
        for k, rs in sorted(bb.items(), key=lambda kv: -S(kv[1], max(REALISTIC, key=lambda m: S(kv[1], m)))):
            br = max(REALISTIC, key=lambda m: S(rs, m))
            print(f"  {k:16} n={len(rs):3} rec={S(rs,'recorded_final_r'):6} first_tp={S(rs,'m1_first_tp_close'):7} BEST={br}({S(rs,br)}) R/t={round(S(rs,br)/max(1,len(rs)),3)}")

    # cohort-filter x risk-model portfolios
    print("\n===== PORTFOLIO SEARCH (actionable universe) =====")
    pos_cohorts = {pb for pb, rs in by.items() if max(S(rs, m) for m in REALISTIC) > 0}
    portfolios = {
        "A all-actionable": A,
        "B positive-realistic-cohorts": [x for x in A if x["playbook"] in pos_cohorts],
        "D crypto-only": [x for x in A if x["asset_class"] == "crypto"],
        "E stocks-only": [x for x in A if x["asset_class"] == "stocks"],
        "F catalyst-only": [x for x in A if x["catalyst"] == "yes"],
        "G trend-aligned": [x for x in A if "trend" in x["regime"] or x["regime"] in ("bullish", "bearish")],
        "H risk-off-shorts": [x for x in A if x["direction"] == "short" and ("off" in x["regime"] or "bear" in x["regime"])],
        "I no-chop": [x for x in A if "chop" not in x["regime"] and "range" not in x["regime"]],
        "K hybrid(pos-cohorts+catalyst-or-trend)": [x for x in A if x["playbook"] in pos_cohorts and (x["catalyst"] == "yes" or "trend" in x["regime"])],
    }
    print(f"  positive-realistic cohorts: {sorted(pos_cohorts)}")
    print(f"  {'portfolio':42} {'n':>4} {'first_tp':>9} {'hold_tp3':>9} {'+0.5lock':>9} {'partial':>9} {'BESTreal':>16}")
    for name, rs in portfolios.items():
        if not rs:
            print(f"  {name:42} EMPTY"); continue
        br = max(REALISTIC, key=lambda m: S(rs, m))
        print(f"  {name:42} {len(rs):>4} {S(rs,'m1_first_tp_close'):>9} {S(rs,'m2_hold_tp3'):>9} {S(rs,'dC_lock05'):>9} {S(rs,'m5_partial_be'):>9} {br}={S(rs,br):>7}")


if __name__ == "__main__":
    main()
