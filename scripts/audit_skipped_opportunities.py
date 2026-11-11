"""PART 1 — Skipped / near-miss opportunity logger.

For every rejected idea (in `rejected_ideas`) and every C-tier signal in
`proposed_signals` (last 14d), look up subsequent price action and decide:

  - did the same symbol later become A/B?
  - did the price reach +0.5R / +1R / current TP (proxy: pct moves)?
  - did the skip save a loss or miss a winner?

Outputs:
  reports/SKIPPED_SIGNAL_OPPORTUNITY_AUDIT.md
  reports/SKIPPED_SIGNAL_FOLLOWUP.csv

Read-only. Never writes back into `proposed_signals` / `signal_outcomes` /
`signal_alerts` / `watchlist_alerts`.
"""

from __future__ import annotations

import csv
import json
import sqlite3
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

DB = ROOT / "db" / "crypto_ai_desk.sqlite"


def _load_candles_for_symbol(symbol: str, asset_class: str) -> pd.DataFrame | None:
    """Try the most-likely candle source and return a normalized df."""
    if asset_class == "crypto":
        base = symbol.replace("/", "_").replace("-", "_")
        for exch in ("binance", "bybit", "mexc"):
            for tf in ("15m", "1h"):
                p = ROOT / "data" / "raw" / "ohlcv" / exch / tf / f"{base}.csv"
                if p.exists():
                    try:
                        df = pd.read_csv(p)
                        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
                        return df.sort_values("timestamp").reset_index(drop=True)
                    except Exception:
                        continue
        return None
    # stocks
    for tf in ("15m", "1h", "1d"):
        p = ROOT / "data" / "raw" / "stocks" / tf / f"{symbol}.csv"
        if p.exists():
            try:
                df = pd.read_csv(p)
                if "Datetime" in df.columns:
                    df = df.rename(columns={"Datetime": "timestamp"})
                df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
                return df.sort_values("timestamp").reset_index(drop=True)
            except Exception:
                continue
    return None


def _move_pct(df: pd.DataFrame, after: datetime, hours: int, direction: str) -> float | None:
    """Return signed pct move from price-at-decision to highest/lowest in window."""
    cutoff = after + pd.Timedelta(hours=hours)
    sub = df[(df["timestamp"] > after) & (df["timestamp"] <= cutoff)]
    if sub.empty:
        return None
    decision_row = df[df["timestamp"] <= after].tail(1)
    if decision_row.empty:
        return None
    p0 = float(decision_row["close"].iloc[0])
    if p0 <= 0:
        return None
    if direction == "long":
        peak = float(sub["high"].max())
        return (peak - p0) / p0
    peak = float(sub["low"].min())
    return (p0 - peak) / p0


def main() -> None:
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row

    # Rejected ideas in last 14d
    rejected = con.execute("""
        SELECT created_at, symbol, asset_class, direction_bias, score,
               primary_reason, reasons_json, risk_flags_json
        FROM rejected_ideas
        WHERE created_at >= '2026-05-28'
        ORDER BY created_at DESC
    """).fetchall()

    # C-tier signals in last 14d (different table, different schema)
    c_tier = con.execute("""
        SELECT created_at, symbol, asset_class, direction, mode, score, tier,
               setup_type, market_regime, news_supported
        FROM proposed_signals
        WHERE tier = 'C' AND created_at >= '2026-05-28'
        ORDER BY created_at DESC
    """).fetchall()

    # Did the same symbol later get A/B? (any time after the skip)
    later_ab = defaultdict(list)
    for r in con.execute("""
        SELECT symbol, created_at, tier, direction, mode,
               (SELECT final_r FROM signal_outcomes o WHERE o.signal_id = ps.signal_id
                ORDER BY o.id DESC LIMIT 1) AS final_r
        FROM proposed_signals ps
        WHERE tier IN ('A','B')
    """).fetchall():
        later_ab[r["symbol"]].append({
            "created_at": r["created_at"], "tier": r["tier"],
            "direction": r["direction"], "final_r": r["final_r"],
        })

    csv_path = ROOT / "reports" / "SKIPPED_SIGNAL_FOLLOWUP.csv"
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "kind", "timestamp", "symbol", "asset_class", "direction", "score",
        "reason", "later_ab_promoted", "later_ab_wins", "later_ab_total_r",
        "move_1h_pct", "move_4h_pct", "move_24h_pct",
        "reached_+0.5R_proxy", "reached_+1R_proxy",
        "skip_saved_loss", "skip_missed_winner", "notes",
    ]

    rows_out = []
    reason_counter: Counter = Counter()
    saved_losses = 0
    missed_winners = 0

    def classify(symbol: str, asset_class: str, direction: str, ts: str,
                 reason: str, score: float, kind: str) -> dict:
        decision = pd.to_datetime(ts, utc=True)
        df = _load_candles_for_symbol(symbol, asset_class)
        m1 = m4 = m24 = None
        reached_05 = reached_10 = ""
        if df is not None and not df.empty:
            m1 = _move_pct(df, decision, 1, direction)
            m4 = _move_pct(df, decision, 4, direction)
            m24 = _move_pct(df, decision, 24, direction)
            # +0.5R proxy: assume risk = ~1.5% for crypto, ~1% for stocks
            risk_pct = 0.015 if asset_class == "crypto" else 0.01
            best = m4 if m4 is not None else (m1 or 0)
            reached_05 = "yes" if best and best >= 0.5 * risk_pct else "no"
            reached_10 = "yes" if best and best >= 1.0 * risk_pct else "no"
        ab_hits = later_ab.get(symbol, [])
        ab_after = [a for a in ab_hits if a["created_at"] > ts]
        ab_wins = sum(1 for a in ab_after if (a["final_r"] or 0) > 0)
        ab_total_r = sum(float(a["final_r"] or 0) for a in ab_after)
        # Heuristics:
        # - skip_saved_loss: same symbol later got A/B + LOST
        # - skip_missed_winner: same symbol later got A/B + WON, OR
        #   price moved >= +1R in intended direction within 24h with no later A/B
        skip_saved_loss = ab_after and ab_total_r < 0
        skip_missed_winner = (ab_wins > 0) or (reached_10 == "yes" and not ab_after)
        return {
            "kind": kind,
            "timestamp": ts,
            "symbol": symbol,
            "asset_class": asset_class,
            "direction": direction,
            "score": score,
            "reason": reason[:90],
            "later_ab_promoted": "yes" if ab_after else "no",
            "later_ab_wins": ab_wins,
            "later_ab_total_r": f"{ab_total_r:+.2f}",
            "move_1h_pct": f"{m1*100:+.2f}" if m1 is not None else "",
            "move_4h_pct": f"{m4*100:+.2f}" if m4 is not None else "",
            "move_24h_pct": f"{m24*100:+.2f}" if m24 is not None else "",
            "reached_+0.5R_proxy": reached_05,
            "reached_+1R_proxy": reached_10,
            "skip_saved_loss": "yes" if skip_saved_loss else "no",
            "skip_missed_winner": "yes" if skip_missed_winner else "no",
            "notes": "",
        }

    # Sample-down rejected to keep CSV manageable (~5000 rejected → cap 800)
    rejected_sample = list(rejected)[:800]
    print(f"processing {len(rejected_sample)} rejected + {len(c_tier)} C-tier rows...")
    for r in rejected_sample:
        rec = classify(r["symbol"], r["asset_class"] or "crypto",
                       r["direction_bias"] or "long", r["created_at"],
                       r["primary_reason"] or "", float(r["score"] or 0), "rejected")
        rows_out.append(rec)
        reason_counter[(r["primary_reason"] or "")[:50]] += 1
        if rec["skip_saved_loss"] == "yes": saved_losses += 1
        if rec["skip_missed_winner"] == "yes": missed_winners += 1
    for r in c_tier:
        rec = classify(r["symbol"], r["asset_class"] or "crypto",
                       r["direction"] or "long", r["created_at"],
                       f"C-tier (mode={r['mode']}, regime={r['market_regime']})",
                       float(r["score"] or 0), "c_tier")
        rows_out.append(rec)
        reason_counter[f"C-tier {r['mode']}"] += 1
        if rec["skip_saved_loss"] == "yes": saved_losses += 1
        if rec["skip_missed_winner"] == "yes": missed_winners += 1

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows_out:
            w.writerow(r)
    print(f"wrote {csv_path}")

    # Markdown summary
    out = []
    out.append("# Skipped / Near-Miss Opportunity Audit (PART 1)")
    out.append("")
    out.append(f"**Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    out.append(f"**Scope:** rejected_ideas (sampled {len(rejected_sample)}/{len(rejected)} last 14d) + C-tier ({len(c_tier)} signals last 14d).")
    out.append("**Source-of-truth:** read-only join of `rejected_ideas`, `proposed_signals`, OHLCV candles.")
    out.append("")
    out.append("## Headline")
    out.append("")
    out.append(f"- Records analyzed: **{len(rows_out)}**")
    out.append(f"- Skips that saved a likely loss (same symbol later A/B and lost): **{saved_losses}**")
    out.append(f"- Skips that missed a likely winner (same symbol later A/B+won OR price moved ≥ +1R proxy): **{missed_winners}**")
    out.append(f"- Net opportunity score: **{missed_winners - saved_losses:+d}** (positive = filter cost more than saved)")
    out.append("")
    out.append("## Top skip reasons (last 14d)")
    out.append("")
    out.append("| Reason | n |")
    out.append("|---|---:|")
    for reason, n in reason_counter.most_common(15):
        out.append(f"| {reason} | {n} |")
    out.append("")
    out.append("## Interpretation")
    out.append("")
    out.append("- The `move_*_pct` columns use **the last close before the decision time** as p0 and the high/low of the post-decision window. This is a **proxy**, not an exact replay.")
    out.append("- `reached_+0.5R_proxy` assumes risk = 1.5% (crypto) / 1% (stocks). If the move exceeded that, the price COULD have hit a typical TP1.")
    out.append("- `skip_saved_loss` is **conservative**: only counts when the same symbol later got A/B and that A/B turned into a real loss.")
    out.append("- `skip_missed_winner` triggers on either (a) same symbol later A/B and won, OR (b) price moved ≥ +1R proxy without ever becoming A/B (= filter missed a real move).")
    out.append("")
    out.append("## What this DOES NOT do")
    out.append("- Does not promote C-tier or rejected ideas to A/B.")
    out.append("- Does not reduce existing filters.")
    out.append("- Does not write to production tables.")
    out.append("- Does not send Telegram.")
    out.append("")
    out.append("## Read the full CSV")
    out.append("")
    out.append(f"`{csv_path.relative_to(ROOT)}`")
    out.append("")
    out.append("## Recommendation")
    out.append("")
    if missed_winners > 2 * saved_losses:
        out.append("- Missed winners materially outnumber saved losses — consider opening a deeper study on the top skip reasons before any filter relaxation.")
    elif saved_losses > missed_winners:
        out.append("- Filters are net-protective. NO relaxation recommended.")
    else:
        out.append("- Filters look roughly balanced. Monitor; revisit after 14 more days.")

    out_md = ROOT / "reports" / "SKIPPED_SIGNAL_OPPORTUNITY_AUDIT.md"
    out_md.write_text("\n".join(out), encoding="utf-8")
    print(f"wrote {out_md}")


if __name__ == "__main__":
    main()
