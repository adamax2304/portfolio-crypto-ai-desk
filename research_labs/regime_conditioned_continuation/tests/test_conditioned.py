from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from research_labs.regime_conditioned_continuation.src.common import load_config, parameter_grid
from research_labs.regime_conditioned_continuation.src.regime import conditioned_gate
from research_labs.regime_conditioned_continuation.src.run_backtest import (
    _chronological_trades,
    _folds,
    _load_frozen_variant,
)
from research_labs.technical_trend_reclaim.src.engine import Bundle


def _context(*, growth: float, aligned: bool = True, atr_ratio: float = 1.0) -> pd.DataFrame:
    count = 140
    opened = pd.date_range("2024-01-01", periods=count, freq="4h", tz="UTC")
    close = np.linspace(100.0, 100.0 * (1.0 + growth), count)
    fast = close * (0.99 if aligned else 0.96)
    slow = close * (0.98 if aligned else 1.02)
    atr_pct = np.full(count, 0.02)
    atr_pct[-1] *= atr_ratio
    return pd.DataFrame({
        "bar_open_at": opened,
        "bar_close_at": opened + pd.Timedelta(hours=4) - pd.Timedelta(milliseconds=1),
        "close": close,
        "ema_fast": fast,
        "ema_slow": slow,
        "ema_slope_atr": np.full(count, 0.20 if aligned else -0.20),
        "adx": np.full(count, 30.0),
        "atr": close * atr_pct,
    })


def _bundle(context: pd.DataFrame) -> Bundle:
    empty = pd.DataFrame()
    return Bundle("crypto", "ALT/USDT", empty, context, empty, "15m", "fixture", empty, empty)


def _variant(**updates: float) -> dict[str, float]:
    row: dict[str, float] = {
        "btc_adx_min": 15.0,
        "btc_slope_min_atr": 0.05,
        "rs_24h_min_pct": 0.0,
        "vol_ratio_min": 0.80,
    }
    row.update(updates)
    return row


def test_grid_is_exactly_pre_registered_sixteen() -> None:
    rows = parameter_grid()
    assert len(rows) == 16
    assert len({row["parameter_hash"] for row in rows}) == 16
    assert {row["btc_adx_min"] for row in rows} == {15.0, 22.0}
    assert {row["btc_slope_min_atr"] for row in rows} == {0.05, 0.15}
    assert {row["rs_24h_min_pct"] for row in rows} == {0.0, 2.0}
    assert {row["vol_ratio_min"] for row in rows} == {0.8, 1.1}


def test_v2_frequency_recovery_grid_is_frozen_at_sixteen() -> None:
    path = Path(__file__).resolve().parents[1] / "config" / "crypto_v2.yaml"
    rows = parameter_grid(load_config(path))
    assert len(rows) == 16
    assert len({row["parameter_hash"] for row in rows}) == 16
    assert {row["btc_adx_min"] for row in rows} == {10.0, 15.0}
    assert {row["btc_slope_min_atr"] for row in rows} == {0.05}
    assert {row["rs_24h_min_pct"] for row in rows} == {0.5, 1.0, 1.5, 2.0}
    assert {row["vol_ratio_min"] for row in rows} == {0.65, 0.8}


def test_aligned_relative_strength_and_normal_volatility_pass() -> None:
    cfg = load_config()["strategy"]
    symbol = _context(growth=0.30)
    btc = _context(growth=0.08)
    at = symbol.iloc[-1]["bar_close_at"]
    ok, reason, features = conditioned_gate(_bundle(symbol), btc, at, "long", _variant(), cfg)
    assert ok is True
    assert reason is None
    assert features["aligned"] is True
    assert features["directional_rs_24h"] > 0


def test_misaligned_btc_is_rejected() -> None:
    cfg = load_config()["strategy"]
    symbol = _context(growth=0.30)
    btc = _context(growth=0.08, aligned=False)
    ok, reason, _ = conditioned_gate(
        _bundle(symbol), btc, symbol.iloc[-1]["bar_close_at"], "long", _variant(), cfg
    )
    assert ok is False
    assert reason == "BTC_REGIME_NOT_ALIGNED"


def test_strict_relative_strength_threshold_rejects_weak_leadership() -> None:
    cfg = load_config()["strategy"]
    symbol = _context(growth=0.10)
    btc = _context(growth=0.08)
    ok, reason, _ = conditioned_gate(
        _bundle(symbol), btc, symbol.iloc[-1]["bar_close_at"], "long",
        _variant(rs_24h_min_pct=2.0), cfg,
    )
    assert ok is False
    assert reason == "RELATIVE_STRENGTH_BELOW"


def test_compressed_volatility_is_rejected() -> None:
    cfg = load_config()["strategy"]
    symbol = _context(growth=0.30, atr_ratio=0.40)
    btc = _context(growth=0.08)
    ok, reason, features = conditioned_gate(
        _bundle(symbol), btc, symbol.iloc[-1]["bar_close_at"], "long",
        _variant(vol_ratio_min=0.80), cfg,
    )
    assert ok is False
    assert reason == "VOLATILITY_COMPRESSED"
    assert features["vol_ratio"] < 0.80


def test_development_folds_are_contiguous_and_end_before_validation() -> None:
    cfg = load_config()
    start = pd.Timestamp("2023-08-07", tz="UTC")
    end = pd.Timestamp("2026-08-06", tz="UTC")
    folds = _folds(start, end, "development", cfg)
    assert len(folds) == 4
    assert all(left.end == right.start for left, right in zip(folds, folds[1:]))
    assert folds[-1].end == pd.Timestamp(cfg["experiment"]["development_end"])
    validation = _folds(start, end, "validation", cfg)
    assert validation[0].start == folds[-1].end
    assert validation[0].end == pd.Timestamp(cfg["experiment"]["validation_end"])


def test_validation_requires_a_valid_frozen_profile(tmp_path: Path) -> None:
    missing = tmp_path / "missing.json"
    with pytest.raises(RuntimeError, match="requires the profile frozen"):
        _load_frozen_variant(missing)
    malformed = tmp_path / "bad.json"
    malformed.write_text(json.dumps({"variant": {}, "next_stage": "historical_validation_only"}))
    with pytest.raises(RuntimeError, match="valid variant"):
        _load_frozen_variant(malformed)


def test_isolated_package_does_not_reference_production_write_tables() -> None:
    src = Path(__file__).resolve().parents[1] / "src"
    text = "\n".join(path.read_text(encoding="utf-8") for path in src.glob("*.py"))
    for forbidden in ("proposed_signals", "signal_outcomes", "final_r", "paper_portfolio_ledger"):
        assert forbidden not in text


def test_drawdown_input_is_ordered_by_actual_exit_not_worker_arrival() -> None:
    rows = [
        {"trade_id": "late", "entry_at": "2024-01-03", "exit_at": "2024-01-04"},
        {"trade_id": "early", "entry_at": "2024-01-01", "exit_at": "2024-01-02"},
    ]
    assert [row["trade_id"] for row in _chronological_trades(rows)] == ["early", "late"]
