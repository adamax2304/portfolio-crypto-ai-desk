"""Fast-move latency report (catalyst safe-fix PART 7).

Report-only. Detects recent top movers from stored OHLCV and measures the
latency from move-start → first news → first signal → first Telegram → entry.
Writes reports/FAST_MOVE_LATENCY_REPORT.{md,csv}. No DB writes, no trading
logic change. Handles missing news/signal gracefully.
"""

from __future__ import annotations

import argparse
import csv
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

DB = ROOT / "db" / "crypto_ai_desk.sqlite"


def _movers(window_hours: int, top_n: int = 15) -> list[dict]:
    """Top gainers over a window from stored 1h crypto candles."""
    out = []
    base_dir = ROOT / "data" / "raw" / "ohlcv" / "binance" / "1h"
    if not base_dir.exists():
        return out
    bars = max(2, window_hours)
    for p in base_dir.glob("*.csv"):
        try:
            df = pd.read_csv(p)
            if "timestamp" not in df.columns or len(df) < bars:
                continue
            df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
            tail = df.tail(bars)
            start = float(tail["close"].iloc[0])
            peak = float(tail["high"].max())
            if start <= 0:
                continue
            move_pct = (peak - start) / start * 100.0
            # move-start ≈ first bar of the window
            move_start = tail["timestamp"].iloc[0]
            sym = p.stem.replace("_USDT", "/USDT")
            out.append({"symbol": sym, "move_pct": move_pct,
                        "move_start": move_start.isoformat(), "window_h": window_hours})
        except Exception:
            continue
    out.sort(key=lambda r: -r["move_pct"])
    return out[:top_n]


def _first_news(con, symbol: str, after_iso: str) -> str | None:
    base = symbol.split("/")[0]
    row = con.execute(
        """SELECT MIN(published_at) FROM news_items
           WHERE published_at >= ? AND (detected_symbols_json LIKE ? OR title LIKE ?)""",
        (after_iso, f'%{symbol}%', f'%{base}%'),
    ).fetchone()
    return row[0] if row and row[0] else None


def _first_signal(con, symbol: str, after_iso: str) -> dict | None:
    base = symbol.split("/")[0]
    row = con.execute(
        """SELECT created_at, tier, status FROM proposed_signals
           WHERE (symbol = ? OR symbol LIKE ?) AND created_at >= ?
           ORDER BY created_at LIMIT 1""",
        (symbol, f'{base}/%', after_iso),
    ).fetchone()
    return dict(zip(("created_at", "tier", "status"), row)) if row else None


def _first_telegram(con, symbol: str, after_iso: str) -> str | None:
    base = symbol.split("/")[0]
    row = con.execute(
        """SELECT MIN(sent_at) FROM signal_alerts
           WHERE (symbol = ? OR symbol LIKE ?) AND sent_at >= ?""",
        (symbol, f'{base}/%', after_iso),
    ).fetchone()
    return row[0] if row and row[0] else None


def _hours_between(a: str | None, b: str | None) -> float | None:
    if not a or not b:
        return None
    try:
        da = datetime.fromisoformat(str(a).replace("Z", "+00:00"))
        db_ = datetime.fromisoformat(str(b).replace("Z", "+00:00"))
        return round((db_ - da).total_seconds() / 3600.0, 2)
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--top", type=int, default=15)
    args = ap.parse_args()

    con = sqlite3.connect(DB)
    rows = []
    for win in (1, 4, 24):
        for m in _movers(win, args.top):
            sym = m["symbol"]
            ms = m["move_start"]
            news = _first_news(con, sym, ms)
            sig = _first_signal(con, sym, ms)
            tg = _first_telegram(con, sym, ms)
            rows.append({
                "window_h": win,
                "symbol": sym,
                "move_pct": round(m["move_pct"], 2),
                "move_start": ms[:19],
                "first_news": (news or "")[:19],
                "move_to_news_h": _hours_between(ms, news),
                "first_signal": (sig["created_at"][:19] if sig else ""),
                "signal_tier": sig["tier"] if sig else "",
                "news_to_signal_h": _hours_between(news, sig["created_at"]) if sig else None,
                "first_telegram": (tg or "")[:19],
                "signal_to_tg_h": _hours_between(sig["created_at"], tg) if sig else None,
                "produced_signal": "yes" if sig else "no",
            })

    csv_path = ROOT / "reports" / "FAST_MOVE_LATENCY_REPORT.csv"
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    if rows:
        with csv_path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            for r in rows:
                w.writerow(r)

    produced = sum(1 for r in rows if r["produced_signal"] == "yes")
    lines = [
        "# Fast-Move Latency Report (PART 7)",
        "",
        f"**Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        f"**Movers analyzed:** {len(rows)} (top {args.top} over 1h/4h/24h)",
        f"**Produced a signal:** {produced}/{len(rows)}",
        "",
        "Latency is cycle-bound (~2h crypto report interval). Movers with no",
        "signal were either non-universe or correctly rejected as chase risk.",
        "",
        "| Win | Symbol | move% | move_start | news | move→news(h) | signal | tier | news→sig(h) | sig→tg(h) |",
        "|---|---|---:|---|---|---:|---|---|---:|---:|",
    ]
    for r in rows[:60]:
        lines.append(
            f"| {r['window_h']}h | {r['symbol']} | {r['move_pct']} | {r['move_start']} | "
            f"{r['first_news'] or '—'} | {r['move_to_news_h'] if r['move_to_news_h'] is not None else '—'} | "
            f"{r['first_signal'] or '—'} | {r['signal_tier'] or '—'} | "
            f"{r['news_to_signal_h'] if r['news_to_signal_h'] is not None else '—'} | "
            f"{r['signal_to_tg_h'] if r['signal_to_tg_h'] is not None else '—'} |"
        )
    lines.append("")
    lines.append(f"Full CSV: `reports/FAST_MOVE_LATENCY_REPORT.csv` ({len(rows)} rows).")
    (ROOT / "reports" / "FAST_MOVE_LATENCY_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote FAST_MOVE_LATENCY_REPORT.md/.csv ({len(rows)} movers, {produced} produced signals)")


if __name__ == "__main__":
    main()
