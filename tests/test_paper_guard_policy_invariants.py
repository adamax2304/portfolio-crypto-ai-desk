from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

from src.notifiers.paper_entry import entry_freshness, is_shadow_only_scalp


ROOT = Path(__file__).resolve().parents[1]


def _yaml(relative: str):
    return yaml.safe_load((ROOT / relative).read_text(encoding="utf-8"))


def test_proven_paper_guards_remain_enabled_and_live_locked():
    cqo = _yaml("config/crypto_quality_overlay.yaml")["crypto_quality_overlay"]
    features = _yaml("config/paper_features.yaml")
    session = _yaml("config/session_risk.yaml")

    assert cqo["enabled"] is True
    assert cqo["paper_actionability_enabled"] is True
    assert cqo["live_enabled"] is False
    assert cqo["modes"]["scalp"]["disabled"] is True
    assert features["paper_risk_authority"]["enabled"] is True
    assert features["paper_risk_authority"]["live_enabled"] is False
    assert features["features"]["circuit_breaker_block"]["state"] == "active_paper_accounting"
    assert session["disabled_modes"]["crypto"] == ["scalp"]
    # Asia is diagnostic/sizing context. Scalp remains disabled globally,
    # while intraday is routed by the calibrated quality overlay rather than
    # being killed a second time by the session guard.
    assert session["asia_dead_zone"]["blocked_modes"] == []
    assert session["asia_dead_zone"]["allowed_mode_risk_multiplier"] == 1.0


def test_scalp_and_disabled_entry_modes_stay_out_of_paper():
    policy = _yaml("config/paper_entry_mode_policy.yaml")
    disabled = {(row["asset_class"], row["mode"]): set(row["entry_modes"])
                for row in policy["disabled_shadow"]}

    assert is_shadow_only_scalp({"asset_class": "crypto", "mode": "scalp"}) is True
    assert disabled[("crypto", "scalp")] == {"*"}
    assert {"PULLBACK_LIMIT", "LIMIT_THEN_TAKER_TIMEOUT"}.issubset(disabled[("crypto", "*")])
    assert {"MOMENTUM_TAKER_NOW", "LIMIT_THEN_TAKER_TIMEOUT"}.issubset(
        disabled[("stocks", "intraday")])


def test_latency_change_does_not_relax_entry_freshness_cutoffs():
    now = datetime(2026, 7, 14, 15, 0, tzinfo=timezone.utc)
    crypto_15m = (now - timedelta(minutes=15)).isoformat()
    crypto_16m = (now - timedelta(minutes=16)).isoformat()
    stocks_45m = (now - timedelta(minutes=45)).isoformat()
    stocks_46m = (now - timedelta(minutes=46)).isoformat()

    assert entry_freshness(crypto_15m, now=now, asset_class="crypto", mode="intraday")[2] is True
    assert entry_freshness(crypto_16m, now=now, asset_class="crypto", mode="intraday")[2] is False
    assert entry_freshness(stocks_45m, now=now, asset_class="stocks", mode="intraday")[2] is True
    assert entry_freshness(stocks_46m, now=now, asset_class="stocks", mode="intraday")[2] is False
