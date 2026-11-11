"""Shadow news-impact evaluation (2026-07-03) — READ-ONLY, does NOT change trading.

For each recent signal it derives news/catalyst tags from `news_items` (+ `events` for earnings) in
the 24h BEFORE the signal, then joins the authoritative forward paper outcome
(`paper_execution_outcomes.paper_execution_r`) and reports edge (net_r / winrate / profit-factor) by
tag. This is the evidence layer that shows WHICH news tags actually help or hurt — but it never
changes any signal, score, tier, or routing. A future threshold could be tested in paper/shadow only.
"""
from __future__ import annotations

import json
import sqlite3
from typing import Any

from src.config import load_config
from src.execution.paper_execution_accounting import EVIDENCE_FORWARD, EVIDENCE_BACKFILL

# forward_postfreeze trades needed (with + without combined) before a tag verdict may be read as
# "improves edge" / "hurts edge" rather than INSUFFICIENT_FORWARD_SAMPLE — mirrors the existing
# >=10/>=10 with/without threshold below.
MIN_FORWARD_FOR_VERDICT = 10

PRIMARY_SOURCES = {"Binance Announcements", "SEC EDGAR", "SEC EDGAR Filings",
                   "t.me/binance_announcements", "t.me/Bybit_Announcements", "t.me/MEXCEnglish"}
PR_WIRES = {"PR Newswire", "PRNewswire", "Business Wire", "BusinessWire", "GlobeNewswire", "GlobeNewswire (Stocks)"}
_LEGAL_KW = ("sec ", "lawsuit", "settlement", "charged", "fraud", "investigation", "subpoena", "doj", "8-k")
_BULL = ("beats", "surge", "approval", "upgrade", "record", "partnership", "buyback", "wins", "soars")
_BEAR = ("miss", "downgrade", "probe", "lawsuit", "recall", "cuts", "warns", "plunge", "halts", "delist")


def _conn(db):
    c = sqlite3.connect(db or str(load_config().db_path))
    c.row_factory = sqlite3.Row
    return c


def _base(sym: str) -> str:
    return str(sym or "").split("/")[0].strip().upper()


def _news_features(conn, symbol: str, created_at: str, asset_class: str) -> dict[str, Any]:
    base = _base(symbol)
    if not base or not created_at:
        return {}
    like = f'%"{base}/%' if str(asset_class).startswith(("crypto",)) or "/" in str(symbol) else f'%"{base}"%'
    try:
        rows = [dict(r) for r in conn.execute(
            "SELECT source, title, importance, published_at FROM news_items "
            "WHERE detected_symbols_json LIKE ? AND published_at <= ? "
            "AND published_at >= datetime(?, '-24 hours') ORDER BY published_at DESC LIMIT 40",
            (like, created_at, created_at)).fetchall()]
    except sqlite3.OperationalError:
        rows = []
    fresh = bool(rows)
    primary = any((r["source"] in PRIMARY_SOURCES) or ((r["importance"] or 0) >= 2.0) for r in rows)
    press = any(r["source"] in PR_WIRES for r in rows)
    legal = any(any(k in (r["title"] or "").lower() for k in _LEGAL_KW) for r in rows) \
        or any("sec" in str(r["source"]).lower() or "edgar" in str(r["source"]).lower() for r in rows)
    titles = " ".join((r["title"] or "").lower() for r in rows)
    bull = any(k in titles for k in _BULL)
    bear = any(k in titles for k in _BEAR)
    direction = ("mixed" if bull and bear else "bullish" if bull else "bearish" if bear else "unknown")
    # earnings risk: an earnings event for this ticker within ±3 days of the signal
    earn = False
    try:
        earn = conn.execute(
            "SELECT 1 FROM events WHERE event_type='earnings' AND upper(ticker)=? "
            "AND ABS(julianday(event_date) - julianday(?)) <= 3 LIMIT 1", (base, created_at)).fetchone() is not None
    except sqlite3.OperationalError:
        earn = False
    quality = "primary" if primary else ("secondary" if fresh else "none")
    return {"had_fresh_news_24h": fresh, "had_primary_source_24h": primary,
            "had_press_release_24h": press, "had_sec_or_legal_risk": legal,
            "had_earnings_risk": earn, "news_source_quality_bucket": quality,
            "catalyst_direction": direction}


def evaluate(db: str | None = None, *, lookback_days: int = 60, limit: int = 900) -> dict[str, Any]:
    conn = _conn(db)
    try:
        conn.execute("SELECT 1 FROM paper_execution_outcomes LIMIT 1")
    except sqlite3.OperationalError:
        conn.close()
        return {"available": False, "reason": "paper_execution_outcomes not populated"}
    try:
        has_evidence = any(r[1] == "evidence_class"
                          for r in conn.execute("PRAGMA table_info(paper_execution_outcomes)"))
        evidence_col = "o.evidence_class" if has_evidence else "NULL"
        sigs = [dict(r) for r in conn.execute(
            "SELECT p.signal_id, p.symbol, p.created_at, p.asset_class, p.mode, p.tier, p.direction, "
            f"o.paper_execution_r AS r, {evidence_col} AS evidence_class FROM proposed_signals p "
            "JOIN paper_execution_outcomes o ON o.signal_id = p.signal_id "
            "WHERE o.paper_execution_r IS NOT NULL AND p.created_at >= datetime('now', ?) "
            "ORDER BY p.created_at DESC LIMIT ?", (f"-{int(lookback_days)} days", int(limit))).fetchall()]
        tagged = []
        for s in sigs:
            feat = _news_features(conn, s["symbol"], s["created_at"], s["asset_class"] or "crypto")
            tagged.append({**s, **feat})
    finally:
        conn.close()

    def _book(rows):
        rs = [float(r["r"]) for r in rows if r.get("r") is not None]
        wins = [x for x in rs if x > 0]
        losses = [x for x in rs if x < 0]
        gl, gw = abs(sum(losses)), sum(wins)
        pf = (gw / gl) if gl > 0 else (float("inf") if wins else None)
        fwd = [r for r in rows if r.get("evidence_class") == EVIDENCE_FORWARD]
        return {"n": len(rs), "net_r": round(sum(rs), 2),
                "winrate": round(len(wins) / len(rs), 3) if rs else None,
                "avg_r": round(sum(rs) / len(rs), 3) if rs else None,
                "profit_factor": (round(pf, 2) if isinstance(pf, float) and pf != float("inf") else pf),
                "forward_n": len(fwd)}

    def _evidence_bucket(rows, cls_or_none):
        sub = [r for r in rows if (r.get("evidence_class") == cls_or_none if cls_or_none else
                                   r.get("evidence_class") not in (EVIDENCE_FORWARD, EVIDENCE_BACKFILL))]
        b = _book(sub)
        return {"n": b["n"], "resolved": b["n"], "net_r_sum": b["net_r"]}

    def _split(key, truthy):
        yes = [t for t in tagged if truthy(t.get(key))]
        no = [t for t in tagged if not truthy(t.get(key))]
        return {"with": _book(yes), "without": _book(no)}

    bool_tags = ["had_fresh_news_24h", "had_primary_source_24h", "had_press_release_24h",
                 "had_sec_or_legal_risk", "had_earnings_risk"]
    by_tag = {k: _split(k, lambda v: bool(v)) for k in bool_tags}
    by_quality = {q: _book([t for t in tagged if t.get("news_source_quality_bucket") == q])
                  for q in ("primary", "secondary", "none")}
    by_direction = {d: _book([t for t in tagged if t.get("catalyst_direction") == d])
                    for d in ("bullish", "bearish", "mixed", "unknown")}
    # edge deltas (with − without) for each boolean tag, to see which tags help/hurt.
    # "improves edge"/"hurts edge" is a promote/disable-style claim, so it must be backed by
    # forward_postfreeze evidence (Model F) — backfill_pretrained is the same in-sample data that
    # chose Model F's own thresholds and must never be read as proof by itself.
    verdicts = []
    for k, sp in by_tag.items():
        w, wo = sp["with"], sp["without"]
        if (w["n"] or 0) >= 10 and (wo["n"] or 0) >= 10 and w["avg_r"] is not None and wo["avg_r"] is not None:
            d = round(w["avg_r"] - wo["avg_r"], 3)
            fwd_n = (w.get("forward_n") or 0) + (wo.get("forward_n") or 0)
            if fwd_n < MIN_FORWARD_FOR_VERDICT:
                reading = "INSUFFICIENT_FORWARD_SAMPLE"
            else:
                reading = "improves edge" if d > 0.05 else "hurts edge" if d < -0.05 else "noise"
            verdicts.append({"tag": k, "delta_avg_r": d, "with_n": w["n"], "without_n": wo["n"],
                             "forward_n": fwd_n, "reading": reading})
    verdicts.sort(key=lambda x: x["delta_avg_r"], reverse=True)
    evidence_summary = {"forward_postfreeze": _evidence_bucket(tagged, EVIDENCE_FORWARD),
                        "backfill_pretrained": _evidence_bucket(tagged, EVIDENCE_BACKFILL),
                        "unclassified": _evidence_bucket(tagged, None)}
    return {"available": True, "lookback_days": lookback_days, "signals_evaluated": len(tagged),
            "by_tag": by_tag, "by_source_quality": by_quality, "by_catalyst_direction": by_direction,
            "tag_edge_verdicts": verdicts, "evidence_summary": evidence_summary,
            "note": "SHADOW/DIAGNOSTIC ONLY. paper_execution_r is authoritative paper-R. Nothing here "
                    "changes signals, score, tier, routing or live. A future news threshold could be "
                    "tested in paper/shadow only, with operator sign-off. Only forward_postfreeze "
                    "(Model F) is provable edge — backfill_pretrained is in-sample hypothesis only."}


def render_markdown(e: dict) -> str:
    if not e.get("available"):
        return f"## News shadow-impact evaluation\n- unavailable ({e.get('reason')})"
    lines = [f"## News shadow-impact evaluation (last {e['lookback_days']}d, "
             f"{e['signals_evaluated']} signals; paper_execution_r)"]
    lines.append("")
    ev = e.get("evidence_summary") or {}
    if ev:
        fwd = ev.get("forward_postfreeze") or {}; bfd = ev.get("backfill_pretrained") or {}
        unc = ev.get("unclassified") or {}
        lines.append("**Evidence quality (Model F):** only forward_postfreeze is proof of edge — "
                     "backfill_pretrained is the in-sample data that chose Model F's own thresholds "
                     "and must never be read as \"profitable\" on its own.")
        lines.append(f"- forward_postfreeze: n={fwd.get('n', 0)}, resolved={fwd.get('resolved', 0)}, "
                     f"netR={fwd.get('net_r_sum', 0):+.2f}")
        lines.append(f"- backfill_pretrained: n={bfd.get('n', 0)}, resolved={bfd.get('resolved', 0)}, "
                     f"netR={bfd.get('net_r_sum', 0):+.2f}")
        lines.append(f"- unclassified/null: n={unc.get('n', 0)}")
        lines.append("")
    lines.append("**Which news tags help / hurt edge (avg R with − without):**")
    for v in e["tag_edge_verdicts"]:
        lines.append(f"- {v['tag']}: Δavg {v['delta_avg_r']:+.3f}R (n {v['with_n']}/{v['without_n']}, "
                     f"forward_n={v.get('forward_n', 0)}) → {v['reading']}")
    if not e["tag_edge_verdicts"]:
        lines.append("- not enough paired samples yet (need ≥10 with and without per tag)")
    lines.append("")
    lines.append("**By source quality bucket:**")
    for q, b in e["by_source_quality"].items():
        lines.append(f"- {q}: n {b['n']} · net {b['net_r']}R · WR "
                     f"{int(b['winrate']*100) if b['winrate'] is not None else '—'}% · PF {b['profit_factor']}")
    lines.append("")
    lines.append(f"_{e['note']}_")
    return "\n".join(lines)
