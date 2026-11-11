"""READ-ONLY 48h trade-universe + analysis. Writes CSV/MD; prints digest. No mutations."""
from __future__ import annotations
import csv, json, sqlite3, collections, statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
db = sqlite3.connect(str(ROOT / "db" / "crypto_ai_desk.sqlite")); db.row_factory = sqlite3.Row
W = "-48 hours"

rows = db.execute(f"""
WITH latest AS (SELECT signal_id,final_r,final_outcome,entry_triggered,entry_triggered_at,
   stop_hit,stop_hit_at,tp1_hit,tp1_hit_at,tp2_hit,tp3_hit,
   max_favorable_excursion_r mfe,max_adverse_excursion_r mae,
   ROW_NUMBER() OVER (PARTITION BY signal_id ORDER BY checked_at DESC) rn FROM signal_outcomes)
SELECT p.signal_id,p.asset_class,p.symbol,p.mode,p.direction,p.tier,p.score,p.created_at,
   p.source_report_path,p.entry_low,p.entry_high,p.invalidation,p.tp1,p.tp2,p.tp3,p.status,
   p.market_regime,p.sector,p.news_supported,p.expires_at,p.raw_idea_json,
   l.final_r,l.final_outcome,l.entry_triggered,l.entry_triggered_at,l.stop_hit,l.stop_hit_at,
   l.tp1_hit,l.tp1_hit_at,l.mfe,l.mae
FROM proposed_signals p LEFT JOIN latest l ON l.signal_id=p.signal_id AND l.rn=1
WHERE p.created_at>=datetime('now',?) ORDER BY p.created_at""", (W,)).fetchall()

# telegram-sent lookup
wl = {(r["symbol"], r["sent_at"][:13]) for r in db.execute(
    "SELECT symbol,sent_at FROM watchlist_alerts WHERE sent_at>=datetime('now',?)", (W,))}
sa_syms = {r["symbol"] for r in db.execute(
    "SELECT DISTINCT symbol FROM signal_alerts WHERE sent_at>=datetime('now',?) AND telegram_status='sent'", (W,))}
wl_syms = {s for s, _ in wl}

def caps_of(raw):
    try:
        return json.loads(raw or "{}").get("cap_reasons") or []
    except Exception:
        return []

recs = []
for r in rows:
    caps = caps_of(r["raw_idea_json"])
    capstr = " ; ".join(caps)
    tg = (r["symbol"] in wl_syms) or (r["symbol"] in sa_syms)
    recs.append({
        "signal_id": r["signal_id"], "asset_class": r["asset_class"], "symbol": r["symbol"],
        "mode": r["mode"], "direction": r["direction"], "tier": r["tier"], "score": r["score"],
        "created_at": r["created_at"], "source_report_path": r["source_report_path"] or "",
        "telegram_sent": "yes" if tg else "no",
        "entry_low": r["entry_low"], "entry_high": r["entry_high"], "stop": r["invalidation"],
        "tp1": r["tp1"], "tp2": r["tp2"], "tp3": r["tp3"], "status": r["status"],
        "final_outcome": r["final_outcome"] or "", "final_r": r["final_r"],
        "mfe_r": r["mfe"], "mae_r": r["mae"], "entry_triggered": r["entry_triggered"],
        "entry_at": r["entry_triggered_at"] or "", "tp1_at": r["tp1_hit_at"] or "",
        "stop_at": r["stop_hit_at"] or "", "expires_at": r["expires_at"] or "",
        "regime": r["market_regime"] or "", "sector": r["sector"] or "",
        "news_supported": r["news_supported"], "cap_reasons": capstr,
        "capped": "yes" if caps else "no",
    })

# write CSV
csv_path = ROOT / "reports" / "TRADE_UNIVERSE_48H.csv"
csv_path.parent.mkdir(exist_ok=True)
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(recs[0].keys()))
    w.writeheader(); w.writerows(recs)
print(f"WROTE {csv_path} ({len(recs)} rows)")

def resolved(x):
    return x["entry_triggered"] == 1 and x["final_r"] is not None and x["final_outcome"] not in ("", "pending", "open", "active")

def metrics(items):
    res = [x for x in items if resolved(x)]
    n = len(items); trig = sum(1 for x in items if x["entry_triggered"] == 1)
    wins = sum(1 for x in res if x["final_r"] > 0); loss = sum(1 for x in res if x["final_r"] < 0)
    flat = sum(1 for x in res if x["final_r"] == 0)
    totR = sum(x["final_r"] for x in res); avgR = totR/len(res) if res else 0
    gp = sum(x["final_r"] for x in res if x["final_r"] > 0); gl = -sum(x["final_r"] for x in res if x["final_r"] < 0)
    pf = gp/gl if gl > 0 else (999 if gp > 0 else 0)
    wr = wins/(wins+loss) if (wins+loss) else 0
    return dict(n=n, trig=trig, res=len(res), W=wins, L=loss, flat=flat, totR=round(totR,1),
                avgR=round(avgR,3), PF=round(pf,2), WR=round(wr,3))

def grp(items, key):
    g = collections.defaultdict(list)
    for x in items:
        g[key(x)].append(x)
    return {k: metrics(v) for k, v in sorted(g.items())}

def show(title, d):
    print(f"\n## {title}")
    for k, m in sorted(d.items(), key=lambda kv: kv[1]["totR"]):
        print(f"  {str(k):28} n={m['n']:3} trig={m['trig']:3} W/L/flat={m['W']}/{m['L']}/{m['flat']} "
              f"PF={m['PF']:.2f} avgR={m['avgR']:+.3f} totR={m['totR']:+.1f} WR={m['WR']:.0%}")

for ac in ("crypto", "stocks"):
    sub = [x for x in recs if x["asset_class"] == ac]
    ab = [x for x in sub if x["tier"] in ("A", "B")]
    c = [x for x in sub if x["tier"] == "C"]
    print(f"\n===== {ac.upper()} (48h): total {len(sub)} | A/B {len(ab)} | C {len(c)} =====")
    print("A/B HEADLINE:", metrics(ab))
    print("C-tier watchlist:", metrics(c))
    show(f"{ac} A/B by mode", grp(ab, lambda x: x["mode"]))
    show(f"{ac} A/B by tier", grp(ab, lambda x: x["tier"]))
    show(f"{ac} A/B by direction", grp(ab, lambda x: x["direction"]))
    show(f"{ac} A/B by regime", grp(ab, lambda x: x["regime"] or "(blank)"))
    if ac == "stocks":
        show("stocks A/B ETF-vs-single", grp(ab, lambda x: "ETF" if x["symbol"] in {"SPY","QQQ","IWM","DIA","SMH","XLK","XLF","XLE","XLY","XLV"} else "single"))
    show(f"{ac} A/B catalyst-supported", grp(ab, lambda x: "news" if x["news_supported"] else "no_news"))
    # capped shorts (crypto)
    if ac == "crypto":
        sq = [x for x in sub if x["direction"]=="short" and "squeeze" in x["cap_reasons"].lower()]
        print(f"\n  crypto shorts squeeze-capped: {len(sq)} ->", [x['symbol'] for x in sq][:15])
        passed_short = [x for x in ab if x["direction"]=="short"]
        print(f"  crypto A/B shorts (passed): {len(passed_short)}", metrics(passed_short))

db.close()
