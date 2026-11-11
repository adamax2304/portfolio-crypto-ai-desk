"""Level A — Signal Execution Replay (read-only).

Replays historical signals against stored OHLCV candle tape and computes
raw R + playbook-aware sized R using `config/sizing_weights.yaml`.

NEVER writes to proposed_signals / signal_outcomes / signal_alerts /
watchlist_alerts. Outputs go only to reports/SIGNAL_EXECUTION_REPLAY_*.

Companion docs:
  reports/BACKTEST_FEASIBILITY_AUDIT.md
  reports/BACKTEST_METHODOLOGY_SPEC.md
"""

from __future__ import annotations

import argparse
import csv
import json
import sqlite3
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.signals.playbooks import label_for  # noqa: E402
from src.signals.sizing import size_decision  # noqa: E402

DB = ROOT / "db" / "crypto_ai_desk.sqlite"

# Fees / slippage defaults (per spec)
FEES_BPS = {
    "crypto": {"taker": 5.0, "maker": 2.0, "thin_extra": 10.0},  # bps per side
    "stocks": {"commission": 0.0, "slippage_bps": 2.0},
}


@dataclass
class ReplayResult:
    signal_id: str
    asset_class: str
    symbol: str
    playbook: str
    mode: str
    direction: str
    tier: str
    score: float
    created_at: str
    entry: float
    stop: float
    tp1: float
    tp2: float | None
    tp3: float | None
    original_outcome: str
    original_final_r: float | None
    replay_outcome: str
    replay_raw_r: float
    size_weight: float
    replay_sized_r: float
    fees_slippage_r_adjustment: float
    candle_timeframe_used: str
    data_coverage_quality: str
    ambiguous: bool
    notes: str = ""


def _load_signals(con: sqlite3.Connection, *, asset_class: str | None,
                  since: str | None, mode: str | None,
                  playbook_filter: str | None) -> list[dict]:
    cur = con.cursor()
    where = []
    params: list[Any] = []
    if asset_class and asset_class != "all":
        where.append("asset_class = ?")
        params.append(asset_class)
    if since:
        where.append("created_at >= ?")
        params.append(since)
    if mode:
        where.append("mode = ?")
        params.append(mode)
    sql = "SELECT * FROM proposed_signals"
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY created_at ASC"
    cur.execute(sql, params)
    cols = [d[0] for d in cur.description]
    rows = [dict(zip(cols, r)) for r in cur.fetchall()]
    # latest outcome per signal
    cur.execute("""
        SELECT signal_id, final_outcome, final_r FROM signal_outcomes
        WHERE id IN (SELECT MAX(id) FROM signal_outcomes GROUP BY signal_id)
    """)
    outcomes = {r[0]: {"final_outcome": r[1], "final_r": r[2]} for r in cur.fetchall()}
    for s in rows:
        s["_outcome"] = outcomes.get(s["signal_id"], {})
    # optional playbook filter (after labeling)
    if playbook_filter:
        out = []
        for s in rows:
            try:
                pl = label_for(s).playbook
            except Exception:
                pl = ""
            if pl == playbook_filter:
                out.append(s)
        rows = out
    return rows


def _candle_paths(signal: dict, *, tf: str) -> list[Path]:
    """Return ordered list of candidate OHLCV CSV paths for this signal."""
    asset = signal.get("asset_class", "crypto")
    sym = signal.get("symbol", "")
    if asset == "stocks":
        return [ROOT / "data" / "raw" / "stocks" / tf / f"{sym}.csv"]
    # crypto: try primary_exchange then other venues
    primary = (signal.get("primary_exchange") or signal.get("exchange_focus") or "binance").lower()
    base = sym.replace("/USDT", "_USDT").replace("/", "_")
    out = []
    venues = [primary] + [v for v in ("binance", "bybit", "mexc") if v != primary]
    for v in venues:
        out.append(ROOT / "data" / "raw" / "ohlcv" / v / tf / f"{base}.csv")
    return out


def _load_candles(signal: dict, *, preferences: list[str]) -> tuple[pd.DataFrame | None, str, list[str]]:
    """Try each TF in preference order. Return (df, tf_used, tried_paths)."""
    tried = []
    for tf in preferences:
        for p in _candle_paths(signal, tf=tf):
            tried.append(str(p.relative_to(ROOT)))
            if p.exists():
                try:
                    df = pd.read_csv(p)
                    # Normalize timestamp column (stocks csv uses 'Datetime')
                    if "timestamp" not in df.columns:
                        for c in ("Datetime", "datetime", "date", "Date"):
                            if c in df.columns:
                                df = df.rename(columns={c: "timestamp"})
                                break
                    if "timestamp" not in df.columns:
                        continue
                    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
                    df = df.sort_values("timestamp").reset_index(drop=True)
                    return df, tf, tried
                except Exception:
                    continue
    return None, "", tried


def _direction_sign(direction: str) -> int:
    return 1 if direction.lower() == "long" else -1


def _simulate(signal: dict, df: pd.DataFrame, *, tf: str,
              conservative: bool, include_fees: bool,
              include_slippage: bool) -> dict:
    """Walk candles forward from created_at. Determine fill + exit.

    Returns dict with: outcome, raw_r, fees_r, ambiguous, notes,
    entry_used, coverage_quality.
    """
    created_at = pd.to_datetime(signal["created_at"], utc=True)
    direction = signal["direction"].lower()
    sign = _direction_sign(direction)
    entry_low = float(signal.get("entry_low") or 0)
    entry_high = float(signal.get("entry_high") or 0)
    entry_trigger = float(signal.get("entry_trigger") or 0)
    entry_type = (signal.get("entry_type") or "zone").lower()
    stop = float(signal.get("stop_loss") or signal.get("invalidation") or 0)
    invalid = float(signal.get("invalidation") or stop)
    tp1 = float(signal.get("tp1") or 0)
    tp2 = signal.get("tp2")
    tp3 = signal.get("tp3")
    risk_per_unit = abs(float(signal.get("risk_per_unit") or 0)) or None
    validity_hours = float(signal.get("validity_window_hours") or 24.0)
    expires_at = created_at + pd.Timedelta(hours=validity_hours)

    # restrict to candles strictly after created_at
    after = df[df["timestamp"] > created_at].copy()
    if after.empty:
        return {
            "outcome": "no_candles_after_creation",
            "raw_r": None, "fees_r": 0.0, "ambiguous": False,
            "entry_used": None, "coverage_quality": "low",
            "notes": "candle archive does not cover post-creation window",
        }

    # Coverage quality
    last_candle_time = after["timestamp"].iloc[-1]
    if last_candle_time < expires_at:
        coverage_quality = "medium"
    else:
        coverage_quality = "high"
    if tf in ("1h", "1d"):
        # 1h/1d cannot adjudicate intrabar reliably
        coverage_quality = "medium" if coverage_quality == "high" else coverage_quality

    # ---------------- Entry phase --------------------------------------
    entry_idx = None
    entry_price = None
    pre_entry_status = "pending"
    notes_bits: list[str] = []

    # Stale / moved-away check: if price drifts past invalidation BEFORE entry,
    # mark moved_away
    for i, row in after.iterrows():
        low = float(row["low"])
        high = float(row["high"])
        # entry detection
        if entry_type == "trigger" and entry_trigger > 0:
            if direction == "long" and high >= entry_trigger >= low:
                entry_idx = i
                entry_price = max(entry_trigger, low)
                break
            if direction == "short" and high >= entry_trigger >= low:
                entry_idx = i
                entry_price = min(entry_trigger, high)
                break
        else:
            # zone fill — touch the zone in our direction
            zlo = min(entry_low, entry_high) if entry_low and entry_high else (entry_low or entry_high)
            zhi = max(entry_low, entry_high) if entry_low and entry_high else (entry_low or entry_high)
            if zlo and zhi and high >= zlo and low <= zhi:
                # For longs, the zone-low (or low edge) is preferred fill;
                # for shorts, the zone-high.
                if direction == "long":
                    entry_price = max(zlo, low)
                else:
                    entry_price = min(zhi, high)
                entry_idx = i
                break
        # invalidation-before-entry
        if invalid:
            if direction == "long" and low <= invalid:
                pre_entry_status = "entry_moved_away"
                break
            if direction == "short" and high >= invalid:
                pre_entry_status = "entry_moved_away"
                break
        # stale window
        if row["timestamp"] >= expires_at:
            pre_entry_status = "stale_before_entry"
            break

    if entry_idx is None:
        return {
            "outcome": pre_entry_status if pre_entry_status != "pending" else "no_entry_in_window",
            "raw_r": 0.0, "fees_r": 0.0, "ambiguous": False,
            "entry_used": None, "coverage_quality": coverage_quality,
            "notes": f"never filled before {pre_entry_status}; tf={tf}",
        }

    # Compute risk_per_unit if missing
    if not risk_per_unit:
        risk_per_unit = abs(entry_price - stop)
        if risk_per_unit == 0:
            return {
                "outcome": "zero_risk",
                "raw_r": None, "fees_r": 0.0, "ambiguous": False,
                "entry_used": entry_price, "coverage_quality": "low",
                "notes": "stop==entry; cannot compute R",
            }

    # ---------------- Post-entry phase ---------------------------------
    post = after.loc[entry_idx + 1:] if entry_idx + 1 in after.index else pd.DataFrame()
    if post.empty:
        # Same-candle entry; check if TP/stop also hit in same candle
        post = after.loc[[entry_idx]]

    target_r = 1.0  # TP1 is +1R by construction (entry+risk*1)
    # We compute exit R generically from final exit price
    exit_price = None
    exit_reason = "open"
    ambiguous = False

    for i, row in post.iterrows():
        low = float(row["low"])
        high = float(row["high"])
        # Did TP1 hit?
        tp1_hit = (direction == "long" and high >= tp1) or (direction == "short" and low <= tp1)
        stop_hit = (direction == "long" and low <= stop) or (direction == "short" and high >= stop)
        if tp1_hit and stop_hit:
            ambiguous = True
            # try to disambiguate by checking finer TF if available — caller didn't pass one,
            # so apply policy
            if conservative:
                exit_reason = "stop_ambiguous"
                exit_price = stop
            else:
                exit_reason = "tp1_ambiguous"
                exit_price = tp1
            break
        if stop_hit:
            exit_reason = "stop"
            exit_price = stop
            break
        if tp1_hit:
            exit_reason = "tp1"
            exit_price = tp1
            break
        if row["timestamp"] >= expires_at:
            exit_reason = "expired"
            exit_price = float(row["close"])
            break

    if exit_reason == "open":
        # No event in window
        exit_reason = "open_no_event"
        exit_price = float(post["close"].iloc[-1])

    raw_r = sign * (exit_price - entry_price) / risk_per_unit

    # ---------------- Fees / slippage ---------------------------------
    fees_r = 0.0
    if include_fees or include_slippage:
        asset = signal.get("asset_class", "crypto")
        if asset == "crypto":
            cfg = FEES_BPS["crypto"]
            bps_round_trip = (cfg["taker"] * 2) if include_fees else 0.0
            slip_bps = 5.0 if include_slippage else 0.0  # 0.05% per side ~ 10bps RT
            if (signal.get("primary_exchange") or "").lower() == "mexc" or \
               (signal.get("data_confidence") or "") == "low":
                bps_round_trip += cfg["thin_extra"]
            # Convert bps cost to R: cost_per_unit_price = entry_price * bps/10000
            cost = entry_price * (bps_round_trip + slip_bps) / 10000.0
            fees_r = -cost / risk_per_unit
        else:
            slip = 0.02 if include_slippage else 0.0  # $0.02 round-trip on 15m fills
            fees_r = -slip / risk_per_unit

    notes_bits.append(f"exit={exit_reason}; tf={tf}")
    if ambiguous:
        notes_bits.append("same-candle TP/stop ambiguity")
    return {
        "outcome": exit_reason,
        "raw_r": float(raw_r),
        "fees_r": float(fees_r),
        "ambiguous": ambiguous,
        "entry_used": float(entry_price),
        "coverage_quality": coverage_quality,
        "notes": "; ".join(notes_bits),
    }


def replay_one(signal: dict, *, preferences: list[str], conservative: bool,
               include_fees: bool, include_slippage: bool) -> ReplayResult:
    df, tf_used, tried = _load_candles(signal, preferences=preferences)
    pl = label_for(signal)
    playbook = pl.playbook
    if df is None:
        # No candles at all — fall back to recorded outcome only
        sized = size_decision({**signal, "final_r": signal.get("_outcome", {}).get("final_r")})
        return ReplayResult(
            signal_id=signal["signal_id"], asset_class=signal["asset_class"],
            symbol=signal["symbol"], playbook=playbook,
            mode=signal["mode"] or "", direction=signal["direction"],
            tier=signal["tier"] or "", score=float(signal.get("score") or 0),
            created_at=signal["created_at"],
            entry=float(signal.get("entry_trigger") or signal.get("entry_low") or 0),
            stop=float(signal.get("stop_loss") or 0),
            tp1=float(signal.get("tp1") or 0),
            tp2=signal.get("tp2"), tp3=signal.get("tp3"),
            original_outcome=signal.get("_outcome", {}).get("final_outcome") or "",
            original_final_r=signal.get("_outcome", {}).get("final_r"),
            replay_outcome="no_candles",
            replay_raw_r=signal.get("_outcome", {}).get("final_r") or 0.0,
            size_weight=sized.weight,
            replay_sized_r=(sized.sized_r if sized.sized_r is not None else 0.0),
            fees_slippage_r_adjustment=0.0,
            candle_timeframe_used="",
            data_coverage_quality="low",
            ambiguous=False,
            notes=f"no candle file found; tried {len(tried)} paths; fallback to recorded outcome",
        )

    res = _simulate(signal, df, tf=tf_used,
                    conservative=conservative,
                    include_fees=include_fees,
                    include_slippage=include_slippage)
    raw_r = res.get("raw_r")
    if raw_r is None:
        raw_r = signal.get("_outcome", {}).get("final_r") or 0.0
    fees_r = res.get("fees_r", 0.0)
    sized = size_decision({**signal, "final_r": raw_r + fees_r})
    return ReplayResult(
        signal_id=signal["signal_id"], asset_class=signal["asset_class"],
        symbol=signal["symbol"], playbook=playbook,
        mode=signal["mode"] or "", direction=signal["direction"],
        tier=signal["tier"] or "", score=float(signal.get("score") or 0),
        created_at=signal["created_at"],
        entry=float(res.get("entry_used") or signal.get("entry_trigger") or signal.get("entry_low") or 0),
        stop=float(signal.get("stop_loss") or 0),
        tp1=float(signal.get("tp1") or 0),
        tp2=signal.get("tp2"), tp3=signal.get("tp3"),
        original_outcome=signal.get("_outcome", {}).get("final_outcome") or "",
        original_final_r=signal.get("_outcome", {}).get("final_r"),
        replay_outcome=res["outcome"],
        replay_raw_r=float(raw_r),
        size_weight=sized.weight,
        replay_sized_r=(sized.sized_r if sized.sized_r is not None else 0.0),
        fees_slippage_r_adjustment=float(fees_r),
        candle_timeframe_used=tf_used,
        data_coverage_quality=res["coverage_quality"],
        ambiguous=res["ambiguous"],
        notes=res["notes"],
    )


def write_csv(results: list[ReplayResult], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(ReplayResult.__dataclass_fields__.keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in results:
            w.writerow({k: getattr(r, k) for k in fieldnames})


def summarize(results: list[ReplayResult], *, output_path: Path,
              include_fees: bool, include_slippage: bool) -> None:
    by_class = Counter([r.asset_class for r in results])
    by_outcome = Counter([r.replay_outcome for r in results])
    by_coverage = Counter([r.data_coverage_quality for r in results])
    n_ambiguous = sum(1 for r in results if r.ambiguous)
    total_raw = sum(r.replay_raw_r for r in results)
    total_sized = sum(r.replay_sized_r for r in results)
    total_fees = sum(r.fees_slippage_r_adjustment for r in results)
    wins = sum(1 for r in results if r.replay_raw_r > 0)
    losses = sum(1 for r in results if r.replay_raw_r < 0)
    wr = (wins / (wins + losses)) if (wins + losses) else 0.0
    pf = (sum(r.replay_raw_r for r in results if r.replay_raw_r > 0) /
          abs(sum(r.replay_raw_r for r in results if r.replay_raw_r < 0))) \
        if any(r.replay_raw_r < 0 for r in results) else float("inf")
    # By playbook
    by_pl: dict[str, list[ReplayResult]] = {}
    for r in results:
        by_pl.setdefault(r.playbook, []).append(r)

    lines = []
    lines.append("# Signal Execution Replay — Summary")
    lines.append("")
    lines.append(f"**Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append(f"**Total replayed:** {len(results)}")
    lines.append(f"**Fees included:** {include_fees} · **Slippage included:** {include_slippage}")
    lines.append("")
    lines.append("## Headline")
    lines.append("")
    lines.append(f"- Raw R (sum): **{total_raw:+.2f}**")
    lines.append(f"- Sized R (sum, playbook-aware): **{total_sized:+.2f}**")
    lines.append(f"- Fees/slippage R adjustment (sum): **{total_fees:+.2f}**")
    lines.append(f"- Wins / Losses: {wins} / {losses}  ·  WR = {wr:.1%}  ·  PF = {pf:.2f}")
    lines.append(f"- Same-candle ambiguous: {n_ambiguous} ({(n_ambiguous/len(results) if results else 0):.1%})")
    lines.append("")
    lines.append("## Coverage quality")
    for k, n in by_coverage.most_common():
        lines.append(f"- {k}: {n}")
    lines.append("")
    lines.append("## Replay outcome distribution")
    for k, n in by_outcome.most_common():
        lines.append(f"- {k}: {n}")
    lines.append("")
    lines.append("## By asset class")
    for k, n in by_class.most_common():
        sub = [r for r in results if r.asset_class == k]
        sub_raw = sum(r.replay_raw_r for r in sub)
        sub_sized = sum(r.replay_sized_r for r in sub)
        lines.append(f"- **{k}** — n={n}, raw R={sub_raw:+.2f}, sized R={sub_sized:+.2f}")
    lines.append("")
    lines.append("## By playbook")
    lines.append("| Playbook | n | raw R | sized R | WR |")
    lines.append("|---|---:|---:|---:|---:|")
    for pl, rows in sorted(by_pl.items(), key=lambda kv: -sum(r.replay_sized_r for r in kv[1])):
        wr_pl = sum(1 for r in rows if r.replay_raw_r > 0) / max(1, sum(1 for r in rows if r.replay_raw_r != 0))
        lines.append(f"| {pl} | {len(rows)} | {sum(r.replay_raw_r for r in rows):+.2f} | "
                     f"{sum(r.replay_sized_r for r in rows):+.2f} | {wr_pl:.0%} |")
    lines.append("")
    lines.append("## Cross-check vs original tracker")
    diffs = []
    for r in results:
        if r.original_final_r is not None:
            try:
                d = float(r.replay_raw_r) - float(r.original_final_r)
                diffs.append(abs(d))
            except Exception:
                pass
    if diffs:
        lines.append(f"- Replay-vs-tracker mean |Δraw R| = {sum(diffs)/len(diffs):.3f} ({len(diffs)} compared)")
    lines.append("")
    lines.append("## Notes")
    lines.append("- Replay uses **no look-ahead**: candles are processed strictly forward from `created_at`.")
    lines.append("- Same-candle TP-vs-stop events on lower-resolution timeframes are marked **ambiguous** "
                 "and resolved by policy (conservative=stop first).")
    lines.append("- All outputs are write-only into reports/. `proposed_signals`, `signal_outcomes`, "
                 "`signal_alerts`, `watchlist_alerts` are NOT touched.")
    output_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--asset-class", choices=["crypto", "stocks", "all"], default="all")
    ap.add_argument("--since", default=None, help="YYYY-MM-DD (ISO date, optional)")
    ap.add_argument("--mode", default=None)
    ap.add_argument("--playbook", default=None)
    ap.add_argument("--timeframe-preference", default="1m,5m,15m,1h,1d",
                    help="comma-separated order; first existing one used")
    ap.add_argument("--use-1m-if-available", action="store_true",
                    help="alias for putting 1m first in preference")
    ap.add_argument("--conservative-intrabar-policy", action="store_true", default=True,
                    help="default; same-candle TP+stop → stop hit first")
    ap.add_argument("--include-fees", action="store_true")
    ap.add_argument("--include-slippage", action="store_true")
    ap.add_argument("--output-prefix", default="SIGNAL_EXECUTION_REPLAY")
    args = ap.parse_args()

    prefs = [t.strip() for t in args.timeframe_preference.split(",") if t.strip()]
    if args.use_1m_if_available and "1m" in prefs:
        prefs = ["1m"] + [t for t in prefs if t != "1m"]

    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    signals = _load_signals(con, asset_class=args.asset_class,
                            since=args.since, mode=args.mode,
                            playbook_filter=args.playbook)
    print(f"loaded {len(signals)} signals")
    results: list[ReplayResult] = []
    for i, s in enumerate(signals):
        try:
            r = replay_one(s, preferences=prefs,
                           conservative=args.conservative_intrabar_policy,
                           include_fees=args.include_fees,
                           include_slippage=args.include_slippage)
        except Exception as e:
            r = ReplayResult(
                signal_id=s.get("signal_id", "?"),
                asset_class=s.get("asset_class", "?"),
                symbol=s.get("symbol", "?"),
                playbook="", mode=s.get("mode") or "",
                direction=s.get("direction") or "",
                tier=s.get("tier") or "",
                score=float(s.get("score") or 0),
                created_at=s.get("created_at") or "",
                entry=0, stop=0, tp1=0, tp2=None, tp3=None,
                original_outcome=s.get("_outcome", {}).get("final_outcome") or "",
                original_final_r=s.get("_outcome", {}).get("final_r"),
                replay_outcome="error", replay_raw_r=0.0,
                size_weight=0.0, replay_sized_r=0.0,
                fees_slippage_r_adjustment=0.0,
                candle_timeframe_used="", data_coverage_quality="low",
                ambiguous=False, notes=f"error: {e}",
            )
        results.append(r)
        if (i + 1) % 100 == 0:
            print(f"  ... {i+1}/{len(signals)}")

    out_csv = ROOT / "reports" / f"{args.output_prefix}_RESULTS.csv"
    out_md = ROOT / "reports" / f"{args.output_prefix}_SUMMARY.md"
    write_csv(results, out_csv)
    summarize(results, output_path=out_md,
              include_fees=args.include_fees,
              include_slippage=args.include_slippage)
    print(f"wrote {out_csv}")
    print(f"wrote {out_md}")


if __name__ == "__main__":
    main()
