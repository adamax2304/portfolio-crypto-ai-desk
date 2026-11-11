"""PART 1 — Telegram daily paper-shadow A/B summary (composer, dry-run by default).

Composes a once-daily message from the FORWARD window (the only valid evidence) + a one-line
backfill hypothesis with a clear caveat. Does NOT spam per-trade. Sending reuses the existing
Telegram notifier when creds exist; otherwise compose-only (dry-run).
"""
from __future__ import annotations

from src.execution.paper_shadow_monitor import forward_by_mode, forward_quality, promotion_gate


def compose(db: str | None = None, include_top_examples: bool = True) -> str:
    fq = forward_quality(db)
    if not fq.get("available"):
        return "📊 Paper-Shadow A/B — lane not yet populated."
    A, B = fq["A"], fq["B"]
    g = promotion_gate(db)
    passed = sum(1 for c in g.get("criteria", []) if c["ok"])
    total = len(g.get("criteria", []))
    sign = lambda x: ("+" if x >= 0 else "") + str(round(x, 2))
    modes = [m for m in forward_by_mode(db) if (m["a_t"] + m["b_t"]) > 0]
    best = modes[0] if modes else None
    worst = modes[-1] if modes else None
    mk_rate = fq.get("maker_fill_rate")
    lines = [
        "📊 *Paper-Shadow A/B* — daily (FORWARD = valid evidence)",
        f"window: {fq.get('forward_days') or 0}d · forward signals {fq.get('forward_signals', 0)}",
        f"A (old): {A['trades']}t · {sign(A['net_r'])}R · ${sign(A['net_usd'])} · fee ${A['fees_usd']}",
        f"B (new): {B['trades']}t · {sign(B['net_r'])}R · ${sign(B['net_usd'])} · fee ${B['fees_usd']}",
        f"Δ: {sign(fq['delta_net_r'])}R · ${sign(fq['delta_net_usd'])}",
    ]
    if include_top_examples and best:
        lines.append(f"best B mode: {best['mode']} {sign(best['delta_r'])}R · "
                     f"worst: {worst['mode']} {sign(worst['delta_r'])}R")
    lines += [
        f"maker fill {mk_rate if mk_rate is not None else '—'}% "
        f"(posted {fq.get('maker_posted', 0)} · missed {fq.get('maker_missed', 0)} · "
        f"taker-fb {fq.get('maker_taker_fallback', 0)})",
        f"B: missed {fq['B_missed']} · no-chase {fq['B_skipped']} · dir-flips {fq['B_dir_flips']} · "
        f"DATA_GAP excl {fq['data_gap_excluded']}",
        f"B max-DD {B['max_drawdown_r']}R vs A {A['max_drawdown_r']}R · B fee-drag {B['fee_drag_r']}R",
        f"promotion gate: *{g['verdict']}* ({passed}/{total}) — evaluation only, no auto-promote",
    ]
    if fq.get("warnings"):
        lines.append("⚠ " + " · ".join(fq["warnings"]))
    lines.append("_backfill is look-ahead — a hypothesis, NOT proof. Decide on FORWARD only._")
    return "\n".join(lines)


def send_daily(dry_run: bool = True, db: str | None = None, include_top_examples: bool = True) -> dict:
    msg = compose(db, include_top_examples=include_top_examples)
    if dry_run:
        return {"sent": False, "dry_run": True, "message": msg}
    try:
        from pathlib import Path
        from src.notifiers.trade_telegram import notifier_for
        notifier_for(Path(__file__).resolve().parents[2]).send(msg, parse_mode="")
        return {"sent": True, "dry_run": False, "message": msg}
    except Exception as e:
        return {"sent": False, "dry_run": False, "error": str(e), "message": msg}


# --- once-daily scheduler entrypoint (idempotent; safe to call every cycle) -------------------
_CFG_PATH = "config/paper_shadow_digest.yaml"
_STATE_PATH = "data/.paper_shadow_digest_last.txt"


def _load_digest_cfg() -> dict:
    import os

    import yaml
    try:
        with open(_CFG_PATH, encoding="utf-8") as f:
            return (yaml.safe_load(f) or {}).get("paper_shadow_telegram_digest", {}) or {}
    except Exception:
        return {}


def _last_sent_date() -> str | None:
    try:
        with open(_STATE_PATH, encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return None


def _record_sent(date_str: str) -> None:
    import os
    try:
        os.makedirs(os.path.dirname(_STATE_PATH), exist_ok=True)
        with open(_STATE_PATH, "w", encoding="utf-8") as f:
            f.write(date_str)
    except Exception:
        pass


def send_daily_if_due(db: str | None = None, now=None, force: bool = False, dry_run: bool = False) -> dict:
    """Send the digest at most once per local day, when past send_time_local. Idempotent.

    Called each scheduler cycle (command_nonfatal). Does nothing if disabled, already sent today,
    or before the configured send time — unless ``force``. Never trades / promotes / changes scoring.
    """
    import datetime as _dt
    cfg = _load_digest_cfg()
    if not cfg.get("enabled", False) and not force:
        return {"sent": False, "skipped": "disabled"}
    now = now or _dt.datetime.now()
    today = now.strftime("%Y-%m-%d")
    if not force:
        if _last_sent_date() == today:
            return {"sent": False, "skipped": "already_sent_today"}
        send_time = str(cfg.get("send_time_local", "09:00"))
        try:
            hh, mm = (int(x) for x in send_time.split(":")[:2])
        except Exception:
            hh, mm = 9, 0
        if (now.hour, now.minute) < (hh, mm):
            return {"sent": False, "skipped": "before_send_time", "send_time_local": send_time}
    res = send_daily(dry_run=dry_run, db=db,
                     include_top_examples=bool(cfg.get("include_top_examples", True)))
    if res.get("sent") or dry_run:
        _record_sent(today)
    return {**res, "date": today}
