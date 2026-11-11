"""StockTradeIdeaAgent — orchestrate scoring output into TradeIdea objects.

This is the terminal stocks agent: it consumes the upstream payloads and
produces TradeIdea instances with asset_class='stocks'. The objects can
then flow into the existing signal-registry path (which already accepts
asset_class) once the supervisor wires stocks in Stage 5.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from src.models import TradeIdea
from src.stocks.agents.base import StocksBaseAgent
from src.stocks.earnings_freshness import load_recent_earnings_news
from src.stocks.legal_risk import detect_legal_risk, load_active_legal_news
from src.stocks.market_calendar import is_us_cash_session_open


class StockTradeIdeaAgent(StocksBaseAgent):
    name = "stock_trade_idea"

    def run(
        self,
        *,
        scoring_payload: dict[str, Any],
        technical_payload: dict[str, Any],
        news_payload: dict[str, Any],
        earnings_payload: dict[str, Any],
        rs_payload: dict[str, Any],
        regime_payload: dict[str, Any],
        sector_payload: dict[str, Any],
        risk_payload: dict[str, Any],
        mode: str = "intraday",
        now: datetime | None = None,
        apply_intraday_guards: bool = True,
    ) -> dict[str, Any]:
        setups_by_symbol = {
            s["symbol"].upper(): s for s in (technical_payload.get("setups") or [])
        }
        earnings_by_symbol = {
            r["symbol"].upper(): r for r in (earnings_payload.get("risks") or [])
        }
        risk_by_symbol = risk_payload.get("by_symbol") or {}
        rs_by_symbol = {
            r["symbol"].upper(): r for r in (rs_payload.get("rows") or [])
        }
        news_by_symbol = news_payload.get("hits_by_symbol") or {}
        regime_label = (regime_payload.get("regime") or {}).get("label", "unknown")

        # PART 17 fix — fetch persistent legal-flag news in one batch (90-day
        # window) so SMCI-style stale-but-active legal overhangs reach the
        # gate even when the recent-news pipeline has pushed them past its
        # 200-row freshness ceiling.
        all_symbols = [
            (score_row.get("symbol") or "").upper()
            for score_row in (scoring_payload.get("scores") or [])
            if score_row.get("symbol")
        ]
        try:
            persistent_legal_by_symbol = load_active_legal_news(
                self.db, all_symbols, lookback_days=90, now=now
            )
        except Exception:
            # Fail open — legal-flag carry is additive; if the loader breaks
            # we still run the original PART 3 path against recent news.
            persistent_legal_by_symbol = {}

        # ── P1-fix (2026-06-04) ─────────────────────────────────────────────
        # Gate A: market-closed intraday. Fresh actionable intraday stock
        # entries built while the US cash session is CLOSED ran on stale
        # extended-hours prices and stopped out (12h audit overnight cluster).
        # When closed, intraday A/B → demote to C (planning/watchlist only).
        market_open = is_us_cash_session_open(now)
        # Gate B: post-earnings stale setup. News-confirmed earnings PRINT in
        # the last ~36h, used to invalidate a setup whose own earnings calendar
        # is still UNKNOWN (the AVGO regression). News wins over calendar.
        try:
            recent_earnings_by_symbol = load_recent_earnings_news(
                self.db, all_symbols, lookback_hours=36, now=now
            )
        except Exception:
            recent_earnings_by_symbol = {}

        # Hard RR gate + rolling-guard config (read once). require_rr_to_tp1_gte is a HARD invariant
        # for A/B; the rolling guards are read-only over paper_execution_r (stocks-intraday only).
        risk_cfg = getattr(self.stocks_config, "risk", {}) or {}
        _struct = risk_cfg.get("structure") or {}
        min_rr = float(_struct.get("require_rr_to_tp1_gte", 1.5))
        _guards = risk_cfg.get("intraday_guards") or {}
        enforce_rr = bool(_guards.get("enforce_rr_hard_gate", True))

        ideas: list[TradeIdea] = []
        for score_row in scoring_payload.get("scores") or []:
            symbol = score_row["symbol"]
            tier = score_row["tier"]
            # Raw/pre-gate tier straight from scoring, BEFORE any demote gate below. Persisted into
            # raw_idea_json so recovery/diagnostic stats can find would-have-been-A/B setups that a
            # gate later demoted to C (they would otherwise vanish from the final-tier cohort).
            pre_gate_tier = tier
            direction = score_row["direction"]
            if tier == "rejected" or direction == "no_trade":
                # Skip non-tradeable here; the report builder (Stage 5) will
                # list rejections separately via risk_payload + scoring_payload.
                continue

            setup = setups_by_symbol.get(symbol) or {}
            er = earnings_by_symbol.get(symbol) or {}
            rs = rs_by_symbol.get(symbol) or {}
            risk = risk_by_symbol.get(symbol) or {}
            news = news_by_symbol.get(symbol) or []

            timeframe = {"intraday": "15m/1h", "swing": "1h/1d", "invest": "1d/1wk"}.get(
                mode, "1h"
            )
            thesis = self._thesis(symbol, direction, mode, setup, rs, er, regime_label)
            evidence = self._evidence(setup, rs, er, news)
            counter = self._counter(setup, rs, er, regime_label)
            entry_plan = _format_entry(setup, direction)
            invalidation_str = _format_invalidation(setup, direction)
            targets = _format_targets(setup, direction)

            # PART 3 + PART 17 — legal/headline risk detection.
            # Step 1: scan recent CompanyNewsAgent hits (original PART 3 path).
            # Step 2: union with the 90-day persistent legal-flag window so
            # SMCI-style stale-but-active overhangs are caught (PART 17).
            # Step 3: if blocking AND tier in {A, B} → demote tier to C
            # ("MANUAL REVIEW REQUIRED" surfaced via cap_reasons and
            # avoid_conditions). Score is preserved for transparency —
            # report shows the demoted tier with a "legal_headline_risk"
            # cap_reason so the human sees both the original price-model
            # output AND the safety override.
            recent_news = list(news or [])
            persistent_news = persistent_legal_by_symbol.get(symbol, []) or []
            # Dedup by URL — recent + persistent often overlap for fresh
            # high-severity stories.
            seen_urls: set[str] = set()
            merged_news: list[dict[str, Any]] = []
            for hit in recent_news + persistent_news:
                url_key = str(hit.get("url") or "")
                if url_key and url_key in seen_urls:
                    continue
                if url_key:
                    seen_urls.add(url_key)
                merged_news.append(hit)
            legal_assessment = detect_legal_risk(merged_news)
            cap_reasons = list(score_row.get("cap_reasons") or [])
            avoid_conditions = self._avoid(er, mode)
            if legal_assessment.categories:
                ct = legal_assessment.counter_thesis
                if ct and ct not in counter:
                    counter.append(ct)
                cap = legal_assessment.cap_reason
                if cap and cap not in cap_reasons:
                    cap_reasons.append(cap)
                marker = legal_assessment.avoid_condition
                if marker and marker not in avoid_conditions:
                    avoid_conditions.append(marker)
            # PART 17 — hard tier demotion on blocking legal risk.
            if legal_assessment.blocking and tier in ("A", "B"):
                original_tier = tier
                tier = "C"
                demotion_reason = (
                    f"tier demoted {original_tier}→C: active legal/headline risk "
                    f"({','.join(sorted(legal_assessment.categories))}) — "
                    "manual review required"
                )
                if demotion_reason not in cap_reasons:
                    cap_reasons.append(demotion_reason)

            # ── P1-fix Gate B — post-earnings stale setup ───────────────────
            # If a verified earnings PRINT hit the tape within the lookback AND
            # the setup's own earnings calendar is still UNKNOWN (blind), the
            # entry/invalidation levels predate the event and cannot be
            # trusted. Demote A/B → C (manual review) until a fresh
            # post-earnings setup is computed. ETFs (severity not_applicable)
            # and stocks with a properly-detected event are unaffected.
            earn_news = recent_earnings_by_symbol.get(symbol)
            er_sev = str(er.get("severity") or "").lower()
            if earn_news and er_sev == "unknown":
                stale_reason = (
                    "stale_post_earnings_setup: verified earnings print "
                    f"({earn_news.get('published_at') or 'recent'}) while calendar "
                    "is UNKNOWN — pre-earnings levels invalid, requires fresh levels"
                )
                if stale_reason not in cap_reasons:
                    cap_reasons.append(stale_reason)
                note = (
                    "post-earnings stale setup — entry/invalidation predate the "
                    "earnings print; do not trade until levels are recomputed from "
                    "fresh post-earnings session data."
                )
                if note not in avoid_conditions:
                    avoid_conditions.append(note)
                if note not in counter:
                    counter.append(note)
                if tier in ("A", "B"):
                    original_tier = tier
                    tier = "C"
                    dem = (
                        f"tier demoted {original_tier}→C: stale_post_earnings_setup "
                        "(news-confirmed earnings, calendar UNKNOWN) — manual review required"
                    )
                    if dem not in cap_reasons:
                        cap_reasons.append(dem)

            # ── P1-fix Gate A — market-closed intraday planning-only ────────
            # When the US cash session is closed, intraday stock entries are
            # built on stale extended-hours prices and are NOT actionable.
            # Demote A/B → C so they register as planning/watchlist only and
            # are never Telegram-pushed as fresh intraday trades.
            if mode == "intraday" and not market_open:
                marker = (
                    "market_closed_intraday_planning_only: US cash session closed — "
                    "planning levels only, not an actionable intraday entry"
                )
                if marker not in cap_reasons:
                    cap_reasons.append(marker)
                if tier in ("A", "B"):
                    original_tier = tier
                    tier = "C"
                    dem = (
                        f"tier demoted {original_tier}→C: market_closed_intraday_planning_only"
                    )
                    if dem not in cap_reasons:
                        cap_reasons.append(dem)
                avoid_note = (
                    "US market closed — do not treat as a live intraday entry; "
                    "re-evaluate on fresh levels at/after the cash open (09:30 ET)."
                )
                if avoid_note not in avoid_conditions:
                    avoid_conditions.append(avoid_note)

            # ── P1-fix Gate C — stocks swing mode paused (48h audit) ────────
            # The 48h post-fix audit found stocks SWING was the single biggest
            # confirmed loss bucket (−12R, 0W/12L) — swing longs faded into the
            # AVGO-led semiconductor pullback. Until reviewed, cap stocks-swing
            # A/B candidates to C (watchlist/research only): they stay visible
            # in reports but are NOT Telegram-pushed as actionable A/B trades.
            # Scope is strictly stocks + swing: intraday, invest, and ALL
            # crypto modes are untouched.
            if mode == "swing":
                marker = "stocks_swing_paused_after_48h_audit"
                if marker not in cap_reasons:
                    cap_reasons.append(marker)
                if tier in ("A", "B"):
                    original_tier = tier
                    tier = "C"
                    dem = (
                        f"tier demoted {original_tier}→C: "
                        "stocks_swing_paused_after_48h_audit (−12R, 0W/12L) — "
                        "watchlist/research only until reviewed"
                    )
                    if dem not in cap_reasons:
                        cap_reasons.append(dem)
                swing_note = (
                    "stocks swing temporarily paused (48h audit: −12R, 0W/12L) — "
                    "watchlist/research only, not an actionable A/B entry."
                )
                if swing_note not in avoid_conditions:
                    avoid_conditions.append(swing_note)

            # ── Mode-Viability-Audit Gate — stocks invest mode (2026-06-09) ──
            # The 14d mode-viability audit found stocks INVEST: 0W/7L A/B over
            # 14d; stops fire within 1–6 days despite a 30-day validity window;
            # same tickers/directions/failure anatomy as the already-paused
            # stocks-swing pipeline. Until reviewed, cap stocks-invest A/B
            # candidates to C (watchlist/research only): they stay visible in
            # reports but are NOT Telegram-pushed as actionable A/B trades.
            # Scope is strictly stocks + invest: intraday, swing (which has its
            # own pause), and ALL crypto modes are untouched.
            if mode == "invest":
                marker = "stocks_invest_paused_after_mode_viability_audit"
                if marker not in cap_reasons:
                    cap_reasons.append(marker)
                if tier in ("A", "B"):
                    original_tier = tier
                    tier = "C"
                    dem = (
                        f"tier demoted {original_tier}→C: "
                        "stocks_invest_paused_after_mode_viability_audit "
                        "(0W/7L over 14d) — watchlist/research only until reviewed"
                    )
                    if dem not in cap_reasons:
                        cap_reasons.append(dem)
                invest_note = (
                    "Stocks invest is temporarily watchlist-only after mode "
                    "viability audit: 0W/7L over 14d; same failure mode as "
                    "paused stocks swing."
                )
                if invest_note not in avoid_conditions:
                    avoid_conditions.append(invest_note)

            # ── RR hard gate (2026-07-02) — an A/B idea MUST offer a real >= min reward:risk to
            # TP1. The technical setup now computes rr_to_tp1 from structural levels; below the
            # configured minimum (or missing) the idea can NEVER be A/B → C watchlist. C/rejected
            # are unaffected and are never actionable.
            rr_val = setup.get("rr_to_tp1")
            if enforce_rr and tier in ("A", "B"):
                rr_ok = isinstance(rr_val, (int, float)) and rr_val >= min_rr
                if not rr_ok:
                    original_tier = tier
                    tier = "C"
                    shown = f"{rr_val:.2f}" if isinstance(rr_val, (int, float)) else "n/a"
                    if "rr_below_min_required" not in cap_reasons:
                        cap_reasons.append("rr_below_min_required")
                    dem = (f"tier demoted {original_tier}→C: rr_below_min_required "
                           f"(rr_to_tp1={shown} < {min_rr:.2f}) — no clean structural {min_rr:.1f}R target")
                    if dem not in cap_reasons:
                        cap_reasons.append(dem)
                    note = (f"reward:risk to TP1 is {shown} (< {min_rr:.2f} required) — watchlist only, "
                            "not an actionable A/B entry.")
                    if note not in avoid_conditions:
                        avoid_conditions.append(note)

            # ── Shared long-confirmation context (reused by the ATR-only-TP1 gate AND the rolling
            # guard below). STRICT: missing data is never confirmation (see intraday_guards). Sector
            # is a TRUE/FALSE/None tri-state so genuinely-unknown sector is NOT silently treated as
            # "known-not-weak" (that would let an ATR-only setup stay A on no evidence).
            sector_contradicts, sector_weak = _sector_confirmation_state(
                rs, setup, sector_payload, risk.get("flags"))
            idea_ctx = {
                "rs_vs_spy": rs.get("rs_vs_spy_20d"),
                "volume_ratio": setup.get("volume_ratio"),
                "sector_contradicts": sector_contradicts,
                "sector_weak": sector_weak,
                "atr_extension": setup.get("atr_extension"),
            }
            try:
                from src.stocks import intraday_guards
                conf_ok = intraday_guards.long_confirmation_ok(idea_ctx, risk_cfg)
            except Exception:
                conf_ok = False

            # ── ATR-only TP1 gate (2026-07-03) — a TP1 that is only a measured 1.5*ATR objective
            # (tp1_source == "atr_measured", i.e. NO structural prior-day level) is weaker evidence
            # than a real structural target. Such a setup can be B but must NOT be A without extra
            # confirmation. Read-only, stocks-intraday paper/actionability only; caps A→B (never
            # promotes). A short (no short-confirmation gate) is always capped when ATR-only.
            atr_only_blocks_a = bool(_guards.get("atr_only_tp1_blocks_a_tier", True))
            tp1_source = str(setup.get("tp1_source") or "")
            if (mode == "intraday" and atr_only_blocks_a and tier == "A"
                    and tp1_source == "atr_measured" and not conf_ok):
                tier = "B"
                if "atr_only_tp1_capped_to_B" not in cap_reasons:
                    cap_reasons.append("atr_only_tp1_capped_to_B")
                dem = ("tier capped A→B: atr_only_tp1_capped_to_B (TP1 is a measured 1.5*ATR "
                       "objective with no structural prior-day level and no extra confirmation)")
                if dem not in cap_reasons:
                    cap_reasons.append(dem)
                anote = ("TP1 is an ATR-measured objective (no structural target) and lacks extra "
                         "confirmation (RS/volume/sector/extension) — treated as B, not A.")
                if anote not in avoid_conditions:
                    avoid_conditions.append(anote)

            # ── Rolling performance guards (2026-07-02) — READ-ONLY, stocks-intraday paper/
            # actionability only. Global 7d drawdown circuit breaker + per-direction guard from
            # paper_execution_r. NEVER live, NEVER crypto. A weak-long-cohort long survives ONLY
            # with extra confirmation (RS>0, sector not weak, not extended, adequate volume).
            if apply_intraday_guards and mode == "intraday" and tier in ("A", "B"):
                try:
                    from src.stocks import intraday_guards
                    guard_reasons = intraday_guards.guard_cap_reasons(
                        self.db, risk_cfg, direction=direction, long_confirmation_ok=conf_ok, now=now)
                except Exception:
                    guard_reasons = []
                if guard_reasons:
                    original_tier = tier
                    tier = "C"
                    for gr in guard_reasons:
                        if gr not in cap_reasons:
                            cap_reasons.append(gr)
                    dem = (f"tier demoted {original_tier}→C: {', '.join(guard_reasons)} "
                           "(rolling paper-R drawdown guard)")
                    if dem not in cap_reasons:
                        cap_reasons.append(dem)
                    gnote = ("stocks intraday under a rolling-performance guard (recent paper-R "
                             "drawdown) — watchlist/review only until the cohort recovers.")
                    if gnote not in avoid_conditions:
                        avoid_conditions.append(gnote)

            # ── SI-1..SI-5 actionability gates (2026-07-08) — READ-ONLY, stocks-intraday paper/
            # actionability only. Market context (SPY/QQQ) + sector confirmation + RTH session rule +
            # RVOL/liquidity + catalyst quality. ANY gate not confirmed → demote A/B→C (watchlist).
            # Fail-conservative: missing/stale confirming data demotes. Fields persisted (raw) for the
            # report + post-trade classifier. Never live, never crypto, never re-enables swing/invest.
            intraday_gate_fields: dict = {}
            _agates = (_guards.get("actionability_gates") or {})
            if mode == "intraday" and tier in ("A", "B") and bool(_agates.get("enabled", True)):
                try:
                    from src.stocks import intraday_gate_context as _igc
                    from src.stocks import intraday_actionability_gates as _iag
                    _gctx = _igc.build_context(symbol=symbol, direction=direction, setup=setup, now=now,
                                               idea_ctx=idea_ctx, catalyst_meta=_catalyst_meta_from_news(news),
                                               cfg=_agates)
                    _gres = _iag.evaluate(direction=direction, phase=_gctx["phase"],
                                          setup_type=setup.get("setup_type"), market_ctx=_gctx["market_ctx"],
                                          sector_ctx=_gctx["sector_ctx"], liquidity=_gctx["liquidity"],
                                          catalyst=_gctx["catalyst"], cfg=_agates)
                    intraday_gate_fields = _gres.fields
                    if _gres.decision == "C":
                        original_tier = tier
                        tier = "C"
                        for _r in _gres.demote_reasons:
                            if _r not in cap_reasons:
                                cap_reasons.append(_r)
                        _dem = (f"tier demoted {original_tier}→C: {', '.join(_gres.demote_reasons)} "
                                "(stocks-intraday actionability gates)")
                        if _dem not in cap_reasons:
                            cap_reasons.append(_dem)
                        _an = ("stocks intraday demoted by actionability gates (market/sector/session/"
                               "liquidity/catalyst not confirmed) — watchlist/review only, not actionable.")
                        if _an not in avoid_conditions:
                            avoid_conditions.append(_an)
                except Exception as _gerr:
                    # FAIL-CONSERVATIVE (not fail-open): if the gate/context evaluation throws, we must
                    # NOT leave an intraday A/B actionable without a real gate check. Demote to C and
                    # record the error so it is explainable in report/UI/diagnostics. Never re-raise —
                    # the scheduler/report must not crash.
                    original_tier = tier
                    tier = "C"
                    _err_reason = "intraday_actionability_gate_error"
                    if _err_reason not in cap_reasons:
                        cap_reasons.append(_err_reason)
                    _dem = (f"tier demoted {original_tier}→C: {_err_reason} "
                            f"({type(_gerr).__name__}) — stocks-intraday actionability gates failed")
                    if _dem not in cap_reasons:
                        cap_reasons.append(_dem)
                    _an = "stocks intraday actionability gates failed; review/watchlist only, not actionable."
                    if _an not in avoid_conditions:
                        avoid_conditions.append(_an)
                    intraday_gate_fields = {
                        "gate_error": type(_gerr).__name__,
                        "gate_error_message": str(_gerr)[:300],
                        "market_context_status": "error",
                        "sector_confirmation_status": "error",
                        "session_rule_status": "error",
                        "liquidity_status": "error",
                        "catalyst_quality": "unknown",
                        "demote_reasons": [_err_reason],
                    }

            idea = TradeIdea(
                symbol=symbol,
                direction=direction,
                score=float(score_row["final_score"]),
                confidence=str(score_row["confidence"]),
                risk_level=str(risk.get("risk_level") or "medium"),
                timeframe=timeframe,
                tier=tier,  # type: ignore[arg-type]
                mode=mode,  # type: ignore[arg-type]
                asset_class="stocks",
                exchange_focus="US",  # NYSE/NASDAQ universe; refined in Stage 5
                exchanges_confirmed=["US"],
                data_confidence=str(score_row.get("confidence") or "medium"),
                thesis=thesis,
                evidence=evidence,
                counterarguments=counter,
                entry_plan=entry_plan,
                invalidation=invalidation_str,
                targets=targets,
                what_to_monitor=self._monitor(mode, er),
                avoid_conditions=avoid_conditions,
                data_sources_used=["yfinance", "rss_news"],
                cap_reasons=cap_reasons,
                # Pre-gate vs final tier persist inside raw (raw_idea_json): pre_gate_tier is the raw
                # scoring tier; final_tier is what ships after every demote gate. demoted_by_gate lets
                # the report + recovery stats spot would-have-been-A/B setups a gate pushed to C.
                raw={
                    "pre_gate_tier": pre_gate_tier,
                    "final_tier": tier,
                    "demoted_by_gate": bool(pre_gate_tier in ("A", "B") and tier not in ("A", "B")),
                    "setup": {
                        "entry_low": setup.get("entry_low"),
                        "entry_high": setup.get("entry_high"),
                        "invalidation": setup.get("invalidation"),
                        "tp1": setup.get("tp1"),
                        "tp2": setup.get("tp2"),
                        "tp3": setup.get("tp3"),
                        "rr_to_tp1": setup.get("rr_to_tp1"),
                        "rr_to_structural_tp1": setup.get("rr_to_structural_tp1"),
                        "tp1_source": setup.get("tp1_source"),
                        "atr_extension": setup.get("atr_extension"),
                        "volume_ratio": setup.get("volume_ratio"),
                    },
                    # sector persists into the proposed_signals.sector column via the registry.
                    "candidate": {
                        "sector": rs.get("sector"),
                        "sector_etf": rs.get("sector_etf"),
                    },
                    # structured metrics exposed in raw_idea_json (schema has no dedicated columns
                    # for rs/volume) → reports + control-plane + LLM packet can surface them.
                    "structured": {
                        "sector": rs.get("sector"),
                        "sector_etf": rs.get("sector_etf"),
                        "rs_vs_spy": rs.get("rs_vs_spy_20d"),
                        "rs_vs_sector": rs.get("rs_vs_sector_20d"),
                        "volume_ratio": setup.get("volume_ratio"),
                        "rr_to_tp1": setup.get("rr_to_tp1"),
                        "rr_to_structural_tp1": setup.get("rr_to_structural_tp1"),
                        "tp1_source": setup.get("tp1_source"),
                        "atr_extension": setup.get("atr_extension"),
                    },
                    "score": score_row,
                    "relative_strength": rs,
                    "earnings": er,
                    "regime": {"label": regime_label},
                    "news_count": len(news),
                    "legal_risk": legal_assessment.to_dict(),
                    # 2026-06-15 catalyst safe-fix: display-only catalyst meta
                    # from the freshest ticker-specific news hit. Drives the
                    # dashboard/journal/Telegram catalyst labels. No scoring use.
                    "catalyst_meta": _catalyst_meta_from_news(news),
                    # SI-1..SI-5 actionability-gate diagnostics (market/sector/session/liquidity/
                    # catalyst statuses + demote reasons). Persisted for the intraday report and the
                    # SI-7 post-trade classifier. {} when gates did not run (non-intraday/non-A-B).
                    "intraday_actionability": intraday_gate_fields,
                },
            )
            ideas.append(idea)

        payload = {
            "mode": mode,
            "asset_class": "stocks",
            "ideas": [idea.model_dump() for idea in ideas],
            "rejected_count": sum(
                1 for s in scoring_payload.get("scores") or [] if s["tier"] == "rejected"
            ),
        }
        self.save_output(payload)
        return payload

    @staticmethod
    def _thesis(
        symbol: str,
        direction: str,
        mode: str,
        setup: dict[str, Any],
        rs: dict[str, Any],
        er: dict[str, Any],
        regime_label: str,
    ) -> str:
        bits = [f"{symbol} {direction} ({mode})"]
        trend = setup.get("trend")
        if trend:
            bits.append(f"trend={trend}")
        cls = rs.get("classification")
        if cls:
            bits.append(f"RS={cls}")
        bits.append(f"regime={regime_label}")
        sev = er.get("severity")
        # PART 18 — "safe" and ETF "not_applicable" are both clean cases.
        if sev and sev not in ("safe", "not_applicable"):
            bits.append(f"earnings:{sev}")
        return " | ".join(bits)

    @staticmethod
    def _evidence(
        setup: dict[str, Any],
        rs: dict[str, Any],
        er: dict[str, Any],
        news: list[dict[str, Any]],
    ) -> list[str]:
        ev: list[str] = []
        if setup.get("notes"):
            ev.extend(str(n) for n in setup["notes"])
        if (rs.get("rs_vs_spy_20d") or 0) > 0:
            ev.append(f"RS vs SPY (20d): +{rs['rs_vs_spy_20d']:.2f}%")
        if (rs.get("rs_vs_sector_20d") or 0) > 0:
            ev.append(f"RS vs sector ETF (20d): +{rs['rs_vs_sector_20d']:.2f}%")
        if news:
            ev.append(f"{len(news)} news catalyst(s) in lookback window")

        # Earnings line — surface ACTUAL date / days_ahead / severity, not just
        # "earnings:unknown". This is what was missing per the audit.
        ev.append(_earnings_evidence_line(er))
        return ev

    @staticmethod
    def _counter(
        setup: dict[str, Any],
        rs: dict[str, Any],
        er: dict[str, Any],
        regime_label: str,
    ) -> list[str]:
        c: list[str] = []
        if regime_label == "risk_off":
            c.append("market regime is risk-off; index can drag the trade")
        if (rs.get("classification") or "") in ("laggard", "weak"):
            c.append("relative strength is not in the leader bucket")

        sev = (er.get("severity") or "").lower()
        # PART 18 — ETFs hit "not_applicable" earlier in the pipeline; skip
        # the unknown-event-risk counter-thesis for them entirely.
        if sev == "unknown":
            # Per audit: surface unknown earnings as a real risk flag, not
            # a soft "earnings:unknown" footnote.
            c.append(
                "earnings date is UNKNOWN — calendar lookup missing; "
                "any held position carries undated event risk"
            )
        elif sev in {"active", "next_session"}:
            c.append(
                f"earnings risk: {sev} ({er.get('note') or 'event imminent'})"
            )
        elif sev == "this_week":
            c.append(
                f"earnings risk: this_week ({er.get('next_earnings_date') or 'date tbd'})"
            )
        if setup.get("trend") == "range":
            c.append("setup is range-bound; breakouts may fail")
        return c

    @staticmethod
    def _monitor(mode: str, er: dict[str, Any]) -> list[str]:
        m = [
            "SPY/QQQ direction and intraday VIX moves",
            "sector ETF trend (alignment with the trade)",
            "relative volume vs 20-day average",
        ]
        if mode == "swing" and er.get("severity") in ("this_week", "next_session", "active"):
            m.append("earnings announcement and post-earnings drift")
        return m

    @staticmethod
    def _avoid(er: dict[str, Any], mode: str) -> list[str]:
        a = [
            "do not chase if price is > 2 ATR from planned entry",
            "do not enter against a clear SPY breakdown",
        ]
        if mode == "swing" and er.get("severity") in ("next_session", "active"):
            a.append("avoid holding through scheduled earnings unless explicit strategy")
        return a


def _sector_confirmation_state(
    rs: dict[str, Any],
    setup: dict[str, Any],
    sector_payload: dict[str, Any] | None,
    risk_flags: list[Any] | None,
) -> tuple[bool | None, bool | None]:
    """Resolve (sector_contradicts, sector_weak) as a TRUE / FALSE / None tri-state for the strict
    long-confirmation check.

    - True  = KNOWN weak / contradicting (explicit risk flag, or the sector-rotation snapshot says
              status == "weak").
    - False = KNOWN not weak (the sector-rotation snapshot says status == "strong"/"mixed").
    - None  = UNKNOWN — no sector name/ETF, or no sector status/score, and no explicit risk flag.

    Genuinely-unknown sector MUST stay None so it is never mistaken for "known-not-weak". Only reads
    already-collected payloads; no I/O.
    """
    flags = [str(f).lower() for f in (risk_flags or [])]
    contradicts: bool | None = True if any(
        "sector" in f and "contradict" in f for f in flags) else None
    weak: bool | None = None
    if any("sector" in f and ("weak" in f or "laggard" in f) for f in flags):
        weak = True

    if weak is None:
        name = str(rs.get("sector") or (setup.get("sector") if isinstance(setup, dict) else "")
                   or "").strip().lower()
        etf = str(rs.get("sector_etf") or "").strip().upper()
        if name or etf:
            match = None
            for s in ((sector_payload or {}).get("sectors") or []):
                s_name = str(s.get("sector") or "").strip().lower()
                s_etf = str(s.get("etf") or "").strip().upper()
                if (etf and s_etf == etf) or (name and s_name == name):
                    match = s
                    break
            if match is not None:
                status = str(match.get("status") or "").strip().lower()
                if status == "weak":
                    weak = True
                elif status in ("strong", "mixed"):
                    weak = False            # KNOWN not weak (have a real sector status)
                # any other / empty status string → leave None (unknown)
    return contradicts, weak


def _catalyst_meta_from_news(news: list[dict[str, Any]] | None) -> dict[str, Any]:
    """Display-only catalyst meta from the freshest ticker-specific news hit.

    Returns {} when no ticker news. Never used for scoring/tier. The
    classifier may tag analyst actions — surface that as the catalyst type
    when it is the leading hit (PART 5).
    """
    if not news:
        return {}
    # Prefer the newest hit by published_at if present.
    def _key(h: dict[str, Any]) -> str:
        return str(h.get("published_at") or h.get("ts") or "")
    try:
        hits = sorted(news, key=_key, reverse=True)
    except Exception:
        hits = list(news)
    top = hits[0] if hits else {}
    if not isinstance(top, dict):
        return {}
    cat_type = str(top.get("catalyst_type") or top.get("category") or "")
    return {
        "headline_short": str(top.get("title") or top.get("headline") or "")[:80],
        "source": str(top.get("source") or ""),
        "published_at": top.get("published_at") or top.get("ts"),
        "catalyst_type": cat_type,
        "direction_hint": str(top.get("direction_hint") or top.get("sentiment") or "").lower(),
        "source_quality": str(top.get("source_quality") or top.get("quality") or "unknown").lower(),
        "is_analyst_action": "analyst" in cat_type.lower(),
        "mapping": "exact",  # CompanyNewsAgent hits are per-ticker
    }


def _format_entry(setup: dict[str, Any], direction: str) -> str:
    low = setup.get("entry_low")
    high = setup.get("entry_high")
    if low is None and high is None:
        return "(no entry plan)"
    if low is None:
        return f"{direction} at {high}"
    if high is None:
        return f"{direction} at {low}"
    return f"{direction} zone {low:.4f}–{high:.4f}"


def _format_invalidation(setup: dict[str, Any], direction: str) -> str:
    inv = setup.get("invalidation")
    if inv is None:
        return "(no invalidation)"
    return f"close beyond {inv:.4f}"


def _format_targets(setup: dict[str, Any], direction: str) -> list[str]:
    out: list[str] = []
    for label, key in (("TP1", "tp1"), ("TP2", "tp2"), ("TP3", "tp3")):
        v = setup.get(key)
        if v is not None:
            out.append(f"{label}: {v:.4f}")
    return out


def _earnings_evidence_line(er: dict[str, Any]) -> str:
    """Build a single evidence string from the EarningsRiskAgent payload.

    Surfaces the actual next-earnings date when known instead of the legacy
    "earnings:unknown" footnote.
    """
    sev = (er.get("severity") or "unknown").lower()
    nx = er.get("next_earnings_date")
    days = er.get("days_ahead")
    # PART 18 — ETFs are not subject to earnings event risk; the
    # earnings-risk agent now tags them with severity='not_applicable'.
    if sev == "not_applicable":
        return "earnings: N/A (ETF — does not report earnings)"
    if sev == "safe":
        return "earnings: safe (no event in the near window)"
    if sev == "unknown" or nx is None:
        return "earnings: UNKNOWN (calendar lookup missing — treat as undated event risk)"
    days_str = f"{days}d" if isinstance(days, int) else "?"
    return f"earnings: {sev} (next: {nx}, in {days_str})"
