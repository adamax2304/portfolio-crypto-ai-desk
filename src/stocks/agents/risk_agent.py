"""StockRiskAgent — combine risk signals into per-symbol flags + penalties.

Reads:
  - regime payload (from StocksMarketRegimeAgent)
  - sector payload (SectorRotationAgent)
  - RS payload (StockRelativeStrengthAgent)
  - earnings payload (EarningsRiskAgent)
  - technical setup (StockTechnicalAgent)

Output: per-symbol list of risk flags + total raw penalty (negative number)
to be applied by StockScoringAgent. Pure function over the inputs — no I/O
beyond save_output.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from src.stocks.agents.base import StocksBaseAgent


@dataclass
class StockRiskAssessment:
    symbol: str
    direction: str
    flags: list[str]
    penalty: float
    risk_level: str  # low / medium / high
    blocks: list[str]  # hard-block reasons (e.g. earnings within blocking window)


class StockRiskAgent(StocksBaseAgent):
    name = "stock_risk"

    def run(
        self,
        *,
        regime_payload: dict[str, Any],
        sector_payload: dict[str, Any],
        rs_payload: dict[str, Any],
        earnings_payload: dict[str, Any],
        technical_payload: dict[str, Any],
        mode: str = "intraday",
    ) -> dict[str, Any]:
        regime_label = (regime_payload.get("regime") or {}).get("label", "unknown")
        regime_bias = (regime_payload.get("regime") or {}).get("bias", "neutral")

        sector_status: dict[str, str] = {
            row["sector"]: row["status"]
            for row in (sector_payload.get("sectors") or [])
        }

        rs_by_symbol: dict[str, dict[str, Any]] = {
            row["symbol"].upper(): row for row in (rs_payload.get("rows") or [])
        }

        earnings_by_symbol: dict[str, dict[str, Any]] = {
            row["symbol"].upper(): row for row in (earnings_payload.get("risks") or [])
        }

        assessments: list[StockRiskAssessment] = []
        for setup in technical_payload.get("setups") or []:
            symbol = setup["symbol"].upper()
            direction = setup.get("direction") or "no_trade"
            flags: list[str] = []
            blocks: list[str] = []
            penalty = 0.0

            # Regime alignment — track whether the broad index contradicts
            # this trade direction so we can later combine with sector
            # alignment for the "both contradict" rule.
            index_contradicts = False
            if direction == "long" and regime_label == "risk_off":
                penalty += self.stocks_config.risk_penalty("contradicts_index_trend", -8.0)
                flags.append("long_in_risk_off_regime")
                index_contradicts = True
                rule = self.stocks_config.regime_rule("risk_off")
                if rule.get("long_requires_exceptional_rs"):
                    rs_row_tmp = rs_by_symbol.get(symbol) or {}
                    if (rs_row_tmp.get("classification") or "unknown") not in ("leader",):
                        flags.append("rs_not_exceptional_for_risk_off_long")
                        penalty += -6
            elif direction == "short" and regime_label == "bullish":
                penalty += self.stocks_config.risk_penalty("contradicts_index_trend", -8.0)
                flags.append("short_in_bullish_regime")
                index_contradicts = True
            elif direction == "long" and regime_bias == "short":
                # Catch any other regime label whose bias points opposite.
                index_contradicts = True
            elif direction == "short" and regime_bias == "long":
                index_contradicts = True

            # Sector alignment
            rs_row = rs_by_symbol.get(symbol) or {}
            sector = rs_row.get("sector") or ""
            sector_contradicts = False
            if sector:
                status = sector_status.get(sector, "mixed")
                if direction == "long" and status == "weak":
                    penalty += self.stocks_config.risk_penalty(
                        "contradicts_sector_trend", -6.0
                    )
                    flags.append("long_in_weak_sector")
                    sector_contradicts = True
                elif direction == "short" and status == "strong":
                    penalty += self.stocks_config.risk_penalty(
                        "contradicts_sector_trend", -6.0
                    )
                    flags.append("short_in_strong_sector")
                    sector_contradicts = True

            # "Both index AND sector contradict" composite rule.
            # config/stocks/risk.yaml → confirmation.both_contradict.reject
            if (
                index_contradicts
                and sector_contradicts
                and direction in ("long", "short")
            ):
                rule = self.stocks_config.confirmation_rule("both_contradict")
                flags.append("both_index_and_sector_contradict")
                if rule.get("reject"):
                    blocks.append("both_index_and_sector_contradict")

            # Relative strength
            cls = rs_row.get("classification")
            if cls == "weak" and direction == "long":
                penalty += self.stocks_config.risk_penalty("weak_relative_strength", -6.0)
                flags.append("weak_relative_strength")

            # Earnings
            er = earnings_by_symbol.get(symbol) or {}
            severity = er.get("severity")
            days_ahead = er.get("days_ahead")
            if severity == "active":
                penalty += self.stocks_config.risk_penalty("earnings_today", -20.0)
                flags.append("earnings_today")
                if mode == "swing":
                    blocks.append("earnings_today_blocks_swing")
            elif severity == "next_session":
                penalty += self.stocks_config.risk_penalty(
                    "earnings_next_session", -12.0
                )
                flags.append("earnings_next_session")
                if mode == "swing" and er.get("blocks_swing"):
                    blocks.append("earnings_blocks_swing_entry")
            elif (
                severity == "this_week"
                and mode == "swing"
                and isinstance(days_ahead, int)
                and days_ahead <= 3
            ):
                penalty += self.stocks_config.risk_penalty(
                    "earnings_within_3_days_for_swing", -10.0
                )
                flags.append("earnings_within_3_days_swing")

            # Technical / structure
            if direction in ("long", "short") and setup.get("invalidation") is None:
                penalty += self.stocks_config.risk_penalty("no_clean_invalidation", -10.0)
                flags.append("no_invalidation")
                blocks.append("no_invalidation")

            rr = setup.get("rr_to_tp1")
            min_rr = float(self.stocks_config.structure_rules.get("require_rr_to_tp1_gte", 1.5))
            if isinstance(rr, (int, float)) and rr < min_rr:
                flags.append(f"rr_below_{min_rr}")
                penalty += -4

            if direction == "no_trade":
                blocks.append("no_directional_setup")

            risk_level = "low"
            if penalty <= -15 or len(blocks) >= 1:
                risk_level = "high"
            elif penalty <= -6:
                risk_level = "medium"

            assessments.append(
                StockRiskAssessment(
                    symbol=symbol,
                    direction=direction,
                    flags=flags,
                    penalty=round(penalty, 2),
                    risk_level=risk_level,
                    blocks=blocks,
                )
            )

        payload = {
            "mode": mode,
            "regime_label": regime_label,
            "regime_bias": regime_bias,
            "assessments": [asdict(a) for a in assessments],
            "by_symbol": {a.symbol: asdict(a) for a in assessments},
        }
        self.save_output(payload)
        return payload
