"""Move 2 — sequential (SPRT) promotion gate. Pure-math correctness + guardrails.

Read-model / evaluation-only: SEQ_ACCEPT never promotes, module never writes a live table.
"""
from __future__ import annotations

from pathlib import Path

from src.execution import sequential_gate as sg

_P = dict(alpha=0.05, beta=0.20, min_edge_r=0.10, min_n_accept=20, min_n_reject=10)


def test_sprt_accepts_a_clear_positive_edge():
    # strong, low-variance positive edge → should ACCEPT once past min_n_accept
    diffs = [0.5] * 25
    r = sg.sprt(diffs, **_P)
    assert r["decision"] == "SEQ_ACCEPT" and r["n"] == 25 and r["mean"] > 0


def test_sprt_rejects_a_clear_negative_edge():
    diffs = [-0.5] * 25
    r = sg.sprt(diffs, **_P)
    assert r["decision"] == "SEQ_REJECT"


def test_sprt_continues_when_ambiguous():
    # mean edge ~halfway between H0 (0) and H1 (0.10R) with real spread → LLR sits between the
    # boundaries, so neither hypothesis is favored yet → keep accumulating.
    diffs = [0.6, -0.5] * 6                 # n=12, mean=0.05, Σ=0.6 = n·min_edge_r/2 → LLR≈0
    r = sg.sprt(diffs, **_P)
    assert r["decision"] == "SEQ_CONTINUE", (r["llr"], r["lower"], r["upper"])


def test_accept_blocked_below_min_n_even_if_llr_crosses():
    # same strong edge but too few observations → guard forces CONTINUE, not ACCEPT
    diffs = [0.5] * 5
    r = sg.sprt(diffs, **_P)
    assert r["decision"] == "SEQ_CONTINUE" and r["n"] < _P["min_n_accept"]


def test_reject_blocked_below_min_n_reject():
    diffs = [-0.5] * 3                       # clearly negative but n < min_n_reject
    r = sg.sprt(diffs, **_P)
    assert r["decision"] == "SEQ_CONTINUE"


def test_boundaries_have_expected_sign():
    r = sg.sprt([0.1, 0.1], **_P)
    assert r["upper"] > 0 and r["lower"] < 0   # Wald A>0>B


def test_sprt_handles_tiny_n():
    assert sg.sprt([], **_P)["decision"] == "SEQ_CONTINUE"
    assert sg.sprt([0.3], **_P)["decision"] == "SEQ_CONTINUE"


def test_zero_variance_positive_constant_accepts_past_min_n():
    r = sg.sprt([0.2] * 22, **_P)              # constant edge above min_edge_r, sigma == 0 path
    assert r["sigma"] == 0.0 and r["decision"] == "SEQ_ACCEPT"


def test_wide_pairing_counts_new_logic_skips_as_avoided_trades(tmp_path):
    # wide lane: old fills 4 losers; new SKIPS 3 of them (books 0R = avoided) and FILLS 1.
    # with-avoided edge must yield 4 decisions (the 3 skips + 1 fill), not just the 1 executed pair.
    import sqlite3
    db = tmp_path / "t.sqlite"
    c = sqlite3.connect(db)
    c.execute("""CREATE TABLE paper_shadow_wide_outcomes (
        generated_at TEXT, lane TEXT, signal_id TEXT, branch TEXT, symbol TEXT, asset_class TEXT,
        mode TEXT, entry_mode TEXT, window TEXT, entry_fill_status TEXT, entry_fill_time TEXT,
        net_r REAL, net_pnl_usdt REAL)""")
    rows = []
    for i in range(4):
        rows.append(("g", "w", f"s{i}", "old_paper", "X", "crypto", "scalp", "PL", "forward_since_activation",
                     "filled", f"2026-01-0{i+1}", -1.0, -25.0))            # old loses -1R each
    for i in range(3):
        rows.append(("g", "w", f"s{i}", "new_logic_shadow", "X", "crypto", "scalp", "NO_CHASE_SKIP",
                     "forward_since_activation", "skipped", None, None, None))  # new avoids
    rows.append(("g", "w", "s3", "new_logic_shadow", "X", "crypto", "scalp", "PL",
                 "forward_since_activation", "filled", "2026-01-04", 0.5, 12.5))  # new takes, +0.5R
    c.executemany("INSERT INTO paper_shadow_wide_outcomes VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", rows)
    c.commit(); c.close()
    groups = sg._paired_diffs_by_mode(str(db), source="wide")
    decisions = groups[("crypto", "scalp")]
    assert len(decisions) == 4                                # 3 avoided + 1 executed, not just 1
    # 3 avoided vs old -1R → d=+1.0 each; 1 executed +0.5 vs -1 → d=+1.5
    ds = sorted(round(d["d_r"], 3) for d in decisions)
    assert ds == [1.0, 1.0, 1.0, 1.5]


def test_module_is_read_model_only():
    src = Path(sg.__file__).read_text(encoding="utf-8").lower()
    for bad in ("create_order", "place_order", "auto_live", "manual_live", "final_r =",
                "update proposed_signals", "insert into proposed_signals",
                "update signal_outcomes", "insert into signal_outcomes"):
        assert bad not in src, bad
    # the ONLY table it writes is the read-model gate table (via an f-string on {table})
    assert "insert or replace into {table}" in src and "sequential_promotion_gate" in src
