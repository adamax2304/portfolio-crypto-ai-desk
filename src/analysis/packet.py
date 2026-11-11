"""Build the LLM analysis packet.

The packet is a single Markdown file the LLM reads before any analysis.
It bundles:
  - the requested mode (and fallback if invest -> swing),
  - a system-prompt reminder,
  - the latest desk context (context_for_llm.md, last_update.json),
  - the latest matching report content (head only),
  - relevant Obsidian rules + checklists,
  - a list of vault pages to load on demand,
  - the pre-analysis checklist embedded,
  - the required output format.

Strict invariants:
  - Read-only over every source file.
  - Never write into news_trader/.
  - Degrades gracefully when a source is missing.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from src.config import ProjectConfig


SUPPORTED_MODES = {"scalp", "intraday", "swing", "invest", "review", "news-only"}
FALLBACK_MODE_MAP = {"invest": "swing", "long-term": "swing", "long_term": "swing"}


def _safe_read(path: Path, max_chars: int | None = None) -> str:
    if not path.exists():
        return ""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    if max_chars and len(text) > max_chars:
        return text[:max_chars] + "\n\n... [truncated to first " + str(max_chars) + " chars]\n"
    return text


def _latest_report(config: ProjectConfig, kind: str) -> Path | None:
    directory = config.reports_dir / kind
    if not directory.exists():
        return None
    reports = sorted(directory.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    return reports[0] if reports else None


def _latest_agent_output(config: ProjectConfig, suffix: str) -> Path | None:
    directory = config.processed_dir / "agent_outputs"
    if not directory.exists():
        return None
    files = sorted(directory.glob(f"*_{suffix}.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    return files[0] if files else None


def _list_recent_vault_files(folder: Path, max_items: int = 5) -> list[Path]:
    if not folder.exists():
        return []
    files = sorted(
        (p for p in folder.iterdir() if p.is_file() and p.suffix == ".md" and p.name != "README.md"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return files[:max_items]


def _section(title: str, body: str) -> str:
    return f"## {title}\n\n{body.strip()}\n"


def _bullet_list(items: Iterable[str]) -> str:
    items = list(items)
    if not items:
        return "_none_"
    return "\n".join(f"- {item}" for item in items)


def _fmt_metric(value: Any) -> str:
    if value is None:
        return "—"
    if isinstance(value, float):
        if value == float("inf"):
            return "∞"
        return f"{value:.3f}".rstrip("0").rstrip(".") or "0"
    return str(value)


def _build_sizing_context_block() -> str:
    """Playbook-Aware Sizing Context — annotation-only reporting layer.

    Tells Opus that the system computes a sized_r per signal alongside
    raw_r, and explains the per-playbook weight schedule. Does NOT
    influence signal generation, scoring, or alerts.
    """
    body = (
        "The system reports two R values per signal:\n"
        "- `raw_r` — the tracker's recorded R per the existing TP/SL geometry. UNCHANGED by sizing.\n"
        "- `sized_r` = `raw_r * playbook_weight`. Annotation-only paper-PnL.\n\n"
        "### Playbook size weights (v1, from `reports/PROFITABILITY_LEVERS_AUDIT.md`)\n\n"
        "| Cohort | Weight | Rationale |\n"
        "|---|---:|---|\n"
        "| `crypto_swing_narrative_rs_momentum` | 1.0× | Primary playbook (PF 2.22) |\n"
        "| `crypto_intraday_catalyst_or_momentum` | 1.0× | Catalyst lane PF 1.83 |\n"
        "| `crypto_failed_bounce_short` | 1.0× | PF 1.38 |\n"
        "| `crypto_scalp_momentum_continuation` | **0.5×** | Low-confidence; TP/horizon mismatch |\n"
        "| `stocks_intraday_rth_momentum` B-tier | 1.0× | WR 56%, healthy edge |\n"
        "| `stocks_intraday_rth_momentum` A-tier long | **0.5×** | A-tier overpromotion symptom (21% WR / −6.2R) |\n"
        "| `stocks_swing_watchlist_rs_rotation` | **0×** | DEPRECATED/REMOVED — poor forward perf; never sized |\n"
        "| `stocks_invest_watchlist_30d_thesis` | **0×** | DEPRECATED/REMOVED — poor forward perf; never sized |\n"
        "| `stocks_swing_growth_breakout` (NEW) | **0×** | Shadow-only research; not sized, not actionable |\n"
        "| C-tier / watchlist / shadow | **0×** | Informational |\n\n"
        "### Decision implication for Opus\n"
        "- When summarising a trade as 'in this scheme it would have been …', cite the cohort weight explicitly.\n"
        "- Do not propose sizing **changes** in the Telegram summary — that is a separate human-approval lane.\n"
        "- A scalp signal is still a valid A/B alert at 0.5× — surface it as research-grade, not as fully-sized.\n"
        "- Old (deprecated/removed) stocks swing/invest are NEVER traded at any size; the new "
        "`stocks_swing_growth_breakout` is shadow-only research (not sized, not actionable).\n\n"
        "Weights live in `config/sizing_weights.yaml`. Logic in `src/signals/sizing.py`.\n"
    )
    return _section("Playbook-Aware Sizing", body)


def _build_playbook_context_block() -> str:
    """Strategy Playbook Context — single block for Opus reasoning.

    Renders the canonical playbook → status → 14d performance map
    described in `reports/STRATEGY_PLAYBOOK_AUDIT.md` and
    `reports/CURRENT_TRADING_PLAYBOOKS.md`. Annotation only — does not
    change any signal logic.
    """
    body = (
        "Use these named playbooks to reason about every signal in this packet. "
        "Each idea card below carries a Playbook block tying it back to one of "
        "these strategies. Sources: "
        "`reports/STRATEGY_PLAYBOOK_AUDIT.md`, `reports/CURRENT_TRADING_PLAYBOOKS.md`.\n\n"
        "### Mode playbooks (status × 14d performance)\n"
        "| Playbook | Status | 14d evidence |\n"
        "|---|---|---|\n"
        "| `crypto_swing_narrative_rs_momentum` | **actionable — primary** | WR 72% · PF 5.80 · +24R (n=18 closed) |\n"
        "| `crypto_intraday_catalyst_or_momentum` (with catalyst) | actionable | WR 50% · PF 2.75 · +7R |\n"
        "| `crypto_intraday_catalyst_or_momentum` (no catalyst) | actionable, weaker | WR 23% · PF 0.70 · −3R |\n"
        "| `crypto_failed_bounce_short` | actionable | WR 40% · PF 2.00 · +9R (crypto shorts) |\n"
        "| `crypto_scalp_momentum_continuation` | **low_confidence** | WR 12% · PF 0.14 · −6R; entry edge real, TP/horizon mismatch |\n"
        "| `stocks_intraday_rth_momentum` | **actionable — primary** | WR 55% · PF 2.03 · +80R; shorts subset PF 9.00 |\n"
        "| `stocks_swing_watchlist_rs_rotation` | **DEPRECATED/REMOVED** | removed from active analysis (pre-removal WR 11% · PF 0.15 · −33R); NOT paused-to-return |\n"
        "| `stocks_invest_watchlist_30d_thesis` | **DEPRECATED/REMOVED** | removed from active analysis (WR 0% · 0W/24L · −24R); NOT paused-to-return |\n"
        "| `stocks_swing_growth_breakout` (NEW) | **shadow_only research** | separate position framework; no actionability/live/Telegram; needs forward evidence |\n\n"
        "### Overlays (additive to the primary playbook)\n"
        "- `catalyst_backed` — news_supported=1 on the signal; lifts crypto intraday + swing PF; neutral on scalp.\n"
        "- `rs_leader` — top-decile RS proxy (score ≥ 80 on crypto intraday/swing long); the cleanest crypto-swing sub-cohort.\n"
        "- `short_playbook` — short direction on crypto or stocks; small but cleaner PF than longs in 14d.\n"
        "- `low_confidence_scalp` — every crypto scalp; treat with lower confidence than intraday/swing.\n"
        "- `deprecated_old_stocks_swing_invest` — the OLD stocks swing/invest playbooks are REMOVED "
        "from active analysis (not paused-to-return); never actionable. The NEW "
        "`stocks_swing_growth_breakout` is a separate shadow-only research lane.\n\n"
        "### Decision shortcuts\n"
        "- If `status=actionable` AND playbook PF > 2.0 — clean lane, the standard scoring/tier flow is trustworthy.\n"
        "- If `status=low_confidence` — prefer partial early take or skip; treat A/B alerts as research-grade.\n"
        "- If `status=watchlist_only` — do **not** propose a Telegram-actionable trade on it; it is research/diagnostic only.\n"
        "- If `status=DEPRECATED/REMOVED` — the playbook is retired; never cite its old stats as proof and never propose a trade on it.\n"
        "- If `status=shadow_only research` (stocks_swing_growth_breakout) — review as a watchlist/research candidate only; never actionable/live until the forward evidence gate passes AND the operator signs off.\n"
        "- Catalyst overlay does **not** rescue crypto scalp — do not over-weight catalyst on scalp ideas.\n"
    )
    return _section("Strategy Playbook Context", body)


def _build_stocks_position_framework_block() -> str:
    """Stocks Position Framework — shadow-only research (Opus extended-analysis section).

    Tells Opus the NEW stocks_swing_growth_breakout framework is research-only, distinct from the
    deprecated old stocks swing/invest. Annotation only — never turns anything actionable/live.
    """
    latest = ""
    latest_v2 = ""
    try:
        from src.stocks.position_framework import shadow_store as _pf_store

        cands = _pf_store.latest_candidates(limit=5, only_open=True)
        scan_t = _pf_store.latest_scan_time()
        if cands:
            tops = ", ".join(
                f"{c.get('symbol')} ({c.get('setup_variant')}, score {c.get('score')})" for c in cands)
            latest = (f"\n**Latest shadow scan** (`{scan_t}`): {len(cands)} open candidate(s) — {tops}. "
                      f"USD-net outcomes pending (no fake PnL).\n")
        else:
            latest = f"\n**Latest shadow scan** (`{scan_t or 'none yet'}`): no open candidates.\n"
    except Exception:
        latest = ""

    try:
        from src.stocks.position_framework import v2_store as _v2_store
        from src.stocks.position_framework.v2_config import load_config as _load_v2_config

        v2_rows = _v2_store.open_candidates()
        v2_ready = _v2_store.readiness(_load_v2_config())
        top_v2 = ", ".join(
            f"{row.get('symbol')} ({row.get('setup_variant')}, score {row.get('score')})"
            for row in v2_rows[:5]
        )
        latest_v2 = (
            "\n**Stocks Position Swing V2** "
            f"({v2_ready['verdict']}): {len(v2_rows)} open; "
            f"clean closed={v2_ready['clean_closed']}; net USD=${v2_ready['net_pnl_usd']:.2f}"
            + (f"; top: {top_v2}." if top_v2 else ".")
            + "\n"
        )
    except Exception:
        latest_v2 = ""

    body = (
        "This is **NOT** the old stocks swing/invest. The old `stocks_swing_watchlist_rs_rotation` "
        "and `stocks_invest_watchlist_30d_thesis` are **deprecated/removed** due to poor forward "
        "performance — do not resurrect them and do not cite their old stats as proof.\n\n"
        "The NEW framework is currently active only for:\n"
        "- `stocks_swing_growth_breakout` — long-only, weekly/daily primary (1H optional later).\n"
        "- Phase-2 `stocks_swing_earnings_drift` and Phase-3 `stocks_invest_stage2_position` are "
        "disabled placeholders (not active).\n\n"
        "Status: **shadow-only research** — no actionability, no live/auto-live/manual-live, no "
        "Telegram, not sized in the paper book. Authoritative profitability = **USD net**; legacy "
        "final_r is diagnostic only.\n"
        f"{latest}{latest_v2}\n"
        "The isolated `stocks_position_swing_v2` lane tests only confirmed "
        "`BREAKOUT_RETEST` and `TREND_PULLBACK_RECLAIM`, using next-session gap-aware "
        "execution, portfolio/sector caps, earnings/corporate-event gates, and separate "
        "candidates/outcomes/reviews. Never merge its evidence with V1.\n\n"
        "### Opus tasks (review candidates as research/watchlist only)\n"
        "1. Validate market regime: SPY/QQQ/VIX.\n"
        "2. Validate sector strength (sector above 50D, RS vs SPY).\n"
        "3. Validate the stock's RS vs SPY and vs its sector.\n"
        "4. Validate the setup variant (breakout / pullback_21d_50d / reclaim_after_shakeout / consolidation_continuation).\n"
        "5. Check earnings / gap / news risk.\n"
        "6. Check stop placement (below structure + ATR buffer) and holding horizon (≤40 days Phase 1).\n"
        "7. Label each as a **research candidate only**.\n"
        "8. For V2, review may only narrow/reject; never alter entry, stop, targets, or score.\n\n"
        "### Opus must NOT\n"
        "- turn any candidate actionable, or suggest a live entry;\n"
        "- reuse old stocks swing/invest stats as proof of this framework;\n"
        "- call legacy `final_r` a profit.\n\n"
        "### Required output\n"
        "- candidate quality assessment;\n"
        "- risk warnings;\n"
        "- default to **\"needs more forward evidence\"** unless the evidence gate has actually passed.\n"
    )
    return _section("Stocks Position Framework — shadow-only research", body)


def _build_catalyst_block(config: ProjectConfig) -> str:
    """Catalyst / narrative block for the packet (PART 1 of catalyst layer).

    Reads the LATEST `catalyst_events.jsonl` + `narrative_baskets.jsonl`
    under ``data/catalysts/<today>/`` (the scheduler writes one append-
    set per cycle). Pure read; fails open with a stub when the catalyst
    scan has not yet run.
    """

    import json
    from datetime import datetime, timezone

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    cat_dir = config.root / "data" / "catalysts" / today
    events_path = cat_dir / "catalyst_events.jsonl"
    baskets_path = cat_dir / "narrative_baskets.jsonl"

    if not events_path.exists() and not baskets_path.exists():
        return _section(
            "Catalyst / Narrative (auto-collected)",
            "_catalyst scan has not run yet today — run `python -m src.cli catalyst-scan`._",
        )

    events: list[dict] = []
    baskets: list[dict] = []
    try:
        if events_path.exists():
            with events_path.open("r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        events.append(json.loads(line))
                    except Exception:
                        continue
        if baskets_path.exists():
            with baskets_path.open("r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        baskets.append(json.loads(line))
                    except Exception:
                        continue
    except Exception as exc:
        return _section(
            "Catalyst / Narrative (auto-collected)",
            f"_could not load catalyst JSONL: {exc}_",
        )

    # De-duplicate events by catalyst_id (events file is append-per-cycle).
    seen_ids: set[str] = set()
    deduped: list[dict] = []
    for ev in reversed(events):
        cid = ev.get("catalyst_id")
        if not cid or cid in seen_ids:
            continue
        seen_ids.add(cid)
        deduped.append(ev)

    lines: list[str] = []
    lines.append(
        f"Auto-collected by scheduler — {len(deduped)} unique events today, "
        f"{len(baskets)} narrative baskets. "
        f"Files: `{events_path.relative_to(config.root)}`, "
        f"`{baskets_path.relative_to(config.root)}`."
    )
    lines.append("")

    if baskets:
        lines.append("### Narrative baskets")
        lines.append("")
        for b in baskets[:6]:
            primary = ", ".join(b.get("primary_symbols") or []) or "—"
            related = ", ".join(b.get("related_symbols") or []) or "—"
            lines.append(
                f"- **{b.get('basket_name')}** "
                f"(playbook: `{b.get('suggested_playbook')}`, "
                f"source: {b.get('source_quality')}, fresh: {b.get('freshness')})"
            )
            lines.append(f"  - primary: {primary}")
            lines.append(f"  - related: {related}")
            lines.append(f"  - {b.get('catalyst_summary', '')[:240]}")
        lines.append("")

    high_conf = [
        e for e in deduped
        if e.get("confidence") == "high" and e.get("catalyst_type") != "other_news"
    ]
    if high_conf:
        # 2026-06-15 catalyst safe-fix PART 6: explicit per-catalyst age tag +
        # source quality, sorted freshest-first, with an "old (>6h)" marker so
        # Opus does not treat a stale catalyst as fresh. Display only — no gate,
        # no suppression, no score change.
        from datetime import datetime, timezone

        def _age_h(ts: object) -> float | None:
            if not ts:
                return None
            try:
                d = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
                if d.tzinfo is None:
                    d = d.replace(tzinfo=timezone.utc)
                return max(0.0, (datetime.now(timezone.utc) - d).total_seconds() / 3600.0)
            except Exception:
                return None

        def _src_q(src: str) -> str:
            s = (src or "").lower()
            if any(h in s for h in ("announcement", "binance", "coinbase", "sec.gov")):
                return "official"
            if any(h in s for h in ("coindesk", "cointelegraph", "reuters", "bloomberg",
                                     "theblock", "the block", "cnbc", "marketwatch")):
                return "reputable"
            if "t.me" in s or "twitter" in s or "x.com" in s:
                return "social"
            return "unknown"

        tagged = []
        for e in high_conf:
            age = _age_h(e.get("timestamp"))
            tagged.append((age if age is not None else 1e9, e, age))
        tagged.sort(key=lambda t: t[0])  # freshest first

        lines.append("### High-confidence catalysts (primary source, freshest first)")
        lines.append("")
        any_fresh = False
        for _, e, age in tagged[:10]:
            sym = e.get("symbol") or "(basket)"
            if age is None:
                age_lbl = "age?"
            elif age <= 1:
                age_lbl = f"fresh({age:.1f}h)"; any_fresh = True
            elif age <= 6:
                age_lbl = f"recent({age:.1f}h)"; any_fresh = True
            else:
                age_lbl = f"OLD({age:.1f}h)"
            lines.append(
                f"- **{sym}** [{e.get('catalyst_type')}] {age_lbl}, "
                f"{_src_q(e.get('source'))} — "
                f"{(e.get('title') or '')[:130]} ({e.get('source')})"
            )
        if not any_fresh:
            lines.append("_No fresh (<6h) high-confidence catalyst — all listed are stale._")
        lines.append("")

    legal = [e for e in deduped if e.get("catalyst_type") == "legal_risk"]
    if legal:
        lines.append("### Legal / regulatory risk")
        lines.append("")
        for e in legal[:8]:
            sym = e.get("symbol") or "(basket)"
            lines.append(f"- **{sym}**: {(e.get('title') or '')[:160]} ({e.get('source')})")
        lines.append("")

    rumours = [e for e in deduped if e.get("catalyst_type") == "rumour_only"]
    if rumours:
        lines.append("### Rumours (low confidence)")
        lines.append("")
        for e in rumours[:6]:
            sym = e.get("symbol") or "(basket)"
            lines.append(f"- {sym}: {(e.get('title') or '')[:140]} ({e.get('source')})")
        lines.append("")

    return _section("Catalyst / Narrative (auto-collected)", "\n".join(lines))


def _build_news_risk_events_block(config: ProjectConfig) -> str:
    """PRODUCTION normalized-event + risk-warning context for Opus (read-model only).

    Surfaces (a) the unified normalized event layer summary (asset-class / event-type
    / conflicting symbols) and (b) risk-only warnings (block_requires_operator_review,
    do_not_chase, freshness/source-quality). These are ADVISORY: they never generate a
    buy/sell, never change a score or tier, never unlock live. Wrapped so a DB hiccup
    never blocks packet generation.
    """
    lines: list[str] = []
    try:
        from src.news.events import normalized_events

        ev = normalized_events(str(config.db_path), hours=48, limit=400)
        if ev.get("available"):
            by_type: dict[str, int] = {}
            for e in ev.get("events", []):
                by_type[e.get("event_type", "other")] = by_type.get(e.get("event_type", "other"), 0) + 1
            top = sorted(by_type.items(), key=lambda kv: -kv[1])[:8]
            lines.append(
                f"- Normalized events (48h): {ev.get('count', 0)} "
                f"(deduped from {ev.get('deduped_from', 0)}); "
                f"types: {', '.join(f'{k}×{v}' for k, v in top) or 'none'}."
            )
            conflicting = ev.get("conflicting_symbols", [])
            if conflicting:
                lines.append(
                    f"- ⚠ Conflicting news (both bullish & bearish in window): "
                    f"{', '.join(conflicting[:10])} — treat as no-clean-read, do not chase."
                )
            # Include the actual material rows, not only event counts. Opus can
            # now see content/source confidence and the risk/linkage decision.
            material = [e for e in ev.get("events", [])
                        if e.get("linkage_allowed") or e.get("risk_action") not in (None, "none")]
            if material:
                lines.append("- Material canonical events for review (advisory; not an auto-score):")
                for e in material[:10]:
                    syms = ",".join(e.get("symbols") or []) or "macro"
                    lines.append(
                        f"  - {syms} · {e.get('event_type')} · {e.get('direction_hint')} · "
                        f"confidence={e.get('confidence')} · {e.get('source_quality')}/"
                        f"{e.get('content_level')} · risk={e.get('risk_action')} · "
                        f"{str(e.get('title') or '')[:150]}"
                    )
        else:
            lines.append("- Normalized event layer unavailable this cycle.")
    except Exception as exc:  # noqa: BLE001 — advisory only
        lines.append(f"- Normalized event layer failed to render (non-fatal): {exc}")

    try:
        from src.news.risk_advisory import compute_risk_warnings

        rw = compute_risk_warnings(str(config.db_path))
        review = rw.get("symbols_requiring_operator_review", [])
        warns = rw.get("warnings", [])
        if review:
            lines.append(
                f"- Operator-review warning (risk-only advisory — does NOT gate routing or create a "
                f"trade): {', '.join(review[:12])}."
            )
        if warns:
            shown = warns[:8]
            for w in shown:
                lines.append(
                    f"  - {w.get('symbol')}: {w.get('effect')} — "
                    f"{(w.get('reason') or w.get('title') or '')[:120]}"
                )
        if not review and not warns:
            lines.append("- No strong risk events (SEC/legal/hack/delisting/unlock/earnings) in window.")
        lines.append(
            "- Guardrail: these effects are risk-only "
            "(block_requires_operator_review / do_not_chase / risk_warning / freshness / "
            "source_quality / conflicting_news). They NEVER boost a score, upgrade a tier, "
            "create a buy/sell, place a live order, or unlock live."
        )
    except Exception as exc:  # noqa: BLE001 — advisory only
        lines.append(f"- Risk-warning layer failed to render (non-fatal): {exc}")

    return _section("Normalized Events & Risk Warnings (production, risk-only)", "\n".join(lines))


def _build_signal_performance_block(config: ProjectConfig) -> str:
    """Compact, sample-size-aware Signal Performance block for the packet.

    Safe — wrapped in try/except so a database/migration hiccup never blocks
    packet generation. Falls back to a short stub explaining how to enable.
    """

    try:
        from src.signals.analytics import (
            compact_packet_summary,
            compute_breakdowns,
            headline_split,
            observations,
        )
        from src.signals.config import load_signal_tracking_config
        from src.storage.sqlite import SQLiteStore
    except Exception:
        return _section(
            "Recent Signal Performance",
            "_signal-tracking module not importable yet — run `python -m src.cli signal-stats` after a report._",
        )

    try:
        tracking_config = load_signal_tracking_config(config.root)
        if not tracking_config.enabled:
            return _section(
                "Recent Signal Performance",
                "_signal tracking disabled in `config/signal_tracking.yaml`._",
            )
        store = SQLiteStore(config.db_path)
        store.init_db()
        breakdown_week = compute_breakdowns(store, config=tracking_config, period="week")
        overall_24h = compute_breakdowns(store, config=tracking_config, period="today").overall
        obs = observations(breakdown_week, config=tracking_config)
        # R1: actionable A/B headline (C-tier watchlist excluded from headline).
        hl_week = headline_split(store, config=tracking_config, period="week")
    except Exception as exc:
        return _section(
            "Recent Signal Performance",
            f"_signal-tracking failed to render (will not block analysis): {exc}_",
        )

    overall_week = breakdown_week.overall
    sample_week = overall_week.get("sample_size", 0) or 0
    sample_today = overall_24h.get("sample_size", 0) or 0

    lines: list[str] = []
    lines.append(
        f"**Sample sizes** — last 24h: {sample_today} signals "
        f"(confidence `{overall_24h.get('confidence_level', 'anecdotal')}`) "
        f"| last 7d: {sample_week} signals "
        f"(confidence `{overall_week.get('confidence_level', 'anecdotal')}`)."
    )
    if sample_week == 0 and sample_today == 0:
        lines.append("")
        lines.append(
            "_No tracked signals yet. Auto-registration runs after every report, "
            "or run `python -m src.cli register-signals` manually._"
        )
        return _section("Recent Signal Performance", "\n".join(lines))

    # R1: actionable A/B headline first; C-tier excluded from it.
    ab = (hl_week or {}).get("actionable", {}) or {}
    cw = (hl_week or {}).get("watchlist", {}) or {}
    lines.append("")
    lines.append("### Last 7 days — HEADLINE actionable (A/B only)")
    lines.append(
        f"- sample {ab.get('sample_size', 0)} | triggered {ab.get('triggered', 0)} | "
        f"wins {ab.get('wins', 0)} / losses {ab.get('losses', 0)} | "
        f"winrate {_fmt_metric(ab.get('winrate_triggered'))} | "
        f"PF {_fmt_metric(ab.get('profit_factor'))} | total R {_fmt_metric(ab.get('total_r'))}"
    )
    lines.append(
        f"- _C-tier watchlist (separate, not actionable): n {cw.get('sample_size', 0)}, "
        f"PF {_fmt_metric(cw.get('profit_factor'))}, total R {_fmt_metric(cw.get('total_r'))}._"
    )

    lines.append("")
    lines.append("### Last 7 days — all-tier diagnostic (A/B/C, not the headline)")
    lines.append(
        f"- triggered: {overall_week.get('triggered', 0)} "
        f"(capture {_fmt_metric(overall_week.get('capture_rate'))}) | "
        f"wins {overall_week.get('wins', 0)} / losses {overall_week.get('losses', 0)} / "
        f"amb {overall_week.get('ambiguous', 0)}"
    )
    lines.append(
        f"- TP1/TP2/TP3 hits: {overall_week.get('tp1_hits', 0)} / "
        f"{overall_week.get('tp2_hits', 0)} / {overall_week.get('tp3_hits', 0)} | "
        f"stop hits: {overall_week.get('stop_hits', 0)}"
    )
    lines.append(
        f"- winrate triggered: {_fmt_metric(overall_week.get('winrate_triggered'))} | "
        f"PF: {_fmt_metric(overall_week.get('profit_factor'))} | "
        f"avg R: {_fmt_metric(overall_week.get('average_r'))} | "
        f"total R: {_fmt_metric(overall_week.get('total_r'))}"
    )

    def _compact_table(title: str, rows: list[dict[str, Any]]) -> list[str]:
        if not rows:
            return []
        out = ["", f"### {title}"]
        out.append("| label | n | conf | wins | losses | winrate | PF | avg R |")
        out.append("|---|---|---|---|---|---|---|---|")
        for row in rows[:8]:
            out.append(
                f"| {row.get('label')} | {row.get('sample_size')} | "
                f"{row.get('confidence_level')} | {row.get('wins')} | "
                f"{row.get('losses')} | "
                f"{_fmt_metric(row.get('winrate_triggered'))} | "
                f"{_fmt_metric(row.get('profit_factor'))} | "
                f"{_fmt_metric(row.get('average_r'))} |"
            )
        return out

    lines += _compact_table("By tier", breakdown_week.by_tier)
    lines += _compact_table("By mode", breakdown_week.by_mode)
    lines += _compact_table("By direction", breakdown_week.by_direction)
    lines += _compact_table("By weekend mode", breakdown_week.by_weekend_mode)
    lines += _compact_table("By exchange confirmation", breakdown_week.by_exchange_confirmation)

    lines.append("")
    if obs:
        lines.append("### Observations (manual approval required — never auto-apply)")
        for note in obs[:6]:
            lines.append(
                f"- _{note['level']}_ (confidence `{note['confidence']}`, "
                f"n={note['sample']}): {note['text']}"
            )
    else:
        lines.append(
            "### Observations\n_No observations passed sample-size threshold. Treat current "
            "performance numbers as anecdotal until at least "
            f"{tracking_config.minimum_sample_for_recommendations} tracked signals exist._"
        )

    lines.append("")
    lines.append(
        "_The signal tracker is passive. Use `signal-stats`, `review-signals`, "
        "or `signal-detail <id>` for details. **Any scoring/rule change requires "
        "manual approval.**_"
    )

    return _section("Recent Signal Performance", "\n".join(lines))


def _build_market_intelligence_block(config: ProjectConfig) -> str:
    """Canonical derivatives/on-chain context for the enriched review."""
    import json

    try:
        from src.data_collectors import market_intelligence_store as mi

        lines = [
            "Point-in-time context. Missing/stale data is never positive evidence; "
            "these fields may reduce paper risk but never raise score or tier.", "",
            "| Symbol | venues | funding 8h | OI 24h | OI/price regime | on-chain |",
            "|---|---:|---:|---:|---|---|",
        ]
        with mi.connect() as conn:
            for symbol in ("BTC/USDT", "ETH/USDT", "SOL/USDT"):
                deriv = mi.latest_derivatives_context(conn, symbol)
                chain = mi.latest_onchain_context(conn, symbol)
                funding = deriv.get("funding_rate_8h")
                oi = deriv.get("oi_change_24h")
                funding_text = f"{funding:.6f}" if isinstance(funding, (int, float)) else "unknown"
                oi_text = f"{oi * 100:+.1f}%" if isinstance(oi, (int, float)) else "unknown"
                lines.append(
                    f"| {symbol} | {deriv.get('venue_count', 0)} | {funding_text} | {oi_text} | "
                    f"{deriv.get('oi_price_regime') or 'unknown'} | {chain.get('status') or 'unknown'} |"
                )
            verified = conn.execute(
                "SELECT COUNT(*) FROM asset_contract_registry WHERE verification_status='verified'"
            ).fetchone()[0]
            candidates = conn.execute(
                "SELECT COUNT(*) FROM asset_contract_registry WHERE verification_status!='verified'"
            ).fetchone()[0]
        lines += ["", f"Contract registry: verified={verified}, candidates/ambiguous={candidates}. "
                  "Ticker-only candidates have zero paper authority."]
        health_path = config.root / "data" / "diagnostics" / "market_intelligence_health.json"
        if health_path.exists():
            health = json.loads(health_path.read_text(encoding="utf-8"))
            lines.append(f"Health: {health.get('status')}; issues={len(health.get('issues') or [])}; "
                         f"as_of={health.get('as_of')}.")
        return _section("Derivatives / On-chain Intelligence", "\n".join(lines))
    except Exception as exc:
        return _section("Derivatives / On-chain Intelligence", f"_unavailable: {type(exc).__name__}_")


def build_packet(config: ProjectConfig, mode: str, source_report: str | None = None) -> str:
    """Build the LLM analysis packet and return as Markdown string.

    Parameters
    ----------
    source_report:
        Optional path to the report that triggered this packet refresh. Surfaced
        in the header so the LLM (and any auditor) can verify packet freshness
        against the underlying report.
    """
    requested_mode = mode.lower().strip()
    actual_mode = FALLBACK_MODE_MAP.get(requested_mode, requested_mode)
    fallback_note = ""
    if requested_mode != actual_mode:
        fallback_note = (
            f"User requested **{requested_mode}**, but `{requested_mode}` is **not implemented** "
            f"in code. Falling back to **{actual_mode}**. Long-term thesis overlay must be applied "
            "manually using `obsidian_vault/10_Trade_Idea_Format/Long_Term_Trade_Template.md`.\n"
        )

    if actual_mode not in {"scalp", "intraday", "swing", "review", "news-only"}:
        actual_mode = "intraday"
        fallback_note += (
            f"\nUnknown mode `{requested_mode}` — defaulting to **intraday**.\n"
        )

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    root = config.root
    processed = config.processed_dir
    vault = root / "obsidian_vault"
    prompts_dir = root / "prompts" / "system"

    # 1. Mode + system-prompt reminder.
    mode_block = _section(
        "Requested Mode",
        f"- Requested: `{requested_mode}`\n- Actual (implemented): `{actual_mode}`\n- Generated at (UTC): `{now}`\n"
        + (f"\n**Fallback note**: {fallback_note}" if fallback_note else ""),
    )

    # 1b. Weekend Mode status — surfaced near the top so the LLM applies the
    #     overlay before reading any candidate data.
    try:
        from src.analysis import weekend_mode as _weekend_mode

        weekend_cfg = _weekend_mode.load_config(root)
        weekend_status_obj = _weekend_mode.current_status(weekend_cfg, config.settings)
        weekend_block = _weekend_mode.status_markdown(weekend_status_obj, mode=actual_mode) + "\n"
        adjustments_path = processed / "weekend_mode_latest.json"
        if adjustments_path.exists():
            weekend_block += (
                "\n_Latest persisted adjustments_: `"
                + str(adjustments_path.relative_to(root))
                + "`\n"
            )
    except Exception as exc:
        weekend_block = (
            "## Weekend Mode Status\n\n_Could not evaluate Weekend Mode status: "
            f"{exc}_\n"
        )

    system_prompt_path = prompts_dir / "AI_TRADING_DESK_SYSTEM_PROMPT.md"
    system_prompt_excerpt = _safe_read(system_prompt_path, max_chars=4000)
    if system_prompt_excerpt:
        system_block = _section(
            "System Prompt Reminder",
            f"Source: `prompts/system/AI_TRADING_DESK_SYSTEM_PROMPT.md`\n\n{system_prompt_excerpt}",
        )
    else:
        system_block = _section(
            "System Prompt Reminder",
            "`prompts/system/AI_TRADING_DESK_SYSTEM_PROMPT.md` missing. "
            "Read the canonical file before running analysis.",
        )

    # 2. Fresh market context.
    context_path = processed / "context_for_llm.md"
    context_excerpt = _safe_read(context_path, max_chars=12000)
    context_block = _section(
        "Fresh Market Context",
        (
            f"Source: `{context_path.relative_to(root)}`\n\n{context_excerpt or '_missing — run `python -m src.cli daily-report`._'}"
        ),
    )

    last_update_path = processed / "market_summary" / "last_update.json"
    last_update_excerpt = _safe_read(last_update_path, max_chars=4000)
    last_update_block = _section(
        "Last Update Summary",
        f"Source: `{last_update_path.relative_to(root)}`\n\n```json\n{last_update_excerpt or '{}'}\n```",
    )

    # 3. Latest matching report.
    report_kind = {
        "scalp": "scalp",
        "intraday": "intraday",
        "swing": "swing",
        "review": "reviews",
        "news-only": "intraday",
    }.get(actual_mode, "intraday")
    latest_report = _latest_report(config, report_kind)
    if latest_report is None:
        latest_report = _latest_report(config, "daily")
    report_excerpt = ""
    report_path_str = ""
    if latest_report is not None:
        report_path_str = str(latest_report.relative_to(root))
        report_excerpt = _safe_read(latest_report, max_chars=12000)
    report_block = _section(
        f"Latest {report_kind.title()} Report",
        f"Source: `{report_path_str}`\n\n{report_excerpt or '_no report yet for this kind. Run the matching report command._'}",
    )

    # 4. Candidate ranking.
    ranked_path = processed / "candidates" / f"universe_ranked_candidates_{actual_mode}.json"
    if not ranked_path.exists():
        ranked_path = processed / "candidates" / "universe_ranked_candidates.json"
    ranked_excerpt = _safe_read(ranked_path, max_chars=6000)
    ranked_block = _section(
        "Candidate Universe (Stage 2 ranking)",
        f"Source: `{ranked_path.relative_to(root) if ranked_path.exists() else 'not generated yet'}`\n\n```json\n{ranked_excerpt or '{}'}\n```",
    )

    # 5. Latest trade-idea agent payload (for active ideas + rejected).
    trade_idea_dump = _latest_agent_output(config, "trade_idea_agent")
    trade_idea_excerpt = _safe_read(trade_idea_dump, max_chars=8000) if trade_idea_dump else ""
    trade_idea_block = _section(
        "Latest Trade-Idea Agent Output (A/B/C/rejected)",
        (
            f"Source: `{trade_idea_dump.relative_to(root) if trade_idea_dump else 'not generated yet'}`\n\n"
            f"```json\n{trade_idea_excerpt or '{}'}\n```"
        ),
    )

    # 6. news_trader_bridge snapshot.
    bridge_path = processed / "news_trader_bridge_latest.json"
    bridge_excerpt = _safe_read(bridge_path, max_chars=4000)
    bridge_block = _section(
        "News / Telegram Pulse (news_trader_bridge)",
        f"Source: `{bridge_path.relative_to(root) if bridge_path.exists() else 'unavailable'}`\n\n```json\n{bridge_excerpt or '{}'}\n```",
    )

    # 7. Obsidian rules + checklists references.
    mode_file_map = {
        "scalp": "obsidian_vault/02_Trading_Modes/Scalp_Mode.md",
        "intraday": "obsidian_vault/02_Trading_Modes/Intraday_Mode.md",
        "swing": "obsidian_vault/02_Trading_Modes/Swing_Mode.md",
        "review": "obsidian_vault/02_Trading_Modes/Trading_Modes_Overview.md",
        "news-only": "obsidian_vault/05_News_Telegram_Catalysts_Sentiment/News_System_Overview.md",
    }
    rules_paths = [
        "obsidian_vault/00_System_Overview/System_Principles.md",
        "obsidian_vault/00_System_Overview/LLM_Operating_Instructions.md",
        "obsidian_vault/00_System_Overview/Implemented_vs_Recommended.md",
        "obsidian_vault/03_Risk_Management/No_Trade_Conditions.md",
        "obsidian_vault/09_Scoring_System/Scoring_Overview.md",
        "obsidian_vault/09_Scoring_System/Score_Caps.md",
        "obsidian_vault/15_LLM_Context/System_Prompt_For_Analysis.md",
        "obsidian_vault/15_LLM_Context/Pre_Analysis_Checklist.md",
        "obsidian_vault/15_LLM_Context/Post_Analysis_Checklist.md",
        "obsidian_vault/15_LLM_Context/Current_Context_For_LLM.md",
        mode_file_map.get(actual_mode, mode_file_map["intraday"]),
    ]
    if actual_mode in {"news-only"} or requested_mode == "news-only":
        rules_paths.extend(
            [
                "obsidian_vault/05_News_Telegram_Catalysts_Sentiment/Telegram_News_Evaluation.md",
                "obsidian_vault/05_News_Telegram_Catalysts_Sentiment/News_Verification.md",
                "obsidian_vault/05_News_Telegram_Catalysts_Sentiment/Telegram_Integration.md",
            ]
        )
    rules_block = _section(
        "Obsidian Rules To Load (read these before answering)",
        _bullet_list(f"`{p}`" for p in rules_paths),
    )

    # 8. Recent trade-journal summaries.
    journal_potential = vault / "11_Trade_Journal" / "Potential_Trades"
    journal_watchlist = vault / "11_Trade_Journal" / "Watchlist_Ideas"
    journal_rejected = vault / "11_Trade_Journal" / "Rejected_Ideas"
    journal_reviews = vault / "11_Trade_Journal" / "Reviews"
    journal_block = _section(
        "Recent Trade Journal (Obsidian)",
        "**Potential_Trades** (latest 5):\n"
        + _bullet_list(str(p.relative_to(root)) for p in _list_recent_vault_files(journal_potential))
        + "\n\n**Watchlist_Ideas** (latest 5):\n"
        + _bullet_list(str(p.relative_to(root)) for p in _list_recent_vault_files(journal_watchlist))
        + "\n\n**Rejected_Ideas** (latest 5):\n"
        + _bullet_list(str(p.relative_to(root)) for p in _list_recent_vault_files(journal_rejected))
        + "\n\n**Reviews** (latest 5):\n"
        + _bullet_list(str(p.relative_to(root)) for p in _list_recent_vault_files(journal_reviews)),
    )

    # 9. Recent news intelligence.
    news_useful = vault / "12_News_Intelligence_Journal" / "Useful_News"
    news_useless = vault / "12_News_Intelligence_Journal" / "Useless_News"
    news_fake = vault / "12_News_Intelligence_Journal" / "Fake_or_Unverified_News"
    news_moving = vault / "12_News_Intelligence_Journal" / "Market_Moving_News"
    news_telegram = vault / "12_News_Intelligence_Journal" / "Telegram_News"
    news_block = _section(
        "Recent News Intelligence (Obsidian)",
        "**Useful_News** (latest 5):\n"
        + _bullet_list(str(p.relative_to(root)) for p in _list_recent_vault_files(news_useful))
        + "\n\n**Market_Moving_News** (latest 5):\n"
        + _bullet_list(str(p.relative_to(root)) for p in _list_recent_vault_files(news_moving))
        + "\n\n**Telegram_News** (latest 5):\n"
        + _bullet_list(str(p.relative_to(root)) for p in _list_recent_vault_files(news_telegram))
        + "\n\n**Useless_News** (latest 3):\n"
        + _bullet_list(
            str(p.relative_to(root)) for p in _list_recent_vault_files(news_useless, max_items=3)
        )
        + "\n\n**Fake_or_Unverified_News** (latest 3):\n"
        + _bullet_list(
            str(p.relative_to(root)) for p in _list_recent_vault_files(news_fake, max_items=3)
        ),
    )

    # 10. Active watchlist (from latest trade-idea-agent JSON).
    active_watchlist_block = _section(
        "Active Watchlist (from latest report)",
        "The latest trade-idea-agent JSON (above) contains every C-tier symbol with its setup. "
        "Promote C-tier names to `Potential_Trades` only after a confirmed C→B/A upgrade via "
        "`python -m src.cli monitor-watchlist`.",
    )

    # 11. Recent lessons.
    improvement_backlog = vault / "13_Debugging_and_Improvement" / "Improvement_Backlog.md"
    lessons_excerpt = _safe_read(improvement_backlog, max_chars=4000)
    lessons_block = _section(
        "Recent Lessons / Improvement Backlog",
        f"Source: `{improvement_backlog.relative_to(root) if improvement_backlog.exists() else 'missing'}`\n\n{lessons_excerpt or '_no entries yet_'}",
    )

    # 12. Pre-analysis checklist (embedded).
    pre_checklist_path = vault / "15_LLM_Context" / "Pre_Analysis_Checklist.md"
    pre_checklist = _safe_read(pre_checklist_path, max_chars=5000)
    pre_checklist_block = _section(
        "Pre-Analysis Checklist (embedded)",
        pre_checklist or "_missing — read `obsidian_vault/15_LLM_Context/Pre_Analysis_Checklist.md`._",
    )

    # 13. Required output format.
    output_format_block = _section(
        "Required Output Format",
        (
            "Every trade idea card must include:\n\n"
            "- symbol (e.g. SOL/USDT)\n"
            "- mode (scalp / intraday / swing)\n"
            "- direction (long / short / watchlist / no_trade)\n"
            "- tier (A / B / C / rejected)\n"
            "- score + confidence + data_confidence\n"
            "- exchange focus (binance / bybit / mexc)\n"
            "- market regime alignment\n"
            "- entry zone\n"
            "- invalidation (timeframe close beyond level)\n"
            "- targets (TP1 / TP2 / TP3)\n"
            "- thesis (1 paragraph)\n"
            "- key evidence (3–6 bullets)\n"
            "- Telegram / news impact (verified / single_source / rumor)\n"
            "- counter-thesis (1–3 bullets)\n"
            "- do-not-enter conditions\n"
            "- monitoring checklist\n"
            "- caps active (or `none`)\n"
            "- logging destination (vault folder + filename)\n\n"
            "Finish with: compact trade table, risk warnings, what to monitor next, weak/missing data, logging actions taken."
        ),
    )

    signal_perf_block = _build_signal_performance_block(config)
    market_intelligence_block = _build_market_intelligence_block(config)
    catalyst_block = _build_catalyst_block(config)
    news_risk_block = _build_news_risk_events_block(config)
    # 2026-06-09: Strategy playbook context block. Lets Opus reason about
    # signals by named strategy + actionability tier instead of only by
    # symbol/score. Source: STRATEGY_PLAYBOOK_AUDIT.md and CURRENT_TRADING_PLAYBOOKS.md.
    playbook_block = _build_playbook_context_block()
    sizing_block = _build_sizing_context_block()
    # 2026-07-02: Stocks Position Framework (shadow-only research). Distinct from stocks intraday
    # and from the deprecated/removed old stocks swing/invest. Annotation only — never actionable.
    stocks_position_block = _build_stocks_position_framework_block()

    sections = [
        mode_block,
        weekend_block,
        system_block,
        playbook_block,
        sizing_block,
        stocks_position_block,
        context_block,
        last_update_block,
        report_block,
        ranked_block,
        trade_idea_block,
        bridge_block,
        rules_block,
        journal_block,
        news_block,
        catalyst_block,
        news_risk_block,
        active_watchlist_block,
        signal_perf_block,
        market_intelligence_block,
        lessons_block,
        pre_checklist_block,
        output_format_block,
    ]

    source_line = ""
    if source_report:
        source_line = f"_Source report_: `{source_report}`\n"
    header = (
        f"# LLM Analysis Packet\n\n"
        f"_Generated by `python -m src.cli prepare-analysis --mode {requested_mode}` at {now} UTC._\n"
        f"{source_line}"
    )
    return header + "\n" + "\n".join(sections)


def write_packet(config: ProjectConfig, mode: str, source_report: str | None = None) -> Path:
    """Write the packet to data/processed/llm_analysis_packet.md and return path.

    Parameters
    ----------
    source_report:
        Optional report path to record in the packet header for freshness audit.
    """
    content = build_packet(config, mode, source_report=source_report)
    target = config.processed_dir / "llm_analysis_packet.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return target
