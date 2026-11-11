"""Markdown report builder for the stocks pipeline.

Renders the structure defined in the stocks module spec:
  1. Market regime
  2. Sector rotation
  3. Earnings / event risk
  4. News / catalysts
  5. Top candidates (ranked, with tier)
  6. Trade ideas (A/B in full detail)
  7. Watchlist (C-tier)
  8. Rejected / not ready
  9. Final summary
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from src.stocks.pipelines.stocks_pipeline import StocksPipelineResult


def build_stocks_report(result: StocksPipelineResult, *, config=None) -> str:
    """Build the stocks Markdown report.

    Parameters
    ----------
    result:
        Pipeline output.
    config:
        Optional :class:`ProjectConfig`. When provided, enables the Recent
        Signal Performance section. Pipeline callers always pass it; tests
        that only render the visible sections can omit it.
    """
    lines: list[str] = []
    lines.append("# Stocks AI Desk Report")
    lines.append("")
    lines.append(f"Date: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}")
    lines.append(f"Mode: {result.mode}")
    lines.append("Asset class: stocks")
    lines.append(f"Market session: {_market_session_label()}")
    lines.append(f"Data freshness: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    # P1-fix (2026-06-04): planning-only banner when the US cash session is
    # closed and this is an intraday run — intraday A/B entries are demoted to
    # C (planning/watchlist) by the trade-idea agent, so flag it up top.
    try:
        from src.stocks.market_calendar import is_us_cash_session_open
        if result.mode == "intraday" and not is_us_cash_session_open():
            lines.append(
                "> **MARKET CLOSED — planning / watchlist only.** "
                "US cash session is closed; intraday A/B entries are demoted to "
                "C and are NOT actionable. Re-evaluate on fresh levels at/after "
                "the 09:30 ET open."
            )
    except Exception:
        pass
    # P1-fix (2026-06-05): stocks SWING is temporarily watchlist-only after the
    # 48h audit (swing was the single biggest loss bucket). Swing A/B ideas are
    # demoted to C by the trade-idea agent (Gate C) and are NOT Telegram-pushed;
    # they remain visible here for research. Flag it up top.
    if result.mode == "swing":
        lines.append(
            "> **STOCKS SWING — watchlist / research only.** Stocks swing is "
            "temporarily watchlist-only due to 48h audit: −12R, 0W/12L. Swing "
            "A/B candidates are capped to C (no Telegram A/B alerts) until "
            "reviewed; they remain listed below for research."
        )
    # Mode-Viability-Audit (2026-06-09): stocks INVEST is temporarily
    # watchlist-only. Invest A/B ideas are demoted to C by the trade-idea
    # agent and are NOT Telegram-pushed; they stay listed below for research.
    if result.mode == "invest":
        lines.append(
            "> **STOCKS INVEST — watchlist / research only after mode "
            "viability audit: 0W/7L over 14d, same failure mode as paused "
            "stocks swing.** Invest A/B candidates are capped to C (no "
            "Telegram A/B alerts) until reviewed; they remain listed below "
            "for research."
        )
    lines.append("")
    lines.append(_data_summary_section(result))
    lines.append("")

    lines.append(_regime_section(result.regime))
    lines.append("")
    lines.append(_sector_section(result.sectors))
    lines.append("")
    lines.append(_earnings_section(result.earnings))
    lines.append("")
    lines.append(_news_section(result.news))
    lines.append("")
    lines.append(_candidates_section(result.scoring, result.ideas_payload))
    lines.append("")
    lines.append(_ideas_section(result.ideas_payload, result.scoring))
    lines.append("")
    lines.append(_watchlist_section(result.ideas_payload, result.scoring))
    lines.append("")
    lines.append(_rejected_section(result.scoring, result.risk))
    lines.append("")
    if config is not None:
        lines.append(_signal_performance_section(config))
        lines.append("")
        lines.append(_catalyst_advisory_section(config))
        lines.append("")
        lines.append(_news_advisory_section(config))
        lines.append("")
        lines.append(_news_risk_section(config))
        lines.append("")
        if result.mode == "intraday":
            lines.append(_intraday_quality_section(config))
            lines.append("")
            lines.append(_intraday_actionability_section(result, config))
            lines.append("")
    lines.append(_summary_section(result))
    lines.append("")
    return "\n".join(lines)


def _signal_performance_section(config) -> str:
    """Render the shared Recent Signal Performance block for stocks.

    Read-only: this block reflects historical outcomes; it never feeds back
    into scoring or rule changes.
    """
    from src.signals.report_section import build_signal_performance_block

    return build_signal_performance_block(config, asset_class="stocks")


def _catalyst_advisory_section(config) -> str:
    """DISPLAY-ONLY catalyst-linkage advisory (news_supported vs 24h/48h exact-match shadow uplift).
    Never changes tier/actionability/scoring — a visibility surface for the reviewer only."""
    try:
        from src.signals.catalyst_linkage_shadow_audit import (
            stocks_catalyst_advisory, render_advisory_block)
        adv = stocks_catalyst_advisory(str(config.db_path))
        return render_advisory_block(adv)
    except Exception as exc:  # noqa: BLE001 — advisory is best-effort, never fatal
        return f"## Catalyst linkage — advisory (display-only)\n- unavailable ({exc})"


def _news_advisory_section(config) -> str:
    """DISPLAY-ONLY news advisory: earnings risk + fresh SEC/legal filings + source-health warnings.
    Never changes score/tier/actionability."""
    try:
        from src.news.advisory import news_advisory, render_advisory_block
        return render_advisory_block(news_advisory(str(config.db_path)))
    except Exception as exc:  # noqa: BLE001 — advisory is best-effort, never fatal
        return f"## News/catalyst advisory (display-only)\n- unavailable ({exc})"


def _news_risk_section(config) -> str:
    """PRODUCTION news RISK warnings (risk-only): block_requires_operator_review / do_not_chase /
    risk_warning from STRONG events (SEC/legal/FDA/hack/delisting/unlock/maintenance/offering/
    earnings). NEVER a buy/sell, NEVER a score/tier change."""
    try:
        from src.news.risk_advisory import compute_risk_warnings, render_markdown
        return render_markdown(compute_risk_warnings(str(config.db_path)))
    except Exception as exc:  # noqa: BLE001 — best-effort, never fatal
        return f"## Production risk warnings (risk-only)\n- unavailable ({exc})"


# ---------------------------------------------------------------------------
# Section builders
# ---------------------------------------------------------------------------

def _data_summary_section(result: StocksPipelineResult) -> str:
    ds = result.data_summary
    lines = ["## 0. Data Coverage"]
    if ds.indices:
        lines.append(f"- Indices: ok={ds.indices.ok}, fail={ds.indices.fail}")
    if ds.sectors:
        lines.append(f"- Sector ETFs: ok={ds.sectors.ok}, fail={ds.sectors.fail}")
    if ds.symbols:
        lines.append(f"- Symbols: ok={ds.symbols.ok}, fail={ds.symbols.fail}")
    lines.append(f"- Earnings events tracked: {ds.earnings_count}")
    if ds.earnings_failed:
        lines.append(f"- Earnings lookup failed for: {', '.join(ds.earnings_failed[:10])}")
    return "\n".join(lines)


def _regime_section(payload: dict[str, Any]) -> str:
    regime = payload.get("regime") or {}
    indices = payload.get("indices") or []
    lines = ["## 1. Stock Market Regime"]
    lines.append(f"- Label: **{regime.get('label', 'unknown')}**")
    lines.append(f"- Bias: {regime.get('bias', 'neutral')}")
    lines.append(f"- Risk-on: {regime.get('risk_on', False)}")
    if regime.get("vix_level") is not None:
        lines.append(f"- VIX: {regime['vix_level']:.2f}")
    if regime.get("breadth_above_ema20") is not None:
        lines.append(f"- Breadth above EMA20: {regime['breadth_above_ema20']:.1%}")
    if regime.get("breadth_above_ema50") is not None:
        lines.append(f"- Breadth above EMA50: {regime['breadth_above_ema50']:.1%}")
    if regime.get("explanation"):
        lines.append(f"- Explanation: {regime['explanation']}")
    if indices:
        lines.append("")
        lines.append("### Index Trends")
        for idx in indices:
            r20 = idx.get("return_20d")
            r5 = idx.get("return_5d")
            r20_s = f"{r20:+.2f}%" if isinstance(r20, (int, float)) else "n/a"
            r5_s = f"{r5:+.2f}%" if isinstance(r5, (int, float)) else "n/a"
            lines.append(
                f"- {idx['symbol']}: trend={idx['trend']}, 5d={r5_s}, 20d={r20_s}"
            )
    return "\n".join(lines)


def _sector_section(payload: dict[str, Any]) -> str:
    lines = ["## 2. Sector Rotation"]
    bench = payload.get("benchmark_return_20d")
    if bench is not None:
        lines.append(f"- Benchmark ({payload.get('benchmark')}) 20d return: {bench:+.2f}%")
    strongest = payload.get("strongest") or []
    weakest = payload.get("weakest") or []
    if strongest:
        lines.append("")
        lines.append("### Strongest Sectors")
        for s in strongest:
            rs = s.get("rs_vs_spy_20d")
            lines.append(
                f"- {s['sector']} ({s['etf']}): status={s['status']}, "
                f"RS vs SPY 20d={_fmt_signed(rs)}, 20d return={_fmt_signed(s.get('return_20d'))}"
            )
    if weakest:
        lines.append("")
        lines.append("### Weakest Sectors")
        for s in weakest:
            rs = s.get("rs_vs_spy_20d")
            lines.append(
                f"- {s['sector']} ({s['etf']}): status={s['status']}, "
                f"RS vs SPY 20d={_fmt_signed(rs)}, 20d return={_fmt_signed(s.get('return_20d'))}"
            )
    return "\n".join(lines)


def _earnings_section(payload: dict[str, Any]) -> str:
    lines = ["## 3. Earnings / Event Risk"]
    risks = payload.get("risks") or []
    if not risks:
        lines.append("- No earnings risks tracked.")
        return "\n".join(lines)
    active = [r for r in risks if r.get("severity") == "active"]
    soon = [r for r in risks if r.get("severity") in ("next_session", "this_week")]
    safe = [r for r in risks if r.get("severity") == "safe"]
    if active:
        lines.append("### Earnings Today")
        for r in active:
            lines.append(f"- {r['symbol']}: {r['note']}")
    if soon:
        lines.append("")
        lines.append("### Earnings Within The Week")
        for r in sorted(soon, key=lambda x: x.get("days_ahead") or 99):
            lines.append(
                f"- {r['symbol']}: {r['note']} (days_ahead={r.get('days_ahead')})"
            )
    blocks = payload.get("blocks_swing") or []
    if blocks:
        lines.append("")
        lines.append(f"**Swing-blocked by earnings:** {', '.join(blocks)}")
    if safe:
        lines.append("")
        lines.append(f"_Safe (no near-term earnings): {len(safe)} symbols_")
    return "\n".join(lines)


def _news_section(payload: dict[str, Any]) -> str:
    lines = ["## 4. News / Catalysts"]
    has_catalyst = payload.get("has_catalyst") or []
    if not has_catalyst:
        lines.append("- No fresh stock-tagged catalysts in the lookback window.")
        return "\n".join(lines)
    hits = payload.get("hits_by_symbol") or {}
    for sym in has_catalyst:
        items = hits.get(sym) or []
        if not items:
            continue
        lines.append(f"### {sym}")
        for h in items[:3]:
            ts = h.get("published_at") or ""
            lines.append(f"- {h['title']} ({h['source']}, {ts[:10]})")
    return "\n".join(lines)


def _candidates_section(scoring_payload: dict[str, Any],
                        ideas_payload: dict[str, Any] | None = None) -> str:
    lines = ["## 5. Top Candidates"]
    rows = scoring_payload.get("scores") or []
    if not rows:
        lines.append("- No candidates produced.")
        return "\n".join(lines)
    # Final (post-gate) tier per (symbol, direction) from the ideas payload. A raw A/B here may have
    # been DEMOTED to C by a gate (RR / rolling guard / legal / earnings / market-closed / ATR-only
    # TP1). Showing both makes the gate action visible instead of hiding it behind the raw score.
    final_by_key: dict[tuple[str, str], str] = {}
    for idea in (ideas_payload or {}).get("ideas") or []:
        final_by_key[((idea.get("symbol") or "").upper(), idea.get("direction") or "")] = (
            idea.get("tier") or "—")
    lines.append("")
    lines.append("_Tier (raw) = scoring output; Final = tier after demote gates. ⤵ marks a gate "
                 "demotion._")
    lines.append("")
    lines.append("| Symbol | Direction | Tier (raw) | Final | Score | Confidence | Risk Penalty |")
    lines.append("|--------|-----------|-----------|-------|-------|------------|--------------|")
    for r in rows[:15]:
        raw_tier = r["tier"]
        final = final_by_key.get(((r.get("symbol") or "").upper(), r.get("direction") or ""))
        if final is None:
            # Not in the ideas payload → either a pre-gate reject or a no_trade (never became an idea).
            final = "rejected" if raw_tier == "rejected" else raw_tier
        marker = " ⤵" if final != raw_tier else ""
        lines.append(
            f"| {r['symbol']} | {r['direction']} | {raw_tier} | {final}{marker} | "
            f"{r['final_score']} | {r['confidence']} | {r['risk_penalty']} |"
        )
    return "\n".join(lines)


def _ideas_section(ideas_payload: dict[str, Any], scoring: dict[str, Any]) -> str:
    from src.signals.playbooks import label_for

    lines = ["## 6. A/B Actionable Candidates (A/B-tier)"]
    ideas = ideas_payload.get("ideas") or []
    ab_ideas = [i for i in ideas if i.get("tier") in ("A", "B")]
    if not ab_ideas:
        lines.append("- No A/B-tier actionable setups in this run.")
        return "\n".join(lines)

    # Build a symbol → score-row lookup so we can attach component breakdowns.
    score_rows = {
        (r.get("symbol") or "").upper(): r for r in (scoring.get("scores") or [])
    }
    for i, idea in enumerate(ab_ideas, start=1):
        lines.append("")
        lines.append(f"### Idea #{i} — {idea['tier']} {idea['symbol']} {idea['direction']}")
        # 2026-06-09: playbook label block — annotation-only.
        lbl = label_for({**idea, "asset_class": "stocks"})
        lines.append(lbl.to_markdown_block(heading_level=4))
        lines.append("")
        lines.append(f"- Score: {idea['score']:.2f}")
        lines.append(f"- Confidence: {idea['confidence']}")
        # Surface data_confidence (separate from setup confidence) per audit.
        dc = idea.get("data_confidence")
        if dc and dc != idea.get("confidence"):
            lines.append(f"- Data confidence: {dc}")
        # Surface data_flags / data_sources_used so reviewer can see what was used.
        if idea.get("data_sources_used"):
            lines.append(
                f"- Data sources: {', '.join(idea['data_sources_used'])}"
            )
        lines.append(f"- Risk level: {idea['risk_level']}")
        lines.append(f"- Timeframe: {idea['timeframe']}")
        lines.append(f"- Thesis: {idea['thesis']}")
        if idea.get("evidence"):
            lines.append("- Evidence:")
            for e in idea["evidence"]:
                lines.append(f"  - {e}")
        # Per-component score breakdown — was missing from stocks reports.
        row = score_rows.get((idea.get("symbol") or "").upper()) or {}
        comps = row.get("components") or {}
        if comps:
            lines.append("- Score breakdown:")
            for key, value in comps.items():
                try:
                    fv = float(value)
                except (TypeError, ValueError):
                    fv = 0.0
                lines.append(f"  - {key}: {fv:.2f}")
            penalty = row.get("risk_penalty")
            if penalty is not None:
                lines.append(f"  - risk_penalty: {penalty}")
        lines.append(f"- Entry: {idea['entry_plan']}")
        lines.append(f"- Invalidation: {idea['invalidation']}")
        # Explicit structural levels + reward:risk (audit: RR was invisible and always ~1.0).
        _setup = (idea.get("raw") or {}).get("setup") or {}
        _struct = (idea.get("raw") or {}).get("structured") or {}

        def _n(v):
            try:
                return f"{float(v):.2f}"
            except (TypeError, ValueError):
                return "—"
        lines.append(
            f"- Levels: entry_low {_n(_setup.get('entry_low'))} / entry_high "
            f"{_n(_setup.get('entry_high'))} · stop {_n(_setup.get('invalidation'))} · "
            f"TP1 {_n(_setup.get('tp1'))} · **rr_to_tp1 {_n(_setup.get('rr_to_tp1'))}**")
        if _struct:
            lines.append(
                f"- Context: sector {_struct.get('sector') or '—'} "
                f"({_struct.get('sector_etf') or '—'}) · RS·SPY {_n(_struct.get('rs_vs_spy'))} · "
                f"vol {_n(_struct.get('volume_ratio'))}×")
        if idea.get("targets"):
            lines.append(f"- Targets: {', '.join(idea['targets'])}")
        if idea.get("counterarguments"):
            lines.append("- Counter-thesis:")
            for c in idea["counterarguments"]:
                lines.append(f"  - {c}")
        if idea.get("avoid_conditions"):
            lines.append("- Avoid:")
            for a in idea["avoid_conditions"]:
                lines.append(f"  - {a}")
        # What to Monitor — agent already populates `what_to_monitor`; just render.
        if idea.get("what_to_monitor"):
            lines.append("- What to monitor:")
            for m in idea["what_to_monitor"]:
                lines.append(f"  - {m}")
        if idea.get("cap_reasons"):
            lines.append(f"- Caps applied: {', '.join(idea['cap_reasons'])}")
    return "\n".join(lines)


def _watchlist_section(ideas_payload: dict[str, Any], scoring: dict[str, Any]) -> str:
    """C-tier watchlist — NEVER actionable. Built from the IDEAS payload so that A/B ideas that were
    DEMOTED to C (RR gate / rolling guard / legal / earnings / market-closed) appear here with their
    demote reason, instead of vanishing from both the A/B and watchlist sections."""
    lines = ["## 7. C-tier Watchlist — NOT actionable",
             "_Research / planning only. These are never Telegram-pushed and never actionable._"]
    c_ideas = [i for i in (ideas_payload.get("ideas") or []) if i.get("tier") == "C"]
    if not c_ideas:
        lines.append("- No C-tier symbols.")
        return "\n".join(lines)
    for idea in c_ideas[:15]:
        caps = idea.get("cap_reasons") or []
        raw = idea.get("raw") or {}
        # demoted_from: the pre-gate tier (persisted). Fall back to parsing the demote cap string
        # ("tier demoted A→C: …") for older ideas that predate pre_gate_tier persistence.
        pre = raw.get("pre_gate_tier")
        demote = next((c for c in caps if "demoted" in c.lower()), None)
        if not pre and demote:
            import re
            m = re.search(r"demoted\s+([AB])\s*[→\-]", demote)
            pre = m.group(1) if m else None
        was = f" (was {pre})" if pre in ("A", "B") else ""
        # Compact cap markers: short reason tokens, not the long human sentences.
        short_caps = [c for c in caps if "demoted" not in c.lower() and "→" not in c][:3]
        cap_str = f" · caps: {', '.join(short_caps)}" if short_caps else ""
        reason = f" — {demote}" if demote else ""
        lines.append(
            f"- {idea['symbol']} ({idea['direction']}){was}: score {float(idea.get('score', 0)):.0f} · "
            f"**watchlist / not actionable**{reason}{cap_str}")
    return "\n".join(lines)


def _rejected_section(scoring: dict[str, Any], risk: dict[str, Any]) -> str:
    lines = ["## 8. Rejected / Not Ready"]
    risk_by_symbol = risk.get("by_symbol") or {}
    rows = [r for r in (scoring.get("scores") or []) if r.get("tier") == "rejected"]
    if not rows:
        lines.append("- No rejected ideas.")
        return "\n".join(lines)
    for r in rows[:15]:
        sym = r["symbol"]
        info = risk_by_symbol.get(sym) or {}
        blocks = info.get("blocks") or []
        flags = info.get("flags") or []
        reason = ", ".join(blocks or flags[:3]) or "low score"
        lines.append(f"- {sym} ({r['direction']}): {r['final_score']} — {reason}")
    return "\n".join(lines)


def _intraday_quality_section(config) -> str:
    """Recent A/B intraday paper performance, sliced by direction / RR bucket / regime / setup /
    catalyst / sector. Uses `paper_execution_r` (NOT legacy final_r). Read-only diagnostics."""
    lines = ["## 9. Intraday A/B Quality — recent paper performance (paper_execution_r)"]
    try:
        from src.storage.sqlite import SQLiteStore
        from src.stocks import intraday_guards, load_stocks_config
        db = SQLiteStore(config.db_path)
        _risk = getattr(load_stocks_config(), "risk", {}) or {}
        cohort = intraday_guards.cohort_stats_for_report(db, cfg_risk=_risk)
        bd = intraday_guards.ab_breakdowns(db, lookback_days=30, cfg_risk=_risk)
    except Exception as exc:  # noqa: BLE001
        lines.append(f"- unavailable ({exc})")
        return "\n".join(lines)
    lines.append("> `paper_execution_r` (Model F), NOT legacy final_r. Read-only.")

    def _pf(v):
        return "∞" if v == float("inf") else ("—" if v is None else f"{v:.2f}")

    def _cell(s):
        return f"{s['net_r']:+.1f}R/PF{_pf(s['pf'])}/n{s['n']}"

    lines.append("")
    lines.append("**A/B by direction:**")
    lines.append("| dir | 7d | 14d | 30d |")
    lines.append("|---|---|---|---|")
    for d in ("all", "long", "short"):
        c = cohort.get(d, {})
        lines.append(f"| {d} | {_cell(c.get('7d', {'net_r':0,'pf':None,'n':0}))} | "
                     f"{_cell(c.get('14d', {'net_r':0,'pf':None,'n':0}))} | "
                     f"{_cell(c.get('30d', {'net_r':0,'pf':None,'n':0}))} |")

    ev = cohort.get("evidence") or {}
    if ev:
        lines.append("")
        lines.append("_Evidence-class split (Model F, 'all' cohort): only forward_postfreeze is proof these "
                     "trades are profitable — backfill_pretrained is the in-sample data that chose Model F's "
                     "own thresholds and must never be read as \"profitable\"; unclassified predates the "
                     "evidence_class column. The guard table above intentionally still uses ALL trades._")
        lines.append("| window | forward_postfreeze n/netR | backfill_pretrained n/netR | unclassified n |")
        lines.append("|---|---|---|---|")
        for w in ("7d", "14d", "30d"):
            e = ev.get(w, {})
            fwd = e.get("forward_postfreeze") or {}; bfd = e.get("backfill_pretrained") or {}
            unc = e.get("unclassified") or {}
            fwd_r = fwd.get("net_r_sum"); bfd_r = bfd.get("net_r_sum")
            lines.append(f"| {w} | {fwd.get('n', 0)}/{'-' if fwd_r is None else f'{fwd_r:+.1f}'} | "
                         f"{bfd.get('n', 0)}/{'-' if bfd_r is None else f'{bfd_r:+.1f}'} | {unc.get('n', 0)} |")

    # Global vs side-specific guard scope (item 7). The `long`/`short` rows above are the
    # side-specific picture; this note explains how the GLOBAL breaker interacts with them.
    try:
        _g = (_risk or {}).get("intraday_guards") or {}
        _blocks_all = bool(_g.get("global_guard_blocks_all_directions", True))
        _reset = _g.get("reset_at_utc")
    except Exception:
        _blocks_all = True
        _reset = None
    lines.append("")
    if _reset:
        lines.append(f"> **Guard reset:** rolling guard metrics ignore stocks-intraday A/B outcomes "
                     f"created before `{_reset}`. Old rows remain in the archive; the new paper regime "
                     "gets a fresh forward window.")
        lines.append("")
    if _blocks_all:
        lines.append("> **Guard scope:** the global 7d drawdown circuit breaker blocks NEW A/B of "
                     "**both** directions when the overall A/B cohort is weak — so individually "
                     "profitable shorts can still be blocked by an overall-negative book. Read the "
                     "per-direction rows above for the side-specific picture "
                     "(`global_guard_blocks_all_directions: true`).")
    else:
        lines.append("> **Guard scope:** the global breaker is **per-direction only** "
                     "(`global_guard_blocks_all_directions: false`) — each side is judged on its own "
                     "cohort, so a weak long book will not block shorts.")

    # Recovery / would-have-been-A/B diagnostics (item 2) — includes raw A/B a gate demoted to C.
    try:
        rec = intraday_guards.recovery_stats(db, lookback_days=14, cfg_risk=_risk)
        if rec.get("n"):
            lines.append("")
            lines.append("**Would-have-been-A/B (14d, incl. gate-demoted):** "
                         f"n {rec['n']} · demoted {rec['demoted_n']} · net {rec['net_r']:+.1f}R · "
                         f"PF {_pf(rec['pf'])} · demoted-only net {rec['demoted_net_r']:+.1f}R")
            lines.append("_Diagnostic only — separate from the authoritative final-tier guard; shows "
                         "whether near-A/B setups a gate demoted would have recovered._")
    except Exception:
        pass

    def _block(title, dct):
        if not dct:
            return
        lines.append("")
        lines.append(f"**A/B by {title} (30d):**")
        for k, a in sorted(dct.items(), key=lambda kv: kv[1]["net_r"]):
            wr = f"{a['winrate']*100:.0f}%" if a.get("winrate") is not None else "—"
            lines.append(f"- {k}: net {a['net_r']:+.1f}R · n {a['n']} · WR {wr}")

    _block("RR bucket", bd.get("by_rr_bucket"))
    _block("regime", bd.get("by_regime"))
    _block("setup_type", bd.get("by_setup"))
    _block("catalyst", bd.get("by_catalyst"))
    _block("sector", bd.get("by_sector"))
    return "\n".join(lines)


def _intraday_actionability_section(result: StocksPipelineResult, config) -> str:
    """SI-1..SI-5 + SI-7: this cycle's actionability-gate demotions (why raw A/B → C watchlist) plus
    the deterministic post-trade diagnostics (why closed paper trades won/lost). Read-only,
    explainable. Every demotion carries a named reason so a demoted candidate is never a silent drop.
    Profitability is paper_execution_r — never legacy final_r."""
    lines = ["## 10. Intraday Actionability Gates — demotions + post-trade diagnostics"]
    lines.append("> SI-1..5 demote (never promote) A/B→C when market/sector/session/liquidity/catalyst "
                 "is not confirmed. Fail-conservative: missing/stale confirming data demotes. C-tier is "
                 "never actionable. Live untouched.")
    ideas = (result.ideas_payload or {}).get("ideas") or []
    # Count gate demotions this cycle from the persisted intraday_actionability fields.
    reason_keys = ("market_context_reason", "sector_confirmation_reason", "session_rule_reason",
                   "liquidity_reason", "catalyst_quality_reason")
    demoted, reason_tally = [], {}
    for idea in ideas:
        if str(idea.get("mode")) != "intraday":
            continue
        raw = idea.get("raw") or {}
        g = raw.get("intraday_actionability") or {}
        pre = raw.get("pre_gate_tier")
        # demoted_by_gate is set by any gate (RR/guard/actionability); here we attribute specifically
        # to the SI-1..5 gates when one of their reasons is present.
        si_reasons = [g.get(k) for k in reason_keys if g.get(k)]
        if pre in ("A", "B") and str(idea.get("tier")) == "C" and si_reasons:
            demoted.append((idea.get("symbol"), idea.get("direction"), si_reasons))
            for r in si_reasons:
                reason_tally[r] = reason_tally.get(r, 0) + 1
    ab_now = sum(1 for i in ideas if str(i.get("mode")) == "intraday" and str(i.get("tier")) in ("A", "B"))
    lines.append("")
    lines.append(f"**This cycle:** actionable A/B (intraday) after gates: **{ab_now}** · "
                 f"raw-A/B demoted to C by SI-1..5 gates: **{len(demoted)}**")
    if reason_tally:
        lines.append("")
        lines.append("**Demotion reasons (this cycle):**")
        for r, n in sorted(reason_tally.items(), key=lambda kv: -kv[1]):
            lines.append(f"- `{r}` × {n}")
    if demoted:
        lines.append("")
        lines.append("**Demoted candidates (watchlist/review only, not actionable):**")
        for sym, d, rs in demoted[:15]:
            lines.append(f"- {sym} {d} — {', '.join(rs)}")
    # SI-7 post-trade diagnostics (deterministic, R-based).
    try:
        from src.stocks import intraday_post_trade_classifier as ptc
        pt = ptc.report_sections(db=str(config.db_path), lookback_days=14)
        if pt:
            lines.append("")
            lines.append(pt)
    except Exception as exc:  # noqa: BLE001
        lines.append(f"\n_post-trade diagnostics unavailable ({exc})_")
    return "\n".join(lines)


def _summary_section(result: StocksPipelineResult) -> str:
    # Count FINAL (post-gate) tiers from the ideas payload — a raw A/B demoted to C by a gate must
    # count as C here, not A/B. Rejected are pre-gate rejects that never became ideas (from scoring).
    ideas = result.ideas_payload.get("ideas") or []
    ab = sum(1 for i in ideas if i.get("tier") in ("A", "B"))
    c = sum(1 for i in ideas if i.get("tier") == "C")
    demoted = sum(1 for i in ideas if (i.get("raw") or {}).get("demoted_by_gate"))
    rejected = sum(1 for r in (result.scoring.get("scores") or []) if r["tier"] == "rejected")
    label = (result.regime.get("regime") or {}).get("label", "unknown")
    bias = (result.regime.get("regime") or {}).get("bias", "neutral")

    lines = ["## 10. Final Summary"]
    lines.append(f"- Regime: **{label}** (bias={bias})")
    lines.append(f"- Trade ideas (final tiers): A/B={ab}, C={c}, rejected={rejected}")
    if demoted:
        lines.append(f"- Demoted A/B→C by gates: {demoted} "
                     "(RR / rolling guard / legal / earnings / market-closed / ATR-only TP1)")
    if result.signal_ids:
        lines.append(f"- Signals registered: {len(result.signal_ids)}")
    if result.report_path:
        lines.append(f"- Report file: `{result.report_path.name}`")
    if ab == 0:
        lines.append("- No actionable setups. Wait for cleaner regime/index alignment.")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _fmt_signed(value: float | None) -> str:
    if value is None or not isinstance(value, (int, float)):
        return "n/a"
    return f"{value:+.2f}%"


def _market_session_label() -> str:
    """Best-effort label for the current US market session window.

    Uses UTC clock only — does not consult holidays. Stage 5 ships with this
    minimal heuristic; refining for holidays / DST is Stage 6+.
    """

    now = datetime.now(timezone.utc)
    weekday = now.weekday()  # 0 = Monday
    if weekday >= 5:
        return "weekend"
    minutes = now.hour * 60 + now.minute
    # NYSE regular session: 14:30–21:00 UTC during DST (EDT), 15:30–22:00 UTC EST.
    # We accept either window since we don't have DST awareness here.
    pre = 13 * 60 + 30  # premarket from ~09:30 ET equivalents on the early side
    regular_start = 13 * 60 + 30  # treat as regular for any time after early premarket
    regular_end = 21 * 60         # close at 21:00 UTC (EDT)
    after_end = 24 * 60
    if minutes < pre:
        return "after-hours (UTC overnight)"
    if minutes < regular_start:
        return "premarket"
    if minutes < regular_end:
        return "regular session"
    if minutes < after_end:
        return "after-hours"
    return "after-hours"
