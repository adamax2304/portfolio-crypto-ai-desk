"""Crypto scalp counterfactual exit study (PART 4).

Compares 6 exit policies against the same entry/stop/TPs on existing
crypto scalp signals. Counterfactual ONLY — no production change.

Policies:
  A. current TP/SL (TP1 / stop)
  B. TP1 at +0.5R
  C. partial 50% at +0.5R, rest at original TP1
  D. TP1 at +0.7R
  E. breakeven after +0.6R, then stop=entry
  F. 4h hard expiry

Caveat: 1m crypto archive is only ~4h wide; this study falls back to 5m
or 15m and labels the result LOWER-CONFIDENCE if 1m unavailable. See
reports/BACKTEST_FEASIBILITY_AUDIT.md §7.
"""

from __future__ import annotations

import argparse
import sqlite3
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.replay_signal_execution import _candle_paths  # noqa: E402

DB = ROOT / "db" / "crypto_ai_desk.sqlite"


def _load_candles(signal: dict, prefs: tuple[str, ...]) -> tuple[pd.DataFrame | None, str]:
    for tf in prefs:
        for p in _candle_paths(signal, tf=tf):
            if not p.exists():
                continue
            try:
                df = pd.read_csv(p)
                if "timestamp" not in df.columns:
                    for c in ("Datetime", "datetime", "date", "Date"):
                        if c in df.columns:
                            df = df.rename(columns={c: "timestamp"})
                            break
                if "timestamp" not in df.columns:
                    continue
                df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
                df = df.sort_values("timestamp").reset_index(drop=True)
                return df, tf
            except Exception:
                continue
    return None, ""


def _walk(signal: dict, df: pd.DataFrame) -> dict | None:
    """Walk candles and produce per-policy R outcome."""
    created = pd.to_datetime(signal["created_at"], utc=True)
    direction = signal["direction"].lower()
    sign = 1 if direction == "long" else -1
    entry = float(signal.get("entry_trigger") or signal.get("entry_low") or 0)
    stop = float(signal.get("stop_loss") or 0)
    tp1 = float(signal.get("tp1") or 0)
    if not entry or not stop or not tp1:
        return None
    risk = abs(entry - stop)
    if risk == 0:
        return None
    expiry_4h = created + pd.Timedelta(hours=4)
    after = df[df["timestamp"] > created].copy()
    if after.empty:
        return None

    # find entry
    entry_idx = None
    entry_price = None
    for i, row in after.iterrows():
        low = float(row["low"]); high = float(row["high"])
        zlo = min(entry, stop); zhi = max(entry, stop)
        # simple fill: zone touch around entry
        if low <= entry <= high:
            entry_idx = i
            entry_price = entry
            break
    if entry_idx is None:
        return None

    post = after.loc[entry_idx + 1:] if entry_idx + 1 in after.index else after.loc[[entry_idx]]
    if post.empty:
        return None

    # for each policy compute R
    def r_from(price: float) -> float:
        return sign * (price - entry_price) / risk

    tp_0_5 = entry_price + sign * 0.5 * risk
    tp_0_7 = entry_price + sign * 0.7 * risk
    be_trigger = entry_price + sign * 0.6 * risk

    state = {
        "A": {"r": None, "hit": "open"},
        "B": {"r": None, "hit": "open"},
        "C": {"r": None, "hit": "open", "half_locked": False},
        "D": {"r": None, "hit": "open"},
        "E": {"r": None, "hit": "open", "be_armed": False, "stop_eff": stop},
        "F": {"r": None, "hit": "open"},
    }

    for i, row in post.iterrows():
        low = float(row["low"]); high = float(row["high"])
        t = row["timestamp"]

        def lhit(target):  # adverse vs target depending on direction
            if sign == 1:
                return low <= target <= high
            return low <= target <= high

        # A — current: TP1 / stop
        if state["A"]["r"] is None:
            tp_h = (sign == 1 and high >= tp1) or (sign == -1 and low <= tp1)
            st_h = (sign == 1 and low <= stop) or (sign == -1 and high >= stop)
            if tp_h and st_h:
                state["A"] = {"r": -1.0, "hit": "amb_stop"}
            elif st_h:
                state["A"] = {"r": -1.0, "hit": "stop"}
            elif tp_h:
                state["A"] = {"r": r_from(tp1), "hit": "tp1"}

        # B — TP1 at +0.5R
        if state["B"]["r"] is None:
            tp_h = (sign == 1 and high >= tp_0_5) or (sign == -1 and low <= tp_0_5)
            st_h = (sign == 1 and low <= stop) or (sign == -1 and high >= stop)
            if tp_h and st_h:
                state["B"] = {"r": -1.0, "hit": "amb_stop"}
            elif st_h:
                state["B"] = {"r": -1.0, "hit": "stop"}
            elif tp_h:
                state["B"] = {"r": 0.5, "hit": "tp_0.5R"}

        # C — partial 50% at +0.5R, rest at TP1
        if state["C"]["r"] is None:
            tp05_h = (sign == 1 and high >= tp_0_5) or (sign == -1 and low <= tp_0_5)
            tp1_h = (sign == 1 and high >= tp1) or (sign == -1 and low <= tp1)
            st_h = (sign == 1 and low <= stop) or (sign == -1 and high >= stop)
            if not state["C"]["half_locked"]:
                if tp05_h and st_h:
                    state["C"] = {"r": -0.75, "hit": "amb_partial_then_stop", "half_locked": True}  # +0.25 - 0.5
                elif st_h:
                    state["C"] = {"r": -1.0, "hit": "stop", "half_locked": False}
                elif tp05_h:
                    state["C"]["half_locked"] = True  # locked +0.25R, BE for remainder
            if state["C"]["half_locked"] and state["C"]["r"] is None:
                # remainder uses BE stop
                if tp1_h:
                    state["C"] = {"r": 0.25 + 0.5 * r_from(tp1), "hit": "tp1_after_partial"}
                elif sign == 1 and low <= entry_price:
                    state["C"] = {"r": 0.25, "hit": "be_after_partial"}
                elif sign == -1 and high >= entry_price:
                    state["C"] = {"r": 0.25, "hit": "be_after_partial"}

        # D — TP1 at +0.7R
        if state["D"]["r"] is None:
            tp_h = (sign == 1 and high >= tp_0_7) or (sign == -1 and low <= tp_0_7)
            st_h = (sign == 1 and low <= stop) or (sign == -1 and high >= stop)
            if tp_h and st_h:
                state["D"] = {"r": -1.0, "hit": "amb_stop"}
            elif st_h:
                state["D"] = {"r": -1.0, "hit": "stop"}
            elif tp_h:
                state["D"] = {"r": 0.7, "hit": "tp_0.7R"}

        # E — breakeven after +0.6R
        if state["E"]["r"] is None:
            if not state["E"]["be_armed"]:
                be_h = (sign == 1 and high >= be_trigger) or (sign == -1 and low <= be_trigger)
                if be_h:
                    state["E"]["be_armed"] = True
                    state["E"]["stop_eff"] = entry_price
            stop_eff = state["E"]["stop_eff"]
            tp_h = (sign == 1 and high >= tp1) or (sign == -1 and low <= tp1)
            st_h = (sign == 1 and low <= stop_eff) or (sign == -1 and high >= stop_eff)
            if tp_h and st_h:
                # adverse first
                state["E"] = {"r": r_from(stop_eff), "hit": "amb_stop_eff",
                              "be_armed": state["E"]["be_armed"], "stop_eff": stop_eff}
            elif st_h:
                state["E"] = {"r": r_from(stop_eff), "hit": "stop_eff",
                              "be_armed": state["E"]["be_armed"], "stop_eff": stop_eff}
            elif tp_h:
                state["E"] = {"r": r_from(tp1), "hit": "tp1",
                              "be_armed": state["E"]["be_armed"], "stop_eff": stop_eff}

        # F — 4h hard expiry on top of A
        if state["F"]["r"] is None:
            tp_h = (sign == 1 and high >= tp1) or (sign == -1 and low <= tp1)
            st_h = (sign == 1 and low <= stop) or (sign == -1 and high >= stop)
            if tp_h and st_h:
                state["F"] = {"r": -1.0, "hit": "amb_stop"}
            elif st_h:
                state["F"] = {"r": -1.0, "hit": "stop"}
            elif tp_h:
                state["F"] = {"r": r_from(tp1), "hit": "tp1"}
            elif t >= expiry_4h:
                state["F"] = {"r": r_from(float(row["close"])), "hit": "expiry_4h"}

        if all(s["r"] is not None for s in state.values()):
            break

    for k, s in state.items():
        if s["r"] is None:
            s["r"] = 0.0
            s["hit"] = "open"

    return {k: state[k]["r"] for k in state}, {k: state[k]["hit"] for k in state}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prefer-1m", action="store_true")
    args = ap.parse_args()

    prefs = ("1m", "5m", "15m") if args.prefer_1m else ("5m", "15m", "1h")

    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("""
        SELECT * FROM proposed_signals
        WHERE asset_class='crypto' AND mode='scalp'
        ORDER BY created_at
    """)
    cols = [d[0] for d in cur.description]
    rows = [dict(zip(cols, r)) for r in cur.fetchall()]
    print(f"scalp signals: {len(rows)}")

    # per-policy aggregates
    per_policy = {k: {"n": 0, "sum": 0.0, "wins": 0, "losses": 0, "by_hit": Counter()}
                  for k in ("A", "B", "C", "D", "E", "F")}
    tf_used_counter: Counter = Counter()
    skipped_no_entry = 0
    skipped_no_candle = 0
    n_with_1m = 0

    for s in rows:
        df, tf = _load_candles(s, prefs)
        if df is None:
            skipped_no_candle += 1
            continue
        tf_used_counter[tf] += 1
        if tf == "1m":
            n_with_1m += 1
        out = _walk(s, df)
        if not out:
            skipped_no_entry += 1
            continue
        rs, hits = out
        for k, r in rs.items():
            per_policy[k]["n"] += 1
            per_policy[k]["sum"] += r
            if r > 0:
                per_policy[k]["wins"] += 1
            elif r < 0:
                per_policy[k]["losses"] += 1
            per_policy[k]["by_hit"][hits[k]] += 1

    # report
    lines = []
    lines.append("# Crypto Scalp — Counterfactual 1m Exit Replay (PART 4)")
    lines.append("")
    lines.append(f"**Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append(f"**Scope:** Counterfactual exit-policy comparison on existing crypto scalp signals.")
    lines.append(f"**Source:** Existing `proposed_signals` (crypto, mode=scalp). No production change.")
    lines.append("")
    lines.append("## Data caveat (CRITICAL)")
    lines.append("")
    lines.append(f"- Total scalp signals: **{len(rows)}**")
    lines.append(f"- Replayable (entry filled in available candles): **{per_policy['A']['n']}**")
    lines.append(f"- With 1m candles available: **{n_with_1m}** (1m archive is rolling ~4h, so most fall back)")
    lines.append(f"- Skipped — no candle file: {skipped_no_candle}")
    lines.append(f"- Skipped — no entry fill in window: {skipped_no_entry}")
    lines.append("")
    lines.append(f"Candle TF used: " + ", ".join(f"{k}={v}" for k, v in tf_used_counter.most_common()))
    lines.append("")
    lines.append("**Confidence label:** **LOWER-CONFIDENCE** because most replays use 5m or 15m, "
                 "not 1m. Same-bar TP-vs-stop is adjudicated conservatively (stop first).")
    lines.append("")
    lines.append("## Policy comparison")
    lines.append("")
    lines.append("| Policy | Description | n | sum R | WR | avg R |")
    lines.append("|---|---|---:|---:|---:|---:|")
    pol_descr = {
        "A": "current (TP1 / stop)",
        "B": "TP1 at +0.5R",
        "C": "partial 50% at +0.5R, BE for rest, +TP1",
        "D": "TP1 at +0.7R",
        "E": "BE after +0.6R, then TP1 or BE-stop",
        "F": "current + 4h hard expiry",
    }
    for k in ("A", "B", "C", "D", "E", "F"):
        p = per_policy[k]
        wr = p["wins"] / max(1, p["wins"] + p["losses"])
        avg = p["sum"] / max(1, p["n"])
        lines.append(f"| {k} — {pol_descr[k]} | | {p['n']} | {p['sum']:+.2f} | {wr:.0%} | {avg:+.3f} |")
    lines.append("")
    lines.append("## Per-policy exit reason breakdown")
    for k in ("A", "B", "C", "D", "E", "F"):
        p = per_policy[k]
        lines.append(f"### Policy {k}")
        for h, n in p["by_hit"].most_common():
            lines.append(f"- {h}: {n}")
        lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("- The relative ranking of policies is informative; the absolute R values are not "
                 "trustworthy due to the 1m gap.")
    lines.append("- Same-bar TP/stop on 5m or 15m may understate B and C (partial / tight TPs).")
    lines.append("- This study is research-only; **no production exit change is implemented**.")
    lines.append("")
    lines.append("## Recommendation")
    lines.append("")
    lines.append("- Before considering any TP/SL change, run a sustained 1m collection campaign "
                 "(≥ 14 days continuous) and re-run this study with full 1m coverage.")
    lines.append("- Even with limited data, prefer the policy that **dominates A on both sum R "
                 "and WR** across re-runs; reject any policy that wins only on one metric.")

    out_md = ROOT / "reports" / "CRYPTO_SCALP_1M_EXIT_REPLAY.md"
    out_md.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out_md}")


if __name__ == "__main__":
    main()
