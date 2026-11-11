"""HISTORICAL TP/STOP AUDIT + COUNTERFACTUAL REPLAY (read-only research).

Builds a deduped economic-trade dataset from signal_outcomes, computes TP reach-
rates, and replays counterfactual exit models reconstructed from the RECORDED
TP/stop timestamps (no re-walk needed — the production tracker already recorded
the order of level touches). Writes a CSV + prints aggregates.

IMPORTANT exit-model note (see report): the PRODUCTION tracker records
final_r = R of the HIGHEST TP level the price ever touched (banked), else stop,
else 0 (expired). i.e. it is OPTIMISTIC — a trade that touches TP1 then reverses
to the original stop is recorded as a +TP1 WIN, not a loss. The stop NEVER moves
(no BE/trailing/partial in production; shadow_exit_manager is shadow-only).
So 2TP/BE ideas only change R under a STRICTER hold-to-target model — this script
computes both the production ("best-TP") view and realistic single-target-hold
and BE views so the difference is explicit.

NOTHING is changed in production. Pure measurement.
"""
from __future__ import annotations

import csv
import json
import sqlite3
from collections import defaultdict
from datetime import datetime, timedelta, timezone

DB = "db/crypto_ai_desk.sqlite"
OUT_CSV = None  # set in main via date


def parse(ts):
    if not ts:
        return None
    try:
        s = str(ts).replace("Z", "+00:00")
        d = datetime.fromisoformat(s)
        return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
    except Exception:
        return None


def f(v):
    try:
        return None if v in (None, "") else float(v)
    except (TypeError, ValueError):
        return None


def r_multiple(entry, stop, level, direction):
    """R of `level` relative to entry, risk = |entry-stop|. None if not computable."""
    if entry is None or stop is None or level is None:
        return None
    risk = abs(entry - stop)
    if risk <= 0:
        return None
    if direction == "short":
        return (entry - level) / risk
    return (level - entry) / risk


def main():
    import os
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    now = cur.execute("SELECT max(checked_at) FROM signal_outcomes").fetchone()[0]
    now = parse(now) or datetime.now(timezone.utc)
    win60 = (now - timedelta(days=60)).isoformat()

    # latest outcome row per signal, entered, within 60d window (by entry or check)
    cur.execute("""
    WITH latest AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY signal_id ORDER BY checked_at DESC, id DESC) rn FROM signal_outcomes)
    SELECT o.*, p.symbol,p.direction,p.mode,p.tier,p.asset_class,p.market_regime,p.news_supported,
           p.telegram_supported,p.derivatives_supported,p.setup_type,p.created_at,p.suggested_entry,
           p.entry_trigger,p.entry_low,p.entry_high,p.stop_loss,p.invalidation,p.tp1,p.tp2,p.tp3,
           p.validity_window_hours,p.oi_context,p.funding_context,p.raw_idea_json
    FROM latest o JOIN proposed_signals p ON p.signal_id=o.signal_id
    WHERE o.rn=1 AND o.entry_triggered=1 AND COALESCE(o.entry_triggered_at,o.checked_at) >= ?
    """, (win60,))
    rows = [dict(r) for r in cur.fetchall()]

    try:
        from src.signals.playbooks import label_for
    except Exception:
        label_for = None

    trades = {}
    prio = {"win": 5, "loss": 5, "ambiguous": 4, "expired": 3, "not_triggered": 1, None: 0}
    for r in rows:
        entry = f(r["suggested_entry"]) or f(r["entry_trigger"]) or f(r["entry_low"])
        stop = f(r["invalidation"]) or f(r["stop_loss"])
        d = (r["direction"] or "long").lower()
        key = (r["symbol"], d, (r["mode"] or "").lower(), (r["tier"] or "").upper(),
               round(entry or 0, 8), (parse(r["entry_triggered_at"]) or parse(r["created_at"]) or now).date().isoformat())
        # dedupe: keep most-resolved
        if key in trades and prio.get(r["final_outcome"], 0) <= prio.get(trades[key]["final_outcome"], 0):
            continue
        pb = ""
        if label_for:
            try:
                sig = dict(r)
                if r["raw_idea_json"]:
                    sig.update(json.loads(r["raw_idea_json"]))
                sig.update({"tier": r["tier"], "mode": r["mode"], "asset_class": r["asset_class"], "symbol": r["symbol"]})
                pb = label_for(sig).playbook
            except Exception:
                pb = r["setup_type"] or ""
        r["_entry"] = entry; r["_stop"] = stop; r["_pb"] = pb; r["_key"] = "|".join(str(x) for x in key)
        trades[key] = r

    data = list(trades.values())

    # per-trade R ladder + exit-model reconstruction
    def rmult(r, level):
        return r_multiple(r["_entry"], r["_stop"], f(level), (r["direction"] or "long").lower())

    recs = []
    for r in data:
        d = (r["direction"] or "long").lower()
        r_tp1 = rmult(r, r["tp1"]); r_tp2 = rmult(r, r["tp2"]); r_tp3 = rmult(r, r["tp3"])
        r_stop = -1.0
        t_tp1, t_tp2, t_tp3, t_stop = (parse(r["tp1_hit_at"]), parse(r["tp2_hit_at"]),
                                       parse(r["tp3_hit_at"]), parse(r["stop_hit_at"]))
        reached1, reached2, reached3 = bool(r["tp1_hit"]), bool(r["tp2_hit"]), bool(r["tp3_hit"])
        stopped = bool(r["stop_hit"])
        fo = (r["final_outcome"] or "").lower()
        expired = fo == "expired" or (not reached1 and not stopped and fo != "win")
        mfe = f(r["max_favorable_excursion_r"]); mae = f(r["max_adverse_excursion_r"])
        cur_r = f(r["final_r"]) if r["final_r"] is not None else 0.0

        # exit-model: single-target hold to TPk (give back to stop if not reached)
        def hold_to(k_reached, r_tpk):
            if k_reached and r_tpk is not None:
                return r_tpk
            if stopped:
                return r_stop
            return 0.0  # expired/open unresolved
        hold_tp1 = hold_to(reached1, r_tp1)
        hold_tp2 = hold_to(reached2, r_tp2)
        hold_tp3 = hold_to(reached3, r_tp3)

        # best-TP-touched (production model) and a 2TP cap of it
        def best_tp(maxk):
            if maxk >= 3 and reached3 and r_tp3 is not None: return r_tp3
            if maxk >= 2 and reached2 and r_tp2 is not None: return r_tp2
            if reached1 and r_tp1 is not None: return r_tp1
            if stopped: return r_stop
            return 0.0
        prod_best = best_tp(3)        # == recorded final_r (sanity)
        cap_tp2 = best_tp(2)          # VARIANT A under production model

        # BE-after-TP1 under hold-to-TP3 baseline: if tp1 reached but tp3 not, and later stop -> 0R instead of -1R
        be_after_tp1 = hold_tp3
        if reached1 and not reached3 and stopped:
            be_after_tp1 = 0.0
        # partial 50% at TP1, runner to TP3 with BE: 0.5*r_tp1 + 0.5*(r_tp3 if reached3 else 0 if (reached1 and stopped) else stop)
        if reached1 and r_tp1 is not None:
            runner = r_tp3 if (reached3 and r_tp3 is not None) else (0.0 if stopped else 0.0)
            partial_be = 0.5 * r_tp1 + 0.5 * runner
        else:
            partial_be = r_stop if stopped else 0.0

        recs.append({
            "key": r["_key"], "signal_id": r["signal_id"], "symbol": r["symbol"], "asset_class": r["asset_class"],
            "mode": r["mode"], "tier": r["tier"], "direction": d, "playbook": r["_pb"],
            "regime": (r["market_regime"] or "").strip() or "unknown",
            "catalyst": "yes" if (r["news_supported"] or r["telegram_supported"]) else "no",
            "created_at": r["created_at"], "entry_at": r["entry_triggered_at"], "stop_at": r["stop_hit_at"],
            "final_outcome": r["final_outcome"], "final_r": cur_r,
            "r_tp1": r_tp1, "r_tp2": r_tp2, "r_tp3": r_tp3,
            "reached_tp1": int(reached1), "reached_tp2": int(reached2), "reached_tp3": int(reached3),
            "hit_stop": int(stopped), "expired": int(expired), "ambiguous": int(bool(r["status"] == "ambiguous") if r["status"] else 0),
            "mfe_r": mfe, "mae_r": mae,
            "m_prod_best": prod_best, "m_cap_tp2": cap_tp2,
            "m_hold_tp1": hold_tp1, "m_hold_tp2": hold_tp2, "m_hold_tp3": hold_tp3,
            "m_be_after_tp1": be_after_tp1, "m_partial_be": partial_be,
        })

    # write CSV
    date = now.date().isoformat()
    out_csv = f"data/research/tp_stop_replay_dataset_{date}.csv"
    os.makedirs("data/research", exist_ok=True)
    with open(out_csv, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(recs[0].keys()) if recs else ["key"])
        w.writeheader(); w.writerows(recs)

    # ---- aggregates ----
    n = len(recs)
    def rate(pred):
        c = sum(1 for x in recs if pred(x))
        return c, (round(100 * c / n, 1) if n else 0)
    print(f"=== DATASET: {n} deduped entered economic trades (60d, since {win60[:10]}) -> {out_csv}")
    # coverage: trades with any TP/stop resolution
    resolved = sum(1 for x in recs if x["reached_tp1"] or x["hit_stop"] or x["expired"])
    print(f"coverage: resolved(any tp/stop/expiry)={resolved}/{n}  with_r_ladder={sum(1 for x in recs if x['r_tp3'] is not None)}/{n}")
    print(f"TP1 reached: {rate(lambda x: x['reached_tp1'])}  TP2: {rate(lambda x: x['reached_tp2'])}  TP3: {rate(lambda x: x['reached_tp3'])}")
    print(f"stop hit: {rate(lambda x: x['hit_stop'])}  expired: {rate(lambda x: x['expired'])}")
    print(f"reached TP1 but NOT TP3: {rate(lambda x: x['reached_tp1'] and not x['reached_tp3'])}")
    print(f"reached TP2 but NOT TP3: {rate(lambda x: x['reached_tp2'] and not x['reached_tp3'])}")
    print(f"reached TP1 then later stop (give-back risk): {rate(lambda x: x['reached_tp1'] and x['hit_stop'])}")

    def sumr(recs2, kkey):
        vals = [x[kkey] for x in recs2 if x[kkey] is not None]
        return round(sum(vals), 1)
    models = ["m_prod_best", "m_cap_tp2", "m_hold_tp1", "m_hold_tp2", "m_hold_tp3", "m_be_after_tp1", "m_partial_be"]
    print("\n=== TOTAL net R by exit model (ALL entered) ===")
    for m in models:
        print(f"  {m:16} sumR={sumr(recs,m):8}  avgR={round(sumr(recs,m)/n,3) if n else 0}")

    print("\n=== by mode ===")
    bym = defaultdict(list)
    for x in recs: bym[(x['asset_class'], x['mode'])].append(x)
    for k in sorted(bym):
        g = bym[k]
        print(f"  {k[0]}/{k[1]:9} n={len(g):3}  prod={sumr(g,'m_prod_best'):6} holdTP3={sumr(g,'m_hold_tp3'):6} holdTP2={sumr(g,'m_hold_tp2'):6} capTP2={sumr(g,'m_cap_tp2'):6} BE_tp1={sumr(g,'m_be_after_tp1'):6} | TP3reached={sum(z['reached_tp3'] for z in g)}")

    print("\n=== by regime ===")
    byr = defaultdict(list)
    for x in recs: byr[x['regime']].append(x)
    for k in sorted(byr, key=lambda z:-len(byr[z])):
        g = byr[k]
        print(f"  {k[:16]:16} n={len(g):3} prod={sumr(g,'m_prod_best'):6} holdTP3={sumr(g,'m_hold_tp3'):6} capTP2={sumr(g,'m_cap_tp2'):6} TP3reached={sum(z['reached_tp3'] for z in g)}")

    print("\n=== by playbook (top) ===")
    byp = defaultdict(list)
    for x in recs: byp[x['playbook'] or '?'].append(x)
    for k in sorted(byp, key=lambda z:-len(byp[z]))[:12]:
        g = byp[k]
        tp3c = sum(z['reached_tp3'] for z in g)
        # TP3 contribution under production model = prod_best - cap_tp2
        tp3_contrib = round(sumr(g,'m_prod_best') - sumr(g,'m_cap_tp2'),1)
        print(f"  {k[:30]:30} n={len(g):3} prodR={sumr(g,'m_prod_best'):6} TP3reached={tp3c} TP3_addR(prod)={tp3_contrib} holdTP3={sumr(g,'m_hold_tp3'):6} holdTP2={sumr(g,'m_hold_tp2'):6}")


if __name__ == "__main__":
    main()
