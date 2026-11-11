"""Tests for the stocks config loader. No network."""

from __future__ import annotations

from src.stocks import load_stocks_config


def test_loader_reads_default_universe():
    cfg = load_stocks_config()
    assert cfg.enabled is True
    assert "NVDA" in cfg.default_symbols
    assert "SPY" in cfg.default_symbols
    assert "SPY" in cfg.indices
    assert "QQQ" in cfg.indices


def test_sector_map_resolves():
    cfg = load_stocks_config()
    assert cfg.sector_for("NVDA") == "semiconductors"
    assert cfg.sector_etf_for("NVDA") == "SMH"
    assert cfg.sector_for("AAPL") == "technology"
    assert cfg.sector_etf_for("AAPL") == "XLK"
    # Unmapped symbol returns empty strings rather than raising.
    assert cfg.sector_for("UNKNOWN") == ""
    assert cfg.sector_etf_for("UNKNOWN") == ""


def test_mode_timeframes_per_mode():
    cfg = load_stocks_config()
    assert cfg.timeframes_for("intraday") == ["15m", "1h", "1d"]
    assert cfg.timeframes_for("swing") == ["1h", "1d"]
    assert cfg.timeframes_for("invest") == ["1d", "1wk"]
    # Unknown mode falls back to 1d
    assert cfg.timeframes_for("nonexistent") == ["1d"]


def test_scoring_weights_and_multipliers():
    cfg = load_stocks_config()
    # Base weights exist
    assert cfg.weight("technical_setup") == 20.0
    assert cfg.weight("market_regime_alignment") == 15.0
    # Mode multipliers default to 1.0 when missing
    assert cfg.mode_multiplier("intraday", "technical_setup") == 1.10
    assert cfg.mode_multiplier("intraday", "no_such_component") == 1.0
    # Regime multipliers also default to 1.0
    assert cfg.regime_multiplier("risk_off", "relative_strength") == 1.15
    assert cfg.regime_multiplier("nonexistent", "anything") == 1.0


def test_tier_thresholds():
    cfg = load_stocks_config()
    assert cfg.tier_threshold("A", 80.0) == 80.0
    assert cfg.tier_threshold("B", 65.0) == 65.0
    assert cfg.tier_threshold("C", 50.0) == 50.0


def test_risk_rules():
    cfg = load_stocks_config()
    intraday_rule = cfg.earnings_rule("intraday")
    assert intraday_rule.get("require_explicit_acknowledgement") is True
    swing_rule = cfg.earnings_rule("swing")
    assert swing_rule.get("block_if_days_ahead_le") == 2
    # Regime rule lookup
    risk_off_rule = cfg.regime_rule("risk_off")
    assert risk_off_rule.get("long_requires_exceptional_rs") is True
    # Liquidity rules
    assert cfg.liquidity_rules.get("min_price") == 5.0
