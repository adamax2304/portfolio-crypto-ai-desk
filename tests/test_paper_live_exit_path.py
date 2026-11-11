from src.execution.paper_live_exit_path import simulate_live_exit_path


def _bar(ts, low, high):
    return {"timestamp": ts, "open": 100.0, "high": high, "low": low, "close": 100.0}


def test_breakeven_arms_for_next_bar_and_closes_on_retest():
    result = simulate_live_exit_path(
        direction="long", entry=100, stop=90, tp1=110, tp2=120, tp3=130,
        candles=[_bar("t1", 99, 107), _bar("t2", 99, 104)],
    )
    assert result["terminal"] is True
    assert result["paper_execution_r"] == 0.0
    assert result["close_reason"] == "breakeven_stop"


def test_partial_tp_then_profit_lock_stop_uses_remaining_size():
    result = simulate_live_exit_path(
        direction="long", entry=100, stop=90, tp1=110, tp2=120, tp3=130,
        candles=[_bar("t1", 99, 111), _bar("t2", 104, 108)],
    )
    # 33% at +1R, remaining 67% at +0.5R.
    assert result["paper_execution_r"] == 0.665
    assert result["close_reason"] == "profit_lock_stop"


def test_three_targets_use_weighted_live_scale_out_not_full_tp3_r():
    result = simulate_live_exit_path(
        direction="long", entry=100, stop=90, tp1=110, tp2=120, tp3=130,
        candles=[_bar("t1", 99, 131)],
    )
    assert result["paper_execution_r"] == 2.01
    assert result["close_reason"] == "three_leg_tp3"


def test_same_bar_active_stop_and_target_is_stop_first():
    result = simulate_live_exit_path(
        direction="short", entry=100, stop=110, tp1=90, tp2=80, tp3=70,
        candles=[_bar("t1", 93, 101), _bar("t2", 89, 101)],
    )
    assert result["paper_execution_r"] == 0.0
    assert result["same_candle_ambiguous"] is True


def test_incremental_batches_match_single_pass_without_reprocessing():
    first_bar = _bar("2026-09-27T10:01:00+00:00", 99, 111)
    second_bar = _bar("2026-09-27T10:02:00+00:00", 104, 108)
    first = simulate_live_exit_path(
        direction="long", entry=100, stop=90, tp1=110, tp2=120, tp3=130,
        candles=[first_bar], path_start_at="2026-09-27T10:00:00+00:00",
    )
    assert first["terminal"] is False
    assert first["path_tp1_filled"] is True
    assert first["path_realized_r"] == 0.33

    incremental = simulate_live_exit_path(
        direction="long", entry=100, stop=90, tp1=110, tp2=120, tp3=130,
        # The rolling frame may still contain the prior candle. Persisted state
        # must cause it to be ignored instead of crediting TP1 twice.
        candles=[first_bar, second_bar], initial_state=first,
        path_start_at="2026-09-27T10:00:00+00:00",
    )
    single_pass = simulate_live_exit_path(
        direction="long", entry=100, stop=90, tp1=110, tp2=120, tp3=130,
        candles=[first_bar, second_bar], path_start_at="2026-09-27T10:00:00+00:00",
    )
    assert incremental["paper_execution_r"] == single_pass["paper_execution_r"] == 0.665
    assert incremental["path_remaining_fraction"] == 0.0


def test_candle_gap_is_quarantined_before_later_price_path_is_used():
    result = simulate_live_exit_path(
        direction="long", entry=100, stop=90, tp1=110, tp2=120, tp3=130,
        candles=[
            _bar("2026-09-27T10:01:00+00:00", 99, 105),
            _bar("2026-09-27T10:10:00+00:00", 89, 131),
        ],
        path_start_at="2026-09-27T10:00:00+00:00",
    )
    assert result["terminal"] is False
    assert result["path_data_quality"] == "gap"
    assert result["path_gap_seconds"] == 540.0
    assert result["path_last_candle_at"] == "2026-09-27T10:01:00+00:00"
    assert result["paper_execution_r"] is None
