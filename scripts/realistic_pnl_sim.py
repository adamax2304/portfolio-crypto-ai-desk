"""CRITICAL REALISTIC PnL ACCOUNTING AUDIT + DYNAMIC STOP SIMULATION (read-only).

Reconstructs, per deduped economic trade, the R that 7 execution models would have
produced from the RECORDED TP/stop touch order (signal_outcomes timestamps). Compares
them to the production touch-based final_r to quantify overstatement. Also runs dynamic
-stop variants. Writes a derived CSV + prints window/book aggregates + overstatement
counts.

DOES NOT mutate signal_outcomes or any production logic. Same-candle = stop-first
(conservative, matches production). Absolute R for hold/BE/partial models is RELATIVE-
ONLY (5m/15m granularity); legacy_touch == recorded final_r (validated 99.8%).
"""
from __future__ import annotations
import csv, json, os, sqlite3
from collections import defaultdict
from datetime import datetime, timedelta, timezone

DB = "db/crypto_ai_desk.sqlite"
STOCKS_SWING_EVENT_RS_PROFILES = {
    "stocks_swing_event_rs_pullback_quality_paper_v1",
    "stocks_swing_event_rs_pullback_flow_paper_v1",
}


def parse(ts):
    if not ts: return None
    try:
        d = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
        return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
    except Exception:
        return None

def ff(v):
    try: return None if v in (None, "") else float(v)
    except (TypeError, ValueError): return None

def rmult(entry, stop, level, direction):
    if entry is None or stop is None or level is None: return None
    risk = abs(entry - stop)
    if risk <= 0: return None
    return (entry - level)/risk if direction == "short" else (level - entry)/risk

def raw_payload(signal):
    if not isinstance(signal, dict):
        return {}
    raw = signal.get("raw_idea_json")
    if isinstance(raw, dict):
        return dict(raw)
    try:
        parsed = json.loads(raw or "{}")
        return parsed if isinstance(parsed, dict) else {}
    except Exception:
        return {}


def paper_profile(signal):
    if not isinstance(signal, dict):
        return ""
    direct = str(signal.get("paper_entry_profile") or "").strip()
    if direct:
        return direct
    return str(raw_payload(signal).get("paper_entry_profile") or "").strip()


def actionable(asset, mode, tier, signal=None):
    if (tier or "").upper() not in ("A", "B"): return False
    if asset == "crypto" and mode == "scalp": return False
    if asset == "stocks" and mode == "swing":
        return paper_profile(signal) in STOCKS_SWING_EVENT_RS_PROFILES
    if asset == "stocks" and mode == "invest": return False
    return True


def compute_models(c1, c2, c3, st, exp, R1, R2, R3):
    """Per-trade R under each execution model, from recorded touch state.
    Same-candle = stop-first conservative (matches production). Pure + testable."""
    m0 = (R3 if c3 else R2 if c2 else R1 if c1 else (-1.0 if st else 0.0))            # legacy touch (==final_r)
    m1 = (R1 if c1 else (-1.0 if st else 0.0))                                         # first TP full close
    m2 = (R3 if c3 else (-1.0 if st else 0.0))                                         # hold TP3, fixed stop
    m3 = (R3 if c3 else (0.0 if (c1 and (st or exp)) else (-1.0 if st else 0.0)))       # TP1->BE
    m4 = (R3 if c3 else (0.2 if (c1 and (st or exp)) else (-1.0 if st else 0.0)))       # TP1->+0.2R
    m5 = (0.5*R1 + 0.5*(R3 if c3 else 0.0)) if c1 else (-1.0 if st else 0.0)            # partial50 + BE runner
    m6 = ((R1 + (R2 if c2 else 0.0) + (R3 if c3 else 0.0))/3.0) if c1 else (-1.0 if st else 0.0)
    dC = (R3 if c3 else (0.5 if (c1 and (st or exp)) else (-1.0 if st else 0.0)))       # +0.5R after TP1
    dD = (R3 if c3 else (R1 if (c2 and (st or exp)) else (-1.0 if st else 0.0)))         # stop->TP1 after TP2
    return {"m0_legacy_touch": m0, "m1_first_tp_close": m1, "m2_hold_tp3": m2, "m3_tp1_be": m3,
            "m4_tp1_lock02": m4, "m5_partial_be": m5, "m6_partial_tp1_tp2": m6, "dC_lock05": dC, "dD_tp1_after_tp2": dD}


def model_f_mfe(c3, st, exp, mfe, m0):
    """MODEL F — MFE-armed protective stop (real-time trigger, not after-TP1):
    move stop to BE once price is +0.6R favorable; lock +0.5R once +1R favorable.
    Path-aware: a stopped trade whose MFE>=0.6R passed back through entry, so BE
    would have triggered at 0R (not -1R). MILD optimism only on same-candle bars."""
    if c3:
        return m0                      # ran all the way to TP3 -> keep best-TP
    if mfe >= 1.0:
        return 0.5 if (st or exp) else m0   # locked +0.5R if it later reversed; else its TP win
    if mfe >= 0.6:
        return 0.0 if (st or exp) else m0   # BE scratch if it reversed; else its TP win
    return -1.0 if st else 0.0          # never got +0.6R favorable -> full stop / flat


def main():
    con = sqlite3.connect(DB); con.row_factory = sqlite3.Row; cur = con.cursor()
    now = parse(cur.execute("SELECT max(checked_at) FROM signal_outcomes").fetchone()[0]) or datetime.now(timezone.utc)
    win60 = (now - timedelta(days=60)).isoformat()
    cur.execute("""
    WITH latest AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY signal_id ORDER BY checked_at DESC, id DESC) rn FROM signal_outcomes)
    SELECT o.*, p.symbol,p.direction,p.mode,p.tier,p.asset_class,p.market_regime,p.news_supported,p.telegram_supported,
           p.setup_type,p.created_at,p.suggested_entry,p.entry_trigger,p.entry_low,p.stop_loss,p.invalidation,
           p.tp1,p.tp2,p.tp3,p.raw_idea_json
    FROM latest o JOIN proposed_signals p ON p.signal_id=o.signal_id
    WHERE o.rn=1 AND o.entry_triggered=1 AND COALESCE(o.entry_triggered_at,o.checked_at) >= ?""", (win60,))
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
                sig = dict(r);
                if r["raw_idea_json"]: sig.update(json.loads(r["raw_idea_json"]))
                sig.update({"tier": r["tier"], "mode": r["mode"], "asset_class": r["asset_class"], "symbol": r["symbol"]})
                pb = label_for(sig).playbook
            except Exception:
                pass
        r["_e"] = entry; r["_s"] = stop; r["_pb"] = pb; r["_eat"] = eat; r["_key"] = "|".join(str(x) for x in key)
        trades[key] = r

    recs = []
    for r in trades.values():
        d = (r["direction"] or "long").lower()
        r1, r2, r3 = rmult(r["_e"], r["_s"], ff(r["tp1"]), d), rmult(r["_e"], r["_s"], ff(r["tp2"]), d), rmult(r["_e"], r["_s"], ff(r["tp3"]), d)
        R1, R2, R3 = (r1 or 0), (r2 or 0), (r3 or 0)
        c1, c2, c3 = bool(r["tp1_hit"]), bool(r["tp2_hit"]), bool(r["tp3_hit"])
        st = bool(r["stop_hit"]); fo = (r["final_outcome"] or "").lower()
        exp = fo == "expired" or (not c1 and not st and fo != "win")
        amb = (r["status"] or "") == "ambiguous"

        mm = compute_models(c1, c2, c3, st, exp, R1, R2, R3)
        m0, m1, m2, m3, m4, m5, m6, dC, dD = (mm["m0_legacy_touch"], mm["m1_first_tp_close"], mm["m2_hold_tp3"],
            mm["m3_tp1_be"], mm["m4_tp1_lock02"], mm["m5_partial_be"], mm["m6_partial_tp1_tp2"], mm["dC_lock05"], mm["dD_tp1_after_tp2"])
        runner_pb = (r["_pb"] in ("crypto_swing_narrative_rs_momentum", "crypto_failed_bounce_short", "crypto_intraday_catalyst_or_momentum")
                     or (r["asset_class"] == "crypto" and (r["mode"] or "") == "swing"))
        dG = m2 if runner_pb else m3                                                       # playbook-specific

        recs.append({
            "key": r["_key"], "signal_id": r["signal_id"], "book": ("actionable" if actionable(r["asset_class"], (r["mode"] or "").lower(), r["tier"], r) else "shadow"),
            "symbol": r["symbol"], "asset_class": r["asset_class"], "mode": r["mode"], "tier": r["tier"], "direction": d,
            "playbook": r["_pb"], "regime": (r["market_regime"] or "").strip() or "unknown",
            "catalyst": "yes" if (r["news_supported"] or r["telegram_supported"]) else "no",
            "entry_at": r["entry_triggered_at"], "stop_at": r["stop_hit_at"],
            "reached_tp1": int(c1), "reached_tp2": int(c2), "reached_tp3": int(c3), "hit_stop": int(st), "expired": int(exp),
            "tp1_then_stop": int(c1 and st and not c3), "tp2_then_stop": int(c2 and st and not c3),
            "mfe_r": ff(r["max_favorable_excursion_r"]), "mae_r": ff(r["max_adverse_excursion_r"]),
            "recorded_final_r": ff(r["final_r"]) if r["final_r"] is not None else 0.0,
            "m0_legacy_touch": round(m0, 3), "m1_first_tp_close": round(m1, 3), "m2_hold_tp3": round(m2, 3),
            "m3_tp1_be": round(m3, 3), "m4_tp1_lock02": round(m4, 3), "m5_partial_be": round(m5, 3), "m6_partial_tp1_tp2": round(m6, 3),
            "dC_lock05": round(dC, 3), "dD_tp1_after_tp2": round(dD, 3), "dG_playbook": round(dG, 3),
            "ambiguous": int(amb),
        })

    date = now.date().isoformat()
    out = f"data/research/realistic_execution_simulation_{date}.csv"
    os.makedirs("data/research", exist_ok=True)
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(recs[0].keys())); w.writeheader(); w.writerows(recs)
    print(f"=== {len(recs)} economic trades -> {out}  (now={now.date()})")

    models = ["recorded_final_r", "m0_legacy_touch", "m1_first_tp_close", "m2_hold_tp3", "m3_tp1_be", "m4_tp1_lock02", "m5_partial_be", "m6_partial_tp1_tp2", "dC_lock05", "dD_tp1_after_tp2", "dG_playbook"]
    def S(rs, k): return round(sum(x[k] for x in rs), 1)

    windows = {"60d": win60, "30d": (now-timedelta(days=30)).isoformat(), "7d": (now-timedelta(days=7)).isoformat(),
               "48h": (now-timedelta(hours=48)).isoformat(), "today": now.date().isoformat()}
    for book in ("actionable", "shadow"):
        print(f"\n===== BOOK={book} — net R by model x window =====")
        print(f"{'model':20}" + "".join(f"{w:>9}" for w in windows))
        for m in models:
            line = f"{m:20}"
            for w, since in windows.items():
                g = [x for x in recs if x["book"] == book and (x["entry_at"] or "") >= since]
                line += f"{S(g,m):>9}"
            print(line)
        g60 = [x for x in recs if x["book"] == book]
        print(f"  n(60d)={len(g60)}  TP1={sum(x['reached_tp1'] for x in g60)} TP2={sum(x['reached_tp2'] for x in g60)} TP3={sum(x['reached_tp3'] for x in g60)} stop={sum(x['hit_stop'] for x in g60)} exp={sum(x['expired'] for x in g60)}")

    # overstatement counts (actionable, 60d)
    A = [x for x in recs if x["book"] == "actionable"]
    win_now_loss_hold = [x for x in A if x["m0_legacy_touch"] > 0 and x["m2_hold_tp3"] < 0]
    tp1_then_stop_win = [x for x in A if x["tp1_then_stop"] and x["m0_legacy_touch"] > 0]
    tp2_then_stop_win = [x for x in A if x["tp2_then_stop"] and x["m0_legacy_touch"] > 0]
    over1 = [x for x in A if (x["m0_legacy_touch"] - x["m2_hold_tp3"]) >= 1.0]
    match = [x for x in A if abs(x["m0_legacy_touch"] - x["m2_hold_tp3"]) < 0.01]
    print("\n===== OVERSTATEMENT (actionable, 60d) =====")
    print(f"current WIN but hold-TP3 LOSS: {len(win_now_loss_hold)}  (R overstated here: {round(S(win_now_loss_hold,'m0_legacy_touch')-S(win_now_loss_hold,'m2_hold_tp3'),1)})")
    print(f"TP1-then-stop counted as profit by current: {len(tp1_then_stop_win)}")
    print(f"TP2-then-stop counted as profit by current: {len(tp2_then_stop_win)}")
    print(f"current_R - hold_R >= 1R: {len(over1)} trades")
    print(f"current == hold (match): {len(match)}/{len(A)}")
    print(f"TOTAL overstatement actionable 60d: legacy {S(A,'m0_legacy_touch')} vs hold_tp3 {S(A,'m2_hold_tp3')} = {round(S(A,'m0_legacy_touch')-S(A,'m2_hold_tp3'),1)}R; vs first_tp_close {S(A,'m1_first_tp_close')}; vs partial_be {S(A,'m5_partial_be')}")


if __name__ == "__main__":
    main()
