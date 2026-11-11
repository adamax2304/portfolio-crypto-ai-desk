"""Move 4 — backtest↔forward reconciliation verdict logic + read-only guardrails."""
from __future__ import annotations

from pathlib import Path

from src.execution import backtest_forward_reconciliation as rec


def test_tracks_when_close_and_sign_agree():
    assert rec._verdict(n=40, mean_abs_div=0.10, sign_agree=0.90) == "TRACKS"


def test_diverges_when_far_apart():
    assert rec._verdict(n=40, mean_abs_div=1.20, sign_agree=0.40) == "DIVERGES"


def test_partial_middle_ground():
    assert rec._verdict(n=40, mean_abs_div=0.50, sign_agree=0.60) == "PARTIAL"


def test_need_more_data_below_min_n():
    assert rec._verdict(n=5, mean_abs_div=0.01, sign_agree=1.0) == "NEED_MORE_DATA"


def test_close_divergence_but_low_sign_agreement_is_not_tracks():
    # magnitudes agree but the win/loss SIGN often flips → not trustworthy → PARTIAL/DIVERGES, not TRACKS
    assert rec._verdict(n=40, mean_abs_div=0.20, sign_agree=0.50) != "TRACKS"


def test_end_to_end_on_temp_db(tmp_path):
    import sqlite3
    db = tmp_path / "t.sqlite"
    c = sqlite3.connect(db)
    c.execute("""CREATE TABLE paper_shadow_execution_outcomes (
        signal_id TEXT, branch TEXT, net_r REAL, entry_fill_status TEXT, window TEXT)""")
    c.execute("""CREATE TABLE paper_shadow_wide_outcomes (
        signal_id TEXT, branch TEXT, net_r REAL, asset_class TEXT, mode TEXT, entry_fill_status TEXT)""")
    for i in range(25):
        r = 0.5 if i % 2 else -0.5
        c.execute("INSERT INTO paper_shadow_execution_outcomes VALUES (?,?,?,?,?)",
                  (f"s{i}", "new_logic_shadow", r, "filled", "forward_since_activation"))
        c.execute("INSERT INTO paper_shadow_wide_outcomes VALUES (?,?,?,?,?,?)",
                  (f"s{i}", "new_logic_shadow", r + 0.05, "crypto", "scalp", "filled"))  # tiny, same sign
    c.commit(); c.close()
    res = rec.refresh(db=str(db), persist=True, write_report_file=False)
    row = next(m for m in res["modes"] if m["mode"] == "scalp")
    assert row["n"] == 25 and row["verdict"] == "TRACKS" and row["sign_agreement"] == 1.0
    assert res["matches_persisted_table"] is True


def test_module_is_read_model_only():
    src = Path(rec.__file__).read_text(encoding="utf-8").lower()
    for bad in ("create_order", "place_order", "auto_live", "manual_live", "final_r =",
                "update proposed_signals", "insert into proposed_signals",
                "update signal_outcomes", "insert into signal_outcomes",
                "insert into paper_shadow_execution_outcomes"):
        assert bad not in src, bad
