"""StockTechnicalAgent — per-symbol technical setup.

Mode-aware:
  intraday: 15m structure + 1h trend filter + prev-day H/L + VWAP if available
  swing:    1h structure + 1d trend filter
  invest:   1d structure + 1wk trend filter

Outputs a setup with entry zone, invalidation, targets, RR, plus a quality
score (0-100) that StockScoringAgent feeds into the technical_setup weight.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

import pandas as pd

from src.execution.stop_contract import (
    build_initial_stop_contract,
    entry_anchor,
    stock_intraday_structural_stop_contract,
)
from src.indicators.technicals import atr, ema, pct_return
from src.stocks.agents.base import StocksBaseAgent
from src.stocks.data_collectors.stock_ohlcv_collector import StockOHLCVCollector


@dataclass
class TechnicalSetup:
    symbol: str
    mode: str
    direction: str            # long / short / no_trade
    trend: str                # uptrend / downtrend / range
    last_close: float | None
    ema20: float | None
    ema50: float | None
    atr14: float | None
    prev_day_high: float | None
    prev_day_low: float | None
    vwap: float | None        # intraday only; None elsewhere
    volume_ratio: float | None  # last bar volume / rolling 20-bar mean; None when missing
    entry_low: float | None
    entry_high: float | None
    invalidation: float | None
    tp1: float | None
    tp2: float | None
    tp3: float | None
    rr_to_tp1: float | None
    quality_score: float
    notes: list[str]
    # Raw 0..1 fraction reflecting completeness of inputs for this setup.
    # Consumed by StockScoringAgent's data_confidence component.
    data_confidence_raw: float = 0.5
    # Flags surfaced to the report for visibility (e.g. missing intraday frame).
    data_flags: list[str] = field(default_factory=list)
    # TP1 provenance: "structural" (a real prior-day level), "atr_measured" (1.5*ATR fallback, NO
    # structural level), or "unavailable". rr_to_structural_tp1 is the RR to the structural level
    # only (None when there is none) so a pure ATR objective is never mistaken for a structural target.
    tp1_source: str = "unavailable"
    rr_to_structural_tp1: float | None = None
    # Distance of price beyond the 20-EMA in ATR units, in the trade direction (>0 = extended).
    atr_extension: float | None = None
    stop_source: str = ""
    stop_model: str = ""
    stop_contract: dict[str, Any] = field(default_factory=dict)
    candidate_structural_stop_contract: dict[str, Any] = field(default_factory=dict)


class StockTechnicalAgent(StocksBaseAgent):
    name = "stock_technical"

    def run(
        self,
        symbols: list[str] | None = None,
        *,
        mode: str = "intraday",
    ) -> dict[str, Any]:
        symbols = [s.upper() for s in (symbols or self.stocks_config.default_symbols)]
        loader = StockOHLCVCollector(self.config, self.stocks_config)
        setups: list[TechnicalSetup] = []

        for symbol in symbols:
            setup = self._build(symbol, loader, mode)
            if setup is not None:
                setups.append(setup)

        setups.sort(key=lambda s: s.quality_score, reverse=True)
        payload = {
            "mode": mode,
            "setups": [asdict(s) for s in setups],
        }
        self.save_output(payload)
        return payload

    def _build(
        self,
        symbol: str,
        loader: StockOHLCVCollector,
        mode: str,
    ) -> TechnicalSetup | None:
        # Pick context/exec frames per mode.
        if mode == "intraday":
            exec_tf, context_tf = "15m", "1h"
        elif mode == "swing":
            exec_tf, context_tf = "1h", "1d"
        else:  # invest
            exec_tf, context_tf = "1d", "1wk"

        exec_frame = loader.load_cached(symbol, exec_tf)
        context_frame = loader.load_cached(symbol, context_tf)
        if context_frame is None or len(context_frame) < 30:
            return None
        # Daily frame is the source of prev-day H/L regardless of mode.
        daily_frame = loader.load_cached(symbol, "1d")

        close = context_frame["close"]
        ema20_series = ema(close, 20)
        ema50_series = ema(close, 50)
        atr14 = atr(context_frame, 14)
        last_close = float(close.iloc[-1])
        ema20_last = None if pd.isna(ema20_series.iloc[-1]) else float(ema20_series.iloc[-1])
        ema50_last = None if pd.isna(ema50_series.iloc[-1]) else float(ema50_series.iloc[-1])
        atr_last = None if pd.isna(atr14.iloc[-1]) else float(atr14.iloc[-1])

        trend = self._trend(close, ema20_series, ema50_series)
        prev_h, prev_l = _prev_day_levels(daily_frame)
        vwap_val = _vwap(exec_frame) if mode == "intraday" else None
        volume_ratio = _volume_ratio(context_frame, window=20)

        direction = self._direction(trend)
        notes: list[str] = []

        # Data-completeness score for downstream data_confidence component.
        data_conf, data_flags = _compute_data_confidence(
            mode=mode,
            context_frame=context_frame,
            exec_frame=exec_frame,
            daily_frame=daily_frame,
            prev_h=prev_h,
            prev_l=prev_l,
            atr_last=atr_last,
            volume_ratio=volume_ratio,
            vwap_val=vwap_val,
        )

        # Build entry zone + invalidation + targets.
        # 2026-07-02 RR fix: the old geometry put the stop 1.5*ATR from the entry anchor while TP1
        # sat 1.5*ATR away → rr_to_tp1 was mechanically ~1.0 for EVERY setup, so the
        # require_rr_to_tp1_gte:1.5 gate could never pass. Now the live production stop stays the
        # legacy 1.0*ATR distance, while a separate structural-stop candidate is stored for research.
        # TP1 is the STRUCTURAL prior-day extreme when it is a real level
        # beyond the entry (else a measured 1.5*ATR objective). rr_to_tp1 is computed from those
        # real levels — setups that do not offer a clean >=1.5R first target get a low rr and are
        # demoted to C by the hard RR gate downstream (no artificial TP stretching).
        entry_low = entry_high = invalidation = tp1 = tp2 = tp3 = None
        rr_to_tp1: float | None = None
        rr_to_structural_tp1: float | None = None
        tp1_source: str = "unavailable"
        atr_extension: float | None = None
        stop_source = ""
        stop_model = ""
        if atr_last is not None and direction in ("long", "short"):
            if direction == "long":
                entry_high = last_close
                entry_low = last_close - 0.5 * atr_last
                invalidation = entry_high - 1.0 * atr_last     # legacy 1.0-ATR stop
                stop_source = "legacy_atr_stop"
                stop_model = "atr_distance_v1"
                risk = entry_high - invalidation
                structural_tp1 = prev_h if (prev_h is not None and prev_h > entry_high + 0.1 * atr_last) else None
                if structural_tp1 is not None:
                    tp1, tp1_source = structural_tp1, "structural"
                else:
                    tp1, tp1_source = entry_high + 1.5 * atr_last, "atr_measured"
                tp2 = max(entry_high + 2.5 * atr_last, tp1 + atr_last)
                tp3 = max(entry_high + 4.0 * atr_last, tp2 + atr_last)
                reward = tp1 - entry_high
                rr_to_tp1 = round(reward / risk, 2) if risk and risk > 0 else None
                if structural_tp1 is not None and risk and risk > 0:
                    rr_to_structural_tp1 = round((structural_tp1 - entry_high) / risk, 2)
                if ema20_last is not None and atr_last:
                    atr_extension = round((last_close - ema20_last) / atr_last, 2)
            else:  # short
                entry_low = last_close
                entry_high = last_close + 0.5 * atr_last
                invalidation = entry_low + 1.0 * atr_last      # legacy 1.0-ATR stop
                stop_source = "legacy_atr_stop"
                stop_model = "atr_distance_v1"
                risk = invalidation - entry_low
                structural_tp1 = prev_l if (prev_l is not None and prev_l < entry_low - 0.1 * atr_last) else None
                if structural_tp1 is not None:
                    tp1, tp1_source = structural_tp1, "structural"
                else:
                    tp1, tp1_source = entry_low - 1.5 * atr_last, "atr_measured"
                tp2 = min(entry_low - 2.5 * atr_last, tp1 - atr_last)
                tp3 = min(entry_low - 4.0 * atr_last, tp2 - atr_last)
                reward = entry_low - tp1
                rr_to_tp1 = round(reward / risk, 2) if risk and risk > 0 else None
                if structural_tp1 is not None and risk and risk > 0:
                    rr_to_structural_tp1 = round((entry_low - structural_tp1) / risk, 2)
                if ema20_last is not None and atr_last:
                    atr_extension = round((ema20_last - last_close) / atr_last, 2)

        quality = self._quality_score(
            trend=trend,
            direction=direction,
            last_close=last_close,
            ema20=ema20_last,
            ema50=ema50_last,
            atr_last=atr_last,
            rr_to_tp1=rr_to_tp1,
            prev_h=prev_h,
            prev_l=prev_l,
            vwap=vwap_val,
            notes=notes,
        )

        actual_entry_anchor = entry_anchor(direction, entry_low, entry_high, last_close)
        if direction in ("long", "short"):
            stop_contract = build_initial_stop_contract(
                symbol=symbol,
                asset_class="stocks",
                mode=mode,
                direction=direction,
                entry_price=actual_entry_anchor,
                stop_price=invalidation,
                setup={
                    "timeframe": exec_tf,
                    "entry_low": entry_low,
                    "entry_high": entry_high,
                    "invalidation": invalidation,
                    "atr14": atr_last,
                    "vwap": vwap_val,
                    "stop_source": stop_source,
                    "stop_model": stop_model,
                },
            )
            structural_stop_contract = stock_intraday_structural_stop_contract(
                symbol=symbol,
                direction=direction,
                entry_price=actual_entry_anchor,
                exec_frame=exec_frame,
                atr_value=atr_last,
                vwap=vwap_val,
                timeframe=exec_tf,
            ) if mode == "intraday" else {}
        else:
            stop_contract = {}
            structural_stop_contract = {}

        return TechnicalSetup(
            symbol=symbol,
            mode=mode,
            direction=direction,
            trend=trend,
            last_close=last_close,
            ema20=ema20_last,
            ema50=ema50_last,
            atr14=atr_last,
            prev_day_high=prev_h,
            prev_day_low=prev_l,
            vwap=vwap_val,
            volume_ratio=volume_ratio,
            entry_low=entry_low,
            entry_high=entry_high,
            invalidation=invalidation,
            tp1=tp1,
            tp2=tp2,
            tp3=tp3,
            rr_to_tp1=rr_to_tp1,
            quality_score=quality,
            notes=notes,
            data_confidence_raw=data_conf,
            data_flags=data_flags,
            tp1_source=tp1_source,
            rr_to_structural_tp1=rr_to_structural_tp1,
            atr_extension=atr_extension,
            stop_source=stop_source,
            stop_model=stop_model,
            stop_contract=stop_contract,
            candidate_structural_stop_contract=structural_stop_contract,
        )

    @staticmethod
    def _trend(close: pd.Series, ema20: pd.Series, ema50: pd.Series) -> str:
        if len(close) < 6:
            return "range"
        last = float(close.iloc[-1])
        e20 = float(ema20.iloc[-1])
        e20_prev = float(ema20.iloc[-5])
        e50 = float(ema50.iloc[-1])
        if last > e20 > e20_prev and last > e50:
            return "uptrend"
        if last < e20 < e20_prev and last < e50:
            return "downtrend"
        return "range"

    @staticmethod
    def _direction(trend: str) -> str:
        if trend == "uptrend":
            return "long"
        if trend == "downtrend":
            return "short"
        return "no_trade"

    @staticmethod
    def _quality_score(
        *,
        trend: str,
        direction: str,
        last_close: float | None,
        ema20: float | None,
        ema50: float | None,
        atr_last: float | None,
        rr_to_tp1: float | None,
        prev_h: float | None,
        prev_l: float | None,
        vwap: float | None,
        notes: list[str],
    ) -> float:
        score = 0.0
        if trend in ("uptrend", "downtrend"):
            score += 30
        else:
            notes.append("trend not directional")
        if direction in ("long", "short") and ema20 is not None and ema50 is not None:
            if direction == "long" and last_close and last_close > ema50:
                score += 15
            elif direction == "short" and last_close and last_close < ema50:
                score += 15
            else:
                notes.append("price below/above EMA50 inconsistent with direction")
        if rr_to_tp1 is not None and rr_to_tp1 >= 1.5:
            score += 20
        elif rr_to_tp1 is not None:
            notes.append(f"RR to TP1 below 1.5 ({rr_to_tp1})")
        if atr_last is not None and last_close and (atr_last / last_close) > 0.005:
            score += 15
        else:
            notes.append("ATR too small for actionable move")
        if vwap is not None and last_close:
            if direction == "long" and last_close > vwap:
                score += 10
            elif direction == "short" and last_close < vwap:
                score += 10
        if prev_h and prev_l and last_close:
            # Tag breakouts/breakdowns versus the prior day's range.
            if direction == "long" and last_close > prev_h:
                score += 10
                notes.append("above prev day high")
            elif direction == "short" and last_close < prev_l:
                score += 10
                notes.append("below prev day low")
        return round(max(0.0, min(100.0, score)), 2)


def _prev_day_levels(frame: pd.DataFrame | None) -> tuple[float | None, float | None]:
    if frame is None or len(frame) < 2:
        return None, None
    prev = frame.iloc[-2]
    return float(prev["high"]), float(prev["low"])


def _vwap(frame: pd.DataFrame | None) -> float | None:
    """Rolling session-ish VWAP: use the last ~26 bars (≈ a US session for 15m)."""

    if frame is None or len(frame) < 5:
        return None
    tail = frame.tail(26)
    typical = (tail["high"] + tail["low"] + tail["close"]) / 3.0
    vol = tail["volume"].clip(lower=0)
    denom = float(vol.sum())
    if denom <= 0:
        return None
    num = float((typical * vol).sum())
    return round(num / denom, 4)


def _volume_ratio(frame: pd.DataFrame | None, *, window: int = 20) -> float | None:
    """Last bar volume / rolling-`window` mean. Returns None when we don't have
    enough history or volume is zero/missing."""

    if frame is None or "volume" not in frame.columns:
        return None
    vol = frame["volume"].astype(float)
    if len(vol) < window:
        return None
    avg = vol.rolling(window, min_periods=window).mean().iloc[-1]
    if pd.isna(avg) or avg <= 0:
        return None
    last = float(vol.iloc[-1])
    if last <= 0:
        return None
    return round(last / float(avg), 3)


def _compute_data_confidence(
    *,
    mode: str,
    context_frame: pd.DataFrame,
    exec_frame: pd.DataFrame | None,
    daily_frame: pd.DataFrame | None,
    prev_h: float | None,
    prev_l: float | None,
    atr_last: float | None,
    volume_ratio: float | None,
    vwap_val: float | None,
) -> tuple[float, list[str]]:
    """Compute a 0..1 raw data-confidence score + human flags.

    The score reflects whether the inputs the agents downstream rely on are
    actually present. Missing intraday frame, short context history, no
    prev-day H/L, etc. each subtract.
    """

    score = 0.0
    flags: list[str] = []

    # Context frame quantity (≥50 bars is comfortable, ≥30 is the bare minimum
    # to even enter `_build`).
    n_ctx = len(context_frame)
    if n_ctx >= 100:
        score += 0.30
    elif n_ctx >= 50:
        score += 0.20
    elif n_ctx >= 30:
        score += 0.10
        flags.append("short_context_history")
    else:
        flags.append("very_short_context_history")

    # Daily frame for prev-day levels.
    if daily_frame is not None and len(daily_frame) >= 2:
        score += 0.10
    else:
        flags.append("missing_daily_history")

    # Exec frame is only required for intraday (15m). For swing/invest the
    # exec frame is the context frame.
    if mode == "intraday":
        if exec_frame is not None and len(exec_frame) >= 20:
            score += 0.15
        else:
            flags.append("missing_intraday_exec_frame")
    else:
        score += 0.15  # not applicable → don't penalize swing/invest

    # Prev-day H/L (used by quality_score + structural stops).
    if prev_h is not None and prev_l is not None:
        score += 0.10
    else:
        flags.append("missing_prev_day_levels")

    # ATR (needed for entries/invalidation/RR).
    if atr_last is not None and atr_last > 0:
        score += 0.10
    else:
        flags.append("missing_atr")

    # Volume ratio (needed for scoring's volume component).
    if volume_ratio is not None:
        score += 0.15
    else:
        flags.append("missing_volume_ratio")

    # VWAP (intraday only — bonus, not penalty for swing/invest).
    if mode == "intraday":
        if vwap_val is not None:
            score += 0.10
        else:
            flags.append("missing_vwap")
    else:
        score += 0.10

    return round(min(1.0, max(0.0, score)), 2), flags
