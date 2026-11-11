"""Generate the "Current State" pinned dashboard tab.

Read-only. Reads SQLite, latest reports, catalyst files, and Opus reviews;
writes ONE markdown page as a pinned-MOC tab at the vault root:

    obsidian_vault/11 📌 Trading Desk Current State.md

It is **also called by** `scripts/refresh_obsidian_dashboard.py` via the
exported `build_page()` function, so the same content refreshes every
scheduler cycle alongside the other pinned tabs (00–10).

No code/strategy/scoring/TP/SL changes. No new signals. No Telegram. No
auto-trade. No scheduler ops. Safe to run repeatedly.

Standalone usage:
    python -m scripts.write_obsidian_current_state_dashboard
"""
from __future__ import annotations

import json
import os
import sqlite3
import sys
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = REPO_ROOT / "db" / "crypto_ai_desk.sqlite"
VAULT = REPO_ROOT / "obsidian_vault"
PAGE = VAULT / "11 📌 Trading Desk Current State.md"


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def now_eest_str() -> str:
    # EEST = UTC+3 in summer 2026; render approximate local time for header
    local = datetime.now(timezone.utc) + timedelta(hours=3)
    return local.strftime("%Y-%m-%d %H:%M EEST")


def iso_minus_hours(now: datetime, hours: float) -> str:
    return (now - timedelta(hours=hours)).isoformat()


def fmt_dt(s: str | None, *, brief: bool = False) -> str:
    if not s:
        return "—"
    s = s.replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(s)
    except Exception:
        return s[:16]
    if brief:
        return dt.strftime("%m-%d %H:%M")
    return dt.strftime("%Y-%m-%d %H:%M UTC")


def fmt_num(v: Any, prec: int = 4) -> str:
    if v is None:
        return "—"
    try:
        f = float(v)
    except Exception:
        return str(v)
    if abs(f) >= 1000:
        return f"{f:,.2f}"
    if abs(f) >= 1:
        return f"{f:.{max(2, prec - 2)}f}"
    return f"{f:.{prec}f}"


def fmt_r(v: Any) -> str:
    if v is None:
        return "—"
    try:
        return f"{float(v):+.2f}R"
    except Exception:
        return str(v)


def crypto_tv_link(symbol: str) -> str:
    sym = symbol.replace("/", "")
    return f"https://www.tradingview.com/chart/?symbol=BINANCE:{sym}"


def stocks_tv_link(symbol: str) -> str:
    return f"https://www.tradingview.com/chart/?symbol={symbol}"


def tv_link(asset_class: str, symbol: str) -> str:
    return crypto_tv_link(symbol) if asset_class == "crypto" else stocks_tv_link(symbol)


# ─────────────────────────────────────────────────────────────────────────────
# DB helpers
# ─────────────────────────────────────────────────────────────────────────────

def open_db() -> sqlite3.Connection:
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db


def deduped_signal_rows(db: sqlite3.Connection, *, since: str | None = None,
                        asset_class: str | None = None,
                        only_open: bool = False) -> list[sqlite3.Row]:
    where = []
    args: list[Any] = []
    if since:
        where.append("ps.created_at >= ?")
        args.append(since)
    if asset_class:
        where.append("ps.asset_class = ?")
        args.append(asset_class)
    if only_open:
        where.append("(so.final_outcome IS NULL OR so.final_outcome IN ('not_triggered'))")
    where_sql = ("WHERE " + " AND ".join(where)) if where else ""
    q = f"""
        SELECT ps.signal_id, ps.asset_class, ps.symbol, ps.direction, ps.mode, ps.tier,
               ps.score, ps.created_at, ps.expires_at, ps.validity_window_hours,
               ps.entry_low, ps.entry_high, ps.stop_loss, ps.invalidation,
               ps.tp1, ps.tp2, ps.tp3,
               ps.news_supported, ps.sector, ps.market_regime,
               ps.source_report_path, ps.status,
               so.final_outcome, so.final_r,
               so.entry_triggered, so.entry_triggered_at, so.entry_price_used,
               so.stop_hit, so.stop_hit_at, so.tp1_hit, so.tp1_hit_at,
               so.tp2_hit, so.tp2_hit_at,
               so.max_favorable_excursion_r, so.max_adverse_excursion_r
        FROM proposed_signals ps
        LEFT JOIN signal_outcomes so
          ON so.signal_id = ps.signal_id
         AND so.id = (SELECT MAX(id) FROM signal_outcomes WHERE signal_id = ps.signal_id)
        {where_sql}
        ORDER BY ps.created_at DESC
    """
    return db.execute(q, args).fetchall()


# ─────────────────────────────────────────────────────────────────────────────
# Process / scheduler probes
# ─────────────────────────────────────────────────────────────────────────────

def _parse_cim_date(raw: str | None) -> str | None:
    """PowerShell ConvertTo-Json renders CIM datetime as `/Date(ms)/`.
    Translate to ISO UTC. Return None on failure."""
    if not raw:
        return None
    s = str(raw)
    if s.startswith("/Date(") and s.endswith(")/"):
        try:
            ms = int(s[6:-2].split("+")[0].split("-")[0])
            return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).isoformat(timespec="seconds")
        except Exception:
            return None
    return s


def probe_processes() -> dict[str, Any]:
    """Best-effort probe of scheduler/collector/monitor python processes via WMI.
    Returns a dict; never raises — dashboard will degrade gracefully."""
    out = {
        "scheduler": None,
        "telegram_collector": None,
        "crypto_monitor": None,
        "stocks_monitor": None,
        "probed_at": now_iso(),
        "error": None,
    }
    if sys.platform != "win32":
        out["error"] = "process probe only supported on win32"
        return out
    try:
        import subprocess
        ps = subprocess.run(
            [
                "powershell.exe",
                "-NoProfile",
                "-Command",
                "Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" "
                "| Select-Object ProcessId, CreationDate, CommandLine | ConvertTo-Json -Compress -Depth 3"
            ],
            capture_output=True, text=True, timeout=20,
        )
        if ps.returncode != 0 or not ps.stdout.strip():
            out["error"] = f"powershell rc={ps.returncode}"
            return out
        data = json.loads(ps.stdout)
        if isinstance(data, dict):
            data = [data]
        for p in data:
            cmd = (p.get("CommandLine") or "")
            pid = p.get("ProcessId")
            born = _parse_cim_date(p.get("CreationDate")) or "—"
            entry = {"pid": pid, "born": born, "cmd": cmd}
            if "run_default_market_schedule" in cmd:
                out["scheduler"] = entry
            elif "run_telegram_collector" in cmd or "telegram_collector" in cmd:
                out["telegram_collector"] = entry
            elif "monitor-watchlist" in cmd:
                out["crypto_monitor"] = entry
            elif "stocks-monitor-session" in cmd:
                out["stocks_monitor"] = entry
        return out
    except Exception as exc:
        out["error"] = f"probe failed: {type(exc).__name__}: {exc}"
        return out


# ─────────────────────────────────────────────────────────────────────────────
# Latest-file probes
# ─────────────────────────────────────────────────────────────────────────────

def latest_in(dir_path: Path, suffix: str = ".md") -> Path | None:
    if not dir_path.exists():
        return None
    files = [p for p in dir_path.iterdir() if p.is_file() and p.suffix == suffix]
    if not files:
        return None
    return max(files, key=lambda p: p.stat().st_mtime)


def file_mtime_iso(p: Path | None) -> str | None:
    if p is None or not p.exists():
        return None
    return datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc).isoformat(timespec="seconds")


def latest_opus_review() -> Path | None:
    candidates = sorted(REPO_ROOT.glob("OPUS_ENRICHED_REVIEW_AUTO_*.md"))
    return candidates[-1] if candidates else None


# ─────────────────────────────────────────────────────────────────────────────
# Catalyst snapshot
# ─────────────────────────────────────────────────────────────────────────────

def latest_catalyst_events(limit: int = 15) -> list[dict]:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    yest = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d")
    events: list[dict] = []
    for d in (today, yest):
        path = REPO_ROOT / "data" / "catalysts" / d / "catalyst_events.jsonl"
        if not path.exists():
            continue
        try:
            with path.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        events.append(json.loads(line))
                    except Exception:
                        continue
        except Exception:
            continue
    # Sort by ts/headline
    def ts_key(e):
        return e.get("ts") or e.get("published_at") or e.get("created_at") or ""
    events.sort(key=ts_key, reverse=True)
    return events[:limit]


def latest_narrative_baskets(limit: int = 8) -> list[dict]:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    yest = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d")
    rows: list[dict] = []
    for d in (today, yest):
        path = REPO_ROOT / "data" / "catalysts" / d / "narrative_baskets.jsonl"
        if not path.exists():
            continue
        try:
            with path.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        rows.append(json.loads(line))
                    except Exception:
                        continue
        except Exception:
            continue
    return rows[:limit]


# ─────────────────────────────────────────────────────────────────────────────
# Stats slices (mirror of audit script, simplified)
# ─────────────────────────────────────────────────────────────────────────────

def slice_stats(rows: list[sqlite3.Row]) -> dict:
    wins = [r for r in rows if r["final_outcome"] == "win"]
    losses = [r for r in rows if r["final_outcome"] == "loss"]
    closed = wins + losses
    net_r = sum((r["final_r"] or 0) for r in closed)
    win_r = sum((r["final_r"] or 0) for r in wins)
    loss_r = abs(sum((r["final_r"] or 0) for r in losses)) or 1e-9
    return {
        "n": len(rows), "W": len(wins), "L": len(losses), "closed": len(closed),
        "WR": (len(wins) / len(closed) * 100) if closed else 0.0,
        "netR": net_r,
        "PF": (win_r / loss_r) if losses else (float("inf") if wins else 0.0),
    }


def fmt_stats(s: dict) -> str:
    wr = f"{s['WR']:.0f}%" if s["closed"] else "—"
    pf = "∞" if s["PF"] == float("inf") else (f"{s['PF']:.2f}" if s["PF"] else "—")
    return (f"n={s['n']} closed={s['closed']} W={s['W']} L={s['L']} "
            f"WR={wr} PF(legacy-touch)={pf} legacyTouchR={s['netR']:+.0f}R (optimistic · NOT PnL)")


# ─────────────────────────────────────────────────────────────────────────────
# Comments / per-trade narrative
# ─────────────────────────────────────────────────────────────────────────────

def open_trade_comment(r: sqlite3.Row) -> str:
    mfe = float(r["max_favorable_excursion_r"] or 0)
    mae = float(r["max_adverse_excursion_r"] or 0)
    triggered = (r["entry_triggered"] == 1)
    status = (r["status"] or "").lower()
    # 2026-06-09 revalidator statuses surface first.
    if status == "stale_before_entry":
        return "stale — pending past freshness horizon, manual review"
    if status == "entry_moved_away":
        return "missed by the move — favorable run without fill"
    if status == "regime_changed":
        return "regime flipped against thesis — manual review"
    if status == "needs_reprice":
        return "needs reprice — original entry may be invalid"
    if not triggered:
        return "waiting for entry"
    if r["tier"] == "C":
        return "watchlist only — not actionable"
    if r["asset_class"] == "crypto" and r["mode"] == "scalp":
        return "low-confidence scalp (mode audit)"
    if mfe >= 1.5 and not r["tp1_hit"]:
        return "triggered, near TP1"
    if mae <= -0.7:
        return "triggered, near invalidation"
    if mfe >= 0.5 and not r["tp1_hit"]:
        return "good MFE but not yet TP"
    return "triggered, in-flight"


def closed_trade_comment(r: sqlite3.Row) -> str:
    fo = r["final_outcome"]
    mfe = float(r["max_favorable_excursion_r"] or 0)
    mae = float(r["max_adverse_excursion_r"] or 0)
    news = bool(r["news_supported"])
    # If the outcome notes carry the new execution annotations, prepend a flag.
    note = ""
    try:
        n = (r["outcome_notes"] or "") if "outcome_notes" in r.keys() else ""
    except Exception:
        n = ""
    if "intrabar_entry_stop" in n:
        note = " ⚠ intrabar entry+stop (one-bar resolution)"
    elif "intrabar_entry_tp" in n:
        note = " ⚠ intrabar entry+TP (one-bar resolution)"
    elif "gap_slip_stop_pct_of_risk" in n:
        note = " ⚠ gap slip past stop (real fill worse than reported R)"
    elif "gap_slip_tp_pct_of_risk" in n:
        note = " ⚠ gap slip past TP (real fill better than reported R)"

    if fo == "win":
        if news:
            return "Good signal: reached TP after clean catalyst-backed move." + note
        return "Reached TP on momentum alone (no catalyst flag)." + note
    if fo == "loss":
        if mfe < 0.3 and mae <= -1.0:
            return "Stopped quickly: likely bad entry / wrong regime." + note
        if mfe >= 0.8:
            return "Stopped after favorable run — possible squeeze/reversal." + note
        return "Stopped: thesis invalidated." + note
    if fo == "expired":
        if mfe >= 0.5:
            return "Expired flat but had positive MFE: possible TP/horizon issue."
        return "Expired flat — no decisive move inside validity window."
    if fo == "not_triggered":
        return "Did not trigger: entry zone never reached."
    return "—"


# ─────────────────────────────────────────────────────────────────────────────
# Section builders
# ─────────────────────────────────────────────────────────────────────────────

def section_header(now_str: str, status: str,
                   freshness: dict | None = None) -> list[str]:
    canonical_rel = "obsidian_vault/11 📌 Trading Desk Current State.md"
    lines = [
        "# 📌 Trading Desk — Current State",
        "",
        f"_Refreshed: **{now_str}** · Source: `proposed_signals` × latest `signal_outcomes`, "
        "live reports, catalyst JSONL, Opus reviews, process probe._",
        "",
        f"_Canonical dashboard file: `{canonical_rel}` (single pinned tab; "
        "no duplicates)._",
        "",
    ]
    # Freshness self-warning. Compares newest DB row vs page-generation time.
    # If the underlying data is materially newer than the page (> 30 min), a
    # ⚠ warning is rendered at the top so the user notices without scrolling.
    if freshness:
        age_min = freshness.get("data_age_minutes")
        newest_db = freshness.get("newest_db_iso", "—")
        if age_min is not None:
            if age_min >= 30:
                lines.append(
                    f"> ⚠ **STALE: this page is {age_min:.0f} min behind the latest DB row.** "
                    f"Latest DB activity: `{newest_db}`. Re-run "
                    "`python -m scripts.refresh_obsidian_dashboard` to refresh now, "
                    "or wait for the next scheduler cycle."
                )
            else:
                lines.append(
                    f"> ✅ **Data freshness:** {age_min:.0f} min behind newest DB row "
                    f"(`{newest_db}`)."
                )
            lines.append("")
    lines.extend([
        f"> **System status:** {status}",
        "> **Current focus:** crypto swing/intraday + crypto scalp (low-confidence); "
        "stocks intraday actionable; old stocks swing/invest DEPRECATED/REMOVED; new stocks_swing_growth_breakout shadow-only research.",
        "",
        "This page is a single-screen sweep for a manual monitoring pass — top-to-bottom: "
        "what the system is doing → live trades → just-closed → news → recap → risks → "
        "mode routing → performance → manual checks. Sibling tabs: "
        "[[01 📌 Active Signals]] (raw active list), [[02 📌 Trade History]] (full history), "
        "[[10 📌 Performance by Mode]] (deep performance), [[07 📌 Schedule Status]] (raw health).",
        "",
        "---",
        "",
    ])
    return lines


def section_health(procs: dict, db: sqlite3.Connection) -> tuple[list[str], str]:
    lines = ["## 1. System Health", ""]

    def fmt_proc(label: str, p: dict | None) -> tuple[str, str]:
        if not p:
            return ("❌", f"- {label}: ❌ not running")
        return ("✅", f"- {label}: ✅ running (PID `{p['pid']}`, born `{p['born']}`)")

    sched_sym, sched = fmt_proc("Scheduler (default market schedule)", procs.get("scheduler"))
    tg_sym, tg = fmt_proc("Telegram collector", procs.get("telegram_collector"))
    cm_sym, cm = fmt_proc("Crypto watchlist monitor", procs.get("crypto_monitor"))
    sm_sym, sm = fmt_proc("Stocks intraday monitor", procs.get("stocks_monitor"))
    for ln in (sched, tg, cm, sm):
        lines.append(ln)
    lines.append("")

    # Latest LLM packets
    crypto_pkt = REPO_ROOT / "data" / "processed" / "llm_analysis_packet.md"
    stocks_pkt = REPO_ROOT / "data" / "processed" / "llm_stocks_packet.md"
    lines.append(f"- Crypto LLM packet: `data/processed/llm_analysis_packet.md` "
                 f"(refreshed `{fmt_dt(file_mtime_iso(crypto_pkt))}`)")
    lines.append(f"- Stocks LLM packet: `data/processed/llm_stocks_packet.md` "
                 f"(refreshed `{fmt_dt(file_mtime_iso(stocks_pkt))}`)")

    # Latest Opus review
    opus = latest_opus_review()
    if opus:
        lines.append(f"- Latest Opus enriched review: `{opus.name}` "
                     f"(`{fmt_dt(file_mtime_iso(opus))}`)")
    else:
        lines.append("- Latest Opus enriched review: ❌ not found")

    # Untracked legacy alerts
    try:
        cutoff = iso_minus_hours(datetime.now(timezone.utc), 24)
        cnt = db.execute(
            """
            SELECT COUNT(*) FROM watchlist_alerts wa
            WHERE wa.asset_class='crypto' AND wa.sent_at >= ?
              AND NOT EXISTS (
                SELECT 1 FROM proposed_signals ps
                WHERE ps.symbol = wa.symbol
                  AND ABS((julianday(ps.created_at) - julianday(wa.sent_at)) * 24) < 6
              )
            """,
            (cutoff,),
        ).fetchone()[0]
    except Exception:
        cnt = "n/a"
    sym = "✅" if cnt == 0 else "⚠️"
    lines.append(f"- Untracked legacy crypto alerts (24h): {sym} `{cnt}`")
    lines.append("")

    # Overall status
    issues = []
    if not procs.get("scheduler"):
        issues.append("scheduler down")
    if not procs.get("telegram_collector"):
        issues.append("telegram collector down")
    if isinstance(cnt, int) and cnt > 0:
        issues.append(f"{cnt} untracked legacy alerts")
    if not opus:
        issues.append("no Opus review")
    if issues:
        lines.append(f"**Issues:** {', '.join(issues)}.")
        overall = "⚠️ PARTIAL"
    else:
        overall = "✅ GREEN"
    lines.append("")
    return lines, overall


def section_open_trades(db: sqlite3.Connection) -> list[str]:
    # Open = no final outcome OR final_outcome IN (not_triggered) AND not expired/closed
    rows = db.execute(
        """
        SELECT ps.signal_id, ps.asset_class, ps.symbol, ps.direction, ps.mode, ps.tier,
               ps.score, ps.created_at, ps.expires_at,
               ps.entry_low, ps.entry_high, ps.stop_loss, ps.invalidation,
               ps.tp1, ps.tp2, ps.tp3,
               ps.news_supported, ps.sector,
               ps.source_report_path, ps.status,
               so.final_outcome, so.final_r,
               so.entry_triggered, so.entry_triggered_at, so.entry_price_used,
               so.stop_hit, so.tp1_hit, so.tp2_hit,
               so.max_favorable_excursion_r, so.max_adverse_excursion_r
        FROM proposed_signals ps
        LEFT JOIN signal_outcomes so
          ON so.signal_id = ps.signal_id
         AND so.id = (SELECT MAX(id) FROM signal_outcomes WHERE signal_id = ps.signal_id)
        WHERE ps.tier IN ('A','B')
          AND (ps.expires_at = '' OR ps.expires_at IS NULL OR ps.expires_at >= ?)
          AND (so.final_outcome IS NULL OR so.final_outcome NOT IN ('expired','loss','win'))
        ORDER BY ps.asset_class, ps.created_at DESC
        """,
        (now_iso(),),
    ).fetchall()
    crypto = [r for r in rows if r["asset_class"] == "crypto"]
    stocks = [r for r in rows if r["asset_class"] == "stocks"]

    lines = ["## 2. Currently Open / Active Paper Trades", ""]
    if not crypto and not stocks:
        lines.append("_No active A/B paper trades right now._")
        lines.append("")
        return lines

    for label, sub in (("### Crypto", crypto), ("### Stocks", stocks)):
        lines.append(label)
        if not sub:
            lines.append("")
            lines.append("- _none_")
            lines.append("")
            continue
        for r in sub:
            lines.extend(render_open_trade(r, db=db))
            lines.append("")
    return lines


def _playbook_for_row(r: sqlite3.Row):
    """Resolve a sqlite Row to a PlaybookLabel; defensive against missing fields."""
    from src.signals.playbooks import label_for
    return label_for({
        "asset_class": r["asset_class"],
        "mode": r["mode"],
        "direction": r["direction"],
        "tier": r["tier"],
        "score": r["score"] or 0,
        "news_supported": bool(r["news_supported"]),
    })


def _paper_entry_alert_state(db: sqlite3.Connection, signal_id: str) -> tuple[str, str]:
    """Return (status, sized_reason_short) for the paper-entry telegram alert.

    status is one of: 'sent', 'not_triggered_yet', 'not_sent_skipped', 'unknown'.
    """
    try:
        row = db.execute(
            "SELECT telegram_status, payload_json, sent_at FROM signal_alerts "
            "WHERE signal_id = ? AND alert_type = 'paper_entry' "
            "ORDER BY sent_at DESC LIMIT 1",
            (signal_id,),
        ).fetchone()
    except sqlite3.OperationalError:
        return ("unknown", "")
    if not row:
        return ("none", "")
    sized = ""
    try:
        import json as _json
        d = _json.loads(row["payload_json"] or "{}")
        w = d.get("size_weight")
        r = d.get("size_reason") or ""
        if w is not None:
            sized = f"{w}x — {r}".strip(" —")
    except Exception:
        pass
    return (row["telegram_status"] or "sent", sized)


def render_open_trade(r: sqlite3.Row, *, db: sqlite3.Connection | None = None) -> list[str]:
    sym = r["symbol"]
    link = tv_link(r["asset_class"], sym)
    head = f"**{sym}** · {r['direction'].upper()} · {r['mode']} · tier {r['tier']} · score {r['score']:.0f} · [TradingView]({link})"
    paper_entry = "Paper entry: not triggered yet." if r["entry_triggered"] != 1 else (
        f"Paper entry: `{fmt_dt(r['entry_triggered_at'])}` at price `{fmt_num(r['entry_price_used'])}`"
    )
    entry = f"`{fmt_num(r['entry_low'])} – {fmt_num(r['entry_high'])}`"
    sl_val = r["stop_loss"] or r["invalidation"]
    tp1, tp2, tp3 = fmt_num(r["tp1"]), fmt_num(r["tp2"]), fmt_num(r["tp3"])
    mfe = fmt_r(r["max_favorable_excursion_r"])
    mae = fmt_r(r["max_adverse_excursion_r"])
    news = "yes" if r["news_supported"] else "no"
    fr = fmt_r(r["final_r"]) if r["final_r"] is not None else "open"
    comment = open_trade_comment(r)
    sec = f", sector `{r['sector']}`" if r["sector"] else ""
    src = f"`{r['source_report_path']}`" if r["source_report_path"] else "—"
    lbl = _playbook_for_row(r)
    overlays = lbl.overlay_str()
    # Paper-entry telegram annotation
    if db is not None:
        pe_status, pe_size = _paper_entry_alert_state(db, r["signal_id"])
    else:
        pe_status, pe_size = ("unknown", "")
    # 2026-06-14 standardization: dashboard labels mirror Telegram headers.
    if r["entry_triggered"] != 1:
        pe_line = "SETUP — WAITING FOR ENTRY · No paper entry yet."
    elif pe_status == "sent":
        pe_line = f"PAPER ENTRY — TRIGGERED · ✅ Telegram sent · {pe_size}".rstrip(" ·")
    elif pe_status == "dry_run":
        pe_line = f"PAPER ENTRY — TRIGGERED · 🟡 dry-run only · {pe_size}".rstrip(" ·")
    elif pe_status == "none":
        pe_line = "PAPER ENTRY — TRIGGERED · ⚠️ alert not sent (filtered by tier / playbook / asset-class gate)."
    elif str(pe_status).startswith("error"):
        pe_line = f"PAPER ENTRY — TRIGGERED · ❌ Telegram failed ({pe_status})."
    else:
        pe_line = f"PAPER ENTRY — TRIGGERED · {pe_status}".rstrip()
    # If the trade closed, surface the close label too.
    fo = r["final_outcome"] if "final_outcome" in r.keys() else None
    if fo in ("win", "loss", "expired", "ambiguous"):
        label = {"win": "✅ CLOSE — TP HIT", "loss": "❌ CLOSE — STOP HIT",
                 "expired": "⏳ CLOSE — EXPIRED",
                 "ambiguous": "⚠️ CLOSE — AMBIGUOUS"}[fo]
        pe_line = f"{label} · " + pe_line
    # 2026-06-15 scalp downgrade: crypto scalp is SHADOW ONLY (0× size).
    is_scalp = (str(r["asset_class"]).lower() == "crypto" and str(r["mode"]).lower() == "scalp")
    shadow_line = None
    if is_scalp:
        shadow_line = ("  - 🚫 **SHADOW ONLY · 0x size · NOT for manual live shadow** "
                       "— reason: 12m backtest net-negative after fees")
    head_lines = [
        f"- {head}",
        f"  - Created: `{fmt_dt(r['created_at'])}` | Expires: `{fmt_dt(r['expires_at']) if r['expires_at'] else '—'}`{sec}",
    ]
    if shadow_line:
        head_lines.append(shadow_line)
    return head_lines + [
        f"  - {paper_entry}",
        f"  - {pe_line}",
        f"  - Entry zone: {entry} | SL: `{fmt_num(sl_val)}` | TP1 `{tp1}` / TP2 `{tp2}` / TP3 `{tp3}`",
        f"  - Status: `{r['status']}` | Legacy touch R (not PnL): {fr} | MFE: {mfe} | MAE: {mae} | catalyst: {news}",
        f"  - Playbook: `{lbl.playbook}` · status **{lbl.status}** · overlays: {overlays}",
        f"  - Failure mode: _{lbl.failure_mode}_",
        f"  - Manual review hint: _{lbl.manual_review_hint}_",
        f"  - Source report: {src}",
        f"  - **Comment:** {comment}",
    ]


def section_recent_trades(db: sqlite3.Connection, asset_class: str, n: int = 5) -> list[str]:
    rows = db.execute(
        """
        SELECT ps.signal_id, ps.asset_class, ps.symbol, ps.direction, ps.mode, ps.tier,
               ps.score, ps.created_at, ps.expires_at,
               ps.entry_low, ps.entry_high, ps.stop_loss, ps.invalidation,
               ps.tp1, ps.tp2, ps.tp3,
               ps.news_supported, ps.sector,
               ps.source_report_path, ps.status,
               so.final_outcome, so.final_r,
               so.entry_triggered, so.entry_triggered_at, so.entry_price_used,
               so.stop_hit, so.stop_hit_at, so.tp1_hit, so.tp1_hit_at,
               so.tp2_hit,
               so.max_favorable_excursion_r, so.max_adverse_excursion_r,
               so.notes as outcome_notes
        FROM proposed_signals ps
        LEFT JOIN signal_outcomes so
          ON so.signal_id = ps.signal_id
         AND so.id = (SELECT MAX(id) FROM signal_outcomes WHERE signal_id = ps.signal_id)
        WHERE ps.asset_class=? AND ps.tier IN ('A','B')
          AND so.final_outcome IN ('win','loss','expired','not_triggered')
        ORDER BY ps.created_at DESC
        LIMIT ?
        """,
        (asset_class, n),
    ).fetchall()

    label = "Crypto" if asset_class == "crypto" else "Stocks"
    sect_num = "3" if asset_class == "crypto" else "4"
    lines = [f"## {sect_num}. Last {n} {label} Trades", ""]
    if not rows:
        lines.append("_No recent trades found._")
        lines.append("")
        return lines
    for r in rows:
        lines.extend(render_recent_trade(r))
        lines.append("")
    return lines


def render_recent_trade(r: sqlite3.Row) -> list[str]:
    sym = r["symbol"]
    link = tv_link(r["asset_class"], sym)
    lbl = _playbook_for_row(r)
    head = (f"**{sym}** · {r['direction'].upper()} · {r['mode']} · tier {r['tier']} · "
            f"score {r['score']:.0f} · playbook `{lbl.playbook}` · [TradingView]({link})")
    paper_entry = "not triggered" if r["entry_triggered"] != 1 else fmt_dt(r["entry_triggered_at"])
    duration = "—"
    if r["entry_triggered_at"] and (r["tp1_hit_at"] or r["stop_hit_at"]):
        end_iso = r["tp1_hit_at"] or r["stop_hit_at"]
        try:
            t0 = datetime.fromisoformat(r["entry_triggered_at"].replace("Z", "+00:00"))
            t1 = datetime.fromisoformat(end_iso.replace("Z", "+00:00"))
            hours = (t1 - t0).total_seconds() / 3600
            duration = f"{hours:.1f}h" if hours < 48 else f"{hours/24:.1f}d"
        except Exception:
            pass
    sl_val = r["stop_loss"] or r["invalidation"]
    return [
        f"- {head}",
        f"  - Created: `{fmt_dt(r['created_at'])}` | Paper entry: `{paper_entry}` | Time in trade: `{duration}`",
        f"  - Entry zone: `{fmt_num(r['entry_low'])}–{fmt_num(r['entry_high'])}` | SL: `{fmt_num(sl_val)}` | "
        f"TP1 `{fmt_num(r['tp1'])}` / TP2 `{fmt_num(r['tp2'])}` / TP3 `{fmt_num(r['tp3'])}`",
        f"  - Outcome: **`{r['final_outcome']}`** | Legacy touch R (not PnL): **{fmt_r(r['final_r'])}** | "
        f"MFE: {fmt_r(r['max_favorable_excursion_r'])} | MAE: {fmt_r(r['max_adverse_excursion_r'])} | "
        f"catalyst: {'yes' if r['news_supported'] else 'no'}",
        f"  - **Comment:** {closed_trade_comment(r)}",
    ]


def section_events_today() -> list[str]:
    lines = ["## 5. Main Events Today", ""]
    events = latest_catalyst_events(limit=12)
    crypto_evs = [e for e in events if (e.get("asset_class") or "crypto") == "crypto"]
    stocks_evs = [e for e in events if (e.get("asset_class") or "") == "stocks"]
    # If asset_class missing, fall back on symbol heuristic
    if not crypto_evs and not stocks_evs and events:
        crypto_evs = events  # treat all as crypto by default

    for label, sub in (("### Crypto", crypto_evs), ("### Stocks / Macro", stocks_evs)):
        lines.append(label)
        if not sub:
            lines.append("")
            lines.append("- _no notable catalysts captured in the last 24h_")
            lines.append("")
            continue
        # Dedupe by title to avoid showing the same headline from different days
        seen: set[str] = set()
        rendered = 0
        for e in sub:
            if rendered >= 6:
                break
            headline = e.get("title") or e.get("headline") or "(no headline)"
            if headline in seen:
                continue
            seen.add(headline)
            source = e.get("source") or e.get("publisher") or "—"
            ts = e.get("timestamp") or e.get("collected_at") or e.get("ts")
            syms = e.get("symbol") or e.get("related_symbols") or e.get("symbols") or []
            if isinstance(syms, str):
                syms = [syms]
            sym_str = ", ".join(s for s in syms[:5]) if syms else "—"
            why = e.get("catalyst_type") or e.get("narrative") or "—"
            importance = e.get("importance") or e.get("confidence") or "—"
            lines.append(f"- **{headline[:140]}** — _{source}_ · `{fmt_dt(ts)}`")
            lines.append(f"  - Symbols: `{sym_str}` | Type: `{why}` | Importance: `{importance}`")
            rendered += 1
        lines.append("")
    lines.append("_Note: catalyst→symbol mapping is partial — use as context, not as a trade trigger._")
    lines.append("")
    return lines


def section_events_week(db: sqlite3.Connection) -> list[str]:
    lines = ["## 6. Main Events This Week", ""]
    # Pull last-7d narrative baskets summary
    baskets = latest_narrative_baskets(limit=10)
    cutoff = iso_minus_hours(datetime.now(timezone.utc), 24 * 7)

    # Crypto week recap from closed trades
    crypto_closed = db.execute(
        """
        SELECT ps.symbol, ps.mode, ps.direction, so.final_outcome, so.final_r, ps.news_supported
        FROM proposed_signals ps
        LEFT JOIN signal_outcomes so
          ON so.signal_id = ps.signal_id
         AND so.id = (SELECT MAX(id) FROM signal_outcomes WHERE signal_id = ps.signal_id)
        WHERE ps.asset_class='crypto' AND ps.tier IN ('A','B')
          AND ps.created_at >= ? AND so.final_outcome IN ('win','loss')
        ORDER BY ps.created_at DESC
        """,
        (cutoff,),
    ).fetchall()
    stocks_closed = db.execute(
        """
        SELECT ps.symbol, ps.mode, ps.direction, so.final_outcome, so.final_r
        FROM proposed_signals ps
        LEFT JOIN signal_outcomes so
          ON so.signal_id = ps.signal_id
         AND so.id = (SELECT MAX(id) FROM signal_outcomes WHERE signal_id = ps.signal_id)
        WHERE ps.asset_class='stocks' AND ps.tier IN ('A','B')
          AND ps.created_at >= ? AND so.final_outcome IN ('win','loss')
        ORDER BY ps.created_at DESC
        """,
        (cutoff,),
    ).fetchall()

    # Crypto: top narratives observed (dedupe by basket_name)
    lines.append("### Crypto narratives & catalysts (7d)")
    if baskets:
        seen_b: set[str] = set()
        rendered_b = 0
        for b in baskets:
            if rendered_b >= 6:
                break
            name = b.get("basket_name") or b.get("narrative") or b.get("name") or "(unnamed)"
            if name in seen_b:
                continue
            seen_b.add(name)
            primary = b.get("primary_symbols") or []
            related = b.get("related_symbols") or []
            members = (primary + related) if (primary or related) else (b.get("symbols") or [])
            mstr = ", ".join(m for m in members[:6]) if members else "—"
            summary = b.get("catalyst_summary") or "—"
            quality = b.get("source_quality") or "—"
            lines.append(f"- **{name}** (source: {quality}) — members: `{mstr}`")
            if summary and summary != "—":
                lines.append(f"  - _{summary[:160]}_")
            rendered_b += 1
    else:
        lines.append("- _no narrative baskets persisted in the last 48h_")
    lines.append("")

    # Crypto: recurring winners/losers
    if crypto_closed:
        win_syms: dict[str, float] = {}
        loss_syms: dict[str, float] = {}
        for r in crypto_closed:
            if r["final_outcome"] == "win":
                win_syms[r["symbol"]] = win_syms.get(r["symbol"], 0.0) + (r["final_r"] or 0)
            else:
                loss_syms[r["symbol"]] = loss_syms.get(r["symbol"], 0.0) + (r["final_r"] or 0)
        if win_syms:
            top = sorted(win_syms.items(), key=lambda x: -x[1])[:5]
            lines.append("- **Crypto winners (7d):** "
                         + ", ".join(f"{s} {fmt_r(r)}" for s, r in top))
        if loss_syms:
            bot = sorted(loss_syms.items(), key=lambda x: x[1])[:5]
            lines.append("- **Crypto losers (7d):** "
                         + ", ".join(f"{s} {fmt_r(r)}" for s, r in bot))
    lines.append("")

    # Stocks: recurring winners/losers
    lines.append("### Stocks / macro recap (7d)")
    if stocks_closed:
        win_syms2: dict[str, float] = {}
        loss_syms2: dict[str, float] = {}
        for r in stocks_closed:
            if r["final_outcome"] == "win":
                win_syms2[r["symbol"]] = win_syms2.get(r["symbol"], 0.0) + (r["final_r"] or 0)
            else:
                loss_syms2[r["symbol"]] = loss_syms2.get(r["symbol"], 0.0) + (r["final_r"] or 0)
        if win_syms2:
            top = sorted(win_syms2.items(), key=lambda x: -x[1])[:5]
            lines.append("- **Stocks winners (7d):** "
                         + ", ".join(f"{s} {fmt_r(r)}" for s, r in top))
        if loss_syms2:
            bot = sorted(loss_syms2.items(), key=lambda x: x[1])[:5]
            lines.append("- **Stocks losers (7d):** "
                         + ", ".join(f"{s} {fmt_r(r)}" for s, r in bot))
    else:
        lines.append("- _no closed stocks A/B in last 7d_")
    lines.append("")
    return lines


def section_top_risks() -> list[str]:
    lines = [
        "## 7. Top Risks",
        "",
        "### Crypto risks",
        "",
        "- **P1** — BTC/ETH range/transition regime: breadth EMA50 only ~22%, edge is narrow. Treat broad longs cautiously.",
        "- **P1** — Crypto scalp mode is **low-confidence** (1W/7L over 14d, PF 0.14); entry edge real but TP/horizon mismatch — see scalp banner.",
        "- **P2** — Short funding still skewed: open shorts on majors face squeeze risk on news pops.",
        "- **P2** — Thin-liquid alt scalps: avoid mid/low-cap shorts without volume confirmation.",
        "- **P2** — Catalyst→symbol mapping partial: news-supported flag is reliable for swing/intraday but not for scalp.",
        "- **P3** — A few crypto reports may carry stale `last_update` if a source 429s; the parallel-fetch fix improved this, monitor next 24h.",
        "",
        "### Stocks risks",
        "",
        "- **P1** — Stocks **swing** paused (12% WR, −30R over 14d); pause stays until C-tier counterfactual reaches 20 closures.",
        "- **P1** — Stocks **invest** newly watchlist-only (0W/7L; same failure mode as swing).",
        "- **P1** — **NVDA / SMCI longs** structurally losing (0/4 + 0/3 in 14d intraday) — treat any fresh A/B long on them with extreme skepticism.",
        "- **P2** — A-tier stocks lifetime WR 18.8% (mostly the failed pre-pause swing/invest A's); intraday A-tier sample too small to grade post-pause.",
        "- **P2** — Earnings calendar: confirm `severity != UNKNOWN` before acting; the ETF-UNKNOWN false-positive fix should hold but spot-check.",
        "- **P2** — Headline/legal risk filter only catches matched RSS items; a fresh out-of-band catalyst can slip through.",
        "- **P3** — Market-closed banner active outside RTH; do not chase pre-market without RTH confirmation.",
        "",
    ]
    return lines


def section_playbook_performance(db: sqlite3.Connection) -> list[str]:
    """Compact 14d Playbook Performance Snapshot.

    Buckets by playbook label (mode × asset × direction × news) and reports
    PF / WR / netR. Read-only.
    """
    cutoff = iso_minus_hours(datetime.now(timezone.utc), 24 * 14)
    rows = db.execute(
        """
        SELECT ps.asset_class, ps.mode, ps.direction, ps.tier,
               ps.score, ps.news_supported,
               so.final_outcome, so.final_r
        FROM proposed_signals ps
        LEFT JOIN signal_outcomes so
          ON so.signal_id = ps.signal_id
         AND so.id = (SELECT MAX(id) FROM signal_outcomes WHERE signal_id = ps.signal_id)
        WHERE ps.tier IN ('A','B') AND ps.created_at >= ?
        """,
        (cutoff,),
    ).fetchall()

    def stat(filter_fn) -> tuple[int, int, int, str, str, int]:
        sub = [r for r in rows if filter_fn(r)]
        wins = [r for r in sub if r["final_outcome"] == "win"]
        losses = [r for r in sub if r["final_outcome"] == "loss"]
        closed = wins + losses
        net = sum((r["final_r"] or 0) for r in closed)
        wR = sum((r["final_r"] or 0) for r in wins)
        lR = abs(sum((r["final_r"] or 0) for r in losses)) or 1e-9
        pf = (wR / lR) if losses else (float("inf") if wins else 0.0)
        wr = (len(wins) / len(closed) * 100) if closed else 0.0
        pf_s = "∞" if pf == float("inf") else (f"{pf:.2f}" if pf else "—")
        wr_s = f"{wr:.0f}%" if closed else "—"
        return len(sub), len(closed), len(wins), pf_s, wr_s, int(net)

    rows_out: list[tuple[str, tuple]] = [
        ("`crypto_swing_narrative_rs_momentum` (long)",
         stat(lambda r: r["asset_class"] == "crypto" and r["mode"] == "swing" and r["direction"] == "long")),
        ("`crypto_intraday_catalyst_or_momentum` (catalyst=1)",
         stat(lambda r: r["asset_class"] == "crypto" and r["mode"] == "intraday" and r["news_supported"] == 1)),
        ("`crypto_intraday_catalyst_or_momentum` (no catalyst)",
         stat(lambda r: r["asset_class"] == "crypto" and r["mode"] == "intraday" and not r["news_supported"])),
        ("`crypto_scalp_momentum_continuation` (low-confidence)",
         stat(lambda r: r["asset_class"] == "crypto" and r["mode"] == "scalp")),
        ("`crypto_failed_bounce_short`",
         stat(lambda r: r["asset_class"] == "crypto" and r["direction"] == "short")),
        ("`stocks_intraday_rth_momentum` (long)",
         stat(lambda r: r["asset_class"] == "stocks" and r["mode"] == "intraday" and r["direction"] == "long")),
        ("`stocks_intraday_rth_momentum` (short)",
         stat(lambda r: r["asset_class"] == "stocks" and r["mode"] == "intraday" and r["direction"] == "short")),
        ("`stocks_swing_watchlist_rs_rotation` (DEPRECATED/REMOVED)",
         stat(lambda r: r["asset_class"] == "stocks" and r["mode"] == "swing")),
        ("`stocks_invest_watchlist_30d_thesis` (DEPRECATED/REMOVED)",
         stat(lambda r: r["asset_class"] == "stocks" and r["mode"] == "invest")),
    ]
    # Build sized R for each cohort (reporting-only, see config/sizing_weights.yaml).
    try:
        from src.signals.sizing import size_decision
        all_rows_for_sizing = db.execute(
            """
            SELECT ps.asset_class, ps.mode, ps.tier, ps.direction, ps.news_supported,
                   so.final_r
            FROM proposed_signals ps
            LEFT JOIN signal_outcomes so
              ON so.signal_id = ps.signal_id
             AND so.id = (SELECT MAX(id) FROM signal_outcomes WHERE signal_id = ps.signal_id)
            WHERE ps.tier IN ('A','B') AND ps.created_at >= ?
              AND so.final_r IS NOT NULL
            """,
            (cutoff,),
        ).fetchall()
        decisions = [size_decision(dict(r)) for r in all_rows_for_sizing]
        sized_total = sum((d.sized_r or 0) for d in decisions)
        raw_total = sum((d.raw_r or 0) for d in decisions)
    except Exception:
        sized_total = None
        raw_total = None

    lines = ["## 8b. Playbook Performance Snapshot (14d, A/B, deduped)", ""]
    if sized_total is not None:
        lines.append(
            f"_Raw R total: **{raw_total:+.1f}R** · "
            f"playbook-aware sized total: **{sized_total:+.1f}R** "
            f"(see [reports/PROFITABILITY_LEVERS_AUDIT.md]; weights: "
            f"`config/sizing_weights.yaml`)._"
        )
        lines.append("")
    lines.append("_R/PF columns = LEGACY TOUCH R (optimistic highest-TP-touched) — NOT PnL. "
                 "Authoritative PnL is USD net (`paper_portfolio_ledger.net_pnl_usdt`) in the app._")
    lines.append("")
    lines.append("| Playbook | n | closed | W | WR | PF(leg) | legacyTouchR |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|")
    for name, s in rows_out:
        n, closed, w, pf, wr, net = s
        lines.append(f"| {name} | {n} | {closed} | {w} | {wr} | {pf} | {net:+d} |")
    lines.append("")
    lines.append("Source: deduped `proposed_signals × latest signal_outcomes`, 14d. "
                 "See [reports/STRATEGY_PLAYBOOK_AUDIT.md] for the full per-playbook contract.")
    lines.append("")
    return lines


def section_mode_routing() -> list[str]:
    return [
        "## 8. Mode Routing Status",
        "",
        "### Crypto",
        "- **scalp** — ✅ active (annotated `low confidence`). Reason: real entry edge (100% expired with positive MFE, avg +0.54R) but TP1/2h horizon mismatch — capture limited.",
        "- **intraday** — ✅ actionable. Catalyst-backed intraday strongly outperforms (PF 2.75) vs no-catalyst (PF 0.70).",
        "- **swing** — ✅ actionable. Strongest mode: 12W/3L 14d, PF 9.00, +24R; catalyst not required.",
        "",
        "### Stocks",
        "- **intraday** — ✅ actionable. +84R / PF 2.17 / WR 56% over 14d B-tier.",
        "- **swing** — 🛑 watchlist-only. Pre-pause 5W/36L (12% WR, −30R); pause cap = `stocks_swing_paused_after_48h_audit`.",
        "- **invest** — 🛑 watchlist-only (new, 2026-06-09). 0W/7L 14d; cap = `stocks_invest_paused_after_mode_viability_audit`. Same failure mode as swing.",
        "",
    ]


def section_performance(db: sqlite3.Connection) -> list[str]:
    now = datetime.now(timezone.utc)
    cuts = {
        "48h": iso_minus_hours(now, 48),
        "7d": iso_minus_hours(now, 24 * 7),
        "14d": iso_minus_hours(now, 24 * 14),
    }
    lines = ["## 9. Performance Snapshot", ""]
    for window, cutoff in cuts.items():
        lines.append(f"### Window: {window}")
        for ac, ac_label in (("crypto", "Crypto"), ("stocks", "Stocks")):
            rows = deduped_signal_rows(db, since=cutoff, asset_class=ac)
            ab = [r for r in rows if r["tier"] in ("A", "B")]
            if not ab:
                lines.append(f"- {ac_label}: no A/B signals in window")
                continue
            lines.append(f"- **{ac_label} A/B overall:** {fmt_stats(slice_stats(ab))}")
            # By mode
            modes = sorted({r["mode"] for r in ab})
            for m in modes:
                sub = [r for r in ab if r["mode"] == m]
                lines.append(f"  - {m}: {fmt_stats(slice_stats(sub))}")
            # By direction
            longs = [r for r in ab if r["direction"] == "long"]
            shorts = [r for r in ab if r["direction"] == "short"]
            if longs:
                lines.append(f"  - long: {fmt_stats(slice_stats(longs))}")
            if shorts:
                lines.append(f"  - short: {fmt_stats(slice_stats(shorts))}")
            # By news (crypto only — stocks rarely populates it)
            if ac == "crypto":
                ns1 = [r for r in ab if r["news_supported"] == 1]
                ns0 = [r for r in ab if not r["news_supported"]]
                if ns1:
                    lines.append(f"  - news=1: {fmt_stats(slice_stats(ns1))}")
                if ns0:
                    lines.append(f"  - news=0: {fmt_stats(slice_stats(ns0))}")
            else:
                # Stocks: tier split
                a_only = [r for r in ab if r["tier"] == "A"]
                b_only = [r for r in ab if r["tier"] == "B"]
                if a_only:
                    lines.append(f"  - A-tier: {fmt_stats(slice_stats(a_only))}")
                if b_only:
                    lines.append(f"  - B-tier: {fmt_stats(slice_stats(b_only))}")
        lines.append("")
    return lines


def section_manual_review(db: sqlite3.Connection) -> list[str]:
    # Items the user should inspect
    items: list[str] = []

    # Open trades near stop / near TP / MFE rich
    rows = db.execute(
        """
        SELECT ps.signal_id, ps.asset_class, ps.symbol, ps.direction, ps.mode, ps.tier,
               ps.entry_low, ps.entry_high, ps.stop_loss, ps.invalidation,
               ps.tp1,
               so.max_favorable_excursion_r, so.max_adverse_excursion_r,
               so.entry_triggered, so.tp1_hit, so.stop_hit
        FROM proposed_signals ps
        LEFT JOIN signal_outcomes so
          ON so.signal_id = ps.signal_id
         AND so.id = (SELECT MAX(id) FROM signal_outcomes WHERE signal_id = ps.signal_id)
        WHERE ps.tier IN ('A','B')
          AND (so.final_outcome IS NULL OR so.final_outcome = 'not_triggered')
        ORDER BY ps.created_at DESC
        """
    ).fetchall()
    near_stop = [r for r in rows if (r["max_adverse_excursion_r"] or 0) <= -0.7 and not r["stop_hit"]]
    near_tp = [r for r in rows if (r["max_favorable_excursion_r"] or 0) >= 1.5 and not r["tp1_hit"]]
    mfe_no_tp = [r for r in rows if r["mode"] == "scalp" and (r["max_favorable_excursion_r"] or 0) >= 0.5 and not r["tp1_hit"]]

    def _dedupe_sym_mode(rows: list, fmt) -> list[str]:
        seen: set[tuple[str, str]] = set()
        out: list[str] = []
        for r in rows:
            key = (r["symbol"], r["mode"])
            if key in seen:
                continue
            seen.add(key)
            out.append(fmt(r))
        return out

    if near_stop:
        items.append("**Open trades near stop (MAE ≤ −0.7R):** " +
                     ", ".join(_dedupe_sym_mode(near_stop, lambda r: f"{r['symbol']} ({r['mode']})")[:8]))
    if near_tp:
        items.append("**Open trades near TP (MFE ≥ +1.5R, TP1 not hit):** " +
                     ", ".join(_dedupe_sym_mode(near_tp, lambda r: f"{r['symbol']} ({r['mode']})")[:8]))
    if mfe_no_tp:
        items.append("**Scalp trades with positive MFE but no TP1:** " +
                     ", ".join(_dedupe_sym_mode(mfe_no_tp, lambda r: f"{r['symbol']} (MFE {r['max_favorable_excursion_r']:.2f}R)")[:8]))

    # Stocks A-tier still actionable? Dedupe by symbol+mode at SQL level.
    a_tier_active = db.execute(
        """
        SELECT DISTINCT ps.symbol, ps.mode FROM proposed_signals ps
        LEFT JOIN signal_outcomes so
          ON so.signal_id = ps.signal_id
         AND so.id = (SELECT MAX(id) FROM signal_outcomes WHERE signal_id = ps.signal_id)
        WHERE ps.asset_class='stocks' AND ps.tier='A'
          AND (so.final_outcome IS NULL OR so.final_outcome = 'not_triggered')
        """
    ).fetchall()
    if a_tier_active:
        items.append("**Stocks A-tier active candidates (manual gut-check):** " +
                     ", ".join(f"{r['symbol']} ({r['mode']})" for r in a_tier_active[:8]))

    # NVDA/SMCI active longs — dedupe symbol+mode+tier
    nvda_smci = db.execute(
        """
        SELECT DISTINCT ps.symbol, ps.mode, ps.tier FROM proposed_signals ps
        LEFT JOIN signal_outcomes so
          ON so.signal_id = ps.signal_id
         AND so.id = (SELECT MAX(id) FROM signal_outcomes WHERE signal_id = ps.signal_id)
        WHERE ps.symbol IN ('NVDA','SMCI') AND ps.direction='long' AND ps.tier IN ('A','B')
          AND (so.final_outcome IS NULL OR so.final_outcome = 'not_triggered')
        """
    ).fetchall()
    if nvda_smci:
        items.append("**NVDA/SMCI longs active (historically losing — extra scrutiny):** " +
                     ", ".join(f"{r['symbol']} ({r['mode']}, {r['tier']})" for r in nvda_smci))

    lines = ["## 10. Manual Review Checklist", ""]
    if items:
        for it in items:
            lines.append(f"- {it}")
    else:
        lines.append("- _Nothing flagged automatically. Still spot-check open trades visually._")
    lines.extend([
        "",
        "Always also verify by hand:",
        "- Open trades where the chart structure no longer matches the system thesis.",
        "- Any signal with legal/headline/earnings risk in news feed.",
        "- Any thin-liquid crypto short (squeeze risk).",
        "- Any signal where TradingView shows a different regime than the report.",
        "",
    ])
    return lines


def section_low_risk_diagnostics(db: sqlite3.Connection) -> list[str]:
    """4 additive read-only panels: skipped opps / expired-MFE / short caution / cluster ranking.

    Never suppresses an alert; never changes a number above. Pulls live aggregates from DB.
    """
    lines = ["## 12. Low-Risk Diagnostics (additive, read-only)", ""]

    # Panel 1 — Skipped opportunity monitor (last 14d)
    skipped = db.execute("""
        SELECT COUNT(*) AS n, primary_reason
        FROM rejected_ideas
        WHERE created_at >= datetime('now', '-14 days')
        GROUP BY primary_reason ORDER BY n DESC LIMIT 5
    """).fetchall()
    c_count = db.execute("""
        SELECT COUNT(*) FROM proposed_signals
        WHERE tier='C' AND created_at >= datetime('now', '-14 days')
    """).fetchone()[0]
    promoted = db.execute("""
        SELECT COUNT(DISTINCT r.symbol)
        FROM rejected_ideas r
        JOIN proposed_signals ps ON ps.symbol = r.symbol AND ps.tier IN ('A','B')
        WHERE r.created_at >= datetime('now', '-14 days') AND ps.created_at > r.created_at
    """).fetchone()[0]
    lines.append("### 12a. Skipped opportunity monitor (last 14d)")
    lines.append("")
    lines.append(f"- C-tier signals: **{c_count}** (0× weight, never produced sized R).")
    lines.append(f"- Rejected ideas whose symbol LATER became A/B: **{promoted}** distinct symbols (= skip reversal candidates).")
    lines.append("- Top skip reasons:")
    for r in skipped:
        lines.append(f"  - {(r['primary_reason'] or '')[:80]}: **{r['n']}**")
    lines.append("- Detail: see [reports/SKIPPED_SIGNAL_OPPORTUNITY_AUDIT.md] + `reports/SKIPPED_SIGNAL_FOLLOWUP.csv`")
    lines.append("")

    # Panel 2 — Expired positive-MFE
    exp_pos = db.execute("""
        SELECT COUNT(*) AS n
        FROM proposed_signals ps
        JOIN (SELECT signal_id, MAX(id) AS mid FROM signal_outcomes GROUP BY signal_id) m
          ON m.signal_id = ps.signal_id
        JOIN signal_outcomes o ON o.id = m.mid
        WHERE ps.tier IN ('A','B') AND o.entry_triggered = 1
          AND o.final_outcome = 'expired' AND o.max_favorable_excursion_r > 0.05
    """).fetchone()[0]
    exp_strong = db.execute("""
        SELECT COUNT(*) AS n
        FROM proposed_signals ps
        JOIN (SELECT signal_id, MAX(id) AS mid FROM signal_outcomes GROUP BY signal_id) m
          ON m.signal_id = ps.signal_id
        JOIN signal_outcomes o ON o.id = m.mid
        WHERE ps.tier IN ('A','B') AND o.entry_triggered = 1
          AND o.final_outcome = 'expired' AND o.max_favorable_excursion_r >= 0.5
    """).fetchone()[0]
    lines.append("### 12b. Expired positive-MFE monitor")
    lines.append("")
    lines.append(f"- A/B trades expired with positive MFE (>+0.05R): **{exp_pos}**")
    lines.append(f"- Of those, MFE ≥ +0.5R (potential partial-TP candidates): **{exp_strong}**")
    lines.append(f"- Theoretical partial @+0.5R uplift: ≈ **+{exp_strong * 0.25:.1f}R** (50% × 0.5R × n)")
    lines.append(f"- Winner-cut risk: see [reports/EXPIRED_POSITIVE_MFE_OPPORTUNITY_AUDIT.md] — research only, no TP change.")
    lines.append("")

    # Panel 3 — Crypto intraday short caution
    short_total = db.execute("""
        SELECT COUNT(*) FROM proposed_signals
        WHERE asset_class='crypto' AND mode='intraday' AND direction='short' AND tier IN ('A','B')
    """).fetchone()[0]
    short_no_news = db.execute("""
        SELECT COUNT(*) FROM proposed_signals
        WHERE asset_class='crypto' AND mode='intraday' AND direction='short' AND tier IN ('A','B')
          AND COALESCE(news_supported,0) = 0
    """).fetchone()[0]
    short_loss_r = db.execute("""
        SELECT COALESCE(SUM(o.final_r), 0)
        FROM proposed_signals ps
        JOIN (SELECT signal_id, MAX(id) AS mid FROM signal_outcomes GROUP BY signal_id) m
          ON m.signal_id = ps.signal_id
        JOIN signal_outcomes o ON o.id = m.mid
        WHERE ps.asset_class='crypto' AND ps.mode='intraday' AND ps.direction='short'
          AND ps.tier IN ('A','B') AND COALESCE(ps.news_supported,0) = 0
    """).fetchone()[0]
    lines.append("### 12c. Crypto intraday short caution")
    lines.append("")
    lines.append(f"- Total A/B crypto intraday shorts: **{short_total}**")
    lines.append(f"- No-news shorts: **{short_no_news}** (caution label candidates)")
    lines.append(f"- Realized R from no-news shorts (closed): **{short_loss_r:+.1f}R**")
    lines.append("- Caution label only; no hard filter — see [reports/CRYPTO_INTRADAY_SHORT_CAUTION_STUDY.md].")
    lines.append("")

    # Panel 4 — Stocks cluster ranking
    today_clusters = db.execute("""
        SELECT DATE(ps.created_at) AS d, COUNT(*) AS n
        FROM proposed_signals ps
        WHERE ps.asset_class='stocks' AND ps.mode='intraday' AND ps.tier IN ('A','B')
          AND ps.created_at >= datetime('now', '-1 days')
        GROUP BY d
    """).fetchall()
    today_count = today_clusters[0]["n"] if today_clusters else 0
    lines.append("### 12d. Stocks intraday cluster ranking")
    lines.append("")
    lines.append(f"- A/B stocks intraday signals in last 24h: **{today_count}**")
    lines.append("- Cluster rank is **additive** (`#N/M` shown per signal); no alert suppression.")
    lines.append("- Per-day ranking by cluster: see [reports/STOCKS_INTRADAY_CLUSTER_RANKING_AUDIT.md].")
    lines.append("")
    return lines


def section_manual_live_shadow_cockpit(db: sqlite3.Connection) -> list[str]:
    """§13 — Manual Live Shadow Cockpit.

    Additive only. Surfaces the operator-facing snapshot:
    open / waiting / today P&L / 48h P&L / allowed candidates / cautions /
    Telegram sync / journal pointer.
    """
    lines = ["## 13. Manual Live Shadow Cockpit", ""]
    lines.append("_Operator-facing snapshot. Manual shadow only — auto-execution forbidden._")
    lines.append("")
    # 1. Open paper trades
    open_n = db.execute("""
        SELECT COUNT(*) FROM proposed_signals ps
        JOIN (SELECT signal_id, MAX(id) AS mid FROM signal_outcomes GROUP BY signal_id) m
          ON m.signal_id = ps.signal_id
        JOIN signal_outcomes o ON o.id = m.mid
        WHERE ps.tier IN ('A','B') AND o.entry_triggered = 1
          AND (o.final_outcome IS NULL OR o.final_outcome NOT IN ('win','loss','expired'))
    """).fetchone()[0]
    # 2. Waiting
    wait_n = db.execute("""
        SELECT COUNT(*) FROM proposed_signals ps
        WHERE ps.tier IN ('A','B') AND ps.status IN ('waiting_for_entry','not_triggered','pending','generated')
          AND ps.created_at >= datetime('now', '-1 days')
    """).fetchone()[0]
    # 3. Last paper-entry alerts
    pe_today = db.execute("""
        SELECT COUNT(*) FROM signal_alerts
        WHERE alert_type='paper_entry' AND DATE(sent_at) = DATE('now')
    """).fetchone()[0]
    pe_48h = db.execute("""
        SELECT COUNT(*) FROM signal_alerts
        WHERE alert_type='paper_entry' AND sent_at >= datetime('now', '-2 days')
    """).fetchone()[0]
    # 4. Today P&L
    today_r = db.execute("""
        SELECT COALESCE(SUM(o.final_r), 0)
        FROM proposed_signals ps
        JOIN (SELECT signal_id, MAX(id) AS mid FROM signal_outcomes GROUP BY signal_id) m
          ON m.signal_id = ps.signal_id
        JOIN signal_outcomes o ON o.id = m.mid
        WHERE ps.tier IN ('A','B') AND DATE(ps.created_at) = DATE('now')
          AND o.final_outcome IN ('win','loss','expired')
    """).fetchone()[0]
    # 5. 48h P&L
    r48 = db.execute("""
        SELECT COALESCE(SUM(o.final_r), 0)
        FROM proposed_signals ps
        JOIN (SELECT signal_id, MAX(id) AS mid FROM signal_outcomes GROUP BY signal_id) m
          ON m.signal_id = ps.signal_id
        JOIN signal_outcomes o ON o.id = m.mid
        WHERE ps.tier IN ('A','B') AND ps.created_at >= datetime('now', '-2 days')
          AND o.final_outcome IN ('win','loss','expired')
    """).fetchone()[0]
    # 8. Stale / moved-away
    stale_n = db.execute("""
        SELECT COUNT(*) FROM proposed_signals
        WHERE tier IN ('A','B') AND status IN ('stale_before_entry','entry_moved_away')
          AND created_at >= datetime('now', '-2 days')
    """).fetchone()[0]
    # 9. Telegram sync
    tg_failed = db.execute("""
        SELECT COUNT(*) FROM signal_alerts
        WHERE alert_type='paper_entry' AND sent_at >= datetime('now', '-2 days')
          AND telegram_status NOT IN ('sent','dry_run')
    """).fetchone()[0]
    tg_status = "✅ OK" if tg_failed == 0 else f"⚠️ {tg_failed} failed sends"

    lines.append(f"- Open paper trades: **{open_n}**")
    lines.append(f"- Waiting setups (valid): **{wait_n}**")
    lines.append(f"- Stale / moved-away (do NOT manual-fill): **{stale_n}**")
    lines.append(f"- Paper-entry alerts today: **{pe_today}** · last 48h: **{pe_48h}**")
    lines.append(f"- Today legacy-touch R (optimistic · NOT PnL): **{today_r:+.1f}R**")
    lines.append(f"- 48h legacy-touch R (optimistic · NOT PnL): **{r48:+.1f}R**")
    lines.append("  - _Authoritative PnL = USD net (gross − fees − slippage − funding) from "
                 "`paper_portfolio_ledger.net_pnl_usdt`; realistic R = `paper_execution_r` "
                 "(control-plane app). The R above is the legacy highest-TP-touched metric._")
    lines.append(f"- Telegram sync: {tg_status}")
    lines.append("")
    lines.append("### Top allowed manual-shadow candidates (active or waiting)")
    candidates = db.execute("""
        SELECT ps.symbol, ps.asset_class, ps.mode, ps.tier, ps.direction, ps.score,
               ps.status, o.entry_triggered, o.entry_triggered_at, ps.expires_at
        FROM proposed_signals ps
        LEFT JOIN (SELECT signal_id, MAX(id) AS mid FROM signal_outcomes GROUP BY signal_id) m
          ON m.signal_id = ps.signal_id
        LEFT JOIN signal_outcomes o ON o.id = m.mid
        WHERE ps.tier IN ('A','B') AND ps.created_at >= datetime('now', '-1 days')
          AND (ps.status IN ('waiting_for_entry','triggered') OR o.entry_triggered = 1)
          AND NOT (ps.asset_class='stocks' AND ps.mode='invest')
          AND NOT (
              ps.asset_class='stocks' AND ps.mode='swing'
              AND COALESCE(ps.raw_idea_json,'') NOT LIKE '%stocks_swing_event_rs_pullback_quality_paper_v1%'
              AND COALESCE(ps.raw_idea_json,'') NOT LIKE '%stocks_swing_event_rs_pullback_flow_paper_v1%'
          )
          AND NOT (ps.asset_class='crypto' AND ps.mode='scalp')  -- 2026-06-15: scalp shadow-only
        ORDER BY ps.score DESC LIMIT 5
    """).fetchall()
    if candidates:
        lines.append("")
        lines.append("| Symbol | Asset | Mode | Tier | Dir | Score | Status |")
        lines.append("|---|---|---|---|---|---:|---|")
        for c in candidates:
            lines.append(f"| {c['symbol']} | {c['asset_class']} | {c['mode']} | {c['tier']} | "
                         f"{c['direction']} | {(c['score'] or 0):.1f} | {c['status'] or 'unknown'} |")
    else:
        lines.append("- _none right now_")
    lines.append("")
    lines.append("### Forbidden / caution")
    lines.append("- `crypto_scalp_momentum_continuation` — **SHADOW ONLY (0× sized weight)**. "
                 "Generated for research only; do NOT mirror manually. 12m backtest net-negative "
                 "after fees — see [reports/SCALP_KEEP_REWORK_DISABLE_DECISION.md]")
    lines.append("- `stocks_swing_watchlist_rs_rotation` — DEPRECATED/REMOVED (0×; never sized; not paused-to-return)")
    lines.append("- `stocks_invest_watchlist_30d_thesis` — DEPRECATED/REMOVED (0×; never sized; not paused-to-return)")
    lines.append("- `stocks_swing_growth_breakout` — NEW shadow-only research framework (separate; not actionable/sized)")
    lines.append("- Crypto intraday no-news shorts — caution per [reports/CRYPTO_INTRADAY_SHORT_CAUTION_STUDY.md]")
    lines.append("- All C-tier / shadow / expansion candidates")
    lines.append("")
    lines.append("### Journal")
    lines.append("- [`reports/LIVE_SHADOW_TRADING_JOURNAL.md`](../reports/LIVE_SHADOW_TRADING_JOURNAL.md)")
    lines.append("- [`reports/LIVE_SHADOW_TRADING_JOURNAL.csv`](../reports/LIVE_SHADOW_TRADING_JOURNAL.csv) — preserves manual decision / fill / R / notes columns across refreshes")
    lines.append("- Today's verdict: [`reports/MANUAL_LIVE_SHADOW_TODAY_VERDICT.md`](../reports/MANUAL_LIVE_SHADOW_TODAY_VERDICT.md)")
    lines.append("")
    return lines


def section_catalyst_visibility(db: sqlite3.Connection) -> list[str]:
    """§14 — Catalyst / derivatives visibility (additive, display-only).

    Catalyst-backed vs technical split, funding/OI archive status, stocks
    catalyst labelling status, derived-label distribution. Does NOT change
    any performance calculation.
    """
    lines = ["## 14. Catalyst & Derivatives Visibility (additive)", ""]
    # Catalyst-backed vs technical (crypto A/B closed)
    rows = db.execute("""
        SELECT ps.news_supported, COUNT(*),
               SUM(CASE WHEN o.final_r > 0 THEN 1 ELSE 0 END),
               ROUND(SUM(o.final_r), 1)
        FROM proposed_signals ps
        JOIN (SELECT signal_id, MAX(id) AS mid FROM signal_outcomes GROUP BY signal_id) m
          ON m.signal_id = ps.signal_id
        JOIN signal_outcomes o ON o.id = m.mid
        WHERE ps.asset_class='crypto' AND ps.tier IN ('A','B')
          AND o.final_outcome IN ('win','loss','expired')
        GROUP BY ps.news_supported
    """).fetchall()
    lines.append("### 14a. Catalyst-backed vs technical (crypto A/B, closed)")
    lines.append("")
    lines.append("| news_supported | n | wins | raw R |")
    lines.append("|---|---:|---:|---:|")
    for r in rows:
        lbl = "1 (catalyst-backed)" if r[0] else "0 (technical-only)"
        lines.append(f"| {lbl} | {r[1]} | {r[2]} | {r[3]} |")
    lines.append("")
    # Funding/OI archive status
    try:
        fcount = db.execute("SELECT COUNT(*) FROM funding_snapshots").fetchone()[0]
        ocount = db.execute("SELECT COUNT(*) FROM oi_snapshots").fetchone()[0]
    except sqlite3.OperationalError:
        fcount = ocount = 0
    lines.append("### 14b. Funding/OI archive status")
    lines.append("")
    lines.append(f"- funding_snapshots rows: **{fcount}** · oi_snapshots rows: **{ocount}**")
    lines.append("- Append-only; written best-effort each crypto report cycle. NOT read by scoring.")
    lines.append("")
    # Stocks catalyst labelling status
    stk_ns = db.execute("""
        SELECT COUNT(*) FROM proposed_signals
        WHERE asset_class='stocks' AND news_supported=1
    """).fetchone()[0]
    lines.append("### 14c. Stocks catalyst labelling")
    lines.append("")
    lines.append(f"- Stocks signals now labelled news_supported=1: **{stk_ns}** "
                 f"(forward-only; flag fix landed 2026-06-15).")
    lines.append("")
    # Derived label distribution
    try:
        fr = dict(db.execute(
            "SELECT catalyst_freshness, COUNT(*) FROM signal_catalyst_labels GROUP BY catalyst_freshness"
        ).fetchall())
        dv = dict(db.execute(
            "SELECT derivatives_label, COUNT(*) FROM signal_catalyst_labels GROUP BY derivatives_label"
        ).fetchall())
        lines.append("### 14d. Derived catalyst labels (signal_catalyst_labels)")
        lines.append("")
        lines.append(f"- freshness: {fr}")
        lines.append(f"- derivatives: {dv}")
        lines.append("- Display-only derived table; safe to rebuild. See [reports/CATALYST_LABEL_BACKFILL_REPORT.md].")
    except sqlite3.OperationalError:
        lines.append("_signal_catalyst_labels not yet built._")
    lines.append("")
    return lines


def section_footer() -> list[str]:
    return [
        "---",
        "",
        f"_Page generated: `{now_iso()}`_  ",
        "_Source: `scripts/write_obsidian_current_state_dashboard.py` — read-only._  ",
        "_Re-run: `python -m scripts.write_obsidian_current_state_dashboard`._",
        "",
    ]


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def _compute_freshness(db: sqlite3.Connection) -> dict:
    """Compute newest-DB-row vs now delta for the header banner."""
    rows = db.execute(
        """
        SELECT MAX(ts) FROM (
          SELECT MAX(created_at) as ts FROM proposed_signals
          UNION ALL
          SELECT MAX(updated_at) as ts FROM proposed_signals
          UNION ALL
          SELECT MAX(checked_at) as ts FROM signal_outcomes
          UNION ALL
          SELECT MAX(sent_at) as ts FROM signal_alerts
        )
        """
    ).fetchone()
    newest_iso = rows[0] if rows else None
    if not newest_iso:
        return {"newest_db_iso": "—", "data_age_minutes": None}
    try:
        s = newest_iso.replace("Z", "+00:00")
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        age_min = (datetime.now(timezone.utc) - dt).total_seconds() / 60.0
        return {
            "newest_db_iso": dt.strftime("%Y-%m-%d %H:%M UTC"),
            "data_age_minutes": max(0.0, age_min),
        }
    except Exception:
        return {"newest_db_iso": str(newest_iso)[:16], "data_age_minutes": None}


def build_page() -> str:
    """Return the full markdown body for the Current State pinned tab.

    Importable from `scripts/refresh_obsidian_dashboard.py` so the page
    refreshes on every scheduler cycle alongside the other 📌 tabs.
    """
    db = open_db()
    try:
        procs = probe_processes()
        health_lines, status = section_health(procs, db)
        freshness = _compute_freshness(db)
        parts: list[str] = []
        parts += section_header(now_eest_str(), status, freshness=freshness)
        parts += health_lines
        parts += section_open_trades(db)
        parts += section_recent_trades(db, "crypto", 5)
        parts += section_recent_trades(db, "stocks", 5)
        parts += section_events_today()
        parts += section_events_week(db)
        parts += section_top_risks()
        parts += section_mode_routing()
        parts += section_playbook_performance(db)
        parts += section_performance(db)
        parts += section_manual_review(db)
        parts += section_low_risk_diagnostics(db)
        parts += section_manual_live_shadow_cockpit(db)
        parts += section_catalyst_visibility(db)
        parts += section_footer()
        return "\n".join(parts) + "\n"
    finally:
        db.close()


def main() -> int:
    if not DB_PATH.exists():
        print(f"ERROR: DB missing: {DB_PATH}", file=sys.stderr)
        return 2
    text = build_page()
    PAGE.parent.mkdir(parents=True, exist_ok=True)
    PAGE.write_text(text, encoding="utf-8")
    print(f"OK — wrote {PAGE.name} ({len(text)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
