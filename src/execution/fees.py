"""Fee / slippage / funding accounting for paper trades (PAPER ONLY).

Configurable per-exchange/account/VIP/symbol/order-type fee profiles
(config/fee_profiles.yaml). Open fee uses the ENTRY notional + entry order type;
close fee uses the EXIT notional + exit order type. If the exit price is unknown
the close fee is estimated from the entry notional and flagged `fee_estimated`.
Never a universal hardcoded rate. No live, no orders.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None

_ROOT = Path(__file__).resolve().parents[2]
_DEFAULT_FEE_PROFILE = {"maker_fee_rate": 0.0002, "taker_fee_rate": 0.00055,
                        "source_note": "built-in fallback (bybit non-VIP)"}


def load_fee_profiles() -> dict[str, Any]:
    path = _ROOT / "config" / "fee_profiles.yaml"
    if yaml and path.exists():
        try:
            with open(path, "r", encoding="utf-8") as fh:
                return yaml.safe_load(fh) or {}
        except Exception:
            pass
    return {"fee_profiles": {"bybit_non_vip_usdt_perp": _DEFAULT_FEE_PROFILE},
            "fee_profile_aliases": {"bybit_default_futures": "bybit_non_vip_usdt_perp"}}


def _resolve_profile(profile: str, cfg: dict) -> tuple[str, dict]:
    """Resolve aliases → (canonical_name, profile_dict)."""
    aliases = cfg.get("fee_profile_aliases") or {}
    name = aliases.get(profile, profile)
    prof = (cfg.get("fee_profiles") or {}).get(name)
    if prof is None:
        name, prof = "bybit_non_vip_usdt_perp", _DEFAULT_FEE_PROFILE
    return name, prof


def fee_rate(profile: str = "bybit_non_vip_usdt_perp", order_type: str = "taker",
             profiles: dict | None = None) -> float:
    cfg = profiles or load_fee_profiles()
    _, prof = _resolve_profile(profile, cfg)
    key = "maker_fee_rate" if str(order_type).lower() == "maker" else "taker_fee_rate"
    return float(prof.get(key, _DEFAULT_FEE_PROFILE["taker_fee_rate"]))


def slippage_rate(symbol: str, slip_cfg: dict | None = None, majors: list | None = None) -> tuple[float, bool]:
    slip_cfg = slip_cfg or {"major": 0.0002, "liquid_alt": 0.0005, "illiquid_alt": 0.0010}
    base = str(symbol or "").split("/")[0].upper()
    majors = [m.upper() for m in (majors or ["BTC", "ETH", "SOL", "BNB", "XRP"])]
    if base in majors:
        return float(slip_cfg.get("major", 0.0002)), True
    return float(slip_cfg.get("liquid_alt", 0.0005)), False


@dataclass
class CostResult:
    entry_notional_usdt: float
    exit_notional_usdt: float
    entry_fee_rate: float
    exit_fee_rate: float
    open_fee_usdt: float
    close_fee_usdt: float
    fee_usdt: float
    slippage_usdt: float
    funding_usdt: float
    funding_known: bool
    fee_estimated: bool
    fee_profile: str
    fee_source: str
    total_cost_usdt: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def trade_costs(
    *,
    notional_usdt: float,                 # ENTRY notional (qty × entry_price)
    exit_notional_usdt: float | None = None,  # qty × exit_price; None → estimate from entry
    symbol: str = "",
    fee_profile: str = "bybit_non_vip_usdt_perp",
    entry_order_type: str = "taker",
    exit_order_type: str = "taker",
    slip_cfg: dict | None = None,
    majors: list | None = None,
    funding_usdt: float | None = None,
    exit_slices: list | None = None,          # PART 4: [(fraction, order_type), ...] for the exit
) -> CostResult:
    cfg = load_fee_profiles()
    name, prof = _resolve_profile(fee_profile, cfg)
    er = fee_rate(fee_profile, entry_order_type, cfg)
    xr = fee_rate(fee_profile, exit_order_type, cfg)
    estimated = exit_notional_usdt is None
    exit_notional = float(notional_usdt) if estimated else float(exit_notional_usdt)
    open_fee = float(notional_usdt) * er
    if exit_slices:
        # PART 4: slice-aware exit — each slice (TP partial = maker, stop/expiry remainder = taker)
        # pays its own rate on its share of the exit notional. Blended, not single taker on the whole.
        close_fee = sum(exit_notional * float(frac) * fee_rate(fee_profile, otype, cfg)
                        for frac, otype in exit_slices)
        xr = (close_fee / exit_notional) if exit_notional else xr   # report the blended rate
    else:
        close_fee = exit_notional * xr        # FIX: close fee on EXIT notional
    slip_r, _known = slippage_rate(symbol, slip_cfg, majors)
    slippage = (float(notional_usdt) + exit_notional) * slip_r   # per-side on each notional
    fund = float(funding_usdt) if funding_usdt is not None else 0.0
    total = open_fee + close_fee + slippage + fund
    return CostResult(
        entry_notional_usdt=round(float(notional_usdt), 4), exit_notional_usdt=round(exit_notional, 4),
        entry_fee_rate=er, exit_fee_rate=xr,
        open_fee_usdt=round(open_fee, 6), close_fee_usdt=round(close_fee, 6),
        fee_usdt=round(open_fee + close_fee, 6), slippage_usdt=round(slippage, 6),
        funding_usdt=round(fund, 6), funding_known=(funding_usdt is not None),
        fee_estimated=estimated, fee_profile=name,
        fee_source=str(prof.get("source_note") or prof.get("source_url") or ""),
        total_cost_usdt=round(total, 6),
    )


def net_pnl_usdt(gross_pnl_usdt: float, cost: CostResult) -> float:
    return round(gross_pnl_usdt - cost.total_cost_usdt, 6)
