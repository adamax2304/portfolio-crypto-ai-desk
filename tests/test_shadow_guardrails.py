"""Guardrails (item 9) — the shadow/read-model/diagnostics lane must never write execution state,
never place orders, and never auto-promote. Source-level + behavioural assertions. No network/live."""
from __future__ import annotations

import inspect
from pathlib import Path

import src.execution.paper_shadow_engine as eng
import src.execution.paper_shadow_monitor as mon
import src.signals.latency_readmodel as lr
import src.signals.catalyst_linkage_shadow_audit as cat


def _src(mod) -> str:
    return Path(mod.__file__).read_text(encoding="utf-8").lower()


def test_no_write_to_signal_outcomes_or_final_r():
    # the shadow lane writes ONLY its own tables — never mutates authoritative execution state.
    for mod in (eng, mon, lr):
        s = _src(mod)
        for bad in ("final_r =", "set final_r", "update signal_outcomes",
                    "insert into signal_outcomes", "update proposed_signals",
                    "insert into proposed_signals"):
            assert bad not in s, f"{mod.__name__} must not write execution state: {bad!r}"


def test_no_exchange_order_or_live_code():
    for mod in (eng, mon, lr, cat):
        s = _src(mod)
        for bad in ("create_order", "place_order", "cancel_order", "ccxt", "api_secret",
                    "/order", "private_post", "manual_live", "auto_live"):
            assert bad not in s, f"{mod.__name__} must contain no order/live code: {bad!r}"


def test_readiness_is_evaluation_only_never_bare_ready():
    src = inspect.getsource(mon.promotion_readiness_by_mode).lower()
    assert '"executed": false' in src                     # returns executed=False
    assert "ready_for_operator_review" in src             # operator-review framing, not bare READY
    # a bare "READY" verdict (auto-promotion wording) must never be produced
    assert '"ready"' not in src.replace("ready_for_operator_review", "")


def test_catalyst_advisory_declares_no_scoring_or_actionability_change():
    adv = cat.stocks_catalyst_advisory.__doc__ or ""
    assert "never changes scoring" in adv.lower() or "read-only advisory" in adv.lower()


def test_fee_profile_selection_is_cost_model_only():
    # selecting a fee profile is a cost-model choice — it must not depend on direction/entry/tp/sl.
    sig = inspect.signature(eng.select_fee_profile)
    assert set(sig.parameters) <= {"asset_class", "crypto_default"}
