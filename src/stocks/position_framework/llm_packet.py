"""Enriched read-only analysis packet for the Stocks Position Framework (SHADOW ONLY).

Builds `data/processed/llm_stocks_position_packet.md` for an Opus / enriched review of the current
`stocks_swing_growth_breakout` shadow candidates. STRICTLY read-only research:
  * never changes candidates, never writes proposed_signals / signal_outcomes / paper_* tables;
  * never sends Telegram, never makes anything actionable or live;
  * USD net is the only profitability metric; no conclusion until the forward evidence gate passes.

News/catalyst/legal context is pulled from the LOCAL cache only (no network, no paid providers);
when nothing reliable exists for a ticker the packet says so explicitly rather than fabricating.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from . import PLAYBOOK
from .config import load_config, _ROOT
from . import shadow_store
from .news_context import ticker_context

PACKET_PATH = _ROOT / "data" / "processed" / "llm_stocks_position_packet.md"

DISCLAIMER = (
    "> **SHADOW ONLY — research review.** This is NOT the paper book and NOT live. Reviewing this "
    "packet must NOT change candidates, must NOT write to proposed_signals / signal_outcomes / "
    "paper_* tables, must NOT send Telegram, and must NOT make anything actionable or live. The old "
    "stocks swing/invest playbooks are deprecated/removed. Authoritative profitability = **USD net**."
)

OPUS_INSTRUCTIONS = (
    "## Opus tasks — Stocks Position Framework (shadow-only review)\n\n"
    "Review ONLY the current top candidates below. For each, decide whether it is worth continuing "
    "to track in the SHADOW lane. This is research triage, never a trade instruction.\n\n"
    "- Reject on earnings / legal / headline risk (`reject_earnings_risk`, `reject_legal_risk`, "
    "`reject_news_risk`).\n"
    "- Prefer **`wait_pullback`** over `approve_shadow` if the setup is extended or the news is stale.\n"
    "- Use `needs_more_data` when the local context is too thin to judge.\n"
    "- NEVER call a candidate actionable; NEVER suggest live / manual-live / paper promotion; NEVER "
    "reuse old stocks swing/invest stats as proof; NEVER call legacy final_r a profit.\n"
    "- Default to caution: with no forward USD-net outcomes yet, there is **no profitability "
    "conclusion**.\n\n"
    "### Required output — one JSON object per candidate, inside a ```json fence:\n"
    "```json\n"
    "{\n"
    '  "candidate_id": "spf_SYMBOL_YYYY-MM-DD",\n'
    '  "verdict": "approve_shadow | wait_pullback | reject_news_risk | reject_earnings_risk | '
    'reject_legal_risk | needs_more_data",\n'
    '  "confidence": 0.0,\n'
    '  "reasons": ["..."],\n'
    '  "key_news": ["..."],\n'
    '  "risk_notes": ["..."]\n'
    "}\n"
    "```\n"
    "Ingest with `python -m src.cli ingest-stocks-position-review --file <path>` (read-only; writes "
    "only the separate `stocks_position_reviews` table)."
)


def _fmt(v: Any, nd: int = 2, dash: str = "—") -> str:
    try:
        return dash if v is None else f"{float(v):.{nd}f}"
    except (TypeError, ValueError):
        return str(v) if v is not None else dash


def _outcomes_summary(outs: list[dict]) -> str:
    closed = [o for o in outs if o.get("status") == "closed" and o.get("net_pnl_usd") is not None]
    pending = [o for o in outs if o.get("status") == "pending"]
    no_entry = [o for o in outs if o.get("status") == "no_entry"]
    line = (f"- Outcomes: **closed {len(closed)}** · pending {len(pending)} · no-entry {len(no_entry)}")
    if closed:
        nets = [float(o["net_pnl_usd"]) for o in closed]
        wins = sum(1 for x in nets if x > 0)
        gl = abs(sum(x for x in nets if x < 0))
        gw = sum(x for x in nets if x > 0)
        pf = f"{gw/gl:.2f}" if gl > 0 else "inf"
        line += (f"\n- USD net (closed n={len(closed)}): total ${sum(nets):.2f} · "
                 f"avg ${sum(nets)/len(nets):.2f} · winrate {wins/len(nets):.0%} · PF {pf}")
    else:
        line += "\n- USD net: **none closed yet** — no profitability conclusion (pending; no fake fills)."
    return line


def _candidate_block(c: dict, config) -> str:
    cid = c.get("candidate_id") or f"spf_{c.get('symbol')}_{str(c.get('created_at'))[:10]}"
    lines = [
        f"### {c.get('symbol')} — {c.get('setup_variant')}  ·  `{cid}`",
        f"- sector: {c.get('sector') or '—'} ({c.get('sector_etf') or '—'})  ·  "
        f"score {_fmt(c.get('score'), 0)}  ·  data_confidence {_fmt(c.get('data_confidence'), 2)}",
        f"- entry {_fmt(c.get('entry_price'))} (zone {_fmt(c.get('entry_low'))}–{_fmt(c.get('entry_high'))})  ·  "
        f"stop {_fmt(c.get('stop_price'))}  ·  TP1 {_fmt(c.get('tp1'))} ({_fmt(c.get('tp1_r'), 1)}R)  ·  "
        f"TP2 {_fmt(c.get('tp2'))} ({_fmt(c.get('tp2_r'), 1)}R)",
        f"- risk_usd {_fmt(c.get('risk_usd'))}  ·  RS·SPY {_fmt((c.get('rs_spy') or 0)*100, 1)}%  ·  "
        f"RS·sector {_fmt((c.get('rs_sector') or 0)*100, 1) if c.get('rs_sector') is not None else '—'}  ·  "
        f"vol {_fmt(c.get('volume_ratio'), 2)}×  ·  near-high {_fmt(c.get('near_high_pct'), 1)}%",
        f"- market_regime: {c.get('market_regime') or '—'}  ·  earnings_risk: {c.get('earnings_risk') or 'none flagged'}",
    ]
    if c.get("thesis"):
        lines.append(f"- thesis: {c.get('thesis')}")
    if c.get("counter_thesis"):
        lines.append(f"- counter-thesis: {c.get('counter_thesis')}")
    # local news / catalyst / analyst / earnings / legal context — never fabricated
    ctx = ticker_context(c.get("symbol"), config=config)
    lines.append("- **Local ticker context:**")
    if ctx.get("lines"):
        lines.extend(f"  - {ln}" for ln in ctx["lines"])
    else:
        lines.append("  - _No reliable ticker-specific news found in local cache._")
    return "\n".join(lines)


def _recent_closed(outs: list[dict]) -> str:
    import json as _json
    closed = [o for o in outs if o.get("status") == "closed"][:15]
    if not closed:
        return "_No closed shadow outcomes yet._"
    head = ("| Candidate | Net $ | Fees $ | Slip $ | MFE R | MAE R | Hold d | Close reason |\n"
            "|---|---:|---:|---:|---:|---:|---:|---|\n")
    rows = []
    for o in closed:
        notes = {}
        try:
            notes = _json.loads(o.get("notes_json") or "{}")
        except Exception:
            notes = {}
        rows.append(
            f"| {o.get('candidate_id')} | {_fmt(o.get('net_pnl_usd'))} | {_fmt(notes.get('fees_usd'))} | "
            f"{_fmt(notes.get('slippage_usd'))} | {_fmt(o.get('max_favorable_excursion_r'), 2)} | "
            f"{_fmt(o.get('max_adverse_excursion_r'), 2)} | {_fmt(o.get('holding_days'), 0)} | "
            f"{o.get('close_reason') or '—'} |")
    return head + "\n".join(rows)


def build_packet(config=None, *, limit: int = 10, db_path=None) -> str:
    cfg = load_config()
    dbp = db_path or (getattr(config, "db_path", None))
    cands = shadow_store.latest_candidates(limit=limit, only_open=True, db_path=dbp)
    outs = shadow_store.latest_outcomes(limit=100000, db_path=dbp)
    scan_t = shadow_store.latest_scan_time(db_path=dbp)
    sched = bool(cfg.get("scheduler_enabled", False))
    gate = cfg.get("evidence_gate") or {}
    mt = int(gate.get("min_forward_trades", 30))
    closed_n = sum(1 for o in outs if o.get("status") == "closed")

    parts = [
        f"# LLM Analysis Packet — Stocks Position Framework ({PLAYBOOK})", "",
        DISCLAIMER, "",
        "## Status", "",
        f"- Latest scan (UTC): `{scan_t or 'none yet'}`",
        f"- scheduler_enabled: **{sched}**" + ("" if sched else "  _(manual scans only)_"),
        f"- Open shadow candidates: **{len(cands)}**",
        _outcomes_summary(outs),
        f"- Evidence gate: need ≥ **{mt}** forward trades; current closed sample = **{closed_n}** → "
        "**no profitability conclusion yet** (backfill is not proof).",
        "",
        f"## Top open candidates (max {limit})", "",
    ]
    if not cands:
        parts.append("_No open shadow candidates in the latest scan._")
    else:
        parts += [_candidate_block(c, config) for c in cands]
    parts += [
        "", "## Recent closed outcomes (USD net)", "", _recent_closed(outs), "",
        "## Risk notes (read before judging)", "",
        "- **Correlation / sector concentration:** several candidates may share a sector ETF — treat "
        "stacked same-sector names as one correlated bet, not independent edge.",
        "- **Gap risk:** overnight gaps can jump the entry or the stop; fills here are modelled "
        "gap-aware, but real slippage may be worse.",
        "- **Earnings risk:** reject/hold candidates with earnings inside the holding window.",
        "- **Headline / legal / regulatory risk:** a fresh negative headline or legal/regulatory "
        "action invalidates the technical setup regardless of RS.",
        "- **DO NOT promote to paper or live from this packet.** Verdicts stay in the shadow review "
        "table; promotion needs forward USD-net evidence + operator sign-off.",
        "", OPUS_INSTRUCTIONS, "",
    ]
    return "\n".join(p for p in parts if p is not None)


def parse_reviews(text: str) -> list[dict[str, Any]]:
    """Extract review objects from Opus output: a raw JSON array/object, OR one-or-more ```json
    fenced blocks in markdown, OR bare `{...}` objects. Returns a list of dicts (never raises)."""
    import json as _json
    import re
    text = text or ""
    found: list[dict] = []

    def _collect(obj):
        if isinstance(obj, list):
            found.extend(x for x in obj if isinstance(x, dict))
        elif isinstance(obj, dict):
            # {"reviews": [...]} or a single review object
            if isinstance(obj.get("reviews"), list):
                found.extend(x for x in obj["reviews"] if isinstance(x, dict))
            else:
                found.append(obj)

    stripped = text.strip()
    if stripped[:1] in ("[", "{"):
        try:
            _collect(_json.loads(stripped))
        except Exception:
            pass
    if not found:
        for block in re.findall(r"```(?:json)?\s*(.*?)```", text, flags=re.DOTALL):
            try:
                _collect(_json.loads(block.strip()))
            except Exception:
                continue
    if not found:  # last resort: scan for standalone {...} objects containing candidate_id
        for m in re.findall(r"\{[^{}]*candidate_id[^{}]*\}", text, flags=re.DOTALL):
            try:
                _collect(_json.loads(m))
            except Exception:
                continue
    # keep only rows that carry a candidate_id
    return [r for r in found if r.get("candidate_id")]


def write_packet(config=None, *, limit: int = 10, path=None, db_path=None) -> Path:
    md = build_packet(config, limit=limit, db_path=db_path)
    p = Path(path) if path else PACKET_PATH
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(md, encoding="utf-8")
    return p
