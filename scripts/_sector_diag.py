"""READ-ONLY stocks sector-performance diagnostic + sector-gate simulation.

No DB writes, no scoring/threshold/logic changes. Pulls unique stock setups
(deduped by signal_id, latest outcome) from the live DB, joins sector +
relative-strength parsed from each idea's evidence, and:
  PART 1 — performance breakdown by sector/symbol/mode/tier/direction/flags.
  PART 2 — simulate 3 sector-aware long-gate variants (A/B/C) read-only.

Run: py -3 scripts/_sector_diag.py
"""
from __future__ import annotations

import collections
import json
import re
import statistics
import sqlite3
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db" / "crypto_ai_desk.sqlite"
DAYS = 14
LEADER_RS = 5.0      # sector ETF RS vs SPY >= this → leader
LAGGARD_RS = -3.0    # sector ETF RS vs SPY <= this → laggard

cfg = yaml.safe_load((ROOT / "config" / "stocks" / "universe.yaml").read_text(encoding="utf-8"))
SYM_SECTOR = cfg["symbol_sector_map"]
SECTOR_ETF = cfg["sector_etfs"]
ETF_TO_SECTOR = {v: k for k, v in SECTOR_ETF.items()}
INDICES = {"SPY", "QQQ", "IWM", "DIA"}

db = sqlite3.connect(str(DB))
db.row_factory = sqlite3.Row

rows = db.execute(
    """
    WITH latest AS (
      SELECT signal_id, final_r, final_outcome, entry_triggered, tp1_hit, stop_hit,
             ROW_NUMBER() OVER (PARTITION BY signal_id ORDER BY checked_at DESC) rn
      FROM signal_outcomes)
    SELECT p.signal_id, p.symbol, p.tier, p.mode, p.direction, p.score, p.created_at,
           p.news_supported, p.thesis, p.raw_idea_json,
           l.final_r, l.final_outcome, l.entry_triggered, l.tp1_hit, l.stop_hit
    FROM proposed_signals p
    LEFT JOIN latest l ON l.signal_id = p.signal_id AND l.rn = 1
    WHERE p.asset_class='stocks' AND p.created_at >= date('now', ?)
    """,
    (f"-{DAYS} day",),
).fetchall()


def parse_ev(raw):
    rs_spy = rs_sec = None
    earnings = "?"
    catalyst = False
    try:
        ev = (json.loads(raw) or {}).get("evidence", []) if raw else []
    except Exception:
        ev = []
    for e in ev:
        m = re.search(r"RS vs SPY \(20d\): ([+-]?[0-9.]+)%", e)
        if m:
            rs_spy = float(m.group(1))
        m = re.search(r"RS vs sector ETF \(20d\): ([+-]?[0-9.]+)%", e)
        if m:
            rs_sec = float(m.group(1))
        le = e.lower()
        if "earnings:" in le:
            if "safe" in le:
                earnings = "safe"
            elif "n/a" in le:
                earnings = "n/a"
            elif "unknown" in le:
                earnings = "unknown"
            elif "today" in le:
                earnings = "today"
        if "catalyst" in le or "news" in le:
            catalyst = True
    return rs_spy, rs_sec, earnings, catalyst


def sector_of(sym):
    if sym in INDICES:
        return "index_etf"
    if sym in ETF_TO_SECTOR:
        return ETF_TO_SECTOR[sym]
    return SYM_SECTOR.get(sym, "unknown")


recs = []
for r in rows:
    rs_spy, rs_sec, earnings, catalyst = parse_ev(r["raw_idea_json"])
    recs.append({
        "sid": r["signal_id"], "sym": r["symbol"], "tier": r["tier"], "mode": r["mode"],
        "dir": r["direction"], "created": r["created_at"][:10],
        "sector": sector_of(r["symbol"]),
        "is_etf": r["symbol"] in INDICES or r["symbol"] in ETF_TO_SECTOR,
        "rs_spy": rs_spy, "rs_sec": rs_sec, "earnings": earnings,
        "catalyst": bool(catalyst) or bool(r["news_supported"]),
        "trig": (r["entry_triggered"] or 0) == 1,
        "fr": r["final_r"], "fo": (r["final_outcome"] or ""),
        "tp1": (r["tp1_hit"] or 0) == 1, "stop": (r["stop_hit"] or 0) == 1,
    })

# sector RS (from each sector ETF's own RS-vs-SPY signals)
sec_rs_samples = collections.defaultdict(list)
for x in recs:
    if x["sym"] in ETF_TO_SECTOR and x["rs_spy"] is not None:
        sec_rs_samples[ETF_TO_SECTOR[x["sym"]]].append(x["rs_spy"])
SECTOR_RS = {s: round(statistics.mean(v), 2) for s, v in sec_rs_samples.items() if v}


def sector_bucket(sector):
    rs = SECTOR_RS.get(sector)
    if rs is None:
        return "neutral?"  # no ETF signal sampled
    if rs >= LEADER_RS:
        return "leader"
    if rs <= LAGGARD_RS:
        return "laggard"
    return "neutral"


for x in recs:
    x["sec_bucket"] = sector_bucket(x["sector"])


def resolved(x):
    return x["trig"] and x["fr"] is not None and x["fo"] not in ("", "pending", "open", "active")


def metrics(items):
    res = [x for x in items if resolved(x)]
    n = len(items)
    trig = sum(1 for x in items if x["trig"])
    wins = sum(1 for x in res if x["fr"] > 0)
    losses = sum(1 for x in res if x["fr"] < 0)
    totR = sum(x["fr"] for x in res)
    avgR = (totR / len(res)) if res else 0.0
    gp = sum(x["fr"] for x in res if x["fr"] > 0)
    gl = -sum(x["fr"] for x in res if x["fr"] < 0)
    pf = (gp / gl) if gl > 0 else (float("inf") if gp > 0 else 0.0)
    stops = sum(1 for x in res if x["stop"])
    tp1s = sum(1 for x in res if x["tp1"])
    return {
        "n": n, "trig": trig, "res": len(res), "wins": wins, "losses": losses,
        "avgR": round(avgR, 3), "totR": round(totR, 1),
        "PF": round(pf, 2) if pf != float("inf") else 999.0,
        "stop%": round(100 * stops / len(res), 0) if res else 0,
        "tp1%": round(100 * tp1s / len(res), 0) if res else 0,
    }


def table(title, key):
    print(f"\n### {title}")
    groups = collections.defaultdict(list)
    for x in recs:
        groups[x[key]].append(x)
    print(f"{'group':22} | n | trig | res | W | L | avgR | totR | PF | stop% | tp1%")
    for k in sorted(groups, key=lambda g: metrics(groups[g])["totR"]):
        m = metrics(groups[k])
        print(f"{str(k):22} | {m['n']:3} | {m['trig']:3} | {m['res']:3} | {m['wins']:3} | {m['losses']:3} | "
              f"{m['avgR']:+.3f} | {m['totR']:+.1f} | {m['PF']:.2f} | {m['stop%']:.0f} | {m['tp1%']:.0f}")


print(f"=== WINDOW: last {DAYS} days | unique stock setups: {len(recs)} ===")
print(f"SECTOR RS vs SPY (sampled from ETF signals): {SECTOR_RS}")
print("\n############ PART 1 — PERFORMANCE BREAKDOWN ############")
table("By TIER", "tier")
table("By MODE", "mode")
table("By DIRECTION", "dir")
table("By SECTOR", "sector")
table("By SECTOR BUCKET (leader/neutral/laggard)", "sec_bucket")
table("ETF vs single name", "is_etf")
table("By SYMBOL", "sym")

# overall
print("\n### OVERALL")
print(metrics(recs))

print("\n############ PART 2 — SECTOR-GATE SIMULATION (read-only) ############")
# population: actionable A/B LONG stock signals
pop = [x for x in recs if x["tier"] in ("A", "B") and x["dir"] == "long"]
cur = metrics(pop)
rs_cov = sum(1 for x in pop if x["rs_spy"] is not None)
sec_cov = sum(1 for x in pop if x["rs_sec"] is not None)
print(f"\nCURRENT actionable A/B longs: {cur}")
print(f"RS-vs-SPY coverage in population: {rs_cov}/{len(pop)} ({100*rs_cov/len(pop):.0f}%)")
print(f"RS-vs-sector coverage in population: {sec_cov}/{len(pop)} ({100*sec_cov/len(pop):.0f}%)")


def keep(x, variant):
    """Decision uses STOCK-level RS (reliably stored per signal). Sector-ETF
    RS-vs-SPY is only available for tech/semis in the DB, so we proxy "weak
    sector" with the stock's own RS-vs-sector-ETF (rs_sec) which IS stored.
    Signals with no parsed RS are KEPT (insufficient data → never penalised)."""
    rs_spy = x["rs_spy"]
    rs_sec = x["rs_sec"]
    cat = x["catalyst"]
    if rs_spy is None:
        return True  # cannot decide → keep
    if variant == "A":  # strict: stock leads market AND its sector
        if rs_sec is None:
            return rs_spy > 0
        return rs_spy > 0 and rs_sec > 0
    if variant == "B":  # moderate: stock leads the market (RS vs SPY > 0)
        return rs_spy > 0
    if variant == "C":  # moderate + catalyst exception
        return (rs_spy > 0) or cat
    return True


for variant in ("A", "B", "C"):
    kept = [x for x in pop if keep(x, variant)]
    removed = [x for x in pop if not keep(x, variant)]
    km = metrics(kept)
    rm = metrics(removed)
    rem_res = [x for x in removed if resolved(x)]
    rem_win = sum(1 for x in rem_res if x["fr"] > 0)
    rem_los = sum(1 for x in rem_res if x["fr"] < 0)
    rem_win_R = round(sum(x["fr"] for x in rem_res if x["fr"] > 0), 1)
    rem_los_R = round(sum(x["fr"] for x in rem_res if x["fr"] < 0), 1)
    net = round(km["totR"] - cur["totR"], 1)
    rem_syms = collections.Counter(x["sym"] for x in removed)
    print(f"\n--- VARIANT {variant} ---")
    print(f" kept:    n={km['n']} res={km['res']} totR={km['totR']:+.1f} PF={km['PF']:.2f} avgR={km['avgR']:+.3f}")
    print(f" removed: n={rm['n']} res={rm['res']} winners_removed={rem_win}({rem_win_R:+.1f}R) losers_removed={rem_los}({rem_los_R:+.1f}R)")
    print(f" NET totR change (kept - current): {net:+.1f}R  | PF {cur['PF']:.2f} -> {km['PF']:.2f}")
    print(f" removed symbols: {dict(rem_syms.most_common(12))}")
