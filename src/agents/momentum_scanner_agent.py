from __future__ import annotations

import pandas as pd

from src.agents.base_agent import BaseAgent
from src.indicators.relative_strength import relative_strength_return
from src.indicators.technicals import enrich_ohlcv, pct_return, recent_range
from src.indicators.volatility import atr_percentile
from src.indicators.volume_anomaly import volume_ratio
from src.models import MomentumCandidate
from src.utils.validation import clamp, model_to_dict


class MomentumScannerAgent(BaseAgent):
    name = "momentum_scanner_agent"

    def run(
        self,
        market_data: dict[str, dict[str, pd.DataFrame]],
        symbols: list[str] | None = None,
    ) -> list[MomentumCandidate]:
        tf = self.config.settings.get("execution", {}).get("default_timeframe", "1h")
        selected_symbols = symbols or list(market_data.keys())
        btc_frame = market_data.get("BTC/USDT", {}).get(tf)
        eth_frame = market_data.get("ETH/USDT", {}).get(tf)
        candidates: list[MomentumCandidate] = []

        for symbol in selected_symbols:
            frame = market_data.get(symbol, {}).get(tf)
            if frame is None or len(frame) < 60:
                continue
            enriched = enrich_ohlcv(frame)
            last = enriched.iloc[-1]
            close = float(last["close"])
            atr = float(last["atr14"]) if pd.notna(last["atr14"]) else None
            ema20 = float(last["ema20"]) if pd.notna(last["ema20"]) else close
            ema50 = float(last["ema50"]) if pd.notna(last["ema50"]) else close
            ret24 = pct_return(frame, 24)
            ret7d = pct_return(frame, 24 * 7)
            rs_btc = (
                relative_strength_return(frame, btc_frame, 24)
                if btc_frame is not None and symbol != "BTC/USDT"
                else 0.0
            )
            rs_eth = (
                relative_strength_return(frame, eth_frame, 24)
                if eth_frame is not None and symbol != "ETH/USDT"
                else 0.0
            )
            vol_ratio = volume_ratio(frame, 20)
            atr_pct = atr_percentile(frame)
            range_high, range_low = recent_range(frame, 20)

            # PART 22 — short squeeze-risk diagnostics (1h tf):
            # 1h return, 24h quote volume (USD), and upper-wick/ATR stats over
            # the recent window. Computed read-only from the frame; consumed by
            # the short squeeze guard in the scoring agent.
            ret1h = pct_return(frame, 1)
            recent24 = frame.tail(24)
            quote_vol_24h = (
                float((recent24["close"] * recent24["volume"]).sum())
                if len(recent24) else None
            )
            uw_max = uw_avg = None
            try:
                tail = enriched.tail(48)
                upper_wick = tail["high"] - tail[["open", "close"]].max(axis=1)
                uw_ratio = (upper_wick / tail["atr14"]).replace(
                    [float("inf"), float("-inf")], pd.NA
                ).dropna()
                if len(uw_ratio):
                    uw_max = float(uw_ratio.max())
                    uw_avg = float(uw_ratio.mean())
            except Exception:
                uw_max = uw_avg = None

            tags: list[str] = []
            warnings: list[str] = []
            if rs_btc is not None and rs_btc > 1.5:
                tags.append("relative_strength")
            if rs_btc is not None and rs_btc < -1.5:
                tags.append("weak_vs_market")
            if vol_ratio is not None and vol_ratio >= 1.5:
                tags.append("volume_expansion")
            if range_high is not None and close > range_high:
                tags.append("breakout")
            if range_low is not None and close < range_low:
                tags.append("breakdown")

            distance_atr = None
            if atr and atr > 0:
                distance_atr = (close - ema20) / atr
                if abs(distance_atr) > 2:
                    tags.append("overextended")
                    warnings.append("Price is more than 2 ATR from EMA20; do not chase.")

            long_score = 45.0
            if ret24 is not None:
                long_score += max(min(ret24, 10), -10) * 1.2
            if ret7d is not None:
                long_score += max(min(ret7d, 20), -20) * 0.35
            if rs_btc is not None:
                long_score += max(min(rs_btc, 8), -8) * 1.4
            if rs_eth is not None:
                long_score += max(min(rs_eth, 8), -8) * 0.8
            if vol_ratio is not None:
                long_score += min(max(vol_ratio - 1, 0), 3) * 5
            if close > ema20 > ema50:
                long_score += 10
            if "breakout" in tags:
                long_score += 8
            if "overextended" in tags:
                long_score -= 8

            short_score = 45.0
            if ret24 is not None:
                short_score += max(min(-ret24, 10), -10) * 1.2
            if rs_btc is not None:
                short_score += max(min(-rs_btc, 8), -8) * 1.4
            if vol_ratio is not None:
                short_score += min(max(vol_ratio - 1, 0), 3) * 4
            if close < ema20 < ema50:
                short_score += 12
            if "breakdown" in tags:
                short_score += 8
            if "overextended" in tags and distance_atr is not None and distance_atr < -2:
                short_score -= 6

            long_score = clamp(long_score)
            short_score = clamp(short_score)
            if long_score >= short_score and long_score >= 50:
                bias = "long"
                score = long_score
            elif short_score > long_score and short_score >= 50:
                bias = "short"
                score = short_score
            else:
                bias = "watch"
                score = max(long_score, short_score)

            candidates.append(
                MomentumCandidate(
                    symbol=symbol,
                    direction_bias=bias,
                    score=round(score, 1),
                    return_24h=round(ret24, 2) if ret24 is not None else None,
                    return_7d=round(ret7d, 2) if ret7d is not None else None,
                    relative_strength_btc=round(rs_btc, 2) if rs_btc is not None else None,
                    relative_strength_eth=round(rs_eth, 2) if rs_eth is not None else None,
                    volume_ratio=round(vol_ratio, 2) if vol_ratio is not None else None,
                    atr_percentile=round(atr_pct, 1) if atr_pct is not None else None,
                    distance_from_ema20_atr=round(distance_atr, 2)
                    if distance_atr is not None
                    else None,
                    reason_tags=tags,
                    warnings=warnings,
                    return_1h=round(ret1h, 2) if ret1h is not None else None,
                    quote_volume_24h_usd=round(quote_vol_24h, 2)
                    if quote_vol_24h is not None else None,
                    upper_wick_atr_max=round(uw_max, 2) if uw_max is not None else None,
                    upper_wick_atr_avg=round(uw_avg, 2) if uw_avg is not None else None,
                )
            )

        candidates.sort(key=lambda item: item.score, reverse=True)
        for index, candidate in enumerate(candidates, start=1):
            candidate.rank = index
        self.save_output({"candidates": [model_to_dict(item) for item in candidates]})
        return candidates
