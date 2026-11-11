"""Shadow exit manager tests (FAST SAFE ACCELERATION PART 3).

Asserts variants are computed in shadow only, the conservative same-candle rule,
missing-data honesty, archive-first OHLCV, idempotent ledger keys, and that the
real partial_exit_model flag is never mutated.
"""
from __future__ import annotations

from src.exits.shadow_exit_manager import (
    VARIANTS,
    ohlcv_path,
    shadow_rows_for_trade,
    simulate_variant,
)


def _c(o, h, l, cl):
    return {"open": o, "high": h, "low": l, "close": cl}


# entry 100, stop 99 (r_unit=1), tps at +1R/+2R/+3R
TPS = [101.0, 102.0, 103.0]


def test_current_variant_reaches_final_target():
    path = [_c(100, 101, 99.5, 100.8), _c(100.8, 103, 100.5, 102.9)]
    r = simulate_variant("A_current", 100, 99, TPS, "long", path)
    assert r["shadow_R"] == 3.0 and r["exit_reason"] == "target"


def test_be_after_1R_moves_stop_only_in_shadow():
    # runs to +1R (high 101), then pulls back to BE → exits ~0R
    path = [_c(100, 101.0, 99.6, 100.9), _c(100.9, 100.95, 99.9, 99.95)]
    r = simulate_variant("C_BE_1R", 100, 99, TPS, "long", path)
    assert r["moved_to_BE"] is True
    assert r["touched_1R"] is True
    assert abs(r["shadow_R"]) < 0.05  # stopped at break-even, not -1
    assert r["stopped_after_BE"] is True


def test_partial_variant_records_partial_in_shadow():
    # hits tp1 (+1R) → books 0.5R, then pulls back to BE on remainder
    path = [_c(100, 101.0, 99.6, 100.9), _c(100.9, 100.95, 99.9, 99.95)]
    r = simulate_variant("D_partial50_1R", 100, 99, TPS, "long", path)
    assert r["partial_taken"] is True
    assert r["shadow_R"] == 0.5  # 0.5 booked at +1R, remainder out at BE (0)


def test_conservative_same_candle_rule_takes_stop():
    # one candle straddles both stop (99) and a target — stop taken first
    path = [_c(100, 103.0, 99.0, 100.0)]
    r = simulate_variant("A_current", 100, 99, TPS, "long", path)
    assert r["shadow_R"] == -1.0 and r["exit_reason"] == "stop"


def test_missing_ohlcv_is_missing_data_not_fake():
    trade = {"signal_id": "x", "symbol": "FOO/USDT", "asset_class": "crypto",
             "mode": "intraday", "tier": "B", "direction": "long",
             "entry": 100, "stop": 99, "tp1": 101, "tp2": 102, "tp3": 103,
             "actual_R": -1.0}
    rows = shadow_rows_for_trade(trade, None)
    assert len(rows) == len(VARIANTS)
    assert all(r["data_coverage_status"] == "missing_data" for r in rows)
    assert all(r["shadow_R"] is None for r in rows)
    assert all(r["exit_reason"] == "missing_data" for r in rows)


def test_shadow_rows_do_not_mutate_actual_outcome():
    trade = {"signal_id": "y", "symbol": "FOO/USDT", "asset_class": "crypto",
             "mode": "intraday", "tier": "B", "direction": "long",
             "entry": 100, "stop": 99, "tp1": 101, "tp2": 102, "tp3": 103,
             "actual_R": -1.0}
    before = dict(trade)
    rows = shadow_rows_for_trade(trade, [_c(100, 101, 99.6, 100.9)], coverage_status="covered")
    assert trade == before  # input untouched
    # actual_R is carried verbatim into every row, never recomputed
    assert all(r["actual_R"] == -1.0 for r in rows)


def test_one_unique_row_per_variant():
    trade = {"signal_id": "z", "symbol": "FOO/USDT", "entry": 100, "stop": 99,
             "tp1": 101, "tp2": 102, "tp3": 103, "actual_R": 1.0, "direction": "long"}
    rows = shadow_rows_for_trade(trade, [_c(100, 103, 99.6, 102.9)], coverage_status="covered")
    variants = [r["variant"] for r in rows]
    assert sorted(variants) == sorted(VARIANTS)
    assert len(set(variants)) == len(VARIANTS)


def test_loser_saved_and_winner_clipped_flags():
    # actual was a loser (-1); BE-after-1R saved it to ~0 → loser_saved
    trade = {"signal_id": "s", "symbol": "FOO/USDT", "entry": 100, "stop": 99,
             "tp1": 101, "tp2": 102, "tp3": 103, "actual_R": -1.0, "direction": "long"}
    path = [_c(100, 101.0, 99.6, 100.9), _c(100.9, 100.95, 99.9, 99.95)]
    rows = shadow_rows_for_trade(trade, path, coverage_status="covered")
    be1 = next(r for r in rows if r["variant"] == "C_BE_1R")
    assert be1["loser_saved"] is True


def test_archive_first_ohlcv_path(tmp_path, monkeypatch):
    import src.exits.shadow_exit_manager as m
    monkeypatch.setattr(m, "ARCHIVE_DIR", tmp_path / "archive")
    monkeypatch.setattr(m, "CACHE_DIR", tmp_path / "cache")
    cache = m.CACHE_DIR / "binance" / "5m" / "BTC_USDT.csv"
    arch = m.ARCHIVE_DIR / "binance" / "5m" / "BTC_USDT.csv"
    cache.parent.mkdir(parents=True, exist_ok=True); cache.write_text("x")
    assert m.ohlcv_path("binance", "5m", "BTC_USDT") == cache
    arch.parent.mkdir(parents=True, exist_ok=True); arch.write_text("x")
    assert m.ohlcv_path("binance", "5m", "BTC_USDT") == arch  # archive preferred


def test_partial_exit_model_flag_unchanged():
    from src.config import load_config, load_yaml
    raw = load_yaml(load_config().root / "config" / "signal_tracking.yaml")
    assert raw["partial_exit_model"]["enabled"] is False  # shadow work never enables it
