"""READ-ONLY trade-by-trade OHLCV diagnosis for triggered/closed A/B (72h)."""
from __future__ import annotations
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
db = sqlite3.connect(str(ROOT / "db" / "crypto_ai_desk.sqlite")); db.row_factory = sqlite3.Row
from src.config import load_config
from src.storage.file_store import FileStore
cfg = load_config(); fs = FileStore(cfg)


def ts(s):
    try: return datetime.fromisoformat(str(s).replace("Z", "+00:00")).astimezone(timezone.utc)
    except Exception: return None


def load(sym, ac):
    exs = (["binance", "mexc", "bybit"] if ac == "crypto" else ["us", "yfinance", "stocks"])
    for ex in exs:
        try:
            md = fs.load_market_data(ex, [sym], ["15m"]); f = md.get(sym, {}).get("15m")
        except Exception:
            f = None
        if f is not None and len(f) > 20:
            f = f.copy(); f["timestamp"] = pd.to_datetime(f["timestamp"], utc=True)
            return f.sort_values("timestamp").reset_index(drop=True)
    return None


rows = db.execute("""
WITH l AS (SELECT signal_id,final_r,final_outcome,entry_triggered,entry_triggered_at,stop_hit_at,tp1_hit_at,
   max_favorable_excursion_r mfe,max_adverse_excursion_r mae,
   ROW_NUMBER() OVER (PARTITION BY signal_id ORDER BY checked_at DESC) rn FROM signal_outcomes)
SELECT p.signal_id,p.asset_class ac,p.symbol,p.mode,p.direction d,p.tier,p.score,p.created_at,
   p.entry_low,p.entry_high,p.invalidation stop,p.tp1,p.tp2,p.status,p.market_regime,p.news_supported,
   l.final_r,l.final_outcome,l.entry_triggered,l.stop_hit_at,l.tp1_hit_at,l.mfe,l.mae
FROM proposed_signals p LEFT JOIN l ON l.signal_id=p.signal_id AND l.rn=1
WHERE p.created_at>=datetime('now','-72 hours') AND p.tier IN ('A','B') ORDER BY p.asset_class,p.created_at""").fetchall()

out = ["# Post-Weekend Trade-by-Trade Review — A/B (72h)\n",
       "_OHLCV-derived diagnosis from 15m bars (entry-reach, wick-vs-close stop, MFE milestone, "
       "stop-then-TP, overextension). Charts omitted (diagnosis-only run); crypto charts available via "
       "`_audit48_charts.py`. Stocks 15m cache path limited (TODO-stocks-chart-ohlcv-path).\n",
       "| asset | sym | mode | dir | tier | sc | outcome | R | MFE | MAE | catalyst | diagnosis |",
       "|---|---|---|---|---|---|---|---|---|---|---|---|"]

for r in rows:
    sym, ac, d = r["symbol"], r["ac"], r["d"]
    trig = r["entry_triggered"] == 1
    closed = (r["final_outcome"] or "") not in ("", "pending", "open", "active")
    if not (trig or closed):
        continue
    entry_lo, entry_hi, stop, tp1 = r["entry_low"], r["entry_high"], r["stop"], r["tp1"]
    created = ts(r["created_at"]); f = load(sym, ac)
    flags = []
    short = (d == "short")
    if f is not None and created is not None and entry_lo and entry_hi:
        post = f[f["timestamp"] >= created]
        if len(post):
            reached = (post["low"].min() <= entry_hi) if not short else (post["high"].max() >= entry_lo)
            flags.append("entry_reached" if (trig or reached) else "NEVER_ENTERED")
            if stop and len(post):
                crossed = post[post["high"] >= stop] if short else post[post["low"] <= stop]
                if len(crossed):
                    c0 = crossed.iloc[0]
                    wick = (c0["close"] < stop) if short else (c0["close"] > stop)
                    flags.append("wick_only_stop" if wick else "close_beyond_stop")
            # stop-then-TP
            if stop and tp1 and r["stop_hit_at"] and len(post):
                sh = ts(r["stop_hit_at"])
                if sh is not None:
                    aft = post[post["timestamp"] > sh]
                    if len(aft):
                        hit = (aft["low"].min() <= tp1) if short else (aft["high"].max() >= tp1)
                        if hit: flags.append("stop_then_TP")
    else:
        flags.append("no_ohlcv")
    mfe = r["mfe"] or 0; mae = r["mae"] or 0
    for thr, lab in ((2, "MFE>=2R"), (1, "MFE>=1R"), (0.8, "MFE>=0.8R"), (0.5, "MFE>=0.5R")):
        if mfe >= thr: flags.append(lab); break
    # classify loss
    fr = r["final_r"]
    if fr is not None and fr < 0:
        if "wick_only_stop" in flags: flags.append("DIAG:wick_stop")
        elif mfe < 0.5: flags.append("DIAG:faded_no_mfe(late/bad-candidate)")
        elif mfe >= 1: flags.append("DIAG:gave_back_winner(TP-too-far/trail)")
        else: flags.append("DIAG:normal_chop")
    cat = "news" if r["news_supported"] else "-"
    out.append(f"| {ac} | {sym} | {r['mode']} | {d} | {r['tier']} | {r['score']:.0f} | "
               f"{r['final_outcome'] or r['status']} | {fr} | {round(mfe,2)} | {round(mae,2)} | {cat} | "
               f"{', '.join(flags)} |")

(ROOT / "reports" / "POST_WEEKEND_TRADE_BY_TRADE_REVIEW.md").write_text("\n".join(out), encoding="utf-8")
print(f"rows diagnosed: {len(out)-4} | A/B trig-or-closed of {len(rows)} A/B total")
db.close()
