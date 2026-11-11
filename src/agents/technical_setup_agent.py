from __future__ import annotations

import pandas as pd

from src.agents.base_agent import BaseAgent
from src.analysis.relative_strength_gate import gate_params, is_relative_strength_leader
from src.execution.stop_contract import build_initial_stop_contract, entry_anchor
from src.indicators.technicals import enrich_ohlcv, recent_range, trend_label
from src.models import MarketRegime, MomentumCandidate, TechnicalSetup
from src.utils.validation import clamp, model_to_dict


class TechnicalSetupAgent(BaseAgent):
    name = "technical_setup_agent"

    def run(
        self,
        candidates: list[MomentumCandidate],
        market_data: dict[str, dict[str, pd.DataFrame]],
        regime: MarketRegime,
        limit: int = 12,
    ) -> list[TechnicalSetup]:
        tf = self.config.settings.get("execution", {}).get("setup_timeframe", "1h")
        setups: list[TechnicalSetup] = []

        for candidate in candidates[:limit]:
            frame = market_data.get(candidate.symbol, {}).get(tf)
            if frame is None or len(frame) < 60:
                continue

            enriched = enrich_ohlcv(frame)
            last = enriched.iloc[-1]
            close = float(last["close"])
            atr = float(last["atr14"]) if pd.notna(last["atr14"]) else None
            ema20 = float(last["ema20"]) if pd.notna(last["ema20"]) else close
            resistance, support = recent_range(frame, 20)
            trend = trend_label(frame)
            warnings = list(candidate.warnings)

            if not atr or atr <= 0:
                setups.append(
                    TechnicalSetup(
                        symbol=candidate.symbol,
                        direction="no_trade",
                        timeframe=tf,
                        current_price=close,
                        trend=trend,
                        warnings=["ATR unavailable; cannot build clean invalidation."],
                    )
                )
                continue

            distance_atr = abs((close - ema20) / atr)
            if candidate.direction_bias == "long":
                direction = "long"
                entry_low = close - 0.65 * atr
                entry_high = close - 0.20 * atr
                atr_stop = close - 1.2 * atr
                support_stop = (support - 0.15 * atr) if support else None
                invalidation = (
                    support_stop
                    if support_stop is not None and support_stop > close - 1.8 * atr
                    else atr_stop
                )
                stop_source = "support_resistance" if invalidation == support_stop else "atr_fallback"
                stop_model = (
                    "support_minus_atr_buffer_v1"
                    if stop_source == "support_resistance" else "atr_distance_v1"
                )
                tp1 = close + 1.0 * atr
                tp2 = close + 2.0 * atr
                tp3 = close + 3.0 * atr
                # PART 20 (2026-06): a long in a bearish/danger tape is only a
                # "conflict" when the coin is drifting WITH the falling market.
                # A relative-strength leader (rising vs a weak BTC) is the
                # opposite — it is defying the tape, which is a strength signal,
                # not a conflict. We surface it as a counter-tape note (no
                # "conflict"/"fights" keyword → no regime_conflict penalty in
                # scoring) so it can still reach B-tier downstream.
                if regime.label in {"bearish trend", "high-volatility danger"}:
                    if is_relative_strength_leader(candidate, **gate_params(self.config)):
                        rs_val = getattr(candidate, "relative_strength_btc", None)
                        rs_txt = f"{rs_val:+.1f}%" if rs_val is not None else "n/a"
                        warnings.append(
                            "Relative-strength leader: rising vs a weak BTC tape "
                            f"(RS vs BTC {rs_txt}); counter-tape long — reduce size."
                        )
                    else:
                        warnings.append("Long setup conflicts with current market regime.")
            elif candidate.direction_bias == "short":
                direction = "short"
                entry_low = close + 0.20 * atr
                entry_high = close + 0.65 * atr
                atr_stop = close + 1.2 * atr
                resistance_stop = (resistance + 0.15 * atr) if resistance else None
                invalidation = (
                    resistance_stop
                    if resistance_stop is not None and resistance_stop < close + 1.8 * atr
                    else atr_stop
                )
                stop_source = "support_resistance" if invalidation == resistance_stop else "atr_fallback"
                stop_model = (
                    "resistance_plus_atr_buffer_v1"
                    if stop_source == "support_resistance" else "atr_distance_v1"
                )
                tp1 = close - 1.0 * atr
                tp2 = close - 2.0 * atr
                tp3 = close - 3.0 * atr
                if regime.label == "bullish trend":
                    warnings.append("Short setup fights a bullish tape.")
            else:
                direction = "watchlist_only"
                entry_low = entry_high = invalidation = tp1 = tp2 = tp3 = None
                stop_source = ""
                stop_model = ""

            if direction in {"long", "short"}:
                entry_mid = (entry_low + entry_high) / 2
                risk = abs(entry_mid - invalidation)
                reward = abs(tp1 - entry_mid)
                rr_to_tp1 = reward / risk if risk else None
            else:
                rr_to_tp1 = None

            setup_quality = candidate.score * 0.45
            if trend in {"uptrend", "downtrend"}:
                setup_quality += 16
            elif trend.startswith("transition"):
                setup_quality += 10
            else:
                setup_quality += 5
            if rr_to_tp1 is not None:
                setup_quality += min(rr_to_tp1, 2.5) * 8
            if distance_atr > 2:
                setup_quality -= 14
                warnings.append("Entry quality is weak because the move is extended.")
            if rr_to_tp1 is not None and rr_to_tp1 < 1:
                setup_quality -= 12
                warnings.append("Risk/reward to TP1 is below 1R.")

            if distance_atr > 2.5:
                direction = "watchlist_only"
                warnings.append("Converted to watchlist only: wait for pullback.")
                stop_source = ""
                stop_model = ""

            if direction in {"long", "short"}:
                stop_contract = build_initial_stop_contract(
                    symbol=candidate.symbol,
                    asset_class="crypto",
                    mode="intraday",
                    direction=direction,
                    entry_price=entry_anchor(direction, entry_low, entry_high, close),
                    stop_price=invalidation,
                    setup={
                        "timeframe": tf,
                        "entry_low": entry_low,
                        "entry_high": entry_high,
                        "invalidation": invalidation,
                        "atr": atr,
                        "support": support,
                        "resistance": resistance,
                        "stop_source": stop_source,
                        "stop_model": stop_model,
                        "stop_buffer_atr": 0.15 if stop_source == "support_resistance" else None,
                    },
                )
            else:
                stop_contract = {}

            setups.append(
                TechnicalSetup(
                    symbol=candidate.symbol,
                    direction=direction,
                    timeframe=tf,
                    current_price=round(close, 8),
                    entry_low=round(entry_low, 8) if direction in {"long", "short"} else None,
                    entry_high=round(entry_high, 8) if direction in {"long", "short"} else None,
                    invalidation=round(invalidation, 8)
                    if direction in {"long", "short"}
                    else None,
                    tp1=round(tp1, 8) if direction in {"long", "short"} else None,
                    tp2=round(tp2, 8) if direction in {"long", "short"} else None,
                    tp3=round(tp3, 8) if direction in {"long", "short"} else None,
                    atr=round(atr, 8),
                    rr_to_tp1=round(rr_to_tp1, 2) if rr_to_tp1 is not None else None,
                    setup_quality=round(clamp(setup_quality), 1),
                    trend=trend,
                    support=round(support, 8) if support is not None else None,
                    resistance=round(resistance, 8) if resistance is not None else None,
                    stop_source=stop_source,
                    stop_model=stop_model,
                    stop_contract=stop_contract,
                    warnings=warnings,
                )
            )

        self.save_output({"setups": [model_to_dict(item) for item in setups]})
        return setups
