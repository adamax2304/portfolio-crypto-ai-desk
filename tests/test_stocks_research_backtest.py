from __future__ import annotations

import sqlite3
from datetime import datetime, timedelta, timezone

import pandas as pd

from src.backtest import stocks_research as research


UTC = timezone.utc


def _row(at: datetime, pnl: float) -> dict:
    return {
        "decision_at": at.isoformat(), "eligibility_status": "eligible", "outcome_status": "closed",
        "is_clean_for_edge": 1, "net_pnl_usd": pnl,
    }


def test_metrics_calculates_net_pf_and_drawdown():
    result = research.metrics([_row(datetime(2026, 1, 1, tzinfo=UTC), 3.0),
                               _row(datetime(2026, 1, 2, tzinfo=UTC), -1.0),
                               _row(datetime(2026, 1, 3, tzinfo=UTC), 2.0)])
    assert result == {
        "closed": 3, "net_pnl_usd": 4.0, "profit_factor": 5.0,
        "winrate": 0.6667, "max_drawdown_usd": 1.0,
    }


def test_walk_forward_selects_only_from_prior_training_window():
    start = datetime(2026, 1, 1, tzinfo=UTC)
    winner = [_row(start + timedelta(days=i), 2.0 if i < 3 else -0.5) for i in range(4)]
    loser = [_row(start + timedelta(days=i), -1.0) for i in range(4)]
    result = research.walk_forward(
        {"winner": winner, "loser": loser},
        [{"variant_id": "winner", "family": "earnings"}, {"variant_id": "loser", "family": "earnings"}],
        study_start=start, study_end=start + timedelta(days=8),
        cfg={"train_days": 4, "test_days": 2, "step_days": 2, "minimum_train_closed": 3,
             "minimum_train_pf": 1.0},
    )
    assert result[0]["selected_variant"] == "winner"
    assert result[0]["test"]["closed"] == 0


def test_insufficient_history_returns_without_touching_forbidden_tables(tmp_path):
    db = tmp_path / "research.sqlite"
    conn = sqlite3.connect(db)
    for table in ("proposed_signals", "signal_outcomes", "final_r", "paper_ledger", "live_routing"):
        conn.execute(f"CREATE TABLE {table}(value TEXT)")
        conn.execute(f"INSERT INTO {table} VALUES ('stable')")
    conn.commit()
    before = {table: conn.execute(f"SELECT * FROM {table}").fetchall()
              for table in ("proposed_signals", "signal_outcomes", "final_r", "paper_ledger", "live_routing")}
    conn.close()

    config = tmp_path / "research.yaml"
    config.write_text(
        "stocks_catalyst_research:\n"
        f"  history_root: {str(tmp_path / 'missing-history').replace('\\', '/')}\n"
        "  variants:\n    - variant_id: earnings_test\n      family: earnings_gap\n      overrides: {}\n",
        encoding="utf-8",
    )
    result = research.run(
        db=str(db), config_path=config, study_start="2026-01-01T00:00:00+00:00",
        study_end="2026-08-01T00:00:00+00:00", persist=True,
    )
    assert result["status"] == "INSUFFICIENT_HISTORY"
    conn = sqlite3.connect(db)
    for table, expected in before.items():
        assert conn.execute(f"SELECT * FROM {table}").fetchall() == expected
    assert conn.execute("SELECT name FROM sqlite_master WHERE name='stocks_research_backtest_runs'").fetchone() is None
    conn.close()


def test_research_run_persists_only_its_own_read_model_tables(tmp_path):
    db = tmp_path / "research.sqlite"
    conn = sqlite3.connect(db)
    conn.execute(
        "CREATE TABLE news_canonical_events (event_id TEXT, news_item_id INTEGER, asset_class TEXT, "
        "linkage_allowed INTEGER, effective_at TEXT, published_at TEXT, created_at TEXT, event_type TEXT, "
        "title TEXT, trusted_symbols_json TEXT, mentioned_symbols_json TEXT, source_quality TEXT)"
    )
    conn.execute("INSERT INTO news_canonical_events VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (
        "earnings-aapl", 1, "stocks", 1, "2026-07-14T13:00:00+00:00", "2026-07-14T13:00:00+00:00",
        "2026-07-14T13:01:00+00:00", "earnings", "AAPL reports earnings", '["AAPL"]', '["AAPL"]', "primary",
    ))
    for table in ("proposed_signals", "signal_outcomes", "final_r", "paper_ledger", "live_routing"):
        conn.execute(f"CREATE TABLE {table}(value TEXT)")
        conn.execute(f"INSERT INTO {table} VALUES ('stable')")
    conn.commit(); conn.close()

    history = tmp_path / "history" / "15m"
    history.mkdir(parents=True)
    pd.DataFrame([
        {"timestamp": "2026-01-01T14:30:00+00:00", "open": 100, "high": 101, "low": 99, "close": 100, "volume": 1},
        {"timestamp": "2026-07-14T14:30:00+00:00", "open": 100, "high": 101, "low": 99, "close": 100, "volume": 1},
    ]).to_csv(history / "SPY.csv", index=False)
    config = tmp_path / "research.yaml"
    config.write_text(
        "stocks_catalyst_research:\n"
        f"  history_root: {str(tmp_path / 'history').replace('\\', '/')}\n"
        "  minimum_history_days: 180\n"
        "  variants:\n"
        "    - variant_id: earnings_test\n"
        "      family: earnings_gap\n"
        "      overrides:\n"
        "        allowed_directional_event_types: [earnings]\n"
        "        excluded_event_types: []\n",
        encoding="utf-8",
    )
    result = research.run(
        db=str(db), config_path=config, study_start="2026-01-01T00:00:00+00:00",
        study_end="2026-08-01T00:00:00+00:00", persist=True,
    )
    assert result["status"] == "RESEARCH_ONLY"
    assert result["persisted"] is True
    conn = sqlite3.connect(db)
    assert conn.execute("SELECT count(*) FROM stocks_research_backtest_runs").fetchone()[0] == 1
    assert conn.execute("SELECT count(*) FROM stocks_research_backtest_results").fetchone()[0] == 1
    for table in ("proposed_signals", "signal_outcomes", "final_r", "paper_ledger", "live_routing"):
        assert conn.execute(f"SELECT * FROM {table}").fetchall() == [("stable",)]
    conn.close()


def test_load_history_falls_back_to_causal_parquet(tmp_path):
    root = tmp_path / "parquet"
    target = root / "SPY"
    target.mkdir(parents=True)
    pd.DataFrame([{
        "bar_open_at": "2026-01-02T14:30:00+00:00",
        "bar_close_at": "2026-01-02T14:45:00+00:00",
        "available_at": "2026-01-02T14:45:00.001000+00:00",
        "open": 100.0, "high": 101.0, "low": 99.0, "close": 100.5, "volume": 10,
    }]).to_parquet(target / "15m.parquet", index=False)

    frame = research.load_history({
        "history_root": str(tmp_path / "missing"),
        "parquet_roots": [str(root)],
    }, "SPY", "15m")

    assert len(frame) == 1
    assert frame.iloc[0]["timestamp"] == pd.Timestamp("2026-01-02T14:30:00+00:00")
