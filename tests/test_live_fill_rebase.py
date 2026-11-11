from __future__ import annotations

import pytest

from src.live_execution.sizing import rebase_filled_plan, stop_risk_components


def _plan(direction: str = "long") -> dict:
    if direction == "long":
        stop, targets = 98.0, (102.0, 104.0, 106.0)
    else:
        stop, targets = 102.0, (98.0, 96.0, 94.0)
    return {
        "direction": direction,
        "limit_price": 100.0,
        "original_stop": stop,
        "tp1": targets[0],
        "tp2": targets[1],
        "tp3": targets[2],
        "volume_contracts": 4.0,
        "contract_size": 1.0,
        "price_tick": 0.01,
        "actual_risk_usdt": 8.2,
        "risk_budget_usdt": 10.0,
        "taker_fee_rate": 0.0005,
        "slippage_rate": 0.0005,
        "partial_tp_legs": [
            {"leg": 1, "target": targets[0], "volume_contracts": 1.0},
            {"leg": 2, "target": targets[1], "volume_contracts": 1.0},
            {"leg": 3, "target": targets[2], "volume_contracts": 2.0},
        ],
    }


@pytest.mark.parametrize(("direction", "fill"), [("long", 99.5), ("short", 100.5)])
def test_fill_rebase_preserves_direction_and_caps_reserved_risk(direction: str, fill: float):
    rebased = rebase_filled_plan(_plan(direction), fill_price=fill)
    if direction == "long":
        assert rebased["original_stop"] < fill < rebased["tp1"] < rebased["tp2"] < rebased["tp3"]
    else:
        assert rebased["tp3"] < rebased["tp2"] < rebased["tp1"] < fill < rebased["original_stop"]
    risk = stop_risk_components(
        entry_price=fill,
        stop_price=rebased["original_stop"],
        volume_contracts=rebased["volume_contracts"],
        contract_size=rebased["contract_size"],
        taker_fee_rate=rebased["taker_fee_rate"],
        slippage_rate=rebased["slippage_rate"],
    )
    assert risk["net_stop_risk_usdt"] <= _plan(direction)["actual_risk_usdt"] + 0.02
    assert [leg["target"] for leg in rebased["partial_tp_legs"]] == [
        rebased["tp1"], rebased["tp2"], rebased["tp3"]
    ]


def test_fill_rebase_preserves_original_r_ladder():
    rebased = rebase_filled_plan(_plan("long"), fill_price=99.5)
    risk = 99.5 - rebased["original_stop"]
    actual = [(rebased[key] - 99.5) / risk for key in ("tp1", "tp2", "tp3")]
    assert actual == pytest.approx([1.0, 2.0, 3.0], abs=0.02)
