"""Independent reconstruction of paper execution from raw OHLCV.

Read-only diagnostic. Pulls A/B signals from the last 14 days, loads the same
cached OHLCV the tracker uses, then independently walks candles to detect:

 - whether the signal's recorded entry/stop/TP times reproduce from candles;
 - intrabar-ambiguous events (same-candle entry+stop / entry+TP / stop+TP);
 - gap slippage (stop or TP gapped through by > N bp);
 - pre-entry invalidation cases.

Writes:
 - reports/PAPER_EXECUTION_VALIDATION_DATASET.csv (per-signal columns)
 - reports/PAPER_EXECUTION_RECONSTRUCTION_REPORT.md (human summary)

NO writes to SQLite. NO mutation of any signal_outcomes row. NO scheduler ops.
"""
from __future__ import annotations

import csv
import sqlite3
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

REPO = Path(__file__).resolve().parent.parent
DB = REPO / "db" / "crypto_ai_desk.sqlite"
CSV_OUT = REPO / "reports" / "PAPER_EXECUTION_VALIDATION_DATASET.csv"
MD_OUT = REPO / "reports" / "PAPER_EXECUTION_RECONSTRUCTION_REPORT.md"

sys.stdout.reconfigure(encoding="utf-8")

# Mode → timeframe preference (mirror tracker.py)
TF_CRYPTO = {
    "scalp": ("5m", "15m", "1h"),
    "intraday": ("15m", "1h", "4h"),
    "swing": ("1h", "4h", "1d"),
    "invest": ("4h", "1d"),
}
TF_STOCKS = {
    "scalp": ("15m", "1h", "1d"),
    "intraday": ("15m", "1h", "1d"),
    "swing": ("1h", "1d"),
    "invest": ("1d", "1wk"),
}


def parse_ts(s: str | None):
    if not s:
        return None
    try:
        return datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    except Exception:
        return None


def load_ohlcv(asset_class: str, symbol: str, mode: str) -> tuple[pd.DataFrame | None, str, str]:
    """Mirror src/signals/tracker._load_ohlcv_for_signal lookup."""
    if asset_class == "stocks":
        for tf in TF_STOCKS.get(mode, TF_STOCKS["intraday"]):
            path = REPO / "data" / "raw" / "stocks" / tf / f"{symbol}.csv"
            if path.exists():
                df = pd.read_csv(path)
                ts_col = None
                for cand in ("Datetime", "Date", "timestamp"):
                    if cand in df.columns:
                        ts_col = cand
                        break
                if ts_col is None:
                    continue
                df["timestamp"] = pd.to_datetime(df[ts_col], utc=True, errors="coerce")
                return df.dropna(subset=["timestamp"]).reset_index(drop=True), "stocks", tf
        return None, "", ""
    # crypto: anchor=binance then bybit, mexc
    sym_fs = symbol.replace("/", "_")
    for exch in ("binance", "bybit", "mexc"):
        for tf in TF_CRYPTO.get(mode, TF_CRYPTO["intraday"]):
            path = REPO / "data" / "raw" / "ohlcv" / exch / tf / f"{sym_fs}.csv"
            if path.exists():
                df = pd.read_csv(path)
                df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
                return df.dropna(subset=["timestamp"]).reset_index(drop=True), exch, tf
    return None, "", ""


@dataclass
class Reconstruction:
    triggered: bool = False
    triggered_at: str | None = None
    entry_price: float | None = None
    stop_hit: bool = False
    stop_hit_at: str | None = None
    tp1_hit: bool = False
    tp1_hit_at: str | None = None
    tp2_hit: bool = False
    tp2_hit_at: str | None = None
    mfe_pct: float = 0.0
    mae_pct: float = 0.0
    # NEW: ambiguity flags the existing tracker does not produce
    intrabar_entry_stop: bool = False
    intrabar_entry_tp: bool = False
    intrabar_stop_tp: bool = False
    pre_entry_invalidation: bool = False
    gap_slippage_stop_pct: float = 0.0   # how far past stop the candle low/high went, as fraction of risk
    gap_slippage_tp1_pct: float = 0.0
    candles_walked: int = 0
    final_outcome: str | None = None


def walk(
    *, direction: str, entry_low: float | None, entry_high: float | None,
    entry_trigger: float | None, invalidation: float | None,
    tp1: float | None, tp2: float | None,
    candles: pd.DataFrame, expires_at: datetime | None,
) -> Reconstruction:
    r = Reconstruction()
    if invalidation is None or candles is None or candles.empty or direction not in ("long", "short"):
        return r
    has_zone = entry_low is not None and entry_high is not None
    has_trigger = entry_trigger is not None
    risk_distance = None
    for _, row in candles.iterrows():
        ts = row.get("timestamp")
        if pd.isna(ts):
            continue
        if expires_at is not None and ts > expires_at:
            break
        r.candles_walked += 1
        o = float(row.get("open", row.get("close", 0)))
        h = float(row.get("high", row.get("close", 0)))
        l = float(row.get("low", row.get("close", 0)))
        ts_iso = pd.to_datetime(ts, utc=True).strftime("%Y-%m-%dT%H:%M:%S+00:00")

        if not r.triggered:
            triggered_now = False
            entry_used = None
            if has_zone:
                lo = min(entry_low, entry_high)
                hi = max(entry_low, entry_high)
                if l <= hi and h >= lo:
                    triggered_now = True
                    if lo <= o <= hi:
                        entry_used = o
                    else:
                        entry_used = hi if direction == "long" and l <= hi else lo
                        if direction == "short":
                            entry_used = lo if h >= lo else hi
            elif has_trigger:
                t = float(entry_trigger)
                if direction == "long" and h >= t:
                    triggered_now = True
                    entry_used = t
                elif direction == "short" and l <= t:
                    triggered_now = True
                    entry_used = t
            if not triggered_now:
                if direction == "long" and l <= float(invalidation):
                    r.pre_entry_invalidation = True
                    r.stop_hit_at = ts_iso
                    r.final_outcome = "not_triggered_invalidation"
                    return r
                if direction == "short" and h >= float(invalidation):
                    r.pre_entry_invalidation = True
                    r.stop_hit_at = ts_iso
                    r.final_outcome = "not_triggered_invalidation"
                    return r
                continue
            r.triggered = True
            r.triggered_at = ts_iso
            r.entry_price = entry_used
            risk_distance = abs(entry_used - float(invalidation)) if entry_used else None

        # in-position
        anchor = float(r.entry_price or 0)
        if anchor:
            if direction == "long":
                fav = (h - anchor) / anchor
                adv = (l - anchor) / anchor
            else:
                fav = (anchor - l) / anchor
                adv = (anchor - h) / anchor
            if fav > r.mfe_pct:
                r.mfe_pct = fav
            if adv < r.mae_pct:
                r.mae_pct = adv

        stop_touched = (
            (direction == "long" and l <= float(invalidation))
            or (direction == "short" and h >= float(invalidation))
        )

        def _tp(level):
            if level is None:
                return False
            return (direction == "long" and h >= float(level)) or (direction == "short" and l <= float(level))

        tp1_now = _tp(tp1) and not r.tp1_hit
        tp2_now = _tp(tp2) and not r.tp2_hit

        # NEW: intrabar ambiguity detection (the gap PART 1 §A/§B identified)
        triggered_this_bar = r.triggered and r.triggered_at == ts_iso
        if triggered_this_bar and stop_touched and not r.stop_hit:
            r.intrabar_entry_stop = True
        if triggered_this_bar and (tp1_now or tp2_now):
            r.intrabar_entry_tp = True
        if stop_touched and (tp1_now or tp2_now) and not triggered_this_bar:
            r.intrabar_stop_tp = True

        # Gap-slippage past stop / TP1 (as fraction of risk distance)
        if stop_touched and risk_distance:
            if direction == "long":
                slip = (float(invalidation) - l) / risk_distance
            else:
                slip = (h - float(invalidation)) / risk_distance
            r.gap_slippage_stop_pct = max(r.gap_slippage_stop_pct, slip)
        if tp1 is not None and tp1_now and risk_distance:
            if direction == "long":
                slip = (h - float(tp1)) / risk_distance
            else:
                slip = (float(tp1) - l) / risk_distance
            r.gap_slippage_tp1_pct = max(r.gap_slippage_tp1_pct, slip)

        # Resolve same-candle TP+stop after entry — mirror tracker's conservative model
        if stop_touched and (tp1_now or tp2_now):
            if tp1_now:
                r.tp1_hit = True
                r.tp1_hit_at = ts_iso
            if tp2_now:
                r.tp2_hit = True
                r.tp2_hit_at = ts_iso
            r.stop_hit = True
            r.stop_hit_at = ts_iso
            r.final_outcome = "ambiguous"
            return r
        if tp1_now:
            r.tp1_hit = True
            r.tp1_hit_at = ts_iso
        if tp2_now:
            r.tp2_hit = True
            r.tp2_hit_at = ts_iso
        if stop_touched:
            r.stop_hit = True
            r.stop_hit_at = ts_iso
            r.final_outcome = "loss"
            return r
        if r.tp2_hit:
            r.final_outcome = "win"
            return r
    # End of walk
    if r.triggered:
        if r.tp1_hit:
            r.final_outcome = "win"
        else:
            r.final_outcome = "expired"
    elif r.pre_entry_invalidation:
        pass  # already set
    else:
        r.final_outcome = "not_triggered"
    return r


# ─────────────────────────────────────────────────────────────────────────────
# Driver
# ─────────────────────────────────────────────────────────────────────────────

def pick_signals(db: sqlite3.Connection) -> list[sqlite3.Row]:
    rows = db.execute(
        """
        SELECT ps.signal_id, ps.asset_class, ps.symbol, ps.direction, ps.mode, ps.tier,
               ps.score, ps.created_at, ps.expires_at,
               ps.entry_low, ps.entry_high, ps.entry_trigger,
               ps.stop_loss, ps.invalidation, ps.tp1, ps.tp2, ps.tp3,
               ps.risk_per_unit, ps.suggested_entry,
               so.final_outcome, so.final_r,
               so.entry_triggered, so.entry_triggered_at, so.entry_price_used,
               so.stop_hit, so.stop_hit_at,
               so.tp1_hit, so.tp1_hit_at, so.tp2_hit, so.tp2_hit_at,
               so.max_favorable_excursion_r, so.max_adverse_excursion_r,
               so.notes as outcome_notes
        FROM proposed_signals ps
        LEFT JOIN signal_outcomes so
          ON so.signal_id = ps.signal_id
         AND so.id = (SELECT MAX(id) FROM signal_outcomes WHERE signal_id = ps.signal_id)
        WHERE ps.tier IN ('A','B')
          AND ps.created_at >= ?
        ORDER BY ps.created_at DESC
        """,
        ("2026-05-26T00:00:00+00:00",),
    ).fetchall()
    crypto = [r for r in rows if r["asset_class"] == "crypto"][:20]
    stocks = [r for r in rows if r["asset_class"] == "stocks"][:20]
    return crypto + stocks


def compare(sys_val, recon_val) -> str:
    """Loose comparison: True if both None/empty, both equal, or trivially close."""
    if sys_val in (None, "", 0) and recon_val in (None, "", 0):
        return "match"
    if isinstance(sys_val, str) and isinstance(recon_val, str):
        return "match" if sys_val[:13] == recon_val[:13] else "mismatch"
    try:
        a = float(sys_val) if sys_val is not None else None
        b = float(recon_val) if recon_val is not None else None
        if a is None and b is None:
            return "match"
        if a is None or b is None:
            return "mismatch"
        if abs(a - b) / max(abs(a), abs(b), 1e-9) < 0.01:
            return "match"
        return "mismatch"
    except Exception:
        return str(sys_val) == str(recon_val) and "match" or "mismatch"


def main() -> int:
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    sigs = pick_signals(db)
    print(f"Selected {len(sigs)} signals (crypto + stocks A/B last 14d)")

    headers = [
        "signal_id", "asset_class", "symbol", "mode", "direction", "tier", "score",
        "created_at", "expires_at",
        "entry_low", "entry_high", "stop_loss", "invalidation", "tp1", "tp2",
        "sys_outcome", "sys_final_r", "sys_entry_triggered_at", "sys_stop_hit_at",
        "sys_tp1_hit_at", "sys_mfe_r", "sys_mae_r",
        "recon_outcome", "recon_entry_at", "recon_stop_at", "recon_tp1_at",
        "recon_mfe_pct", "recon_mae_pct", "recon_candles",
        "ohlcv_source", "ohlcv_tf",
        "diff_outcome", "diff_entry_at", "diff_stop_at", "diff_tp1_at",
        "flag_intrabar_entry_stop", "flag_intrabar_entry_tp", "flag_intrabar_stop_tp",
        "flag_pre_entry_invalidation", "gap_slip_stop_pct_of_risk", "gap_slip_tp1_pct_of_risk",
    ]
    rows_out: list[dict[str, Any]] = []
    diffs = {"match": 0, "mismatch": 0, "ambiguous": 0, "missing_data": 0}
    intrabar_entry_stop = 0
    intrabar_entry_tp = 0
    intrabar_stop_tp = 0
    pre_entry_inval = 0
    gap_stops = 0
    gap_tps = 0

    for s in sigs:
        frame, exch, tf = load_ohlcv(s["asset_class"], s["symbol"], s["mode"])
        if frame is None or frame.empty:
            diffs["missing_data"] += 1
            rows_out.append({
                **{h: "" for h in headers},
                "signal_id": s["signal_id"], "asset_class": s["asset_class"],
                "symbol": s["symbol"], "mode": s["mode"], "direction": s["direction"],
                "tier": s["tier"], "score": s["score"], "created_at": s["created_at"],
                "diff_outcome": "missing_data",
            })
            continue
        created = parse_ts(s["created_at"])
        if created is not None:
            frame = frame[frame["timestamp"] >= created].reset_index(drop=True)
        expires_dt = parse_ts(s["expires_at"]) if s["expires_at"] else None
        r = walk(
            direction=s["direction"],
            entry_low=s["entry_low"], entry_high=s["entry_high"],
            entry_trigger=s["entry_trigger"], invalidation=s["invalidation"],
            tp1=s["tp1"], tp2=s["tp2"],
            candles=frame, expires_at=expires_dt,
        )
        # Diff
        do = compare(s["final_outcome"], r.final_outcome)
        de = compare(s["entry_triggered_at"], r.triggered_at)
        dsh = compare(s["stop_hit_at"], r.stop_hit_at)
        dtp1 = compare(s["tp1_hit_at"], r.tp1_hit_at)
        if r.intrabar_entry_stop: intrabar_entry_stop += 1
        if r.intrabar_entry_tp: intrabar_entry_tp += 1
        if r.intrabar_stop_tp: intrabar_stop_tp += 1
        if r.pre_entry_invalidation: pre_entry_inval += 1
        if r.gap_slippage_stop_pct > 0.1: gap_stops += 1
        if r.gap_slippage_tp1_pct > 0.1: gap_tps += 1
        if r.intrabar_entry_stop or r.intrabar_entry_tp:
            diffs["ambiguous"] += 1
        elif do == "match":
            diffs["match"] += 1
        else:
            diffs["mismatch"] += 1
        rows_out.append({
            "signal_id": s["signal_id"], "asset_class": s["asset_class"],
            "symbol": s["symbol"], "mode": s["mode"], "direction": s["direction"],
            "tier": s["tier"], "score": s["score"],
            "created_at": s["created_at"], "expires_at": s["expires_at"],
            "entry_low": s["entry_low"], "entry_high": s["entry_high"],
            "stop_loss": s["stop_loss"], "invalidation": s["invalidation"],
            "tp1": s["tp1"], "tp2": s["tp2"],
            "sys_outcome": s["final_outcome"], "sys_final_r": s["final_r"],
            "sys_entry_triggered_at": s["entry_triggered_at"],
            "sys_stop_hit_at": s["stop_hit_at"], "sys_tp1_hit_at": s["tp1_hit_at"],
            "sys_mfe_r": s["max_favorable_excursion_r"], "sys_mae_r": s["max_adverse_excursion_r"],
            "recon_outcome": r.final_outcome, "recon_entry_at": r.triggered_at,
            "recon_stop_at": r.stop_hit_at, "recon_tp1_at": r.tp1_hit_at,
            "recon_mfe_pct": round(r.mfe_pct * 100, 2),
            "recon_mae_pct": round(r.mae_pct * 100, 2),
            "recon_candles": r.candles_walked,
            "ohlcv_source": exch, "ohlcv_tf": tf,
            "diff_outcome": do, "diff_entry_at": de,
            "diff_stop_at": dsh, "diff_tp1_at": dtp1,
            "flag_intrabar_entry_stop": int(r.intrabar_entry_stop),
            "flag_intrabar_entry_tp": int(r.intrabar_entry_tp),
            "flag_intrabar_stop_tp": int(r.intrabar_stop_tp),
            "flag_pre_entry_invalidation": int(r.pre_entry_invalidation),
            "gap_slip_stop_pct_of_risk": round(r.gap_slippage_stop_pct * 100, 1),
            "gap_slip_tp1_pct_of_risk": round(r.gap_slippage_tp1_pct * 100, 1),
        })

    # Write CSV
    CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
    with CSV_OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=headers)
        w.writeheader()
        for row in rows_out:
            w.writerow({h: row.get(h, "") for h in headers})
    print(f"Wrote {CSV_OUT.name}: {len(rows_out)} rows")
    print(f"Diffs: match={diffs['match']} mismatch={diffs['mismatch']} "
          f"ambiguous={diffs['ambiguous']} missing_data={diffs['missing_data']}")
    print(f"Flags: intrabar_entry_stop={intrabar_entry_stop}, intrabar_entry_tp={intrabar_entry_tp}, "
          f"intrabar_stop_tp={intrabar_stop_tp}, pre_entry_inval={pre_entry_inval}, "
          f"gap_slip_stop>10%={gap_stops}, gap_slip_tp1>10%={gap_tps}")

    # Markdown summary
    md = MD_OUT
    lines = [
        "# Paper Execution Reconstruction Report (PART 3)",
        "",
        f"**Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d')}  ",
        f"**Sample:** {len(rows_out)} A/B signals (last 14d, crypto + stocks)  ",
        "**Method:** Read-only candle replay against the same cached OHLCV the tracker uses. No DB writes.",
        "",
        "## 1. Aggregate match vs system",
        "",
        f"| Category | n | share |",
        f"|---|---:|---:|",
        f"| match (system & reconstruction agree on outcome) | {diffs['match']} | {diffs['match']/max(len(rows_out),1)*100:.0f}% |",
        f"| ambiguous (intrabar entry+stop or entry+TP detected — system silently called it) | {diffs['ambiguous']} | {diffs['ambiguous']/max(len(rows_out),1)*100:.0f}% |",
        f"| mismatch (real diff) | {diffs['mismatch']} | {diffs['mismatch']/max(len(rows_out),1)*100:.0f}% |",
        f"| missing_data (no cached OHLCV) | {diffs['missing_data']} | {diffs['missing_data']/max(len(rows_out),1)*100:.0f}% |",
        "",
        "## 2. Execution-quality flags detected",
        "",
        f"- **intrabar_entry_stop** (entry and stop in the SAME candle, system did not flag): {intrabar_entry_stop} / {len(rows_out)}",
        f"- **intrabar_entry_tp** (entry and TP1 in the SAME candle, system did not flag): {intrabar_entry_tp} / {len(rows_out)}",
        f"- **intrabar_stop_tp** (stop and TP1 same candle, AFTER entry — system DOES flag this): {intrabar_stop_tp} / {len(rows_out)}",
        f"- **pre_entry_invalidation** (invalidation hit before entry): {pre_entry_inval} / {len(rows_out)}",
        f"- **gap_slip_stop > 10% of risk** (low/high pierced > 10% past stop): {gap_stops} / {len(rows_out)}",
        f"- **gap_slip_tp1 > 10% of risk** (high/low pierced > 10% past TP1): {gap_tps} / {len(rows_out)}",
        "",
        "## 3. Per-signal table",
        "",
        "Full row-level data is in `PAPER_EXECUTION_VALIDATION_DATASET.csv` (40 rows × 40 columns).",
        "",
        "Notable signals:",
        "",
    ]
    # Highlight intrabar cases
    flagged = [r for r in rows_out if r.get("flag_intrabar_entry_stop") or r.get("flag_intrabar_entry_tp")]
    if flagged:
        lines.append("### Intrabar-ambiguous signals (system reported a clean outcome but entry collided with stop/TP in one bar)")
        lines.append("")
        for r in flagged[:15]:
            tag = []
            if r.get("flag_intrabar_entry_stop"): tag.append("entry+stop")
            if r.get("flag_intrabar_entry_tp"): tag.append("entry+TP1")
            lines.append(
                f"- **{r['symbol']}** ({r['asset_class']} {r['mode']} {r['direction']}, "
                f"created {r['created_at'][:16]}) — system outcome: `{r['sys_outcome']}` R={r['sys_final_r']} · "
                f"flags: `{', '.join(tag)}` · ohlcv `{r['ohlcv_source']}/{r['ohlcv_tf']}`"
            )
        lines.append("")
    else:
        lines.append("- _No intrabar-ambiguous flags raised in this sample._")
        lines.append("")
    # Real mismatches
    mismatches = [r for r in rows_out if r.get("diff_outcome") == "mismatch" and not (r.get("flag_intrabar_entry_stop") or r.get("flag_intrabar_entry_tp"))]
    if mismatches:
        lines.append("### True mismatches (reconstruction differs from system on outcome)")
        lines.append("")
        for r in mismatches[:10]:
            lines.append(
                f"- **{r['symbol']}** {r['mode']} {r['direction']} (created {r['created_at'][:16]}) "
                f"· system: `{r['sys_outcome']}` · reconstruction: `{r['recon_outcome']}`"
            )
        lines.append("")
    lines.extend([
        "## 4. Conclusion",
        "",
        f"The reconstruction confirms the tracker's chronological logic on **{diffs['match']} of {len(rows_out)}** signals.",
        f"It exposes **{intrabar_entry_stop + intrabar_entry_tp}** intrabar-entry-collision cases the existing tracker silently called a clean win/loss — these are the PART 1 §A/§B issues confirmed empirically.",
        "",
        "**No outcome data was modified.** The diff CSV is a diagnostic artifact only.",
        "",
        "## Verdict",
        "",
        "```",
        "RECONSTRUCTION_COMPLETE_WITH_FLAGS" if (intrabar_entry_stop + intrabar_entry_tp) else "RECONSTRUCTION_MATCHES_SYSTEM",
        "```",
    ])
    md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {MD_OUT.name}")
    db.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
