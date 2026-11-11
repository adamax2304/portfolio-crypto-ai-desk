"""Paper-only stock entry provenance policy.

The free yfinance path labels a freshly revalidated quote as
``provider_delayed_current_bar``.  That is not live-grade market data, but it
can be accepted for forward Paper accounting when the operator explicitly
enables the delayed-data cohort in the stocks risk config.
"""

from __future__ import annotations

from typing import Any


POINT_IN_TIME_CURRENT_BAR = "point_in_time_current_bar"
PROVIDER_DELAYED_CURRENT_BAR = "provider_delayed_current_bar"


def _accept_delayed_provider(risk: dict[str, Any] | None = None) -> bool:
    if risk is None:
        try:
            from src.stocks import load_stocks_config

            risk = load_stocks_config().risk
        except Exception:
            return False
    guards = (risk or {}).get("intraday_guards") or {}
    provenance = guards.get("paper_entry_provenance") or {}
    return bool(provenance.get("accept_provider_delayed_current_bar", False))


def accepted_stock_intraday_paper_bases(
    risk: dict[str, Any] | None = None,
) -> frozenset[str]:
    bases = {POINT_IN_TIME_CURRENT_BAR}
    if _accept_delayed_provider(risk):
        bases.add(PROVIDER_DELAYED_CURRENT_BAR)
    return frozenset(bases)


def is_accepted_stock_intraday_paper_basis(
    basis: str | None, risk: dict[str, Any] | None = None,
) -> bool:
    return str(basis or "") in accepted_stock_intraday_paper_bases(risk)


def paper_provenance_rank(
    basis: str | None, *, stocks_intraday: bool,
    risk: dict[str, Any] | None = None,
) -> int:
    """Rank observations for replacing cached provenance.

    Live-grade point-in-time data always wins.  An enabled delayed-provider
    observation may replace a historical reconstruction, but never a genuine
    point-in-time observation.
    """
    value = str(basis or "")
    if value == POINT_IN_TIME_CURRENT_BAR:
        return 2
    if (stocks_intraday and value == PROVIDER_DELAYED_CURRENT_BAR
            and _accept_delayed_provider(risk)):
        return 1
    return 0


__all__ = [
    "POINT_IN_TIME_CURRENT_BAR",
    "PROVIDER_DELAYED_CURRENT_BAR",
    "accepted_stock_intraday_paper_bases",
    "is_accepted_stock_intraday_paper_basis",
    "paper_provenance_rank",
]
