"""Markdown report for the Stocks Position Framework (shadow-only research).

No fabricated profitability: until the outcome engine is wired, outcomes render as
"pending / outcome unavailable" rather than fake numbers. Authoritative profitability is USD net.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from .config import _ROOT
from . import shadow_store, PLAYBOOK

REPORT_PATH = _ROOT / "reports" / "stocks_position_framework_latest.md"

BANNER = (
    "> **SHADOW ONLY — research candidates.** No actionability · no live / auto-live / manual-live · "
    "no Telegram · not sized in the paper book. The old stocks swing/invest playbooks "
    "(`stocks_swing_watchlist_rs_rotation`, `stocks_invest_watchlist_30d_thesis`) are "
    "**deprecated/removed** — not paused-to-return. Authoritative profitability = **USD net PnL**; "
    "legacy final_r is diagnostic only."
)


def _fmt(v: Any, nd: int = 2, dash: str = "—") -> str:
    try:
        return dash if v is None else f"{float(v):.{nd}f}"
    except (TypeError, ValueError):
        return str(v) if v is not None else dash


def _market_line(market: dict) -> str:
    if not market:
        return "Market: _unavailable_"
    vix = _fmt(market.get("vix"), 1)
    return (f"Market regime: **{market.get('label', 'unknown')}** · "
            f"SPY>50D={market.get('spy_above_50d')} · SPY>200D={market.get('spy_above_200d')} · "
            f"QQQ>50D={market.get('qqq_above_50d')} · VIX={vix}")


def _candidate_rows(cands: list[dict]) -> str:
    if not cands:
        return "_No qualifying candidates in the latest scan._\n"
    head = ("| Symbol | Setup | Score | Entry | Stop | TP1 (R) | TP2 (R) | Risk $ | Sector | "
            "RS·SPY | Near-high % | Earnings |\n"
            "|---|---|---:|---:|---:|---:|---:|---:|---|---:|---:|---|\n")
    lines = []
    for c in cands:
        rp = c.get("risk_plan") or {}
        stop = c.get("stop_price", rp.get("stop_price"))
        tp1 = c.get("tp1", rp.get("tp1")); tp1r = c.get("tp1_r", rp.get("tp1_r"))
        tp2 = c.get("tp2", rp.get("tp2")); tp2r = c.get("tp2_r", rp.get("tp2_r"))
        risk_usd = c.get("risk_usd", rp.get("risk_usd"))
        rs = c.get("rs_spy")
        rs_s = "—" if rs is None else f"{float(rs)*100:+.1f}%"
        lines.append(
            f"| {c.get('symbol')} | {c.get('setup_variant')} | {_fmt(c.get('score'), 0)} | "
            f"{_fmt(c.get('entry_price'))} | {_fmt(stop)} | {_fmt(tp1)} ({_fmt(tp1r, 1)}) | "
            f"{_fmt(tp2)} ({_fmt(tp2r, 1)}) | {_fmt(risk_usd)} | {c.get('sector') or '—'} | "
            f"{rs_s} | {_fmt(c.get('near_high_pct'), 1)} | {c.get('earnings_risk') or '—'} |")
    return head + "\n".join(lines) + "\n"


def _runbook_block(cfg: dict, db_path=None) -> str:
    """Operator/forward-audit status: scheduler state, latest scan, stored candidates, outcome
    counts, small-sample warning, and the explicit no-conclusion statement."""
    sched = bool((cfg or {}).get("scheduler_enabled", False))
    try:
        scan_t = shadow_store.latest_scan_time(db_path=db_path)
        stored = len(shadow_store.latest_candidates(limit=100000, only_open=True, db_path=db_path))
        outs = shadow_store.latest_outcomes(limit=100000, db_path=db_path)
    except Exception:
        scan_t, stored, outs = None, 0, []
    closed = [o for o in outs if o.get("status") == "closed"]
    pending = [o for o in outs if o.get("status") == "pending"]
    no_entry = [o for o in outs if o.get("status") == "no_entry"]
    gate = (cfg or {}).get("evidence_gate") or {}
    min_trades = int(gate.get("min_forward_trades", 30))
    lines = [
        "### Runbook / status (forward-audit)", "",
        f"- scheduler_enabled: **{sched}**" + ("" if sched else "  _(manual `stocks-position-scan` only)_"),
        f"- latest scan (UTC): `{scan_t or 'none yet'}`",
        f"- candidates stored (open): **{stored}**",
        f"- outcomes: closed **{len(closed)}** · pending **{len(pending)}** · no-entry **{len(no_entry)}**",
    ]
    if not sched:
        lines.append("- ⚠️ scheduler disabled — no automatic forward accumulation yet.")
    if len(closed) < min_trades:
        lines.append(f"- ⚠️ sample too small: {len(closed)} closed < {min_trades} required for any read.")
    lines += ["", f"> **No profitability conclusion** until ≥{min_trades} forward candidates have "
              "resolved through the outcome engine in **USD net**. Backfill is not proof."]
    return "\n".join(lines)


def _outcomes_section(db_path=None) -> str:
    try:
        outcomes = shadow_store.latest_outcomes(limit=100000, db_path=db_path)
    except Exception:
        outcomes = []
    closed = [o for o in outcomes if o.get("status") == "closed" and o.get("net_pnl_usd") is not None]
    if not outcomes:
        return ("### Outcomes\n\n_No outcomes computed yet — run `stocks-position-outcome-refresh`. "
                "Outcomes render **pending / unavailable** until real USD-net fills exist "
                "(no fake fills)._\n")
    metrics = ""
    if closed:
        nets = [float(o["net_pnl_usd"]) for o in closed]
        wins = sum(1 for x in nets if x > 0)
        gross_win = sum(x for x in nets if x > 0)
        gross_loss = abs(sum(x for x in nets if x < 0))
        pf = round(gross_win / gross_loss, 3) if gross_loss > 0 else "∞"
        metrics = (f"\n**USD net (closed n={len(closed)}):** total ${sum(nets):.2f} · "
                   f"avg ${sum(nets)/len(nets):.2f} · winrate {wins/len(nets):.0%} · PF {pf}\n")
    head = ("| Candidate | Status | Net $ | Paper-exec R | MFE R | MAE R | Hold d |\n"
            "|---|---|---:|---:|---:|---:|---:|\n")
    rows = [f"| {o.get('candidate_id')} | {o.get('status')} | {_fmt(o.get('net_pnl_usd'))} | "
            f"{_fmt(o.get('paper_execution_r'), 2)} | {_fmt(o.get('max_favorable_excursion_r'), 2)} | "
            f"{_fmt(o.get('max_adverse_excursion_r'), 2)} | {_fmt(o.get('holding_days'), 0)} |"
            for o in outcomes]
    return ("### Outcomes\n\n> USD net is authoritative; `paper_execution_r` is auxiliary. Rows with "
            "NULL PnL are still open/pending (not zero).\n" + metrics + "\n" + head + "\n".join(rows) + "\n")


def _evidence_gate(cfg: dict) -> str:
    g = (cfg or {}).get("evidence_gate") or {}
    if not g:
        return ""
    return ("### Promotion / evidence gate (NOT met — shadow only)\n\n"
            f"- min forward days: {g.get('min_forward_days', 28)}\n"
            f"- min forward trades: {g.get('min_forward_trades', 30)}\n"
            f"- require net USD positive: {g.get('require_net_usd_positive', True)}\n"
            f"- require better than old stocks swing: {g.get('require_better_than_old_stocks_swing', True)}\n"
            f"- require drawdown acceptable: {g.get('require_drawdown_acceptable', True)}\n\n"
            "Nothing here becomes actionable/live until this gate passes on FORWARD data **and** the "
            "operator signs off. Backfill is not proof.\n")


def render_scan(result, cfg: dict) -> str:
    """Render a just-completed ScanResult (used by stocks-position-scan)."""
    passed = getattr(result, "passed", []) or []
    rejected = getattr(result, "rejected", []) or []
    parts = [
        f"# Stocks Position Framework — {PLAYBOOK} (shadow research)",
        "", BANNER, "",
        f"- Scan time (UTC): `{getattr(result, 'created_at', '—')}`",
        f"- Universe: {getattr(result, 'universe_size', 0)} · scanned: {getattr(result, 'scanned', 0)} · "
        f"candidates: **{len(passed)}** · rejected: {len(rejected)}"
        + ("  _(dry-run — not persisted)_" if getattr(result, "dry_run", False) else ""),
        f"- {_market_line(getattr(result, 'market', {}))}",
        "", "### Candidates", "", _candidate_rows(passed),
    ]
    if passed:
        top = passed[0]
        parts += ["#### Top candidate thesis", "",
                  f"**{top.get('symbol')}** ({top.get('setup_variant')}): {top.get('thesis', '')}",
                  "", f"_Counter-thesis:_ {top.get('counter_thesis', '')}", ""]
    if rejected:
        shown = rejected[:12]
        parts.append("### Rejected (sample)\n")
        for r in shown:
            reasons = ", ".join((r.get("rejection_reasons") or [])[:3]) or "—"
            parts.append(f"- {r.get('symbol')}: {reasons}")
        parts.append("")
    parts += [_runbook_block(cfg), "", _outcomes_section(), "", _evidence_gate(cfg)]
    return "\n".join(p for p in parts if p is not None)


def render_from_store(cfg: dict, *, limit: int = 25, db_path=None) -> str:
    """Render the latest stored candidates/outcomes (used by stocks-position-report)."""
    cands = shadow_store.latest_candidates(limit=limit, only_open=True, db_path=db_path)
    scan_time = shadow_store.latest_scan_time(db_path=db_path)
    market = {}  # market snapshot isn't persisted per-candidate; keep the report honest about that
    parts = [
        f"# Stocks Position Framework — {PLAYBOOK} (shadow research)",
        "", BANNER, "",
        f"- Latest scan (UTC): `{scan_time or '—'}`",
        f"- Stored open candidates: **{len(cands)}**",
        "", "### Candidates", "", _candidate_rows(cands),
        _runbook_block(cfg, db_path=db_path), "",
        _outcomes_section(db_path=db_path), "", _evidence_gate(cfg),
    ]
    return "\n".join(p for p in parts if p is not None)


def ascii_summary(cfg: dict, *, limit: int = 25, db_path=None) -> str:
    """Plain-ASCII stdout summary (safe for a Windows cp1252 console — no emoji / >= / arrows).
    The full (unicode) Markdown still goes to the report file via write_report()."""
    try:
        cands = shadow_store.latest_candidates(limit=limit, only_open=True, db_path=db_path)
        scan_t = shadow_store.latest_scan_time(db_path=db_path)
        outs = shadow_store.latest_outcomes(limit=100000, db_path=db_path)
    except Exception:
        cands, scan_t, outs = [], None, []
    closed = [o for o in outs if o.get("status") == "closed"]
    pending = [o for o in outs if o.get("status") == "pending"]
    no_entry = [o for o in outs if o.get("status") == "no_entry"]
    sched = bool((cfg or {}).get("scheduler_enabled", False))
    mt = int(((cfg or {}).get("evidence_gate") or {}).get("min_forward_trades", 30))
    lines = [
        f"Stocks Position Framework -- SHADOW ONLY ({PLAYBOOK})",
        "  no live / no auto-live / no manual-live / no Telegram / no actionability; USD net authoritative.",
        f"  scheduler_enabled={sched}  latest_scan={scan_t or 'none yet'}  open_candidates={len(cands)}",
        f"  outcomes: closed={len(closed)} pending={len(pending)} no_entry={len(no_entry)}",
    ]
    for c in cands[:limit]:
        rp = c.get("risk_plan") or {}
        lines.append(
            f"  - {c.get('symbol')} {c.get('setup_variant')} score={_fmt(c.get('score'), 0)} "
            f"entry={_fmt(c.get('entry_price'))} stop={_fmt(c.get('stop_price', rp.get('stop_price')))} "
            f"tp1={_fmt(c.get('tp1', rp.get('tp1')))}")
    closed_metric = ""
    if closed:
        nets = [float(o["net_pnl_usd"]) for o in closed if o.get("net_pnl_usd") is not None]
        if nets:
            closed_metric = f" | USD net total={sum(nets):.2f} avg={sum(nets)/len(nets):.2f}"
    lines.append(f"  No profitability conclusion until >= {mt} forward candidates resolve in USD net; "
                 f"backfill is not proof.{closed_metric}")
    return "\n".join(lines)


def write_report(markdown: str, path: str | Path | None = None) -> Path:
    p = Path(path) if path else REPORT_PATH
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(markdown, encoding="utf-8")
    return p
