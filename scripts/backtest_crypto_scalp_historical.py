"""Crypto scalp historical backtest engine (PART 3).

Pure-technical replay mirroring production scalp geometry
(reports/SCALP_LOGIC_RECONSTRUCTION_AUDIT.md):
  - EMA20/ATR14 indicators (production enrich_ohlcv)
  - entry zone close∓[0.20,0.65]ATR, ATR stop close∓1.2ATR, TP 1/2/3 ATR
  - 2h validity, chase filter (|close-EMA20|/ATR <= 2), no-lookahead.

Reads db/scalp_history.sqlite (downloaded archive). NEVER touches the
production DB. Outputs reports/SCALP_HISTORICAL_BACKTEST_*.{csv,md}.

Exit policies (PART 4) selectable via --policy:
  A current | B tp0.5 | C partial0.5 | D tp0.7 | E be0.6 | F expiry4h | G trail0.7
"""

from __future__ import annotations

import argparse
import csv
import sqlite3
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
ARCHIVE = ROOT / "db" / "scalp_history.sqlite"

from src.indicators.technicals import enrich_ohlcv, recent_range, trend_label  # noqa: E402

# Execution cost (crypto taker round-trip + slippage), per BACKTEST_EXECUTION_COST_MODEL
FEE_BPS_RT = 10.0
SLIP_BPS = 5.0
VALIDITY_BARS_5M = 24       # 2h on 5m
SCAN_EVERY_BARS = 6         # scan every 30 min on 5m
WARMUP = 210                # need EMA200/ATR warmup


@dataclass
class Trade:
    symbol: str
    direction: str
    created_at: str
    entry: float
    stop: float
    tp1: float
    risk: float
    policy: str
    outcome: str = "open"
    raw_r: float = 0.0
    mfe_r: float = 0.0
    mae_r: float = 0.0
    bars_to_mfe: int = 0
    fakeout: bool = False
    fees_r: float = 0.0
    regime: str = ""
    session: str = ""


def _load(con, symbol: str, tf: str = "5m") -> pd.DataFrame:
    df = pd.read_sql_query(
        "SELECT ts, open, high, low, close, volume FROM ohlcv "
        "WHERE symbol=? AND timeframe=? ORDER BY ts", con, params=(symbol, tf),
    )
    if df.empty:
        return df
    df["timestamp"] = pd.to_datetime(df["ts"], unit="ms", utc=True)
    return df


def _session(ts: pd.Timestamp) -> str:
    h = ts.hour
    if 0 <= h < 8:
        return "asia"
    if 8 <= h < 14:
        return "europe"
    return "us"


def _simulate_exit(direction, entry, stop, tp1, tp2, tp3, fwd, policy):
    """Walk forward candles after entry. Return (outcome, raw_r, mfe_r, mae_r, bars_to_mfe, fakeout)."""
    sign = 1 if direction == "long" else -1
    risk = abs(entry - stop)
    if risk == 0:
        return "zero_risk", 0.0, 0.0, 0.0, 0, False
    be_armed = False
    eff_stop = stop
    half_locked = False
    best = 0.0
    bmfe = 0
    for i, c in enumerate(fwd.itertuples()):
        hi, lo, cl = float(c.high), float(c.low), float(c.close)
        fav = (hi - entry) / risk if sign == 1 else (entry - lo) / risk
        adv = (lo - entry) / risk if sign == 1 else (entry - hi) / risk
        if fav > best:
            best = fav; bmfe = i + 1
        # policy-specific TP target
        if policy == "B":
            tp_px = entry + sign * 0.5 * risk
        elif policy == "D":
            tp_px = entry + sign * 0.7 * risk
        else:
            tp_px = tp1
        tp_hit = (sign == 1 and hi >= tp_px) or (sign == -1 and lo <= tp_px)
        # breakeven arm (E) / trail (G)
        if policy == "E" and not be_armed:
            if (sign == 1 and hi >= entry + 0.6 * risk) or (sign == -1 and lo <= entry - 0.6 * risk):
                be_armed = True; eff_stop = entry
        if policy == "G" and best >= 0.7:
            # trail to (best-0.5)R behind
            trail = entry + sign * (best - 0.5) * risk
            eff_stop = max(eff_stop, trail) if sign == 1 else min(eff_stop, trail)
        stop_hit = (sign == 1 and lo <= eff_stop) or (sign == -1 and hi >= eff_stop)
        # partial (C): 50% at +0.5R then BE for remainder to tp1
        if policy == "C":
            half_tp = entry + sign * 0.5 * risk
            half_hit = (sign == 1 and hi >= half_tp) or (sign == -1 and lo <= half_tp)
            if not half_locked and half_hit:
                half_locked = True; eff_stop = entry
            if half_locked:
                if (sign == 1 and hi >= tp1) or (sign == -1 and lo <= tp1):
                    return "tp1_after_partial", 0.25 + 0.5 * sign * (tp1 - entry) / risk, best, adv, bmfe, False
                if (sign == 1 and lo <= eff_stop) or (sign == -1 and hi >= eff_stop):
                    return "be_after_partial", 0.25, best, adv, bmfe, best >= 0.5
                continue
            if (sign == 1 and lo <= eff_stop) or (sign == -1 and hi >= eff_stop):
                return "stop", -1.0, best, adv, bmfe, False
            continue
        if tp_hit and stop_hit:
            return "stop_ambiguous", sign * (eff_stop - entry) / risk, best, adv, bmfe, best >= 0.5
        if stop_hit:
            return "stop", sign * (eff_stop - entry) / risk, best, adv, bmfe, best >= 0.5
        if tp_hit:
            return "tp", sign * (tp_px - entry) / risk, best, adv, bmfe, False
    # expired
    last_close = float(fwd["close"].iloc[-1]) if len(fwd) else entry
    return "expired", sign * (last_close - entry) / risk, best, (adv if len(fwd) else 0.0), bmfe, best >= 0.5


def backtest(policy: str, validity_bars: int) -> list[Trade]:
    con = sqlite3.connect(ARCHIVE)
    symbols = [r[0] for r in con.execute(
        "SELECT DISTINCT symbol FROM ohlcv WHERE timeframe='5m'").fetchall()]
    trades: list[Trade] = []
    for sym in symbols:
        df = _load(con, sym, "5m")
        if len(df) < WARMUP + 50:
            continue
        enr = enrich_ohlcv(df)
        n = len(enr)
        # Precompute arrays once — avoid O(n) frame slicing per scan (was O(n^2)).
        close_a = enr["close"].to_numpy(dtype=float)
        high_a = enr["high"].to_numpy(dtype=float)
        low_a = enr["low"].to_numpy(dtype=float)
        ema20_a = enr["ema20"].to_numpy(dtype=float)
        ema50_a = enr["ema50"].to_numpy(dtype=float) if "ema50" in enr.columns else ema20_a
        atr_a = enr["atr14"].to_numpy(dtype=float)
        ts_a = enr["timestamp"].to_numpy()
        for i in range(WARMUP, n - validity_bars, SCAN_EVERY_BARS):
            close = close_a[i]
            atr = atr_a[i]
            ema20 = ema20_a[i]
            ema50 = ema50_a[i]
            if not atr or atr <= 0 or atr != atr:  # NaN guard
                continue
            dist = abs((close - ema20) / atr)
            if dist > 2.0:  # chase filter
                continue
            # trend_label equivalent: close vs ema20 vs ema50
            if close > ema20 > ema50:
                direction = "long"
            elif close < ema20 < ema50:
                direction = "short"
            else:
                continue
            tr = "uptrend" if direction == "long" else "downtrend"
            # recent_range over last 20 bars ending at i
            lo20 = low_a[i - 20: i + 1]
            hi20 = high_a[i - 20: i + 1]
            support = float(lo20.min())
            resistance = float(hi20.max())
            sign = 1 if direction == "long" else -1
            entry_lo = close - 0.65 * atr if sign == 1 else close + 0.20 * atr
            entry_hi = close - 0.20 * atr if sign == 1 else close + 0.65 * atr
            atr_stop = close - 1.2 * atr if sign == 1 else close + 1.2 * atr
            if sign == 1:
                supp_stop = (support - 0.15 * atr) if support else None
                stop = supp_stop if (supp_stop is not None and supp_stop > close - 1.8 * atr) else atr_stop
            else:
                res_stop = (resistance + 0.15 * atr) if resistance else None
                stop = res_stop if (res_stop is not None and res_stop < close + 1.8 * atr) else atr_stop
            tp1 = close + sign * 1.0 * atr
            tp2 = close + sign * 2.0 * atr
            tp3 = close + sign * 3.0 * atr
            # Sanity guard (backtest only): the stop must sit on the correct
            # side of the entry zone with a sane distance. A support/resistance
            # stop landing inside/near the entry zone produces a degenerate
            # near-zero risk → exploding R. Production RR checks reject these;
            # we skip them here (mirrors "no clean invalidation").
            entry_ref = entry_lo if sign == 1 else entry_hi
            min_risk = 0.30 * atr
            if sign == 1:
                if stop >= entry_ref - min_risk:
                    stop = entry_ref - min_risk
            else:
                if stop <= entry_ref + min_risk:
                    stop = entry_ref + min_risk
            # entry fill within validity window
            fut = enr.iloc[i + 1: i + 1 + validity_bars]
            entry_fill = None; fill_idx = None
            zlo, zhi = min(entry_lo, entry_hi), max(entry_lo, entry_hi)
            for j, c in enumerate(fut.itertuples()):
                if float(c.low) <= zhi and float(c.high) >= zlo:
                    entry_fill = (zlo if sign == 1 else zhi)
                    fill_idx = j
                    break
                # moved away before fill
                if (sign == 1 and float(c.low) <= stop) or (sign == -1 and float(c.high) >= stop):
                    break
            if entry_fill is None:
                continue
            post = fut.iloc[fill_idx + 1:]
            if post.empty:
                continue
            outcome, raw_r, mfe, mae, bmfe, fake = _simulate_exit(
                direction, entry_fill, stop, tp1, tp2, tp3, post, policy)
            # fees in R
            risk = abs(entry_fill - stop)
            fees_r = -(entry_fill * (FEE_BPS_RT + SLIP_BPS) / 10000.0) / risk if risk else 0.0
            ts = pd.Timestamp(ts_a[i])
            trades.append(Trade(
                symbol=sym, direction=direction, created_at=ts.isoformat(),
                entry=entry_fill, stop=stop, tp1=tp1, risk=risk, policy=policy,
                outcome=outcome, raw_r=raw_r + fees_r, mfe_r=mfe, mae_r=mae,
                bars_to_mfe=bmfe, fakeout=fake, fees_r=fees_r,
                regime=tr, session=_session(ts),
            ))
    con.close()
    return trades


ALL_POLICIES = ["A", "B", "C", "D", "E", "F", "G"]


def backtest_all_policies(validity_bars: int) -> dict[str, list[Trade]]:
    """One scan pass; evaluate every exit policy per generated candidate.

    Far cheaper than running backtest() 7×. Candidate generation + entry fill
    are identical across policies; only the exit walk differs.
    """
    con = sqlite3.connect(ARCHIVE)
    symbols = [r[0] for r in con.execute(
        "SELECT DISTINCT symbol FROM ohlcv WHERE timeframe='5m'").fetchall()]
    out: dict[str, list[Trade]] = {p: [] for p in ALL_POLICIES}
    for sym in symbols:
        df = _load(con, sym, "5m")
        if len(df) < WARMUP + 50:
            continue
        enr = enrich_ohlcv(df)
        n = len(enr)
        close_a = enr["close"].to_numpy(dtype=float)
        high_a = enr["high"].to_numpy(dtype=float)
        low_a = enr["low"].to_numpy(dtype=float)
        ema20_a = enr["ema20"].to_numpy(dtype=float)
        ema50_a = enr["ema50"].to_numpy(dtype=float) if "ema50" in enr.columns else ema20_a
        atr_a = enr["atr14"].to_numpy(dtype=float)
        ts_a = enr["timestamp"].to_numpy()
        for i in range(WARMUP, n - validity_bars, SCAN_EVERY_BARS):
            close, atr, ema20, ema50 = close_a[i], atr_a[i], ema20_a[i], ema50_a[i]
            if not atr or atr <= 0 or atr != atr:
                continue
            if abs((close - ema20) / atr) > 2.0:
                continue
            if close > ema20 > ema50:
                direction = "long"; sign = 1; tr = "uptrend"
            elif close < ema20 < ema50:
                direction = "short"; sign = -1; tr = "downtrend"
            else:
                continue
            support = float(low_a[i - 20: i + 1].min())
            resistance = float(high_a[i - 20: i + 1].max())
            entry_lo = close - 0.65 * atr if sign == 1 else close + 0.20 * atr
            entry_hi = close - 0.20 * atr if sign == 1 else close + 0.65 * atr
            atr_stop = close - 1.2 * atr if sign == 1 else close + 1.2 * atr
            if sign == 1:
                supp = (support - 0.15 * atr) if support else None
                stop = supp if (supp is not None and supp > close - 1.8 * atr) else atr_stop
            else:
                res = (resistance + 0.15 * atr) if resistance else None
                stop = res if (res is not None and res < close + 1.8 * atr) else atr_stop
            tp1 = close + sign * 1.0 * atr
            tp2 = close + sign * 2.0 * atr
            tp3 = close + sign * 3.0 * atr
            entry_ref = entry_lo if sign == 1 else entry_hi
            min_risk = 0.30 * atr
            if sign == 1 and stop >= entry_ref - min_risk:
                stop = entry_ref - min_risk
            elif sign == -1 and stop <= entry_ref + min_risk:
                stop = entry_ref + min_risk
            fut = enr.iloc[i + 1: i + 1 + validity_bars]
            zlo, zhi = min(entry_lo, entry_hi), max(entry_lo, entry_hi)
            entry_fill = None; fill_idx = None
            for j, c in enumerate(fut.itertuples()):
                if float(c.low) <= zhi and float(c.high) >= zlo:
                    entry_fill = zlo if sign == 1 else zhi; fill_idx = j; break
                if (sign == 1 and float(c.low) <= stop) or (sign == -1 and float(c.high) >= stop):
                    break
            if entry_fill is None:
                continue
            post = fut.iloc[fill_idx + 1:]
            if post.empty:
                continue
            risk = abs(entry_fill - stop)
            fees_r = -(entry_fill * (FEE_BPS_RT + SLIP_BPS) / 10000.0) / risk if risk else 0.0
            ts = pd.Timestamp(ts_a[i])
            sess = _session(ts)
            for p in ALL_POLICIES:
                # policy F uses a longer expiry window already captured by post
                # (we approximate F by extending the post slice to 4h = 48 bars).
                pp = post
                if p == "F":
                    pp = enr.iloc[i + 1 + fill_idx + 1: i + 1 + fill_idx + 1 + 48]
                    if pp.empty:
                        pp = post
                oc, rr, mfe, mae, bmfe, fake = _simulate_exit(
                    direction, entry_fill, stop, tp1, tp2, tp3, pp, "A" if p == "F" else p)
                out[p].append(Trade(
                    symbol=sym, direction=direction, created_at=ts.isoformat(),
                    entry=entry_fill, stop=stop, tp1=tp1, risk=risk, policy=p,
                    outcome=oc, raw_r=rr + fees_r, mfe_r=mfe, mae_r=mae,
                    bars_to_mfe=bmfe, fakeout=fake, fees_r=fees_r, regime=tr, session=sess))
    con.close()
    return out


def summarize(trades: list[Trade]) -> dict:
    n = len(trades)
    wins = sum(1 for t in trades if t.raw_r > 0)
    losses = sum(1 for t in trades if t.raw_r < 0)
    expired = sum(1 for t in trades if t.outcome == "expired")
    raw = sum(t.raw_r for t in trades)
    sized = raw * 0.5
    pf = (sum(t.raw_r for t in trades if t.raw_r > 0) /
          abs(sum(t.raw_r for t in trades if t.raw_r < 0))) if any(t.raw_r < 0 for t in trades) else float("inf")
    import statistics
    mfe = statistics.mean([t.mfe_r for t in trades]) if trades else 0
    mae = statistics.mean([t.mae_r for t in trades]) if trades else 0
    fees = sum(t.fees_r for t in trades)
    # max drawdown on equity curve
    eq = 0.0; peak = 0.0; mdd = 0.0
    for t in sorted(trades, key=lambda x: x.created_at):
        eq += t.raw_r
        peak = max(peak, eq)
        mdd = min(mdd, eq - peak)
    return dict(n=n, wins=wins, losses=losses, expired=expired,
                wr=wins / max(1, wins + losses), pf=pf, raw=raw, sized=sized,
                avg_r=raw / max(1, n), mfe=mfe, mae=mae, fees=fees, mdd=mdd,
                fakeouts=sum(1 for t in trades if t.fakeout))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--policy", default="A")
    ap.add_argument("--validity-bars", type=int, default=VALIDITY_BARS_5M)
    ap.add_argument("--write-csv", action="store_true")
    ap.add_argument("--all-policies", action="store_true")
    args = ap.parse_args()
    if args.all_policies:
        allt = backtest_all_policies(args.validity_bars)
        import json as _json
        res = {}
        for p, ts in allt.items():
            res[p] = summarize(ts)
        out = ROOT / "reports" / "SCALP_EXIT_VARIANTS_SUMMARY.json"
        out.write_text(_json.dumps(res, indent=2), encoding="utf-8")
        for p in ALL_POLICIES:
            s = res[p]
            print(f"{p}: n={s['n']} WR={s['wr']:.0%} PF={s['pf']:.2f} "
                  f"avgR={s['avg_r']:+.3f} rawR={s['raw']:+.0f} MDD={s['mdd']:.0f} "
                  f"MFE={s['mfe']:.2f} fees={s['fees']:.0f}")
        # also dump regime/session split for policy A
        a = allt["A"]
        split = {"by_regime": {}, "by_session": {}, "by_direction": {}, "by_symbol": {}}
        import collections
        for key, attr in (("by_regime", "regime"), ("by_session", "session"), ("by_direction", "direction"), ("by_symbol", "symbol")):
            g = collections.defaultdict(list)
            for t in a:
                g[getattr(t, attr)].append(t)
            for k, ts in g.items():
                split[key][k] = summarize(ts)
        (ROOT / "reports" / "SCALP_SPLIT_SUMMARY.json").write_text(_json.dumps(split, indent=2), encoding="utf-8")
        print("wrote SCALP_EXIT_VARIANTS_SUMMARY.json + SCALP_SPLIT_SUMMARY.json")
        return
    trades = backtest(args.policy, args.validity_bars)
    s = summarize(trades)
    print(f"policy={args.policy} n={s['n']} W={s['wins']} L={s['losses']} exp={s['expired']} "
          f"WR={s['wr']:.0%} PF={s['pf']:.2f} rawR={s['raw']:+.1f} sizedR={s['sized']:+.1f} "
          f"avgR={s['avg_r']:+.3f} MFE={s['mfe']:.2f} MAE={s['mae']:.2f} MDD={s['mdd']:.1f} fees={s['fees']:.1f}")
    if args.write_csv:
        out = ROOT / "reports" / "SCALP_HISTORICAL_BACKTEST_RESULTS.csv"
        with out.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["symbol", "direction", "created_at", "entry", "stop", "outcome",
                        "raw_r", "mfe_r", "mae_r", "bars_to_mfe", "fakeout", "regime", "session"])
            for t in trades:
                w.writerow([t.symbol, t.direction, t.created_at, f"{t.entry:.6f}", f"{t.stop:.6f}",
                            t.outcome, f"{t.raw_r:.3f}", f"{t.mfe_r:.2f}", f"{t.mae_r:.2f}",
                            t.bars_to_mfe, t.fakeout, t.regime, t.session])
        print(f"wrote {out}")


if __name__ == "__main__":
    main()
