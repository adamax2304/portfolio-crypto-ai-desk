from __future__ import annotations

from src.agents.base_agent import BaseAgent
from src.analysis.relative_strength_gate import gate_params, is_relative_strength_leader
from src.analysis.short_squeeze_gate import (
    assess_short_squeeze,
    gate_params as squeeze_params,
)
from src.models import (
    CatalystSummary,
    Critique,
    DerivativesSummary,
    ExchangeConfirmation,
    MarketRegime,
    MomentumCandidate,
    NarrativeSummary,
    RiskAssessment,
    ScoreBreakdown,
    TechnicalSetup,
)
from src.utils.validation import clamp, model_to_dict


class ScoringAgent(BaseAgent):
    name = "scoring_agent"

    def _market_alignment(
        self, direction: str, regime: MarketRegime, rs_leader: bool = False
    ) -> float:
        """Score how well ``direction`` aligns with the current regime.

        PART 14a (2026-06) — when the regime label is ambiguous
        (``transition`` / ``range/chop`` / ``high-volatility danger``) the
        BTC trend itself is the cleanest tie-breaker. The audit showed
        crypto-intraday in such regimes generated **zero** short signals
        despite BTC printing a clean downtrend, simply because the
        ambiguous-regime alignment for shorts collapsed to a flat 0.58 —
        below the threshold that lets shorts reach B-tier (need ~0.72).
        Now we add a directional boost when ``btc_trend`` agrees with
        the trade direction inside an ambiguous regime.

        Mapping (post-fix):
          * bullish trend + long → 0.90 (unchanged)
          * bearish trend + short → 0.88 (unchanged)
          * ambiguous regime + (BTC downtrend, short)  → **0.74** (was 0.58)
          * ambiguous regime + (BTC uptrend,   long)   → **0.74** (was 0.58)
          * ambiguous regime + (BTC sideways,  either) → 0.58 (unchanged)
          * counter-trend trades against a clean regime → 0.25 (unchanged)
        """
        ambiguous = {"transition", "range/chop", "high-volatility danger"}
        btc_trend = (regime.btc_trend or "").strip().lower()

        if direction == "long":
            if regime.label == "bullish trend":
                return 0.9
            if regime.label == "high-volatility trend":
                # Broad high-volatility uptrends are tradeable, but never get
                # the same regime credit as a calm bullish tape.  The Paper
                # overlay subsequently forces reduced size for this label.
                return 0.8 if btc_trend in {"uptrend", "transition_up"} else 0.35
            if regime.label in ambiguous:
                if btc_trend == "uptrend":
                    return 0.74
                # PART 20: a coin rising against a weak/sideways BTC inside an
                # ambiguous regime is showing strength, not conflict — give it
                # a fair (not bull-tape) alignment so it can reach B-tier.
                if rs_leader:
                    return 0.72
                return 0.58
            if regime.label == "bearish trend":
                # PART 20: outperformer defying a bear tape — counter-trend but
                # tradable with discipline (downstream caps it at B).
                if rs_leader:
                    return 0.6
                return 0.25
            return 0.35
        if direction == "short":
            if regime.label == "bearish trend":
                return 0.88
            if regime.label == "high-volatility trend":
                return 0.8 if btc_trend in {"downtrend", "transition_down"} else 0.35
            # PART 21: a volatile-bear tape (high-volatility danger + BTC
            # downtrend) is still a falling market — a short WITH that trend is
            # aligned, not a coin-flip. Score it almost like a clean bearish
            # short so genuine shorts can reach B (risk agent + caps keep the
            # size discipline).
            if regime.label == "high-volatility danger":
                if btc_trend in {"downtrend", "transition_down"}:
                    return 0.84
                return 0.58
            if regime.label in ambiguous:
                if btc_trend == "downtrend":
                    return 0.74
                return 0.58
            if regime.label == "bullish trend":
                return 0.25
            return 0.4
        return 0.35

    def run(
        self,
        setups: list[TechnicalSetup],
        candidates: list[MomentumCandidate],
        regime: MarketRegime,
        derivatives: dict[str, DerivativesSummary] | None = None,
        catalysts: dict[str, CatalystSummary] | None = None,
        risks: dict[str, RiskAssessment] | None = None,
        critiques: dict[str, Critique] | None = None,
        narratives: dict[str, NarrativeSummary] | None = None,
        exchange_confirmations: dict[str, ExchangeConfirmation] | None = None,
        data_freshness_minutes: float | None = None,
        mode: str = "intraday",
    ) -> dict[str, ScoreBreakdown]:
        candidate_map = {candidate.symbol: candidate for candidate in candidates}
        derivatives = derivatives or {}
        catalysts = catalysts or {}
        risks = risks or {}
        critiques = critiques or {}
        narratives = narratives or {}
        exchange_confirmations = exchange_confirmations or {}
        base_weights = self.config.scoring.get("weights", {})
        regime_block = self.config.scoring.get("regime_weights", {}) or {}
        mode_block = self.config.scoring.get("mode_weights", {}) or {}
        regime_multipliers = regime_block.get(regime.label, {}) or {}
        mode_multipliers = mode_block.get(mode, {}) or {}
        weights = self._apply_multipliers(base_weights, regime_multipliers, mode_multipliers)
        baselines = self.config.scoring.get("missing_data_baselines", {})
        penalties = self.config.scoring.get("risk_penalties", {})
        thresholds = self.config.scoring.get("thresholds", {})
        a_tier_threshold = float(thresholds.get("a_tier", thresholds.get("strong_idea", 80)))
        b_tier_threshold = float(thresholds.get("b_tier", thresholds.get("valid_idea", 65)))
        c_tier_threshold = float(thresholds.get("c_tier", thresholds.get("watchlist_only", 50)))
        high_risk_exchanges = self.config.high_risk_exchanges
        results: dict[str, ScoreBreakdown] = {}

        for setup in setups:
            candidate = candidate_map.get(setup.symbol)
            direction = setup.direction
            components: dict[str, float] = {}
            risk_penalty = 0.0
            reasons: list[str] = []
            warnings = list(setup.warnings)

            if direction in {"watchlist_only", "no_trade"}:
                direction_for_alignment = candidate.direction_bias if candidate else "watch"
            else:
                direction_for_alignment = direction

            # PART 20: relative-strength leader (rising vs a weak BTC tape).
            rs_leader = is_relative_strength_leader(candidate, **gate_params(self.config))

            components["market_regime"] = (
                self._market_alignment(direction_for_alignment, regime, rs_leader=rs_leader)
                * float(weights.get("market_regime", 15))
            )
            components["technical_setup"] = (
                setup.setup_quality / 100 * float(weights.get("technical_setup", 20))
            )
            components["momentum"] = (
                (candidate.score if candidate else 0) / 100
                * float(weights.get("momentum", 15))
            )

            derivative = derivatives.get(setup.symbol)
            derivative_quality = float(baselines.get("derivatives", 0.4))
            if derivative and derivative.data_available:
                alignment = derivative.alignment_score
                if direction_for_alignment == "short":
                    alignment = -alignment
                derivative_quality = clamp((alignment + 1) / 2, 0.15, 1.0)
                if derivative_quality >= 0.65:
                    reasons.append("Derivatives support the setup direction.")
                elif derivative_quality <= 0.35:
                    warnings.append("Derivatives lean against the setup.")
            else:
                risk_penalty += float(penalties.get("missing_derivatives", 4))
                warnings.append("Derivatives data unavailable for this symbol.")
            components["derivatives"] = float(weights.get("derivatives", 15)) * derivative_quality

            catalyst = catalysts.get(setup.symbol)
            catalyst_quality = float(baselines.get("catalyst_news", 0.3))
            if catalyst:
                catalyst_quality = min(1.0, catalyst_quality + catalyst.importance_score / 10)
                if catalyst.risk_events:
                    catalyst_quality = max(0.15, catalyst_quality - 0.25)
                    warnings.append("Catalyst risk event reduces setup quality.")
                if catalyst.catalysts:
                    reasons.append("Fresh news/catalyst mentions are attached to the symbol.")
            else:
                risk_penalty += float(penalties.get("missing_news", 3))
            components["catalyst_news"] = float(weights.get("catalyst_news", 15)) * catalyst_quality
            narrative_quality = self._symbol_narrative_quality(setup.symbol, narratives)
            if narrative_quality is None:
                narrative_quality = float(baselines.get("narrative", 0.35))
            elif narrative_quality >= 0.65:
                reasons.append("Symbol belongs to a heating narrative.")
            components["narrative"] = float(weights.get("narrative", 10)) * narrative_quality

            execution_quality = 0.65
            if setup.rr_to_tp1 is not None:
                execution_quality = min(max(setup.rr_to_tp1 / 2, 0.25), 1.0)
            components["execution_quality"] = execution_quality * float(
                weights.get("execution_quality", 10)
            )

            if any("conflict" in warning.lower() or "fights" in warning.lower() for warning in warnings):
                risk_penalty += float(penalties.get("regime_conflict", 8))
            if any("extended" in warning.lower() or "chase" in warning.lower() for warning in warnings):
                risk_penalty += float(penalties.get("overextended", 8))
            if setup.rr_to_tp1 is not None and setup.rr_to_tp1 < 1:
                risk_penalty += float(penalties.get("poor_risk_reward", 10))
            if setup.invalidation is None and direction in {"long", "short"}:
                risk_penalty += float(penalties.get("no_clear_invalidation", 15))
            risk = risks.get(setup.symbol)
            if risk:
                risk_penalty += min(risk.risk_score * 0.18, 18)
                warnings.extend(risk.warnings[:4])
            critique = critiques.get(setup.symbol)
            if critique:
                if critique.verdict == "reject":
                    risk_penalty += 10
                if critique.weak_signal_dependency:
                    risk_penalty += 4
                if critique.late_or_crowded:
                    risk_penalty += 5
            if len(warnings) >= 3:
                risk_penalty += float(penalties.get("too_many_warnings", 5))
            warnings = list(dict.fromkeys(warnings))

            total = sum(components.values()) - risk_penalty
            total = clamp(total)

            # --- Score caps (do not let weak/risky setups produce A-tier) ---
            caps: list[tuple[float, str]] = []
            confirmation = exchange_confirmations.get(setup.symbol)
            if setup.invalidation is None and direction in {"long", "short"}:
                caps.append((50.0, "no clean invalidation"))
            if direction not in {"long", "short", "watchlist_only", "no_trade"}:
                caps.append((50.0, f"unsupported direction {direction}"))
            if confirmation and confirmation.high_risk_only:
                # MEXC-only: cap at B unless liquidity is exceptional.
                cap_value = 70.0
                liq_component = components.get("technical_setup", 0)
                if liq_component < 14:
                    cap_value = 65.0
                caps.append((cap_value, "MEXC-only listing (exchange confirmation missing)"))
            if confirmation and not confirmation.anchor_listed and not confirmation.high_risk_only:
                caps.append((75.0, f"not listed on anchor exchange {self.config.anchor_exchange}"))
            risk = risks.get(setup.symbol)
            if risk and "low_liquidity" in {warning.lower() for warning in risk.warnings}:
                caps.append((60.0, "low liquidity"))
            if data_freshness_minutes is not None and data_freshness_minutes > 180:
                caps.append((50.0, "stale data (>3h old)"))
            catalyst = catalysts.get(setup.symbol)
            if catalyst and any("rumor" in (item or "").lower() for item in catalyst.catalysts):
                if not catalyst.risk_events and catalyst.verification_status in {"none", "rumor", "single_source"}:
                    caps.append((55.0, "unverified rumor-only catalyst"))
            derivative = derivatives.get(setup.symbol)
            if derivative and derivative.data_available and derivative.funding_rate is not None:
                if direction == "long" and float(derivative.funding_rate) > 0.001:
                    caps.append((78.0, "extreme positive funding against long crowding"))
                if direction == "short" and float(derivative.funding_rate) < -0.001:
                    caps.append((78.0, "extreme negative funding against short"))

            # PART 22 (2026-06) — short squeeze-risk guard. Conservative
            # safety layer: caps high-squeeze-risk SHORTS to C/watchlist
            # (bounce into / thin liquidity / high upper-wick / no-derivatives-
            # on-thin-tape). Does NOT touch longs, does NOT widen stops, does
            # NOT hard-reject. `late_short_after_exhaustion` alone is a warning,
            # so liquid majors falling cleanly are not capped just for shorting.
            squeeze_verdict = None
            if direction == "short" and candidate is not None:
                squeeze_verdict = assess_short_squeeze(
                    candidate, setup, derivative, params=squeeze_params(self.config)
                )
                for f in squeeze_verdict.flags:
                    if f not in warnings:
                        warnings.append(f)
                if squeeze_verdict.cap and squeeze_verdict.cap_value is not None:
                    caps.append((float(squeeze_verdict.cap_value), squeeze_verdict.cap_reason))
                elif squeeze_verdict.note:
                    reasons.append(squeeze_verdict.note)

            # PART 11 (2026-06) audit fix — crypto intraday B-tier longs were
            # net -0.75 R over 10 days (0 W / 6 L) when the regime was
            # bearish-trend. The setup engine still found valid technical
            # patterns, but the regime headwind made them unprofitable. We
            # demote these to C-tier (watchlist only — no Telegram alert)
            # so the trader can still see them but no money / attention is
            # spent. Symmetrical cap for shorts against bullish-trend.
            #
            # Gate is mode-specific: scalp and swing buckets were positive
            # in the same audit window, so they keep their original scoring.
            # See AUDIT_PAPER_TRADING.md §3.1.
            if mode == "intraday":
                if direction == "long" and regime.label == "bearish trend":
                    # PART 20: a relative-strength leader may reach B-tier
                    # (counter-trend, capped) instead of being demoted to C —
                    # it is rising against the tape, not drifting with it.
                    if rs_leader:
                        caps.append((
                            70.0,
                            "RS-leader long vs bearish tape (counter-trend, capped B)",
                        ))
                    else:
                        caps.append((
                            60.0,
                            "crypto intraday long against bearish-trend regime (audit cap)",
                        ))
                elif (
                    direction == "long"
                    and regime.label == "high-volatility danger"
                    and rs_leader
                ):
                    # PART 20: never a clean A against a danger tape, but a
                    # confirmed outperformer can surface as an actionable B.
                    caps.append((
                        70.0,
                        "RS-leader long in high-volatility danger (counter-trend, capped B)",
                    ))
                elif direction == "short" and regime.label == "bullish trend":
                    caps.append((
                        60.0,
                        "crypto intraday short against bullish-trend regime (audit cap)",
                    ))

            cap_reasons: list[str] = []
            score_cap: float | None = None
            if caps:
                score_cap = min(value for value, _ in caps)
                cap_reasons = [reason for value, reason in caps if value == score_cap]
                if total > score_cap:
                    reasons.append(
                        f"Score capped at {score_cap:.0f} ({'; '.join(cap_reasons)})."
                    )
                    total = score_cap

            # --- Tier classification ---
            invalidation_missing = any("invalidation" in reason.lower() for reason in cap_reasons)
            stale_cap = any("stale" in reason.lower() for reason in cap_reasons)
            if invalidation_missing or stale_cap:
                # A trade without invalidation or with stale data is not an idea.
                tier = "rejected"
            elif direction in {"long", "short"} and total >= a_tier_threshold and not caps:
                tier = "A"
            elif direction in {"long", "short"} and total >= b_tier_threshold:
                tier = "B"
            elif total >= c_tier_threshold:
                tier = "C"
            else:
                tier = "rejected"

            if total >= 85:
                confidence = "high"
            elif total >= 75:
                confidence = "medium-high"
            elif total >= 60:
                confidence = "medium"
            else:
                confidence = "low"

            missing_count = 0
            if not derivative or not derivative.data_available:
                missing_count += 1
            if not catalyst or catalyst.verification_status == "none":
                missing_count += 1
            if missing_count >= 2:
                data_quality = "acceptable"
            elif missing_count == 1:
                data_quality = "good"
            else:
                data_quality = "strong"

            if components["technical_setup"] >= 12:
                reasons.append("Technical setup is doing real work in the score.")
            if components["momentum"] >= 10:
                reasons.append("Momentum and relative strength are above desk threshold.")
            if missing_count:
                reasons.append("Some evidence streams are missing or weak; confidence is reduced.")
            if warnings:
                reasons.append("Risk warnings reduced the final score.")

            results[setup.symbol] = ScoreBreakdown(
                final_score=round(total, 1),
                confidence=confidence,
                data_quality=data_quality,
                tier=tier,
                components={k: round(v, 1) for k, v in components.items()},
                risk_penalty=round(risk_penalty, 1),
                score_cap=round(score_cap, 1) if score_cap is not None else None,
                cap_reasons=cap_reasons,
                reasons=reasons,
                warnings=warnings,
            )

        self.save_output({symbol: model_to_dict(score) for symbol, score in results.items()})
        return results

    @staticmethod
    def _apply_multipliers(
        base: dict, regime: dict, mode: dict
    ) -> dict[str, float]:
        out: dict[str, float] = {}
        for key, value in base.items():
            multiplier = 1.0
            if key in regime:
                try:
                    multiplier *= float(regime[key])
                except (TypeError, ValueError):
                    pass
            if key in mode:
                try:
                    multiplier *= float(mode[key])
                except (TypeError, ValueError):
                    pass
            out[key] = float(value) * multiplier
        return out

    @staticmethod
    def _symbol_narrative_quality(
        symbol: str, narratives: dict[str, NarrativeSummary]
    ) -> float | None:
        matches = [
            narrative for narrative in narratives.values()
            if symbol in narrative.representative_symbols
        ]
        if not matches:
            return None
        best = max(matches, key=lambda item: item.heat_score)
        quality = best.heat_score / 100
        if best.risk_score >= 65:
            quality -= 0.2
        return clamp(quality, 0.1, 1.0)
