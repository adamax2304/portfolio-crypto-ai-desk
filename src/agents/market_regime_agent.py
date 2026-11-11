from __future__ import annotations

import pandas as pd

from src.agents.base_agent import BaseAgent
from src.indicators.technicals import enrich_ohlcv, pct_return, recent_range, trend_label
from src.indicators.volatility import atr_percentile
from src.models import MarketRegime
from src.utils.validation import clamp, model_to_dict


class MarketRegimeAgent(BaseAgent):
    name = "market_regime_agent"

    def _high_volatility_config(self) -> dict[str, float]:
        """Return conservative, config-backed thresholds for a volatile trend.

        High realized volatility alone is not direction.  When both majors and
        breadth agree, classifying that condition as ``danger`` suppresses
        orderly pullback entries precisely when a trend is broadening.  The
        thresholds remain deliberately stricter than the ordinary bullish or
        bearish labels, so a single volatile BTC candle cannot unlock the
        regime.
        """
        block = ((self.config.scoring.get("regime_classifier") or {})
                 .get("high_volatility") or {})
        return {
            "atr_percentile_min": float(block.get("atr_percentile_min", 80.0)),
            "large_btc_move_pct": float(block.get("large_btc_move_pct", 4.0)),
            "min_breadth_symbols": float(block.get("min_breadth_symbols", 6.0)),
            "trend_min_breadth_ema20_pct": float(block.get("trend_min_breadth_ema20_pct", 55.0)),
            "trend_min_positive_24h_pct": float(block.get("trend_min_positive_24h_pct", 55.0)),
            "trend_max_breadth_ema20_pct": float(block.get("trend_max_breadth_ema20_pct", 45.0)),
            "trend_max_positive_24h_pct": float(block.get("trend_max_positive_24h_pct", 45.0)),
        }

    @staticmethod
    def _first_frame(
        frames: dict[str, pd.DataFrame], preferred: str, fallback: str = "1h"
    ) -> pd.DataFrame | None:
        frame = frames.get(preferred)
        if frame is not None:
            return frame
        return frames.get(fallback)

    def _symbol_trend(self, frame: pd.DataFrame | None) -> str:
        if frame is None or len(frame) < 60:
            return "unknown"
        return trend_label(frame)

    def run(self, market_data: dict[str, dict[str, pd.DataFrame]]) -> MarketRegime:
        warnings: list[str] = []
        regime_tf = self.config.settings.get("execution", {}).get("regime_timeframe", "4h")
        btc_frame = self._first_frame(market_data.get("BTC/USDT", {}), regime_tf)
        eth_frame = self._first_frame(market_data.get("ETH/USDT", {}), regime_tf)

        if btc_frame is None:
            warnings.append("BTC data unavailable; regime confidence reduced.")
        if eth_frame is None:
            warnings.append("ETH data unavailable; regime confidence reduced.")

        btc_trend = self._symbol_trend(btc_frame)
        eth_trend = self._symbol_trend(eth_frame)
        btc_ret_24h = pct_return(btc_frame, 6 if regime_tf == "4h" else 24) if btc_frame is not None else None

        above_ema20 = 0
        above_ema50 = 0
        positive_24h = 0
        outperform_btc = 0
        total = 0
        btc_ret_ref = btc_ret_24h or 0.0

        for symbol, frames in market_data.items():
            frame = self._first_frame(frames, regime_tf)
            if frame is None or len(frame) < 60:
                continue
            enriched = enrich_ohlcv(frame)
            last = enriched.iloc[-1]
            close = float(last["close"])
            total += 1
            if pd.notna(last["ema20"]) and close > float(last["ema20"]):
                above_ema20 += 1
            if pd.notna(last["ema50"]) and close > float(last["ema50"]):
                above_ema50 += 1
            symbol_ret = pct_return(frame, 6 if regime_tf == "4h" else 24)
            if symbol_ret is not None and symbol_ret > 0:
                positive_24h += 1
            if symbol != "BTC/USDT" and symbol_ret is not None and symbol_ret > btc_ret_ref:
                outperform_btc += 1

        breadth = {
            "symbols_counted": float(total),
            "above_ema20_pct": (above_ema20 / total * 100) if total else 0.0,
            "above_ema50_pct": (above_ema50 / total * 100) if total else 0.0,
            "positive_24h_pct": (positive_24h / total * 100) if total else 0.0,
            "outperforming_btc_pct": (outperform_btc / max(total - 1, 1) * 100) if total else 0.0,
        }

        volatility_cfg = self._high_volatility_config()
        btc_atr_pct = atr_percentile(btc_frame) if btc_frame is not None else None
        high_vol = (
            btc_atr_pct is not None
            and btc_atr_pct >= volatility_cfg["atr_percentile_min"]
        )
        breadth_sample_ok = total >= int(volatility_cfg["min_breadth_symbols"])
        if not breadth_sample_ok:
            warnings.append(
                "Market breadth sample is too small for a directional regime; "
                f"counted {total}, require {int(volatility_cfg['min_breadth_symbols'])}."
            )
        breadth_score = breadth["above_ema20_pct"]

        large_btc_move = (
            btc_ret_24h is not None
            and abs(btc_ret_24h) > volatility_cfg["large_btc_move_pct"]
        )
        bullish_volatile_trend = (
            high_vol
            and large_btc_move
            and breadth_sample_ok
            and btc_trend in {"uptrend", "transition_up"}
            and eth_trend in {"uptrend", "transition_up"}
            and breadth_score >= volatility_cfg["trend_min_breadth_ema20_pct"]
            and breadth["positive_24h_pct"] >= volatility_cfg["trend_min_positive_24h_pct"]
        )
        bearish_volatile_trend = (
            high_vol
            and large_btc_move
            and breadth_sample_ok
            and btc_trend in {"downtrend", "transition_down"}
            and eth_trend in {"downtrend", "transition_down"}
            and breadth_score <= volatility_cfg["trend_max_breadth_ema20_pct"]
            and breadth["positive_24h_pct"] <= volatility_cfg["trend_max_positive_24h_pct"]
        )

        if bullish_volatile_trend or bearish_volatile_trend:
            label = "high-volatility trend"
            if bullish_volatile_trend:
                risk_mode = "cautious-risk-on"
                style = "reduced-size trend continuation; enter only confirmed pullbacks or retests"
            else:
                risk_mode = "cautious-risk-off"
                style = "reduced-size short continuation; enter only confirmed failed bounces or retests"
        elif high_vol and large_btc_move:
            label = "high-volatility danger"
            risk_mode = "danger"
            style = "reduce size or no trade until structure settles"
        elif breadth_sample_ok and btc_trend in {"uptrend", "transition_up"} and eth_trend in {
            "uptrend",
            "transition_up",
        } and breadth_score >= 55:
            label = "bullish trend"
            risk_mode = "risk-on"
            style = "selective longs; prefer pullbacks on relative strength"
        elif breadth_sample_ok and btc_trend in {"downtrend", "transition_down"} and breadth_score <= 40:
            label = "bearish trend"
            risk_mode = "risk-off"
            style = "short bias or no trade; avoid weak altcoin longs"
        elif 40 <= breadth_score <= 60:
            label = "range/chop"
            risk_mode = "neutral"
            style = "mean reversion or wait for clean breakouts"
        else:
            label = "transition"
            risk_mode = "mixed"
            style = "selective only; demand clean invalidation"

        confidence = 45.0
        if btc_trend != "unknown":
            confidence += 20
        if eth_trend != "unknown":
            confidence += 10
        if total >= 8:
            confidence += 15
        if btc_atr_pct is not None:
            confidence += 10
        if not breadth_sample_ok:
            confidence = min(confidence, 70.0)
        confidence = clamp(confidence)

        key_levels: dict[str, dict[str, float]] = {}
        for symbol, frame in [("BTC/USDT", btc_frame), ("ETH/USDT", eth_frame)]:
            if frame is None or frame.empty:
                continue
            resistance, support = recent_range(frame, 20)
            key_levels[symbol] = {
                "last": float(frame["close"].iloc[-1]),
                "local_support": float(support) if support is not None else 0.0,
                "local_resistance": float(resistance) if resistance is not None else 0.0,
            }

        explanation = (
            f"BTC trend is {btc_trend}, ETH trend is {eth_trend}, and "
            f"{breadth['above_ema20_pct']:.1f}% of tracked symbols are above EMA20."
        )

        regime = MarketRegime(
            label=label,
            confidence=round(confidence, 1),
            risk_mode=risk_mode,
            recommended_style=style,
            btc_trend=btc_trend,
            eth_trend=eth_trend,
            alt_breadth=breadth,
            volatility={
                "btc_atr_percentile": round(btc_atr_pct, 1) if btc_atr_pct is not None else "n/a",
                "state": (
                    "elevated_trending"
                    if (bullish_volatile_trend or bearish_volatile_trend)
                    else "elevated" if high_vol else "normal/unknown"
                ),
            },
            key_levels=key_levels,
            explanation=explanation,
            warnings=warnings,
        )
        self.save_output(model_to_dict(regime))
        return regime
