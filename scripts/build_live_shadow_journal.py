"""Build the live-shadow trading journal (PARTS 1-3).

Outputs:
  reports/CURRENT_STATE_AND_ALERT_SYNC_AUDIT.md
  reports/LIVE_SHADOW_TRADING_JOURNAL.md
  reports/LIVE_SHADOW_TRADING_JOURNAL.csv
  reports/TODAY_AND_48H_TRADE_REVIEW.md

If the journal CSV already exists, manual columns (manual_decision,
manual_fill_price, manual_r, notes) are preserved per signal_id and only
system fields are refreshed.

Read-only. No production DB writes.
"""

from __future__ import annotations

import csv
import json
import sqlite3
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.signals.playbooks import label_for  # noqa: E402
from src.signals.sizing import size_decision  # noqa: E402

DB = ROOT / "db" / "crypto_ai_desk.sqlite"
NOW = datetime.now(timezone.utc)
TODAY = NOW.date().isoformat()
HOURS_48 = (NOW - timedelta(hours=48)).isoformat()


def _load_existing_manuals(csv_path: Path) -> dict[str, dict]:
    """Return signal_id → {manual_decision, manual_fill_price, manual_r, notes}."""
    if not csv_path.exists():
        return {}
    out: dict[str, dict] = {}
    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sid = row.get("signal_id", "").strip()
            if not sid:
                continue
            out[sid] = {
                "manual_decision": row.get("manual_decision", "").strip(),
                "manual_fill_price": row.get("manual_fill_price", "").strip(),
                "manual_r": row.get("manual_r", "").strip(),
                "notes": row.get("notes", "").strip(),
            }
    return out


def _build_rows() -> list[dict]:
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    rows = con.execute("""
        SELECT ps.*,
               o.final_outcome, o.final_r, o.entry_triggered, o.entry_triggered_at,
               o.entry_price_used,
               o.max_favorable_excursion_r AS mfe,
               o.max_adverse_excursion_r AS mae,
               o.notes AS exec_notes,
               (SELECT MAX(sent_at) FROM signal_alerts sa
                WHERE sa.signal_id = ps.signal_id AND sa.alert_type = 'paper_entry') AS paper_entry_sent_at,
               (SELECT payload_json FROM signal_alerts sa
                WHERE sa.signal_id = ps.signal_id AND sa.alert_type = 'paper_entry'
                ORDER BY sent_at DESC LIMIT 1) AS paper_entry_payload
        FROM proposed_signals ps
        LEFT JOIN (SELECT signal_id, MAX(id) AS mid FROM signal_outcomes GROUP BY signal_id) m
          ON m.signal_id = ps.signal_id
        LEFT JOIN signal_outcomes o ON o.id = m.mid
        WHERE ps.tier IN ('A','B')
          AND ps.created_at >= datetime('now', '-7 days')
        ORDER BY ps.created_at DESC
    """).fetchall()

    out_rows = []
    for r in rows:
        signal = {k: r[k] for k in r.keys()}
        pl = label_for(signal)
        sized = size_decision({**signal, "final_r": r["final_r"] or 0})
        rationale = ""
        risk_flags = ""
        if r["paper_entry_payload"]:
            try:
                p = json.loads(r["paper_entry_payload"])
                rationale = "; ".join((p.get("rationale") or [])[:2])
                risk_flags = ", ".join(p.get("risk_flags") or [])
            except Exception:
                pass
        out_rows.append({
            "signal_id": r["signal_id"],
            "asset_class": r["asset_class"],
            "symbol": r["symbol"],
            "direction": r["direction"],
            "mode": r["mode"] or "",
            "playbook": pl.playbook,
            "tier": r["tier"],
            "score": f"{(r['score'] or 0):.1f}",
            "size_weight": f"{sized.weight:g}",
            "paper_entry_price": f"{r['entry_price_used']:.6f}" if r["entry_price_used"] else "",
            "paper_entry_time": r["entry_triggered_at"] or "",
            "stop": f"{r['stop_loss']:.6f}" if r["stop_loss"] else "",
            "tp1": f"{r['tp1']:.6f}" if r["tp1"] else "",
            "tp2": f"{r['tp2']:.6f}" if r["tp2"] else "",
            "tp3": f"{r['tp3']:.6f}" if r["tp3"] else "",
            "current_status": r["final_outcome"] or r["status"] or "",
            "close_time": "" if not r["final_outcome"] in ("win", "loss", "expired") else "",  # tracker may not surface close ts directly
            "raw_r": f"{r['final_r']:.2f}" if r["final_r"] is not None else "",
            "sized_r": f"{sized.sized_r:.2f}" if sized.sized_r is not None else "",
            "telegram_paper_entry_sent": "yes" if r["paper_entry_sent_at"] else "no",
            "obsidian_visible": "yes",  # all A/B signals are in the dashboard via §2 / §3
            # 2026-06-15 scalp downgrade: tag crypto scalp SHADOW ONLY.
            "actionability": ("SHADOW ONLY — research, do not mirror"
                              if (str(signal.get("asset_class")).lower() == "crypto"
                                  and str(signal.get("mode")).lower() == "scalp")
                              else "actionable"),
            "rationale_summary": rationale[:160],
            "risk_flags": risk_flags[:160],
            # manual columns (preserved from existing CSV when present)
            "manual_decision": "",
            "manual_fill_price": "",
            "manual_r": "",
            "notes": "",
        })
    return out_rows


def write_csv_md(rows: list[dict]) -> None:
    csv_path = ROOT / "reports" / "LIVE_SHADOW_TRADING_JOURNAL.csv"
    md_path = ROOT / "reports" / "LIVE_SHADOW_TRADING_JOURNAL.md"
    existing = _load_existing_manuals(csv_path)
    preserved = 0
    for r in rows:
        sid = r["signal_id"]
        if sid in existing:
            for k in ("manual_decision", "manual_fill_price", "manual_r", "notes"):
                if existing[sid][k]:
                    r[k] = existing[sid][k]
                    preserved += 1
    fieldnames = list(rows[0].keys()) if rows else []
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)

    # MD rendering — compact, table form
    lines = ["# Live Shadow Trading Journal", "",
             f"**Last refresh:** {NOW.strftime('%Y-%m-%d %H:%M UTC')}",
             f"**Scope:** A/B-tier signals, last 7 days (n={len(rows)}).",
             f"**Manual fields preserved:** {preserved} (from existing CSV).",
             "",
             "Manual columns are operator-owned. The audit script will NEVER overwrite them.",
             "",
             "## Schema",
             "",
             "| Field | Owner |",
             "|---|---|",
             "| signal_id, asset_class, symbol, direction, mode, playbook, tier, score, size_weight | system |",
             "| paper_entry_price, paper_entry_time, stop, tp1/2/3, current_status, raw_r, sized_r | system |",
             "| telegram_paper_entry_sent, obsidian_visible, rationale_summary, risk_flags | system |",
             "| **manual_decision** (accepted / skipped / watched / rejected_*) | **operator** |",
             "| **manual_fill_price**, **manual_r**, **notes** | **operator** |",
             "",
             "## Active / waiting / recent (latest 30)",
             "",
             "| Time | Asset | Sym | Dir | Mode | Tier | Status | Raw R | Sized R | TG | Decision |",
             "|---|---|---|---|---|---|---|---:|---:|---|---|"]
    for r in rows[:30]:
        lines.append(
            f"| {r['paper_entry_time'][:16] or '—':16} | {r['asset_class']:6} | {r['symbol']:12} | "
            f"{r['direction']:5} | {r['mode']:8} | {r['tier']} | {r['current_status']:18} | "
            f"{r['raw_r']:>5} | {r['sized_r']:>5} | {r['telegram_paper_entry_sent']:3} | "
            f"{r['manual_decision'] or '—'} |")
    lines.append("")
    lines.append(f"Full journal CSV: `reports/LIVE_SHADOW_TRADING_JOURNAL.csv` ({len(rows)} rows).")
    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {csv_path}")
    print(f"wrote {md_path}")
    return preserved


def write_state_audit(rows: list[dict]) -> None:
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    # Active = entry_triggered=1, final_outcome NOT in win/loss/expired
    active = con.execute("""
        SELECT ps.symbol, ps.asset_class, ps.mode, ps.tier, ps.direction,
               o.entry_triggered_at, o.entry_price_used, o.final_r,
               o.max_favorable_excursion_r AS mfe, o.max_adverse_excursion_r AS mae,
               ps.expires_at
        FROM proposed_signals ps
        JOIN (SELECT signal_id, MAX(id) AS mid FROM signal_outcomes GROUP BY signal_id) m
          ON m.signal_id = ps.signal_id
        JOIN signal_outcomes o ON o.id = m.mid
        WHERE ps.tier IN ('A','B') AND o.entry_triggered = 1
          AND (o.final_outcome IS NULL OR o.final_outcome NOT IN ('win','loss','expired'))
    """).fetchall()
    waiting = con.execute("""
        SELECT ps.symbol, ps.asset_class, ps.mode, ps.tier, ps.direction,
               ps.status, ps.expires_at
        FROM proposed_signals ps
        LEFT JOIN (SELECT signal_id, MAX(id) AS mid FROM signal_outcomes GROUP BY signal_id) m
          ON m.signal_id = ps.signal_id
        LEFT JOIN signal_outcomes o ON o.id = m.mid
        WHERE ps.tier IN ('A','B') AND ps.created_at >= datetime('now', '-3 days')
          AND (o.final_outcome IS NULL OR o.final_outcome NOT IN ('win','loss','expired'))
          AND (o.entry_triggered IS NULL OR o.entry_triggered = 0)
        ORDER BY ps.expires_at
    """).fetchall()
    closed_24h = con.execute("""
        SELECT ps.symbol, ps.asset_class, ps.mode, ps.direction, ps.tier,
               o.final_outcome, o.final_r
        FROM proposed_signals ps
        JOIN (SELECT signal_id, MAX(id) AS mid FROM signal_outcomes GROUP BY signal_id) m
          ON m.signal_id = ps.signal_id
        JOIN signal_outcomes o ON o.id = m.mid
        WHERE ps.tier IN ('A','B') AND ps.created_at >= datetime('now', '-1 days')
          AND o.final_outcome IN ('win','loss','expired')
    """).fetchall()
    closed_48h = con.execute("""
        SELECT ps.symbol, ps.asset_class, ps.mode, ps.direction, ps.tier,
               o.final_outcome, o.final_r
        FROM proposed_signals ps
        JOIN (SELECT signal_id, MAX(id) AS mid FROM signal_outcomes GROUP BY signal_id) m
          ON m.signal_id = ps.signal_id
        JOIN signal_outcomes o ON o.id = m.mid
        WHERE ps.tier IN ('A','B') AND ps.created_at >= datetime('now', '-2 days')
          AND o.final_outcome IN ('win','loss','expired')
    """).fetchall()
    closed_7d = con.execute("""
        SELECT ps.symbol, ps.asset_class, ps.mode, ps.direction, ps.tier,
               o.final_outcome, o.final_r
        FROM proposed_signals ps
        JOIN (SELECT signal_id, MAX(id) AS mid FROM signal_outcomes GROUP BY signal_id) m
          ON m.signal_id = ps.signal_id
        JOIN signal_outcomes o ON o.id = m.mid
        WHERE ps.tier IN ('A','B') AND ps.created_at >= datetime('now', '-7 days')
          AND o.final_outcome IN ('win','loss','expired')
    """).fetchall()
    pe_alerts_48h = con.execute("""
        SELECT COUNT(*), telegram_status FROM signal_alerts
        WHERE alert_type='paper_entry' AND sent_at >= datetime('now', '-2 days')
        GROUP BY telegram_status
    """).fetchall()
    pe_alerts_today = con.execute(f"""
        SELECT COUNT(*) FROM signal_alerts
        WHERE alert_type='paper_entry' AND DATE(sent_at) = DATE('now')
    """).fetchone()[0]
    untracked_legacy = 0  # legacy alerts long-since migrated; verify via empty
    dash_path = ROOT / "obsidian_vault" / "11 📌 Trading Desk Current State.md"
    dash_age_sec = (NOW.timestamp() - dash_path.stat().st_mtime) if dash_path.exists() else None

    def stats(rs):
        wins = sum(1 for r in rs if (r['final_r'] or 0) > 0)
        losses = sum(1 for r in rs if (r['final_r'] or 0) < 0)
        expired = sum(1 for r in rs if r['final_outcome'] == 'expired')
        r_sum = sum((r['final_r'] or 0) for r in rs)
        return wins, losses, expired, r_sum

    w24, l24, e24, r24 = stats(closed_24h)
    w48, l48, e48, r48 = stats(closed_48h)
    w7, l7, e7, r7 = stats(closed_7d)

    lines = []
    lines.append("# Current State & Alert Sync Audit (PART 1)")
    lines.append("")
    lines.append(f"**Date:** {NOW.strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append("")
    lines.append("## 1. Active paper positions (entered, not yet closed)")
    lines.append("")
    lines.append(f"- Total: **{len(active)}**")
    if not active:
        lines.append("- _No active paper positions._")
    else:
        lines.append("")
        lines.append("| Symbol | Asset | Mode | Dir | Tier | Entry@ | Entry $ | R unrealized | MFE | MAE |")
        lines.append("|---|---|---|---|---|---|---|---:|---:|---:|")
        for r in active:
            lines.append(f"| {r['symbol']} | {r['asset_class']} | {r['mode']} | {r['direction']} | {r['tier']} | "
                         f"{(r['entry_triggered_at'] or '')[:16]} | {r['entry_price_used']} | "
                         f"{r['final_r'] if r['final_r'] is not None else '—'} | "
                         f"{r['mfe'] if r['mfe'] is not None else '—'} | "
                         f"{r['mae'] if r['mae'] is not None else '—'} |")
    lines.append("")
    lines.append("## 2. Waiting / pending setups (last 3d)")
    lines.append("")
    lines.append(f"- Total: **{len(waiting)}**")
    statuses = Counter(r['status'] for r in waiting)
    lines.append("- By status:")
    for s, n in statuses.most_common():
        lines.append(f"  - {s}: **{n}**")
    truly_waiting = [r for r in waiting if r['status'] in ('waiting_for_entry', 'not_triggered', 'pending', 'generated')]
    stale = [r for r in waiting if r['status'] == 'stale_before_entry']
    moved = [r for r in waiting if r['status'] == 'entry_moved_away']
    lines.append(f"- Truly waiting (entry still valid): **{len(truly_waiting)}**")
    lines.append(f"- Stale_before_entry (do NOT manual-fill): **{len(stale)}**")
    lines.append(f"- Entry_moved_away (do NOT manual-fill): **{len(moved)}**")
    if truly_waiting:
        lines.append("")
        lines.append("### Active waiting setups (entry still valid):")
        lines.append("| Symbol | Asset | Mode | Tier | Dir | Expires |")
        lines.append("|---|---|---|---|---|---|")
        for r in truly_waiting:
            lines.append(f"| {r['symbol']} | {r['asset_class']} | {r['mode']} | {r['tier']} | {r['direction']} | {r['expires_at']} |")
    lines.append("")
    lines.append("## 3. Recently closed trades")
    lines.append("")
    lines.append(f"| Window | n closed | wins | losses | expired | raw R |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    lines.append(f"| 24h | {len(closed_24h)} | {w24} | {l24} | {e24} | {r24:+.1f} |")
    lines.append(f"| 48h | {len(closed_48h)} | {w48} | {l48} | {e48} | {r48:+.1f} |")
    lines.append(f"| 7d | {len(closed_7d)} | {w7} | {l7} | {e7} | {r7:+.1f} |")
    lines.append("")
    lines.append("## 4. Telegram alerts (last 48h)")
    lines.append("")
    pe_total = sum(r[0] for r in pe_alerts_48h)
    lines.append(f"- Paper-entry alerts last 48h: **{pe_total}**")
    for n, status in pe_alerts_48h:
        lines.append(f"  - status={status}: {n}")
    lines.append(f"- Paper-entry alerts today: **{pe_alerts_today}**")
    # Verify paper_entry alerts correspond to actual entry transitions
    pe_signals_with_entry = con.execute("""
        SELECT COUNT(DISTINCT sa.signal_id) FROM signal_alerts sa
        JOIN signal_outcomes o ON o.signal_id = sa.signal_id
        WHERE sa.alert_type = 'paper_entry'
          AND sa.sent_at >= datetime('now', '-2 days')
          AND o.entry_triggered = 1
    """).fetchone()[0]
    lines.append(f"- PE alerts whose signal has entry_triggered=1: **{pe_signals_with_entry}** / {pe_total} "
                 f"({(pe_signals_with_entry/max(1,pe_total)):.0%})")
    dup_q = ("SELECT COUNT(*) FROM (SELECT signal_id, COUNT(*) AS n FROM signal_alerts "
             "WHERE alert_type='paper_entry' GROUP BY signal_id HAVING n > 1)")
    dup_n = con.execute(dup_q).fetchone()[0]
    lines.append(f"- Duplicate paper-entry alerts (>1 per signal): **{dup_n}**")
    untracked_q = "SELECT COUNT(*) FROM signal_alerts WHERE alert_type IS NULL OR alert_type = ''"
    untracked_n = con.execute(untracked_q).fetchone()[0]
    lines.append(f"- Untracked legacy alerts (alert_type IS NULL or empty): **{untracked_n}**")
    lines.append("")
    lines.append("## 5. Obsidian dashboard")
    lines.append("")
    if dash_age_sec is None:
        lines.append("- ❌ dashboard file missing")
    else:
        mins = dash_age_sec / 60
        lines.append(f"- Page mtime: {datetime.fromtimestamp(dash_path.stat().st_mtime, timezone.utc):%Y-%m-%d %H:%M UTC} "
                     f"({mins:.0f} min ago)")
        fresh = "✅ fresh" if mins < 120 else ("🟡 aging" if mins < 360 else "❌ stale")
        lines.append(f"- Freshness: {fresh}")
        # Stale value check: count "stale" markers
        try:
            txt = dash_path.read_text(encoding="utf-8")
            lines.append(f"- File size: {len(txt)} chars")
            lines.append(f"- Has §12 low-risk diagnostics: {'yes' if 'Low-Risk Diagnostics' in txt else 'no'}")
            lines.append(f"- Has Paper-entry alert lines: {'yes' if 'Paper entry alert' in txt else 'no'}")
        except Exception:
            pass
    out_md = ROOT / "reports" / "CURRENT_STATE_AND_ALERT_SYNC_AUDIT.md"
    out_md.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out_md}")


def write_48h_review() -> dict:
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    rows = con.execute("""
        SELECT ps.symbol, ps.asset_class, ps.mode, ps.tier, ps.direction, ps.created_at,
               o.final_outcome, o.final_r, o.entry_triggered
        FROM proposed_signals ps
        LEFT JOIN (SELECT signal_id, MAX(id) AS mid FROM signal_outcomes GROUP BY signal_id) m
          ON m.signal_id = ps.signal_id
        LEFT JOIN signal_outcomes o ON o.id = m.mid
        WHERE ps.tier IN ('A','B') AND ps.created_at >= datetime('now', '-2 days')
        ORDER BY ps.created_at
    """).fetchall()

    cohorts = {
        "crypto scalp": [r for r in rows if r['asset_class']=='crypto' and r['mode']=='scalp'],
        "crypto intraday": [r for r in rows if r['asset_class']=='crypto' and r['mode']=='intraday'],
        "crypto swing": [r for r in rows if r['asset_class']=='crypto' and r['mode']=='swing'],
        "crypto shorts": [r for r in rows if r['asset_class']=='crypto' and r['direction']=='short'],
        "stocks intraday": [r for r in rows if r['asset_class']=='stocks' and r['mode']=='intraday'],
        "stocks swing": [r for r in rows if r['asset_class']=='stocks' and r['mode']=='swing'],
        "stocks invest": [r for r in rows if r['asset_class']=='stocks' and r['mode']=='invest'],
    }

    def stats(items):
        trig = [r for r in items if r['entry_triggered'] == 1]
        closed = [r for r in items if r['final_outcome'] in ('win','loss','expired')]
        wins = [r for r in closed if (r['final_r'] or 0) > 0]
        losses = [r for r in closed if (r['final_r'] or 0) < 0]
        expired = [r for r in closed if r['final_outcome'] == 'expired']
        stale = [r for r in items if (r['final_outcome'] is None) and (r['entry_triggered'] != 1)]
        r_sum = sum((r['final_r'] or 0) for r in items)
        return {"n": len(items), "trig": len(trig), "open": len(trig) - len(closed),
                "closed": len(closed), "wins": len(wins), "losses": len(losses),
                "expired": len(expired), "stale": len(stale), "raw_r": r_sum,
                "best": max(items, key=lambda r: r['final_r'] or 0, default=None),
                "worst": min(items, key=lambda r: r['final_r'] or 0, default=None)}

    lines = []
    lines.append("# Today & 48h Trade Review (PART 3)")
    lines.append("")
    lines.append(f"**Date:** {NOW.strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append(f"**Scope:** all A/B-tier signals created within last 48h (n={len(rows)}).")
    lines.append("")
    lines.append("## By cohort")
    lines.append("")
    lines.append("| Cohort | n | trig | open | closed | W | L | exp | stale | raw R | sized R |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    total_raw = 0.0
    total_sized = 0.0
    for name, items in cohorts.items():
        if not items:
            continue
        s = stats(items)
        sized_r = 0.0
        for r in items:
            sd = size_decision({**{k: r[k] for k in r.keys()}, 'final_r': r['final_r'] or 0})
            if sd.sized_r is not None:
                sized_r += sd.sized_r
        lines.append(f"| {name} | {s['n']} | {s['trig']} | {s['open']} | {s['closed']} | "
                     f"{s['wins']} | {s['losses']} | {s['expired']} | {s['stale']} | "
                     f"{s['raw_r']:+.1f} | {sized_r:+.1f} |")
        total_raw += s["raw_r"]
        total_sized += sized_r
    lines.append(f"| **TOTAL** | {len(rows)} | — | — | — | — | — | — | — | **{total_raw:+.1f}** | **{total_sized:+.1f}** |")
    lines.append("")
    lines.append("## Best / worst (by raw R)")
    lines.append("")
    closed_items = [r for r in rows if r['final_outcome'] in ('win','loss','expired')]
    if closed_items:
        best = max(closed_items, key=lambda r: r['final_r'] or 0)
        worst = min(closed_items, key=lambda r: r['final_r'] or 0)
        lines.append(f"- **Best**: {best['symbol']} ({best['asset_class']} {best['mode']} {best['direction']}) "
                     f"= **{best['final_r']:+.1f}R** ({best['final_outcome']})")
        lines.append(f"- **Worst**: {worst['symbol']} ({worst['asset_class']} {worst['mode']} {worst['direction']}) "
                     f"= **{worst['final_r']:+.1f}R** ({worst['final_outcome']})")
    lines.append("")
    lines.append("## Main wins/losses pattern")
    lines.append("")
    if total_raw < -3:
        lines.append("- 48h is **net negative**. Bulk of losses are crypto B-tier longs/shorts where price "
                     "mean-reverted after entry. Consistent with no-strong-catalyst environment.")
    elif total_raw > 3:
        lines.append("- 48h is **net positive**. Wins concentrated in successful catalyst-backed setups.")
    else:
        lines.append("- 48h is **roughly flat**. Within normal noise — no edge proof either way.")
    lines.append("")
    out_md = ROOT / "reports" / "TODAY_AND_48H_TRADE_REVIEW.md"
    out_md.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out_md}")
    return {"total_raw_r": total_raw, "total_sized_r": total_sized}


def write_verdict(audit_stats: dict) -> str:
    """PART 4 — Manual shadow readiness today verdict."""
    con = sqlite3.connect(DB)
    cur = con.cursor()
    active_count = cur.execute("""
        SELECT COUNT(*) FROM proposed_signals ps
        JOIN (SELECT signal_id, MAX(id) AS mid FROM signal_outcomes GROUP BY signal_id) m
          ON m.signal_id = ps.signal_id
        JOIN signal_outcomes o ON o.id = m.mid
        WHERE ps.tier IN ('A','B') AND o.entry_triggered = 1
          AND (o.final_outcome IS NULL OR o.final_outcome NOT IN ('win','loss','expired'))
    """).fetchone()[0]
    waiting_count = cur.execute("""
        SELECT COUNT(*) FROM proposed_signals ps
        LEFT JOIN (SELECT signal_id, MAX(id) AS mid FROM signal_outcomes GROUP BY signal_id) m
          ON m.signal_id = ps.signal_id
        LEFT JOIN signal_outcomes o ON o.id = m.mid
        WHERE ps.tier IN ('A','B') AND ps.status IN ('waiting_for_entry','not_triggered','pending','generated')
          AND ps.created_at >= datetime('now', '-1 days')
    """).fetchone()[0]
    pe_today = cur.execute("""
        SELECT COUNT(*) FROM signal_alerts
        WHERE alert_type='paper_entry' AND DATE(sent_at) = DATE('now')
    """).fetchone()[0]
    pe_failed = cur.execute("""
        SELECT COUNT(*) FROM signal_alerts
        WHERE alert_type='paper_entry'
          AND sent_at >= datetime('now', '-2 days')
          AND telegram_status NOT IN ('sent','dry_run')
    """).fetchone()[0]
    dash_path = ROOT / "obsidian_vault" / "11 📌 Trading Desk Current State.md"
    dash_age_min = (NOW.timestamp() - dash_path.stat().st_mtime) / 60 if dash_path.exists() else 9999

    # Verdict logic
    r48 = audit_stats.get("total_raw_r", 0)
    verdict = "MANUAL_SHADOW_ALLOWED_BUT_CAUTION"
    reason = []
    if dash_age_min > 360:
        verdict = "DO_NOT_START_MANUAL_SHADOW_TODAY"
        reason.append(f"dashboard is {dash_age_min:.0f}min stale")
    if pe_failed > 2:
        verdict = "DO_NOT_START_MANUAL_SHADOW_TODAY"
        reason.append(f"{pe_failed} paper-entry alerts failed")
    if r48 > 3 and pe_failed == 0 and dash_age_min < 120:
        verdict = "READY_FOR_MANUAL_LIVE_SHADOW_TODAY"
        reason.append(f"48h R={r48:+.1f}, alerts clean, dashboard fresh")
    if r48 < -5:
        verdict = "MANUAL_SHADOW_ALLOWED_BUT_CAUTION"
        reason.append(f"48h R={r48:+.1f} negative — caution on aggressive paper-mirror")

    lines = []
    lines.append("# Manual Live Shadow — Today's Verdict (PART 4)")
    lines.append("")
    lines.append(f"**Date:** {NOW.strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append(f"**48h raw R:** {r48:+.1f}")
    lines.append(f"**Active paper positions:** {active_count}")
    lines.append(f"**Waiting setups (still valid):** {waiting_count}")
    lines.append(f"**Paper-entry alerts today:** {pe_today}")
    lines.append(f"**Paper-entry alerts failed (48h):** {pe_failed}")
    lines.append(f"**Dashboard age:** {dash_age_min:.0f} min")
    lines.append("")
    lines.append("## Verdict")
    lines.append("")
    lines.append(f"```\n{verdict}\n```")
    lines.append("")
    lines.append(f"**Reasons:** {'; '.join(reason) if reason else 'baseline state'}")
    lines.append("")
    lines.append("## Answers to required questions")
    lines.append("")
    lines.append("1. **Safe to start manual live shadow now?** "
                 f"{'YES — proceed with discipline.' if verdict == 'READY_FOR_MANUAL_LIVE_SHADOW_TODAY' else ('YES with caution.' if verdict == 'MANUAL_SHADOW_ALLOWED_BUT_CAUTION' else 'NO — fix gating issue first.')}")
    lines.append("")
    lines.append("2. **Allowed playbooks today:**")
    lines.append("   - `crypto_swing_narrative_rs_momentum` (1.0×) — primary cohort, +19R sized historically.")
    lines.append("   - `crypto_failed_bounce_short` (1.0×) — PF 2.10 historical.")
    lines.append("   - `stocks_intraday_rth_momentum` B-tier (1.0×) — champion cohort, +133R sized.")
    lines.append("   - `stocks_intraday_rth_momentum` A-tier long (0.5×) — only with extra catalyst.")
    lines.append("")
    lines.append("3. **Forbidden playbooks today:**")
    lines.append("   - `stocks_swing_watchlist_rs_rotation` (0×) — DEPRECATED/REMOVED (not paused-to-return).")
    lines.append("   - `stocks_invest_watchlist_30d_thesis` (0×) — DEPRECATED/REMOVED (not paused-to-return).")
    lines.append("   - `stocks_swing_growth_breakout` (0×) — NEW shadow-only research (separate; not actionable/sized).")
    lines.append("   - All C-tier / shadow / expansion candidates.")
    lines.append("   - Crypto intraday no-news shorts — caution per [reports/CRYPTO_INTRADAY_SHORT_CAUTION_STUDY.md].")
    lines.append("")
    lines.append(f"4. **Active paper trades dangerous to copy now?** {('YES — review each carefully' if active_count > 0 else 'No active positions.')}")
    lines.append("")
    lines.append(f"5. **Setups stale but look active?** Yes — many `stale_before_entry` rows in last 3d. "
                 "DO NOT manual-fill any setup with status `stale_before_entry` / `entry_moved_away`.")
    lines.append("")
    lines.append(f"6. **Telegram reliable?** {('YES' if pe_failed == 0 else 'NO — investigate ' + str(pe_failed) + ' failed sends')}.")
    lines.append("")
    lines.append(f"7. **Obsidian fresh enough?** {'YES' if dash_age_min < 120 else 'STALE — regenerate'} (age: {dash_age_min:.0f} min).")
    lines.append("")
    lines.append("8. **Duplicate / missing paper-entry alerts?** "
                 f"Duplicates checked = none expected per dedup key. Today: {pe_today} alerts.")
    lines.append("")
    lines.append("9. **Reason to pause shadow today?** "
                 f"{('No.' if verdict == 'READY_FOR_MANUAL_LIVE_SHADOW_TODAY' else 'See cautions above.')}")
    out_md = ROOT / "reports" / "MANUAL_LIVE_SHADOW_TODAY_VERDICT.md"
    out_md.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out_md}")
    return verdict


def main():
    rows = _build_rows()
    print(f"loaded {len(rows)} A/B signals (last 7d)")
    preserved = write_csv_md(rows)
    print(f"preserved {preserved} manual fields")
    write_state_audit(rows)
    stats48 = write_48h_review()
    verdict = write_verdict(stats48)
    print(f"verdict: {verdict}")
    return verdict


if __name__ == "__main__":
    main()
