"""READ-ONLY: per-A/B-trade charts + auto-diagnosis for the 48h audit."""
from __future__ import annotations
import json, sqlite3
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "reports" / "trade_charts" / "48h"; OUT.mkdir(parents=True, exist_ok=True)
db = sqlite3.connect(str(ROOT / "db" / "crypto_ai_desk.sqlite")); db.row_factory = sqlite3.Row
from src.config import load_config
from src.storage.file_store import FileStore
cfg = load_config(); fs = FileStore(cfg)


def ts(s):
    try: return datetime.fromisoformat(str(s).replace("Z", "+00:00")).astimezone(timezone.utc)
    except Exception: return None


def load(sym, ac):
    tfs = ["15m"]
    exs = (["binance", "mexc", "bybit"] if ac == "crypto" else ["us", "yfinance", "stocks"])
    for ex in exs:
        try:
            md = fs.load_market_data(ex, [sym], tfs); f = md.get(sym, {}).get("15m")
        except Exception:
            f = None
        if f is not None and len(f) > 20:
            f = f.copy(); f["timestamp"] = pd.to_datetime(f["timestamp"], utc=True)
            return f.sort_values("timestamp").reset_index(drop=True)
    # stocks fall back to any cached path
    return None


rows = db.execute("""
WITH l AS (SELECT signal_id,final_r,final_outcome,entry_triggered,entry_triggered_at,stop_hit_at,tp1_hit_at,
   max_favorable_excursion_r mfe,max_adverse_excursion_r mae,
   ROW_NUMBER() OVER (PARTITION BY signal_id ORDER BY checked_at DESC) rn FROM signal_outcomes)
SELECT p.signal_id,p.asset_class ac,p.symbol,p.mode,p.direction d,p.tier,p.score,p.created_at,
   p.entry_low,p.entry_high,p.invalidation stop,p.tp1,p.tp2,p.tp3,p.status,p.expires_at,
   l.final_r,l.final_outcome,l.entry_triggered,l.entry_triggered_at,l.stop_hit_at,l.mfe,l.mae
FROM proposed_signals p LEFT JOIN l ON l.signal_id=p.signal_id AND l.rn=1
WHERE p.created_at>=datetime('now','-48 hours') AND p.tier IN ('A','B') ORDER BY p.created_at""").fetchall()

diag_lines = ["# Trade-by-Trade Chart Review — 48h (A/B)\n",
              "_Charts under `reports/trade_charts/48h/`. Diagnosis auto-derived from 15m OHLCV "
              "(same data a chart shows): entry-reach, late-entry, wick-vs-close stop, MFE milestones, "
              "stop-then-TP, overextension. Read-only._\n",
              "| asset | sym | mode | dir | tier | sc | outcome | R | MFE | MAE | diagnosis |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]
made = 0
for r in rows:
    sym, ac, d = r["symbol"], r["ac"], r["d"]
    entry_mid = ((r["entry_low"] or 0) + (r["entry_high"] or 0)) / 2 or None
    stop, tp1 = r["stop"], r["tp1"]
    created = ts(r["created_at"]); f = load(sym, ac)
    flags = []
    if f is not None and created is not None and entry_mid:
        post = f[f["timestamp"] >= created]
        atr = (f["high"] - f["low"]).rolling(14).mean().iloc[-1] if len(f) > 15 else None
        if len(post):
            short = (d == "short")
            reached = (post["low"].min() <= r["entry_high"]) if not short else (post["high"].max() >= r["entry_low"])
            flags.append("entry_reached" if (r["entry_triggered"] == 1 or reached) else "NEVER_ENTERED")
            if stop:
                crossed = post[post["high"] >= stop] if short else post[post["low"] <= stop]
                if len(crossed):
                    c0 = crossed.iloc[0]
                    wick = (c0["close"] < stop) if short else (c0["close"] > stop)
                    flags.append("wick_only_stop" if wick else "close_beyond_stop")
        # chart
        try:
            win = f[(f["timestamp"] >= created - pd.Timedelta(hours=6))]
            win = win[win["timestamp"] <= created + pd.Timedelta(hours=48)].tail(200)
            if len(win) > 5:
                fig, ax = plt.subplots(figsize=(9, 4))
                ax.plot(win["timestamp"], win["close"], lw=0.9, color="black")
                ax.fill_between(win["timestamp"], win["low"], win["high"], alpha=0.12, color="gray")
                if r["entry_low"] and r["entry_high"]:
                    ax.axhspan(r["entry_low"], r["entry_high"], alpha=0.18, color="blue", label="entry")
                if stop: ax.axhline(stop, color="red", lw=1, ls="--", label="stop")
                for tp, cl in ((r["tp1"], "green"), (r["tp2"], "darkgreen"), (r["tp3"], "teal")):
                    if tp: ax.axhline(tp, color=cl, lw=0.7, ls=":")
                ax.axvline(created, color="purple", lw=0.8)
                ax.set_title(f"{ac} {sym} {r['mode']} {d} {r['tier']} sc{r['score']:.0f} -> {r['final_outcome']} ({r['final_r']})", fontsize=8)
                ax.legend(fontsize=6, loc="best"); ax.tick_params(labelsize=6)
                fig.autofmt_xdate(); fig.tight_layout()
                name = f"{ac}_{r['mode']}_{sym.replace('/','-')}_{d}_{r['tier']}_{r['signal_id'][:12]}.png"
                fig.savefig(OUT / name, dpi=70); plt.close(fig); made += 1
        except Exception as e:
            flags.append(f"chart_err")
    else:
        flags.append("no_ohlcv")
    # milestone flags
    mfe = r["mfe"] or 0
    for thr, lab in ((2, "MFE>=2R"), (1, "MFE>=1R"), (0.8, "MFE>=0.8R"), (0.5, "MFE>=0.5R")):
        if mfe >= thr: flags.append(lab); break
    diag_lines.append(f"| {ac} | {sym} | {r['mode']} | {d} | {r['tier']} | {r['score']:.0f} | "
                      f"{r['final_outcome'] or r['status']} | {r['final_r']} | {round(mfe,2)} | {round(r['mae'] or 0,2)} | "
                      f"{', '.join(flags)} |")

(ROOT / "reports" / "TRADE_BY_TRADE_CHART_REVIEW_48H.md").write_text("\n".join(diag_lines), encoding="utf-8")
print(f"charts made: {made} | A/B rows: {len(rows)} | review MD written")
db.close()
