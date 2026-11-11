"""LLM analysis packet builder for the stocks pipeline.

Mirrors src/analysis/packet.py (crypto) but bundles stocks-specific
context: regime, sector rotation, RS leaders, earnings risk, top
candidates, and the latest stocks trade-idea JSON.

The packet is intended for an LLM to read before producing stock trade
ideas. It is asset-class isolated: no crypto candidates, no crypto rules.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from src.config import ProjectConfig
from src.signals.analytics import compact_packet_summary
from src.signals.config import load_signal_tracking_config
from src.storage.sqlite import SQLiteStore


def write_stocks_packet(
    config: ProjectConfig,
    *,
    mode: str = "intraday",
    source_report: str | None = None,
) -> Path:
    """Write data/processed/llm_stocks_packet.md and return its path.

    Parameters
    ----------
    source_report:
        Optional path to the report that triggered this packet refresh. Surfaced
        in the header so the LLM and auditors can verify packet freshness.
    """

    content = build_stocks_packet(config, mode=mode, source_report=source_report)
    target = config.processed_dir / "llm_stocks_packet.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return target


def build_stocks_packet(
    config: ProjectConfig,
    *,
    mode: str,
    source_report: str | None = None,
) -> str:
    db = SQLiteStore(config.db_path)
    db.init_db()

    lines: list[str] = []
    lines.append("# Stocks AI Desk — LLM Analysis Packet")
    lines.append("")
    lines.append(f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append(f"Mode: {mode}")
    lines.append("Asset class: stocks")
    if source_report:
        lines.append(f"Source report: `{source_report}`")
    lines.append("")
    lines.append("## Read me first")
    lines.append("")
    lines.append(
        "- This packet is for STOCKS analysis only. Do not include crypto "
        "candidates, crypto regime references, or USDT pair logic."
    )
    lines.append(
        "- Index direction (SPY/QQQ/IWM) and sector ETF alignment are first-"
        "class signals. Treat them with the same weight as fundamentals "
        "for intraday/swing decisions."
    )
    lines.append(
        "- Earnings risk overrides clean technicals. Refuse swing entries "
        "into earnings unless the user explicitly asks for an earnings trade."
    )
    lines.append(
        "- yfinance is the data source; treat it as best-effort, not "
        "tick-accurate. If data freshness is suspect, mark trades watchlist."
    )
    lines.append("")

    # 2026-06-09: playbook context block so Opus reasons about stocks ideas
    # by named strategy and current status (intraday actionable, swing/invest
    # watchlist-only). Same source-of-truth as the crypto packet.
    from src.analysis.packet import (
        _build_playbook_context_block,
        _build_sizing_context_block,
    )
    lines.append(_build_playbook_context_block())
    lines.append("")
    lines.append(_build_sizing_context_block())
    lines.append("")
    lines.append(_latest_report_section(config, mode))
    lines.append("")
    lines.append(_latest_agent_outputs_section(config))
    lines.append("")
    lines.append(_company_news_analyst_section(config))
    lines.append("")
    lines.append(_catalyst_advisory_section(config))
    lines.append("")
    lines.append(_news_advisory_section(config))
    lines.append("")
    lines.append(_signal_performance_section(db, config))
    lines.append("")
    lines.append(_upcoming_earnings_section(db))
    lines.append("")
    if mode == "intraday":
        lines.append(_intraday_ab_review_section(db))
        lines.append("")
    lines.append(_rules_section())
    lines.append("")
    lines.append(_checklist_section())
    lines.append("")
    return "\n".join(lines)


def _loads(raw_json: str | None) -> dict[str, Any]:
    try:
        return json.loads(raw_json or "{}")
    except Exception:
        return {}


def _ab_compatibility(r: dict[str, Any], min_rr: float,
                      max_atr_ext: float | None = None) -> tuple[bool, list[str]]:
    """Is this open A/B row CURRENT/compatible with the post-hardening logic?

    Returns (ok, missing). A row is CURRENT only when it clears the same bar a freshly-generated A/B
    would: rr_to_tp1 ≥ min_rr, a KNOWN tp1_source, and — for an ATR-only TP1 — the FULL confirmation
    set that long_confirmation_ok / the ATR-only gate require: RS, volume, a known sector, and an
    ATR extension that is present and within `max_atr_ext`. `missing` explains why a legacy row is
    excluded so the operator sees it is stale, not silently trusted. Structural TP1 needs none of the
    extra ATR-only confirmation."""
    raw = _loads(r.get("raw_idea_json"))
    st = raw.get("structured") or {}
    setup = raw.get("raw_setup") or raw.get("setup") or {}
    missing: list[str] = []

    rr = r.get("expected_rr_tp1")
    try:
        rr = float(rr)
    except (TypeError, ValueError):
        rr = None
    if rr is None:
        missing.append("rr_to_tp1 missing")
    elif rr < min_rr:
        missing.append(f"rr_to_tp1 {rr:.2f} < {min_rr:.2f}")

    tp1_source = st.get("tp1_source") or setup.get("tp1_source")
    if not tp1_source or str(tp1_source) == "unavailable":
        missing.append("tp1_source missing")
    elif str(tp1_source) == "atr_measured":
        # ATR-only TP1 must clear the SAME confirmation bar as long_confirmation_ok.
        if st.get("rs_vs_spy") is None or st.get("volume_ratio") is None:
            missing.append("atr_measured without confirmation fields (RS/volume)")
        sector = r.get("sector") or st.get("sector")
        if not (sector and str(sector).strip()):
            missing.append("sector missing for atr_measured confirmation")
        atr_ext = st.get("atr_extension")
        if atr_ext is None:
            atr_ext = setup.get("atr_extension")
        if atr_ext is None:
            missing.append("atr_extension missing for atr_measured confirmation")
        elif max_atr_ext is not None:
            try:
                if float(atr_ext) > float(max_atr_ext):
                    missing.append(
                        f"atr_extension {float(atr_ext):.2f} > max {float(max_atr_ext):.2f}")
            except (TypeError, ValueError):
                missing.append("atr_extension missing for atr_measured confirmation")

    return (len(missing) == 0), missing


def _intraday_ab_review_section(db: SQLiteStore, *, now: datetime | None = None,
                                window_hours: int = 48) -> str:
    """Enriched-review hook: FRESH-WINDOW (last 48h) open A/B stocks-intraday candidates + a "Top
    demoted near-A/B" block (raw A/B or high-score C the gates demoted) + recent cohort stats, with
    an Opus approve/wait/reject prompt. Ingestion stays read-only — this packet NEVER makes anything
    actionable/live and NEVER auto-calls an LLM."""
    from src.stocks import intraday_guards
    lines = ["## Stocks Intraday A/B — enriched review (approve / wait / reject)"]
    ref = now or datetime.now(timezone.utc)
    since = (ref - timedelta(hours=int(window_hours))).isoformat()
    _risk = {}
    try:
        from src.stocks import load_stocks_config
        _risk = getattr(load_stocks_config(), "risk", {}) or {}
        cohort = intraday_guards.cohort_stats_for_report(db, now=now, cfg_risk=_risk)
    except Exception:
        cohort = {}

    def _pf(v):
        return "inf" if v == float("inf") else ("-" if v is None else f"{v:.2f}")

    if cohort:
        a7, a14 = cohort.get("all", {}).get("7d", {}), cohort.get("all", {}).get("14d", {})
        reset = ((_risk.get("intraday_guards") or {}).get("reset_at_utc") if _risk else None)
        reset_note = f" after guard reset `{reset}`" if reset else ""
        lines.append(f"- Recent A/B cohort (paper_execution_r{reset_note}): 7d net {a7.get('net_r', 0):+.1f}R "
                     f"PF {_pf(a7.get('pf'))} n{a7.get('n', 0)} · 14d net {a14.get('net_r', 0):+.1f}R "
                     f"PF {_pf(a14.get('pf'))} n{a14.get('n', 0)}. If a direction cohort is weak, a "
                     "rolling guard demotes new A/B of that direction to C. NOTE: the global 7d "
                     "breaker can block BOTH directions when the overall book is weak — read the "
                     "long/short split in the report before overriding.")
        ev7 = (cohort.get("evidence") or {}).get("7d") or {}
        fwd7 = ev7.get("forward_postfreeze") or {}
        if ev7:
            lines.append(f"- Evidence quality (Model F, 7d): forward_postfreeze n{fwd7.get('n', 0)} "
                         f"(the only bucket usable as proof of edge) vs backfill_pretrained "
                         f"n{(ev7.get('backfill_pretrained') or {}).get('n', 0)} (in-sample, hypothesis only) "
                         f"vs unclassified n{(ev7.get('unclassified') or {}).get('n', 0)}. Do NOT cite the "
                         "cohort numbers above as \"proven profitable\" unless forward_postfreeze n is large.")
    # Fresh-window rows only (last `window_hours`) so we never surface stale candidates from an
    # earlier batch as if they were current.
    try:
        rows = db.load_signals_for_period(since=since, mode="intraday", asset_class="stocks")
    except Exception:
        rows = []
    # Minimum RR a CURRENT A/B must offer + the max ATR extension for ATR-only confirmation — same
    # hard invariants as the report RR gate / long_extra_confirmation.
    min_rr, max_atr_ext = 1.5, None
    try:
        from src.stocks import load_stocks_config
        _risk = getattr(load_stocks_config(), "risk", {}) or {}
        min_rr = float((_risk.get("structure") or {}).get("require_rr_to_tp1_gte", 1.5))
        _conf = (_risk.get("intraday_guards") or {}).get("long_extra_confirmation") or {}
        _mx = _conf.get("max_atr_extension_from_entry")
        max_atr_ext = float(_mx) if _mx is not None else None
    except Exception:
        min_rr, max_atr_ext = 1.5, None
    open_statuses = ("waiting_for_entry", "triggered", "tp1_hit", "tp2_hit")
    open_ab = [r for r in rows if (r.get("tier") in ("A", "B"))
               and str(r.get("status") or "") in open_statuses]
    # Split into CURRENT (compatible with the post-hardening logic) vs LEGACY (pre-gate signals that
    # still look A/B but fail the new requirements — rr≈1.0, missing tp1_source / confirmation).
    current: list[dict[str, Any]] = []
    legacy: list[tuple[dict[str, Any], list[str]]] = []
    for r in open_ab:
        ok, missing = _ab_compatibility(r, min_rr, max_atr_ext)
        if ok:
            current.append(r)
        else:
            legacy.append((r, missing))
    current = current[:10]

    lines.append("")
    lines.append(f"_Open A/B below = CURRENT/compatible only (last {window_hours}h, rr_to_tp1 ≥ "
                 f"{min_rr:.2f}, known tp1_source; ATR-only requires RS+volume+sector+ATR-extension "
                 "confirmation). Legacy pre-hardening A/B are listed separately below and are NOT "
                 "actionable._")
    if not current:
        lines.append(f"- No current/compatible open A/B intraday candidates in the last {window_hours}h.")
    else:
        for r in current:
            st = _loads(r.get("raw_idea_json")).get("structured") or {}
            lines.append(
                f"- **{r.get('symbol')} {r.get('direction')}** ({r.get('tier')}): "
                f"rr_to_tp1 {r.get('expected_rr_tp1')} (tp1_source {st.get('tp1_source') or '—'}) · "
                f"sector {r.get('sector') or st.get('sector') or '—'} "
                f"· RS·SPY {st.get('rs_vs_spy')} · vol {st.get('volume_ratio')} · "
                f"regime {r.get('market_regime') or '—'} · news_supported {r.get('news_supported')}")

    # ── Legacy open A/B excluded by the new hardening — shown explicitly so the operator SEES they
    # are stale/invalid by the new logic instead of silently trusting them as current A/B.
    lines.append("")
    lines.append("### Legacy open A/B excluded by new hardening")
    if not legacy:
        lines.append("- None — every open A/B in the window meets the new requirements.")
    else:
        for r, missing in legacy[:10]:
            st = _loads(r.get("raw_idea_json")).get("structured") or {}
            lines.append(
                f"- **{r.get('symbol')} {r.get('direction')}** ({r.get('tier')}): "
                f"rr_to_tp1 {r.get('expected_rr_tp1')} · tp1_source {st.get('tp1_source') or '—'} · "
                f"created {str(r.get('created_at') or '—')[:16]} · status {r.get('status') or '—'} · "
                f"excluded: {', '.join(missing) or 'incompatible'}")

    # ── Top demoted near-A/B candidates (last window) — raw A/B or high-score C that a gate demoted
    # (rolling guard / RR / market-closed / ATR-only TP1). Surfaces what the guards removed so Opus
    # can sanity-check; still read-only and NEVER actionable.
    demoted: list[tuple[float, dict, dict]] = []
    for r in rows:
        if str(r.get("tier")) != "C":
            continue
        raw = _loads(r.get("raw_idea_json"))
        caps_txt = " ".join(str(c).lower() for c in (raw.get("cap_reasons") or []))
        pre = raw.get("pre_gate_tier")
        by_gate = bool(raw.get("demoted_by_gate"))
        gate_marker = any(k in caps_txt for k in
                          ("guard", "rr_below", "market_closed", "atr_only"))
        score = float(raw.get("score") or 0)
        if by_gate or pre in ("A", "B") or (gate_marker and score >= 50):
            demoted.append((score, r, raw))
    demoted.sort(key=lambda t: t[0], reverse=True)
    lines.append("")
    lines.append(f"### Top demoted near-A/B candidates (last {window_hours}h)")
    if not demoted:
        lines.append("- None — no A/B-grade setups were demoted in this window.")
    else:
        for score, r, raw in demoted[:8]:
            st = raw.get("structured") or {}
            caps = [c for c in (raw.get("cap_reasons") or []) if "demoted" not in str(c).lower()][:3]
            demote = next((c for c in (raw.get("cap_reasons") or []) if "demoted" in str(c).lower()), "")
            lines.append(
                f"- **{r.get('symbol')} {r.get('direction')}** (was {pre_or_q(raw)}→C, score {score:.0f}): "
                f"rr_to_tp1 {st.get('rr_to_tp1') if st.get('rr_to_tp1') is not None else r.get('expected_rr_tp1')} "
                f"(tp1_source {st.get('tp1_source') or '—'}) · "
                f"sector {r.get('sector') or st.get('sector') or '—'} · RS·SPY {st.get('rs_vs_spy')} · "
                f"vol {st.get('volume_ratio')} · caps: {', '.join(caps) or '—'}")
            if demote:
                lines.append(f"    - {demote}")

    lines.append("")
    lines.append(
        "**Opus tasks:** for each fresh A/B candidate, judge **approve / wait / reject** using RR, "
        "sector strength, earnings proximity, catalyst quality, and legal/headline risk. For the "
        "demoted list, say whether the demotion looks right or whether the setup deserves a second "
        "look on the next fresh session. Reject on earnings/legal/headline risk; prefer *wait* if "
        "extended or news is stale. This stays paper/actionability only — never suggest "
        "live/auto-live/manual-live and never bypass the rolling guards. Output a short verdict line "
        "per symbol; ingestion is read-only.")
    return "\n".join(lines)


def pre_or_q(raw: dict) -> str:
    v = raw.get("pre_gate_tier")
    return v if v in ("A", "B") else "?"


# ---------------------------------------------------------------------------
# Section builders
# ---------------------------------------------------------------------------

def _latest_report_section(config: ProjectConfig, mode: str) -> str:
    lines = ["## Latest stocks report"]
    report_dir = config.reports_dir / "stocks" / mode
    if not report_dir.exists():
        lines.append(
            "_No stocks report yet for this mode. Run "
            f"`python -m src.cli stocks-{mode}-report` first._"
        )
        return "\n".join(lines)
    files = sorted(report_dir.glob("*.md"))
    if not files:
        lines.append("_No stocks reports found._")
        return "\n".join(lines)
    latest = files[-1]
    lines.append(f"_File: `{latest.relative_to(config.root)}`_")
    lines.append("")
    text = latest.read_text(encoding="utf-8")
    # Trim to first ~6000 chars — enough for regime/sectors/ideas/summary,
    # not enough to drown the LLM in raw evidence prose.
    if len(text) > 6000:
        text = text[:6000] + "\n\n_…(report truncated, see file for full body)_"
    lines.append(text)
    return "\n".join(lines)


def _catalyst_advisory_section(config: ProjectConfig) -> str:
    """DISPLAY/ADVISORY-ONLY catalyst-linkage block for the packet. news_supported vs 24h/48h
    exact-match shadow uplift + temporal-coincidence caveat. Never changes tier/actionability."""
    try:
        from src.signals.catalyst_linkage_shadow_audit import (
            stocks_catalyst_advisory, render_advisory_block)
        return render_advisory_block(stocks_catalyst_advisory(str(config.db_path)))
    except Exception as exc:  # noqa: BLE001 — advisory is best-effort, never fatal
        return f"## Catalyst linkage — advisory (display-only)\n- unavailable ({exc})"


def _news_advisory_section(config: ProjectConfig) -> str:
    """DISPLAY-ONLY earnings + SEC/legal + source-health advisory. No score/tier/actionability change."""
    try:
        from src.news.advisory import news_advisory, render_advisory_block
        return render_advisory_block(news_advisory(str(config.db_path)))
    except Exception as exc:  # noqa: BLE001 — advisory is best-effort, never fatal
        return f"## News/catalyst advisory (display-only)\n- unavailable ({exc})"


def _company_news_analyst_section(config: ProjectConfig) -> str:
    """2026-06-15 catalyst safe-fix PART 5: surface company news + analyst
    actions to Opus. Display only — does NOT change score/tier. Reads the
    latest company-news agent output and explicitly flags analyst actions
    (upgrade/downgrade/initiate/price-target) which were classified but
    previously invisible to the packet.
    """
    lines = ["## Company news & analyst actions (display-only)"]
    out_dir = config.root / "data" / "processed" / "agent_outputs"
    files = sorted(out_dir.glob("*_stocks_stock_company_news.json")) if out_dir.exists() else []
    if not files:
        files = sorted(out_dir.glob("*company_news*.json")) if out_dir.exists() else []
    if not files:
        lines.append("_No company-news agent output found._")
        lines.append("_Options / open-interest data: not available for stocks._")
        return "\n".join(lines)
    try:
        payload = json.loads(files[-1].read_text(encoding="utf-8"))
    except Exception:
        lines.append("_Could not parse company-news output._")
        return "\n".join(lines)
    hits_by_symbol = payload.get("hits_by_symbol") or {}
    analyst_lines: list[str] = []
    news_syms: list[str] = []
    for sym, hits in hits_by_symbol.items():
        if not hits:
            continue
        news_syms.append(sym)
        for h in hits[:3]:
            if not isinstance(h, dict):
                continue
            ctype = str(h.get("catalyst_type") or h.get("category") or "").lower()
            if "analyst" in ctype:
                title = str(h.get("title") or h.get("headline") or "")[:90]
                src = h.get("source") or "?"
                analyst_lines.append(f"- {sym}: analyst action — {title} ({src})")
    if news_syms:
        lines.append(f"- Symbols with ticker-specific news: {', '.join(news_syms[:15])}")
    else:
        lines.append("- No ticker-specific company news in the latest cycle.")
    if analyst_lines:
        lines.append("")
        lines.append("**Analyst actions (informational, not a scoring input):**")
        lines.extend(analyst_lines[:10])
    lines.append("")
    lines.append("_Options / open-interest data: not available for stocks (earnings + news only)._")
    return "\n".join(lines)


def _latest_agent_outputs_section(config: ProjectConfig) -> str:
    lines = ["## Latest stocks agent outputs"]
    out_dir = config.root / "data" / "processed" / "agent_outputs"
    if not out_dir.exists():
        lines.append("_No agent outputs directory._")
        return "\n".join(lines)
    targets = [
        ("stock_trade_idea", "Trade idea agent output"),
        ("stock_scoring", "Scoring agent output"),
        ("stocks_market_regime", "Regime snapshot"),
        ("sector_rotation", "Sector rotation snapshot"),
    ]
    for slug, label in targets:
        files = sorted(out_dir.glob(f"*_stocks_{slug}.json"))
        if not files:
            continue
        latest = files[-1]
        try:
            payload = json.loads(latest.read_text(encoding="utf-8"))
        except Exception:
            continue
        lines.append(f"### {label}")
        lines.append(f"_File: `{latest.relative_to(config.root)}`_")
        lines.append("")
        lines.append("```json")
        snippet = json.dumps(payload, indent=2, default=str)
        if len(snippet) > 4000:
            snippet = snippet[:4000] + "\n…(truncated)"
        lines.append(snippet)
        lines.append("```")
        lines.append("")
    return "\n".join(lines)


def _signal_performance_section(db: SQLiteStore, config: ProjectConfig) -> str:
    lines = ["## Stocks signal performance (recent)"]
    tracking_cfg = load_signal_tracking_config(config.root)
    if not tracking_cfg.enabled:
        lines.append("_Signal tracking disabled in config._")
        return "\n".join(lines)
    summary = compact_packet_summary(
        db, config=tracking_cfg, period="month", asset_class="stocks"
    )
    overall = summary.get("overall") or {}
    if not overall or overall.get("sample_size", 0) == 0:
        lines.append(
            "_No stocks signals tracked yet. Once `stocks-*-report` produces "
            "A/B ideas, this section will show R-based win/loss stats._"
        )
        return "\n".join(lines)
    # R1: headline = ACTIONABLE (A/B) only; C-tier shown separately; the
    # all-tier number is kept as a labelled diagnostic.
    from src.signals.analytics import headline_split

    hl = headline_split(db, config=tracking_cfg, period="month", asset_class="stocks")
    ab = hl.get("actionable", {}) or {}
    cw = hl.get("watchlist", {}) or {}
    lines.append(
        f"- **Headline (A/B only)** — period={summary.get('period')}, "
        f"sample={ab.get('sample_size')} (confidence={ab.get('confidence_level')}): "
        f"wins={ab.get('wins')} / losses={ab.get('losses')}, "
        f"avgR={ab.get('average_r')}, totalR={ab.get('total_r')}, "
        f"PF={ab.get('profit_factor')}"
    )
    lines.append(
        f"- _C-tier watchlist (not actionable): sample={cw.get('sample_size')}, "
        f"totalR={cw.get('total_r')}, PF={cw.get('profit_factor')}._"
    )
    lines.append(
        f"- _All-tier diagnostic (A/B/C, not the headline): sample={overall.get('sample_size')}, "
        f"wins={overall.get('wins')} / losses={overall.get('losses')}, "
        f"totalR={overall.get('total_r')}._"
    )
    return "\n".join(lines)


def _upcoming_earnings_section(db: SQLiteStore) -> str:
    lines = ["## Upcoming earnings (next 7 days)"]
    rows = db.load_events(limit=200)
    today = datetime.now(timezone.utc).date()
    soon: list[dict[str, Any]] = []
    for row in rows:
        if str(row.get("asset_class") or "") != "stocks":
            continue
        if str(row.get("event_type") or "") != "earnings":
            continue
        try:
            d = datetime.strptime(str(row.get("event_date") or ""), "%Y-%m-%d").date()
        except ValueError:
            continue
        delta = (d - today).days
        if 0 <= delta <= 7:
            soon.append({"date": d.isoformat(), "ticker": row.get("ticker"), "days": delta})
    if not soon:
        lines.append("_No tracked earnings within the next 7 days._")
        return "\n".join(lines)
    for ev in sorted(soon, key=lambda e: e["days"]):
        lines.append(f"- {ev['date']} ({ev['days']}d): {ev['ticker']}")
    return "\n".join(lines)


def _rules_section() -> str:
    return (
        "## Stocks scoring & risk rules (summary)\n"
        "- Tiering: A ≥ 80, B ≥ 65, C ≥ 50, rejected otherwise.\n"
        "- Hard rejects: missing invalidation, no directional setup, "
        "earnings_today_blocks_swing (when mode=swing).\n"
        "- Caps: score capped at 60 when earnings active (swing); capped at 70 "
        "when data is partial (no invalidation).\n"
        "- Regime overrides: in risk_off regime, longs require leader-grade "
        "relative strength.\n"
        "- Sector alignment: short in a strong sector or long in a weak sector "
        "incurs a -6 penalty per the risk_penalties block.\n"
        "- Earnings windows (swing): blocked if ≤2 trading days ahead unless "
        "the user invokes an explicit earnings strategy.\n"
    )


def _checklist_section() -> str:
    return (
        "## Pre-output checklist\n"
        "1. Did you reference SPY/QQQ direction for every long/short call?\n"
        "2. Did you flag earnings risk explicitly for every A/B idea?\n"
        "3. Did you avoid mixing crypto symbols/funding/OI references?\n"
        "4. Is there a clean invalidation level for every actionable idea?\n"
        "5. Did you use the sector ETF (XLK/SMH/XLF/etc) as a confirmation check?\n"
        "6. If yfinance data is stale or sparse for a symbol, did you downgrade?\n"
    )
