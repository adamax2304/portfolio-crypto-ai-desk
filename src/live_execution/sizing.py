from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR
from typing import Any

from src.execution.stop_contract import is_structural_stop_contract

from .config import LiveCanaryConfig


class PlanRejected(ValueError):
    """A deterministic preflight rejection with optional operator diagnostics."""

    def __init__(self, reason: str, *, details: dict[str, Any] | None = None):
        super().__init__(reason)
        self.details = details or {}


def _f(value: Any, default: float | None = None) -> float | None:
    try:
        return default if value in (None, "") else float(value)
    except (TypeError, ValueError):
        return default


def _round_step(value: float, step: float, rounding: str = "down") -> float:
    if step <= 0:
        return value
    mode = ROUND_FLOOR if rounding == "down" else ROUND_CEILING
    units = (Decimal(str(value)) / Decimal(str(step))).to_integral_value(rounding=mode)
    return float(units * Decimal(str(step)))


def stop_risk_components(*, entry_price: float, stop_price: float,
                         volume_contracts: float, contract_size: float,
                         taker_fee_rate: float, slippage_rate: float) -> dict[str, float]:
    """Return the all-in stop loss for an exact MEXC fill.

    MEXC reports the price-only component in its TP/SL modal.  The local risk
    reservation additionally includes conservative entry/exit fees and
    slippage, but must always use the actual fill price rather than an IOC
    limit that may have filled favourably.
    """
    if min(entry_price, stop_price, volume_contracts, contract_size) <= 0:
        raise ValueError("STOP_RISK_COMPONENTS_REQUIRE_POSITIVE_VALUES")
    entry_notional = volume_contracts * contract_size * entry_price
    stop_notional = volume_contracts * contract_size * stop_price
    gross_stop_loss = volume_contracts * contract_size * abs(entry_price - stop_price)
    fees = (entry_notional + stop_notional) * max(0.0, taker_fee_rate)
    slippage = (entry_notional + stop_notional) * max(0.0, slippage_rate)
    return {
        "gross_stop_loss_usdt": gross_stop_loss,
        "estimated_fees_usdt": fees,
        "estimated_slippage_usdt": slippage,
        "net_stop_risk_usdt": gross_stop_loss + fees + slippage,
    }


def rebase_filled_plan(plan: dict[str, Any], *, fill_price: float) -> dict[str, Any]:
    """Re-freeze SL/TP geometry from the exchange-confirmed entry fill.

    The submitted IOC limit is only a worst executable price, not the position
    entry.  Keeping targets anchored to that limit creates fictitious R and can
    make Paper/live comparisons disagree.  Preserve the planned stop percentage
    and target R ladder, cap the resulting stop by the already-reserved all-in
    risk, and rewrite all three partial-TP targets for reconciliation.
    """
    out = dict(plan)
    entry = float(fill_price)
    reference = float(plan.get("limit_price") or plan.get("reference_entry") or 0.0)
    stop = float(plan.get("original_stop") or 0.0)
    targets = [float(plan.get(key) or 0.0) for key in ("tp1", "tp2", "tp3")]
    direction = str(plan.get("direction") or "").lower()
    if entry <= 0 or reference <= 0 or stop <= 0 or min(targets) <= 0:
        raise PlanRejected("FILL_REBASE_GEOMETRY_MISSING")
    if direction not in {"long", "short"}:
        raise PlanRejected("FILL_REBASE_DIRECTION_INVALID")
    valid = (
        stop < reference < targets[0] < targets[1] < targets[2]
        if direction == "long"
        else targets[2] < targets[1] < targets[0] < reference < stop
    )
    if not valid:
        raise PlanRejected("FILL_REBASE_GEOMETRY_INVALID")

    original_distance = abs(reference - stop)
    risk_pct = original_distance / reference
    r_multipliers = [abs(target - reference) / original_distance for target in targets]
    volume = float(plan.get("volume_contracts") or 0.0)
    contract_size = float(plan.get("contract_size") or 0.0)
    unit_notional = volume * contract_size
    if unit_notional <= 0:
        raise PlanRejected("FILL_REBASE_VOLUME_INVALID")
    target_risk = float(plan.get("actual_risk_usdt") or plan.get("risk_budget_usdt") or 0.0)
    if target_risk <= 0:
        # Plans frozen before fill-rebasing existed do not carry an explicit
        # risk budget. Their original all-in stop risk is the authoritative cap.
        target_risk = stop_risk_components(
            entry_price=reference,
            stop_price=stop,
            volume_contracts=volume,
            contract_size=contract_size,
            taker_fee_rate=float(plan.get("taker_fee_rate") or 0.0),
            slippage_rate=float(plan.get("slippage_rate") or 0.0),
        )["net_stop_risk_usdt"]
    friction = max(0.0, float(plan.get("taker_fee_rate") or 0.0)) + max(
        0.0, float(plan.get("slippage_rate") or 0.0)
    )
    base = target_risk / unit_notional - 2.0 * entry * friction
    denominator = (1.0 - friction) if direction == "long" else (1.0 + friction)
    max_budget_distance = base / denominator if denominator > 0 else 0.0
    if max_budget_distance <= 0:
        raise PlanRejected("FILL_REBASE_RISK_BUDGET_INVALID")
    tick = float(plan.get("price_tick") or 0.0)
    structural_contract = plan.get("stop_contract") if isinstance(plan.get("stop_contract"), dict) else None
    preserve_structural_stop = is_structural_stop_contract(structural_contract)
    structural_stop_budget_capped = False
    if preserve_structural_stop:
        if direction == "long":
            new_stop = _round_step(stop, tick, "up")
        else:
            new_stop = _round_step(stop, tick, "down")
        distance = abs(entry - new_stop)
        if distance <= 0:
            raise PlanRejected("FILL_REBASE_STRUCTURAL_STOP_INVALID")
        if distance > max_budget_distance:
            structural_stop_budget_capped = True
            distance = max_budget_distance
            preserve_structural_stop = False
    else:
        structural_distance = entry * risk_pct
        distance = min(structural_distance, max_budget_distance)

    if direction == "long":
        if not preserve_structural_stop:
            # Round the stop toward the entry so exchange tick conversion cannot
            # increase the already-reserved dollar risk.
            new_stop = _round_step(entry - distance, tick, "up")
        new_targets = [_round_step(entry + distance * r, tick, "down") for r in r_multipliers]
    else:
        if not preserve_structural_stop:
            new_stop = _round_step(entry + distance, tick, "down")
        new_targets = [_round_step(entry - distance * r, tick, "up") for r in r_multipliers]
    raw_targets = list(new_targets)
    min_gap = tick if tick > 0 else max(abs(entry) * 1e-8, 1e-12)
    if direction == "long":
        adjusted_targets = []
        floor = entry
        for target in new_targets:
            candidate = max(float(target), floor + min_gap)
            adjusted = _round_step(candidate, tick, "up") if tick > 0 else candidate
            adjusted_targets.append(adjusted)
            floor = adjusted
        new_targets = adjusted_targets
        valid = new_stop < entry < new_targets[0] < new_targets[1] < new_targets[2]
    else:
        adjusted_targets = []
        ceiling = entry
        for target in new_targets:
            candidate = min(float(target), ceiling - min_gap)
            adjusted = _round_step(candidate, tick, "down") if tick > 0 else candidate
            adjusted_targets.append(adjusted)
            ceiling = adjusted
        new_targets = adjusted_targets
        valid = new_targets[2] < new_targets[1] < new_targets[0] < entry < new_stop
    if not valid:
        raise PlanRejected("FILL_REBASE_ROUNDED_GEOMETRY_INVALID")

    risk = stop_risk_components(
        entry_price=entry,
        stop_price=new_stop,
        volume_contracts=volume,
        contract_size=contract_size,
        taker_fee_rate=float(plan.get("taker_fee_rate") or 0.0),
        slippage_rate=float(plan.get("slippage_rate") or 0.0),
    )
    if risk["net_stop_risk_usdt"] > target_risk + max(0.02, target_risk * 0.01):
        raise PlanRejected("FILL_REBASE_RISK_EXCEEDS_RESERVED")

    out.update({
        "fill_price": entry,
        "fill_rebased": True,
        "pre_fill_limit_price": reference,
        "pre_fill_original_stop": stop,
        "original_stop": new_stop,
        "tp1": new_targets[0],
        "tp2": new_targets[1],
        "tp3": new_targets[2],
        "stop_distance_pct": abs(entry - new_stop) / entry,
        "actual_risk_usdt": risk["net_stop_risk_usdt"],
        "fill_rebase_r_multipliers": r_multipliers,
        "fill_rebase_min_target_gap_applied": raw_targets != list(new_targets),
        "fill_rebase_preserved_structural_stop": preserve_structural_stop,
        "fill_rebase_structural_stop_budget_capped": structural_stop_budget_capped,
    })
    legs = []
    for index, leg in enumerate(plan.get("partial_tp_legs") or []):
        updated = dict(leg)
        if index < 3:
            updated["target"] = new_targets[index]
        legs.append(updated)
    if legs:
        out["partial_tp_legs"] = legs
    return out


def _looks_like_stock_futures(contract: dict[str, Any]) -> bool:
    raw_plates = contract.get("conceptPlate") or []
    if isinstance(raw_plates, str):
        raw_plates = [raw_plates]
    plates = {str(value).lower() for value in raw_plates}
    text = " ".join(
        str(contract.get(key) or "").upper()
        for key in ("symbol", "baseCoin", "baseCoinName", "displayName", "symbolType")
    )
    return (
        any(
            "stock" in plate or "tradfi" in plate or plate == "etf"
            for plate in plates
        )
        or "STOCK" in text
        or str(contract.get("symbolType") or "").strip().lower() == "etf"
    )


@dataclass(frozen=True)
class OrderPlan:
    decision_id: str
    signal_id: str
    symbol: str
    external_oid: str
    entry_mode: str
    direction: str
    order_type: int
    side: int
    open_type: int
    position_mode: int
    limit_price: float
    reference_entry: float
    current_ask: float
    current_bid: float
    spread_bps: float
    volume_contracts: float
    contract_size: float
    price_tick: float
    volume_step: float
    min_volume: float
    notional_usdt: float
    original_stop: float
    tp1: float
    tp2: float
    tp3: float
    stop_distance_pct: float
    risk_rate: float
    risk_budget_usdt: float
    actual_risk_usdt: float
    leverage: int
    estimated_margin_usdt: float
    estimated_liquidation_price: float
    liquidation_distance_multiple: float
    maker_fee_rate: float
    taker_fee_rate: float
    slippage_rate: float
    stop_contract: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def mexc_order(self) -> dict[str, Any]:
        # Keep the fill protected while the monitor atomically replaces this
        # fallback with the three strategy-native partial TP/SL legs.
        return {
            "symbol": self.symbol,
            "price": self.limit_price,
            "vol": self.volume_contracts,
            "leverage": self.leverage,
            "side": self.side,
            "type": self.order_type,
            "openType": self.open_type,
            "externalOid": self.external_oid,
            "stopLossPrice": self.original_stop,
            "lossTrend": 2,
            "positionMode": self.position_mode,
            "stpMode": 1,
        }


def allocate_partial_tp_volumes(*, total_volume: float, volume_step: float,
                                min_volume: float,
                                weights: tuple[float, float, float]) -> tuple[float, float, float]:
    """Split a MEXC contract volume into three valid deterministic legs."""
    if volume_step <= 0 or min_volume <= 0 or len(weights) != 3:
        raise PlanRejected("PARTIAL_TP_METADATA_INVALID")
    if min(weights) <= 0 or abs(sum(weights) - 1.0) > 1e-9:
        raise PlanRejected("PARTIAL_TP_WEIGHTS_INVALID")
    step = Decimal(str(volume_step))
    total_units = int((Decimal(str(total_volume)) / step).to_integral_value(rounding=ROUND_FLOOR))
    min_units = int((Decimal(str(min_volume)) / step).to_integral_value(rounding=ROUND_CEILING))
    if total_units < 3 * min_units:
        raise PlanRejected("PARTIAL_TP_VOLUME_TOO_SMALL")

    exact = [Decimal(total_units) * Decimal(str(weight)) for weight in weights]
    units = [max(min_units, int(value.to_integral_value(rounding=ROUND_FLOOR))) for value in exact]
    while sum(units) > total_units:
        candidates = [idx for idx, value in enumerate(units) if value > min_units]
        if not candidates:
            raise PlanRejected("PARTIAL_TP_VOLUME_TOO_SMALL")
        idx = max(candidates, key=lambda i: (Decimal(units[i]) - exact[i], -i))
        units[idx] -= 1
    while sum(units) < total_units:
        idx = max(range(3), key=lambda i: (exact[i] - Decimal(units[i]), i))
        units[idx] += 1
    volumes = tuple(float(Decimal(value) * step) for value in units)
    if abs(sum(volumes) - total_volume) > max(1e-9, volume_step * 1e-9):
        raise PlanRejected("PARTIAL_TP_VOLUME_SUM_MISMATCH")
    return volumes


def build_mexc_pretrade_parity(*, plan: OrderPlan, contract: dict[str, Any],
                               depth: dict[str, Any], captured_at: str,
                               weights: tuple[float, float, float]) -> dict[str, Any]:
    """Freeze the exact MEXC contract/book/geometry used before submission."""
    asks, bids = depth.get("asks") or [], depth.get("bids") or []
    if not asks or not bids:
        raise PlanRejected("MEXC_PARITY_BOOK_MISSING")
    ask, bid = float(asks[0][0]), float(bids[0][0])
    mid = (ask + bid) / 2.0
    spread_bps = (ask - bid) / mid * 10_000.0
    volumes = allocate_partial_tp_volumes(
        total_volume=plan.volume_contracts,
        volume_step=plan.volume_step,
        min_volume=plan.min_volume,
        weights=weights,
    )
    direction = str(plan.direction).lower()
    if direction not in {"long", "short"}:
        raise PlanRejected("UNSUPPORTED_DIRECTION")
    targets = (plan.tp1, plan.tp2, plan.tp3)
    legs = []
    entry_notional = plan.volume_contracts * plan.contract_size * plan.limit_price
    exit_turnover = 0.0
    gross_targets = 0.0
    for index, (volume, target) in enumerate(zip(volumes, targets), start=1):
        leg_notional = volume * plan.contract_size * plan.limit_price
        gross = volume * plan.contract_size * (
            (target - plan.limit_price) if direction == "long" else (plan.limit_price - target)
        )
        exit_value = volume * plan.contract_size * target
        exit_turnover += exit_value
        gross_targets += gross
        legs.append({
            "leg": index,
            "target": target,
            "volume_contracts": volume,
            "entry_notional_usdt": round(leg_notional, 8),
            "gross_pnl_at_target_usdt": round(gross, 8),
        })
    fees = (entry_notional + exit_turnover) * plan.taker_fee_rate
    slippage = (entry_notional + exit_turnover) * plan.slippage_rate
    stop_gross = plan.volume_contracts * plan.contract_size * (
        (plan.original_stop - plan.limit_price)
        if direction == "long" else (plan.limit_price - plan.original_stop)
    )
    executable_price = ask if direction == "long" else bid
    clean = bool(
        str(contract.get("symbol") or "") == plan.symbol
        and int(contract.get("state", -1)) == 0
        and contract.get("apiAllowed") is True
        and abs(executable_price - (plan.current_ask if direction == "long" else plan.current_bid))
        <= max(plan.price_tick, 1e-12)
        and abs(spread_bps - plan.spread_bps) <= 1e-3
        and abs(sum(volumes) - plan.volume_contracts) <= max(1e-9, plan.volume_step * 1e-9)
    )
    if not clean:
        raise PlanRejected("MEXC_PARITY_SNAPSHOT_NOT_CLEAN")
    return {
        "version": "mexc_native_pretrade_v2",
        "captured_at": captured_at,
        "clean": True,
        "evidence_class": "forward_post_activation",
        "contract": {
            "symbol": plan.symbol,
            "state": int(contract.get("state", -1)),
            "api_allowed": bool(contract.get("apiAllowed")),
            "contract_size": plan.contract_size,
            "price_tick": plan.price_tick,
            "volume_step": plan.volume_step,
            "min_volume": plan.min_volume,
        },
        "book": {
            "best_bid": bid,
            "best_ask": ask,
            "spread_bps": round(spread_bps, 6),
            "paper_reference_entry": plan.reference_entry,
            "mexc_limit_entry": plan.limit_price,
            "entry_drift_bps": round(
                ((ask - plan.reference_entry) if direction == "long" else (plan.reference_entry - bid))
                / plan.reference_entry * 10_000.0,
                6,
            ),
        },
        "exit_profile_id": "mexc_live_partial_tp_33_33_34_v1",
        "legs": legs,
        "paper_equivalent_on_mexc": {
            "gross_pnl_all_targets_usdt": round(gross_targets, 8),
            "fees_usdt": round(fees, 8),
            "slippage_usdt": round(slippage, 8),
            "funding_usdt": 0.0,
            "net_pnl_all_targets_usdt": round(gross_targets - fees - slippage, 8),
            "gross_pnl_at_stop_usdt": round(stop_gross, 8),
            "net_pnl_at_stop_usdt": round(stop_gross - fees - slippage, 8),
        },
    }


def build_order_plan(*, decision: dict[str, Any], contract: dict[str, Any],
                     depth: dict[str, Any], cfg: LiveCanaryConfig,
                     exchange_equity_usdt: float | None = None) -> OrderPlan:
    contract_symbol = str(contract.get("symbol") or "")
    contract_state = int(contract.get("state", -1))
    if contract_state != 0:
        raise PlanRejected(
            "CONTRACT_STATE_NOT_OPEN",
            details={"native_symbol": contract_symbol, "contract_state": contract_state},
        )
    if contract.get("apiAllowed") is not True:
        raise PlanRejected(
            "CONTRACT_API_DISABLED",
            details={"native_symbol": contract_symbol, "api_allowed": contract.get("apiAllowed")},
        )
    asset_class = str(decision.get("asset_class") or "crypto").lower()
    if int(contract.get("futureType", 0)) != 1 or str(contract.get("quoteCoin") or "").upper() != "USDT":
        raise PlanRejected("CONTRACT_NOT_USDT_PERPETUAL")
    if asset_class == "stock_futures":
        if not _looks_like_stock_futures(contract):
            raise PlanRejected("CONTRACT_NOT_STOCK_FUTURES")
    elif bool(contract.get("preMarket")) or int(contract.get("typeLabel") or 0) != 0:
        raise PlanRejected("CONTRACT_NOT_STANDARD_CRYPTO_PERPETUAL")

    asks = depth.get("asks") or []
    bids = depth.get("bids") or []
    if not asks or not bids:
        raise PlanRejected("ORDER_BOOK_UNAVAILABLE")
    ask = _f(asks[0][0])
    bid = _f(bids[0][0])
    if ask is None or bid is None or ask <= 0 or bid <= 0 or ask < bid:
        raise PlanRejected("ORDER_BOOK_INVALID")
    mid = (ask + bid) / 2.0
    spread_bps = (ask - bid) / mid * 10_000.0
    spread_cap_bps = (
        float(cfg.get("max_spread_bps_stock_futures", cfg.get("max_spread_bps", 15.0)))
        if asset_class == "stock_futures"
        else cfg.spread_limit_bps(str(decision.get("symbol") or contract.get("symbol") or ""))
    )
    if spread_bps > spread_cap_bps:
        raise PlanRejected(
            "SPREAD_TOO_WIDE",
            details={
                "best_bid": bid,
                "best_ask": ask,
                "spread_bps": round(spread_bps, 4),
                "spread_cap_bps": spread_cap_bps,
            },
        )

    # Legacy immutable long-only plans predate the explicit direction field.
    # Treating that missing field as long preserves their original scope; new
    # Paper decisions always freeze an explicit direction.
    direction = str(decision.get("direction") or "long").lower()
    if direction not in {"long", "short"}:
        raise PlanRejected("UNSUPPORTED_DIRECTION")
    reference = _f(decision.get("entry_price"))
    stop = _f(decision.get("original_stop"))
    tp1 = _f(decision.get("tp1"))
    tp2 = _f(decision.get("tp2"))
    tp3 = _f(decision.get("tp3"))
    valid_frozen_geometry = (
        stop < reference < tp1 < tp2 < tp3 if direction == "long"
        else tp3 < tp2 < tp1 < reference < stop
    ) if None not in (reference, stop, tp1, tp2, tp3) else False
    if not valid_frozen_geometry:
        raise PlanRejected("INVALID_FROZEN_GEOMETRY")
    entry_mode = str(decision.get("entry_mode") or "").upper()
    trade_mode = str(decision.get("mode") or "").lower()
    drift_bps = cfg.entry_limit("max_entry_drift_bps", entry_mode, 15.0, mode=trade_mode)
    adverse_limit = reference * (1.0 + drift_bps / 10_000.0) if direction == "long" else reference * (1.0 - drift_bps / 10_000.0)
    executable_price = ask if direction == "long" else bid
    if (direction == "long" and executable_price > adverse_limit) or (
        direction == "short" and executable_price < adverse_limit
    ):
        raise PlanRejected("ENTRY_DRIFT_TOO_LARGE")
    # A better MEXC quote must not turn a still-valid Paper setup into a reject.
    # The IOC remains capped at the adverse limit and sizing uses that worst
    # executable price, so a favourable fill can only reduce realized stop risk.
    # The frozen structural stop and its buffer remain authoritative.
    stop_buffer_modes = {
        str(value).upper()
        for value in (cfg.get("enforce_stop_buffer_entry_modes", [
            "PULLBACK_LIMIT", "STRUCTURAL_RETEST",
        ]) or [])
    }
    if entry_mode in stop_buffer_modes:
        min_live_stop_buffer = float(cfg.get("min_live_entry_to_stop_buffer_pct", 0.0035))
        too_close_to_stop = (
            executable_price <= stop * (1.0 + min_live_stop_buffer)
            if direction == "long"
            else executable_price >= stop * (1.0 - min_live_stop_buffer)
        )
        if too_close_to_stop:
            raise PlanRejected(
                "ENTRY_TOO_CLOSE_TO_FROZEN_STOP",
                details={
                    "reference_entry": reference,
                    "executable_price": executable_price,
                    "original_stop": stop,
                    "minimum_stop_buffer_pct": min_live_stop_buffer,
                    "entry_mode": entry_mode,
                },
            )
    tick = _f(contract.get("priceUnit"), 0.0) or 0.0
    # IOC is allowed to consume the book only up to the frozen drift cap. This
    # is more fill-reliable than posting exactly at a now-stale best ask while
    # still bounding worst-case slippage deterministically.
    limit_price = _round_step(adverse_limit, tick, "down" if direction == "long" else "up")
    # An IOC protection cap must never sit beyond the first reduce-only target.
    # Otherwise a valid current quote can be rejected solely because its worst
    # permitted fill would cross TP1. Keep one native tick between the cap and
    # TP1; if the current book is already there, the setup is genuinely stale.
    if direction == "long":
        limit_price = min(limit_price, _round_step(tp1 - tick, tick, "down"))
    else:
        limit_price = max(limit_price, _round_step(tp1 + tick, tick, "up"))
    if (direction == "long" and limit_price < ask) or (
        direction == "short" and limit_price > bid
    ):
        raise PlanRejected("ENTRY_TICK_EXCEEDS_DRIFT_CAP")
    if (direction == "long" and limit_price > adverse_limit + 1e-12) or (
        direction == "short" and limit_price < adverse_limit - 1e-12
    ):
        raise PlanRejected("ENTRY_TICK_EXCEEDS_DRIFT_CAP")

    stop = _round_step(stop, tick, "up" if direction == "long" else "down")
    tp_round = "down" if direction == "long" else "up"
    tp1 = _round_step(tp1, tick, tp_round)
    tp2 = _round_step(tp2, tick, tp_round)
    tp3 = _round_step(tp3, tick, tp_round)
    valid_native_geometry = (
        stop < limit_price < tp1 < tp2 < tp3 if direction == "long"
        else tp3 < tp2 < tp1 < limit_price < stop
    )
    if not valid_native_geometry:
        raise PlanRejected("MEXC_NATIVE_GEOMETRY_INVALID")

    stop_pct = abs(limit_price - stop) / limit_price
    min_stop_pct = cfg.stop_distance_limit(
        "min_stop_distance_pct", mode=trade_mode, default=0.0035)
    max_stop_pct = cfg.stop_distance_limit(
        "max_stop_distance_pct", mode=trade_mode, default=0.08)
    if stop_pct < min_stop_pct:
        raise PlanRejected("STOP_TOO_TIGHT")
    if stop_pct > max_stop_pct:
        raise PlanRejected("STOP_TOO_WIDE")

    # API fees take precedence over app/web promotional values. Use the worse
    # of current contract metadata and the official API fallback.
    maker_fee = max(_f(contract.get("makerFeeRate"), 0.0) or 0.0,
                    float(cfg.get("fallback_maker_fee_rate", 0.0006)))
    taker_fee = max(_f(contract.get("takerFeeRate"), 0.0) or 0.0,
                    float(cfg.get("fallback_taker_fee_rate", 0.0008)))
    slippage_rate = float(cfg.get("fallback_slippage_bps", 5.0)) / 10_000.0
    # Both selected modes are executed as capped IOC after Paper detects the
    # touch. This avoids a delayed second-touch fill that Paper never took.
    risk_rate = stop_pct + 2.0 * taker_fee + 2.0 * slippage_rate

    allocated = float(cfg.allocated_equity_usdt)
    equity_basis = allocated if exchange_equity_usdt is None else min(allocated, exchange_equity_usdt)
    risk_multiplier = _f(decision.get("live_risk_multiplier"), 1.0)
    if risk_multiplier is None or not (0.0 < risk_multiplier <= 1.0):
        raise PlanRejected("INVALID_LIVE_RISK_MULTIPLIER")
    risk_budget = cfg.risk_per_trade_usdt * risk_multiplier
    if risk_budget <= 0:
        raise PlanRejected("NO_RISK_BUDGET")
    raw_notional = risk_budget / risk_rate
    max_gross_notional = cfg.execution_limit(
        "max_gross_notional_usdt", decision, 500.0, allow_unlimited=True
    )
    if max_gross_notional is not None:
        raw_notional = min(raw_notional, max_gross_notional)

    contract_size = _f(contract.get("contractSize"))
    vol_step = _f(contract.get("volUnit"))
    min_vol = _f(contract.get("minVol"))
    max_vol = min(
        x for x in (_f(contract.get("maxVol"), float("inf")),
                    _f(contract.get("limitMaxVol"), float("inf"))) if x is not None
    )
    if not contract_size or not vol_step or min_vol is None:
        raise PlanRejected("CONTRACT_SIZE_METADATA_MISSING")
    raw_vol = raw_notional / (contract_size * limit_price)
    vol = _round_step(raw_vol, vol_step, "down")
    if vol < min_vol:
        raise PlanRejected("BELOW_MIN_CONTRACT_VOLUME")
    if vol > max_vol:
        vol = _round_step(max_vol, vol_step, "down")
    notional = vol * contract_size * limit_price
    stop_risk = stop_risk_components(
        entry_price=limit_price,
        stop_price=stop,
        volume_contracts=vol,
        contract_size=contract_size,
        taker_fee_rate=taker_fee,
        slippage_rate=slippage_rate,
    )
    actual_risk = stop_risk["net_stop_risk_usdt"]
    if actual_risk > risk_budget + 1e-8:
        raise PlanRejected("ROUNDED_RISK_EXCEEDS_BUDGET")

    mmr = _f(contract.get("maintenanceMarginRate"), 0.0) or 0.0
    liquidation_fee = _f(contract.get("liquidationFeeRate"), 0.0) or 0.0
    multiple = float(cfg.get("liquidation_buffer_to_stop", 3.0))
    extra = float(cfg.get("min_stop_to_liquidation_buffer_pct", 0.005))
    denom = multiple * stop_pct + extra + mmr + liquidation_fee
    max_safe_leverage = max(1, math.floor(1.0 / denom))
    country_max = int(_f(contract.get("countryConfigContractMaxLeverage"), 0) or 0)
    exchange_max = int(_f(contract.get("maxLeverage"), 1) or 1)
    if country_max > 0:
        exchange_max = min(exchange_max, country_max)
    configured_ceiling = _f(cfg.get("exchange_leverage_ceiling"))
    leverage_caps = [max_safe_leverage, exchange_max]
    if configured_ceiling is not None and configured_ceiling > 0:
        leverage_caps.append(int(configured_ceiling))
    leverage = min(leverage_caps)
    leverage = max(leverage, int(_f(contract.get("minLeverage"), 1) or 1))
    margin = notional / leverage
    max_total_margin = cfg.execution_limit(
        "max_total_margin_usdt", decision, 50.0, allow_unlimited=True
    )
    if max_total_margin is not None and margin > max_total_margin + 1e-9:
        raise PlanRejected("MARGIN_CAP_EXCEEDED")

    liq_distance_pct = max(0.0, 1.0 / leverage - mmr - liquidation_fee)
    estimated_liq = limit_price * (
        1.0 - liq_distance_pct if direction == "long" else 1.0 + liq_distance_pct
    )
    liq_multiple = abs(estimated_liq - limit_price) / max(abs(limit_price - stop), 1e-12)
    stop_to_liq = (
        (stop - estimated_liq) / limit_price if direction == "long"
        else (estimated_liq - stop) / limit_price
    )
    if liq_multiple + 1e-9 < multiple or stop_to_liq < extra - 1e-9:
        raise PlanRejected("LIQUIDATION_BUFFER_FAIL")

    decision_id = str(decision.get("decision_id") or "")
    external_oid = "cad_" + decision_id.replace("-", "")[:28]
    return OrderPlan(
        decision_id=decision_id,
        signal_id=str(decision.get("signal_id") or ""),
        symbol=str(contract.get("symbol") or ""),
        external_oid=external_oid,
        entry_mode=entry_mode,
        direction=direction,
        order_type=3,
        side=1 if direction == "long" else 3,
        open_type=1,
        position_mode=1,
        limit_price=limit_price,
        reference_entry=reference,
        current_ask=ask,
        current_bid=bid,
        spread_bps=round(spread_bps, 4),
        volume_contracts=vol,
        contract_size=contract_size,
        price_tick=tick,
        volume_step=vol_step,
        min_volume=min_vol,
        notional_usdt=round(notional, 8),
        original_stop=stop,
        tp1=tp1,
        tp2=tp2,
        tp3=tp3,
        stop_distance_pct=round(stop_pct, 8),
        risk_rate=round(risk_rate, 8),
        risk_budget_usdt=round(risk_budget, 8),
        actual_risk_usdt=round(actual_risk, 8),
        leverage=leverage,
        estimated_margin_usdt=round(margin, 8),
        estimated_liquidation_price=round(estimated_liq, 10),
        liquidation_distance_multiple=round(liq_multiple, 4),
        maker_fee_rate=maker_fee,
        taker_fee_rate=taker_fee,
        slippage_rate=slippage_rate,
        stop_contract=decision.get("stop_contract") if isinstance(decision.get("stop_contract"), dict) else None,
    )


def model_f_stop(*, entry: float, original_stop: float, highest_price: float | None = None,
                 favorable_price: float | None = None, direction: str = "long",
                 cfg: LiveCanaryConfig) -> tuple[str, float, float]:
    """Return Model F protection for a long or short using a favorable extreme."""
    direction = str(direction).lower()
    if direction not in {"long", "short"}:
        raise ValueError("unsupported direction")
    extreme = favorable_price if favorable_price is not None else highest_price
    if extreme is None:
        raise ValueError("favorable price is required")
    risk_per_unit = (entry - original_stop) if direction == "long" else (original_stop - entry)
    if risk_per_unit <= 0:
        raise ValueError("invalid directional geometry")
    mfe_r = max(0.0, (
        (extreme - entry) / risk_per_unit if direction == "long" else (entry - extreme) / risk_per_unit
    ))
    model = cfg.get("model_f", {}) or {}
    if mfe_r >= float(model.get("lock_profit_at_r", 1.0)):
        stop = entry + (1 if direction == "long" else -1) * float(model.get("lock_level_r", 0.5)) * risk_per_unit
        return "PROFIT_LOCK", stop, mfe_r
    if mfe_r >= float(model.get("arm_breakeven_at_r", 0.6)):
        return "BREAKEVEN", entry, mfe_r
    return "ORIGINAL_STOP", original_stop, mfe_r
