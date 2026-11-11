"""PARTS 2-7 — safe observability + DB hygiene tests.

Guardrails asserted: retention never loses the latest row per signal / final_r values / recent rows;
catalyst shadow audit + diagnostics never mutate scoring/actionability/threshold/final_r; digest
composes; no live.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

import src.maintenance.agent_runs_retention as arr
import src.maintenance.signal_outcomes_retention as ret


# ---------- PART 3: retention safety on a synthetic DB ----------
def _make_db(path: str) -> None:
    c = sqlite3.connect(path)
    c.execute("""CREATE TABLE signal_outcomes (id INTEGER PRIMARY KEY AUTOINCREMENT,
        signal_id TEXT, checked_at TEXT, final_r REAL, final_outcome TEXT)""")
    # 2 signals, 5 per-bar rows each: 4 old (>days) + 1 recent; old rows carry a copied final_outcome
    rows = []
    for sig in ("sig_a", "sig_b"):
        for i, ts in enumerate(["2026-01-01T00:00:00+00:00", "2026-01-02T00:00:00+00:00",
                                "2026-01-03T00:00:00+00:00", "2026-01-04T00:00:00+00:00"]):
            rows.append((sig, ts, 1.5, "tp1"))                       # old intermediate (carry final)
        rows.append((sig, "2099-01-01T00:00:00+00:00", 1.5, "tp1"))  # "recent" latest row
    c.executemany("INSERT INTO signal_outcomes (signal_id, checked_at, final_r, final_outcome) "
                  "VALUES (?,?,?,?)", rows)
    c.commit(); c.close()


def test_retention_dry_run_mutates_nothing(tmp_path: Path):
    db = str(tmp_path / "t.sqlite"); _make_db(db)
    before = sqlite3.connect(db).execute("SELECT COUNT(*) FROM signal_outcomes").fetchone()[0]
    r = ret.run(days=30, dry_run=True, db=db, now=None)
    after = sqlite3.connect(db).execute("SELECT COUNT(*) FROM signal_outcomes").fetchone()[0]
    assert r["dry_run"] is True and r["deleted_rows"] == 0 and before == after == 10


def test_retention_keeps_latest_per_signal_and_recent(tmp_path: Path):
    db = str(tmp_path / "t.sqlite"); _make_db(db)
    archdir = str(tmp_path / "arch")
    res = ret.run(days=30, archive=True, dry_run=False, db=db, archive_dir=archdir)
    conn = sqlite3.connect(db); conn.row_factory = sqlite3.Row
    # every signal still has its LATEST row (the 2099 one) → final_r preserved, never lost
    for sig in ("sig_a", "sig_b"):
        latest = conn.execute("SELECT MAX(checked_at) FROM signal_outcomes WHERE signal_id=?", (sig,)).fetchone()[0]
        assert latest == "2099-01-01T00:00:00+00:00"
        assert conn.execute("SELECT final_r FROM signal_outcomes WHERE signal_id=? ORDER BY checked_at DESC LIMIT 1",
                            (sig,)).fetchone()[0] == 1.5
    # the 4 old intermediate rows per signal were archived+deleted (8 total)
    assert res["deleted_rows"] == 8
    assert conn.execute("SELECT COUNT(*) FROM signal_outcomes").fetchone()[0] == 2
    assert Path(res["archive_file"]).exists()
    conn.close()


def test_retention_module_never_updates_final_r():
    src = Path(ret.__file__).read_text(encoding="utf-8").upper()
    assert "UPDATE" not in src                      # retention only DELETEs old rows, never rewrites
    assert "SET FINAL_R" not in src


# ---------- agent_runs.summary_json retention (the real 1.66GB hog) ----------
def _make_agent_runs_db(path: str) -> None:
    c = sqlite3.connect(path)
    c.execute("""CREATE TABLE agent_runs (id INTEGER PRIMARY KEY AUTOINCREMENT,
        agent_name TEXT, run_at TEXT, output_path TEXT, asset_class TEXT, summary_json TEXT)""")
    rows = [("a", "2026-01-01T00:00:00+00:00", "p1", "crypto", "{\"big\":\"OLD\"}"),
            ("b", "2026-01-02T00:00:00+00:00", "p2", "crypto", "{\"big\":\"OLD\"}"),
            ("c", "2099-01-01T00:00:00+00:00", "p3", "crypto", "{\"big\":\"RECENT\"}")]
    c.executemany("INSERT INTO agent_runs (agent_name, run_at, output_path, asset_class, summary_json) "
                  "VALUES (?,?,?,?,?)", rows)
    c.commit(); c.close()


def test_agent_runs_dry_run_mutates_nothing(tmp_path: Path):
    db = str(tmp_path / "ar.sqlite"); _make_agent_runs_db(db)
    r = arr.run(days=30, dry_run=True, db=db)
    n = sqlite3.connect(db).execute(
        "SELECT COUNT(*) FROM agent_runs WHERE summary_json IS NOT NULL").fetchone()[0]
    assert r["cleared_rows"] == 0 and n == 3


def test_agent_runs_clears_old_keeps_metadata_and_recent(tmp_path: Path):
    db = str(tmp_path / "ar.sqlite"); _make_agent_runs_db(db)
    res = arr.run(days=30, archive=True, dry_run=False, db=db, archive_dir=str(tmp_path / "arch"))
    conn = sqlite3.connect(db); conn.row_factory = sqlite3.Row
    # old blobs nulled, recent kept
    assert res["cleared_rows"] == 2
    assert conn.execute("SELECT COUNT(*) FROM agent_runs WHERE summary_json IS NOT NULL").fetchone()[0] == 1
    # metadata rows survive intact (all 3 rows + their output_path)
    assert conn.execute("SELECT COUNT(*) FROM agent_runs").fetchone()[0] == 3
    assert conn.execute("SELECT output_path FROM agent_runs WHERE agent_name='a'").fetchone()[0] == "p1"
    assert Path(res["archive_file"]).exists()
    conn.close()


def test_agent_runs_module_touches_no_trading_table():
    up = Path(arr.__file__).read_text(encoding="utf-8").upper()
    assert arr.TABLE == "agent_runs"
    # no SQL read/write against any trading table, and never rewrites final_r
    for bad in ("FROM PROPOSED_SIGNALS", "UPDATE PROPOSED_SIGNALS", "FROM SIGNAL_OUTCOMES",
                "UPDATE SIGNAL_OUTCOMES", "PAPER_SHADOW_EXECUTION_OUTCOMES", "PAPER_EXECUTION_OUTCOMES",
                "SET FINAL_R"):
        assert bad not in up, f"agent_runs retention must not contain SQL: {bad}"


# ---------- PART 4: catalyst shadow audit never changes scoring ----------
def test_catalyst_shadow_audit_no_scoring_change(tmp_path: Path):
    from src.signals import catalyst_linkage_shadow_audit as cat
    src = Path(cat.__file__).read_text(encoding="utf-8")
    up = src.upper()
    assert "UPDATE PROPOSED_SIGNALS" not in up                 # never flips news_supported
    assert "INSERT INTO SIGNAL_CATALYST_LABELS" not in up      # never writes the production label cache
    assert "UPDATE SIGNAL_CATALYST_LABELS" not in up
    # the only table it writes is the additive shadow table
    assert "INSERT INTO catalyst_shadow_audit" in src


# ---------- PART 5: A-tier diagnostic never mutates the threshold ----------
def test_a_tier_diagnostic_read_only():
    from src.diagnostics import a_tier_strictness as at
    src = Path(at.__file__).read_text(encoding="utf-8").upper()
    for verb in ("UPDATE ", "INSERT INTO", "DELETE FROM"):
        assert verb not in src
    assert at.A_TIER_THRESHOLD == 80.0


# ---------- PART 6: stocks readiness never changes actionability ----------
def test_stocks_readiness_read_only():
    from src.diagnostics import stocks_mode_readiness as sm
    src = Path(sm.__file__).read_text(encoding="utf-8").upper()
    for verb in ("UPDATE ", "INSERT INTO", "DELETE FROM"):
        assert verb not in src


# ---------- PART 2: digest composer ----------
def test_digest_compose_has_required_fields():
    from src.notifiers.paper_shadow_telegram import compose
    msg = compose()
    # lane may be empty in CI → either the empty marker or the full digest with the caveat
    assert "Paper-Shadow A/B" in msg
    if "FORWARD = valid evidence" in msg:
        assert "promotion gate" in msg and "NOT proof" in msg
