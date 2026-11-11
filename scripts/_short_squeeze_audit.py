"""READ-ONLY crypto short squeeze / scam-wick audit. No writes, no live logic."""
from __future__ import annotations
import sqlite3
from datetime import datetime, timezone
import pandas as pd
from src.config import load_config
from src.storage.file_store import FileStore

cfg = load_config(); fs = FileStore(cfg)
db = sqlite3.connect("db/crypto_ai_desk.sqlite"); db.row_factory = sqlite3.Row


def load15(sym):
    for ex in ("binance", "mexc", "bybit"):
        md = fs.load_market_data(ex, [sym], ["15m"])
        f = md.get(sym, {}).get("15m")
        if f is not None and len(f) > 30:
            f = f.copy(); f["timestamp"] = pd.to_datetime(f["timestamp"], utc=True)
            return ex, f.sort_values("timestamp").reset_index(drop=True)
    return None, None


def atr(f, n=14):
    h, l, c = f["high"], f["low"], f["close"]
    pc = c.shift(1)
    tr = pd.concat([h - l, (h - pc).abs(), (l - pc).abs()], axis=1).max(axis=1)
    return tr.rolling(n).mean()


def parse_ts(s):
    if not s:
        return None
    try:
        return datetime.fromisoformat(str(s).replace("Z", "+00:00")).astimezone(timezone.utc)
    except Exception:
        return None


rows = db.execute("""WITH latest AS (SELECT signal_id,final_r,final_outcome,entry_triggered,entry_triggered_at,
  stop_hit,stop_hit_at,tp1_hit,max_favorable_excursion_r mfe,max_adverse_excursion_r mae,
  ROW_NUMBER() OVER (PARTITION BY signal_id ORDER BY checked_at DESC) rn FROM signal_outcomes)
SELECT p.symbol,p.mode,p.tier,p.score,p.created_at,p.entry_low,p.entry_high,p.invalidation,p.tp1,p.tp2,
  p.status,p.market_regime,l.final_r,l.final_outcome,l.entry_triggered,l.entry_triggered_at,
  l.stop_hit,l.stop_hit_at,l.tp1_hit,l.mfe,l.mae
FROM proposed_signals p LEFT JOIN latest l ON l.signal_id=p.signal_id AND l.rn=1
WHERE p.asset_class='crypto' AND p.direction='short' AND p.created_at>=datetime('now','-48 hours')
ORDER BY p.created_at""").fetchall()

print(f"=== {len(rows)} crypto shorts (48h) ===\n")
for r in rows:
    sym = r["symbol"]
    ex, f = load15(sym)
    created = parse_ts(r["created_at"])
    entry_mid = (r["entry_low"] + r["entry_high"]) / 2 if r["entry_low"] and r["entry_high"] else None
    stop = r["invalidation"]
    tp1 = r["tp1"]
    print(f"## {sym} ({r['mode']}, {r['tier']}, sc={r['score']:.1f}) created {r['created_at'][5:16]} reg={r['market_regime']}")
    print(f"   entry~{entry_mid} stop={stop} tp1={tp1} | outcome={r['final_outcome']} R={r['final_r']} mfe={r['mfe']} mae={r['mae']} | data_ex={ex}")
    if f is None or created is None or entry_mid is None:
        print("   (insufficient data)\n"); continue
    f["atr"] = atr(f)
    # pre-entry window: candles up to created
    pre = f[f["timestamp"] <= created]
    if len(pre) < 30:
        print("   (not enough pre-entry candles)\n"); continue
    last = pre.iloc[-1]
    a = last["atr"]
    close0 = last["close"]
    ema20 = pre["close"].ewm(span=20).mean().iloc[-1]
    # downside extension
    def ret_over(periods):
        if len(pre) > periods:
            return (close0 / pre["close"].iloc[-1-periods] - 1) * 100
        return None
    ret_4 = ret_over(4)    # 1h (4x15m)
    ret_16 = ret_over(16)  # 4h
    ret_96 = ret_over(96)  # 24h
    dist_ema_atr = (close0 - ema20) / a if a else None
    atr_pct = a / close0 * 100 if close0 else None
    # upper-wick stats over last 48 pre candles (~12h)
    w = pre.tail(48).copy()
    w["uw"] = w["high"] - w[["open", "close"]].max(axis=1)
    w["uw_atr"] = w["uw"] / w["atr"]
    avg_uw_atr = w["uw_atr"].mean()
    max_uw_atr = w["uw_atr"].max()
    p90_uw = w["uw"].quantile(0.90)
    stop_dist = (stop - entry_mid) if stop and entry_mid else None
    stop_dist_atr = stop_dist / a if (stop_dist and a) else None
    stop_vs_p90wick = (stop_dist / p90_uw) if (stop_dist and p90_uw) else None
    # post-entry path
    entry_t = parse_ts(r["entry_triggered_at"]) or created
    post = f[f["timestamp"] >= entry_t]
    wick_only_stop = None
    post_stop_low = None
    hit_tp1_after_stop = None
    if stop and len(post):
        crossed = post[post["high"] >= stop]
        if len(crossed):
            c0 = crossed.iloc[0]
            wick_only_stop = bool(c0["close"] < stop)  # wick above stop but closed below
            after = post[post["timestamp"] > c0["timestamp"]]
            if len(after):
                post_stop_low = float(after["low"].min())
                if tp1:
                    hit_tp1_after_stop = bool(after["low"].min() <= tp1)
    print(f"   PRE: 1h={ret_4:+.1f}% 4h={ret_16:+.1f}% 24h={ret_96:+.1f}% | distEMA20={dist_ema_atr:+.2f}ATR | ATR%={atr_pct:.2f}")
    print(f"   WICK(48c): avg_uw/atr={avg_uw_atr:.2f} max_uw/atr={max_uw_atr:.2f} | stop_dist={stop_dist_atr:+.2f}ATR | stop/p90wick={stop_vs_p90wick}")
    print(f"   POST: wick_only_stop={wick_only_stop} | post_stop_low={post_stop_low} (tp1={tp1}) | hit_tp1_after_stop={hit_tp1_after_stop}")
    # classification
    mfe = r["mfe"] or 0
    if mfe >= 0.8:
        cls = "near_miss_then_squeeze"
    elif mfe <= 0.2 and (r["mae"] or 0) <= -0.8:
        cls = "immediate_wrong_side / late_short"
    elif r["final_outcome"] == "expired":
        cls = "expired_flat / inconclusive"
    else:
        cls = "inconclusive"
    if dist_ema_atr is not None and dist_ema_atr < -2:
        cls += " | overextended_down(>2ATR)"
    print(f"   CLASS: {cls}\n")
db.close()
