from src.live_execution.routing_registry import load_registry, route, route_enabled
from src.live_execution.crypto_invest_bridge import load_crypto_invest_live_config
from src.live_execution.crypto_liquidity_sweep_bridge import load_liquidity_sweep_live_config


def test_live_registry_has_one_explicit_state_per_supported_route():
    registry = load_registry()
    assert set(registry["routes"]) == {
        "crypto_swing_breakout",
        "crypto_swing_limit_then_taker",
        "crypto_swing_pullback",
        "crypto_intraday_level_hold_v2",
        "crypto_intraday_breakout",
        "crypto_intraday_pullback",
        "stocks_intraday_breakout",
        "crypto_liquidity_sweep",
        "crypto_invest",
    }
    assert route_enabled(mode="swing", entry_mode="BREAKOUT_CONTINUATION") is False
    assert route_enabled(mode="swing", entry_mode="LIMIT_THEN_TAKER_TIMEOUT") is False
    assert route_enabled(mode="swing", entry_mode="PULLBACK_LIMIT") is False
    assert route_enabled(mode="intraday", entry_mode="LEVEL_HOLD_V2") is False
    assert route_enabled(mode="intraday", entry_mode="BREAKOUT_CONTINUATION") is False
    assert route_enabled(mode="intraday", entry_mode="PULLBACK_LIMIT") is False
    assert route_enabled(
        mode="stock_intraday", entry_mode="BREAKOUT_CONTINUATION", asset_class="stocks"
    ) is False
    assert route_enabled(mode="invest", entry_mode="REGIME_RECLAIM") is False
    assert route_enabled(mode="liquidity_sweep", entry_mode="LIQUIDITY_SWEEP") is False
    assert route(mode="invest", entry_mode="REGIME_RECLAIM")["risk_usdt"] == 5.0
    assert route(mode="swing", entry_mode="LIMIT_THEN_TAKER_TIMEOUT")["risk_usdt"] == 5.0
    assert route(mode="intraday", entry_mode="LEVEL_HOLD_V2")["risk_usdt"] == 5.0
    assert route(mode="intraday", entry_mode="LEVEL_HOLD_V2")["evidence_state"] == (
        "disabled_live_compatible_pf_negative"
    )
    assert route(mode="intraday", entry_mode="BREAKOUT_CONTINUATION")["risk_usdt"] == 5.0
    assert route(mode="intraday", entry_mode="PULLBACK_LIMIT")["risk_usdt"] == 5.0
    assert route(mode="swing", entry_mode="BREAKOUT_CONTINUATION")["evidence_state"] == (
        "paper_only_pending_live_loser_research"
    )
    sweep_route = route(mode="liquidity_sweep", entry_mode="LIQUIDITY_SWEEP")
    assert sweep_route["enabled"] is False
    assert sweep_route["risk_usdt"] == 2.5
    assert sweep_route["evidence_state"] == "archived_negative_live_and_shadow_pf_2026_09_30"


def test_independent_live_routes_are_explicitly_pinned_or_disabled():
    invest = load_crypto_invest_live_config()
    sweep = load_liquidity_sweep_live_config()
    assert invest["enabled"] is False and invest["risk_multiplier"] == 0.5
    assert sweep["enabled"] is False and sweep["risk_multiplier"] == 0.25
    assert sweep["allowed_directions"] == ["long"]
    assert "risk_off" in sweep["market_regime_filter"]["blocked_regimes"]
    # Archived routes preserve their last sizing metadata for audit only.
    assert invest["fixed_risk_usdt"] == sweep["fixed_risk_usdt"] == 10.0
