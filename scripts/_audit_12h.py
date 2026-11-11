"""READ-ONLY 12h post-fix audit data pull. No writes. Prints structured sections."""
from __future__ import annotations
import sqlite3, json, re, collections
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
db = sqlite3.connect(str(ROOT / "db" / "crypto_ai_desk.sqlite"))
db.row_factory = sqlite3.Row
W = "-14 hours"  # audit window

def q(sql, *p):
    return db.execute(sql, p).fetchall()

print("=== WINDOW: last 14h (UTC). now(UTC) =", q("SELECT datetime('now')")[0][0], "===")

# ---- volumes ----
print("\n## NEWS / CATALYST / NARRATIVE VOLUMES (14h)")
print("news_items:", q("SELECT COUNT(*) FROM news_items WHERE published_at>=datetime('now',?)", W)[0][0],
      "| by asset_class:", dict((r[0] or 'none', r[1]) for r in q(
        "SELECT asset_class,COUNT(*) FROM news_items WHERE published_at>=datetime('now',?) GROUP BY asset_class", W)))
for tbl in ("catalyst_events","narrative_baskets","events"):
    try:
        cols=[c[1] for c in q(f"PRAGMA table_info({tbl})")]
        tcol = "created_at" if "created_at" in cols else ("detected_at" if "detected_at" in cols else ("event_date" if "event_date" in cols else None))
        if tcol:
            n=q(f"SELECT COUNT(*) FROM {tbl} WHERE {tcol}>=datetime('now',?)", W)[0][0]
        else:
            n=q(f"SELECT COUNT(*) FROM {tbl}")[0][0]
        print(f"{tbl}: {n} (timecol={tcol}) cols={cols[:10]}")
    except Exception as e:
        print(f"{tbl}: ERR {e}")

# ---- catalyst importance ----
try:
    cols=[c[1] for c in q("PRAGMA table_info(catalyst_events)")]
    impcol = next((c for c in cols if "importance" in c.lower() or c.lower() in ("score","weight")), None)
    symcol = next((c for c in cols if "symbol" in c.lower() or "ticker" in c.lower()), None)
    tcol = "created_at" if "created_at" in cols else ("detected_at" if "detected_at" in cols else None)
    print("\n## CATALYST IMPORTANCE (14h) impcol=",impcol,"symcol=",symcol)
    if impcol and tcol:
        rows=q(f"SELECT {impcol} v FROM catalyst_events WHERE {tcol}>=datetime('now',?)", W)
        vals=[r[0] for r in rows if r[0] is not None]
        if vals:
            nz=sum(1 for v in vals if float(v)>0)
            print(f"n={len(vals)} nonzero={nz} min={min(vals)} max={max(vals)} avg={sum(vals)/len(vals):.2f}")
        # top events
        catcol=next((c for c in cols if c.lower() in ('category','type','catalyst_type','event_type')),None)
        titcol=next((c for c in cols if c.lower() in ('title','headline','text','summary')),None)
        sel=f"{impcol},{symcol or 'NULL'},{catcol or 'NULL'},{titcol or 'NULL'}"
        top=q(f"SELECT {sel} FROM catalyst_events WHERE {tcol}>=datetime('now',?) ORDER BY {impcol} DESC LIMIT 10", W)
        print("TOP catalysts:")
        for r in top: print("  imp=",r[0],"| sym=",r[1],"| cat=",r[2],"|",str(r[3])[:70])
        # mapped vs unmapped
        if symcol:
            mapped=q(f"SELECT SUM(CASE WHEN {symcol} IS NOT NULL AND {symcol}!='' THEN 1 ELSE 0 END), COUNT(*) FROM catalyst_events WHERE {tcol}>=datetime('now',?)", W)[0]
            print(f"mapped(symbol set)={mapped[0]} / total={mapped[1]}")
except Exception as e:
    print("catalyst importance ERR", e)

# ---- telegram collector messages ----
for tbl in ("telegram_messages","tg_messages","news_trader_messages"):
    try:
        cols=[c[1] for c in q(f"PRAGMA table_info({tbl})")]
        if cols:
            print(f"\n{tbl} exists cols={cols[:8]}")
    except Exception:
        pass

# ---- signals helper ----
def latest_signals(asset, w=W):
    return q("""WITH latest AS (SELECT signal_id,final_r,final_outcome,entry_triggered,tp1_hit,stop_hit,
        max_favorable_excursion_r mfe,max_adverse_excursion_r mae,
        ROW_NUMBER() OVER (PARTITION BY signal_id ORDER BY checked_at DESC) rn FROM signal_outcomes)
      SELECT p.signal_id,p.symbol,p.tier,p.mode,p.direction,p.score,p.status,p.created_at,
             p.entry_low,p.entry_high,p.invalidation,p.tp1,p.tp2,p.sector,p.market_regime,
             l.final_r,l.final_outcome,l.entry_triggered,l.tp1_hit,l.stop_hit,l.mfe,l.mae
      FROM proposed_signals p LEFT JOIN latest l ON l.signal_id=p.signal_id AND l.rn=1
      WHERE p.asset_class=? AND p.created_at>=datetime('now',?) ORDER BY p.created_at DESC""", asset, w)

for asset in ("crypto","stocks"):
    rows=latest_signals(asset)
    print(f"\n## {asset.upper()} SIGNALS created last 14h: {len(rows)}")
    by=collections.Counter((r['tier'],r['mode'],r['direction']) for r in rows)
    for k,v in sorted(by.items()): print("  ",k,"=",v)
    # A/B detail
    ab=[r for r in rows if r['tier'] in ('A','B')]
    print(f"  -- A/B signals: {len(ab)} --")
    for r in ab[:40]:
        print(f"  {r['created_at'][5:16]} {r['tier']} {r['symbol']:12} {r['mode']:8} {r['direction']:5} "
              f"sc={r['score']:.1f} st={r['status']:16} trig={r['entry_triggered']} fr={r['final_r']} "
              f"out={r['final_outcome']} mfe={r['mfe']} mae={r['mae']} reg={r['market_regime']}")

# ---- alerts 14h ----
print("\n## ALERTS (14h)")
print("watchlist_alerts (report-path):")
for r in q("SELECT asset_class,symbol,new_tier,direction,mode,sent_at FROM watchlist_alerts WHERE sent_at>=datetime('now',?) ORDER BY sent_at", W):
    print("  ",r['sent_at'][5:16],r['asset_class'],r['new_tier'],r['symbol'],r['direction'],r['mode'])
print("signal_alerts (monitor-path):")
sa=q("SELECT asset_class,symbol,tier,direction,alert_type,telegram_status,sent_at FROM signal_alerts WHERE sent_at>=datetime('now',?) ORDER BY sent_at", W)
print(f"  count={len(sa)}; failed={sum(1 for r in sa if 'fail' in str(r['telegram_status']))}")
for r in sa[:25]:
    print("  ",r['sent_at'][5:16],r['asset_class'],r['tier'],r['symbol'],r['direction'],r['alert_type'],r['telegram_status'])

# ---- SMCI legal gate ----
print("\n## SMCI current state")
for r in q("SELECT tier,mode,direction,score,status,created_at,counter_thesis,no_entry_conditions_json FROM proposed_signals WHERE symbol='SMCI' ORDER BY created_at DESC LIMIT 4"):
    print(f"  {r['created_at'][5:16]} tier={r['tier']} {r['mode']} {r['direction']} sc={r['score']} status={r['status']}")
    ct=(r['counter_thesis'] or '')+' '+(r['no_entry_conditions_json'] or '')
    if 'legal' in ct.lower() or 'manual review' in ct.lower(): print("    legal-flag present:", ct[:150])
# any other legal-risk stock in A/B?
print("Other stocks A/B with legal markers (14h):")
for r in q("""SELECT symbol,tier,counter_thesis FROM proposed_signals WHERE asset_class='stocks' AND tier IN ('A','B')
   AND created_at>=datetime('now',?) AND (lower(counter_thesis) LIKE '%legal%' OR lower(counter_thesis) LIKE '%indict%')""", W):
    print("  ",r['symbol'],r['tier'],str(r['counter_thesis'])[:80])

# ---- stop/TP mechanics: stopped signals ----
print("\n## STOPPED SIGNALS (14h) — MFE/MAE for stop-then-reverse analysis")
for asset in ("crypto","stocks"):
    rows=[r for r in latest_signals(asset) if r['stop_hit']==1 or r['final_outcome']=='loss']
    print(f"  {asset}: {len(rows)} stopped/loss")
    for r in rows[:20]:
        # mfe>0 and reasonably large => price went favorable before/after stop
        print(f"    {r['tier']} {r['symbol']:12} {r['mode']:8} {r['direction']:5} fr={r['final_r']} "
              f"mfe={r['mfe']} mae={r['mae']} (mfe>0.8R suggests reversal-to-target potential)")

db.close()
