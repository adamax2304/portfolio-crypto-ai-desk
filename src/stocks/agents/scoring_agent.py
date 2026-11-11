"""StockScoringAgent — aggregate component scores into a final 0-100 tier.

Inputs (already produced by upstream agents):
  - regime payload  : market regime label + bias
  - sector payload  : per-sector status
  - rs payload      : per-symbol RS classification
  - technical payload: per-symbol setup + quality_score
  - news payload    : per-symbol catalyst hits
  - risk payload    : per-symbol penalty + blocks

Output: per-symbol final score + tier (A/B/C/rejected), with the component
breakdown preserved for the report.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from src.stocks.agents.base import StocksBaseAgent


@dataclass
class StockScore:
    symbol: str
    direction: str
    final_score: float
    tier: str
    confidence: str
    components: dict[str, float]
    risk_penalty: float
    cap_reasons: list[str]
    blocks: list[str]


class StockScoringAgent(StocksBaseAgent):
    name = "stock_scoring"

    COMPONENTS = (
        "market_regime_alignment",
        "index_confirmation",
        "sector_confirmation",
        "relative_strength",
        "technical_setup",
        "volume_relative_volume",
        "news_catalyst",
        "earnings_risk_adjustment",
        "risk_reward",
        "data_confidence",
    )

    def run(
        self,
        *,
        regime_payload: dict[str, Any],
        sector_payload: dict[str, Any],
        rs_payload: dict[str, Any],
        technical_payload: dict[str, Any],
        news_payload: dict[str, Any],
        risk_payload: dict[str, Any],
        mode: str = "intraday",
    ) -> dict[str, Any]:
        regime = regime_payload.get("regime") or {}
        regime_label = regime.get("label", "unknown")
        regime_bias = regime.get("bias", "neutral")

        sector_status: dict[str, str] = {
            row["sector"]: row["status"]
            for row in (sector_payload.get("sectors") or [])
        }
        rs_by_symbol = {
            row["symbol"].upper(): row for row in (rs_payload.get("rows") or [])
        }
        news_by_symbol = news_payload.get("hits_by_symbol") or {}
        risk_by_symbol = risk_payload.get("by_symbol") or {}

        scores: list[StockScore] = []
        for setup in technical_payload.get("setups") or []:
            symbol = setup["symbol"].upper()
            direction = setup.get("direction") or "no_trade"

            comps = self._components(
                symbol=symbol,
                direction=direction,
                setup=setup,
                regime_label=regime_label,
                regime_bias=regime_bias,
                rs_row=rs_by_symbol.get(symbol) or {},
                sector_status=sector_status,
                news_hits=news_by_symbol.get(symbol) or [],
                mode=mode,
            )
            base_total = sum(comps.values())

            risk_info = risk_by_symbol.get(symbol) or {}
            penalty = float(risk_info.get("penalty") or 0.0)
            blocks = list(risk_info.get("blocks") or [])

            final = base_total + penalty

            cap_reasons: list[str] = []
            final, cap_reasons = self._apply_caps(final, blocks, cap_reasons)

            tier = self._tier(final, blocks)
            confidence = self._confidence(comps, blocks)

            scores.append(
                StockScore(
                    symbol=symbol,
                    direction=direction,
                    final_score=round(final, 2),
                    tier=tier,
                    confidence=confidence,
                    components=comps,
                    risk_penalty=round(penalty, 2),
                    cap_reasons=cap_reasons,
                    blocks=blocks,
                )
            )

        scores.sort(key=lambda s: s.final_score, reverse=True)
        payload = {
            "mode": mode,
            "regime_label": regime_label,
            "regime_bias": regime_bias,
            "scores": [asdict(s) for s in scores],
        }
        self.save_output(payload)
        return payload

    # ------------------------------------------------------------------
    # Components
    # ------------------------------------------------------------------
    def _components(
        self,
        *,
        symbol: str,
        direction: str,
        setup: dict[str, Any],
        regime_label: str,
        regime_bias: str,
        rs_row: dict[str, Any],
        sector_status: dict[str, str],
        news_hits: list[dict[str, Any]],
        mode: str,
    ) -> dict[str, float]:
        cfg = self.stocks_config

        # Helper to compute a single weighted component with mode + regime multipliers.
        def weighted(component: str, raw: float, max_score: float) -> float:
            w = cfg.weight(component)
            mode_mult = cfg.mode_multiplier(mode, component)
            regime_mult = cfg.regime_multiplier(regime_label, component)
            # raw is in [0, 1]; scale to weight × multipliers
            value = raw * w * mode_mult * regime_mult
            return round(min(value, max_score * mode_mult * regime_mult), 2)

        # market_regime_alignment: 1.0 if direction matches regime bias
        if direction == "no_trade":
            regime_raw = 0.0
        elif regime_bias == direction:
            regime_raw = 1.0
        elif regime_bias == "neutral":
            regime_raw = 0.5
        else:
            regime_raw = 0.0

        # index_confirmation: 1.0 if RS vs SPY is positive (long) / negative (short)
        rs_spy = rs_row.get("rs_vs_spy_20d")
        if direction == "long" and isinstance(rs_spy, (int, float)) and rs_spy > 0:
            index_raw = 1.0
        elif direction == "short" and isinstance(rs_spy, (int, float)) and rs_spy < 0:
            index_raw = 1.0
        elif rs_spy is None:
            index_raw = 0.4  # neutral if unknown
        else:
            index_raw = 0.2

        # sector_confirmation: based on sector_status
        sector = rs_row.get("sector") or ""
        status = sector_status.get(sector, "mixed") if sector else "mixed"
        if direction == "long" and status == "strong":
            sector_raw = 1.0
        elif direction == "short" and status == "weak":
            sector_raw = 1.0
        elif status == "mixed":
            sector_raw = 0.5
        else:
            sector_raw = 0.2

        # relative_strength: classification-based
        cls = rs_row.get("classification") or "unknown"
        rs_raw_map = {"leader": 1.0, "follower": 0.7, "laggard": 0.4, "weak": 0.1, "unknown": 0.3}
        rs_raw = rs_raw_map.get(cls, 0.3)

        # technical_setup: quality_score is already 0-100 → 0-1
        tech_raw = float(setup.get("quality_score") or 0.0) / 100.0

        # volume_relative_volume: derived from the technical agent's measured
        # last-bar / 20-bar-avg ratio. Mapping:
        #   ≤ 0.5x → 0.0 (very thin participation)
        #   1.0x   → 0.33
        #   1.5x   → 0.67
        #   ≥ 2.0x → 1.0 (volume surge)
        # When the technical agent could not compute the ratio (missing
        # data), fall back to neutral 0.5.
        vol_ratio = setup.get("volume_ratio")
        if vol_ratio is None or not isinstance(vol_ratio, (int, float)) or vol_ratio <= 0:
            vol_raw = 0.5
        else:
            vol_raw = max(0.0, min(1.0, (float(vol_ratio) - 0.5) / 1.5))

        # news_catalyst: bonus if any verified hit
        news_raw = 1.0 if news_hits else 0.0

        # earnings_risk_adjustment: positive when no earnings risk, negative
        # when there is (this is in addition to risk_penalty which is separate).
        # We score this as positive contribution = catalyst-free reliability.
        # The hard penalties live in StockRiskAgent; here we add a *bonus* when
        # earnings are far away (>5 days) so safe plays get credit.
        # For simplicity, neutral 0.5 by default.
        earnings_raw = 0.5

        # risk_reward: from setup.rr_to_tp1
        rr = setup.get("rr_to_tp1")
        if isinstance(rr, (int, float)):
            rr_raw = min(max((rr - 1.0) / 2.0, 0.0), 1.0)  # 1.0R → 0, 3.0R → 1
        else:
            rr_raw = 0.3

        # data_confidence: read from the technical agent's measured score
        # (0..1) which reflects which inputs were actually available for this
        # symbol (context history depth, daily history, intraday exec frame,
        # prev-day H/L, ATR, volume ratio, VWAP). Falls back to neutral 0.5
        # when the setup did not surface the field (legacy payloads).
        data_raw_value = setup.get("data_confidence_raw")
        if isinstance(data_raw_value, (int, float)):
            data_raw = max(0.0, min(1.0, float(data_raw_value)))
        else:
            data_raw = 0.5

        return {
            "market_regime_alignment": weighted("market_regime_alignment", regime_raw, cfg.weight("market_regime_alignment")),
            "index_confirmation": weighted("index_confirmation", index_raw, cfg.weight("index_confirmation")),
            "sector_confirmation": weighted("sector_confirmation", sector_raw, cfg.weight("sector_confirmation")),
            "relative_strength": weighted("relative_strength", rs_raw, cfg.weight("relative_strength")),
            "technical_setup": weighted("technical_setup", tech_raw, cfg.weight("technical_setup")),
            "volume_relative_volume": weighted("volume_relative_volume", vol_raw, cfg.weight("volume_relative_volume")),
            "news_catalyst": weighted("news_catalyst", news_raw, cfg.weight("news_catalyst")),
            "earnings_risk_adjustment": weighted("earnings_risk_adjustment", earnings_raw, cfg.weight("earnings_risk_adjustment") or 10.0),
            "risk_reward": weighted("risk_reward", rr_raw, cfg.weight("risk_reward")),
            "data_confidence": weighted("data_confidence", data_raw, cfg.weight("data_confidence")),
        }

    # ------------------------------------------------------------------
    # Caps + tiering
    # ------------------------------------------------------------------
    def _apply_caps(
        self,
        score: float,
        blocks: list[str],
        cap_reasons: list[str],
    ) -> tuple[float, list[str]]:
        cap_partial = self.stocks_config.cap("max_score_if_data_partial")
        cap_earnings = self.stocks_config.cap("max_score_if_earnings_active")
        floor = self.stocks_config.cap("min_score_floor") or 0.0
        ceiling = self.stocks_config.cap("max_score_ceiling") or 100.0
        out = score
        if "earnings_today_blocks_swing" in blocks and cap_earnings is not None:
            if out > cap_earnings:
                out = cap_earnings
                cap_reasons.append("capped: earnings active")
        if cap_partial is not None and out > cap_partial and "no_invalidation" in blocks:
            out = cap_partial
            cap_reasons.append("capped: data partial")
        out = max(floor, min(ceiling, out))
        return round(out, 2), cap_reasons

    def _tier(self, final_score: float, blocks: list[str]) -> str:
        if blocks:
            return "rejected"
        from src.signals.tier_policy import tier_from_score
        return tier_from_score(
            final_score,
            a=self.stocks_config.tier_threshold("A", 80.0),
            b=self.stocks_config.tier_threshold("B", 65.0),
            c=self.stocks_config.tier_threshold("C", 50.0),
        )

    @staticmethod
    def _confidence(comps: dict[str, float], blocks: list[str]) -> str:
        if blocks:
            return "low"
        total = sum(comps.values())
        if total >= 80:
            return "high"
        if total >= 60:
            return "medium"
        return "low"
