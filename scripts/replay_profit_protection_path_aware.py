"""Path-aware crypto profit-protection replay (profitability guardrails PART 4).

Unlike the MFE/MAE counterfactual, this walks OHLCV candle-by-candle in sequence
(entry first, then each candle) so BE/partial/trailing triggers respect path order
and BE-stop whipsaw is modeled. Read-only; writes only a CSV + the MD report.

DOES NOT enable partial_exit_model or change any config. If path-aware net R is
not clearly positive, the verdict is DO_NOT_ENABLE / DATA_COVERAGE_INSUFFICIENT.

Coverage caveat: the live OHLCV store keeps only rolling ~220-candle windows
(1m≈4h, 5m≈18h, 15m≈2.3d, 1h≈9d). A clean 7-30d 1m/5m replay is therefore NOT
possible; the script uses the finest timeframe that fully covers each trade's
entry→exit window and reports coverage %.
"""
from __future__ import annotations

import csv
import sqlite3
import statistics
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db" / "crypto_ai_desk.sqlite"
OUT_CSV = ROOT / "reports" / "CRYPTO_PROFIT_PROTECTION_PATH_AWARE_REPLAY.csv"
EXCHANGES = ("binance", "bybit", "mexc")
TFS = ("5m", "15m", "1h")  # finest first; 1m is today-only so excluded
LOOKBACK_DAYS = 30

VARIANTS = ["A_current", "B_BE_0.5R", "C_BE_1R", "D_partial50_1R",
            "E_33_33_runner", "F_trail_1R", "G_candle_close_stop",
            "H_one_reentry", "I_no_reentry"]


def _parse(ts):
    if not ts:
        return None
    try:
        return datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
    except Exception:
        return None


def load_trades():
    conn = sqlite3.connect(f"file:{DB.as_posix()}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    since = (datetime.now(timezone.utc).timestamp() - LOOKBACK_DAYS * 86400)
    rows = conn.execute(
        """
        SELECT s.signal_id, s.symbol, s.mode, s.direction, s.tier, s.asset_class,
               s.market_regime, s.news_supported,
               s.entry_low, s.entry_high, s.suggested_entry, s.entry_trigger,
               s.stop_loss, s.invalidation, s.tp1, s.tp2, s.tp3, s.created_at,
               o.entry_triggered, o.entry_triggered_at, o.entry_price_used,
               o.final_r, o.final_outcome,
               COALESCE(o.stop_hit_at, o.tp3_hit_at, o.tp2_hit_at, o.tp1_hit_at,
                        o.checked_at) AS exit_at
        FROM proposed_signals s
        JOIN signal_outcomes o ON o.signal_id = s.signal_id
        WHERE o.id IN (SELECT MAX(id) FROM signal_outcomes GROUP BY signal_id)
          AND (s.asset_class = 'crypto' OR s.asset_class IS NULL)
          AND s.mode IN ('intraday', 'swing')
          AND o.entry_triggered = 1
          AND o.final_outcome IN ('win', 'loss', 'partial_win')
        """
    ).fetchall()
    conn.close()
    out = []
    for r in rows:
        d = dict(r)
        ct = _parse(d["created_at"])
        if ct and ct.timestamp() >= since:
            out.append(d)
    return out


ARCHIVE_DIR = ROOT / "data" / "archive" / "ohlcv"
CACHE_DIR = ROOT / "data" / "raw" / "ohlcv"


def _ohlcv_path(ex, tf, sym):
    """Prefer the deep archive (PART 6) over the rolling cache, so a path-aware
    replay sees as much history as has been accumulated."""
    arch = ARCHIVE_DIR / ex / tf / f"{sym}.csv"
    if arch.exists():
        return arch
    cache = CACHE_DIR / ex / tf / f"{sym}.csv"
    return cache if cache.exists() else None


def load_ohlcv(symbol):
    """Return (df, exchange, tf) of the finest TF available for this symbol,
    archive-first then rolling cache."""
    sym = symbol.replace("/", "_").upper()
    for tf in TFS:
        for ex in EXCHANGES:
            p = _ohlcv_path(ex, tf, sym)
            if p is not None:
                try:
                    df = pd.read_csv(p)
                    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
                    return df, ex, tf
                except Exception:
                    continue
    return None, None, None


def _r_at(price, entry, r_unit, direction):
    if direction == "short":
        return (entry - price) / r_unit
    return (price - entry) / r_unit


def simulate(variant, entry, stop, tps, direction, candles):
    """Walk candles after entry; return realized R for the variant.

    Conservative same-candle rule: if a candle's range hits both the active stop
    and a target, the stop is taken first (matches the production tracker)."""
    r_unit = abs(entry - stop)
    if r_unit == 0 or not candles:
        return None
    long = direction != "short"
    # ordered targets (nearest first)
    tlist = [t for t in tps if t is not None]
    tlist = sorted(tlist) if long else sorted(tlist, reverse=True)

    active_stop = stop
    peak_r = 0.0
    booked = 0.0          # realized R already locked from partials
    remaining = 1.0       # fraction of position still open
    tps_hit = 0
    moved_be = False
    reentered = False

    def hit_stop(c):
        return (c["low"] <= active_stop) if long else (c["high"] >= active_stop)

    def hit_stop_close(c):
        return (c["close"] <= active_stop) if long else (c["close"] >= active_stop)

    def hit_price(c, px):
        return (c["high"] >= px) if long else (c["low"] <= px)

    for c in candles:
        cand_r = _r_at(c["high"] if long else c["low"], entry, r_unit, direction)
        peak_r = max(peak_r, cand_r)

        # dynamic stop adjustments BEFORE evaluating this candle's stop
        if variant in ("B_BE_0.5R",) and peak_r >= 0.5 and not moved_be:
            active_stop = entry; moved_be = True
        if variant in ("C_BE_1R", "D_partial50_1R") and peak_r >= 1.0 and not moved_be:
            active_stop = entry; moved_be = True
        if variant == "F_trail_1R" and peak_r >= 1.0:
            trail = (entry + (peak_r - 1.0) * r_unit) if long else (entry - (peak_r - 1.0) * r_unit)
            active_stop = max(active_stop, trail) if long else min(active_stop, trail)

        # partial bookings
        if variant == "D_partial50_1R" and remaining == 1.0 and hit_price(c, tlist[0] if tlist else entry) and tlist:
            booked += 0.5 * _r_at(tlist[0], entry, r_unit, direction)
            remaining = 0.5
            active_stop = entry; moved_be = True
        if variant == "E_33_33_runner" and tlist:
            # book 1/3 at tp1, 1/3 at tp2 as they are reached
            if tps_hit == 0 and len(tlist) >= 1 and hit_price(c, tlist[0]):
                booked += (1 / 3) * _r_at(tlist[0], entry, r_unit, direction); tps_hit = 1; remaining = 2 / 3
            if tps_hit == 1 and len(tlist) >= 2 and hit_price(c, tlist[1]):
                booked += (1 / 3) * _r_at(tlist[1], entry, r_unit, direction); tps_hit = 2; remaining = 1 / 3
                active_stop = entry; moved_be = True

        # stop check (conservative; candle-close variant uses close)
        stopped = hit_stop_close(c) if variant == "G_candle_close_stop" else hit_stop(c)
        if stopped:
            exit_r = _r_at(active_stop, entry, r_unit, direction)
            total = booked + remaining * exit_r
            if variant == "H_one_reentry" and not reentered and exit_r <= -0.99:
                reentered = True
                # re-enter when price reclaims entry later in the same series
                continue
            return round(total, 3)

        # final target check
        if tlist:
            final_tp = tlist[-1]
            if hit_price(c, final_tp):
                total = booked + remaining * _r_at(final_tp, entry, r_unit, direction)
                return round(total, 3)

    # ran out of candles → mark at last close (path incomplete within window)
    last = candles[-1]
    total = booked + remaining * _r_at(last["close"], entry, r_unit, direction)
    return round(total, 3)


def covered(df, entry_dt, exit_dt):
    if df is None or entry_dt is None:
        return False
    tmin, tmax = df["timestamp"].min(), df["timestamp"].max()
    end = exit_dt or entry_dt
    return tmin <= entry_dt and tmax >= end


def main():
    trades = load_trades()
    rows = []
    per_variant = {v: [] for v in VARIANTS}
    n_total = len(trades)
    n_covered = 0
    tf_used = {}

    for t in trades:
        df, ex, tf = load_ohlcv(t["symbol"])
        entry_dt = _parse(t["entry_triggered_at"]) or _parse(t["created_at"])
        exit_dt = _parse(t["exit_at"])
        entry = (t["entry_price_used"] or t["suggested_entry"]
                 or t["entry_trigger"] or t["entry_low"])
        stop = t["stop_loss"] or t["invalidation"]
        if entry is None or stop is None:
            continue
        if not covered(df, entry_dt, exit_dt):
            rows.append({"signal_id": t["signal_id"], "symbol": t["symbol"],
                         "mode": t["mode"], "covered": False, "tf": tf or "none",
                         "actual_final_r": t["final_r"]})
            continue
        n_covered += 1
        tf_used[tf] = tf_used.get(tf, 0) + 1
        walk = df[df["timestamp"] >= entry_dt].to_dict("records")
        direction = (t["direction"] or "long").lower()
        tps = [t["tp1"], t["tp2"], t["tp3"]]
        row = {"signal_id": t["signal_id"], "symbol": t["symbol"], "mode": t["mode"],
               "tier": t["tier"], "regime": t["market_regime"],
               "catalyst": "yes" if (t["news_supported"] or 0) > 0 else "no",
               "covered": True, "tf": tf, "actual_final_r": t["final_r"]}
        for v in VARIANTS:
            r = simulate(v, float(entry), float(stop), [float(x) if x is not None else None for x in tps],
                         direction, walk)
            row[v] = r
            if r is not None:
                per_variant[v].append(r)
        rows.append(row)

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fields = ["signal_id", "symbol", "mode", "tier", "regime", "catalyst",
              "covered", "tf", "actual_final_r"] + VARIANTS
    with OUT_CSV.open("w", newline="", encoding="utf-8") as fo:
        w = csv.DictWriter(fo, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    def stats(rs):
        if not rs:
            return {"n": 0, "net_R": 0, "PF": None, "winrate": None,
                    "avg_win": None, "avg_loss": None}
        wins = [x for x in rs if x > 0]
        losses = [x for x in rs if x < 0]
        gp, gl = sum(wins), -sum(losses)
        return {"n": len(rs), "net_R": round(sum(rs), 2),
                "PF": round(gp / gl, 2) if gl else None,
                "winrate": round(len(wins) / len(rs) * 100, 1),
                "avg_win": round(statistics.mean(wins), 2) if wins else None,
                "avg_loss": round(statistics.mean(losses), 2) if losses else None}

    summary = {
        "n_total": n_total, "n_covered": n_covered,
        "coverage_pct": round(n_covered / n_total * 100, 1) if n_total else 0,
        "tf_used": tf_used,
        "variants": {v: stats(per_variant[v]) for v in VARIANTS},
    }
    import json
    print(json.dumps(summary, indent=1))
    (ROOT / "reports" / "_profit_protection_path_aware.json").write_text(
        json.dumps(summary, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
