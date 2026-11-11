from __future__ import annotations

from typing import Any

import pandas as pd

from src.agents.base_agent import BaseAgent
from src.indicators.technicals import pct_return
from src.models import DerivativesSummary
from src.utils.validation import clamp, model_to_dict


class DerivativesAgent(BaseAgent):
    name = "derivatives_agent"

    def run(
        self,
        market_data: dict[str, dict[str, pd.DataFrame]],
        raw_records: dict[str, dict[str, Any]],
        external_records: dict[str, dict[str, Any]] | None = None,
    ) -> dict[str, DerivativesSummary]:
        """Build per-symbol derivatives summary.

        ``raw_records`` comes from the primary (Binance) derivatives
        collector. PART 14b — ``external_records`` is the optional
        multi-exchange ``MultiExchangeDerivativesCollectionSummary.records``
        map keyed by symbol. When Binance returns no data for a symbol
        we fall back to MEXC > Bybit > OKX (in that order) and build a
        ``data_available=True`` summary from the fallback venue.
        """

        results: dict[str, DerivativesSummary] = {}
        external_records = external_records or {}

        for symbol, frames in market_data.items():
            record = raw_records.get(symbol, {})
            warnings: list[str] = []
            frame = frames.get("1h")
            price_change_pct = pct_return(frame, 24) if frame is not None else None

            primary_ok = bool(record) and not record.get("error")

            if not primary_ok:
                # PART 14b fallback — try MEXC / Bybit / OKX before giving up.
                fallback = self._build_from_external(
                    symbol=symbol,
                    external=external_records.get(symbol),
                    price_change_pct=price_change_pct,
                )
                if fallback is not None:
                    results[symbol] = fallback
                    continue
                results[symbol] = DerivativesSummary(
                    symbol=symbol,
                    data_available=False,
                    warnings=[record.get("error", "futures data unavailable")] if record else ["futures data unavailable"],
                )
                continue

            premium = record.get("premium_index") or {}
            open_interest = record.get("open_interest") or {}
            hist = record.get("open_interest_hist") or []
            long_short = record.get("long_short_ratio") or []

            try:
                funding_rate = float(premium.get("lastFundingRate"))
            except Exception:
                funding_rate = None
            try:
                oi = float(open_interest.get("openInterest"))
            except Exception:
                oi = None
            oi_value = None
            oi_change_pct = self._oi_change(hist)
            ls_ratio = self._long_short_ratio(long_short)

            interpretation, alignment = self._interpret(price_change_pct, oi_change_pct)
            crowding = "unknown"
            squeeze = "unknown"
            if funding_rate is not None:
                if funding_rate >= 0.001:
                    crowding = "extreme long crowding"
                    warnings.append("Funding is extremely positive; long squeeze risk rises.")
                    alignment -= 0.35
                elif funding_rate >= 0.0005:
                    crowding = "elevated long crowding"
                    warnings.append("Funding is positive enough to reduce late-long quality.")
                    alignment -= 0.15
                elif funding_rate <= -0.0005:
                    squeeze = "short squeeze potential"
                    warnings.append("Funding is negative; shorts may be crowded.")
                    alignment += 0.15
                else:
                    crowding = "normal"
                    squeeze = "normal"

            if ls_ratio is not None and ls_ratio >= 2:
                warnings.append("Global long/short ratio is heavily long skewed.")
            elif ls_ratio is not None and ls_ratio <= 0.5:
                warnings.append("Global long/short ratio is heavily short skewed.")

            results[symbol] = DerivativesSummary(
                symbol=symbol,
                data_available=True,
                funding_rate=funding_rate,
                open_interest=oi,
                open_interest_value=oi_value,
                oi_change_pct=round(oi_change_pct, 2) if oi_change_pct is not None else None,
                price_change_pct=round(price_change_pct, 2) if price_change_pct is not None else None,
                long_short_ratio=round(ls_ratio, 3) if ls_ratio is not None else None,
                interpretation=interpretation,
                crowding_risk=crowding,
                squeeze_potential=squeeze,
                alignment_score=round(clamp(alignment, -1.0, 1.0), 2),
                warnings=warnings,
            )

        self.save_output({symbol: model_to_dict(item) for symbol, item in results.items()})
        return results

    def _build_from_external(
        self,
        *,
        symbol: str,
        external: dict[str, Any] | None,
        price_change_pct: float | None,
    ) -> DerivativesSummary | None:
        """PART 14b — try MEXC > Bybit > OKX from the multi-exchange records.

        Returns ``None`` if no venue has funding/OI for this symbol — caller
        falls back to ``data_available=False``. When we do find data the
        summary is marked available with a ``fallback_via_<venue>`` note in
        ``interpretation`` so downstream scoring/reports know it's not the
        primary Binance feed.
        """
        if not external:
            return None
        venues = (external.get("exchanges") or {}) if isinstance(external, dict) else {}
        if not venues:
            return None
        order = ("mexc", "bybit", "okx")
        for venue in order:
            payload = venues.get(venue)
            if not payload or not isinstance(payload, dict):
                continue
            funding = payload.get("funding_rate")
            oi = payload.get("open_interest")
            if funding is None and oi is None:
                continue
            try:
                funding_rate = float(funding) if funding is not None else None
            except (TypeError, ValueError):
                funding_rate = None
            try:
                oi_val = float(oi) if oi is not None else None
            except (TypeError, ValueError):
                oi_val = None

            # Use Binance-style interpretation. We have no OI delta history
            # from external venues (only point-in-time), so derive a coarse
            # alignment from funding sign + price direction.
            #
            # PART 14b refinement: the fallback is a SUCCESS, not a warning.
            # Earlier the venue-fallback text leaked into the rejected-ideas
            # primary_reason field through ``score.warnings``. The
            # ``interpretation`` field already encodes ``fallback_via_<venue>``
            # for traceability, so we keep the warnings list empty.
            alignment = 0.0
            crowding = "unknown"
            squeeze = "unknown"
            warnings: list[str] = []
            if funding_rate is not None:
                if funding_rate >= 0.001:
                    crowding = "extreme long crowding"
                    alignment -= 0.35
                elif funding_rate >= 0.0005:
                    crowding = "elevated long crowding"
                    alignment -= 0.15
                elif funding_rate <= -0.0005:
                    squeeze = "short squeeze potential"
                    alignment += 0.15
                else:
                    crowding = "normal"
                    squeeze = "normal"
            if price_change_pct is not None:
                # Mild trend nudge so shorts in a down move and longs in an
                # up move get a non-zero alignment from the fallback.
                if price_change_pct < 0:
                    alignment -= 0.2
                elif price_change_pct > 0:
                    alignment += 0.2

            interpretation = (
                f"fallback_via_{venue}: funding "
                f"{funding_rate if funding_rate is not None else 'n/a'}, "
                f"24h move {price_change_pct if price_change_pct is not None else 'n/a'}%"
            )
            return DerivativesSummary(
                symbol=symbol,
                data_available=True,
                funding_rate=funding_rate,
                open_interest=oi_val,
                open_interest_value=payload.get("open_interest_value"),
                oi_change_pct=None,
                price_change_pct=(
                    round(price_change_pct, 2)
                    if price_change_pct is not None else None
                ),
                long_short_ratio=None,
                interpretation=interpretation,
                crowding_risk=crowding,
                squeeze_potential=squeeze,
                alignment_score=round(clamp(alignment, -1.0, 1.0), 2),
                warnings=warnings,
            )
        return None

    @staticmethod
    def _oi_change(hist: list[dict[str, Any]]) -> float | None:
        if not hist or len(hist) < 2:
            return None
        try:
            first = float(hist[0].get("sumOpenInterest"))
            last = float(hist[-1].get("sumOpenInterest"))
        except Exception:
            return None
        if first <= 0:
            return None
        return (last / first - 1) * 100

    @staticmethod
    def _long_short_ratio(rows: list[dict[str, Any]]) -> float | None:
        if not rows:
            return None
        try:
            return float(rows[-1].get("longShortRatio"))
        except Exception:
            return None

    @staticmethod
    def _interpret(price_change_pct: float | None, oi_change_pct: float | None) -> tuple[str, float]:
        if price_change_pct is None or oi_change_pct is None:
            return "data partially unavailable", 0.0
        if price_change_pct > 0 and oi_change_pct > 0:
            return "price up + OI up: fresh positioning confirms trend, monitor crowding", 0.65
        if price_change_pct > 0 and oi_change_pct < 0:
            return "price up + OI down: short covering, weaker continuation quality", 0.2
        if price_change_pct < 0 and oi_change_pct > 0:
            return "price down + OI up: fresh shorts pressing, possible squeeze if price reclaims", -0.45
        if price_change_pct < 0 and oi_change_pct < 0:
            return "price down + OI down: deleveraging or long liquidation", -0.25
        return "flat price/OI: no strong derivatives read", 0.0
