from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from src.config import ProjectConfig
from src.models import (
    CatalystSummary,
    CoverageAudit,
    CrowdAttention,
    CrowdWatchSummary,
    DerivativesSummary,
    ExchangeConfirmation,
    MacroGeopoliticsSummary,
    MarketRegime,
    MomentumCandidate,
    MultiExchangeDerivativesSummary,
    NarrativeSummary,
    RejectedIdea,
    SocialAttentionSummary,
    TradeIdea,
)
from src.reports.markdown_templates import trade_idea_markdown
from src.utils.formatting import bullet_list, fmt_pct
from src.utils.time import report_timestamp, utc_now


class ReportBuilder:
    def __init__(self, config: ProjectConfig):
        self.config = config
        self.timezone = config.settings.get("project", {}).get("timezone", "UTC")

    def build_daily(
        self,
        regime: MarketRegime,
        candidates: list[MomentumCandidate],
        ideas: list[TradeIdea],
        data_freshness: str,
        derivatives: dict[str, DerivativesSummary] | None = None,
        news_output: dict | None = None,
        catalysts: dict[str, CatalystSummary] | None = None,
        narratives: dict[str, NarrativeSummary] | None = None,
        macro: MacroGeopoliticsSummary | None = None,
        social_attention: dict[str, SocialAttentionSummary] | None = None,
        crowd_watch: CrowdWatchSummary | None = None,
        multi_derivatives: dict[str, MultiExchangeDerivativesSummary] | None = None,
        coverage: CoverageAudit | None = None,
        exchange_confirmations: dict[str, ExchangeConfirmation] | None = None,
        crowd_attention: dict[str, CrowdAttention] | None = None,
        rejected_ideas: list[RejectedIdea] | None = None,
        candidate_funnel: dict | None = None,
        exchange_status: dict | None = None,
        mode: str = "intraday",
        expansion_result: Any = None,
    ) -> str:
        derivatives = derivatives or {}
        news_output = news_output or {}
        catalysts = catalysts or {}
        narratives = narratives or {}
        social_attention = social_attention or {}
        multi_derivatives = multi_derivatives or {}
        exchange_confirmations = exchange_confirmations or {}
        crowd_attention = crowd_attention or {}
        rejected_ideas = rejected_ideas or []
        candidate_funnel = candidate_funnel or {}
        exchange_status = exchange_status or {}
        a_tier = [idea for idea in ideas if idea.tier == "A" and idea.direction in {"long", "short"}]
        b_tier = [idea for idea in ideas if idea.tier == "B" and idea.direction in {"long", "short"}]
        c_tier = [idea for idea in ideas if idea.tier == "C" or idea.direction == "watchlist only"]
        valid_ideas = a_tier + b_tier
        watchlist = c_tier
        strongest = candidates[:8]
        weakest = sorted(
            candidates,
            key=lambda item: item.relative_strength_btc
            if item.relative_strength_btc is not None
            else 999,
        )[:5]
        unusual_volume = [
            item for item in candidates if item.volume_ratio is not None and item.volume_ratio >= 1.5
        ][:8]

        lines = [
            "# Crypto AI Desk Report",
            "",
            f"Date: {datetime.now().strftime('%Y-%m-%d')}",
            f"Generated at: {report_timestamp(self.timezone)}",
            f"Mode: {mode}",
            f"Data freshness: {data_freshness}",
            f"Market regime: {regime.label} ({regime.risk_mode})",
            "",
        ]
        # Mode-Viability-Audit (2026-06-09): crypto SCALP stays active for
        # data collection but is flagged low-confidence in user-facing
        # surfaces. Entry edge is real (100% of expired had positive MFE,
        # avg +0.54R) but TP1/2h horizon mismatch caps capture. Re-audit at
        # 20 closed A/B scalp signals. No scoring/TP/SL changes here.
        if mode == "scalp":
            lines.append(
                "> **CRYPTO SCALP — low confidence.** Entry edge exists "
                "(100% of expired scalps had positive MFE, avg +0.54R) but "
                "TP1/2h horizon mismatch caps capture (1W/7L over 14d, "
                "PF 0.14). Scalp remains active for data collection; re-audit "
                "at 20 closed A/B scalp signals. Treat A/B scalp ideas with "
                "lower confidence than intraday/swing."
            )
            lines.append("")
        lines.extend([
            "## 0. Exchange Coverage & Candidate Funnel",
            "",
            self._exchange_coverage_section(exchange_status),
            "",
            self._funnel_section(candidate_funnel),
            "",
            "## 1. Market Regime",
            "",
            f"- BTC trend: {regime.btc_trend}",
            f"- ETH trend: {regime.eth_trend}",
            f"- Altcoin breadth above EMA20: {fmt_pct(regime.alt_breadth.get('above_ema20_pct'))}",
            f"- Altcoin breadth above EMA50: {fmt_pct(regime.alt_breadth.get('above_ema50_pct'))}",
            f"- Volatility: {regime.volatility}",
            f"- Recommended trading style: {regime.recommended_style}",
            f"- Explanation: {regime.explanation}",
            "",
            "## 2. Where Money Is Flowing",
            "",
            "### Strongest Symbols",
            bullet_list(
                [
                    f"{item.symbol}: score {item.score}, 24h {fmt_pct(item.return_24h)}, "
                    f"RS vs BTC {fmt_pct(item.relative_strength_btc)}, volume {item.volume_ratio or 'n/a'}x"
                    for item in strongest
                ]
            ),
            "",
            "### Weakest Symbols",
            bullet_list(
                [
                    f"{item.symbol}: bias {item.direction_bias}, 24h {fmt_pct(item.return_24h)}, "
                    f"RS vs BTC {fmt_pct(item.relative_strength_btc)}"
                    for item in weakest
                ]
            ),
            "",
            "### Unusual Volume",
            bullet_list(
                [
                    f"{item.symbol}: {item.volume_ratio}x 20-period average, tags {', '.join(item.reason_tags)}"
                    for item in unusual_volume
                ]
            ),
            "",
            "### Narrative Heatmap",
            self._narrative_section(narratives),
            "",
            "## 3. Derivatives Overview",
            "",
            self._derivatives_section(derivatives, strongest),
            "",
            "### Bybit/OKX Cross-Check",
            self._multi_derivatives_section(multi_derivatives, strongest),
            "",
            "## 4. Macro, Geopolitics, Crowd",
            "",
            self._macro_crowd_section(macro, social_attention, crowd_watch),
            "",
            "## 5. News and Catalysts",
            "",
            self._news_catalyst_section(news_output, catalysts),
            "",
            "## 5b. Structured Catalyst / Narrative (auto-collected)",
            "",
            self._structured_catalyst_section(),
            "",
            "## 5c. Production News Risk Warnings (risk-only)",
            "",
            self._news_risk_section(),
            "",
            "## 6. Top Trade Ideas",
            "",
            "### A-tier (high conviction, no active caps)",
            "",
        ])

        if a_tier:
            for index, idea in enumerate(a_tier, start=1):
                lines.append(trade_idea_markdown(index, idea))
        else:
            lines.append("- No A-tier setups found. Do not force a trade.")

        lines.extend(["", "### B-tier (valid but one or two confirmations missing)", ""])
        if b_tier:
            for index, idea in enumerate(b_tier, start=1):
                lines.append(trade_idea_markdown(index, idea))
        else:
            lines.append("- No B-tier setups found.")

        lines.extend(["", "## 7. C-tier / Watchlist", ""])
        if watchlist:
            for index, idea in enumerate(
                watchlist[: int(self.config.report_setting("max_watchlist", 10))], start=1
            ):
                lines.append(trade_idea_markdown(index, idea))
        else:
            lines.append("- Nothing worth stalking yet.")

        lines.extend(
            [
                "",
                "## 7b. Rejected / Not Ready",
                "",
                self._rejected_section(rejected_ideas),
                "",
                "## 7c. Multi-Exchange Confirmation",
                "",
                self._exchange_confirmation_section(exchange_confirmations, ideas),
                "",
                "## 7d. Crowd Attention Stages",
                "",
                self._crowd_attention_section(crowd_attention, ideas, candidates),
            ]
        )

        # Crypto Signal Expansion v1 — read-only watchlist of additional names
        # surfaced beyond the top-N deep analysis cap. Informational only;
        # does NOT register proposed_signals. See spec for the contract.
        if expansion_result is not None:
            try:
                from src.agents.discovery_expansion_agent import (
                    render_expansion_watchlist_markdown,
                )
                lines.append("")
                lines.append(render_expansion_watchlist_markdown(expansion_result))
            except Exception:
                pass

        lines.extend(
            [
                "",
                "## 8. No-Trade Warnings",
                "",
                bullet_list(
                    regime.warnings
                    + [
                        *(macro.warnings if macro else []),
                        *(coverage.warnings if coverage else []),
                        "If BTC loses local support, reduce long aggression immediately.",
                        "Avoid extended entries. The system prefers missing a move over chasing a bad one.",
                        "If derivatives/news are stale or missing for a symbol, reduce confidence.",
                    ]
                ),
                "",
                "## 9. Data Coverage / Blindspots",
                "",
                self._coverage_section(coverage),
                "",
                self._signal_performance_section(),
                "",
                "## 10. Final Summary",
                "",
                self._final_summary(regime, valid_ideas, watchlist),
                "",
            ]
        )
        return "\n".join(lines)

    def _signal_performance_section(self) -> str:
        """Render the shared Recent Signal Performance block for crypto.

        Read-only: this block reflects historical outcomes; it never feeds
        back into scoring or rule changes.
        """
        from src.signals.report_section import build_signal_performance_block

        return build_signal_performance_block(self.config, asset_class="crypto")

    def _news_risk_section(self) -> str:
        """PRODUCTION news RISK warnings (risk-only): block_requires_operator_review /
        do_not_chase / risk_warning from STRONG events (SEC/legal/hack/delisting/unlock/
        maintenance/offering + earnings). NEVER a buy/sell, NEVER a score/tier change.
        Best-effort — never fatal to the report."""
        try:
            from src.news.risk_advisory import compute_risk_warnings, render_markdown
            db = getattr(self.config, "db_path", None)
            return render_markdown(compute_risk_warnings(str(db) if db else None))
        except Exception as exc:  # noqa: BLE001 — advisory only
            return f"- Production risk warnings unavailable ({exc})"

    def _structured_catalyst_section(self) -> str:
        """Compact catalyst / narrative section for the markdown report
        (PART 1 of catalyst layer). Reads `data/catalysts/<today>/`."""

        import json
        from datetime import datetime, timezone

        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        cat_dir = self.config.root / "data" / "catalysts" / today
        events_path = cat_dir / "catalyst_events.jsonl"
        baskets_path = cat_dir / "narrative_baskets.jsonl"

        if not events_path.exists() and not baskets_path.exists():
            return (
                "_Catalyst scan has not run yet today. Run "
                "`python -m src.cli catalyst-scan` to populate._"
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
            return f"_Could not load catalyst JSONL: {exc}_"

        seen: set[str] = set()
        deduped: list[dict] = []
        for ev in reversed(events):
            cid = ev.get("catalyst_id")
            if cid and cid not in seen:
                seen.add(cid)
                deduped.append(ev)

        lines = [
            f"- Unique events today: **{len(deduped)}**; baskets: **{len(baskets)}**.",
            f"- Files: `data/catalysts/{today}/catalyst_events.jsonl`, "
            f"`data/catalysts/{today}/narrative_baskets.jsonl`.",
        ]
        if baskets:
            lines.append("- Active narrative baskets:")
            for b in baskets[:5]:
                primary = ", ".join(b.get("primary_symbols") or []) or "—"
                lines.append(
                    f"  - **{b.get('basket_name')}** "
                    f"(playbook `{b.get('suggested_playbook')}`, "
                    f"source {b.get('source_quality')}, fresh {b.get('freshness')}) "
                    f"primary: {primary}"
                )

        # Surface high-confidence + legal categories explicitly.
        notable = [
            e for e in deduped
            if e.get("catalyst_type") in {
                "legal_risk", "exploit_hack", "exchange_listing",
                "exchange_delisting", "margin_delisting", "token_unlock",
                "hodler_airdrop", "mainnet_launch", "regulatory_sector_headline",
            }
        ]
        if notable:
            # Rank by importance (falls back to 0.0 for legacy rows written
            # before importance scoring existed) so the most consequential
            # catalysts surface first instead of insertion order.
            notable.sort(key=lambda e: float(e.get("importance") or 0.0), reverse=True)
            lines.append("- Notable events:")
            for e in notable[:8]:
                sym = e.get("symbol") or "(basket)"
                lines.append(
                    f"  - **{sym}** [{e.get('catalyst_type')}] "
                    f"{(e.get('title') or '')[:140]} ({e.get('source')})"
                )

        lines.append(
            "- _Auto-collected enrichment; does not change scoring. "
            "Manual Opus review consumes the JSONL via the `enriched-review` skill._"
        )
        return "\n".join(lines)

    def build_context_for_llm(
        self,
        regime: MarketRegime,
        candidates: list[MomentumCandidate],
        ideas: list[TradeIdea],
        data_freshness: str,
        derivatives: dict[str, DerivativesSummary] | None = None,
        news_output: dict | None = None,
        catalysts: dict[str, CatalystSummary] | None = None,
        narratives: dict[str, NarrativeSummary] | None = None,
        macro: MacroGeopoliticsSummary | None = None,
        social_attention: dict[str, SocialAttentionSummary] | None = None,
        crowd_watch: CrowdWatchSummary | None = None,
        multi_derivatives: dict[str, MultiExchangeDerivativesSummary] | None = None,
        coverage: CoverageAudit | None = None,
        exchange_confirmations: dict[str, ExchangeConfirmation] | None = None,
        crowd_attention: dict[str, CrowdAttention] | None = None,
        rejected_ideas: list[RejectedIdea] | None = None,
        candidate_funnel: dict | None = None,
        exchange_status: dict | None = None,
        mode: str = "intraday",
        expansion_result: Any = None,
    ) -> str:
        derivatives = derivatives or {}
        news_output = news_output or {}
        catalysts = catalysts or {}
        narratives = narratives or {}
        social_attention = social_attention or {}
        multi_derivatives = multi_derivatives or {}
        exchange_confirmations = exchange_confirmations or {}
        crowd_attention = crowd_attention or {}
        rejected_ideas = rejected_ideas or []
        candidate_funnel = candidate_funnel or {}
        exchange_status = exchange_status or {}
        top = candidates[:10]
        lower_volume = self._lower_volume_symbols()
        a_tier = [idea for idea in ideas if idea.tier == "A" and idea.direction in {"long", "short"}]
        b_tier = [idea for idea in ideas if idea.tier == "B" and idea.direction in {"long", "short"}]
        active = a_tier + b_tier
        watch = [idea for idea in ideas if idea.tier == "C" or idea.direction == "watchlist only"][:10]
        ctx = "\n".join(
            [
                "# Crypto AI Desk Context",
                "",
                f"Generated at: {utc_now().isoformat()}",
                f"Mode: {mode}",
                f"Data freshness: {data_freshness}",
                "",
                "## Exchange Coverage",
                self._exchange_coverage_section(exchange_status),
                "",
                "## Candidate Funnel",
                self._funnel_section(candidate_funnel),
                "",
                "## Market Regime",
                f"- Label: {regime.label}",
                f"- Risk mode: {regime.risk_mode}",
                f"- Confidence: {regime.confidence}/100",
                f"- Style: {regime.recommended_style}",
                f"- Breadth: {regime.alt_breadth}",
                "",
                "## Top Movers / Relative Strength",
                bullet_list(
                    [
                        f"{item.symbol}: bias {item.direction_bias}, score {item.score}, "
                        f"24h {fmt_pct(item.return_24h)}, RS/BTC {fmt_pct(item.relative_strength_btc)}, "
                        f"vol {item.volume_ratio or 'n/a'}x, tags {', '.join(item.reason_tags)}"
                        for item in top
                    ]
                ),
                "",
                "## Lower-Cap / Expanded Universe Leaders",
                bullet_list(
                    [
                        f"{item.symbol}: bias {item.direction_bias}, score {item.score}, "
                        f"24h {fmt_pct(item.return_24h)}, RS/BTC {fmt_pct(item.relative_strength_btc)}, "
                        f"vol {item.volume_ratio or 'n/a'}x, tags {', '.join(item.reason_tags)}"
                        for item in candidates
                        if item.symbol in lower_volume
                    ][:12]
                ),
                "",
                "## Derivatives",
                bullet_list(
                    [
                        f"{symbol}: {item.interpretation}; funding {item.funding_rate if item.funding_rate is not None else 'n/a'}; "
                        f"OI change {item.oi_change_pct if item.oi_change_pct is not None else 'n/a'}%; crowding {item.crowding_risk}"
                        for symbol, item in derivatives.items()
                        if item.data_available
                    ][:10]
                ),
                "",
                "## External Derivatives Cross-Check",
                bullet_list(
                    [
                        f"{symbol}: {item.consensus}; venues={item.exchanges_available}; "
                        f"funding={item.funding_rates}; crowding={item.crowding_risk}"
                        for symbol, item in multi_derivatives.items()
                        if item.exchanges_available
                    ][:10]
                ),
                "",
                "## Macro / Geopolitics",
                self._macro_context(macro),
                "",
                "## Social Attention / Crowd",
                bullet_list(
                    [
                        f"{symbol}: attention {item.attention_score}/100, mentions {item.mention_count}, "
                        f"sources {item.sources}, warnings {item.warnings}"
                        for symbol, item in social_attention.items()
                    ][:10]
                ),
                "",
                "## KOL / Crowd Watch",
                self._crowd_context(crowd_watch),
                "",
                "## News / Events",
                bullet_list(
                    [
                        f"{item.get('title')} ({item.get('source')}) symbols={item.get('detected_symbols', [])}"
                        for item in news_output.get("top_news", [])[:10]
                    ]
                ),
                "",
                "## Catalysts",
                bullet_list(
                    [
                        f"{symbol}: {item.interpretation}; catalysts={item.catalysts[:2]}; risks={item.risk_events[:2]}"
                        for symbol, item in catalysts.items()
                        if item.catalysts or item.risk_events
                    ][:10]
                ),
                "",
                "## Narratives",
                bullet_list(
                    [
                        f"{item.narrative}: heat {item.heat_score}/100, status {item.status}, representatives {item.representative_symbols}"
                        for item in narratives.values()
                    ][:10]
                ),
                "",
                "## A-tier Ideas",
                bullet_list(
                    [
                        f"{idea.direction.upper()} {idea.symbol} [tier {idea.tier}, focus {idea.exchange_focus}]: "
                        f"score {idea.score}, conf {idea.confidence}, data_conf {idea.data_confidence}, "
                        f"entry {idea.entry_plan}, invalidation {idea.invalidation}"
                        for idea in a_tier
                    ]
                    or ["No A-tier ideas."]
                ),
                "",
                "## B-tier Ideas",
                bullet_list(
                    [
                        f"{idea.direction.upper()} {idea.symbol} [tier {idea.tier}, focus {idea.exchange_focus}]: "
                        f"score {idea.score}, conf {idea.confidence}, data_conf {idea.data_confidence}, "
                        f"entry {idea.entry_plan}, invalidation {idea.invalidation}"
                        for idea in b_tier
                    ]
                    or ["No B-tier ideas."]
                ),
                "",
                "## C-tier / Watchlist",
                bullet_list(
                    [f"{idea.symbol}: score {idea.score}, {idea.thesis}" for idea in watch]
                    or ["Nothing on watchlist."]
                ),
                "",
                "## Rejected / Not Ready",
                bullet_list(
                    [
                        f"{item.symbol} ({item.direction_bias}, score {item.score}): {item.primary_reason}. "
                        f"Reasons: {'; '.join(item.reasons[:3])}"
                        for item in rejected_ideas[:15]
                    ]
                    or ["No rejected ideas."]
                ),
                "",
                "## Multi-Exchange Confirmation",
                bullet_list(
                    [
                        f"{symbol}: {item.interpretation} (score {item.confirmation_score}/100, "
                        f"exchanges {item.exchanges_listed}, focus {item.suggested_exchange_focus})"
                        for symbol, item in list(exchange_confirmations.items())[:12]
                    ]
                    or ["No fusion data."]
                ),
                "",
                "## Crowd Attention",
                bullet_list(
                    [
                        f"{item.symbol}: stage {item.stage}, attention {item.attention_score}/100, "
                        f"crowding {item.crowding_risk}/100, confidence {item.confidence}"
                        for item in sorted(
                            crowd_attention.values(),
                            key=lambda i: i.attention_score,
                            reverse=True,
                        )[:10]
                    ]
                    or ["No crowd staging."]
                ),
                "",
                "## Risk Warnings",
                bullet_list(
                    regime.warnings
                    + [
                        *(macro.warnings if macro else []),
                        *(coverage.warnings if coverage else []),
                        "Missing derivatives and news reduce confidence.",
                        "No clear invalidation means no active trade.",
                        "Do not chase moves extended more than 2 ATR from the entry zone.",
                    ]
                ),
                "",
                "## Data Coverage / Missing Intelligence",
                self._coverage_section(coverage),
                "",
            ]
        )
        # Crypto Signal Expansion v1 — context_for_llm append.
        if expansion_result is not None:
            try:
                from src.agents.discovery_expansion_agent import (
                    render_expansion_watchlist_markdown,
                )
                ctx += "\n" + render_expansion_watchlist_markdown(expansion_result)
            except Exception:
                pass
        return ctx

    def report_path(self, kind: str = "daily") -> Path:
        now = utc_now()
        if kind == "daily":
            filename = f"{now.strftime('%Y-%m-%d')}_daily_report.md"
            return Path("data") / "reports" / "daily" / filename
        if kind == "scalp":
            filename = f"{now.strftime('%Y-%m-%d_%H-%M')}_scalp_report.md"
            return Path("data") / "reports" / "scalp" / filename
        if kind == "swing":
            filename = f"{now.strftime('%Y-%m-%d_%H-%M')}_swing_report.md"
            return Path("data") / "reports" / "swing" / filename
        filename = f"{now.strftime('%Y-%m-%d_%H-%M')}_intraday_report.md"
        return Path("data") / "reports" / "intraday" / filename

    def _lower_volume_symbols(self) -> set[str]:
        path = self.config.root / "data" / "processed" / "market_summary" / "universe_latest.json"
        if not path.exists():
            return set()
        try:
            import json

            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return set()
        return {str(symbol) for symbol in payload.get("lower_volume_symbols", [])}

    @staticmethod
    def _derivatives_section(
        derivatives: dict[str, DerivativesSummary], strongest: list[MomentumCandidate]
    ) -> str:
        if not derivatives:
            return "- No derivatives data available; confidence is reduced."
        rows = []
        for candidate in strongest[:8]:
            item = derivatives.get(candidate.symbol)
            if item is None:
                continue
            if not item.data_available:
                rows.append(f"{candidate.symbol}: futures data unavailable.")
                continue
            rows.append(
                f"{candidate.symbol}: {item.interpretation}; funding {item.funding_rate if item.funding_rate is not None else 'n/a'}; "
                f"OI 24h {item.oi_change_pct if item.oi_change_pct is not None else 'n/a'}%; long/short {item.long_short_ratio if item.long_short_ratio is not None else 'n/a'}; crowding {item.crowding_risk}."
            )
        return bullet_list(rows)

    @staticmethod
    def _multi_derivatives_section(
        multi_derivatives: dict[str, MultiExchangeDerivativesSummary],
        strongest: list[MomentumCandidate],
    ) -> str:
        if not multi_derivatives:
            return "- No Bybit/OKX cross-check available."
        rows = []
        for candidate in strongest[:8]:
            item = multi_derivatives.get(candidate.symbol)
            if item is None:
                continue
            if not item.exchanges_available:
                rows.append(f"{candidate.symbol}: no external futures data.")
                continue
            rows.append(
                f"{candidate.symbol}: {item.consensus}; venues {', '.join(item.exchanges_available)}; "
                f"funding {item.funding_rates or 'n/a'}; crowding {item.crowding_risk}."
            )
        return bullet_list(rows or ["No strongest-symbol external derivatives rows available."])

    @staticmethod
    def _macro_crowd_section(
        macro: MacroGeopoliticsSummary | None,
        social_attention: dict[str, SocialAttentionSummary],
        crowd_watch: CrowdWatchSummary | None,
    ) -> str:
        rows = []
        if macro:
            rows.append(
                f"Macro/geopolitics: risk {macro.risk_score}/100, BTC bias {macro.btc_bias}. "
                f"{macro.explanation}"
            )
            rows.extend([f"Macro headline: {headline}" for headline in macro.headlines[:4]])
        else:
            rows.append("Macro/geopolitics: no structured macro scan available.")

        if social_attention:
            rows.append("Social attention leaders:")
            rows.extend(
                [
                    f"{symbol}: attention {item.attention_score}/100 from {item.mention_count} mention(s); "
                    f"sources {', '.join(item.sources)}"
                    for symbol, item in list(social_attention.items())[:6]
                ]
            )
        else:
            rows.append("Social attention: no symbol-level hits from configured free sources.")

        if crowd_watch:
            if crowd_watch.active_signals:
                rows.append("Manual KOL/crowd signals:")
                rows.extend(crowd_watch.active_signals[:5])
            rows.extend(crowd_watch.warnings[:3])
        else:
            rows.append("KOL/crowd watch: not configured.")
        return bullet_list(rows)

    @staticmethod
    def _news_catalyst_section(
        news_output: dict, catalysts: dict[str, CatalystSummary]
    ) -> str:
        lines: list[str] = []
        top_news = news_output.get("top_news", [])[:8]
        if top_news:
            lines.append("Top news:")
            lines.extend(
                [
                    f"{item.get('title')} ({item.get('source')}; symbols {item.get('detected_symbols', [])}; verification {item.get('verification_status')})"
                    for item in top_news
                ]
            )
        else:
            lines.append("No RSS news items available.")
        catalyst_rows = [
            f"{symbol}: {item.interpretation}; catalysts {item.catalysts[:2]}; risks {item.risk_events[:2]}"
            for symbol, item in catalysts.items()
            if item.catalysts or item.risk_events
        ][:8]
        if catalyst_rows:
            lines.append("Catalysts/events:")
            lines.extend(catalyst_rows)
        return bullet_list(lines)

    @staticmethod
    def _narrative_section(narratives: dict[str, NarrativeSummary]) -> str:
        if not narratives:
            return "- No narrative heatmap available."
        return bullet_list(
            [
                f"{item.narrative}: heat {item.heat_score}/100, attention {item.attention_score}/100, "
                f"momentum {item.momentum_score}/100, volume {item.volume_score}/100, risk {item.risk_score}/100, "
                f"status {item.status}, coins {', '.join(item.representative_symbols) or 'n/a'}"
                for item in list(narratives.values())[:8]
            ]
        )

    @staticmethod
    def _macro_context(macro: MacroGeopoliticsSummary | None) -> str:
        if not macro:
            return "- No macro/geopolitics summary available."
        return bullet_list(
            [
                f"Risk score: {macro.risk_score}/100",
                f"BTC bias: {macro.btc_bias}",
                f"Themes: {', '.join(macro.themes) if macro.themes else 'none detected'}",
                f"Explanation: {macro.explanation}",
                *[f"Headline: {headline}" for headline in macro.headlines[:5]],
                *macro.warnings,
            ]
        )

    @staticmethod
    def _crowd_context(crowd_watch: CrowdWatchSummary | None) -> str:
        if not crowd_watch:
            return "- No crowd watch summary available."
        return bullet_list(
            [
                f"Configured sources: {', '.join(crowd_watch.configured_sources) or 'none'}",
                f"Manual signal count: {crowd_watch.signal_count}",
                f"Symbols: {', '.join(crowd_watch.symbols) or 'none'}",
                *crowd_watch.active_signals[:8],
                *crowd_watch.warnings,
            ]
        )

    @staticmethod
    def _coverage_section(coverage: CoverageAudit | None) -> str:
        if not coverage:
            return "- No data coverage audit available."
        rows = [f"{key}: {value}" for key, value in coverage.source_health.items()]
        rows.extend([f"Missing: {item}" for item in coverage.missing_sources])
        rows.extend([f"Partial/stale: {item}" for item in coverage.stale_or_partial_sources])
        rows.append("Important blindspots still not automated:")
        rows.extend(coverage.important_blindspots[:8])
        return bullet_list(rows)

    @staticmethod
    def _exchange_coverage_section(exchange_status: dict) -> str:
        if not exchange_status or not exchange_status.get("per_exchange"):
            return "- Exchange coverage data not available."
        rows = [f"Anchor exchange: {exchange_status.get('anchor_exchange')}"]
        for exchange, block in exchange_status["per_exchange"].items():
            failed = block.get("ohlcv_failed") or {}
            rows.append(
                f"{exchange}: role={block.get('role')}, universe={block.get('universe_symbols')}, "
                f"ohlcv_fetched={block.get('ohlcv_fetched')}, "
                f"failed={len(failed)}, high_risk={block.get('high_risk')}"
            )
        return bullet_list(rows)

    @staticmethod
    def _funnel_section(funnel: dict) -> str:
        if not funnel:
            return "- Candidate funnel not available."
        per = funnel.get("per_exchange_scanned") or {}
        rows = []
        for exchange, count in per.items():
            rows.append(f"Scanned on {exchange}: {count}")
        rows.append(f"After liquidity filter: {funnel.get('after_liquidity_filter')}")
        rows.append(f"After momentum filter: {funnel.get('after_momentum_filter')}")
        rows.append(f"Fused candidates: {funnel.get('fused_candidates')}")
        rows.append(f"Deep analysis: {funnel.get('selected_for_deep_analysis')}")
        rows.append(f"Full agent analysis: {funnel.get('selected_for_full_agent_analysis')}")
        return bullet_list(rows)

    @staticmethod
    def _rejected_section(rejected: list[RejectedIdea]) -> str:
        if not rejected:
            return "- No symbols rejected; full candidate list reached at least watchlist quality."
        rows = []
        for item in rejected[:15]:
            reasons = "; ".join(item.reasons[:3])
            exchanges = ", ".join(item.exchanges) or "n/a"
            rows.append(
                f"{item.symbol}: score {item.score} ({item.direction_bias}) — {item.primary_reason}. "
                f"Reasons: {reasons}. Exchanges: {exchanges}."
            )
        return bullet_list(rows)

    @staticmethod
    def _exchange_confirmation_section(
        confirmations: dict[str, ExchangeConfirmation], ideas: list[TradeIdea]
    ) -> str:
        if not confirmations:
            return "- No multi-exchange confirmation data available."
        rows = []
        for idea in ideas[:12]:
            item = confirmations.get(idea.symbol)
            if not item:
                continue
            rows.append(
                f"{idea.symbol} [{idea.tier}]: exchanges={item.exchanges_listed}, "
                f"anchor={item.anchor_listed}, derivatives={item.derivatives_listed}, "
                f"high_risk_only={item.high_risk_only}, confirmation={item.confirmation_score}/100, "
                f"focus={item.suggested_exchange_focus}. {item.interpretation}"
            )
        return bullet_list(rows or ["No confirmations for current idea set."])

    @staticmethod
    def _crowd_attention_section(
        crowd_attention: dict[str, CrowdAttention],
        ideas: list[TradeIdea],
        candidates: list[MomentumCandidate],
    ) -> str:
        if not crowd_attention:
            return "- No crowd-attention staging available."
        # Show top 10 by combined attention + momentum.
        sorted_items = sorted(
            crowd_attention.values(),
            key=lambda item: item.attention_score + item.momentum_score / 2,
            reverse=True,
        )[:10]
        rows = [
            f"{item.symbol}: stage {item.stage}, attention {item.attention_score}/100, "
            f"momentum {item.momentum_score}/100, crowding {item.crowding_risk}/100, "
            f"confidence {item.confidence}"
            for item in sorted_items
        ]
        return bullet_list(rows or ["No symbols with crowd staging."])

    @staticmethod
    def _final_summary(
        regime: MarketRegime, active: list[TradeIdea], watchlist: list[TradeIdea]
    ) -> str:
        if active:
            best = active[0]
            return (
                f"Best current idea is {best.direction.upper()} {best.symbol} at "
                f"{best.score}/100, but only if the planned entry and invalidation are respected. "
                f"The tape is {regime.label}; do not force correlated trades."
            )
        if watchlist:
            return (
                f"No active trade clears the desk threshold. Best watchlist name is "
                f"{watchlist[0].symbol} at {watchlist[0].score}/100. Wait for cleaner execution."
            )
        return "No trade. Data does not justify a fresh idea right now."
