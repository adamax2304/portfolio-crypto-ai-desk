"""Old-paper-vs-new-logic-shadow underperformance diagnostic tests (audit item #3).

Covers: aggregation/attribution math (slice_stats, group_pairs), authoritative-fee_profile pairing
(never mixes crypto/stock cost models), exit-class classification, chase (NO_CHASE_SKIP)
attribution, global top-N tail merge/dedupe, and the read-only guardrail (no writes to
signal_outcomes / final_r / proposed_signals; no live/order surface; writes nothing to the DB).
"""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from src.execution import old_paper_underperformance_diagnostic as diag
from src.execution import paper_shadow_engine as pse
from src.execution.entry_mode_calibration import BRANCH_OLD, BRANCH_NEW, FORWARD, BACKFILL

ROOT = Path(__file__).resolve().parents[1]


# ============================ pure-function unit tests ============================

def test_exit_class_protective_vs_original_stop():
    assert diag._exit_class({"close_reason": "stop", "net_r": 0.5}) == "protective_stop"
    assert diag._exit_class({"close_reason": "stopped_full", "net_r": -1.0}) == "original_stop"
    assert diag._exit_class({"close_reason": "closed_win", "net_r": 2.0}) == "win"
    assert diag._exit_class({"close_reason": "expired_exit", "net_r": 0.3}) == "expired_win"
    assert diag._exit_class({"close_reason": "expired_no_fill", "net_r": None}) == "expired_flat"
    assert diag._exit_class({"close_reason": "skipped", "net_r": None}) == "no_entry"
    assert diag._exit_class({"close_reason": "something_else", "net_r": None}) == "other"


def _pair(sid, old_usd, new_usd, old_filled=True, new_filled=True, old_fee=1.0, new_fee=1.0,
         old_gross_r=None, new_gross_r=None, skipped_new=None):
    def leg(usd, filled, fee, gross_r):
        return {"net_pnl_usdt": usd if filled else None,
                "net_r": (usd / 25.0) if filled else None,
                "entry_fill_status": "filled" if filled else "missed",
                "fees_usdt": fee, "slippage_usdt": 0.0, "gross_r": gross_r,
                "close_reason": "closed_win" if (filled and usd > 0) else "stopped_full",
                "created_at": "2026-07-01T00:00:00+00:00", "entry_fill_time": "2026-07-01T00:05:00+00:00"}
    old = leg(old_usd, old_filled, old_fee, old_gross_r)
    new = leg(new_usd, new_filled, new_fee, new_gross_r)
    if skipped_new:
        new["skipped_shadow_reason"] = skipped_new
    return {"signal_id": sid, "old": old, "new": new}


def test_slice_stats_executed_vs_with_skips_split():
    pairs = [
        _pair("s1", old_usd=-10.0, new_usd=20.0),                       # both filled, new better
        _pair("s2", old_usd=15.0, new_usd=5.0),                         # both filled, old better
        _pair("s3", old_usd=-8.0, new_usd=0.0, new_filled=False),       # old lost, new skipped -> avoided_bad
        _pair("s4", old_usd=12.0, new_usd=0.0, new_filled=False),       # old won, new skipped -> missed_good
    ]
    s = diag.slice_stats(pairs)
    assert s["pairs_total"] == 4
    assert s["executed_common"] == 2                     # s1, s2 only
    assert s["new_better_count"] == 1 and s["old_better_count"] == 1
    assert s["executed_sum_delta_usd"] == (20.0 - -10.0) + (5.0 - 15.0)   # 30 + -10 = 20
    assert s["with_skips_common"] == 4
    assert s["avoided_bad_count"] == 1 and s["avoided_bad_usd"] == -8.0
    assert s["missed_good_count"] == 1 and s["missed_good_usd"] == 12.0
    # with_skips delta: (20-(-10)) + (5-15) + (0-(-8)) + (0-12) = 30 -10 +8 -12 = 16
    assert s["with_skips_sum_delta_usd"] == 16.0


def test_slice_stats_fee_and_gross_r_attribution():
    pairs = [
        _pair("s1", old_usd=-5.0, new_usd=5.0, old_fee=2.0, new_fee=0.5, old_gross_r=0.3, new_gross_r=0.3),
    ]
    s = diag.slice_stats(pairs)
    assert s["old_avg_fee_usd"] == 2.0 and s["new_avg_fee_usd"] == 0.5
    assert s["fee_delta_usd"] == 1.5          # old paid 1.5 more in fees+slippage than new
    assert s["old_gross_r_sum"] == 0.3
    # old net R is negative (-5/25=-0.2) while gross R is positive (0.3) -> costs ate a real edge
    assert s["old_net_r_sum"] < 0 < s["old_gross_r_sum"]


def test_group_pairs_buckets_by_key():
    pairs = [_pair("s1", -1, 1), _pair("s2", -1, 1), _pair("s3", 5, -5)]
    keyed = {"s1": "A", "s2": "A", "s3": "B"}
    buckets = diag.group_pairs(pairs, lambda p: keyed[p["signal_id"]])
    assert set(buckets.keys()) == {"A", "B"}
    assert buckets["A"]["executed_common"] == 2
    assert buckets["B"]["executed_common"] == 1


def test_chase_avoided_stats_isolates_no_chase_skip_only():
    pairs = [
        _pair("s1", old_usd=-20.0, new_usd=0.0, new_filled=False, skipped_new="no_chase_skip"),   # chase, old lost
        _pair("s2", old_usd=10.0, new_usd=0.0, new_filled=False, skipped_new="no_chase_skip"),     # chase, old won
        _pair("s3", old_usd=-30.0, new_usd=0.0, new_filled=False, skipped_new="entry_mode_disabled_by_policy"),
    ]
    ch = diag.chase_avoided_stats(pairs)
    assert ch["chase_pairs_total"] == 2                 # s3 excluded (different skip reason)
    assert ch["old_losses_avoided_n"] == 1 and ch["old_losses_avoided_usd"] == -20.0
    assert ch["old_wins_also_missed_n"] == 1 and ch["old_wins_also_missed_usd"] == 10.0


def test_global_tails_dedupe_keeps_most_extreme_and_sorts():
    persisted = [
        {"asset_class": "crypto", "mode": "scalp", "window": FORWARD,
         "tails_json": json.dumps({"worse_tail": [{"signal_id": "a", "delta_usd": -10, "delta_r": -0.4},
                                                   {"signal_id": "b", "delta_usd": -5, "delta_r": -0.2}],
                                    "better_tail": [{"signal_id": "c", "delta_usd": 8, "delta_r": 0.3}]})},
        {"asset_class": "crypto", "mode": "intraday", "window": FORWARD,
         "tails_json": json.dumps({"worse_tail": [{"signal_id": "a", "delta_usd": -50, "delta_r": -2.0}],
                                    "better_tail": [{"signal_id": "c", "delta_usd": 3, "delta_r": 0.1}]})},
    ]
    tails = diag.global_tails(persisted, n=10)
    worst_by_sid = {e["signal_id"]: e for e in tails["worst"]}
    assert worst_by_sid["a"]["delta_usd"] == -50           # kept the MORE extreme (min) of the two dupes
    assert tails["worst"][0]["signal_id"] == "a"           # sorted ascending (worst first)
    best_by_sid = {e["signal_id"]: e for e in tails["best"]}
    assert best_by_sid["c"]["delta_usd"] == 8              # kept the MORE extreme (max) of the two dupes


# ============================ seeded-DB integration tests ============================

def _seed(path: str):
    conn = sqlite3.connect(path)
    conn.execute("CREATE TABLE proposed_signals (signal_id TEXT PRIMARY KEY, mode TEXT, "
                "market_regime TEXT, tier TEXT, created_at TEXT)")
    conn.execute("CREATE TABLE signal_outcomes (signal_id TEXT, final_r REAL)")
    pse.ensure_tables(conn)

    def insert_signal(sid, mode="intraday"):
        conn.execute("INSERT INTO proposed_signals VALUES (?,?,?,?,?)",
                     (sid, mode, "bull", "A", "2026-06-30T00:00:00+00:00"))

    def insert_shadow(sid, branch, *, asset_class="crypto", fee_profile="bybit_non_vip_usdt_perp",
                      entry_mode="PULLBACK_LIMIT", entry_fill_status="filled", net_pnl_usdt=0.0,
                      net_r=0.0, close_reason="stopped_full", window=FORWARD, skipped_shadow_reason=None):
        conn.execute(
            "INSERT INTO paper_shadow_execution_outcomes "
            "(signal_id, branch, fee_profile, symbol, asset_class, entry_mode, entry_fill_status, "
            " entry_fill_time, entry_late_status, missed_entry_reason, skipped_shadow_reason, "
            " close_reason, outcome_status, net_pnl_usdt, net_r, gross_r, fees_usdt, slippage_usdt, "
            " mfe_r, window, created_at, cost_model_status) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (sid, branch, fee_profile, "BTCUSDT", asset_class, entry_mode, entry_fill_status,
             "2026-07-01T00:05:00+00:00", "ok", None, skipped_shadow_reason, close_reason, "closed",
             net_pnl_usdt, net_r, net_r, 1.0, 0.1, 0.2, window, "2026-07-01T00:00:00+00:00", "current"))

    insert_signal("s1"); insert_shadow("s1", BRANCH_OLD, net_pnl_usdt=-10.0, net_r=-0.4)
    insert_shadow("s1", BRANCH_NEW, net_pnl_usdt=15.0, net_r=0.6, close_reason="closed_win")

    insert_signal("s2"); insert_shadow("s2", BRANCH_OLD, net_pnl_usdt=20.0, net_r=0.8, close_reason="closed_win")
    insert_shadow("s2", BRANCH_NEW, net_pnl_usdt=5.0, net_r=0.2, close_reason="closed_win")

    # non-authoritative fee_profile row for s1/old -- must be ignored by pairing
    insert_shadow("s1", BRANCH_OLD, fee_profile="stock_etf_default", net_pnl_usdt=999.0, net_r=99.0)

    conn.commit(); conn.close()


def test_diagnose_unavailable_when_shadow_table_missing(tmp_path):
    p = str(tmp_path / "empty.sqlite")
    sqlite3.connect(p).close()
    res = diag.diagnose(db=p, refresh_source=False)
    assert res["available"] is False


def test_diagnose_end_to_end_uses_authoritative_fee_profile_only(tmp_path):
    p = str(tmp_path / "diag.sqlite")
    _seed(p)
    res = diag.diagnose(db=p, refresh_source=False)
    assert res["available"] is True
    assert res["pairs_total"] == 2   # s1, s2 -- the non-authoritative s1/old row must not create a 3rd pair
    ov = res["overall_all_windows"]
    assert ov["executed_common"] == 2
    # s1: new(15) - old(-10) = 25; s2: new(5) - old(20) = -15 -> sum = 10
    assert ov["executed_sum_delta_usd"] == 10.0


def test_diagnose_excludes_after_expiry_blocked_rows_from_executed_common(tmp_path):
    """Regression for the expiry-aware fix (audit item #3 follow-up): a row paper_shadow_engine
    correctly refuses to mark 'filled' (entry_fill_status='missed', entry_late_status=
    'after_expiry_blocked') must NOT be counted in executed_common / PnL, even though a pair partner
    on the other branch IS genuinely filled."""
    p = str(tmp_path / "diag_expiry.sqlite")
    conn = sqlite3.connect(p)
    conn.execute("CREATE TABLE proposed_signals (signal_id TEXT PRIMARY KEY, mode TEXT, "
                "market_regime TEXT, tier TEXT, created_at TEXT)")
    conn.execute("CREATE TABLE signal_outcomes (signal_id TEXT, final_r REAL)")
    pse.ensure_tables(conn)
    conn.execute("INSERT INTO proposed_signals VALUES ('s1','intraday','bull','A','2026-06-30T00:00:00+00:00')")

    def insert(branch, entry_fill_status, entry_late_status, net_pnl_usdt, net_r):
        conn.execute(
            "INSERT INTO paper_shadow_execution_outcomes "
            "(signal_id, branch, fee_profile, symbol, asset_class, entry_mode, entry_fill_status, "
            " entry_fill_time, entry_late_status, missed_entry_reason, skipped_shadow_reason, "
            " close_reason, outcome_status, net_pnl_usdt, net_r, gross_r, fees_usdt, slippage_usdt, "
            " mfe_r, window, created_at, cost_model_status) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            ("s1", branch, "bybit_non_vip_usdt_perp", "BTCUSDT", "crypto", "PULLBACK_LIMIT",
             entry_fill_status, "2026-07-01T00:05:00+00:00" if entry_fill_status == "filled" else None,
             entry_late_status, None if entry_fill_status == "filled" else "expired_no_fill", None,
             "closed_win" if entry_fill_status == "filled" else "no_entry",
             "closed" if entry_fill_status == "filled" else "no_entry",
             net_pnl_usdt, net_r, net_r, 1.0 if entry_fill_status == "filled" else 0.0,
             0.1 if entry_fill_status == "filled" else 0.0, 0.2, FORWARD,
             "2026-07-01T00:00:00+00:00", "current"))

    insert(BRANCH_OLD, "filled", "ok", 50.0, 2.0)                        # old genuinely filled and won
    insert(BRANCH_NEW, "missed", "after_expiry_blocked", 0.0, 0.0)       # new correctly blocked
    conn.commit(); conn.close()

    res = diag.diagnose(db=p, refresh_source=False)
    assert res["pairs_total"] == 1
    ov = res["overall_all_windows"]
    assert ov["executed_common"] == 0          # blocked row must NOT count as executed
    assert ov["with_skips_common"] == 1        # still visible in the with-skips view (as $0 for new)
    assert ov["with_skips_sum_delta_usd"] == -50.0   # 0 (new, blocked) - 50 (old, filled)


def test_diagnose_never_writes_signal_outcomes_or_final_r(tmp_path):
    p = str(tmp_path / "diag.sqlite")
    _seed(p)
    conn = sqlite3.connect(p)
    conn.execute("INSERT INTO signal_outcomes VALUES ('s1', 0.5)")
    conn.commit()
    before_tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    before_so = conn.execute("SELECT signal_id, final_r FROM signal_outcomes").fetchall()
    conn.close()

    diag.diagnose(db=p, refresh_source=False)

    conn = sqlite3.connect(p)
    after_tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    after_so = conn.execute("SELECT signal_id, final_r FROM signal_outcomes").fetchall()
    conn.close()
    assert before_so == after_so                 # final_r untouched
    assert after_tables == before_tables          # this module creates/writes NO tables at all


def test_render_markdown_and_write_report(tmp_path):
    p = str(tmp_path / "diag.sqlite")
    _seed(p)
    res = diag.diagnose(db=p, refresh_source=False)
    md = diag.render_markdown(res)
    assert "Underperformance Diagnostic" in md
    assert "Evidence quality" in md
    out_path = tmp_path / "OUT.md"
    written = diag.write_report(res, path=str(out_path))
    assert Path(written).exists()
    assert "Underperformance Diagnostic" in Path(written).read_text(encoding="utf-8")


# ============================ guardrails ============================

def test_diagnostic_module_has_no_live_order_surface():
    import src.execution.old_paper_underperformance_diagnostic as m
    src = Path(m.__file__).read_text(encoding="utf-8").lower()
    for bad in ("create_order", "place_order", "submit_order", "auto_live", "manual_live",
                "update proposed_signals", "update signal_outcomes", "insert into signal_outcomes",
                "final_r ="):
        assert bad not in src, f"found forbidden pattern: {bad}"
