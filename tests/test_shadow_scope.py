"""Shadow-testing scope: exclude stocks intraday; new_logic_only for stocks swing/invest.

PAPER/SHADOW read-model only — verifies the engine simulates the right branches and prunes
out-of-scope rows, without touching live / proposed_signals / final_r.
"""
from __future__ import annotations

import sqlite3

from src.execution import paper_shadow_engine as pse


def test_config_scope_loaded():
    excl, nlo = pse._load_shadow_scope()
    assert ("stocks", "intraday") in excl                 # dropped entirely (already live in paper)
    assert ("stocks", "swing") in nlo and ("stocks", "invest") in nlo   # new-logic-only


def test_branches_new_logic_only_drops_old_paper():
    _, nlo = pse._load_shadow_scope()
    assert pse._branches_for("stocks", "swing", nlo) == ("new_logic_shadow",)
    assert pse._branches_for("stocks", "invest", nlo) == ("new_logic_shadow",)


def test_branches_default_keeps_both_for_crypto():
    _, nlo = pse._load_shadow_scope()
    assert pse._branches_for("crypto", "swing", nlo) == ("old_paper", "new_logic_shadow")
    assert pse._branches_for("crypto", "intraday", nlo) == ("old_paper", "new_logic_shadow")
    assert pse._branches_for("crypto", "scalp", nlo) == ("old_paper", "new_logic_shadow")


def _seed(db):
    c = sqlite3.connect(db)
    c.execute("CREATE TABLE proposed_signals (signal_id TEXT, asset_class TEXT, mode TEXT)")
    c.execute("CREATE TABLE paper_shadow_execution_outcomes (signal_id TEXT, branch TEXT)")
    rows_ps = [
        ("st_intra", "stocks", "intraday"), ("st_swing", "stocks", "swing"),
        ("st_inv", "stocks", "invest"), ("cr_swing", "crypto", "swing"),
    ]
    c.executemany("INSERT INTO proposed_signals VALUES (?,?,?)", rows_ps)
    for sid, *_ in rows_ps:
        for br in ("old_paper", "new_logic_shadow"):
            c.execute("INSERT INTO paper_shadow_execution_outcomes VALUES (?,?)", (sid, br))
    c.commit()
    return c


def test_prune_removes_excluded_and_new_logic_old_paper(tmp_path):
    db = tmp_path / "t.sqlite"
    c = _seed(str(db))
    removed = pse.prune_shadow_scope(c)
    # stocks intraday: BOTH branches gone (2 rows); stocks swing+invest: only old_paper gone (2 rows)
    assert removed["excluded_rows"] == 2 and removed["old_paper_rows"] == 2
    remaining = dict.fromkeys([])
    rows = c.execute("SELECT signal_id, branch FROM paper_shadow_execution_outcomes ORDER BY signal_id, branch").fetchall()
    got = {(r[0], r[1]) for r in rows}
    assert ("st_intra", "old_paper") not in got and ("st_intra", "new_logic_shadow") not in got
    assert ("st_swing", "old_paper") not in got and ("st_swing", "new_logic_shadow") in got
    assert ("st_inv", "new_logic_shadow") in got
    assert ("cr_swing", "old_paper") in got and ("cr_swing", "new_logic_shadow") in got   # crypto untouched
    c.close()


def test_prune_never_writes_live_tables():
    import pathlib
    src = pathlib.Path(pse.__file__).read_text(encoding="utf-8").lower()
    # prune only deletes from the shadow outcomes table; never writes proposed_signals/final_r
    assert "delete from paper_shadow_execution_outcomes where signal_id in" in src
    for bad in ("update proposed_signals", "insert into proposed_signals", "final_r ="):
        assert bad not in src, bad
